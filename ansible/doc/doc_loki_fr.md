# Playbook Loki

Ce playbook installe et configure Loki.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i inventory/hosts playbooks/loki.yml
```

## Tâches

- Installe le paquet Loki.
- Démarre et active le service Loki.

## Gestionnaires

- Redémarre le service Loki en cas de modification de la configuration.
