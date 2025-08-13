"""
Database Session Management for ViewTrendsSL

This module provides session management utilities including context managers,
dependency injection for FastAPI/Flask, and transaction handling.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.data_access.database.connection import get_database_connection, DatabaseConnection

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseSession:
    """Database session manager with transaction support."""
    
    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """Initialize session manager."""
        self.db_connection = db_connection or get_database_connection()
    
    def create_session(self) -> Session:
        """Create a new database session."""
        return self.db_connection.session_factory()
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions with automatic cleanup.
        
        Usage:
            with session_manager.get_session() as session:
                # Use session here
                user = session.query(User).first()
        """
        session = self.create_session()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Session error, rolling back: {e}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def get_transaction(self) -> Generator[Session, None, None]:
        """
        Context manager for database transactions with automatic commit/rollback.
        
        Usage:
            with session_manager.get_transaction() as session:
                # All operations in this block are part of one transaction
                user = User(email="test@example.com")
                session.add(user)
                # Automatically commits on success, rolls back on exception
        """
        session = self.create_session()
        try:
            yield session
            session.commit()
            logger.debug("Transaction committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction failed, rolling back: {e}")
            raise
        finally:
            session.close()
    
    def execute_in_transaction(self, func, *args, **kwargs) -> Any:
        """
        Execute a function within a database transaction.
        
        Args:
            func: Function to execute (should accept session as first parameter)
            *args: Additional arguments to pass to the function
            **kwargs: Additional keyword arguments to pass to the function
        
        Returns:
            The result of the function execution
        
        Usage:
            def create_user(session, email, password):
                user = User(email=email, password_hash=hash_password(password))
                session.add(user)
                return user
            
            user = session_manager.execute_in_transaction(create_user, "test@example.com", "password")
        """
        with self.get_transaction() as session:
            return func(session, *args, **kwargs)


# Global session manager instance
_session_manager: Optional[DatabaseSession] = None

def get_session_manager(db_connection: Optional[DatabaseConnection] = None) -> DatabaseSession:
    """Get the global session manager instance."""
    global _session_manager
    
    if _session_manager is None:
        _session_manager = DatabaseSession(db_connection)
    
    return _session_manager


# Context managers for direct use
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Convenience context manager for getting a database session.
    
    Usage:
        from src.data_access.database.session import get_db_session
        
        with get_db_session() as session:
            users = session.query(User).all()
    """
    session_manager = get_session_manager()
    with session_manager.get_session() as session:
        yield session


@contextmanager
def get_db_transaction() -> Generator[Session, None, None]:
    """
    Convenience context manager for database transactions.
    
    Usage:
        from src.data_access.database.session import get_db_transaction
        
        with get_db_transaction() as session:
            user = User(email="test@example.com")
            session.add(user)
            # Automatically commits
    """
    session_manager = get_session_manager()
    with session_manager.get_transaction() as session:
        yield session


# Dependency injection for FastAPI
def get_db_dependency() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        from fastapi import Depends
        from src.data_access.database.session import get_db_dependency
        
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db_dependency)):
            return db.query(User).all()
    """
    with get_db_session() as session:
        yield session


# Flask integration
class FlaskSessionManager:
    """Flask integration for database sessions."""
    
    def __init__(self, app=None):
        """Initialize Flask session manager."""
        self.session_manager = get_session_manager()
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the Flask app with database session management."""
        app.teardown_appcontext(self.close_db)
        app.before_request(self.before_request)
    
    def before_request(self):
        """Create a session before each request."""
        from flask import g
        if not hasattr(g, 'db_session'):
            g.db_session = self.session_manager.create_session()
    
    def close_db(self, error):
        """Close the database session after each request."""
        from flask import g
        session = getattr(g, 'db_session', None)
        if session is not None:
            if error is not None:
                session.rollback()
            session.close()
    
    def get_session(self) -> Session:
        """Get the current Flask session."""
        from flask import g
        return g.db_session


def get_flask_db() -> Session:
    """
    Get database session for Flask routes.
    
    Usage:
        from src.data_access.database.session import get_flask_db
        
        @app.route('/users')
        def get_users():
            db = get_flask_db()
            users = db.query(User).all()
            return jsonify([user.to_dict() for user in users])
    """
    from flask import g
    return g.db_session


# Utility functions
def execute_raw_sql(sql: str, params: Optional[dict] = None) -> Any:
    """
    Execute raw SQL with automatic session management.
    
    Args:
        sql: SQL query to execute
        params: Optional parameters for the query
    
    Returns:
        Query result
    
    Usage:
        result = execute_raw_sql("SELECT COUNT(*) FROM users WHERE active = :active", {"active": True})
    """
    with get_db_session() as session:
        if params:
            result = session.execute(sql, params)
        else:
            result = session.execute(sql)
        return result.fetchall()


def execute_raw_sql_transaction(sql: str, params: Optional[dict] = None) -> Any:
    """
    Execute raw SQL within a transaction.
    
    Args:
        sql: SQL query to execute
        params: Optional parameters for the query
    
    Returns:
        Query result
    """
    with get_db_transaction() as session:
        if params:
            result = session.execute(sql, params)
        else:
            result = session.execute(sql)
        return result.fetchall()


class SessionScope:
    """
    Context manager for handling database sessions with explicit control.
    
    Usage:
        with SessionScope() as session:
            user = session.query(User).first()
            user.name = "Updated Name"
            session.commit()  # Explicit commit
    """
    
    def __init__(self, commit_on_exit: bool = False):
        """
        Initialize session scope.
        
        Args:
            commit_on_exit: Whether to automatically commit on successful exit
        """
        self.commit_on_exit = commit_on_exit
        self.session: Optional[Session] = None
        self.session_manager = get_session_manager()
    
    def __enter__(self) -> Session:
        """Enter the session scope."""
        self.session = self.session_manager.create_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the session scope with cleanup."""
        if self.session:
            try:
                if exc_type is None and self.commit_on_exit:
                    self.session.commit()
                elif exc_type is not None:
                    self.session.rollback()
            except SQLAlchemyError as e:
                logger.error(f"Error during session cleanup: {e}")
                self.session.rollback()
            finally:
                self.session.close()


# Health check function
def check_database_health() -> dict:
    """
    Check database connectivity and return health status.
    
    Returns:
        Dictionary with health check results
    """
    try:
        with get_db_session() as session:
            # Simple query to test connectivity
            result = session.execute("SELECT 1")
            result.fetchone()
            
            return {
                'status': 'healthy',
                'database_type': get_database_connection().config.database_type,
                'connection_pool_size': getattr(session.bind.pool, 'size', 'N/A'),
                'checked_out_connections': getattr(session.bind.pool, 'checkedout', 'N/A')
            }
    
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
