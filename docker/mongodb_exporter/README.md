# MongoDB Exporter

## Description

This directory contains the Dockerized version of the MongoDB Exporter.

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
| `MONGODB_URI` | The URI of the MongoDB server. | `mongodb://hostname:27017` |
