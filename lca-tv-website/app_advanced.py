#!/usr/bin/env python3
"""
LCA TV - Application Avancée avec Système de Gestion Complet
Gestion des utilisateurs, clients, publicités et espaces publicitaires
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash, send_from_directory
import requests
import os
import json
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import threading
import time
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from PIL import Image
import base64

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lcatv-advanced-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'ads'), exist_ok=True)

# Configuration conditionnelle pour APPLICATION_ROOT
if os.environ.get('FLASK_ENV') == 'production':
    app.config['APPLICATION_ROOT'] = '/lca'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
else:
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0')
YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', 'UCkquZjmd6ubRQh2W2YpbSLQ')
YOUTUBE_LIVE_VIDEO_ID = os.environ.get('YOUTUBE_LIVE_VIDEO_ID', 'ixQEmhTbvTI')

# Extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class DatabaseManager:
    """Gestionnaire de base de données avancé"""
    
    def __init__(self, db_path='lca_tv.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialiser la base de données avec toutes les tables"""
        # Ne pas créer de nouvelles tables, utiliser la base existante
        # Juste s'assurer que l'utilisateur admin existe
        self.ensure_admin_user()
    
    def ensure_admin_user(self):
        """S'assurer que l'utilisateur admin existe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur admin existe
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@lcatv.bf', generate_password_hash('lcatv2024'), 'admin', 'Administrateur LCA TV', 1))
            conn.commit()
            print("✅ Utilisateur admin créé")
        
        conn.close()
    
    
# Initialiser la base de données
db_manager = DatabaseManager()

def login_required(f):
    """Decorator pour les routes admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            flash('Vous devez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_activity(action, description=None, user_id=None):
    """Enregistrer une activité dans les logs"""
    if not user_id:
        user_id = session.get('user_id')
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO activity_logs (user_id, action, description, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, action, description, request.remote_addr, request.headers.get('User-Agent')))
    
    conn.commit()
    conn.close()

# ============================================================================
# ROUTES PUBLIQUES DU SITE
# ============================================================================

@app.route('/')
def home():
    """Page d'accueil avec publicités intégrées"""
    try:
        # Charger les publicités actives pour la page d'accueil
        ads = get_active_ads_for_location(['header', 'sidebar', 'popup'])
        
        # Simuler des vidéos (à remplacer par l'API YouTube)
        featured_videos = [
            {
                'id': 'eSApphrRKWg',
                'title': 'Journal LCA TV - Édition du Soir',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'category': 'actualites'
            }
        ] * 6
        
        return render_template('home.html', featured_videos=featured_videos, ads=ads)
    except Exception as e:
        print(f"Home page error: {e}")
        return render_template('home.html', featured_videos=[], ads={})

@app.route('/videos')
def videos():
    """Page des vidéos avec publicités"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar-video', 'banner'])
        videos = []  # À implémenter avec l'API YouTube
        return render_template('videos.html', videos=videos, ads=ads)
    except Exception as e:
        print(f"Videos page error: {e}")
        return render_template('videos.html', videos=[], ads={})

@app.route('/videos/category/<category>')
def videos_by_category(category):
    """Vidéos par catégorie"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar-video', 'banner'])
        # Simuler des vidéos par catégorie
        videos = [
            {
                'id': 'eSApphrRKWg',
                'title': f'Vidéo {category.title()} - LCA TV',
                'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                'category': category,
                'published_at': '2024-12-15T19:00:00Z'
            }
        ] * 3
        return render_template('videos.html', videos=videos, ads=ads, category=category)
    except Exception as e:
        print(f"Category videos error: {e}")
        return render_template('videos.html', videos=[], ads={}, category=category)

@app.route('/live')
def live():
    """Page de diffusion en direct avec publicités"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar'])
        return render_template('live.html', ads=ads)
    except Exception as e:
        print(f"Live page error: {e}")
        return render_template('live.html', ads={})

@app.route('/about')
def about():
    """Page à propos"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar'])
        return render_template('about.html', ads=ads)
    except Exception as e:
        print(f"About page error: {e}")
        return render_template('about.html', ads={})

@app.route('/contact')
def contact():
    """Page de contact"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar'])
        return render_template('contact.html', ads=ads)
    except Exception as e:
        print(f"Contact page error: {e}")
        return render_template('contact.html', ads={})

@app.route('/emissions')
def emissions():
    """Page des émissions"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar-video', 'banner'])
        videos = []  # À implémenter avec l'API YouTube
        return render_template('emissions.html', videos=videos, ads=ads)
    except Exception as e:
        print(f"Emissions page error: {e}")
        return render_template('emissions.html', videos=[], ads={})

@app.route('/publicite')
def publicite():
    """Page publicité"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar'])
        return render_template('publicite.html', ads=ads)
    except Exception as e:
        print(f"Publicite page error: {e}")
        return render_template('publicite.html', ads={})

@app.route('/journal')
def journal():
    """Page journal/actualités"""
    try:
        ads = get_active_ads_for_location(['header', 'sidebar', 'banner'])
        videos = []  # À implémenter avec l'API YouTube
        return render_template('journal.html', videos=videos, ads=ads)
    except Exception as e:
        print(f"Journal page error: {e}")
        return render_template('journal.html', videos=[], ads={})

def get_active_ads_for_location(locations):
    """Récupérer les publicités actives pour des emplacements donnés"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date()
    placeholders = ','.join(['?' for _ in locations])
    
    cursor.execute(f'''
        SELECT a.*, s.location, s.width, s.height, c.name as client_name
        FROM advertisements a
        JOIN ad_spaces s ON a.ad_space_id = s.id
        JOIN clients c ON a.client_id = c.id
        WHERE s.location IN ({placeholders})
        AND a.status = 'active'
        AND a.start_date <= ?
        AND a.end_date >= ?
        ORDER BY a.created_at DESC
    ''', locations + [today, today])
    
    ads_data = cursor.fetchall()
    conn.close()
    
    # Organiser les publicités par emplacement
    ads = {}
    for ad in ads_data:
        location = ad['location']
        if location not in ads:
            ads[location] = []
        
        ad_dict = dict(ad)
        ads[location].append(ad_dict)
        
        # Incrémenter les impressions
        increment_ad_impressions(ad['id'])
    
    return ads

def increment_ad_impressions(ad_id):
    """Incrémenter le compteur d'impressions d'une publicité"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Incrémenter dans la table des statistiques
    cursor.execute('''
        INSERT OR IGNORE INTO ad_stats (advertisement_id, date, impressions, clicks)
        VALUES (?, ?, 0, 0)
    ''', (ad_id, today))
    
    cursor.execute('''
        UPDATE ad_stats SET impressions = impressions + 1
        WHERE advertisement_id = ? AND date = ?
    ''', (ad_id, today))
    
    # Incrémenter dans la table des publicités
    cursor.execute('''
        UPDATE advertisements SET impressions = impressions + 1
        WHERE id = ?
    ''', (ad_id,))
    
    conn.commit()
    conn.close()

@app.route('/ad-click/<int:ad_id>')
def ad_click(ad_id):
    """Gérer les clics sur les publicités"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Récupérer l'URL de destination
    cursor.execute('SELECT target_url FROM advertisements WHERE id = ?', (ad_id,))
    result = cursor.fetchone()
    
    if result and result['target_url']:
        # Incrémenter les clics
        today = datetime.now().date()
        
        cursor.execute('''
            INSERT OR IGNORE INTO ad_stats (advertisement_id, date, impressions, clicks)
            VALUES (?, ?, 0, 0)
        ''', (ad_id, today))
        
        cursor.execute('''
            UPDATE ad_stats SET clicks = clicks + 1
            WHERE advertisement_id = ? AND date = ?
        ''', (ad_id, today))
        
        cursor.execute('''
            UPDATE advertisements SET clicks = clicks + 1
            WHERE id = ?
        ''', (ad_id,))
        
        conn.commit()
        conn.close()
        
        return redirect(result['target_url'])
    
    conn.close()
    return redirect(url_for('home'))

# ============================================================================
# ROUTES ADMINISTRATIVES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion administrateur"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Mettre à jour la dernière connexion
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                         (datetime.now(), user['id']))
            conn.commit()
            
            session['user'] = user['username']
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session.permanent = True
            
            log_activity('login', f'Connexion réussie pour {username}', user['id'])
            
            flash(f'Bienvenue {user["full_name"] or user["username"]} !', 'success')
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            log_activity('login_failed', f'Tentative de connexion échouée pour {username}')
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        
        conn.close()
    
    return render_template('login_simple.html')

@app.route('/logout')
def logout():
    """Déconnexion admin"""
    user = session.get('user', 'Utilisateur')
    log_activity('logout', f'Déconnexion de {user}')
    session.clear()
    flash(f'Au revoir {user} !', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard administrateur avancé"""
    try:
        # Statistiques générales
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Compter les utilisateurs
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        total_users = cursor.fetchone()[0]
        
        # Compter les clients
        cursor.execute('SELECT COUNT(*) FROM clients WHERE status = "active"')
        total_clients = cursor.fetchone()[0]
        
        # Compter les publicités actives
        today = datetime.now().date()
        cursor.execute('''
            SELECT COUNT(*) FROM advertisements 
            WHERE status = "active" AND start_date <= ? AND end_date >= ?
        ''', (today, today))
        total_ads = cursor.fetchone()[0]
        
        # Calculer les revenus mensuels
        cursor.execute('''
            SELECT SUM(price) FROM subscriptions 
            WHERE status = "active" AND start_date <= ? AND end_date >= ?
        ''', (today, today))
        result = cursor.fetchone()
        monthly_revenue = result[0] if result[0] else 0
        
        conn.close()
        
        stats = {
            'total_users': total_users,
            'total_clients': total_clients,
            'total_ads': total_ads,
            'monthly_revenue': monthly_revenue
        }
        
        settings = get_all_settings()
        
        return render_template('dashboard_advanced.html', stats=stats, settings=settings)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard_advanced.html', stats={}, settings={})

# ============================================================================
# API ADMINISTRATIVE - UTILISATEURS
# ============================================================================

@app.route('/api/admin/users', methods=['GET', 'POST'])
@login_required
def api_users():
    """API de gestion des utilisateurs"""
    if request.method == 'POST':
        return create_user()
    else:
        return get_users()

def get_users():
    """Récupérer la liste des utilisateurs"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, role, full_name, phone, is_active, last_login, created_at
        FROM users ORDER BY created_at DESC
    ''')
    
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(users)

def create_user():
    """Créer un nouvel utilisateur"""
    try:
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'editor')
        full_name = data.get('full_name', '')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Champs obligatoires manquants'}), 400
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe déjà
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Utilisateur déjà existant'}), 400
        
        # Créer l'utilisateur
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        ''', (username, email, password_hash, role, full_name))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity('user_created', f'Utilisateur {username} créé', session.get('user_id'))
        
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['PUT', 'DELETE'])
@login_required
def api_user_detail(user_id):
    """API pour modifier ou supprimer un utilisateur"""
    if request.method == 'PUT':
        return update_user(user_id)
    elif request.method == 'DELETE':
        return delete_user(user_id)

def update_user(user_id):
    """Mettre à jour un utilisateur"""
    try:
        data = request.form
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Construire la requête de mise à jour
        updates = []
        params = []
        
        for field in ['email', 'role', 'full_name', 'phone']:
            if field in data:
                updates.append(f'{field} = ?')
                params.append(data[field])
        
        if 'password' in data and data['password']:
            updates.append('password_hash = ?')
            params.append(generate_password_hash(data['password']))
        
        if updates:
            updates.append('updated_at = ?')
            params.append(datetime.now())
            params.append(user_id)
            
            query = f'UPDATE users SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
        
        log_activity('user_updated', f'Utilisateur ID {user_id} modifié', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def delete_user(user_id):
    """Supprimer (désactiver) un utilisateur"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_active = 0, updated_at = ? WHERE id = ?', 
                      (datetime.now(), user_id))
        conn.commit()
        conn.close()
        
        log_activity('user_deleted', f'Utilisateur ID {user_id} supprimé', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API ADMINISTRATIVE - CLIENTS
# ============================================================================

@app.route('/api/admin/clients', methods=['GET', 'POST'])
@login_required
def api_clients():
    """API de gestion des clients"""
    if request.method == 'POST':
        return create_client()
    else:
        return get_clients()

def get_clients():
    """Récupérer la liste des clients"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, 
               COUNT(s.id) as subscriptions_count,
               COALESCE(SUM(s.price), 0) as total_revenue
        FROM clients c
        LEFT JOIN subscriptions s ON c.id = s.client_id AND s.status = 'active'
        WHERE c.status = 'active'
        GROUP BY c.id
        ORDER BY c.created_at DESC
    ''')
    
    clients = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(clients)

def create_client():
    """Créer un nouveau client"""
    try:
        data = request.form
        name = data.get('client_name')
        email = data.get('client_email')
        phone = data.get('client_phone', '')
        company_name = data.get('company_name', '')
        notes = data.get('client_notes', '')
        
        if not name or not email:
            return jsonify({'success': False, 'error': 'Nom et email obligatoires'}), 400
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clients (name, email, phone, company_name, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, company_name, notes, session.get('user_id')))
        
        client_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity('client_created', f'Client {name} créé', session.get('user_id'))
        
        return jsonify({'success': True, 'client_id': client_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/clients/<int:client_id>', methods=['PUT', 'DELETE'])
@login_required
def api_client_detail(client_id):
    """API pour modifier ou supprimer un client"""
    if request.method == 'PUT':
        return update_client(client_id)
    elif request.method == 'DELETE':
        return delete_client(client_id)

def update_client(client_id):
    """Mettre à jour un client"""
    try:
        data = request.form
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE clients 
            SET name = ?, email = ?, phone = ?, company_name = ?, notes = ?, updated_at = ?
            WHERE id = ?
        ''', (data.get('client_name'), data.get('client_email'), data.get('client_phone'),
              data.get('company_name'), data.get('client_notes'), datetime.now(), client_id))
        
        conn.commit()
        conn.close()
        
        log_activity('client_updated', f'Client ID {client_id} modifié', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def delete_client(client_id):
    """Supprimer un client"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE clients SET status = "inactive", updated_at = ? WHERE id = ?', 
                      (datetime.now(), client_id))
        conn.commit()
        conn.close()
        
        log_activity('client_deleted', f'Client ID {client_id} supprimé', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API ADMINISTRATIVE - ESPACES PUBLICITAIRES
# ============================================================================

@app.route('/api/admin/ad-spaces', methods=['GET', 'POST'])
@login_required
def api_ad_spaces():
    """API de gestion des espaces publicitaires"""
    if request.method == 'POST':
        return create_ad_space()
    else:
        return get_ad_spaces()

def get_ad_spaces():
    """Récupérer la liste des espaces publicitaires"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    cursor.execute('''
        SELECT s.*, 
               CASE WHEN a.id IS NOT NULL THEN 1 ELSE 0 END as occupied,
               a.client_name
        FROM ad_spaces s
        LEFT JOIN advertisements a ON s.location = a.position 
            AND a.status = 'active' 
            AND a.start_date <= ? 
            AND a.end_date >= ?
        WHERE s.is_active = 1
        ORDER BY s.location, s.name
    ''', (today, today))
    
    spaces = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(spaces)

def create_ad_space():
    """Créer un nouvel espace publicitaire"""
    try:
        data = request.form
        name = data.get('space_name')
        location = data.get('space_location')
        width = int(data.get('space_width'))
        height = int(data.get('space_height'))
        price = float(data.get('space_price'))
        
        if not all([name, location, width, height, price]):
            return jsonify({'success': False, 'error': 'Tous les champs sont obligatoires'}), 400
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ad_spaces (name, location, width, height, price_monthly)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, location, width, height, price))
        
        space_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_activity('ad_space_created', f'Espace publicitaire {name} créé', session.get('user_id'))
        
        return jsonify({'success': True, 'space_id': space_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/ad-spaces/<int:space_id>', methods=['DELETE'])
@login_required
def api_ad_space_detail(space_id):
    """API pour supprimer un espace publicitaire"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE ad_spaces SET is_active = 0, updated_at = ? WHERE id = ?', 
                      (datetime.now(), space_id))
        conn.commit()
        conn.close()
        
        log_activity('ad_space_deleted', f'Espace publicitaire ID {space_id} supprimé', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API ADMINISTRATIVE - PUBLICITÉS
# ============================================================================

@app.route('/api/admin/advertisements', methods=['GET', 'POST'])
@login_required
def api_advertisements():
    """API de gestion des publicités"""
    if request.method == 'POST':
        return create_advertisement()
    else:
        return get_advertisements()

def get_advertisements():
    """Récupérer la liste des publicités"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, c.name as client_name, s.name as space_name, s.location as position
        FROM advertisements a
        JOIN clients c ON a.client_id = c.id
        JOIN ad_spaces s ON a.ad_space_id = s.id
        ORDER BY a.created_at DESC
    ''')
    
    ads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(ads)

def create_advertisement():
    """Créer une nouvelle publicité - Version corrigée pour la structure existante"""
    try:
        print("=== DEBUG: Création de publicité (version corrigée) ===")
        print(f"Form data: {dict(request.form)}")
        print(f"Files: {list(request.files.keys())}")
        
        data = request.form
        
        # Récupérer les données du formulaire
        ad_title = data.get('ad_title', '').strip()
        client_id_str = data.get('ad_client', '')
        space_id_str = data.get('ad_space', '')
        content_type = data.get('ad_type', 'image')
        target_url = data.get('ad_url', '').strip()
        start_date = data.get('ad_start_date', '').strip()
        end_date = data.get('ad_end_date', '').strip()
        
        print(f"Données reçues: title={ad_title}, client_id={client_id_str}, space_id={space_id_str}")
        
        # Validation des champs obligatoires
        if not ad_title:
            return jsonify({'success': False, 'error': 'Le titre est obligatoire'}), 400
        
        if not client_id_str or not client_id_str.isdigit():
            return jsonify({'success': False, 'error': 'Veuillez sélectionner un client'}), 400
        
        if not space_id_str or not space_id_str.isdigit():
            return jsonify({'success': False, 'error': 'Veuillez sélectionner un espace publicitaire'}), 400
        
        if not start_date or not end_date:
            return jsonify({'success': False, 'error': 'Les dates sont obligatoires'}), 400
        
        try:
            client_id = int(client_id_str)
            space_id = int(space_id_str)
        except ValueError:
            return jsonify({'success': False, 'error': 'IDs invalides'}), 400
        
        # Validation des dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end_date_obj < start_date_obj:
                return jsonify({'success': False, 'error': 'Date de fin invalide'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Format de date invalide'}), 400
        
        # Connexion à la base de données
        conn = sqlite3.connect('lca_tv.db')
        cursor = conn.cursor()
        
        # Récupérer les informations du client
        cursor.execute('SELECT name, email, phone FROM clients WHERE id = ?', (client_id,))
        client_info = cursor.fetchone()
        if not client_info:
            conn.close()
            return jsonify({'success': False, 'error': 'Client introuvable'}), 400
        
        client_name, client_email, client_phone = client_info
        
        # Récupérer les informations de l'espace publicitaire
        cursor.execute('SELECT name, location FROM ad_spaces WHERE id = ?', (space_id,))
        space_info = cursor.fetchone()
        if not space_info:
            conn.close()
            return jsonify({'success': False, 'error': 'Espace publicitaire introuvable'}), 400
        
        space_name, space_location = space_info
        
        # Traiter le contenu selon le type
        ad_content = ""
        media_url = ""
        media_filename = ""
        
        if content_type == 'image':
            if 'ad_image' in request.files:
                file = request.files['ad_image']
                if file and file.filename and allowed_file(file.filename):
                    try:
                        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ads', filename)
                        file.save(file_path)
                        media_url = f"/static/uploads/ads/{filename}"
                        media_filename = filename
                        ad_content = f'<img src="{media_url}" alt="{ad_title}" style="max-width:100%;height:auto;">'
                        print(f"Image sauvegardée: {media_url}")
                    except Exception as e:
                        conn.close()
                        return jsonify({'success': False, 'error': f'Erreur upload: {str(e)}'}), 500
                else:
                    conn.close()
                    return jsonify({'success': False, 'error': 'Image invalide'}), 400
            else:
                conn.close()
                return jsonify({'success': False, 'error': 'Image requise'}), 400
        
        elif content_type == 'html':
            html_content = data.get('ad_html', '').strip()
            if not html_content:
                conn.close()
                return jsonify({'success': False, 'error': 'Code HTML requis'}), 400
            ad_content = html_content
            # Mapper 'html' vers 'banner' pour la base de données
            content_type = 'banner'
        
        # Insérer la publicité avec la structure existante
        try:
            cursor.execute("""
                INSERT INTO advertisements 
                (client_name, client_email, client_phone, ad_title, ad_content, 
                 media_type, media_url, media_filename, start_date, end_date, 
                 position, status, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 0.00)
            """, (client_name, client_email, client_phone, ad_title, ad_content,
                  content_type, media_url, media_filename, start_date, end_date, space_location))
            
            ad_id = cursor.lastrowid
            conn.commit()
            print(f"Publicité créée avec ID: {ad_id}")
            
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            print(f"Erreur SQLite: {e}")
            return jsonify({'success': False, 'error': f'Erreur base de données: {str(e)}'}), 500
        
        conn.close()
        
        return jsonify({'success': True, 'ad_id': ad_id, 'message': 'Publicité créée avec succès'})
        
    except Exception as e:
        print(f"Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Erreur interne: {str(e)}'}), 500

@app.route('/api/admin/advertisements/<int:ad_id>', methods=['DELETE'])
@login_required
def api_advertisement_detail(ad_id):
    """API pour supprimer une publicité"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE advertisements SET status = "inactive", updated_at = ? WHERE id = ?', 
                      (datetime.now(), ad_id))
        conn.commit()
        conn.close()
        
        log_activity('advertisement_deleted', f'Publicité ID {ad_id} supprimée', session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API ADMINISTRATIVE - STATISTIQUES ET AUTRES
# ============================================================================

@app.route('/api/admin/overview')
@login_required
def api_admin_overview():
    """Statistiques générales du dashboard"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Statistiques de base
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM clients WHERE status = "active"')
        total_clients = cursor.fetchone()[0]
        
        today = datetime.now().date()
        cursor.execute('''
            SELECT COUNT(*) FROM advertisements 
            WHERE status = "active" AND start_date <= ? AND end_date >= ?
        ''', (today, today))
        total_ads = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COALESCE(SUM(price), 0) FROM subscriptions 
            WHERE status = "active" AND start_date <= ? AND end_date >= ?
        ''', (today, today))
        monthly_revenue = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_users': total_users,
            'total_clients': total_clients,
            'total_ads': total_ads,
            'monthly_revenue': monthly_revenue
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/recent-activity')
@login_required
def api_admin_recent_activity():
    """Activité récente"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT l.*, u.username
            FROM activity_logs l
            LEFT JOIN users u ON l.user_id = u.id
            ORDER BY l.created_at DESC
            LIMIT 10
        ''')
        
        activities = []
        for row in cursor.fetchall():
            activity = dict(row)
            # Mapper les actions vers des icônes
            icon_map = {
                'login': 'sign-in-alt',
                'logout': 'sign-out-alt',
                'user_created': 'user-plus',
                'client_created': 'handshake',
                'advertisement_created': 'ad',
                'ad_space_created': 'map'
            }
            activity['icon'] = icon_map.get(activity['action'], 'info-circle')
            
            # Calculer le temps écoulé
            created_at = datetime.fromisoformat(activity['created_at'])
            time_diff = datetime.now() - created_at
            
            if time_diff.days > 0:
                activity['time'] = f"{time_diff.days} jour(s)"
            elif time_diff.seconds > 3600:
                activity['time'] = f"{time_diff.seconds // 3600} heure(s)"
            elif time_diff.seconds > 60:
                activity['time'] = f"{time_diff.seconds // 60} min"
            else:
                activity['time'] = "À l'instant"
            
            activities.append(activity)
        
        conn.close()
        return jsonify(activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@login_required
def api_admin_settings():
    """API de gestion des paramètres"""
    if request.method == 'POST':
        return save_settings()
    else:
        return jsonify(get_all_settings())

def get_all_settings():
    """Récupérer tous les paramètres"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT key, value FROM settings')
    settings = {row['key']: row['value'] for row in cursor.fetchall()}
    
    conn.close()
    return settings

def save_settings():
    """Sauvegarder les paramètres"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        for key, value in data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_by, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (key, value, user_id, datetime.now()))
        
        conn.commit()
        conn.close()
        
        log_activity('settings_updated', 'Paramètres mis à jour', user_id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# ROUTES UTILITAIRES
# ============================================================================

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    """Servir les fichiers uploadés"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health_check():
    """Health check avec informations avancées"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0-advanced',
        'database': 'connected',
        'features': {
            'user_management': True,
            'client_management': True,
            'ad_management': True,
            'ad_spaces': True,
            'analytics': True,
            'file_upload': True
        }
    })

@app.route('/debug')
@login_required
def debug_info():
    """Informations de debug pour diagnostiquer les problèmes"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Compter les enregistrements dans chaque table
        tables_info = {}
        tables = ['users', 'clients', 'ad_spaces', 'advertisements', 'subscriptions', 'activity_logs', 'ad_stats', 'settings']
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            tables_info[table] = count
        
        # Récupérer quelques clients pour debug
        cursor.execute('SELECT id, name, email FROM clients WHERE status = "active" LIMIT 5')
        sample_clients = [dict(row) for row in cursor.fetchall()]
        
        # Récupérer quelques espaces pour debug
        cursor.execute('SELECT id, name, location FROM ad_spaces WHERE is_active = 1 LIMIT 5')
        sample_spaces = [dict(row) for row in cursor.fetchall()]
        
        # Récupérer les dernières publicités
        cursor.execute('''
            SELECT a.id, a.title, a.status, c.name as client_name, s.name as space_name
            FROM advertisements a
            JOIN clients c ON a.client_id = c.id
            JOIN ad_spaces s ON a.ad_space_id = s.id
            ORDER BY a.created_at DESC
            LIMIT 5
        ''')
        sample_ads = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'database_status': 'connected',
            'tables_count': tables_info,
            'sample_clients': sample_clients,
            'sample_spaces': sample_spaces,
            'sample_ads': sample_ads,
            'upload_folder': app.config['UPLOAD_FOLDER'],
            'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
            'ads_folder_exists': os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'ads')),
            'session_user': session.get('user'),
            'session_user_id': session.get('user_id')
        })
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': str(e)}), 500

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

# WSGI application pour production
application = app

if __name__ == '__main__':
    print("🚀 Démarrage de LCA TV - Version Avancée")
    print("=" * 60)
    print("🌐 Site Public:")
    print("   • Accueil: http://localhost:5005/")
    print("   • Vidéos: http://localhost:5005/videos")
    print("   • Live: http://localhost:5005/live")
    print()
    print("🔐 Administration Avancée:")
    print("   • Login: http://localhost:5005/login")
    print("   • Dashboard: http://localhost:5005/dashboard")
    print("   • Identifiants: admin / lcatv2024")
    print()
    print("✨ Fonctionnalités:")
    print("   • Gestion des utilisateurs")
    print("   • Portefeuille clients")
    print("   • Espaces publicitaires")
    print("   • Upload de fichiers")
    print("   • Analytics avancées")
    print("   • Logs d'activité")
    print()
    print("📊 Base de Données:")
    print(f"   • Fichier: {db_manager.db_path}")
    print(f"   • Upload: {app.config['UPLOAD_FOLDER']}")
    print()
    print("🔧 API Endpoints:")
    print("   • /api/admin/users")
    print("   • /api/admin/clients")
    print("   • /api/admin/advertisements")
    print("   • /api/admin/ad-spaces")
    print("   • /health")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5005)