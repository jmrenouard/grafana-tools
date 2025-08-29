# Makefile for Grafana Dashboard Generator
#
# This Makefile provides a set of commands to help you manage the project,
# from installing dependencies to building and publishing Docker images.

# --- Configuration ---
# Get the script version from the Python file
VERSION := $(shell grep '__version__' grafana_helper.py | cut -d '"' -f 2)
# Docker image name
IMAGE_NAME := jmrenouard/grafana-tools

# --- Phony Targets ---
# These targets do not produce files as output.
.PHONY: help install lint run build push clean

# --- Targets ---

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help      Show this help message."
	@echo "  install   Install Python dependencies from requirements.txt."
	@echo "  lint      Run pylint on the main script (requires pylint)."
	@echo "  run       Run the dashboard generator. Pass a file with 'make run file=path/to/your.yaml'."
	@echo "  build     Build the Docker image with 'latest' and version tags."
	@echo "  push      Push the Docker image to Docker Hub."
	@echo "  clean     Remove Python cache files."

install:
	pip install -r requirements.txt

lint:
	# Note: You may need to install pylint first (pip install pylint)
	pylint grafana_helper.py

# Example: make run file=examples/linux-overview.yaml
run:
	@if [ -z "$(file)" ]; then \
		echo "Error: Please provide a yaml file. Usage: make run file=<path-to-file.yaml>"; \
		exit 1; \
	fi
	python3 grafana_helper.py --file $(file)

build:
	@echo "Building Docker image ${IMAGE_NAME}:latest and ${IMAGE_NAME}:${VERSION}..."
	docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${VERSION} .

push: build
	@echo "Pushing Docker image ${IMAGE_NAME}:latest and ${IMAGE_NAME}:${VERSION}..."
	docker push ${IMAGE_NAME}:latest
	docker push ${IMAGE_NAME}:${VERSION}

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up Python cache files."
