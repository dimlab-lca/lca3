"""
Production configuration for LCA TV application
"""
import os
from datetime import timedelta

class ProductionConfig:
    """Production configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key-change-this'
    DEBUG = False
    TESTING = False
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///lcatv_production.db'
    
    # YouTube API settings
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY') or ''
    YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID') or ''
    YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID') or ''
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12)
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # Cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

# Configuration dictionary
config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}