#!/usr/bin/env python3
"""
Script de test pour la création de publicité
"""

import sqlite3
import os
from datetime import datetime, timedelta

def test_database():
    """Test de la base de données"""
    db_path = 'lca_tv.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['clients', 'ad_spaces', 'advertisements']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Tables manquantes: {missing_tables}")
            return False
        
        print("✅ Toutes les tables requises sont présentes")
        
        # Vérifier les données de test
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ad_spaces")
        space_count = cursor.fetchone()[0]
        
        print(f"📊 Clients: {client_count}")
        print(f"📊 Espaces publicitaires: {space_count}")
        
        if client_count == 0:
            print("⚠️  Aucun client trouvé - création d'un client de test")
            cursor.execute("""
                INSERT INTO clients (name, email, phone, company_name, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "Test Client",
                "test@example.com",
                "+225 01 02 03 04 05",
                "Test Company",
                "active",
                datetime.now().isoformat()
            ))
            conn.commit()
            print("✅ Client de test créé")
        
        if space_count == 0:
            print("⚠️  Aucun espace publicitaire trouvé - création d'espaces de test")
            spaces = [
                ("Header Banner", "header", 728, 90, 50000),
                ("Sidebar Ad", "sidebar", 300, 250, 30000),
                ("Footer Banner", "footer", 728, 90, 40000),
                ("Popup Ad", "popup", 400, 300, 60000)
            ]
            
            for name, location, width, height, price in spaces:
                cursor.execute("""
                    INSERT INTO ad_spaces (name, location, width, height, price, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, location, width, height, price, True, datetime.now().isoformat()))
            
            conn.commit()
            print("✅ Espaces publicitaires de test créés")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

def test_ad_creation():
    """Test de création de publicité"""
    try:
        conn = sqlite3.connect('lca_tv.db')
        cursor = conn.cursor()
        
        # Récupérer un client et un espace
        cursor.execute("SELECT id FROM clients LIMIT 1")
        client_result = cursor.fetchone()
        if not client_result:
            print("❌ Aucun client disponible")
            return False
        client_id = client_result[0]
        
        cursor.execute("SELECT id FROM ad_spaces LIMIT 1")
        space_result = cursor.fetchone()
        if not space_result:
            print("❌ Aucun espace publicitaire disponible")
            return False
        space_id = space_result[0]
        
        # Créer une publicité de test avec la structure existante
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
        
        # Récupérer les infos du client
        cursor.execute("SELECT name, email, phone FROM clients WHERE id = ?", (client_id,))
        client_info = cursor.fetchone()
        client_name, client_email, client_phone = client_info
        
        # Récupérer les infos de l'espace
        cursor.execute("SELECT location FROM ad_spaces WHERE id = ?", (space_id,))
        space_location = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO advertisements (
                client_name, client_email, client_phone, ad_title, ad_content,
                media_type, media_url, media_filename, start_date, end_date, 
                position, status, price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            client_name,
            client_email,
            client_phone,
            "Test Advertisement",
            "<div style='background: #28a745; color: white; padding: 20px; text-align: center;'>Test Pub</div>",
            "banner",
            "",
            "",
            start_date.isoformat(),
            end_date.isoformat(),
            space_location,
            "active",
            0.00
        ))
        
        conn.commit()
        ad_id = cursor.lastrowid
        
        print(f"✅ Publicité de test créée avec l'ID: {ad_id}")
        
        # Vérifier la création
        cursor.execute("SELECT * FROM advertisements WHERE id = ?", (ad_id,))
        ad = cursor.fetchone()
        
        if ad:
            print("✅ Publicité vérifiée dans la base de données")
            print(f"   Titre: {ad[4]}")  # ad_title est à l'index 4
            print(f"   Client: {ad[1]}")  # client_name est à l'index 1
            print(f"   Position: {ad[11]}")  # position est à l'index 11
            print(f"   Statut: {ad[12]}")  # status est à l'index 12
        else:
            print("❌ Publicité non trouvée après création")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de publicité: {e}")
        return False

def main():
    print("🧪 Test de création de publicité LCA TV")
    print("=" * 50)
    
    # Test de la base de données
    if not test_database():
        print("\n❌ Échec du test de base de données")
        return
    
    print("\n" + "=" * 50)
    
    # Test de création de publicité
    if test_ad_creation():
        print("\n✅ Tous les tests sont passés avec succès!")
        print("\n🚀 Vous pouvez maintenant tester la création de publicité dans le dashboard:")
        print("   1. Connectez-vous au dashboard (admin / lcatv2024)")
        print("   2. Allez dans l'onglet 'Publicités'")
        print("   3. Cliquez sur 'Nouvelle Publicité'")
        print("   4. Remplissez le formulaire et testez")
    else:
        print("\n❌ Échec du test de création de publicité")

if __name__ == "__main__":
    main()