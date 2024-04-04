.PHONY: run format quality-check test

run:
	poetry run python manage.py runserver

format:
	poetry run black .

quality-check:
	poetry run flake8 .
	poetry run black --check .

test:
	poetry run python manage.py test
