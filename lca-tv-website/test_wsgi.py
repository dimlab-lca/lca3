#!/usr/bin/python3.9
"""
Test WSGI pour diagnostiquer les problèmes de routage LCA TV
Uploadez ce fichier dans /public_html/lca/ et testez https://edifice.bf/lca/test_wsgi.py
"""

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)
    
    # Récupérer les informations de la requête
    path_info = environ.get('PATH_INFO', '')
    script_name = environ.get('SCRIPT_NAME', '')
    request_uri = environ.get('REQUEST_URI', '')
    query_string = environ.get('QUERY_STRING', '')
    server_name = environ.get('SERVER_NAME', '')
    request_method = environ.get('REQUEST_METHOD', '')
    
    # Récupérer tous les headers
    headers_info = []
    for key, value in environ.items():
        if key.startswith('HTTP_'):
            header_name = key[5:].replace('_', '-').title()
            headers_info.append(f"<tr><td>{header_name}</td><td>{value}</td></tr>")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LCA TV - Test WSGI</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .success {{ color: green; font-weight: bold; }}
            .info {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .test-links {{ background: #e8f5e8; padding: 15px; margin: 20px 0; }}
            .test-links a {{ display: block; margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>🎯 LCA TV - Test WSGI</h1>
        <p class="success">✅ WSGI fonctionne! L'application Python est accessible.</p>
        
        <div class="info">
            <h2>📊 Informations de la Requête</h2>
            <table>
                <tr><th>Variable</th><th>Valeur</th></tr>
                <tr><td><strong>REQUEST_METHOD</strong></td><td>{request_method}</td></tr>
                <tr><td><strong>SERVER_NAME</strong></td><td>{server_name}</td></tr>
                <tr><td><strong>REQUEST_URI</strong></td><td>{request_uri}</td></tr>
                <tr><td><strong>SCRIPT_NAME</strong></td><td>{script_name}</td></tr>
                <tr><td><strong>PATH_INFO</strong></td><td>{path_info}</td></tr>
                <tr><td><strong>QUERY_STRING</strong></td><td>{query_string}</td></tr>
            </table>
        </div>
        
        <div class="info">
            <h2>🌐 Headers HTTP</h2>
            <table>
                <tr><th>Header</th><th>Valeur</th></tr>
                {''.join(headers_info)}
            </table>
        </div>
        
        <div class="test-links">
            <h2>🧪 Liens de Test</h2>
            <p>Testez ces liens pour vérifier le routage:</p>
            <a href="/lca/">🏠 Accueil LCA TV</a>
            <a href="/lca/health">❤️ Health Check</a>
            <a href="/lca/debug">🔍 Debug Info</a>
            <a href="/lca/journal">📰 Journal</a>
            <a href="/lca/live">📺 Live</a>
            <a href="/lca/emissions">📻 Émissions</a>
            <a href="/lca/login">🔐 Login</a>
            <a href="/lca/api/videos">🎬 API Videos</a>
        </div>
        
        <div class="info">
            <h2>🔧 Diagnostic</h2>
            <ul>
                <li><strong>Si vous voyez cette page:</strong> WSGI fonctionne ✅</li>
                <li><strong>Si SCRIPT_NAME = '/lca':</strong> Configuration correcte ✅</li>
                <li><strong>Si les liens de test fonctionnent:</strong> Routage OK ✅</li>
                <li><strong>Si les liens ne fonctionnent pas:</strong> Problème de routage Flask ❌</li>
            </ul>
        </div>
        
        <div class="info">
            <h2>📝 Prochaines Étapes</h2>
            <ol>
                <li>Testez chaque lien ci-dessus</li>
                <li>Si un lien ne fonctionne pas, notez l'erreur</li>
                <li>Vérifiez les logs: <code>tail -f ~/logs/error.log</code></li>
                <li>Redémarrez l'app: <code>touch ~/public_html/lca/tmp/restart.txt</code></li>
            </ol>
        </div>
        
        <hr>
        <p><small>Test généré le: {__import__('datetime').datetime.now()}</small></p>
    </body>
    </html>
    """
    
    return [html.encode('utf-8')]

# Pour les tests directs
if __name__ == '__main__':
    print("Test WSGI pour LCA TV")
    print("Uploadez ce fichier et testez: https://edifice.bf/lca/test_wsgi.py")