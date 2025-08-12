"""
User Service

This module provides business logic for user management,
including authentication, profile management, and user preferences.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

from src.data_access.repositories.user.user_repository import UserRepository
from src.business.utils.data_validator import validate_email, validate_password

logger = logging.getLogger(__name__)


class UserService:
    """Service for handling user management operations."""
    
    def __init__(self):
        """Initialize the user service."""
        self.user_repository = UserRepository()
    
    def register_user(
        self,
        email: str,
        password: str,
        full_name: str,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            email: User email address
            password: User password
            full_name: User's full name
            preferences: User preferences (optional)
            
        Returns:
            Dictionary containing user information and registration status
        """
        try:
            # Validate input
            if not validate_email(email):
                raise ValueError("Invalid email address")
            
            if not validate_password(password):
                raise ValueError("Password does not meet requirements")
            
            if not full_name or len(full_name.strip()) < 2:
                raise ValueError("Full name is required")
            
            # Check if user already exists
            existing_user = self.user_repository.get_user_by_email(email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Generate email verification token
            verification_token = self._generate_verification_token()
            
            # Set default preferences
            default_preferences = {
                'email_notifications': True,
                'prediction_reminders': False,
                'weekly_insights': True,
                'theme': 'light',
                'language': 'en',
                'timezone': 'Asia/Colombo'
            }
            
            if preferences:
                default_preferences.update(preferences)
            
            # Create user data
            user_data = {
                'id': user_id,
                'email': email.lower().strip(),
                'password_hash': password_hash,
                'full_name': full_name.strip(),
                'is_active': False,  # Requires email verification
                'is_verified': False,
                'verification_token': verification_token,
                'preferences': default_preferences,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Save user to database
            created_user = self.user_repository.create_user(user_data)
            
            # Send verification email (implement email service)
            self._send_verification_email(email, verification_token)
            
            return {
                'user_id': user_id,
                'email': email,
                'full_name': full_name,
                'is_verified': False,
                'message': 'Registration successful. Please check your email to verify your account.',
                'verification_required': True
            }
            
        except Exception as e:
            logger.error(f"User registration error: {str(e)}")
            raise
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User information if authentication successful, None otherwise
        """
        try:
            # Get user by email
            user = self.user_repository.get_user_by_email(email.lower().strip())
            
            if not user:
                return None
            
            # Check if account is active
            if not user.get('is_active', False):
                raise ValueError("Account is not active. Please verify your email.")
            
            # Verify password
            if not check_password_hash(user['password_hash'], password):
                return None
            
            # Update last login
            self.user_repository.update_last_login(user['id'])
            
            # Return user info (without password hash)
            user_info = {k: v for k, v in user.items() if k != 'password_hash'}
            
            return user_info
            
        except Exception as e:
            logger.error(f"User authentication error: {str(e)}")
            raise
    
    def verify_email(self, verification_token: str) -> bool:
        """
        Verify user email with verification token.
        
        Args:
            verification_token: Email verification token
            
        Returns:
            True if verification successful, False otherwise
        """
        try:
            # Find user by verification token
            user = self.user_repository.get_user_by_verification_token(verification_token)
            
            if not user:
                return False
            
            # Check if token is expired (24 hours)
            created_at = user.get('created_at')
            if created_at and datetime.now() - created_at > timedelta(hours=24):
                return False
            
            # Update user status
            self.user_repository.verify_user_email(user['id'])
            
            return True
            
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User information or None if not found
        """
        try:
            user = self.user_repository.get_user_by_id(user_id)
            
            if user:
                # Remove sensitive information
                user_info = {k: v for k, v in user.items() if k != 'password_hash'}
                return user_info
            
            return None
            
        except Exception as e:
            logger.error(f"Get user by ID error: {str(e)}")
            raise
    
    def update_user_profile(
        self,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user profile information.
        
        Args:
            user_id: User ID
            updates: Dictionary of fields to update
            
        Returns:
            Updated user information
        """
        try:
            # Validate updates
            allowed_fields = ['full_name', 'preferences', 'timezone']
            filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}
            
            if not filtered_updates:
                raise ValueError("No valid fields to update")
            
            # Validate specific fields
            if 'full_name' in filtered_updates:
                if not filtered_updates['full_name'] or len(filtered_updates['full_name'].strip()) < 2:
                    raise ValueError("Full name is required")
                filtered_updates['full_name'] = filtered_updates['full_name'].strip()
            
            # Add update timestamp
            filtered_updates['updated_at'] = datetime.now()
            
            # Update user in database
            updated_user = self.user_repository.update_user(user_id, filtered_updates)
            
            if not updated_user:
                raise ValueError("User not found")
            
            # Return updated user info (without password hash)
            user_info = {k: v for k, v in updated_user.items() if k != 'password_hash'}
            
            return user_info
            
        except Exception as e:
            logger.error(f"Update user profile error: {str(e)}")
            raise
    
    def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully, False otherwise
        """
        try:
            # Get user
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Verify current password
            if not check_password_hash(user['password_hash'], current_password):
                raise ValueError("Current password is incorrect")
            
            # Validate new password
            if not validate_password(new_password):
                raise ValueError("New password does not meet requirements")
            
            # Hash new password
            new_password_hash = generate_password_hash(new_password)
            
            # Update password in database
            success = self.user_repository.update_password(user_id, new_password_hash)
            
            if success:
                logger.info(f"Password changed for user {user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            raise
    
    def request_password_reset(self, email: str) -> bool:
        """
        Request password reset for user.
        
        Args:
            email: User email
            
        Returns:
            True if reset email sent, False otherwise
        """
        try:
            # Get user by email
            user = self.user_repository.get_user_by_email(email.lower().strip())
            
            if not user:
                # Don't reveal if email exists or not
                return True
            
            # Generate reset token
            reset_token = self._generate_reset_token()
            reset_expires = datetime.now() + timedelta(hours=1)  # 1 hour expiry
            
            # Save reset token
            self.user_repository.save_password_reset_token(
                user['id'], reset_token, reset_expires
            )
            
            # Send reset email
            self._send_password_reset_email(email, reset_token)
            
            return True
            
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            return False
    
    def reset_password(self, reset_token: str, new_password: str) -> bool:
        """
        Reset password using reset token.
        
        Args:
            reset_token: Password reset token
            new_password: New password
            
        Returns:
            True if password reset successful, False otherwise
        """
        try:
            # Find user by reset token
            user = self.user_repository.get_user_by_reset_token(reset_token)
            
            if not user:
                return False
            
            # Check if token is expired
            reset_expires = user.get('reset_expires')
            if not reset_expires or datetime.now() > reset_expires:
                return False
            
            # Validate new password
            if not validate_password(new_password):
                raise ValueError("New password does not meet requirements")
            
            # Hash new password
            new_password_hash = generate_password_hash(new_password)
            
            # Update password and clear reset token
            success = self.user_repository.reset_password(user['id'], new_password_hash)
            
            if success:
                logger.info(f"Password reset for user {user['id']}")
            
            return success
            
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return False
    
    def update_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user preferences.
        
        Args:
            user_id: User ID
            preferences: New preferences
            
        Returns:
            Updated preferences
        """
        try:
            # Get current user
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Merge with existing preferences
            current_preferences = user.get('preferences', {})
            updated_preferences = {**current_preferences, **preferences}
            
            # Update in database
            self.user_repository.update_user(user_id, {
                'preferences': updated_preferences,
                'updated_at': datetime.now()
            })
            
            return updated_preferences
            
        except Exception as e:
            logger.error(f"Update preferences error: {str(e)}")
            raise
    
    def get_user_activity(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get user activity summary.
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            User activity summary
        """
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            activity = self.user_repository.get_user_activity(
                user_id=user_id,
                start_date=start_date
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Get user activity error: {str(e)}")
            raise
    
    def deactivate_user(self, user_id: str, reason: str = None) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User ID
            reason: Deactivation reason (optional)
            
        Returns:
            True if deactivation successful, False otherwise
        """
        try:
            success = self.user_repository.deactivate_user(user_id, reason)
            
            if success:
                logger.info(f"User {user_id} deactivated. Reason: {reason}")
            
            return success
            
        except Exception as e:
            logger.error(f"Deactivate user error: {str(e)}")
            return False
    
    def reactivate_user(self, user_id: str) -> bool:
        """
        Reactivate user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if reactivation successful, False otherwise
        """
        try:
            success = self.user_repository.reactivate_user(user_id)
            
            if success:
                logger.info(f"User {user_id} reactivated")
            
            return success
            
        except Exception as e:
            logger.error(f"Reactivate user error: {str(e)}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user account (soft delete).
        
        Args:
            user_id: User ID
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            success = self.user_repository.delete_user(user_id)
            
            if success:
                logger.info(f"User {user_id} deleted")
            
            return success
            
        except Exception as e:
            logger.error(f"Delete user error: {str(e)}")
            return False
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get user statistics and metrics.
        
        Args:
            user_id: User ID
            
        Returns:
            User statistics
        """
        try:
            stats = self.user_repository.get_user_statistics(user_id)
            
            return stats
            
        except Exception as e:
            logger.error(f"Get user statistics error: {str(e)}")
            raise
    
    def search_users(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search users (admin function).
        
        Args:
            query: Search query
            page: Page number
            per_page: Items per page
            filters: Additional filters
            
        Returns:
            Search results with pagination
        """
        try:
            results = self.user_repository.search_users(
                query=query,
                page=page,
                per_page=per_page,
                filters=filters
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Search users error: {str(e)}")
            raise
    
    def get_user_export_data(self, user_id: str) -> Dict[str, Any]:
        """
        Get user data for export (GDPR compliance).
        
        Args:
            user_id: User ID
            
        Returns:
            Complete user data for export
        """
        try:
            export_data = self.user_repository.get_user_export_data(user_id)
            
            return export_data
            
        except Exception as e:
            logger.error(f"Get user export data error: {str(e)}")
            raise
    
    # Private helper methods
    def _generate_verification_token(self) -> str:
        """Generate email verification token."""
        return secrets.token_urlsafe(32)
    
    def _generate_reset_token(self) -> str:
        """Generate password reset token."""
        return secrets.token_urlsafe(32)
    
    def _send_verification_email(self, email: str, token: str):
        """
        Send email verification email.
        
        Args:
            email: User email
            token: Verification token
        """
        # TODO: Implement email service
        logger.info(f"Verification email sent to {email} with token {token}")
    
    def _send_password_reset_email(self, email: str, token: str):
        """
        Send password reset email.
        
        Args:
            email: User email
            token: Reset token
        """
        # TODO: Implement email service
        logger.info(f"Password reset email sent to {email} with token {token}")
    
    def _hash_password(self, password: str) -> str:
        """
        Hash password using secure method.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return generate_password_hash(password)
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(password_hash, password)
