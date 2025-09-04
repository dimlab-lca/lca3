#!/usr/bin/env python3
"""
Test direct de l'API des espaces publicitaires
"""

import sqlite3
import json
from datetime import datetime

def test_spaces_api_direct():
    """Tester directement la logique de l'API des espaces"""
    print("🧪 Test direct de l'API des espaces publicitaires")
    print("=" * 60)
    
    try:
        # Connexion directe à la base de données
        conn = sqlite3.connect('lca_tv.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        # Requête similaire à celle de l'API (corrigée)
        cursor.execute('''
            SELECT s.*, 
                   CASE WHEN a.id IS NOT NULL THEN 1 ELSE 0 END as occupied,
                   a.client_name
            FROM ad_spaces s
            LEFT JOIN advertisements a ON s.location = a.position 
                AND a.status = 'active' 
                AND a.start_date <= ? 
                AND a.end_date >= ?
            WHERE s.is_active = 1
            ORDER BY s.location, s.name
        ''', (today, today))
        
        spaces = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        print(f"✅ {len(spaces)} espaces publicitaires trouvés")
        print("\n📋 Liste des espaces:")
        
        for i, space in enumerate(spaces, 1):
            print(f"   {i}. {space['name']}")
            print(f"      • ID: {space['id']}")
            print(f"      • Location: {space['location']}")
            print(f"      • Dimensions: {space['width']}x{space['height']}")
            print(f"      • Prix: {space.get('price', 'N/A')} FCFA/mois")
            print(f"      • Occupé: {'Oui' if space['occupied'] else 'Non'}")
            if space['client_name']:
                print(f"      • Client: {space['client_name']}")
            print()
        
        # Générer le JSON comme l'API
        json_output = json.dumps(spaces, indent=2, default=str)
        print("📄 JSON généré (extrait):")
        print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
        
        return spaces
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_clients_api_direct():
    """Tester directement la logique de l'API des clients"""
    print("\n" + "=" * 60)
    print("🧪 Test direct de l'API des clients")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('lca_tv.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, 
                   COUNT(s.id) as subscriptions_count,
                   COALESCE(SUM(s.price), 0) as total_revenue
            FROM clients c
            LEFT JOIN subscriptions s ON c.id = s.client_id AND s.status = 'active'
            WHERE c.status = 'active'
            GROUP BY c.id
            ORDER BY c.created_at DESC
        ''')
        
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        print(f"✅ {len(clients)} clients trouvés")
        print("\n📋 Liste des clients:")
        
        for i, client in enumerate(clients, 1):
            print(f"   {i}. {client['name']}")
            print(f"      • ID: {client['id']}")
            print(f"      • Email: {client['email']}")
            print(f"      • Téléphone: {client.get('phone', 'N/A')}")
            print(f"      • Entreprise: {client.get('company_name', 'N/A')}")
            print()
        
        return clients
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return []

def create_test_html():
    """Créer un fichier HTML de test pour vérifier le JavaScript"""
    html_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test API Espaces Publicitaires</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .error { color: red; }
        .success { color: green; }
        select, button { padding: 10px; margin: 5px; }
        #results { background: #f5f5f5; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test API Espaces Publicitaires LCA TV</h1>
        
        <div class="section">
            <h2>Test de l'API</h2>
            <button onclick="testSpacesAPI()">Tester /api/admin/ad-spaces</button>
            <button onclick="testClientsAPI()">Tester /api/admin/clients</button>
            <button onclick="testHealthAPI()">Tester /health</button>
        </div>
        
        <div class="section">
            <h2>Simulation du formulaire</h2>
            <label for="client-select">Client:</label>
            <select id="client-select">
                <option value="">Sélectionner un client</option>
            </select>
            <br>
            <label for="space-select">Espace publicitaire:</label>
            <select id="space-select">
                <option value="">Sélectionner un espace</option>
            </select>
            <br>
            <button onclick="loadFormData()">Charger les données</button>
        </div>
        
        <div class="section">
            <h2>Résultats</h2>
            <div id="results">Cliquez sur un bouton pour tester...</div>
        </div>
    </div>

    <script>
        const baseURL = 'http://localhost:5005';
        
        function log(message, type = 'info') {
            const results = document.getElementById('results');
            const timestamp = new Date().toLocaleTimeString();
            const className = type === 'error' ? 'error' : (type === 'success' ? 'success' : '');
            results.innerHTML += `<div class="${className}">[${timestamp}] ${message}</div>`;
        }
        
        function clearResults() {
            document.getElementById('results').innerHTML = '';
        }
        
        async function testHealthAPI() {
            clearResults();
            log('🔍 Test de l\\'API Health...');
            
            try {
                const response = await fetch(`${baseURL}/health`);
                const data = await response.json();
                
                if (response.ok) {
                    log('✅ API Health OK', 'success');
                    log(`Version: ${data.version}`);
                    log(`Database: ${data.database}`);
                    log(`Features: ${JSON.stringify(data.features)}`);
                } else {
                    log(`❌ Erreur Health API: ${response.status}`, 'error');
                }
            } catch (error) {
                log(`❌ Erreur de connexion: ${error.message}`, 'error');
                log('Assurez-vous que l\\'application est démarrée sur le port 5005', 'error');
            }
        }
        
        async function testSpacesAPI() {
            clearResults();
            log('🔍 Test de l\\'API Espaces Publicitaires...');
            
            try {
                const response = await fetch(`${baseURL}/api/admin/ad-spaces`);
                
                if (response.status === 401) {
                    log('⚠️ Authentification requise (normal pour l\\'API admin)', 'error');
                    log('Vous devez être connecté pour accéder à cette API');
                    return;
                }
                
                const data = await response.json();
                
                if (response.ok) {
                    log(`✅ ${data.length} espaces publicitaires trouvés`, 'success');
                    
                    // Remplir le select
                    const select = document.getElementById('space-select');
                    select.innerHTML = '<option value="">Sélectionner un espace</option>';
                    
                    data.forEach(space => {
                        const option = document.createElement('option');
                        option.value = space.id;
                        option.textContent = `${space.name} (${space.width}x${space.height})`;
                        select.appendChild(option);
                        
                        log(`• ${space.name} - ${space.location} (${space.width}x${space.height})`);
                    });
                    
                } else {
                    log(`❌ Erreur API Spaces: ${response.status}`, 'error');
                    log(`Response: ${JSON.stringify(data)}`, 'error');
                }
            } catch (error) {
                log(`❌ Erreur de connexion: ${error.message}`, 'error');
            }
        }
        
        async function testClientsAPI() {
            clearResults();
            log('🔍 Test de l\\'API Clients...');
            
            try {
                const response = await fetch(`${baseURL}/api/admin/clients`);
                
                if (response.status === 401) {
                    log('⚠️ Authentification requise (normal pour l\\'API admin)', 'error');
                    return;
                }
                
                const data = await response.json();
                
                if (response.ok) {
                    log(`✅ ${data.length} clients trouvés`, 'success');
                    
                    // Remplir le select
                    const select = document.getElementById('client-select');
                    select.innerHTML = '<option value="">Sélectionner un client</option>';
                    
                    data.forEach(client => {
                        const option = document.createElement('option');
                        option.value = client.id;
                        option.textContent = client.name;
                        select.appendChild(option);
                        
                        log(`• ${client.name} - ${client.email}`);
                    });
                    
                } else {
                    log(`❌ Erreur API Clients: ${response.status}`, 'error');
                }
            } catch (error) {
                log(`❌ Erreur de connexion: ${error.message}`, 'error');
            }
        }
        
        async function loadFormData() {
            clearResults();
            log('🔄 Chargement des données du formulaire...');
            
            await testClientsAPI();
            await testSpacesAPI();
            
            log('✅ Données du formulaire chargées', 'success');
        }
        
        // Test automatique au chargement
        window.onload = function() {
            log('🚀 Page de test chargée');
            log('Cliquez sur "Tester /health" pour vérifier la connexion');
        };
    </script>
</body>
</html>'''
    
    with open('test_api.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📄 Fichier test_api.html créé")
    print("   Ouvrez ce fichier dans votre navigateur pour tester l'API")

def main():
    print("🔧 Diagnostic complet de l'API LCA TV")
    print("=" * 60)
    
    # Test 1: API des espaces
    spaces = test_spaces_api_direct()
    
    # Test 2: API des clients  
    clients = test_clients_api_direct()
    
    # Test 3: Créer un fichier HTML de test
    print("\n" + "=" * 60)
    print("🌐 Création d'un fichier de test HTML")
    print("=" * 60)
    create_test_html()
    
    print("\n" + "=" * 60)
    print("📋 Résumé du diagnostic")
    print("=" * 60)
    print(f"✅ Espaces publicitaires: {len(spaces)} trouvés")
    print(f"✅ Clients: {len(clients)} trouvés")
    print("✅ Fichier de test HTML créé")
    
    print("\n🎯 Prochaines étapes:")
    print("   1. Démarrez l'application: python app_advanced.py")
    print("   2. Ouvrez test_api.html dans votre navigateur")
    print("   3. Testez les APIs pour identifier le problème")
    print("   4. Ou connectez-vous au dashboard: http://localhost:5005/login")

if __name__ == "__main__":
    main()