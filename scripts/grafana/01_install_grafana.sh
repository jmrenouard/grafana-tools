#!/bin/bash

# ==============================================================================
# Script 1 : Installation de Grafana OSS
# ==============================================================================

set -e
set -o pipefail

# --- Couleurs et Fonctions (dupliqué pour l'exécution autonome) ---
C_RESET='\033[0m'; C_RED='\033[0;31m'; C_GREEN='\033[0;32m'; C_YELLOW='\033[0;33m'; C_BLUE='\033[0;34m'
info() { echo -e "${C_BLUE}[INFO]${C_RESET} $1"; }
success() { echo -e "${C_GREEN}[SUCCESS]${C_RESET} $1"; }
warn() { echo -e "${C_YELLOW}[WARNING]${C_RESET} $1"; }
error() { echo -e "${C_RED}[ERROR]${C_RESET} $1" >&2; exit 1; }

# --- Début du script ---
info "### Étape 1 : Installation de Grafana ###"

# --- Tests Prérequis ---
info "Vérification des prérequis pour Grafana..."

if command -v grafana-server &>/dev/null; then
    warn "Grafana semble déjà installé. Poursuite pour assurer la configuration."
else
    if ! command -v wget &>/dev/null; then
        error "'wget' n'est pas installé. Veuillez l'installer avec 'sudo apt install wget'."
    fi
    if ! command -v gpg &>/dev/null; then
        error "'gpg' n'est pas installé. Veuillez l'installer avec 'sudo apt install gpg'."
    fi
    success "Prérequis pour l'installation validés."

    # --- Installation ---
    info "Ajout du référentiel APT de Grafana..."
    apt-get install -y apt-transport-https software-properties-common &>/dev/null
    mkdir -p /etc/apt/keyrings/
    wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | tee /etc/apt/keyrings/grafana.gpg > /dev/null
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
    
    info "Mise à jour des paquets et installation de Grafana..."
    apt-get update #&>/dev/null
    apt-get install -y grafana #&>/dev/null
    success "Grafana a été installé."
fi

# --- Démarrage et Activation du Service ---
info "Démarrage et activation du service grafana-server..."
systemctl daemon-reload
systemctl start grafana-server
systemctl enable grafana-server

# --- Tests Post-Installation ---
info "Validation de l'installation de Grafana..."

# 1. Vérifier si le service est actif
if ! systemctl is-active --quiet grafana-server; then
    error "Le service grafana-server n'a pas pu démarrer."
fi
success "Le service grafana-server est actif."

# 2. Vérifier si le service est activé au démarrage
if ! systemctl is-enabled --quiet grafana-server; then
    warn "Le service grafana-server n'est pas activé au démarrage."
else
    success "Le service grafana-server est activé au démarrage."
fi

# 3. Vérifier si le port 3000 est en écoute
if ! ss -tuln | grep -q ':3000'; then
    error "Grafana n'écoute pas sur le port 3000."
fi
success "Grafana écoute bien sur le port 3000."

# 4. Vérifier la réponse HTTP locale
info "Test de la réponse HTTP sur http://localhost:3000..."
if ! curl -s -I http://localhost:3000 | grep -q "HTTP/1.1 302 Found"; then
    error "La réponse de Grafana sur localhost:3000 est inattendue."
fi
success "Grafana répond correctement en local."
