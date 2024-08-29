package server

import (
	"context"
	"encoding/json"
	"kafkabridge/internal/config"
	"kafkabridge/internal/db"
	"kafkabridge/internal/models"
	"kafkabridge/internal/repositories"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"go.uber.org/zap"
)

type Server struct {
	db     *db.DB
	logger *zap.SugaredLogger
	repo   *repositories.EventRepository
	cfg    *config.Config
}

func NewServer(cfg *config.Config, db *db.DB, logger *zap.SugaredLogger) *Server {
	return &Server{
		db:     db,
		logger: logger,
		repo:   repositories.NewEventRepository(db),
		cfg:    cfg,
	}
}

func (s *Server) SetupRouter() http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /events", s.getAllEventsHandler)
	mux.HandleFunc("GET /events/{id}", s.getEventByIDHandler)
	mux.HandleFunc("POST /events", s.createEventHandler)
	mux.HandleFunc("PUT /events/{id}", s.updateEventHandler)
	mux.HandleFunc("DELETE /events/{id}", s.deleteEventHandler)

	return mux
}

func (s *Server) getAllEventsHandler(w http.ResponseWriter, r *http.Request) {
	eventType := r.URL.Query().Get("event_type")
	startDateStr := r.URL.Query().Get("start_date")
	endDateStr := r.URL.Query().Get("end_date")

	var startDate, endDate time.Time
	var err error

	if startDateStr != "" {
		startDate, err = time.Parse(time.RFC3339, startDateStr)
		if err != nil {
			s.logger.Errorw("Invalid start_date format", "error", err)
			http.Error(w, "Invalid start_date format. Expected RFC3339 format.", http.StatusBadRequest)
			return
		}
	}

	if endDateStr != "" {
		endDate, err = time.Parse(time.RFC3339, endDateStr)
		if err != nil {
			s.logger.Errorw("Invalid end_date format", "error", err)
			http.Error(w, "Invalid end_date format. Expected RFC3339 format.", http.StatusBadRequest)
			return
		}
	}

	events, err := s.repo.FetchEventsByFilters(r.Context(), eventType, startDate, endDate)
	if err != nil {
		s.logger.Errorw("Error fetching events", "error", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(events)
}

func (s *Server) getEventByIDHandler(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	event, err := s.repo.FetchEventByID(r.Context(), id)
	if err != nil {
		s.logger.Errorw("Error fetching event", "error", err, "id", id)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if event == nil {
		http.Error(w, "Event not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(event)
}

func (s *Server) createEventHandler(w http.ResponseWriter, r *http.Request) {
	var event models.Event
	err := json.NewDecoder(r.Body).Decode(&event)
	if err != nil {
		s.logger.Errorw("Error decoding event", "error", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	event.CreatedAt = time.Now()
	event.UpdatedAt = time.Now()

	err = s.repo.UpsertEvent(r.Context(), &event)
	if err != nil {
		s.logger.Errorw("Error creating event", "error", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(event)
}

func (s *Server) updateEventHandler(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	var event models.Event
	err := json.NewDecoder(r.Body).Decode(&event)
	if err != nil {
		s.logger.Errorw("Error decoding event", "error", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	event.ID = id
	event.UpdatedAt = time.Now()

	err = s.repo.UpsertEvent(r.Context(), &event)
	if err != nil {
		s.logger.Errorw("Error updating event", "error", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(event)
}

func (s *Server) deleteEventHandler(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	err := s.repo.DeleteEvent(r.Context(), id)
	if err != nil {
		s.logger.Errorw("Error deleting event", "error", err, "id", id)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func Start(cfg *config.Config, db *db.DB, logger *zap.SugaredLogger) error {
	server := NewServer(cfg, db, logger)
	router := server.SetupRouter()

	srv := &http.Server{
		Addr:         cfg.ServerAddress,
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)

	go func() {
		logger.Infof("Starting HTTP server on %s", cfg.ServerAddress)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatalf("Could not listen on %s: %v\n", cfg.ServerAddress, err)
		}
	}()

	<-stop

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Fatalf("Server Shutdown Failed:%+v", err)
	}
	logger.Info("Server exited properly")

	return nil
}
