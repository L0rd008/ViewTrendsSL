"""
Authentication Routes

This module defines the authentication API endpoints for user registration,
login, logout, token refresh, and password management.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt
)
from marshmallow import Schema, fields, ValidationError
from werkzeug.security import check_password_hash
import logging

from src.business.services.user.user_service import UserService
from src.application.middleware.rate_limit_middleware import rate_limit
from src.business.utils.data_validator import validate_email, validate_password

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize services
user_service = UserService()


class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 8)
    first_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    last_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    channel_url = fields.Url(required=False, allow_none=True)


class UserLoginSchema(Schema):
    """Schema for user login validation."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class PasswordResetSchema(Schema):
    """Schema for password reset validation."""
    email = fields.Email(required=True)


class PasswordChangeSchema(Schema):
    """Schema for password change validation."""
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=lambda x: len(x) >= 8)


@auth_bp.route('/register', methods=['POST'])
@rate_limit('5/minute')
def register():
    """
    Register a new user.
    
    Returns:
        JSON response with user data and tokens or error message
    """
    try:
        # Validate request data
        schema = UserRegistrationSchema()
        data = schema.load(request.get_json())
        
        # Additional password validation
        if not validate_password(data['password']):
            return jsonify({
                'error': 'Password must contain at least 8 characters with uppercase, lowercase, number, and special character'
            }), 400
        
        # Check if user already exists
        if user_service.get_user_by_email(data['email']):
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = user_service.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            channel_url=data.get('channel_url')
        )
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        logger.info(f"New user registered: {user.email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'channel_url': user.channel_url,
                'created_at': user.created_at.isoformat()
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/login', methods=['POST'])
@rate_limit('10/minute')
def login():
    """
    Authenticate user and return tokens.
    
    Returns:
        JSON response with user data and tokens or error message
    """
    try:
        # Validate request data
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # Get user by email
        user = user_service.get_user_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        user_service.update_last_login(user.id)
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        logger.info(f"User logged in: {user.email}")
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'channel_url': user.channel_url,
                'last_login': user.last_login.isoformat() if user.last_login else None
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    
    Returns:
        JSON response with new access token
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user still exists and is active
        user = user_service.get_user_by_id(current_user_id)
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Generate new access token
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user by blacklisting the token.
    
    Returns:
        JSON response confirming logout
    """
    try:
        # Get the JWT token
        jti = get_jwt()['jti']
        
        # Add token to blacklist (implement token blacklisting in production)
        # For now, just return success
        
        logger.info(f"User logged out: {get_jwt_identity()}")
        
        return jsonify({
            'message': 'Successfully logged out'
        }), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile.
    
    Returns:
        JSON response with user profile data
    """
    try:
        current_user_id = get_jwt_identity()
        user = user_service.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'channel_url': user.channel_url,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@rate_limit('5/minute')
def update_profile():
    """
    Update user profile.
    
    Returns:
        JSON response with updated user data
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate allowed fields
        allowed_fields = ['first_name', 'last_name', 'channel_url']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        # Update user
        user = user_service.update_user(current_user_id, update_data)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        logger.info(f"User profile updated: {user.email}")
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'channel_url': user.channel_url,
                'updated_at': user.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@rate_limit('3/minute')
def change_password():
    """
    Change user password.
    
    Returns:
        JSON response confirming password change
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Validate request data
        schema = PasswordChangeSchema()
        data = schema.load(request.get_json())
        
        # Get current user
        user = user_service.get_user_by_id(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not check_password_hash(user.password_hash, data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Validate new password
        if not validate_password(data['new_password']):
            return jsonify({
                'error': 'New password must contain at least 8 characters with uppercase, lowercase, number, and special character'
            }), 400
        
        # Update password
        user_service.update_password(current_user_id, data['new_password'])
        
        logger.info(f"Password changed for user: {user.email}")
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
@rate_limit('3/hour')
def forgot_password():
    """
    Request password reset.
    
    Returns:
        JSON response confirming reset email sent
    """
    try:
        # Validate request data
        schema = PasswordResetSchema()
        data = schema.load(request.get_json())
        
        # Check if user exists
        user = user_service.get_user_by_email(data['email'])
        
        # Always return success to prevent email enumeration
        # In production, send actual reset email if user exists
        if user:
            # Generate password reset token and send email
            # This would be implemented with email service
            logger.info(f"Password reset requested for: {user.email}")
        
        return jsonify({
            'message': 'If an account with this email exists, a password reset link has been sent'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Verify if the current token is valid.
    
    Returns:
        JSON response with token validity status
    """
    try:
        current_user_id = get_jwt_identity()
        user = user_service.get_user_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Invalid token or inactive user'}), 401
        
        return jsonify({
            'valid': True,
            'user_id': current_user_id
        }), 200
        
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Invalid token'}), 401


# Error handlers
@auth_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle marshmallow validation errors."""
    return jsonify({'error': 'Validation error', 'details': e.messages}), 400


@auth_bp.errorhandler(429)
def handle_rate_limit_error(e):
    """Handle rate limit errors."""
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
