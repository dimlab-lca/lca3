#!/usr/bin/env python3
"""
Script pour démarrer l'application LCA TV avec la bonne configuration
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_database():
    """Vérifier la base de données"""
    db_path = 'lca_tv.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables importantes
        tables_to_check = ['clients', 'ad_spaces', 'advertisements']
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"✅ Table {table}: {count} enregistrements")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

def main():
    print("🚀 Démarrage de LCA TV - Dashboard Avancé")
    print("=" * 60)
    
    # Vérifier la base de données
    print("📊 Vérification de la base de données...")
    if not check_database():
        print("\n❌ Problème avec la base de données")
        sys.exit(1)
    
    print("\n🔧 Configuration:")
    print(f"   • Base de données: lca_tv.db")
    print(f"   • Port: 5005")
    print(f"   • Mode: Development")
    
    print("\n🔐 Identifiants de connexion:")
    print("   • Utilisateur: admin")
    print("   • Mot de passe: lcatv2024")
    
    print("\n🌐 URLs importantes:")
    print("   • Site public: http://localhost:5005/")
    print("   • Login admin: http://localhost:5005/login")
    print("   • Dashboard: http://localhost:5005/dashboard")
    print("   • API Health: http://localhost:5005/health")
    
    print("\n" + "=" * 60)
    print("Démarrage de l'application...")
    
    # Importer et démarrer l'application
    try:
        from app_advanced import app
        app.run(debug=True, host='0.0.0.0', port=5005)
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur de démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()