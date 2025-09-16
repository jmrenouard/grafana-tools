#!/bin/bash

# ==============================================================================
# Script 1 : Installation de la stack de monitoring (Grafana, Prometheus, etc.)
# ==============================================================================

set -e
set -o pipefail
# --- Couleurs et Fonctions ---
C_RESET='\033[0m'; C_RED='\033[0;31m'; C_GREEN='\033[0;32m'; C_YELLOW='\033[0;33m'; C_BLUE='\033[0;34m'
info() { echo -e    "${C_BLUE}[INFO   ]${C_RESET}ℹ️ $1"; }
success() { echo -e "${C_GREEN}[SUCCESS]${C_RESET}✅ $1"; }
warn() { echo -e    "${C_YELLOW}[WARN   ]${C_RESET}⚠️ $1"; }
error() { echo -e   "${C_RED}[ERROR  ]${C_RESET}❌ $1" >&2; echo ".... Fin le script avec une erreur"; exit 1; }
start_script() { echo -e "${C_BLUE}[START  ]${C_RESET}🏁 $1🚀"; }
end_success() { echo -e "${C_GREEN}[END    ]${C_RESET}🏁 $1"; exit 0; }
# --- Liste des Paquets ---
PCK_LIST="grafana
prometheus
prometheus-node-exporter
prometheus-alertmanager
prometheus-pushgateway
prometheus-process-exporter
net-tools
jq
curl
vim
htop
nload
nmap
git
unzip
zip
python3
python3-pip
python3-venv
python3-prometheus-client
pigz
pv
sysstat
bind9-dnsutils"

# --- Début du script ---
start_script "### Étape 1 : Installation de la Stack de Monitoring ###"

# --- Tests Prérequis ---
info "Vérification des prérequis..."
if command -v grafana-server &>/dev/null || command -v prometheus &>/dev/null; then
    warn "Grafana ou Prometheus semble déjà installé. Le script va s'assurer que tous les paquets sont présents."
fi
success "Prérequis validés."

# --- Installation ---
info "Mise à jour du cache APT et installation des dépendances..."
apt-get update >/dev/null
apt-get install software-properties-common apt-transport-https wget gpg -y &>/dev/null|| error "L'installation des dépendances a échoué."

info "Configuration du référentiel Grafana..."
rm -f /etc/apt/sources.list.d/grafana.list
mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | tee /etc/apt/keyrings/grafana.gpg > /dev/null || error "Échec du téléchargement ou du traitement de la clé GPG de Grafana."
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list

info "Mise à jour de la liste des paquets..."
apt-get update &>/dev/null || error "La mise à jour de la liste des paquets a échoué."
success "Le cache APT a été mis à jour."

info "Installation de la suite de paquets..."
for pck in $PCK_LIST; do
  echo " * Installation de $pck..."
  apt-get install -y "$pck" &>/dev/null || error "L'installation du paquet '$pck' a échoué."
  success "Le paquet '$pck' a été installé avec succès."
done
success "Tous les paquets ont été installés."

# --- Démarrage et Activation des Services ---
info "Démarrage et activation des services principaux..."
systemctl daemon-reload

systemctl enable grafana-server
systemctl start grafana-server || error "Le démarrage du service grafana-server a échoué."
success "Le service grafana-server a été démarré et activé."

# --- Pause pour démarrage ---
info "Pause de 10 secondes pour laisser le temps aux services de démarrer complètement..."
sleep 10s

# --- Tests Post-Installation ---
info "Validation de l'installation..."
# Validation Grafana
if ! systemctl is-active --quiet grafana-server; then error "Le service grafana-server n'a pas pu démarrer."; fi
if ! ss -tuln | grep -q ':3000'; then error "Grafana n'écoute pas sur le port 3000."; fi
if ! curl -s -I http://localhost:3000 | grep -q "HTTP/1.1 302 Found"; then error "La réponse de Grafana sur localhost:3000 est inattendue."; fi
success "Grafana est actif et répond correctement."

systemctl enable prometheus
systemctl start prometheus || error "Le démarrage du service prometheus a échoué."
success "Le service prometheus a été démarré et activé."

# --- Pause pour démarrage ---
info "Pause de 10 secondes pour laisser le temps aux services de démarrer complètement..."
sleep 10s

# Validation Prometheus
if ! systemctl is-active --quiet prometheus; then error "Le service prometheus n'a pas pu démarrer."; fi
if ! ss -tuln | grep -q ':9090'; then error "Prometheus n'écoute pas sur le port 9090."; fi
if ! curl -s -I http://localhost:9090/classic/status | grep -q "HTTP/1.1 405 Method Not Allowed"; then error "La réponse de Prometheus sur localhost:9090 est inattendue."; fi
success "Prometheus est actif et répond correctement."
end_success "Installation et validation de la stack de monitoring terminées avec succès."