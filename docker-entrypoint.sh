#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Updating search index"
python manage.py update_index || echo "Failed to update the search index"

echo "Executing scripts in /docker-entrypoint.d"
    for f in /docker-entrypoint.d/*; do
        case "$f" in
            *.sh)     echo "Running init file $f"; . "$f" ;;
            *)        echo "Ignoring $f (not an sh file)" ;;
        esac
    done

echo "Starting serving app"
/usr/bin/supervisord
