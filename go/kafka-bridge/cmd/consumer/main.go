package main

import (
	"kafkabridge/internal/config"
	"kafkabridge/internal/db"
	"kafkabridge/internal/kafka"
	"kafkabridge/internal/repositories"
	"log"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	database, err := db.NewDB(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}
	defer database.Close()

	repo := repositories.NewEventRepository(database)

	if err := kafka.ConsumeEvents(cfg, repo); err != nil {
		log.Fatalf("failed to consume events: %v", err)
	}
}
