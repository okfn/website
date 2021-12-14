# Commands used during migration

ENV="$1"

OLD_PROD_BUCKET=oki-cloud-sql-snapshots

if [ "$ENV" == "prod"]; then

DB_INSTANCE=oki-website-production
DJANGO_MEDIA_BUCKET=django-statics-okf-website-production
PROJECT_NAME=oki-website-production
PROJECT_NUMBER=247414672907
PROJECT_ID=oki-website-production
S3_BUCKET=okfn-org-production
REDIS_INSTANC_ID=okf-production-redis
VPC_ID=vpc-prod-redis-crun
ELASTIC_INSTANCE=OKF-elastic-prod-website

else

DB_INSTANCE=oki-website-staging
DJANGO_MEDIA_BUCKET=django-statics-okf-website-staging
PROJECT_NAME=oki-website-staging
PROJECT_NUMBER=73584343230
PROJECT_ID=melodic-keyword-303819
S3_BUCKET=okfn-org-staging
REDIS_INSTANC_ID=okf-staging-redis
VPC_ID=vpc-connector-redis-crun
ELASTIC_INSTANCE=OKF-elastic-stg-website

fi

# use 
gcloud sql export sql oki-cloud-sql gs://${OLD_PROD_BUCKET}/okfn.sql --database=okfn

gcloud sql databases delete website --instance=$DB_INSTANCE
gcloud sql databases create website --instance=${DB_INSTANCE}

gcloud sql import sql ${DB_INSTANCE} gs://${OLD_PROD_BUCKET}/okfn.sql --database=website
gsutil rm gs://${OLD_PROD_BUCKET}/okfn.sql

# copy media (requires AWS CLI working and with permissions)

gsutil -m cp -R s3://${S3_BUCKET}/media/articles gs://${DJANGO_MEDIA_BUCKET}/articles
gsutil -m cp -R s3://${S3_BUCKET}/media/banners gs://${DJANGO_MEDIA_BUCKET}/banners
gsutil -m cp -R s3://${S3_BUCKET}/media/cache gs://${DJANGO_MEDIA_BUCKET}/cache
gsutil -m cp -R s3://${S3_BUCKET}/media/cms_page_media gs://${DJANGO_MEDIA_BUCKET}/cms_page_media
gsutil -m cp -R s3://${S3_BUCKET}/media/features gs://${DJANGO_MEDIA_BUCKET}/features
gsutil -m cp -R s3://${S3_BUCKET}/media/filer_public gs://${DJANGO_MEDIA_BUCKET}/filer_public
gsutil -m cp -R s3://${S3_BUCKET}/media/filer_public_thumbnails gs://${DJANGO_MEDIA_BUCKET}/filer_public_thumbnails
gsutil -m cp -R s3://${S3_BUCKET}/media/organisation gs://${DJANGO_MEDIA_BUCKET}/organisation
gsutil -m cp -R s3://${S3_BUCKET}/media/projects gs://${DJANGO_MEDIA_BUCKET}/projects
gsutil -m cp -R s3://${S3_BUCKET}/media/themes gs://${DJANGO_MEDIA_BUCKET}/themes
