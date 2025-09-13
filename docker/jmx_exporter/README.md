# JMX Exporter

## Description

This directory contains the Dockerized version of the JMX Exporter.

## Usage

The JMX Exporter runs as a Java agent and needs to be attached to a running JVM. The `run` command in the `Makefile` is a placeholder.

Please refer to the [JMX Exporter documentation](https://github.com/prometheus/jmx_exporter) for instructions on how to use it with your Java application.

### Build the image

```
make build
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

This service does not require any specific environment variables in the `.env` file. Configuration is done via a YAML file passed to the Java agent.
