# Redis Exporter

## Description

This directory contains the Dockerized version of the Redis Exporter.

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
| `REDIS_ADDR` | The address of the Redis server. | `redis://hostname:6379` |
