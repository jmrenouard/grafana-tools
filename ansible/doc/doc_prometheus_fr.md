# Playbook Prometheus

Ce playbook installe et configure Prometheus.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i inventory/hosts playbooks/prometheus.yml
```

## Tâches

- Installe le paquet Prometheus.
- Démarre et active le service Prometheus.

## Gestionnaires

- Redémarre le service Prometheus en cas de modification de la configuration.
