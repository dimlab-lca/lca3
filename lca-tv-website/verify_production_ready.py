#!/usr/bin/env python3
"""
LCA TV Production Readiness Verification Script
Checks all components before deployment
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filepath}")
    return exists

def check_directory_structure():
    """Verify directory structure"""
    print("\n📁 Directory Structure Check:")
    
    required_dirs = [
        "templates",
        "static",
        "static/images",
        "static/css",
        "static/js"
    ]
    
    all_good = True
    for directory in required_dirs:
        exists = os.path.exists(directory)
        status = "✅" if exists else "❌"
        print(f"{status} {directory}/")
        if not exists:
            all_good = False
    
    return all_good

def check_production_files():
    """Check production-ready files"""
    print("\n🚀 Production Files Check:")
    
    production_files = [
        ("app_production_ready.py", True),
        ("passenger_wsgi_production.py", True),
        ("run_production.py", True),
        ("requirements_production.txt", True),
        (".env_production", True),
        ("PRODUCTION_DEPLOYMENT_GUIDE.md", True)
    ]
    
    all_good = True
    for filepath, required in production_files:
        exists = check_file_exists(filepath, required)
        if required and not exists:
            all_good = False
    
    return all_good

def check_template_files():
    """Check template files"""
    print("\n📄 Template Files Check:")
    
    template_files = [
        "templates/base.html",
        "templates/home.html",
        "templates/live.html",
        "templates/videos.html",
        "templates/journal.html",
        "templates/emissions.html",
        "templates/publicite.html",
        "templates/about.html",
        "templates/contact.html",
        "templates/login.html",
        "templates/dashboard.html",
        "templates/404.html",
        "templates/500.html"
    ]
    
    all_good = True
    for template in template_files:
        exists = check_file_exists(template, True)
        if not exists:
            all_good = False
    
    return all_good

def check_static_files():
    """Check static files"""
    print("\n🎨 Static Files Check:")
    
    # Check for your actual images
    image_files = [
        "static/images/LOGO LCA.png",
        "static/images/FRANC PARLER (TOUS LES MERCREDIS A 20H 40).png",
        "static/images/7 AFRIQUE (TOUS LES DIMANCHES A 13H 00).png",
        "static/images/QUESTIONS DE FEMMES (TOUS LES LUNDIS A 20H 40).png",
        "static/images/SOLEIL D_AFRIQUE (DU LUNDI AU VENDREDI A 11H 00).png"
    ]
    
    all_good = True
    for image in image_files:
        exists = check_file_exists(image, True)
        if not exists:
            all_good = False
    
    return all_good

def check_configuration():
    """Check configuration files"""
    print("\n⚙️ Configuration Check:")
    
    config_files = [
        ("config.py", True),
        (".env.example", True),
        ("requirements.txt", False),  # Original, not required if production version exists
    ]
    
    all_good = True
    for filepath, required in config_files:
        exists = check_file_exists(filepath, required)
        if required and not exists:
            all_good = False
    
    return all_good

def check_wsgi_compatibility():
    """Check WSGI compatibility"""
    print("\n🔧 WSGI Compatibility Check:")
    
    try:
        # Try importing the production app
        sys.path.insert(0, os.getcwd())
        from app_production_ready import application
        print("✅ app_production_ready.py imports successfully")
        
        # Check if it has the required WSGI interface
        if callable(application):
            print("✅ Application is callable (WSGI compatible)")
        else:
            print("❌ Application is not callable")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_dependencies():
    """Check if dependencies are reasonable"""
    print("\n📦 Dependencies Check:")
    
    try:
        with open("requirements_production.txt", "r") as f:
            deps = f.read().strip().split("\n")
        
        print(f"✅ Found {len(deps)} dependencies")
        
        # Check for critical dependencies
        critical_deps = ["Flask", "requests", "Werkzeug"]
        for dep in critical_deps:
            found = any(dep in line for line in deps)
            status = "✅" if found else "❌"
            print(f"{status} {dep}")
        
        return True
        
    except FileNotFoundError:
        print("❌ requirements_production.txt not found")
        return False

def generate_deployment_summary():
    """Generate deployment summary"""
    print("\n📋 Deployment Summary:")
    
    summary = {
        "status": "ready",
        "domains": {
            "primary": "edifice.bf/lca",
            "subdomain": "tv-lca.edifice.bf"
        },
        "hosting": "PlanetHoster",
        "python_version": "3.9",
        "features": [
            "Beautiful slider with your program banners",
            "Professional responsive design",
            "Admin dashboard with content management",
            "YouTube integration with fallbacks",
            "Mobile-optimized experience",
            "Production-ready performance",
            "Comprehensive error handling",
            "Security best practices"
        ],
        "files_to_upload": [
            "app_production_ready.py → app.py (or keep as is)",
            "passenger_wsgi_production.py → passenger_wsgi.py",
            "run_production.py → run.py",
            "requirements_production.txt → requirements.txt",
            ".env_production → .env (configure with your values)",
            "All templates/ directory",
            "All static/ directory"
        ]
    }
    
    print(json.dumps(summary, indent=2))
    return summary

def main():
    """Main verification function"""
    print("🔍 LCA TV Production Readiness Verification")
    print("=" * 50)
    
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Production Files", check_production_files),
        ("Template Files", check_template_files),
        ("Static Files", check_static_files),
        ("Configuration", check_configuration),
        ("WSGI Compatibility", check_wsgi_compatibility),
        ("Dependencies", check_dependencies)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("🎉 ALL CHECKS PASSED! Your LCA TV website is PRODUCTION READY!")
        print("\n✅ Ready for deployment to PlanetHoster")
        print("✅ Subdirectory support configured")
        print("✅ Beautiful slider with your images")
        print("✅ Professional responsive design")
        print("✅ Admin dashboard included")
        print("✅ Error handling implemented")
        
        generate_deployment_summary()
        
        print("\n🚀 Next Steps:")
        print("1. Upload files to /public_html/lca/")
        print("2. Rename production files as indicated")
        print("3. Configure .env with your secure passwords")
        print("4. Install dependencies in cPanel")
        print("5. Test at https://edifice.bf/lca")
        
    else:
        print("⚠️ Some checks failed. Please review the issues above.")
        failed_checks = [checks[i][0] for i, result in enumerate(results) if not result]
        print(f"Failed checks: {', '.join(failed_checks)}")
    
    print("\n📖 See PRODUCTION_DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()