#!/usr/bin/env python3
"""
LCA TV Admin Dashboard Launcher
Run this script to start the complete admin backend
"""

import os
import sys
from app_admin import app

def main():
    print("🚀 Démarrage du Dashboard Admin LCA TV")
    print("=" * 50)
    print()
    
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    
    print("📋 Configuration:")
    print(f"   • Mode: Développement")
    print(f"   • Debug: Activé")
    print(f"   • Port: 5001")
    print(f"   • Host: 0.0.0.0")
    print()
    
    print("🔐 Identifiants par défaut:")
    print(f"   • Utilisateur: admin")
    print(f"   • Mot de passe: lcatv2024")
    print()
    
    print("🌐 URLs d'accès:")
    print(f"   • Dashboard: http://localhost:5001/dashboard")
    print(f"   • Login: http://localhost:5001/login")
    print(f"   • API: http://localhost:5001/api/admin/")
    print()
    
    print("✨ Fonctionnalités disponibles:")
    print(f"   ✅ Gestion des utilisateurs")
    print(f"   ✅ Gestion de la publicité")
    print(f"   ✅ Gestion des vidéos")
    print(f"   ✅ Gestion des articles")
    print(f"   ✅ Gestion des médias")
    print(f"   ✅ Paramètres du site")
    print(f"   ✅ Analytics et statistiques")
    print()
    
    print("🔧 Base de données:")
    print(f"   • SQLite: lcatv.db")
    print(f"   • Tables: Initialisées automatiquement")
    print(f"   • Données par défaut: Chargées")
    print()
    
    try:
        print("🎯 Démarrage du serveur...")
        print("   Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5001,
            use_reloader=True,
            use_debugger=True
        )
        
    except KeyboardInterrupt:
        print("\n")
        print("🛑 Arrêt du serveur...")
        print("👋 Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()