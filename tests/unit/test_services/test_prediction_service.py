"""
Unit Tests for Prediction Service

This module contains unit tests for the PredictionService class,
testing its core functionality in isolation.

Author: ViewTrendsSL Team
Date: 2025
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.business.services.prediction.prediction_service import PredictionService
from tests.fixtures.mock_data import (
    generate_mock_video_data,
    generate_mock_feature_vector,
    generate_video_id
)


class TestPredictionService:
    """Test cases for PredictionService."""
    
    @pytest.fixture
    def mock_database_path(self, tmp_path):
        """Create a temporary database path."""
        return str(tmp_path / "test.db")
    
    @pytest.fixture
    def mock_ml_models(self):
        """Create mock ML models."""
        shorts_model = Mock()
        longform_model = Mock()
        
        # Mock prediction methods
        shorts_model.predict.return_value = [500, 2000, 5000]  # 24h, 7d, 30d
        longform_model.predict.return_value = [1000, 5000, 15000]
        
        # Mock feature importance
        shorts_model.feature_importances_ = [0.3, 0.2, 0.15, 0.1, 0.25]
        longform_model.feature_importances_ = [0.25, 0.3, 0.2, 0.1, 0.15]
        
        return shorts_model, longform_model
    
    @pytest.fixture
    def mock_feature_extractor(self):
        """Create mock feature extractor."""
        extractor = Mock()
        extractor.extract_features.return_value = generate_mock_feature_vector()
        return extractor
    
    @pytest.fixture
    def prediction_service(self, mock_database_path, mock_ml_models, mock_feature_extractor):
        """Create PredictionService with mocked dependencies."""
        shorts_model, longform_model = mock_ml_models
        
        with patch('src.business.services.prediction.prediction_service.joblib.load') as mock_load:
            mock_load.side_effect = [shorts_model, longform_model]
            
            service = PredictionService(database_path=mock_database_path)
            service.feature_extractor = mock_feature_extractor
            
            return service
    
    def test_initialization(self, mock_database_path):
        """Test service initialization."""
        with patch('src.business.services.prediction.prediction_service.joblib.load') as mock_load:
            mock_load.side_effect = [Mock(), Mock()]
            
            service = PredictionService(database_path=mock_database_path)
            
            assert service.database_path == mock_database_path
            assert service.shorts_model is not None
            assert service.longform_model is not None
            assert mock_load.call_count == 2
    
    def test_predict_shorts_video(self, prediction_service, mock_ml_models):
        """Test prediction for Shorts video."""
        shorts_model, _ = mock_ml_models
        
        video_data = generate_mock_video_data(is_short=True)
        
        result = prediction_service.predict_viewership(video_data)
        
        # Verify the correct model was used
        shorts_model.predict.assert_called_once()
        
        # Verify result structure
        assert 'predicted_views_24h' in result
        assert 'predicted_views_7d' in result
        assert 'predicted_views_30d' in result
        assert 'confidence_score' in result
        assert 'prediction_type' in result
        assert result['prediction_type'] == 'shorts'
    
    def test_predict_longform_video(self, prediction_service, mock_ml_models):
        """Test prediction for long-form video."""
        _, longform_model = mock_ml_models
        
        video_data = generate_mock_video_data(is_short=False)
        
        result = prediction_service.predict_viewership(video_data)
        
        # Verify the correct model was used
        longform_model.predict.assert_called_once()
        
        # Verify result structure
        assert result['prediction_type'] == 'longform'
        assert result['predicted_views_24h'] > 0
        assert result['predicted_views_7d'] > result['predicted_views_24h']
        assert result['predicted_views_30d'] > result['predicted_views_7d']
    
    def test_feature_extraction_called(self, prediction_service, mock_feature_extractor):
        """Test that feature extraction is called during prediction."""
        video_data = generate_mock_video_data()
        
        prediction_service.predict_viewership(video_data)
        
        mock_feature_extractor.extract_features.assert_called_once_with(video_data)
    
    def test_prediction_with_invalid_data(self, prediction_service):
        """Test prediction with invalid video data."""
        invalid_data = {'invalid': 'data'}
        
        with pytest.raises(KeyError):
            prediction_service.predict_viewership(invalid_data)
    
    def test_prediction_with_missing_duration(self, prediction_service):
        """Test prediction with missing duration field."""
        video_data = generate_mock_video_data()
        del video_data['duration_seconds']
        
        with pytest.raises(KeyError):
            prediction_service.predict_viewership(video_data)
    
    def test_confidence_score_calculation(self, prediction_service, mock_ml_models):
        """Test confidence score calculation."""
        shorts_model, _ = mock_ml_models
        
        # Mock prediction probabilities for confidence calculation
        shorts_model.predict_proba = Mock(return_value=[[0.2, 0.8]])
        
        video_data = generate_mock_video_data(is_short=True)
        result = prediction_service.predict_viewership(video_data)
        
        assert 0 <= result['confidence_score'] <= 1
    
    def test_batch_prediction(self, prediction_service):
        """Test batch prediction functionality."""
        video_list = [
            generate_mock_video_data(is_short=True),
            generate_mock_video_data(is_short=False),
            generate_mock_video_data(is_short=True)
        ]
        
        results = prediction_service.predict_batch(video_list)
        
        assert len(results) == 3
        assert results[0]['prediction_type'] == 'shorts'
        assert results[1]['prediction_type'] == 'longform'
        assert results[2]['prediction_type'] == 'shorts'
    
    def test_prediction_caching(self, prediction_service):
        """Test that predictions are cached."""
        video_data = generate_mock_video_data()
        video_id = video_data['video_id']
        
        # First prediction
        result1 = prediction_service.predict_viewership(video_data)
        
        # Second prediction with same video
        result2 = prediction_service.predict_viewership(video_data)
        
        # Results should be identical (from cache)
        assert result1 == result2
    
    @patch('src.business.services.prediction.prediction_service.sqlite3.connect')
    def test_save_prediction_to_database(self, mock_connect, prediction_service):
        """Test saving prediction to database."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        video_data = generate_mock_video_data()
        user_id = 1
        
        result = prediction_service.predict_viewership(video_data, user_id=user_id)
        
        # Verify database interaction
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    def test_get_prediction_history(self, prediction_service):
        """Test retrieving prediction history."""
        video_id = generate_video_id()
        
        with patch('src.business.services.prediction.prediction_service.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Mock database response
            mock_cursor.fetchall.return_value = [
                (1, video_id, 1, 'shorts', 500, 2000, 5000, 0.85, '2024-01-01T10:00:00'),
                (2, video_id, 1, 'shorts', 600, 2200, 5500, 0.87, '2024-01-02T10:00:00')
            ]
            
            history = prediction_service.get_prediction_history(video_id)
            
            assert len(history) == 2
            assert history[0]['predicted_views_24h'] == 500
            assert history[1]['predicted_views_24h'] == 600
    
    def test_model_performance_metrics(self, prediction_service):
        """Test model performance metrics calculation."""
        with patch('src.business.services.prediction.prediction_service.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Mock actual vs predicted data
            mock_cursor.fetchall.return_value = [
                (1000, 950),   # actual, predicted
                (2000, 2100),
                (500, 480)
            ]
            
            metrics = prediction_service.get_model_performance_metrics('shorts')
            
            assert 'mae' in metrics
            assert 'mape' in metrics
            assert 'rmse' in metrics
            assert metrics['mae'] >= 0
            assert metrics['mape'] >= 0
            assert metrics['rmse'] >= 0
    
    def test_feature_importance_analysis(self, prediction_service, mock_ml_models):
        """Test feature importance analysis."""
        shorts_model, longform_model = mock_ml_models
        
        # Mock feature names
        feature_names = ['duration', 'title_length', 'subscriber_count', 'publish_hour', 'category']
        shorts_model.feature_names_in_ = feature_names
        longform_model.feature_names_in_ = feature_names
        
        importance = prediction_service.get_feature_importance('shorts')
        
        assert len(importance) == len(feature_names)
        assert all(isinstance(score, float) for score in importance.values())
        assert sum(importance.values()) == pytest.approx(1.0, rel=1e-2)
    
    def test_prediction_explanation(self, prediction_service):
        """Test prediction explanation generation."""
        video_data = generate_mock_video_data()
        
        result = prediction_service.predict_viewership(video_data, explain=True)
        
        assert 'explanation' in result
        assert 'top_factors' in result['explanation']
        assert 'prediction_reasoning' in result['explanation']
    
    def test_error_handling_model_load_failure(self, mock_database_path):
        """Test error handling when model loading fails."""
        with patch('src.business.services.prediction.prediction_service.joblib.load') as mock_load:
            mock_load.side_effect = FileNotFoundError("Model file not found")
            
            with pytest.raises(FileNotFoundError):
                PredictionService(database_path=mock_database_path)
    
    def test_prediction_with_extreme_values(self, prediction_service):
        """Test prediction with extreme input values."""
        video_data = generate_mock_video_data()
        
        # Test with extreme duration
        video_data['duration_seconds'] = 86400  # 24 hours
        result = prediction_service.predict_viewership(video_data)
        assert result['predicted_views_24h'] > 0
        
        # Test with zero duration
        video_data['duration_seconds'] = 0
        with pytest.raises(ValueError):
            prediction_service.predict_viewership(video_data)
    
    def test_prediction_time_series_generation(self, prediction_service):
        """Test time series prediction generation."""
        video_data = generate_mock_video_data()
        
        time_series = prediction_service.generate_prediction_time_series(video_data, days=7)
        
        assert len(time_series) == 7 * 24  # Hourly predictions for 7 days
        assert all('timestamp' in point for point in time_series)
        assert all('predicted_views' in point for point in time_series)
        assert time_series[0]['predicted_views'] <= time_series[-1]['predicted_views']
    
    def test_model_version_tracking(self, prediction_service):
        """Test model version tracking in predictions."""
        video_data = generate_mock_video_data()
        
        with patch.object(prediction_service, 'model_version', 'v1.2.3'):
            result = prediction_service.predict_viewership(video_data)
            
            assert 'model_version' in result
            assert result['model_version'] == 'v1.2.3'
    
    def test_prediction_validation(self, prediction_service):
        """Test prediction result validation."""
        video_data = generate_mock_video_data()
        
        result = prediction_service.predict_viewership(video_data)
        
        # Validate prediction structure
        required_fields = [
            'predicted_views_24h', 'predicted_views_7d', 'predicted_views_30d',
            'confidence_score', 'prediction_type', 'created_at'
        ]
        
        for field in required_fields:
            assert field in result
        
        # Validate prediction values
        assert result['predicted_views_24h'] > 0
        assert result['predicted_views_7d'] >= result['predicted_views_24h']
        assert result['predicted_views_30d'] >= result['predicted_views_7d']
        assert 0 <= result['confidence_score'] <= 1
    
    def test_concurrent_predictions(self, prediction_service):
        """Test handling of concurrent prediction requests."""
        import threading
        import time
        
        video_data = generate_mock_video_data()
        results = []
        
        def make_prediction():
            result = prediction_service.predict_viewership(video_data)
            results.append(result)
        
        # Create multiple threads
        threads = [threading.Thread(target=make_prediction) for _ in range(5)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all predictions completed
        assert len(results) == 5
        
        # All results should be identical (cached)
        for result in results[1:]:
            assert result == results[0]


class TestPredictionServiceEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_prediction_with_null_values(self, prediction_service):
        """Test prediction with null/None values in data."""
        video_data = generate_mock_video_data()
        video_data['description'] = None
        video_data['tags'] = None
        
        # Should handle null values gracefully
        result = prediction_service.predict_viewership(video_data)
        assert result is not None
    
    def test_prediction_with_unicode_content(self, prediction_service):
        """Test prediction with Unicode content (Sinhala/Tamil)."""
        video_data = generate_mock_video_data()
        video_data['title'] = 'ශ්‍රී ලංකා වීඩියෝ එක'  # Sinhala title
        video_data['description'] = 'இது ஒரு தமிழ் வீடியோ'  # Tamil description
        
        # Should handle Unicode content gracefully
        result = prediction_service.predict_viewership(video_data)
        assert result is not None
        assert result['predicted_views_24h'] > 0
    
    def test_prediction_with_empty_strings(self, prediction_service):
        """Test prediction with empty string values."""
        video_data = generate_mock_video_data()
        video_data['title'] = ''
        video_data['description'] = ''
        video_data['tags'] = []
        
        # Should handle empty values gracefully
        result = prediction_service.predict_viewership(video_data)
        assert result is not None
    
    def test_prediction_with_very_long_content(self, prediction_service):
        """Test prediction with very long title/description."""
        video_data = generate_mock_video_data()
        video_data['title'] = 'A' * 1000  # Very long title
        video_data['description'] = 'B' * 5000  # Very long description
        
        result = prediction_service.predict_viewership(video_data)
        assert result is not None
