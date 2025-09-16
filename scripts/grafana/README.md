# **Scripts d'Installation Automatisée : Grafana \+ Nginx sur Ubuntu 24.04**

## **🎯 Objectif**

Cette collection de scripts permet d'installer et de configurer automatiquement Grafana (OSS) avec Nginx en tant que reverse proxy local sur un serveur Ubuntu 24.04.

L'accès final se fera via http://localhost (ou http://\<IP\_DU\_SERVEUR\>) sur le port 80\.

## **📦 Fichiers**

* run\_all.sh: Script principal qui exécute tous les autres scripts dans l'ordre.  
* 01\_install\_grafana.sh: Installe la stack de monitoring Grafana (prometheus, alert-manage, grafana-server).  
* 02\_install\_nginx.sh: Installe Nginx.  
* 03\_configure\_nginx\_proxy.sh: Configure Nginx en reverse proxy.  
* 04\_configure\_firewall.sh: Configure le pare-feu UFW.

## **🚀 Utilisation**

1. Rendre les scripts exécutables :  
   Assurez-vous que tous les fichiers .sh sont dans le même répertoire.  
   chmod \+x \*.sh

2. Lancer l'installation :  
   Exécutez le script principal avec les privilèges sudo.  
   sudo ./run\_all.sh

Le script vous guidera à travers chaque étape, en effectuant des tests avant et après chaque opération majeure. En cas d'erreur, l'exécution s'arrêtera.

## **✔️ Validation Finale**

Une fois que le script run\_all.sh est terminé avec succès, vous pouvez vérifier l'installation en ouvrant votre navigateur et en accédant à :

* http://localhost (si vous êtes sur le serveur)  
* http://\<IP\_DE\_VOTRE\_SERVEUR\> (depuis une autre machine)

Les identifiants Grafana par défaut sont admin / admin.