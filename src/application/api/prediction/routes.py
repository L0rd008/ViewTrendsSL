"""
Prediction Routes

This module defines the prediction API endpoints for video viewership forecasting,
batch predictions, and prediction history management.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from src.business.services.prediction.prediction_service import PredictionService
from src.application.middleware.rate_limit_middleware import rate_limit
from src.business.utils.data_validator import validate_youtube_url
from src.external.youtube_api.client import YouTubeAPIClient

# Create blueprint
prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/v1/prediction')

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize services
prediction_service = PredictionService()
youtube_client = YouTubeAPIClient()


class VideoPredictionSchema(Schema):
    """Schema for video prediction request validation."""
    video_url = fields.Url(required=True)
    prediction_timeframes = fields.List(
        fields.Int(validate=lambda x: x in [1, 3, 7, 14, 30, 90]),
        missing=[7, 30]
    )
    include_confidence = fields.Bool(missing=True)
    include_insights = fields.Bool(missing=True)


class BatchPredictionSchema(Schema):
    """Schema for batch prediction request validation."""
    video_urls = fields.List(fields.Url(), required=True, validate=lambda x: 1 <= len(x) <= 10)
    prediction_timeframes = fields.List(
        fields.Int(validate=lambda x: x in [1, 3, 7, 14, 30, 90]),
        missing=[7, 30]
    )
    include_confidence = fields.Bool(missing=True)


class CustomPredictionSchema(Schema):
    """Schema for custom prediction with manual video metadata."""
    title = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    description = fields.Str(missing="")
    duration_seconds = fields.Int(required=True, validate=lambda x: x > 0)
    category_id = fields.Int(required=True, validate=lambda x: 1 <= x <= 44)
    tags = fields.List(fields.Str(), missing=[])
    publish_time = fields.DateTime(missing=lambda: datetime.now())
    channel_subscriber_count = fields.Int(missing=1000)
    is_short = fields.Bool(missing=False)
    prediction_timeframes = fields.List(
        fields.Int(validate=lambda x: x in [1, 3, 7, 14, 30, 90]),
        missing=[7, 30]
    )


@prediction_bp.route('/predict', methods=['POST'])
@jwt_required()
@rate_limit('20/hour')
def predict_video():
    """
    Predict viewership for a single YouTube video.
    
    Returns:
        JSON response with prediction results
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Validate request data
        schema = VideoPredictionSchema()
        data = schema.load(request.get_json())
        
        # Validate YouTube URL
        if not validate_youtube_url(data['video_url']):
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Extract video ID from URL
        video_id = youtube_client.extract_video_id(data['video_url'])
        if not video_id:
            return jsonify({'error': 'Could not extract video ID from URL'}), 400
        
        # Get video metadata from YouTube API
        video_metadata = youtube_client.get_video_details(video_id)
        if not video_metadata:
            return jsonify({'error': 'Video not found or not accessible'}), 404
        
        # Make prediction
        prediction_result = prediction_service.predict_video_performance(
            video_metadata=video_metadata,
            timeframes=data['prediction_timeframes'],
            user_id=current_user_id,
            include_confidence=data['include_confidence'],
            include_insights=data['include_insights']
        )
        
        logger.info(f"Prediction made for video {video_id} by user {current_user_id}")
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'video_title': video_metadata.get('title'),
            'predictions': prediction_result['predictions'],
            'confidence_scores': prediction_result.get('confidence_scores'),
            'insights': prediction_result.get('insights'),
            'prediction_id': prediction_result['prediction_id'],
            'created_at': prediction_result['created_at']
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/predict/batch', methods=['POST'])
@jwt_required()
@rate_limit('5/hour')
def predict_batch():
    """
    Predict viewership for multiple YouTube videos.
    
    Returns:
        JSON response with batch prediction results
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Validate request data
        schema = BatchPredictionSchema()
        data = schema.load(request.get_json())
        
        # Validate all URLs
        invalid_urls = []
        for url in data['video_urls']:
            if not validate_youtube_url(url):
                invalid_urls.append(url)
        
        if invalid_urls:
            return jsonify({
                'error': 'Invalid YouTube URLs',
                'invalid_urls': invalid_urls
            }), 400
        
        # Process batch prediction
        batch_result = prediction_service.predict_batch_videos(
            video_urls=data['video_urls'],
            timeframes=data['prediction_timeframes'],
            user_id=current_user_id,
            include_confidence=data['include_confidence']
        )
        
        logger.info(f"Batch prediction made for {len(data['video_urls'])} videos by user {current_user_id}")
        
        return jsonify({
            'success': True,
            'batch_id': batch_result['batch_id'],
            'total_videos': len(data['video_urls']),
            'successful_predictions': len(batch_result['successful_predictions']),
            'failed_predictions': len(batch_result['failed_predictions']),
            'predictions': batch_result['successful_predictions'],
            'errors': batch_result['failed_predictions'],
            'created_at': batch_result['created_at']
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/predict/custom', methods=['POST'])
@jwt_required()
@rate_limit('10/hour')
def predict_custom():
    """
    Predict viewership for custom video metadata (without YouTube URL).
    
    Returns:
        JSON response with prediction results
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Validate request data
        schema = CustomPredictionSchema()
        data = schema.load(request.get_json())
        
        # Create custom video metadata
        custom_metadata = {
            'title': data['title'],
            'description': data['description'],
            'duration_seconds': data['duration_seconds'],
            'category_id': data['category_id'],
            'tags': data['tags'],
            'publish_time': data['publish_time'],
            'channel_subscriber_count': data['channel_subscriber_count'],
            'is_short': data['is_short']
        }
        
        # Make prediction
        prediction_result = prediction_service.predict_custom_video(
            video_metadata=custom_metadata,
            timeframes=data['prediction_timeframes'],
            user_id=current_user_id
        )
        
        logger.info(f"Custom prediction made by user {current_user_id}")
        
        return jsonify({
            'success': True,
            'predictions': prediction_result['predictions'],
            'confidence_scores': prediction_result.get('confidence_scores'),
            'prediction_id': prediction_result['prediction_id'],
            'created_at': prediction_result['created_at']
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        logger.error(f"Custom prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    """
    Get user's prediction history.
    
    Returns:
        JSON response with prediction history
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Parse dates if provided
        date_filter = {}
        if start_date:
            try:
                date_filter['start_date'] = datetime.fromisoformat(start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date:
            try:
                date_filter['end_date'] = datetime.fromisoformat(end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Get prediction history
        history = prediction_service.get_user_prediction_history(
            user_id=current_user_id,
            page=page,
            per_page=per_page,
            **date_filter
        )
        
        return jsonify({
            'success': True,
            'predictions': history['predictions'],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': history['total'],
                'pages': history['pages'],
                'has_next': history['has_next'],
                'has_prev': history['has_prev']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get prediction history error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/history/<prediction_id>', methods=['GET'])
@jwt_required()
def get_prediction_details(prediction_id: str):
    """
    Get detailed information about a specific prediction.
    
    Args:
        prediction_id: Prediction ID
        
    Returns:
        JSON response with prediction details
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get prediction details
        prediction = prediction_service.get_prediction_details(
            prediction_id=prediction_id,
            user_id=current_user_id
        )
        
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404
        
        return jsonify({
            'success': True,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        logger.error(f"Get prediction details error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/models/info', methods=['GET'])
def get_model_info():
    """
    Get information about available prediction models.
    
    Returns:
        JSON response with model information
    """
    try:
        model_info = prediction_service.get_model_information()
        
        return jsonify({
            'success': True,
            'models': model_info
        }), 200
        
    except Exception as e:
        logger.error(f"Get model info error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_prediction_stats():
    """
    Get user's prediction statistics.
    
    Returns:
        JSON response with prediction statistics
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get time period from query params
        period = request.args.get('period', 'month')  # week, month, year, all
        
        if period not in ['week', 'month', 'year', 'all']:
            return jsonify({'error': 'Invalid period. Use: week, month, year, or all'}), 400
        
        # Get prediction statistics
        stats = prediction_service.get_user_prediction_stats(
            user_id=current_user_id,
            period=period
        )
        
        return jsonify({
            'success': True,
            'period': period,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get prediction stats error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/compare', methods=['POST'])
@jwt_required()
@rate_limit('10/hour')
def compare_predictions():
    """
    Compare predictions for multiple videos.
    
    Returns:
        JSON response with comparison results
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate prediction IDs
        prediction_ids = data.get('prediction_ids', [])
        if not prediction_ids or len(prediction_ids) < 2:
            return jsonify({'error': 'At least 2 prediction IDs required for comparison'}), 400
        
        if len(prediction_ids) > 5:
            return jsonify({'error': 'Maximum 5 predictions can be compared at once'}), 400
        
        # Get comparison results
        comparison = prediction_service.compare_predictions(
            prediction_ids=prediction_ids,
            user_id=current_user_id
        )
        
        if not comparison:
            return jsonify({'error': 'One or more predictions not found'}), 404
        
        return jsonify({
            'success': True,
            'comparison': comparison
        }), 200
        
    except Exception as e:
        logger.error(f"Compare predictions error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@prediction_bp.route('/export', methods=['POST'])
@jwt_required()
@rate_limit('3/hour')
def export_predictions():
    """
    Export user's predictions to CSV format.
    
    Returns:
        JSON response with export download link
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # Get export parameters
        export_format = data.get('format', 'csv')  # csv, json
        date_range = data.get('date_range', 'all')  # week, month, year, all
        include_details = data.get('include_details', True)
        
        if export_format not in ['csv', 'json']:
            return jsonify({'error': 'Invalid format. Use: csv or json'}), 400
        
        # Generate export
        export_result = prediction_service.export_user_predictions(
            user_id=current_user_id,
            format=export_format,
            date_range=date_range,
            include_details=include_details
        )
        
        return jsonify({
            'success': True,
            'export_id': export_result['export_id'],
            'download_url': export_result['download_url'],
            'expires_at': export_result['expires_at'],
            'file_size': export_result['file_size']
        }), 200
        
    except Exception as e:
        logger.error(f"Export predictions error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# Error handlers
@prediction_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle marshmallow validation errors."""
    return jsonify({'error': 'Validation error', 'details': e.messages}), 400


@prediction_bp.errorhandler(429)
def handle_rate_limit_error(e):
    """Handle rate limit errors."""
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
