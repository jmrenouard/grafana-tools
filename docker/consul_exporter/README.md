# Consul Exporter

## Description

This directory contains the Dockerized version of the Consul Exporter.

## Usage

### Build the image

```
make build
```

### Run the container

```
make run
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

The following environment variables can be set in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `CONSUL_SERVER` | The address of the Consul server. | `hostname:8500` |
