# Loki Playbook

This playbook installs and configures Loki.

## Usage

To run this playbook, use the following command:

```bash
ansible-playbook -i inventory/hosts playbooks/loki.yml
```

## Tasks

- Installs the Loki package.
- Starts and enables the Loki service.

## Handlers

- Restarts the Loki service on configuration changes.
