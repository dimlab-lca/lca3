# Guide de Dépannage - Erreur Passenger sur N0C

## 🚨 Problème: "We're sorry, but something went wrong"

Cette erreur Passenger est courante lors du déploiement sur N0C. Voici comment la résoudre étape par étape.

## 🔧 Solution Rapide

### Étape 1: Utilisez les Fichiers Simplifiés

J'ai créé une version simplifiée de votre application qui devrait fonctionner immédiatement:

**Fichiers à utiliser:**
- ✅ `passenger_wsgi_fixed.py` → Renommez en `passenger_wsgi.py`
- ✅ `app_simple.py` → Application Flask simplifiée
- ✅ `requirements_simple.txt` → Dépendances minimales
- ✅ Templates simplifiés dans `/templates/`

### Étape 2: Remplacement des Fichiers

1. **Supprimez l'ancien `passenger_wsgi.py`**
2. **Renommez `passenger_wsgi_fixed.py` en `passenger_wsgi.py`**
3. **Remplacez `requirements.txt` par `requirements_simple.txt`**

### Étape 3: Modification du Point d'Entrée

Éditez `passenger_wsgi.py` pour qu'il contienne:

```python
#!/usr/bin/python3
import os
import sys

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the simple Flask application
from app_simple import application

if __name__ == "__main__":
    application.run()
```

## 🔍 Diagnostic des Erreurs

### Étape 1: Vérifiez les Logs

Via SSH:
```bash
ssh votre-utilisateur@votre-domaine.com -p 5022
cd lcatv
tail -f logs/error.log
```

### Étape 2: Page de Debug

Visitez: `https://votre-domaine.com/lcatv/debug`

Cette page vous montrera:
- Version Python utilisée
- Chemins Python
- Variables d'environnement
- Répertoire de l'application

### Étape 3: Test de Santé

Visitez: `https://votre-domaine.com/lcatv/health`

## 🛠 Solutions par Type d'Erreur

### Erreur 1: Module non trouvé

**Symptôme:** `ImportError: No module named 'xxx'`

**Solution:**
```bash
# Via SSH
source /home/votre-utilisateur/virtualenv/lcatv/3.8/bin/activate
pip install -r requirements_simple.txt
```

### Erreur 2: Problème de chemin Python

**Symptôme:** `ImportError: No module named 'app'`

**Solution:** Vérifiez que `passenger_wsgi.py` contient:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
```

### Erreur 3: Permissions de fichiers

**Symptôme:** `Permission denied`

**Solution:**
```bash
# Via SSH
chmod 755 passenger_wsgi.py
chmod 644 app_simple.py
chmod -R 755 templates/
chmod -R 755 static/
```

### Erreur 4: Version Python incompatible

**Symptôme:** `SyntaxError` ou version Python

**Solution:**
1. Dans N0C: **Langages** > **Python** > **Modifier la version**
2. Sélectionnez Python 3.8 ou plus récent

## 📋 Checklist de Dépannage

### ✅ Vérifications de Base

- [ ] Fichier `passenger_wsgi.py` présent et exécutable
- [ ] Application Flask importable (`from app_simple import application`)
- [ ] Dépendances installées (`pip install -r requirements_simple.txt`)
- [ ] Permissions correctes sur les fichiers
- [ ] Version Python compatible (3.8+)

### ✅ Structure des Fichiers

```
lcatv/
├── passenger_wsgi.py          # Point d'entrée WSGI
├── app_simple.py              # Application Flask
├── requirements_simple.txt    # Dépendances
├── templates/
│   ├── home_simple.html
│   ├── videos_simple.html
│   └── live_simple.html
└── static/ (optionnel)
```

### ✅ Test de l'Application

1. **Page d'accueil:** `https://votre-domaine.com/lcatv/`
2. **Debug:** `https://votre-domaine.com/lcatv/debug`
3. **Santé:** `https://votre-domaine.com/lcatv/health`
4. **API:** `https://votre-domaine.com/lcatv/api/videos`

## 🔄 Redémarrage de l'Application

### Via Interface N0C:
1. **Langages** > **Python**
2. Trouvez votre application `lcatv`
3. Cliquez sur l'icône **Redémarrer**

### Via SSH:
```bash
cloudlinux-selector restart --json --interpreter python --app-root lcatv
```

## 📞 Support Supplémentaire

### Commandes de Diagnostic

```bash
# Vérifier l'état de l'application
cloudlinux-selector list --json --interpreter python

# Voir les versions Python disponibles
cloudlinux-selector get --json --interpreter python

# Tester l'import Python
python3 -c "import sys; print(sys.path)"
python3 -c "from app_simple import application; print('OK')"
```

### Logs Utiles

```bash
# Logs d'erreur Apache
tail -f ~/logs/error.log

# Logs d'accès
tail -f ~/logs/access.log

# Logs Python (si configurés)
tail -f ~/lcatv/logs/app.log
```

## 🎯 Version Minimale qui Fonctionne

Si tout échoue, utilisez cette version ultra-simple de `passenger_wsgi.py`:

```python
#!/usr/bin/python3

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LCA TV - Test</title>
    </head>
    <body>
        <h1>LCA TV Application Test</h1>
        <p>Si vous voyez cette page, l'application fonctionne!</p>
        <p>Timestamp: {}</p>
    </body>
    </html>
    """.format(__import__('datetime').datetime.now())
    
    return [html.encode('utf-8')]
```

## ✅ Résultat Attendu

Une fois corrigé, vous devriez voir:
- ✅ Page d'accueil LCA TV fonctionnelle
- ✅ Navigation entre les pages
- ✅ Vidéos affichées avec des images placeholder
- ✅ Page de direct avec programme
- ✅ Connexion admin fonctionnelle

L'application simplifiée utilise des données de démonstration et devrait fonctionner immédiatement sur N0C hosting.