# Fix pour .htaccess Principal - Edifice.bf

## 🚨 **Problème Identifié**

Le fichier `.htaccess` principal d'edifice.bf (WordPress) intercepte toutes les requêtes, y compris celles destinées à votre application LCA TV dans `/lca`.

## 🔍 **Règle Problématique**

Dans le `.htaccess` principal:
```apache
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
```

Cette règle envoie TOUTES les requêtes vers WordPress, même `/lca/journal`.

## 🔧 **Solution: Exclure le Répertoire /lca**

### **Modification du .htaccess Principal**

Remplacez la section WordPress par:

```apache
# BEGIN WordPress
# Les directives (lignes) entre « BEGIN WordPress » et « END WordPress » sont générées
# dynamiquement, et doivent être modifiées uniquement via les filtres WordPress.
# Toute modification des directives situées entre ces marqueurs sera surchargée.

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /

# IMPORTANT: Exclure le répertoire /lca de WordPress
RewriteCond %{REQUEST_URI} ^/lca(/.*)?$ [NC]
RewriteRule ^(.*)$ - [L]

RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>

# END WordPress
```

### **Explication de la Modification**

La nouvelle règle:
```apache
RewriteCond %{REQUEST_URI} ^/lca(/.*)?$ [NC]
RewriteRule ^(.*)$ - [L]
```

- **`^/lca(/.*)?$`** - Correspond à `/lca` et tout ce qui suit
- **`[NC]`** - Insensible à la casse
- **`- [L]`** - Arrête le traitement et laisse passer la requête
- **Placée AVANT** les règles WordPress

## 📋 **Fichier .htaccess Principal Complet**

Voici le fichier `.htaccess` principal modifié:

```apache
# BEGIN LSCACHE
## LITESPEED WP CACHE PLUGIN - Do not edit the contents of this block! ##
<IfModule LiteSpeed>
RewriteEngine on
CacheLookup on
RewriteRule .* - [E=Cache-Control:no-autoflush]
RewriteRule litespeed/debug/.*\.log$ - [F,L]
RewriteRule \.litespeed_conf\.dat - [F,L]

### marker ASYNC start ###
RewriteCond %{REQUEST_URI} /wp-admin/admin-ajax\.php
RewriteCond %{QUERY_STRING} action=async_litespeed
RewriteRule .* - [E=noabort:1]
### marker ASYNC end ###

### marker CACHE RESOURCE start ###
RewriteRule wp-content/.*/[^/]*(responsive|css|js|dynamic|loader|fonts)\.php - [E=cache-control:max-age=3600]
### marker CACHE RESOURCE end ###

### marker LOGIN COOKIE start ###
RewriteRule .? - [E="Cache-Vary:,wp-postpass_a34b0969900ac826508f8b358f4bef68"]
### marker LOGIN COOKIE end ###

### marker DROPQS start ###
CacheKeyModify -qs:fbclid
CacheKeyModify -qs:gclid
CacheKeyModify -qs:utm*
CacheKeyModify -qs:_ga
### marker DROPQS end ###
</IfModule>
## LITESPEED WP CACHE PLUGIN - Do not edit the contents of this block! ##
# END LSCACHE

# BEGIN NON_LSCACHE
## LITESPEED WP CACHE PLUGIN - Do not edit the contents of this block! ##
## LITESPEED WP CACHE PLUGIN - Do not edit the contents of this block! ##
# END NON_LSCACHE

# BEGIN Security Block
# Block the include-only files.
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^wp-admin/includes/ - [F,L]
RewriteRule !^wp-includes/ - [S=3]
RewriteRule ^wp-includes/[^/]+\.php$ - [F,L]
RewriteRule ^wp-includes/js/tinymce/langs/.+\.php - [F,L]
RewriteRule ^wp-includes/theme-compat/ - [F,L]
</IfModule>

# Disable directory listing
Options All -Indexes

# Remove header with PHP version
Header always unset X-Powered-By
Header unset X-Powered-By
# END Security Block

# BEGIN WordPress
# Les directives (lignes) entre « BEGIN WordPress » et « END WordPress » sont générées
# dynamiquement, et doivent être modifiées uniquement via les filtres WordPress.
# Toute modification des directives situées entre ces marqueurs sera surchargée.

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /

# IMPORTANT: Exclure le répertoire /lca de WordPress
# Cette règle doit être AVANT les règles WordPress
RewriteCond %{REQUEST_URI} ^/lca(/.*)?$ [NC]
RewriteRule ^(.*)$ - [L]

RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>

# END WordPress
```

## 🚀 **Instructions de Déploiement**

### **Étape 1: Sauvegarde**
```bash
# Connectez-vous en SSH
ssh username@edifice.bf -p 5022

# Sauvegardez le .htaccess actuel
cp ~/public_html/.htaccess ~/public_html/.htaccess.backup
```

### **Étape 2: Modification**
```bash
# Éditez le fichier principal
nano ~/public_html/.htaccess

# Ou uploadez le nouveau fichier via cPanel File Manager
```

### **Étape 3: Test Immédiat**
```bash
# Testez votre application LCA
curl -I https://edifice.bf/lca/
curl -I https://edifice.bf/lca/journal

# Testez que WordPress fonctionne toujours
curl -I https://edifice.bf/
```

## ⚠️ **Attention WordPress**

**IMPORTANT:** WordPress peut réécrire automatiquement cette section. Pour éviter cela:

### **Option 1: Protection via WordPress**
Ajoutez ce code dans `wp-config.php`:
```php
// Empêcher WordPress de modifier .htaccess
define('DISALLOW_FILE_EDIT', true);
```

### **Option 2: Surveillance**
Vérifiez régulièrement que la règle d'exclusion est toujours présente.

### **Option 3: Plugin WordPress**
Utilisez un plugin comme "Htaccess File Editor" pour protéger vos modifications.

## 🧪 **Tests de Validation**

### **Test 1: Application LCA**
- ✅ `https://edifice.bf/lca/` → Page LCA TV
- ✅ `https://edifice.bf/lca/journal` → Page journal LCA TV
- ✅ `https://edifice.bf/lca/live` → Page live LCA TV

### **Test 2: WordPress**
- ✅ `https://edifice.bf/` → Site WordPress principal
- ✅ `https://edifice.bf/wp-admin/` → Admin WordPress
- ✅ Pages WordPress existantes fonctionnent

### **Test 3: Autres Répertoires**
- ✅ Autres sous-répertoires non affectés
- ✅ Fichiers statiques accessibles

## 🔍 **Diagnostic si Problème**

### **Si LCA ne fonctionne toujours pas:**
1. Vérifiez que la règle est bien placée AVANT les règles WordPress
2. Testez avec: `curl -v https://edifice.bf/lca/debug`
3. Vérifiez les logs: `tail -f ~/logs/error.log`

### **Si WordPress ne fonctionne plus:**
1. Restaurez la sauvegarde: `cp ~/public_html/.htaccess.backup ~/public_html/.htaccess`
2. Vérifiez la syntaxe de la règle ajoutée
3. Contactez le support PlanetHoster si nécessaire

## 🎯 **Résultat Attendu**

Après cette modification:

**✅ WordPress:** Continue de fonctionner normalement
**✅ LCA TV:** Toutes les routes fonctionnent (`/lca/journal`, `/lca/live`, etc.)
**✅ Coexistence:** Les deux applications fonctionnent ensemble

## 💡 **Explication Technique**

**Avant:** Toutes les requêtes → WordPress `index.php`
**Après:** 
- Requêtes `/lca/*` → Application Python LCA TV
- Autres requêtes → WordPress `index.php`

Cette solution permet aux deux applications de coexister parfaitement sur le même domaine! 🎯