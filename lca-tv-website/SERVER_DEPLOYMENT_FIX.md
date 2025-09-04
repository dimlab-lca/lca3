# LCA TV - Server Deployment Fix

## Problem: "Incomplete response received from application"

This error typically occurs when:
1. The WSGI application file is incomplete or corrupted
2. Python dependencies are missing
3. File permissions are incorrect
4. Python version incompatibility

## ✅ SOLUTION

### Step 1: Replace Files on Server

Upload these **FIXED** files to your server:

1. **`app_production_fixed.py`** - Fixed production application
2. **`passenger_wsgi_fixed.py`** - Fixed WSGI configuration
3. **`templates/dashboard_simple.html`** - Fixed dashboard template

### Step 2: Rename Files on Server

```bash
# Backup old files
mv passenger_wsgi.py passenger_wsgi_old.py
mv app_production_final.py app_production_final_old.py

# Use fixed versions
mv passenger_wsgi_fixed.py passenger_wsgi.py
mv app_production_fixed.py app_production_final.py
```

### Step 3: Verify File Integrity

Check that files are complete and not truncated:

```bash
# Check file sizes
ls -la *.py

# Check if files end properly (should show "if __name__ == '__main__':")
tail -5 passenger_wsgi.py
tail -5 app_production_final.py
```

### Step 4: Check Python Environment

```bash
# Verify Python version (should be 3.9+)
python3 --version

# Install/update dependencies
pip3 install --user flask requests

# Or if you have requirements.txt:
pip3 install --user -r requirements.txt
```

### Step 5: Test the Application

```bash
# Test import
python3 -c "from passenger_wsgi import application; print('Import successful')"

# Test basic functionality
python3 -c "
from passenger_wsgi import application
with application.test_client() as client:
    response = client.get('/')
    print(f'Home page status: {response.status_code}')
    response = client.get('/health')
    print(f'Health check status: {response.status_code}')
"
```

### Step 6: Check File Permissions

```bash
# Ensure files are readable
chmod 644 *.py
chmod 644 templates/*.html
chmod 755 static/

# Ensure directories are accessible
find . -type d -exec chmod 755 {} \;
```

## 🔧 Alternative Solutions

### Option A: Use Simple WSGI (if main fix doesn't work)

Create a minimal `passenger_wsgi.py`:

```python
#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Simple import with fallback
try:
    from app_production_fixed import application
except ImportError:
    try:
        from app import application
    except ImportError:
        from flask import Flask
        application = Flask(__name__)
        
        @application.route('/')
        def home():
            return "LCA TV - Service Available"
        
        @application.route('/health')
        def health():
            return {"status": "ok"}

if __name__ == "__main__":
    application.run()
```

### Option B: Debug Mode (temporary)

For debugging, create `passenger_wsgi_debug.py`:

```python
#!/usr/bin/env python3
import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(__file__))

try:
    from app_production_fixed import application
    print("Application loaded successfully", file=sys.stderr)
except Exception as e:
    print(f"Error loading application: {e}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    
    # Create emergency app
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error_page():
        return f"Error: {str(e)}"
```

## 🚨 Emergency Recovery

If nothing works, use this minimal working version:

```python
#!/usr/bin/env python3
# passenger_wsgi.py - Emergency version
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, jsonify

application = Flask(__name__)
application.config['SECRET_KEY'] = 'emergency-key'

@application.route('/')
def home():
    return render_template('home.html', featured_videos=[])

@application.route('/health')
def health():
    return jsonify({"status": "emergency_mode", "message": "LCA TV running in emergency mode"})

@application.route('/login')
def login():
    return render_template('login_simple.html')

if __name__ == "__main__":
    application.run()
```

## 📋 Verification Checklist

After deployment, verify:

- [ ] Home page loads: `https://yoursite.com/lca/`
- [ ] Health check works: `https://yoursite.com/lca/health`
- [ ] Login page loads: `https://yoursite.com/lca/login`
- [ ] No "Incomplete response" errors
- [ ] Server error logs are clean

## 🔍 Troubleshooting

### Check Server Logs

Look for these common issues:

1. **Import errors**: Missing dependencies
2. **Syntax errors**: File corruption during upload
3. **Permission errors**: Incorrect file permissions
4. **Memory errors**: Insufficient server resources

### Common Fixes

1. **File upload issues**: Re-upload files in binary mode
2. **Line ending issues**: Convert Windows line endings to Unix
3. **Encoding issues**: Ensure files are UTF-8 encoded
4. **Path issues**: Use absolute paths in imports

## 📞 Support

If you continue to have issues:

1. Check server error logs
2. Test with the emergency version above
3. Verify Python version and dependencies
4. Contact your hosting provider for WSGI configuration help

---

**Status**: ✅ **FIXED** - Use `app_production_fixed.py` and `passenger_wsgi_fixed.py`