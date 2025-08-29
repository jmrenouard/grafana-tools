# Grafana Dashboard Generator

This project provides a command-line tool to generate and publish Grafana dashboards from simple YAML configuration files.

## 🚀 Installation

1.  **Clone or copy the files** from this project, especially `grafana_helper.py`.

2.  **Install the required Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🐳 Docker Usage

A Docker image is available to run the tool without installing Python or dependencies directly.

### Pull the image

```bash
docker pull jmrenouard/grafana-tools:latest
```

### Run the tool

To use the tool with Docker, you need to mount your current directory (containing your `dashboard.yaml`) into the container and pass the required environment variables.

```bash
docker run --rm \
  -v $(pwd):/app \
  -e GRAFANA_URL="http://your-grafana-url" \
  -e GRAFANA_API_KEY="your-api-key" \
  jmrenouard/grafana-tools:latest \
  --file dashboard.yaml --push
```

## ⚙️ Configuration

### Environment Variables

To publish a dashboard (`--push`), you must configure the following environment variables:

-   `GRAFANA_URL`: The full URL of your Grafana instance (e.g., `http://grafana.imporelec.local`).
-   `GRAFANA_API_KEY`: A Grafana API token. You can create one in `Configuration > API Keys` with the `Editor` role.

```bash
export GRAFANA_URL="http://localhost:3000"
export GRAFANA_API_KEY="ey..."
```

### YAML Configuration File

Create a `.yaml` file (e.g., `dashboard.yaml`) to describe your dashboard. An example file is provided in the comments of the `grafana_helper.py` script.

## 🕹️ Usage

The tool is used via the command line.

### Display the generated JSON

To see the dashboard JSON that would be generated, without saving or publishing it.

```bash
python3 grafana_helper.py --file dashboard.yaml
```

### Save the JSON to a file

Useful for archiving or debugging.

```bash
python3 grafana_helper.py --file dashboard.yaml --output my-dashboard.json
```

### Publish the dashboard to Grafana

To create or update the dashboard directly in your Grafana instance.

```bash
python3 grafana_helper.py --file dashboard.yaml --push
```

## ✨ Extending the tool

To add support for new panel types (e.g., `barchart`, `table`), simply modify the `create_panel` function in the `grafana_helper.py` script by adding a new `elif` condition.
