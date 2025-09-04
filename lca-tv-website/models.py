#!/usr/bin/env python3
"""
LCA TV - Database Models and Managers
Complete backend functionality for dashboard management
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from typing import List, Dict, Optional, Any

class DatabaseManager:
    """Main database manager for LCA TV"""
    
    def __init__(self, db_path='lcatv.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'editor',
                full_name TEXT,
                phone TEXT,
                avatar_url TEXT,
                is_active BOOLEAN DEFAULT 1,
                last_login DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Publicity subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publicity_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                client_email TEXT NOT NULL,
                client_phone TEXT,
                company_name TEXT,
                package_type TEXT NOT NULL,
                duration_months INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status TEXT DEFAULT 'active',
                payment_status TEXT DEFAULT 'pending',
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Publicity packages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publicity_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price_monthly DECIMAL(10,2) NOT NULL,
                features TEXT, -- JSON string
                max_ads INTEGER DEFAULT 1,
                positions TEXT, -- JSON string
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Advertisements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                media_type TEXT DEFAULT 'image',
                media_url TEXT,
                media_filename TEXT,
                position TEXT DEFAULT 'sidebar',
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status TEXT DEFAULT 'active',
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subscription_id) REFERENCES publicity_subscriptions (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                youtube_id TEXT UNIQUE,
                title TEXT NOT NULL,
                description TEXT,
                thumbnail_url TEXT,
                category TEXT NOT NULL,
                duration TEXT,
                published_at DATETIME,
                view_count INTEGER DEFAULT 0,
                like_count INTEGER DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                is_live BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'published',
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Articles/News table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT UNIQUE,
                content TEXT NOT NULL,
                excerpt TEXT,
                featured_image TEXT,
                category TEXT NOT NULL,
                author_id INTEGER,
                status TEXT DEFAULT 'draft',
                is_featured BOOLEAN DEFAULT 0,
                is_breaking BOOLEAN DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                published_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        ''')
        
        # Media files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                mime_type TEXT,
                uploaded_by INTEGER,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploaded_by) REFERENCES users (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                category TEXT DEFAULT 'general',
                updated_by INTEGER,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (updated_by) REFERENCES users (id)
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT, -- JSON string
                ip_address TEXT,
                user_agent TEXT,
                user_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert default data
        self.insert_default_data()
    
    def insert_default_data(self):
        """Insert default data for the application"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Default admin user
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@lcatv.bf', generate_password_hash('lcatv2024'), 'admin', 'Administrateur LCA TV', 1))
        
        # Default publicity packages
        cursor.execute('SELECT COUNT(*) FROM publicity_packages')
        if cursor.fetchone()[0] == 0:
            packages = [
                ('Package Basic', 'Publicité basique avec 1 annonce', 50000, '["Affichage sidebar", "1 annonce"]', 1, '["sidebar"]'),
                ('Package Standard', 'Publicité standard avec 3 annonces', 120000, '["Affichage sidebar et header", "3 annonces", "Analytics basiques"]', 3, '["sidebar", "header"]'),
                ('Package Premium', 'Publicité premium avec annonces illimitées', 250000, '["Toutes positions", "Annonces illimitées", "Analytics avancées", "Support prioritaire"]', -1, '["sidebar", "header", "banner", "popup"]'),
                ('Package Sponsor', 'Sponsoring complet de programmes', 500000, '["Sponsoring programmes", "Mentions à l\'antenne", "Logo permanent", "Analytics complètes"]', -1, '["all"]')
            ]
            
            for name, desc, price, features, max_ads, positions in packages:
                cursor.execute('''
                    INSERT INTO publicity_packages (name, description, price_monthly, features, max_ads, positions)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, desc, price, features, max_ads, positions))
        
        # Default settings
        settings = [
            ('site_title', 'LCA TV', 'Titre du site', 'general'),
            ('site_description', 'Votre chaîne de référence au Burkina Faso', 'Description du site', 'general'),
            ('contact_email', 'contact@lcatv.bf', 'Email de contact', 'contact'),
            ('contact_phone', '+226 XX XX XX XX', 'Téléphone de contact', 'contact'),
            ('youtube_channel_id', 'UCkquZjmd6ubRQh2W2YpbSLQ', 'ID de la chaîne YouTube', 'youtube'),
            ('youtube_live_video_id', 'ixQEmhTbvTI', 'ID de la vidéo live par défaut', 'youtube'),
            ('analytics_enabled', 'true', 'Activer les analytics', 'analytics'),
            ('maintenance_mode', 'false', 'Mode maintenance', 'system')
        ]
        
        for key, value, desc, category in settings:
            cursor.execute('SELECT COUNT(*) FROM settings WHERE key = ?', (key,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO settings (key, value, description, category)
                    VALUES (?, ?, ?, ?)
                ''', (key, value, desc, category))
        
        conn.commit()
        conn.close()

class UserManager:
    """User management functionality"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_user(self, username: str, email: str, password: str, role: str = 'editor', **kwargs) -> int:
        """Create a new user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name, phone, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, role, 
              kwargs.get('full_name', ''), kwargs.get('phone', ''), 
              kwargs.get('is_active', True)))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                         (datetime.now(), user['id']))
            conn.commit()
            
            user_dict = dict(user)
            del user_dict['password_hash']  # Remove password hash from return
            conn.close()
            return user_dict
        
        conn.close()
        return None
    
    def get_users(self, role: Optional[str] = None, active_only: bool = True) -> List[Dict]:
        """Get all users with optional filtering"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT id, username, email, role, full_name, phone, is_active, last_login, created_at FROM users'
        params = []
        
        conditions = []
        if role:
            conditions.append('role = ?')
            params.append(role)
        if active_only:
            conditions.append('is_active = 1')
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Update user information"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['email', 'role', 'full_name', 'phone', 'is_active']
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f'{field} = ?')
                params.append(value)
        
        if updates:
            updates.append('updated_at = ?')
            params.append(datetime.now())
            params.append(user_id)
            
            query = f'UPDATE users SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """Soft delete user (set inactive)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_active = 0, updated_at = ? WHERE id = ?', 
                      (datetime.now(), user_id))
        conn.commit()
        conn.close()
        return True

class PublicityManager:
    """Publicity and subscription management"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_packages(self) -> List[Dict]:
        """Get all publicity packages"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM publicity_packages WHERE is_active = 1 ORDER BY price_monthly')
        packages = []
        for row in cursor.fetchall():
            package = dict(row)
            package['features'] = json.loads(package['features']) if package['features'] else []
            package['positions'] = json.loads(package['positions']) if package['positions'] else []
            packages.append(package)
        
        conn.close()
        return packages
    
    def create_subscription(self, client_data: Dict, package_id: int, duration_months: int, created_by: int) -> int:
        """Create a new publicity subscription"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get package info
        cursor.execute('SELECT * FROM publicity_packages WHERE id = ?', (package_id,))
        package = cursor.fetchone()
        
        if not package:
            raise ValueError("Package not found")
        
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=duration_months * 30)
        total_price = package['price_monthly'] * duration_months
        
        cursor.execute('''
            INSERT INTO publicity_subscriptions 
            (client_name, client_email, client_phone, company_name, package_type, 
             duration_months, price, start_date, end_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (client_data['name'], client_data['email'], client_data.get('phone', ''),
              client_data.get('company', ''), package['name'], duration_months,
              total_price, start_date, end_date, created_by))
        
        subscription_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return subscription_id
    
    def get_subscriptions(self, status: Optional[str] = None) -> List[Dict]:
        """Get publicity subscriptions"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT s.*, u.username as created_by_username
            FROM publicity_subscriptions s
            LEFT JOIN users u ON s.created_by = u.id
        '''
        params = []
        
        if status:
            query += ' WHERE s.status = ?'
            params.append(status)
        
        query += ' ORDER BY s.created_at DESC'
        
        cursor.execute(query, params)
        subscriptions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return subscriptions
    
    def create_advertisement(self, ad_data: Dict, created_by: int) -> int:
        """Create a new advertisement"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO advertisements 
            (subscription_id, title, content, media_type, media_url, media_filename,
             position, start_date, end_date, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ad_data.get('subscription_id'), ad_data['title'], ad_data.get('content', ''),
              ad_data.get('media_type', 'image'), ad_data.get('media_url', ''),
              ad_data.get('media_filename', ''), ad_data.get('position', 'sidebar'),
              ad_data['start_date'], ad_data['end_date'], ad_data.get('status', 'active'),
              created_by))
        
        ad_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ad_id
    
    def get_advertisements(self, status: Optional[str] = None) -> List[Dict]:
        """Get advertisements"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT a.*, s.client_name, u.username as created_by_username
            FROM advertisements a
            LEFT JOIN publicity_subscriptions s ON a.subscription_id = s.id
            LEFT JOIN users u ON a.created_by = u.id
        '''
        params = []
        
        if status:
            query += ' WHERE a.status = ?'
            params.append(status)
        
        query += ' ORDER BY a.created_at DESC'
        
        cursor.execute(query, params)
        ads = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return ads

class VideoManager:
    """Video management functionality"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_video(self, video_data: Dict, created_by: int) -> int:
        """Add a new video"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos 
            (youtube_id, title, description, thumbnail_url, category, duration,
             published_at, is_featured, is_live, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (video_data.get('youtube_id'), video_data['title'], 
              video_data.get('description', ''), video_data.get('thumbnail_url', ''),
              video_data['category'], video_data.get('duration', ''),
              video_data.get('published_at'), video_data.get('is_featured', False),
              video_data.get('is_live', False), video_data.get('status', 'published'),
              created_by))
        
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return video_id
    
    def get_videos(self, category: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get videos with optional filtering"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT v.*, u.username as created_by_username
            FROM videos v
            LEFT JOIN users u ON v.created_by = u.id
        '''
        params = []
        conditions = []
        
        if category:
            conditions.append('v.category = ?')
            params.append(category)
        if status:
            conditions.append('v.status = ?')
            params.append(status)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY v.created_at DESC'
        
        cursor.execute(query, params)
        videos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return videos

class SettingsManager:
    """Settings management"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        return result['value'] if result else None
    
    def set_setting(self, key: str, value: str, updated_by: int) -> bool:
        """Set a setting value"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_by, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (key, value, updated_by, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_settings(self, category: Optional[str] = None) -> Dict[str, str]:
        """Get all settings as a dictionary"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT key, value FROM settings'
        params = []
        
        if category:
            query += ' WHERE category = ?'
            params.append(category)
        
        cursor.execute(query, params)
        settings = {row['key']: row['value'] for row in cursor.fetchall()}
        conn.close()
        return settings

# Initialize managers
db_manager = DatabaseManager()
user_manager = UserManager(db_manager)
publicity_manager = PublicityManager(db_manager)
video_manager = VideoManager(db_manager)
settings_manager = SettingsManager(db_manager)