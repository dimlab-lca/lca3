#!/usr/bin/env python3
"""
Local Development Server for LCA TV
Run this file to start the application locally without subdirectory configuration
"""

import os
import sys
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
from datetime import datetime, timedelta
import json
from functools import wraps
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Create Flask app for local development
app = Flask(__name__)

# Local development configuration
app.config['SECRET_KEY'] = 'local-dev-secret-key-lcatv'
app.config['DEBUG'] = True
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['APPLICATION_ROOT'] = '/'  # No subdirectory for local dev

# YouTube API configuration (you can add your own API key here)
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')  # Add your API key
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', '')
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', 'ixQEmhTbvTI')

print("🚀 Starting LCA TV Local Development Server...")
print(f"📺 YouTube API Key: {'✅ Set' if YOUTUBE_API_KEY else '❌ Not Set (using mock data)'}")

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

cache = CacheManager()

class YouTubeService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()
        self.session.timeout = 10
    
    def get_channel_videos(self, max_results=12):
        """Get videos with fallback to mock data for local development"""
        if not self.api_key:
            print("📺 Using mock video data (no YouTube API key)")
            return self.get_mock_videos()
        
        cache_key = f"channel_videos_{max_results}"
        cached_videos = cache.get(cache_key, ttl_seconds=300)
        if cached_videos:
            return cached_videos
        
        try:
            # Try to get real videos if API key is available
            videos = self.get_mock_videos()  # For now, always use mock data
            cache.set(cache_key, videos)
            return videos
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return self.get_mock_videos()
    
    def get_mock_videos(self):
        """Mock video data for local development"""
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
            },
            {
                'id': 'abc123def456',
                'title': 'Météo Burkina - Prévisions de la Semaine',
                'description': 'Les prévisions météorologiques pour tout le Burkina Faso.',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'published_at': '2024-12-10T08:00:00Z',
                'category': 'actualites',
                'channel_title': 'LCA TV',
                'view_count': '4200',
                'like_count': '89',
                'comment_count': '12'
            }
        ]

youtube_service = YouTubeService(YOUTUBE_API_KEY)

# Mock managers for local development
class MockManager:
    def get_subscriptions(self, status=None): return []
    def get_subscription_packages(self): return []
    def get_analytics_summary(self): return {'active_subscriptions': 0, 'active_campaigns': 0, 'monthly_revenue': 0, 'monthly_impressions': 0}
    def get_news(self, active_only=True, breaking_only=False): return []
    def get_breaking_news(self): return []

publicity_manager = MockManager()
news_manager = MockManager()

# Simple user credentials
ADMIN_USERS = {
    'admin': 'lcatv2024',
    'musk': 'tesla123',
    'editor': 'editor123'
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
    """Home page with featured videos"""
    videos = youtube_service.get_channel_videos(12)
    featured_videos = videos[:6]
    return render_template('home.html', featured_videos=featured_videos)

@app.route('/videos')
def videos():
    """All videos page"""
    all_videos = youtube_service.get_channel_videos(30)
    return render_template('videos.html', videos=all_videos)

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos filtered by category"""
    all_videos = youtube_service.get_channel_videos(30)
    filtered_videos = [v for v in all_videos if v['category'] == category]
    return render_template('videos.html', videos=filtered_videos, category=category)

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
    all_videos = youtube_service.get_channel_videos(20)
    return render_template('emissions.html', videos=all_videos)

@app.route('/publicite')
def publicite():
    """Publicite page"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Journal/News broadcasting page"""
    all_videos = youtube_service.get_channel_videos(20)
    news_videos = [v for v in all_videos if v['category'] == 'actualites']
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
    """Admin dashboard"""
    videos = youtube_service.get_channel_videos(20)
    stats = {
        'total_videos': len(videos),
        'total_playlists': 0,
        'categories': {},
        'recent_videos': videos[:5] if videos else []
    }
    
    for video in videos:
        category = video.get('category', 'other')
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
    
    return render_template('dashboard_enhanced.html', 
                         videos=videos, 
                         playlists=[], 
                         live_info=None,
                         stats=stats,
                         subscriptions=[],
                         packages=[],
                         publicity_stats={'active_subscriptions': 0, 'active_campaigns': 0, 'monthly_revenue': 0, 'monthly_impressions': 0},
                         all_news=[],
                         recent_news=[],
                         breaking_news=[])

# API endpoints
@app.route('/api/videos')
def api_videos():
    """API endpoint for videos"""
    videos = youtube_service.get_channel_videos(30)
    return jsonify(videos)

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API endpoint for videos by category"""
    all_videos = youtube_service.get_channel_videos(30)
    filtered_videos = [v for v in all_videos if v['category'] == category]
    return jsonify(filtered_videos)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': 'local_development',
        'youtube_api': bool(YOUTUBE_API_KEY)
    })

@app.route('/debug')
def debug_info():
    """Debug endpoint for local development"""
    import sys
    
    debug_data = {
        'environment': 'Local Development',
        'python_version': sys.version,
        'flask_debug': app.config.get('DEBUG'),
        'application_root': app.config.get('APPLICATION_ROOT'),
        'youtube_api_available': bool(YOUTUBE_API_KEY),
        'cache_stats': {
            'cached_items': len(cache.cache),
            'cache_keys': list(cache.cache.keys())
        }
    }
    
    return f"""
    <html>
    <head><title>LCA TV Local Debug</title></head>
    <body>
        <h1>🚀 LCA TV Local Development</h1>
        <h2>✅ Status: Running</h2>
        
        <h3>🔗 Navigation Links</h3>
        <ul>
            <li><a href="{url_for('home')}">🏠 Home</a></li>
            <li><a href="{url_for('journal')}">📰 Journal</a></li>
            <li><a href="{url_for('live')}">📺 Live</a></li>
            <li><a href="{url_for('videos')}">🎬 Videos</a></li>
            <li><a href="{url_for('emissions')}">📻 Émissions</a></li>
            <li><a href="{url_for('about')}">ℹ️ About</a></li>
            <li><a href="{url_for('login')}">🔐 Login</a></li>
        </ul>
        
        <h3>🔧 Debug Information</h3>
        <pre>{json.dumps(debug_data, indent=2, default=str)}</pre>
        
        <h3>👤 Test Accounts</h3>
        <ul>
            <li><strong>admin</strong> / lcatv2024</li>
            <li><strong>musk</strong> / tesla123</li>
            <li><strong>editor</strong> / editor123</li>
        </ul>
    </body>
    </html>
    """

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return f"""
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body>
        <h1>🚫 Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="{url_for('home')}">← Back to Home</a>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return f"""
    <html>
    <head><title>500 - Server Error</title></head>
    <body>
        <h1>⚠️ Server Error</h1>
        <p>Something went wrong on our end.</p>
        <a href="{url_for('home')}">← Back to Home</a>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎯 LCA TV Local Development Server")
    print("="*60)
    print(f"🌐 URL: http://localhost:5000")
    print(f"🔧 Debug Mode: {app.config['DEBUG']}")
    print(f"📺 YouTube API: {'✅ Configured' if YOUTUBE_API_KEY else '❌ Using Mock Data'}")
    print("\n📋 Available Routes:")
    print("   • http://localhost:5000/ (Home)")
    print("   • http://localhost:5000/journal (Journal)")
    print("   • http://localhost:5000/live (Live TV)")
    print("   • http://localhost:5000/videos (All Videos)")
    print("   • http://localhost:5000/login (Admin Login)")
    print("   • http://localhost:5000/debug (Debug Info)")
    print("\n👤 Test Login Credentials:")
    print("   • admin / lcatv2024")
    print("   • musk / tesla123")
    print("   • editor / editor123")
    print("\n🚀 Starting server...")
    print("="*60)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")