#!/usr/bin/env python3
"""
Script de démarrage pour LCA TV
"""

from app import app

if __name__ == '__main__':
    print("🚀 Démarrage de LCA TV")
    print("=" * 40)
    print("🌐 URLs disponibles:")
    print("   • Site: http://localhost:5002/")
    print("   • Login: http://localhost:5002/login")
    print("   • Dashboard: http://localhost:5002/dashboard")
    print()
    print("🔐 Identifiants Admin:")
    print("   • Utilisateur: admin")
    print("   • Mot de passe: lcatv2024")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5002)