# Playbook Metricbeat

Ce playbook installe et configure Metricbeat.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i inventory/hosts playbooks/metricbeat.yml
```

## Tâches

- Installe le paquet Metricbeat.
- Démarre et active le service Metricbeat.

## Gestionnaires

- Redémarre le service Metricbeat en cas de modification de la configuration.
