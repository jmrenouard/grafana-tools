# Loki

## Description

This directory contains the Dockerized version of Loki.

## Usage

### Build the image

```
make build
```

### Run the container

To run the container, you need to provide a `loki-config.yaml` configuration file.

```
make run
```

*Note*: The `run` command in the `Makefile` is a basic example. You will need to mount your `loki-config.yaml` file to `/etc/loki/loki-config.yaml` in the container.

Example:
```
docker run -d --name loki -p 3100:3100 -v $(PWD)/loki-config.yaml:/etc/loki/loki-config.yaml grafana/loki
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

This service does not require any specific environment variables in the `.env` file. Configuration is done via the `loki-config.yaml` file.
