"""
Main Flask Application

This module creates and configures the main Flask application for ViewTrendsSL,
including all blueprints, middleware, and error handlers.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
import os
from datetime import timedelta

# Import configuration
from config.api.api_config import APIConfig
from config.api.cors_config import CORSConfig
from config.api.authentication_config import AuthenticationConfig
from config.database.database_config import DatabaseConfig

# Import blueprints
from src.application.api.auth import auth_bp
from src.application.api.prediction import prediction_bp
from src.application.api.analytics import analytics_bp

# Import middleware
from src.application.middleware.auth_middleware import init_auth_middleware
from src.application.middleware.cors_middleware import init_cors_middleware
from src.application.middleware.rate_limit_middleware import init_rate_limiting

# Import database
from src.data_access.database.connection import init_database


def create_app(config_name='development'):
    """
    Create and configure Flask application.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(APIConfig)
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = AuthenticationConfig.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = AuthenticationConfig.JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = AuthenticationConfig.JWT_REFRESH_TOKEN_EXPIRES
    
    # Initialize extensions
    jwt = JWTManager(app)
    
    # Configure CORS
    CORS(app, 
         origins=CORSConfig.ALLOWED_ORIGINS,
         methods=CORSConfig.ALLOWED_METHODS,
         allow_headers=CORSConfig.ALLOWED_HEADERS,
         supports_credentials=CORSConfig.SUPPORTS_CREDENTIALS)
    
    # Initialize middleware
    init_auth_middleware(app)
    init_cors_middleware(app)
    init_rate_limiting(app)
    
    # Initialize database
    init_database(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(analytics_bp)
    
    # Configure logging
    configure_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register JWT handlers
    register_jwt_handlers(jwt)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'ViewTrendsSL API',
            'version': '1.0.0',
            'timestamp': request.headers.get('X-Request-Time', 'unknown')
        }), 200
    
    # API info endpoint
    @app.route('/api/v1/info', methods=['GET'])
    def api_info():
        """API information endpoint."""
        return jsonify({
            'name': 'ViewTrendsSL API',
            'version': '1.0.0',
            'description': 'YouTube Viewership Forecasting API for Sri Lankan Audience',
            'endpoints': {
                'auth': '/api/v1/auth',
                'prediction': '/api/v1/prediction',
                'analytics': '/api/v1/analytics'
            },
            'documentation': '/api/v1/docs',
            'status': 'active'
        }), 200
    
    return app


def configure_logging(app):
    """Configure application logging."""
    if not app.debug and not app.testing:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log'),
                logging.StreamHandler()
            ]
        )
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
    
    # Set specific logger levels
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors."""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors."""
        return jsonify({
            'error': 'Forbidden',
            'message': 'Access denied'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors."""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit exceeded errors."""
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors."""
        app.logger.error(f'Internal server error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle service unavailable errors."""
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable'
        }), 503


def register_jwt_handlers(jwt):
    """Register JWT-specific handlers."""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired token."""
        return jsonify({
            'error': 'Token Expired',
            'message': 'The token has expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token."""
        return jsonify({
            'error': 'Invalid Token',
            'message': 'The token is invalid'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token."""
        return jsonify({
            'error': 'Missing Token',
            'message': 'Authorization token is required'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """Handle non-fresh token."""
        return jsonify({
            'error': 'Fresh Token Required',
            'message': 'A fresh token is required'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked token."""
        return jsonify({
            'error': 'Token Revoked',
            'message': 'The token has been revoked'
        }), 401


# Application factory for different environments
def create_development_app():
    """Create development application."""
    app = create_app('development')
    app.config['DEBUG'] = True
    return app


def create_production_app():
    """Create production application."""
    app = create_app('production')
    app.config['DEBUG'] = False
    return app


def create_testing_app():
    """Create testing application."""
    app = create_app('testing')
    app.config['TESTING'] = True
    return app


# Default application instance
app = create_app()

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
