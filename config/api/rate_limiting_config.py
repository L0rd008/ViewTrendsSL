"""
Rate Limiting Configuration Module

This module handles API rate limiting configuration for the ViewTrendsSL
application to prevent abuse and ensure fair usage of resources.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import Dict, List, Optional, Callable
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class RateLimitConfig:
    """
    Rate limiting configuration class for ViewTrendsSL API.
    
    This class manages rate limiting settings to protect the API from
    abuse while ensuring legitimate users have fair access to resources.
    """
    
    # Default rate limits for different endpoint types
    DEFAULT_LIMITS = {
        'global': '1000 per hour',
        'auth': '5 per minute',
        'prediction': '10 per minute',
        'analytics': '50 per hour',
        'data_collection': '100 per hour',
        'upload': '5 per minute'
    }
    
    # Rate limits for different user tiers
    USER_TIER_LIMITS = {
        'free': {
            'prediction': '5 per minute, 50 per hour',
            'analytics': '20 per hour',
            'global': '500 per hour'
        },
        'pro': {
            'prediction': '20 per minute, 200 per hour',
            'analytics': '100 per hour',
            'global': '2000 per hour'
        },
        'admin': {
            'prediction': '100 per minute',
            'analytics': '500 per hour',
            'global': '10000 per hour'
        }
    }
    
    # Storage configuration
    STORAGE_URI = os.getenv('RATE_LIMIT_STORAGE_URI', 'memory://')
    
    # Key function options
    KEY_FUNCTIONS = {
        'ip': get_remote_address,
        'user': lambda: getattr(g, 'current_user_id', get_remote_address()),
        'api_key': lambda: request.headers.get('X-API-Key', get_remote_address())
    }
    
    @classmethod
    def get_storage_uri(cls) -> str:
        """
        Get rate limiting storage URI.
        
        Returns:
            str: Storage URI for rate limiting backend
        """
        # Use Redis if available, otherwise fall back to memory
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            return redis_url
        
        return cls.STORAGE_URI
    
    @classmethod
    def get_key_func(cls, key_type: str = 'ip') -> Callable:
        """
        Get key function for rate limiting.
        
        Args:
            key_type: Type of key function ('ip', 'user', 'api_key')
            
        Returns:
            Callable: Key function for rate limiting
        """
        return cls.KEY_FUNCTIONS.get(key_type, cls.KEY_FUNCTIONS['ip'])
    
    @classmethod
    def get_limit_for_endpoint(cls, endpoint_type: str, user_tier: str = 'free') -> str:
        """
        Get rate limit for specific endpoint type and user tier.
        
        Args:
            endpoint_type: Type of endpoint (prediction, analytics, etc.)
            user_tier: User tier (free, pro, admin)
            
        Returns:
            str: Rate limit string
        """
        # Get tier-specific limits first
        tier_limits = cls.USER_TIER_LIMITS.get(user_tier, cls.USER_TIER_LIMITS['free'])
        
        # Return tier-specific limit if available, otherwise default
        return tier_limits.get(endpoint_type, cls.DEFAULT_LIMITS.get(endpoint_type, cls.DEFAULT_LIMITS['global']))
    
    @classmethod
    def configure_limiter(cls, app, key_func: str = 'ip') -> Limiter:
        """
        Configure Flask-Limiter for the application.
        
        Args:
            app: Flask application instance
            key_func: Key function type for rate limiting
            
        Returns:
            Limiter: Configured Flask-Limiter instance
        """
        limiter = Limiter(
            app,
            key_func=cls.get_key_func(key_func),
            storage_uri=cls.get_storage_uri(),
            default_limits=[cls.DEFAULT_LIMITS['global']],
            headers_enabled=True,
            retry_after='http-date'
        )
        
        # Add custom rate limit exceeded handler
        @limiter.request_filter
        def rate_limit_filter():
            """Filter requests that should bypass rate limiting."""
            # Skip rate limiting for health checks
            if request.endpoint == 'health':
                return True
            
            # Skip rate limiting for admin users in development
            if app.config.get('DEBUG') and hasattr(g, 'current_user') and g.current_user.is_admin:
                return True
            
            return False
        
        return limiter
    
    @classmethod
    def get_rate_limit_headers(cls) -> List[str]:
        """
        Get list of rate limit headers to include in responses.
        
        Returns:
            List[str]: List of rate limit header names
        """
        return [
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Reset',
            'Retry-After'
        ]


class EndpointRateLimits:
    """
    Predefined rate limits for different API endpoints.
    
    This class provides decorators and configurations for applying
    rate limits to specific endpoint types.
    """
    
    # Authentication endpoints
    AUTH_LIMITS = [
        '5 per minute',
        '20 per hour'
    ]
    
    # Prediction endpoints
    PREDICTION_LIMITS = {
        'free': ['5 per minute', '50 per hour'],
        'pro': ['20 per minute', '200 per hour'],
        'admin': ['100 per minute']
    }
    
    # Analytics endpoints
    ANALYTICS_LIMITS = {
        'free': ['20 per hour'],
        'pro': ['100 per hour'],
        'admin': ['500 per hour']
    }
    
    # Data collection endpoints
    DATA_COLLECTION_LIMITS = [
        '100 per hour',
        '1000 per day'
    ]
    
    # File upload endpoints
    UPLOAD_LIMITS = [
        '5 per minute',
        '50 per hour'
    ]
    
    @classmethod
    def get_auth_limits(cls) -> List[str]:
        """Get rate limits for authentication endpoints."""
        return cls.AUTH_LIMITS
    
    @classmethod
    def get_prediction_limits(cls, user_tier: str = 'free') -> List[str]:
        """Get rate limits for prediction endpoints based on user tier."""
        return cls.PREDICTION_LIMITS.get(user_tier, cls.PREDICTION_LIMITS['free'])
    
    @classmethod
    def get_analytics_limits(cls, user_tier: str = 'free') -> List[str]:
        """Get rate limits for analytics endpoints based on user tier."""
        return cls.ANALYTICS_LIMITS.get(user_tier, cls.ANALYTICS_LIMITS['free'])
    
    @classmethod
    def get_data_collection_limits(cls) -> List[str]:
        """Get rate limits for data collection endpoints."""
        return cls.DATA_COLLECTION_LIMITS
    
    @classmethod
    def get_upload_limits(cls) -> List[str]:
        """Get rate limits for file upload endpoints."""
        return cls.UPLOAD_LIMITS


def create_rate_limit_decorator(limiter: Limiter, endpoint_type: str):
    """
    Create a rate limit decorator for specific endpoint type.
    
    Args:
        limiter: Flask-Limiter instance
        endpoint_type: Type of endpoint
        
    Returns:
        Decorator function for rate limiting
    """
    def decorator(func):
        """Rate limit decorator."""
        # Get user tier from request context
        def get_user_tier():
            if hasattr(g, 'current_user'):
                return getattr(g.current_user, 'tier', 'free')
            return 'free'
        
        # Get appropriate limits based on endpoint type and user tier
        if endpoint_type == 'auth':
            limits = EndpointRateLimits.get_auth_limits()
        elif endpoint_type == 'prediction':
            limits = EndpointRateLimits.get_prediction_limits(get_user_tier())
        elif endpoint_type == 'analytics':
            limits = EndpointRateLimits.get_analytics_limits(get_user_tier())
        elif endpoint_type == 'data_collection':
            limits = EndpointRateLimits.get_data_collection_limits()
        elif endpoint_type == 'upload':
            limits = EndpointRateLimits.get_upload_limits()
        else:
            limits = [RateLimitConfig.DEFAULT_LIMITS['global']]
        
        # Apply rate limits
        for limit in limits:
            func = limiter.limit(limit)(func)
        
        return func
    
    return decorator


def setup_rate_limiting(app, limiter: Limiter) -> None:
    """
    Set up rate limiting error handlers and middleware.
    
    Args:
        app: Flask application instance
        limiter: Flask-Limiter instance
    """
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit exceeded errors."""
        return {
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.',
            'retry_after': error.retry_after
        }, 429
    
    @app.before_request
    def before_request():
        """Add rate limiting information to request context."""
        g.rate_limit_info = {
            'remaining': getattr(g, 'view_rate_limit', {}).get('remaining', 0),
            'limit': getattr(g, 'view_rate_limit', {}).get('limit', 0),
            'reset_time': getattr(g, 'view_rate_limit', {}).get('reset_time', 0)
        }
    
    @app.after_request
    def after_request(response):
        """Add rate limiting headers to response."""
        if hasattr(g, 'rate_limit_info'):
            response.headers['X-RateLimit-Remaining'] = str(g.rate_limit_info.get('remaining', 0))
            response.headers['X-RateLimit-Limit'] = str(g.rate_limit_info.get('limit', 0))
            response.headers['X-RateLimit-Reset'] = str(g.rate_limit_info.get('reset_time', 0))
        
        return response
