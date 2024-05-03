# May 03 2024
# Description: Makefile for FastAPI Application
# Author: Wickes1

PROJECT = fastapi-todo
LABEL := v1.0.0
# PROJECT := $(shell basename -s .git `git config --get remote.origin.url`)
# LABEL := $(shell git describe --tags $(shell git rev-list --tags --max-count=1))

deps:
	poetry add fastapi 'uvicorn[standard]' gunicorn python-dotenv pydantic-settings
	poetry add -G dev ruff mypy pytest coverage pytest-asyncio setuptools

dev:
	poetry run python -m app.main

prod:
	poetry run gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app.main:app

format:
	@poetry run ruff format
	@poetry run ruff check --fix

check:
	@poetry run mypy app

test:
	@export TESTING=true && poetry run coverage run --source ./app -m pytest --disable-warnings
	@poetry run coverage report

docker/build:
	docker build -t $(PROJECT):$(LABEL) .

docker/run:
	docker run -p 8000:8000 $(PROJECT):$(LABEL)

k8s/deploy: format check test
	$(eval CONTEXT := $(shell kubectl config current-context))
	@cd k8s && kustomize edit set image demo=$(PROJECT):$(LABEL)
	@echo "Deploy $(PROJECT):$(LABEL) to $(CONTEXT), press any key to continue or Ctrl+C to cancel."
	@read -n 1 -s -r -p "" && echo "Deploying..."
	@kustomize build k8s | kubectl apply -f -
