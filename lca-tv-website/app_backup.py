from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime, timedelta
import json
from config import config
from functools import wraps
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try to import performance monitoring and models, fallback if not available
try:
    from performance_monitor import init_performance_monitoring, monitor_performance, cache_metrics
    PERFORMANCE_MONITORING = True
except ImportError:
    PERFORMANCE_MONITORING = False
    print("Performance monitoring not available")

try:
    from models import db_manager, publicity_manager, news_manager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Database models not available - using fallback")
    
    # Create dummy managers for fallback
    class DummyManager:
        def get_subscriptions(self, status=None): return []
        def get_subscription_packages(self): return []
        def get_analytics_summary(self): return {'active_subscriptions': 0, 'active_campaigns': 0, 'monthly_revenue': 0, 'monthly_impressions': 0}
        def get_news(self, active_only=True, breaking_only=False): return []
        def get_breaking_news(self): return []
    
    publicity_manager = DummyManager()
    news_manager = DummyManager()

app = Flask(__name__, static_url_path='/lca/static', static_folder='static')

# Configure for subdirectory deployment
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SERVER_NAME'] = None  # Let Flask auto-detect
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

# Custom URL adapter to ensure proper subdirectory handling
class SubdirectoryURLAdapter:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Ensure SCRIPT_NAME is properly set for URL generation
        if 'SCRIPT_NAME' not in environ or not environ['SCRIPT_NAME']:
            environ['SCRIPT_NAME'] = '/lca'
        
        # Ensure PATH_INFO doesn't include the script name
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/lca'):
            environ['PATH_INFO'] = path_info[4:] or '/'
        
        return self.app(environ, start_response)

# Wrap the Flask app with our custom adapter
app.wsgi_app = SubdirectoryURLAdapter(app.wsgi_app)

# Force Flask to use the subdirectory in URL generation
@app.before_request
def force_subdirectory():
    """Ensure all URLs are generated with the correct subdirectory"""
    # Set the script name in the request context
    if not hasattr(request, 'script_root') or request.script_root != '/lca':
        # This ensures url_for() generates URLs with /lca prefix
        pass

# Custom url_for function that ensures subdirectory prefix
from flask import url_for as flask_url_for

def url_for(endpoint, **values):
    """Custom url_for that ensures /lca prefix"""
    url = flask_url_for(endpoint, **values)
    # Ensure the URL starts with /lca if it doesn't already
    if not url.startswith('/lca') and not url.startswith('http'):
        if url.startswith('/'):
            url = '/lca' + url
        else:
            url = '/lca/' + url
    return url

# Make the custom url_for available in templates
app.jinja_env.globals['url_for'] = url_for

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
try:
    app.config.from_object(config[config_name])
except:
    # Fallback configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-fallback-secret-key')
    app.config['DEBUG'] = False

YOUTUBE_API_KEY = app.config.get('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = app.config.get('YOUTUBE_CHANNEL_ID')
YOUTUBE_LIVE_VIDEO_ID = app.config.get('YOUTUBE_LIVE_VIDEO_ID')

class CacheManager:
    """Simple in-memory cache with TTL"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.lock = threading.Lock()
    
    def get(self, key, ttl_seconds=300):  # 5 minutes default TTL
        with self.lock:
            if key in self.cache:
                if time.time() - self.timestamps[key] < ttl_seconds:
                    return self.cache[key]
                else:
                    # Cache expired
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
        self.session = requests.Session()  # Reuse connections
        self.session.timeout = 10  # Set timeout
    
    def get_channel_id_by_handle(self, handle):
        """Get channel ID from @LCATV handle with caching"""
        cache_key = f"channel_id_{handle}"
        cached_result = cache.get(cache_key, ttl_seconds=3600)  # Cache for 1 hour
        if cached_result:
            return cached_result
        
        try:
            search_url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': 'LCATV',
                'type': 'channel',
                'key': self.api_key,
                'maxResults': 10  # Reduced from 50
            }
            
            response = self.session.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('items'):
                    # Look for exact LCATV match
                    for item in data['items']:
                        channel_title = item['snippet']['title']
                        channel_id = item['snippet']['channelId']
                        
                        if channel_title.upper() == 'LCATV' or 'LCATV' in channel_title.upper():
                            cache.set(cache_key, channel_id)
                            return channel_id
                    
                    # Fallback to first result
                    first_channel = data['items'][0]
                    channel_id = first_channel['snippet']['channelId']
                    cache.set(cache_key, channel_id)
                    return channel_id
            
            return None
        except Exception as e:
            print(f"Error getting channel ID: {e}")
            return None
    
    def get_channel_videos(self, max_results=50):
        """Get latest videos with aggressive caching"""
        cache_key = f"channel_videos_{max_results}"
        cached_videos = cache.get(cache_key, ttl_seconds=300)  # Cache for 5 minutes
        if cached_videos:
            return cached_videos
        
        try:
            videos = self.get_videos_from_playlists_optimized(max_results)
            
            if not videos:
                videos = self.get_mock_videos()
            
            cache.set(cache_key, videos)
            return videos
            
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return self.get_mock_videos()
    
    def get_videos_from_playlists_optimized(self, max_results=50):
        """Optimized version with parallel requests and early termination"""
        playlist_ids = [
            'PLk5BkfzB9R2y_GaeShMuKrdQAR-eGn86S',
            'PLk5BkfzB9R2xqyMzMrGs4Z0uMxZMW2EQe', 
            'PLk5BkfzB9R2xJVGaQXQW0Q8yxwFPEY3k5',
            'PLk5BkfzB9R2wMXgDqP_apnJc7iq8p2ML2',
            'PLk5BkfzB9R2z1LpmM6ZNkSjhJeUCcjcH6'
        ]
        
        all_videos = []
        
        # Use ThreadPoolExecutor for parallel requests
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_playlist = {
                executor.submit(self.fetch_playlist_videos, playlist_id, min(20, max_results // len(playlist_ids))): playlist_id 
                for playlist_id in playlist_ids
            }
            
            for future in as_completed(future_to_playlist):
                try:
                    videos = future.result(timeout=5)  # 5 second timeout per request
                    all_videos.extend(videos)
                    
                    # Early termination if we have enough videos
                    if len(all_videos) >= max_results:
                        break
                except Exception as e:
                    playlist_id = future_to_playlist[future]
                    print(f"Error processing playlist {playlist_id}: {e}")
        
        # Remove duplicates and limit results
        seen_ids = set()
        unique_videos = []
        for video in all_videos:
            if video['id'] not in seen_ids and len(unique_videos) < max_results:
                seen_ids.add(video['id'])
                unique_videos.append(video)
        
        # Skip enrichment for better performance - use basic data
        return unique_videos
    
    def fetch_playlist_videos(self, playlist_id, max_results=20):
        """Fetch videos from a single playlist"""
        try:
            playlist_url = f"{self.base_url}/playlistItems"
            params = {
                'part': 'snippet',
                'playlistId': playlist_id,
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = self.session.get(playlist_url, params=params)
            if response.status_code == 200:
                data = response.json()
                videos = []
                
                for item in data.get('items', []):
                    # Get the best available thumbnail
                    thumbnails = item['snippet']['thumbnails']
                    thumbnail_url = ''
                    if 'high' in thumbnails:
                        thumbnail_url = thumbnails['high']['url']
                    elif 'medium' in thumbnails:
                        thumbnail_url = thumbnails['medium']['url']
                    elif 'default' in thumbnails:
                        thumbnail_url = thumbnails['default']['url']
                    
                    video = {
                        'id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                        'thumbnail': thumbnail_url,
                        'published_at': item['snippet']['publishedAt'],
                        'category': self.categorize_video_fast(item['snippet']['title']),
                        'channel_title': item['snippet']['channelTitle'],
                        'playlist_id': playlist_id,
                        'view_count': '0',  # Default values to avoid additional API calls
                        'like_count': '0',
                        'comment_count': '0'
                    }
                    videos.append(video)
                
                return videos
            return []
        except Exception as e:
            print(f"Error processing playlist {playlist_id}: {e}")
            return []
    
    def get_live_stream_info(self):
        """Get live stream information with caching"""
        cache_key = "live_stream_info"
        cached_info = cache.get(cache_key, ttl_seconds=60)  # Cache for 1 minute
        if cached_info:
            return cached_info
        
        try:
            if not YOUTUBE_LIVE_VIDEO_ID:
                return None
                
            video_url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,liveStreamingDetails',
                'id': YOUTUBE_LIVE_VIDEO_ID,
                'key': self.api_key
            }
            
            response = self.session.get(video_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    video = data['items'][0]
                    live_info = {
                        'id': video['id'],
                        'title': video['snippet']['title'],
                        'description': video['snippet']['description'],
                        'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'is_live': video['snippet'].get('liveBroadcastContent') == 'live',
                        'scheduled_start': video.get('liveStreamingDetails', {}).get('scheduledStartTime'),
                        'actual_start': video.get('liveStreamingDetails', {}).get('actualStartTime'),
                        'concurrent_viewers': video.get('liveStreamingDetails', {}).get('concurrentViewers')
                    }
                    cache.set(cache_key, live_info)
                    return live_info
            return None
        except Exception as e:
            print(f"Error fetching live stream info: {e}")
            return None
    
    def get_playlists(self):
        """Get channel playlists with caching"""
        cache_key = "channel_playlists"
        cached_playlists = cache.get(cache_key, ttl_seconds=1800)  # Cache for 30 minutes
        if cached_playlists:
            return cached_playlists
        
        try:
            if not YOUTUBE_CHANNEL_ID or YOUTUBE_CHANNEL_ID == 'UCYourChannelIDHere':
                channel_id = self.get_channel_id_by_handle('@LCATV')
                if not channel_id:
                    return []
            else:
                channel_id = YOUTUBE_CHANNEL_ID
            
            playlists_url = f"{self.base_url}/playlists"
            params = {
                'part': 'snippet,contentDetails',
                'channelId': channel_id,
                'maxResults': 25,  # Reduced from 50
                'key': self.api_key
            }
            
            response = self.session.get(playlists_url, params=params)
            if response.status_code == 200:
                data = response.json()
                playlists = []
                
                for item in data.get('items', []):
                    playlist = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'][:150] + '...' if len(item['snippet']['description']) > 150 else item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'video_count': item['contentDetails']['itemCount'],
                        'published_at': item['snippet']['publishedAt']
                    }
                    playlists.append(playlist)
                
                cache.set(cache_key, playlists)
                return playlists
            return []
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []
    
    def categorize_video_fast(self, title):
        """Faster categorization with reduced keyword sets"""
        title_lower = title.lower()
        
        # Simplified categories with key terms only
        if any(word in title_lower for word in ['journal', 'info', 'actualité', 'news', 'flash']):
            return 'actualites'
        elif any(word in title_lower for word in ['débat', 'franc-parler', 'discussion']):
            return 'debats'
        elif any(word in title_lower for word in ['culture', 'festival', 'musique', 'art']):
            return 'culture'
        elif any(word in title_lower for word in ['sport', 'football', 'étalons', 'match']):
            return 'sport'
        elif any(word in title_lower for word in ['jeunesse', 'jeune', 'éducation']):
            return 'jeunesse'
        elif any(word in title_lower for word in ['économie', 'business', 'agriculture']):
            return 'economie'
        elif any(word in title_lower for word in ['politique', 'gouvernement', 'élection']):
            return 'politique'
        elif any(word in title_lower for word in ['santé', 'médecine', 'hôpital']):
            return 'sante'
        elif any(word in title_lower for word in ['société', 'social', 'communauté']):
            return 'societe'
        
        return 'actualites'  # Default category
    
    def get_mock_videos(self):
        """Fallback videos using your real video IDs with rich content"""
        return [
            {
                'id': 'eSApphrRKWg',
                'title': 'Journal LCA TV - Édition du Soir',
                'description': 'Retrouvez l\'actualité nationale et internationale avec notre équipe de journalistes.',
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
                'description': 'Un débat enrichissant sur les enjeux économiques du Burkina Faso.',
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
                'title': 'Étalons du Burkina - Qualification CAN 2024',
                'description': 'Suivez les Étalons dans leur match crucial de qualification.',
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
                'title': 'Jeunesse Avenir - L\'Entrepreneuriat au Burkina',
                'description': 'Une émission dédiée aux jeunes entrepreneurs burkinabè.',
                'thumbnail': 'https://i.ytimg.com/vi/pMlWnB5Wj3Q/hqdefault.jpg',
                'published_at': '2024-12-11T17:30:00Z',
                'category': 'jeunesse',
                'channel_title': 'LCA TV',
                'view_count': '6890',
                'like_count': '134',
                'comment_count': '34'
            }
        ]

youtube_service = YouTubeService(YOUTUBE_API_KEY)

# Simple user credentials (in production, use a proper database)
ADMIN_USERS = {
    'admin': 'lcatv2024',
    'musk': 'tesla123',
    'editor': 'editor123'
}

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Home page with featured videos - optimized"""
    videos = youtube_service.get_channel_videos(12)  # Reduced from 50
    featured_videos = videos[:6]
    return render_template('home.html', featured_videos=featured_videos)

@app.route('/videos')
def videos():
    """All videos page - optimized"""
    all_videos = youtube_service.get_channel_videos(30)  # Reduced from 50
    return render_template('videos.html', videos=all_videos)

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos filtered by category - optimized with caching"""
    cache_key = f"videos_category_{category}"
    cached_videos = cache.get(cache_key, ttl_seconds=300)
    
    if cached_videos:
        filtered_videos = cached_videos
    else:
        all_videos = youtube_service.get_channel_videos(30)
        filtered_videos = [v for v in all_videos if v['category'] == category]
        cache.set(cache_key, filtered_videos)
    
    return render_template('videos.html', videos=filtered_videos, category=category)

@app.route('/category/<category>')
def category(category):
    """Category page - alias for videos_by_category"""
    return videos_by_category(category)

@app.route('/live')
def live():
    """Live streaming page - no API calls needed"""
    return render_template('live.html')

@app.route('/about')
def about():
    """About page - static content"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page - static content"""
    return render_template('contact.html')

@app.route('/emissions')
def emissions():
    """Emissions page - optimized"""
    all_videos = youtube_service.get_channel_videos(20)  # Reduced from 50
    return render_template('emissions.html', videos=all_videos)

@app.route('/publicite')
def publicite():
    """Publicite page - static content"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Journal/News broadcasting page - optimized"""
    cache_key = "journal_videos"
    cached_videos = cache.get(cache_key, ttl_seconds=300)
    
    if cached_videos:
        news_videos = cached_videos
    else:
        all_videos = youtube_service.get_channel_videos(20)
        news_videos = [v for v in all_videos if v['category'] == 'actualites']
        cache.set(cache_key, news_videos)
    
    return render_template('journal.html', videos=news_videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['user'] = username
            flash(f'Bienvenue {username} ! Connexion réussie.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    user = session.get('user', 'Utilisateur')
    session.pop('user', None)
    flash(f'Au revoir {user} ! Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Enhanced admin dashboard with publicity and news management"""
    try:
        # Get content data
        videos = youtube_service.get_channel_videos(20)
        playlists = youtube_service.get_playlists()
        live_info = youtube_service.get_live_stream_info()
        
        # Get publicity data
        subscriptions = publicity_manager.get_subscriptions()
        packages = publicity_manager.get_subscription_packages()
        publicity_stats = publicity_manager.get_analytics_summary()
        
        # Get news data
        all_news = news_manager.get_news(active_only=False)
        recent_news = news_manager.get_news(active_only=True)[:5]
        breaking_news = news_manager.get_breaking_news()
        
        # Calculate content statistics
        stats = {
            'total_videos': len(videos),
            'total_playlists': len(playlists),
            'categories': {},
            'recent_videos': videos[:5] if videos else []
        }
        
        # Count videos by category
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
        print(f"Dashboard error: {e}")
        # Return with empty data on error
        return render_template('dashboard_enhanced.html', 
                             videos=[], 
                             playlists=[], 
                             live_info=None,
                             stats={'total_videos': 0, 'total_playlists': 0, 'categories': {}, 'recent_videos': []},
                             subscriptions=[],
                             packages=[],
                             publicity_stats={'active_subscriptions': 0, 'active_campaigns': 0, 'monthly_revenue': 0, 'monthly_impressions': 0},
                             all_news=[],
                             recent_news=[],
                             breaking_news=[])

# API endpoints with caching
@app.route('/api/live-status')
def api_live_status():
    """API endpoint for live stream status"""
    live_info = youtube_service.get_live_stream_info()
    return jsonify(live_info)

@app.route('/api/playlists')
def api_playlists():
    """API endpoint for playlists"""
    playlists = youtube_service.get_playlists()
    return jsonify(playlists)

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """API endpoint for dashboard statistics - cached"""
    cache_key = "dashboard_stats"
    cached_stats = cache.get(cache_key, ttl_seconds=300)
    
    if cached_stats:
        return jsonify(cached_stats)
    
    try:
        videos = youtube_service.get_channel_videos(20)
        playlists = youtube_service.get_playlists()
        live_info = youtube_service.get_live_stream_info()
        
        stats = {
            'total_videos': len(videos),
            'total_playlists': len(playlists),
            'is_live': live_info.get('is_live', False) if live_info else False,
            'concurrent_viewers': live_info.get('concurrent_viewers', 0) if live_info else 0,
            'categories': {}
        }
        
        # Count videos by category
        for video in videos:
            category = video.get('category', 'other')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        cache.set(cache_key, stats)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos')
def api_videos():
    """API endpoint for videos"""
    videos = youtube_service.get_channel_videos(30)
    return jsonify(videos)

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API endpoint for videos by category"""
    cache_key = f"api_videos_category_{category}"
    cached_videos = cache.get(cache_key, ttl_seconds=300)
    
    if cached_videos:
        return jsonify(cached_videos)
    
    all_videos = youtube_service.get_channel_videos(30)
    filtered_videos = [v for v in all_videos if v['category'] == category]
    cache.set(cache_key, filtered_videos)
    return jsonify(filtered_videos)

@app.route('/api/cache/clear')
@login_required
def api_clear_cache():
    """Clear cache - admin only"""
    cache.clear()
    return jsonify({'message': 'Cache cleared successfully'})

# Publicity Management API Endpoints
@app.route('/api/subscriptions', methods=['GET', 'POST'])
@login_required
def api_subscriptions():
    """API endpoint for managing publicity subscriptions"""
    if request.method == 'GET':
        status = request.args.get('status')
        subscriptions = publicity_manager.get_subscriptions(status)
        return jsonify(subscriptions)
    
    elif request.method == 'POST':
        try:
            data = {
                'company_name': request.form.get('company_name'),
                'contact_person': request.form.get('contact_person'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone', ''),
                'subscription_type': request.form.get('subscription_type'),
                'start_date': request.form.get('start_date'),
                'end_date': request.form.get('end_date'),
                'amount': float(request.form.get('amount')),
                'status': 'active'
            }
            
            subscription_id = publicity_manager.create_subscription(data)
            return jsonify({'success': True, 'subscription_id': subscription_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/subscriptions/<int:subscription_id>/status', methods=['PUT'])
@login_required
def api_update_subscription_status(subscription_id):
    """Update subscription status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        success = publicity_manager.update_subscription_status(subscription_id, status)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/campaigns', methods=['GET', 'POST'])
@login_required
def api_campaigns():
    """API endpoint for managing publicity campaigns"""
    if request.method == 'GET':
        subscription_id = request.args.get('subscription_id', type=int)
        campaigns = publicity_manager.get_campaigns(subscription_id)
        return jsonify(campaigns)
    
    elif request.method == 'POST':
        try:
            data = {
                'subscription_id': int(request.form.get('subscription_id')),
                'campaign_name': request.form.get('campaign_name'),
                'ad_type': request.form.get('ad_type'),
                'content_url': request.form.get('content_url', ''),
                'content_text': request.form.get('content_text', ''),
                'target_audience': request.form.get('target_audience', ''),
                'schedule_start': request.form.get('schedule_start'),
                'schedule_end': request.form.get('schedule_end'),
                'impressions_target': int(request.form.get('impressions_target', 0)),
                'status': 'pending'
            }
            
            campaign_id = publicity_manager.create_campaign(data)
            return jsonify({'success': True, 'campaign_id': campaign_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/packages')
def api_packages():
    """API endpoint for subscription packages"""
    packages = publicity_manager.get_subscription_packages()
    return jsonify(packages)

@app.route('/api/publicity/analytics')
@login_required
def api_publicity_analytics():
    """API endpoint for publicity analytics"""
    analytics = publicity_manager.get_analytics_summary()
    return jsonify(analytics)

# News Management API Endpoints
@app.route('/api/news', methods=['GET', 'POST'])
@login_required
def api_news():
    """API endpoint for managing news"""
    if request.method == 'GET':
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        breaking_only = request.args.get('breaking_only', 'false').lower() == 'true'
        news = news_manager.get_news(active_only, breaking_only)
        return jsonify(news)
    
    elif request.method == 'POST':
        try:
            data = {
                'title': request.form.get('title'),
                'content': request.form.get('content'),
                'priority': request.form.get('priority', 'normal'),
                'is_breaking': request.form.get('is_breaking', 'false').lower() == 'true',
                'author': request.form.get('author', session.get('user', 'Admin')),
                'expire_date': request.form.get('expire_date') or None
            }
            
            news_id = news_manager.create_news(data)
            return jsonify({'success': True, 'news_id': news_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/news/<int:news_id>/status', methods=['PUT'])
@login_required
def api_update_news_status(news_id):
    """Update news status"""
    try:
        data = request.get_json()
        is_active = data.get('is_active')
        
        success = news_manager.update_news_status(news_id, is_active)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/news/breaking')
def api_breaking_news():
    """API endpoint for breaking news"""
    breaking_news = news_manager.get_breaking_news()
    return jsonify(breaking_news)

@app.route('/api/news/<int:news_id>/view', methods=['POST'])
def api_increment_news_views(news_id):
    """Increment news view count"""
    success = news_manager.increment_news_views(news_id)
    return jsonify({'success': success})

# Public API endpoints for website integration
@app.route('/api/public/breaking-news')
def api_public_breaking_news():
    """Public API for breaking news (for website display)"""
    breaking_news = news_manager.get_breaking_news()
    return jsonify(breaking_news)

@app.route('/api/public/flash-news')
def api_public_flash_news():
    """Public API for flash news (for website display)"""
    flash_news = news_manager.get_news(active_only=True)[:10]
    return jsonify(flash_news)

# Utility endpoints
@app.route('/api/expire-old-news', methods=['POST'])
@login_required
def api_expire_old_news():
    """Expire old news items"""
    expired_count = news_manager.expire_old_news()
    return jsonify({'success': True, 'expired_count': expired_count})

@app.route('/debug')
def debug_info():
    """Debug endpoint for deployment troubleshooting"""
    import sys
    
    # Get request information
    request_info = {
        'method': request.method,
        'path': request.path,
        'full_path': request.full_path,
        'url': request.url,
        'base_url': request.base_url,
        'url_root': request.url_root,
        'script_root': request.script_root,
        'headers': dict(request.headers),
        'environ_script_name': request.environ.get('SCRIPT_NAME'),
        'environ_path_info': request.environ.get('PATH_INFO'),
        'environ_request_uri': request.environ.get('REQUEST_URI'),
    }
    
    debug_data = {
        'python_version': sys.version,
        'python_path': sys.path,
        'current_directory': os.getcwd(),
        'app_directory': os.path.dirname(__file__),
        'files_in_directory': os.listdir(os.path.dirname(__file__)),
        'environment_variables': {k: v for k, v in os.environ.items() if 'SECRET' not in k and 'PASSWORD' not in k},
        'flask_config': {
            'APPLICATION_ROOT': app.config.get('APPLICATION_ROOT'),
            'SECRET_KEY': 'SET' if app.config.get('SECRET_KEY') else 'NOT SET',
            'DEBUG': app.config.get('DEBUG'),
            'SERVER_NAME': app.config.get('SERVER_NAME'),
            'PREFERRED_URL_SCHEME': app.config.get('PREFERRED_URL_SCHEME')
        },
        'request_info': request_info,
        'cache_stats': {
            'cached_items': len(cache.cache),
            'cache_keys': list(cache.cache.keys())
        },
        'services_available': {
            'database': DATABASE_AVAILABLE,
            'performance_monitoring': PERFORMANCE_MONITORING,
            'youtube_api_key': bool(YOUTUBE_API_KEY)
        }
    }
    
    return f"""
    <html>
    <head><title>LCA TV Debug Info - PlanetHoster</title></head>
    <body>
        <h1>LCA TV Debug Information</h1>
        <h2>Deployment Status</h2>
        <p><strong>Primary Domain:</strong> edifice.bf/lca</p>
        <p><strong>Subdomain:</strong> tv-lca.edifice.bf</p>
        <p><strong>Hosting:</strong> PlanetHoster</p>
        <p><strong>Python Version:</strong> 3.9</p>
        <p><strong>Application Root:</strong> {app.config.get('APPLICATION_ROOT', 'Not Set')}</p>
        
        <h2>Request Information</h2>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr><td><strong>Method</strong></td><td>{request_info['method']}</td></tr>
            <tr><td><strong>Path</strong></td><td>{request_info['path']}</td></tr>
            <tr><td><strong>Full Path</strong></td><td>{request_info['full_path']}</td></tr>
            <tr><td><strong>URL</strong></td><td>{request_info['url']}</td></tr>
            <tr><td><strong>Base URL</strong></td><td>{request_info['base_url']}</td></tr>
            <tr><td><strong>URL Root</strong></td><td>{request_info['url_root']}</td></tr>
            <tr><td><strong>Script Root</strong></td><td>{request_info['script_root']}</td></tr>
            <tr><td><strong>SCRIPT_NAME</strong></td><td>{request_info['environ_script_name']}</td></tr>
            <tr><td><strong>PATH_INFO</strong></td><td>{request_info['environ_path_info']}</td></tr>
            <tr><td><strong>REQUEST_URI</strong></td><td>{request_info['environ_request_uri']}</td></tr>
        </table>
        
        <h2>System Information</h2>
        <pre>{json.dumps(debug_data, indent=2, default=str)}</pre>
        
        <h2>Test Links</h2>
        <ul>
            <li><a href="{url_for('home')}">Home (url_for)</a></li>
            <li><a href="{url_for('journal')}">Journal (url_for)</a></li>
            <li><a href="{url_for('live')}">Live (url_for)</a></li>
            <li><a href="{url_for('videos')}">Videos (url_for)</a></li>
            <li><a href="{url_for('health_check')}">Health Check</a></li>
            <li><a href="{url_for('api_videos')}">Videos API</a></li>
            <li><a href="{url_for('login')}">Admin Login</a></li>
        </ul>
        
        <h2>Direct Links (for testing)</h2>
        <ul>
            <li><a href="/lca/">Home (direct /lca/)</a></li>
            <li><a href="/lca/journal">Journal (direct /lca/journal)</a></li>
            <li><a href="/lca/live">Live (direct /lca/live)</a></li>
            <li><a href="/lca/videos">Videos (direct /lca/videos)</a></li>
        </ul>
    </body>
    </html>
    """

@app.route('/debug/youtube')
def debug_youtube():
    """Debug endpoint to test YouTube API"""
    try:
        # Test API key
        test_url = f"{youtube_service.base_url}/search"
        test_params = {
            'part': 'snippet',
            'q': 'LCATV',
            'type': 'channel',
            'key': YOUTUBE_API_KEY,
            'maxResults': 5
        }
        
        response = requests.get(test_url, params=test_params)
        
        debug_info = {
            'api_key_valid': response.status_code == 200,
            'status_code': response.status_code,
            'cache_stats': {
                'cached_items': len(cache.cache),
                'cache_keys': list(cache.cache.keys())
            },
            'database_stats': {
                'subscriptions_count': len(publicity_manager.get_subscriptions()),
                'news_count': len(news_manager.get_news(active_only=False))
            }
        }
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e), 'api_key_provided': bool(YOUTUBE_API_KEY)})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'domains': {
            'primary': 'edifice.bf/lca',
            'subdomain': 'tv-lca.edifice.bf'
        },
        'hosting': 'PlanetHoster',
        'application_root': app.config.get('APPLICATION_ROOT'),
        'services': {
            'database': DATABASE_AVAILABLE,
            'performance_monitoring': PERFORMANCE_MONITORING,
            'youtube_api': bool(YOUTUBE_API_KEY)
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Initialize performance monitoring if available
if PERFORMANCE_MONITORING:
    try:
        init_performance_monitoring(app)
        print("Performance monitoring initialized")
    except Exception as e:
        print(f"Performance monitoring initialization failed: {e}")

# WSGI application for deployment
application = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)