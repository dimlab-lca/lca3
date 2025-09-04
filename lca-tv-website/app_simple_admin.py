#!/usr/bin/env python3
"""
LCA TV - Simple Admin Dashboard
Simplified version with complete management features
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import os
from datetime import datetime, timedelta
from functools import wraps
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-admin-secret-key')
app.config['DEBUG'] = True

# Simple user credentials
ADMIN_USERS = {
    'admin': 'lcatv2024',
    'musk': 'tesla123',
    'editor': 'editor123'
}

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

# Routes
@app.route('/')
def home():
    """Home page - redirect to dashboard if logged in"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
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

@app.route('/logout')
def logout():
    """Logout user"""
    user = session.get('user', 'Utilisateur')
    session.clear()
    flash(f'Au revoir {user} !', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Complete admin dashboard"""
    # Mock data for demonstration
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

# API Routes for dashboard functionality
@app.route('/api/admin/overview')
@login_required
def api_overview():
    """Get overview statistics"""
    stats = {
        'total_users': 5,
        'total_videos': 150,
        'total_ads': 12,
        'total_articles': 45,
        'active_subscriptions': 8,
        'monthly_revenue': 2500000
    }
    return jsonify(stats)

@app.route('/api/admin/recent-activity')
@login_required
def api_recent_activity():
    """Get recent activity"""
    activities = [
        {'icon': 'user-plus', 'description': 'Nouvel utilisateur créé', 'time': '5 min'},
        {'icon': 'video', 'description': 'Vidéo ajoutée', 'time': '15 min'},
        {'icon': 'ad', 'description': 'Nouvelle souscription', 'time': '1 heure'},
        {'icon': 'edit', 'description': 'Article modifié', 'time': '2 heures'},
        {'icon': 'settings', 'description': 'Paramètres mis à jour', 'time': '3 heures'},
    ]
    return jsonify(activities)

@app.route('/api/admin/users')
@login_required
def api_users():
    """Get all users"""
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

@app.route('/api/admin/subscriptions')
@login_required
def api_subscriptions():
    """Get subscriptions"""
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

@app.route('/api/admin/advertisements')
@login_required
def api_advertisements():
    """Get advertisements"""
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

@app.route('/api/admin/packages')
@login_required
def api_packages():
    """Get publicity packages"""
    packages = [
        {
            'id': 1,
            'name': 'Package Basic',
            'description': 'Publicité basique avec 1 annonce',
            'price_monthly': 50000,
            'features': ['Affichage sidebar', '1 annonce', 'Analytics basiques'],
            'max_ads': 1,
            'positions': ['sidebar']
        },
        {
            'id': 2,
            'name': 'Package Standard',
            'description': 'Publicité standard avec 3 annonces',
            'price_monthly': 120000,
            'features': ['Affichage sidebar et header', '3 annonces', 'Analytics détaillées'],
            'max_ads': 3,
            'positions': ['sidebar', 'header']
        },
        {
            'id': 3,
            'name': 'Package Premium',
            'description': 'Publicité premium avec annonces illimitées',
            'price_monthly': 250000,
            'features': ['Toutes positions', 'Annonces illimitées', 'Analytics avancées', 'Support prioritaire'],
            'max_ads': -1,
            'positions': ['sidebar', 'header', 'banner', 'popup']
        }
    ]
    return jsonify(packages)

@app.route('/api/admin/videos')
@login_required
def api_videos():
    """Get videos"""
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

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@login_required
def api_settings():
    """Get or save settings"""
    if request.method == 'POST':
        # In a real app, save to database
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
    if request.is_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

if __name__ == '__main__':
    print("🚀 Démarrage du Dashboard Admin LCA TV")
    print("=" * 50)
    print("🌐 URL: http://localhost:5001/dashboard")
    print("🔐 Login: admin / lcatv2024")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5001)