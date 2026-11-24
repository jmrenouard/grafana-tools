# CLI, YAML Schema, Transformations & Examples

## CLI Flags (`grafana_helper.py` v1.0.1)

| Flag | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `--file FILE` | Yes | — | Path to input dashboard YAML file |
| `--output OUTPUT` | No | — | Output path for formatted dashboard JSON |
| `--push` | No | `False` | Publish JSON payload to `$GRAFANA_URL/api/dashboards/db` |
| `--version` | No | — | Print `grafana_helper.py 1.0.1` and exit |
| `-h`, `--help` | No | — | Show usage and exit |

## Environment Variables (`--push` Only)

| Variable | Format | Purpose |
| :--- | :--- | :--- |
| `GRAFANA_URL` | `http(s)://host[:port]` | Base Grafana server URL (trailing `/` trimmed) |
| `GRAFANA_API_KEY` | Editor API token / SA token | Sent in `Authorization: Bearer <token>` header |

## YAML Top-Level Schema

| Section | Type | Fields |
| :--- | :--- | :--- |
| `dashboard` | Mapping | `title` (default `"Untitled Dashboard"`), `description`, `tags` (list), `timezone` (default `"browser"`) |
| `variables` | List of mappings | `name`, `label`, `type` (default `"query"`), `datasource`, `query`, `multi` (`False`), `includeAll` (`False`) |
| `panels` | List of mappings | `title`, `type`, `datasource`, `gridPos` (`h`, `w`, `x`, `y`), `options.unit`, `targets` (`expr`, `legendFormat`, `refId`, optional `datasource`), `transformations` |

## Supported Panel Types & Units

| `type` Value | `grafanalib.core` Class | Unit Argument | Default When Omitted |
| :--- | :--- | :--- | :--- |
| `timeseries` | `TimeSeries` | `unit` | `""` |
| `stat` | `Stat` | `format` | `"none"` |
| `gauge` | `GaugePanel` | `format` | `"none"` |

Supported `options.unit` keys (`UNIT_FORMATS` in [`grafana_helper.py`](../../grafana_helper.py)):

| YAML `options.unit` | `grafanalib.core` Constant |
| :--- | :--- |
| `bytes` | `BYTES_FORMAT` |
| `seconds` | `SECONDS_FORMAT` |
| `percent` | `PERCENT_FORMAT` |

## Transformation Registry (`grafana_transforms.py`)

`TRANSFORMATIONS_MAP` defines `17` Grafana transformation builders:

| YAML `type` | Class | Grafana `id` | Constructor Arguments (`options`) |
| :--- | :--- | :--- | :--- |
| `filterByName` | `FilterByName` | `filterFieldsByName` | `include=None` |
| `filterByValue` | `FilterByValue` | `filterByValue` | `field`, `operator`, `value` |
| `filterByQuery` | `FilterByQuery` | `filterByRefId` | `refIds` |
| `merge` | `Merge` | `merge` | *(none)* |
| `outerJoin` | `OuterJoin` | `outerJoin` | `field` |
| `addFieldFromCalculation` | `AddFieldFromCalculation` | `addFieldFromCalculation` | `mode`, `reducer`, `expression=None` |
| `reduce` | `Reduce` | `reduce` | `reducer` |
| `groupBy` | `GroupBy` | `groupBy` | `fields`, `aggregations` |
| `organize` | `Organize` | `organize` | `renameByName=None`, `sortBy=None` |
| `labelsToFields` | `LabelsToFields` | `labelsToFields` | `labels=None`, `valueLabel=None` |
| `seriesToRows` | `SeriesToRows` | `seriesToRows` | *(none)* |
| `convertFieldType` | `ConvertFieldType` | `convertFieldType` | `field`, `targetType` |
| `groupToNestedTable` | `GroupToNestedTable` | `groupToNestedTable` | `key` |
| `sortBy` | `SortBy` | `sortBy` | `field`, `reverse=False` |
| `limit` | `Limit` | `limit` | `limit` |
| `extractFields` | `ExtractFields` | `extractFields` | `source`, `regex`, `rename=None` |
| `debug` | `Debug` | `debug` | *(none)* |

## Bundled Example Dashboards (`examples/`, 21 Files)

| Category | YAML Files |
| :--- | :--- |
| **Linux (`4`)** | `linux-overview.yaml`, `linux-detailed.yaml`, `linux-network.yaml`, `linux-disk.yaml` |
| **MySQL / MariaDB (`3`)** | `mysql-overview.yaml`, `mysql-performance.yaml`, `mysql-replication.yaml` |
| **PostgreSQL (`3`)** | `postgresql-overview.yaml`, `postgresql-performance.yaml`, `postgresql-database-stats.yaml` |
| **Cassandra (`2`)** | `cassandra-overview.yaml`, `cassandra-cluster.yaml` |
| **MongoDB (`2`)** | `mongodb-overview.yaml`, `mongodb-atlas.yaml` |
| **Nginx (`3`)** | `nginx-overview.yaml`, `nginx-requests.yaml`, `nginx-performance.yaml` |
| **App & Social (`4`)** | `sql-app-metrics.yaml`, `app-sales-dashboard.yaml`, `social-linkedin-analytics.yaml`, `social-x-analytics.yaml` |

## HTTP API Contract (`--push`)

- **Method & Path:** `POST {GRAFANA_URL}/api/dashboards/db`
- **Headers:** `Authorization: Bearer {GRAFANA_API_KEY}`, `Content-Type: application/json`, `Accept: application/json`
- **Payload Keys:** `dashboard` (unwrapped dashboard object), `folderId: 0` (`General`), `overwrite: true`
- **Request Timeout:** `10` seconds
