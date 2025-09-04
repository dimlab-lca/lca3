#!/usr/bin/env python3
"""
WSGI Configuration for LCA TV Production
Configuration spécifique pour PlanetHoster avec sous-répertoire /lca
"""

import sys
import os

# Ajouter le répertoire de l'application au path Python
sys.path.insert(0, os.path.dirname(__file__))

# Configuration des variables d'environnement pour la production
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_CONFIG'] = 'production'

# Import de l'application
from app_production_final import application

# Configuration spécifique pour PlanetHoster
if __name__ == "__main__":
    application.run()