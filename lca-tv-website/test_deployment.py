#!/usr/bin/python3.9
"""
Test script to verify LCA TV deployment on PlanetHoster
Run this script to check if all components are working
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__} - OK")
    except ImportError as e:
        print(f"❌ Flask - FAILED: {e}")
        return False
    
    try:
        import requests
        print(f"✅ Requests {requests.__version__} - OK")
    except ImportError as e:
        print(f"❌ Requests - FAILED: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv - OK")
    except ImportError as e:
        print(f"❌ Python-dotenv - FAILED: {e}")
        return False
    
    return True

def test_app_import():
    """Test if the main app can be imported"""
    print("\n🧪 Testing app import...")
    
    try:
        from app import application
        print("✅ App import - OK")
        return True
    except ImportError as e:
        print(f"❌ App import - FAILED: {e}")
        return False

def test_wsgi_structure():
    """Test if WSGI structure is correct"""
    print("\n🧪 Testing WSGI structure...")
    
    try:
        from run import app
        print("✅ run.py - OK")
    except ImportError as e:
        print(f"❌ run.py - FAILED: {e}")
        return False
    
    try:
        import passenger_wsgi
        print("✅ passenger_wsgi.py - OK")
    except ImportError as e:
        print(f"❌ passenger_wsgi.py - FAILED: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files are present"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'run.py',
        'passenger_wsgi.py',
        'app.py',
        'config.py',
        'requirements.txt',
        '.htaccess'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    # Check directories
    required_dirs = ['templates', 'static']
    for dir in required_dirs:
        if os.path.exists(dir) and os.path.isdir(dir):
            print(f"✅ {dir}/ - OK")
        else:
            print(f"❌ {dir}/ - MISSING")
            missing_files.append(f"{dir}/")
    
    return len(missing_files) == 0

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n🧪 Testing environment configuration...")
    
    if not os.path.exists('.env'):
        print("⚠️ .env file not found - You need to create it on the server")
        print("📝 Required variables:")
        print("   - FLASK_SECRET_KEY")
        print("   - FLASK_CONFIG=production")
        print("   - ADMIN_PASSWORD")
        print("   - EDITOR_PASSWORD")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['FLASK_SECRET_KEY', 'FLASK_CONFIG']
        missing_vars = []
        
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var} - OK")
            else:
                print(f"❌ {var} - MISSING")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ .env file error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 LCA TV Deployment Test")
    print("=" * 50)
    
    print(f"📍 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("WSGI Structure", test_wsgi_structure),
        ("App Import", test_app_import),
        ("Environment", test_env_file)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your application is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Upload all files to public_html/lca/ on PlanetHoster")
        print("2. Create .env file with your configuration")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Configure Python App in cPanel")
        print("5. Test at: https://edifice.bf/lca/")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before deployment.")
        print("\n🔧 Common fixes:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Ensure all files are in the correct directory")
        print("- Create .env file with required variables")

if __name__ == "__main__":
    main()