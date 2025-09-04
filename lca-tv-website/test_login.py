#!/usr/bin/env python3
"""
Script de test pour diagnostiquer les problèmes de connexion LCA TV
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, ADMIN_USERS

def test_credentials():
    """Test des identifiants administrateur"""
    print("🔍 DIAGNOSTIC DES IDENTIFIANTS LCA TV")
    print("=" * 50)
    
    print("📋 Identifiants configurés :")
    for username, password in ADMIN_USERS.items():
        print(f"   • {username}: {password}")
    
    print("\n🧪 Test de validation :")
    
    # Test avec les identifiants admin
    test_username = "admin"
    test_password = "lcatv2024"
    
    print(f"   • Test avec: {test_username} / {test_password}")
    
    if test_username in ADMIN_USERS:
        stored_password = ADMIN_USERS[test_username]
        print(f"   • Mot de passe stocké: '{stored_password}'")
        print(f"   • Mot de passe testé: '{test_password}'")
        print(f"   • Longueur stockée: {len(stored_password)}")
        print(f"   • Longueur testée: {len(test_password)}")
        print(f"   • Comparaison directe: {stored_password == test_password}")
        print(f"   • Comparaison après strip: {stored_password.strip() == test_password.strip()}")
        
        if stored_password == test_password:
            print("   ✅ SUCCÈS: Les identifiants correspondent")
        else:
            print("   ❌ ÉCHEC: Les identifiants ne correspondent pas")
            print(f"   • Caractères stockés: {[ord(c) for c in stored_password]}")
            print(f"   • Caractères testés: {[ord(c) for c in test_password]}")
    else:
        print(f"   ❌ ÉCHEC: Utilisateur '{test_username}' non trouvé")
    
    print("\n🌐 Test avec l'application Flask :")
    
    with app.test_client() as client:
        # Test GET de la page de login
        response = client.get('/login')
        print(f"   • GET /login: {response.status_code}")
        
        # Test POST avec les bonnes identifiants
        response = client.post('/login', data={
            'username': test_username,
            'password': test_password
        }, follow_redirects=False)
        
        print(f"   • POST /login: {response.status_code}")
        
        if response.status_code == 302:  # Redirection = succès
            print("   ✅ SUCCÈS: Connexion réussie (redirection)")
            print(f"   • Redirection vers: {response.location}")
        else:
            print("   ❌ ÉCHEC: Connexion échouée")
            print(f"   • Contenu de la réponse: {response.data.decode()[:200]}...")

def test_session():
    """Test de la gestion des sessions"""
    print("\n🔐 TEST DES SESSIONS")
    print("=" * 30)
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            print(f"   • Session vide: {dict(sess)}")
        
        # Connexion
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'lcatv2024'
        })
        
        with client.session_transaction() as sess:
            print(f"   • Session après connexion: {dict(sess)}")
        
        # Test d'accès au dashboard
        response = client.get('/dashboard')
        print(f"   • Accès dashboard: {response.status_code}")

if __name__ == '__main__':
    test_credentials()
    test_session()
    
    print("\n" + "=" * 50)
    print("🚀 INSTRUCTIONS DE CONNEXION:")
    print("   1. Allez sur: http://localhost:5001/login")
    print("   2. Utilisateur: admin")
    print("   3. Mot de passe: lcatv2024")
    print("   4. Cliquez sur 'Se connecter'")
    print("=" * 50)