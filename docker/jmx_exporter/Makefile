# Makefile for jmx-exporter

# Environment variables
include .env

# Docker image name
IMAGE_NAME := jmx-exporter
CONTAINER_NAME := jmx-exporter

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
# Note: This exporter runs as a java agent, and needs to be attached to a JVM.
# The run command will depend on the target application.
run:
	echo "This exporter needs to be attached to a running JVM. See the documentation for details."

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
