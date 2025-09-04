# 🎛️ LCA TV - Dashboard Administrateur Complet

## 📋 Vue d'ensemble

Dashboard administrateur complet pour LCA TV avec toutes les fonctionnalités de gestion backend nécessaires pour administrer le site web et la chaîne de télévision.

## 🚀 Démarrage Rapide

### 1. Installation des dépendances
```bash
pip install flask werkzeug pillow requests
```

### 2. Lancement du dashboard
```bash
python run_admin.py
```

### 3. Accès au dashboard
- **URL**: http://localhost:5001/dashboard
- **Login**: http://localhost:5001/login
- **Utilisateur**: `admin`
- **Mot de passe**: `lcatv2024`

## ✨ Fonctionnalités Principales

### 👥 Gestion des Utilisateurs
- ✅ Créer, modifier, supprimer des utilisateurs
- ✅ Gestion des rôles (Admin, Modérateur, Éditeur)
- ✅ Activation/désactivation des comptes
- ✅ Historique des connexions
- ✅ Gestion des permissions

### 📺 Gestion des Vidéos
- ✅ Ajout de vidéos YouTube
- ✅ Upload de vidéos locales
- ✅ Gestion des catégories
- ✅ Vidéos à la une
- ✅ Synchronisation YouTube automatique
- �� Gestion des miniatures
- ✅ Programmation de diffusion

### 💰 Gestion de la Publicité
- ✅ Packages publicitaires configurables
- ✅ Souscriptions clients
- ✅ Gestion des annonces
- ✅ Suivi des impressions/clics
- ✅ Calcul automatique des prix
- ✅ Remises sur la durée
- ✅ Positions d'affichage multiples

### 📰 Gestion des Articles
- ✅ Éditeur de texte riche
- ✅ Images à la une
- ✅ Catégorisation
- ✅ Articles à la une
- ✅ Actualités urgentes
- ✅ Programmation de publication
- ✅ SEO optimisé

### 🖼️ Gestion des Médias
- ✅ Upload par glisser-déposer
- ✅ Support multi-formats (images, vidéos, documents)
- ✅ Redimensionnement automatique
- ✅ Galerie avec prévisualisation
- ✅ Recherche et filtrage
- ✅ Métadonnées complètes

### ⚙️ Paramètres du Site
- ✅ Configuration générale
- ✅ Informations de contact
- ✅ Intégration YouTube
- ✅ Paramètres système
- ✅ Mode maintenance
- ✅ Analytics

### 📊 Analytics et Statistiques
- ✅ Tableau de bord avec KPIs
- ✅ Statistiques de trafic
- ✅ Performance des publicités
- ✅ Revenus publicitaires
- ✅ Vidéos populaires
- ✅ Activité récente

## 🗂️ Structure des Fichiers

```
lca-tv-website/
├── app_admin.py                 # Application Flask principale
├── models.py                    # Modèles de base de données
├── run_admin.py                 # Script de lancement
├── lcatv.db                     # Base de données SQLite
├── templates/
│   ├── dashboard_admin.html     # Template principal du dashboard
│   └── modals/                  # Modales pour les formulaires
│       ├── user_modal.html
│       ├── subscription_modal.html
│       ├── video_modal.html
│       ├── article_modal.html
│       └── media_modal.html
├── static/
│   ├── js/
│   │   └── admin-dashboard.js   # JavaScript du dashboard
│   └── uploads/                 # Fichiers uploadés
│       ├── images/
│       ├── videos/
│       └── documents/
└── requirements.txt
```

## 🔐 Système d'Authentification

### Rôles Utilisateurs
- **Admin**: Accès complet à toutes les fonctionnalités
- **Modérateur**: Gestion du contenu et des utilisateurs
- **Éditeur**: Gestion du contenu uniquement

### Sécurité
- Mots de passe hashés avec Werkzeug
- Sessions sécurisées
- Protection CSRF
- Validation des uploads
- Limitation de taille des fichiers

## 💾 Base de Données

### Tables Principales
- `users` - Utilisateurs du système
- `publicity_subscriptions` - Souscriptions publicitaires
- `publicity_packages` - Packages publicitaires
- `advertisements` - Annonces publicitaires
- `videos` - Vidéos du site
- `articles` - Articles/actualités
- `media_files` - Fichiers médias
- `settings` - Paramètres du site
- `analytics` - Données d'analytics

### Initialisation Automatique
La base de données est créée automatiquement au premier lancement avec :
- Tables structurées
- Utilisateur admin par défaut
- Packages publicitaires de base
- Paramètres par défaut

## 🎨 Interface Utilisateur

### Design Moderne
- Interface responsive
- Thème vert LCA TV
- Navigation par onglets
- Modales pour les formulaires
- Notifications en temps réel

### Fonctionnalités UX
- Glisser-déposer pour les uploads
- Prévisualisation en temps réel
- Recherche et filtrage
- Pagination automatique
- Sauvegarde automatique

## 📡 API REST

### Endpoints Principaux
```
GET    /api/admin/overview          # Statistiques générales
GET    /api/admin/users             # Liste des utilisateurs
POST   /api/admin/users             # Créer un utilisateur
PUT    /api/admin/users/{id}        # Modifier un utilisateur
DELETE /api/admin/users/{id}        # Supprimer un utilisateur

GET    /api/admin/subscriptions     # Souscriptions publicitaires
POST   /api/admin/subscriptions     # Créer une souscription
GET    /api/admin/advertisements    # Annonces publicitaires
POST   /api/admin/advertisements    # Créer une annonce

GET    /api/admin/videos            # Liste des vidéos
POST   /api/admin/videos            # Ajouter une vidéo
POST   /api/admin/youtube/sync      # Synchroniser YouTube

GET    /api/admin/media             # Fichiers médias
POST   /api/admin/media/upload      # Upload de fichiers

GET    /api/admin/settings          # Paramètres du site
POST   /api/admin/settings          # Sauvegarder les paramètres
```

## 🔧 Configuration

### Variables d'Environnement
```bash
FLASK_ENV=development              # Mode de développement
SECRET_KEY=your-secret-key         # Clé secrète Flask
YOUTUBE_API_KEY=your-api-key       # Clé API YouTube
YOUTUBE_CHANNEL_ID=your-channel    # ID de la chaîne YouTube
```

### Paramètres de Production
```python
app.config['DEBUG'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

## 📈 Packages Publicitaires

### Package Basic (50,000 FCFA/mois)
- 1 annonce simultanée
- Position sidebar
- Analytics basiques

### Package Standard (120,000 FCFA/mois)
- 3 annonces simultanées
- Positions sidebar + header
- Analytics détaillées

### Package Premium (250,000 FCFA/mois)
- Annonces illimitées
- Toutes positions
- Analytics avancées
- Support prioritaire

### Package Sponsor (500,000 FCFA/mois)
- Sponsoring de programmes
- Mentions à l'antenne
- Logo permanent
- Analytics complètes

## 🎯 Remises Automatiques
- **3 mois**: -5%
- **6 mois**: -10%
- **12 mois**: -15%

## 🚀 Déploiement

### Développement
```bash
python run_admin.py
```

### Production
```bash
# Utiliser un serveur WSGI comme Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app_admin:application
```

## 🔍 Dépannage

### Problèmes Courants

1. **Base de données verrouillée**
   ```bash
   rm lcatv.db
   python run_admin.py  # Recréera la DB
   ```

2. **Erreur d'upload**
   - Vérifier les permissions du dossier `static/uploads/`
   - Vérifier la taille du fichier (max 50MB)

3. **Erreur YouTube API**
   - Vérifier la clé API dans les paramètres
   - Vérifier les quotas API

## 📞 Support

Pour toute question ou problème :
- 📧 Email: admin@lcatv.bf
- 📱 Téléphone: +226 XX XX XX XX
- 🌐 Site: https://lcatv.bf

## 📝 Changelog

### Version 1.0.0
- ✅ Dashboard complet fonctionnel
- ✅ Gestion des utilisateurs
- ✅ Gestion de la publicité
- ✅ Gestion des vidéos et médias
- ✅ Paramètres et analytics
- ✅ Interface responsive
- ✅ API REST complète

---

**🎉 Le dashboard admin LCA TV est maintenant prêt à être utilisé !**