#!/usr/bin/env python3
"""
Performance testing script for LCA TV website
"""
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_endpoint(url, num_requests=5):
    """Test an endpoint multiple times and return performance metrics"""
    response_times = []
    
    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                response_times.append(end_time - start_time)
            else:
                print(f"Request {i+1} failed with status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    if response_times:
        return {
            'avg_time': statistics.mean(response_times),
            'min_time': min(response_times),
            'max_time': max(response_times),
            'median_time': statistics.median(response_times),
            'successful_requests': len(response_times),
            'total_requests': num_requests
        }
    else:
        return None

def test_concurrent_requests(url, num_concurrent=3):
    """Test concurrent requests to an endpoint"""
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(requests.get, url, timeout=30) for _ in range(num_concurrent)]
        
        successful = 0
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    successful += 1
            except Exception as e:
                print(f"Concurrent request failed: {e}")
    
    end_time = time.time()
    
    return {
        'total_time': end_time - start_time,
        'successful_requests': successful,
        'total_requests': num_concurrent
    }

def main():
    """Run performance tests"""
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/",
        "/videos",
        "/live",
        "/about",
        "/contact",
        "/emissions",
        "/journal",
        "/api/videos",
        "/api/dashboard-stats"
    ]
    
    print("🚀 LCA TV Performance Test Results")
    print("=" * 50)
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\n📊 Testing: {endpoint}")
        
        # Test sequential requests
        metrics = test_endpoint(url, num_requests=3)
        
        if metrics:
            print(f"   Average response time: {metrics['avg_time']:.3f}s")
            print(f"   Min/Max response time: {metrics['min_time']:.3f}s / {metrics['max_time']:.3f}s")
            print(f"   Success rate: {metrics['successful_requests']}/{metrics['total_requests']}")
            
            # Performance rating
            if metrics['avg_time'] < 1.0:
                rating = "🟢 Excellent"
            elif metrics['avg_time'] < 2.0:
                rating = "🟡 Good"
            elif metrics['avg_time'] < 5.0:
                rating = "🟠 Acceptable"
            else:
                rating = "🔴 Slow"
            
            print(f"   Performance: {rating}")
        else:
            print("   ❌ All requests failed")
    
    # Test concurrent requests on homepage
    print(f"\n🔄 Testing concurrent requests to homepage...")
    concurrent_metrics = test_concurrent_requests(base_url + "/", num_concurrent=5)
    
    if concurrent_metrics:
        print(f"   Total time for {concurrent_metrics['total_requests']} concurrent requests: {concurrent_metrics['total_time']:.3f}s")
        print(f"   Success rate: {concurrent_metrics['successful_requests']}/{concurrent_metrics['total_requests']}")
    
    # Test cache effectiveness
    print(f"\n💾 Testing cache effectiveness...")
    
    # First request (cache miss)
    start_time = time.time()
    response1 = requests.get(base_url + "/videos")
    first_request_time = time.time() - start_time
    
    # Second request (cache hit)
    start_time = time.time()
    response2 = requests.get(base_url + "/videos")
    second_request_time = time.time() - start_time
    
    if response1.status_code == 200 and response2.status_code == 200:
        improvement = ((first_request_time - second_request_time) / first_request_time) * 100
        print(f"   First request (cache miss): {first_request_time:.3f}s")
        print(f"   Second request (cache hit): {second_request_time:.3f}s")
        print(f"   Cache improvement: {improvement:.1f}%")
    
    print(f"\n✅ Performance test completed!")
    print(f"\n💡 Tips for better performance:")
    print(f"   - Static pages (about, contact, live) should be fastest")
    print(f"   - API endpoints should benefit from caching")
    print(f"   - Second requests should be faster due to caching")

if __name__ == "__main__":
    main()