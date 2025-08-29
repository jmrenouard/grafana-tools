# Playbook de la Stack de Monitoring

Ce playbook déploie une stack de monitoring complète sur un groupe de serveurs.

## Hôtes Cibles

Ce playbook est conçu pour être exécuté sur un groupe d'hôtes nommé `monitoring_servers`. Assurez-vous que ce groupe est défini dans votre inventaire Ansible.

## Rôles

Ce playbook inclut les rôles suivants :

-   **`grafana`**: Installe et configure Grafana, le tableau de bord de visualisation.
-   **`prometheus`**: Installe et configure Prometheus, la base de données de séries temporelles et le système de monitoring.
-   **`loki`**: Installe et configure Loki, le système d'agrégation de logs.
-   **`node_exporter`**: Installe l'exportateur de nœud Prometheus pour collecter les métriques au niveau du système.
-   **`metricbeat`**: Installe Metricbeat pour collecter les métriques du système et des services.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i <votre_fichier_inventaire> ansible/playbooks/monitoring.yml
```

Assurez-vous de remplacer `<votre_fichier_inventaire>` par le chemin de votre fichier d'inventaire Ansible.
