# Export and Publish Dashboards to Grafana

## Prerequisites

- Install Python `3.9` or newer on the host.
- Install dependencies from [`requirements.txt`](../../requirements.txt).
- Obtain a Grafana instance URL and an Editor API token.
- Confirm your YAML configuration file exists in `examples/` or locally.

## Procedure

### Export a JSON Backup Snapshot

1. Validate the YAML syntax and export the dashboard JSON file.

```bash
python3 grafana_helper.py --file examples/linux-overview.yaml --output linux-overview.json
```

2. Inspect the exported file to verify the dashboard title and panel count.

```bash
python3 -c "import json; d = json.load(open('linux-overview.json'))['dashboard']; print(d['title'], len(d['panels']))"
```

### Publish a Dashboard with the Grafana API

CAUTION: Export or commit a JSON backup before you publish. The `--push` flag enables `overwrite` in Grafana and replaces any dashboard with the same title.

1. Set the required Grafana environment variables in your shell session.

```bash
export GRAFANA_URL="http://localhost:3000"
export GRAFANA_API_KEY="glsa_replace_with_token"
```

NOTE: `push_to_grafana` sends the token as a Bearer authorization header to `/api/dashboards/db` with a `10` second timeout.

2. Verify that `GRAFANA_URL` responds cleanly before you push changes.

```bash
curl -fsS "${GRAFANA_URL%/}/api/health"
```

3. Push the dashboard YAML file to the Grafana General folder.

```bash
python3 grafana_helper.py --file examples/linux-overview.yaml --push
```

4. If the HTTP request fails with status `401` or `403`, create a new Editor token and export `GRAFANA_API_KEY`.

## Validation

Confirm the command prints the `Success:` status and a valid dashboard URL. Then open that URL in Grafana or query the search endpoint:

```bash
curl -fsS -H "Authorization: Bearer ${GRAFANA_API_KEY}" "${GRAFANA_URL%/}/api/search?query=Linux"
```

## Rollback

1. If the published dashboard breaks queries or panels, check out the previous YAML revision from Git.

```bash
git show HEAD~1:examples/linux-overview.yaml > /tmp/linux-overview-rollback.yaml
```

2. Push the previous YAML revision to restore the stable dashboard in Grafana.

```bash
python3 grafana_helper.py --file /tmp/linux-overview-rollback.yaml --push
```

3. Remove the temporary YAML and JSON files from your local directory.

```bash
rm -f /tmp/linux-overview-rollback.yaml linux-overview.json
```

## Related Documentation

- [CLI, YAML Schema & Transformations Reference](../03-reference/cli-yaml-schema-and-transformations.md)
- [Architecture, Pipeline & API Design](../04-explanation/architecture-yaml-pipeline-and-api-design.md)
