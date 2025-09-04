# 🚀 LCA TV - Système de Gestion Avancé

## 📋 Vue d'ensemble

Ce système complet de gestion pour LCA TV inclut :
- **Gestion des utilisateurs** avec rôles et permissions
- **Portefeuille clients** avec suivi des revenus
- **Espaces publicitaires** configurables
- **Système de publicités** avec upload d'images et code HTML
- **Analytics avancées** avec tracking des impressions et clics
- **Logs d'activité** détaillés
- **Interface d'administration** moderne et intuitive

## 🔧 Installation et Démarrage

### Prérequis
- Python 3.9+
- Flask et dépendances (voir requirements.txt)
- SQLite (inclus avec Python)

### Démarrage rapide
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer le système avancé
python start_advanced.py
```

### URLs d'accès
- **Site public** : http://localhost:5005/
- **Administration** : http://localhost:5005/login
- **Dashboard** : http://localhost:5005/dashboard

### Identifiants par défaut
- **Utilisateur** : `admin`
- **Mot de passe** : `lcatv2024`

## 🏗️ Architecture du Système

### Base de Données
Le système utilise SQLite avec les tables suivantes :

#### 👥 Users (Utilisateurs)
```sql
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE) 
- password_hash
- role (admin/editor/moderator)
- full_name
- phone
- is_active
- last_login
- created_at, updated_at
```

#### 🤝 Clients (Portefeuille)
```sql
- id (PRIMARY KEY)
- name
- email (UNIQUE)
- phone
- company_name
- address
- notes
- status (active/inactive)
- total_revenue
- created_by (FK users)
- created_at, updated_at
```

#### 📍 Ad_Spaces (Espaces Publicitaires)
```sql
- id (PRIMARY KEY)
- name
- location (header/sidebar/footer/popup/banner/etc.)
- width, height (dimensions en pixels)
- price_monthly
- description
- is_active
- created_at, updated_at
```

#### 📢 Advertisements (Publicités)
```sql
- id (PRIMARY KEY)
- client_id (FK clients)
- ad_space_id (FK ad_spaces)
- title
- content_type (image/html/video)
- image_url
- html_content
- target_url
- start_date, end_date
- status (active/inactive)
- impressions, clicks
- created_by (FK users)
- created_at, updated_at
```

#### 📊 Ad_Stats (Statistiques)
```sql
- id (PRIMARY KEY)
- advertisement_id (FK advertisements)
- date
- impressions
- clicks
- created_at
```

#### 📝 Activity_Logs (Logs d'activité)
```sql
- id (PRIMARY KEY)
- user_id (FK users)
- action
- description
- ip_address
- user_agent
- created_at
```

## 🎛️ Guide d'Utilisation du Dashboard

### 1. Vue d'ensemble
- **Statistiques générales** : Utilisateurs, clients, publicités actives, revenus
- **Activité récente** : Dernières actions effectuées
- **Graphiques** : Évolution des revenus et performances

### 2. Gestion des Utilisateurs
#### Créer un utilisateur
1. Aller dans l'onglet "Utilisateurs"
2. Cliquer sur "Ajouter Utilisateur"
3. Remplir le formulaire :
   - Nom d'utilisateur (unique)
   - Email (unique)
   - Mot de passe
   - Rôle (admin/editor/moderator)
   - Nom complet
   - Téléphone (optionnel)

#### Modifier un utilisateur
1. Cliquer sur l'icône "Modifier" dans la liste
2. Modifier les champs souhaités
3. Sauvegarder

#### Supprimer un utilisateur
1. Cliquer sur l'icône "Supprimer"
2. Confirmer l'action
3. L'utilisateur sera désactivé (soft delete)

### 3. Portefeuille Clients
#### Ajouter un client
1. Aller dans l'onglet "Clients"
2. Cliquer sur "Nouveau Client"
3. Remplir les informations :
   - Nom/Entreprise
   - Email de contact
   - Téléphone
   - Nom de l'entreprise
   - Notes

#### Suivi des revenus
- Le système calcule automatiquement les revenus par client
- Affichage du nombre de souscriptions actives
- Historique des paiements

### 4. Espaces Publicitaires
#### Créer un espace
1. Aller dans l'onglet "Espaces Pub"
2. Cliquer sur "Nouvel Espace"
3. Définir :
   - Nom de l'espace
   - Emplacement (header/sidebar/footer/etc.)
   - Dimensions (largeur x hauteur en pixels)
   - Prix mensuel en FCFA

#### Emplacements disponibles
- **Header** : Bannière en haut de page (728x90)
- **Sidebar** : Encart latéral (300x250)
- **Footer** : Bannière en bas de page (728x90)
- **Popup** : Fenêtre popup (400x300)
- **Banner** : Grande bannière (970x250)
- **Interstitiel** : Entre les contenus (300x250)

### 5. Gestion des Publicités
#### Créer une publicité
1. Aller dans l'onglet "Publicités"
2. Cliquer sur "Nouvelle Publicité"
3. Remplir le formulaire :
   - Titre de la publicité
   - Client (sélectionner dans la liste)
   - Espace publicitaire
   - Type de contenu :
     - **Image** : Upload d'un fichier image
     - **HTML** : Code HTML personnalisé
     - **Vidéo** : Intégration vidéo
   - URL de destination (optionnel)
   - Dates de début et fin

#### Types de contenu supportés
- **Images** : PNG, JPG, JPEG, GIF, WEBP (max 16MB)
- **HTML** : Code HTML avec CSS inline
- **Vidéo** : Intégration YouTube, Vimeo, etc.

#### Exemple de code HTML
```html
<div style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
            color: white; padding: 20px; text-align: center; 
            font-weight: bold; border-radius: 10px;">
    <h3>🏢 VOTRE ENTREPRISE</h3>
    <p>Votre message publicitaire ici</p>
    <small>Contactez-nous : +226 XX XX XX XX</small>
</div>
```

### 6. Analytics et Statistiques
#### Métriques disponibles
- **Impressions** : Nombre d'affichages de la publicité
- **Clics** : Nombre de clics sur la publicité
- **CTR** : Taux de clic (clics/impressions)
- **Revenus** : Revenus générés par client/période

#### Tracking automatique
- Les impressions sont comptées quand la publicité est visible
- Les clics sont trackés via l'URL `/ad-click/<id>`
- Statistiques quotidiennes sauvegardées

### 7. Logs d'Activité
Toutes les actions sont enregistrées :
- Connexions/déconnexions
- Création/modification/suppression d'utilisateurs
- Ajout/modification de clients
- Création/modification de publicités
- Modifications des paramètres

## 🌐 Intégration des Publicités sur le Site

### Utilisation du composant d'affichage
```html
{% from 'components/ad_display.html' import render_ad_space %}

<!-- Afficher une publicité header -->
{{ render_ad_space('header', ads, 728, 90) }}

<!-- Afficher une publicité sidebar -->
{{ render_ad_space('sidebar', ads, 300, 250) }}
```

### Emplacements sur le site
- **Header** : En haut de toutes les pages
- **Sidebar** : Dans la barre latérale
- **Footer** : En bas de toutes les pages
- **Popup** : Fenêtre popup (avec fermeture automatique)
- **Banner** : Grande bannière sur pages spécifiques
- **Interstitiel** : Entre les sections de contenu

### Responsive Design
- Les publicités s'adaptent automatiquement aux écrans mobiles
- Dimensions alternatives pour mobile (320x50 pour header)
- Masquage intelligent sur petits écrans

## 🔧 API Endpoints

### Authentification requise
Toutes les API admin nécessitent une session active.

### Utilisateurs
- `GET /api/admin/users` - Liste des utilisateurs
- `POST /api/admin/users` - Créer un utilisateur
- `PUT /api/admin/users/<id>` - Modifier un utilisateur
- `DELETE /api/admin/users/<id>` - Supprimer un utilisateur

### Clients
- `GET /api/admin/clients` - Liste des clients
- `POST /api/admin/clients` - Créer un client
- `PUT /api/admin/clients/<id>` - Modifier un client
- `DELETE /api/admin/clients/<id>` - Supprimer un client

### Publicités
- `GET /api/admin/advertisements` - Liste des publicités
- `POST /api/admin/advertisements` - Créer une publicité
- `DELETE /api/admin/advertisements/<id>` - Supprimer une publicité

### Espaces Publicitaires
- `GET /api/admin/ad-spaces` - Liste des espaces
- `POST /api/admin/ad-spaces` - Créer un espace
- `DELETE /api/admin/ad-spaces/<id>` - Supprimer un espace

### Statistiques
- `GET /api/admin/overview` - Statistiques générales
- `GET /api/admin/recent-activity` - Activité récente

### Paramètres
- `GET /api/admin/settings` - Récupérer les paramètres
- `POST /api/admin/settings` - Sauvegarder les paramètres

## 🚀 Déploiement en Production

### Configuration
1. Modifier les variables d'environnement :
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=votre-clé-secrète-forte
   ```

2. Configurer la base de données :
   - Utiliser PostgreSQL ou MySQL pour la production
   - Modifier la configuration dans `app_advanced.py`

3. Serveur web :
   - Utiliser Gunicorn ou uWSGI
   - Configurer Nginx comme reverse proxy

### Sécurité
- Changer le mot de passe admin par défaut
- Utiliser HTTPS en production
- Configurer les CORS si nécessaire
- Limiter les tailles d'upload
- Valider tous les inputs utilisateur

### Sauvegarde
- Sauvegarder régulièrement la base de données
- Sauvegarder le dossier `static/uploads`
- Conserver les logs d'activité

## 🔍 Dépannage

### Problèmes courants
1. **Erreur de base de données** : Vérifier les permissions du fichier SQLite
2. **Upload échoué** : Vérifier l'espace disque et les permissions
3. **Publicités non affichées** : Vérifier les dates de validité
4. **Problème de connexion** : Vérifier les identifiants et la session

### Logs
- Les erreurs sont affichées dans la console en mode debug
- Les logs d'activité sont dans la base de données
- Utiliser `/health` pour vérifier l'état du système

### Support
- Consulter les logs d'activité dans le dashboard
- Utiliser l'endpoint `/debug` pour les informations système
- Vérifier la configuration avec `/health`

## 📈 Évolutions Futures

### Fonctionnalités prévues
- **Système de facturation** automatique
- **Notifications** par email
- **Rapports** PDF exportables
- **API publique** pour intégrations
- **Multi-langue** (français/anglais)
- **Thèmes** personnalisables
- **Backup automatique**

### Intégrations possibles
- **Systèmes de paiement** (Orange Money, Moov Money)
- **CRM** externes
- **Outils d'emailing**
- **Analytics** Google/Facebook
- **Réseaux sociaux**

---

## 📞 Contact et Support

Pour toute question ou assistance :
- **Email** : support@lcatv.bf
- **Téléphone** : +226 XX XX XX XX
- **Documentation** : Consultez ce guide
- **Logs** : Utilisez le dashboard pour diagnostiquer

---

*Guide créé pour LCA TV - Système de Gestion Avancé v3.0*