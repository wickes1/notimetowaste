FROM golang:1.23-alpine AS builder

RUN apk update && apk add --no-cache git

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /app/consumer cmd/consumer/main.go
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/producer cmd/producer/main.go
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server cmd/server/main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

COPY --from=builder /app/migrations /root/migrations
COPY --from=builder /app/consumer /root/consumer
COPY --from=builder /app/producer /root/producer
COPY --from=builder /app/server /root/server

CMD ["./server"]
