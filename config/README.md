# Configuration System

This directory contains the comprehensive configuration system for the ViewTrendsSL application. The configuration is organized into modular components that handle different aspects of the application.

## Overview

The configuration system is designed to:
- Provide environment-specific settings (development, testing, staging, production)
- Support multiple deployment platforms (Heroku, AWS, GCP, etc.)
- Handle database configurations for SQLite and PostgreSQL
- Manage API settings, CORS, rate limiting, and authentication
- Enable easy configuration validation and health checks

## Structure

```
config/
├── __init__.py                 # Main configuration aggregator
├── README.md                   # This documentation
├── api/                        # API-related configurations
│   ├── api_config.py          # Core API settings
│   ├── cors_config.py         # CORS configuration
│   ├── rate_limiting_config.py # Rate limiting settings
│   └── authentication_config.py # Auth configuration
├── database/                   # Database configurations
│   ├── database_config.py     # Main database config
│   ├── sqlite_config.py       # SQLite-specific settings
│   └── postgresql_config.py   # PostgreSQL-specific settings
└── deployment/                 # Deployment configurations
    └── deployment_config.py   # Cloud provider settings
```

## Usage

### Basic Usage

```python
from config import get_config, create_app_config

# Get configuration for current environment
config = get_config()

# Create Flask app configuration
app_config = create_app_config('production')

# Get specific configuration sections
api_config = config.get_api_config()
db_config = config.get_database_config()
```

### Environment-Specific Configuration

```python
from config import DevelopmentConfig, ProductionConfig

# Development configuration
dev_config = DevelopmentConfig()
dev_db = dev_config.get_database_config()

# Production configuration
prod_config = ProductionConfig()
prod_db = prod_config.get_database_config()
```

### Configuration Validation

```python
from config import Config

# Validate configuration
validation = Config.validate_config('production')
if not validation['valid']:
    print("Configuration errors:", validation['errors'])
    print("Configuration warnings:", validation['warnings'])
```

## Environment Variables

The configuration system uses environment variables for sensitive and environment-specific settings:

### Core Application
- `FLASK_ENV`: Environment name (development, testing, staging, production)
- `SECRET_KEY`: Application secret key (required for production)
- `DEBUG`: Enable debug mode (True/False)
- `TESTING`: Enable testing mode (True/False)

### Database Configuration
- `DATABASE_URL`: Complete database URL
- `DATABASE_URL_DEVELOPMENT`: Development database URL
- `DATABASE_URL_TESTING`: Testing database URL
- `DATABASE_URL_PRODUCTION`: Production database URL

#### PostgreSQL Specific
- `PG_HOST`: PostgreSQL host
- `PG_PORT`: PostgreSQL port
- `PG_DATABASE`: Database name
- `PG_USERNAME`: Database username
- `PG_PASSWORD`: Database password
- `PG_SSL_MODE`: SSL mode (disable, allow, prefer, require, verify-ca, verify-full)

### API Configuration
- `API_VERSION`: API version (default: v1)
- `API_TITLE`: API title
- `API_DESCRIPTION`: API description
- `MAX_CONTENT_LENGTH`: Maximum request size
- `REQUEST_TIMEOUT`: Request timeout in seconds

### Rate Limiting
- `RATE_LIMIT_ENABLED`: Enable rate limiting (True/False)
- `RATE_LIMIT_DEFAULT`: Default rate limit (e.g., "100/hour")
- `RATE_LIMIT_STORAGE_URL`: Redis URL for rate limiting storage

### Authentication
- `JWT_SECRET_KEY`: JWT secret key
- `JWT_ACCESS_TOKEN_EXPIRES`: Access token expiration time
- `JWT_REFRESH_TOKEN_EXPIRES`: Refresh token expiration time
- `BCRYPT_LOG_ROUNDS`: Bcrypt hashing rounds

### CORS Configuration
- `CORS_ORIGINS`: Allowed origins (comma-separated)
- `CORS_METHODS`: Allowed methods (comma-separated)
- `CORS_HEADERS`: Allowed headers (comma-separated)

### Deployment Configuration
- `DEPLOYMENT_ENV`: Deployment environment
- `CLOUD_PROVIDER`: Cloud provider (heroku, aws, gcp, azure, etc.)
- `HOST`: Application host
- `PORT`: Application port
- `WEB_CONCURRENCY`: Number of worker processes
- `WORKER_CLASS`: Worker class type
- `WORKER_TIMEOUT`: Worker timeout

### Cloud Provider Specific

#### Heroku
- `HEROKU_APP_NAME`: Heroku app name
- `HEROKU_REGION`: Heroku region

#### AWS
- `AWS_REGION`: AWS region
- `AWS_SERVICE`: AWS service (elastic-beanstalk, ecs, etc.)
- `AWS_INSTANCE_TYPE`: EC2 instance type

#### Google Cloud Platform
- `GCP_PROJECT_ID`: GCP project ID
- `GCP_REGION`: GCP region
- `GCP_SERVICE`: GCP service (app-engine, cloud-run, etc.)

## Configuration Classes

### Config (Base Class)
The main configuration class that aggregates all configuration modules.

**Methods:**
- `get_api_config()`: Get API configuration
- `get_cors_config()`: Get CORS configuration
- `get_rate_limiting_config()`: Get rate limiting configuration
- `get_authentication_config()`: Get authentication configuration
- `get_database_config()`: Get database configuration
- `get_deployment_config()`: Get deployment configuration
- `get_all_config()`: Get complete configuration
- `validate_config()`: Validate configuration

### DevelopmentConfig
Configuration for development environment with debug enabled and SQLite database.

### TestingConfig
Configuration for testing environment with in-memory SQLite database.

### StagingConfig
Configuration for staging environment with production-like settings.

### ProductionConfig
Configuration for production environment with strict validation and security settings.

## Database Configuration

### SQLite Configuration
Used for development and testing environments.

**Features:**
- WAL mode for better concurrency
- Optimized PRAGMA settings
- Automatic database file creation
- Backup and vacuum operations

### PostgreSQL Configuration
Used for staging and production environments.

**Features:**
- Connection pooling
- SSL configuration
- Performance optimization
- Backup and restore commands
- Slow query monitoring

## API Configuration

### Core API Settings
- Version management
- Request/response formatting
- Timeout configuration
- Content length limits

### CORS Configuration
- Origin validation
- Method restrictions
- Header management
- Credential handling

### Rate Limiting
- Per-endpoint limits
- User-based limits
- IP-based limits
- Redis storage backend

### Authentication
- JWT token management
- Password hashing
- Session configuration
- OAuth integration

## Deployment Configuration

### Environment Management
- Development: Local development with debug enabled
- Testing: Automated testing with in-memory database
- Staging: Production-like environment for testing
- Production: Live environment with security hardening

### Cloud Provider Support
- **Heroku**: Buildpacks, add-ons, config vars
- **AWS**: Elastic Beanstalk, ECS, Lambda
- **Google Cloud**: App Engine, Cloud Run, GKE
- **Azure**: App Service, Container Instances
- **DigitalOcean**: App Platform
- **Railway**: Simple deployment
- **Render**: Static sites and web services

## Health Checks

The configuration system includes health check settings for monitoring:

```python
from config import get_health_check_config

health_config = get_health_check_config()
# Returns configuration for database, API, and external service checks
```

## Logging Configuration

Centralized logging configuration with environment-specific settings:

```python
from config import get_logging_config

logging_config = get_logging_config('production')
# Returns logging configuration with appropriate levels and handlers
```

## Best Practices

### Security
1. Never commit sensitive values to version control
2. Use environment variables for all secrets
3. Validate configuration in production
4. Enable HTTPS in production environments
5. Use strong secret keys

### Environment Management
1. Use separate databases for each environment
2. Configure appropriate logging levels
3. Enable debug mode only in development
4. Use connection pooling in production
5. Monitor resource usage

### Configuration Validation
1. Validate configuration on application startup
2. Fail fast if required settings are missing
3. Log configuration warnings
4. Test configuration changes in staging first

### Deployment
1. Use infrastructure as code when possible
2. Automate configuration deployment
3. Monitor configuration drift
4. Backup configuration settings
5. Document environment-specific requirements

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Confirm network connectivity
   - Check SSL configuration

2. **Authentication Failures**
   - Verify JWT_SECRET_KEY is set
   - Check token expiration settings
   - Confirm password hashing configuration

3. **CORS Issues**
   - Check allowed origins
   - Verify request methods
   - Confirm header configuration

4. **Rate Limiting Problems**
   - Check Redis connection
   - Verify rate limit settings
   - Monitor rate limit storage

### Debug Mode

Enable debug logging to troubleshoot configuration issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from config import Config
config = Config()
validation = config.validate_config()
print(validation)
```

## Contributing

When adding new configuration options:

1. Add environment variable documentation
2. Include validation logic
3. Provide sensible defaults
4. Add tests for new configuration
5. Update this documentation

## Examples

See the `examples/` directory for complete configuration examples for different deployment scenarios.
