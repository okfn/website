# okfn.org

![Run tests](https://github.com/okfn/website/workflows/Run%20tests/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/okfn/website/branch/master/graph/badge.svg?token=tYNQSAiFYu)](https://codecov.io/gh/okfn/website)

This is the [Django](https://www.djangoproject.com/)/[Django CMS](https://www.django-cms.org/) project that runs <http://okfn.org>.


## When do I need to modify this?

http://okfn.org/ runs on Django CMS. A lot of the website content can be changed via the [admin panel](https://okfn.org/admin). If we just want to add or remove text and images on the site, it can probably be done via the admin panel. If we need to make global styling or data model changes, then we need to edit the code in this repo.

## Prerequisites and assumptions

You must have the following installed:

- Python 3
- Node JS

Also, the python packages being used require the following libraries to be installed:
- libxml - `sudo apt-get install libxml2-dev`
- libxslt - `sudo apt-get install libxslt1-dev`
- libsasl2 - `sudo apt-get install libsasl2-dev`
- Python Imaging Library (PIL) dependencies, see [here](http://stackoverflow.com/a/21151777/3449709) for quick ubuntu instructions.

You should also follow any install instructions inside a Python virtual environment. Explaining `virtualenv` is outside of the scope of this README, but [this tutorial might help](http://hackercodex.com/guide/python-development-environment-on-mac-osx/).

## Running in development

### Database

It is possible to run the app with no database content. If `DATABASE_URL` is not set, we fall back to a blank SQLite database so this step can be skipped for a minimal case.

To run with a database, you will need a local Postgres server.

- Get a dump of the database
- Create a local database `sudo -u postgres createdb okfn`
- Populate it `sudo -u postgres psql okfn < file=/path/to/dump.sql` or `sudo -u postgres pg_restore -d okfn path/to/dump.dump`

### Running the application

Cherry-pick environment variables from `.env.example` you'd like to set and add it to the `.env` file.
If no env vars are set, we will fall back to default values for development.

If running with Postgres, you will need `DATABASE_URL="postgres://user:pass@127.0.0.1:5432/okfn"` set as a minimum.

Prepare the app:

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

Another option is to use Docker. For this one you should configure your database to work with remote connections using a proper IP address in the connection string or you should use default SQLite database (omit `DATABASE_URL`):

```bash
docker build -t okfn .
docker run -d -p 8888:80 -e DATABASE_URL=<change_me> -e <...> okfn
```

### File uploads

Because this is a CMS project, a lot of the site content is created via the web UI. This means a lot of the images on the site are file uploads, not static content so if you run with a dump of the production or staging DB you will have a lot of blanks where images are supposed to go. In production, the uploaded files are hosted on S3.

The safe way to run the local dev environment with the file uploads corresponding to the DB content is to clone the files from the staging or production bucket(corresponding to the DB dump) to your local environment e.g:

```bash
mkdir media
cd media
aws s3 cp s3://okfn-org-staging/media/ . --recursive
```

Running a local dev environment connected to the prod S3 environment is not recommended.

## Frontend and Static Assets

Javscript and SCSS files live in `/src` and are compiled to `/static`. We use grunt for running front-end tasks.

* `npx grunt watch` Monitor `/src` for changes and auto-compile
* `npx grunt sass:dist && npx grunt postcss:dist` - compile SCSS
* `npx grunt uglify:scripts` - compile javascript

Run `npx grunt --help` to list other available tasks.

We commit compiled static assets to the repo

## Deployment

Production deployment is based on this [Dockerfile](https://github.com/okfn/website/blob/master/Dockerfile). When we want to deploy, we push a tag to this repo. Pushing a tag will trigger a DockerCloud build and publish an image on https://hub.docker.com/r/openknowledge/website/

We can then use the ansible playbooks/helm charts in [okfn/devops](https://github.com/okfn/devops) (private repo) to deploy the image to Google Cloud. Further docs on this are in the devops repo.

## Dependency Management

Dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools).
Add new packages to `requirements.in` / `requirements.dev.in` and compile `requirements.txt` / `requirements.dev.txt` with `pip-compile`.
