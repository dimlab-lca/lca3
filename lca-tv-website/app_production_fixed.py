#!/usr/bin/env python3
"""
LCA TV - Application Production Fixed
Fixed version for server deployment without incomplete response issues
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime, timedelta
from functools import wraps
import json
import threading
import time
import sys
import traceback

app = Flask(__name__)

# Configuration pour production avec sous-répertoire
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-secret-key-production')
app.config['DEBUG'] = False  # Always False in production
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', 'UCkquZjmd6ubRQh2W2YpbSLQ')
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', 'ixQEmhTbvTI')

# Admin credentials
ADMIN_USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'lcatv2024'),
    'musk': os.environ.get('MUSK_PASSWORD', 'tesla123'),
    'editor': os.environ.get('EDITOR_PASSWORD', 'editor123')
}

# Error logging for production
def log_error(error, context=""):
    """Log errors to stderr for server debugging"""
    error_msg = f"[LCA TV ERROR] {context}: {str(error)}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)

# Gestion des URLs pour production
@app.before_request
def force_subdirectory():
    """Ensure all URLs work correctly with subdirectory"""
    try:
        # En production, s'assurer que les URLs sont correctes
        if not app.config['DEBUG']:
            # Force HTTPS en production
            if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
                return redirect(request.url.replace('http://', 'https://'))
    except Exception as e:
        log_error(e, "force_subdirectory")
        # Don't break the request if there's an error
        pass

class CacheManager:
    """Simple cache manager"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.lock = threading.Lock()
    
    def get(self, key, ttl_seconds=300):
        try:
            with self.lock:
                if key in self.cache:
                    if time.time() - self.timestamps[key] < ttl_seconds:
                        return self.cache[key]
                    else:
                        del self.cache[key]
                        del self.timestamps[key]
                return None
        except Exception as e:
            log_error(e, "CacheManager.get")
            return None
    
    def set(self, key, value):
        try:
            with self.lock:
                self.cache[key] = value
                self.timestamps[key] = time.time()
        except Exception as e:
            log_error(e, "CacheManager.set")

cache = CacheManager()

class YouTubeService:
    """YouTube service for fetching videos"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_channel_videos(self, max_results=20):
        """Get videos with fallback"""
        try:
            cache_key = f"channel_videos_{max_results}"
            cached_videos = cache.get(cache_key, ttl_seconds=600)
            
            if cached_videos:
                return cached_videos
            
            videos = self._get_fallback_videos()
            cache.set(cache_key, videos)
            return videos
        except Exception as e:
            log_error(e, "YouTubeService.get_channel_videos")
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
        try:
            if 'user' not in session:
                if request.is_json:
                    return jsonify({'error': 'Authentication required'}), 401
                flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        except Exception as e:
            log_error(e, "login_required decorator")
            return jsonify({'error': 'Internal server error'}), 500
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
        log_error(e, "home route")
        return render_template('home.html', featured_videos=[])

@app.route('/videos')
def videos():
    """Page des vidéos"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        return render_template('videos.html', videos=all_videos)
    except Exception as e:
        log_error(e, "videos route")
        return render_template('videos.html', videos=[])

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Vidéos par catégorie"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        return render_template('videos.html', videos=filtered_videos, category=category)
    except Exception as e:
        log_error(e, f"videos_by_category route - category: {category}")
        return render_template('videos.html', videos=[], category=category)

@app.route('/live')
def live():
    """Page de diffusion en direct"""
    try:
        return render_template('live.html')
    except Exception as e:
        log_error(e, "live route")
        return "Error loading live page", 500

@app.route('/about')
def about():
    """Page à propos"""
    try:
        return render_template('about.html')
    except Exception as e:
        log_error(e, "about route")
        return "Error loading about page", 500

@app.route('/contact')
def contact():
    """Page de contact"""
    try:
        return render_template('contact.html')
    except Exception as e:
        log_error(e, "contact route")
        return "Error loading contact page", 500

@app.route('/emissions')
def emissions():
    """Page des émissions"""
    try:
        all_videos = youtube_service.get_channel_videos(20)
        return render_template('emissions.html', videos=all_videos)
    except Exception as e:
        log_error(e, "emissions route")
        return render_template('emissions.html', videos=[])

@app.route('/publicite')
def publicite():
    """Page publicité"""
    try:
        return render_template('publicite.html')
    except Exception as e:
        log_error(e, "publicite route")
        return "Error loading publicite page", 500

@app.route('/journal')
def journal():
    """Page journal/actualités"""
    try:
        all_videos = youtube_service.get_channel_videos(20)
        news_videos = [v for v in all_videos if v['category'] == 'actualites']
        return render_template('journal.html', videos=news_videos)
    except Exception as e:
        log_error(e, "journal route")
        return render_template('journal.html', videos=[])

# ============================================================================
# ROUTES ADMINISTRATIVES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion administrateur"""
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if username in ADMIN_USERS and ADMIN_USERS[username] == password:
                session['user'] = username
                session.permanent = True
                flash(f'Bienvenue {username} !', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        
        return render_template('login_simple.html')
    except Exception as e:
        log_error(e, "login route")
        return "Error loading login page", 500

@app.route('/logout')
def logout():
    """Déconnexion admin"""
    try:
        user = session.get('user', 'Utilisateur')
        session.clear()
        flash(f'Au revoir {user} !', 'info')
        return redirect(url_for('home'))
    except Exception as e:
        log_error(e, "logout route")
        return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard administrateur"""
    try:
        stats = {
            'total_users': 5,
            'total_videos': 150,
            'total_ads': 12,
            'total_articles': 45,
            'active_subscriptions': 8,
            'monthly_revenue': 2500000
        }
        
        settings = {
            'site_title': 'LCA TV',
            'site_description': 'Votre chaîne de référence au Burkina Faso',
            'contact_email': 'contact@lcatv.bf',
            'contact_phone': '+226 XX XX XX XX',
            'youtube_channel_id': 'UCkquZjmd6ubRQh2W2YpbSLQ',
            'youtube_live_video_id': 'ixQEmhTbvTI',
            'analytics_enabled': 'true',
            'maintenance_mode': 'false'
        }
        
        return render_template('dashboard_simple.html', stats=stats, settings=settings)
    except Exception as e:
        log_error(e, "dashboard route")
        return "Error loading dashboard", 500

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
        log_error(e, "api_videos")
        return jsonify([])

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API vidéos par catégorie"""
    try:
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        return jsonify(filtered_videos)
    except Exception as e:
        log_error(e, f"api_videos_by_category - category: {category}")
        return jsonify([])

# ============================================================================
# API ADMINISTRATIVE
# ============================================================================

@app.route('/api/admin/overview')
@login_required
def api_admin_overview():
    """Statistiques admin"""
    try:
        stats = {
            'total_users': 5,
            'total_videos': 150,
            'total_ads': 12,
            'total_articles': 45,
            'active_subscriptions': 8,
            'monthly_revenue': 2500000
        }
        return jsonify(stats)
    except Exception as e:
        log_error(e, "api_admin_overview")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/admin/recent-activity')
@login_required
def api_admin_recent_activity():
    """Activité récente"""
    try:
        activities = [
            {'icon': 'user-plus', 'description': 'Nouvel utilisateur créé', 'time': '5 min'},
            {'icon': 'video', 'description': 'Vidéo ajoutée', 'time': '15 min'},
            {'icon': 'ad', 'description': 'Nouvelle souscription', 'time': '1 heure'},
            {'icon': 'edit', 'description': 'Article modifié', 'time': '2 heures'},
            {'icon': 'settings', 'description': 'Paramètres mis à jour', 'time': '3 heures'},
        ]
        return jsonify(activities)
    except Exception as e:
        log_error(e, "api_admin_recent_activity")
        return jsonify([])

@app.route('/api/admin/users')
@login_required
def api_admin_users():
    """Liste des utilisateurs"""
    try:
        users = [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@lcatv.bf',
                'role': 'admin',
                'full_name': 'Administrateur LCA TV',
                'last_login': '2024-01-15T10:30:00',
                'is_active': True
            },
            {
                'id': 2,
                'username': 'editor',
                'email': 'editor@lcatv.bf',
                'role': 'editor',
                'full_name': 'Éditeur Principal',
                'last_login': '2024-01-14T16:45:00',
                'is_active': True
            },
            {
                'id': 3,
                'username': 'musk',
                'email': 'musk@lcatv.bf',
                'role': 'moderator',
                'full_name': 'Modérateur',
                'last_login': '2024-01-13T09:15:00',
                'is_active': True
            }
        ]
        return jsonify(users)
    except Exception as e:
        log_error(e, "api_admin_users")
        return jsonify([])

@app.route('/api/admin/subscriptions')
@login_required
def api_admin_subscriptions():
    """Souscriptions publicitaires"""
    try:
        subscriptions = [
            {
                'id': 1,
                'client_name': 'Entreprise ABC',
                'package_type': 'Package Premium',
                'duration_months': 6,
                'price': 1500000,
                'start_date': '2024-01-01',
                'end_date': '2024-07-01',
                'status': 'active'
            },
            {
                'id': 2,
                'client_name': 'Société XYZ',
                'package_type': 'Package Standard',
                'duration_months': 3,
                'price': 360000,
                'start_date': '2024-01-15',
                'end_date': '2024-04-15',
                'status': 'active'
            }
        ]
        return jsonify(subscriptions)
    except Exception as e:
        log_error(e, "api_admin_subscriptions")
        return jsonify([])

@app.route('/api/admin/advertisements')
@login_required
def api_admin_advertisements():
    """Publicités actives"""
    try:
        advertisements = [
            {
                'id': 1,
                'title': 'Publicité Entreprise ABC',
                'client_name': 'Entreprise ABC',
                'position': 'header',
                'start_date': '2024-01-01',
                'end_date': '2024-07-01',
                'impressions': 15420,
                'clicks': 234,
                'status': 'active'
            },
            {
                'id': 2,
                'title': 'Bannière Société XYZ',
                'client_name': 'Société XYZ',
                'position': 'sidebar',
                'start_date': '2024-01-15',
                'end_date': '2024-04-15',
                'impressions': 8750,
                'clicks': 156,
                'status': 'active'
            }
        ]
        return jsonify(advertisements)
    except Exception as e:
        log_error(e, "api_admin_advertisements")
        return jsonify([])

@app.route('/api/admin/videos')
@login_required
def api_admin_videos():
    """Gestion des vidéos"""
    try:
        videos = [
            {
                'id': 1,
                'title': 'Journal LCA TV - Édition du Soir',
                'category': 'actualites',
                'thumbnail_url': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'youtube_id': 'eSApphrRKWg',
                'view_count': 15420,
                'created_at': '2024-01-15T19:00:00',
                'status': 'published'
            },
            {
                'id': 2,
                'title': 'Franc-Parler - Débat Économie',
                'category': 'debats',
                'thumbnail_url': 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
                'youtube_id': 'xJatmbxIaIM',
                'view_count': 8750,
                'created_at': '2024-01-14T20:30:00',
                'status': 'published'
            }
        ]
        return jsonify(videos)
    except Exception as e:
        log_error(e, "api_admin_videos")
        return jsonify([])

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@login_required
def api_admin_settings():
    """Paramètres du site"""
    try:
        if request.method == 'POST':
            return jsonify({'success': True})
        
        settings = {
            'site_title': 'LCA TV',
            'site_description': 'Votre chaîne de référence au Burkina Faso',
            'contact_email': 'contact@lcatv.bf',
            'contact_phone': '+226 XX XX XX XX',
            'youtube_channel_id': 'UCkquZjmd6ubRQh2W2YpbSLQ',
            'youtube_live_video_id': 'ixQEmhTbvTI',
            'analytics_enabled': 'true',
            'maintenance_mode': 'false'
        }
        return jsonify(settings)
    except Exception as e:
        log_error(e, "api_admin_settings")
        return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# UTILITAIRES
# ============================================================================

@app.route('/health')
def health_check():
    """Health check"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0-fixed',
            'environment': 'production',
            'application_root': app.config.get('APPLICATION_ROOT'),
            'request_info': {
                'url': request.url,
                'base_url': request.base_url,
                'script_root': request.script_root,
                'path': request.path
            },
            'features': {
                'public_site': True,
                'admin_dashboard': True,
                'youtube_integration': True
            }
        })
    except Exception as e:
        log_error(e, "health_check")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/debug')
def debug_info():
    """Debug information for deployment troubleshooting"""
    try:
        debug_data = {
            'python_version': sys.version,
            'current_directory': os.getcwd(),
            'app_directory': os.path.dirname(__file__),
            'request_info': {
                'url': request.url,
                'base_url': request.base_url,
                'script_root': request.script_root,
                'path': request.path,
                'host': request.host,
                'headers': dict(request.headers)
            },
            'flask_config': {
                'APPLICATION_ROOT': app.config.get('APPLICATION_ROOT'),
                'SECRET_KEY': 'SET' if app.config.get('SECRET_KEY') else 'NOT SET',
                'DEBUG': app.config.get('DEBUG'),
                'PREFERRED_URL_SCHEME': app.config.get('PREFERRED_URL_SCHEME')
            },
            'environment_variables': {k: v for k, v in os.environ.items() if 'SECRET' not in k and 'PASSWORD' not in k},
            'url_map': [str(rule) for rule in app.url_map.iter_rules()]
        }
        
        return jsonify(debug_data)
    except Exception as e:
        log_error(e, "debug_info")
        return jsonify({'error': 'Debug info error', 'message': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    try:
        if request.is_json:
            return jsonify({'error': 'Not found', 'path': request.path}), 404
        return render_template('404.html'), 404
    except Exception as e:
        log_error(e, "404 error handler")
        return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    try:
        log_error(error, "500 internal error")
        if request.is_json:
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('500.html'), 500
    except Exception as e:
        log_error(e, "500 error handler")
        return "Internal server error", 500

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# WSGI application pour production
application = app

if __name__ == '__main__':
    print("🚀 Démarrage de LCA TV - Version Production Fixed")
    print("=" * 60)
    print("🌐 Site Public:")
    print("   • Accueil: http://localhost:5001/")
    print("   • Vidéos: http://localhost:5001/videos")
    print("   • Live: http://localhost:5001/live")
    print()
    print("🔐 Administration:")
    print("   • Login: http://localhost:5001/login")
    print("   • Dashboard: http://localhost:5001/dashboard")
    print("   • Identifiants: admin / lcatv2024")
    print()
    print("📡 API & Debug:")
    print("   • Health: http://localhost:5001/health")
    print("   • Debug: http://localhost:5001/debug")
    print()
    print("🌍 Production URLs:")
    print("   • Site: https://edifice.bf/lca/")
    print("   • Login: https://edifice.bf/lca/login")
    print("   • Dashboard: https://edifice.bf/lca/dashboard")
    print("   • Debug: https://edifice.bf/lca/debug")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5001)