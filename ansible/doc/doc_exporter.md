# Exporter Playbook

This playbook installs and configures the Prometheus Node Exporter.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i inventory/hosts playbooks/exporter.yml
```

## Tasks

- Installs the Prometheus Node Exporter package.
- Starts and enables the Prometheus Node Exporter service.

## Handlers

- Restarts the Prometheus Node Exporter service on configuration changes.
