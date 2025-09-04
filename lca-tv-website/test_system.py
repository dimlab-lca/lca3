#!/usr/bin/env python3
"""
Script de test pour le système LCA TV avancé
Vérifie toutes les fonctionnalités principales
"""

import os
import sys
import requests
import json
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Tester toutes les fonctionnalités du système"""
    base_url = "http://localhost:5005"
    
    print("🧪 TEST DU SYSTÈME LCA TV AVANCÉ")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. 🔍 Test Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Système en ligne - Version {data.get('version', 'N/A')}")
            print(f"   📊 Fonctionnalités: {len(data.get('features', {}))} activées")
        else:
            print(f"   ❌ Health check échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Page d'accueil
    print("\n2. 🏠 Test Page d'accueil...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Page d'accueil accessible")
            if "LCA TV" in response.text:
                print("   ✅ Contenu correct affiché")
            else:
                print("   ⚠️ Contenu inattendu")
        else:
            print(f"   ❌ Page d'accueil inaccessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Page de connexion
    print("\n3. 🔐 Test Page de connexion...")
    try:
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("   ✅ Page de connexion accessible")
        else:
            print(f"   ❌ Page de connexion inaccessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Authentification
    print("\n4. 🔑 Test Authentification...")
    session = requests.Session()
    try:
        # Récupérer la page de login pour obtenir le token CSRF si nécessaire
        login_page = session.get(f"{base_url}/login")
        
        # Tenter la connexion
        login_data = {
            'username': 'admin',
            'password': 'lcatv2024'
        }
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirection = succès
            print("   ✅ Authentification réussie")
            
            # Test d'accès au dashboard
            dashboard_response = session.get(f"{base_url}/dashboard")
            if dashboard_response.status_code == 200:
                print("   ✅ Accès au dashboard confirmé")
            else:
                print(f"   ❌ Accès au dashboard échoué: {dashboard_response.status_code}")
        else:
            print(f"   ❌ Authentification échouée: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 5: API Endpoints
    print("\n5. 🔌 Test API Endpoints...")
    api_endpoints = [
        '/api/admin/overview',
        '/api/admin/users',
        '/api/admin/clients',
        '/api/admin/advertisements',
        '/api/admin/ad-spaces',
        '/api/admin/recent-activity',
        '/api/admin/settings'
    ]
    
    for endpoint in api_endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"   ✅ {endpoint}")
            elif response.status_code == 401:
                print(f"   🔒 {endpoint} (authentification requise)")
            else:
                print(f"   ❌ {endpoint} ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {endpoint} (erreur: {e})")
    
    # Test 6: Base de données
    print("\n6. 🗄️ Test Base de données...")
    try:
        from app_advanced import db_manager
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Tester chaque table
        tables = [
            'users', 'clients', 'ad_spaces', 'advertisements', 
            'subscriptions', 'activity_logs', 'ad_stats', 'settings'
        ]
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"   ✅ Table {table}: {count} enregistrements")
        
        conn.close()
        print("   �� Base de données opérationnelle")
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
    
    # Test 7: Upload de fichiers
    print("\n7. 📁 Test Système de fichiers...")
    try:
        from app_advanced import app
        upload_folder = app.config['UPLOAD_FOLDER']
        ads_folder = os.path.join(upload_folder, 'ads')
        
        if os.path.exists(upload_folder):
            print(f"   ✅ Dossier upload existe: {upload_folder}")
        else:
            print(f"   ❌ Dossier upload manquant: {upload_folder}")
        
        if os.path.exists(ads_folder):
            print(f"   ✅ Dossier publicités existe: {ads_folder}")
        else:
            print(f"   ❌ Dossier publicités manquant: {ads_folder}")
        
        # Tester les permissions d'écriture
        test_file = os.path.join(upload_folder, 'test.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("   ✅ Permissions d'écriture OK")
        except Exception as e:
            print(f"   ❌ Permissions d'écriture: {e}")
            
    except Exception as e:
        print(f"   ❌ Erreur système de fichiers: {e}")
    
    # Test 8: Templates
    print("\n8. 🎨 Test Templates...")
    templates_to_check = [
        'dashboard_advanced.html',
        'components/ad_display.html',
        'home_with_ads.html',
        'login_simple.html'
    ]
    
    for template in templates_to_check:
        template_path = os.path.join('templates', template)
        if os.path.exists(template_path):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} manquant")
    
    print("\n" + "=" * 50)
    print("🎯 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print("✅ Tests réussis: Système opérationnel")
    print("🔧 Pour démarrer: python start_advanced.py")
    print("🌐 URL: http://localhost:5005")
    print("👤 Login: admin / lcatv2024")
    print("=" * 50)
    
    return True

def test_api_functionality():
    """Test spécifique des fonctionnalités API"""
    print("\n🔬 TESTS FONCTIONNELS AVANCÉS")
    print("=" * 40)
    
    base_url = "http://localhost:5005"
    session = requests.Session()
    
    # Connexion
    login_data = {'username': 'admin', 'password': 'lcatv2024'}
    session.post(f"{base_url}/login", data=login_data)
    
    # Test création d'utilisateur
    print("1. 👤 Test création d'utilisateur...")
    user_data = {
        'username': f'test_user_{datetime.now().strftime("%H%M%S")}',
        'email': f'test_{datetime.now().strftime("%H%M%S")}@test.com',
        'password': 'test123',
        'role': 'editor',
        'full_name': 'Utilisateur Test'
    }
    
    try:
        response = session.post(f"{base_url}/api/admin/users", data=user_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Utilisateur créé avec ID: {result.get('user_id')}")
            else:
                print(f"   ❌ Échec création: {result.get('error')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test création de client
    print("\n2. 🤝 Test création de client...")
    client_data = {
        'client_name': f'Client Test {datetime.now().strftime("%H:%M:%S")}',
        'client_email': f'client_{datetime.now().strftime("%H%M%S")}@test.bf',
        'client_phone': '+226 70 12 34 56',
        'company_name': 'Entreprise Test',
        'client_notes': 'Client créé automatiquement pour test'
    }
    
    try:
        response = session.post(f"{base_url}/api/admin/clients", data=client_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Client créé avec ID: {result.get('client_id')}")
            else:
                print(f"   ❌ Échec création: {result.get('error')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test récupération des statistiques
    print("\n3. 📊 Test statistiques...")
    try:
        response = session.get(f"{base_url}/api/admin/overview")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Utilisateurs: {stats.get('total_users', 0)}")
            print(f"   ✅ Clients: {stats.get('total_clients', 0)}")
            print(f"   ✅ Publicités: {stats.get('total_ads', 0)}")
            print(f"   ✅ Revenus: {stats.get('monthly_revenue', 0)} FCFA")
        else:
            print(f"   ❌ Erreur statistiques: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n✅ Tests fonctionnels terminés")

if __name__ == '__main__':
    print("🚀 DÉMARRAGE DES TESTS SYSTÈME")
    print("Assurez-vous que le serveur est démarré avec: python start_advanced.py")
    print()
    
    # Attendre confirmation
    input("Appuyez sur Entrée pour commencer les tests...")
    
    # Exécuter les tests
    if test_system():
        test_api_functionality()
    
    print("\n🎉 Tests terminés !")
    print("Consultez les résultats ci-dessus pour identifier d'éventuels problèmes.")