"""
Database Configuration Module

This module handles database configuration for the ViewTrendsSL application,
including connection settings, ORM configuration, and database-specific
optimizations for different environments.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import Dict, Any, Optional
from urllib.parse import urlparse


class DatabaseConfig:
    """
    Main database configuration class for ViewTrendsSL application.
    
    This class manages database connection settings, SQLAlchemy configuration,
    and environment-specific database optimizations.
    """
    
    # Default database URLs for different environments
    DEFAULT_DATABASE_URLS = {
        'development': 'sqlite:///data/viewtrendssl_dev.db',
        'testing': 'sqlite:///:memory:',
        'production': os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/viewtrendssl')
    }
    
    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.getenv('SQLALCHEMY_RECORD_QUERIES', 'False').lower() == 'true'
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,  # 1 hour
        'pool_timeout': 30,
        'max_overflow': 20,
        'echo': SQLALCHEMY_ECHO
    }
    
    # Connection Pool Configuration
    POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
    MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '20'))
    POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '3600'))
    POOL_PRE_PING = os.getenv('DB_POOL_PRE_PING', 'True').lower() == 'true'
    
    # Query Configuration
    QUERY_TIMEOUT = int(os.getenv('DB_QUERY_TIMEOUT', '30'))
    SLOW_QUERY_THRESHOLD = float(os.getenv('DB_SLOW_QUERY_THRESHOLD', '1.0'))
    
    # Migration Configuration
    MIGRATION_DIRECTORY = 'src/data_access/database/migrations'
    MIGRATION_COMPARE_TYPE = True
    MIGRATION_COMPARE_SERVER_DEFAULT = True
    
    # Backup Configuration
    BACKUP_DIRECTORY = 'data/backups'
    BACKUP_RETENTION_DAYS = int(os.getenv('DB_BACKUP_RETENTION_DAYS', '30'))
    AUTO_BACKUP_ENABLED = os.getenv('DB_AUTO_BACKUP_ENABLED', 'True').lower() == 'true'
    
    @classmethod
    def get_database_url(cls, environment: str = None) -> str:
        """
        Get database URL for specified environment.
        
        Args:
            environment: Environment name (development, testing, production)
            
        Returns:
            str: Database URL
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')
        
        # Get URL from environment variable first
        env_var_name = f'DATABASE_URL_{environment.upper()}'
        database_url = os.getenv(env_var_name) or os.getenv('DATABASE_URL')
        
        if database_url:
            return database_url
        
        # Use default URL for environment
        return cls.DEFAULT_DATABASE_URLS.get(environment, cls.DEFAULT_DATABASE_URLS['development'])
    
    @classmethod
    def parse_database_url(cls, database_url: str) -> Dict[str, Any]:
        """
        Parse database URL into components.
        
        Args:
            database_url: Database URL to parse
            
        Returns:
            Dict[str, Any]: Parsed database components
        """
        parsed = urlparse(database_url)
        
        return {
            'scheme': parsed.scheme,
            'username': parsed.username,
            'password': parsed.password,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path.lstrip('/') if parsed.path else None,
            'query': dict(param.split('=') for param in parsed.query.split('&') if '=' in param) if parsed.query else {}
        }
    
    @classmethod
    def get_engine_options(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get SQLAlchemy engine options for environment.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Engine options
        """
        database_url = cls.get_database_url(environment)
        db_info = cls.parse_database_url(database_url)
        
        # Base engine options
        options = {
            'pool_pre_ping': cls.POOL_PRE_PING,
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_timeout': cls.POOL_TIMEOUT,
            'echo': cls.SQLALCHEMY_ECHO
        }
        
        # Database-specific options
        if db_info['scheme'] == 'postgresql':
            options.update({
                'pool_size': cls.POOL_SIZE,
                'max_overflow': cls.MAX_OVERFLOW,
                'connect_args': {
                    'connect_timeout': cls.QUERY_TIMEOUT,
                    'application_name': 'ViewTrendsSL'
                }
            })
        elif db_info['scheme'] == 'sqlite':
            options.update({
                'pool_size': 1,
                'max_overflow': 0,
                'connect_args': {
                    'timeout': cls.QUERY_TIMEOUT,
                    'check_same_thread': False
                }
            })
        
        # Environment-specific adjustments
        if environment == 'testing':
            options.update({
                'pool_size': 1,
                'max_overflow': 0,
                'echo': False
            })
        elif environment == 'development':
            options.update({
                'echo': True
            })
        
        return options
    
    @classmethod
    def get_sqlalchemy_config(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get complete SQLAlchemy configuration.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: SQLAlchemy configuration
        """
        return {
            'SQLALCHEMY_DATABASE_URI': cls.get_database_url(environment),
            'SQLALCHEMY_TRACK_MODIFICATIONS': cls.SQLALCHEMY_TRACK_MODIFICATIONS,
            'SQLALCHEMY_RECORD_QUERIES': cls.SQLALCHEMY_RECORD_QUERIES,
            'SQLALCHEMY_ECHO': cls.SQLALCHEMY_ECHO,
            'SQLALCHEMY_ENGINE_OPTIONS': cls.get_engine_options(environment)
        }
    
    @classmethod
    def validate_database_config(cls, environment: str = None) -> None:
        """
        Validate database configuration.
        
        Args:
            environment: Environment name
            
        Raises:
            ValueError: If database configuration is invalid
        """
        database_url = cls.get_database_url(environment)
        
        if not database_url:
            raise ValueError("Database URL is required")
        
        db_info = cls.parse_database_url(database_url)
        
        # Validate database scheme
        supported_schemes = ['sqlite', 'postgresql', 'mysql']
        if db_info['scheme'] not in supported_schemes:
            raise ValueError(f"Unsupported database scheme: {db_info['scheme']}")
        
        # Validate production database
        if environment == 'production':
            if db_info['scheme'] == 'sqlite':
                raise ValueError("SQLite not recommended for production")
            
            if not db_info['hostname']:
                raise ValueError("Database hostname required for production")
    
    @classmethod
    def is_sqlite(cls, environment: str = None) -> bool:
        """
        Check if using SQLite database.
        
        Args:
            environment: Environment name
            
        Returns:
            bool: True if using SQLite
        """
        database_url = cls.get_database_url(environment)
        return database_url.startswith('sqlite')
    
    @classmethod
    def is_postgresql(cls, environment: str = None) -> bool:
        """
        Check if using PostgreSQL database.
        
        Args:
            environment: Environment name
            
        Returns:
            bool: True if using PostgreSQL
        """
        database_url = cls.get_database_url(environment)
        return database_url.startswith('postgresql')
    
    @classmethod
    def get_backup_filename(cls, environment: str = None) -> str:
        """
        Generate backup filename for database.
        
        Args:
            environment: Environment name
            
        Returns:
            str: Backup filename
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        env_suffix = f"_{environment}" if environment else ""
        
        return f"viewtrendssl_backup{env_suffix}_{timestamp}.sql"


class ConnectionManager:
    """
    Database connection management utilities.
    
    This class provides utilities for managing database connections,
    health checks, and connection pooling.
    """
    
    def __init__(self, database_url: str, engine_options: Dict[str, Any] = None):
        """
        Initialize connection manager.
        
        Args:
            database_url: Database URL
            engine_options: SQLAlchemy engine options
        """
        self.database_url = database_url
        self.engine_options = engine_options or {}
        self._engine = None
    
    @property
    def engine(self):
        """Get SQLAlchemy engine instance."""
        if self._engine is None:
            from sqlalchemy import create_engine
            self._engine = create_engine(self.database_url, **self.engine_options)
        return self._engine
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test database connection.
        
        Returns:
            Dict[str, Any]: Connection test result
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                result.fetchone()
            
            return {
                'success': True,
                'message': 'Database connection successful'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Database connection failed: {str(e)}'
            }
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get database connection information.
        
        Returns:
            Dict[str, Any]: Connection information
        """
        db_info = DatabaseConfig.parse_database_url(self.database_url)
        
        return {
            'database_type': db_info['scheme'],
            'hostname': db_info['hostname'],
            'port': db_info['port'],
            'database': db_info['database'],
            'pool_size': self.engine_options.get('pool_size', 'N/A'),
            'max_overflow': self.engine_options.get('max_overflow', 'N/A')
        }
    
    def close_connections(self) -> None:
        """Close all database connections."""
        if self._engine:
            self._engine.dispose()
            self._engine = None


def create_database_if_not_exists(database_url: str) -> None:
    """
    Create database if it doesn't exist (PostgreSQL only).
    
    Args:
        database_url: Database URL
    """
    db_info = DatabaseConfig.parse_database_url(database_url)
    
    if db_info['scheme'] != 'postgresql':
        return  # Only needed for PostgreSQL
    
    # Create database URL without database name
    server_url = f"postgresql://{db_info['username']}:{db_info['password']}@{db_info['hostname']}"
    if db_info['port']:
        server_url += f":{db_info['port']}"
    server_url += "/postgres"
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(server_url)
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {'dbname': db_info['database']}
            )
            
            if not result.fetchone():
                # Create database
                connection.execute(text(f"CREATE DATABASE {db_info['database']}"))
                print(f"Created database: {db_info['database']}")
        
        engine.dispose()
    
    except Exception as e:
        print(f"Error creating database: {str(e)}")


def get_database_health() -> Dict[str, Any]:
    """
    Get database health information.
    
    Returns:
        Dict[str, Any]: Database health status
    """
    try:
        environment = os.getenv('FLASK_ENV', 'development')
        database_url = DatabaseConfig.get_database_url(environment)
        engine_options = DatabaseConfig.get_engine_options(environment)
        
        connection_manager = ConnectionManager(database_url, engine_options)
        connection_test = connection_manager.test_connection()
        connection_info = connection_manager.get_connection_info()
        
        return {
            'status': 'healthy' if connection_test['success'] else 'unhealthy',
            'connection_test': connection_test,
            'connection_info': connection_info,
            'environment': environment
        }
    
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
