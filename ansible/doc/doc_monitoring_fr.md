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

## Configuration

Chaque rôle a un fichier `defaults/main.yml` avec des variables que vous pouvez surcharger dans votre inventaire ou votre playbook pour personnaliser l'installation.

### Grafana

-   `grafana_version`: La version de Grafana à installer.
-   `grafana_config_file`: Le chemin vers le fichier de configuration de Grafana.
-   `grafana_data_dir`: Le chemin vers le répertoire de données de Grafana.
-   `grafana_logs_dir`: Le chemin vers le répertoire de logs de Grafana.
-   `grafana_user`: L'utilisateur qui exécute Grafana.
-   `grafana_group`: Le groupe qui exécute Grafana.
-   `prometheus_datasource_name`: Le nom de la source de données Prometheus dans Grafana.
-   `prometheus_datasource_url`: L'URL de la source de données Prometheus.
-   `loki_datasource_name`: Le nom de la source de données Loki dans Grafana.
-   `loki_datasource_url`: L'URL de la source de données Loki.

### Prometheus

-   `prometheus_version`: La version de Prometheus à installer.
-   `prometheus_user`: L'utilisateur qui exécute Prometheus.
-   `prometheus_group`: Le groupe qui exécute Prometheus.
-   `prometheus_config_dir`: Le chemin vers le répertoire de configuration de Prometheus.
-   `prometheus_data_dir`: Le chemin vers le répertoire de données de Prometheus.
-   `prometheus_bin_dir`: Le chemin vers les binaires de Prometheus.
-   `prometheus_config_file`: Le chemin vers le fichier de configuration de Prometheus.
-   `prometheus_service_file`: Le chemin vers le fichier de service systemd de Prometheus.

### Loki

-   `loki_version`: La version de Loki à installer.
-   `loki_user`: L'utilisateur qui exécute Loki.
-   `loki_group`: Le groupe qui exécute Loki.
-   `loki_config_dir`: Le chemin vers le répertoire de configuration de Loki.
-   `loki_data_dir`: Le chemin vers le répertoire de données de Loki.
-   `loki_bin_dir`: Le chemin vers les binaires de Loki.
-   `loki_config_file`: Le chemin vers le fichier de configuration de Loki.
-   `loki_service_file`: Le chemin vers le fichier de service systemd de Loki.

### Node Exporter

-   `node_exporter_version`: La version de Node Exporter à installer.
-   `node_exporter_user`: L'utilisateur qui exécute Node Exporter.
-   `node_exporter_group`: Le groupe qui exécute Node Exporter.
-   `node_exporter_bin_dir`: Le chemin vers les binaires de Node Exporter.
-   `node_exporter_service_file`: Le chemin vers le fichier de service systemd de Node Exporter.

### Metricbeat

-   `metricbeat_version`: La version de Metricbeat à installer.

## Utilisation

Pour exécuter ce playbook, utilisez la commande suivante :

```bash
ansible-playbook -i <votre_fichier_inventaire> ansible/playbooks/monitoring.yml
```

Assurez-vous de remplacer `<votre_fichier_inventaire>` par le chemin de votre fichier d'inventaire Ansible.
