"""
SQLite Database Configuration Module

This module contains SQLite-specific configuration and optimizations
for the ViewTrendsSL application, including performance tuning,
WAL mode configuration, and development-specific settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sqlite3
from typing import Dict, Any, Optional
from pathlib import Path


class SQLiteConfig:
    """
    SQLite-specific configuration class for ViewTrendsSL application.
    
    This class manages SQLite database settings, performance optimizations,
    and development-specific configurations.
    """
    
    # Database file paths
    DATABASE_DIRECTORY = 'data'
    DATABASE_FILENAME = 'viewtrendssl.db'
    TEST_DATABASE_FILENAME = 'viewtrendssl_test.db'
    
    # SQLite PRAGMA settings for performance optimization
    PRAGMA_SETTINGS = {
        'journal_mode': 'WAL',  # Write-Ahead Logging for better concurrency
        'synchronous': 'NORMAL',  # Balance between safety and performance
        'cache_size': -64000,  # 64MB cache (negative value = KB)
        'temp_store': 'MEMORY',  # Store temporary tables in memory
        'mmap_size': 268435456,  # 256MB memory-mapped I/O
        'page_size': 4096,  # 4KB page size (good for most workloads)
        'auto_vacuum': 'INCREMENTAL',  # Automatic space reclamation
        'busy_timeout': 30000,  # 30 second timeout for locked database
        'foreign_keys': 'ON',  # Enable foreign key constraints
        'recursive_triggers': 'ON',  # Enable recursive triggers
    }
    
    # Development-specific settings
    DEVELOPMENT_PRAGMA_SETTINGS = {
        **PRAGMA_SETTINGS,
        'synchronous': 'OFF',  # Faster writes in development
        'journal_mode': 'MEMORY',  # Faster for development
    }
    
    # Production-specific settings
    PRODUCTION_PRAGMA_SETTINGS = {
        **PRAGMA_SETTINGS,
        'synchronous': 'FULL',  # Maximum safety in production
        'secure_delete': 'ON',  # Secure deletion of data
    }
    
    # Connection pool settings
    POOL_SIZE = 1  # SQLite doesn't support multiple connections well
    MAX_OVERFLOW = 0
    POOL_TIMEOUT = 30
    POOL_RECYCLE = 3600
    
    # Backup settings
    BACKUP_ENABLED = True
    BACKUP_INTERVAL_HOURS = 6
    BACKUP_RETENTION_COUNT = 10
    
    @classmethod
    def get_database_path(cls, environment: str = None, filename: str = None) -> str:
        """
        Get full path to SQLite database file.
        
        Args:
            environment: Environment name
            filename: Database filename (optional)
            
        Returns:
            str: Full path to database file
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')
        
        if filename is None:
            if environment == 'testing':
                filename = cls.TEST_DATABASE_FILENAME
            else:
                filename = cls.DATABASE_FILENAME
        
        # Create database directory if it doesn't exist
        db_dir = Path(cls.DATABASE_DIRECTORY)
        db_dir.mkdir(parents=True, exist_ok=True)
        
        return str(db_dir / filename)
    
    @classmethod
    def get_database_url(cls, environment: str = None) -> str:
        """
        Get SQLite database URL.
        
        Args:
            environment: Environment name
            
        Returns:
            str: SQLite database URL
        """
        if environment == 'testing':
            return 'sqlite:///:memory:'
        
        db_path = cls.get_database_path(environment)
        return f'sqlite:///{db_path}'
    
    @classmethod
    def get_pragma_settings(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get PRAGMA settings for environment.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: PRAGMA settings
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')
        
        if environment == 'production':
            return cls.PRODUCTION_PRAGMA_SETTINGS
        elif environment == 'development':
            return cls.DEVELOPMENT_PRAGMA_SETTINGS
        else:
            return cls.PRAGMA_SETTINGS
    
    @classmethod
    def get_connection_args(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get SQLite connection arguments.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Connection arguments
        """
        return {
            'check_same_thread': False,  # Allow multiple threads
            'timeout': cls.POOL_TIMEOUT,
            'isolation_level': None,  # Autocommit mode
        }
    
    @classmethod
    def get_engine_options(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get SQLAlchemy engine options for SQLite.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Engine options
        """
        return {
            'pool_size': cls.POOL_SIZE,
            'max_overflow': cls.MAX_OVERFLOW,
            'pool_timeout': cls.POOL_TIMEOUT,
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_pre_ping': True,
            'connect_args': cls.get_connection_args(environment),
            'echo': environment == 'development'
        }
    
    @classmethod
    def configure_connection(cls, connection, environment: str = None) -> None:
        """
        Configure SQLite connection with PRAGMA settings.
        
        Args:
            connection: SQLite connection
            environment: Environment name
        """
        pragma_settings = cls.get_pragma_settings(environment)
        
        for pragma, value in pragma_settings.items():
            connection.execute(f'PRAGMA {pragma} = {value}')
    
    @classmethod
    def create_database_file(cls, environment: str = None) -> str:
        """
        Create SQLite database file if it doesn't exist.
        
        Args:
            environment: Environment name
            
        Returns:
            str: Path to created database file
        """
        db_path = cls.get_database_path(environment)
        
        if not os.path.exists(db_path):
            # Create empty database file
            connection = sqlite3.connect(db_path)
            cls.configure_connection(connection, environment)
            connection.close()
            
            print(f"Created SQLite database: {db_path}")
        
        return db_path
    
    @classmethod
    def get_database_info(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get SQLite database information.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Database information
        """
        db_path = cls.get_database_path(environment)
        
        info = {
            'database_type': 'SQLite',
            'database_path': db_path,
            'database_exists': os.path.exists(db_path),
            'environment': environment or os.getenv('FLASK_ENV', 'development')
        }
        
        if info['database_exists']:
            try:
                stat = os.stat(db_path)
                info.update({
                    'file_size_bytes': stat.st_size,
                    'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'last_modified': stat.st_mtime
                })
            except OSError:
                pass
        
        return info
    
    @classmethod
    def vacuum_database(cls, environment: str = None) -> Dict[str, Any]:
        """
        Vacuum SQLite database to reclaim space.
        
        Args:
            environment: Environment name
            
        Returns:
            Dict[str, Any]: Vacuum operation result
        """
        db_path = cls.get_database_path(environment)
        
        if not os.path.exists(db_path):
            return {'success': False, 'message': 'Database file does not exist'}
        
        try:
            # Get file size before vacuum
            size_before = os.path.getsize(db_path)
            
            # Perform vacuum
            connection = sqlite3.connect(db_path)
            cls.configure_connection(connection, environment)
            connection.execute('VACUUM')
            connection.close()
            
            # Get file size after vacuum
            size_after = os.path.getsize(db_path)
            space_saved = size_before - size_after
            
            return {
                'success': True,
                'message': 'Database vacuum completed successfully',
                'size_before_mb': round(size_before / (1024 * 1024), 2),
                'size_after_mb': round(size_after / (1024 * 1024), 2),
                'space_saved_mb': round(space_saved / (1024 * 1024), 2)
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Database vacuum failed: {str(e)}'
            }
    
    @classmethod
    def backup_database(cls, environment: str = None, backup_path: str = None) -> Dict[str, Any]:
        """
        Create backup of SQLite database.
        
        Args:
            environment: Environment name
            backup_path: Custom backup path (optional)
            
        Returns:
            Dict[str, Any]: Backup operation result
        """
        db_path = cls.get_database_path(environment)
        
        if not os.path.exists(db_path):
            return {'success': False, 'message': 'Database file does not exist'}
        
        if backup_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'viewtrendssl_backup_{timestamp}.db'
            backup_path = os.path.join('data/backups', backup_filename)
        
        try:
            # Create backup directory if it doesn't exist
            backup_dir = os.path.dirname(backup_path)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create backup using SQLite backup API
            source_conn = sqlite3.connect(db_path)
            backup_conn = sqlite3.connect(backup_path)
            
            source_conn.backup(backup_conn)
            
            source_conn.close()
            backup_conn.close()
            
            backup_size = os.path.getsize(backup_path)
            
            return {
                'success': True,
                'message': 'Database backup completed successfully',
                'backup_path': backup_path,
                'backup_size_mb': round(backup_size / (1024 * 1024), 2)
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Database backup failed: {str(e)}'
            }


class SQLiteConnectionManager:
    """
    SQLite-specific connection manager.
    
    This class provides SQLite-specific connection management utilities
    including connection pooling, health checks, and optimization.
    """
    
    def __init__(self, database_path: str, environment: str = None):
        """
        Initialize SQLite connection manager.
        
        Args:
            database_path: Path to SQLite database file
            environment: Environment name
        """
        self.database_path = database_path
        self.environment = environment
        self._connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get SQLite connection with optimized settings.
        
        Returns:
            sqlite3.Connection: Configured SQLite connection
        """
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.database_path,
                **SQLiteConfig.get_connection_args(self.environment)
            )
            SQLiteConfig.configure_connection(self._connection, self.environment)
        
        return self._connection
    
    def close_connection(self) -> None:
        """Close SQLite connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test SQLite database connection.
        
        Returns:
            Dict[str, Any]: Connection test result
        """
        try:
            connection = self.get_connection()
            cursor = connection.execute('SELECT 1')
            cursor.fetchone()
            cursor.close()
            
            return {
                'success': True,
                'message': 'SQLite connection successful'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'SQLite connection failed: {str(e)}'
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get SQLite database statistics.
        
        Returns:
            Dict[str, Any]: Database statistics
        """
        try:
            connection = self.get_connection()
            
            # Get database size
            cursor = connection.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            db_size = cursor.fetchone()[0]
            cursor.close()
            
            # Get table count
            cursor = connection.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            cursor.close()
            
            # Get index count
            cursor = connection.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
            index_count = cursor.fetchone()[0]
            cursor.close()
            
            return {
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'table_count': table_count,
                'index_count': index_count
            }
        
        except Exception as e:
            return {
                'error': f'Failed to get database stats: {str(e)}'
            }


def create_sqlite_engine(environment: str = None):
    """
    Create SQLAlchemy engine for SQLite.
    
    Args:
        environment: Environment name
        
    Returns:
        Engine: Configured SQLAlchemy engine
    """
    from sqlalchemy import create_engine, event
    
    database_url = SQLiteConfig.get_database_url(environment)
    engine_options = SQLiteConfig.get_engine_options(environment)
    
    engine = create_engine(database_url, **engine_options)
    
    # Add event listener to configure each connection
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """Set SQLite PRAGMA settings on each connection."""
        SQLiteConfig.configure_connection(dbapi_connection, environment)
    
    return engine


def get_sqlite_health(environment: str = None) -> Dict[str, Any]:
    """
    Get SQLite database health information.
    
    Args:
        environment: Environment name
        
    Returns:
        Dict[str, Any]: Database health status
    """
    try:
        db_path = SQLiteConfig.get_database_path(environment)
        connection_manager = SQLiteConnectionManager(db_path, environment)
        
        connection_test = connection_manager.test_connection()
        db_info = SQLiteConfig.get_database_info(environment)
        db_stats = connection_manager.get_database_stats()
        
        connection_manager.close_connection()
        
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
