#!/usr/bin/python3.9
"""
Production run script for LCA TV
Compatible with PlanetHoster's existing structure
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

def app(environ, start_response):
    """WSGI application entry point for production"""
    try:
        # Set up environment for subdirectory deployment
        environ['SCRIPT_NAME'] = '/lca'
        
        # Handle PATH_INFO for subdirectory
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/lca/'):
            environ['PATH_INFO'] = path_info[4:]
        elif path_info == '/lca':
            environ['PATH_INFO'] = '/'
        elif path_info.startswith('/lca'):
            new_path_info = path_info[4:]
            environ['PATH_INFO'] = new_path_info if new_path_info else '/'
        
        # Ensure HTTPS in production
        if 'HTTP_X_FORWARDED_PROTO' in environ:
            environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']
        else:
            environ['wsgi.url_scheme'] = 'https'
        
        # Import and run the production application
        from app_production_ready import application
        return application(environ, start_response)
        
    except ImportError as e:
        logging.error(f"Import error: {e}")
        
        # Fallback to regular app
        try:
            from app import application
            return application(environ, start_response)
        except ImportError:
            return _error_response(start_response, "Application import failed")
    
    except Exception as e:
        logging.error(f"Application error: {e}")
        return _error_response(start_response, f"Application error: {str(e)}")

def _error_response(start_response, message):
    """Return error response"""
    error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LCA TV - Service Temporarily Unavailable</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .error {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .logo {{ color: #28a745; font-size: 2rem; margin-bottom: 20px; }}
        .message {{ color: #666; margin-bottom: 20px; }}
        .links {{ margin-top: 30px; }}
        .links a {{ color: #28a745; text-decoration: none; margin: 0 10px; }}
    </style>
</head>
<body>
    <div class="error">
        <div class="logo">LCA TV</div>
        <h1>Service Temporarily Unavailable</h1>
        <div class="message">
            We're experiencing technical difficulties. Our team is working to resolve this issue.
        </div>
        <div class="message">
            <strong>Error:</strong> {message}
        </div>
        <div class="links">
            <a href="https://edifice.bf/lca">Try Again</a> |
            <a href="https://tv-lca.edifice.bf">Subdomain Access</a>
        </div>
        <div style="margin-top: 20px; font-size: 12px; color: #999;">
            Hosting: PlanetHoster | Domain: edifice.bf/lca
        </div>
    </div>
</body>
</html>
    """
    
    start_response('503 Service Unavailable', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Retry-After', '300')
    ])
    return [error_html.encode('utf-8')]