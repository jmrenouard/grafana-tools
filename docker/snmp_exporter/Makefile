# Makefile for snmp-exporter

# Environment variables
include .env

# Docker image name
IMAGE_NAME := snmp-exporter
CONTAINER_NAME := snmp-exporter

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
# Note: You need to mount a snmp.yml configuration file
run:
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p 9116:9116 -v $(PWD)/snmp.yml:/etc/snmp_exporter/snmp.yml $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# View the container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: all build run stop logs
