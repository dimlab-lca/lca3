#!/usr/bin/env python3
"""
Backend API Tests for LCA TV Mobile App
Tests all backend endpoints with comprehensive validation
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'https://lcatv-mobile.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

# Test data as specified in the review request
TEST_USER_DATA = {
    "nom": "Jean",
    "prenom": "Dupont", 
    "email": "jean.dupont@test.bf",
    "telephone": "70123456",
    "password": "test123456",
    "confirm_password": "test123456",
    "accept_cgu": True,
    "newsletter": False
}

LOGIN_DATA = {
    "email": "jean.dupont@test.bf",
    "password": "test123456",
    "remember_me": False
}

class LCATVAPITester:
    def __init__(self):
        self.access_token = None
        self.user_id = None
        self.test_results = []
        
    def log_result(self, test_name, success, details="", response_data=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def test_root_endpoint(self):
        """Test GET / - Root endpoint"""
        try:
            response = requests.get(BACKEND_URL, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "LCA TV" in data["message"]:
                    self.log_result("Root Endpoint", True, f"Status: {response.status_code}, Message: {data.get('message')}")
                    return True
                else:
                    self.log_result("Root Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Root Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Root Endpoint", False, f"Connection error: {str(e)}")
            return False

    def test_user_registration(self):
        """Test POST /api/auth/register - User registration"""
        try:
            # First, try to clean up any existing user
            try:
                requests.delete(f"{API_BASE}/user/cleanup", json={"email": TEST_USER_DATA["email"]})
            except:
                pass
                
            response = requests.post(f"{API_BASE}/auth/register", json=TEST_USER_DATA, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "user" in data:
                    self.access_token = data["access_token"]
                    self.user_id = data["user"]["_id"]
                    user = data["user"]
                    
                    # Validate user data
                    if (user["nom"] == TEST_USER_DATA["nom"] and 
                        user["prenom"] == TEST_USER_DATA["prenom"] and
                        user["email"] == TEST_USER_DATA["email"] and
                        "points" in user):
                        self.log_result("User Registration", True, 
                                      f"User created with ID: {self.user_id}, Points: {user.get('points', 0)}")
                        return True
                    else:
                        self.log_result("User Registration", False, "Invalid user data returned", data)
                        return False
                else:
                    self.log_result("User Registration", False, "Missing access_token or user in response", data)
                    return False
            else:
                self.log_result("User Registration", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("User Registration", False, f"Request error: {str(e)}")
            return False

    def test_user_login(self):
        """Test POST /api/auth/login - User login"""
        try:
            response = requests.post(f"{API_BASE}/auth/login", json=LOGIN_DATA, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "user" in data:
                    # Update token if we got a new one
                    if not self.access_token:
                        self.access_token = data["access_token"]
                        self.user_id = data["user"]["_id"]
                    
                    user = data["user"]
                    self.log_result("User Login", True, 
                                  f"Login successful for user: {user['email']}, Last login updated")
                    return True
                else:
                    self.log_result("User Login", False, "Missing access_token or user in response", data)
                    return False
            else:
                self.log_result("User Login", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("User Login", False, f"Request error: {str(e)}")
            return False

    def test_user_profile(self):
        """Test GET /api/user/profile - User profile (requires auth)"""
        if not self.access_token:
            self.log_result("User Profile", False, "No access token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{API_BASE}/user/profile", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if ("_id" in data and "email" in data and "nom" in data and 
                    data["email"] == TEST_USER_DATA["email"]):
                    self.log_result("User Profile", True, 
                                  f"Profile retrieved for: {data['nom']} {data['prenom']}, Points: {data.get('points', 0)}")
                    return True
                else:
                    self.log_result("User Profile", False, "Invalid profile data", data)
                    return False
            elif response.status_code == 401:
                self.log_result("User Profile", False, "Authentication failed - Invalid token")
                return False
            else:
                self.log_result("User Profile", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("User Profile", False, f"Request error: {str(e)}")
            return False

    def test_videos_list(self):
        """Test GET /api/videos - Video list"""
        try:
            response = requests.get(f"{API_BASE}/videos", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "videos" in data and isinstance(data["videos"], list):
                    videos = data["videos"]
                    if len(videos) > 0:
                        # Validate video structure
                        video = videos[0]
                        required_fields = ["id", "title", "description", "thumbnail", "category"]
                        if all(field in video for field in required_fields):
                            self.log_result("Videos List", True, 
                                          f"Retrieved {len(videos)} videos, Sample: {video['title']}")
                            return True
                        else:
                            self.log_result("Videos List", False, "Invalid video structure", video)
                            return False
                    else:
                        self.log_result("Videos List", False, "No videos returned")
                        return False
                else:
                    self.log_result("Videos List", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Videos List", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Videos List", False, f"Request error: {str(e)}")
            return False

    def test_featured_videos(self):
        """Test GET /api/videos/featured - Featured videos"""
        try:
            response = requests.get(f"{API_BASE}/videos/featured", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "videos" in data and isinstance(data["videos"], list):
                    videos = data["videos"]
                    self.log_result("Featured Videos", True, 
                                  f"Retrieved {len(videos)} featured videos")
                    return True
                else:
                    self.log_result("Featured Videos", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Featured Videos", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Featured Videos", False, f"Request error: {str(e)}")
            return False

    def test_news_list(self):
        """Test GET /api/news - News list"""
        try:
            response = requests.get(f"{API_BASE}/news", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "news" in data and isinstance(data["news"], list):
                    news = data["news"]
                    if len(news) > 0:
                        # Validate news structure
                        article = news[0]
                        required_fields = ["_id", "title", "content", "category", "published_at"]
                        if all(field in article for field in required_fields):
                            self.log_result("News List", True, 
                                          f"Retrieved {len(news)} articles, Sample: {article['title']}")
                            return True
                        else:
                            self.log_result("News List", False, "Invalid news structure", article)
                            return False
                    else:
                        self.log_result("News List", True, "No news articles (empty collection)")
                        return True
                else:
                    self.log_result("News List", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("News List", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("News List", False, f"Request error: {str(e)}")
            return False

    def test_categories(self):
        """Test GET /api/categories - Video categories"""
        try:
            response = requests.get(f"{API_BASE}/categories", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "categories" in data and isinstance(data["categories"], list):
                    categories = data["categories"]
                    if len(categories) > 0:
                        # Validate category structure
                        category = categories[0]
                        required_fields = ["id", "name"]
                        if all(field in category for field in required_fields):
                            self.log_result("Categories", True, 
                                          f"Retrieved {len(categories)} categories")
                            return True
                        else:
                            self.log_result("Categories", False, "Invalid category structure", category)
                            return False
                    else:
                        self.log_result("Categories", False, "No categories returned")
                        return False
                else:
                    self.log_result("Categories", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Categories", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Categories", False, f"Request error: {str(e)}")
            return False

    def test_live_status(self):
        """Test GET /api/live/status - Live stream status"""
        try:
            response = requests.get(f"{API_BASE}/live/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["is_live", "stream_url", "title"]
                if all(field in data for field in required_fields):
                    self.log_result("Live Status", True, 
                                  f"Live status: {data['is_live']}, Title: {data['title']}")
                    return True
                else:
                    self.log_result("Live Status", False, "Invalid live status structure", data)
                    return False
            else:
                self.log_result("Live Status", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Live Status", False, f"Request error: {str(e)}")
            return False

    def test_add_favorite(self):
        """Test POST /api/user/favorites/{video_id} - Add favorite (requires auth)"""
        if not self.access_token:
            self.log_result("Add Favorite", False, "No access token available")
            return False
            
        try:
            # First get a video ID to use
            videos_response = requests.get(f"{API_BASE}/videos", timeout=10)
            if videos_response.status_code != 200:
                self.log_result("Add Favorite", False, "Could not get videos for testing")
                return False
                
            videos = videos_response.json()["videos"]
            if not videos:
                self.log_result("Add Favorite", False, "No videos available for testing")
                return False
                
            video_id = videos[0]["id"]
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.post(f"{API_BASE}/user/favorites/{video_id}", 
                                   headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "points_earned" in data:
                    self.log_result("Add Favorite", True, 
                                  f"Added video {video_id} to favorites, Points earned: {data['points_earned']}")
                    return True
                else:
                    self.log_result("Add Favorite", False, "Invalid response format", data)
                    return False
            elif response.status_code == 400:
                # Might already be in favorites
                self.log_result("Add Favorite", True, "Video already in favorites (expected behavior)")
                return True
            elif response.status_code == 401:
                self.log_result("Add Favorite", False, "Authentication failed")
                return False
            else:
                self.log_result("Add Favorite", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Add Favorite", False, f"Request error: {str(e)}")
            return False

    def test_get_favorites(self):
        """Test GET /api/user/favorites - User favorites list (requires auth)"""
        if not self.access_token:
            self.log_result("Get Favorites", False, "No access token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{API_BASE}/user/favorites", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "favorites" in data and isinstance(data["favorites"], list):
                    favorites = data["favorites"]
                    self.log_result("Get Favorites", True, 
                                  f"Retrieved {len(favorites)} favorite videos")
                    return True
                else:
                    self.log_result("Get Favorites", False, "Invalid response format", data)
                    return False
            elif response.status_code == 401:
                self.log_result("Get Favorites", False, "Authentication failed")
                return False
            else:
                self.log_result("Get Favorites", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Get Favorites", False, f"Request error: {str(e)}")
            return False

    def test_error_handling(self):
        """Test error handling scenarios"""
        print("Testing Error Handling Scenarios:")
        
        # Test 401 - Unauthorized access
        try:
            response = requests.get(f"{API_BASE}/user/profile", timeout=10)
            if response.status_code == 401:
                self.log_result("401 Error Handling", True, "Correctly returns 401 for unauthorized access")
            else:
                self.log_result("401 Error Handling", False, f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_result("401 Error Handling", False, f"Request error: {str(e)}")
        
        # Test 404 - Not found
        try:
            response = requests.get(f"{API_BASE}/videos/nonexistent-video-id", timeout=10)
            if response.status_code == 404:
                self.log_result("404 Error Handling", True, "Correctly returns 404 for non-existent video")
            else:
                self.log_result("404 Error Handling", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("404 Error Handling", False, f"Request error: {str(e)}")
        
        # Test 400 - Bad request (invalid registration data)
        try:
            invalid_data = {"email": "invalid-email", "password": "123"}
            response = requests.post(f"{API_BASE}/auth/register", json=invalid_data, timeout=10)
            if response.status_code == 400 or response.status_code == 422:
                self.log_result("400 Error Handling", True, "Correctly validates registration data")
            else:
                self.log_result("400 Error Handling", False, f"Expected 400/422, got {response.status_code}")
        except Exception as e:
            self.log_result("400 Error Handling", False, f"Request error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 60)
        print("LCA TV Mobile API - Backend Testing")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print("=" * 60)
        print()
        
        # Run tests in order
        tests = [
            self.test_root_endpoint,
            self.test_user_registration,
            self.test_user_login,
            self.test_user_profile,
            self.test_videos_list,
            self.test_featured_videos,
            self.test_news_list,
            self.test_categories,
            self.test_live_status,
            self.test_add_favorite,
            self.test_get_favorites,
            self.test_error_handling
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print("=" * 60)
        
        return passed, total, self.test_results

if __name__ == "__main__":
    tester = LCATVAPITester()
    passed, total, results = tester.run_all_tests()
    
    # Save detailed results
    with open("/app/test_results_detailed.json", "w") as f:
        json.dump({
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": (passed/total)*100
            },
            "results": results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: /app/test_results_detailed.json")