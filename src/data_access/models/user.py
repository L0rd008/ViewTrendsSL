"""User model for authentication and user management."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

from .base import BaseModel


class User(BaseModel):
    """User model for authentication and user management.
    
    This model handles user registration, authentication, and profile management.
    It includes password hashing, JWT token generation, and user preferences.
    """
    
    __tablename__ = 'users'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    
    # Account status
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    
    # Account metadata
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, nullable=False, default=0)
    failed_login_attempts = Column(Integer, nullable=False, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # User preferences
    timezone = Column(String(50), nullable=True, default='UTC')
    language = Column(String(10), nullable=True, default='en')
    email_notifications = Column(Boolean, nullable=False, default=True)
    
    # API usage tracking
    api_requests_today = Column(Integer, nullable=False, default=0)
    api_requests_reset_date = Column(DateTime, nullable=True)
    
    # Profile additional info
    bio = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    def __init__(self, email: str, password: str, **kwargs):
        """Initialize a new user with email and password."""
        super().__init__(**kwargs)
        self.email = email.lower().strip()
        self.set_password(password)
        self.api_requests_reset_date = datetime.utcnow().date()
    
    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def is_account_locked(self) -> bool:
        """Check if the account is currently locked due to failed login attempts."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock the account for a specified duration."""
        self.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts += 1
    
    def unlock_account(self) -> None:
        """Unlock the account and reset failed login attempts."""
        self.locked_until = None
        self.failed_login_attempts = 0
    
    def record_login(self) -> None:
        """Record a successful login."""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def generate_jwt_token(self, expires_in: int = 3600) -> str:
        """Generate a JWT token for the user.
        
        Args:
            expires_in: Token expiration time in seconds (default: 1 hour)
            
        Returns:
            JWT token string
        """
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'is_premium': self.is_premium
        }
        
        secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional['User']:
        """Verify a JWT token and return the associated user.
        
        Args:
            token: JWT token string
            
        Returns:
            User instance if token is valid, None otherwise
        """
        try:
            secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Import here to avoid circular imports
            from ..repositories.user.user_repository import UserRepository
            user_repo = UserRepository()
            return user_repo.get_by_id(payload['user_id'])
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
            return None
    
    def can_make_api_request(self) -> bool:
        """Check if the user can make an API request based on their limits."""
        # Reset daily counter if needed
        today = datetime.utcnow().date()
        if self.api_requests_reset_date != today:
            self.api_requests_today = 0
            self.api_requests_reset_date = today
        
        # Check limits based on account type
        daily_limit = 1000 if self.is_premium else 100
        return self.api_requests_today < daily_limit
    
    def increment_api_usage(self) -> None:
        """Increment the user's API usage counter."""
        today = datetime.utcnow().date()
        if self.api_requests_reset_date != today:
            self.api_requests_today = 0
            self.api_requests_reset_date = today
        
        self.api_requests_today += 1
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email.split('@')[0]
    
    @property
    def display_name(self) -> str:
        """Get the user's display name (username or full name)."""
        return self.username or self.full_name
    
    @property
    def is_admin(self) -> bool:
        """Check if the user has admin privileges."""
        # For now, check if email is in admin list
        admin_emails = os.getenv('ADMIN_EMAILS', '').split(',')
        return self.email in [email.strip() for email in admin_emails]
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary, optionally including sensitive data."""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'full_name': self.full_name,
            'display_name': self.display_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_premium': self.is_premium,
            'is_admin': self.is_admin,
            'timezone': self.timezone,
            'language': self.language,
            'bio': self.bio,
            'website': self.website,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_sensitive:
            data.update({
                'login_count': self.login_count,
                'failed_login_attempts': self.failed_login_attempts,
                'locked_until': self.locked_until.isoformat() if self.locked_until else None,
                'api_requests_today': self.api_requests_today,
                'email_notifications': self.email_notifications,
            })
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the user."""
        return f"<User(id={self.id}, email='{self.email}', active={self.is_active})>"
