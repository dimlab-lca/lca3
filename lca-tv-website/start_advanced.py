#!/usr/bin/env python3
"""
Script de démarrage pour LCA TV - Version Avancée
Avec système complet de gestion des publicités
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_advanced import app, db_manager

def create_sample_data():
    """Créer des données d'exemple pour tester le système"""
    print("🔧 Création des données d'exemple...")
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Vérifier si des clients existent déjà
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        # Créer des clients d'exemple
        sample_clients = [
            ('Entreprise ABC', 'contact@abc.bf', '+226 70 12 34 56', 'ABC Industries', 'Client premium depuis 2023'),
            ('Société XYZ', 'info@xyz.bf', '+226 71 23 45 67', 'XYZ Services', 'Nouveau client - secteur télécoms'),
            ('Boutique Mode BF', 'mode@boutique.bf', '+226 72 34 56 78', 'Fashion BF', 'Spécialisé mode et beauté'),
            ('Restaurant Le Sahel', 'contact@sahel.bf', '+226 73 45 67 89', 'Groupe Sahel', 'Chaîne de restaurants'),
            ('Banque Populaire', 'pub@banque.bf', '+226 74 56 78 90', 'BP Burkina', 'Institution financière')
        ]
        
        for name, email, phone, company, notes in sample_clients:
            cursor.execute('''
                INSERT INTO clients (name, email, phone, company_name, notes, created_by)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (name, email, phone, company, notes))
        
        print("   ✅ 5 clients d'exemple créés")
    
    # Vérifier si des publicités existent déjà
    cursor.execute('SELECT COUNT(*) FROM advertisements')
    if cursor.fetchone()[0] == 0:
        # Créer des publicités d'exemple
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        end_date = today + timedelta(days=30)
        
        # Récupérer les IDs des clients et espaces
        cursor.execute('SELECT id FROM clients LIMIT 5')
        client_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT id, location FROM ad_spaces WHERE is_active = 1 LIMIT 5')
        spaces = cursor.fetchall()
        
        sample_ads = [
            ('Publicité ABC - Header', 'image', None, '<div style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white; padding: 20px; text-align: center; font-weight: bold;">🏢 ABC INDUSTRIES - Votre partenaire de confiance</div>', 'https://abc-industries.bf'),
            ('Promo XYZ Télécoms', 'html', None, '<div style="background: #007bff; color: white; padding: 15px; text-align: center; border-radius: 5px;"><h3>📱 XYZ TELECOMS</h3><p>Forfaits Internet à partir de 5000 FCFA/mois</p></div>', 'https://xyz-telecoms.bf'),
            ('Mode & Beauté BF', 'html', None, '<div style="background: linear-gradient(135deg, #ff9a9e, #fecfef); padding: 20px; text-align: center; border-radius: 10px;"><h3>👗 BOUTIQUE MODE BF</h3><p>Nouvelle collection automne 2024</p></div>', 'https://boutique-mode.bf'),
            ('Restaurant Le Sahel', 'html', None, '<div style="background: #28a745; color: white; padding: 15px; text-align: center; border-radius: 8px;"><h3>🍽️ RESTAURANT LE SAHEL</h3><p>Cuisine authentique burkinabè</p></div>', 'https://restaurant-sahel.bf'),
            ('Banque Populaire', 'html', None, '<div style="background: #ffc107; color: #333; padding: 20px; text-align: center; font-weight: bold; border-radius: 5px;">🏦 BANQUE POPULAIRE<br>Crédit auto à taux préférentiel</div>', 'https://banque-populaire.bf')
        ]
        
        for i, (title, content_type, image_url, html_content, target_url) in enumerate(sample_ads):
            if i < len(client_ids) and i < len(spaces):
                cursor.execute('''
                    INSERT INTO advertisements 
                    (client_id, ad_space_id, title, content_type, image_url, html_content, 
                     target_url, start_date, end_date, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (client_ids[i], spaces[i][0], title, content_type, image_url, html_content,
                      target_url, today, end_date))
        
        print("   ✅ 5 publicités d'exemple créées")
    
    conn.commit()
    conn.close()
    print("   ✅ Données d'exemple prêtes")

def show_admin_info():
    """Afficher les informations d'administration"""
    print("\n" + "=" * 70)
    print("🔐 INFORMATIONS D'ADMINISTRATION")
    print("=" * 70)
    print("👤 Compte Administrateur:")
    print("   • Nom d'utilisateur: admin")
    print("   • Mot de passe: lcatv2024")
    print("   • Rôle: Administrateur principal")
    print()
    print("🌐 URLs d'accès:")
    print("   • Site public: http://localhost:5005/")
    print("   • Page de connexion: http://localhost:5005/login")
    print("   • Dashboard avancé: http://localhost:5005/dashboard")
    print()
    print("📊 Fonctionnalités disponibles:")
    print("   ✅ Gestion des utilisateurs (CRUD)")
    print("   ✅ Portefeuille clients complet")
    print("   ✅ Espaces publicitaires configurables")
    print("   ✅ Upload et gestion de fichiers")
    print("   ✅ Publicités HTML et images")
    print("   ✅ Analytics et statistiques")
    print("   ✅ Logs d'activité détaillés")
    print("   ✅ Système de tracking des clics")
    print()
    print("🔧 API Endpoints:")
    print("   • /api/admin/users - Gestion utilisateurs")
    print("   • /api/admin/clients - Gestion clients")
    print("   • /api/admin/advertisements - Gestion publicités")
    print("   • /api/admin/ad-spaces - Gestion espaces pub")
    print("   • /api/admin/overview - Statistiques générales")
    print("   • /health - Health check système")
    print()
    print("📁 Structure de la base de données:")
    print("   • users - Utilisateurs du système")
    print("   • clients - Portefeuille clients")
    print("   • ad_spaces - Espaces publicitaires")
    print("   • advertisements - Publicités actives")
    print("   • subscriptions - Souscriptions clients")
    print("   • activity_logs - Logs d'activité")
    print("   • ad_stats - Statistiques publicités")
    print("   • settings - Paramètres système")
    print("=" * 70)

if __name__ == '__main__':
    print("🚀 DÉMARRAGE DE LCA TV - VERSION AVANCÉE")
    print("=" * 70)
    print("🔧 Initialisation du système...")
    
    # Créer les données d'exemple
    create_sample_data()
    
    # Afficher les informations d'administration
    show_admin_info()
    
    print("\n🎯 INSTRUCTIONS DE TEST:")
    print("1. Connectez-vous avec admin / lcatv2024")
    print("2. Explorez le dashboard avancé")
    print("3. Testez la création d'utilisateurs")
    print("4. Ajoutez des clients au portefeuille")
    print("5. Créez des espaces publicitaires")
    print("6. Uploadez des publicités (images/HTML)")
    print("7. Consultez les analytics et logs")
    print("8. Visitez le site public pour voir les publicités")
    print()
    print("💡 CONSEIL: Ouvrez plusieurs onglets pour tester")
    print("   - Dashboard admin dans un onglet")
    print("   - Site public dans un autre onglet")
    print()
    print("🔥 Le serveur va démarrer sur http://localhost:5005")
    print("=" * 70)
    
    # Démarrer l'application
    app.run(debug=True, host='0.0.0.0', port=5005)