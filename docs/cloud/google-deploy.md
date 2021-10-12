# OKF Website in the cloud

## Staging

We use Google Cloud (`oki-website-staging` project) to run this staging version for the OKFN website in the `europe-north1` region.  

### Database 

We have a [SQL service](https://console.cloud.google.com/sql/instances?referrer=search&project=melodic-keyword-303819) running for the required PostgreSQL instance.  

### Django app

We use Google Cloud Run to run a service based on the `Dockerfile` in this repo. To deploy a new version, you only need to push to the `develop` branch (see [triggers](https://console.cloud.google.com/cloud-build/triggers?project=melodic-keyword-303819)).  

The secrets are defined in [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=melodic-keyword-303819) and this project Django settings automatically use them when available. For local custom settings, add a local `.env` file.  

We use Cloud Run [Domain mapping](https://console.cloud.google.com/run/domains?project=melodic-keyword-303819)
to redirect the domain [stg.okfn.org](https://stg.okfn.org) to this application. Finally, we add a CNAME record to point this new domain (ensure remove the proxy and set the record a _DNS only_).  
