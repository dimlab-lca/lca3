#!/usr/bin/env python3
"""
Script de test pour l'API des espaces publicitaires
"""

import requests
import json

def test_api():
    """Tester l'API des espaces publicitaires"""
    
    # URL de base
    base_url = "http://localhost:5005"
    
    print("🧪 Test de l'API des espaces publicitaires")
    print("=" * 50)
    
    # Test 1: Vérifier que l'application fonctionne
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Application accessible")
            health_data = response.json()
            print(f"   Version: {health_data.get('version', 'N/A')}")
            print(f"   Database: {health_data.get('database', 'N/A')}")
        else:
            print(f"❌ Application non accessible (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        print("   Assurez-vous que l'application est démarrée avec: python app_advanced.py")
        return False
    
    # Test 2: Tester l'API des espaces publicitaires (sans authentification)
    try:
        response = requests.get(f"{base_url}/api/admin/ad-spaces", timeout=5)
        print(f"\n📡 Test API /api/admin/ad-spaces")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("   ⚠️  Authentification requise (normal)")
        elif response.status_code == 200:
            spaces = response.json()
            print(f"   ✅ {len(spaces)} espaces publicitaires trouvés")
            for space in spaces[:3]:  # Afficher les 3 premiers
                print(f"      - {space.get('name', 'N/A')} ({space.get('location', 'N/A')})")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur de requête: {e}")
    
    # Test 3: Tester la page de login
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        print(f"\n🔐 Test page de login")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Page de login accessible")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur de requête: {e}")
    
    # Test 4: Tester la page dashboard (sans authentification)
    try:
        response = requests.get(f"{base_url}/dashboard", timeout=5)
        print(f"\n📊 Test page dashboard")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 302:
            print("   ✅ Redirection vers login (normal)")
        elif response.status_code == 200:
            print("   ⚠️  Dashboard accessible sans authentification")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur de requête: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Instructions pour tester manuellement:")
    print("   1. Démarrez l'application: python app_advanced.py")
    print("   2. Ouvrez: http://localhost:5005/login")
    print("   3. Connectez-vous: admin / lcatv2024")
    print("   4. Allez dans l'onglet 'Publicités'")
    print("   5. Cliquez sur 'Nouvelle Publicité'")
    print("   6. Vérifiez si les espaces s'affichent dans le dropdown")
    
    return True

if __name__ == "__main__":
    test_api()