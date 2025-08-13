"""
Database Connection Management for ViewTrendsSL

This module handles database connections using SQLAlchemy with support for
both SQLite (development) and PostgreSQL (production) databases.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import logging
from typing import Optional
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from config.database.database_config import DatabaseConfig

# Configure logging
logger = logging.getLogger(__name__)

# Create the declarative base for all models
Base = declarative_base()

class DatabaseConnection:
    """Manages database connections and engine configuration."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize database connection manager."""
        self.config = config or DatabaseConfig()
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        
    @property
    def engine(self) -> Engine:
        """Get or create the database engine."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    @property
    def session_factory(self) -> sessionmaker:
        """Get or create the session factory."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
        return self._session_factory
    
    def _create_engine(self) -> Engine:
        """Create and configure the database engine."""
        database_url = self.config.database_url
        
        # Engine configuration based on database type
        if self.config.database_type == 'sqlite':
            engine = create_engine(
                database_url,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 30
                },
                echo=self.config.echo_sql,
                future=True
            )
            
            # Enable foreign key constraints for SQLite
            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
                
        elif self.config.database_type == 'postgresql':
            engine = create_engine(
                database_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,
                echo=self.config.echo_sql,
                future=True
            )
        else:
            raise ValueError(f"Unsupported database type: {self.config.database_type}")
        
        logger.info(f"Database engine created for {self.config.database_type}")
        return engine
    
    def create_tables(self) -> None:
        """Create all database tables."""
        try:
            # Import all models to ensure they're registered with Base
            from src.data_access.models import (
                User, Channel, Video, Tag, VideoTag, Snapshot
            )
            
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self) -> None:
        """Drop all database tables."""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
            
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test the database connection."""
        try:
            with self.engine.connect() as connection:
                if self.config.database_type == 'sqlite':
                    result = connection.execute("SELECT 1")
                else:  # PostgreSQL
                    result = connection.execute("SELECT 1")
                
                result.fetchone()
                logger.info("Database connection test successful")
                return True
                
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_database_info(self) -> dict:
        """Get information about the database."""
        try:
            with self.engine.connect() as connection:
                info = {
                    'database_type': self.config.database_type,
                    'database_url': self.config.database_url.split('@')[-1] if '@' in self.config.database_url else self.config.database_url,
                    'pool_size': getattr(self.engine.pool, 'size', None),
                    'checked_out': getattr(self.engine.pool, 'checkedout', None),
                    'overflow': getattr(self.engine.pool, 'overflow', None),
                    'echo_sql': self.config.echo_sql
                }
                
                # Get database version
                if self.config.database_type == 'sqlite':
                    result = connection.execute("SELECT sqlite_version()")
                    info['version'] = result.fetchone()[0]
                else:  # PostgreSQL
                    result = connection.execute("SELECT version()")
                    info['version'] = result.fetchone()[0].split(' ')[1]
                
                return info
                
        except Exception as e:
            logger.error(f"Failed to get database info: {e}")
            return {'error': str(e)}
    
    def close(self) -> None:
        """Close the database connection."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("Database connection closed")


# Global database connection instance
_db_connection: Optional[DatabaseConnection] = None

def get_database_connection(config: Optional[DatabaseConfig] = None) -> DatabaseConnection:
    """Get the global database connection instance."""
    global _db_connection
    
    if _db_connection is None:
        _db_connection = DatabaseConnection(config)
    
    return _db_connection

def initialize_database(config: Optional[DatabaseConfig] = None, create_tables: bool = True) -> DatabaseConnection:
    """Initialize the database connection and optionally create tables."""
    db_connection = get_database_connection(config)
    
    # Test connection
    if not db_connection.test_connection():
        raise RuntimeError("Failed to establish database connection")
    
    # Create tables if requested
    if create_tables:
        db_connection.create_tables()
    
    logger.info("Database initialized successfully")
    return db_connection

def close_database_connection() -> None:
    """Close the global database connection."""
    global _db_connection
    
    if _db_connection:
        _db_connection.close()
        _db_connection = None
