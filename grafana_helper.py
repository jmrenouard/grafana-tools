#
# -----------------------------------------------------------------------------
# grafana_helper.py
# -----------------------------------------------------------------------------
#
# Description:
# Outil en ligne de commande pour générer et publier des dashboards Grafana
# à partir d'un fichier de configuration YAML simple.
#
# Auteur: Gemini pour Jean-Marie Renouard
#
# Prérequis:
# pip install grafanalib PyYAML requests
#
# Variables d'environnement requises pour la publication :
# - GRAFANA_URL: L'URL de votre instance Grafana (ex: http://localhost:3000)
# - GRAFANA_API_KEY: Un jeton d'API Grafana avec les droits d'Éditeur.
#
# Utilisation:
# 1. Générer le JSON et l'afficher dans la console :
#    python3 grafana_helper.py --file dashboard.yaml
#
# 2. Générer le JSON et le sauvegarder dans un fichier :
#    python3 grafana_helper.py --file dashboard.yaml --output my-dashboard.json
#
# 3. Générer et publier directement le dashboard dans Grafana :
#    python3 grafana_helper.py --file dashboard.yaml --push
#

import argparse
import json
import os
import sys
import yaml
import requests

from grafanalib.core import (
    Dashboard, GridPos,
    Row, Target, Templating, Template,
    TimeSeries, Stat, GaugePanel, BarGauge,
    SECONDS_FORMAT, BYTES_FORMAT, PERCENT_FORMAT
)

# --- Mapping des unités pour une utilisation simple dans le YAML ---
UNIT_FORMATS = {
    "bytes": BYTES_FORMAT,
    "seconds": SECONDS_FORMAT,
    "percent": PERCENT_FORMAT,
    # Ajoutez d'autres unités ici si nécessaire
}

def create_panel(panel_config):
    """
    Crée un objet panneau Grafanalib à partir d'un dictionnaire de configuration.
    C'est ici que l'on peut étendre l'outil pour supporter plus de types de graphiques.
    """
    panel_type = panel_config.get('type', 'timeseries').lower()
    title = panel_config.get('title', 'N/A')
    grid_pos = panel_config.get('gridPos')
    datasource = panel_config.get('datasource')
    options = panel_config.get('options', {})

    # --- Création de la position et de la taille du panneau ---
    if not grid_pos:
        raise ValueError(f"Le panneau '{title}' n'a pas de 'gridPos' défini.")
    panel_grid_pos = GridPos(
        h=grid_pos.get('h', 8),
        w=grid_pos.get('w', 12),
        x=grid_pos.get('x', 0),
        y=grid_pos.get('y', 0)
    )

    # --- Création des cibles (requêtes) ---
    targets = []
    for target_config in panel_config.get('targets', []):
        targets.append(Target(
            expr=target_config.get('expr'),
            legendFormat=target_config.get('legendFormat', ''),
            refId=target_config.get('refId', 'A'),
            datasource=target_config.get('datasource', datasource) # Utilise la datasource du panneau par défaut
        ))

    # --- Sélection du type de panneau ---
    panel = None
    if panel_type == 'timeseries':
        panel = TimeSeries(
            title=title,
            dataSource=datasource,
            targets=targets,
            gridPos=panel_grid_pos,
            unit=UNIT_FORMATS.get(options.get('unit'))
        )
    elif panel_type == 'stat':
        panel = Stat(
            title=title,
            dataSource=datasource,
            targets=targets,
            gridPos=panel_grid_pos,
            unit=UNIT_FORMATS.get(options.get('unit'))
        )
    elif panel_type == 'gauge':
        panel = GaugePanel(
            title=title,
            dataSource=datasource,
            targets=targets,
            gridPos=panel_grid_pos,
            unit=UNIT_FORMATS.get(options.get('unit'))
        )
    # Ajoutez d'autres types de panneaux ici (elif panel_type == '...':)
    else:
        raise NotImplementedError(f"Le type de panneau '{panel_type}' n'est pas encore supporté.")

    return panel


def generate_dashboard(config):
    """
    Génère l'objet Dashboard Grafanalib complet à partir de la configuration.
    """
    dashboard_config = config.get('dashboard', {})
    
    # --- Création des variables de templating ---
    templates = []
    for var_config in config.get('templating', []):
        templates.append(Template(
            name=var_config.get('name'),
            label=var_config.get('label'),
            dataSource=var_config.get('datasource'),
            query=var_config.get('query'),
            type=var_config.get('type', 'query'),
            multi=var_config.get('multi', False),
            includeAll=var_config.get('includeAll', False),
        ))

    # --- Création des panneaux ---
    panels = [create_panel(p) for p in config.get('panels', [])]

    # --- Assemblage du dashboard ---
    return Dashboard(
        title=dashboard_config.get('title', 'Dashboard sans titre'),
        description=dashboard_config.get('description', ''),
        tags=dashboard_config.get('tags', []),
        timezone=dashboard_config.get('timezone', 'browser'),
        panels=panels,
        templating=Templating(list=templates)
    ).auto_panel_ids()


def push_to_grafana(dashboard_json, grafana_url, api_key):
    """
    Publie le dashboard (au format JSON) sur l'API de Grafana.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = {
        'dashboard': json.loads(dashboard_json),
        'folderId': 0,  # 0 = Dossier "General"
        'overwrite': True
    }
    
    url = f"{grafana_url.rstrip('/')}/api/dashboards/db"
    
    print(f"Publication du dashboard sur {url}...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        
        response_data = response.json()
        print(f"✅ Succès ! Dashboard '{response_data.get('slug')}' publié.")
        print(f"   URL: {grafana_url.rstrip('/')}{response_data.get('url')}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la publication sur Grafana : {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"   Détails de l'erreur : {e.response.json()}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"   Réponse du serveur (non-JSON) : {e.response.text}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Fonction principale du script.
    """
    parser = argparse.ArgumentParser(
        description="Générateur de dashboards Grafana à partir de fichiers YAML."
    )
    parser.add_argument(
        '--file',
        required=True,
        help="Chemin vers le fichier de configuration YAML du dashboard."
    )
    parser.add_argument(
        '--output',
        help="Chemin vers le fichier de sortie pour le JSON généré."
    )
    parser.add_argument(
        '--push',
        action='store_true',
        help="Publier le dashboard directement sur l'API de Grafana."
    )
    args = parser.parse_args()

    # --- Chargement de la configuration YAML ---
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{args.file}' n'a pas été trouvé.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Erreur de syntaxe dans le fichier YAML '{args.file}': {e}", file=sys.stderr)
        sys.exit(1)

    # --- Génération du dashboard ---
    dashboard_obj = generate_dashboard(config)
    
    # La méthode to_json de grafanalib nécessite un `dashboard_cls`
    # Nous le créons ici pour formater correctement le JSON final.
    dashboard_json = json.dumps(
        {
            "dashboard": dashboard_obj.to_json_data(),
            "overwrite": True,
        },
        sort_keys=True,
        indent=2,
        cls=Dashboard.JSONEncoder,
    )

    # --- Actions en fonction des arguments ---
    if args.push:
        grafana_url = os.getenv('GRAFANA_URL')
        api_key = os.getenv('GRAFANA_API_KEY')
        if not grafana_url or not api_key:
            print(
                "Erreur : Les variables d'environnement GRAFANA_URL et GRAFANA_API_KEY "
                "doivent être définies pour publier.",
                file=sys.stderr
            )
            sys.exit(1)
        push_to_grafana(dashboard_json, grafana_url, api_key)
    
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(dashboard_json)
        print(f"Dashboard JSON sauvegardé dans '{args.output}'.")
    
    else:
        # Si aucune action n'est spécifiée, on affiche le JSON
        print(dashboard_json)


if __name__ == "__main__":
    main()

#
# -----------------------------------------------------------------------------
# dashboard.yaml (Exemple de fichier de configuration)
# -----------------------------------------------------------------------------
#
"""
# Métadonnées générales du dashboard
dashboard:
  title: "Statistiques Serveur Prometheus"
  description: "Dashboard de monitoring généré automatiquement."
  tags: ['prometheus', 'serveur', 'autogen']
  timezone: "browser"

# Variables du dashboard (pour le rendre dynamique)
templating:
  - name: "instance"
    label: "Instance"
    type: "query"
    datasource: "Prometheus" # Doit correspondre au nom de votre datasource
    query: "label_values(node_uname_info, instance)"
    multi: true
    includeAll: true

# Définition des panneaux (graphiques)
panels:
  # Premier graphique : CPU Usage
  - title: "Utilisation CPU (%)"
    type: "timeseries"
    datasource: "Prometheus"
    gridPos: { h: 8, w: 12, x: 0, y: 0 }
    options:
      unit: "percent"
    targets:
      - expr: '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle", instance=~"$instance"}[5m])) * 100)'
        legendFormat: "{{instance}}"

  # Second graphique : Mémoire disponible
  - title: "Mémoire Disponible"
    type: "timeseries"
    datasource: "Prometheus"
    gridPos: { h: 8, w: 12, x: 12, y: 0 }
    options:
      unit: "bytes"
    targets:
      - expr: 'node_memory_MemAvailable_bytes{instance=~"$instance"}'
        legendFormat: "{{instance}} - Disponible"
      - expr: 'node_memory_MemFree_bytes{instance=~"$instance"}'
        legendFormat: "{{instance}} - Libre"

  # Troisième panneau : Statistique de la charge système
  - title: "Charge Système (5m)"
    type: "stat"
    datasource: "Prometheus"
    gridPos: { h: 4, w: 6, x: 0, y: 8 }
    targets:
      - expr: 'node_load5{instance=~"$instance"}'
        legendFormat: "{{instance}}"

  # Quatrième panneau : Espace disque
  - title: "Espace Disque Utilisé (%)"
    type: "gauge"
    datasource: "Prometheus"
    gridPos: { h: 4, w: 6, x: 6, y: 8 }
    options:
      unit: "percent"
    targets:
      - expr: '(1 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs", instance=~"$instance"} / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs", instance=~"$instance"})) * 100'
        legendFormat: "{{instance}} - {{device}}"
"""

#
# -----------------------------------------------------------------------------
# requirements.txt
# -----------------------------------------------------------------------------
#
"""
grafanalib
PyYAML
requests
"""

#
# -----------------------------------------------------------------------------
# README.md
# -----------------------------------------------------------------------------
#
"""
# Générateur de Dashboard Grafana

Ce projet fournit un outil en ligne de commande pour générer et publier des dashboards Grafana à partir de fichiers de configuration YAML simples.

## 🚀 Installation

1.  **Clonez ou copiez les fichiers** de ce projet, notamment `grafana_helper.py`.

2.  **Installez les dépendances Python** requises :
    ```bash
    pip install -r requirements.txt
    ```
    (Le contenu de `requirements.txt` est : `grafanalib`, `PyYAML`, `requests`)

## ⚙️ Configuration

### Variables d'environnement

Pour pouvoir publier un dashboard (`--push`), vous devez configurer les variables d'environnement suivantes :

-   `GRAFANA_URL`: L'URL complète de votre instance Grafana (ex: `http://grafana.imporelec.local`).
-   `GRAFANA_API_KEY`: Un jeton d'API Grafana. Vous pouvez en créer un dans `Configuration > API Keys` avec le rôle `Editor`.

```bash
export GRAFANA_URL="http://localhost:3000"
export GRAFANA_API_KEY="ey..."
```

### Fichier de configuration YAML

Créez un fichier `.yaml` (par exemple, `dashboard.yaml`) pour décrire votre dashboard. La structure est expliquée dans le fichier d'exemple fourni.

## 🕹️ Utilisation

L'outil s'utilise en ligne de commande.

### Afficher le JSON généré

Pour voir le JSON du dashboard qui serait généré, sans le sauvegarder ni le publier.

```bash
python3 grafana_helper.py --file dashboard.yaml
```

### Sauvegarder le JSON dans un fichier

Utile pour l'archivage ou le débogage.

```bash
python3 grafana_helper.py --file dashboard.yaml --output mon-dashboard.json
```

### Publier le dashboard sur Grafana

Pour créer ou mettre à jour le dashboard directement dans votre instance Grafana.

```bash
python3 grafana_helper.py --file dashboard.yaml --push
```

## ✨ Étendre l'outil

Pour ajouter le support de nouveaux types de panneaux (ex: `barchart`, `table`), il suffit de modifier la fonction `create_panel` dans le script `grafana_helper.py` en y ajoutant une nouvelle condition `elif`.
"""
