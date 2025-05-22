#!/bin/bash
set -e

echo "Running entrypoint.sh"

# Wait for database to be ready (if needed)
# sleep 5

# Run migrations
echo "Running migrations..."
poetry run python manage.py makemigrations
poetry run python manage.py makemigrations api
poetry run python manage.py makemigrations content_management
poetry run python manage.py migrate
poetry run python manage.py migrate api
poetry run python manage.py migrate content_management

# Collect static files
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Run the application
echo "Starting Gunicorn..."
poetry run gunicorn alma.wsgi:application --bind 0.0.0.0:8000 --workers 3
