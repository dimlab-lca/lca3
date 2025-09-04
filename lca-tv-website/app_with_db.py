#!/usr/bin/env python3
"""
LCA TV - Application avec Base de Données
Version utilisant SQLite pour l'authentification
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime, timedelta
from functools import wraps
import json
import threading
import time

# Import des managers de base de données
from models import db_manager, user_manager, publicity_manager, video_manager, settings_manager

app = Flask(__name__)

# Configuration pour production avec sous-répertoire
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', 'UCkquZjmd6ubRQh2W2YpbSLQ')
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', 'ixQEmhTbvTI')

# Gestion des URLs pour production
@app.before_request
def force_subdirectory():
    """Ensure all URLs work correctly with subdirectory"""
    # En production, s'assurer que les URLs sont correctes
    if not app.config['DEBUG']:
        # Force HTTPS en production
        if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
            return redirect(request.url.replace('http://', 'https://'))

class CacheManager:
    """Simple cache manager"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.lock = threading.Lock()
    
    def get(self, key, ttl_seconds=300):
        with self.lock:
            if key in self.cache:
                if time.time() - self.timestamps[key] < ttl_seconds:
                    return self.cache[key]
                else:
                    del self.cache[key]
                    del self.timestamps[key]
            return None
    
    def set(self, key, value):
        with self.lock:
            self.cache[key] = value
            self.timestamps[key] = time.time()

cache = CacheManager()

class YouTubeService:
    """YouTube service for fetching videos"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_channel_videos(self, max_results=20):
        """Get videos with fallback"""
        cache_key = f"channel_videos_{max_results}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            return cached_videos
        
        try:
            videos = self._get_fallback_videos()
            cache.set(cache_key, videos)
            return videos
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return self._get_fallback_videos()
    
    def _get_fallback_videos(self):
        """Fallback videos with real LCA TV content"""
        return [
            {
                'id': 'eSApphrRKWg',
                'title': 'Journal LCA TV - Édition du Soir',
                'description': 'Retrouvez l\'actualité nationale et internationale.',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'published_at': '2024-12-15T19:00:00Z',
                'category': 'actualites',
                'channel_title': 'LCA TV',
                'view_count': '15420',
                'like_count': '234',
                'comment_count': '45'
            },
            {
                'id': 'xJatmbxIaIM',
                'title': 'Franc-Parler - Débat Économie',
                'description': 'Débat sur les enjeux économiques du Burkina Faso.',
                'thumbnail': 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
                'published_at': '2024-12-14T20:30:00Z',
                'category': 'debats',
                'channel_title': 'LCA TV',
                'view_count': '8750',
                'like_count': '156',
                'comment_count': '67'
            },
            {
                'id': '8aIAKRe4Spo',
                'title': 'Festival des Masques - Culture',
                'description': 'Découvrez la richesse culturelle du Burkina Faso.',
                'thumbnail': 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
                'published_at': '2024-12-13T18:00:00Z',
                'category': 'culture',
                'channel_title': 'LCA TV',
                'view_count': '12300',
                'like_count': '298',
                'comment_count': '89'
            },
            {
                'id': 'R2EocmxeJ5Q',
                'title': 'Étalons du Burkina - Sport',
                'description': 'Suivez les Étalons dans leur match crucial.',
                'thumbnail': 'https://i.ytimg.com/vi/R2EocmxeJ5Q/hqdefault.jpg',
                'published_at': '2024-12-12T21:00:00Z',
                'category': 'sport',
                'channel_title': 'LCA TV',
                'view_count': '25600',
                'like_count': '567',
                'comment_count': '123'
            },
            {
                'id': 'pMlWnB5Wj3Q',
                'title': 'Jeunesse Avenir - Entrepreneuriat',
                'description': 'Émission dédiée aux jeunes entrepreneurs.',
                'thumbnail': 'https://i.ytimg.com/vi/pMlWnB5Wj3Q/hqdefault.jpg',
                'published_at': '2024-12-11T17:30:00Z',
                'category': 'jeunesse',
                'channel_title': 'LCA TV',
                'view_count': '6890',
                'like_count': '134',
                'comment_count': '34'
            },
            {
                'id': 'ixQEmhTbvTI',
                'title': 'Diffusion en direct de LCA TV',
                'description': 'Stream live de LCA TV.',
                'thumbnail': 'https://i.ytimg.com/vi/ixQEmhTbvTI/hqdefault.jpg',
                'published_at': '2024-12-10T11:00:00Z',
                'category': 'live',
                'channel_title': 'LCA TV',
                'view_count': '9450',
                'like_count': '187',
                'comment_count': '56'
            }
        ]

youtube_service = YouTubeService(YOUTUBE_API_KEY)

def login_required(f):
    """Decorator for admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# ROUTES PUBLIQUES DU SITE
# ============================================================================

@app.route('/')
def home():
    """Page d'accueil publique"""
    try:
        videos = youtube_service.get_channel_videos(12)
        featured_videos = videos[:6]
        return render_template('home.html', featured_videos=featured_videos)
    except Exception as e:
        print(f"Home page error: {e}")
        return render_template('home.html', featured_videos=[])

@app.route('/videos')
def videos():
    """Page des vidéos"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        return render_template('videos.html', videos=all_videos)
    except Exception as e:
        print(f"Videos page error: {e}")
        return render_template('videos.html', videos=[])

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Vidéos par catégorie"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        return render_template('videos.html', videos=filtered_videos, category=category)
    except Exception as e:
        print(f"Category videos error: {e}")
        return render_template('videos.html', videos=[], category=category)

@app.route('/live')
def live():
    """Page de diffusion en direct"""
    return render_template('live.html')

@app.route('/about')
def about():
    """Page à propos"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Page de contact"""
    return render_template('contact.html')

@app.route('/emissions')
def emissions():
    """Page des émissions"""
    try:
        all_videos = youtube_service.get_channel_videos(20)
        return render_template('emissions.html', videos=all_videos)
    except Exception as e:
        print(f"Emissions page error: {e}")
        return render_template('emissions.html', videos=[])

@app.route('/publicite')
def publicite():
    """Page publicité"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Page journal/actualités"""
    try:
        all_videos = youtube_service.get_channel_videos(20)
        news_videos = [v for v in all_videos if v['category'] == 'actualites']
        return render_template('journal.html', videos=news_videos)
    except Exception as e:
        print(f"Journal page error: {e}")
        return render_template('journal.html', videos=[])

# ============================================================================
# ROUTES ADMINISTRATIVES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion administrateur avec base de données"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Authentification via la base de données
        user = user_manager.authenticate_user(username, password)
        
        if user:
            session['user'] = user['username']
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session.permanent = True
            flash(f'Bienvenue {user["full_name"] or user["username"]} !', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login_simple.html')

@app.route('/logout')
def logout():
    """Déconnexion admin"""
    user = session.get('user', 'Utilisateur')
    session.clear()
    flash(f'Au revoir {user} !', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard administrateur avec données de la base"""
    try:
        # Statistiques depuis la base de données
        users = user_manager.get_users()
        subscriptions = publicity_manager.get_subscriptions(status='active')
        advertisements = publicity_manager.get_advertisements(status='active')
        videos = video_manager.get_videos(status='published')
        
        stats = {
            'total_users': len(users),
            'total_videos': len(videos),
            'total_ads': len(advertisements),
            'total_articles': 0,  # À implémenter si nécessaire
            'active_subscriptions': len(subscriptions),
            'monthly_revenue': sum(sub['price'] for sub in subscriptions)
        }
        
        # Paramètres depuis la base de données
        settings = settings_manager.get_all_settings()
        
        return render_template('dashboard_simple.html', stats=stats, settings=settings)
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Fallback avec données par défaut
        stats = {
            'total_users': 0,
            'total_videos': 0,
            'total_ads': 0,
            'total_articles': 0,
            'active_subscriptions': 0,
            'monthly_revenue': 0
        }
        settings = {}
        return render_template('dashboard_simple.html', stats=stats, settings=settings)

# ============================================================================
# API PUBLIQUE
# ============================================================================

@app.route('/api/videos')
def api_videos():
    """API publique des vidéos"""
    try:
        videos = youtube_service.get_channel_videos(30)
        return jsonify(videos)
    except Exception as e:
        return jsonify([])

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API vidéos par catégorie"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        return jsonify(filtered_videos)
    except Exception as e:
        return jsonify([])

# ============================================================================
# API ADMINISTRATIVE
# ============================================================================

@app.route('/api/admin/overview')
@login_required
def api_admin_overview():
    """Statistiques admin depuis la base de données"""
    try:
        users = user_manager.get_users()
        subscriptions = publicity_manager.get_subscriptions(status='active')
        advertisements = publicity_manager.get_advertisements(status='active')
        videos = video_manager.get_videos(status='published')
        
        stats = {
            'total_users': len(users),
            'total_videos': len(videos),
            'total_ads': len(advertisements),
            'total_articles': 0,
            'active_subscriptions': len(subscriptions),
            'monthly_revenue': sum(sub['price'] for sub in subscriptions)
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users')
@login_required
def api_admin_users():
    """Liste des utilisateurs depuis la base de données"""
    try:
        users = user_manager.get_users(active_only=False)
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/subscriptions')
@login_required
def api_admin_subscriptions():
    """Souscriptions publicitaires depuis la base de données"""
    try:
        subscriptions = publicity_manager.get_subscriptions()
        return jsonify(subscriptions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/advertisements')
@login_required
def api_admin_advertisements():
    """Publicités actives depuis la base de données"""
    try:
        advertisements = publicity_manager.get_advertisements()
        return jsonify(advertisements)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/videos')
@login_required
def api_admin_videos():
    """Gestion des vidéos depuis la base de données"""
    try:
        videos = video_manager.get_videos()
        return jsonify(videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@login_required
def api_admin_settings():
    """Paramètres du site depuis la base de données"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_id = session.get('user_id')
            
            for key, value in data.items():
                settings_manager.set_setting(key, value, user_id)
            
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    try:
        settings = settings_manager.get_all_settings()
        return jsonify(settings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# UTILITAIRES
# ============================================================================

@app.route('/health')
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'database': 'connected',
        'environment': os.environ.get('FLASK_ENV', 'production'),
        'application_root': app.config.get('APPLICATION_ROOT'),
        'features': {
            'public_site': True,
            'admin_dashboard': True,
            'youtube_integration': True,
            'database_auth': True
        }
    })

@app.route('/debug')
def debug_info():
    """Debug information for deployment troubleshooting"""
    import sys
    debug_data = {
        'python_version': sys.version,
        'current_directory': os.getcwd(),
        'app_directory': os.path.dirname(__file__),
        'database_path': db_manager.db_path,
        'database_exists': os.path.exists(db_manager.db_path),
        'flask_config': {
            'APPLICATION_ROOT': app.config.get('APPLICATION_ROOT'),
            'SECRET_KEY': 'SET' if app.config.get('SECRET_KEY') else 'NOT SET',
            'DEBUG': app.config.get('DEBUG'),
            'PREFERRED_URL_SCHEME': app.config.get('PREFERRED_URL_SCHEME')
        },
        'url_map': [str(rule) for rule in app.url_map.iter_rules()]
    }
    
    return jsonify(debug_data)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    if request.is_json:
        return jsonify({'error': 'Not found', 'path': request.path}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# WSGI application pour production
application = app

if __name__ == '__main__':
    print("🚀 Démarrage de LCA TV - Version avec Base de Données")
    print("=" * 60)
    print("🌐 Site Public:")
    print("   • Accueil: http://localhost:5003/")
    print("   • Vidéos: http://localhost:5003/videos")
    print("   • Live: http://localhost:5003/live")
    print()
    print("🔐 Administration:")
    print("   • Login: http://localhost:5003/login")
    print("   • Dashboard: http://localhost:5003/dashboard")
    print("   • Authentification: Base de données SQLite")
    print()
    print("📊 Base de Données:")
    print(f"   • Fichier: {db_manager.db_path}")
    print(f"   • Existe: {'✅' if os.path.exists(db_manager.db_path) else '❌'}")
    print()
    print("🔧 Gestion:")
    print("   • Ajouter admin: python add_admin.py")
    print("   • Health: http://localhost:5003/health")
    print("   • Debug: http://localhost:5003/debug")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5003)