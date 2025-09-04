# 🚀 Guide de Déploiement LCA TV

## 🔧 Problème de Login 404 - Solution

Le problème de redirection 404 lors du login vient de la configuration des URLs pour le sous-répertoire `/lca`. Voici la solution complète :

## 📁 Structure des Fichiers

```
lca-tv-website/
├── app.py                    # Application principale (production)
├── passenger_wsgi.py         # Configuration WSGI pour PlanetHoster
├── templates/               # Templates HTML
├── static/                  # Fichiers statiques
└── .htaccess               # Configuration Apache (IMPORTANT)
```

## 🔧 Configuration .htaccess

Créez ou modifiez le fichier `.htaccess` dans le répertoire `/lca` :

```apache
# .htaccess pour LCA TV
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Redirection vers l'application Flask
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [QSA,L]

# Configuration pour les fichiers statiques
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
</FilesMatch>
```

## 🌐 URLs Correctes

### En Local (Développement)
- Site: `http://localhost:5001/`
- Login: `http://localhost:5001/login`
- Dashboard: `http://localhost:5001/dashboard`

### En Production (PlanetHoster)
- Site: `https://edifice.bf/lca/`
- Login: `https://edifice.bf/lca/login`
- Dashboard: `https://edifice.bf/lca/dashboard`

## 🔐 Configuration des Identifiants

Les identifiants par défaut sont :
- **admin** / **lcatv2024**
- **editor** / **editor123**
- **musk** / **tesla123**

## 🛠️ Étapes de Déploiement

### 1. Upload des Fichiers
```bash
# Uploadez ces fichiers dans le répertoire /lca/ :
- app.py
- passenger_wsgi.py
- templates/ (dossier complet)
- static/ (dossier complet)
- .htaccess
```

### 2. Configuration du Serveur
```bash
# Assurez-vous que ces permissions sont définies :
chmod 644 app.py
chmod 644 passenger_wsgi.py
chmod 644 .htaccess
chmod -R 644 templates/
chmod -R 644 static/
```

### 3. Test de Fonctionnement
```bash
# Testez ces URLs dans l'ordre :
1. https://edifice.bf/lca/health
2. https://edifice.bf/lca/debug
3. https://edifice.bf/lca/
4. https://edifice.bf/lca/login
```

## 🐛 Diagnostic des Problèmes

### URL de Debug
Accédez à `https://edifice.bf/lca/debug` pour voir :
- Configuration Flask
- Variables d'environnement
- Informations de requête
- Routes disponibles

### Logs d'Erreur
Vérifiez les logs du serveur pour :
- Erreurs 404
- Erreurs de redirection
- Problèmes de permissions

## 🔧 Solutions aux Problèmes Courants

### 1. Login redirige vers 404
**Cause :** Configuration .htaccess incorrecte
**Solution :** Vérifiez que le .htaccess est dans le bon répertoire

### 2. CSS/JS ne se chargent pas
**Cause :** Chemins statiques incorrects
**Solution :** Vérifiez les chemins dans les templates

### 3. Erreur 500
**Cause :** Erreur Python ou configuration
**Solution :** Vérifiez les logs et la configuration WSGI

## 📊 Fonctionnalités du Dashboard

Une fois connecté, le dashboard offre :

### 📈 Vue d'Ensemble
- Statistiques générales
- Activité récente
- Revenus publicitaires

### 👥 Gestion des Utilisateurs
- Créer/modifier/supprimer des utilisateurs
- Gestion des rôles (admin, editor, moderator)
- Historique des connexions

### 💰 Gestion de la Publicité
- Souscriptions clients
- Packages publicitaires
- Suivi des performances

### 📺 Gestion des Vidéos
- Ajout de vidéos YouTube
- Catégorisation
- Gestion des miniatures

### 📰 Gestion des Articles
- Éditeur de texte riche
- Publication programmée
- Catégories d'actualités

### 🖼️ Gestion des Médias
- Upload de fichiers
- Galerie d'images
- Gestion des documents

### ⚙️ Paramètres
- Configuration du site
- Intégration YouTube
- Paramètres de contact

### 📊 Analytics
- Statistiques de trafic
- Performance des vidéos
- Données publicitaires

## 🆘 Support

En cas de problème :

1. **Vérifiez l'URL de debug :** `https://edifice.bf/lca/debug`
2. **Consultez les logs du serveur**
3. **Vérifiez la configuration .htaccess**
4. **Testez en local d'abord**

## 📞 Contact

- Email : admin@lcatv.bf
- Support technique : Vérifiez les logs et la documentation

---

**✅ Une fois ces étapes suivies, le login devrait fonctionner correctement !**