"""
Pytest Configuration and Fixtures

This module provides shared fixtures and configuration for all tests
in the ViewTrendsSL project.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import pytest
import tempfile
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, MagicMock

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config.database.sqlite_config import get_sqlite_config
from src.business.services.prediction.prediction_service import PredictionService
from src.business.services.analytics.analytics_service import AnalyticsService
from src.business.services.user.user_service import UserService


@pytest.fixture(scope="session")
def test_database():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    # Initialize test database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create test tables
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE NOT NULL,
            channel_id TEXT NOT NULL,
            title TEXT NOT NULL,
            published_at TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL,
            is_short BOOLEAN NOT NULL,
            category_id TEXT,
            view_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            user_id INTEGER,
            prediction_type TEXT NOT NULL,
            predicted_views_24h INTEGER,
            predicted_views_7d INTEGER,
            predicted_views_30d INTEGER,
            confidence_score REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            subscriber_count INTEGER DEFAULT 0,
            video_count INTEGER DEFAULT 0,
            country TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    os.unlink(db_path)


@pytest.fixture
def mock_youtube_api():
    """Mock YouTube API client."""
    mock_api = Mock()
    
    # Mock videos().list() response
    mock_videos_response = {
        'items': [
            {
                'id': 'test_video_1',
                'snippet': {
                    'title': 'Test Video 1',
                    'description': 'Test description',
                    'publishedAt': '2024-01-01T10:00:00Z',
                    'channelId': 'test_channel_1',
                    'categoryId': '22',
                    'tags': ['test', 'video']
                },
                'statistics': {
                    'viewCount': '1000',
                    'likeCount': '50',
                    'commentCount': '10'
                },
                'contentDetails': {
                    'duration': 'PT5M30S'
                }
            }
        ]
    }
    
    mock_api.videos().list().execute.return_value = mock_videos_response
    
    # Mock channels().list() response
    mock_channels_response = {
        'items': [
            {
                'id': 'test_channel_1',
                'snippet': {
                    'title': 'Test Channel',
                    'description': 'Test channel description',
                    'country': 'LK'
                },
                'statistics': {
                    'subscriberCount': '10000',
                    'videoCount': '100'
                }
            }
        ]
    }
    
    mock_api.channels().list().execute.return_value = mock_channels_response
    
    return mock_api


@pytest.fixture
def sample_video_data():
    """Sample video data for testing."""
    return {
        'video_id': 'test_video_123',
        'channel_id': 'test_channel_123',
        'title': 'Test Video Title',
        'description': 'Test video description',
        'published_at': '2024-01-01T10:00:00Z',
        'duration_seconds': 330,
        'is_short': False,
        'category_id': '22',
        'view_count': 1000,
        'like_count': 50,
        'comment_count': 10,
        'tags': ['test', 'video', 'sample']
    }


@pytest.fixture
def sample_shorts_data():
    """Sample Shorts data for testing."""
    return {
        'video_id': 'test_short_123',
        'channel_id': 'test_channel_123',
        'title': 'Test Short Title',
        'description': 'Test short description',
        'published_at': '2024-01-01T15:00:00Z',
        'duration_seconds': 45,
        'is_short': True,
        'category_id': '24',
        'view_count': 5000,
        'like_count': 200,
        'comment_count': 30,
        'tags': ['shorts', 'test']
    }


@pytest.fixture
def sample_channel_data():
    """Sample channel data for testing."""
    return {
        'channel_id': 'test_channel_123',
        'title': 'Test Channel',
        'description': 'Test channel description',
        'subscriber_count': 10000,
        'video_count': 100,
        'country': 'LK',
        'created_at': datetime.now().isoformat()
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'email': 'test@example.com',
        'password': 'test_password_123',
        'is_active': True
    }


@pytest.fixture
def mock_ml_model():
    """Mock machine learning model."""
    mock_model = Mock()
    
    # Mock prediction methods
    mock_model.predict.return_value = [1000, 5000, 10000]  # 24h, 7d, 30d predictions
    mock_model.predict_proba.return_value = [[0.8, 0.2]]  # Confidence scores
    
    # Mock model attributes
    mock_model.feature_names_ = [
        'duration_seconds', 'title_length', 'publish_hour',
        'publish_day_of_week', 'is_weekend', 'subscriber_count'
    ]
    
    return mock_model


@pytest.fixture
def mock_feature_extractor():
    """Mock feature extractor."""
    mock_extractor = Mock()
    
    # Mock feature extraction
    mock_extractor.extract_features.return_value = {
        'duration_seconds': 330,
        'title_length': 15,
        'publish_hour': 10,
        'publish_day_of_week': 1,
        'is_weekend': False,
        'subscriber_count': 10000,
        'tag_count': 3,
        'description_length': 25
    }
    
    return mock_extractor


@pytest.fixture
def prediction_service(test_database, mock_ml_model, mock_feature_extractor):
    """Create prediction service with mocked dependencies."""
    service = PredictionService(database_path=test_database)
    service.shorts_model = mock_ml_model
    service.longform_model = mock_ml_model
    service.feature_extractor = mock_feature_extractor
    return service


@pytest.fixture
def analytics_service(test_database):
    """Create analytics service with test database."""
    return AnalyticsService(database_path=test_database)


@pytest.fixture
def user_service(test_database):
    """Create user service with test database."""
    return UserService(database_path=test_database)


@pytest.fixture
def api_client():
    """Create test API client."""
    from src.application.api.app import create_app
    
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def authenticated_user(api_client, sample_user_data):
    """Create and authenticate a test user."""
    # Register user
    response = api_client.post('/api/auth/register', json=sample_user_data)
    assert response.status_code == 201
    
    # Login user
    login_data = {
        'email': sample_user_data['email'],
        'password': sample_user_data['password']
    }
    response = api_client.post('/api/auth/login', json=login_data)
    assert response.status_code == 200
    
    token = response.json['access_token']
    
    return {
        'token': token,
        'headers': {'Authorization': f'Bearer {token}'},
        'user_data': sample_user_data
    }


@pytest.fixture
def sample_prediction_request():
    """Sample prediction request data."""
    return {
        'video_url': 'https://www.youtube.com/watch?v=test_video_123',
        'video_metadata': {
            'title': 'Test Video Title',
            'description': 'Test video description',
            'duration_seconds': 330,
            'category_id': '22',
            'tags': ['test', 'video']
        },
        'channel_metadata': {
            'subscriber_count': 10000,
            'video_count': 100
        }
    }


@pytest.fixture
def sample_performance_data():
    """Sample performance tracking data."""
    base_time = datetime.now()
    return [
        {
            'video_id': 'test_video_123',
            'timestamp': base_time.isoformat(),
            'view_count': 100,
            'like_count': 5,
            'comment_count': 1,
            'hours_since_publish': 1
        },
        {
            'video_id': 'test_video_123',
            'timestamp': (base_time + timedelta(hours=6)).isoformat(),
            'view_count': 500,
            'like_count': 25,
            'comment_count': 5,
            'hours_since_publish': 7
        },
        {
            'video_id': 'test_video_123',
            'timestamp': (base_time + timedelta(hours=24)).isoformat(),
            'view_count': 1000,
            'like_count': 50,
            'comment_count': 10,
            'hours_since_publish': 25
        }
    ]


# Test configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "external: mark test as requiring external services"
    )


# Test collection configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Add unit marker to unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add external marker to tests requiring external services
        if "external" in str(item.fspath) or "youtube_api" in str(item.fspath):
            item.add_marker(pytest.mark.external)
