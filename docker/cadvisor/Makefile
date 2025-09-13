# Makefile for cadvisor

# Environment variables
include .env

# Docker image name
IMAGE_NAME := cadvisor
CONTAINER_NAME := cadvisor

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run \
	  --volume=/:/rootfs:ro \
	  --volume=/var/run:/var/run:ro \
	  --volume=/sys:/sys:ro \
	  --volume=/var/lib/docker/:/var/lib/docker:ro \
	  --volume=/dev/disk/:/dev/disk:ro \
	  --publish=8080:8080 \
	  --detach=true \
	  --name=$(CONTAINER_NAME) \
	  $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
