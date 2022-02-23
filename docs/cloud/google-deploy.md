# OKF Website in the cloud

We are using Google Cloud Platform for our infrastructure.

## Environments

Available environments:
 - Staging: `oki-website-staging` project in the `europe-north1` region. 
 - Production: `oki-website-production` project in the `us-central1` region.  

Changes at `develop` branch trigger a deploy to `staging` environment.  
Changes at `main` branch trigger a deploy to `production` environment.  
`master` branch remains with the lastest version of the old infrastructure.

### Database 

We have a SQL service 
([staging](https://console.cloud.google.com/sql/instances?project=melodic-keyword-303819) - 
 [prod](https://console.cloud.google.com/sql/instances/?project=oki-website-production))
running for the required PostgreSQL instances.  


This DB was started using a production copy:
```
# https://cloud.google.com/sdk/gcloud/reference/sql/export/sql
gcloud sql export sql oki-cloud-sql gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql --database=okfn
```

And then, import this dump to the new SQL instance
You must delete previous database and then create a new one

```
gcloud sql databases delete website --instance=oki-website-staging
gcloud sql databases create website --instance=oki-website-staging
# https://cloud.google.com/sdk/gcloud/reference/sql/import/sql
# Note: the service account in the SQL instance must be added to the bucket permissions
gcloud sql import sql oki-website-staging gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql --database=website
```

Finally, drop the dump file:
```
gsutil rm gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql
```

Create a DB user

```
gcloud sql users create okfn --instance=oki-website-production --password=xxx
# "okfn" is the user name and "oki-website-production" is the instance name
```

To the secrets file
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=website
DB_USER=okfn
DB_PASSWORD=XXXXX
# example, the //cloudsql prefix is important
DB_HOST=//cloudsql/oki-website-production:us-central1:oki-website-production
DB_PORT=5432
```

#### Static files

Django requires a `media` and a `static` folder. `media` is for uploaded files, `static` is for static files (JS and CSS mainly).  
We create a public bucket in Google Cloud Storage
([staging](https://console.cloud.google.com/storage/browser?project=melodic-keyword-303819) - 
 [production](https://console.cloud.google.com/storage/browser?project=oki-website-production))
called `django-statics-okf-website-ENV` (must be unique globally) for the `media` files.  
All S3 files were transfered to Google Cloud Storage. You can do it with the
[Data Transfer tool](https://console.cloud.google.com/transfer/cloud/jobs?cloudshell=true&project=melodic-keyword-303819)
or with the command:

```
gsutil cp -R s3://okfn-org-staging gs://django-statics-okf-website-staging
# or -m for parallel
gsutil -m cp -R s3://okfn-org-staging gs://django-statics-okf-website-staging
```

Django `static` files lives in a local folder (it would be better to move them
 to Google Cloud Storage) and we serve them with `nginx`. 

### Redis

Google bring us Redis through the _Memorystore_ service. We are not using this service now.  
To activate it: Create an [instance](https://console.cloud.google.com/memorystore/redis/instances?project=oki-website-production)
This [requires](https://medium.com/google-cloud/using-memorystore-with-cloud-run-82e3d61df016)
a [VPC connector](https://console.cloud.google.com/networking/connectors/list?project=oki-website-production) 
to be visible from Cloud Run.  

Note that you'll need a secret pointing to the Redis instance
Example:
```
CACHE_URL=redis://10.23.81.3:6379/0
```

### Search engine

We are using [Django Haystack](https://django-haystack.readthedocs.io/en/master/) 
to set up the application search engine (you can pick different technologies).  

Google Cloud allows you to use Elasticsearch through a special service manged by Elastic.  
We are not using this service anymore, to use it, you will need to create an instance 
and set up the `SEARCH_URL=https://USER:PASSWORD@okf-elastic-XX.com:92XX`.  

We are now using a simpler Haystack solution:  
[Whoos](https://django-haystack.readthedocs.io/en/v2.3.2/tutorial.html#whoosh) (just 
removing the `SEARCH_URL` config value from _Google secrets_).  

Note that `python manage.py update_index` runs every time we build the DockerFile.  


### Django app

We use Google Cloud Run to run a service based on the `Dockerfile` in this repo.
To deploy a new version, you only need to push to the `develop` or `main` branch
(see triggers
([staging]((https://console.cloud.google.com/cloud-build/triggers?project=melodic-keyword-303819)) - 
 [prod](https://console.cloud.google.com/cloud-build/triggers?project=oki-website-production)).

The secrets are defined in Google Secret Manager
([staging](https://console.cloud.google.com/security/secret-manager?project=melodic-keyword-303819) -
 [prod](https://console.cloud.google.com/security/secret-manager?project=oki-website-production)
You'll need to edit Cloud Run _Variable & settings_ to mount them as a file at /secrets/django_settings.  

Google Secrets are required to connect this application with external services like Redis, Elasticsearch, etc.

Cloud Run extra tasks:
 - Google does not allow to update secrets directly, so you need to _View secret value_ (from action menu)
then copy them, update manually and finally deploy a new secrets version (for local custom settings, 
just add a local `.env` file.)
 - Remember using the VPC connerctor in the Cloud Run _Connection_ settings.
 - Add _Cluster SQL Connection_ to _Connection_ setting in the Cloud Run service. 
   - Or with gclod: `gcloud run services update website4 --add-cloudsql-instances=oki-website-production:us-central1:oki-website-production`

We use Cloud Run Domain mapping
([staging](https://console.cloud.google.com/run/domains?project=melodic-keyword-303819) - 
 [prod](https://console.cloud.google.com/run/domains?project=oki-website-production)
to redirect the domains okfn.org and next.okfn.org to this application. 
Finally, we add a CNAME record pointing to ghs.googlehosted.com (ensure to remove the proxy and set the record a _DNS only_ at Cloudflare ).  

**Notes: The staging environment is using the `min-instances` setting as 0. So if no one is using it, the first request might give you a 502 error until the service starts.**

Final production DNS change notes:
 - okfn.org main CNAME record from from okfn-production.openknowledge.io (proxied) to ghs.googlehosted.com (DNS only).
 - www CNAME record from k8s-production.openknowledge.io (proxied) to ghs.googlehosted.com (DNS only).

## Alerts

We defined Google [alert policies](https://console.cloud.google.com/monitoring/alerting/policies?project=oki-website-production)
to be sent to the #infra-alerts Slack Channel.
