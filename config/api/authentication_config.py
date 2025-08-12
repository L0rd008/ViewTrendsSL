"""
Authentication Configuration Module

This module handles authentication and authorization configuration
for the ViewTrendsSL API, including JWT tokens, user sessions,
and security settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from datetime import timedelta
from typing import Dict, List, Optional, Any
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class AuthenticationConfig:
    """
    Authentication configuration class for ViewTrendsSL API.
    
    This class manages authentication settings including JWT tokens,
    password hashing, session management, and security policies.
    """
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'dev-jwt-secret'))
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_HOURS', '1')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_DAYS', '30')))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Password Configuration
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', '8'))
    PASSWORD_REQUIRE_UPPERCASE = os.getenv('PASSWORD_REQUIRE_UPPERCASE', 'True').lower() == 'true'
    PASSWORD_REQUIRE_LOWERCASE = os.getenv('PASSWORD_REQUIRE_LOWERCASE', 'True').lower() == 'true'
    PASSWORD_REQUIRE_NUMBERS = os.getenv('PASSWORD_REQUIRE_NUMBERS', 'True').lower() == 'true'
    PASSWORD_REQUIRE_SPECIAL = os.getenv('PASSWORD_REQUIRE_SPECIAL', 'False').lower() == 'true'
    PASSWORD_HASH_METHOD = 'pbkdf2:sha256'
    PASSWORD_SALT_LENGTH = 8
    
    # Session Configuration
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'viewtrendssl:'
    SESSION_COOKIE_NAME = 'viewtrendssl_session'
    SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN')
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('FORCE_HTTPS', 'False').lower() == 'true'
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Key Configuration
    API_KEY_LENGTH = 32
    API_KEY_PREFIX = 'vtsl_'
    API_KEY_HEADER = 'X-API-Key'
    API_KEY_EXPIRES_DAYS = int(os.getenv('API_KEY_EXPIRES_DAYS', '365'))
    
    # User Roles and Permissions
    USER_ROLES = {
        'user': {
            'name': 'User',
            'permissions': ['predict', 'view_analytics', 'manage_profile']
        },
        'pro': {
            'name': 'Pro User',
            'permissions': ['predict', 'view_analytics', 'manage_profile', 'export_data', 'advanced_analytics']
        },
        'admin': {
            'name': 'Administrator',
            'permissions': ['*']  # All permissions
        }
    }
    
    # OAuth Configuration (for future implementation)
    OAUTH_PROVIDERS = {
        'google': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'server_metadata_url': 'https://accounts.google.com/.well-known/openid_configuration',
            'client_kwargs': {
                'scope': 'openid email profile'
            }
        }
    }
    
    # Security Configuration
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', '12'))
    LOGIN_ATTEMPTS_LIMIT = int(os.getenv('LOGIN_ATTEMPTS_LIMIT', '5'))
    LOGIN_LOCKOUT_DURATION = timedelta(minutes=int(os.getenv('LOGIN_LOCKOUT_MINUTES', '15')))
    
    @classmethod
    def validate_password(cls, password: str) -> Dict[str, Any]:
        """
        Validate password against security requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            Dict[str, Any]: Validation result with is_valid and errors
        """
        errors = []
        
        # Check minimum length
        if len(password) < cls.PASSWORD_MIN_LENGTH:
            errors.append(f'Password must be at least {cls.PASSWORD_MIN_LENGTH} characters long')
        
        # Check uppercase requirement
        if cls.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            errors.append('Password must contain at least one uppercase letter')
        
        # Check lowercase requirement
        if cls.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            errors.append('Password must contain at least one lowercase letter')
        
        # Check numbers requirement
        if cls.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            errors.append('Password must contain at least one number')
        
        # Check special characters requirement
        if cls.PASSWORD_REQUIRE_SPECIAL:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                errors.append('Password must contain at least one special character')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash password using configured method.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        return generate_password_hash(
            password,
            method=cls.PASSWORD_HASH_METHOD,
            salt_length=cls.PASSWORD_SALT_LENGTH
        )
    
    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
            
        Returns:
            bool: True if password matches hash
        """
        return check_password_hash(password_hash, password)
    
    @classmethod
    def generate_jwt_token(cls, user_id: str, token_type: str = 'access', **kwargs) -> str:
        """
        Generate JWT token for user.
        
        Args:
            user_id: User identifier
            token_type: Type of token ('access' or 'refresh')
            **kwargs: Additional claims to include in token
            
        Returns:
            str: JWT token
        """
        import time
        
        # Set expiration based on token type
        if token_type == 'refresh':
            expires_delta = cls.JWT_REFRESH_TOKEN_EXPIRES
        else:
            expires_delta = cls.JWT_ACCESS_TOKEN_EXPIRES
        
        # Create payload
        payload = {
            'user_id': user_id,
            'token_type': token_type,
            'iat': int(time.time()),
            'exp': int(time.time() + expires_delta.total_seconds()),
            **kwargs
        }
        
        # Generate token
        return jwt.encode(payload, cls.JWT_SECRET_KEY, algorithm=cls.JWT_ALGORITHM)
    
    @classmethod
    def decode_jwt_token(cls, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Dict[str, Any]: Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        return jwt.decode(token, cls.JWT_SECRET_KEY, algorithms=[cls.JWT_ALGORITHM])
    
    @classmethod
    def get_user_permissions(cls, role: str) -> List[str]:
        """
        Get permissions for user role.
        
        Args:
            role: User role
            
        Returns:
            List[str]: List of permissions
        """
        role_config = cls.USER_ROLES.get(role, cls.USER_ROLES['user'])
        return role_config['permissions']
    
    @classmethod
    def has_permission(cls, user_role: str, permission: str) -> bool:
        """
        Check if user role has specific permission.
        
        Args:
            user_role: User role
            permission: Permission to check
            
        Returns:
            bool: True if user has permission
        """
        permissions = cls.get_user_permissions(user_role)
        return '*' in permissions or permission in permissions
    
    @classmethod
    def generate_api_key(cls) -> str:
        """
        Generate API key for user.
        
        Returns:
            str: Generated API key
        """
        import secrets
        
        # Generate random key
        key = secrets.token_urlsafe(cls.API_KEY_LENGTH)
        
        # Add prefix
        return f"{cls.API_KEY_PREFIX}{key}"
    
    @classmethod
    def validate_api_key_format(cls, api_key: str) -> bool:
        """
        Validate API key format.
        
        Args:
            api_key: API key to validate
            
        Returns:
            bool: True if format is valid
        """
        return (
            api_key.startswith(cls.API_KEY_PREFIX) and
            len(api_key) == len(cls.API_KEY_PREFIX) + cls.API_KEY_LENGTH
        )


class JWTManager:
    """
    JWT token management utilities.
    
    This class provides utilities for managing JWT tokens including
    blacklisting, validation, and token refresh.
    """
    
    def __init__(self):
        """Initialize JWT manager."""
        self.blacklisted_tokens = set()  # In production, use Redis or database
    
    def blacklist_token(self, token: str) -> None:
        """
        Add token to blacklist.
        
        Args:
            token: JWT token to blacklist
        """
        self.blacklisted_tokens.add(token)
    
    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted.
        
        Args:
            token: JWT token to check
            
        Returns:
            bool: True if token is blacklisted
        """
        return token in self.blacklisted_tokens
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            Dict[str, Any]: Validation result
        """
        try:
            # Check if token is blacklisted
            if self.is_token_blacklisted(token):
                return {'valid': False, 'error': 'Token is blacklisted'}
            
            # Decode token
            payload = AuthenticationConfig.decode_jwt_token(token)
            
            return {'valid': True, 'payload': payload}
        
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token has expired'}
        except jwt.InvalidTokenError as e:
            return {'valid': False, 'error': f'Invalid token: {str(e)}'}
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Generate new access token from refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Dict[str, Any]: New tokens or error
        """
        validation_result = self.validate_token(refresh_token)
        
        if not validation_result['valid']:
            return validation_result
        
        payload = validation_result['payload']
        
        # Check if it's a refresh token
        if payload.get('token_type') != 'refresh':
            return {'valid': False, 'error': 'Invalid token type'}
        
        # Generate new access token
        user_id = payload['user_id']
        new_access_token = AuthenticationConfig.generate_jwt_token(user_id, 'access')
        
        return {
            'valid': True,
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': AuthenticationConfig.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()
        }


# Global JWT manager instance
jwt_manager = JWTManager()


def require_auth(permission: str = None):
    """
    Decorator to require authentication for endpoints.
    
    Args:
        permission: Required permission (optional)
        
    Returns:
        Decorator function
    """
    def decorator(func):
        """Authentication decorator."""
        from functools import wraps
        from flask import request, jsonify, g
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function."""
            # Get token from header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid authorization header'}), 401
            
            token = auth_header.split(' ')[1]
            
            # Validate token
            validation_result = jwt_manager.validate_token(token)
            if not validation_result['valid']:
                return jsonify({'error': validation_result['error']}), 401
            
            # Set current user in request context
            payload = validation_result['payload']
            g.current_user_id = payload['user_id']
            g.current_user_role = payload.get('role', 'user')
            
            # Check permission if required
            if permission and not AuthenticationConfig.has_permission(g.current_user_role, permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def require_api_key():
    """
    Decorator to require API key for endpoints.
    
    Returns:
        Decorator function
    """
    def decorator(func):
        """API key decorator."""
        from functools import wraps
        from flask import request, jsonify
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function."""
            # Get API key from header
            api_key = request.headers.get(AuthenticationConfig.API_KEY_HEADER)
            if not api_key:
                return jsonify({'error': 'Missing API key'}), 401
            
            # Validate API key format
            if not AuthenticationConfig.validate_api_key_format(api_key):
                return jsonify({'error': 'Invalid API key format'}), 401
            
            # TODO: Validate API key against database
            # For now, just check format
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
