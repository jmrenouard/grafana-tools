# Grafana

## Description

This directory contains the Dockerized version of Grafana.

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
| `GF_SECURITY_ADMIN_PASSWORD` | The admin password for Grafana. | `admin` |
