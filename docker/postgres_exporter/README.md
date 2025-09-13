# Postgres Exporter

## Description

This directory contains the Dockerized version of the Postgres Exporter.

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
| `DATA_SOURCE_NAME` | The data source name for the PostgreSQL connection. | `postgresql://user:password@hostname:5432/postgres?sslmode=disable` |
