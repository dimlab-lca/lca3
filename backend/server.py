#!/usr/bin/env python3
"""
LCA TV Mobile App Backend
FastAPI backend for the LCA TV mobile application
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import jwt
import bcrypt
import pymongo
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import uuid
import re
import json

load_dotenv()

app = FastAPI(title="LCA TV Mobile API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/lcatv")
client = MongoClient(MONGO_URL)
db = client.lcatv

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "lcatv-mobile-secret-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# YouTube API settings
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyDrCcAWodOImhiWs9R8Uo1aIuhzcopAoXE")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UCkquZjmd6ubRQh2W2YpbSLQ")
YOUTUBE_CHANNEL_HANDLE = "@LCATV"

# Security
security = HTTPBearer()

# Pydantic models
class UserRegister(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    password: str
    confirm_password: str
    accept_cgu: bool = True
    newsletter: bool = False

class UserLogin(BaseModel):
    email: str
    password: str
    remember_me: bool = False

class UserResponse(BaseModel):
    id: str
    nom: str
    prenom: str
    email: str
    telephone: str
    points: int = 0
    favorites: List[str] = []
    created_at: datetime
    last_login: Optional[datetime] = None

class VideoResponse(BaseModel):
    id: str
    title: str
    description: str
    thumbnail: str
    published_at: str
    category: str
    view_count: str
    like_count: str
    duration: Optional[str] = None
    channel_title: str = "LCA TV"

class NewsArticle(BaseModel):
    id: str
    title: str
    content: str
    excerpt: str
    image_url: Optional[str] = None
    category: str
    published_at: datetime
    author: str = "LCA TV"

# Utility functions
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.users.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def parse_youtube_duration(duration: str) -> str:
    """Convert YouTube ISO 8601 duration to readable format"""
    if not duration or duration == 'PT0S':
        return '0:00'
    
    # Parse PT4M13S -> 4:13
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return '0:00'
    
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def format_count(count_str: str) -> str:
    """Format view/like counts for display"""
    try:
        count = int(count_str)
        if count >= 1000000:
            return f"{count/1000000:.1f}M"
        elif count >= 1000:
            return f"{count/1000:.1f}K"
        else:
            return str(count)
    except (ValueError, TypeError):
        return "0"

def categorize_video(title: str) -> str:
    """Categorize video based on title keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['journal', 'info', 'actualité', 'news']):
        return 'actualites'
    elif any(word in title_lower for word in ['franc-parler', 'débat', 'discussion']):
        return 'debats'
    elif any(word in title_lower for word in ['questions de femmes', 'femme']):
        return 'femmes'
    elif any(word in title_lower for word in ['sport', 'étalons', 'football', 'match']):
        return 'sport'
    elif any(word in title_lower for word in ['culture', 'tradition', 'masque', 'danse']):
        return 'culture'
    elif any(word in title_lower for word in ['jeunesse', 'avenir', 'jeune']):
        return 'jeunesse'
    elif any(word in title_lower for word in ['burkina', 'faso', 'national']):
        return 'national'
    else:
        return 'general'

def fetch_youtube_videos(max_results: int = 20) -> List[Dict]:
    """Fetch videos from LCA TV YouTube channel"""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        
        # Initialize YouTube API client
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # First, search for the LCA TV channel
        try:
            search_response = youtube.search().list(
                q="@LCATV OR LCA TV Burkina",
                type='channel',
                part='snippet',
                maxResults=5
            ).execute()
            
            channel_id = YOUTUBE_CHANNEL_ID  # Default fallback
            for item in search_response.get('items', []):
                if 'LCA' in item['snippet']['title'] or 'LCATV' in item['snippet']['title']:
                    channel_id = item['snippet']['channelId']
                    print(f"Found LCA TV channel: {item['snippet']['title']} ({channel_id})")
                    break
                    
        except Exception as e:
            print(f"Error searching for channel: {e}")
            channel_id = YOUTUBE_CHANNEL_ID
        
        # Get videos from the channel
        try:
            videos_response = youtube.search().list(
                channelId=channel_id,
                type='video',
                order='date',
                part='snippet',
                maxResults=max_results,
                regionCode='BF'
            ).execute()
            
            videos = []
            video_ids = []
            
            # Collect video IDs for detailed stats
            for item in videos_response.get('items', []):
                video_ids.append(item['id']['videoId'])
            
            # Get detailed video statistics
            stats_by_id = {}
            if video_ids:
                stats_response = youtube.videos().list(
                    id=','.join(video_ids),
                    part='statistics,contentDetails'
                ).execute()
                
                for item in stats_response.get('items', []):
                    stats_by_id[item['id']] = item
            
            # Process videos with real data
            for item in videos_response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                stats_item = stats_by_id.get(video_id, {})
                stats = stats_item.get('statistics', {})
                content_details = stats_item.get('contentDetails', {})
                
                duration = content_details.get('duration', 'PT0S')
                duration_formatted = parse_youtube_duration(duration)
                
                video_data = {
                    'id': video_id,
                    'title': snippet.get('title', 'Titre non disponible'),
                    'description': snippet.get('description', '')[:200] + '...',
                    'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', 
                               snippet.get('thumbnails', {}).get('medium', {}).get('url', 
                               snippet.get('thumbnails', {}).get('default', {}).get('url', ''))),
                    'published_at': snippet.get('publishedAt', ''),
                    'category': categorize_video(snippet.get('title', '')),
                    'channel_title': snippet.get('channelTitle', 'LCA TV'),
                    'view_count': format_count(stats.get('viewCount', '0')),
                    'like_count': format_count(stats.get('likeCount', '0')),
                    'duration': duration_formatted
                }
                videos.append(video_data)
            
            if videos:
                print(f"Successfully fetched {len(videos)} videos from YouTube API")
                return videos
            else:
                print("No videos found, falling back to demo content")
                
        except HttpError as e:
            print(f"YouTube API error: {e}")
            
    except Exception as e:
        print(f"Error initializing YouTube API: {e}")
    
    # Fallback videos for demo/testing
    fallback_videos = [
        {
            'id': 'eSApphrRKWg',
            'title': 'Journal LCA TV - Édition du Soir',
            'description': 'Retrouvez l\'actualité nationale et internationale du Burkina Faso.',
            'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
            'published_at': '2024-12-15T19:00:00Z',
            'category': 'actualites',
            'channel_title': 'LCA TV',
            'view_count': '15420',
            'like_count': '234',
            'duration': '25:30'
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
            'duration': '45:12'
        },
        {
            'id': '8aIAKRe4Spo',
            'title': 'Festival des Masques - Culture Burkinabè',
            'description': 'Découvrez la richesse culturelle du Burkina Faso à travers le festival des masques.',
            'thumbnail': 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
            'published_at': '2024-12-13T18:00:00Z',
            'category': 'culture',
            'channel_title': 'LCA TV',
            'view_count': '12300',
            'like_count': '298',
            'duration': '35:45'
        },
        {
            'id': 'R2EocmxeJ5Q',
            'title': 'Étalons du Burkina - Match Analysis',
            'description': 'Analyse du dernier match des Étalons du Burkina Faso.',
            'thumbnail': 'https://i.ytimg.com/vi/R2EocmxeJ5Q/hqdefault.jpg',
            'published_at': '2024-12-12T21:00:00Z',
            'category': 'sport',
            'channel_title': 'LCA TV',
            'view_count': '25600',
            'like_count': '567',
            'duration': '52:18'
        },
        {
            'id': 'pMlWnB5Wj3Q',
            'title': 'Jeunesse Avenir - Entrepreneuriat',
            'description': 'Émission dédiée aux jeunes entrepreneurs du Burkina Faso.',
            'thumbnail': 'https://i.ytimg.com/vi/pMlWnB5Wj3Q/hqdefault.jpg',
            'published_at': '2024-12-11T17:30:00Z',
            'category': 'jeunesse',
            'channel_title': 'LCA TV',
            'view_count': '6890',
            'like_count': '134',
            'duration': '30:22'
        },
        {
            'id': 'ixQEmhTbvTI',
            'title': 'Questions de Femmes - Édition Spéciale',
            'description': 'Émission spéciale dédiée aux femmes entrepreneures.',
            'thumbnail': 'https://i.ytimg.com/vi/ixQEmhTbvTI/hqdefault.jpg',
            'published_at': '2024-12-10T16:00:00Z',
            'category': 'femmes',
            'channel_title': 'LCA TV',
            'view_count': '9450',
            'like_count': '187',
            'duration': '28:15'
        }
    ]
        return fallback_videos[:max_results]

# Initialize database collections
def init_db():
    """Initialize database with indexes and default data"""
    # Create indexes
    db.users.create_index("email", unique=True)
    db.users.create_index("telephone", unique=True)
    db.news.create_index("published_at")
    db.favorites.create_index([("user_id", 1), ("video_id", 1)], unique=True)
    
    # Insert sample news articles if collection is empty
    if db.news.count_documents({}) == 0:
        sample_news = [
            {
                "_id": str(uuid.uuid4()),
                "title": "Actualités nationales - Flash info du jour",
                "content": "Les dernières nouvelles du Burkina Faso. Point sur la situation politique et économique du pays...",
                "excerpt": "Flash info: Point sur l'actualité nationale et internationale du Burkina Faso.",
                "image_url": "https://via.placeholder.com/400x300?text=Breaking+News+LCA+TV",
                "category": "national",
                "published_at": datetime.utcnow(),
                "author": "LCA TV",
                "view_count": 0
            },
            {
                "_id": str(uuid.uuid4()),
                "title": "Sport - Étalons du Burkina en préparation",
                "content": "L'équipe nationale se prépare pour les prochaines échéances internationales...",
                "excerpt": "Les Étalons du Burkina Faso continuent leur préparation pour les prochains matches.",
                "image_url": "https://via.placeholder.com/400x300?text=Sport+LCA+TV",
                "category": "sport",
                "published_at": datetime.utcnow() - timedelta(hours=2),
                "author": "LCA TV",
                "view_count": 0
            },
            {
                "_id": str(uuid.uuid4()),
                "title": "Culture - Festival de danse traditionnelle",
                "content": "Le festival annuel de danse traditionnelle met en valeur la culture burkinabè...",
                "excerpt": "Découvrez les temps forts du festival de danse traditionnelle organisé à Ouagadougou.",
                "image_url": "https://via.placeholder.com/400x300?text=Culture+LCA+TV",
                "category": "culture",
                "published_at": datetime.utcnow() - timedelta(hours=5),
                "author": "LCA TV",
                "view_count": 0
            }
        ]
        db.news.insert_many(sample_news)

# Initialize database on startup
init_db()

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LCA TV Mobile API",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    """Register new user"""
    # Validate passwords match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Les mots de passe ne correspondent pas"
        )
    
    # Check if user already exists
    if db.users.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    if db.users.find_one({"telephone": user_data.telephone}):
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec ce numéro de téléphone existe déjà"
        )
    
    # Validate phone number (basic validation for Burkina Faso)
    if not re.match(r'^\+226\d{8}$|^\d{8}$', user_data.telephone):
        raise HTTPException(
            status_code=400,
            detail="Format de numéro de téléphone invalide"
        )
    
    # Create user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user_doc = {
        "_id": user_id,
        "nom": user_data.nom,
        "prenom": user_data.prenom,
        "email": user_data.email,
        "telephone": user_data.telephone,
        "password": hashed_password,
        "points": 100,  # Welcome bonus
        "favorites": [],
        "newsletter": user_data.newsletter,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "is_active": True
    }
    
    db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    # Return user data without password
    user_doc.pop("password")
    
    return {
        "user": user_doc,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/api/auth/login")
async def login(login_data: UserLogin):
    """Login user"""
    user = db.users.find_one({"email": login_data.email, "is_active": True})
    
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    
    # Update last login
    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create access token
    token_expires = timedelta(days=30) if login_data.remember_me else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["_id"]}, expires_delta=token_expires)
    
    # Return user data without password
    user.pop("password")
    
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/api/user/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    # Remove password from response
    user_data = current_user.copy()
    user_data.pop("password", None)
    return user_data

@app.get("/api/videos")
async def get_videos(category: Optional[str] = None, limit: int = 20):
    """Get videos from YouTube channel"""
    videos = fetch_youtube_videos(limit)
    
    if category:
        videos = [v for v in videos if v.get('category') == category]
    
    return {"videos": videos}

@app.get("/api/videos/featured")
async def get_featured_videos(limit: int = 6):
    """Get featured videos for home page"""
    videos = fetch_youtube_videos(limit)
    return {"videos": videos}

@app.get("/api/videos/{video_id}")
async def get_video_details(video_id: str):
    """Get details for a specific video"""
    videos = fetch_youtube_videos(50)
    video = next((v for v in videos if v['id'] == video_id), None)
    
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    
    return {"video": video}

@app.post("/api/user/favorites/{video_id}")
async def add_to_favorites(video_id: str, current_user: dict = Depends(get_current_user)):
    """Add video to user favorites"""
    try:
        db.favorites.insert_one({
            "user_id": current_user["_id"],
            "video_id": video_id,
            "added_at": datetime.utcnow()
        })
        
        # Update user favorites list
        db.users.update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"favorites": video_id}}
        )
        
        # Add points for engagement
        db.users.update_one(
            {"_id": current_user["_id"]},
            {"$inc": {"points": 5}}
        )
        
        return {"message": "Vidéo ajoutée aux favoris", "points_earned": 5}
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Vidéo déjà dans les favoris")

@app.delete("/api/user/favorites/{video_id}")
async def remove_from_favorites(video_id: str, current_user: dict = Depends(get_current_user)):
    """Remove video from user favorites"""
    db.favorites.delete_one({
        "user_id": current_user["_id"],
        "video_id": video_id
    })
    
    # Update user favorites list
    db.users.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"favorites": video_id}}
    )
    
    return {"message": "Vidéo retirée des favoris"}

@app.get("/api/user/favorites")
async def get_user_favorites(current_user: dict = Depends(get_current_user)):
    """Get user's favorite videos"""
    favorites = list(db.favorites.find(
        {"user_id": current_user["_id"]},
        {"video_id": 1, "added_at": 1}
    ).sort("added_at", -1))
    
    # Get video details for each favorite
    videos = fetch_youtube_videos(50)
    favorite_videos = []
    
    for fav in favorites:
        video = next((v for v in videos if v['id'] == fav['video_id']), None)
        if video:
            video['added_to_favorites'] = fav['added_at']
            favorite_videos.append(video)
    
    return {"favorites": favorite_videos}

@app.get("/api/news")
async def get_news(category: Optional[str] = None, limit: int = 10):
    """Get news articles"""
    query = {}
    if category:
        query["category"] = category
    
    news = list(db.news.find(query).sort("published_at", -1).limit(limit))
    
    return {"news": news}

@app.get("/api/news/{news_id}")
async def get_news_article(news_id: str):
    """Get specific news article"""
    article = db.news.find_one({"_id": news_id})
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    
    # Increment view count
    db.news.update_one(
        {"_id": news_id},
        {"$inc": {"view_count": 1}}
    )
    
    return {"article": article}

@app.post("/api/user/watch-video/{video_id}")
async def track_video_watch(video_id: str, current_user: dict = Depends(get_current_user)):
    """Track video watch for points and analytics"""
    # Add points for watching
    db.users.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"points": 2}}
    )
    
    # Track viewing history
    db.viewing_history.insert_one({
        "user_id": current_user["_id"],
        "video_id": video_id,
        "watched_at": datetime.utcnow()
    })
    
    return {"message": "Visionnage enregistré", "points_earned": 2}

@app.get("/api/categories")
async def get_categories():
    """Get video categories"""
    categories = [
        {"id": "actualites", "name": "📰 Actualités", "icon": "newspaper"},
        {"id": "debats", "name": "🗣️ Franc-Parler", "icon": "chatbubbles"},
        {"id": "femmes", "name": "🎭 Questions de Femmes", "icon": "woman"},
        {"id": "culture", "name": "🌍 Soleil d'Afrique", "icon": "sunny"},
        {"id": "sport", "name": "⚽ Sports & Étalons", "icon": "football"},
        {"id": "jeunesse", "name": "👥 Jeunesse Avenir", "icon": "people"},
        {"id": "national", "name": "🇧🇫 Burkina Faso", "icon": "flag"},
        {"id": "musique", "name": "🎪 Danse des Masques", "icon": "musical-notes"},
    ]
    return {"categories": categories}

@app.get("/api/live/status")
async def get_live_status():
    """Get live stream status"""
    return {
        "is_live": True,
        "stream_url": "https://www.youtube.com/watch?v=ixQEmhTbvTI",
        "title": "LCA TV - Direct",
        "viewers": 1250,
        "started_at": "2024-01-15T08:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)