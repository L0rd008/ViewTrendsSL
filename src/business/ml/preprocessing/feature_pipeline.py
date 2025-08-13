"""
Feature Engineering Pipeline for ViewTrendsSL

This module provides standardized feature engineering capabilities for
YouTube video data, including text analysis, temporal features, and
Sri Lankan content detection.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pickle
import json

logger = logging.getLogger(__name__)


class FeaturePipeline:
    """Standardized feature engineering pipeline for YouTube video data."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the feature pipeline.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._get_default_config()
        self.fitted_transformers = {}
        self.feature_names = []
        self.is_fitted = False
        
        # Sri Lankan keywords for content detection
        self.sri_lankan_keywords = [
            'sri lanka', 'srilanka', 'colombo', 'kandy', 'galle', 'jaffna',
            'sinhala', 'tamil', 'ceylon', 'lk', 'rupee', 'rupees',
            'mahinda', 'gotabaya', 'ranil', 'sajith', 'anura',
            'cricket', 'sl cricket', 'lions', 'malinga', 'sangakkara',
            'buddhist', 'temple', 'kovil', 'church', 'mosque',
            'curry', 'rice', 'kottu', 'hoppers', 'string hoppers',
            'ayubowan', 'vanakkam', 'kohomada', 'eppadi'
        ]
        
        logger.info("FeaturePipeline initialized")
    
    def fit(self, data: pd.DataFrame) -> 'FeaturePipeline':
        """
        Fit the feature pipeline on training data.
        
        Args:
            data: Training dataset
            
        Returns:
            Self for method chaining
        """
        try:
            logger.info("Fitting feature pipeline")
            
            # Fit text-based transformers
            self._fit_text_features(data)
            
            # Fit numerical transformers
            self._fit_numerical_features(data)
            
            # Fit categorical transformers
            self._fit_categorical_features(data)
            
            self.is_fitted = True
            logger.info("Feature pipeline fitted successfully")
            
            return self
            
        except Exception as e:
            logger.error(f"Error fitting feature pipeline: {str(e)}")
            raise
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data using the fitted pipeline.
        
        Args:
            data: Input dataset
            
        Returns:
            Transformed dataset with engineered features
        """
        try:
            logger.info(f"Transforming data with {len(data)} samples")
            
            df = data.copy()
            
            # Basic feature engineering
            df = self._engineer_basic_features(df)
            
            # Time-based features
            df = self._engineer_time_features(df)
            
            # Text features
            df = self._engineer_text_features(df)
            
            # Channel features
            df = self._engineer_channel_features(df)
            
            # Content analysis features
            df = self._engineer_content_features(df)
            
            # Sri Lankan content detection
            df = self._engineer_sri_lankan_features(df)
            
            # Video type specific features
            df = self._engineer_video_type_features(df)
            
            # Interaction features
            df = self._engineer_interaction_features(df)
            
            # Store feature names
            self.feature_names = [col for col in df.columns 
                                if col not in ['video_id', 'published_at']]
            
            logger.info(f"Feature engineering completed: {len(self.feature_names)} features")
            
            return df
            
        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
            raise
    
    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the pipeline and transform data in one step.
        
        Args:
            data: Input dataset
            
        Returns:
            Transformed dataset
        """
        return self.fit(data).transform(data)
    
    def get_feature_names(self) -> List[str]:
        """
        Get list of engineered feature names.
        
        Returns:
            List of feature names
        """
        return self.feature_names.copy()
    
    def get_feature_importance_groups(self) -> Dict[str, List[str]]:
        """
        Get features grouped by type for importance analysis.
        
        Returns:
            Dictionary mapping feature types to feature names
        """
        groups = {
            'basic': [],
            'time': [],
            'text': [],
            'channel': [],
            'content': [],
            'sri_lankan': [],
            'video_type': [],
            'interaction': []
        }
        
        for feature in self.feature_names:
            if any(keyword in feature for keyword in ['duration', 'category']):
                groups['basic'].append(feature)
            elif any(keyword in feature for keyword in ['hour', 'day', 'weekend', 'time']):
                groups['time'].append(feature)
            elif any(keyword in feature for keyword in ['title', 'description', 'text', 'word']):
                groups['text'].append(feature)
            elif any(keyword in feature for keyword in ['channel', 'subscriber', 'authority']):
                groups['channel'].append(feature)
            elif any(keyword in feature for keyword in ['tag', 'thumbnail', 'content']):
                groups['content'].append(feature)
            elif 'sri_lankan' in feature or 'sinhala' in feature or 'tamil' in feature:
                groups['sri_lankan'].append(feature)
            elif any(keyword in feature for keyword in ['short', 'longform', 'video_type']):
                groups['video_type'].append(feature)
            else:
                groups['interaction'].append(feature)
        
        return groups
    
    def save_pipeline(self, filepath: str) -> bool:
        """
        Save the fitted pipeline to disk.
        
        Args:
            filepath: Path to save the pipeline
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pipeline_data = {
                'config': self.config,
                'fitted_transformers': self.fitted_transformers,
                'feature_names': self.feature_names,
                'is_fitted': self.is_fitted,
                'sri_lankan_keywords': self.sri_lankan_keywords,
                'saved_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(pipeline_data, f)
            
            logger.info(f"Feature pipeline saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving pipeline: {str(e)}")
            return False
    
    def load_pipeline(self, filepath: str) -> bool:
        """
        Load a fitted pipeline from disk.
        
        Args:
            filepath: Path to the saved pipeline
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'rb') as f:
                pipeline_data = pickle.load(f)
            
            self.config = pipeline_data['config']
            self.fitted_transformers = pipeline_data['fitted_transformers']
            self.feature_names = pipeline_data['feature_names']
            self.is_fitted = pipeline_data['is_fitted']
            self.sri_lankan_keywords = pipeline_data.get('sri_lankan_keywords', self.sri_lankan_keywords)
            
            logger.info(f"Feature pipeline loaded from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading pipeline: {str(e)}")
            return False
    
    # Private helper methods
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'max_duration_shorts': 60,
            'min_duration_longform': 61,
            'text_features': {
                'max_title_length': 200,
                'max_description_length': 5000,
                'min_word_length': 2
            },
            'channel_features': {
                'min_subscribers': 1,
                'max_subscribers': 100000000,
                'authority_weight': 0.7
            },
            'time_features': {
                'peak_hours': [18, 19, 20, 21],  # 6-9 PM
                'weekend_days': [5, 6]  # Saturday, Sunday
            }
        }
    
    def _fit_text_features(self, data: pd.DataFrame):
        """Fit text-based feature transformers."""
        # Calculate text statistics for normalization
        if 'title' in data.columns:
            self.fitted_transformers['title_length_stats'] = {
                'mean': data['title'].str.len().mean(),
                'std': data['title'].str.len().std()
            }
        
        if 'description' in data.columns:
            self.fitted_transformers['description_length_stats'] = {
                'mean': data['description'].str.len().mean(),
                'std': data['description'].str.len().std()
            }
    
    def _fit_numerical_features(self, data: pd.DataFrame):
        """Fit numerical feature transformers."""
        numerical_cols = ['duration_seconds', 'channel_subscriber_count', 'channel_video_count']
        
        for col in numerical_cols:
            if col in data.columns:
                self.fitted_transformers[f'{col}_stats'] = {
                    'mean': data[col].mean(),
                    'std': data[col].std(),
                    'min': data[col].min(),
                    'max': data[col].max()
                }
    
    def _fit_categorical_features(self, data: pd.DataFrame):
        """Fit categorical feature transformers."""
        if 'category_id' in data.columns:
            self.fitted_transformers['category_frequencies'] = data['category_id'].value_counts().to_dict()
    
    def _engineer_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer basic video features."""
        
        # Duration features
        if 'duration_seconds' in df.columns:
            df['duration_minutes'] = df['duration_seconds'] / 60
            df['duration_hours'] = df['duration_seconds'] / 3600
            df['is_short'] = (df['duration_seconds'] <= self.config['max_duration_shorts']).astype(int)
            df['is_longform'] = (df['duration_seconds'] > self.config['min_duration_longform']).astype(int)
            
            # Duration categories
            df['duration_category'] = pd.cut(
                df['duration_seconds'],
                bins=[0, 60, 300, 600, 1800, float('inf')],
                labels=['very_short', 'short', 'medium', 'long', 'very_long']
            ).astype(str)
        
        # Category features
        if 'category_id' in df.columns:
            # Popular categories in Sri Lanka
            popular_categories = [1, 10, 17, 22, 24, 25]  # Film, Music, Sports, People, Entertainment, News
            df['is_popular_category'] = df['category_id'].isin(popular_categories).astype(int)
        
        return df
    
    def _engineer_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer time-based features."""
        
        if 'published_at' in df.columns:
            # Convert to datetime if not already
            df['published_at'] = pd.to_datetime(df['published_at'])
            
            # Basic time features
            df['publish_hour'] = df['published_at'].dt.hour
            df['publish_day_of_week'] = df['published_at'].dt.dayofweek
            df['publish_month'] = df['published_at'].dt.month
            df['publish_year'] = df['published_at'].dt.year
            
            # Derived time features
            df['is_weekend'] = df['publish_day_of_week'].isin(self.config['time_features']['weekend_days']).astype(int)
            df['is_peak_hour'] = df['publish_hour'].isin(self.config['time_features']['peak_hours']).astype(int)
            
            # Time of day categories
            df['time_of_day'] = pd.cut(
                df['publish_hour'],
                bins=[0, 6, 12, 18, 24],
                labels=['night', 'morning', 'afternoon', 'evening'],
                include_lowest=True
            ).astype(str)
            
            # Season (for Sri Lanka - monsoon patterns)
            df['season'] = df['publish_month'].map({
                12: 'northeast_monsoon', 1: 'northeast_monsoon', 2: 'northeast_monsoon',
                3: 'inter_monsoon', 4: 'inter_monsoon', 5: 'inter_monsoon',
                6: 'southwest_monsoon', 7: 'southwest_monsoon', 8: 'southwest_monsoon',
                9: 'inter_monsoon', 10: 'inter_monsoon', 11: 'inter_monsoon'
            })
        
        return df
    
    def _engineer_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer text-based features."""
        
        # Title features
        if 'title' in df.columns:
            df['title'] = df['title'].fillna('')
            df['title_length'] = df['title'].str.len()
            df['title_word_count'] = df['title'].str.split().str.len()
            df['title_char_count'] = df['title'].str.len()
            
            # Title analysis
            df['has_question_in_title'] = df['title'].str.contains(r'\?', na=False).astype(int)
            df['has_exclamation_in_title'] = df['title'].str.contains(r'!', na=False).astype(int)
            df['has_numbers_in_title'] = df['title'].str.contains(r'\d', na=False).astype(int)
            df['title_caps_ratio'] = df['title'].apply(
                lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(str(x)), 1)
            )
            
            # Emotional indicators
            df['title_has_emotional_words'] = df['title'].str.lower().str.contains(
                r'\b(amazing|incredible|shocking|unbelievable|wow|omg|best|worst|epic|fail)\b',
                na=False
            ).astype(int)
            
            # Clickbait indicators
            clickbait_patterns = [
                r'\byou won\'t believe\b',
                r'\bthis will\b',
                r'\bwhat happens next\b',
                r'\btop \d+\b',
                r'\b\d+ things\b',
                r'\bsecret\b',
                r'\btrick\b'
            ]
            df['title_clickbait_score'] = df['title'].str.lower().apply(
                lambda x: sum(1 for pattern in clickbait_patterns if re.search(pattern, str(x)))
            )
        
        # Description features
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('')
            df['description_length'] = df['description'].str.len()
            df['description_word_count'] = df['description'].str.split().str.len()
            df['has_description'] = (df['description_length'] > 0).astype(int)
            
            # URL and hashtag counts
            df['description_url_count'] = df['description'].str.count(r'http[s]?://\S+')
            df['description_hashtag_count'] = df['description'].str.count(r'#\w+')
            df['description_mention_count'] = df['description'].str.count(r'@\w+')
        
        return df
    
    def _engineer_channel_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer channel-based features."""
        
        if 'channel_subscriber_count' in df.columns and 'channel_video_count' in df.columns:
            # Channel authority score
            df['channel_authority_score'] = (
                np.log1p(df['channel_subscriber_count']) * 
                np.log1p(df['channel_video_count']) * 
                self.config['channel_features']['authority_weight']
            )
            
            # Channel size categories
            df['channel_size'] = pd.cut(
                df['channel_subscriber_count'],
                bins=[0, 1000, 10000, 100000, 1000000, float('inf')],
                labels=['micro', 'small', 'medium', 'large', 'mega']
            ).astype(str)
            
            # Videos per subscriber ratio
            df['videos_per_subscriber'] = df['channel_video_count'] / np.maximum(df['channel_subscriber_count'], 1)
            
            # Channel activity level
            df['channel_activity_level'] = pd.cut(
                df['channel_video_count'],
                bins=[0, 50, 200, 1000, float('inf')],
                labels=['low', 'medium', 'high', 'very_high']
            ).astype(str)
        
        return df
    
    def _engineer_content_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer content-based features."""
        
        # Tag features
        if 'tags' in df.columns:
            df['tags'] = df['tags'].fillna('')
            df['tag_count'] = df['tags'].str.split(',').str.len()
            df['has_tags'] = (df['tag_count'] > 0).astype(int)
            
            # Popular tag categories
            tech_tags = ['technology', 'tech', 'software', 'programming', 'coding']
            entertainment_tags = ['entertainment', 'funny', 'comedy', 'music', 'dance']
            education_tags = ['education', 'tutorial', 'howto', 'learning', 'tips']
            
            df['has_tech_tags'] = df['tags'].str.lower().str.contains('|'.join(tech_tags), na=False).astype(int)
            df['has_entertainment_tags'] = df['tags'].str.lower().str.contains('|'.join(entertainment_tags), na=False).astype(int)
            df['has_education_tags'] = df['tags'].str.lower().str.contains('|'.join(education_tags), na=False).astype(int)
        
        return df
    
    def _engineer_sri_lankan_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer Sri Lankan content detection features."""
        
        # Combine title and description for analysis
        df['combined_text'] = (df.get('title', '') + ' ' + df.get('description', '')).str.lower()
        
        # Sri Lankan keyword detection
        df['sri_lankan_keyword_count'] = df['combined_text'].apply(
            lambda x: sum(1 for keyword in self.sri_lankan_keywords if keyword in str(x))
        )
        df['is_sri_lankan_content'] = (df['sri_lankan_keyword_count'] > 0).astype(int)
        
        # Language detection (basic)
        sinhala_chars = r'[\u0D80-\u0DFF]'  # Sinhala Unicode range
        tamil_chars = r'[\u0B80-\u0BFF]'    # Tamil Unicode range
        
        df['has_sinhala_text'] = df['combined_text'].str.contains(sinhala_chars, na=False).astype(int)
        df['has_tamil_text'] = df['combined_text'].str.contains(tamil_chars, na=False).astype(int)
        df['has_local_language'] = ((df['has_sinhala_text'] == 1) | (df['has_tamil_text'] == 1)).astype(int)
        
        # Sri Lankan location mentions
        locations = ['colombo', 'kandy', 'galle', 'jaffna', 'negombo', 'anuradhapura', 'polonnaruwa']
        df['sri_lankan_location_mentions'] = df['combined_text'].apply(
            lambda x: sum(1 for location in locations if location in str(x))
        )
        
        # Cultural references
        cultural_terms = ['buddhist', 'temple', 'kovil', 'church', 'mosque', 'poya', 'vesak', 'avurudu']
        df['cultural_reference_count'] = df['combined_text'].apply(
            lambda x: sum(1 for term in cultural_terms if term in str(x))
        )
        
        # Food references
        food_terms = ['curry', 'rice', 'kottu', 'hoppers', 'string hoppers', 'roti', 'pol sambol']
        df['food_reference_count'] = df['combined_text'].apply(
            lambda x: sum(1 for term in food_terms if term in str(x))
        )
        
        # Overall Sri Lankan content score
        df['sri_lankan_content_score'] = (
            df['sri_lankan_keyword_count'] * 2 +
            df['has_local_language'] * 3 +
            df['sri_lankan_location_mentions'] * 2 +
            df['cultural_reference_count'] +
            df['food_reference_count']
        )
        
        # Clean up temporary column
        df = df.drop('combined_text', axis=1)
        
        return df
    
    def _engineer_video_type_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer video type specific features."""
        
        if 'is_short' in df.columns:
            # Shorts-specific features
            df['shorts_optimal_duration'] = ((df['duration_seconds'] >= 15) & 
                                           (df['duration_seconds'] <= 60)).astype(int)
            
            # Long-form specific features
            df['longform_optimal_duration'] = ((df['duration_seconds'] >= 480) & 
                                             (df['duration_seconds'] <= 1200)).astype(int)  # 8-20 minutes
            
            # Video type and category interaction
            if 'category_id' in df.columns:
                # Categories that work well for Shorts
                shorts_friendly_categories = [10, 17, 22, 24]  # Music, Sports, People, Entertainment
                df['shorts_category_match'] = (df['is_short'] & 
                                             df['category_id'].isin(shorts_friendly_categories)).astype(int)
                
                # Categories that work well for long-form
                longform_friendly_categories = [1, 2, 15, 25, 27, 28]  # Film, Autos, Pets, News, Education, Science
                df['longform_category_match'] = ((df['is_short'] == 0) & 
                                               df['category_id'].isin(longform_friendly_categories)).astype(int)
        
        return df
    
    def _engineer_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer interaction and derived features."""
        
        # Title and duration interaction
        if 'title_length' in df.columns and 'duration_seconds' in df.columns:
            df['title_duration_ratio'] = df['title_length'] / np.maximum(df['duration_seconds'], 1)
        
        # Channel authority and video type interaction
        if 'channel_authority_score' in df.columns and 'is_short' in df.columns:
            df['authority_shorts_interaction'] = df['channel_authority_score'] * df['is_short']
            df['authority_longform_interaction'] = df['channel_authority_score'] * (1 - df['is_short'])
        
        # Time and content type interaction
        if 'is_peak_hour' in df.columns and 'is_popular_category' in df.columns:
            df['peak_hour_popular_category'] = (df['is_peak_hour'] & df['is_popular_category']).astype(int)
        
        # Weekend and video type interaction
        if 'is_weekend' in df.columns and 'is_short' in df.columns:
            df['weekend_shorts'] = (df['is_weekend'] & df['is_short']).astype(int)
            df['weekend_longform'] = (df['is_weekend'] & (df['is_short'] == 0)).astype(int)
        
        # Sri Lankan content and time interaction
        if 'is_sri_lankan_content' in df.columns and 'time_of_day' in df.columns:
            # Sri Lankan content might perform better at certain times
            df['sri_lankan_evening'] = (df['is_sri_lankan_content'] & 
                                       (df['time_of_day'] == 'evening')).astype(int)
        
        # Title engagement features
        if 'has_question_in_title' in df.columns and 'has_exclamation_in_title' in df.columns:
            df['title_engagement_score'] = (
                df['has_question_in_title'] +
                df['has_exclamation_in_title'] +
                df.get('title_has_emotional_words', 0) +
                df.get('title_clickbait_score', 0)
            )
        
        return df
