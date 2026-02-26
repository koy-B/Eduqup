# 🚀 Déploiement EduQuP sur PythonAnywhere

Guide complet pour déployer votre plateforme d'éducation avec IA sur PythonAnywhere.

## 📋 Prérequis

- ✅ **Compte PythonAnywhere** : [pythonanywhere.com](https://www.pythonanywhere.com)
- ✅ **Clé API Gemini** : [Google AI Studio](https://aistudio.google.com/app/apikey)
- ✅ **Plan payant** : Hacker ($9/mois) minimum pour les WebSockets

## 💰 Coûts sur PythonAnywhere

- **Beginner** : $0/mois (limité, pas recommandé)
- **Hacker** : $9/mois (recommandé - 512MB RAM, MySQL)
- **Expert** : $24/mois (plus de ressources)
- **Total** : **$9/mois** + domaine optionnel

## 🚀 Déploiement étape par étape

### Étape 1 : Créer un compte PythonAnywhere

1. Aller sur [pythonanywhere.com](https://www.pythonanywhere.com)
2. Créer un compte (Beginner gratuit pour commencer)
3. **Important** : Upgrade vers Hacker ($9/mois) pour :
   - MySQL database
   - WebSockets support
   - Plus de stockage

### Étape 2 : Préparer votre code local

```bash
# Depuis votre ordinateur local
# Uploader les fichiers sur PythonAnywhere via Git ou FTP

# Ou utiliser Git directement sur PythonAnywhere
git clone https://github.com/yourusername/edututor.git
```

### Étape 3 : Configuration sur PythonAnywhere

#### A. Ouvrir la console Bash

1. Aller dans **Consoles** → **Bash**
2. Naviguer vers votre répertoire :
   ```bash
   cd edututor
   ```

#### B. Créer et configurer le virtualenv

```bash
# Créer le virtualenv
mkvirtualenv --python=python3.10 edututor

# L'activer (sera automatique après)
workon edututor

# Installer les dépendances
pip install -r requirements.txt
```

#### C. Configuration de la base de données

```bash
# Ouvrir l'interface MySQL
# Databases → Create database

# Puis dans la console :
python manage.py migrate
python manage.py collectstatic --noinput
```

### Étape 4 : Créer l'application Web

#### A. Interface Web Apps

1. Aller dans **Web** → **Add a new web app**
2. Choisir **Django**
3. **Python version** : 3.10
4. **Path** : `/home/your-username/edututor`

#### B. Configuration de l'application

1. **Virtualenv** : `edututor`
2. **WSGI file** : Modifier le fichier généré avec :
   ```python
   # Remplacer le contenu par celui du fichier wsgi.py fourni
   import os
   import sys

   project_home = '/home/your-username/edututor'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'edututor_ai.settings'

   activate_this = '/home/your-username/.virtualenvs/edututor/bin/activate_this.py'
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))

   import django
   django.setup()

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### Étape 5 : Variables d'environnement

#### A. Via l'interface Web

1. **Web** → Votre app → **Environment variables**
2. Ajouter :
   ```
   DJANGO_SECRET_KEY=votre-cle-secrete-django-ici
   DEBUG=False
   GEMINI_API_KEY=votre-cle-api-gemini
   DATABASE_NAME=your-username$db
   DATABASE_USER=your-username
   DATABASE_PASSWORD=votre-mot-de-passe-mysql
   PYTHONANYWHERE=True
   ```

#### B. Configuration de la base de données

1. **Databases** → Créer une base MySQL
2. Noter le mot de passe généré
3. L'ajouter dans les variables d'environnement

### Étape 6 : Configuration statique et média

#### A. Fichiers statiques

Dans **Web** → Votre app → **Static files** :
- URL : `/static/`
- Directory : `/home/your-username/edututor/staticfiles`

#### B. Fichiers média

- URL : `/media/`
- Directory : `/home/your-username/edututor/media`

### Étape 7 : Redémarrage et test

1. **Reload** votre application web
2. Tester l'URL : `https://your-username.pythonanywhere.com`
3. Créer un superutilisateur :
   ```bash
   python manage.py createsuperuser
   ```

## 🔧 Configuration avancée

### Domaine personnalisé

1. Acheter un domaine
2. Dans **Web** → **Custom domains**
3. Ajouter votre domaine
4. Configurer les DNS chez votre registrar :
   - Type : CNAME
   - Name : `www`
   - Value : `webapp-XXXXXX.pythonanywhere.com`

### SSL automatique

PythonAnywhere fournit automatiquement :
- ✅ Certificat SSL Let's Encrypt
- ✅ Renouvellement automatique
- ✅ HTTP → HTTPS redirection

## 📊 Monitoring et logs

### Logs d'erreur

```bash
# Console Bash
tail -f /var/log/your-username.pythonanywhere.com.error.log
```

### Logs d'accès

```bash
tail -f /var/log/your-username.pythonanywhere.com.access.log
```

### Debug

- **Web** → Votre app → **Logs** (interface web)
- Variables d'environnement dans les logs d'erreur
- Test avec `python manage.py shell`

## 🔄 Mises à jour

### Via Git

```bash
# Dans la console Bash
cd edututor
git pull origin main

# Redémarrer l'app
# Web → Votre app → Reload
```

### Via FTP/SFTP

1. Uploader les nouveaux fichiers
2. Redémarrer l'application

## 🚨 Dépannage

### Problèmes courants

1. **Erreur 500 - Internal Server Error**
   ```
   # Vérifier les logs d'erreur
   tail -f /var/log/*.error.log

   # Test local
   python manage.py check --deploy
   ```

2. **Erreur de base de données**
   ```
   # Vérifier DATABASE_* variables
   # Vérifier que la DB existe
   python manage.py dbshell
   ```

3. **Fichiers statiques non chargés**
   ```
   # Vérifier la configuration static files
   # Relancer collectstatic
   python manage.py collectstatic --noinput
   ```

4. **WebSockets ne fonctionnent pas**
   ```
   # Nécessite le plan Hacker ou supérieur
   # Vérifier les logs pour les erreurs Channels
   ```

### Commandes de debug

```bash
# Test de l'application
python manage.py check

# Test de la base de données
python manage.py dbshell

# Test des migrations
python manage.py showmigrations

# Shell Django
python manage.py shell
```

## 🎯 Optimisations pour PythonAnywhere

### Performance
- ✅ **Plan Hacker** minimum recommandé
- ✅ **MySQL** optimisé pour PythonAnywhere
- ✅ **WhiteNoise** pour les fichiers statiques
- ✅ **InMemoryChannelLayer** pour les WebSockets (limité)

### Stockage
- 📁 **512MB** sur Hacker (fichiers upload limités)
- 💾 **Base de données** : 1GB incluse
- 📊 **Logs** : Rotation automatique

## 📞 Support

- **Documentation PythonAnywhere** : [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **Forum** : [forum.pythonanywhere.com](https://www.pythonanywhere.com/forum/)
- **Support** : support@pythonanywhere.com

---

## 🎉 Checklist de déploiement

- [ ] Compte PythonAnywhere créé (plan Hacker+)
- [ ] Code uploadé sur PythonAnywhere
- [ ] Virtualenv créé et configuré
- [ ] Dépendances installées
- [ ] Base de données MySQL créée
- [ ] Application Web configurée
- [ ] Variables d'environnement définies
- [ ] Fichiers statiques configurés
- [ ] Application rechargée et testée
- [ ] Superutilisateur créé
- [ ] Domaine personnalisé (optionnel)

**🚀 Votre plateforme EduQuP est maintenant en ligne sur PythonAnywhere !**