"""
CORS Configuration Module

This module handles Cross-Origin Resource Sharing (CORS) configuration
for the ViewTrendsSL API, allowing controlled access from web browsers
and other client applications.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import List, Dict, Any
from flask_cors import CORS


class CORSConfig:
    """
    CORS configuration class for ViewTrendsSL API.
    
    This class manages Cross-Origin Resource Sharing settings to allow
    secure access from web browsers and other client applications while
    maintaining security best practices.
    """
    
    # Default CORS origins for different environments
    DEVELOPMENT_ORIGINS = [
        'http://localhost:3000',  # React development server
        'http://localhost:5000',  # Flask development server
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5000',
    ]
    
    PRODUCTION_ORIGINS = [
        'https://viewtrendssl.herokuapp.com',
        'https://www.viewtrendssl.com',
        'https://viewtrendssl.com',
    ]
    
    # Allowed HTTP methods
    ALLOWED_METHODS = [
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'HEAD',
        'PATCH'
    ]
    
    # Allowed headers
    ALLOWED_HEADERS = [
        'Content-Type',
        'Authorization',
        'X-Requested-With',
        'X-API-Key',
        'Accept',
        'Origin',
        'Cache-Control',
        'X-File-Name'
    ]
    
    # Exposed headers (headers that the client can access)
    EXPOSED_HEADERS = [
        'Content-Range',
        'X-Content-Range',
        'X-Total-Count',
        'X-Rate-Limit-Remaining',
        'X-Rate-Limit-Reset'
    ]
    
    @classmethod
    def get_origins(cls, environment: str = None) -> List[str]:
        """
        Get allowed origins based on environment.
        
        Args:
            environment: Environment name (development, production, testing)
            
        Returns:
            List[str]: List of allowed origins
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')
        
        # Get origins from environment variable first
        env_origins = os.getenv('CORS_ORIGINS')
        if env_origins:
            return [origin.strip() for origin in env_origins.split(',')]
        
        # Use default origins based on environment
        if environment == 'production':
            return cls.PRODUCTION_ORIGINS
        elif environment == 'development':
            return cls.DEVELOPMENT_ORIGINS
        else:
            # Testing environment - allow all origins
            return ['*']
    
    @classmethod
    def get_cors_config(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get complete CORS configuration dictionary.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: CORS configuration dictionary
        """
        return {
            'origins': cls.get_origins(environment),
            'methods': cls.ALLOWED_METHODS,
            'allow_headers': cls.ALLOWED_HEADERS,
            'expose_headers': cls.EXPOSED_HEADERS,
            'supports_credentials': True,
            'max_age': 86400,  # 24 hours
            'send_wildcard': False,
            'vary_header': True
        }
    
    @classmethod
    def configure_cors(cls, app, environment: str = None) -> CORS:
        """
        Configure CORS for Flask application.
        
        Args:
            app: Flask application instance
            environment: Environment name
            
        Returns:
            CORS: Configured CORS instance
        """
        cors_config = cls.get_cors_config(environment)
        
        # Initialize CORS with configuration
        cors = CORS(app, **cors_config)
        
        # Add custom CORS headers for API endpoints
        @app.after_request
        def after_request(response):
            """Add custom CORS headers to all responses."""
            origin = request.headers.get('Origin')
            
            if origin in cors_config['origins'] or '*' in cors_config['origins']:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = ', '.join(cors_config['methods'])
                response.headers['Access-Control-Allow-Headers'] = ', '.join(cors_config['allow_headers'])
                response.headers['Access-Control-Expose-Headers'] = ', '.join(cors_config['expose_headers'])
                response.headers['Access-Control-Max-Age'] = str(cors_config['max_age'])
            
            return response
        
        return cors
    
    @classmethod
    def is_origin_allowed(cls, origin: str, environment: str = None) -> bool:
        """
        Check if an origin is allowed.
        
        Args:
            origin: Origin URL to check
            environment: Environment name
            
        Returns:
            bool: True if origin is allowed, False otherwise
        """
        allowed_origins = cls.get_origins(environment)
        
        # Allow all origins if wildcard is present
        if '*' in allowed_origins:
            return True
        
        # Check exact match
        return origin in allowed_origins
    
    @classmethod
    def validate_cors_config(cls, environment: str = None) -> None:
        """
        Validate CORS configuration.
        
        Args:
            environment: Environment name
            
        Raises:
            ValueError: If CORS configuration is invalid
        """
        origins = cls.get_origins(environment)
        
        if not origins:
            raise ValueError("No CORS origins configured")
        
        # In production, ensure no wildcard origins
        if environment == 'production' and '*' in origins:
            raise ValueError("Wildcard origins not allowed in production")
        
        # Validate origin URLs
        for origin in origins:
            if origin != '*' and not (origin.startswith('http://') or origin.startswith('https://')):
                raise ValueError(f"Invalid origin URL: {origin}")


# Pre-configured CORS instances for different use cases
class APICORSConfig(CORSConfig):
    """CORS configuration specifically for API endpoints."""
    
    ALLOWED_HEADERS = CORSConfig.ALLOWED_HEADERS + [
        'X-API-Version',
        'X-Request-ID'
    ]


class WebAppCORSConfig(CORSConfig):
    """CORS configuration for web application endpoints."""
    
    ALLOWED_METHODS = ['GET', 'POST', 'OPTIONS']
    
    ALLOWED_HEADERS = [
        'Content-Type',
        'X-Requested-With',
        'Accept',
        'Origin'
    ]


def configure_api_cors(app, environment: str = None) -> CORS:
    """
    Configure CORS specifically for API endpoints.
    
    Args:
        app: Flask application instance
        environment: Environment name
        
    Returns:
        CORS: Configured CORS instance for API
    """
    return APICORSConfig.configure_cors(app, environment)


def configure_webapp_cors(app, environment: str = None) -> CORS:
    """
    Configure CORS specifically for web application.
    
    Args:
        app: Flask application instance
        environment: Environment name
        
    Returns:
        CORS: Configured CORS instance for web app
    """
    return WebAppCORSConfig.configure_cors(app, environment)
