#!/usr/bin/env python3
"""
LCA TV - Script de démarrage
"""

import os
import sys

def main():
    print("🚀 Démarrage de LCA TV")
    print("=" * 50)
    
    try:
        from app import app
        
        print("✅ Application chargée avec succès!")
        print()
        print("🌐 SITE PUBLIC:")
        print("   • Accueil: http://localhost:5001/")
        print("   • Vidéos: http://localhost:5001/videos")
        print("   • Live: http://localhost:5001/live")
        print("   • À propos: http://localhost:5001/about")
        print("   • Contact: http://localhost:5001/contact")
        print()
        print("🔐 ADMINISTRATION:")
        print("   • Login: http://localhost:5001/admin/login")
        print("   • Dashboard: http://localhost:5001/admin/dashboard")
        print()
        print("🔑 IDENTIFIANTS ADMIN:")
        print("   • admin / lcatv2024")
        print("   • editor / editor123")
        print("   • musk / tesla123")
        print()
        print("📡 API:")
        print("   • Vidéos: http://localhost:5001/api/videos")
        print("   • Health: http://localhost:5001/health")
        print()
        print("🎯 Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5001)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        print("👋 Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("Vérifiez que tous les fichiers sont présents.")
        sys.exit(1)

if __name__ == '__main__':
    main()