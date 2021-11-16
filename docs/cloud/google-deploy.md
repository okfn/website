# OKF Website in the cloud

## Staging

We use Google Cloud (`oki-website-staging` project) to run the staging version for the OKFN website in the `europe-north1` region.  

### Database 

We have a [SQL service](https://console.cloud.google.com/sql/instances?referrer=search&project=melodic-keyword-303819) running for the required PostgreSQL instance.  

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
gcloud sql import sql oki-website-staging gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql --database=website
```

Finally, drop the dump file:
```
gsutil rm gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql
```

### Django app

We use Google Cloud Run to run a service based on the `Dockerfile` in this repo. To deploy a new version, you only need to push to the `develop` branch (see [triggers](https://console.cloud.google.com/cloud-build/triggers?project=melodic-keyword-303819)).  

The secrets are defined in [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=melodic-keyword-303819) and this project will automatically use them when available. For local custom settings, add a local `.env` file.  

We use Cloud Run [Domain mapping](https://console.cloud.google.com/run/domains?project=melodic-keyword-303819)
to redirect the domain [stg.okfn.org](https://stg.okfn.org) to this application. 
Finally, we add a CNAME record to point this new domain (ensure remove the proxy and set the record a _DNS only_ at Cloudflare).  

**Notes: The staging environment is using the `min-instances` setting as 0. So if no one is using it, the first request might give you a 502 error until the service starts.**

#### Static files

We create a
[public bucket in Google Cloud Storage](https://console.cloud.google.com/storage/browser?project=melodic-keyword-303819)
called `django-statics-okf-website-staging` (must be unique globally).  
All S3 files transfered to Google Cloud Storage. You can do it with the
[Data Transfer tool](https://console.cloud.google.com/transfer/cloud/jobs?cloudshell=true&project=melodic-keyword-303819)
or with the command:

```
gsutil cp -R s3://okfn-org-staging gs://django-statics-okf-website-staging
# or -m for parallel
gsutil -m cp -R s3://okfn-org-staging gs://django-statics-okf-website-staging
```

This website uses `media` files from an external bucket but use django `statics` from a local folder.  
We are using `nginx` here just because this static files.  

### Redis

Google bring us [Redis through the _Memorystore_ service](https://console.cloud.google.com/memorystore/redis/instances?project=melodic-keyword-303819),
this [requires](https://medium.com/google-cloud/using-memorystore-with-cloud-run-82e3d61df016)
a [VPC connector](https://console.cloud.google.com/networking/connectors/list?project=melodic-keyword-303819)
to be visible from Cloud Run.  

Note that you'll need a secret pointing to the Redis instance
Example:
```
CACHE_URL=redis://10.23.81.3:6379/0
```

### Elasticsearch

Google allow using Elastic through a special service
[manged by Elastic](https://cloud.elastic.co/deployments/d1bdd16cf365403fa92fdd7320a4d527)
(external provider).  
Note that `python manage.py update_index` runs every time we build the DockerFile.  
You'll need a secret pointing to the Redis instance:

```
SEARCH_URL=https://USER:PASSWORD@okf-elastic-XX.com:92XX
```

To see/manage Elastic indexes go [here](https://okf-elastic-stg-website.kb.europe-north1.gcp.elastic-cloud.com:9243/app/management/data/index_management/indices) (it's very difficult to find).  
