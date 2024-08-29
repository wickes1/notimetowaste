package main

import (
	"flag"
	"kafkabridge/internal/config"
	"kafkabridge/internal/db"
	"kafkabridge/internal/server"
	"log"
	"os"

	"go.uber.org/zap"
)

func main() {
	migrate := flag.Bool("migrate", false, "Run database migrations and exit")
	flag.Parse()

	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	database, err := db.NewDB(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}
	defer database.Close()

	logger, _ := zap.NewProduction()
	defer logger.Sync()

	sugaredLogger := logger.Sugar()

	if *migrate {
		if err := database.Migrate("./migrations"); err != nil {
			log.Fatalf("failed to run migrations: %v", err)
		}
		log.Println("migrations ran successfully")
		os.Exit(0)
	}

	if err := server.Start(cfg, database, sugaredLogger); err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
