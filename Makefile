.PHONY: format quality-check

format:
	poetry run black .

quality-check:
	poetry run flake8 .
	poetry run black --check .
