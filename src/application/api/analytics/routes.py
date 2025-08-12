"""
Analytics Routes

This module defines the analytics API endpoints for data insights,
trend analysis, and performance metrics.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
import logging
from datetime import datetime, timedelta

from src.business.services.analytics.analytics_service import AnalyticsService
from src.application.middleware.rate_limit_middleware import rate_limit

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/v1/analytics')

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize services
analytics_service = AnalyticsService()


class AnalyticsQuerySchema(Schema):
    """Schema for analytics query validation."""
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    category_ids = fields.List(fields.Int(), required=False)
    video_types = fields.List(fields.Str(validate=lambda x: x in ['short', 'long']), required=False)
    metrics = fields.List(fields.Str(), required=False)


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    """
    Get dashboard analytics data.
    
    Returns:
        JSON response with dashboard metrics
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get dashboard data
        dashboard_data = analytics_service.get_dashboard_data(user_id=current_user_id)
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        }), 200
        
    except Exception as e:
        logger.error(f"Dashboard data error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@analytics_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    Get trending videos and patterns.
    
    Returns:
        JSON response with trend data
    """
    try:
        # Get query parameters
        period = request.args.get('period', 'week')  # week, month, year
        category = request.args.get('category')
        video_type = request.args.get('type')  # short, long
        
        # Get trends data
        trends = analytics_service.get_trends(
            period=period,
            category=category,
            video_type=video_type
        )
        
        return jsonify({
            'success': True,
            'trends': trends
        }), 200
        
    except Exception as e:
        logger.error(f"Get trends error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@analytics_bp.route('/insights', methods=['POST'])
@jwt_required()
@rate_limit('10/hour')
def get_insights():
    """
    Get data insights based on query parameters.
    
    Returns:
        JSON response with insights
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Validate request data
        schema = AnalyticsQuerySchema()
        data = schema.load(request.get_json() or {})
        
        # Get insights
        insights = analytics_service.get_insights(
            user_id=current_user_id,
            **data
        )
        
        return jsonify({
            'success': True,
            'insights': insights
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Get insights error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# Error handlers
@analytics_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle marshmallow validation errors."""
    return jsonify({'error': 'Validation error', 'details': e.messages}), 400
