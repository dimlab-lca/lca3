#!/usr/bin/python3.9
"""
LCA TV Application Entry Point for PlanetHoster
Compatible with existing run.py/passenger_wsgi.py structure
"""

import os
import sys
import traceback

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def app(environ, start_response):
    """WSGI application entry point for LCA TV"""
    try:
        # Debug information
        server_name = environ.get('SERVER_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        request_uri = environ.get('REQUEST_URI', '')
        query_string = environ.get('QUERY_STRING', '')
        
        # CRITICAL: Always set SCRIPT_NAME for subdirectory deployment
        environ['SCRIPT_NAME'] = '/lca'
        
        # Handle PATH_INFO properly - this is crucial for routing
        original_path_info = path_info
        
        if path_info.startswith('/lca/'):
            # Remove /lca from PATH_INFO but keep the trailing slash and path
            new_path_info = path_info[4:]  # Remove '/lca' but keep the rest
            environ['PATH_INFO'] = new_path_info
        elif path_info == '/lca':
            # Exact /lca should go to home
            environ['PATH_INFO'] = '/'
        elif path_info.startswith('/lca'):
            # Handle /lca without trailing slash
            new_path_info = path_info[4:]
            if not new_path_info:
                new_path_info = '/'
            environ['PATH_INFO'] = new_path_info
        else:
            # If PATH_INFO doesn't start with /lca, it might be already processed
            # Keep it as is
            pass
        
        # Ensure proper URL scheme
        if 'HTTP_X_FORWARDED_PROTO' in environ:
            environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']
        elif environ.get('HTTPS', '').lower() in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        else:
            environ['wsgi.url_scheme'] = 'https'  # Force HTTPS for production
        
        # Add debug headers for troubleshooting
        environ['HTTP_X_LCA_ORIGINAL_PATH'] = original_path_info
        environ['HTTP_X_LCA_NEW_PATH'] = environ['PATH_INFO']
        environ['HTTP_X_LCA_SCRIPT_NAME'] = environ['SCRIPT_NAME']
        
        # Import and run the Flask app
        from app import application as flask_app
        return flask_app(environ, start_response)
        
    except ImportError as e:
        # If import fails, return a detailed error page
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LCA TV - Import Error</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .error {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .error h1 {{ color: #dc3545; }}
        .error pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
        .info {{ margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>LCA TV - Import Error</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        
        <div class="info">
            <h3>Debug Information:</h3>
            <p><strong>Server Name:</strong> {server_name}</p>
            <p><strong>Path Info:</strong> {path_info}</p>
            <p><strong>Python Version:</strong> {sys.version}</p>
            <p><strong>Current Directory:</strong> {os.getcwd()}</p>
            <p><strong>Files in directory:</strong></p>
            <pre>{chr(10).join(os.listdir(os.path.dirname(__file__)))}</pre>
        </div>
        
        <div class="info">
            <h3>Access Methods:</h3>
            <ul>
                <li><strong>Subdirectory:</strong> https://edifice.bf/lca</li>
                <li><strong>Subdomain:</strong> https://tv-lca.edifice.bf</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>Troubleshooting Steps:</h3>
            <ol>
                <li>Ensure all Python files are uploaded correctly</li>
                <li>Check that app.py exists in the application directory</li>
                <li>Verify Python dependencies are installed: pip install -r requirements.txt</li>
                <li>Check file permissions (755 for directories, 644 for files)</li>
                <li>Restart the application in PlanetHoster cPanel</li>
            </ol>
        </div>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_html.encode('utf-8')]
        
    except Exception as e:
        # Handle any other errors
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LCA TV - Application Error</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .error {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .error h1 {{ color: #dc3545; }}
        .error pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>LCA TV - Application Error</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        
        <p><strong>Traceback:</strong></p>
        <pre>{traceback.format_exc()}</pre>
        
        <p><strong>Domain Access:</strong></p>
        <ul>
            <li>Subdirectory: edifice.bf/lca</li>
            <li>Subdomain: tv-lca.edifice.bf</li>
        </ul>
        <p><strong>Hosting:</strong> PlanetHoster</p>
        <p><strong>Python Version:</strong> {sys.version}</p>
        <p><strong>Timestamp:</strong> {__import__('datetime').datetime.now()}</p>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_html.encode('utf-8')]