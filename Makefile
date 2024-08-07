.PHONY: run format quality-check test migrate superuser delete-database collectstatic copy-env generate-secret-key run-prod

run:
	poetry run python manage.py runserver

format:
	poetry run black .

quality-check:
	poetry run flake8 .
	poetry run black --check .

test:
	poetry run python manage.py test

migrate:
	@poetry run python manage.py makemigrations
	@poetry run python manage.py makemigrations api
	@poetry run python manage.py makemigrations content_management
	@poetry run python manage.py migrate
	@poetry run python manage.py migrate api
	@poetry run python manage.py migrate content_management

superuser:
	@poetry run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') and print('Superuser created successfully')"

delete-database:
	@rm -f db.sqlite3
	@echo "Database deleted successfully."

collectstatic:
	@poetry run python manage.py collectstatic --noinput
	@echo "Static files collected successfully."

copy-env:
	@cp .env.example .env
	@echo "Environment file copied successfully."

generate-secret-key:
	@poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

run-prod:
	poetry run gunicorn alma.wsgi:application --bind 0.0.0.0:8000 --workers 3
	