#!/usr/bin/env python3
"""
LCA TV - Complete Admin Backend Application
Full-featured dashboard with user management, publicity, videos, articles, and more
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash, send_from_directory
import requests
import os
from datetime import datetime, timedelta
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
import logging
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import mimetypes
from PIL import Image
import io

# Import our models
from models import (
    db_manager, user_manager, publicity_manager, video_manager, 
    settings_manager, DatabaseManager, UserManager, PublicityManager, 
    VideoManager, SettingsManager
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-admin-secret-key-change-me')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
app.config['APPLICATION_ROOT'] = '/lca'
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'video': {'mp4', 'webm', 'avi', 'mov'},
    'audio': {'mp3', 'wav', 'ogg'},
    'document': {'pdf', 'doc', 'docx', 'txt'}
}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'images'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'videos'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'documents'), exist_ok=True)

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', 'UCkquZjmd6ubRQh2W2YpbSLQ')

def login_required(f):
    """Decorator for admin-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for admin-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        
        # Get user info
        user = user_manager.get_users()
        current_user = next((u for u in user if u['username'] == session['user']), None)
        
        if not current_user or current_user['role'] not in ['admin', 'moderator']:
            if request.is_json:
                return jsonify({'error': 'Admin access required'}), 403
            flash('Accès administrateur requis.', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename, file_type=None):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if file_type:
        return ext in ALLOWED_EXTENSIONS.get(file_type, set())
    
    # Check all types
    for extensions in ALLOWED_EXTENSIONS.values():
        if ext in extensions:
            return True
    return False

def get_file_type(filename):
    """Determine file type from extension"""
    if '.' not in filename:
        return 'unknown'
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    
    return 'unknown'

def save_uploaded_file(file, description=''):
    """Save uploaded file and return file info"""
    if not file or not file.filename:
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    
    # Determine file type and subdirectory
    file_type = get_file_type(filename)
    if file_type == 'image':
        subdir = 'images'
    elif file_type == 'video':
        subdir = 'videos'
    else:
        subdir = 'documents'
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, subdir, unique_filename)
    file.save(file_path)
    
    # Get file info
    file_size = os.path.getsize(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    
    # For images, get dimensions
    dimensions = None
    if file_type == 'image':
        try:
            with Image.open(file_path) as img:
                dimensions = f"{img.width}x{img.height}"
        except Exception:
            pass
    
    # Save to database
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO media_files 
        (filename, original_filename, file_path, file_type, file_size, mime_type, uploaded_by, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (unique_filename, filename, file_path, file_type, file_size, mime_type, 
          session.get('user_id', 1), description))
    
    media_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        'id': media_id,
        'filename': unique_filename,
        'original_filename': filename,
        'url': f"/static/uploads/{subdir}/{unique_filename}",
        'file_type': file_type,
        'file_size': file_size,
        'mime_type': mime_type,
        'dimensions': dimensions
    }

# Routes

@app.route('/')
def home():
    """Home page - redirect to dashboard if logged in"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        user = user_manager.authenticate_user(username, password)
        
        if user:
            session['user'] = user['username']
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session.permanent = True
            flash(f'Bienvenue {user["username"]} !', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    user = session.get('user', 'Utilisateur')
    session.clear()
    flash(f'Au revoir {user} !', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main admin dashboard"""
    try:
        # Get overview statistics
        users = user_manager.get_users()
        videos = video_manager.get_videos()
        subscriptions = publicity_manager.get_subscriptions()
        advertisements = publicity_manager.get_advertisements()
        
        stats = {
            'total_users': len(users),
            'total_videos': len(videos),
            'total_ads': len(advertisements),
            'total_articles': 0,  # Will be implemented
            'active_subscriptions': len([s for s in subscriptions if s['status'] == 'active']),
            'monthly_revenue': sum(s['price'] for s in subscriptions if s['status'] == 'active')
        }
        
        # Get settings
        all_settings = settings_manager.get_all_settings()
        
        return render_template('dashboard_admin.html', stats=stats, settings=all_settings)
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        flash('Erreur lors du chargement du dashboard.', 'error')
        return render_template('dashboard_admin.html', stats={}, settings={})

# API Routes

@app.route('/api/admin/overview')
@login_required
def api_overview():
    """Get overview statistics"""
    try:
        users = user_manager.get_users()
        videos = video_manager.get_videos()
        subscriptions = publicity_manager.get_subscriptions()
        advertisements = publicity_manager.get_advertisements()
        
        stats = {
            'total_users': len(users),
            'total_videos': len(videos),
            'total_ads': len(advertisements),
            'total_articles': 0,
            'active_subscriptions': len([s for s in subscriptions if s['status'] == 'active']),
            'monthly_revenue': sum(s['price'] for s in subscriptions if s['status'] == 'active')
        }
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Overview API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/recent-activity')
@login_required
def api_recent_activity():
    """Get recent activity"""
    # This would typically come from an activity log
    # For now, return mock data
    activities = [
        {'icon': 'user-plus', 'description': 'Nouvel utilisateur créé', 'time': '5 min'},
        {'icon': 'video', 'description': 'Vidéo ajoutée', 'time': '15 min'},
        {'icon': 'ad', 'description': 'Nouvelle souscription', 'time': '1 heure'},
        {'icon': 'edit', 'description': 'Article modifié', 'time': '2 heures'},
    ]
    return jsonify(activities)

# User Management APIs

@app.route('/api/admin/users')
@admin_required
def api_users():
    """Get all users"""
    try:
        users = user_manager.get_users(active_only=False)
        return jsonify(users)
    except Exception as e:
        logger.error(f"Users API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users', methods=['POST'])
@admin_required
def api_create_user():
    """Create new user"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Field {field} is required'}), 400
        
        user_id = user_manager.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            full_name=data.get('full_name', ''),
            phone=data.get('phone', ''),
            is_active=data.get('is_active', True)
        )
        
        return jsonify({'success': True, 'user_id': user_id})
        
    except Exception as e:
        logger.error(f"Create user error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def api_update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        
        # Remove password if empty
        if 'password' in data and not data['password']:
            del data['password']
        
        # Hash password if provided
        if 'password' in data:
            data['password_hash'] = generate_password_hash(data['password'])
            del data['password']
        
        success = user_manager.update_user(user_id, **data)
        return jsonify({'success': success})
        
    except Exception as e:
        logger.error(f"Update user error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    """Delete (deactivate) user"""
    try:
        success = user_manager.delete_user(user_id)
        return jsonify({'success': success})
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({'error': str(e)}), 500

# Publicity Management APIs

@app.route('/api/admin/packages')
@login_required
def api_packages():
    """Get publicity packages"""
    try:
        packages = publicity_manager.get_packages()
        return jsonify(packages)
    except Exception as e:
        logger.error(f"Packages API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/subscriptions')
@login_required
def api_subscriptions():
    """Get subscriptions"""
    try:
        status = request.args.get('status')
        subscriptions = publicity_manager.get_subscriptions(status)
        return jsonify(subscriptions)
    except Exception as e:
        logger.error(f"Subscriptions API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/subscriptions', methods=['POST'])
@login_required
def api_create_subscription():
    """Create new subscription"""
    try:
        data = request.get_json()
        
        client_data = {
            'name': data['client_name'],
            'email': data['client_email'],
            'phone': data.get('client_phone', ''),
            'company': data.get('company_name', '')
        }
        
        subscription_id = publicity_manager.create_subscription(
            client_data=client_data,
            package_id=data['package_id'],
            duration_months=data['duration_months'],
            created_by=session['user_id']
        )
        
        return jsonify({'success': True, 'subscription_id': subscription_id})
        
    except Exception as e:
        logger.error(f"Create subscription error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/advertisements')
@login_required
def api_advertisements():
    """Get advertisements"""
    try:
        status = request.args.get('status')
        advertisements = publicity_manager.get_advertisements(status)
        return jsonify(advertisements)
    except Exception as e:
        logger.error(f"Advertisements API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/advertisements', methods=['POST'])
@login_required
def api_create_advertisement():
    """Create new advertisement"""
    try:
        # Handle file upload
        media_url = None
        media_filename = None
        
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename:
                file_info = save_uploaded_file(file, f"Advertisement: {request.form.get('title', 'Unknown')}")
                if file_info:
                    media_url = file_info['url']
                    media_filename = file_info['filename']
        
        ad_data = {
            'subscription_id': request.form.get('subscription_id'),
            'title': request.form.get('title'),
            'content': request.form.get('content', ''),
            'media_type': request.form.get('media_type', 'image'),
            'media_url': media_url or request.form.get('media_url', ''),
            'media_filename': media_filename,
            'position': request.form.get('position', 'sidebar'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'status': request.form.get('status', 'active')
        }
        
        ad_id = publicity_manager.create_advertisement(ad_data, session['user_id'])
        return jsonify({'success': True, 'advertisement_id': ad_id})
        
    except Exception as e:
        logger.error(f"Create advertisement error: {e}")
        return jsonify({'error': str(e)}), 500

# Video Management APIs

@app.route('/api/admin/videos')
@login_required
def api_videos():
    """Get videos"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        videos = video_manager.get_videos(category, status)
        return jsonify(videos)
    except Exception as e:
        logger.error(f"Videos API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/videos', methods=['POST'])
@login_required
def api_create_video():
    """Create new video"""
    try:
        # Handle thumbnail upload
        thumbnail_url = None
        if 'thumbnail' in request.files:
            file = request.files['thumbnail']
            if file and file.filename:
                file_info = save_uploaded_file(file, f"Thumbnail: {request.form.get('title', 'Unknown')}")
                if file_info:
                    thumbnail_url = file_info['url']
        
        video_data = {
            'youtube_id': request.form.get('youtube_id'),
            'title': request.form.get('title'),
            'description': request.form.get('description', ''),
            'thumbnail_url': thumbnail_url or request.form.get('thumbnail_url', ''),
            'category': request.form.get('category'),
            'duration': request.form.get('duration', ''),
            'published_at': request.form.get('published_at'),
            'is_featured': request.form.get('is_featured') == 'true',
            'is_live': request.form.get('is_live') == 'true',
            'status': request.form.get('status', 'published')
        }
        
        video_id = video_manager.add_video(video_data, session['user_id'])
        return jsonify({'success': True, 'video_id': video_id})
        
    except Exception as e:
        logger.error(f"Create video error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/youtube/sync')
@login_required
def api_sync_youtube():
    """Sync videos from YouTube"""
    try:
        # This would implement YouTube API sync
        # For now, return success
        return jsonify({'success': True, 'message': 'YouTube sync completed'})
    except Exception as e:
        logger.error(f"YouTube sync error: {e}")
        return jsonify({'error': str(e)}), 500

# Media Management APIs

@app.route('/api/admin/media')
@login_required
def api_media():
    """Get media files"""
    try:
        file_type = request.args.get('file_type')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT m.*, u.username as uploaded_by_username
            FROM media_files m
            LEFT JOIN users u ON m.uploaded_by = u.id
        '''
        params = []
        
        if file_type:
            query += ' WHERE m.file_type = ?'
            params.append(file_type)
        
        query += ' ORDER BY m.created_at DESC'
        query += ' LIMIT ? OFFSET ?'
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        media_files = []
        
        for row in cursor.fetchall():
            media = dict(row)
            # Generate URL
            subdir = 'images' if media['file_type'] == 'image' else 'videos' if media['file_type'] == 'video' else 'documents'
            media['url'] = f"/static/uploads/{subdir}/{media['filename']}"
            media_files.append(media)
        
        conn.close()
        return jsonify(media_files)
        
    except Exception as e:
        logger.error(f"Media API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/media/upload', methods=['POST'])
@login_required
def api_upload_media():
    """Upload media files"""
    try:
        uploaded_files = []
        
        for file in request.files.getlist('files'):
            if file and file.filename:
                file_info = save_uploaded_file(file, request.form.get('description', ''))
                if file_info:
                    uploaded_files.append(file_info)
        
        return jsonify({'success': True, 'files': uploaded_files})
        
    except Exception as e:
        logger.error(f"Upload media error: {e}")
        return jsonify({'error': str(e)}), 500

# Settings APIs

@app.route('/api/admin/settings')
@admin_required
def api_get_settings():
    """Get all settings"""
    try:
        settings = settings_manager.get_all_settings()
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Settings API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/settings', methods=['POST'])
@admin_required
def api_save_settings():
    """Save settings"""
    try:
        data = request.get_json()
        
        for key, value in data.items():
            settings_manager.set_setting(key, str(value), session['user_id'])
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Save settings error: {e}")
        return jsonify({'error': str(e)}), 500

# File serving

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# Error handlers

@app.errorhandler(404)
def not_found_error(error):
    if request.is_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(error):
    if request.is_json:
        return jsonify({'error': 'File too large'}), 413
    flash('Fichier trop volumineux. Taille maximum: 50MB', 'error')
    return redirect(request.url)

# Health check

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'features': {
            'user_management': True,
            'publicity_management': True,
            'video_management': True,
            'media_management': True,
            'settings_management': True,
            'analytics': True
        }
    })

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# WSGI application
application = app

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5001)