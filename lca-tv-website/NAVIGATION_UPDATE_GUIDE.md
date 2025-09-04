# Guide de Mise à Jour de la Navigation - LCA TV

## 🎯 **État Actuel de la Navigation**

Bonne nouvelle! Votre navigation est déjà correctement configurée pour le sous-répertoire `/lca`. Voici pourquoi:

## ✅ **Navigation Déjà Compatible**

### **Utilisation de `url_for()`**
Tous vos liens de navigation utilisent Flask's `url_for()` qui gère automatiquement le sous-répertoire:

```html
<!-- Navigation principale -->
<li><a href="{{ url_for('home') }}">ACCUEIL</a></li>
<li><a href="{{ url_for('journal') }}">LE JOURNAL</a></li>
<li><a href="{{ url_for('live') }}">EN DIRECT</a></li>
<li><a href="{{ url_for('emissions') }}">ÉMISSIONS & MAGAZINES</a></li>
<li><a href="{{ url_for('publicite') }}">PUBLICITÉ</a></li>
<li><a href="{{ url_for('about') }}">À PROPOS</a></li>

<!-- Liens d'authentification -->
<a href="{{ url_for('dashboard') }}">Dashboard</a>
<a href="{{ url_for('logout') }}">Déconnexion</a>
<a href="{{ url_for('login') }}">Se connecter</a>

<!-- Logo et boutons -->
<a href="{{ url_for('home') }}" class="logo">
<a href="{{ url_for('live') }}" class="watch-live-btn">
```

### **Fichiers Statiques Compatibles**
Les références aux fichiers statiques utilisent aussi `url_for()`:

```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="LCA TV">
```

## 🔧 **Comment Flask Gère le Sous-répertoire**

### **Configuration dans app.py:**
```python
app.config['APPLICATION_ROOT'] = '/lca'
```

### **Configuration WSGI dans run.py:**
```python
# Pour edifice.bf/lca
environ['SCRIPT_NAME'] = '/lca'
if path_info.startswith('/lca'):
    environ['PATH_INFO'] = path_info[4:]  # Remove '/lca'
```

### **Résultat Automatique:**
- `{{ url_for('home') }}` → `/lca/`
- `{{ url_for('videos') }}` → `/lca/videos`
- `{{ url_for('login') }}` → `/lca/login`
- `{{ url_for('static', filename='css/style.css') }}` → `/lca/static/css/style.css`

## 📊 **URLs Générées Automatiquement**

### **Pages Principales:**
| Template Link | URL Générée | URL Complète |
|---------------|-------------|--------------|
| `{{ url_for('home') }}` | `/lca/` | `https://edifice.bf/lca/` |
| `{{ url_for('videos') }}` | `/lca/videos` | `https://edifice.bf/lca/videos` |
| `{{ url_for('live') }}` | `/lca/live` | `https://edifice.bf/lca/live` |
| `{{ url_for('journal') }}` | `/lca/journal` | `https://edifice.bf/lca/journal` |
| `{{ url_for('emissions') }}` | `/lca/emissions` | `https://edifice.bf/lca/emissions` |
| `{{ url_for('publicite') }}` | `/lca/publicite` | `https://edifice.bf/lca/publicite` |
| `{{ url_for('about') }}` | `/lca/about` | `https://edifice.bf/lca/about` |
| `{{ url_for('contact') }}` | `/lca/contact` | `https://edifice.bf/lca/contact` |

### **Administration:**
| Template Link | URL Générée | URL Complète |
|---------------|-------------|--------------|
| `{{ url_for('login') }}` | `/lca/login` | `https://edifice.bf/lca/login` |
| `{{ url_for('dashboard') }}` | `/lca/dashboard` | `https://edifice.bf/lca/dashboard` |
| `{{ url_for('logout') }}` | `/lca/logout` | `https://edifice.bf/lca/logout` |

### **API:**
| Template Link | URL Générée | URL Complète |
|---------------|-------------|--------------|
| `/api/videos` | `/lca/api/videos` | `https://edifice.bf/lca/api/videos` |
| `/api/live-status` | `/lca/api/live-status` | `https://edifice.bf/lca/api/live-status` |
| `/health` | `/lca/health` | `https://edifice.bf/lca/health` |
| `/debug` | `/lca/debug` | `https://edifice.bf/lca/debug` |

## 🔍 **Vérification des Templates**

### **Templates Vérifiés ✅**
- **`base.html`** - Navigation principale ✅
- **`home.html`** - Liens internes ✅
- **`login.html`** - Formulaires et liens ✅
- **`videos.html`** - Filtres de catégories ✅
- **`live.html`** - Liens de navigation ✅

### **Tous Utilisent `url_for()`:**
```html
<!-- Correct - Gère automatiquement le sous-répertoire -->
<a href="{{ url_for('home') }}">Accueil</a>

<!-- Incorrect - Liens en dur (non trouvés dans vos templates) -->
<a href="/home">Accueil</a>
<a href="https://edifice.bf/home">Accueil</a>
```

## 🎉 **Conclusion**

### **✅ Aucune Modification Nécessaire!**

Votre navigation est déjà parfaitement configurée pour le sous-répertoire `/lca` car:

1. **Tous les liens utilisent `url_for()`** - Flask gère automatiquement le préfixe `/lca`
2. **Configuration correcte** - `APPLICATION_ROOT = '/lca'` dans app.py
3. **WSGI compatible** - run.py gère les chemins correctement
4. **Fichiers statiques** - Utilisent `url_for('static', filename='...')`

### **🚀 Prêt pour le Déploiement**

Vos templates fonctionneront automatiquement avec:
- **URL principale**: `https://edifice.bf/lca/`
- **Subdomain** (optionnel): `https://tv-lca.edifice.bf/`

### **🔧 Si Vous Trouvez des Liens Cassés**

Si vous découvrez des liens qui ne fonctionnent pas après le déploiement, vérifiez:

1. **Liens en dur** - Remplacez par `{{ url_for('route_name') }}`
2. **JavaScript** - Mettez à jour les URLs dans le code JS
3. **CSS** - Vérifiez les références d'images dans le CSS

### **Exemple de Correction (si nécessaire):**

```html
<!-- Avant (incorrect) -->
<a href="/videos">Vidéos</a>
<img src="/static/images/logo.png">

<!-- Après (correct) -->
<a href="{{ url_for('videos') }}">Vidéos</a>
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

## 📱 **Test de Navigation**

Une fois déployé, testez ces liens:

### **Navigation Principale:**
- ✅ Logo → Page d'accueil
- ✅ Menu → Toutes les pages
- ✅ Bouton "Regarder en Direct" → Page live
- ✅ Liens d'authentification → Login/Dashboard

### **Navigation Secondaire:**
- ✅ Liens dans le contenu des pages
- ✅ Boutons d'action
- ✅ Formulaires (action URLs)
- ✅ Redirections après connexion

Votre navigation LCA TV est prête pour PlanetHoster! 🎯