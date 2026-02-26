#!/bin/bash

# Script de déploiement pour EduQuP
# Utilisation: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
PROJECT_NAME="edututor"
DOMAIN="yourdomain.com"

echo "🚀 Déploiement de EduQuP en $ENVIRONMENT"

# Vérifier les prérequis
command -v docker >/dev/null 2>&1 || { echo "❌ Docker n'est pas installé"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose n'est pas installé"; exit 1; }

# Créer le répertoire de déploiement
DEPLOY_DIR="/opt/$PROJECT_NAME"
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR

# Copier les fichiers
echo "📁 Copie des fichiers..."
cp -r . $DEPLOY_DIR/
cd $DEPLOY_DIR

# Configuration de l'environnement
if [ "$ENVIRONMENT" = "production" ]; then
    cp .env.production .env
    echo "⚠️  Éditez le fichier .env avec vos vraies valeurs !"
    echo "   - DJANGO_SECRET_KEY"
    echo "   - GEMINI_API_KEY"
    echo "   - DATABASE_URL"
    echo "   - EMAIL_*"
fi

# Construire et démarrer les conteneurs
echo "🐳 Construction des conteneurs..."
docker-compose build

echo "🗄️  Initialisation de la base de données..."
docker-compose up -d db redis
sleep 10

# Appliquer les migrations
echo "📊 Application des migrations..."
docker-compose run --rm web python manage.py migrate

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
docker-compose run --rm web python manage.py collectstatic --noinput

# Créer un superutilisateur (optionnel)
read -p "Voulez-vous créer un superutilisateur ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose run --rm web python manage.py createsuperuser
fi

# Démarrer tous les services
echo "🚀 Démarrage des services..."
docker-compose up -d

# Configuration SSL (Let's Encrypt)
read -p "Voulez-vous configurer SSL avec Let's Encrypt ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔒 Configuration SSL..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
fi

echo "✅ Déploiement terminé !"
echo "🌐 Votre site est accessible sur : https://$DOMAIN"
echo ""
echo "📋 Commandes utiles :"
echo "  - Logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Redémarrer: docker-compose restart"
echo "  - Backup DB: docker-compose exec db pg_dump -U edututor edututor_db > backup.sql"