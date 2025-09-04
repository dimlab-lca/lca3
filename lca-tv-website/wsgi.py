#!/usr/bin/env python3
"""
WSGI Entry Point for LCA TV Website
For PlanetHoster deployment
"""

import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(__file__)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Import the Flask application
from app import application

# For debugging (remove in production)
if __name__ == "__main__":
    application.run(debug=False, host='0.0.0.0', port=8000)