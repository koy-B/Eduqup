#!/bin/bash

# Script de build pour Render
# Ce script s'exécute après le build Docker mais avant le démarrage

set -e

echo "🏗️  Build script pour Render - EduQuP"

# Appliquer les migrations de base de données
echo "📊 Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Créer les répertoires nécessaires s'ils n'existent pas
mkdir -p static media

# Vérifications de sécurité
echo "🔒 Vérifications de sécurité..."
python manage.py check --deploy

echo "✅ Build terminé avec succès !"