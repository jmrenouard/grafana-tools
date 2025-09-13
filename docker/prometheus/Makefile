# Makefile for prometheus

# Environment variables
include .env

# Docker image name
IMAGE_NAME := prometheus
CONTAINER_NAME := prometheus

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
# Note: You need to mount a prometheus.yml configuration file
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p 9090:9090 -v $(PWD)/prometheus.yml:/etc/prometheus/prometheus.yml $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
