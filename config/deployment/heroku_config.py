"""
Heroku Deployment Configuration for ViewTrendsSL

This module provides Heroku-specific configuration settings and utilities
for deploying the ViewTrendsSL application to Heroku platform.

Features:
- Environment detection and configuration
- Database URL parsing and connection setup
- Static file handling with WhiteNoise
- Logging configuration for Heroku
- Process scaling and dyno management
- Add-on configurations (Redis, PostgreSQL)
"""

import os
import logging
from urllib.parse import urlparse
from typing import Dict, Any, Optional
import dj_database_url


class HerokuConfig:
    """
    Heroku-specific configuration class that handles all Heroku platform
    specific settings and optimizations.
    """
    
    def __init__(self):
        self.is_heroku = self._detect_heroku_environment()
        self.app_name = os.environ.get('HEROKU_APP_NAME', 'viewtrendssl')
        self.dyno_type = os.environ.get('DYNO', 'web.1')
        self.release_version = os.environ.get('HEROKU_RELEASE_VERSION', 'v1')
        self.slug_commit = os.environ.get('HEROKU_SLUG_COMMIT', 'unknown')
        
    def _detect_heroku_environment(self) -> bool:
        """
        Detect if the application is running on Heroku platform.
        
        Returns:
            bool: True if running on Heroku, False otherwise
        """
        heroku_indicators = [
            'DYNO',
            'HEROKU_APP_NAME',
            'HEROKU_RELEASE_VERSION',
            'PORT'  # Heroku sets this automatically
        ]
        
        return any(os.environ.get(indicator) for indicator in heroku_indicators)
    
    def get_database_config(self) -> Dict[str, Any]:
        """
        Parse Heroku DATABASE_URL and return database configuration.
        
        Returns:
            Dict[str, Any]: Database configuration dictionary
        """
        if not self.is_heroku:
            return self._get_local_database_config()
            
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not found on Heroku")
        
        # Parse the database URL
        db_config = dj_database_url.parse(database_url)
        
        # Heroku PostgreSQL specific optimizations
        db_config.update({
            'CONN_MAX_AGE': 600,  # Connection pooling
            'OPTIONS': {
                'sslmode': 'require',  # SSL required for Heroku Postgres
                'connect_timeout': 10,
                'application_name': f'{self.app_name}-{self.dyno_type}',
            },
            'ATOMIC_REQUESTS': True,
            'AUTOCOMMIT': True,
        })
        
        return db_config
    
    def _get_local_database_config(self) -> Dict[str, Any]:
        """
        Get local development database configuration.
        
        Returns:
            Dict[str, Any]: Local database configuration
        """
        return {
            'ENGINE': 'sqlite3',
            'NAME': os.path.join(os.getcwd(), 'data', 'viewtrendssl_local.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    
    def get_redis_config(self) -> Optional[Dict[str, Any]]:
        """
        Parse Heroku REDIS_URL and return Redis configuration.
        
        Returns:
            Optional[Dict[str, Any]]: Redis configuration or None if not available
        """
        redis_url = os.environ.get('REDIS_URL') or os.environ.get('REDISCLOUD_URL')
        
        if not redis_url:
            return None
            
        parsed_url = urlparse(redis_url)
        
        return {
            'host': parsed_url.hostname,
            'port': parsed_url.port or 6379,
            'password': parsed_url.password,
            'db': 0,
            'ssl_cert_reqs': None,  # Heroku Redis supports SSL
            'socket_connect_timeout': 5,
            'socket_timeout': 5,
            'retry_on_timeout': True,
            'health_check_interval': 30,
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get Heroku-optimized logging configuration.
        
        Returns:
            Dict[str, Any]: Logging configuration dictionary
        """
        log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'heroku': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'detailed': {
                    'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': log_level,
                    'formatter': 'heroku',
                    'stream': 'ext://sys.stdout'
                },
                'error_console': {
                    'class': 'logging.StreamHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'stream': 'ext://sys.stderr'
                }
            },
            'loggers': {
                'viewtrendssl': {
                    'level': log_level,
                    'handlers': ['console', 'error_console'],
                    'propagate': False
                },
                'gunicorn': {
                    'level': 'INFO',
                    'handlers': ['console'],
                    'propagate': False
                },
                'werkzeug': {
                    'level': 'WARNING',
                    'handlers': ['console'],
                    'propagate': False
                }
            },
            'root': {
                'level': log_level,
                'handlers': ['console']
            }
        }
        
        return config
    
    def get_static_files_config(self) -> Dict[str, Any]:
        """
        Get static files configuration for Heroku deployment.
        
        Returns:
            Dict[str, Any]: Static files configuration
        """
        return {
            'STATIC_URL': '/static/',
            'STATIC_ROOT': os.path.join(os.getcwd(), 'staticfiles'),
            'STATICFILES_DIRS': [
                os.path.join(os.getcwd(), 'src', 'presentation', 'static'),
            ],
            'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
            'WHITENOISE_USE_FINDERS': True,
            'WHITENOISE_AUTOREFRESH': not self.is_heroku,  # Only in development
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """
        Get security configuration for Heroku deployment.
        
        Returns:
            Dict[str, Any]: Security configuration
        """
        config = {
            'SECRET_KEY': os.environ.get('SECRET_KEY'),
            'DEBUG': os.environ.get('DEBUG', 'False').lower() == 'true',
            'ALLOWED_HOSTS': self._get_allowed_hosts(),
            'SECURE_SSL_REDIRECT': self.is_heroku,
            'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https') if self.is_heroku else None,
            'SECURE_HSTS_SECONDS': 31536000 if self.is_heroku else 0,
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': self.is_heroku,
            'SECURE_HSTS_PRELOAD': self.is_heroku,
            'SECURE_CONTENT_TYPE_NOSNIFF': True,
            'SECURE_BROWSER_XSS_FILTER': True,
            'X_FRAME_OPTIONS': 'DENY',
        }
        
        if not config['SECRET_KEY']:
            if self.is_heroku:
                raise ValueError("SECRET_KEY environment variable must be set on Heroku")
            else:
                # Generate a development secret key
                config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        
        return config
    
    def _get_allowed_hosts(self) -> list:
        """
        Get allowed hosts for the application.
        
        Returns:
            list: List of allowed hosts
        """
        if not self.is_heroku:
            return ['localhost', '127.0.0.1', '0.0.0.0']
        
        allowed_hosts = [f'{self.app_name}.herokuapp.com']
        
        # Add custom domain if configured
        custom_domain = os.environ.get('CUSTOM_DOMAIN')
        if custom_domain:
            allowed_hosts.append(custom_domain)
            allowed_hosts.append(f'www.{custom_domain}')
        
        return allowed_hosts
    
    def get_worker_config(self) -> Dict[str, Any]:
        """
        Get worker configuration for different dyno types.
        
        Returns:
            Dict[str, Any]: Worker configuration
        """
        return {
            'web': {
                'bind': f"0.0.0.0:{os.environ.get('PORT', 8000)}",
                'workers': int(os.environ.get('WEB_CONCURRENCY', 2)),
                'worker_class': 'sync',
                'worker_connections': 1000,
                'max_requests': 1000,
                'max_requests_jitter': 100,
                'timeout': 30,
                'keepalive': 2,
                'preload_app': True,
            },
            'worker': {
                'workers': int(os.environ.get('WORKER_CONCURRENCY', 1)),
                'worker_class': 'sync',
                'timeout': 300,  # Longer timeout for background tasks
                'max_requests': 100,
                'preload_app': True,
            }
        }
    
    def get_addon_configs(self) -> Dict[str, Any]:
        """
        Get configuration for Heroku add-ons.
        
        Returns:
            Dict[str, Any]: Add-on configurations
        """
        configs = {}
        
        # Heroku Scheduler
        if os.environ.get('HEROKU_SCHEDULER_ENABLED'):
            configs['scheduler'] = {
                'enabled': True,
                'timezone': 'Asia/Colombo',
                'jobs': [
                    {
                        'command': 'python scripts/data_collection/youtube/collect_videos.py',
                        'schedule': 'daily',
                        'time': '02:00'
                    },
                    {
                        'command': 'python scripts/data_collection/youtube/track_performance.py',
                        'schedule': 'hourly'
                    }
                ]
            }
        
        # Heroku Postgres
        if os.environ.get('DATABASE_URL'):
            configs['postgres'] = {
                'enabled': True,
                'backup_schedule': 'daily',
                'maintenance_window': 'Sunday 02:00'
            }
        
        # Redis add-ons
        redis_url = os.environ.get('REDIS_URL') or os.environ.get('REDISCLOUD_URL')
        if redis_url:
            configs['redis'] = {
                'enabled': True,
                'maxmemory_policy': 'allkeys-lru',
                'timeout': 5
            }
        
        # New Relic (if configured)
        if os.environ.get('NEW_RELIC_LICENSE_KEY'):
            configs['newrelic'] = {
                'enabled': True,
                'app_name': f'{self.app_name}-{os.environ.get("HEROKU_RELEASE_VERSION", "v1")}',
                'log_level': 'info'
            }
        
        # Sentry (if configured)
        if os.environ.get('SENTRY_DSN'):
            configs['sentry'] = {
                'enabled': True,
                'environment': os.environ.get('HEROKU_RELEASE_VERSION', 'production'),
                'release': self.slug_commit,
                'traces_sample_rate': 0.1
            }
        
        return configs
    
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get environment information for debugging and monitoring.
        
        Returns:
            Dict[str, Any]: Environment information
        """
        return {
            'is_heroku': self.is_heroku,
            'app_name': self.app_name,
            'dyno_type': self.dyno_type,
            'release_version': self.release_version,
            'slug_commit': self.slug_commit,
            'port': os.environ.get('PORT', 8000),
            'python_version': os.environ.get('PYTHON_VERSION', '3.11'),
            'buildpack_url': os.environ.get('BUILDPACK_URL', 'heroku/python'),
        }
    
    def setup_heroku_logging(self):
        """
        Set up logging configuration for Heroku environment.
        """
        logging_config = self.get_logging_config()
        logging.config.dictConfig(logging_config)
        
        # Log environment information on startup
        logger = logging.getLogger('viewtrendssl')
        env_info = self.get_environment_info()
        logger.info(f"Starting ViewTrendsSL on Heroku: {env_info}")
    
    def validate_heroku_environment(self) -> bool:
        """
        Validate that all required environment variables are set for Heroku.
        
        Returns:
            bool: True if environment is valid, False otherwise
        """
        required_vars = ['SECRET_KEY']
        
        if self.is_heroku:
            required_vars.extend(['DATABASE_URL', 'PORT'])
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            logger = logging.getLogger('viewtrendssl')
            logger.error(f"Missing required environment variables: {missing_vars}")
            return False
        
        return True
    
    def get_procfile_commands(self) -> Dict[str, str]:
        """
        Get Procfile commands for different process types.
        
        Returns:
            Dict[str, str]: Process type to command mapping
        """
        return {
            'web': 'gunicorn --config config/docker/production/gunicorn.conf.py src.application.api.app:app',
            'worker': 'python -m celery worker -A src.business.tasks.celery_app --loglevel=info',
            'scheduler': 'python scripts/data_collection/orchestrator.py',
            'release': 'python scripts/database/setup/init_database.py'
        }
    
    def get_app_json_config(self) -> Dict[str, Any]:
        """
        Get app.json configuration for Heroku deployment.
        
        Returns:
            Dict[str, Any]: app.json configuration
        """
        return {
            "name": "ViewTrendsSL",
            "description": "YouTube Viewership Forecasting for Sri Lankan Audience",
            "repository": "https://github.com/L0rd008/ViewTrendsSL",
            "logo": "https://raw.githubusercontent.com/L0rd008/ViewTrendsSL/main/src/presentation/static/images/logo.png",
            "keywords": ["python", "machine-learning", "youtube", "analytics", "forecasting"],
            "stack": "heroku-22",
            "buildpacks": [
                {
                    "url": "heroku/python"
                }
            ],
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": "basic"
                }
            },
            "addons": [
                {
                    "plan": "heroku-postgresql:mini",
                    "as": "DATABASE"
                },
                {
                    "plan": "heroku-redis:mini",
                    "as": "REDIS"
                }
            ],
            "env": {
                "SECRET_KEY": {
                    "description": "Secret key for Django application",
                    "generator": "secret"
                },
                "DEBUG": {
                    "description": "Enable debug mode",
                    "value": "False"
                },
                "LOG_LEVEL": {
                    "description": "Logging level",
                    "value": "INFO"
                },
                "YOUTUBE_API_KEY": {
                    "description": "YouTube Data API v3 key",
                    "required": True
                },
                "CUSTOM_DOMAIN": {
                    "description": "Custom domain name (optional)",
                    "required": False
                }
            },
            "scripts": {
                "postdeploy": "python scripts/database/setup/init_database.py"
            }
        }


# Utility functions for Heroku deployment
def get_heroku_config() -> HerokuConfig:
    """
    Get a configured HerokuConfig instance.
    
    Returns:
        HerokuConfig: Configured Heroku configuration instance
    """
    return HerokuConfig()


def setup_heroku_app(app):
    """
    Set up a Flask/Django app for Heroku deployment.
    
    Args:
        app: Flask or Django application instance
    """
    heroku_config = get_heroku_config()
    
    # Validate environment
    if not heroku_config.validate_heroku_environment():
        raise RuntimeError("Invalid Heroku environment configuration")
    
    # Set up logging
    heroku_config.setup_heroku_logging()
    
    # Configure app settings
    if hasattr(app, 'config'):  # Flask app
        security_config = heroku_config.get_security_config()
        for key, value in security_config.items():
            app.config[key] = value
    
    return heroku_config


def create_procfile():
    """
    Create a Procfile for Heroku deployment.
    """
    heroku_config = get_heroku_config()
    commands = heroku_config.get_procfile_commands()
    
    procfile_content = []
    for process_type, command in commands.items():
        procfile_content.append(f"{process_type}: {command}")
    
    with open('Procfile', 'w') as f:
        f.write('\n'.join(procfile_content))
    
    print("Procfile created successfully")


def create_app_json():
    """
    Create an app.json file for Heroku deployment.
    """
    import json
    
    heroku_config = get_heroku_config()
    app_json_config = heroku_config.get_app_json_config()
    
    with open('app.json', 'w') as f:
        json.dump(app_json_config, f, indent=2)
    
    print("app.json created successfully")


if __name__ == "__main__":
    # CLI utility for Heroku configuration
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python heroku_config.py [procfile|app_json|validate]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "procfile":
        create_procfile()
    elif command == "app_json":
        create_app_json()
    elif command == "validate":
        heroku_config = get_heroku_config()
        if heroku_config.validate_heroku_environment():
            print("✅ Heroku environment is valid")
        else:
            print("❌ Heroku environment validation failed")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
