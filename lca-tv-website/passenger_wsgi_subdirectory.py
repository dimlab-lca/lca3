#!/usr/bin/python3.9
"""
WSGI entry point for LCA TV application on N0C hosting
Configured for subdirectory deployment at edifice.bf/tv-lca
Python 3.9 compatible version
"""

import os
import sys
import traceback

# Add the application directory to Python path
app_dir = os.path.dirname(__file__)
sys.path.insert(0, app_dir)

# Add parent directory to path as well
parent_dir = os.path.dirname(app_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def application(environ, start_response):
    """WSGI application with subdirectory support and error handling"""
    try:
        # Set the SCRIPT_NAME for subdirectory deployment
        environ['SCRIPT_NAME'] = '/tv-lca'
        
        # Remove the subdirectory from PATH_INFO
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/tv-lca'):
            environ['PATH_INFO'] = path_info[7:]  # Remove '/tv-lca'
        elif environ['PATH_INFO'] == '/tv-lca':
            environ['PATH_INFO'] = '/'
        
        # Import and run the Flask app
        from app import application as flask_app
        return flask_app(environ, start_response)
        
    except ImportError as e:
        # If import fails, return a detailed error page
        error_msg = f"""
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
            <p><strong>Python Path:</strong></p>
            <pre>{chr(10).join(sys.path)}</pre>
            
            <p><strong>Current Directory:</strong> {os.getcwd()}</p>
            <p><strong>App Directory:</strong> {app_dir}</p>
            
            <p><strong>Files in directory:</strong></p>
            <pre>{chr(10).join(os.listdir(app_dir))}</pre>
            
            <p><strong>Environment Variables:</strong></p>
            <pre>{chr(10).join([f"{k}: {v}" for k, v in environ.items() if 'SECRET' not in k])}</pre>
        </div>
        
        <div class="info">
            <h3>Troubleshooting Steps:</h3>
            <ol>
                <li>Ensure all Python files are uploaded correctly</li>
                <li>Check that app.py exists in the application directory</li>
                <li>Verify Python dependencies are installed</li>
                <li>Check file permissions (755 for directories, 644 for files)</li>
                <li>Restart the application in N0C panel</li>
            </ol>
        </div>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_msg.encode('utf-8')]
        
    except Exception as e:
        # Handle any other errors
        error_msg = f"""
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
        
        <p><strong>Domain:</strong> edifice.bf/tv-lca</p>
        <p><strong>Timestamp:</strong> {__import__('datetime').datetime.now()}</p>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_msg.encode('utf-8')]

# For testing
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, application)
    print("Serving LCA TV on http://localhost:8000/tv-lca")
    server.serve_forever()