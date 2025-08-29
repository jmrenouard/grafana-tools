# Prometheus Playbook

This playbook installs and configures Prometheus.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i inventory/hosts playbooks/prometheus.yml
```

## Tasks

- Installs the Prometheus package.
- Starts and enables the Prometheus service.

## Handlers

- Restarts the Prometheus service on configuration changes.
