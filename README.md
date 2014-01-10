## Running in development

    pip install -r requirements.dev.txt
    pip install honcho
    npm install -g less
    python manage.py syncdb
    python manage.py migrate
    honcho -f Procfile.dev start

## Running on Heroku

    heroku create
    heroku labs:enable user-env-compile
    heroku addons:add heroku-postgresql
    git push heroku master
