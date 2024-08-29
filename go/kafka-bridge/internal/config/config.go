package config

import (
	"fmt"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	KafkaBrokers            []string
	KafkaTopic              string
	KafkaGroupID            string
	KafkaEnableTLS          bool
	KafkaInsecureSkipVerify bool
	KafkaCAFile             string
	KafkaCertFile           string
	KafkaKeyFile            string
	DatabaseURL             string
	ServerAddress           string
}

func LoadConfig() (*Config, error) {
	if err := godotenv.Load(); err != nil {
		return nil, fmt.Errorf("error loading .env file: %w", err)
	}

	return &Config{
		KafkaBrokers:            splitEnv("KAFKA_BROKERS"),
		KafkaTopic:              os.Getenv("KAFKA_TOPIC"),
		KafkaGroupID:            os.Getenv("KAFKA_GROUP_ID"),
		KafkaEnableTLS:          os.Getenv("KAFKA_ENABLE_TLS") == "true",
		KafkaInsecureSkipVerify: os.Getenv("KAFKA_INSECURE_SKIP_VERIFY") == "true",
		KafkaCAFile:             os.Getenv("KAFKA_CA_FILE"),
		KafkaCertFile:           os.Getenv("KAFKA_CERT_FILE"),
		KafkaKeyFile:            os.Getenv("KAFKA_KEY_FILE"),
		DatabaseURL:             os.Getenv("DATABASE_URL"),
		ServerAddress:           os.Getenv("SERVER_ADDRESS"),
	}, nil
}

func splitEnv(envVar string) []string {
	value := os.Getenv(envVar)
	if value == "" {
		return []string{}
	}
	return strings.Split(value, ",")
}
