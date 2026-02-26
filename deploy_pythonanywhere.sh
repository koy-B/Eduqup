#!/bin/bash

# Script de déploiement pour PythonAnywhere
# À exécuter dans la console Bash de PythonAnywhere

echo "🚀 Déploiement EduQuP sur PythonAnywhere"

# Créer un virtualenv si nécessaire
if [ ! -d "~/.virtualenvs/edututor" ]; then
    echo "📦 Création du virtualenv..."
    mkvirtualenv --python=python3.10 edututor
fi

# Activer le virtualenv
workon edututor

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt

# Configuration de la base de données
echo "🗄️  Configuration de la base de données..."
python manage.py migrate

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur (optionnel)
echo "👤 Voulez-vous créer un superutilisateur ? (y/N)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

echo "✅ Déploiement terminé !"
echo "🌐 Configurez maintenant l'application web dans l'interface PythonAnywhere"