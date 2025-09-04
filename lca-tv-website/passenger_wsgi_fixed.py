#!/usr/bin/env python3
"""
WSGI Configuration for LCA TV Production - FIXED
Fixed version to prevent "Incomplete response received from application" error
"""

import sys
import os

# Ajouter le répertoire de l'application au path Python
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

# Configuration des variables d'environnement pour la production
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_CONFIG'] = 'production'

try:
    # Import de l'application fixée
    from app_production_fixed import application
    
    # Ensure the application is properly configured
    if hasattr(application, 'config'):
        application.config['DEBUG'] = False
        application.config['TESTING'] = False
    
    # Log successful import
    print(f"[WSGI] LCA TV application loaded successfully from {current_dir}", file=sys.stderr)
    
except ImportError as e:
    print(f"[WSGI ERROR] Failed to import application: {e}", file=sys.stderr)
    # Fallback to main app.py if the fixed version fails
    try:
        from app import application
        print(f"[WSGI] Fallback to main app.py successful", file=sys.stderr)
    except ImportError as e2:
        print(f"[WSGI ERROR] Fallback also failed: {e2}", file=sys.stderr)
        # Create a minimal WSGI application as last resort
        from flask import Flask
        application = Flask(__name__)
        
        @application.route('/')
        def emergency_response():
            return "LCA TV - Service temporarily unavailable. Please contact support."
        
        print(f"[WSGI] Emergency application created", file=sys.stderr)

except Exception as e:
    print(f"[WSGI ERROR] Unexpected error: {e}", file=sys.stderr)
    # Create emergency application
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def emergency_response():
        return f"LCA TV - Service error: {str(e)}"

# Ensure we have a valid WSGI application
if not hasattr(application, '__call__'):
    print(f"[WSGI ERROR] Application is not callable", file=sys.stderr)
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error_response():
        return "LCA TV - WSGI Configuration Error"

# Configuration spécifique pour PlanetHoster
if __name__ == "__main__":
    try:
        application.run(debug=False, host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"[WSGI ERROR] Failed to run application: {e}", file=sys.stderr)