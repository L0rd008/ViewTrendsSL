"""
Prediction Service

This module provides the core business logic for video viewership prediction,
including model loading, feature engineering, and prediction generation.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

from src.business.ml.models.shorts_model import ShortsModel
from src.business.ml.models.longform_model import LongformModel
from src.business.ml.preprocessing.feature_engineer import FeatureEngineer
from src.business.utils.data_validator import validate_video_metadata
from src.data_access.repositories.video.video_repository import VideoRepository
from src.data_access.repositories.user.user_repository import UserRepository

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for handling video viewership predictions."""
    
    def __init__(self):
        """Initialize the prediction service."""
        self.shorts_model = ShortsModel()
        self.longform_model = LongformModel()
        self.feature_engineer = FeatureEngineer()
        self.video_repository = VideoRepository()
        self.user_repository = UserRepository()
        
        # Load models
        self._load_models()
    
    def _load_models(self):
        """Load the trained ML models."""
        try:
            self.shorts_model.load_model()
            self.longform_model.load_model()
            logger.info("Prediction models loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load prediction models: {str(e)}")
            raise
    
    def predict_video_performance(
        self,
        video_metadata: Dict[str, Any],
        timeframes: List[int] = [7, 30],
        user_id: Optional[str] = None,
        include_confidence: bool = True,
        include_insights: bool = True
    ) -> Dict[str, Any]:
        """
        Predict video performance for given timeframes.
        
        Args:
            video_metadata: Video metadata dictionary
            timeframes: List of prediction timeframes in days
            user_id: User ID making the prediction
            include_confidence: Whether to include confidence scores
            include_insights: Whether to include prediction insights
            
        Returns:
            Dictionary containing predictions and metadata
        """
        try:
            # Validate input
            if not validate_video_metadata(video_metadata):
                raise ValueError("Invalid video metadata")
            
            # Determine if video is a Short
            is_short = self._is_short_video(video_metadata)
            
            # Select appropriate model
            model = self.shorts_model if is_short else self.longform_model
            
            # Engineer features
            features = self.feature_engineer.engineer_features(video_metadata)
            
            # Make predictions for each timeframe
            predictions = {}
            confidence_scores = {} if include_confidence else None
            
            for timeframe in timeframes:
                pred_result = model.predict(features, timeframe)
                predictions[f"{timeframe}_days"] = {
                    'predicted_views': int(pred_result['prediction']),
                    'timeframe_days': timeframe
                }
                
                if include_confidence:
                    confidence_scores[f"{timeframe}_days"] = pred_result.get('confidence', 0.0)
            
            # Generate prediction ID
            prediction_id = str(uuid.uuid4())
            
            # Store prediction in database
            self._store_prediction(
                prediction_id=prediction_id,
                user_id=user_id,
                video_metadata=video_metadata,
                predictions=predictions,
                model_type='shorts' if is_short else 'longform'
            )
            
            # Generate insights if requested
            insights = None
            if include_insights:
                insights = self._generate_insights(video_metadata, predictions, is_short)
            
            return {
                'prediction_id': prediction_id,
                'predictions': predictions,
                'confidence_scores': confidence_scores,
                'insights': insights,
                'model_used': 'shorts' if is_short else 'longform',
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def predict_batch_videos(
        self,
        video_urls: List[str],
        timeframes: List[int] = [7, 30],
        user_id: Optional[str] = None,
        include_confidence: bool = True
    ) -> Dict[str, Any]:
        """
        Predict performance for multiple videos.
        
        Args:
            video_urls: List of YouTube video URLs
            timeframes: List of prediction timeframes in days
            user_id: User ID making the prediction
            include_confidence: Whether to include confidence scores
            
        Returns:
            Dictionary containing batch prediction results
        """
        try:
            batch_id = str(uuid.uuid4())
            successful_predictions = []
            failed_predictions = []
            
            for url in video_urls:
                try:
                    # Extract video ID and get metadata
                    from src.external.youtube_api.client import YouTubeAPIClient
                    youtube_client = YouTubeAPIClient()
                    
                    video_id = youtube_client.extract_video_id(url)
                    if not video_id:
                        failed_predictions.append({
                            'url': url,
                            'error': 'Invalid YouTube URL'
                        })
                        continue
                    
                    video_metadata = youtube_client.get_video_details(video_id)
                    if not video_metadata:
                        failed_predictions.append({
                            'url': url,
                            'error': 'Video not found'
                        })
                        continue
                    
                    # Make prediction
                    prediction_result = self.predict_video_performance(
                        video_metadata=video_metadata,
                        timeframes=timeframes,
                        user_id=user_id,
                        include_confidence=include_confidence,
                        include_insights=False  # Skip insights for batch processing
                    )
                    
                    successful_predictions.append({
                        'url': url,
                        'video_id': video_id,
                        'video_title': video_metadata.get('title'),
                        'prediction': prediction_result
                    })
                    
                except Exception as e:
                    failed_predictions.append({
                        'url': url,
                        'error': str(e)
                    })
            
            return {
                'batch_id': batch_id,
                'successful_predictions': successful_predictions,
                'failed_predictions': failed_predictions,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Batch prediction error: {str(e)}")
            raise
    
    def predict_custom_video(
        self,
        video_metadata: Dict[str, Any],
        timeframes: List[int] = [7, 30],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Predict performance for custom video metadata.
        
        Args:
            video_metadata: Custom video metadata
            timeframes: List of prediction timeframes in days
            user_id: User ID making the prediction
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Add default values for missing fields
            default_metadata = {
                'view_count': 0,
                'like_count': 0,
                'comment_count': 0,
                'published_at': datetime.now().isoformat()
            }
            
            # Merge with provided metadata
            complete_metadata = {**default_metadata, **video_metadata}
            
            # Make prediction
            return self.predict_video_performance(
                video_metadata=complete_metadata,
                timeframes=timeframes,
                user_id=user_id,
                include_confidence=True,
                include_insights=True
            )
            
        except Exception as e:
            logger.error(f"Custom prediction error: {str(e)}")
            raise
    
    def get_user_prediction_history(
        self,
        user_id: str,
        page: int = 1,
        per_page: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get user's prediction history with pagination.
        
        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page
            start_date: Filter start date
            end_date: Filter end date
            
        Returns:
            Dictionary containing paginated prediction history
        """
        try:
            # Get predictions from repository
            predictions = self.video_repository.get_user_predictions(
                user_id=user_id,
                page=page,
                per_page=per_page,
                start_date=start_date,
                end_date=end_date
            )
            
            return predictions
            
        except Exception as e:
            logger.error(f"Get prediction history error: {str(e)}")
            raise
    
    def get_prediction_details(
        self,
        prediction_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific prediction.
        
        Args:
            prediction_id: Prediction ID
            user_id: User ID (for authorization)
            
        Returns:
            Prediction details or None if not found
        """
        try:
            prediction = self.video_repository.get_prediction_by_id(
                prediction_id=prediction_id,
                user_id=user_id
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"Get prediction details error: {str(e)}")
            raise
    
    def get_model_information(self) -> Dict[str, Any]:
        """
        Get information about available prediction models.
        
        Returns:
            Dictionary containing model information
        """
        try:
            return {
                'shorts_model': {
                    'name': 'YouTube Shorts Prediction Model',
                    'version': self.shorts_model.get_version(),
                    'accuracy': self.shorts_model.get_accuracy_metrics(),
                    'features': self.shorts_model.get_feature_names(),
                    'last_trained': self.shorts_model.get_last_trained_date()
                },
                'longform_model': {
                    'name': 'Long-form Video Prediction Model',
                    'version': self.longform_model.get_version(),
                    'accuracy': self.longform_model.get_accuracy_metrics(),
                    'features': self.longform_model.get_feature_names(),
                    'last_trained': self.longform_model.get_last_trained_date()
                }
            }
            
        except Exception as e:
            logger.error(f"Get model info error: {str(e)}")
            raise
    
    def get_user_prediction_stats(
        self,
        user_id: str,
        period: str = 'month'
    ) -> Dict[str, Any]:
        """
        Get user's prediction statistics.
        
        Args:
            user_id: User ID
            period: Time period (week, month, year, all)
            
        Returns:
            Dictionary containing prediction statistics
        """
        try:
            stats = self.video_repository.get_user_prediction_stats(
                user_id=user_id,
                period=period
            )
            
            return stats
            
        except Exception as e:
            logger.error(f"Get prediction stats error: {str(e)}")
            raise
    
    def compare_predictions(
        self,
        prediction_ids: List[str],
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Compare multiple predictions.
        
        Args:
            prediction_ids: List of prediction IDs
            user_id: User ID (for authorization)
            
        Returns:
            Comparison results or None if predictions not found
        """
        try:
            predictions = []
            
            for pred_id in prediction_ids:
                prediction = self.get_prediction_details(pred_id, user_id)
                if prediction:
                    predictions.append(prediction)
            
            if len(predictions) != len(prediction_ids):
                return None
            
            # Generate comparison analysis
            comparison = self._generate_comparison_analysis(predictions)
            
            return comparison
            
        except Exception as e:
            logger.error(f"Compare predictions error: {str(e)}")
            raise
    
    def export_user_predictions(
        self,
        user_id: str,
        format: str = 'csv',
        date_range: str = 'all',
        include_details: bool = True
    ) -> Dict[str, Any]:
        """
        Export user's predictions to specified format.
        
        Args:
            user_id: User ID
            format: Export format (csv, json)
            date_range: Date range (week, month, year, all)
            include_details: Whether to include detailed information
            
        Returns:
            Dictionary containing export information
        """
        try:
            export_id = str(uuid.uuid4())
            
            # Get predictions based on date range
            predictions = self.video_repository.get_user_predictions_for_export(
                user_id=user_id,
                date_range=date_range,
                include_details=include_details
            )
            
            # Generate export file
            file_path, file_size = self._generate_export_file(
                predictions=predictions,
                format=format,
                export_id=export_id
            )
            
            # Generate download URL (implement based on your file storage)
            download_url = f"/api/v1/prediction/download/{export_id}"
            
            # Set expiration time (24 hours)
            expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
            
            return {
                'export_id': export_id,
                'download_url': download_url,
                'expires_at': expires_at,
                'file_size': file_size
            }
            
        except Exception as e:
            logger.error(f"Export predictions error: {str(e)}")
            raise
    
    def _is_short_video(self, video_metadata: Dict[str, Any]) -> bool:
        """
        Determine if a video is a YouTube Short.
        
        Args:
            video_metadata: Video metadata
            
        Returns:
            True if video is a Short, False otherwise
        """
        duration_seconds = video_metadata.get('duration_seconds', 0)
        return duration_seconds <= 61
    
    def _store_prediction(
        self,
        prediction_id: str,
        user_id: Optional[str],
        video_metadata: Dict[str, Any],
        predictions: Dict[str, Any],
        model_type: str
    ):
        """
        Store prediction in database.
        
        Args:
            prediction_id: Unique prediction ID
            user_id: User ID (optional)
            video_metadata: Video metadata
            predictions: Prediction results
            model_type: Type of model used
        """
        try:
            self.video_repository.store_prediction(
                prediction_id=prediction_id,
                user_id=user_id,
                video_metadata=video_metadata,
                predictions=predictions,
                model_type=model_type
            )
        except Exception as e:
            logger.error(f"Failed to store prediction: {str(e)}")
            # Don't raise exception as this is not critical for the prediction itself
    
    def _generate_insights(
        self,
        video_metadata: Dict[str, Any],
        predictions: Dict[str, Any],
        is_short: bool
    ) -> Dict[str, Any]:
        """
        Generate insights based on prediction results.
        
        Args:
            video_metadata: Video metadata
            predictions: Prediction results
            is_short: Whether video is a Short
            
        Returns:
            Dictionary containing insights
        """
        insights = {
            'video_type': 'Short' if is_short else 'Long-form',
            'recommendations': [],
            'performance_indicators': {}
        }
        
        # Add basic insights based on video characteristics
        title_length = len(video_metadata.get('title', ''))
        if title_length < 30:
            insights['recommendations'].append(
                "Consider using a more descriptive title (30-60 characters optimal)"
            )
        elif title_length > 100:
            insights['recommendations'].append(
                "Title might be too long. Consider shortening for better visibility"
            )
        
        # Add performance indicators
        seven_day_views = predictions.get('7_days', {}).get('predicted_views', 0)
        thirty_day_views = predictions.get('30_days', {}).get('predicted_views', 0)
        
        if thirty_day_views > 0:
            growth_rate = ((thirty_day_views - seven_day_views) / seven_day_views) * 100
            insights['performance_indicators']['growth_rate'] = f"{growth_rate:.1f}%"
        
        return insights
    
    def _generate_comparison_analysis(
        self,
        predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comparison analysis for multiple predictions.
        
        Args:
            predictions: List of prediction dictionaries
            
        Returns:
            Comparison analysis
        """
        comparison = {
            'summary': {
                'total_predictions': len(predictions),
                'average_7_day_views': 0,
                'average_30_day_views': 0,
                'best_performing': None,
                'worst_performing': None
            },
            'detailed_comparison': predictions
        }
        
        # Calculate averages and find best/worst performing
        seven_day_views = []
        thirty_day_views = []
        
        for pred in predictions:
            pred_data = pred.get('predictions', {})
            seven_day = pred_data.get('7_days', {}).get('predicted_views', 0)
            thirty_day = pred_data.get('30_days', {}).get('predicted_views', 0)
            
            seven_day_views.append(seven_day)
            thirty_day_views.append(thirty_day)
        
        if seven_day_views:
            comparison['summary']['average_7_day_views'] = int(np.mean(seven_day_views))
            comparison['summary']['best_performing'] = predictions[np.argmax(seven_day_views)]
            comparison['summary']['worst_performing'] = predictions[np.argmin(seven_day_views)]
        
        if thirty_day_views:
            comparison['summary']['average_30_day_views'] = int(np.mean(thirty_day_views))
        
        return comparison
    
    def _generate_export_file(
        self,
        predictions: List[Dict[str, Any]],
        format: str,
        export_id: str
    ) -> tuple:
        """
        Generate export file for predictions.
        
        Args:
            predictions: List of predictions
            format: Export format
            export_id: Export ID
            
        Returns:
            Tuple of (file_path, file_size)
        """
        import os
        import json
        import csv
        
        # Create exports directory if it doesn't exist
        export_dir = 'exports'
        os.makedirs(export_dir, exist_ok=True)
        
        if format == 'csv':
            file_path = os.path.join(export_dir, f"{export_id}.csv")
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                if predictions:
                    fieldnames = predictions[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(predictions)
        
        elif format == 'json':
            file_path = os.path.join(export_dir, f"{export_id}.json")
            
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(predictions, jsonfile, indent=2, default=str)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        return file_path, file_size
