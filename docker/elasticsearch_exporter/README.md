# Elasticsearch Exporter

## Description

This directory contains the Dockerized version of the Elasticsearch Exporter.

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
| `ES_URI` | The URI of the Elasticsearch server. | `http://hostname:9200` |
