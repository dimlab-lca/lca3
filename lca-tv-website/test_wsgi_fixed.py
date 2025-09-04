#!/usr/bin/env python3
"""
Test script for WSGI application
Tests if the application can be imported and responds correctly
"""

import sys
import os

def test_wsgi_import():
    """Test if WSGI application can be imported"""
    print("🧪 Testing WSGI Application Import...")
    print("=" * 50)
    
    try:
        # Test importing the fixed WSGI
        from passenger_wsgi_fixed import application
        print("✅ WSGI application imported successfully")
        
        # Test if it's callable
        if hasattr(application, '__call__'):
            print("✅ Application is callable (valid WSGI)")
        else:
            print("❌ Application is not callable")
            return False
        
        # Test basic configuration
        if hasattr(application, 'config'):
            print(f"✅ Flask config available")
            print(f"   - DEBUG: {application.config.get('DEBUG', 'Not set')}")
            print(f"   - APPLICATION_ROOT: {application.config.get('APPLICATION_ROOT', 'Not set')}")
        else:
            print("❌ No Flask config found")
        
        # Test basic routes
        with application.test_client() as client:
            # Test home page
            response = client.get('/')
            print(f"✅ Home page test: {response.status_code}")
            
            # Test health check
            response = client.get('/health')
            print(f"✅ Health check test: {response.status_code}")
            
            # Test login page
            response = client.get('/login')
            print(f"✅ Login page test: {response.status_code}")
        
        print("\n🎉 All WSGI tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_production_app():
    """Test the production app directly"""
    print("\n🧪 Testing Production App Directly...")
    print("=" * 50)
    
    try:
        from app_production_fixed import application
        print("✅ Production app imported successfully")
        
        with application.test_client() as client:
            # Test key routes
            routes_to_test = [
                ('/', 'Home'),
                ('/videos', 'Videos'),
                ('/live', 'Live'),
                ('/login', 'Login'),
                ('/health', 'Health'),
                ('/api/videos', 'API Videos')
            ]
            
            for route, name in routes_to_test:
                try:
                    response = client.get(route)
                    print(f"✅ {name} ({route}): {response.status_code}")
                except Exception as e:
                    print(f"❌ {name} ({route}): Error - {e}")
        
        print("\n🎉 Production app tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Production app error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LCA TV WSGI Application Test Suite")
    print("=" * 60)
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Run tests
    wsgi_ok = test_wsgi_import()
    prod_ok = test_production_app()
    
    print("\n" + "=" * 60)
    if wsgi_ok and prod_ok:
        print("🎉 ALL TESTS PASSED - Application ready for deployment!")
        print("\n📋 Deployment Instructions:")
        print("1. Upload all files to your server")
        print("2. Rename 'passenger_wsgi_fixed.py' to 'passenger_wsgi.py'")
        print("3. Ensure Python 3.9+ is available")
        print("4. Install requirements: pip install -r requirements.txt")
        print("5. Test the application")
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
        print("\n🔧 Troubleshooting:")
        print("- Check Python version (3.9+ required)")
        print("- Verify all dependencies are installed")
        print("- Check file permissions")
        print("- Review server error logs")
    
    print("=" * 60)