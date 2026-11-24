# Tutorial 1: Generate and Export Your First Dashboard

In this tutorial, you install the Python dependencies, render [`examples/linux-overview.yaml`](../../examples/linux-overview.yaml) into Grafana JSON, save an archival snapshot with `--output`, and confirm how panels and transformations serialize.

## Prerequisites

- Python `3.9` or newer
- Repository dependencies (`grafanalib`, `PyYAML`, `requests`)

Install the dependencies and verify the CLI version:

```bash
pip install -r requirements.txt
python3 grafana_helper.py --version
```

Expected output:

```text
grafana_helper.py 1.0.1
```

## Step 1: Preview Dashboard JSON in Stdout

Run `grafana_helper.py` on [`examples/linux-overview.yaml`](../../examples/linux-overview.yaml) without `--output` or `--push`:

```bash
python3 grafana_helper.py --file examples/linux-overview.yaml
```

The command prints a formatted JSON document containing:

- Top-level keys `"dashboard"` and `"overwrite": true`.
- `dashboard.title`: `"Linux Server Overview"`.
- `dashboard.templating.list`: One `instance` query variable.
- `dashboard.panels`: Six panels with automatically assigned panel IDs (`1` through `6`).

## Step 2: Export an Archival JSON Snapshot

Save the generated payload to a local file for backup, code review, or GitOps archiving:

```bash
python3 grafana_helper.py --file examples/linux-overview.yaml --output linux-overview.json
```

Expected output:

```text
Dashboard JSON saved to 'linux-overview.json'.
```

Verify the saved JSON structure and inspect the `Memory Usage` panel transformations (`merge` and `filterFieldsByName`):

```bash
python3 -c "import json; d = json.load(open('linux-overview.json'))['dashboard']; print(d['title'], len(d['panels']), [t['id'] for t in d['panels'][4]['transformations']])"
```

Expected output:

```text
Linux Server Overview 6 ['merge', 'filterFieldsByName']
```

## Step 3: Validate All Repository Example Dashboards

Iterate over all `21` files in [`examples/`](../../examples/linux-overview.yaml) to verify every bundled dashboard parses cleanly:

```bash
python3 -c "import glob, subprocess, sys; [subprocess.run([sys.executable, 'grafana_helper.py', '--file', f], check=True, stdout=subprocess.DEVNULL) for f in sorted(glob.glob('examples/*.yaml'))]; print('Validated 21 examples')"
```

Remove your temporary snapshot when finished:

```bash
rm -f linux-overview.json
```

## Next Steps

- Complete [Tutorial 2: Build Custom Panels, Transformations, and Run in Docker](02-customize-variables-transformations-and-container.md).
- Follow [How-To: Export and Publish Dashboards to Grafana](../02-how-to-guides/export-and-publish-dashboards.md) for API publishing and rollback.
