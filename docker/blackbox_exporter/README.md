# Blackbox Exporter

## Description

This directory contains the Dockerized version of the Blackbox Exporter.

## Usage

### Build the image

```
make build
```

### Run the container

To run the container, you need to provide a `blackbox.yml` configuration file.

```
make run
```

*Note*: The `run` command in the `Makefile` is a basic example. You will need to mount your `blackbox.yml` file to `/etc/blackbox_exporter/blackbox.yml` in the container.

Example:
```
docker run -d --name blackbox-exporter -p 9115:9115 -v $(PWD)/blackbox.yml:/etc/blackbox_exporter/blackbox.yml prom/blackbox-exporter
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

This service does not require any specific environment variables in the `.env` file. Configuration is done via the `blackbox.yml` file.
