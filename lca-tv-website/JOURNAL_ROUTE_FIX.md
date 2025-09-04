# Fix pour le Problème de Route Journal - LCA TV

## 🚨 **Problème Identifié**

Quand vous cliquez sur "Journal", vous êtes redirigé vers `https://edifice.bf/lca/journal` mais vous obtenez la page principale d'edifice.bf au lieu de votre application LCA TV.

## 🔍 **Diagnostic du Problème**

Le problème indique que:
1. L'URL est correctement générée (`/lca/journal`)
2. Mais Apache/PlanetHoster ne route pas cette requête vers votre application Python
3. Au lieu de cela, il sert la page par défaut d'edifice.bf

## 🔧 **Solutions Appliquées**

### **1. .htaccess Robuste (Nouveau)**

J'ai créé un nouveau fichier `.htaccess` avec des règles plus strictes:

```apache
# CRITICAL: Ensure ALL Flask routes are processed by Python
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L,E=ORIGINAL_PATH:$1]
```

**Changements clés:**
- Suppression du `/$1` qui pouvait causer des problèmes
- Ajout d'une variable d'environnement pour le debug
- Règles plus spécifiques pour les fichiers statiques

### **2. WSGI Amélioré (run.py)**

Amélioration de la gestion des chemins:

```python
# Handle PATH_INFO properly - this is crucial for routing
if path_info.startswith('/lca/'):
    # Remove /lca from PATH_INFO but keep the trailing slash and path
    new_path_info = path_info[4:]  # Remove '/lca' but keep the rest
    environ['PATH_INFO'] = new_path_info
elif path_info == '/lca':
    # Exact /lca should go to home
    environ['PATH_INFO'] = '/'
```

### **3. Debug Endpoint Amélioré**

Ajout d'informations de debug détaillées dans `/debug` pour diagnostiquer:
- Informations de requête complètes
- Variables d'environnement WSGI
- Test des liens `url_for()`
- Liens directs pour comparaison

## 🧪 **Tests de Diagnostic**

### **Étape 1: Vérifiez le Debug Endpoint**

Visitez: `https://edifice.bf/lca/debug`

**Si ça fonctionne:** Votre application Python est accessible
**Si ça ne fonctionne pas:** Problème de configuration Apache/WSGI

### **Étape 2: Testez les Liens Directs**

Dans la page debug, testez ces liens:
- `Journal (url_for)` - Doit générer `/lca/journal`
- `Journal (direct /lca/journal)` - Test direct

### **Étape 3: Vérifiez les Variables WSGI**

Dans la table "Request Information", vérifiez:
- **SCRIPT_NAME** doit être `/lca`
- **PATH_INFO** doit être `/debug` (pour la page debug)
- **REQUEST_URI** doit être `/lca/debug`

## 🔧 **Actions de Déploiement**

### **1. Upload des Fichiers Mis à Jour**

Uploadez ces fichiers vers `public_html/lca/`:
```
.htaccess (nouveau - plus robuste)
run.py (amélioré)
app.py (debug amélioré)
```

### **2. Vérification des Permissions**

```bash
# SSH vers votre serveur
ssh username@edifice.bf -p 5022

# Navigation vers le répertoire
cd public_html/lca

# Vérification des permissions
ls -la

# Correction si nécessaire
chmod 755 passenger_wsgi.py run.py
chmod 644 .htaccess app.py
```

### **3. Redémarrage de l'Application**

```bash
# Méthode 1: Fichier restart
touch ~/public_html/lca/tmp/restart.txt

# Méthode 2: Via cPanel
# Python App > Restart
```

### **4. Test Immédiat**

```bash
# Test de la page debug
curl -I https://edifice.bf/lca/debug

# Test de la route journal
curl -I https://edifice.bf/lca/journal

# Test de l'accueil
curl -I https://edifice.bf/lca/
```

## 🔍 **Diagnostic Avancé**

### **Si le problème persiste:**

1. **Vérifiez les logs Apache:**
```bash
tail -f ~/logs/error.log
tail -f ~/logs/access.log
```

2. **Testez l'import Python:**
```bash
cd ~/public_html/lca
python3.9 -c "from app import application; print('Import OK')"
```

3. **Vérifiez la configuration Flask:**
```bash
python3.9 -c "from app import app; print('Routes:', [str(rule) for rule in app.url_map.iter_rules()])"
```

4. **Testez le WSGI directement:**
```bash
python3.9 run.py
```

## 🎯 **Solutions Alternatives**

### **Si .htaccess ne fonctionne pas:**

**Option 1: Règle alternative dans .htaccess**
```apache
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [QSA,L]
```

**Option 2: Configuration plus simple**
```apache
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ passenger_wsgi.py [L]
```

**Option 3: Forcer le passage par Python**
```apache
RewriteRule ^journal$ passenger_wsgi.py [QSA,L]
RewriteRule ^live$ passenger_wsgi.py [QSA,L]
RewriteRule ^videos$ passenger_wsgi.py [QSA,L]
```

## 📊 **Checklist de Vérification**

### **Configuration Serveur:**
- [ ] Fichiers uploadés dans `public_html/lca/`
- [ ] Permissions correctes (755 pour .py, 644 pour .htaccess)
- [ ] Application redémarrée
- [ ] Pas d'erreurs dans les logs

### **Test des Routes:**
- [ ] `/lca/` → Page d'accueil LCA TV
- [ ] `/lca/debug` → Page de debug avec infos détaillées
- [ ] `/lca/journal` → Page journal LCA TV (pas edifice.bf)
- [ ] `/lca/live` → Page live LCA TV
- [ ] `/lca/health` → JSON de santé

### **Variables WSGI:**
- [ ] SCRIPT_NAME = `/lca`
- [ ] PATH_INFO correct pour chaque route
- [ ] REQUEST_URI inclut `/lca`

## 🚀 **Test Final**

Une fois les corrections appliquées:

1. **Visitez:** `https://edifice.bf/lca/debug`
2. **Vérifiez:** Toutes les informations de requête
3. **Testez:** Chaque lien dans la section "Test Links"
4. **Confirmez:** Le lien "Journal (url_for)" fonctionne

## 💡 **Explication Technique**

Le problème était que Apache ne routait pas correctement les requêtes vers votre application Python. Les nouvelles règles `.htaccess` forcent TOUTES les requêtes non-fichiers à passer par `passenger_wsgi.py`, garantissant que votre application Flask gère toutes les routes.

**Avant:** `/lca/journal` → Apache cherche un fichier → Trouve rien → Page par défaut edifice.bf
**Après:** `/lca/journal` → Apache → passenger_wsgi.py → Flask → Route journal

Votre route journal devrait maintenant fonctionner parfaitement! 🎯