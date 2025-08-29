# Grafana Playbook

This playbook installs and configures Grafana.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i inventory/hosts playbooks/grafana.yml
```

## Tasks

- Installs the Grafana package.
- Starts and enables the Grafana service.

## Handlers

- Restarts the Grafana service on configuration changes.
