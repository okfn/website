# okfn.org

- [![Build Status](https://travis-ci.org/okfn/website.svg?branch=master)](https://travis-ci.org/okfn/website)
- [![Coverage Status](https://coveralls.io/repos/github/okfn/website/badge.svg?branch=master)](https://coveralls.io/github/okfn/website?branch=master)

- This is the [Django](https://www.djangoproject.com/)/[Django CMS](https://www.django-cms.org/) project that runs <http://okfn.org>.

## Prerequisites and assumptions

You must have the following installed:

- Python 3
- node

Also, the python packages being used require the following libraries to be installed:
- libxml
- libxslt
- libsasl2
- Python Imaging Library (PIL) dependencies, see [here](http://stackoverflow.com/a/21151777/3449709) for a quick ubuntu instructions.

You may also wish to follow any install instructions inside a Python virtual environment. Explaining `virtualenv` is outside of the scope of this README, but [this tutorial might help](http://hackercodex.com/guide/python-development-environment-on-mac-osx/).

## Running in development

Prepare the database. This step can be skipped if you'd like to use dummy SQLite database:
- Get a dump of the database
- Create a local database `createdb okfn`
- Populate it `psql okfn --file=/path/to/dump.sq` or `pg_restore -d okfn path/to/dump.dump`

Cherry-pick environment variables from `.env.example` you'd like to set and add it to the `.env` file. Popular options:
- CACHE_URL
- DATABASE_URL
- DJANGO_DEBUG
- DJANGO_SECRET_KEY

Prepare the app:
```bash
pip install -r requirements.dev.txt
npm install
python manage.py migrate
python manage.py update_index
```

Start the server:
```
python manage.py runserver # dev
gunicorn foundation.wsgi:application --access-logfile '-' --error-logfile '-' # prod
```

Another option is to use Docker. For this one you should configure your database to work with remote connections using a proper IP address in the connection string or you should use default SQLite database (omit `DATABASE_URL`):
```
docker build -t okfn .
docker run -d -p 8888:80 -e DATABASE_URL=<change_me> -e <...> okfn
```

## Static files

Static assets are collected and stored in a Amazon S3 Bucket, and served via Cloudfront CDN. To update the collected static files, make sure you have this env vars set:

```
AWS_STORAGE_BUCKET_NAME="okfn-org-production"
JANGO_USE_AWS_STORAGE="true"

AWS_ACCESS_KEY_ID="change-me"
AWS_SECRET_ACCESS_KEY="change-me"

```

To update the static files run

```
python manage.py collectstatic
```

Note that this *will not* update the images on the site as they are still served by Cloudfront. You need to invalidate the updated files using the AWS cli or web interface.
