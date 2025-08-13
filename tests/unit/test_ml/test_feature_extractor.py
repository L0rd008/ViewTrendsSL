"""
Unit Tests for Feature Extractor

This module contains unit tests for the FeatureExtractor class,
testing feature engineering functionality.

Author: ViewTrendsSL Team
Date: 2025
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.business.utils.feature_extractor import FeatureExtractor
from tests.fixtures.mock_data import generate_mock_video_data, generate_mock_channel_data


class TestFeatureExtractor:
    """Test cases for FeatureExtractor."""
    
    @pytest.fixture
    def feature_extractor(self):
        """Create FeatureExtractor instance."""
        return FeatureExtractor()
    
    @pytest.fixture
    def sample_video_data(self):
        """Create sample video data for testing."""
        return generate_mock_video_data()
    
    def test_extract_basic_features(self, feature_extractor, sample_video_data):
        """Test extraction of basic video features."""
        features = feature_extractor.extract_features(sample_video_data)
        
        # Check that basic features are present
        assert 'duration_seconds' in features
        assert 'is_short' in features
        assert 'title_length' in features
        assert 'description_length' in features
        assert 'tag_count' in features
        
        # Verify feature types
        assert isinstance(features['duration_seconds'], (int, float))
        assert isinstance(features['is_short'], bool)
        assert isinstance(features['title_length'], int)
        assert isinstance(features['description_length'], int)
        assert isinstance(features['tag_count'], int)
    
    def test_extract_time_features(self, feature_extractor, sample_video_data):
        """Test extraction of time-based features."""
        features = feature_extractor.extract_features(sample_video_data)
        
        # Check time-based features
        assert 'publish_hour' in features
        assert 'publish_day_of_week' in features
        assert 'is_weekend' in features
        
        # Verify ranges
        assert 0 <= features['publish_hour'] <= 23
        assert 0 <= features['publish_day_of_week'] <= 6
        assert isinstance(features['is_weekend'], bool)
    
    def test_extract_text_features(self, feature_extractor, sample_video_data):
        """Test extraction of text-based features."""
        features = feature_extractor.extract_features(sample_video_data)
        
        # Check text features
        assert 'title_word_count' in features
        assert 'title_capital_ratio' in features
        assert 'has_question_mark' in features
        assert 'has_exclamation' in features
        assert 'title_sentiment' in features
        
        # Verify types and ranges
        assert isinstance(features['title_word_count'], int)
        assert 0 <= features['title_capital_ratio'] <= 1
        assert isinstance(features['has_question_mark'], bool)
        assert isinstance(features['has_exclamation'], bool)
        assert -1 <= features['title_sentiment'] <= 1
    
    def test_extract_channel_features(self, feature_extractor, sample_video_data):
        """Test extraction of channel-based features."""
        # Mock channel data
        channel_data = generate_mock_channel_data()
        
        with patch.object(feature_extractor, '_get_channel_data', return_value=channel_data):
            features = feature_extractor.extract_features(sample_video_data)
        
        # Check channel features
        assert 'subscriber_count' in features
        assert 'channel_video_count' in features
        assert 'channel_view_count' in features
        assert 'subscriber_to_view_ratio' in features
        
        # Verify types
        assert isinstance(features['subscriber_count'], int)
        assert isinstance(features['channel_video_count'], int)
        assert isinstance(features['channel_view_count'], int)
        assert isinstance(features['subscriber_to_view_ratio'], float)
    
    def test_extract_category_features(self, feature_extractor, sample_video_data):
        """Test extraction of category-based features."""
        features = feature_extractor.extract_features(sample_video_data)
        
        # Check category features
        assert 'category_id' in features
        assert 'is_entertainment' in features
        assert 'is_education' in features
        assert 'is_news' in features
        
        # Verify types
        assert isinstance(features['category_id'], str)
        assert isinstance(features['is_entertainment'], bool)
        assert isinstance(features['is_education'], bool)
        assert isinstance(features['is_news'], bool)
    
    def test_extract_language_features(self, feature_extractor):
        """Test extraction of language-based features."""
        # Test with Sinhala content
        sinhala_video = generate_mock_video_data()
        sinhala_video['title'] = 'ශ්‍රී ලංකා වීඩියෝ එක'
        sinhala_video['description'] = 'මෙය සිංහල වීඩියෝ එකක්'
        
        features = feature_extractor.extract_features(sinhala_video)
        
        assert 'detected_language' in features
        assert 'is_sinhala' in features
        assert 'is_tamil' in features
        assert 'is_english' in features
        
        # Should detect Sinhala
        assert features['is_sinhala'] == True
        assert features['is_tamil'] == False
    
    def test_extract_engagement_features(self, feature_extractor, sample_video_data):
        """Test extraction of engagement-based features."""
        # Add engagement data
        sample_video_data['view_count'] = 10000
        sample_video_data['like_count'] = 500
        sample_video_data['comment_count'] = 50
        
        features = feature_extractor.extract_features(sample_video_data)
        
        # Check engagement features
        assert 'like_to_view_ratio' in features
        assert 'comment_to_view_ratio' in features
        assert 'engagement_rate' in features
        
        # Verify calculations
        assert features['like_to_view_ratio'] == 0.05  # 500/10000
        assert features['comment_to_view_ratio'] == 0.005  # 50/10000
        assert features['engagement_rate'] > 0
    
    def test_extract_tag_features(self, feature_extractor):
        """Test extraction of tag-based features."""
        video_data = generate_mock_video_data()
        video_data['tags'] = ['music', 'srilanka', 'entertainment', 'viral']
        
        features = feature_extractor.extract_features(video_data)
        
        assert 'tag_count' in features
        assert 'has_trending_tags' in features
        assert 'tag_diversity_score' in features
        
        assert features['tag_count'] == 4
        assert isinstance(features['has_trending_tags'], bool)
        assert isinstance(features['tag_diversity_score'], float)
    
    def test_extract_duration_features(self, feature_extractor):
        """Test extraction of duration-based features."""
        # Test short video
        short_video = generate_mock_video_data(is_short=True)
        short_video['duration_seconds'] = 45
        
        features = feature_extractor.extract_features(short_video)
        
        assert features['is_short'] == True
        assert features['duration_category'] == 'short'
        
        # Test long video
        long_video = generate_mock_video_data(is_short=False)
        long_video['duration_seconds'] = 1800  # 30 minutes
        
        features = feature_extractor.extract_features(long_video)
        
        assert features['is_short'] == False
        assert features['duration_category'] == 'long'
    
    def test_normalize_features(self, feature_extractor, sample_video_data):
        """Test feature normalization."""
        features = feature_extractor.extract_features(sample_video_data, normalize=True)
        
        # Check that numerical features are normalized
        numerical_features = ['subscriber_count', 'channel_video_count', 'duration_seconds']
        
        for feature in numerical_features:
            if feature in features:
                # Normalized features should be between 0 and 1 (approximately)
                assert 0 <= features[feature] <= 1 or features[feature] == 0
    
    def test_feature_vector_consistency(self, feature_extractor):
        """Test that feature vectors have consistent structure."""
        video1 = generate_mock_video_data()
        video2 = generate_mock_video_data()
        
        features1 = feature_extractor.extract_features(video1)
        features2 = feature_extractor.extract_features(video2)
        
        # Should have same keys
        assert set(features1.keys()) == set(features2.keys())
        
        # Should have same data types for each feature
        for key in features1.keys():
            assert type(features1[key]) == type(features2[key])
    
    def test_handle_missing_data(self, feature_extractor):
        """Test handling of missing data fields."""
        incomplete_video = {
            'video_id': 'test123',
            'title': 'Test Video',
            'duration_seconds': 300,
            'published_at': datetime.now().isoformat() + 'Z'
            # Missing description, tags, etc.
        }
        
        features = feature_extractor.extract_features(incomplete_video)
        
        # Should handle missing fields gracefully
        assert 'description_length' in features
        assert features['description_length'] == 0
        assert 'tag_count' in features
        assert features['tag_count'] == 0
    
    def test_handle_invalid_data_types(self, feature_extractor):
        """Test handling of invalid data types."""
        invalid_video = generate_mock_video_data()
        invalid_video['duration_seconds'] = 'invalid'  # Should be int
        
        with pytest.raises((ValueError, TypeError)):
            feature_extractor.extract_features(invalid_video)
    
    def test_extract_temporal_features(self, feature_extractor):
        """Test extraction of temporal features."""
        # Test video published at different times
        morning_video = generate_mock_video_data()
        morning_video['published_at'] = '2024-01-15T08:00:00Z'
        
        evening_video = generate_mock_video_data()
        evening_video['published_at'] = '2024-01-15T20:00:00Z'
        
        morning_features = feature_extractor.extract_features(morning_video)
        evening_features = feature_extractor.extract_features(evening_video)
        
        # Should have different time features
        assert morning_features['publish_hour'] == 8
        assert evening_features['publish_hour'] == 20
        
        # Both should be weekdays
        assert morning_features['is_weekend'] == False
        assert evening_features['is_weekend'] == False
    
    def test_batch_feature_extraction(self, feature_extractor):
        """Test batch feature extraction."""
        videos = [generate_mock_video_data() for _ in range(5)]
        
        features_list = feature_extractor.extract_features_batch(videos)
        
        assert len(features_list) == 5
        for features in features_list:
            assert isinstance(features, dict)
            assert 'duration_seconds' in features
            assert 'title_length' in features
    
    def test_feature_importance_weights(self, feature_extractor):
        """Test feature importance weighting."""
        video_data = generate_mock_video_data()
        
        # Extract features with importance weights
        features = feature_extractor.extract_features(video_data, include_weights=True)
        
        if 'feature_weights' in features:
            weights = features['feature_weights']
            assert isinstance(weights, dict)
            assert all(0 <= weight <= 1 for weight in weights.values())
