# foundation

This is the [Django][dj]/[Django CMS][djcms] project that runs <http://okfn.org>.

[dj]: https://www.djangoproject.com/
[djcms]: https://www.django-cms.org/

[![Build Status](https://travis-ci.org/okfn/foundation.png?branch=master)](https://travis-ci.org/okfn/foundation)
[![Coverage Status](https://coveralls.io/repos/okfn/foundation/badge.png?branch=master)](https://coveralls.io/r/okfn/foundation?branch=master)

## Running in development

    pip install -r requirements.dev.txt
    pip install honcho
    npm install -g less
    python manage.py syncdb --migrate
    honcho -f Procfile.dev start

## Running on Heroku

Please note that the following are by no means full instructions. There are a
number of config variables that will also need setting before the application
will work. These will be documented in due course.

    heroku create
    heroku labs:enable user-env-compile
    heroku addons:add heroku-postgresql
    heroku addons:add mandrill
    heroku config DJANGO_DEBUG=false \
                  DJANGO_COMPRESS_OFFLINE=true \
                  ...
    git push heroku master
    heroku run python manage.py syncdb --migrate
