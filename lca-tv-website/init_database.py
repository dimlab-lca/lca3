#!/usr/bin/env python3
"""
Script d'initialisation de la base de données LCA TV
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Créer la base de données avec toutes les tables nécessaires"""
    
    db_path = 'lca_tv.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗄️  Création des tables...")
        
        # Table des utilisateurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'editor',
                full_name TEXT,
                is_active BOOLEAN DEFAULT 1,
                last_login DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                company_name TEXT,
                address TEXT,
                notes TEXT,
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des espaces publicitaires
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ad_spaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des publicités
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                client_id INTEGER NOT NULL,
                space_id INTEGER NOT NULL,
                content_type TEXT NOT NULL DEFAULT 'image',
                content_html TEXT,
                image_path TEXT,
                target_url TEXT,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status TEXT DEFAULT 'active',
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (space_id) REFERENCES ad_spaces (id)
            )
        ''')
        
        # Table des vidéos (existante)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                youtube_id TEXT UNIQUE NOT NULL,
                thumbnail_url TEXT,
                duration TEXT,
                published_at DATETIME,
                category TEXT DEFAULT 'general',
                tags TEXT,
                view_count INTEGER DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des paramètres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ Tables créées avec succès")
        
        # Insérer des données de test
        print("\n📊 Insertion des données de test...")
        
        # Clients de test
        test_clients = [
            ("Entreprise ABC", "contact@abc.com", "+225 01 02 03 04 05", "ABC Corporation", "active"),
            ("Boutique XYZ", "info@xyz.com", "+225 06 07 08 09 10", "XYZ Store", "active"),
            ("Restaurant Le Gourmet", "contact@legourmet.com", "+225 11 12 13 14 15", "Le Gourmet SARL", "active")
        ]
        
        for name, email, phone, company, status in test_clients:
            cursor.execute('''
                INSERT OR IGNORE INTO clients (name, email, phone, company_name, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, company, status, datetime.now().isoformat()))
        
        # Espaces publicitaires de test
        test_spaces = [
            ("Header Principal", "header", 728, 90, 50000, "Bannière en haut de page"),
            ("Sidebar Droit", "sidebar", 300, 250, 30000, "Encart publicitaire latéral"),
            ("Footer Principal", "footer", 728, 90, 40000, "Bannière en bas de page"),
            ("Popup Accueil", "popup", 400, 300, 60000, "Popup d'accueil"),
            ("Banner Large", "banner", 970, 250, 70000, "Grande bannière centrale"),
            ("Carré Sidebar", "sidebar", 250, 250, 25000, "Petit carré latéral")
        ]
        
        for name, location, width, height, price, description in test_spaces:
            cursor.execute('''
                INSERT OR IGNORE INTO ad_spaces (name, location, width, height, price, description, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, location, width, height, price, description, True, datetime.now().isoformat()))
        
        # Paramètres par défaut
        default_settings = [
            ("site_title", "LCA TV", "Titre du site"),
            ("site_description", "Votre chaîne TV en ligne", "Description du site"),
            ("contact_email", "contact@lcatv.com", "Email de contact"),
            ("contact_phone", "+225 01 02 03 04 05", "Téléphone de contact")
        ]
        
        for key, value, description in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value, description, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (key, value, description, datetime.now().isoformat()))
        
        conn.commit()
        print("✅ Données de test insérées")
        
        # Afficher les statistiques
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ad_spaces")
        space_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM advertisements")
        ad_count = cursor.fetchone()[0]
        
        print(f"\n📈 Statistiques de la base de données:")
        print(f"   • Clients: {client_count}")
        print(f"   • Espaces publicitaires: {space_count}")
        print(f"   • Publicités: {ad_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        return False

def main():
    print("🚀 Initialisation de la base de données LCA TV")
    print("=" * 50)
    
    if create_database():
        print("\n✅ Base de données initialisée avec succès!")
        print("\n🎯 Prochaines étapes:")
        print("   1. Démarrez l'application Flask")
        print("   2. Connectez-vous au dashboard (admin / lcatv2024)")
        print("   3. Testez la création de publicités")
    else:
        print("\n❌ Échec de l'initialisation de la base de données")

if __name__ == "__main__":
    main()