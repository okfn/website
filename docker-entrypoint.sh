#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Updating search index"
python manage.py update_index || echo "Failed to update the search index"

echo "Starting serving app"
/usr/bin/supervisord
