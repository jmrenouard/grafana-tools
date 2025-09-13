# Metricbeat Playbook

This playbook installs and configures Metricbeat.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i inventory/hosts playbooks/metricbeat.yml
```

## Tasks

- Installs the Metricbeat package.
- Starts and enables the Metricbeat service.

## Handlers

- Restarts the Metricbeat service on configuration changes.
