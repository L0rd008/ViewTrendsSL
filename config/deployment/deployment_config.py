"""
Deployment Configuration Module

This module handles deployment configuration for the ViewTrendsSL application,
including environment-specific settings, cloud provider configurations,
and deployment automation settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import Dict, Any, List, Optional
from enum import Enum


class DeploymentEnvironment(Enum):
    """Deployment environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class CloudProvider(Enum):
    """Cloud provider enumeration."""
    HEROKU = "heroku"
    AWS = "aws"
    GOOGLE_CLOUD = "gcp"
    AZURE = "azure"
    DIGITAL_OCEAN = "digitalocean"
    RAILWAY = "railway"
    RENDER = "render"


class DeploymentConfig:
    """
    Main deployment configuration class for ViewTrendsSL application.
    
    This class manages deployment settings, environment configurations,
    and cloud provider-specific settings.
    """
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'viewtrendssl')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    APP_DESCRIPTION = 'YouTube Viewership Forecasting for Sri Lankan Audience'
    
    # Environment settings
    DEFAULT_ENVIRONMENT = DeploymentEnvironment.DEVELOPMENT
    CURRENT_ENVIRONMENT = DeploymentEnvironment(os.getenv('DEPLOYMENT_ENV', 'development'))
    
    # Cloud provider settings
    CLOUD_PROVIDER = CloudProvider(os.getenv('CLOUD_PROVIDER', 'heroku'))
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    WORKERS = int(os.getenv('WEB_CONCURRENCY', '1'))
    WORKER_CLASS = os.getenv('WORKER_CLASS', 'sync')
    WORKER_TIMEOUT = int(os.getenv('WORKER_TIMEOUT', '30'))
    
    # SSL/TLS settings
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'False').lower() == 'true'
    SSL_REDIRECT = os.getenv('SSL_REDIRECT', 'False').lower() == 'true'
    
    # Domain settings
    DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'localhost')
    SUBDOMAIN = os.getenv('SUBDOMAIN', 'www')
    
    # Health check settings
    HEALTH_CHECK_ENABLED = True
    HEALTH_CHECK_PATH = '/health'
    READINESS_CHECK_PATH = '/ready'
    
    # Monitoring settings
    MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'True').lower() == 'true'
    METRICS_ENABLED = os.getenv('METRICS_ENABLED', 'True').lower() == 'true'
    
    # Backup settings
    BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'True').lower() == 'true'
    BACKUP_SCHEDULE = os.getenv('BACKUP_SCHEDULE', '0 2 * * *')  # Daily at 2 AM
    
    # Resource limits
    MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', '512M')
    CPU_LIMIT = os.getenv('CPU_LIMIT', '1')
    DISK_LIMIT = os.getenv('DISK_LIMIT', '1G')
    
    @classmethod
    def get_environment_config(cls, environment: DeploymentEnvironment = None) -> Dict[str, Any]:
        """
        Get configuration for specific deployment environment.
        
        Args:
            environment: Deployment environment
            
        Returns:
            Dict[str, Any]: Environment configuration
        """
        if environment is None:
            environment = cls.CURRENT_ENVIRONMENT
        
        base_config = {
            'app_name': cls.APP_NAME,
            'app_version': cls.APP_VERSION,
            'environment': environment.value,
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': False,
            'testing': False
        }
        
        if environment == DeploymentEnvironment.DEVELOPMENT:
            base_config.update({
                'debug': True,
                'host': '127.0.0.1',
                'port': 5000,
                'workers': 1,
                'reload': True,
                'log_level': 'debug'
            })
        
        elif environment == DeploymentEnvironment.STAGING:
            base_config.update({
                'debug': False,
                'workers': 2,
                'log_level': 'info',
                'force_https': True
            })
        
        elif environment == DeploymentEnvironment.PRODUCTION:
            base_config.update({
                'debug': False,
                'workers': cls.WORKERS,
                'worker_class': cls.WORKER_CLASS,
                'worker_timeout': cls.WORKER_TIMEOUT,
                'log_level': 'warning',
                'force_https': cls.FORCE_HTTPS,
                'ssl_redirect': cls.SSL_REDIRECT
            })
        
        elif environment == DeploymentEnvironment.TESTING:
            base_config.update({
                'testing': True,
                'debug': True,
                'workers': 1,
                'log_level': 'error'
            })
        
        return base_config
    
    @classmethod
    def get_cloud_provider_config(cls, provider: CloudProvider = None) -> Dict[str, Any]:
        """
        Get cloud provider-specific configuration.
        
        Args:
            provider: Cloud provider
            
        Returns:
            Dict[str, Any]: Provider configuration
        """
        if provider is None:
            provider = cls.CLOUD_PROVIDER
        
        if provider == CloudProvider.HEROKU:
            return cls._get_heroku_config()
        elif provider == CloudProvider.AWS:
            return cls._get_aws_config()
        elif provider == CloudProvider.GOOGLE_CLOUD:
            return cls._get_gcp_config()
        elif provider == CloudProvider.AZURE:
            return cls._get_azure_config()
        elif provider == CloudProvider.DIGITAL_OCEAN:
            return cls._get_digitalocean_config()
        elif provider == CloudProvider.RAILWAY:
            return cls._get_railway_config()
        elif provider == CloudProvider.RENDER:
            return cls._get_render_config()
        else:
            return {}
    
    @classmethod
    def _get_heroku_config(cls) -> Dict[str, Any]:
        """Get Heroku-specific configuration."""
        return {
            'provider': 'heroku',
            'app_name': os.getenv('HEROKU_APP_NAME', cls.APP_NAME),
            'region': os.getenv('HEROKU_REGION', 'us'),
            'stack': os.getenv('HEROKU_STACK', 'heroku-22'),
            'dyno_type': os.getenv('HEROKU_DYNO_TYPE', 'web'),
            'buildpacks': [
                'heroku/python'
            ],
            'addons': [
                'heroku-postgresql:mini',
                'heroku-redis:mini'
            ],
            'config_vars': {
                'FLASK_ENV': cls.CURRENT_ENVIRONMENT.value,
                'WEB_CONCURRENCY': str(cls.WORKERS),
                'PYTHONPATH': '/app/src'
            }
        }
    
    @classmethod
    def _get_aws_config(cls) -> Dict[str, Any]:
        """Get AWS-specific configuration."""
        return {
            'provider': 'aws',
            'region': os.getenv('AWS_REGION', 'us-east-1'),
            'service': os.getenv('AWS_SERVICE', 'elastic-beanstalk'),
            'instance_type': os.getenv('AWS_INSTANCE_TYPE', 't3.micro'),
            'platform': 'Python 3.9 running on 64bit Amazon Linux 2',
            'environment_variables': {
                'FLASK_ENV': cls.CURRENT_ENVIRONMENT.value,
                'PYTHONPATH': '/var/app/current/src'
            }
        }
    
    @classmethod
    def _get_gcp_config(cls) -> Dict[str, Any]:
        """Get Google Cloud Platform configuration."""
        return {
            'provider': 'gcp',
            'project_id': os.getenv('GCP_PROJECT_ID'),
            'region': os.getenv('GCP_REGION', 'us-central1'),
            'service': os.getenv('GCP_SERVICE', 'app-engine'),
            'runtime': 'python39',
            'instance_class': os.getenv('GCP_INSTANCE_CLASS', 'F1'),
            'environment_variables': {
                'FLASK_ENV': cls.CURRENT_ENVIRONMENT.value,
                'PYTHONPATH': '/srv/src'
            }
        }
    
    @classmethod
    def _get_azure_config(cls) -> Dict[str, Any]:
        """Get Azure-specific configuration."""
        return {
            'provider': 'azure',
            'resource_group': os.getenv('AZURE_RESOURCE_GROUP'),
            'location': os.getenv('AZURE_LOCATION', 'East US'),
            'app_service_plan': os.getenv('AZURE_APP_SERVICE_PLAN'),
            'runtime': 'PYTHON|3.9',
            'sku': os.getenv('AZURE_SKU', 'F1'),
            'environment_variables': {
                'FLASK_ENV': cls.CURRENT_ENVIRONMENT.value,
                'PYTHONPATH': '/home/site/wwwroot/src'
            }
        }
    
    @classmethod
    def _get_digitalocean_config(cls) -> Dict[str, Any]:
        """Get DigitalOcean-specific configuration."""
        return {
            'provider': 'digitalocean',
            'region': os.getenv('DO_REGION', 'nyc1'),
            'size': os.getenv('DO_SIZE', 's-1vcpu-1gb'),
            'app_spec': {
                'name': cls.APP_NAME,
                'services': [{
                    'name': 'web',
                    'source_dir': '/',
                    'github': {
                        'repo': os.getenv('GITHUB_REPO'),
                        'branch': os.getenv('GITHUB_BRANCH', 'main')
                    },
                    'run_command': 'gunicorn --bind 0.0.0.0:$PORT src.application.app:app',
                    'environment_slug': 'python',
                    'instance_count': 1,
                    'instance_size_slug': 'basic-xxs',
                    'envs': [{
                        'key': 'FLASK_ENV',
                        'value': cls.CURRENT_ENVIRONMENT.value
                    }]
                }]
            }
        }
    
    @classmethod
    def _get_railway_config(cls) -> Dict[str, Any]:
        """Get Railway-specific configuration."""
        return {
            'provider': 'railway',
            'project_name': cls.APP_NAME,
            'environment': cls.CURRENT_ENVIRONMENT.value,
            'build_command': 'pip install -r requirements.txt',
            'start_command': 'gunicorn --bind 0.0.0.0:$PORT src.application.app:app',
            'environment_variables': {
                'FLASK_ENV': cls.CURRENT_ENVIRONMENT.value,
                'PYTHONPATH': '/app/src'
            }
        }
    
    @classmethod
    def _get_render_config(cls) -> Dict[str, Any]:
        """Get Render-specific configuration."""
        return {
            'provider': 'render',
            'name': cls.APP_NAME,
            'type': 'web',
            'env': 'python',
            'plan': os.getenv('RENDER_PLAN', 'free'),
            'buildCommand': 'pip install -r requirements.txt',
            'startCommand': 'gunicorn --bind 0.0.0.0:$PORT src.application.app:app',
            'envVars': [{
                'key': 'FLASK_ENV',
                'value': cls.CURRENT_ENVIRONMENT.value
            }, {
                'key': 'PYTHONPATH',
                'value': '/opt/render/project/src'
            }]
        }
    
    @classmethod
    def get_deployment_urls(cls, environment: DeploymentEnvironment = None) -> Dict[str, str]:
        """
        Get deployment URLs for environment.
        
        Args:
            environment: Deployment environment
            
        Returns:
            Dict[str, str]: Deployment URLs
        """
        if environment is None:
            environment = cls.CURRENT_ENVIRONMENT
        
        base_domain = cls.DOMAIN_NAME
        
        if environment == DeploymentEnvironment.DEVELOPMENT:
            return {
                'app_url': f'http://localhost:{cls.PORT}',
                'api_url': f'http://localhost:{cls.PORT}/api',
                'health_url': f'http://localhost:{cls.PORT}{cls.HEALTH_CHECK_PATH}'
            }
        
        elif environment == DeploymentEnvironment.STAGING:
            return {
                'app_url': f'https://staging-{cls.APP_NAME}.{base_domain}',
                'api_url': f'https://staging-{cls.APP_NAME}.{base_domain}/api',
                'health_url': f'https://staging-{cls.APP_NAME}.{base_domain}{cls.HEALTH_CHECK_PATH}'
            }
        
        elif environment == DeploymentEnvironment.PRODUCTION:
            return {
                'app_url': f'https://{cls.SUBDOMAIN}.{base_domain}',
                'api_url': f'https://api.{base_domain}',
                'health_url': f'https://{cls.SUBDOMAIN}.{base_domain}{cls.HEALTH_CHECK_PATH}'
            }
        
        else:
            return {
                'app_url': f'http://localhost:{cls.PORT}',
                'api_url': f'http://localhost:{cls.PORT}/api',
                'health_url': f'http://localhost:{cls.PORT}{cls.HEALTH_CHECK_PATH}'
            }
    
    @classmethod
    def get_resource_requirements(cls, environment: DeploymentEnvironment = None) -> Dict[str, Any]:
        """
        Get resource requirements for environment.
        
        Args:
            environment: Deployment environment
            
        Returns:
            Dict[str, Any]: Resource requirements
        """
        if environment is None:
            environment = cls.CURRENT_ENVIRONMENT
        
        base_requirements = {
            'memory': cls.MEMORY_LIMIT,
            'cpu': cls.CPU_LIMIT,
            'disk': cls.DISK_LIMIT
        }
        
        if environment == DeploymentEnvironment.DEVELOPMENT:
            return {
                'memory': '256M',
                'cpu': '0.5',
                'disk': '500M'
            }
        
        elif environment == DeploymentEnvironment.STAGING:
            return {
                'memory': '512M',
                'cpu': '1',
                'disk': '1G'
            }
        
        elif environment == DeploymentEnvironment.PRODUCTION:
            return {
                'memory': '1G',
                'cpu': '2',
                'disk': '5G'
            }
        
        else:
            return base_requirements
    
    @classmethod
    def validate_deployment_config(cls, environment: DeploymentEnvironment = None) -> List[str]:
        """
        Validate deployment configuration.
        
        Args:
            environment: Deployment environment
            
        Returns:
            List[str]: List of validation errors
        """
        errors = []
        
        if environment is None:
            environment = cls.CURRENT_ENVIRONMENT
        
        # Validate required environment variables
        required_vars = ['SECRET_KEY']
        
        if environment == DeploymentEnvironment.PRODUCTION:
            required_vars.extend([
                'DATABASE_URL',
                'DOMAIN_NAME'
            ])
        
        for var in required_vars:
            if not os.getenv(var):
                errors.append(f'Missing required environment variable: {var}')
        
        # Validate cloud provider configuration
        provider_config = cls.get_cloud_provider_config()
        if not provider_config:
            errors.append(f'Invalid cloud provider: {cls.CLOUD_PROVIDER.value}')
        
        # Validate SSL configuration for production
        if environment == DeploymentEnvironment.PRODUCTION:
            if not cls.FORCE_HTTPS:
                errors.append('HTTPS should be enforced in production')
        
        return errors
    
    @classmethod
    def get_deployment_commands(cls, environment: DeploymentEnvironment = None) -> Dict[str, str]:
        """
        Get deployment commands for environment.
        
        Args:
            environment: Deployment environment
            
        Returns:
            Dict[str, str]: Deployment commands
        """
        if environment is None:
            environment = cls.CURRENT_ENVIRONMENT
        
        provider = cls.CLOUD_PROVIDER
        
        commands = {
            'build': 'docker build -t viewtrendssl .',
            'test': 'python -m pytest tests/',
            'migrate': 'flask db upgrade',
            'seed': 'python scripts/database/seed_data.py'
        }
        
        if provider == CloudProvider.HEROKU:
            commands.update({
                'deploy': f'git push heroku {environment.value}:main',
                'logs': 'heroku logs --tail',
                'scale': f'heroku ps:scale web={cls.WORKERS}'
            })
        
        elif provider == CloudProvider.AWS:
            commands.update({
                'deploy': 'eb deploy',
                'logs': 'eb logs',
                'scale': f'eb scale {cls.WORKERS}'
            })
        
        elif provider == CloudProvider.DIGITAL_OCEAN:
            commands.update({
                'deploy': 'doctl apps create --spec .do/app.yaml',
                'logs': 'doctl apps logs',
                'scale': 'doctl apps update'
            })
        
        return commands


class HealthCheckConfig:
    """Health check configuration for deployment monitoring."""
    
    HEALTH_CHECK_TIMEOUT = int(os.getenv('HEALTH_CHECK_TIMEOUT', '30'))
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', '60'))
    HEALTH_CHECK_RETRIES = int(os.getenv('HEALTH_CHECK_RETRIES', '3'))
    
    @classmethod
    def get_health_check_config(cls) -> Dict[str, Any]:
        """Get health check configuration."""
        return {
            'enabled': DeploymentConfig.HEALTH_CHECK_ENABLED,
            'path': DeploymentConfig.HEALTH_CHECK_PATH,
            'timeout': cls.HEALTH_CHECK_TIMEOUT,
            'interval': cls.HEALTH_CHECK_INTERVAL,
            'retries': cls.HEALTH_CHECK_RETRIES,
            'checks': [
                'database_connection',
                'api_endpoints',
                'external_services'
            ]
        }


def get_current_deployment_info() -> Dict[str, Any]:
    """
    Get current deployment information.
    
    Returns:
        Dict[str, Any]: Current deployment info
    """
    return {
        'app_name': DeploymentConfig.APP_NAME,
        'app_version': DeploymentConfig.APP_VERSION,
        'environment': DeploymentConfig.CURRENT_ENVIRONMENT.value,
        'cloud_provider': DeploymentConfig.CLOUD_PROVIDER.value,
        'host': DeploymentConfig.HOST,
        'port': DeploymentConfig.PORT,
        'workers': DeploymentConfig.WORKERS,
        'deployment_urls': DeploymentConfig.get_deployment_urls(),
        'resource_requirements': DeploymentConfig.get_resource_requirements(),
        'health_check': HealthCheckConfig.get_health_check_config()
    }
