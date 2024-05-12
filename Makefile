.PHONY: start_third_party env run migrate makemigrations test lint clean local requirements docker

start_third_party:
	docker compose up -d --remove-orphans

env:
	cp .env.local .env

run: start_third_party
	poetry run ./manage.py runserver

migrate:
	poetry run ./manage.py migrate

makemigrations:
	poetry run ./manage.py makemigrations

test:
	poetry run ./manage.py test

lint:
	poetry run mypy .
	poetry run ruff check .
	poetry run isort --check .

format:
	poetry run ruff format .
	poetry run isort .
	poetry run ruff check --fix .

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -fr static
	poetry run ./manage.py clearsessions

requirements:
	poetry export --without-hashes --with prod -f requirements.txt -o requirements.txt

docker: requirements
	docker build -t auto_ml_flow .

local: clean env start_third_party makemigrations migrate run
