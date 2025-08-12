"""
API Configuration Module

This module contains the main API configuration class that manages all
Flask application settings, CORS, rate limiting, authentication, and
other API-related configurations for the ViewTrendsSL application.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from datetime import timedelta
from typing import List, Optional


class APIConfig:
    """
    Main API configuration class for ViewTrendsSL application.
    
    This class centralizes all API-related configuration settings including
    Flask configuration, security settings, rate limiting, and external
    service configurations.
    """
    
    # Flask Core Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # API Version and Routing
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Rate Limiting Configuration
    RATE_LIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    DEFAULT_RATE_LIMIT = os.getenv('DEFAULT_RATE_LIMIT', '100 per hour')
    PREDICTION_RATE_LIMIT = os.getenv('PREDICTION_RATE_LIMIT', '10 per minute')
    
    # Authentication Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_HOURS', '1')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_DAYS', '30')))
    JWT_ALGORITHM = 'HS256'
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', '20'))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', '100'))
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json'}
    
    # External API Configuration
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_API_QUOTA_LIMIT = int(os.getenv('YOUTUBE_API_QUOTA_LIMIT', '10000'))
    YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
    
    # Cache Configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))  # 5 minutes
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'data/logs/application/app.log')
    
    # Security Configuration
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'False').lower() == 'true'
    SESSION_COOKIE_SECURE = FORCE_HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database Configuration (imported from database config)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/viewtrendssl.db')
    
    @classmethod
    def validate_config(cls) -> None:
        """
        Validate critical configuration values.
        
        Raises:
            ValueError: If required configuration is missing or invalid
        """
        # Validate required API keys
        if not cls.YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY is required")
        
        # Validate secret key in production
        if not cls.DEBUG and cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set for production")
        
        # Validate JWT configuration
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is required")
    
    @classmethod
    def get_flask_config(cls) -> dict:
        """
        Get Flask-specific configuration dictionary.
        
        Returns:
            dict: Flask configuration dictionary
        """
        return {
            'SECRET_KEY': cls.SECRET_KEY,
            'DEBUG': cls.DEBUG,
            'TESTING': cls.TESTING,
            'MAX_CONTENT_LENGTH': cls.MAX_CONTENT_LENGTH,
            'UPLOAD_FOLDER': cls.UPLOAD_FOLDER,
            'JWT_SECRET_KEY': cls.JWT_SECRET_KEY,
            'JWT_ACCESS_TOKEN_EXPIRES': cls.JWT_ACCESS_TOKEN_EXPIRES,
            'JWT_REFRESH_TOKEN_EXPIRES': cls.JWT_REFRESH_TOKEN_EXPIRES,
            'SQLALCHEMY_DATABASE_URI': cls.DATABASE_URL,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return not cls.DEBUG and not cls.TESTING
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.DEBUG and not cls.TESTING
    
    @classmethod
    def is_testing(cls) -> bool:
        """Check if running in testing environment."""
        return cls.TESTING


# Environment-specific configurations
class DevelopmentConfig(APIConfig):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(APIConfig):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    FORCE_HTTPS = True


class TestingConfig(APIConfig):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(environment: Optional[str] = None) -> APIConfig:
    """
    Get configuration class for specified environment.
    
    Args:
        environment: Environment name (development, production, testing)
        
    Returns:
        APIConfig: Configuration class instance
    """
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')
    
    config_class = config_map.get(environment, config_map['default'])
    return config_class()
