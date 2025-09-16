#!/bin/bash

# ==============================================================================
# Script 2 : Installation de Nginx
# ==============================================================================

set -e
set -o pipefail

# --- Couleurs et Fonctions ---
C_RESET='\033[0m'; C_RED='\033[0;31m'; C_GREEN='\033[0;32m'; C_YELLOW='\033[0;33m'; C_BLUE='\033[0;34m'
info() { echo -e "${C_BLUE}[INFO]${C_RESET} $1"; }
success() { echo -e "${C_GREEN}[SUCCESS]${C_RESET} $1"; }
warn() { echo -e "${C_YELLOW}[WARNING]${C_RESET} $1"; }
error() { echo -e "${C_RED}[ERROR]${C_RESET} $1" >&2; exit 1; }

# --- Début du script ---
info "### Étape 2 : Installation de Nginx ###"

# --- Tests Prérequis ---
info "Vérification des prérequis pour Nginx..."

if command -v nginx &>/dev/null; then
    warn "Nginx semble déjà installé."
else
    # --- Installation ---
    info "Installation de Nginx..."
    apt-get update &>/dev/null
    apt-get install -y nginx &>/dev/null
    success "Nginx a été installé."
fi

# --- Démarrage et Activation du Service ---
systemctl start nginx
systemctl enable nginx

# --- Tests Post-Installation ---
info "Validation de l'installation de Nginx..."

# 1. Vérifier si le service est actif
if ! systemctl is-active --quiet nginx; then
    error "Le service nginx n'a pas pu démarrer."
fi
success "Le service nginx est actif."

# 2. Vérifier si le service est activé au démarrage
if ! systemctl is-enabled --quiet nginx; then
    warn "Le service nginx n'est pas activé au démarrage."
else
    success "Le service nginx est activé au démarrage."
fi

# 3. Vérifier si le port 80 est en écoute
if ! ss -tuln | grep -q ':80'; then
    error "Nginx n'écoute pas sur le port 80."
fi
success "Nginx écoute bien sur le port 80."

# 4. Vérifier la réponse HTTP locale
info "Test de la réponse HTTP sur http://localhost..."
if ! curl -s -I http://localhost | grep -q "HTTP/1.1 200 OK"; then
    warn "La réponse de la page par défaut de Nginx sur localhost est inattendue (ce n'est pas grave à ce stade)."
else
    success "Nginx répond correctement avec sa page par défaut."
fi
