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

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i <your_inventory_file> ansible/playbooks/monitoring.yml
```

Make sure to replace `<your_inventory_file>` with the path to your Ansible inventory file.
