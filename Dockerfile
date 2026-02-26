# Dockerfile optimisé pour Render
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Créer le répertoire de l'application
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Créer les répertoires nécessaires
RUN mkdir -p /app/static /app/media

# Exposer le port (Render utilise la variable $PORT)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# Commande de démarrage (sera remplacée par render.yaml)
CMD ["gunicorn", "edututor_ai.wsgi:application", "--bind", "0.0.0.0:10000", "--workers", "2", "--threads", "2"]