# Guide de Déploiement LCA TV - Sous-répertoire edifice.bf/tv-lca

## 🎯 Configuration Spécifique

Votre application LCA TV sera accessible à l'adresse: **https://edifice.bf/tv-lca**

## 📋 Fichiers Modifiés pour le Sous-répertoire

### Fichiers Principaux:
- ✅ **`app.py`** - Modifié avec `APPLICATION_ROOT = '/tv-lca'`
- ✅ **`passenger_wsgi_subdirectory.py`** - Point d'entrée WSGI pour sous-répertoire
- ✅ **`.htaccess_subdirectory`** - Configuration Apache pour sous-répertoire

## 🚀 Étapes de Déploiement

### Étape 1: Création de l'Application Python sur N0C

1. **Connectez-vous à N0C**: https://mg.n0c.com/fr/
2. **Accédez à Python**: Menu **Langages** > **Python**
3. **Créez l'application**:
   - **VERSION**: Python 3.8 ou plus récent
   - **RÉPERTOIRE D'APPLICATION**: `tv-lca`
   - **DOMAINE/URL D'APPLICATION**: `edifice.bf/tv-lca`
   - **FICHIER DE DÉMARRAGE**: `passenger_wsgi.py`
   - Cliquez sur **CRÉER**

### Étape 2: Upload des Fichiers

Uploadez tous les fichiers dans le répertoire `tv-lca`:

```
tv-lca/
├── passenger_wsgi.py (renommé depuis passenger_wsgi_subdirectory.py)
├── .htaccess (renommé depuis .htaccess_subdirectory)
├── app.py (version modifiée)
├── models.py
├── config.py
├── performance_monitor.py
├── requirements.txt
├── templates/
├── static/
└── .env (à créer)
```

### Étape 3: Renommage des Fichiers

**Important**: Renommez ces fichiers après l'upload:

```bash
# Via SSH ou gestionnaire de fichiers N0C
mv passenger_wsgi_subdirectory.py passenger_wsgi.py
mv .htaccess_subdirectory .htaccess
```

### Étape 4: Configuration de l'Environnement

Créez un fichier `.env` dans le répertoire `tv-lca`:

```bash
# Fichier .env
SECRET_KEY=votre-cle-secrete-super-securisee
YOUTUBE_API_KEY=votre-cle-api-youtube
YOUTUBE_CHANNEL_ID=votre-id-chaine-youtube
YOUTUBE_LIVE_VIDEO_ID=votre-id-video-live
ADMIN_PASSWORD=votre-mot-de-passe-admin-securise
EDITOR_PASSWORD=votre-mot-de-passe-editeur
FLASK_CONFIG=production
```

### Étape 5: Installation des Dépendances

Via SSH:

```bash
# Connexion SSH
ssh votre-utilisateur@edifice.bf -p 5022

# Activation de l'environnement virtuel
source /home/votre-utilisateur/virtualenv/tv-lca/3.8/bin/activate

# Navigation vers le répertoire
cd tv-lca

# Installation des dépendances
pip install -r requirements.txt
```

### Étape 6: Test et Activation

1. **Redémarrez l'application** dans le panneau N0C
2. **Testez l'accès**: https://edifice.bf/tv-lca
3. **Vérifiez les pages**:
   - Page d'accueil: https://edifice.bf/tv-lca/
   - Debug: https://edifice.bf/tv-lca/debug
   - Santé: https://edifice.bf/tv-lca/health
   - Admin: https://edifice.bf/tv-lca/login

## 🔧 Configuration Spécifique au Sous-répertoire

### Modifications dans app.py:

```python
# Configure for subdirectory deployment
app.config['APPLICATION_ROOT'] = '/tv-lca'
```

### Modifications dans passenger_wsgi.py:

```python
# Set the SCRIPT_NAME for subdirectory deployment
environ['SCRIPT_NAME'] = '/tv-lca'

# Remove the subdirectory from PATH_INFO
path_info = environ.get('PATH_INFO', '')
if path_info.startswith('/tv-lca'):
    environ['PATH_INFO'] = path_info[7:]  # Remove '/tv-lca'
```

### Modifications dans .htaccess:

```apache
# Set the base for relative URLs
RewriteBase /tv-lca/

# Custom error pages
ErrorDocument 404 /tv-lca/404.html
ErrorDocument 500 /tv-lca/500.html
```

## 📊 URLs de l'Application

### Pages Principales:
- **Accueil**: https://edifice.bf/tv-lca/
- **Vidéos**: https://edifice.bf/tv-lca/videos
- **Direct**: https://edifice.bf/tv-lca/live
- **Journal**: https://edifice.bf/tv-lca/journal
- **Émissions**: https://edifice.bf/tv-lca/emissions
- **Publicité**: https://edifice.bf/tv-lca/publicite
- **À propos**: https://edifice.bf/tv-lca/about
- **Contact**: https://edifice.bf/tv-lca/contact

### Administration:
- **Connexion**: https://edifice.bf/tv-lca/login
- **Dashboard**: https://edifice.bf/tv-lca/dashboard

### API:
- **Vidéos**: https://edifice.bf/tv-lca/api/videos
- **Statut Live**: https://edifice.bf/tv-lca/api/live-status
- **Actualités**: https://edifice.bf/tv-lca/api/public/breaking-news

### Debug:
- **Debug Info**: https://edifice.bf/tv-lca/debug
- **Santé**: https://edifice.bf/tv-lca/health
- **YouTube Debug**: https://edifice.bf/tv-lca/debug/youtube

## 🔍 Vérifications Post-Déploiement

### Checklist:

- [ ] Application créée dans N0C avec le bon répertoire (`tv-lca`)
- [ ] Fichiers uploadés et renommés correctement
- [ ] Fichier `.env` créé avec les bonnes variables
- [ ] Dépendances Python installées
- [ ] Application redémarrée dans N0C
- [ ] Page d'accueil accessible: https://edifice.bf/tv-lca/
- [ ] Page de debug fonctionne: https://edifice.bf/tv-lca/debug
- [ ] Connexion admin possible: https://edifice.bf/tv-lca/login
- [ ] API répond: https://edifice.bf/tv-lca/api/videos

### Tests de Fonctionnement:

```bash
# Test de l'API
curl https://edifice.bf/tv-lca/health

# Test de la page d'accueil
curl -I https://edifice.bf/tv-lca/

# Test de l'API vidéos
curl https://edifice.bf/tv-lca/api/videos
```

## 🚨 Dépannage Spécifique

### Problème: Erreur 404 sur toutes les pages

**Solution**: Vérifiez que `.htaccess` contient:
```apache
RewriteBase /tv-lca/
```

### Problème: CSS/JS ne se chargent pas

**Solution**: Vérifiez que les fichiers statiques sont dans `tv-lca/static/`

### Problème: Redirections incorrectes

**Solution**: Vérifiez que `app.py` contient:
```python
app.config['APPLICATION_ROOT'] = '/tv-lca'
```

### Problème: Erreur WSGI

**Solution**: Vérifiez que `passenger_wsgi.py` gère correctement le sous-répertoire

## 📞 Support

### Commandes Utiles:

```bash
# Vérifier l'état de l'application
cloudlinux-selector list --json --interpreter python

# Redémarrer l'application
cloudlinux-selector restart --json --interpreter python --app-root tv-lca

# Voir les logs
tail -f ~/logs/error.log
```

### Informations de Déploiement:

- **Domaine**: edifice.bf
- **Sous-répertoire**: /tv-lca
- **URL complète**: https://edifice.bf/tv-lca
- **Répertoire d'application**: tv-lca
- **Point d'entrée**: passenger_wsgi.py

Votre application LCA TV est maintenant configurée pour fonctionner parfaitement à l'adresse **https://edifice.bf/tv-lca** !