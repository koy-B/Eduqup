# 🚀 Déploiement d'EduQuP

Guide complet pour héberger votre plateforme d'éducation avec IA.

## 📋 Prérequis

- **Serveur Linux** (Ubuntu 20.04+ recommandé)
- **Docker & Docker Compose** installés
- **Domaine** pointant vers votre serveur
- **Clé API Gemini** configurée

## 🏗️ Options d'hébergement

### 1. **VPS (Recommandé pour débutants)**
- **DigitalOcean**: $6/mois (1GB RAM)
- **Linode**: $5/mois (1GB RAM)
- **Vultr**: $2.50/mois (512MB RAM)

### 2. **Cloud Managed**
- **Heroku**: Facile, mais cher (~$7/mois)
- **Railway**: Moderne, payant à l'usage
- **Render**: Bon compromis (~$7/mois)

### 3. **Auto-hébergement**
- Votre propre serveur (VPS ou dédié)

## 🚀 Déploiement Rapide (Docker)

### Étape 1: Préparation du serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Redémarrer la session
newgrp docker
```

### Étape 2: Déploiement

```bash
# Cloner votre projet (ou uploader les fichiers)
git clone https://github.com/yourusername/edututor.git
cd edututor

# Copier la configuration de production
cp .env.production .env

# Éditer la configuration
nano .env  # Remplir avec vos vraies valeurs
```

### Étape 3: Lancement

```bash
# Construire et démarrer
docker-compose up -d

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic --noinput

# Créer un admin (optionnel)
docker-compose exec web python manage.py createsuperuser
```

## 🔒 Configuration SSL (HTTPS)

### Avec Let's Encrypt (Gratuit)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir le certificat
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Le certificat se renouvelle automatiquement
```

## 📊 Base de données

Le déploiement utilise PostgreSQL en production (plus robuste que SQLite).

### Sauvegarde

```bash
# Sauvegarde quotidienne
docker-compose exec db pg_dump -U edututor edututor_db > backup_$(date +%Y%m%d).sql

# Restauration
docker-compose exec -T db psql -U edututor edututor_db < backup.sql
```

## 📈 Monitoring

### Logs

```bash
# Logs de l'application
docker-compose logs -f web

# Logs Nginx
docker-compose logs -f nginx

# Logs base de données
docker-compose logs -f db
```

### Métriques

- **Uptime**: `docker-compose ps`
- **Utilisation CPU/RAM**: `docker stats`
- **Espace disque**: `df -h`

## 🔧 Maintenance

### Mise à jour

```bash
# Arrêter les services
docker-compose down

# Mettre à jour le code
git pull origin main

# Redémarrer
docker-compose up -d

# Appliquer les migrations si nécessaire
docker-compose exec web python manage.py migrate
```

### Redémarrage

```bash
# Redémarrage propre
docker-compose restart

# Redémarrage forcé
docker-compose down && docker-compose up -d
```

## 🚨 Dépannage

### Problèmes courants

1. **Port 80/443 occupé**
   ```bash
   sudo netstat -tulpn | grep :80
   sudo systemctl stop apache2  # Si Apache tourne
   ```

2. **Erreur de base de données**
   ```bash
   docker-compose logs db
   docker-compose restart db
   ```

3. **Erreur SSL**
   ```bash
   sudo certbot certificates
   sudo certbot renew
   ```

4. **Mémoire insuffisante**
   ```bash
   # Ajouter du swap
   sudo fallocate -l 1G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## 💰 Coûts estimés

- **VPS (1GB RAM)**: $5-10/mois
- **Domaine**: $10-15/an
- **SSL**: Gratuit (Let's Encrypt)
- **Email**: $0-5/mois (Gmail)
- **Total**: ~$20-30/mois

## 🎯 Checklist de déploiement

- [ ] Serveur configuré avec Docker
- [ ] Domaine pointant vers le serveur
- [ ] Clé API Gemini configurée
- [ ] Variables d'environnement définies
- [ ] SSL configuré
- [ ] Base de données migrée
- [ ] Fichiers statiques collectés
- [ ] Superutilisateur créé
- [ ] Tests fonctionnels effectués

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs: `docker-compose logs`
2. Testez localement d'abord
3. Vérifiez la configuration réseau/firewall
4. Consultez la documentation Django/Docker

---

**🎉 Félicitations !** Votre plateforme EduQuP est maintenant en ligne !