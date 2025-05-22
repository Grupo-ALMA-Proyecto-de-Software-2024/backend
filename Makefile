.PHONY: run format quality-check test migrate superuser delete-database collectstatic copy-env generate-secret-key run-prod

run:
	uv run python manage.py runserver

format:
	uv run black .

quality-check:
	uv run flake8 .
	uv run black --check .

test:
	uv run python manage.py test

migrate:
	@uv run python manage.py makemigrations
	@uv run python manage.py makemigrations api
	@uv run python manage.py makemigrations content_management
	@uv run python manage.py migrate
	@uv run python manage.py migrate api
	@uv run python manage.py migrate content_management

superuser:
	@uv run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') and print('Superuser created successfully')"

delete-database:
	@rm -f db.sqlite3
	@echo "Database deleted successfully."

collectstatic:
	@uv run python manage.py collectstatic --noinput
	@echo "Static files collected successfully."

copy-env:
	@cp .env.example .env
	@echo "Environment file copied successfully."

generate-secret-key:
	@uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

run-prod:
	uv run gunicorn alma.wsgi:application --bind 0.0.0.0:8000 --workers 3
	