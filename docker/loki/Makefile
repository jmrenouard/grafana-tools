# Makefile for loki

# Environment variables
include .env

# Docker image name
IMAGE_NAME := loki
CONTAINER_NAME := loki

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
# Note: You need to mount a loki-config.yaml configuration file
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p 3100:3100 -v $(PWD)/loki-config.yaml:/etc/loki/loki-config.yaml $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
