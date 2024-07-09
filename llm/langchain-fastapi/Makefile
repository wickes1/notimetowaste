# May 03 2024
# Description: Makefile for FastAPI Application
# Author: Wickes1

PROJECT = langchain-fastapi
LABEL := v1.0.0
# PROJECT := $(shell basename -s .git `git config --get remote.origin.url`)
# LABEL := $(shell git describe --tags $(shell git rev-list --tags --max-count=1))
DOCKER_REPO := northamerica-northeast2-docker.pkg.dev/hobby-422104/fastapi-dwss-validator

deps:
	poetry add fastapi 'uvicorn[standard]' gunicorn python-dotenv pydantic-settings
	poetry add -G dev ruff mypy pytest coverage pytest-asyncio setuptools

dev:
	poetry run python -m app.main

prod:
	poetry run gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py app.main:app

lint:
	@poetry run mypy app
	@poetry run ruff check
	@poetry run ruff format --check

format:
	@poetry run ruff check --fix
	@poetry run ruff format

test:
	@export TESTING=true && poetry run coverage run --source ./app -m pytest --disable-warnings
	@poetry run coverage report --show-missing
	@poetry run coverage html --title "${@-coverage}"

docker/build:
	 poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev
	docker build -t $(PROJECT):$(LABEL) .

docker/run:
	# pass dotenv file to container
	docker run -p 8000:8000 --env-file .env $(PROJECT):$(LABEL)

docker/db:
	@docker compose up -d db

docker/push:
	docker tag $(PROJECT):$(LABEL) $(DOCKER_REPO)/$(PROJECT):$(LABEL)
	docker push $(DOCKER_REPO)/$(PROJECT):$(LABEL)

docker-compose/up:
	@docker compose up -d

docker-compose/down:
	@docker compose down

docker-compose/logs:
	@docker compose logs -f

docker-compose/clean:
	@docker compose down --rmi all --volumes --remove-orphans

k8s/deploy: format check test
	$(eval CONTEXT := $(shell kubectl config current-context))
	@cd k8s && kustomize edit set image demo=$(PROJECT):$(LABEL)
	@echo "Deploy $(PROJECT):$(LABEL) to $(CONTEXT), press any key to continue or Ctrl+C to cancel."
	@read -n 1 -s -r -p "" && echo "Deploying..."
	@kustomize build k8s | kubectl apply -f -
