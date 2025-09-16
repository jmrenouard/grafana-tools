Voici le guide tutoriel complet pour déployer Grafana (OSS) derrière un reverse proxy Nginx local sur Ubuntu 24.04.

-----

## 🐧 Partie 1 : Installation de Grafana (OSS)

Cette section couvre l'installation de la version Open Source de Grafana via le référentiel APT officiel.

### 1.1. Prérequis et Ajout du Référentiel APT

Nous devons d'abord installer les dépendances nécessaires et la clé GPG du référentiel Grafana.

```bash
# Installer les paquets prérequis
sudo apt install -y apt-transport-https software-properties-common wget

# Importer la clé GPG de Grafana
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Ajouter le référentiel Grafana (stable)
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Mettre à jour le cache APT
sudo apt update
```

### 1.2. Installation de Grafana

Maintenant, nous pouvons installer le paquet `grafana`.

```bash
# Installer Grafana OSS
sudo apt install -y grafana
```

### 1.3. Démarrage et Activation du Service

Une fois l'installation terminée, nous démarrons le service `grafana-server` et l'activons pour qu'il se lance au démarrage du système.

```bash
# Recharger le daemon systemd
sudo systemctl daemon-reload

# Démarrer le service Grafana
sudo systemctl start grafana-server

# Activer le service au démarrage
sudo systemctl enable grafana-server
```

### 1.4. Vérification Locale

Vérifions que Grafana fonctionne correctement sur son port par défaut (`3000`).

```bash
# Vérifier le statut du service
sudo systemctl status grafana-server
```

Utilisez `curl` pour confirmer que le service répond en local sur le port 3000.

```bash
# Cette commande devrait retourner du HTML (probablement une redirection)
curl -I http://localhost:3000
```

Vous devriez voir une réponse de type `HTTP/1.1 302 Found`, vous redirigeant vers `/login`.

-----

## 🚀 Partie 2 : Installation de Nginx

Nous installons Nginx, qui agira comme notre reverse proxy.

```bash
# Installer le paquet Nginx complet
sudo apt install -y nginx
```

-----

## ⚙️ Partie 3 : Configuration de Nginx en Reverse Proxy (Local)

Nous allons maintenant configurer Nginx pour qu'il reçoive les requêtes sur le port 80 et les transmette à Grafana sur le port 3000.

### 3.1. Création du Fichier de Configuration

Créez un nouveau fichier de configuration pour votre site Grafana local.

```bash
sudo nano /etc/nginx/sites-available/grafana-local
```

### 3.2. Bloc de Configuration Nginx

Collez la configuration suivante dans le fichier que vous venez d'ouvrir. Elle est configurée pour l'accès `localhost` ou via l'IP directe du serveur.

```nginx
server {
    listen 80;
    # Utilise 'localhost' si vous y accédez depuis la machine elle-même.
    # Utilisez '_' pour écouter sur toutes les adresses IP du serveur.
    server_name localhost; 

    # Configuration du reverse proxy pour Grafana
    location / {
        # Transférer la requête au service Grafana local
        proxy_pass http://localhost:3000;

        # Définir les en-têtes essentiels pour le proxy
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3.3. Activation du Site et Test

Nous devons activer ce nouveau site en créant un lien symbolique et (optionnellement) désactiver le site par défaut.

```bash
# Créer le lien symbolique pour activer le site
sudo ln -s /etc/nginx/sites-available/grafana-local /etc/nginx/sites-enabled/

# Optionnel : Supprimer le site par défaut s'il n'est pas utilisé
# sudo rm /etc/nginx/sites-enabled/default

# Tester la syntaxe de la configuration Nginx
sudo nginx -t
```

Si tout est correct, vous devriez voir :
`nginx: the configuration file /etc/nginx/nginx.conf syntax is ok`
`nginx: configuration file /etc/nginx/nginx.conf test is successful`

-----

## 🛡️ Partie 4 : Configuration du Pare-feu (UFW)

Nous configurons le pare-feu `ufw` (Uncomplicated Firewall) pour autoriser le trafic HTTP (port 80) tout en gardant le port 3000 fermé au public.

### 4.1. Autoriser Nginx

Nous utilisons le profil d'application "Nginx HTTP" qui gère le port 80.

```bash
# Autoriser le trafic sur le port 80
sudo ufw allow 'Nginx HTTP'
```

### 4.2. Sécurisation du Port 3000

**Important** : N'ouvrez pas le port 3000 (ex: `ufw allow 3000`). Nginx accède à Grafana *localement* (via `localhost:3000`). Le port 3000 n'a pas besoin d'être exposé à l'extérieur, ce qui améliore la sécurité.

Si le port 3000 était déjà ouvert, fermez-le :
`sudo ufw delete allow 3000/tcp`

### 4.3. Activation ou Rechargement d'UFW

Si UFW n'est pas encore actif, activez-le. S'il l'est déjà, rechargez-le.

```bash
# Pour activer UFW (si ce n'est pas déjà fait)
sudo ufw enable

# Ou pour recharger les règles si UFW est déjà actif
sudo ufw reload
```

-----

## ✅ Partie 5 : Finalisation et Vérification

### 5.1. Redémarrage des Services

Appliquons toutes les modifications en redémarrant Nginx et Grafana.

```bash
sudo systemctl restart nginx
sudo systemctl restart grafana-server
```

### 5.2. Vérification Finale

Ouvrez votre navigateur web et accédez à :

  * `http://localhost` (si vous êtes sur la machine)
  * ou `http://<IP_de_votre_serveur>` (si vous y accédez depuis une autre machine sur le même réseau)

Vous devriez maintenant voir la page de connexion de Grafana, servie par Nginx sur le port 80 standard.

Le login par défaut est :

  * **Utilisateur :** `admin`
  * **Mot de passe :** `admin`

Il vous sera demandé de changer ce mot de passe lors de la première connexion. Votre installation est terminée.