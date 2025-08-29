# Playbook Exporter

Ce playbook installe et configure l'exportateur de nœuds Prometheus.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i inventory/hosts playbooks/exporter.yml
```

## Tâches

- Installe le paquet de l'exportateur de nœuds Prometheus.
- Démarre et active le service de l'exportateur de nœuds Prometheus.

## Gestionnaires

- Redémarre le service de l'exportateur de nœuds Prometheus en cas de modification de la configuration.
