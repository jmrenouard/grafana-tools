# Memcached Exporter

## Description

This directory contains the Dockerized version of the Memcached Exporter.

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
| `MEMCACHED_ADDR` | The address of the Memcached server. | `hostname:11211` |
