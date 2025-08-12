"""
Rate Limiting Middleware

This module provides rate limiting middleware for the ViewTrendsSL application
to prevent abuse and ensure fair usage of API endpoints.

Author: ViewTrendsSL Team
Date: 2025
"""

from functools import wraps
from flask import request, jsonify, g
import time
import logging
from collections import defaultdict, deque
from threading import Lock

logger = logging.getLogger(__name__)

# In-memory rate limiting storage (use Redis in production)
rate_limit_storage = defaultdict(lambda: defaultdict(deque))
storage_lock = Lock()


def init_rate_limiting(app):
    """
    Initialize rate limiting middleware for the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.before_request
    def check_rate_limits():
        """Check rate limits before processing request."""
        # Skip rate limiting for health check
        if request.endpoint in ['health_check', 'api_info']:
            return
        
        # Get client identifier
        client_id = get_client_identifier()
        
        # Store client ID for use in decorators
        g.client_id = client_id


def rate_limit(limit_string):
    """
    Decorator to apply rate limiting to a route.
    
    Args:
        limit_string: Rate limit in format "requests/period" (e.g., "10/minute", "100/hour")
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Parse limit string
            try:
                requests, period = limit_string.split('/')
                max_requests = int(requests)
                
                # Convert period to seconds
                period_seconds = {
                    'second': 1,
                    'minute': 60,
                    'hour': 3600,
                    'day': 86400
                }.get(period, 60)  # Default to minute
                
            except (ValueError, KeyError):
                logger.error(f"Invalid rate limit format: {limit_string}")
                return f(*args, **kwargs)  # Continue without rate limiting
            
            # Get client identifier
            client_id = getattr(g, 'client_id', get_client_identifier())
            
            # Check rate limit
            if is_rate_limited(client_id, f.__name__, max_requests, period_seconds):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {max_requests} requests per {period} allowed',
                    'retry_after': get_retry_after(client_id, f.__name__, period_seconds)
                }), 429
            
            # Record the request
            record_request(client_id, f.__name__, period_seconds)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_client_identifier():
    """
    Get unique identifier for the client making the request.
    
    Returns:
        str: Client identifier
    """
    # Try to get user ID from JWT token
    if hasattr(g, 'current_user') and g.current_user:
        return f"user:{g.current_user.id}"
    
    # Fall back to IP address
    return f"ip:{request.remote_addr}"


def is_rate_limited(client_id, endpoint, max_requests, period_seconds):
    """
    Check if client has exceeded rate limit for endpoint.
    
    Args:
        client_id: Client identifier
        endpoint: Endpoint name
        max_requests: Maximum requests allowed
        period_seconds: Time period in seconds
        
    Returns:
        bool: True if rate limited, False otherwise
    """
    with storage_lock:
        current_time = time.time()
        requests = rate_limit_storage[client_id][endpoint]
        
        # Remove old requests outside the time window
        while requests and requests[0] <= current_time - period_seconds:
            requests.popleft()
        
        # Check if limit exceeded
        return len(requests) >= max_requests


def record_request(client_id, endpoint, period_seconds):
    """
    Record a request for rate limiting purposes.
    
    Args:
        client_id: Client identifier
        endpoint: Endpoint name
        period_seconds: Time period in seconds
    """
    with storage_lock:
        current_time = time.time()
        requests = rate_limit_storage[client_id][endpoint]
        
        # Add current request
        requests.append(current_time)
        
        # Clean up old requests to prevent memory bloat
        while requests and requests[0] <= current_time - period_seconds:
            requests.popleft()


def get_retry_after(client_id, endpoint, period_seconds):
    """
    Get the time in seconds after which the client can retry.
    
    Args:
        client_id: Client identifier
        endpoint: Endpoint name
        period_seconds: Time period in seconds
        
    Returns:
        int: Seconds until retry is allowed
    """
    with storage_lock:
        current_time = time.time()
        requests = rate_limit_storage[client_id][endpoint]
        
        if requests:
            oldest_request = requests[0]
            retry_after = int(oldest_request + period_seconds - current_time)
            return max(0, retry_after)
        
        return 0


def reset_rate_limits(client_id=None, endpoint=None):
    """
    Reset rate limits for debugging or administrative purposes.
    
    Args:
        client_id: Specific client ID to reset (optional)
        endpoint: Specific endpoint to reset (optional)
    """
    with storage_lock:
        if client_id and endpoint:
            # Reset specific client and endpoint
            if client_id in rate_limit_storage:
                rate_limit_storage[client_id][endpoint].clear()
        elif client_id:
            # Reset all endpoints for specific client
            if client_id in rate_limit_storage:
                rate_limit_storage[client_id].clear()
        else:
            # Reset all rate limits
            rate_limit_storage.clear()
    
    logger.info(f"Rate limits reset - Client: {client_id}, Endpoint: {endpoint}")


def get_rate_limit_status(client_id, endpoint, max_requests, period_seconds):
    """
    Get current rate limit status for a client and endpoint.
    
    Args:
        client_id: Client identifier
        endpoint: Endpoint name
        max_requests: Maximum requests allowed
        period_seconds: Time period in seconds
        
    Returns:
        dict: Rate limit status information
    """
    with storage_lock:
        current_time = time.time()
        requests = rate_limit_storage[client_id][endpoint]
        
        # Remove old requests
        while requests and requests[0] <= current_time - period_seconds:
            requests.popleft()
        
        current_requests = len(requests)
        remaining_requests = max(0, max_requests - current_requests)
        
        # Calculate reset time
        reset_time = None
        if requests:
            reset_time = int(requests[0] + period_seconds)
        
        return {
            'limit': max_requests,
            'remaining': remaining_requests,
            'used': current_requests,
            'reset_time': reset_time,
            'period_seconds': period_seconds
        }


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


def adaptive_rate_limit(base_limit, user_tier='free'):
    """
    Apply adaptive rate limiting based on user tier.
    
    Args:
        base_limit: Base rate limit string
        user_tier: User tier (free, pro, enterprise)
        
    Returns:
        Decorator function
    """
    # Multipliers for different user tiers
    tier_multipliers = {
        'free': 1.0,
        'pro': 3.0,
        'enterprise': 10.0
    }
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get user tier from current user
            current_tier = 'free'
            if hasattr(g, 'current_user') and g.current_user:
                current_tier = getattr(g.current_user, 'tier', 'free')
            
            # Calculate adjusted limit
            try:
                requests, period = base_limit.split('/')
                base_requests = int(requests)
                multiplier = tier_multipliers.get(current_tier, 1.0)
                adjusted_requests = int(base_requests * multiplier)
                adjusted_limit = f"{adjusted_requests}/{period}"
                
                # Apply rate limiting with adjusted limit
                return rate_limit(adjusted_limit)(f)(*args, **kwargs)
                
            except (ValueError, KeyError):
                # Fall back to base limit if parsing fails
                return rate_limit(base_limit)(f)(*args, **kwargs)
        
        return decorated_function
    return decorator


def global_rate_limit(limit_string):
    """
    Apply global rate limiting across all users.
    
    Args:
        limit_string: Rate limit string
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use a global identifier
            global_client_id = "global"
            
            # Parse limit string
            try:
                requests, period = limit_string.split('/')
                max_requests = int(requests)
                period_seconds = {
                    'second': 1,
                    'minute': 60,
                    'hour': 3600,
                    'day': 86400
                }.get(period, 60)
                
            except (ValueError, KeyError):
                logger.error(f"Invalid global rate limit format: {limit_string}")
                return f(*args, **kwargs)
            
            # Check global rate limit
            if is_rate_limited(global_client_id, f.__name__, max_requests, period_seconds):
                return jsonify({
                    'error': 'Global rate limit exceeded',
                    'message': 'Service is temporarily overloaded. Please try again later.',
                    'retry_after': get_retry_after(global_client_id, f.__name__, period_seconds)
                }), 503
            
            # Record the request
            record_request(global_client_id, f.__name__, period_seconds)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
