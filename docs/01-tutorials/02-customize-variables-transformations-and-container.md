# Tutorial 2: Build Custom Panels, Transformations, and Run in Docker

In this tutorial, you create a custom YAML dashboard with variables, all three supported panel types (`stat`, `timeseries`, `gauge`), and `grafana_transforms.py` pipelines, then execute `grafana_helper.py` inside a Docker container.

## Prerequisites

- Working Python environment from [Tutorial 1](01-generate-and-export-first-dashboard.md)
- Optional: Docker Engine (`20.10` or newer) for Step 3

## Step 1: Author a Custom YAML Configuration

Create a temporary file `/tmp/service-health.yaml` using `stat`, `timeseries`, and `gauge` panels plus `sortBy` and `limit` transformations from [`grafana_transforms.py`](../../grafana_transforms.py):

```yaml
dashboard:
  title: "Service Health Lab"
  description: "Tutorial dashboard demonstrating panels and transformations."
  tags: ["tutorial", "prometheus"]
  timezone: "browser"

variables:
  - name: "job"
    label: "Job"
    type: "query"
    datasource: "Prometheus"
    query: "label_values(up, job)"
    multi: false
    includeAll: true

panels:
  - title: "Targets Up"
    type: "stat"
    datasource: "Prometheus"
    gridPos: { h: 4, w: 6, x: 0, y: 0 }
    targets:
      - expr: 'sum(up{job=~"$job"})'
        legendFormat: "Up"

  - title: "Request Latency"
    type: "timeseries"
    datasource: "Prometheus"
    gridPos: { h: 8, w: 18, x: 6, y: 0 }
    options:
      unit: "seconds"
    targets:
      - expr: 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))'
        legendFormat: "p95"
    transformations:
      - type: "sortBy"
        options:
          field: "Value"
          reverse: true
      - type: "limit"
        options:
          limit: 10

  - title: "Memory Usage (%)"
    type: "gauge"
    datasource: "Prometheus"
    gridPos: { h: 6, w: 12, x: 0, y: 8 }
    options:
      unit: "percent"
    targets:
      - expr: '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
        legendFormat: "{{instance}}"
```

## Step 2: Render JSON and Verify Transformation IDs

Generate `/tmp/service-health.json` and confirm all three panels and both transformations appear cleanly:

```bash
python3 grafana_helper.py --file /tmp/service-health.yaml --output /tmp/service-health.json
python3 -c "import json; d = json.load(open('/tmp/service-health.json'))['dashboard']; print([p['type'] for p in d['panels']], [t['id'] for t in d['panels'][1]['transformations']])"
```

Expected output:

```text
['stat', 'timeseries', 'gauge'] ['sortBy', 'limit']
```

## Step 3: Build and Run the Container Image

Build the Docker image (`Dockerfile` copies both `grafana_helper.py` and `grafana_transforms.py`) and render `/tmp/service-health.yaml` via bind mount:

```bash
make build
docker run --rm -v /tmp:/work jmrenouard/grafana-tools:latest --file /work/service-health.yaml --output /work/docker-out.json
```

Expected output:

```text
Dashboard JSON saved to '/work/docker-out.json'.
```

Clean up your temporary files:

```bash
rm -f /tmp/service-health.yaml /tmp/service-health.json /tmp/docker-out.json
```

## Next Steps

- Run operational procedures in [How-To: Run Docker Containers and Extend Panel Types](../02-how-to-guides/run-docker-and-extend-panels.md).
- Inspect supported transformation options in [CLI, YAML Schema & Transformations Reference](../03-reference/cli-yaml-schema-and-transformations.md).
