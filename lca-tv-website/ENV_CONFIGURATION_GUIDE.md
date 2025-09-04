# Guide de Configuration .env pour LCA TV

## 📋 Contenu Correct du Fichier .env

Basé sur l'analyse de votre code, voici le contenu exact que doit contenir votre fichier `.env`:

## 🔑 Variables OBLIGATOIRES

### 1. Clé Secrète Flask
```bash
FLASK_SECRET_KEY=votre-cle-secrete-super-securisee-changez-moi
```
**Importance**: CRITIQUE - Utilisée pour la sécurité des sessions
**Comment générer**: Utilisez une chaîne aléatoire de 32+ caractères
**Exemple**: `FLASK_SECRET_KEY=8f42a73054b1749e7e8b4d5c6a9f2e1d3c7b8a9e4f5d6c7b8a9e0f1d2c3b4a5e6`

### 2. Configuration de l'Environnement
```bash
FLASK_CONFIG=production
FLASK_ENV=production
```

### 3. Mots de Passe Admin
```bash
ADMIN_PASSWORD=votre-mot-de-passe-admin-securise
EDITOR_PASSWORD=votre-mot-de-passe-editeur-securise
```
**Utilisateurs disponibles**:
- `admin` avec le mot de passe défini dans `ADMIN_PASSWORD`
- `editor` avec le mot de passe défini dans `EDITOR_PASSWORD`
- `musk` avec mot de passe fixe `tesla123` (défini dans le code)

## 🎥 Variables OPTIONNELLES (YouTube)

### API YouTube (Recommandé pour les vraies vidéos)
```bash
YOUTUBE_API_KEY=votre-cle-api-youtube
YOUTUBE_CHANNEL_ID=UCvotre-id-chaine-youtube
YOUTUBE_LIVE_VIDEO_ID=votre-id-video-live
```

**Note**: L'application fonctionne parfaitement SANS ces variables (utilise des vidéos de démonstration)

## 📄 Fichier .env Complet

Créez un fichier `.env` dans votre répertoire `tv-lca` avec ce contenu:

```bash
# =============================================================================
# CONFIGURATION OBLIGATOIRE
# =============================================================================

# Clé secrète Flask (CHANGEZ CETTE VALEUR!)
FLASK_SECRET_KEY=8f42a73054b1749e7e8b4d5c6a9f2e1d3c7b8a9e4f5d6c7b8a9e0f1d2c3b4a5e6

# Configuration de l'environnement
FLASK_CONFIG=production
FLASK_ENV=production

# Mots de passe admin (CHANGEZ CES VALEURS!)
ADMIN_PASSWORD=MonMotDePasseAdminSecurise2024!
EDITOR_PASSWORD=MonMotDePasseEditeurSecurise2024!

# =============================================================================
# CONFIGURATION OPTIONNELLE
# =============================================================================

# API YouTube (optionnel - l'app fonctionne sans)
YOUTUBE_API_KEY=AIzaSyVotreClefAPIYouTubeIci
YOUTUBE_CHANNEL_ID=UCVotreIdChaineYouTubeIci
YOUTUBE_LIVE_VIDEO_ID=VotreIdVideoLiveIci

# Base de données (optionnel)
DATABASE_URL=sqlite:///lcatv_production.db

# Logs (optionnel)
LOG_LEVEL=INFO
```

## 🔍 Comment Votre Code Utilise Ces Variables

### Dans config.py:
```python
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key'
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')
```

### Dans app.py:
```python
# Configuration Flask
config_name = os.environ.get('FLASK_CONFIG', 'default')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-fallback-secret-key')

# YouTube API
YOUTUBE_API_KEY = app.config.get('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = app.config.get('YOUTUBE_CHANNEL_ID')
YOUTUBE_LIVE_VIDEO_ID = app.config.get('YOUTUBE_LIVE_VIDEO_ID')

# Authentification
ADMIN_USERS = {
    'admin': 'lcatv2024',  # Mot de passe par défaut
    'musk': 'tesla123',    # Mot de passe fixe
    'editor': 'editor123'  # Mot de passe par défaut
}
```

## ⚠️ Variables Importantes à Noter

### 1. Incohérence dans les Noms de Variables
Votre code utilise deux noms différents pour la clé secrète:
- `config.py` cherche: `FLASK_SECRET_KEY`
- `app.py` cherche: `SECRET_KEY`

**Solution**: Utilisez `FLASK_SECRET_KEY` (comme dans config.py)

### 2. Mots de Passe Admin
Les mots de passe sont actuellement codés en dur dans `app.py`. Pour utiliser les variables d'environnement, vous devriez modifier:

```python
ADMIN_USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'lcatv2024'),
    'musk': 'tesla123',
    'editor': os.environ.get('EDITOR_PASSWORD', 'editor123')
}
```

## 🛠 Étapes de Configuration

### 1. Créer le Fichier .env
```bash
# Via SSH ou gestionnaire de fichiers N0C
cd tv-lca
nano .env
```

### 2. Copier le Contenu
Copiez le contenu du fichier `.env` complet ci-dessus

### 3. Personnaliser les Valeurs
- **Changez** `FLASK_SECRET_KEY` avec une valeur unique
- **Changez** `ADMIN_PASSWORD` et `EDITOR_PASSWORD`
- **Ajoutez** vos clés YouTube si vous les avez

### 4. Sauvegarder et Redémarrer
```bash
# Sauvegarder le fichier
# Puis redémarrer l'application dans N0C
```

## 🔐 Génération de Clé Secrète Sécurisée

### Méthode 1: Python
```python
import secrets
print(secrets.token_hex(32))
```

### Méthode 2: OpenSSL
```bash
openssl rand -hex 32
```

### Méthode 3: En ligne
Utilisez un générateur de mots de passe sécurisé en ligne

## ✅ Test de Configuration

### 1. Vérifier les Variables
Visitez: `https://edifice.bf/tv-lca/debug`

### 2. Tester la Connexion Admin
- URL: `https://edifice.bf/tv-lca/login`
- Utilisateur: `admin`
- Mot de passe: Celui défini dans `ADMIN_PASSWORD`

### 3. Vérifier l'API YouTube
Visitez: `https://edifice.bf/tv-lca/debug/youtube`

## 🚨 Sécurité

### ❌ Ne JAMAIS faire:
- Utiliser les mots de passe par défaut en production
- Partager le fichier `.env`
- Commiter le fichier `.env` dans Git

### ✅ Bonnes pratiques:
- Utiliser des mots de passe forts et uniques
- Changer la clé secrète Flask
- Garder le fichier `.env` privé
- Faire des sauvegardes sécurisées

## 📞 Support

Si vous avez des problèmes avec la configuration:

1. **Vérifiez** que le fichier `.env` est dans le bon répertoire (`tv-lca/`)
2. **Vérifiez** les permissions du fichier (644)
3. **Redémarrez** l'application après modification
4. **Consultez** la page de debug pour vérifier les variables

Votre application LCA TV fonctionnera parfaitement avec cette configuration!