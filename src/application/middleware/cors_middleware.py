"""
CORS Middleware

This module provides CORS (Cross-Origin Resource Sharing) middleware
for the ViewTrendsSL application.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)


def init_cors_middleware(app):
    """
    Initialize CORS middleware for the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.after_request
    def after_request(response):
        """Add CORS headers to response."""
        # Allow credentials
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        
        # Add security headers
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('X-Frame-Options', 'DENY')
        response.headers.add('X-XSS-Protection', '1; mode=block')
        
        return response
    
    @app.before_request
    def handle_preflight():
        """Handle CORS preflight requests."""
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', '*')
            response.headers.add('Access-Control-Allow-Methods', '*')
            return response
