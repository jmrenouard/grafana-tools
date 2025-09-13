# SNMP Exporter

## Description

This directory contains the Dockerized version of the SNMP Exporter.

## Usage

### Build the image

```
make build
```

### Run the container

To run the container, you need to provide a `snmp.yml` configuration file.

```
make run
```

*Note*: The `run` command in the `Makefile` is a basic example. You will need to mount your `snmp.yml` file to `/etc/snmp_exporter/snmp.yml` in the container.

Example:
```
docker run -d --name snmp-exporter -p 9116:9116 -v $(PWD)/snmp.yml:/etc/snmp_exporter/snmp.yml prom/snmp-exporter
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

This service does not require any specific environment variables in the `.env` file. Configuration is done via the `snmp.yml` file.
