"""
Performance monitoring for Flask app
"""
import time
import functools
import logging
from flask import request, g

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_performance(f):
    """Decorator to monitor route performance"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            # Log performance metrics
            logger.info(f"Route: {request.endpoint} | Duration: {duration:.3f}s | Method: {request.method}")
            
            # Log slow requests (> 2 seconds)
            if duration > 2.0:
                logger.warning(f"SLOW REQUEST: {request.endpoint} took {duration:.3f}s")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f"ERROR in {request.endpoint} after {duration:.3f}s: {str(e)}")
            raise
    
    return decorated_function

class PerformanceTracker:
    """Track performance metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def record_request(self, endpoint, duration, status_code=200):
        """Record request metrics"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'max_time': 0,
                'min_time': float('inf'),
                'errors': 0
            }
        
        metric = self.metrics[endpoint]
        metric['count'] += 1
        metric['total_time'] += duration
        metric['avg_time'] = metric['total_time'] / metric['count']
        metric['max_time'] = max(metric['max_time'], duration)
        metric['min_time'] = min(metric['min_time'], duration)
        
        if status_code >= 400:
            metric['errors'] += 1
    
    def get_metrics(self):
        """Get performance metrics"""
        return self.metrics
    
    def get_slow_endpoints(self, threshold=2.0):
        """Get endpoints with average response time above threshold"""
        slow_endpoints = {}
        for endpoint, metric in self.metrics.items():
            if metric['avg_time'] > threshold:
                slow_endpoints[endpoint] = metric
        return slow_endpoints

# Global performance tracker
performance_tracker = PerformanceTracker()

def init_performance_monitoring(app):
    """Initialize performance monitoring for Flask app"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            performance_tracker.record_request(
                request.endpoint or 'unknown',
                duration,
                response.status_code
            )
        return response
    
    @app.route('/api/performance/metrics')
    def performance_metrics():
        """API endpoint to get performance metrics"""
        from flask import jsonify
        return jsonify(performance_tracker.get_metrics())
    
    @app.route('/api/performance/slow')
    def slow_endpoints():
        """API endpoint to get slow endpoints"""
        from flask import jsonify
        threshold = request.args.get('threshold', 2.0, type=float)
        return jsonify(performance_tracker.get_slow_endpoints(threshold))

# Cache performance metrics
class CacheMetrics:
    """Track cache performance"""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.total_requests = 0
    
    def record_hit(self):
        self.hits += 1
        self.total_requests += 1
    
    def record_miss(self):
        self.misses += 1
        self.total_requests += 1
    
    def get_hit_rate(self):
        if self.total_requests == 0:
            return 0
        return (self.hits / self.total_requests) * 100
    
    def get_stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': self.total_requests,
            'hit_rate': self.get_hit_rate()
        }

cache_metrics = CacheMetrics()