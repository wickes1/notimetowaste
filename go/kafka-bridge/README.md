# KafkaBridge

## Overview

KafkaBridge is a project that connects different services using Kafka (via Redpanda) for messaging.

The system is composed of several Dockerized services:

1. **Producer**: A service that continuously produces fake events and sends them to a Kafka topic.
2. **Consumer**: A service that consumes events from the Kafka topic and inserts them into a database.
3. **Server**: An API server that also handles database migrations. It provides a RESTful interface for interacting with the events stored in the database.
4. **Redpanda**: A Kafka-compatible streaming platform used as the messaging backbone.
5. **PostgreSQL**: A relational database used to store events consumed from the Kafka topic.
6. **Redpanda Console**: A UI for monitoring and managing Kafka topics, consumer groups, and more.

## Getting Started

### Prerequisites

Make sure you have Docker, Docker Compose, and Make installed.

### Project Structure

```bash
kafkabridge/
├── cmd/
│   ├── consumer/
│   │   └── main.go        # Entry point for the Consumer service
│   ├── producer/
│   │   └── main.go        # Entry point for the Producer service
│   └── server/
│       └── main.go        # Entry point for the API server and migrations
├── Dockerfile             # Dockerfile for building all services
├── docker-compose.yml     # Docker Compose configuration
├── migrations/            # Database migration files
├── certs/                 # SSL certificates for Kafka (Redpanda) TLS
├── .env.example           # Example environment variables file
└── README.md              # Project documentation (this file)
```

### Configuration

#### 1. **Running the Entire Project in Docker**

If you want to run everything inside Docker, including KafkaBridge services:

1. **Set Up Environment Variables**:
   - Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. **Update `.env` for Docker**:
   - Modify the `.env` file with the following values:

   ```env
   DATABASE_URL=postgres://postgres:postgres@kafka-bridge-postgres:5432/postgres?sslmode=disable
   KAFKA_BROKERS=kafka-bridge-redpanda:9092
   ```

3. **Build and Run**:

   ```bash
   make docker-compose-up
   ```

   This command will build the Docker images and start all services, including PostgreSQL, Redpanda, and KafkaBridge services (Producer, Consumer, and Server).

#### 2. **Running Infrastructure in Docker and Services Locally**

If you prefer to run the infrastructure (PostgreSQL, Redpanda, and Redpanda Console) in Docker but run the KafkaBridge services locally:

1. **Set Up Environment Variables**:
   - Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. **Update `.env` for Local Development**:
   - Modify the `.env` file with the following values:

   ```env
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable
   KAFKA_BROKERS=localhost:19092
   ```

3. **Start Infrastructure**:

   ```bash
   make run-infra
   ```

   This command will start PostgreSQL, Redpanda, and Redpanda Console in Docker.

4. **Run KafkaBridge Services**:

   ```bash
   make run-all
   ```

   This will start the Producer, Consumer, and Server services locally on your machine.

### Accessing Redpanda Console

You can monitor Kafka topics and more using the Redpanda Console at `http://localhost:8080`.

### Stopping the Services

To bring down all the services:

```bash
docker-compose down
```
