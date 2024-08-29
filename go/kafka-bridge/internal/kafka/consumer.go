package kafka

import (
	"context"
	"encoding/json"
	"fmt"
	"kafkabridge/internal/config"
	"kafkabridge/internal/models"
	"kafkabridge/internal/repositories"
	"os"
	"os/signal"

	"github.com/IBM/sarama"
)

func ConsumeEvents(cfg *config.Config, repo *repositories.EventRepository) error {
	tlsConfig, err := CreateTLSConfig(cfg.KafkaEnableTLS, cfg.KafkaInsecureSkipVerify, cfg.KafkaCAFile, cfg.KafkaCertFile, cfg.KafkaKeyFile)
	if err != nil {
		return fmt.Errorf("failed to create TLS configuration: %w", err)
	}

	config := sarama.NewConfig()
	config.Consumer.Group.Rebalance.GroupStrategies = []sarama.BalanceStrategy{sarama.NewBalanceStrategyRoundRobin()}
	config.Consumer.Offsets.Initial = sarama.OffsetOldest
	if tlsConfig != nil {
		config.Net.TLS.Enable = true
		config.Net.TLS.Config = tlsConfig
	}

	consumerGroup, err := sarama.NewConsumerGroup(cfg.KafkaBrokers, cfg.KafkaGroupID, config)
	if err != nil {
		return fmt.Errorf("failed to create consumer group: %w", err)
	}
	defer consumerGroup.Close()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	consumer := &eventConsumer{
		repo: repo,
	}

	go func() {
		for err := range consumerGroup.Errors() {
			fmt.Printf("Consumer group error: %v\n", err)
		}
	}()

	go func() {
		for {
			select {
			case <-ctx.Done():
				return
			default:
				if err := consumerGroup.Consume(ctx, []string{cfg.KafkaTopic}, consumer); err != nil {
					fmt.Printf("Error consuming messages: %v\n", err)
					return
				}
			}
		}
	}()

	sigterm := make(chan os.Signal, 1)
	signal.Notify(sigterm, os.Interrupt)
	<-sigterm
	cancel()

	<-ctx.Done()

	return nil
}

type eventConsumer struct {
	repo *repositories.EventRepository
}

func (consumer *eventConsumer) Setup(_ sarama.ConsumerGroupSession) error {
	return nil
}

func (consumer *eventConsumer) Cleanup(_ sarama.ConsumerGroupSession) error {
	return nil
}

func (consumer *eventConsumer) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for message := range claim.Messages() {
		var event models.Event
		if err := json.Unmarshal(message.Value, &event); err != nil {
			fmt.Printf("Failed to unmarshal event: %v\n", err)
			continue
		}

		err := consumer.repo.UpsertEvent(session.Context(), &event)
		if err != nil {
			fmt.Printf("Failed to insert event into database: %v\n", err)
			continue
		}

		fmt.Printf("Consumed event: %s\n", event.ID)
		session.MarkMessage(message, "")
	}
	return nil
}
