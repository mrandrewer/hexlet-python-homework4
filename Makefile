install:
	poetry install --no-root

run:
	poetry run python src/__main__.py

lint:
	poetry run flake8 .