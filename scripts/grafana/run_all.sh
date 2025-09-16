#!/bin/bash

# ==============================================================================
# Script Maître pour l'installation de Grafana avec Nginx en Reverse Proxy
# Auteur : Gemini
# Version : 1.0
# ==============================================================================

# Arrêter le script en cas d'erreur
set -e
set -o pipefail

# --- Définition des couleurs ---
C_RESET='\033[0m'
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'

# --- Fonctions d'affichage ---
info() {
    echo -e "${C_BLUE}[INFO]${C_RESET} $1"
}

success() {
    echo -e "${C_GREEN}[SUCCESS]${C_RESET} $1"
}

error() {
    echo -e "${C_RED}[ERROR]${C_RESET} $1" >&2
    exit 1
}

# --- Vérification des prérequis ---
info "Vérification des prérequis..."

# 1. Vérifier si le script est exécuté en tant que root
if [[ $EUID -ne 0 ]]; then
   error "Ce script doit être exécuté en tant que root. Utilisez 'sudo ./run_all.sh'"
fi

# 2. Vérifier si les scripts enfants existent et sont exécutables
SCRIPTS_DIR=$(dirname "$0")
SCRIPTS=(
    "01_install_grafana.sh"
    "02_install_nginx.sh"
    "03_configure_nginx_proxy.sh"
    "04_configure_firewall.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ ! -f "${SCRIPTS_DIR}/${script}" ] || [ ! -x "${SCRIPTS_DIR}/${script}" ]; then
        error "Le script '${script}' est manquant ou non exécutable. Assurez-vous d'avoir fait 'chmod +x *.sh'."
    fi
done

success "Prérequis validés."
echo "------------------------------------------------------------------"

# --- Exécution des scripts ---
info "Lancement du processus d'installation complet."

for script in "${SCRIPTS[@]}"; do
    info "Exécution du script : ${script}..."
    if ! "${SCRIPTS_DIR}/${script}"; then
        error "L'exécution de ${script} a échoué. Arrêt du processus."
    fi
    success "Le script ${script} s'est terminé avec succès."
    echo "------------------------------------------------------------------"
done

# --- Message Final ---
echo
success "🎉 L'installation et la configuration de Grafana avec Nginx sont terminées !"
info "Vous pouvez maintenant accéder à Grafana via http://localhost ou http://$(hostname -I | awk '{print $1}')"
echo
