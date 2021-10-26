# OKF Website in the cloud

## Staging

We use Google Cloud (`oki-website-staging` project) to run this staging version for the OKFN website in the `europe-north1` region.  

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

Update secrets to point the new database.  

Finally, drop the dump file:
```
gsutil rm gs://oki-cloud-sql-snapshots/okfn-prod-dump-20211026.sql
```

### Django app

We use Google Cloud Run to run a service based on the `Dockerfile` in this repo. To deploy a new version, you only need to push to the `develop` branch (see [triggers](https://console.cloud.google.com/cloud-build/triggers?project=melodic-keyword-303819)).  

The secrets are defined in [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=melodic-keyword-303819) and this project Django settings automatically use them when available. For local custom settings, add a local `.env` file.  

We use Cloud Run [Domain mapping](https://console.cloud.google.com/run/domains?project=melodic-keyword-303819)
to redirect the domain [stg.okfn.org](https://stg.okfn.org) to this application. Finally, we add a CNAME record to point this new domain (ensure remove the proxy and set the record a _DNS only_).  

_Notes: The staging environment is using the `min-instances` setting as 0. So if no one is using it, the first request might give you a 502 error until the service starts._
