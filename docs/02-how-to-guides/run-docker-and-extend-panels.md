# Run Docker Containers and Extend Panel Types

## Prerequisites

- Install Docker Engine `20.10` or newer for container builds.
- Install `make` and `pylint` if you run `Makefile` targets locally.
- Read [`grafana_helper.py`](../../grafana_helper.py) and [`grafana_transforms.py`](../../grafana_transforms.py).

## Procedure

### Build and Run the Container Image

1. Build the local image with `Makefile`.

```bash
make build
```

NOTE: The image version tag comes from `__version__` inside `grafana_helper.py`.

2. Confirm the container prints CLI help with both Python modules packaged.

```bash
docker run --rm jmrenouard/grafana-tools:latest --help
```

3. Mount your workspace directory into `/work` and render a dashboard file.

```bash
docker run --rm \
  -v "$(pwd):/work" \
  jmrenouard/grafana-tools:latest \
  --file /work/examples/linux-overview.yaml --output /work/docker-dashboard.json
```

4. To publish from the container, pass `GRAFANA_URL` and `GRAFANA_API_KEY` as environment flags without literal secrets.

```bash
docker run --rm \
  -v "$(pwd):/work" \
  -e GRAFANA_URL="${GRAFANA_URL}" \
  -e GRAFANA_API_KEY="${GRAFANA_API_KEY}" \
  jmrenouard/grafana-tools:latest \
  --file /work/examples/linux-overview.yaml --push
```

### Add a Panel Type Safely

1. Open `grafana_helper.py` and locate the `_PANEL_TYPES` map.
2. Import the new `grafanalib.core` panel class at the top of `grafana_helper.py`.
3. Add an entry to `_PANEL_TYPES` for the YAML `type` string, panel class, format parameter, and default unit.

CAUTION: Preserve `gridPos` and `transformations` keys in `create_panel`. Incorrect arguments cause `TypeError` failures across dashboard YAML files.

4. Run the test suite and linter to verify compatibility across all `examples/` files.

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
make lint
```

## Validation

Confirm the test suite reports zero failures and `pylint` passes cleanly. Remove any generated local artifact:

```bash
rm -f docker-dashboard.json
```

## Rollback

If a custom panel change breaks tests or image builds, discard the local edits and rebuild the image:

```bash
git checkout -- grafana_helper.py
make build
```

## Related Documentation

- [CLI, YAML Schema & Transformations Reference](../03-reference/cli-yaml-schema-and-transformations.md)
- [Architecture, Pipeline & API Design](../04-explanation/architecture-yaml-pipeline-and-api-design.md)
