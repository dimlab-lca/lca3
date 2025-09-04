# Guide de Déploiement LCA TV - PlanetHoster

## 🎯 **Configuration pour PlanetHoster**

Votre application LCA TV est maintenant configurée pour PlanetHoster avec les accès suivants:
- **Subdirectory**: `https://edifice.bf/lca`
- **Subdomain**: `https://tv-lca.edifice.bf`

## 📋 **Fichiers Mis à Jour**

### **Fichiers Principaux:**
- ✅ **`app.py`** - Configuré avec `APPLICATION_ROOT = '/lca'`
- ✅ **`passenger_wsgi_planethoster.py`** - Point d'entrée WSGI pour PlanetHoster
- ✅ **`.htaccess_planethoster`** - Configuration Apache pour `/lca`
- ✅ **Endpoints de debug** - Adaptés pour PlanetHoster

## 🚀 **Étapes de Déploiement sur PlanetHoster**

### **Étape 1: Préparation des Fichiers**

Renommez les fichiers pour le déploiement:
```bash
# Renommage des fichiers
mv passenger_wsgi_planethoster.py passenger_wsgi.py
mv .htaccess_planethoster .htaccess
```

### **Étape 2: Structure des Fichiers**

Uploadez tous les fichiers dans le répertoire `lca/`:
```
public_html/
└── lca/
    ├── passenger_wsgi.py
    ├── .htaccess
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── runtime.txt
    ├── models.py (optionnel)
    ├── performance_monitor.py (optionnel)
    ├── templates/
    ├── static/
    └── .env (à créer)
```

### **Étape 3: Configuration Python sur PlanetHoster**

1. **Accédez au cPanel** de votre compte PlanetHoster
2. **Trouvez "Python App"** dans la section Software
3. **Créez une nouvelle application Python**:
   - **Python Version**: 3.9
   - **Application Root**: `lca`
   - **Application URL**: `edifice.bf/lca`
   - **Application Startup File**: `passenger_wsgi.py`

### **Étape 4: Installation des Dépendances**

Via SSH ou Terminal dans cPanel:
```bash
# Connexion SSH
ssh votre-username@votre-serveur.planethoster.net

# Navigation vers le répertoire
cd public_html/lca

# Activation de l'environnement virtuel Python
source /home/votre-username/virtualenv/lca/3.9/bin/activate

# Installation des dépendances
pip install -r requirements.txt
```

### **Étape 5: Configuration de l'Environnement**

Créez le fichier `.env` dans le répertoire `lca/`:
```bash
# Configuration LCA TV pour PlanetHoster
FLASK_SECRET_KEY=votre-cle-secrete-super-securisee
FLASK_CONFIG=production
FLASK_ENV=production

# Mots de passe admin (changez ces valeurs!)
ADMIN_PASSWORD=votre-mot-de-passe-admin-securise
EDITOR_PASSWORD=votre-mot-de-passe-editeur-securise

# API YouTube (optionnel)
YOUTUBE_API_KEY=votre-cle-api-youtube
YOUTUBE_CHANNEL_ID=votre-id-chaine-youtube
YOUTUBE_LIVE_VIDEO_ID=votre-id-video-live

# Base de données (optionnel)
DATABASE_URL=sqlite:///lcatv_production.db
```

### **Étape 6: Configuration du Subdomain (Optionnel)**

Pour activer `tv-lca.edifice.bf`:

1. **Dans cPanel** > **Subdomains**
2. **Créez un subdomain**:
   - **Subdomain**: `tv-lca`
   - **Domain**: `edifice.bf`
   - **Document Root**: `public_html/lca`

## 🔧 **Configuration Spécifique PlanetHoster**

### **WSGI Configuration:**
```python
# Gestion des deux types d'accès
server_name = environ.get('SERVER_NAME', '')

if server_name.startswith('tv-lca.'):
    # Accès subdomain: tv-lca.edifice.bf
    environ['SCRIPT_NAME'] = ''
else:
    # Accès subdirectory: edifice.bf/lca
    environ['SCRIPT_NAME'] = '/lca'
```

### **Apache Configuration (.htaccess):**
```apache
# Base pour URLs relatives
RewriteBase /lca/

# Redirection HTTPS forcée
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Routage vers l'application Python
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [L]
```

## ✅ **Tests de Vérification**

### **1. Test d'Accès Principal**
- **URL**: `https://edifice.bf/lca/`
- **Résultat attendu**: Page d'accueil LCA TV

### **2. Test d'Accès Subdomain**
- **URL**: `https://tv-lca.edifice.bf/`
- **Résultat attendu**: Page d'accueil LCA TV

### **3. Test de Debug**
- **URL**: `https://edifice.bf/lca/debug`
- **Résultat attendu**: Page de debug avec informations système

### **4. Test de Santé**
- **URL**: `https://edifice.bf/lca/health`
- **Résultat attendu**: JSON avec status "healthy"

### **5. Test API**
- **URL**: `https://edifice.bf/lca/api/videos`
- **Résultat attendu**: JSON avec liste des vidéos

### **6. Test Admin**
- **URL**: `https://edifice.bf/lca/login`
- **Credentials**: admin / votre-mot-de-passe-admin

## 📊 **URLs de l'Application**

### **Accès Principal (edifice.bf/lca):**
- **Accueil**: `https://edifice.bf/lca/`
- **Vidéos**: `https://edifice.bf/lca/videos`
- **Direct**: `https://edifice.bf/lca/live`
- **Journal**: `https://edifice.bf/lca/journal`
- **Admin**: `https://edifice.bf/lca/dashboard`

### **Accès Subdomain (tv-lca.edifice.bf):**
- **Accueil**: `https://tv-lca.edifice.bf/`
- **Vidéos**: `https://tv-lca.edifice.bf/videos`
- **Direct**: `https://tv-lca.edifice.bf/live`
- **Journal**: `https://tv-lca.edifice.bf/journal`
- **Admin**: `https://tv-lca.edifice.bf/dashboard`

### **API Endpoints:**
- **Vidéos**: `/api/videos`
- **Statut Live**: `/api/live-status`
- **Actualités**: `/api/public/breaking-news`
- **Santé**: `/health`
- **Debug**: `/debug`

## 🛠 **Dépannage PlanetHoster**

### **Problèmes Courants:**

1. **Erreur 500 - Internal Server Error**
   - **Vérifiez**: Permissions des fichiers (644 pour les fichiers, 755 pour les dossiers)
   - **Commande**: `chmod 644 *.py && chmod 755 passenger_wsgi.py`

2. **Module Python non trouvé**
   - **Vérifiez**: Installation des dépendances
   - **Commande**: `pip install -r requirements.txt`

3. **Problème de chemin Python**
   - **Vérifiez**: Configuration dans cPanel Python App
   - **Solution**: Redémarrer l'application Python

4. **Erreur de configuration Flask**
   - **Vérifiez**: Fichier `.env` présent et correct
   - **Solution**: Créer/corriger le fichier `.env`

### **Commandes de Diagnostic:**
```bash
# Vérifier l'état de l'application
ls -la /home/votre-username/public_html/lca/

# Tester l'import Python
python3.9 -c "from app import application; print('OK')"

# Vérifier les logs
tail -f /home/votre-username/logs/error.log

# Tester les permissions
find /home/votre-username/public_html/lca/ -type f -name "*.py" -exec ls -l {} \;
```

### **Redémarrage de l'Application:**
1. **Via cPanel**: Python App > Restart
2. **Via SSH**: `touch /home/votre-username/public_html/lca/tmp/restart.txt`

## 🔐 **Sécurit�� et Performance**

### **Sécurité:**
- ✅ **HTTPS forcé** via .htaccess
- ✅ **Headers de sécurité** configurés
- ✅ **Fichiers sensibles** protégés
- ✅ **Variables d'environnement** sécurisées

### **Performance:**
- ✅ **Compression gzip** activée
- ✅ **Cache des fichiers statiques** configuré
- ✅ **Cache applicatif** avec TTL
- ✅ **Optimisation des requêtes** YouTube API

## 📞 **Support PlanetHoster**

### **Informations de Contact:**
- **Support PlanetHoster**: Via ticket dans l'espace client
- **Documentation**: https://planethoster.com/fr/Base-de-connaissances

### **Informations de Déploiement:**
- **Hosting**: PlanetHoster
- **Python Version**: 3.9
- **Application Type**: WSGI/Passenger
- **Domain**: edifice.bf
- **Subdirectory**: /lca
- **Subdomain**: tv-lca.edifice.bf

## 🎉 **Résultat Final**

Une fois déployé, votre application LCA TV sera accessible via:

### **✅ Fonctionnalités Disponibles:**
- **Site web complet** avec toutes les pages
- **Dashboard administrateur** avec login sécurisé
- **API REST** pour les vidéos et le statut live
- **Design responsive** pour mobile et desktop
- **Gestion des erreurs** et outils de debug
- **Performance optimisée** pour PlanetHoster

### **✅ Accès Multiple:**
- **Principal**: `https://edifice.bf/lca`
- **Subdomain**: `https://tv-lca.edifice.bf`
- **Flexible** selon vos préférences

Votre application LCA TV est maintenant prête pour la production sur PlanetHoster!