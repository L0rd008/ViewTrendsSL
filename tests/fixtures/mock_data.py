"""
Mock Data Generators

This module provides functions to generate mock data for testing
the ViewTrendsSL application.

Author: ViewTrendsSL Team
Date: 2025
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List
from faker import Faker

fake = Faker()


def generate_video_id() -> str:
    """Generate a mock YouTube video ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=11))


def generate_channel_id() -> str:
    """Generate a mock YouTube channel ID."""
    return 'UC' + ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=22))


def generate_mock_video_data(
    is_short: bool = None,
    channel_id: str = None,
    published_days_ago: int = None
) -> Dict[str, Any]:
    """
    Generate mock video data.
    
    Args:
        is_short: Whether the video is a Short
        channel_id: Specific channel ID to use
        published_days_ago: Days ago the video was published
        
    Returns:
        Dictionary containing mock video data
    """
    if is_short is None:
        is_short = random.choice([True, False])
    
    if channel_id is None:
        channel_id = generate_channel_id()
    
    if published_days_ago is None:
        published_days_ago = random.randint(1, 365)
    
    published_at = datetime.now() - timedelta(days=published_days_ago)
    
    # Generate duration based on video type
    if is_short:
        duration_seconds = random.randint(15, 60)
    else:
        duration_seconds = random.randint(61, 3600)  # 1 minute to 1 hour
    
    # Generate realistic view counts
    base_views = random.randint(100, 1000000)
    view_count = base_views
    like_count = int(view_count * random.uniform(0.01, 0.1))  # 1-10% like rate
    comment_count = int(view_count * random.uniform(0.001, 0.05))  # 0.1-5% comment rate
    
    # Generate Sri Lankan content indicators
    sri_lankan_keywords = [
        'Sri Lanka', 'Colombo', 'Kandy', 'Galle', 'Lankan', 'Ceylon',
        'Sinhala', 'Tamil', 'Perahera', 'Cricket', 'Curry'
    ]
    
    title_words = fake.words(nb=random.randint(3, 8))
    if random.random() < 0.3:  # 30% chance of Sri Lankan content
        title_words.append(random.choice(sri_lankan_keywords))
    
    title = ' '.join(title_words).title()
    
    return {
        'video_id': generate_video_id(),
        'channel_id': channel_id,
        'title': title,
        'description': fake.text(max_nb_chars=200),
        'published_at': published_at.isoformat() + 'Z',
        'duration_seconds': duration_seconds,
        'is_short': is_short,
        'category_id': str(random.choice([1, 2, 10, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28])),
        'view_count': view_count,
        'like_count': like_count,
        'comment_count': comment_count,
        'tags': fake.words(nb=random.randint(3, 10)),
        'thumbnail_url': f'https://i.ytimg.com/vi/{generate_video_id()}/maxresdefault.jpg',
        'created_at': datetime.now().isoformat()
    }


def generate_mock_channel_data(
    subscriber_count: int = None,
    country: str = 'LK'
) -> Dict[str, Any]:
    """
    Generate mock channel data.
    
    Args:
        subscriber_count: Specific subscriber count
        country: Channel country code
        
    Returns:
        Dictionary containing mock channel data
    """
    if subscriber_count is None:
        subscriber_count = random.randint(1000, 1000000)
    
    video_count = random.randint(10, 1000)
    
    # Generate Sri Lankan channel names
    sri_lankan_names = [
        'Lanka TV', 'Ceylon News', 'Colombo Today', 'Island Life',
        'Sri Lankan Cooking', 'Kandy Vlogs', 'Galle Adventures'
    ]
    
    if country == 'LK' and random.random() < 0.4:
        title = random.choice(sri_lankan_names)
    else:
        title = fake.company()
    
    return {
        'channel_id': generate_channel_id(),
        'title': title,
        'description': fake.text(max_nb_chars=300),
        'subscriber_count': subscriber_count,
        'video_count': video_count,
        'country': country,
        'view_count': subscriber_count * random.randint(10, 100),
        'created_at': datetime.now().isoformat()
    }


def generate_mock_user_data() -> Dict[str, Any]:
    """Generate mock user data."""
    return {
        'email': fake.email(),
        'password': fake.password(length=12),
        'is_active': random.choice([True, False]),
        'created_at': datetime.now().isoformat()
    }


def generate_mock_prediction_data(
    video_id: str = None,
    user_id: int = None
) -> Dict[str, Any]:
    """
    Generate mock prediction data.
    
    Args:
        video_id: Specific video ID
        user_id: Specific user ID
        
    Returns:
        Dictionary containing mock prediction data
    """
    if video_id is None:
        video_id = generate_video_id()
    
    # Generate realistic predictions with growth pattern
    views_24h = random.randint(100, 10000)
    views_7d = views_24h * random.randint(2, 10)
    views_30d = views_7d * random.randint(1, 5)
    
    return {
        'video_id': video_id,
        'user_id': user_id,
        'prediction_type': random.choice(['shorts', 'longform']),
        'predicted_views_24h': views_24h,
        'predicted_views_7d': views_7d,
        'predicted_views_30d': views_30d,
        'confidence_score': random.uniform(0.6, 0.95),
        'created_at': datetime.now().isoformat()
    }


def generate_mock_performance_data(
    video_id: str = None,
    num_snapshots: int = 10
) -> List[Dict[str, Any]]:
    """
    Generate mock performance tracking data.
    
    Args:
        video_id: Specific video ID
        num_snapshots: Number of snapshots to generate
        
    Returns:
        List of performance snapshots
    """
    if video_id is None:
        video_id = generate_video_id()
    
    snapshots = []
    base_time = datetime.now() - timedelta(days=7)
    
    # Start with initial values
    current_views = random.randint(10, 100)
    current_likes = max(1, int(current_views * 0.05))
    current_comments = max(0, int(current_views * 0.01))
    
    for i in range(num_snapshots):
        # Simulate growth over time
        growth_factor = random.uniform(1.1, 2.0)
        current_views = int(current_views * growth_factor)
        current_likes = int(current_views * random.uniform(0.02, 0.08))
        current_comments = int(current_views * random.uniform(0.005, 0.03))
        
        snapshot_time = base_time + timedelta(hours=i * 6)  # Every 6 hours
        hours_since_publish = (snapshot_time - base_time).total_seconds() / 3600
        
        snapshots.append({
            'video_id': video_id,
            'timestamp': snapshot_time.isoformat(),
            'view_count': current_views,
            'like_count': current_likes,
            'comment_count': current_comments,
            'hours_since_publish': hours_since_publish,
            'collected_at': snapshot_time.isoformat()
        })
    
    return snapshots


def generate_mock_feature_vector(is_short: bool = False) -> Dict[str, Any]:
    """
    Generate mock feature vector for ML models.
    
    Args:
        is_short: Whether features are for a Short video
        
    Returns:
        Dictionary containing mock features
    """
    if is_short:
        duration_seconds = random.randint(15, 60)
    else:
        duration_seconds = random.randint(61, 3600)
    
    publish_hour = random.randint(0, 23)
    publish_day_of_week = random.randint(0, 6)
    is_weekend = publish_day_of_week >= 5
    
    return {
        'duration_seconds': duration_seconds,
        'title_length': random.randint(10, 100),
        'description_length': random.randint(50, 500),
        'tag_count': random.randint(1, 15),
        'publish_hour': publish_hour,
        'publish_day_of_week': publish_day_of_week,
        'is_weekend': is_weekend,
        'subscriber_count': random.randint(1000, 1000000),
        'channel_video_count': random.randint(10, 1000),
        'category_id': random.choice([1, 2, 10, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28]),
        'has_thumbnail': True,
        'title_sentiment': random.uniform(-1, 1),
        'description_sentiment': random.uniform(-1, 1),
        'title_caps_ratio': random.uniform(0, 0.3),
        'title_exclamation_count': random.randint(0, 3),
        'title_question_count': random.randint(0, 2),
        'is_sri_lankan_content': random.choice([True, False])
    }


def generate_mock_youtube_api_response(
    video_ids: List[str] = None,
    include_statistics: bool = True
) -> Dict[str, Any]:
    """
    Generate mock YouTube API response.
    
    Args:
        video_ids: List of video IDs to include
        include_statistics: Whether to include statistics
        
    Returns:
        Mock API response dictionary
    """
    if video_ids is None:
        video_ids = [generate_video_id() for _ in range(3)]
    
    items = []
    for video_id in video_ids:
        item = {
            'id': video_id,
            'snippet': {
                'title': fake.sentence(nb_words=6),
                'description': fake.text(max_nb_chars=200),
                'publishedAt': fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                'channelId': generate_channel_id(),
                'categoryId': str(random.choice([22, 23, 24, 25])),
                'tags': fake.words(nb=random.randint(3, 8))
            },
            'contentDetails': {
                'duration': f'PT{random.randint(1, 10)}M{random.randint(0, 59)}S'
            }
        }
        
        if include_statistics:
            item['statistics'] = {
                'viewCount': str(random.randint(100, 1000000)),
                'likeCount': str(random.randint(10, 50000)),
                'commentCount': str(random.randint(1, 5000))
            }
        
        items.append(item)
    
    return {
        'items': items,
        'pageInfo': {
            'totalResults': len(items),
            'resultsPerPage': len(items)
        }
    }


def generate_bulk_mock_data(
    num_videos: int = 100,
    num_channels: int = 20,
    num_users: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate bulk mock data for testing.
    
    Args:
        num_videos: Number of videos to generate
        num_channels: Number of channels to generate
        num_users: Number of users to generate
        
    Returns:
        Dictionary containing lists of mock data
    """
    # Generate channels first
    channels = [generate_mock_channel_data() for _ in range(num_channels)]
    channel_ids = [channel['channel_id'] for channel in channels]
    
    # Generate videos using the channel IDs
    videos = []
    for _ in range(num_videos):
        channel_id = random.choice(channel_ids)
        video = generate_mock_video_data(channel_id=channel_id)
        videos.append(video)
    
    # Generate users
    users = [generate_mock_user_data() for _ in range(num_users)]
    
    # Generate predictions for some videos
    predictions = []
    for _ in range(num_videos // 2):  # Predictions for half the videos
        video_id = random.choice([v['video_id'] for v in videos])
        user_id = random.randint(1, num_users)
        prediction = generate_mock_prediction_data(video_id, user_id)
        predictions.append(prediction)
    
    return {
        'channels': channels,
        'videos': videos,
        'users': users,
        'predictions': predictions
    }


class MockDataBuilder:
    """Builder class for creating complex mock data scenarios."""
    
    def __init__(self):
        self.data = {
            'channels': [],
            'videos': [],
            'users': [],
            'predictions': [],
            'performance_data': []
        }
    
    def add_sri_lankan_channel(self, subscriber_count: int = None) -> 'MockDataBuilder':
        """Add a Sri Lankan channel."""
        channel = generate_mock_channel_data(subscriber_count, country='LK')
        self.data['channels'].append(channel)
        return self
    
    def add_international_channel(self, subscriber_count: int = None) -> 'MockDataBuilder':
        """Add an international channel."""
        channel = generate_mock_channel_data(subscriber_count, country='US')
        self.data['channels'].append(channel)
        return self
    
    def add_shorts_video(self, channel_id: str = None) -> 'MockDataBuilder':
        """Add a Shorts video."""
        if channel_id is None and self.data['channels']:
            channel_id = self.data['channels'][-1]['channel_id']
        
        video = generate_mock_video_data(is_short=True, channel_id=channel_id)
        self.data['videos'].append(video)
        return self
    
    def add_longform_video(self, channel_id: str = None) -> 'MockDataBuilder':
        """Add a long-form video."""
        if channel_id is None and self.data['channels']:
            channel_id = self.data['channels'][-1]['channel_id']
        
        video = generate_mock_video_data(is_short=False, channel_id=channel_id)
        self.data['videos'].append(video)
        return self
    
    def add_user(self) -> 'MockDataBuilder':
        """Add a user."""
        user = generate_mock_user_data()
        self.data['users'].append(user)
        return self
    
    def add_prediction(self, video_id: str = None, user_id: int = None) -> 'MockDataBuilder':
        """Add a prediction."""
        if video_id is None and self.data['videos']:
            video_id = self.data['videos'][-1]['video_id']
        
        prediction = generate_mock_prediction_data(video_id, user_id)
        self.data['predictions'].append(prediction)
        return self
    
    def add_performance_tracking(self, video_id: str = None, num_snapshots: int = 10) -> 'MockDataBuilder':
        """Add performance tracking data."""
        if video_id is None and self.data['videos']:
            video_id = self.data['videos'][-1]['video_id']
        
        snapshots = generate_mock_performance_data(video_id, num_snapshots)
        self.data['performance_data'].extend(snapshots)
        return self
    
    def build(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build and return the mock data."""
        return self.data.copy()


# Predefined scenarios
def create_sri_lankan_content_scenario() -> Dict[str, List[Dict[str, Any]]]:
    """Create a scenario with Sri Lankan content."""
    builder = MockDataBuilder()
    
    # Add Sri Lankan channels
    builder.add_sri_lankan_channel(50000)  # Medium channel
    builder.add_sri_lankan_channel(500000)  # Large channel
    
    # Add videos for each channel
    for _ in range(5):
        builder.add_shorts_video()
        builder.add_longform_video()
    
    # Add users and predictions
    for _ in range(3):
        builder.add_user()
    
    for _ in range(8):
        builder.add_prediction()
    
    # Add performance tracking for some videos
    for _ in range(3):
        builder.add_performance_tracking()
    
    return builder.build()


def create_mixed_content_scenario() -> Dict[str, List[Dict[str, Any]]]:
    """Create a scenario with mixed Sri Lankan and international content."""
    builder = MockDataBuilder()
    
    # Add mixed channels
    builder.add_sri_lankan_channel(100000)
    builder.add_international_channel(1000000)
    builder.add_sri_lankan_channel(10000)
    
    # Add various videos
    for _ in range(10):
        builder.add_shorts_video()
    
    for _ in range(15):
        builder.add_longform_video()
    
    # Add users and predictions
    for _ in range(5):
        builder.add_user()
    
    for _ in range(20):
        builder.add_prediction()
    
    return builder.build()
