#!/usr/bin/python3.9
"""
Production WSGI entry point for LCA TV on PlanetHoster
Optimized for stability and performance
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Import the production-ready application
    from app_production_ready import application
    
    # Log successful startup
    logging.info("LCA TV application started successfully")
    
except ImportError as e:
    logging.error(f"Failed to import application: {e}")
    
    # Fallback to regular app.py if production version fails
    try:
        from app import application
        logging.warning("Using fallback app.py instead of production version")
    except ImportError as fallback_error:
        logging.critical(f"Failed to import fallback application: {fallback_error}")
        raise

except Exception as e:
    logging.critical(f"Critical error starting application: {e}")
    raise

# Ensure application is available for WSGI
if 'application' not in locals():
    logging.critical("No application object found")
    raise RuntimeError("Application failed to initialize")