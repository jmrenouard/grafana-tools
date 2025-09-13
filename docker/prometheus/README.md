# Prometheus

## Description

This directory contains the Dockerized version of Prometheus.

## Usage

### Build the image

```
make build
```

### Run the container

To run the container, you need to provide a `prometheus.yml` configuration file.

```
make run
```

*Note*: The `run` command in the `Makefile` is a basic example. You will need to mount your `prometheus.yml` file to `/etc/prometheus/prometheus.yml` in the container.

Example:
```
docker run -d --name prometheus -p 9090:9090 -v $(PWD)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

### Stop the container

```
make stop
```

### View logs

```
make logs
```

## Parameters

This service does not require any specific environment variables in the `.env` file. Configuration is done via the `prometheus.yml` file.
