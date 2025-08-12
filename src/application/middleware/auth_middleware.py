"""
Authentication Middleware

This module provides authentication middleware for the ViewTrendsSL application,
including JWT token validation and user authentication checks.

Author: ViewTrendsSL Team
Date: 2025
"""

from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import logging

from src.business.services.user.user_service import UserService

logger = logging.getLogger(__name__)
user_service = UserService()


def init_auth_middleware(app):
    """
    Initialize authentication middleware for the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.before_request
    def load_user():
        """Load user information for authenticated requests."""
        # Skip for health check and public endpoints
        if request.endpoint in ['health_check', 'api_info']:
            return
        
        # Skip for auth endpoints (except profile-related)
        if request.blueprint == 'auth' and request.endpoint not in [
            'auth.get_profile', 'auth.update_profile', 'auth.change_password'
        ]:
            return
        
        # Try to get user from JWT token
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            
            if user_id:
                user = user_service.get_user_by_id(user_id)
                if user and user.is_active:
                    g.current_user = user
                else:
                    g.current_user = None
            else:
                g.current_user = None
                
        except Exception as e:
            logger.debug(f"Auth middleware error: {str(e)}")
            g.current_user = None


def require_auth(f):
    """
    Decorator to require authentication for a route.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user is None:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_active_user(f):
    """
    Decorator to require an active user for a route.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user is None:
            return jsonify({'error': 'Authentication required'}), 401
        
        if not g.current_user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
            
        return f(*args, **kwargs)
    return decorated_function


def optional_auth(f):
    """
    Decorator for optional authentication (user may or may not be logged in).
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # User information is already loaded in before_request
        return f(*args, **kwargs)
    return decorated_function


def check_token_freshness(f):
    """
    Decorator to check if the JWT token is fresh (for sensitive operations).
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(fresh=True)
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Fresh token required: {str(e)}")
            return jsonify({'error': 'Fresh token required for this operation'}), 401
    return decorated_function


def check_user_permissions(required_permissions):
    """
    Decorator to check if user has required permissions.
    
    Args:
        required_permissions: List of required permissions
        
    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'current_user') or g.current_user is None:
                return jsonify({'error': 'Authentication required'}), 401
            
            # For now, all authenticated users have basic permissions
            # This can be extended with role-based access control
            user_permissions = ['basic_access']
            
            if not any(perm in user_permissions for perm in required_permissions):
                return jsonify({'error': 'Insufficient permissions'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_api_key(f):
    """
    Decorator to validate API key for external API access.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Validate API key (implement your validation logic)
        # For now, just check if it exists
        if not _validate_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401
            
        return f(*args, **kwargs)
    return decorated_function


def _validate_api_key(api_key):
    """
    Validate API key.
    
    Args:
        api_key: API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Implement your API key validation logic here
    # This could involve checking against a database or external service
    return len(api_key) >= 32  # Simple validation for now


def log_request_info(f):
    """
    Decorator to log request information for debugging.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = getattr(g, 'current_user', {}).get('id', 'anonymous') if hasattr(g, 'current_user') and g.current_user else 'anonymous'
        
        logger.info(f"Request: {request.method} {request.path} - User: {user_id} - IP: {request.remote_addr}")
        
        return f(*args, **kwargs)
    return decorated_function
