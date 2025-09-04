#!/usr/bin/python3
"""
Simplified LCA TV application for N0C hosting deployment
This version has minimal dependencies and better error handling
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import os
import sys
from datetime import datetime
import json

# Create Flask app
app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-secret-key-change-in-production')
app.config['DEBUG'] = False

# Simple admin credentials
ADMIN_USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'lcatv2024'),
    'editor': os.environ.get('EDITOR_PASSWORD', 'editor123')
}

# Mock data for testing
MOCK_VIDEOS = [
    {
        'id': 'video1',
        'title': 'Journal LCA TV - Édition du Soir',
        'description': 'Retrouvez l\'actualité nationale et internationale avec notre équipe de journalistes.',
        'thumbnail': 'https://via.placeholder.com/320x180/28a745/ffffff?text=LCA+TV+Journal',
        'published_at': '2024-12-15T19:00:00Z',
        'category': 'actualites',
        'channel_title': 'LCA TV',
        'view_count': '15420',
        'like_count': '234',
        'comment_count': '45'
    },
    {
        'id': 'video2',
        'title': 'Franc-Parler - Débat sur l\'Économie Burkinabè',
        'description': 'Un débat enrichissant sur les enjeux économiques du Burkina Faso.',
        'thumbnail': 'https://via.placeholder.com/320x180/4472c4/ffffff?text=Franc-Parler',
        'published_at': '2024-12-14T20:30:00Z',
        'category': 'debats',
        'channel_title': 'LCA TV',
        'view_count': '8750',
        'like_count': '156',
        'comment_count': '67'
    },
    {
        'id': 'video3',
        'title': 'Festival des Masques de Dédougou - Reportage Culture',
        'description': 'Découvrez la richesse culturelle du Burkina Faso.',
        'thumbnail': 'https://via.placeholder.com/320x180/e74c3c/ffffff?text=Culture',
        'published_at': '2024-12-13T18:00:00Z',
        'category': 'culture',
        'channel_title': 'LCA TV',
        'view_count': '12300',
        'like_count': '298',
        'comment_count': '89'
    },
    {
        'id': 'video4',
        'title': 'Étalons du Burkina - Qualification CAN 2024',
        'description': 'Suivez les Étalons dans leur match crucial de qualification.',
        'thumbnail': 'https://via.placeholder.com/320x180/f39c12/ffffff?text=Sport',
        'published_at': '2024-12-12T21:00:00Z',
        'category': 'sport',
        'channel_title': 'LCA TV',
        'view_count': '25600',
        'like_count': '567',
        'comment_count': '123'
    }
]

def login_required(f):
    """Simple login decorator"""
    from functools import wraps
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
        featured_videos = MOCK_VIDEOS[:3]
        return render_template('home_simple.html', featured_videos=featured_videos)
    except Exception as e:
        return f"Erreur page d'accueil: {str(e)}", 500

@app.route('/videos')
def videos():
    """Videos page"""
    try:
        return render_template('videos_simple.html', videos=MOCK_VIDEOS)
    except Exception as e:
        return f"Erreur page vidéos: {str(e)}", 500

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Videos by category"""
    try:
        filtered_videos = [v for v in MOCK_VIDEOS if v['category'] == category]
        return render_template('videos_simple.html', videos=filtered_videos, category=category)
    except Exception as e:
        return f"Erreur catégorie {category}: {str(e)}", 500

@app.route('/live')
def live():
    """Live page"""
    try:
        return render_template('live_simple.html')
    except Exception as e:
        return f"Erreur page live: {str(e)}", 500

@app.route('/about')
def about():
    """About page"""
    return """
    <h1>À propos de LCA TV</h1>
    <p>LCA TV est votre chaîne de télévision burkinabè de référence.</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/contact')
def contact():
    """Contact page"""
    return """
    <h1>Contact LCA TV</h1>
    <p>Contactez-nous à: contact@lcatv.bf</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['user'] = username
            flash(f'Bienvenue {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects', 'error')
    
    return '''
    <form method="post">
        <h2>Connexion LCA TV</h2>
        <p><input type="text" name="username" placeholder="Nom d'utilisateur" required></p>
        <p><input type="password" name="password" placeholder="Mot de passe" required></p>
        <p><input type="submit" value="Se connecter"></p>
    </form>
    <a href="/">Retour à l'accueil</a>
    '''

@app.route('/logout')
def logout():
    """Logout"""
    session.pop('user', None)
    flash('Déconnecté avec succès', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Simple dashboard"""
    try:
        stats = {
            'total_videos': len(MOCK_VIDEOS),
            'categories': {}
        }
        
        for video in MOCK_VIDEOS:
            category = video['category']
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        return f"""
        <h1>Dashboard LCA TV</h1>
        <p>Bienvenue {session.get('user', 'Admin')}!</p>
        <h2>Statistiques</h2>
        <p>Total vidéos: {stats['total_videos']}</p>
        <p>Catégories: {stats['categories']}</p>
        <p><a href="/logout">Déconnexion</a></p>
        <p><a href="/">Retour à l'accueil</a></p>
        """
    except Exception as e:
        return f"Erreur dashboard: {str(e)}", 500

# API endpoints
@app.route('/api/videos')
def api_videos():
    """Videos API"""
    try:
        return jsonify(MOCK_VIDEOS)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/live-status')
def api_live_status():
    """Live status API"""
    try:
        return jsonify({
            'is_live': False,
            'title': 'LCA TV - Hors ligne',
            'viewers': 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'app_directory': os.path.dirname(__file__)
    })

@app.route('/debug')
def debug():
    """Debug information"""
    return f"""
    <h1>Debug Information</h1>
    <p><strong>Python Version:</strong> {sys.version}</p>
    <p><strong>Python Path:</strong> {sys.path}</p>
    <p><strong>Current Directory:</strong> {os.getcwd()}</p>
    <p><strong>App Directory:</strong> {os.path.dirname(__file__)}</p>
    <p><strong>Environment Variables:</strong></p>
    <ul>
    {''.join([f'<li>{k}: {v}</li>' for k, v in os.environ.items() if 'SECRET' not in k])}
    </ul>
    <p><a href="/">Retour à l'accueil</a></p>
    """

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return """
    <h1>Page non trouvée (404)</h1>
    <p>La page que vous cherchez n'existe pas.</p>
    <a href="/">Retour à l'accueil</a>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return f"""
    <h1>Erreur serveur (500)</h1>
    <p>Une erreur interne s'est produite: {str(error)}</p>
    <a href="/">Retour à l'accueil</a>
    """, 500

# WSGI application
application = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)