# okfn.org

![Run tests](https://github.com/okfn/website/workflows/Run%20tests/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/okfn/website/branch/master/graph/badge.svg?token=tYNQSAiFYu)](https://codecov.io/gh/okfn/website)

This is the [Django](https://www.djangoproject.com/)/[Django CMS](https://www.django-cms.org/) project that runs <http://okfn.org>.


## When do I need to modify this?

http://okfn.org/ runs on Django CMS. 

Most of the contents are provided via plugins and our communication person is currently responsible to edit the content or add new stuff 
to the site. It is the idea, and the goal of the development that **all content** is dinamically handled by plugins. This means that we
are aiming to have templates with placeholders instead of text. So, if you need to modify content, probably you can already do it using
Django CMS built in capabilities.

If we need to make global styling or data model changes, then we need to edit the code in this repo.

## Prerequisites and assumptions

You must have the following installed:

- Python 3.10
- Node JS 16

The [/Dockerfile](/Dockerfile) (used for staging/production) and the [requirements file](/requirements.txt)
(built with `pip-tools`) in this repo shows you the application dependencies.

# Development

## Database

It is possible to run the app with no database content. If databaset settings are not set,
we fall back to a blank SQLite database (defined in the [.env.base](/.env.base) file)
so this step can be skipped for a minimal case.

To run with a database, you will need a local Postgres server.

- Get a dump of the database (we store them as `*.sql` in Google Cloud Storage)
- Create a local database `sudo -u postgres createdb okfn`
- Populate it `sudo -u postgres psql okfn < file=/path/to/dump.sql` or `sudo -u postgres pg_restore -d okfn path/to/dump.dump`

## Running the application

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

Make sure to have the correct node version:

```bash
nvm install 16
nvm use 16
```

Create a Python 3.10 local environment (e.g. `python3.10 -m venv ~/okf-website-env`)

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

## File uploads

Because this is a CMS project, a lot of the site content is created via the web UI.  
This means a lot of the images on the site are file uploads.  
In staging and production, the uploaded files are hosted on Google Cloud Storage.

If you want to get all production/staging media files you can download them from Google
Cloud Storage and put them in a local `media` directory (`MEDIA_ROOT` from settings).

**Note:** A dump of the production database will require all the media files of production.
Same for staging.


## Frontend

### CSS

Currently we are using Tailwind, PostCSS as our CSS stack. Please check the documentation to get a sense
of how it works: [Installing Tailwind CSS as a PostCSS plugin](https://tailwindcss.com/docs/installation/using-postcss)

The css build is done by `PostCSS` and the configuration files for it are `tailwind.config.cjs` and `postcss.config.cjs`.

Running `npm run build` will compile our main `styles.css` file and place it in `static/css/styles.css`. (It then will be collected by 
Django when building the Dockerfile)

**Remember:** Tailwind CSS works by scanning all of our HTML files, JavaScript components, and any other templates
 for class names to generate `styles.css`. If you ar adding new files, make sure to update the `content` field `tailwind.config.cjs`. 
 (If required)


### Javascript

1. Clone the repository https://github.com/ishigami/okfn_front
2. `npm i`
3. `npm run build`
4. copy `../dist/assets/main-[HASH].js` to `/static/js/scripts.js`

### Backend (Django and `django-cms`)

New plugins for blocks of content are located on `foundation/okfplugins`.

1. Create a folder on foundation/okfplugins having:
 * `admin.py`: used on Django Admin interface
 * `cms_plugin.py`: configuration to appear on the Django CMS content editor sidebar
 * `templates/`: the django template files (access the plugin variable defined on models.py with instance.VARIABLE)
 * `models.py`: the model for the plugin object on the database

 You can copy a simple plugin as heading or just_text and change the files above. If you do that don't forge to delete the migration files inside migrations/, except by __init__.py.

2. Add the plugin to `foundation/settings.py` (`INSTALLED_APPS` setting).

3. Run `python manage.py makemigrations` after you create the `models.py`.

4. Run the migration to change the database with `python manage.py migrate`

5. Start the server with `python manage.py runserver`

### References for new design and components

 * Components: https://ishigami.github.io/okfn_front/components
 * More components: https://ishigami.github.io/okfn_front/components-2.html
 * Homepage: https://ishigami.github.io/okfn_front/
 * Source: https://github.com/ishigami/okfn_front



# Deployment

Production deployment is based on this [Dockerfile](/Dockerfile). When we want to deploy,
we just push to `main` branch (or `develop` branch for staging environment).

For more info read this [doc](/docs/cloud/google-deploy.md).  

## Dependency Management

Dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools).
Add new packages to `requirements.in` / `requirements.dev.in` 
and compile `requirements.txt` / `requirements.dev.txt` with `pip-compile`.

You can run `pip list --outdated` to see outdated packages.

## Changelog

All changes must be documented at the [CHANGELOG](CHANGELOG.md) file
