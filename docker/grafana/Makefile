# Makefile for grafana

# Environment variables
include .env

# Docker image name
IMAGE_NAME := grafana
CONTAINER_NAME := grafana

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p 3000:3000 $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
