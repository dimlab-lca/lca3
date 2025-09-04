"""
Production version of LCA TV application
Optimized for N0C hosting environment
"""
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime, timedelta
import json
from config_production import config
from functools import wraps
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

# Import models (create if they don't exist)
try:
    from models import db_manager, publicity_manager, news_manager
except ImportError:
    # Create minimal models for production if not available
    class DummyManager:
        def get_subscriptions(self, status=None):
            return []
        def get_subscription_packages(self):
            return []
        def get_analytics_summary(self):
            return {'active_subscriptions': 0, 'active_campaigns': 0, 'monthly_revenue': 0, 'monthly_impressions': 0}
        def get_news(self, active_only=True, breaking_only=False):
            return []
        def get_breaking_news(self):
            return []
    
    publicity_manager = DummyManager()
    news_manager = DummyManager()

app = Flask(__name__)

# Load production configuration
config_name = os.environ.get('FLASK_CONFIG', 'production')
app.config.from_object(config[config_name])

# Environment variables for production
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', app.config.get('YOUTUBE_API_KEY'))
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', app.config.get('YOUTUBE_CHANNEL_ID'))
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', app.config.get('YOUTUBE_LIVE_VIDEO_ID'))

class CacheManager:
    """Simple in-memory cache with TTL"""
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
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()

# Global cache instance
cache = CacheManager()

class YouTubeService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()
        self.session.timeout = 10
    
    def get_channel_videos(self, max_results=20):
        """Get videos with caching - reduced for production"""
        cache_key = f"channel_videos_{max_results}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)  # 10 minutes cache
        if cached_videos:
            return cached_videos
        
        try:
            videos = self.get_mock_videos()  # Use mock data for production demo
            cache.set(cache_key, videos)
            return videos
        except Exception as e:
            app.logger.error(f"Error fetching videos: {e}")
            return self.get_mock_videos()
    
    def get_live_stream_info(self):
        """Get live stream info with caching"""
        cache_key = "live_stream_info"
        cached_info = cache.get(cache_key, ttl_seconds=120)
        if cached_info:
            return cached_info
        
        # Return mock live info for production demo
        live_info = {
            'id': 'demo_live',
            'title': 'LCA TV - Diffusion en Direct',
            'description': 'Suivez notre programmation en direct',
            'thumbnail': '/static/images/live-placeholder.jpg',
            'is_live': False,
            'concurrent_viewers': 0
        }
        cache.set(cache_key, live_info)
        return live_info
    
    def get_playlists(self):
        """Get playlists with caching"""
        cache_key = "channel_playlists"
        cached_playlists = cache.get(cache_key, ttl_seconds=1800)
        if cached_playlists:
            return cached_playlists
        
        # Mock playlists for production demo
        playlists = [
            {
                'id': 'playlist1',
                'title': 'Journal LCA TV',
                'description': 'Toutes les éditions du journal',
                'thumbnail': '/static/images/journal-playlist.jpg',
                'video_count': 25
            },
            {
                'id': 'playlist2',
                'title': 'Émissions Spéciales',
                'description': 'Nos émissions spéciales et débats',
                'thumbnail': '/static/images/emissions-playlist.jpg',
                'video_count': 15
            }
        ]
        cache.set(cache_key, playlists)
        return playlists
    
    def get_mock_videos(self):
        """Mock videos for production demo"""
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
                'title': 'Franc-Parler - Débat Économique',
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
            }
        ]

youtube_service = YouTubeService(YOUTUBE_API_KEY)

# Admin users
ADMIN_USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'lcatv2024'),
    'editor': os.environ.get('EDITOR_PASSWORD', 'editor123')
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    """Home page"""
    try:
        videos = youtube_service.get_channel_videos(12)
        featured_videos = videos[:6]
        return render_template('home.html', featured_videos=featured_videos)
    except Exception as e:
        app.logger.error(f"Error in home route: {e}")
        return render_template('home.html', featured_videos=[])

@app.route('/videos')
def videos():
    """All videos page"""
    try:
        all_videos = youtube_service.get_channel_videos(20)
        return render_template('videos.html', videos=all_videos)
    except Exception as e:
        app.logger.error(f"Error in videos route: {e}")
        return render_template('videos.html', videos=[])

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos by category"""
    try:
        cache_key = f"videos_category_{category}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            filtered_videos = cached_videos
        else:
            all_videos = youtube_service.get_channel_videos(20)
            filtered_videos = [v for v in all_videos if v['category'] == category]
            cache.set(cache_key, filtered_videos)
        
        return render_template('videos.html', videos=filtered_videos, category=category)
    except Exception as e:
        app.logger.error(f"Error in videos_by_category route: {e}")
        return render_template('videos.html', videos=[], category=category)

@app.route('/live')
def live():
    """Live streaming page"""
    return render_template('live.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/emissions')
def emissions():
    """Emissions page"""
    try:
        all_videos = youtube_service.get_channel_videos(15)
        return render_template('emissions.html', videos=all_videos)
    except Exception as e:
        app.logger.error(f"Error in emissions route: {e}")
        return render_template('emissions.html', videos=[])

@app.route('/publicite')
def publicite():
    """Publicite page"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Journal page"""
    try:
        cache_key = "journal_videos"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            news_videos = cached_videos
        else:
            all_videos = youtube_service.get_channel_videos(15)
            news_videos = [v for v in all_videos if v['category'] == 'actualites']
            cache.set(cache_key, news_videos)
        
        return render_template('journal.html', videos=news_videos)
    except Exception as e:
        app.logger.error(f"Error in journal route: {e}")
        return render_template('journal.html', videos=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['user'] = username
            session.permanent = True
            flash(f'Bienvenue {username} ! Connexion réussie.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    user = session.get('user', 'Utilisateur')
    session.pop('user', None)
    flash(f'Au revoir {user} ! Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    try:
        # Get content data
        videos = youtube_service.get_channel_videos(15)
        playlists = youtube_service.get_playlists()
        live_info = youtube_service.get_live_stream_info()
        
        # Get publicity and news data
        subscriptions = publicity_manager.get_subscriptions()
        packages = publicity_manager.get_subscription_packages()
        publicity_stats = publicity_manager.get_analytics_summary()
        all_news = news_manager.get_news(active_only=False)
        recent_news = news_manager.get_news(active_only=True)[:5]
        breaking_news = news_manager.get_breaking_news()
        
        # Calculate statistics
        stats = {
            'total_videos': len(videos),
            'total_playlists': len(playlists),
            'categories': {},
            'recent_videos': videos[:5] if videos else []
        }
        
        for video in videos:
            category = video.get('category', 'other')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        return render_template('dashboard_enhanced.html', 
                             videos=videos, 
                             playlists=playlists, 
                             live_info=live_info,
                             stats=stats,
                             subscriptions=subscriptions,
                             packages=packages,
                             publicity_stats=publicity_stats,
                             all_news=all_news,
                             recent_news=recent_news,
                             breaking_news=breaking_news)
    except Exception as e:
        app.logger.error(f"Dashboard error: {e}")
        return render_template('dashboard_enhanced.html', 
                             videos=[], playlists=[], live_info=None,
                             stats={'total_videos': 0, 'total_playlists': 0, 'categories': {}, 'recent_videos': []},
                             subscriptions=[], packages=[], publicity_stats={},
                             all_news=[], recent_news=[], breaking_news=[])

# API endpoints
@app.route('/api/live-status')
def api_live_status():
    """Live status API"""
    try:
        live_info = youtube_service.get_live_stream_info()
        return jsonify(live_info)
    except Exception as e:
        app.logger.error(f"API live status error: {e}")
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/api/videos')
def api_videos():
    """Videos API"""
    try:
        videos = youtube_service.get_channel_videos(20)
        return jsonify(videos)
    except Exception as e:
        app.logger.error(f"API videos error: {e}")
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}")
    return render_template('500.html'), 500

# WSGI application
application = app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)