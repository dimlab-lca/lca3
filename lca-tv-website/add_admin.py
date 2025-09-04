login le #!/usr/bin/env python3
"""
Script pour ajouter un nouvel administrateur dans la base de données LCA TV
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db_manager, user_manager

def add_new_admin():
    """Ajouter un nouvel administrateur"""
    print("🔧 AJOUT D'UN NOUVEL ADMINISTRATEUR LCA TV")
    print("=" * 50)
    
    # Informations du nouvel administrateur
    username = input("Nom d'utilisateur: ").strip()
    if not username:
        username = "admin2"
        print(f"Utilisation du nom par défaut: {username}")
    
    email = input("Email: ").strip()
    if not email:
        email = f"{username}@lcatv.bf"
        print(f"Utilisation de l'email par défaut: {email}")
    
    password = input("Mot de passe: ").strip()
    if not password:
        password = "lcatv2024"
        print(f"Utilisation du mot de passe par défaut: {password}")
    
    full_name = input("Nom complet: ").strip()
    if not full_name:
        full_name = f"Administrateur {username.title()}"
        print(f"Utilisation du nom complet par défaut: {full_name}")
    
    phone = input("Téléphone (optionnel): ").strip()
    
    try:
        # Créer le nouvel utilisateur
        user_id = user_manager.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            full_name=full_name,
            phone=phone,
            is_active=True
        )
        
        print(f"\n✅ SUCCÈS: Nouvel administrateur créé avec l'ID {user_id}")
        print(f"   • Nom d'utilisateur: {username}")
        print(f"   • Email: {email}")
        print(f"   • Mot de passe: {password}")
        print(f"   • Nom complet: {full_name}")
        if phone:
            print(f"   • Téléphone: {phone}")
        
    except Exception as e:
        print(f"❌ ERREUR: Impossible de créer l'administrateur")
        print(f"   • Détail: {str(e)}")
        return False
    
    return True

def list_all_users():
    """Lister tous les utilisateurs"""
    print("\n📋 LISTE DES UTILISATEURS EXISTANTS")
    print("=" * 40)
    
    try:
        users = user_manager.get_users(active_only=False)
        
        if not users:
            print("Aucun utilisateur trouvé.")
            return
        
        for user in users:
            status = "✅ Actif" if user['is_active'] else "❌ Inactif"
            last_login = user['last_login'] if user['last_login'] else "Jamais"
            
            print(f"\n👤 {user['username']} ({user['role'].upper()})")
            print(f"   • ID: {user['id']}")
            print(f"   • Email: {user['email']}")
            print(f"   • Nom: {user['full_name'] or 'Non défini'}")
            print(f"   • Statut: {status}")
            print(f"   • Dernière connexion: {last_login}")
            print(f"   • Créé le: {user['created_at']}")
            
    except Exception as e:
        print(f"❌ ERREUR: Impossible de lister les utilisateurs")
        print(f"   • Détail: {str(e)}")

def reset_admin_password():
    """Réinitialiser le mot de passe de l'admin principal"""
    print("\n🔄 RÉINITIALISATION DU MOT DE PASSE ADMIN")
    print("=" * 45)
    
    try:
        # Mettre à jour le mot de passe de l'admin principal
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        from werkzeug.security import generate_password_hash
        new_password = "lcatv2024"
        password_hash = generate_password_hash(new_password)
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, updated_at = ?
            WHERE username = 'admin'
        ''', (password_hash, datetime.now()))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ SUCCÈS: Mot de passe de 'admin' réinitialisé")
            print(f"   • Nouveau mot de passe: {new_password}")
        else:
            print("❌ ERREUR: Utilisateur 'admin' non trouvé")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERREUR: Impossible de réinitialiser le mot de passe")
        print(f"   • Détail: {str(e)}")

def main():
    """Menu principal"""
    print("🚀 GESTIONNAIRE D'UTILISATEURS LCA TV")
    print("=" * 40)
    print("1. Ajouter un nouvel administrateur")
    print("2. Lister tous les utilisateurs")
    print("3. Réinitialiser le mot de passe admin")
    print("4. Quitter")
    print("=" * 40)
    
    while True:
        choice = input("\nChoisissez une option (1-4): ").strip()
        
        if choice == '1':
            add_new_admin()
        elif choice == '2':
            list_all_users()
        elif choice == '3':
            reset_admin_password()
        elif choice == '4':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide. Veuillez choisir entre 1 et 4.")

if __name__ == '__main__':
    main()