"""CLI tool to generate and publish Grafana dashboards from YAML files."""

# Keep the package version double-quoted on a single line for Makefile/CI grep.
__version__ = "1.0.1"

import argparse
import json
import os
import sys

import requests
import yaml
from grafanalib._gen import DashboardEncoder
from grafanalib.core import (
    BYTES_FORMAT,
    PERCENT_FORMAT,
    SECONDS_FORMAT,
    Dashboard,
    GaugePanel,
    GridPos,
    Stat,
    Target,
    Template,
    Templating,
    TimeSeries,
)

from grafana_transforms import TRANSFORMATIONS_MAP

# Unit mappings from readable YAML names to grafanalib format constants.
UNIT_FORMATS = {
    "bytes": BYTES_FORMAT,
    "seconds": SECONDS_FORMAT,
    "percent": PERCENT_FORMAT,
}

_PANEL_TYPES = {
    "timeseries": (TimeSeries, "unit", ""),
    "stat": (Stat, "format", "none"),
    "gauge": (GaugePanel, "format", "none"),
}


def _build_transformations(panel_config, title):
    """Build grafanalib transformation instances for a single panel definition."""
    transformations = []
    for t_config in panel_config.get("transformations") or []:
        t_type = t_config.get("type")
        if not t_type:
            raise ValueError(f"Transformation on panel '{title}' is missing 'type'.")

        transform_class = TRANSFORMATIONS_MAP.get(t_type)
        if not transform_class:
            raise NotImplementedError(f"Transformation type '{t_type}' is not supported.")

        transform_options = t_config.get("options") or {}
        try:
            transformations.append(transform_class(**transform_options))
        except TypeError as exc:
            raise ValueError(
                f"Invalid options for transformation '{t_type}' on panel '{title}': {exc}"
            ) from exc
    return transformations


def _build_grid_pos(panel_config, title):
    """Validate and construct a GridPos instance from a panel configuration."""
    grid_pos = panel_config.get("gridPos")
    if not isinstance(grid_pos, dict):
        raise ValueError(f"Panel '{title}' must define a 'gridPos' mapping.")
    return GridPos(
        h=grid_pos.get("h", 8),
        w=grid_pos.get("w", 12),
        x=grid_pos.get("x", 0),
        y=grid_pos.get("y", 0),
    )


def _build_targets(panel_config, default_datasource):
    """Build grafanalib Target queries, falling back to the panel datasource."""
    targets = []
    for target_config in panel_config.get("targets") or []:
        targets.append(
            Target(
                expr=target_config.get("expr"),
                legendFormat=target_config.get("legendFormat", ""),
                refId=target_config.get("refId", "A"),
                datasource=target_config.get("datasource", default_datasource),
            )
        )
    return targets


def create_panel(panel_config):
    """Create a grafanalib panel object from a dashboard YAML panel dictionary."""
    if not isinstance(panel_config, dict):
        raise ValueError("Each panel entry must be a mapping.")

    panel_type = str(panel_config.get("type", "timeseries")).lower()
    if panel_type not in _PANEL_TYPES:
        raise NotImplementedError(f"Panel type '{panel_type}' is not supported yet.")

    title = panel_config.get("title", "N/A")
    datasource = panel_config.get("datasource")
    options = panel_config.get("options") or {}

    panel_cls, format_arg, default_unit = _PANEL_TYPES[panel_type]
    unit_value = UNIT_FORMATS.get(options.get("unit"), default_unit)
    panel_kwargs = {
        "title": title,
        "dataSource": datasource,
        "targets": _build_targets(panel_config, datasource),
        "gridPos": _build_grid_pos(panel_config, title),
        "transformations": _build_transformations(panel_config, title),
        format_arg: unit_value,
    }
    return panel_cls(**panel_kwargs)


def generate_dashboard(config):
    """Generate a complete grafanalib Dashboard instance from parsed YAML config."""
    if not isinstance(config, dict):
        raise ValueError("Dashboard YAML root must be a mapping.")

    dashboard_config = config.get("dashboard") or {}
    if not isinstance(dashboard_config, dict):
        raise ValueError("The 'dashboard' section must be a mapping.")

    templates = []
    for var_config in config.get("variables") or []:
        templates.append(
            Template(
                name=var_config.get("name"),
                label=var_config.get("label"),
                dataSource=var_config.get("datasource"),
                query=var_config.get("query"),
                type=var_config.get("type", "query"),
                multi=var_config.get("multi", False),
                includeAll=var_config.get("includeAll", False),
            )
        )

    panels = [create_panel(panel) for panel in (config.get("panels") or [])]

    return Dashboard(
        title=dashboard_config.get("title", "Untitled Dashboard"),
        description=dashboard_config.get("description", ""),
        tags=dashboard_config.get("tags", []),
        timezone=dashboard_config.get("timezone", "browser"),
        panels=panels,
        templating=Templating(list=templates),
    ).auto_panel_ids()


def _unwrap_dashboard_payload(dashboard_json):
    """Extract the inner dashboard model so /api/dashboards/db never double-nests."""
    parsed = json.loads(dashboard_json) if isinstance(dashboard_json, str) else dashboard_json
    if isinstance(parsed, dict) and "dashboard" in parsed and isinstance(parsed["dashboard"], dict):
        return parsed["dashboard"]
    return parsed


def push_to_grafana(dashboard_json, grafana_url, api_key):
    """Publish a generated dashboard JSON payload to the Grafana HTTP API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "dashboard": _unwrap_dashboard_payload(dashboard_json),
        "folderId": 0,  # 0 targets the built-in General folder.
        "overwrite": True,
    }

    url = f"{grafana_url.rstrip('/')}/api/dashboards/db"

    print(f"Publishing dashboard to {url}...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()

        response_data = response.json()
        print(f"Success: dashboard '{response_data.get('slug')}' published.")
        print(f"URL: {grafana_url.rstrip('/')}{response_data.get('url')}")

    except requests.exceptions.RequestException as exc:
        print(f"Error publishing dashboard to Grafana: {exc}", file=sys.stderr)
        if hasattr(exc, "response") and exc.response is not None:
            try:
                print(f"Error details: {exc.response.json()}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"Server response (non-JSON): {exc.response.text}", file=sys.stderr)
        sys.exit(1)


def build_parser():
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate and publish Grafana dashboards from YAML files."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the dashboard YAML configuration file.",
    )
    parser.add_argument(
        "--output",
        help="Path to write the generated dashboard JSON file.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Publish the generated dashboard directly to the Grafana HTTP API.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {globals()['__' + 'version__']}",
    )
    return parser


def main():
    """CLI entry point for YAML loading, JSON serialization, export, and publish."""
    args = build_parser().parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' was not found.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"YAML syntax error in '{args.file}': {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        dashboard_obj = generate_dashboard(config)
    except (ValueError, NotImplementedError) as exc:
        print(f"Dashboard generation error in '{args.file}': {exc}", file=sys.stderr)
        sys.exit(1)

    # Encode the wrapped payload structure expected by JSON backups and --push.
    dashboard_json = json.dumps(
        {
            "dashboard": dashboard_obj.to_json_data(),
            "overwrite": True,
        },
        sort_keys=True,
        indent=2,
        cls=DashboardEncoder,
    )

    if args.push:
        grafana_url = os.getenv("GRAFANA_URL")
        api_key = os.getenv("GRAFANA_API_KEY")
        if not grafana_url or not api_key:
            print(
                "Error: Both GRAFANA_URL and GRAFANA_API_KEY environment variables "
                "must be set to publish.",
                file=sys.stderr,
            )
            sys.exit(1)
        push_to_grafana(dashboard_json, grafana_url, api_key)

    elif args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(dashboard_json)
        print(f"Dashboard JSON saved to '{args.output}'.")

    else:
        print(dashboard_json)


if __name__ == "__main__":
    main()
