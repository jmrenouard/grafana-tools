# Playbook Grafana

Ce playbook installe et configure Grafana.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i inventory/hosts playbooks/grafana.yml
```

## Tâches

- Installe le paquet Grafana.
- Démarre et active le service Grafana.

## Gestionnaires

- Redémarre le service Grafana en cas de modification de la configuration.
