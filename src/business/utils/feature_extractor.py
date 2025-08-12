"""
Feature Extraction Utilities

This module provides utility functions for extracting features from video metadata
and other data sources for machine learning models.

Author: ViewTrendsSL Team
Date: 2025
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from .time_utils import get_time_features, parse_iso_duration

logger = logging.getLogger(__name__)


def extract_video_features(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract features from video metadata for ML models.
    
    Args:
        video_data: Video metadata dictionary
        
    Returns:
        Dictionary containing extracted features
    """
    features = {}
    
    try:
        # Basic video information
        features['video_id'] = video_data.get('video_id', '')
        features['title'] = video_data.get('title', '')
        features['description'] = video_data.get('description', '')
        
        # Duration features
        duration_seconds = video_data.get('duration_seconds', 0)
        if isinstance(video_data.get('duration'), str):
            duration_seconds = parse_iso_duration(video_data['duration'])
        
        features['duration_seconds'] = duration_seconds
        features['duration_minutes'] = duration_seconds / 60
        features['is_short'] = duration_seconds <= 60
        
        # Title features
        title = features['title']
        features['title_length'] = len(title)
        features['title_word_count'] = len(title.split())
        features['title_char_count'] = len(title)
        features['has_question_in_title'] = 1 if '?' in title else 0
        features['has_exclamation_in_title'] = 1 if '!' in title else 0
        features['title_uppercase_ratio'] = sum(1 for c in title if c.isupper()) / max(len(title), 1)
        features['title_number_count'] = len(re.findall(r'\d+', title))
        
        # Description features
        description = features['description']
        features['description_length'] = len(description)
        features['description_word_count'] = len(description.split())
        features['description_line_count'] = len(description.split('\n'))
        features['has_description'] = 1 if description.strip() else 0
        
        # Time-based features
        published_at = video_data.get('published_at')
        if published_at:
            if isinstance(published_at, str):
                published_at = pd.to_datetime(published_at)
            
            time_features = get_time_features(published_at)
            features.update({
                'publish_hour': time_features['hour'],
                'publish_day_of_week': time_features['day_of_week'],
                'publish_month': time_features['month'],
                'publish_quarter': time_features['quarter'],
                'is_weekend': time_features['is_weekend'],
                'is_optimal_posting_time': time_features['is_optimal_posting_time'],
                'time_period': time_features['time_period']
            })
        
        # Category features
        features['category_id'] = video_data.get('category_id', 0)
        
        # Tags features
        tags = video_data.get('tags', [])
        features['tag_count'] = len(tags)
        features['has_tags'] = 1 if tags else 0
        features['avg_tag_length'] = sum(len(tag) for tag in tags) / max(len(tags), 1)
        
        # Thumbnail features
        features['has_thumbnail'] = 1 if video_data.get('thumbnail_url') else 0
        
        # Channel features
        features['channel_id'] = video_data.get('channel_id', '')
        features['channel_subscriber_count'] = video_data.get('channel_subscriber_count', 0)
        features['channel_video_count'] = video_data.get('channel_video_count', 0)
        features['channel_view_count'] = video_data.get('channel_view_count', 0)
        
        # Engagement features (if available)
        features['view_count'] = video_data.get('view_count', 0)
        features['like_count'] = video_data.get('like_count', 0)
        features['comment_count'] = video_data.get('comment_count', 0)
        
        # Calculate engagement ratios
        view_count = features['view_count']
        if view_count > 0:
            features['like_ratio'] = features['like_count'] / view_count
            features['comment_ratio'] = features['comment_count'] / view_count
        else:
            features['like_ratio'] = 0
            features['comment_ratio'] = 0
        
        # Language detection features (basic)
        features.update(extract_language_features(title, description))
        
        # Content type features
        features.update(extract_content_type_features(title, description, tags))
        
        # SEO features
        features.update(extract_seo_features(title, description, tags))
        
    except Exception as e:
        logger.error(f"Error extracting video features: {str(e)}")
        # Return basic features on error
        features = {
            'duration_seconds': 0,
            'title_length': 0,
            'description_length': 0,
            'tag_count': 0,
            'category_id': 0
        }
    
    return features


def extract_language_features(title: str, description: str) -> Dict[str, Any]:
    """
    Extract language-related features from text.
    
    Args:
        title: Video title
        description: Video description
        
    Returns:
        Dictionary containing language features
    """
    features = {}
    
    # Sinhala character detection
    sinhala_pattern = r'[\u0D80-\u0DFF]'
    features['has_sinhala_title'] = 1 if re.search(sinhala_pattern, title) else 0
    features['has_sinhala_description'] = 1 if re.search(sinhala_pattern, description) else 0
    features['sinhala_char_count_title'] = len(re.findall(sinhala_pattern, title))
    features['sinhala_char_count_description'] = len(re.findall(sinhala_pattern, description))
    
    # Tamil character detection
    tamil_pattern = r'[\u0B80-\u0BFF]'
    features['has_tamil_title'] = 1 if re.search(tamil_pattern, title) else 0
    features['has_tamil_description'] = 1 if re.search(tamil_pattern, description) else 0
    features['tamil_char_count_title'] = len(re.findall(tamil_pattern, title))
    features['tamil_char_count_description'] = len(re.findall(tamil_pattern, description))
    
    # English character ratio
    english_chars_title = len(re.findall(r'[a-zA-Z]', title))
    english_chars_description = len(re.findall(r'[a-zA-Z]', description))
    
    features['english_ratio_title'] = english_chars_title / max(len(title), 1)
    features['english_ratio_description'] = english_chars_description / max(len(description), 1)
    
    # Primary language detection (simple heuristic)
    if features['sinhala_char_count_title'] > english_chars_title:
        features['primary_language'] = 'sinhala'
    elif features['tamil_char_count_title'] > english_chars_title:
        features['primary_language'] = 'tamil'
    else:
        features['primary_language'] = 'english'
    
    return features


def extract_content_type_features(title: str, description: str, tags: List[str]) -> Dict[str, Any]:
    """
    Extract content type features from video metadata.
    
    Args:
        title: Video title
        description: Video description
        tags: Video tags
        
    Returns:
        Dictionary containing content type features
    """
    features = {}
    
    # Combine text for analysis
    all_text = f"{title} {description} {' '.join(tags)}".lower()
    
    # Tutorial/Educational content
    tutorial_keywords = ['how to', 'tutorial', 'guide', 'learn', 'lesson', 'course', 'explain']
    features['is_tutorial'] = 1 if any(keyword in all_text for keyword in tutorial_keywords) else 0
    
    # News content
    news_keywords = ['news', 'breaking', 'update', 'report', 'latest', 'today']
    features['is_news'] = 1 if any(keyword in all_text for keyword in news_keywords) else 0
    
    # Entertainment content
    entertainment_keywords = ['funny', 'comedy', 'entertainment', 'fun', 'laugh', 'joke']
    features['is_entertainment'] = 1 if any(keyword in all_text for keyword in entertainment_keywords) else 0
    
    # Music content
    music_keywords = ['song', 'music', 'cover', 'remix', 'album', 'artist', 'band']
    features['is_music'] = 1 if any(keyword in all_text for keyword in music_keywords) else 0
    
    # Gaming content
    gaming_keywords = ['game', 'gaming', 'gameplay', 'review', 'walkthrough', 'let\'s play']
    features['is_gaming'] = 1 if any(keyword in all_text for keyword in gaming_keywords) else 0
    
    # Vlog content
    vlog_keywords = ['vlog', 'daily', 'life', 'day in', 'routine', 'personal']
    features['is_vlog'] = 1 if any(keyword in all_text for keyword in vlog_keywords) else 0
    
    # Review content
    review_keywords = ['review', 'unboxing', 'test', 'comparison', 'vs', 'opinion']
    features['is_review'] = 1 if any(keyword in all_text for keyword in review_keywords) else 0
    
    return features


def extract_seo_features(title: str, description: str, tags: List[str]) -> Dict[str, Any]:
    """
    Extract SEO-related features from video metadata.
    
    Args:
        title: Video title
        description: Video description
        tags: Video tags
        
    Returns:
        Dictionary containing SEO features
    """
    features = {}
    
    # Title SEO features
    features['title_has_numbers'] = 1 if re.search(r'\d', title) else 0
    features['title_has_brackets'] = 1 if any(char in title for char in '()[]{}') else 0
    features['title_has_caps'] = 1 if any(word.isupper() for word in title.split()) else 0
    
    # Keyword density (simple approach)
    title_words = title.lower().split()
    description_words = description.lower().split()
    tag_words = [tag.lower() for tag in tags]
    
    # Common words between title and description
    common_words = set(title_words) & set(description_words)
    features['title_description_overlap'] = len(common_words) / max(len(title_words), 1)
    
    # Tag optimization
    features['tags_in_title'] = sum(1 for tag in tag_words if tag in title.lower())
    features['tags_in_description'] = sum(1 for tag in tag_words if tag in description.lower())
    
    # Description optimization
    features['description_has_links'] = 1 if 'http' in description else 0
    features['description_has_timestamps'] = 1 if re.search(r'\d+:\d+', description) else 0
    
    return features


def extract_channel_features(channel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract features from channel metadata.
    
    Args:
        channel_data: Channel metadata dictionary
        
    Returns:
        Dictionary containing channel features
    """
    features = {}
    
    try:
        # Basic channel info
        features['channel_id'] = channel_data.get('channel_id', '')
        features['channel_title'] = channel_data.get('channel_title', '')
        features['channel_description'] = channel_data.get('channel_description', '')
        
        # Channel statistics
        features['channel_subscriber_count'] = channel_data.get('subscriber_count', 0)
        features['channel_video_count'] = channel_data.get('video_count', 0)
        features['channel_view_count'] = channel_data.get('view_count', 0)
        
        # Channel age (if available)
        published_at = channel_data.get('published_at')
        if published_at:
            if isinstance(published_at, str):
                published_at = pd.to_datetime(published_at)
            
            channel_age_days = (datetime.now() - published_at).days
            features['channel_age_days'] = channel_age_days
            features['channel_age_years'] = channel_age_days / 365.25
        else:
            features['channel_age_days'] = 0
            features['channel_age_years'] = 0
        
        # Channel performance metrics
        if features['channel_video_count'] > 0:
            features['avg_views_per_video'] = features['channel_view_count'] / features['channel_video_count']
            features['subscribers_per_video'] = features['channel_subscriber_count'] / features['channel_video_count']
        else:
            features['avg_views_per_video'] = 0
            features['subscribers_per_video'] = 0
        
        # Channel size category
        subscriber_count = features['channel_subscriber_count']
        if subscriber_count < 1000:
            features['channel_size'] = 'micro'
        elif subscriber_count < 10000:
            features['channel_size'] = 'small'
        elif subscriber_count < 100000:
            features['channel_size'] = 'medium'
        elif subscriber_count < 1000000:
            features['channel_size'] = 'large'
        else:
            features['channel_size'] = 'mega'
        
    except Exception as e:
        logger.error(f"Error extracting channel features: {str(e)}")
        features = {
            'channel_subscriber_count': 0,
            'channel_video_count': 0,
            'channel_view_count': 0,
            'channel_age_days': 0
        }
    
    return features


def extract_temporal_features(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract temporal features from video data.
    
    Args:
        video_data: Video data with timestamps
        
    Returns:
        Dictionary containing temporal features
    """
    features = {}
    
    try:
        published_at = video_data.get('published_at')
        if published_at:
            if isinstance(published_at, str):
                published_at = pd.to_datetime(published_at)
            
            # Time since upload
            now = datetime.now()
            time_diff = now - published_at
            
            features['hours_since_upload'] = time_diff.total_seconds() / 3600
            features['days_since_upload'] = time_diff.days
            
            # Upload timing features
            features['upload_hour'] = published_at.hour
            features['upload_day_of_week'] = published_at.weekday()
            features['upload_month'] = published_at.month
            features['upload_year'] = published_at.year
            
            # Seasonal features
            features['is_holiday_season'] = 1 if published_at.month in [11, 12, 1] else 0
            features['is_summer'] = 1 if published_at.month in [6, 7, 8] else 0
            
    except Exception as e:
        logger.error(f"Error extracting temporal features: {str(e)}")
        features = {
            'hours_since_upload': 0,
            'days_since_upload': 0,
            'upload_hour': 0,
            'upload_day_of_week': 0
        }
    
    return features


def extract_engagement_features(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract engagement-related features from video data.
    
    Args:
        video_data: Video data with engagement metrics
        
    Returns:
        Dictionary containing engagement features
    """
    features = {}
    
    try:
        view_count = video_data.get('view_count', 0)
        like_count = video_data.get('like_count', 0)
        dislike_count = video_data.get('dislike_count', 0)
        comment_count = video_data.get('comment_count', 0)
        
        features['view_count'] = view_count
        features['like_count'] = like_count
        features['dislike_count'] = dislike_count
        features['comment_count'] = comment_count
        
        # Engagement ratios
        if view_count > 0:
            features['like_rate'] = like_count / view_count
            features['dislike_rate'] = dislike_count / view_count
            features['comment_rate'] = comment_count / view_count
            features['engagement_rate'] = (like_count + dislike_count + comment_count) / view_count
        else:
            features['like_rate'] = 0
            features['dislike_rate'] = 0
            features['comment_rate'] = 0
            features['engagement_rate'] = 0
        
        # Like-to-dislike ratio
        if dislike_count > 0:
            features['like_dislike_ratio'] = like_count / dislike_count
        else:
            features['like_dislike_ratio'] = like_count  # If no dislikes, use like count
        
        # Engagement score (weighted combination)
        features['engagement_score'] = (
            like_count * 1.0 +
            comment_count * 2.0 +
            dislike_count * 0.5
        ) / max(view_count, 1)
        
    except Exception as e:
        logger.error(f"Error extracting engagement features: {str(e)}")
        features = {
            'view_count': 0,
            'like_count': 0,
            'comment_count': 0,
            'engagement_rate': 0
        }
    
    return features


def create_feature_vector(video_data: Dict[str, Any], channel_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a complete feature vector for a video.
    
    Args:
        video_data: Video metadata
        channel_data: Optional channel metadata
        
    Returns:
        Dictionary containing all extracted features
    """
    features = {}
    
    # Extract all feature types
    features.update(extract_video_features(video_data))
    features.update(extract_temporal_features(video_data))
    features.update(extract_engagement_features(video_data))
    
    # Add channel features if available
    if channel_data:
        features.update(extract_channel_features(channel_data))
    
    return features


def normalize_features(features: Dict[str, Any], feature_ranges: Optional[Dict[str, tuple]] = None) -> Dict[str, Any]:
    """
    Normalize feature values to a standard range.
    
    Args:
        features: Feature dictionary
        feature_ranges: Optional dictionary of (min, max) ranges for each feature
        
    Returns:
        Dictionary containing normalized features
    """
    normalized = features.copy()
    
    if not feature_ranges:
        # Default ranges for common features
        feature_ranges = {
            'duration_seconds': (0, 3600),
            'title_length': (0, 200),
            'description_length': (0, 5000),
            'tag_count': (0, 50),
            'channel_subscriber_count': (0, 10000000),
            'view_count': (0, 100000000)
        }
    
    for feature_name, (min_val, max_val) in feature_ranges.items():
        if feature_name in normalized:
            value = normalized[feature_name]
            if isinstance(value, (int, float)):
                # Min-max normalization
                normalized[feature_name] = (value - min_val) / max(max_val - min_val, 1)
                # Clip to [0, 1] range
                normalized[feature_name] = max(0, min(1, normalized[feature_name]))
    
    return normalized


def get_feature_importance_weights() -> Dict[str, float]:
    """
    Get predefined feature importance weights.
    
    Returns:
        Dictionary containing feature importance weights
    """
    return {
        # Video content features
        'duration_seconds': 0.15,
        'title_length': 0.08,
        'description_length': 0.05,
        'tag_count': 0.06,
        
        # Timing features
        'publish_hour': 0.12,
        'publish_day_of_week': 0.10,
        'is_weekend': 0.08,
        'is_optimal_posting_time': 0.09,
        
        # Channel features
        'channel_subscriber_count': 0.20,
        'channel_video_count': 0.07,
        
        # Content type features
        'is_tutorial': 0.05,
        'is_entertainment': 0.04,
        'is_music': 0.06,
        
        # Language features
        'primary_language': 0.08,
        'has_sinhala_title': 0.07,
        
        # SEO features
        'title_has_numbers': 0.03,
        'has_question_in_title': 0.04
    }
