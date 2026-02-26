# 🚀 Déploiement EduQuP sur Render

Guide complet pour déployer votre plateforme d'éducation avec IA sur Render.

## 📋 Prérequis

- ✅ **Compte Render** : [render.com](https://render.com)
- ✅ **Clé API Gemini** : [Google AI Studio](https://aistudio.google.com/app/apikey)
- ✅ **GitHub Repository** : Votre code poussé sur GitHub

## 💰 Coûts sur Render

- **Web Service** : $7/mois (Starter - 512MB RAM)
- **PostgreSQL** : $7/mois (Starter - 256MB)
- **Redis** : $6/mois (Starter - 30MB)
- **Total** : **$20/mois** (gratuit les 750h premiers mois)

## 🚀 Déploiement étape par étape

### Étape 1 : Préparer le repository

```bash
# Pousser votre code sur GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Étape 2 : Créer les services sur Render

#### A. Base de données PostgreSQL
1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Cliquer "New" → "PostgreSQL"
3. Nom : `edututor-db`
4. Plan : Starter ($7/mois)
5. Créer le service

#### B. Redis
1. Cliquer "New" → "Redis"
2. Nom : `edututor-redis`
3. Plan : Starter ($6/mois)
4. Créer le service

#### C. Application Web
1. Cliquer "New" → "Web Service"
2. Connecter votre repository GitHub
3. Configuration :
   - **Name** : `edututor-web`
   - **Runtime** : `Docker`
   - **Plan** : Starter ($7/mois)
   - **Build Command** : `./build.sh`
   - **Start Command** : `gunicorn edututor_ai.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2`

### Étape 3 : Configurer les variables d'environnement

Dans votre service Web, ajouter ces variables :

```
# Variables obligatoires
GEMINI_API_KEY=votre_clé_api_gemini
DJANGO_SECRET_KEY=votre_clé_secrète_django

# Variables optionnelles (valeurs par défaut)
DEBUG=false
GEMINI_MODEL=gemini-2.5-flash
FREE_DAILY_MESSAGE_LIMIT=25
MAX_UPLOAD_SIZE_MB=10
MESSAGE_PAGE_SIZE=20
SECURE_SSL_REDIRECT=true
SECURE_HSTS_SECONDS=31536000
```

### Étape 4 : Déploiement automatique

1. **Push sur GitHub** → Render déploie automatiquement
2. **Durée** : 3-5 minutes pour le premier déploiement
3. **URL** : `https://edututor-web.onrender.com`

## 🔧 Configuration avancée

### Domaine personnalisé

1. Acheter un domaine (Namecheap, GoDaddy, etc.)
2. Dans Render : Settings → Custom Domain
3. Ajouter votre domaine
4. Configurer les DNS :
   - Type : CNAME
   - Name : `www` (ou `@` pour apex)
   - Value : `edututor-web.onrender.com`

### SSL automatique

Render fournit automatiquement :
- ✅ Certificat SSL Let's Encrypt
- ✅ Renouvellement automatique
- ✅ HTTP → HTTPS redirection

## 📊 Monitoring et logs

### Logs en temps réel
```bash
# Depuis Render Dashboard
# Aller dans votre service → Logs tab
```

### Métriques
- **CPU/RAM** : Dashboard → Metrics
- **Requêtes** : Logs pour analyser le trafic
- **Erreurs** : Alertes automatiques

## 🔄 Mises à jour

### Déploiement automatique
```bash
# Push sur main → déploiement automatique
git add .
git commit -m "New features"
git push origin main
```

### Rollback
- Render Dashboard → Manual Deploy → Rollback to previous

## 🚨 Dépannage

### Problèmes courants

1. **Build échoue**
   ```
   # Vérifier les logs de build
   # Vérifier requirements.txt
   # Vérifier Dockerfile
   ```

2. **Migration échoue**
   ```
   # Vérifier DATABASE_URL
   # Vérifier connexion PostgreSQL
   ```

3. **Static files non chargés**
   ```
   # Vérifier WhiteNoise configuration
   # Vérifier build.sh (collectstatic)
   ```

4. **Timeout de déploiement**
   ```
   # Render a une limite de 15 minutes
   # Optimiser le Dockerfile
   ```

### Commandes de debug

```bash
# Test local avec variables Render
export DATABASE_URL="postgresql://..."
export REDIS_URL="redis://..."
export GEMINI_API_KEY="..."
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🎯 Optimisations pour Render

### Performance
- ✅ **Gunicorn** : 2 workers, 2 threads
- ✅ **WhiteNoise** : Fichiers statiques compressés
- ✅ **PostgreSQL** : Base de données managée
- ✅ **Redis** : Cache et WebSockets

### Sécurité
- ✅ **HTTPS obligatoire**
- ✅ **Variables d'environnement** sécurisées
- ✅ **Headers de sécurité** configurés
- ✅ **Utilisateur non-root** dans Docker

## 📞 Support

- **Documentation Render** : [docs.render.com](https://docs.render.com)
- **Support Render** : support@render.com
- **Issues GitHub** : Créer une issue dans votre repo

---

## 🎉 Checklist de déploiement

- [ ] Repository GitHub créé et poussé
- [ ] Services Render créés (Web, PostgreSQL, Redis)
- [ ] Variables d'environnement configurées
- [ ] Premier déploiement réussi
- [ ] Domaine personnalisé configuré (optionnel)
- [ ] Tests fonctionnels effectués
- [ ] Monitoring configuré

**🚀 Votre plateforme EduQuP est maintenant en ligne sur Render !**