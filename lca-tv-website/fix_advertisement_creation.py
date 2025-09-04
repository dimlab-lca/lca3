#!/usr/bin/env python3
"""
Script pour corriger la fonction de création de publicité
en adaptant à la structure existante de la table advertisements
"""

import sqlite3
from datetime import datetime

def analyze_existing_table():
    """Analyser la structure existante de la table advertisements"""
    conn = sqlite3.connect('lca_tv.db')
    cursor = conn.cursor()
    
    # Obtenir la structure de la table
    cursor.execute("PRAGMA table_info(advertisements)")
    columns = cursor.fetchall()
    
    print("📊 Structure actuelle de la table 'advertisements':")
    print("-" * 60)
    for col in columns:
        print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
    
    conn.close()
    return columns

def create_fixed_advertisement_function():
    """Créer une fonction de création de publicité adaptée à la structure existante"""
    
    function_code = '''
def create_advertisement():
    """Créer une nouvelle publicité - Version corrigée pour la structure existante"""
    try:
        print("=== DEBUG: Création de publicité (version corrigée) ===")
        print(f"Form data: {dict(request.form)}")
        print(f"Files: {list(request.files.keys())}")
        
        data = request.form
        
        # Récupérer les données du formulaire
        ad_title = data.get('ad_title', '').strip()
        client_id_str = data.get('ad_client', '')
        space_id_str = data.get('ad_space', '')
        content_type = data.get('ad_type', 'image')
        target_url = data.get('ad_url', '').strip()
        start_date = data.get('ad_start_date', '').strip()
        end_date = data.get('ad_end_date', '').strip()
        
        print(f"Données reçues: title={ad_title}, client_id={client_id_str}, space_id={space_id_str}")
        
        # Validation des champs obligatoires
        if not ad_title:
            return jsonify({'success': False, 'error': 'Le titre est obligatoire'}), 400
        
        if not client_id_str or not client_id_str.isdigit():
            return jsonify({'success': False, 'error': 'Veuillez sélectionner un client'}), 400
        
        if not space_id_str or not space_id_str.isdigit():
            return jsonify({'success': False, 'error': 'Veuillez sélectionner un espace publicitaire'}), 400
        
        if not start_date or not end_date:
            return jsonify({'success': False, 'error': 'Les dates sont obligatoires'}), 400
        
        try:
            client_id = int(client_id_str)
            space_id = int(space_id_str)
        except ValueError:
            return jsonify({'success': False, 'error': 'IDs invalides'}), 400
        
        # Validation des dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if end_date_obj < start_date_obj:
                return jsonify({'success': False, 'error': 'Date de fin invalide'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Format de date invalide'}), 400
        
        # Connexion à la base de données
        conn = sqlite3.connect('lca_tv.db')
        cursor = conn.cursor()
        
        # Récupérer les informations du client
        cursor.execute('SELECT name, email, phone FROM clients WHERE id = ?', (client_id,))
        client_info = cursor.fetchone()
        if not client_info:
            conn.close()
            return jsonify({'success': False, 'error': 'Client introuvable'}), 400
        
        client_name, client_email, client_phone = client_info
        
        # Récupérer les informations de l'espace publicitaire
        cursor.execute('SELECT name, location FROM ad_spaces WHERE id = ?', (space_id,))
        space_info = cursor.fetchone()
        if not space_info:
            conn.close()
            return jsonify({'success': False, 'error': 'Espace publicitaire introuvable'}), 400
        
        space_name, space_location = space_info
        
        # Traiter le contenu selon le type
        ad_content = ""
        media_url = ""
        media_filename = ""
        
        if content_type == 'image':
            if 'ad_image' in request.files:
                file = request.files['ad_image']
                if file and file.filename and allowed_file(file.filename):
                    try:
                        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ads', filename)
                        file.save(file_path)
                        media_url = f"/static/uploads/ads/{filename}"
                        media_filename = filename
                        ad_content = f'<img src="{media_url}" alt="{ad_title}" style="max-width:100%;height:auto;">'
                        print(f"Image sauvegardée: {media_url}")
                    except Exception as e:
                        conn.close()
                        return jsonify({'success': False, 'error': f'Erreur upload: {str(e)}'}), 500
                else:
                    conn.close()
                    return jsonify({'success': False, 'error': 'Image invalide'}), 400
            else:
                conn.close()
                return jsonify({'success': False, 'error': 'Image requise'}), 400
        
        elif content_type == 'html':
            html_content = data.get('ad_html', '').strip()
            if not html_content:
                conn.close()
                return jsonify({'success': False, 'error': 'Code HTML requis'}), 400
            ad_content = html_content
        
        # Insérer la publicité avec la structure existante
        try:
            cursor.execute("""
                INSERT INTO advertisements 
                (client_name, client_email, client_phone, ad_title, ad_content, 
                 media_type, media_url, media_filename, start_date, end_date, 
                 position, status, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 0.00)
            """, (client_name, client_email, client_phone, ad_title, ad_content,
                  content_type, media_url, media_filename, start_date, end_date, space_location))
            
            ad_id = cursor.lastrowid
            conn.commit()
            print(f"Publicité créée avec ID: {ad_id}")
            
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            print(f"Erreur SQLite: {e}")
            return jsonify({'success': False, 'error': f'Erreur base de données: {str(e)}'}), 500
        
        conn.close()
        
        return jsonify({'success': True, 'ad_id': ad_id, 'message': 'Publicité créée avec succès'})
        
    except Exception as e:
        print(f"Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Erreur interne: {str(e)}'}), 500
'''
    
    return function_code

def main():
    print("🔧 Correction de la fonction de création de publicité")
    print("=" * 60)
    
    # Analyser la structure existante
    columns = analyze_existing_table()
    
    print("\n📝 Fonction corrigée générée:")
    print("   • Adaptation à la structure existante")
    print("   • Gestion des clients par nom au lieu d'ID")
    print("   • Mapping correct des champs")
    
    # Générer le code corrigé
    fixed_function = create_fixed_advertisement_function()
    
    # Sauvegarder dans un fichier
    with open('create_advertisement_fixed.py', 'w', encoding='utf-8') as f:
        f.write(fixed_function)
    
    print(f"\n✅ Code corrigé sauvegardé dans 'create_advertisement_fixed.py'")
    print("\n🎯 Prochaines étapes:")
    print("   1. Remplacer la fonction dans app_advanced.py")
    print("   2. Redémarrer l'application")
    print("   3. Tester la création de publicité")

if __name__ == "__main__":
    main()