#!/bin/bash

# ==============================================================================
# Script 3 : Configuration de Nginx en Reverse Proxy
# ==============================================================================

set -e
set -o pipefail

# --- Couleurs et Fonctions ---
C_RESET='\033[0m'; C_RED='\033[0;31m'; C_GREEN='\033[0;32m'; C_YELLOW='\033[0;33m'; C_BLUE='\033[0;34m'
info() { echo -e "${C_BLUE}[INFO]${C_RESET} $1"; }
success() { echo -e "${C_GREEN}[SUCCESS]${C_RESET} $1"; }
warn() { echo -e "${C_YELLOW}[WARNING]${C_RESET} $1"; }
error() { echo -e "${C_RED}[ERROR]${C_RESET} $1" >&2; exit 1; }

# --- Constantes ---
NGINX_CONF_FILE="/etc/nginx/sites-available/grafana-local"
NGINX_ENABLED_LINK="/etc/nginx/sites-enabled/grafana-local"
DEFAULT_SITE_LINK="/etc/nginx/sites-enabled/default"

# --- Début du script ---
info "### Étape 3 : Configuration de Nginx en Reverse Proxy ###"

# --- Tests Prérequis ---
info "Vérification des prérequis..."
if ! command -v nginx &>/dev/null; then
    error "Nginx n'est pas installé. Veuillez exécuter le script 02_install_nginx.sh d'abord."
fi
success "Nginx est bien installé."

# --- Création du Fichier de Configuration ---
info "Création du fichier de configuration Nginx pour Grafana..."

if [ -f "$NGINX_CONF_FILE" ]; then
    warn "Le fichier de configuration '${NGINX_CONF_FILE}' existe déjà. Il ne sera pas modifié."
else
    cat <<EOF > "$NGINX_CONF_FILE"
server {
    listen 80;
    server_name localhost _; # Écoute sur localhost et toutes les IPs

    # Désactiver les logs d'accès pour moins de verbosité si souhaité
    access_log off;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    success "Fichier de configuration créé : ${NGINX_CONF_FILE}"
fi

# --- Activation du Site ---
info "Activation du site Grafana..."
if [ -L "$NGINX_ENABLED_LINK" ]; then
    warn "Le lien symbolique '${NGINX_ENABLED_LINK}' existe déjà."
else
    ln -s "$NGINX_CONF_FILE" "$NGINX_ENABLED_LINK"
    success "Site Grafana activé."
fi

# --- Désactivation du Site par Défaut ---
if [ -L "$DEFAULT_SITE_LINK" ]; then
    info "Désactivation du site Nginx par défaut..."
    rm "$DEFAULT_SITE_LINK"
    success "Site par défaut désactivé."
fi

# --- Tests Post-Configuration ---
info "Validation de la configuration Nginx..."

# 1. Tester la syntaxe de la configuration
if ! nginx -t; then
    error "La syntaxe de la configuration Nginx est invalide. Veuillez vérifier le fichier ${NGINX_CONF_FILE}."
fi
success "Syntaxe de la configuration Nginx valide."

# 2. Redémarrer Nginx pour appliquer les changements
info "Redémarrage de Nginx..."
systemctl restart nginx
success "Nginx a été redémarré."

# 3. Valider l'accès via le proxy
info "Test de l'accès à Grafana via le reverse proxy..."
# Le curl doit maintenant retourner la redirection de Grafana via le port 80
if ! curl -s -I http://localhost | grep -q "HTTP/1.1 302 Found"; then
    error "Le reverse proxy Nginx ne semble pas fonctionner correctement. La réponse de http://localhost est inattendue."
fi
success "Le reverse proxy Nginx fonctionne et redirige vers la page de login de Grafana."
