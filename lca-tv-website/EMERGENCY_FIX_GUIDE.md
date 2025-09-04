# Guide de Correction d'Urgence - Routes LCA TV

## 🚨 **Problème Persistant**

Malgré la modification du .htaccess principal, les routes ne fonctionnent toujours pas:
- `https://edifice.bf/lca/journal` ❌
- `https://edifice.bf/lca/live` ❌  
- `https://edifice.bf/lca/emissions` ❌
- `https://edifice.bf/lca/login` ❌

## 🔍 **Diagnostic Immédiat**

### **Étape 1: Vérifiez si votre app Python fonctionne**
Testez ces URLs:
- `https://edifice.bf/lca/` (page d'accueil)
- `https://edifice.bf/lca/health` (endpoint de santé)
- `https://edifice.bf/lca/debug` (page de debug)

**Si aucune ne fonctionne:** Problème de configuration Python/WSGI
**Si seule l'accueil fonctionne:** Problème de routage des sous-pages

### **Étape 2: Vérifiez le .htaccess principal**
```bash
ssh username@edifice.bf -p 5022
head -50 ~/public_html/.htaccess | grep -A 10 -B 5 "lca"
```

Vous devriez voir:
```apache
RewriteCond %{REQUEST_URI} ^/lca(/.*)?$ [NC]
RewriteRule ^(.*)$ - [L]
```

## 🔧 **Solutions d'Urgence**

### **Solution 1: .htaccess Principal Plus Agressif**

Remplacez la section WordPress par cette version plus forte:

```apache
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /

# EXCLUSION FORTE pour /lca - DOIT être en premier
RewriteRule ^lca(/.*)?$ - [L,QSA]

# Règles WordPress normales
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
```

### **Solution 2: .htaccess LCA Plus Robuste**

Dans `/public_html/lca/.htaccess`, remplacez tout par:

```apache
# LCA TV - Configuration d'urgence pour forcer le routage
RewriteEngine On
RewriteBase /lca/

# Force toutes les requêtes vers passenger_wsgi.py
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/lca/static/
RewriteRule ^(.*)$ /lca/passenger_wsgi.py [L,QSA]

# Alternative si la première ne fonctionne pas
# RewriteRule ^(.*)$ passenger_wsgi.py [L,QSA]

# Gestion des erreurs
ErrorDocument 404 /lca/404.html
ErrorDocument 500 /lca/500.html
```

### **Solution 3: Test Direct du WSGI**

Créez un fichier de test `/public_html/lca/test.py`:

```python
#!/usr/bin/python3.9
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
    path_info = environ.get('PATH_INFO', '')
    script_name = environ.get('SCRIPT_NAME', '')
    request_uri = environ.get('REQUEST_URI', '')
    
    html = f"""
    <html>
    <head><title>LCA TV Test</title></head>
    <body>
        <h1>LCA TV WSGI Test</h1>
        <p><strong>PATH_INFO:</strong> {path_info}</p>
        <p><strong>SCRIPT_NAME:</strong> {script_name}</p>
        <p><strong>REQUEST_URI:</strong> {request_uri}</p>
        <p><strong>Status:</strong> WSGI is working!</p>
        <hr>
        <a href="/lca/test.py">Test Link</a>
    </body>
    </html>
    """
    return [html.encode('utf-8')]
```

Puis testez: `https://edifice.bf/lca/test.py`

## 🚀 **Actions Immédiates**

### **Action 1: Vérification Rapide**
```bash
# Connectez-vous en SSH
ssh username@edifice.bf -p 5022

# Vérifiez que les fichiers existent
ls -la ~/public_html/lca/
ls -la ~/public_html/lca/passenger_wsgi.py
ls -la ~/public_html/lca/.htaccess

# Vérifiez les permissions
chmod 755 ~/public_html/lca/passenger_wsgi.py
chmod 644 ~/public_html/lca/.htaccess
```

### **Action 2: Test Python Direct**
```bash
cd ~/public_html/lca
python3.9 -c "from app import application; print('Import OK')"
python3.9 -c "from app import app; print([str(r) for r in app.url_map.iter_rules()])"
```

### **Action 3: Redémarrage Complet**
```bash
# Redémarrez l'application
touch ~/public_html/lca/tmp/restart.txt

# Attendez 30 secondes puis testez
sleep 30
curl -I https://edifice.bf/lca/health
```

## 🔧 **Solutions Alternatives**

### **Option A: Sous-domaine (Recommandé)**

Si les problèmes persistent, configurez un sous-domaine:

1. **Dans cPanel > Subdomains:**
   - Sous-domaine: `tv-lca`
   - Domaine: `edifice.bf`
   - Document Root: `public_html/lca`

2. **Résultat:** `https://tv-lca.edifice.bf/` (plus de conflit avec WordPress)

### **Option B: Port Différent**

Configurez l'application sur un port différent via cPanel Python App.

### **Option C: Répertoire Différent**

Déplacez l'application vers `/tv/` au lieu de `/lca/`.

## 🧪 **Tests de Diagnostic Avancé**

### **Test 1: Vérification Apache**
```bash
# Vérifiez les logs en temps réel
tail -f ~/logs/error.log &
tail -f ~/logs/access.log &

# Dans un autre terminal, testez
curl -v https://edifice.bf/lca/journal
```

### **Test 2: Vérification WSGI**
```bash
# Testez l'import direct
cd ~/public_html/lca
python3.9 passenger_wsgi.py
```

### **Test 3: Vérification Rewrite**
Ajoutez temporairement dans le .htaccess principal:
```apache
# Debug rewrite
RewriteRule ^lca/(.*)$ /lca/debug-$1 [R=302,L]
```

## 📋 **Checklist de Vérification**

### **Fichiers et Permissions:**
- [ ] `/public_html/.htaccess` modifié avec exclusion `/lca`
- [ ] `/public_html/lca/.htaccess` existe et est correct
- [ ] `/public_html/lca/passenger_wsgi.py` existe (755)
- [ ] `/public_html/lca/app.py` existe (644)
- [ ] `/public_html/lca/run.py` existe (644)

### **Configuration:**
- [ ] Règle d'exclusion `/lca` AVANT les règles WordPress
- [ ] Application Python redémarrée
- [ ] Pas d'erreurs dans les logs

### **Tests:**
- [ ] `https://edifice.bf/lca/` fonctionne
- [ ] `https://edifice.bf/lca/health` retourne JSON
- [ ] `https://edifice.bf/lca/debug` affiche les infos
- [ ] `https://edifice.bf/` (WordPress) fonctionne toujours

## 🎯 **Solution de Dernier Recours**

Si rien ne fonctionne, créez un fichier `/public_html/lca/index.php`:

```php
<?php
// Redirection temporaire vers Python
$path = $_SERVER['REQUEST_URI'];
$path = str_replace('/lca/', '/', $path);

// Définir les variables d'environnement
$_ENV['SCRIPT_NAME'] = '/lca';
$_ENV['PATH_INFO'] = $path;

// Exécuter l'application Python
$output = shell_exec('cd /home/username/public_html/lca && python3.9 passenger_wsgi.py');
echo $output;
?>
```

## 🚨 **Contact Support**

Si toutes les solutions échouent:

1. **Contactez PlanetHoster Support**
2. **Mentionnez:** "Conflit .htaccess entre WordPress et application Python"
3. **Demandez:** Configuration pour sous-répertoire Python avec WordPress existant

## 💡 **Prochaines Étapes**

1. **Testez d'abord:** `https://edifice.bf/lca/debug`
2. **Si ça ne fonctionne pas:** Problème WSGI/Python
3. **Si ça fonctionne:** Problème de routage spécifique

Commencez par le diagnostic et appliquez les solutions dans l'ordre! 🎯