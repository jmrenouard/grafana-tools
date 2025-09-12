# Monitoring Stack Playbook

This playbook deploys a full monitoring stack on a group of servers.

## Target Hosts

This playbook is designed to run on a group of hosts named `monitoring_servers`. Ensure you have this group defined in your Ansible inventory.

## Roles

This playbook includes the following roles:

-   **`grafana`**: Installs and configures Grafana, the visualization dashboard.
-   **`prometheus`**: Installs and configures Prometheus, the time-series database and monitoring system.
-   **`loki`**: Installs and configures Loki, the log aggregation system.
-   **`node_exporter`**: Installs the Prometheus node exporter to collect system-level metrics.
-   **`metricbeat`**: Installs Metricbeat to collect system and service metrics.

## Configuration

Each role has a `defaults/main.yml` file with variables that you can override in your inventory or playbook to customize the installation.

### Grafana

-   `grafana_version`: The version of Grafana to install.
-   `grafana_config_file`: The path to the Grafana configuration file.
-   `grafana_data_dir`: The path to the Grafana data directory.
-   `grafana_logs_dir`: The path to the Grafana logs directory.
-   `grafana_user`: The user that runs Grafana.
-   `grafana_group`: The group that runs Grafana.
-   `prometheus_datasource_name`: The name of the Prometheus data source in Grafana.
-   `prometheus_datasource_url`: The URL of the Prometheus data source.
-   `loki_datasource_name`: The name of the Loki data source in Grafana.
-   `loki_datasource_url`: The URL of the Loki data source.

### Prometheus

-   `prometheus_version`: The version of Prometheus to install.
-   `prometheus_user`: The user that runs Prometheus.
-   `prometheus_group`: The group that runs Prometheus.
-   `prometheus_config_dir`: The path to the Prometheus configuration directory.
-   `prometheus_data_dir`: The path to the Prometheus data directory.
-   `prometheus_bin_dir`: The path to the Prometheus binaries.
-   `prometheus_config_file`: The path to the Prometheus configuration file.
-   `prometheus_service_file`: The path to the Prometheus systemd service file.

### Loki

-   `loki_version`: The version of Loki to install.
-   `loki_user`: The user that runs Loki.
-   `loki_group`: The group that runs Loki.
-   `loki_config_dir`: The path to the Loki configuration directory.
-   `loki_data_dir`: The path to the Loki data directory.
-   `loki_bin_dir`: The path to the Loki binaries.
-   `loki_config_file`: The path to the Loki configuration file.
-   `loki_service_file`: The path to the Loki systemd service file.

### Node Exporter

-   `node_exporter_version`: The version of Node Exporter to install.
-   `node_exporter_user`: The user that runs Node Exporter.
-   `node_exporter_group`: The group that runs Node Exporter.
-   `node_exporter_bin_dir`: The path to the Node Exporter binaries.
-   `node_exporter_service_file`: The path to the Node Exporter systemd service file.

### Metricbeat

-   `metricbeat_version`: The version of Metricbeat to install.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i <your_inventory_file> ansible/playbooks/monitoring.yml
```

Make sure to replace `<your_inventory_file>` with the path to your Ansible inventory file.
