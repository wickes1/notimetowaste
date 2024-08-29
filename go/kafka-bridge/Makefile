#!make
include .env
export $(shell sed 's/=.*//' .env)

DOCKER_IMAGE = kafka-bridge

init:
	@go mod tidy

docker-build:
	@docker build -t $(DOCKER_IMAGE) .

docker-run:
	@docker run --rm -it --network host -v $(shell pwd)/.env:/root/.env -v $(shell pwd)/certs:/root/certs $(DOCKER_IMAGE)

docker-compose-up:
	@docker compose up --build

migrate-up:
	@go run cmd/server/main.go --migrate

migrate-down:
	@migrate -database ${POSTGRESQL_URL} -path migrations down

run-consumer:
	@go run cmd/consumer/main.go

run-producer:
	@go run cmd/producer/main.go

run-server:
	@go run cmd/server/main.go

run-all: migrate-up
	@echo "Starting consumer..."
	@$(MAKE) run-consumer &
	@echo "Starting producer..."
	@$(MAKE) run-producer &
	@echo "Starting server..."
	@$(MAKE) run-server

run-infra:
	@docker-compose up postgres redpanda console
