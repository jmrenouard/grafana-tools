#!/bin/bash

# ==============================================================================
# Script 4 : Configuration du Pare-feu UFW
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

# --- Début du script ---
start_script "### Étape 4 : Configuration du Pare-feu UFW ###"

# --- Tests Prérequis ---
info "Vérification des prérequis..."
if ! command -v ufw &>/dev/null; then
    error "UFW n'est pas installé. C'est inhabituel pour Ubuntu. Veuillez vérifier votre système."
fi

if ! ufw status | grep -q "Status: active"; then
    warn "UFW n'est pas actif. Il sera activé à la fin de ce script."
    UFW_WAS_INACTIVE=true
else
    UFW_WAS_INACTIVE=false
fi
success "UFW est disponible."

# --- Configuration des règles ---
info "Configuration des règles de pare-feu..."

# Autoriser SSH pour ne pas se bloquer l'accès !
ufw allow OpenSSH >/dev/null

# Autoriser Nginx HTTP (port 80)
ufw allow 'Nginx HTTP' >/dev/null
success "Règle 'Nginx HTTP' (port 80) autorisée."

# S'assurer que le port 3000 n'est PAS autorisé
if ufw status | grep -q '3000/tcp.*ALLOW'; then
    info "Le port 3000 est actuellement autorisé, il va être supprimé pour des raisons de sécurité."
    ufw delete allow 3000/tcp >/dev/null
    success "Règle pour le port 3000 supprimée."
else
    success "Le port 3000 n'est pas exposé publiquement, ce qui est correct."
fi

# --- Activation / Rechargement ---
if [ "$UFW_WAS_INACTIVE" = true ]; then
    info "Activation de UFW..."
    # L'option --force est nécessaire pour une exécution non-interactive
    ufw --force enable
else
    info "Rechargement des règles UFW..."
    ufw reload >/dev/null
fi
success "Le pare-feu est actif et configuré."

# --- Tests Post-Configuration ---
info "Validation de la configuration UFW..."

UFW_STATUS=$(ufw status verbose)

if ! echo "$UFW_STATUS" | grep -q "80/tcp.*ALLOW IN.*Anywhere (Nginx HTTP)"; then
    error "La règle pour autoriser Nginx HTTP (port 80) n'a pas été correctement appliquée."
fi
success "La règle pour le port 80 est bien présente."

if echo "$UFW_STATUS" | grep -q "3000/tcp.*ALLOW IN"; then
    error "Le port 3000 est toujours exposé ! Problème de sécurité."
fi
success "La règle pour le port 3000 est bien absente (ou bloquée par défaut)."
end_success "Configuration du pare-feu UFW terminée avec succès."