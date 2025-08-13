"""
User Repository for ViewTrendsSL

This module provides data access operations for User entities,
including authentication, user management, and profile operations.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from src.data_access.database.base import AdvancedRepository
from src.data_access.models.user import User
from src.business.utils.time_utils import get_current_utc_time

# Configure logging
logger = logging.getLogger(__name__)


class UserCreateSchema:
    """Schema for creating a new user."""
    
    def __init__(
        self,
        email: str,
        password_hash: str,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        is_active: bool = True,
        user_type: str = 'creator'
    ):
        self.email = email
        self.password_hash = password_hash
        self.username = username
        self.full_name = full_name
        self.is_active = is_active
        self.user_type = user_type


class UserUpdateSchema:
    """Schema for updating user information."""
    
    def __init__(
        self,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = None,
        user_type: Optional[str] = None,
        last_login: Optional[datetime] = None,
        preferences: Optional[Dict[str, Any]] = None
    ):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.is_active = is_active
        self.user_type = user_type
        self.last_login = last_login
        self.preferences = preferences


class UserRepository(AdvancedRepository[User]):
    """Repository for User entity operations."""
    
    def __init__(self):
        """Initialize the user repository."""
        super().__init__(User)
    
    def create(self, obj_in: UserCreateSchema, session: Optional[Session] = None) -> User:
        """
        Create a new user.
        
        Args:
            obj_in: User creation data
            session: Optional database session
            
        Returns:
            Created User instance
        """
        def _create(session: Session) -> User:
            # Check if user already exists
            existing_user = session.query(User).filter(
                or_(User.email == obj_in.email, User.username == obj_in.username)
            ).first()
            
            if existing_user:
                if existing_user.email == obj_in.email:
                    raise ValueError(f"User with email {obj_in.email} already exists")
                else:
                    raise ValueError(f"User with username {obj_in.username} already exists")
            
            # Create new user
            db_user = User(
                email=obj_in.email,
                username=obj_in.username,
                full_name=obj_in.full_name,
                password_hash=obj_in.password_hash,
                is_active=obj_in.is_active,
                user_type=obj_in.user_type,
                created_at=get_current_utc_time(),
                updated_at=get_current_utc_time()
            )
            
            session.add(db_user)
            session.flush()  # Get the ID without committing
            logger.info(f"Created new user: {db_user.email} (ID: {db_user.id})")
            return db_user
        
        if session:
            return _create(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _create(session)
    
    def update(self, db_obj: User, obj_in: UserUpdateSchema, session: Optional[Session] = None) -> User:
        """
        Update an existing user.
        
        Args:
            db_obj: Existing User instance
            obj_in: User update data
            session: Optional database session
            
        Returns:
            Updated User instance
        """
        def _update(session: Session) -> User:
            # Update fields if provided
            if obj_in.username is not None:
                # Check if username is already taken by another user
                existing_user = session.query(User).filter(
                    and_(User.username == obj_in.username, User.id != db_obj.id)
                ).first()
                if existing_user:
                    raise ValueError(f"Username {obj_in.username} is already taken")
                db_obj.username = obj_in.username
            
            if obj_in.full_name is not None:
                db_obj.full_name = obj_in.full_name
            
            if obj_in.email is not None:
                # Check if email is already taken by another user
                existing_user = session.query(User).filter(
                    and_(User.email == obj_in.email, User.id != db_obj.id)
                ).first()
                if existing_user:
                    raise ValueError(f"Email {obj_in.email} is already taken")
                db_obj.email = obj_in.email
            
            if obj_in.is_active is not None:
                db_obj.is_active = obj_in.is_active
            
            if obj_in.user_type is not None:
                db_obj.user_type = obj_in.user_type
            
            if obj_in.last_login is not None:
                db_obj.last_login = obj_in.last_login
            
            if obj_in.preferences is not None:
                db_obj.preferences = obj_in.preferences
            
            db_obj.updated_at = get_current_utc_time()
            
            logger.info(f"Updated user: {db_obj.email} (ID: {db_obj.id})")
            return db_obj
        
        if session:
            return _update(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _update(session)
    
    def get_by_email(self, email: str, session: Optional[Session] = None) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User's email address
            session: Optional database session
            
        Returns:
            User instance or None if not found
        """
        return self.get_by_field('email', email, session)
    
    def get_by_username(self, username: str, session: Optional[Session] = None) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: User's username
            session: Optional database session
            
        Returns:
            User instance or None if not found
        """
        return self.get_by_field('username', username, session)
    
    def get_active_users(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        session: Optional[Session] = None
    ) -> List[User]:
        """
        Get all active users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of active User instances
        """
        return self.get_multi_by_field('is_active', True, skip, limit, session)
    
    def get_users_by_type(
        self, 
        user_type: str, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[User]:
        """
        Get users by type (creator, analyst, admin).
        
        Args:
            user_type: Type of users to retrieve
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of User instances
        """
        return self.get_multi_by_field('user_type', user_type, skip, limit, session)
    
    def authenticate_user(
        self, 
        email: str, 
        password_hash: str, 
        session: Optional[Session] = None
    ) -> Optional[User]:
        """
        Authenticate user by email and password hash.
        
        Args:
            email: User's email address
            password_hash: Hashed password
            session: Optional database session
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        def _authenticate(session: Session) -> Optional[User]:
            user = session.query(User).filter(
                and_(
                    User.email == email,
                    User.password_hash == password_hash,
                    User.is_active == True
                )
            ).first()
            
            if user:
                # Update last login time
                user.last_login = get_current_utc_time()
                user.updated_at = get_current_utc_time()
                logger.info(f"User authenticated: {email}")
            else:
                logger.warning(f"Authentication failed for email: {email}")
            
            return user
        
        if session:
            return _authenticate(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _authenticate(session)
    
    def update_last_login(self, user_id: int, session: Optional[Session] = None) -> bool:
        """
        Update user's last login timestamp.
        
        Args:
            user_id: User's ID
            session: Optional database session
            
        Returns:
            True if updated successfully, False otherwise
        """
        def _update_last_login(session: Session) -> bool:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.last_login = get_current_utc_time()
                user.updated_at = get_current_utc_time()
                return True
            return False
        
        if session:
            return _update_last_login(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _update_last_login(session)
    
    def deactivate_user(self, user_id: int, session: Optional[Session] = None) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: User's ID
            session: Optional database session
            
        Returns:
            True if deactivated successfully, False otherwise
        """
        def _deactivate(session: Session) -> bool:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.is_active = False
                user.updated_at = get_current_utc_time()
                logger.info(f"Deactivated user: {user.email} (ID: {user_id})")
                return True
            return False
        
        if session:
            return _deactivate(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _deactivate(session)
    
    def activate_user(self, user_id: int, session: Optional[Session] = None) -> bool:
        """
        Activate a user account.
        
        Args:
            user_id: User's ID
            session: Optional database session
            
        Returns:
            True if activated successfully, False otherwise
        """
        def _activate(session: Session) -> bool:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.is_active = True
                user.updated_at = get_current_utc_time()
                logger.info(f"Activated user: {user.email} (ID: {user_id})")
                return True
            return False
        
        if session:
            return _activate(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _activate(session)
    
    def get_recent_users(
        self, 
        days: int = 7, 
        limit: int = 50,
        session: Optional[Session] = None
    ) -> List[User]:
        """
        Get users who registered recently.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of users to return
            session: Optional database session
            
        Returns:
            List of recently registered User instances
        """
        def _get_recent(session: Session) -> List[User]:
            cutoff_date = get_current_utc_time() - timedelta(days=days)
            return session.query(User).filter(
                User.created_at >= cutoff_date
            ).order_by(User.created_at.desc()).limit(limit).all()
        
        if session:
            return _get_recent(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_recent(session)
    
    def get_user_statistics(self, session: Optional[Session] = None) -> Dict[str, Any]:
        """
        Get user statistics.
        
        Args:
            session: Optional database session
            
        Returns:
            Dictionary with user statistics
        """
        def _get_stats(session: Session) -> Dict[str, Any]:
            total_users = session.query(User).count()
            active_users = session.query(User).filter(User.is_active == True).count()
            
            # Users by type
            user_types = session.query(
                User.user_type, 
                func.count(User.id)
            ).group_by(User.user_type).all()
            
            # Recent registrations (last 30 days)
            thirty_days_ago = get_current_utc_time() - timedelta(days=30)
            recent_registrations = session.query(User).filter(
                User.created_at >= thirty_days_ago
            ).count()
            
            # Recent logins (last 7 days)
            seven_days_ago = get_current_utc_time() - timedelta(days=7)
            recent_logins = session.query(User).filter(
                User.last_login >= seven_days_ago
            ).count()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'user_types': dict(user_types),
                'recent_registrations_30d': recent_registrations,
                'recent_logins_7d': recent_logins,
                'activation_rate': (active_users / total_users * 100) if total_users > 0 else 0
            }
        
        if session:
            return _get_stats(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_stats(session)
    
    def search_users(
        self, 
        search_term: str, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[User]:
        """
        Search users by email, username, or full name.
        
        Args:
            search_term: Term to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of matching User instances
        """
        search_fields = ['email', 'username', 'full_name']
        return self.search(search_term, search_fields, skip, limit, session)
    
    def update_user_preferences(
        self, 
        user_id: int, 
        preferences: Dict[str, Any],
        session: Optional[Session] = None
    ) -> bool:
        """
        Update user preferences.
        
        Args:
            user_id: User's ID
            preferences: Dictionary of preferences to update
            session: Optional database session
            
        Returns:
            True if updated successfully, False otherwise
        """
        def _update_preferences(session: Session) -> bool:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                # Merge with existing preferences
                current_prefs = user.preferences or {}
                current_prefs.update(preferences)
                user.preferences = current_prefs
                user.updated_at = get_current_utc_time()
                logger.info(f"Updated preferences for user: {user.email} (ID: {user_id})")
                return True
            return False
        
        if session:
            return _update_preferences(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _update_preferences(session)
    
    def get_users_with_no_recent_activity(
        self, 
        days: int = 30,
        session: Optional[Session] = None
    ) -> List[User]:
        """
        Get users who haven't logged in recently.
        
        Args:
            days: Number of days to consider as "recent"
            session: Optional database session
            
        Returns:
            List of inactive User instances
        """
        def _get_inactive(session: Session) -> List[User]:
            cutoff_date = get_current_utc_time() - timedelta(days=days)
            return session.query(User).filter(
                or_(
                    User.last_login < cutoff_date,
                    User.last_login.is_(None)
                )
            ).filter(User.is_active == True).all()
        
        if session:
            return _get_inactive(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_inactive(session)


# Global repository instance
_user_repository: Optional[UserRepository] = None

def get_user_repository() -> UserRepository:
    """Get the global user repository instance."""
    global _user_repository
    
    if _user_repository is None:
        _user_repository = UserRepository()
    
    return _user_repository
