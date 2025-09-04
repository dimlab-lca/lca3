# LCA TV - Checklist de Déploiement PlanetHoster

## 🎯 **Configuration Actuelle**

- **Hosting**: PlanetHoster
- **Python Version**: 3.9
- **Structure**: run.py + passenger_wsgi.py
- **Domain**: edifice.bf/lca
- **Subdomain**: tv-lca.edifice.bf (optionnel)

## 📋 **Checklist de Déploiement**

### **✅ Étape 1: Préparation des Fichiers**

Assurez-vous d'avoir tous ces fichiers dans votre répertoire local:

```
lca-tv-website/
├── run.py                    ✅ (Point d'entrée WSGI)
├── passenger_wsgi.py         ✅ (Loader Passenger)
├── .htaccess                 ✅ (Configuration Apache)
├── app.py                    ✅ (Application Flask principale)
├── config.py                 ✅ (Configuration)
├── requirements.txt          ✅ (Dépendances Python)
├── runtime.txt               ✅ (Version Python)
├── templates/                ✅ (Templates HTML)
│   ├���─ home.html
│   ├── videos.html
│   ├── live.html
│   ├── login.html
│   └── dashboard_enhanced.html
├── static/                   ✅ (Fichiers statiques)
│   ├── css/
│   ├── js/
│   └── images/
└── .env                      ⚠️ (À créer sur le serveur)
```

### **✅ Étape 2: Upload sur PlanetHoster**

1. **Connectez-vous à cPanel** de votre compte PlanetHoster
2. **Accédez au File Manager**
3. **Naviguez vers** `public_html/lca/`
4. **Uploadez tous les fichiers** (sauf .env)

### **✅ Étape 3: Configuration Python**

1. **Dans cPanel** > **Python App**
2. **Créez une nouvelle application**:
   - **Python Version**: 3.9
   - **Application Root**: `lca`
   - **Application URL**: `edifice.bf/lca`
   - **Application Startup File**: `passenger_wsgi.py`

### **✅ Étape 4: Installation des Dépendances**

Via SSH ou Terminal dans cPanel:
```bash
# Connexion SSH
ssh votre-username@votre-serveur.planethoster.net

# Navigation vers le répertoire
cd public_html/lca

# Activation de l'environnement virtuel
source /home/votre-username/virtualenv/lca/3.9/bin/activate

# Installation des dépendances
pip install -r requirements.txt
```

### **✅ Étape 5: Création du fichier .env**

Créez le fichier `.env` dans `public_html/lca/`:
```bash
# Configuration LCA TV
FLASK_SECRET_KEY=votre-cle-secrete-super-securisee-changez-moi
FLASK_CONFIG=production
FLASK_ENV=production

# Mots de passe admin (CHANGEZ CES VALEURS!)
ADMIN_PASSWORD=votre-mot-de-passe-admin-securise
EDITOR_PASSWORD=votre-mot-de-passe-editeur-securise

# API YouTube (optionnel - l'app fonctionne sans)
YOUTUBE_API_KEY=votre-cle-api-youtube
YOUTUBE_CHANNEL_ID=votre-id-chaine-youtube
YOUTUBE_LIVE_VIDEO_ID=votre-id-video-live

# Base de données (optionnel)
DATABASE_URL=sqlite:///lcatv_production.db
```

### **✅ Étape 6: Vérification des Permissions**

```bash
# Vérifier les permissions des fichiers
chmod 644 *.py
chmod 755 passenger_wsgi.py
chmod 755 run.py
chmod 644 .htaccess
chmod 644 .env
chmod -R 755 templates/
chmod -R 755 static/
```

### **✅ Étape 7: Redémarrage de l'Application**

1. **Via cPanel**: Python App > Restart
2. **Via SSH**: `touch /home/votre-username/public_html/lca/tmp/restart.txt`

## 🧪 **Tests de Vérification**

### **Test 1: Page d'Accueil**
- **URL**: `https://edifice.bf/lca/`
- **Résultat attendu**: Page d'accueil LCA TV avec vidéos

### **Test 2: Debug**
- **URL**: `https://edifice.bf/lca/debug`
- **Résultat attendu**: Page de debug avec informations système

### **Test 3: Santé**
- **URL**: `https://edifice.bf/lca/health`
- **Résultat attendu**: JSON `{"status": "healthy"}`

### **Test 4: API Vidéos**
- **URL**: `https://edifice.bf/lca/api/videos`
- **Résultat attendu**: JSON avec liste des vidéos

### **Test 5: Connexion Admin**
- **URL**: `https://edifice.bf/lca/login`
- **Credentials**: admin / votre-mot-de-passe-admin
- **Résultat attendu**: Accès au dashboard

### **Test 6: Pages Principales**
- **Vidéos**: `https://edifice.bf/lca/videos`
- **Direct**: `https://edifice.bf/lca/live`
- **Journal**: `https://edifice.bf/lca/journal`

## 🚨 **Dépannage**

### **Erreur 500 - Internal Server Error**

1. **Vérifiez les logs**:
   ```bash
   tail -f /home/votre-username/logs/error.log
   ```

2. **Vérifiez les permissions**:
   ```bash
   ls -la /home/votre-username/public_html/lca/
   ```

3. **Testez l'import Python**:
   ```bash
   cd /home/votre-username/public_html/lca/
   python3.9 -c "from app import application; print('OK')"
   ```

### **Module Not Found**

1. **Vérifiez l'installation des dépendances**:
   ```bash
   source /home/votre-username/virtualenv/lca/3.9/bin/activate
   pip list
   pip install -r requirements.txt
   ```

### **Configuration Error**

1. **Vérifiez le fichier .env**:
   ```bash
   cat /home/votre-username/public_html/lca/.env
   ```

2. **Vérifiez la configuration Python App** dans cPanel

## 📊 **Structure Finale sur le Serveur**

```
/home/votre-username/public_html/lca/
├── run.py                    (Point d'entrée WSGI)
├── passenger_wsgi.py         (Loader Passenger)
├── .htaccess                 (Configuration Apache)
├── app.py                    (Application Flask)
├── config.py                 (Configuration)
├── requirements.txt          (Dépendances)
├── runtime.txt               (Python 3.9)
├── .env                      (Variables d'environnement)
├── templates/                (Templates HTML)
├── static/                   (CSS, JS, Images)
├── models.py                 (Optionnel)
├── performance_monitor.py    (Optionnel)
└── tmp/                      (Créé automatiquement)
    └── restart.txt           (Pour redémarrage)
```

## ✅ **Résultat Final**

Une fois déployé avec succès, votre application LCA TV sera accessible à:

- **URL Principale**: `https://edifice.bf/lca/`
- **Dashboard Admin**: `https://edifice.bf/lca/dashboard`
- **API**: `https://edifice.bf/lca/api/videos`

### **Fonctionnalités Disponibles**:
- ✅ Site web complet avec toutes les pages
- ✅ Dashboard administrateur sécurisé
- ✅ API REST pour les vidéos
- ✅ Design responsive mobile/desktop
- ✅ Gestion des erreurs et debug
- ✅ Performance optimisée

### **Comptes Admin par Défaut**:
- **admin** / votre-mot-de-passe-admin (défini dans .env)
- **editor** / votre-mot-de-passe-editeur (défini dans .env)
- **musk** / tesla123 (codé en dur)

Votre application LCA TV est maintenant prête pour la production sur PlanetHoster!