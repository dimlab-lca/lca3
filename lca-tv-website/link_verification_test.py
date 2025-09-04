#!/usr/bin/python3.9
"""
LCA TV Link Verification Test
Tests all navigation links to ensure they work correctly with /lca subdirectory
"""

import requests
import json
from urllib.parse import urljoin

# Base URL for testing
BASE_URL = "https://edifice.bf/lca"

# Test URLs and expected status codes
TEST_URLS = {
    # Main pages
    "/": 200,
    "/videos": 200,
    "/live": 200,
    "/journal": 200,
    "/emissions": 200,
    "/publicite": 200,
    "/about": 200,
    "/contact": 200,
    
    # Authentication
    "/login": 200,
    "/logout": 302,  # Should redirect
    
    # API endpoints
    "/api/videos": 200,
    "/api/live-status": 200,
    "/api/playlists": 200,
    "/api/public/breaking-news": 200,
    "/api/public/flash-news": 200,
    
    # Utility endpoints
    "/health": 200,
    "/debug": 200,
    "/debug/youtube": 200,
    
    # Static files (examples)
    "/static/css/style.css": [200, 404],  # May not exist
    "/static/js/app.js": [200, 404],      # May not exist
    "/static/images/logo.png": [200, 404], # May not exist
}

def test_url(url, expected_status):
    """Test a single URL and return results"""
    full_url = urljoin(BASE_URL, url)
    
    try:
        response = requests.get(full_url, timeout=10, allow_redirects=False)
        
        # Check if status code matches expected
        if isinstance(expected_status, list):
            status_ok = response.status_code in expected_status
        else:
            status_ok = response.status_code == expected_status
        
        # Check if response contains /lca in redirects or content
        redirect_location = response.headers.get('Location', '')
        if redirect_location and not redirect_location.startswith('/lca') and not redirect_location.startswith('http'):
            redirect_issue = f"Redirect to {redirect_location} doesn't include /lca"
        else:
            redirect_issue = None
        
        return {
            'url': full_url,
            'status_code': response.status_code,
            'expected': expected_status,
            'success': status_ok,
            'redirect_location': redirect_location,
            'redirect_issue': redirect_issue,
            'content_length': len(response.content),
            'content_type': response.headers.get('Content-Type', ''),
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'url': full_url,
            'status_code': None,
            'expected': expected_status,
            'success': False,
            'error': str(e),
            'redirect_location': None,
            'redirect_issue': None,
            'content_length': 0,
            'content_type': '',
        }

def test_navigation_links():
    """Test all navigation links"""
    print("🧪 Testing LCA TV Navigation Links")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    results = []
    total_tests = len(TEST_URLS)
    passed_tests = 0
    
    for url, expected_status in TEST_URLS.items():
        result = test_url(url, expected_status)
        results.append(result)
        
        # Print result
        status_icon = "✅" if result['success'] else "❌"
        status_code = result['status_code'] or "ERROR"
        
        print(f"{status_icon} {url:<30} → {status_code} (expected: {expected_status})")
        
        if result['redirect_issue']:
            print(f"   ⚠️  {result['redirect_issue']}")
        
        if result.get('error'):
            print(f"   ❌ Error: {result['error']}")
        
        if result['success']:
            passed_tests += 1
    
    print("=" * 60)
    print(f"📊 Results: {passed_tests}/{total_tests} tests passed")
    
    # Detailed analysis
    failed_tests = [r for r in results if not r['success']]
    if failed_tests:
        print("\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   • {test['url']} - Status: {test['status_code']}, Expected: {test['expected']}")
            if test.get('error'):
                print(f"     Error: {test['error']}")
    
    redirect_issues = [r for r in results if r['redirect_issue']]
    if redirect_issues:
        print("\n⚠️  Redirect Issues:")
        for test in redirect_issues:
            print(f"   • {test['url']} - {test['redirect_issue']}")
    
    return results

def test_specific_navigation():
    """Test specific navigation scenarios"""
    print("\n🔍 Testing Specific Navigation Scenarios")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Home page loads',
            'url': '/',
            'check': lambda r: r.status_code == 200 and 'LCA TV' in r.text
        },
        {
            'name': 'Login page accessible',
            'url': '/login',
            'check': lambda r: r.status_code == 200 and 'connexion' in r.text.lower()
        },
        {
            'name': 'API returns JSON',
            'url': '/api/videos',
            'check': lambda r: r.status_code == 200 and 'application/json' in r.headers.get('Content-Type', '')
        },
        {
            'name': 'Health check works',
            'url': '/health',
            'check': lambda r: r.status_code == 200 and 'healthy' in r.text
        }
    ]
    
    for scenario in scenarios:
        try:
            full_url = urljoin(BASE_URL, scenario['url'])
            response = requests.get(full_url, timeout=10)
            
            if scenario['check'](response):
                print(f"✅ {scenario['name']}")
            else:
                print(f"❌ {scenario['name']} - Check failed")
                
        except Exception as e:
            print(f"❌ {scenario['name']} - Error: {e}")

def generate_report(results):
    """Generate a detailed report"""
    report = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'base_url': BASE_URL,
        'total_tests': len(results),
        'passed_tests': len([r for r in results if r['success']]),
        'failed_tests': len([r for r in results if not r['success']]),
        'results': results
    }
    
    # Save report to file
    with open('link_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: link_test_report.json")
    return report

def main():
    """Main test function"""
    print("🚀 LCA TV Link Verification Test")
    print(f"Testing: {BASE_URL}")
    print()
    
    # Test all navigation links
    results = test_navigation_links()
    
    # Test specific scenarios
    test_specific_navigation()
    
    # Generate report
    report = generate_report(results)
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    if report['passed_tests'] == report['total_tests']:
        print("🎉 ALL TESTS PASSED! Your navigation is working correctly.")
    else:
        print(f"⚠️  {report['failed_tests']} out of {report['total_tests']} tests failed.")
        print("Please check the failed tests and fix the issues.")
    
    print(f"\n🔗 Test your site manually at: {BASE_URL}")
    print("\n📝 Common fixes for failed tests:")
    print("   • Restart your application: touch ~/public_html/lca/tmp/restart.txt")
    print("   • Check file permissions: chmod 755 passenger_wsgi.py run.py")
    print("   • Verify .htaccess configuration")
    print("   • Check Python dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()