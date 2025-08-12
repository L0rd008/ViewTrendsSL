"""
Authentication API Module

This module provides authentication-related API endpoints for the ViewTrendsSL application,
including user registration, login, logout, and token management.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint
from .routes import auth_bp

# Export the authentication blueprint
__all__ = ['auth_bp']
