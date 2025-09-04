# Guide de Correction de Navigation - LCA TV

## 🚨 **Problème Identifié**

Les liens de navigation redirigent vers la page 404 d'edifice.bf au lieu de rester dans le sous-répertoire `/lca`.

## 🔧 **Solutions Appliquées**

### **1. Configuration Flask Améliorée**

**Fichier: `app.py`**
```python
# Configuration pour sous-répertoire
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Fonction pour forcer le sous-répertoire
@app.before_request
def force_subdirectory():
    """Assure que toutes les URLs sont générées avec le bon sous-répertoire"""
    # Géré automatiquement par WSGI
    pass
```

### **2. Configuration .htaccess Corrigée**

**Fichier: `.htaccess`**
```apache
# Base pour URLs relatives
RewriteBase /lca/

# Assure que toutes les routes Flask restent dans /lca
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/lca/static/
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [QSA,L]

# Pages d'erreur personnalisées
ErrorDocument 404 /lca/404.html
ErrorDocument 500 /lca/500.html
```

### **3. Configuration WSGI Optimisée**

**Fichier: `run.py`**
```python
def app(environ, start_response):
    """Point d'entrée WSGI avec gestion du sous-répertoire"""
    try:
        # Gestion des accès subdirectory et subdomain
        server_name = environ.get('SERVER_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        
        if server_name.startswith('tv-lca.'):
            # Accès subdomain: tv-lca.edifice.bf
            environ['SCRIPT_NAME'] = ''
        else:
            # Accès subdirectory: edifice.bf/lca
            environ['SCRIPT_NAME'] = '/lca'
            
            # Supprime le sous-répertoire de PATH_INFO
            if path_info.startswith('/lca'):
                environ['PATH_INFO'] = path_info[4:]
            elif path_info == '/lca':
                environ['PATH_INFO'] = '/'
        
        # Import et exécution de l'app Flask
        from app import application as flask_app
        return flask_app(environ, start_response)
```

## 🧪 **Tests de Vérification**

### **URLs à Tester Après Déploiement:**

1. **Page d'Accueil**
   - URL: `https://edifice.bf/lca/`
   - Résultat attendu: Page LCA TV

2. **Navigation Menu**
   - Accueil: `https://edifice.bf/lca/`
   - Journal: `https://edifice.bf/lca/journal`
   - Direct: `https://edifice.bf/lca/live`
   - Émissions: `https://edifice.bf/lca/emissions`
   - Publicité: `https://edifice.bf/lca/publicite`
   - À propos: `https://edifice.bf/lca/about`

3. **Authentification**
   - Login: `https://edifice.bf/lca/login`
   - Dashboard: `https://edifice.bf/lca/dashboard`
   - Logout: `https://edifice.bf/lca/logout`

4. **API**
   - Vidéos: `https://edifice.bf/lca/api/videos`
   - Santé: `https://edifice.bf/lca/health`
   - Debug: `https://edifice.bf/lca/debug`

## 🔍 **Diagnostic des Problèmes**

### **Problème 1: Redirections vers le domaine principal**

**Symptôme:** Clic sur un lien → Redirection vers `https://edifice.bf/404`

**Cause:** Configuration WSGI ou .htaccess incorrecte

**Solution:**
```bash
# Vérifiez le fichier .htaccess
cat /home/username/public_html/lca/.htaccess

# Vérifiez les permissions
ls -la /home/username/public_html/lca/

# Redémarrez l'application
touch /home/username/public_html/lca/tmp/restart.txt
```

### **Problème 2: URLs générées sans /lca**

**Symptôme:** `url_for('home')` génère `/` au lieu de `/lca/`

**Cause:** Configuration Flask APPLICATION_ROOT

**Solution:**
```python
# Dans app.py, vérifiez:
app.config['APPLICATION_ROOT'] = '/lca'

# Dans run.py, vérifiez:
environ['SCRIPT_NAME'] = '/lca'
```

### **Problème 3: Fichiers statiques non trouvés**

**Symptôme:** CSS/JS/Images ne se chargent pas

**Cause:** Chemin statique incorrect

**Solution:**
```apache
# Dans .htaccess, vérifiez:
RewriteRule ^static/(.*)$ static/$1 [L]
RewriteCond %{REQUEST_URI} !^/lca/static/
```

## 🛠 **Commandes de Dépannage**

### **1. Vérification des Fichiers**
```bash
# Connexion SSH
ssh username@edifice.bf -p 5022

# Navigation vers le répertoire
cd public_html/lca

# Vérification des fichiers
ls -la

# Vérification du contenu .htaccess
cat .htaccess

# Vérification des permissions
find . -name "*.py" -exec ls -l {} \;
```

### **2. Test de l'Application**
```bash
# Test d'import Python
python3.9 -c "from app import application; print('OK')"

# Test de la configuration
python3.9 -c "from app import app; print(app.config.get('APPLICATION_ROOT'))"

# Vérification des logs
tail -f ~/logs/error.log
```

### **3. Redémarrage de l'Application**
```bash
# Méthode 1: Fichier restart
touch ~/public_html/lca/tmp/restart.txt

# Méthode 2: Via cPanel
# Python App > Restart
```

## 📊 **Configuration PlanetHoster**

### **Dans cPanel > Python App:**

1. **Python Version:** 3.9
2. **Application Root:** `lca`
3. **Application URL:** `edifice.bf/lca`
4. **Application Startup File:** `passenger_wsgi.py`
5. **Application Entry Point:** `app`

### **Variables d'Environnement (.env):**
```bash
FLASK_SECRET_KEY=votre-cle-secrete
FLASK_CONFIG=production
FLASK_ENV=production
APPLICATION_ROOT=/lca
```

## 🎯 **Résolution Étape par Étape**

### **Étape 1: Vérification des Fichiers**
```bash
# Assurez-vous que ces fichiers sont présents:
- passenger_wsgi.py
- run.py
- app.py
- .htaccess
- .env
```

### **Étape 2: Vérification de la Configuration**
```bash
# Dans app.py:
app.config['APPLICATION_ROOT'] = '/lca'

# Dans run.py:
environ['SCRIPT_NAME'] = '/lca'

# Dans .htaccess:
RewriteBase /lca/
```

### **Étape 3: Test des URLs**
```bash
# Test manuel des URLs:
curl -I https://edifice.bf/lca/
curl -I https://edifice.bf/lca/health
curl -I https://edifice.bf/lca/debug
```

### **Étape 4: Vérification des Logs**
```bash
# Logs d'erreur Apache
tail -f ~/logs/error.log

# Logs d'accès
tail -f ~/logs/access.log
```

## ✅ **Checklist de Validation**

### **Avant Déploiement:**
- [ ] `app.py` configuré avec `APPLICATION_ROOT = '/lca'`
- [ ] `run.py` gère `SCRIPT_NAME = '/lca'`
- [ ] `.htaccess` configuré avec `RewriteBase /lca/`
- [ ] Tous les templates utilisent `{{ url_for() }}`

### **Après Déploiement:**
- [ ] Page d'accueil accessible: `edifice.bf/lca/`
- [ ] Navigation fonctionne (tous les liens)
- [ ] Authentification fonctionne
- [ ] Fichiers statiques se chargent
- [ ] API endpoints répondent

### **Tests de Navigation:**
- [ ] Logo → Page d'accueil
- [ ] Menu → Toutes les pages
- [ ] Formulaires → Soumission correcte
- [ ] Redirections → Restent dans `/lca`

## 🚀 **Résultat Attendu**

Une fois ces corrections appliquées:

1. **Tous les liens restent dans `/lca`**
2. **Navigation fluide entre les pages**
3. **Aucune redirection vers le domaine principal**
4. **URLs correctement générées avec le préfixe `/lca`**
5. **Fichiers statiques accessibles**

Votre application LCA TV fonctionnera parfaitement sur PlanetHoster! 🎯