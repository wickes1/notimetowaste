package repositories

import (
	"context"
	"database/sql"
	"fmt"
	"kafkabridge/internal/db"
	"kafkabridge/internal/models"
	"strings"
	"time"
)

type EventRepository struct {
	db *db.DB
}

func NewEventRepository(db *db.DB) *EventRepository {
	return &EventRepository{db: db}
}

func (r *EventRepository) FetchEventsByFilters(ctx context.Context, eventType string, startDate, endDate time.Time) ([]models.Event, error) {
	var queryBuilder strings.Builder
	var args []interface{}
	var argCount int

	queryBuilder.WriteString("SELECT id, event_type, source, payload, metadata, created_at, updated_at FROM events WHERE 1=1")

	if eventType != "" {
		argCount++
		queryBuilder.WriteString(fmt.Sprintf(" AND event_type = $%d", argCount))
		args = append(args, eventType)
	}

	if !startDate.IsZero() {
		argCount++
		queryBuilder.WriteString(fmt.Sprintf(" AND created_at >= $%d", argCount))
		args = append(args, startDate)
	}

	if !endDate.IsZero() {
		argCount++
		queryBuilder.WriteString(fmt.Sprintf(" AND created_at <= $%d", argCount))
		args = append(args, endDate)
	}

	queryBuilder.WriteString(" ORDER BY created_at DESC")

	query := queryBuilder.String()

	rows, err := r.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch events: %w", err)
	}
	defer rows.Close()

	var events []models.Event
	for rows.Next() {
		var e models.Event
		err := rows.Scan(&e.ID, &e.EventType, &e.Source, &e.Payload, &e.Metadata, &e.CreatedAt, &e.UpdatedAt)
		if err != nil {
			return nil, fmt.Errorf("failed to scan event: %w", err)
		}
		events = append(events, e)
	}

	if err = rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating over events: %w", err)
	}

	return events, nil
}

func (r *EventRepository) FetchEventByID(ctx context.Context, id string) (*models.Event, error) {
	query := `SELECT id, event_type, source, payload, metadata, created_at, updated_at FROM events WHERE id = $1`
	var e models.Event
	err := r.db.QueryRowContext(ctx, query, id).Scan(&e.ID, &e.EventType, &e.Source, &e.Payload, &e.Metadata, &e.CreatedAt, &e.UpdatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to fetch event by ID: %w", err)
	}
	return &e, nil
}

func (r *EventRepository) UpsertEvent(ctx context.Context, e *models.Event) error {
	query := `
		MERGE INTO events AS e
		USING (VALUES ($1::uuid, $2::varchar, $3::varchar, $4::jsonb, $5::jsonb, $6::timestamptz, $7::timestamptz))
			AS v(id, event_type, source, payload, metadata, created_at, updated_at)
		ON e.id = v.id
		WHEN MATCHED THEN UPDATE SET
			event_type = v.event_type,
			source = v.source,
			payload = v.payload,
			metadata = v.metadata,
			updated_at = CURRENT_TIMESTAMP
		WHEN NOT MATCHED THEN
			INSERT (id, event_type, source, payload, metadata, created_at, updated_at)
			VALUES (v.id, v.event_type, v.source, v.payload, v.metadata, v.created_at, v.updated_at)
	`
	_, err := r.db.ExecContext(ctx, query, e.ID, e.EventType, e.Source, e.Payload, e.Metadata, e.CreatedAt, e.UpdatedAt)
	if err != nil {
		return fmt.Errorf("failed to upsert event: %w", err)
	}
	return nil
}

func (r *EventRepository) DeleteEvent(ctx context.Context, id string) error {
	query := `DELETE FROM events WHERE id = $1`
	result, err := r.db.ExecContext(ctx, query, id)
	if err != nil {
		return fmt.Errorf("failed to delete event: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("no event found with id %s", id)
	}

	return nil
}
