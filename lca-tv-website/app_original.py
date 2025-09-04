from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import requests
import os
from datetime import datetime
import json
from config import config
from functools import wraps


app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

YOUTUBE_API_KEY = app.config.get('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = app.config.get('YOUTUBE_CHANNEL_ID')
YOUTUBE_LIVE_VIDEO_ID = app.config.get('YOUTUBE_LIVE_VIDEO_ID')

class YouTubeService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_channel_id_by_handle(self, handle):
        """Get channel ID from @LCATV handle"""
        try:
            # Try to get channel by handle using the new API method
            search_url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': 'LCATV',
                'type': 'channel',
                'key': self.api_key,
                'maxResults': 50  # Increase to find the right channel
            }
            
            response = requests.get(search_url, params=params)
            print(f"Search API response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Found {len(data.get('items', []))} channels in search")
                
                if data.get('items'):
                    # Print all found channels for debugging
                    for i, item in enumerate(data['items']):
                        channel_title = item['snippet']['title']
                        channel_id = item['snippet']['channelId']
                        print(f"Channel {i+1}: {channel_title} - {channel_id}")
                        
                        # Look for exact LCATV match
                        if channel_title.upper() == 'LCATV' or 'LCATV' in channel_title.upper():
                            print(f"✅ Found exact LCATV channel: {channel_title} - {channel_id}")
                            return channel_id
                    
                    # If no exact match, look for close matches
                    for item in data['items']:
                        channel_title = item['snippet']['title'].lower()
                        if 'lca' in channel_title and ('tv' in channel_title or 'television' in channel_title):
                            print(f"✅ Found close match: {item['snippet']['title']} - {item['snippet']['channelId']}")
                            return item['snippet']['channelId']
                    
                    # Last resort: return first result and let user verify
                    first_channel = data['items'][0]
                    print(f"⚠️ Using first result: {first_channel['snippet']['title']} - {first_channel['snippet']['channelId']}")
                    return first_channel['snippet']['channelId']
            else:
                print(f"Search API error: {response.text}")
            
            return None
        except Exception as e:
            print(f"Error getting channel ID: {e}")
            return None
    
    def get_channel_videos(self, max_results=50):
        """Get latest videos from your LCATV playlists"""
        try:
            # Use your specific playlist IDs directly
            videos = self.get_videos_from_playlists()
            
            # If no videos found (quota exceeded or other error), use mock data
            if not videos:
                print("No videos found from API, using mock data with real video IDs")
                return self.get_mock_videos()
            
            return videos
            
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return self.get_mock_videos()
    
    def get_videos_from_playlists(self):
        """Get videos from your specific playlists"""
        playlist_ids = [
            'PLk5BkfzB9R2y_GaeShMuKrdQAR-eGn86S',
            'PLk5BkfzB9R2xqyMzMrGs4Z0uMxZMW2EQe', 
            'PLk5BkfzB9R2xJVGaQXQW0Q8yxwFPEY3k5',
            'PLk5BkfzB9R2wMXgDqP_apnJc7iq8p2ML2',
            'PLk5BkfzB9R2z1LpmM6ZNkSjhJeUCcjcH6'
        ]
        
        all_videos = []
        
        for playlist_id in playlist_ids:
            try:
                playlist_url = f"{self.base_url}/playlistItems"
                params = {
                    'part': 'snippet',
                    'playlistId': playlist_id,
                    'maxResults': 50,
                    'key': self.api_key
                }
                
                response = requests.get(playlist_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    print(f"Found {len(data.get('items', []))} videos in playlist {playlist_id}")
                    
                    for item in data.get('items', []):
                        # Get the best available thumbnail
                        thumbnails = item['snippet']['thumbnails']
                        thumbnail_url = ''
                        if 'maxres' in thumbnails:
                            thumbnail_url = thumbnails['maxres']['url']
                        elif 'high' in thumbnails:
                            thumbnail_url = thumbnails['high']['url']
                        elif 'medium' in thumbnails:
                            thumbnail_url = thumbnails['medium']['url']
                        elif 'default' in thumbnails:
                            thumbnail_url = thumbnails['default']['url']
                        
                        video = {
                            'id': item['snippet']['resourceId']['videoId'],
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'thumbnail': thumbnail_url,
                            'published_at': item['snippet']['publishedAt'],
                            'category': self.categorize_video(item['snippet']['title']),
                            'channel_title': item['snippet']['channelTitle'],
                            'playlist_id': playlist_id
                        }
                        all_videos.append(video)
                else:
                    print(f"Error fetching playlist {playlist_id}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error processing playlist {playlist_id}: {e}")
        
        # Remove duplicates based on video ID
        seen_ids = set()
        unique_videos = []
        for video in all_videos:
            if video['id'] not in seen_ids:
                seen_ids.add(video['id'])
                unique_videos.append(video)
        
        # Get additional video details in batches
        if unique_videos:
            video_ids = [v['id'] for v in unique_videos]
            unique_videos = self.enrich_video_data(unique_videos, video_ids)
        
        print(f"Total unique videos found: {len(unique_videos)}")
        return unique_videos
    
    def enrich_video_data(self, videos, video_ids):
        """Enrich video data with additional details"""
        try:
            # Process in batches of 50 (YouTube API limit)
            batch_size = 50
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                videos_url = f"{self.base_url}/videos"
                videos_params = {
                    'part': 'statistics,contentDetails',
                    'id': ','.join(batch_ids),
                    'key': self.api_key
                }
                
                videos_response = requests.get(videos_url, params=videos_params)
                if videos_response.status_code == 200:
                    videos_data = videos_response.json()
                    
                    # Create a lookup dict for video stats
                    stats_lookup = {}
                    for video_detail in videos_data.get('items', []):
                        stats_lookup[video_detail['id']] = {
                            'view_count': video_detail.get('statistics', {}).get('viewCount', '0'),
                            'like_count': video_detail.get('statistics', {}).get('likeCount', '0'),
                            'comment_count': video_detail.get('statistics', {}).get('commentCount', '0'),
                            'duration': video_detail.get('contentDetails', {}).get('duration', 'PT0S')
                        }
                    
                    # Enrich videos with stats
                    for video in videos[i:i + batch_size]:
                        if video['id'] in stats_lookup:
                            video.update(stats_lookup[video['id']])
            
            return videos
        except Exception as e:
            print(f"Error enriching video data: {e}")
            return videos
    
    def get_live_stream_info(self):
        """Get live stream information"""
        try:
            if not YOUTUBE_LIVE_VIDEO_ID:
                return None
                
            video_url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,liveStreamingDetails',
                'id': YOUTUBE_LIVE_VIDEO_ID,
                'key': self.api_key
            }
            
            response = requests.get(video_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    video = data['items'][0]
                    return {
                        'id': video['id'],
                        'title': video['snippet']['title'],
                        'description': video['snippet']['description'],
                        'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'is_live': video['snippet'].get('liveBroadcastContent') == 'live',
                        'scheduled_start': video.get('liveStreamingDetails', {}).get('scheduledStartTime'),
                        'actual_start': video.get('liveStreamingDetails', {}).get('actualStartTime'),
                        'concurrent_viewers': video.get('liveStreamingDetails', {}).get('concurrentViewers')
                    }
            return None
        except Exception as e:
            print(f"Error fetching live stream info: {e}")
            return None
    
    def get_playlists(self):
        """Get channel playlists"""
        try:
            # First get the channel ID if we don't have it
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
                'maxResults': 50,
                'key': self.api_key
            }
            
            response = requests.get(playlists_url, params=params)
            if response.status_code == 200:
                data = response.json()
                playlists = []
                
                for item in data.get('items', []):
                    playlist = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'video_count': item['contentDetails']['itemCount'],
                        'published_at': item['snippet']['publishedAt']
                    }
                    playlists.append(playlist)
                
                return playlists
            return []
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []
    
    def categorize_video(self, title):
        """Categorize video based on title keywords"""
        title_lower = title.lower()
        
        categories = {
            'actualites': [
                'journal', 'info', 'actualité', 'actualites', 'news', 'flash', 
                'information', 'bulletin', 'édition', 'reportage', 'enquête',
                'breaking', 'urgent', 'dernière heure', 'direct', 'live'
            ],
            'debats': [
                'débat', 'débats', 'discussion', 'franc-parler', 'analyse', 
                'table ronde', 'forum', 'conférence', 'panel', 'échange',
                'dialogue', 'controverse', 'polémique', 'opinion', 'point de vue'
            ],
            'culture': [
                'culture', 'culturel', 'tradition', 'traditionnel', 'art', 'arts',
                'patrimoine', 'festival', 'musique', 'danse', 'théâtre',
                'littérature', 'poésie', 'conte', 'folklore', 'artisan',
                'artisanat', 'masque', 'cérémonie', 'rituel', 'fête'
            ],
            'sport': [
                'sport', 'sports', 'football', 'étalons', 'compétition', 
                'match', 'championnat', 'coupe', 'tournoi', 'olympique',
                'athlétisme', 'basketball', 'volleyball', 'handball',
                'cyclisme', 'boxe', 'lutte', 'can', 'fifa', 'caf'
            ],
            'jeunesse': [
                'jeunesse', 'jeunes', 'jeune', 'éducation', 'école', 'étudiant',
                'université', 'formation', 'apprentissage', 'bourse',
                'orientation', 'insertion', 'emploi jeune', 'startup',
                'innovation', 'entrepreneuriat', 'talent', 'avenir'
            ],
            'economie': [
                'économie', 'économique', 'business', 'développement', 'marché',
                'commerce', 'industrie', 'agriculture', 'élevage', 'pêche',
                'mines', 'or', 'coton', 'export', 'import', 'investissement',
                'banque', 'finance', 'bourse', 'entreprise', 'pme', 'emploi'
            ],
            'politique': [
                'politique', 'gouvernement', 'ministre', 'président', 'élection',
                'assemblée', 'député', 'sénat', 'conseil', 'maire', 'préfet',
                'parti', 'campagne', 'vote', 'scrutin', 'démocratie',
                'opposition', 'majorité', 'coalition', 'réforme', 'loi'
            ],
            'sante': [
                'santé', 'médecine', 'médical', 'hôpital', 'clinique', 'docteur',
                'prévention', 'vaccination', 'épidémie', 'maladie', 'traitement',
                'médicament', 'soins', 'urgence', 'chirurgie', 'consultation',
                'dispensaire', 'csps', 'chu', 'paludisme', 'vih', 'sida'
            ],
            'societe': [
                'société', 'social', 'communauté', 'famille', 'femme', 'enfant',
                'solidarité', 'entraide', 'association', 'ong', 'bénévolat',
                'citoyenneté', 'civisme', 'droits', 'justice', 'paix',
                'réconciliation', 'cohésion', 'vivre ensemble', 'inclusion'
            ]
        }
        
        # Score each category based on keyword matches
        category_scores = {}
        for category, keywords in categories.items():
            score = 0
            for keyword in keywords:
                if keyword in title_lower:
                    # Give higher score for exact matches and longer keywords
                    score += len(keyword) * title_lower.count(keyword)
            category_scores[category] = score
        
        # Return the category with the highest score
        if category_scores and max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        
        return 'actualites'  # Default category
    
    def get_mock_videos(self):
        """Fallback videos using your real video IDs with rich content"""
        return [
            {
                'id': 'eSApphrRKWg',
                'title': 'Journal LCA TV - Édition du Soir',
                'description': 'Retrouvez l\'actualité nationale et internationale avec notre équipe de journalistes. Au sommaire : politique, économie, sport et culture burkinabè.',
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
                'description': 'Un débat enrichissant sur les enjeux économiques du Burkina Faso avec nos experts invités. Comment relancer l\'économie post-pandémie ?',
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
                'description': 'Découvrez la richesse culturelle du Burkina Faso à travers ce magnifique festival traditionnel. Un voyage au cœur de nos traditions.',
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
                'description': 'Suivez les Étalons dans leur match crucial de qualification pour la Coupe d\'Afrique des Nations. Analyse et réactions.',
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
                'description': 'Une émission dédiée aux jeunes entrepreneurs burkinabè et leurs projets innovants pour l\'avenir du pays.',
                'thumbnail': 'https://i.ytimg.com/vi/pMlWnB5Wj3Q/hqdefault.jpg',
                'published_at': '2024-12-11T17:30:00Z',
                'category': 'jeunesse',
                'channel_title': 'LCA TV',
                'view_count': '6890',
                'like_count': '134',
                'comment_count': '34'
            },
            {
                'id': 'eSApphrRKWg',
                'title': 'Santé Publique - Campagne de Vaccination',
                'description': 'Reportage sur la campagne nationale de vaccination au Burkina Faso. Informations et conseils de nos experts santé.',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'published_at': '2024-12-10T15:00:00Z',
                'category': 'sante',
                'channel_title': 'LCA TV',
                'view_count': '9450',
                'like_count': '187',
                'comment_count': '56'
            },
            {
                'id': 'xJatmbxIaIM',
                'title': 'Développement Rural - Agriculture Burkinabè',
                'description': 'Focus sur les innovations agricoles et le développement rural au Burkina Faso. Rencontre avec les acteurs du secteur.',
                'thumbnail': 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
                'published_at': '2024-12-09T14:00:00Z',
                'category': 'economie',
                'channel_title': 'LCA TV',
                'view_count': '7320',
                'like_count': '145',
                'comment_count': '28'
            },
            {
                'id': '8aIAKRe4Spo',
                'title': 'Assemblée Nationale - Session Ordinaire',
                'description': 'Suivez les débats de l\'Assemblée Nationale sur les questions importantes du pays. Démocratie en action.',
                'thumbnail': 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
                'published_at': '2024-12-08T13:00:00Z',
                'category': 'politique',
                'channel_title': 'LCA TV',
                'view_count': '11200',
                'like_count': '203',
                'comment_count': '78'
            },
            {
                'id': 'R2EocmxeJ5Q',
                'title': 'Société - Solidarité Communautaire à Ouagadougou',
                'description': 'Reportage sur les initiatives de solidarité dans la capitale burkinabè. L\'entraide au cœur de notre société.',
                'thumbnail': 'https://i.ytimg.com/vi/R2EocmxeJ5Q/hqdefault.jpg',
                'published_at': '2024-12-07T12:00:00Z',
                'category': 'societe',
                'channel_title': 'LCA TV',
                'view_count': '5670',
                'like_count': '98',
                'comment_count': '23'
            },
            {
                'id': 'pMlWnB5Wj3Q',
                'title': 'Flash Info - Dernières Nouvelles',
                'description': 'Les dernières informations en bref. Restez connectés avec l\'actualité burkinabè et internationale.',
                'thumbnail': 'https://i.ytimg.com/vi/pMlWnB5Wj3Q/hqdefault.jpg',
                'published_at': '2024-12-06T11:00:00Z',
                'category': 'actualites',
                'channel_title': 'LCA TV',
                'view_count': '18900',
                'like_count': '345',
                'comment_count': '67'
            },
            {
                'id': 'eSApphrRKWg',
                'title': 'Musique Burkinabè - Artistes Émergents',
                'description': 'Découvrez les nouveaux talents de la musique burkinabè. Une émission dédiée à la promotion de nos artistes.',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'published_at': '2024-12-05T16:00:00Z',
                'category': 'culture',
                'channel_title': 'LCA TV',
                'view_count': '13450',
                'like_count': '267',
                'comment_count': '45'
            },
            {
                'id': 'xJatmbxIaIM',
                'title': 'Sport Local - Championnat National',
                'description': 'Suivez le championnat national de football burkinabè. Résultats, analyses et interviews des joueurs.',
                'thumbnail': 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
                'published_at': '2024-12-04T19:30:00Z',
                'category': 'sport',
                'channel_title': 'LCA TV',
                'view_count': '22100',
                'like_count': '456',
                'comment_count': '89'
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
    """Home page with featured videos"""
    videos = youtube_service.get_channel_videos(12)
    featured_videos = videos[:6]  # First 6 videos as featured
    return render_template('home.html', featured_videos=featured_videos)

@app.route('/videos')
def videos():
    """All videos page"""
    all_videos = youtube_service.get_channel_videos(50)
    return render_template('videos.html', videos=all_videos)

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos filtered by category"""
    all_videos = youtube_service.get_channel_videos(50)
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
    all_videos = youtube_service.get_channel_videos(50)
    return render_template('emissions.html', videos=all_videos)

@app.route('/publicite')
def publicite():
    """Publicite page"""
    return render_template('publicite.html')

@app.route('/journal')
def journal():
    """Journal/News broadcasting page"""
    all_videos = youtube_service.get_channel_videos(50)
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
    try:
        # Get all data for dashboard
        videos = youtube_service.get_channel_videos(50)
        playlists = youtube_service.get_playlists()
        live_info = youtube_service.get_live_stream_info()
        
        # Calculate statistics
        stats = {
            'total_videos': len(videos),
            'total_playlists': len(playlists),
            'categories': {},
            'recent_videos': videos[:10] if videos else []
        }
        
        # Count videos by category
        for video in videos:
            category = video.get('category', 'other')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        return render_template('dashboard.html', 
                             videos=videos, 
                             playlists=playlists, 
                             live_info=live_info,
                             stats=stats)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', 
                             videos=[], 
                             playlists=[], 
                             live_info=None,
                             stats={'total_videos': 0, 'total_playlists': 0, 'categories': {}, 'recent_videos': []})

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
    """API endpoint for dashboard statistics"""
    try:
        videos = youtube_service.get_channel_videos(50)
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
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos')
def api_videos():
    """API endpoint for videos"""
    videos = youtube_service.get_channel_videos(50)
    return jsonify(videos)

@app.route('/api/videos/category/<category>')
def api_videos_by_category(category):
    """API endpoint for videos by category"""
    all_videos = youtube_service.get_channel_videos(50)
    filtered_videos = [v for v in all_videos if v['category'] == category]
    return jsonify(filtered_videos)

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
            'search_results': response.json() if response.status_code == 200 else response.text,
            'channel_search': None,
            'videos_test': None
        }
        
        if response.status_code == 200:
            # Try to find LCATV channel
            channel_id = youtube_service.get_channel_id_by_handle('@LCATV')
            debug_info['channel_search'] = {
                'found_channel_id': channel_id,
                'method': 'search'
            }
            
            if channel_id:
                # Try to get some videos
                videos = youtube_service.get_channel_videos(5)
                debug_info['videos_test'] = {
                    'video_count': len(videos),
                    'sample_videos': videos[:3] if videos else []
                }
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e), 'api_key_provided': bool(YOUTUBE_API_KEY)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)