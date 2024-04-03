.PHONY: format linter

format:
	poetry run black .

linter:
	poetry run flake8 .
