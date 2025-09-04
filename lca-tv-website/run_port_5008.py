#!/usr/bin/env python3
"""
Script pour démarrer LCA TV sur le port 5008
"""

from app_advanced import app

if __name__ == '__main__':
    print("🚀 LCA TV - Démarrage sur port 5008")
    print("=" * 50)
    print("🌐 URLs:")
    print("   • Site: http://localhost:5008/")
    print("   • Login: http://localhost:5008/login")
    print("   • Dashboard: http://localhost:5008/dashboard")
    print("   • Debug: http://localhost:5008/debug")
    print()
    print("🔐 Identifiants:")
    print("   • admin / lcatv2024")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5008)