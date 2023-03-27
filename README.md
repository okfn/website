# okfn.org

![Run tests](https://github.com/okfn/website/workflows/Run%20tests/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/okfn/website/branch/master/graph/badge.svg?token=tYNQSAiFYu)](https://codecov.io/gh/okfn/website)

This is the [Django](https://www.djangoproject.com/)/[Django CMS](https://www.django-cms.org/) project that runs <http://okfn.org>.


## When do I need to modify this?

http://okfn.org/ runs on Django CMS. A lot of the website content can be changed via the [admin panel](https://okfn.org/admin). If we just want to add or remove text and images on the site, it can probably be done via the admin panel. If we need to make global styling or data model changes, then we need to edit the code in this repo.

## Prerequisites and assumptions

You must have the following installed:

- Python 3.8
- Node JS

The [/Dockerfile](/Dockerfile) (used for staging/production) and the [requirements file](/requirements.txt)
(built with `pip-tools`) in this repo shows you the application dependencies.

## Running in staging or production

Read this [doc](/docs/cloud/google-deploy.md).  

## Running in development

### Database

It is possible to run the app with no database content. If databaset settings are not set,
we fall back to a blank SQLite database (defined in the [.env.base](/.env.base) file)
so this step can be skipped for a minimal case.

To run with a database, you will need a local Postgres server.

- Get a dump of the database
- Create a local database `sudo -u postgres createdb okfn`
- Populate it `sudo -u postgres psql okfn < file=/path/to/dump.sql` or `sudo -u postgres pg_restore -d okfn path/to/dump.dump`

### Running the application

Cherry-pick environment variables from `.env.example` you'd like to set and add it to the `.env` file.
If no env vars are set, we will fall back to default [.env.base](/.env.base) file.

If running with Postgres, you will need to set:

```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=okfn
DB_USER=user
DB_PASSWORD=pass
DB_HOST=localhost
DB_PORT=5432
```

Prepare the app:

Create a Python 3.8 local environment (e.g. `python3.8 -m venv ~/okf-website-env`)

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
npm install
python manage.py migrate
python manage.py update_index
```

Start the server:

```bash
python manage.py runserver
```

Another option is to use Docker.

```bash
docker build -t okfn .
docker run -d -p 8888:80 okfn
```

### File uploads

Because this is a CMS project, a lot of the site content is created via the web UI.  
This means a lot of the images on the site are file uploads.  
In staging and production, the uploaded files are hosted on Google Cloud Storage.

If you want to get all production/staging media files you can download them from Google
Cloud Storage and put them in a local `media` directory (`MEDIA_ROOT` from settings).

## Frontend and Static Assets

Javscript and SCSS files live in `/src` and are compiled to `/static`. We use grunt for running front-end tasks.

* `npx grunt watch` Monitor `/src` for changes and auto-compile
* `npx grunt sass:dist && npx grunt postcss:dist` - compile SCSS
* `npx grunt uglify:scripts` - compile javascript

Run `npx grunt --help` to list other available tasks.

We commit compiled static assets to the repo

## Deployment

Production deployment is based on this [Dockerfile](/Dockerfile). When we want to deploy,
we just push to `main` branch (or `develop` branch for staging environment).
## Dependency Management

Dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools).
Add new packages to `requirements.in` / `requirements.dev.in` 
and compile `requirements.txt` / `requirements.dev.txt` with `pip-compile`.

You can run `pip list --outdated` to see outdated packages.

## Changelog

All changes must be documented at the [CHANGELOG](CHANGELOG.md) file
