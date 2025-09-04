#!/usr/bin/python3.9
"""
LCA TV - Production Ready Application
Optimized for PlanetHoster deployment with subdirectory support
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime, timedelta
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Production Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-production-secret-key-change-me')
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SERVER_NAME'] = None

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', '')
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', 'ixQEmhTbvTI')

# Admin credentials (use environment variables in production)
ADMIN_USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'lcatv2024'),
    'musk': os.environ.get('MUSK_PASSWORD', 'tesla123'),
    'editor': os.environ.get('EDITOR_PASSWORD', 'editor123')
}

class CacheManager:
    """Production-ready cache with TTL and thread safety"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.lock = threading.Lock()
        self.max_size = 1000  # Prevent memory issues
    
    def get(self, key, ttl_seconds=300):
        with self.lock:
            if key in self.cache:
                if time.time() - self.timestamps[key] < ttl_seconds:
                    return self.cache[key]
                else:
                    self._remove_key(key)
            return None
    
    def set(self, key, value):
        with self.lock:
            # Prevent cache from growing too large
            if len(self.cache) >= self.max_size:
                self._cleanup_old_entries()
            
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def _remove_key(self, key):
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    def _cleanup_old_entries(self):
        """Remove oldest 20% of entries"""
        if not self.timestamps:
            return
        
        sorted_items = sorted(self.timestamps.items(), key=lambda x: x[1])
        remove_count = max(1, len(sorted_items) // 5)
        
        for key, _ in sorted_items[:remove_count]:
            self._remove_key(key)
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()

cache = CacheManager()

class YouTubeService:
    """Production-optimized YouTube service"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()
        self.session.timeout = 10
        
        # Set user agent
        self.session.headers.update({
            'User-Agent': 'LCA-TV-Website/1.0'
        })
    
    def get_channel_videos(self, max_results=20):
        """Get videos with aggressive caching for production"""
        cache_key = f"channel_videos_{max_results}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)  # 10 minutes cache
        
        if cached_videos:
            return cached_videos
        
        try:
            if self.api_key:
                videos = self._fetch_real_videos(max_results)
            else:
                videos = self._get_fallback_videos()
            
            cache.set(cache_key, videos)
            return videos
            
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return self._get_fallback_videos()
    
    def _fetch_real_videos(self, max_results):
        """Fetch real videos from YouTube API"""
        # Simplified approach for production stability
        playlist_ids = [
            'PLk5BkfzB9R2y_GaeShMuKrdQAR-eGn86S',
            'PLk5BkfzB9R2xqyMzMrGs4Z0uMxZMW2EQe'
        ]
        
        all_videos = []
        
        for playlist_id in playlist_ids[:2]:  # Limit to 2 playlists for stability
            try:
                videos = self._fetch_playlist_videos(playlist_id, max_results // 2)
                all_videos.extend(videos)
                
                if len(all_videos) >= max_results:
                    break
                    
            except Exception as e:
                logger.warning(f"Error fetching playlist {playlist_id}: {e}")
                continue
        
        # Remove duplicates
        seen_ids = set()
        unique_videos = []
        for video in all_videos:
            if video['id'] not in seen_ids and len(unique_videos) < max_results:
                seen_ids.add(video['id'])
                unique_videos.append(video)
        
        return unique_videos or self._get_fallback_videos()
    
    def _fetch_playlist_videos(self, playlist_id, max_results):
        """Fetch videos from a single playlist"""
        url = f"{self.base_url}/playlistItems"
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'maxResults': min(max_results, 25),
            'key': self.api_key
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        videos = []
        
        for item in data.get('items', []):
            snippet = item['snippet']
            
            # Get best thumbnail
            thumbnails = snippet['thumbnails']
            thumbnail_url = (
                thumbnails.get('high', {}).get('url') or
                thumbnails.get('medium', {}).get('url') or
                thumbnails.get('default', {}).get('url', '')
            )
            
            video = {
                'id': snippet['resourceId']['videoId'],
                'title': snippet['title'],
                'description': self._truncate_text(snippet.get('description', ''), 200),
                'thumbnail': thumbnail_url,
                'published_at': snippet['publishedAt'],
                'category': self._categorize_video(snippet['title']),
                'channel_title': snippet.get('channelTitle', 'LCA TV'),
                'view_count': '0',
                'like_count': '0',
                'comment_count': '0'
            }
            videos.append(video)
        
        return videos
    
    def _categorize_video(self, title):
        """Fast video categorization"""
        title_lower = title.lower()
        
        categories = {
            'actualites': ['journal', 'info', 'actualité', 'news', 'flash'],
            'debats': ['débat', 'franc-parler', 'discussion', 'franc parler'],
            'culture': ['culture', 'festival', 'musique', 'art', 'soleil'],
            'sport': ['sport', 'football', 'étalons', 'match'],
            'jeunesse': ['jeunesse', 'jeune', 'éducation', 'question'],
            'economie': ['économie', 'business', 'agriculture'],
            'politique': ['politique', 'gouvernement', 'élection'],
            'sante': ['santé', 'médecine', 'hôpital'],
            'societe': ['société', 'social', 'communauté']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'actualites'
    
    def _truncate_text(self, text, max_length):
        """Safely truncate text"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    
    def _get_fallback_videos(self):
        """High-quality fallback videos for production"""
        return [
            {
                'id': 'eSApphrRKWg',
                'title': 'Journal LCA TV - Édition du Soir',
                'description': 'Retrouvez l\'actualité nationale et internationale avec notre équipe de journalistes professionnels.',
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
                'title': 'Franc-Parler - Débat sur l\'Économie Burkinabè',
                'description': 'Un débat enrichissant sur les enjeux économiques du Burkina Faso avec des experts.',
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
                'title': 'Festival des Masques de Dédougou - Reportage Culture',
                'description': 'Découvrez la richesse culturelle du Burkina Faso à travers ce festival traditionnel.',
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
                'title': 'Étalons du Burkina - Qualification CAN 2024',
                'description': 'Suivez les Étalons dans leur match crucial de qualification pour la CAN.',
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
                'title': 'Questions de Femmes - L\'Entrepreneuriat au Burkina',
                'description': 'Une émission dédiée aux femmes entrepreneures burkinabè et leurs succès.',
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
                'title': 'Soleil d\'Afrique - Musique et Culture',
                'description': 'Découvrez la musique africaine authentique et les artistes du continent.',
                'thumbnail': 'https://i.ytimg.com/vi/ixQEmhTbvTI/hqdefault.jpg',
                'published_at': '2024-12-10T11:00:00Z',
                'category': 'culture',
                'channel_title': 'LCA TV',
                'view_count': '9450',
                'like_count': '187',
                'comment_count': '56'
            }
        ]

youtube_service = YouTubeService(YOUTUBE_API_KEY)

def login_required(f):
    """Decorator for admin-only routes"""
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
    """Home page with featured videos"""
    try:
        videos = youtube_service.get_channel_videos(12)
        featured_videos = videos[:6]
        return render_template('home.html', featured_videos=featured_videos)
    except Exception as e:
        logger.error(f"Home page error: {e}")
        return render_template('home.html', featured_videos=[])

@app.route('/videos')
def videos():
    """All videos page"""
    try:
        all_videos = youtube_service.get_channel_videos(24)
        return render_template('videos.html', videos=all_videos)
    except Exception as e:
        logger.error(f"Videos page error: {e}")
        return render_template('videos.html', videos=[])

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos filtered by category"""
    try:
        cache_key = f"videos_category_{category}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            filtered_videos = cached_videos
        else:
            all_videos = youtube_service.get_channel_videos(30)
            filtered_videos = [v for v in all_videos if v['category'] == category]
            cache.set(cache_key, filtered_videos)
        
        return render_template('videos.html', videos=filtered_videos, category=category)
    except Exception as e:
        logger.error(f"Category videos error: {e}")
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
        all_videos = youtube_service.get_channel_videos(20)
        return render_template('emissions.html', videos=all_videos)
    except Exception as e:
        logger.error(f"Emissions page error: {e}")
        return render_template('emissions.html', videos=[])

@app.route('/publicite')
def publicite():
    """Publicite page"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Journal/News page"""
    try:
        cache_key = "journal_videos"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            news_videos = cached_videos
        else:
            all_videos = youtube_service.get_channel_videos(20)
            news_videos = [v for v in all_videos if v['category'] == 'actualites']
            cache.set(cache_key, news_videos)
        
        return render_template('journal.html', videos=news_videos)
    except Exception as e:
        logger.error(f"Journal page error: {e}")
        return render_template('journal.html', videos=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
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
    """Logout user"""
    user = session.get('user', 'Utilisateur')
    session.clear()
    flash(f'Au revoir {user} ! Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    try:
        videos = youtube_service.get_channel_videos(20)
        
        stats = {
            'total_videos': len(videos),
            'total_playlists': 0,
            'categories': {},
            'recent_videos': videos[:5] if videos else []
        }
        
        # Count videos by category
        for video in videos:
            category = video.get('category', 'other')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        return render_template('dashboard.html', 
                             videos=videos, 
                             stats=stats)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('dashboard.html', 
                             videos=[], 
                             stats={'total_videos': 0, 'total_playlists': 0, 'categories': {}, 'recent_videos': []})

# API Endpoints
@app.route('/api/videos')
def api_videos():
    """API endpoint for videos"""
    try:
        videos = youtube_service.get_channel_videos(30)
        return jsonify(videos)
    except Exception as e:
        logger.error(f"API videos error: {e}")
        return jsonify([])

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API endpoint for videos by category"""
    try:
        cache_key = f"api_videos_category_{category}"
        cached_videos = cache.get(cache_key, ttl_seconds=600)
        
        if cached_videos:
            return jsonify(cached_videos)
        
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        cache.set(cache_key, filtered_videos)
        return jsonify(filtered_videos)
    except Exception as e:
        logger.error(f"API category videos error: {e}")
        return jsonify([])

@app.route('/api/cache/clear')
@login_required
def api_clear_cache():
    """Clear cache - admin only"""
    try:
        cache.clear()
        return jsonify({'success': True, 'message': 'Cache cleared successfully'})
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'domains': {
            'primary': 'edifice.bf/lca',
            'subdomain': 'tv-lca.edifice.bf'
        },
        'hosting': 'PlanetHoster',
        'python_version': '3.9',
        'cache_items': len(cache.cache)
    })

@app.route('/debug')
def debug_info():
    """Debug information for troubleshooting"""
    if not app.config['DEBUG']:
        # Only show basic info in production
        return jsonify({
            'status': 'production',
            'timestamp': datetime.now().isoformat(),
            'domains': ['edifice.bf/lca', 'tv-lca.edifice.bf']
        })
    
    # Full debug info only in development
    return jsonify({
        'request_info': {
            'path': request.path,
            'url': request.url,
            'base_url': request.base_url,
            'script_root': request.script_root
        },
        'cache_stats': {
            'items': len(cache.cache),
            'keys': list(cache.cache.keys())[:10]  # Limit for security
        },
        'config': {
            'APPLICATION_ROOT': app.config.get('APPLICATION_ROOT'),
            'DEBUG': app.config.get('DEBUG')
        }
    })

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {e}")
    return render_template('500.html'), 500

# Custom URL handling for subdirectory deployment
@app.before_request
def handle_subdirectory():
    """Ensure proper URL handling for subdirectory deployment"""
    pass

# Custom url_for function for subdirectory support
from flask import url_for as flask_url_for

def url_for(endpoint, **values):
    """Custom url_for that ensures /lca prefix for subdirectory deployment"""
    url = flask_url_for(endpoint, **values)
    
    # For subdirectory deployment, ensure /lca prefix
    if not url.startswith('/lca') and not url.startswith('http'):
        if url.startswith('/'):
            url = '/lca' + url
        else:
            url = '/lca/' + url
    
    return url

# Make custom url_for available in templates
app.jinja_env.globals['url_for'] = url_for

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# WSGI application
application = app

if __name__ == '__main__':
    # Development server
    app.run(debug=False, host='0.0.0.0', port=5001)