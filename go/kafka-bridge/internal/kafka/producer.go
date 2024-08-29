package kafka

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"os/signal"
	"syscall"
	"time"

	"kafkabridge/internal/config"
	"kafkabridge/internal/models"

	"github.com/IBM/sarama"
	"github.com/google/uuid"
)

var eventTypes = []string{"user_signup", "purchase", "system_alert", "file_upload"}
var sources = []string{"web", "mobile", "backend", "third_party"}

func randomPayload(eventType string) map[string]interface{} {
	switch eventType {
	case "user_signup":
		return map[string]interface{}{
			"user_id":   uuid.New().String(),
			"email":     fmt.Sprintf("user%d@example.com", rand.Intn(1000)),
			"signup_at": time.Now().Format(time.RFC3339),
			"referral":  rand.Intn(2) == 1,
		}
	case "purchase":
		return map[string]interface{}{
			"order_id":    uuid.New().String(),
			"user_id":     uuid.New().String(),
			"amount":      rand.Float64() * 100,
			"currency":    "USD",
			"purchase_at": time.Now().Format(time.RFC3339),
			"items":       rand.Intn(5) + 1,
		}
	case "system_alert":
		return map[string]interface{}{
			"alert_id":   uuid.New().String(),
			"severity":   []string{"low", "medium", "high"}[rand.Intn(3)],
			"message":    "System overload detected",
			"alerted_at": time.Now().Format(time.RFC3339),
		}
	case "file_upload":
		return map[string]interface{}{
			"file_id":   uuid.New().String(),
			"user_id":   uuid.New().String(),
			"filename":  fmt.Sprintf("file%d.txt", rand.Intn(1000)),
			"upload_at": time.Now().Format(time.RFC3339),
			"file_size": rand.Intn(1000),
		}
	default:
		return map[string]interface{}{}
	}
}

func randomMetadata() map[string]interface{} {
	return map[string]interface{}{
		"ip_address": fmt.Sprintf("%d.%d.%d.%d", rand.Intn(256), rand.Intn(256), rand.Intn(256), rand.Intn(256)),
		"user_agent": []string{"Chrome", "Firefox", "Safari", "Edge"}[rand.Intn(4)],
		"location":   []string{"US", "CA", "UK", "AU"}[rand.Intn(4)],
	}
}

func ProduceEvents(cfg *config.Config, interval time.Duration) error {
	tlsConfig, err := CreateTLSConfig(cfg.KafkaEnableTLS, cfg.KafkaInsecureSkipVerify, cfg.KafkaCAFile, cfg.KafkaCertFile, cfg.KafkaKeyFile)
	if err != nil {
		return fmt.Errorf("failed to create TLS configuration: %w", err)
	}
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	if tlsConfig != nil {
		config.Net.TLS.Enable = true
		config.Net.TLS.Config = tlsConfig
	}

	producer, err := sarama.NewSyncProducer(cfg.KafkaBrokers, config)
	if err != nil {
		return fmt.Errorf("failed to create producer: %w", err)
	}
	defer producer.Close()

	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)

	for {
		select {
		case <-sigchan:
			fmt.Println("Received shutdown signal, exiting...")
			return nil
		default:
			eventType := eventTypes[rand.Intn(len(eventTypes))]
			source := sources[rand.Intn(len(sources))]

			event := models.Event{
				ID:        uuid.New().String(),
				EventType: eventType,
				Source:    source,
				CreatedAt: time.Now(),
				UpdatedAt: time.Now(),
				Payload:   jsonMarshal(randomPayload(eventType)),
				Metadata:  jsonMarshal(randomMetadata()),
			}

			eventBytes, err := json.Marshal(event)
			if err != nil {
				return fmt.Errorf("failed to marshal event: %w", err)
			}

			msg := &sarama.ProducerMessage{
				Topic: cfg.KafkaTopic,
				Key:   sarama.StringEncoder(event.ID),
				Value: sarama.ByteEncoder(eventBytes),
			}

			partition, offset, err := producer.SendMessage(msg)
			if err != nil {
				return fmt.Errorf("failed to send message: %w", err)
			}

			fmt.Printf("Produced event: %s, partition: %d, offset: %d\n", event.ID, partition, offset)

			time.Sleep(interval)
		}
	}
}

func jsonMarshal(v interface{}) json.RawMessage {
	data, _ := json.Marshal(v)
	return data
}
