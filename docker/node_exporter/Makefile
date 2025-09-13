# Makefile for node-exporter

# Environment variables
include .env

# Docker image name
IMAGE_NAME := node-exporter
CONTAINER_NAME := node-exporter

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d --name $(CONTAINER_NAME) --net="host" --pid="host" -v "/:/host:ro,rslave" $(IMAGE_NAME) --path.rootfs=/host

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
