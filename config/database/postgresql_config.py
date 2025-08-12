"""
PostgreSQL Database Configuration Module

This module contains PostgreSQL-specific configuration and optimizations
for the ViewTrendsSL application, including connection pooling,
performance tuning, and production-specific settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs


class PostgreSQLConfig:
    """
    PostgreSQL-specific configuration class for ViewTrendsSL application.
    
    This class manages PostgreSQL database settings, connection pooling,
    performance optimizations, and production-specific configurations.
    """
    
    # Default connection parameters
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 5432
    DEFAULT_DATABASE = 'viewtrendssl'
    DEFAULT_USERNAME = 'viewtrendssl_user'
    
    # Connection pool settings
    POOL_SIZE = int(os.getenv('PG_POOL_SIZE', '10'))
    MAX_OVERFLOW = int(os.getenv('PG_MAX_OVERFLOW', '20'))
    POOL_TIMEOUT = int(os.getenv('PG_POOL_TIMEOUT', '30'))
    POOL_RECYCLE = int(os.getenv('PG_POOL_RECYCLE', '3600'))  # 1 hour
    POOL_PRE_PING = True
    
    # Connection settings
    CONNECT_TIMEOUT = int(os.getenv('PG_CONNECT_TIMEOUT', '10'))
    COMMAND_TIMEOUT = int(os.getenv('PG_COMMAND_TIMEOUT', '30'))
    APPLICATION_NAME = 'ViewTrendsSL'
    
    # SSL Configuration
    SSL_MODE = os.getenv('PG_SSL_MODE', 'prefer')  # disable, allow, prefer, require, verify-ca, verify-full
    SSL_CERT = os.getenv('PG_SSL_CERT')
    SSL_KEY = os.getenv('PG_SSL_KEY')
    SSL_ROOT_CERT = os.getenv('PG_SSL_ROOT_CERT')
    
    # Performance settings
    STATEMENT_TIMEOUT = int(os.getenv('PG_STATEMENT_TIMEOUT', '30000'))  # 30 seconds in milliseconds
    LOCK_TIMEOUT = int(os.getenv('PG_LOCK_TIMEOUT', '10000'))  # 10 seconds in milliseconds
    IDLE_IN_TRANSACTION_SESSION_TIMEOUT = int(os.getenv('PG_IDLE_TIMEOUT', '300000'))  # 5 minutes
    
    # Logging and monitoring
    LOG_STATEMENT = os.getenv('PG_LOG_STATEMENT', 'none')  # none, ddl, mod, all
    LOG_MIN_DURATION_STATEMENT = int(os.getenv('PG_LOG_MIN_DURATION', '1000'))  # Log queries > 1 second
    
    # Backup and maintenance
    BACKUP_ENABLED = os.getenv('PG_BACKUP_ENABLED', 'True').lower() == 'true'
    BACKUP_RETENTION_DAYS = int(os.getenv('PG_BACKUP_RETENTION_DAYS', '30'))
    AUTO_VACUUM_ENABLED = True
    AUTO_ANALYZE_ENABLED = True
    
    @classmethod
    def get_database_url(cls, environment: str = None) -> str:
        """
        Get PostgreSQL database URL for environment.
        
        Args:
            environment: Environment name
            
        Returns:
            str: PostgreSQL database URL
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')
        
        # Check for environment-specific URL first
        env_var_name = f'DATABASE_URL_{environment.upper()}'
        database_url = os.getenv(env_var_name) or os.getenv('DATABASE_URL')
        
        if database_url:
            return database_url
        
        # Build URL from components
        host = os.getenv('PG_HOST', cls.DEFAULT_HOST)
        port = os.getenv('PG_PORT', str(cls.DEFAULT_PORT))
        database = os.getenv('PG_DATABASE', cls.DEFAULT_DATABASE)
        username = os.getenv('PG_USERNAME', cls.DEFAULT_USERNAME)
        password = os.getenv('PG_PASSWORD', '')
        
        # Add environment suffix to database name
        if environment != 'production':
            database = f"{database}_{environment}"
        
        url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        
        # Add SSL parameters if configured
        ssl_params = []
        if cls.SSL_MODE != 'disable':
            ssl_params.append(f"sslmode={cls.SSL_MODE}")
        
        if cls.SSL_CERT:
            ssl_params.append(f"sslcert={cls.SSL_CERT}")
        
        if cls.SSL_KEY:
            ssl_params.append(f"sslkey={cls.SSL_KEY}")
        
        if cls.SSL_ROOT_CERT:
            ssl_params.append(f"sslrootcert={cls.SSL_ROOT_CERT}")
        
        if ssl_params:
            url += "?" + "&".join(ssl_params)
        
        return url
    
    @classmethod
    def parse_database_url(cls, database_url: str) -> Dict[str, Any]:
        """
        Parse PostgreSQL database URL into components.
        
        Args:
            database_url: Database URL to parse
            
        Returns:
            Dict[str, Any]: Parsed database components
        """
        parsed = urlparse(database_url)
        query_params = parse_qs(parsed.query)
        
        return {
            'host': parsed.hostname or cls.DEFAULT_HOST,
            'port': parsed.port or cls.DEFAULT_PORT,
            'database': parsed.path.lstrip('/') if parsed.path else cls.DEFAULT_DATABASE,
            'username': parsed.username or cls.DEFAULT_USERNAME,
            'password': parsed.password or '',
            'ssl_mode': query_params.get('sslmode', [cls.SSL_MODE])[0],
            'ssl_cert': query_params.get('sslcert', [None])[0],
            'ssl_key': query_params.get('sslkey', [None])[0],
            'ssl_root_cert': query_params.get('sslrootcert', [None])[0]
        }
    
    @classmethod
    def get_connection_args(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get PostgreSQL connection arguments.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Connection arguments
        """
        args = {
            'connect_timeout': cls.CONNECT_TIMEOUT,
            'command_timeout': cls.COMMAND_TIMEOUT,
            'application_name': cls.APPLICATION_NAME,
            'options': f'-c statement_timeout={cls.STATEMENT_TIMEOUT}ms '
                      f'-c lock_timeout={cls.LOCK_TIMEOUT}ms '
                      f'-c idle_in_transaction_session_timeout={cls.IDLE_IN_TRANSACTION_SESSION_TIMEOUT}ms'
        }
        
        # Add SSL configuration
        if cls.SSL_MODE != 'disable':
            args['sslmode'] = cls.SSL_MODE
        
        if cls.SSL_CERT:
            args['sslcert'] = cls.SSL_CERT
        
        if cls.SSL_KEY:
            args['sslkey'] = cls.SSL_KEY
        
        if cls.SSL_ROOT_CERT:
            args['sslrootcert'] = cls.SSL_ROOT_CERT
        
        return args
    
    @classmethod
    def get_engine_options(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get SQLAlchemy engine options for PostgreSQL.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Engine options
        """
        options = {
            'pool_size': cls.POOL_SIZE,
            'max_overflow': cls.MAX_OVERFLOW,
            'pool_timeout': cls.POOL_TIMEOUT,
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_pre_ping': cls.POOL_PRE_PING,
            'connect_args': cls.get_connection_args(environment),
            'echo': environment == 'development'
        }
        
        # Environment-specific adjustments
        if environment == 'testing':
            options.update({
                'pool_size': 1,
                'max_overflow': 0,
                'echo': False
            })
        elif environment == 'production':
            options.update({
                'pool_size': cls.POOL_SIZE * 2,  # More connections in production
                'echo': False
            })
        
        return options
    
    @classmethod
    def get_database_info(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get PostgreSQL database information.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Database information
        """
        database_url = cls.get_database_url(environment)
        db_info = cls.parse_database_url(database_url)
        
        return {
            'database_type': 'PostgreSQL',
            'host': db_info['host'],
            'port': db_info['port'],
            'database': db_info['database'],
            'username': db_info['username'],
            'ssl_mode': db_info['ssl_mode'],
            'environment': environment or os.getenv('FLASK_ENV', 'development')
        }
    
    @classmethod
    def validate_connection_config(cls, environment: str = None) -> None:
        """
        Validate PostgreSQL connection configuration.
        
        Args:
            environment: Environment name
            
        Raises:
            ValueError: If configuration is invalid
        """
        database_url = cls.get_database_url(environment)
        db_info = cls.parse_database_url(database_url)
        
        # Validate required fields
        if not db_info['host']:
            raise ValueError("PostgreSQL host is required")
        
        if not db_info['database']:
            raise ValueError("PostgreSQL database name is required")
        
        if not db_info['username']:
            raise ValueError("PostgreSQL username is required")
        
        # Validate SSL configuration
        if db_info['ssl_mode'] in ['verify-ca', 'verify-full']:
            if not db_info['ssl_root_cert']:
                raise ValueError("SSL root certificate required for SSL verification")
        
        # Validate production requirements
        if environment == 'production':
            if not db_info['password']:
                raise ValueError("PostgreSQL password is required for production")
            
            if db_info['ssl_mode'] == 'disable':
                raise ValueError("SSL should be enabled for production")
    
    @classmethod
    def get_backup_command(cls, environment: str = None, output_file: str = None) -> str:
        """
        Get pg_dump command for database backup.
        
        Args:
            environment: Environment name
            output_file: Output file path
            
        Returns:
            str: pg_dump command
        """
        db_info = cls.parse_database_url(cls.get_database_url(environment))
        
        if output_file is None:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"viewtrendssl_backup_{environment}_{timestamp}.sql"
        
        cmd_parts = [
            'pg_dump',
            f"--host={db_info['host']}",
            f"--port={db_info['port']}",
            f"--username={db_info['username']}",
            f"--dbname={db_info['database']}",
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
            f"--file={output_file}"
        ]
        
        return ' '.join(cmd_parts)
    
    @classmethod
    def get_restore_command(cls, backup_file: str, environment: str = None) -> str:
        """
        Get psql command for database restore.
        
        Args:
            backup_file: Backup file path
            environment: Environment name
            
        Returns:
            str: psql restore command
        """
        db_info = cls.parse_database_url(cls.get_database_url(environment))
        
        cmd_parts = [
            'psql',
            f"--host={db_info['host']}",
            f"--port={db_info['port']}",
            f"--username={db_info['username']}",
            f"--dbname={db_info['database']}",
            f"--file={backup_file}"
        ]
        
        return ' '.join(cmd_parts)


class PostgreSQLConnectionManager:
    """
    PostgreSQL-specific connection manager.
    
    This class provides PostgreSQL-specific connection management utilities
    including connection pooling, health checks, and performance monitoring.
    """
    
    def __init__(self, database_url: str, environment: str = None):
        """
        Initialize PostgreSQL connection manager.
        
        Args:
            database_url: Database URL
            environment: Environment name
        """
        self.database_url = database_url
        self.environment = environment
        self._engine = None
    
    @property
    def engine(self):
        """Get SQLAlchemy engine instance."""
        if self._engine is None:
            from sqlalchemy import create_engine
            engine_options = PostgreSQLConfig.get_engine_options(self.environment)
            self._engine = create_engine(self.database_url, **engine_options)
        return self._engine
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test PostgreSQL database connection.
        
        Returns:
            Dict[str, Any]: Connection test result
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute("SELECT version()")
                version = result.fetchone()[0]
            
            return {
                'success': True,
                'message': 'PostgreSQL connection successful',
                'version': version
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'PostgreSQL connection failed: {str(e)}'
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get PostgreSQL database statistics.
        
        Returns:
            Dict[str, Any]: Database statistics
        """
        try:
            with self.engine.connect() as connection:
                # Get database size
                result = connection.execute(
                    "SELECT pg_size_pretty(pg_database_size(current_database())) as size, "
                    "pg_database_size(current_database()) as size_bytes"
                )
                size_info = result.fetchone()
                
                # Get table count
                result = connection.execute(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = 'public'"
                )
                table_count = result.fetchone()[0]
                
                # Get index count
                result = connection.execute(
                    "SELECT COUNT(*) FROM pg_indexes "
                    "WHERE schemaname = 'public'"
                )
                index_count = result.fetchone()[0]
                
                # Get connection count
                result = connection.execute(
                    "SELECT COUNT(*) FROM pg_stat_activity "
                    "WHERE datname = current_database()"
                )
                connection_count = result.fetchone()[0]
                
                return {
                    'database_size': size_info[0],
                    'database_size_bytes': size_info[1],
                    'table_count': table_count,
                    'index_count': index_count,
                    'active_connections': connection_count
                }
        
        except Exception as e:
            return {
                'error': f'Failed to get database stats: {str(e)}'
            }
    
    def get_slow_queries(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get slow queries from PostgreSQL statistics.
        
        Args:
            limit: Number of queries to return
            
        Returns:
            Dict[str, Any]: Slow queries information
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(f"""
                    SELECT query, calls, total_time, mean_time, rows
                    FROM pg_stat_statements
                    ORDER BY mean_time DESC
                    LIMIT {limit}
                """)
                
                queries = []
                for row in result:
                    queries.append({
                        'query': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
                        'calls': row[1],
                        'total_time': round(row[2], 2),
                        'mean_time': round(row[3], 2),
                        'rows': row[4]
                    })
                
                return {
                    'slow_queries': queries,
                    'count': len(queries)
                }
        
        except Exception as e:
            return {
                'error': f'Failed to get slow queries: {str(e)}',
                'note': 'pg_stat_statements extension may not be installed'
            }
    
    def close_connections(self) -> None:
        """Close all database connections."""
        if self._engine:
            self._engine.dispose()
            self._engine = None


def create_postgresql_engine(environment: str = None):
    """
    Create SQLAlchemy engine for PostgreSQL.
    
    Args:
        environment: Environment name
        
    Returns:
        Engine: Configured SQLAlchemy engine
    """
    from sqlalchemy import create_engine
    
    database_url = PostgreSQLConfig.get_database_url(environment)
    engine_options = PostgreSQLConfig.get_engine_options(environment)
    
    return create_engine(database_url, **engine_options)


def get_postgresql_health(environment: str = None) -> Dict[str, Any]:
    """
    Get PostgreSQL database health information.
    
    Args:
        environment: Environment name
        
    Returns:
        Dict[str, Any]: Database health status
    """
    try:
        database_url = PostgreSQLConfig.get_database_url(environment)
        connection_manager = PostgreSQLConnectionManager(database_url, environment)
        
        connection_test = connection_manager.test_connection()
        db_info = PostgreSQLConfig.get_database_info(environment)
        db_stats = connection_manager.get_database_stats()
        
        connection_manager.close_connections()
        
        return {
            'status': 'healthy' if connection_test['success'] else 'unhealthy',
            'connection_test': connection_test,
            'database_info': db_info,
            'database_stats': db_stats,
            'environment': environment or os.getenv('FLASK_ENV', 'development')
        }
    
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }


def create_database_if_not_exists(environment: str = None) -> Dict[str, Any]:
    """
    Create PostgreSQL database if it doesn't exist.
    
    Args:
        environment: Environment name
        
    Returns:
        Dict[str, Any]: Operation result
    """
    try:
        database_url = PostgreSQLConfig.get_database_url(environment)
        db_info = PostgreSQLConfig.parse_database_url(database_url)
        
        # Connect to postgres database to create target database
        postgres_url = database_url.replace(f"/{db_info['database']}", "/postgres")
        
        from sqlalchemy import create_engine, text
        engine = create_engine(postgres_url)
        
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {'dbname': db_info['database']}
            )
            
            if not result.fetchone():
                # Create database
                connection.execute(text(f'CREATE DATABASE "{db_info["database"]}"'))
                return {
                    'success': True,
                    'message': f'Created database: {db_info["database"]}'
                }
            else:
                return {
                    'success': True,
                    'message': f'Database already exists: {db_info["database"]}'
                }
        
        engine.dispose()
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Error creating database: {str(e)}'
        }
