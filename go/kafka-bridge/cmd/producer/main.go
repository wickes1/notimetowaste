package main

import (
	"kafkabridge/internal/config"
	"kafkabridge/internal/kafka"
	"log"
	"time"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	interval := 5 * time.Second

	if err := kafka.ProduceEvents(cfg, interval); err != nil {
		log.Fatalf("failed to produce event: %v", err)
	}
}
