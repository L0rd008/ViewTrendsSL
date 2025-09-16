"""
Configuration Package for ViewTrendsSL

This package provides centralized configuration management for the ViewTrendsSL application,
including API, database, deployment, and environment-specific settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import Dict, Any, Optional
from .api.api_config import APIConfig
from .api.cors_config import CORSConfig
from .api.rate_limiting_config import RateLimitConfig
from .api.authentication_config import AuthenticationConfig
from .database.database_config import DatabaseConfig
from .database.sqlite_config import SQLiteConfig
from .database.postgresql_config import PostgreSQLConfig
from .deployment.deployment_config import DeploymentConfig, DeploymentEnvironment


class Config:
    """
    Main configuration class that aggregates all configuration modules.
    
    This class provides a unified interface to access all configuration
    settings across the ViewTrendsSL application.
    """
    
    # Application metadata
    APP_NAME = 'ViewTrendsSL'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'YouTube Viewership Forecasting for Sri Lankan Audience'
    
    # Environment detection
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration."""
        return APIConfig.get_api_config()
    
    @classmethod
    def get_cors_config(cls) -> Dict[str, Any]:
        """Get CORS configuration."""
        return CORSConfig.get_cors_config()
    
    @classmethod
    def get_rate_limiting_config(cls) -> Dict[str, Any]:
        """Get rate limiting configuration."""
        return RateLimitConfig.get_rate_limiting_config()
    
    @classmethod
    def get_authentication_config(cls) -> Dict[str, Any]:
        """Get authentication configuration."""
        return AuthenticationConfig.get_authentication_config()
    
    @classmethod
    def get_database_config(cls, environment: str = None) -> Dict[str, Any]:
        """Get database configuration."""
        return DatabaseConfig.get_sqlalchemy_config(environment)
    
    @classmethod
    def get_deployment_config(cls, environment: DeploymentEnvironment = None) -> Dict[str, Any]:
        """Get deployment configuration."""
        return DeploymentConfig.get_environment_config(environment)
    
    @classmethod
    def get_all_config(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get complete application configuration.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Complete configuration
        """
        if environment is None:
            environment = cls.ENVIRONMENT
        
        return {
            'app': {
                'name': cls.APP_NAME,
                'version': cls.APP_VERSION,
                'description': cls.APP_DESCRIPTION,
                'environment': environment,
                'debug': cls.DEBUG,
                'testing': cls.TESTING,
                'secret_key': cls.SECRET_KEY
            },
            'api': cls.get_api_config(),
            'cors': cls.get_cors_config(),
            'rate_limiting': cls.get_rate_limiting_config(),
            'authentication': cls.get_authentication_config(),
            'database': cls.get_database_config(environment),
            'deployment': cls.get_deployment_config()
        }
    
    @classmethod
    def validate_config(cls, environment: str = None) -> Dict[str, Any]:
        """
        Validate application configuration.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Validation results
        """
        errors = []
        warnings = []
        
        # Validate secret key
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            if environment == 'production':
                errors.append('SECRET_KEY must be changed for production')
            else:
                warnings.append('Using default SECRET_KEY (change for production)')
        
        # Validate database configuration
        try:
            DatabaseConfig.validate_database_config(environment)
        except ValueError as e:
            errors.append(f'Database configuration error: {str(e)}')
        
        # Validate deployment configuration
        deployment_errors = DeploymentConfig.validate_deployment_config()
        errors.extend(deployment_errors)
        
        # Validate API configuration
        api_errors = APIConfig.validate_api_config()
        errors.extend(api_errors)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    
    @classmethod
    def get_database_config(cls, environment: str = None) -> Dict[str, Any]:
        """Get development database configuration."""
        return SQLiteConfig.get_engine_options('development')


class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    
    @classmethod
    def get_database_config(cls, environment: str = None) -> Dict[str, Any]:
        """Get testing database configuration."""
        return {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ECHO': False
        }


class StagingConfig(Config):
    """Staging environment configuration."""
    
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    
    @classmethod
    def validate_config(cls, environment: str = None) -> Dict[str, Any]:
        """Validate production configuration with stricter rules."""
        validation = super().validate_config('production')
        
        # Additional production validations
        if cls.DEBUG:
            validation['errors'].append('DEBUG must be False in production')
        
        if not os.getenv('DATABASE_URL'):
            validation['errors'].append('DATABASE_URL is required in production')
        
        validation['valid'] = len(validation['errors']) == 0
        return validation


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}


def get_config(environment: str = None) -> Config:
    """
    Get configuration class for environment.
    
    Args:
        environment: Environment name
        
    Returns:
        Config: Configuration class instance
    """
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')
    
    return config_map.get(environment, DevelopmentConfig)


def create_app_config(environment: str = None) -> Dict[str, Any]:
    """
    Create Flask application configuration.
    
    Args:
        environment: Environment name
        
    Returns:
        Dict[str, Any]: Flask configuration
    """
    config_class = get_config(environment)
    
    # Base Flask configuration
    flask_config = {
        'SECRET_KEY': config_class.SECRET_KEY,
        'DEBUG': config_class.DEBUG,
        'TESTING': config_class.TESTING,
        'ENV': environment or 'development'
    }
    
    # Add database configuration
    flask_config.update(config_class.get_database_config(environment))
    
    # Add API configuration
    api_config = config_class.get_api_config()
    flask_config.update({
        'JSON_SORT_KEYS': api_config.get('json_sort_keys', False),
        'JSONIFY_PRETTYPRINT_REGULAR': api_config.get('pretty_print', True)
    })
    
    # Add CORS configuration
    cors_config = config_class.get_cors_config()
    flask_config.update({
        'CORS_ORIGINS': cors_config.get('origins', ['*']),
        'CORS_METHODS': cors_config.get('methods', ['GET', 'POST', 'PUT', 'DELETE']),
        'CORS_HEADERS': cors_config.get('headers', ['Content-Type', 'Authorization'])
    })
    
    return flask_config


def get_health_check_config() -> Dict[str, Any]:
    """
    Get health check configuration for all components.
    
    Returns:
        Dict[str, Any]: Health check configuration
    """
    return {
        'database': {
            'enabled': True,
            'timeout': 5,
            'critical': True
        },
        'api': {
            'enabled': True,
            'timeout': 3,
            'critical': True
        },
        'external_services': {
            'enabled': True,
            'timeout': 10,
            'critical': False
        }
    }


def get_logging_config(environment: str = None) -> Dict[str, Any]:
    """
    Get logging configuration for environment.
    
    Args:
        environment: Environment name
        
    Returns:
        Dict[str, Any]: Logging configuration
    """
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')
    
    base_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'detailed': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': 'data/logs/application/app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            'viewtrendssl': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'sqlalchemy.engine': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
    
    # Environment-specific adjustments
    if environment == 'production':
        base_config['handlers']['console']['level'] = 'WARNING'
        base_config['loggers']['viewtrendssl']['level'] = 'INFO'
        base_config['root']['level'] = 'WARNING'
    
    elif environment == 'testing':
        base_config['handlers']['console']['level'] = 'ERROR'
        base_config['loggers']['viewtrendssl']['level'] = 'ERROR'
        base_config['root']['level'] = 'ERROR'
    
    return base_config


# Export main configuration classes and functions
__all__ = [
    'Config',
    'DevelopmentConfig',
    'TestingConfig',
    'StagingConfig',
    'ProductionConfig',
    'get_config',
    'create_app_config',
    'get_health_check_config',
    'get_logging_config'
]
