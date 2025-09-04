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
    from models import db_manager, publicity_manager, article_manager, media_manager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Database models not available - using fallback")
    
    # Create dummy managers for fallback
    class DummyManager:
        def get_advertisements(self, status=None, position=None): return []
        def get_active_advertisements(self, position=None): return []
        def get_publicity_packages(self): return []
        def create_advertisement(self, data): return 1
        def update_advertisement_status(self, ad_id, status): return True
        def get_articles(self, status=None, category=None, featured_only=False): return []
        def create_article(self, data): return 1
        def get_media_files(self, file_type=None): return []
        def save_file(self, file, uploaded_by=None, description=None): return None
    
    publicity_manager = DummyManager()
    article_manager = DummyManager()
    media_manager = DummyManager()

app = Flask(__name__)

# Configure for subdirectory deployment
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Force Flask to use the subdirectory in URL generation
@app.before_request
def force_subdirectory():
    """Ensure all URLs are generated with the correct subdirectory"""
    if not request.path.startswith('/lca') and request.endpoint:
        # Only redirect if we're not already in the subdirectory
        if request.environ.get('SCRIPT_NAME') == '/lca':
            pass  # Already handled by WSGI
        else:
            # This shouldn't happen in production, but helps with development
            pass

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
@app.route('/api/advertisements', methods=['GET', 'POST'])
@login_required
def api_advertisements():
    """API endpoint for managing advertisements"""
    if request.method == 'GET':
        status = request.args.get('status')
        position = request.args.get('position')
        advertisements = publicity_manager.get_advertisements(status, position)
        return jsonify(advertisements)
    
    elif request.method == 'POST':
        try:
            # Handle file upload
            media_url = None
            media_filename = None
            
            if 'media_file' in request.files:
                file = request.files['media_file']
                if file and file.filename:
                    media_info = media_manager.save_file(
                        file, 
                        uploaded_by=session.get('user', 'admin'),
                        description=f"Advertisement media for {request.form.get('ad_title', 'Unknown')}"
                    )
                    if media_info:
                        media_url = media_info['url']
                        media_filename = media_info['filename']
            
            data = {
                'client_name': request.form.get('client_name'),
                'client_email': request.form.get('client_email'),
                'client_phone': request.form.get('client_phone'),
                'ad_title': request.form.get('ad_title'),
                'ad_content': request.form.get('ad_content'),
                'media_type': request.form.get('media_type', 'image'),
                'media_url': media_url or request.form.get('media_url'),
                'media_filename': media_filename,
                'start_date': request.form.get('start_date'),
                'end_date': request.form.get('end_date'),
                'position': request.form.get('position', 'sidebar'),
                'status': request.form.get('status', 'pending'),
                'price': float(request.form.get('price', 0))
            }
            
            ad_id = publicity_manager.create_advertisement(data)
            return jsonify({'success': True, 'advertisement_id': ad_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/advertisements/<int:ad_id>/status', methods=['PUT'])
@login_required
def api_update_advertisement_status(ad_id):
    """Update advertisement status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        success = publicity_manager.update_advertisement_status(ad_id, status)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/advertisements/active')
def api_active_advertisements():
    """Get active advertisements for display"""
    position = request.args.get('position')
    advertisements = publicity_manager.get_active_advertisements(position)
    
    # Increment impressions for displayed ads
    for ad in advertisements:
        publicity_manager.increment_impressions(ad['id'])
    
    return jsonify(advertisements)

@app.route('/api/advertisements/<int:ad_id>/click', methods=['POST'])
def api_advertisement_click(ad_id):
    """Track advertisement click"""
    publicity_manager.increment_clicks(ad_id)
    return jsonify({'success': True})

@app.route('/api/packages')
def api_packages():
    """API endpoint for publicity packages"""
    packages = publicity_manager.get_publicity_packages()
    return jsonify(packages)

@app.route('/api/publicity/analytics')
@login_required
def api_publicity_analytics():
    """API endpoint for publicity analytics"""
    try:
        # Get all advertisements for analytics
        all_ads = publicity_manager.get_advertisements()
        active_ads = publicity_manager.get_active_advertisements()
        
        total_impressions = sum(ad.get('impressions', 0) for ad in all_ads)
        total_clicks = sum(ad.get('clicks', 0) for ad in all_ads)
        total_revenue = sum(ad.get('price', 0) for ad in all_ads if ad.get('status') == 'active')
        
        analytics = {
            'total_advertisements': len(all_ads),
            'active_advertisements': len(active_ads),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_revenue': total_revenue,
            'click_through_rate': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        }
        
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Article Management API Endpoints
@app.route('/api/articles', methods=['GET', 'POST'])
@login_required
def api_articles():
    """API endpoint for managing articles"""
    if request.method == 'GET':
        status = request.args.get('status')
        category = request.args.get('category')
        featured_only = request.args.get('featured_only', 'false').lower() == 'true'
        articles = article_manager.get_articles(status, category, featured_only)
        return jsonify(articles)
    
    elif request.method == 'POST':
        try:
            # Handle featured image upload
            featured_image = None
            if 'featured_image' in request.files:
                file = request.files['featured_image']
                if file and file.filename:
                    media_info = media_manager.save_file(
                        file, 
                        uploaded_by=session.get('user', 'admin'),
                        description=f"Featured image for article: {request.form.get('title', 'Unknown')}"
                    )
                    if media_info:
                        featured_image = media_info['url']
            
            data = {
                'title': request.form.get('title'),
                'content': request.form.get('content'),
                'excerpt': request.form.get('excerpt'),
                'author': request.form.get('author', session.get('user', 'Admin')),
                'category': request.form.get('category', 'general'),
                'featured_image': featured_image,
                'status': request.form.get('status', 'draft'),
                'is_featured': request.form.get('is_featured', 'false').lower() == 'true'
            }
            
            article_id = article_manager.create_article(data)
            return jsonify({'success': True, 'article_id': article_id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/articles/<int:article_id>', methods=['GET', 'PUT'])
@login_required
def api_article_detail(article_id):
    """Get or update a specific article"""
    if request.method == 'GET':
        article = article_manager.get_article_by_id(article_id)
        if article:
            return jsonify(article)
        return jsonify({'error': 'Article not found'}), 404
    
    elif request.method == 'PUT':
        try:
            # Handle featured image upload
            featured_image = None
            if 'featured_image' in request.files:
                file = request.files['featured_image']
                if file and file.filename:
                    media_info = media_manager.save_file(
                        file, 
                        uploaded_by=session.get('user', 'admin'),
                        description=f"Featured image for article ID: {article_id}"
                    )
                    if media_info:
                        featured_image = media_info['url']
            
            data = {}
            for field in ['title', 'content', 'excerpt', 'category', 'status']:
                if request.form.get(field):
                    data[field] = request.form.get(field)
            
            if featured_image:
                data['featured_image'] = featured_image
            
            if request.form.get('is_featured'):
                data['is_featured'] = request.form.get('is_featured').lower() == 'true'
            
            success = article_manager.update_article(article_id, data)
            return jsonify({'success': success})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/articles/<int:article_id>/view', methods=['POST'])
def api_increment_article_views(article_id):
    """Increment article view count"""
    article_manager.increment_views(article_id)
    return jsonify({'success': True})

# Media Management API Endpoints
@app.route('/api/media', methods=['GET', 'POST'])
@login_required
def api_media():
    """API endpoint for managing media files"""
    if request.method == 'GET':
        file_type = request.args.get('file_type')
        media_files = media_manager.get_media_files(file_type)
        return jsonify(media_files)
    
    elif request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'success': False, 'message': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'message': 'No file selected'}), 400
            
            description = request.form.get('description', '')
            uploaded_by = session.get('user', 'admin')
            
            media_info = media_manager.save_file(file, uploaded_by, description)
            
            if media_info:
                return jsonify({'success': True, 'media': media_info})
            else:
                return jsonify({'success': False, 'message': 'Failed to save file'}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

# YouTube API Integration for Replay Videos
@app.route('/api/youtube/videos')
def api_youtube_videos():
    """Get YouTube videos for replay section"""
    try:
        # Use the existing YouTube service to get videos
        videos = youtube_service.get_channel_videos(20)
        
        # Format for replay section
        replay_videos = []
        for video in videos:
            replay_videos.append({
                'id': video['id'],
                'title': video['title'],
                'thumbnail': video['thumbnail'],
                'published_at': video['published_at'],
                'category': video['category']
            })
        
        return jsonify(replay_videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Public API endpoints for website integration
@app.route('/api/public/articles')
def api_public_articles():
    """Public API for published articles"""
    category = request.args.get('category')
    featured_only = request.args.get('featured_only', 'false').lower() == 'true'
    articles = article_manager.get_articles('published', category, featured_only)
    return jsonify(articles)

@app.route('/api/public/articles/<int:article_id>')
def api_public_article_detail(article_id):
    """Public API for a specific article"""
    article = article_manager.get_article_by_id(article_id)
    if article and article['status'] == 'published':
        # Increment view count
        article_manager.increment_views(article_id)
        return jsonify(article)
    return jsonify({'error': 'Article not found'}), 404

# Utility endpoints
@app.route('/api/expire-old-advertisements', methods=['POST'])
@login_required
def api_expire_old_advertisements():
    """Expire old advertisements"""
    expired_count = publicity_manager.expire_old_advertisements()
    return jsonify({'success': True, 'expired_count': expired_count})

@app.route('/debug')
def debug_info():
    """Debug endpoint for deployment troubleshooting"""
    import sys
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
            'DEBUG': app.config.get('DEBUG')
        },
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
        
        <h2>System Information</h2>
        <pre>{json.dumps(debug_data, indent=2, default=str)}</pre>
        
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/health">Health Check</a></li>
            <li><a href="/api/videos">Videos API</a></li>
            <li><a href="/login">Admin Login</a></li>
            <li><a href="/debug/youtube">YouTube Debug</a></li>
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