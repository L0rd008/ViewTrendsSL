#!/usr/bin/env python3
"""
Enhanced CSV Data Processing Script for ViewTrendsSL

This script processes the collected CSV data with time-series information
to create proper training datasets that utilize all available features.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import logging
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import json
import re
from isodate import parse_duration

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedCSVProcessor:
    """Enhanced processor for ViewTrendsSL CSV data with time-series features."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the enhanced CSV processor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Create output directories
        self.output_dir = Path(config.get('output_dir', 'data/processed'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Enhanced CSV processor initialized. Output: {self.output_dir}")
    
    def load_csv_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load the CSV data with proper handling of all columns.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading CSV data from {csv_path}")
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Load the CSV with proper data types
        df = pd.read_csv(csv_path, low_memory=False)
        
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
    
    def clean_and_standardize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize the CSV data.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning and standardizing data...")
        
        initial_count = len(df)
        
        # Rename columns for consistency
        column_mapping = {
            'id': 'video_id',
            'likes_count': 'like_count',
            'video_duration': 'duration_iso8601'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Parse published_at to datetime
        if 'published_at' in df.columns:
            df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
        
        # Parse ISO 8601 duration to seconds
        if 'duration_iso8601' in df.columns:
            df['duration_seconds'] = df['duration_iso8601'].apply(self._parse_duration_to_seconds)
        
        # Clean numeric columns
        numeric_columns = ['view_count', 'like_count', 'comment_count', 'duration_seconds']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                df[col] = df[col].clip(lower=0)
        
        # Clean time-series columns (day_1_views, day_2_views, etc.)
        time_series_columns = []
        for col in df.columns:
            if col.startswith(('day_', 'day_')) and ('views' in col or 'likes' in col or 'comments' in col):
                time_series_columns.append(col)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        logger.info(f"Found {len(time_series_columns)} time-series columns")
        
        # Remove rows with missing critical data
        critical_columns = ['video_id', 'published_at', 'duration_seconds']
        df = df.dropna(subset=critical_columns)
        
        # Determine if video is a Short
        df['is_short'] = df['duration_seconds'] <= 60
        
        # Remove outliers
        df = self._remove_outliers(df)
        
        logger.info(f"Data cleaning completed. Records: {initial_count} -> {len(df)}")
        return df
    
    def _parse_duration_to_seconds(self, duration_str: str) -> int:
        """Parse ISO 8601 duration string to seconds."""
        if pd.isna(duration_str) or duration_str == '':
            return 0
        
        try:
            duration = parse_duration(duration_str)
            return int(duration.total_seconds())
        except Exception:
            return 0
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove statistical outliers from the data."""
        initial_count = len(df)
        
        # Remove videos with zero duration
        df = df[df['duration_seconds'] > 0]
        
        # Remove videos with unrealistic durations (> 4 hours)
        df = df[df['duration_seconds'] <= 14400]
        
        # Remove videos with zero views
        df = df[df['view_count'] > 0]
        
        # Remove extreme outliers in view count (top 0.1%)
        view_threshold = df['view_count'].quantile(0.999)
        df = df[df['view_count'] <= view_threshold]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} outlier records")
        
        return df
    
    def extract_time_series_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from time-series data (day_1_views, day_2_views, etc.).
        
        Args:
            df: DataFrame with time-series columns
            
        Returns:
            DataFrame with extracted time-series features
        """
        logger.info("Extracting time-series features...")
        
        # Get time-series columns
        view_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_views')]
        like_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_likes')]
        comment_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_comments')]
        
        # Sort columns by day number
        view_columns = sorted(view_columns, key=lambda x: int(x.split('_')[1]))
        like_columns = sorted(like_columns, key=lambda x: int(x.split('_')[1]))
        comment_columns = sorted(comment_columns, key=lambda x: int(x.split('_')[1]))
        
        logger.info(f"Processing {len(view_columns)} view columns, {len(like_columns)} like columns, {len(comment_columns)} comment columns")
        
        # Create target variables from time-series data
        if view_columns:
            # Use actual time-series data for targets
            if 'day_1_views' in df.columns:
                df['views_at_24h'] = df['day_1_views']
            if 'day_7_views' in df.columns:
                df['views_at_7d'] = df['day_7_views']
            if 'day_30_views' in df.columns:
                df['views_at_30d'] = df['day_30_views']
            
            # If specific days are missing, interpolate
            if 'views_at_24h' not in df.columns and len(view_columns) > 0:
                df['views_at_24h'] = df[view_columns[0]]  # Use first available day
            
            if 'views_at_7d' not in df.columns:
                # Find closest to day 7
                day_7_col = self._find_closest_day_column(view_columns, 7)
                if day_7_col:
                    df['views_at_7d'] = df[day_7_col]
            
            if 'views_at_30d' not in df.columns:
                # Find closest to day 30
                day_30_col = self._find_closest_day_column(view_columns, 30)
                if day_30_col:
                    df['views_at_30d'] = df[day_30_col]
        
        # Extract growth patterns and velocity features
        if len(view_columns) >= 2:
            # Early growth velocity (first few days)
            df['early_growth_velocity'] = self._calculate_growth_velocity(df, view_columns[:7])
            
            # Peak day (day with maximum views)
            df['peak_day'] = self._find_peak_day(df, view_columns)
            
            # Growth consistency (standard deviation of daily growth rates)
            df['growth_consistency'] = self._calculate_growth_consistency(df, view_columns)
            
            # Total growth over available period
            if len(view_columns) > 1:
                first_day = view_columns[0]
                last_day = view_columns[-1]
                df['total_growth_rate'] = (df[last_day] - df[first_day]) / np.maximum(df[first_day], 1)
        
        # Extract engagement progression features
        if like_columns and len(like_columns) >= 2:
            df['like_growth_rate'] = self._calculate_engagement_growth_rate(df, like_columns)
        
        if comment_columns and len(comment_columns) >= 2:
            df['comment_growth_rate'] = self._calculate_engagement_growth_rate(df, comment_columns)
        
        # Calculate engagement ratios at different time points
        for day in [1, 7, 30]:
            view_col = f'day_{day}_views'
            like_col = f'day_{day}_likes'
            comment_col = f'day_{day}_comments'
            
            if view_col in df.columns:
                if like_col in df.columns:
                    df[f'like_ratio_day_{day}'] = df[like_col] / np.maximum(df[view_col], 1)
                if comment_col in df.columns:
                    df[f'comment_ratio_day_{day}'] = df[comment_col] / np.maximum(df[view_col], 1)
        
        logger.info("Time-series feature extraction completed")
        return df
    
    def _find_closest_day_column(self, columns: List[str], target_day: int) -> Optional[str]:
        """Find the column closest to the target day."""
        if not columns:
            return None
        
        day_numbers = []
        for col in columns:
            try:
                day_num = int(col.split('_')[1])
                day_numbers.append((abs(day_num - target_day), col))
            except (IndexError, ValueError):
                continue
        
        if day_numbers:
            day_numbers.sort()
            return day_numbers[0][1]
        return None
    
    def _calculate_growth_velocity(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
        """Calculate early growth velocity."""
        if len(view_columns) < 2:
            return pd.Series(0, index=df.index)
        
        # Calculate average daily growth rate for early days
        growth_rates = []
        for i in range(1, min(len(view_columns), 8)):  # First 7 days
            if i < len(view_columns):
                prev_col = view_columns[i-1]
                curr_col = view_columns[i]
                daily_growth = (df[curr_col] - df[prev_col]) / np.maximum(df[prev_col], 1)
                growth_rates.append(daily_growth)
        
        if growth_rates:
            return pd.concat(growth_rates, axis=1).mean(axis=1)
        else:
            return pd.Series(0, index=df.index)
    
    def _find_peak_day(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
        """Find the day with peak views for each video."""
        if len(view_columns) < 2:
            return pd.Series(1, index=df.index)
        
        # Find the day with maximum views
        view_data = df[view_columns]
        peak_days = view_data.idxmax(axis=1)
        
        # Extract day number from column name
        peak_day_numbers = peak_days.apply(
            lambda x: int(x.split('_')[1]) if pd.notna(x) else 1
        )
        
        return peak_day_numbers
    
    def _calculate_growth_consistency(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
        """Calculate growth consistency (lower values = more consistent growth)."""
        if len(view_columns) < 3:
            return pd.Series(0, index=df.index)
        
        # Calculate daily growth rates
        growth_rates = []
        for i in range(1, len(view_columns)):
            prev_col = view_columns[i-1]
            curr_col = view_columns[i]
            daily_growth = (df[curr_col] - df[prev_col]) / np.maximum(df[prev_col], 1)
            growth_rates.append(daily_growth)
        
        if growth_rates:
            growth_df = pd.concat(growth_rates, axis=1)
            return growth_df.std(axis=1)
        else:
            return pd.Series(0, index=df.index)
    
    def _calculate_engagement_growth_rate(self, df: pd.DataFrame, engagement_columns: List[str]) -> pd.Series:
        """Calculate engagement growth rate."""
        if len(engagement_columns) < 2:
            return pd.Series(0, index=df.index)
        
        first_col = engagement_columns[0]
        last_col = engagement_columns[-1]
        
        growth_rate = (df[last_col] - df[first_col]) / np.maximum(df[first_col], 1)
        return growth_rate
    
    def extract_content_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract comprehensive content-based features.
        
        Args:
            df: DataFrame with content data
            
        Returns:
            DataFrame with content features
        """
        logger.info("Extracting content features...")
        
        # Title features
        if 'title' in df.columns:
            df['title_length'] = df['title'].str.len()
            df['title_word_count'] = df['title'].str.split().str.len()
            df['title_has_question'] = df['title'].str.contains(r'\?', na=False)
            df['title_has_exclamation'] = df['title'].str.contains(r'!', na=False)
            df['title_all_caps_ratio'] = df['title'].apply(self._calculate_caps_ratio)
            df['title_has_numbers'] = df['title'].str.contains(r'\d', na=False)
            df['title_emoji_count'] = df['title'].apply(self._count_emojis)
            
            # Language detection for title
            df['title_language'] = df['title'].apply(self._detect_language)
            df['title_is_sinhala'] = df['title_language'] == 'si'
            df['title_is_tamil'] = df['title_language'] == 'ta'
            df['title_is_english'] = df['title_language'] == 'en'
        
        # Description features
        if 'description' in df.columns:
            df['description_length'] = df['description'].str.len()
            df['description_word_count'] = df['description'].str.split().str.len()
            df['description_has_links'] = df['description'].str.contains(r'http', na=False)
            df['description_hashtag_count'] = df['description'].str.count(r'#\w+')
        
        # Tags features
        if 'tags' in df.columns:
            df['tag_count'] = df['tags'].apply(self._count_tags)
            df['avg_tag_length'] = df['tags'].apply(self._calculate_avg_tag_length)
        
        # Category features
        if 'category_id' in df.columns:
            df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').fillna(0)
            
            # Map category IDs to meaningful names
            category_mapping = {
                1: 'Film & Animation', 2: 'Autos & Vehicles', 10: 'Music',
                15: 'Pets & Animals', 17: 'Sports', 19: 'Travel & Events',
                20: 'Gaming', 22: 'People & Blogs', 23: 'Comedy',
                24: 'Entertainment', 25: 'News & Politics', 26: 'Howto & Style',
                27: 'Education', 28: 'Science & Technology'
            }
            df['category_name'] = df['category_id'].map(category_mapping).fillna('Other')
        
        # Duration-based features
        if 'duration_seconds' in df.columns:
            df['duration_minutes'] = df['duration_seconds'] / 60
            df['duration_category'] = pd.cut(
                df['duration_seconds'],
                bins=[0, 60, 300, 600, 1800, float('inf')],
                labels=['short', 'brief', 'medium', 'long', 'very_long']
            )
            
            # Optimal duration flags for different content types
            df['is_optimal_short'] = (df['duration_seconds'] >= 15) & (df['duration_seconds'] <= 60)
            df['is_optimal_longform'] = (df['duration_seconds'] >= 180) & (df['duration_seconds'] <= 480)
        
        # Temporal features
        if 'published_at' in df.columns:
            df['publish_hour'] = df['published_at'].dt.hour
            df['publish_day_of_week'] = df['published_at'].dt.dayofweek
            df['publish_month'] = df['published_at'].dt.month
            df['publish_year'] = df['published_at'].dt.year
            df['is_weekend'] = df['publish_day_of_week'].isin([5, 6])
            df['is_prime_time'] = df['publish_hour'].isin([19, 20, 21])  # 7-9 PM
            df['is_morning'] = df['publish_hour'].isin([6, 7, 8, 9])
            df['is_afternoon'] = df['publish_hour'].isin([12, 13, 14, 15])
            df['is_evening'] = df['publish_hour'].isin([18, 19, 20, 21])
            
            # Days since publication
            df['days_since_published'] = (pd.Timestamp.now() - df['published_at']).dt.days
            
            # Seasonal features
            df['season'] = df['publish_month'].map({
                12: 'winter', 1: 'winter', 2: 'winter',
                3: 'spring', 4: 'spring', 5: 'spring',
                6: 'summer', 7: 'summer', 8: 'summer',
                9: 'autumn', 10: 'autumn', 11: 'autumn'
            })
        
        # Thumbnail features
        thumbnail_cols = ['thumbnail_default', 'thumbnail_medium', 'thumbnail_high']
        for col in thumbnail_cols:
            if col in df.columns:
                df[f'{col}_available'] = df[col].notna() & (df[col] != '')
        
        logger.info("Content feature extraction completed")
        return df
    
    def _calculate_caps_ratio(self, text: str) -> float:
        """Calculate the ratio of uppercase characters in text."""
        if not text or len(text) == 0:
            return 0.0
        
        uppercase_count = sum(1 for c in text if c.isupper())
        return uppercase_count / len(text)
    
    def _count_emojis(self, text: str) -> int:
        """Count emojis in text."""
        if not text:
            return 0
        
        # Simple emoji detection (Unicode ranges)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE
        )
        return len(emoji_pattern.findall(text))
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text."""
        if not text or len(text.strip()) == 0:
            return 'unknown'
        
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'unknown'
    
    def _count_tags(self, tags_str: str) -> int:
        """Count number of tags."""
        if not tags_str or pd.isna(tags_str):
            return 0
        
        # Assuming tags are in a list format or comma-separated
        if tags_str.startswith('[') and tags_str.endswith(']'):
            try:
                import ast
                tags_list = ast.literal_eval(tags_str)
                return len(tags_list)
            except:
                return 0
        else:
            return len([tag.strip() for tag in tags_str.split(',') if tag.strip()])
    
    def _calculate_avg_tag_length(self, tags_str: str) -> float:
        """Calculate average tag length."""
        if not tags_str or pd.isna(tags_str):
            return 0.0
        
        try:
            if tags_str.startswith('[') and tags_str.endswith(']'):
                import ast
                tags_list = ast.literal_eval(tags_str)
                if tags_list:
                    return sum(len(tag) for tag in tags_list) / len(tags_list)
            else:
                tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                if tags:
                    return sum(len(tag) for tag in tags) / len(tags)
        except:
            pass
        
        return 0.0
    
    def extract_engagement_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract engagement-based features.
        
        Args:
            df: DataFrame with engagement data
            
        Returns:
            DataFrame with engagement features
        """
        logger.info("Extracting engagement features...")
        
        # Basic engagement ratios
        df['like_to_view_ratio'] = df['like_count'] / np.maximum(df['view_count'], 1)
        df['comment_to_view_ratio'] = df['comment_count'] / np.maximum(df['view_count'], 1)
        df['engagement_rate'] = (df['like_count'] + df['comment_count']) / np.maximum(df['view_count'], 1)
        
        # Engagement quality indicators
        df['high_engagement'] = df['engagement_rate'] > df['engagement_rate'].quantile(0.75)
        df['viral_potential'] = (df['like_to_view_ratio'] > 0.05) & (df['comment_to_view_ratio'] > 0.01)
        
        # Engagement velocity (if time-series data available)
        like_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_likes')]
        comment_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_comments')]
        
        if len(like_columns) >= 2:
            df['like_velocity'] = self._calculate_engagement_growth_rate(df, like_columns)
        
        if len(comment_columns) >= 2:
            df['comment_velocity'] = self._calculate_engagement_growth_rate(df, comment_columns)
        
        # Engagement consistency
        if len(like_columns) >= 3:
            df['like_consistency'] = self._calculate_growth_consistency(df, like_columns)
        
        if len(comment_columns) >= 3:
            df['comment_consistency'] = self._calculate_growth_consistency(df, comment_columns)
        
        logger.info("Engagement feature extraction completed")
        return df
    
    def create_channel_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create channel-level aggregated features.
        
        Args:
            df: DataFrame with channel data
            
        Returns:
            DataFrame with channel features
        """
        logger.info("Creating channel features...")
        
        if 'channel_id' not in df.columns:
            logger.warning("No channel_id column found, skipping channel features")
            return df
        
        # Calculate channel-level statistics
        channel_stats = df.groupby('channel_id').agg({
            'view_count': ['mean', 'median', 'std', 'count'],
            'like_count': ['mean', 'median'],
            'comment_count': ['mean', 'median'],
            'duration_seconds': ['mean', 'median'],
            'is_short': 'mean'  # Proportion of shorts
        }).round(2)
        
        # Flatten column names
        channel_stats.columns = ['_'.join(col).strip() for col in channel_stats.columns]
        
        # Rename for clarity
        channel_stats = channel_stats.rename(columns={
            'view_count_mean': 'channel_avg_views',
            'view_count_median': 'channel_median_views',
            'view_count_std': 'channel_view_std',
            'view_count_count': 'channel_video_count',
            'like_count_mean': 'channel_avg_likes',
            'comment_count_mean': 'channel_avg_comments',
            'duration_seconds_mean': 'channel_avg_duration',
            'is_short_mean': 'channel_shorts_ratio'
        })
        
        # Channel authority score (composite metric)
        channel_stats['channel_authority'] = (
            np.log1p(channel_stats['channel_avg_views']) * 0.4 +
            np.log1p(channel_stats['channel_video_count']) * 0.3 +
            channel_stats['channel_avg_likes'] / np.maximum(channel_stats['channel_avg_views'], 1) * 100 * 0.3
        )
        
        # Channel consistency score
        channel_stats['channel_consistency'] = 1 / (1 + channel_stats['channel_view_std'] / np.maximum(channel_stats['channel_avg_views'], 1))
        
        # Merge back to main dataframe
        df = df.merge(channel_stats, left_on='channel_id', right_index=True, how='left')
        
        # Channel performance relative to channel average
        df['relative_performance'] = df['view_count'] / np.maximum(df['channel_avg_views'], 1)
        df['above_channel_average'] = df['view_count'] > df['channel_avg_views']
        
        logger.info("Channel feature creation completed")
        return df
    
    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data into train, validation, and test sets with time-based splitting.
        
        Args:
            df: Complete DataFrame
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        logger.info("Splitting data with time-based approach...")
        
        # Sort by publication date for time-based split
        if 'published_at' in df.columns:
            df = df.sort_values('published_at').reset_index(drop=True)
            
            # Time-based split (older data for training, newer for testing)
            total_size = len(df)
            train_end = int(total_size * 0.7)
            val_end = int(total_size * 0.85)
            
            train_df = df[:train_end].copy()
            val_df = df[train_end:val_end].copy()
            test_df = df[val_end:].copy()
            
            logger.info("Used time-based splitting")
        else:
            # Random split if no time information
            df = df.sample(frac=1, random_state=self.config.get('random_state', 42)).reset_index(drop=True)
            
            total_size = len(df)
            test_size = int(total_size * self.config.get('test_size', 0.15))
            val_size = int(total_size * self.config.get('val_size', 0.15))
            train_size = total_size - test_size - val_size
            
            train_df = df[:train_size].copy()
            val_df = df[train_size:train_size + val_size].copy()
            test_df = df[train_size + val_size:].copy()
            
            logger.info("Used random splitting")
        
        logger.info(f"Data split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
        
        return train_df, val_df, test_df
    
    def save_processed_data(
        self, 
        train_df: pd.DataFrame, 
        val_df: pd.DataFrame, 
        test_df: pd.DataFrame
    ):
        """
        Save processed data to files.
        
        Args:
            train_df: Training data
            val_df: Validation data
            test_df: Test data
        """
        logger.info("Saving processed data...")
        
        # Save individual splits
        train_df.to_csv(self.output_dir / 'train_data.csv', index=False)
        val_df.to_csv(self.output_dir / 'val_data.csv', index=False)
        test_df.to_csv(self.output_dir / 'test_data.csv', index=False)
        
        # Save combined training data (train + val) for model training
        combined_train = pd.concat([train_df, val_df], ignore_index=True)
        combined_train.to_csv(self.output_dir / 'training_data.csv', index=False)
        
        # Save feature information
        feature_info = {
            'total_features': len(train_df.columns),
            'feature_names': list(train_df.columns),
            'target_variables': ['views_at_24h', 'views_at_7d', 'views_at_30d'],
            'categorical_features': self._identify_categorical_features(train_df),
            'numerical_features': self._identify_numerical_features(train_df),
            'time_series_features': self._identify_time_series_features(train_df),
            'content_features': self._identify_content_features(train_df),
            'engagement_features': self._identify_engagement_features(train_df),
            'channel_features': self._identify_channel_features(train_df),
            'created_at': datetime.now().isoformat(),
            'data_splits': {
                'train_samples': len(train_df),
                'val_samples': len(val_df),
                'test_samples': len(test_df),
                'total_samples': len(train_df) + len(val_df) + len(test_df),
                'shorts_samples': int((train_df['is_short'] == True).sum() + (val_df['is_short'] == True).sum() + (test_df['is_short'] == True).sum()),
                'longform_samples': int((train_df['is_short'] == False).sum() + (val_df['is_short'] == False).sum() + (test_df['is_short'] == False).sum())
            }
        }
        
        with open(self.output_dir / 'feature_info.json', 'w') as f:
            json.dump(feature_info, f, indent=2)
        
        logger.info(f"Processed data saved to {self.output_dir}")
        logger.info(f"Total features: {feature_info['total_features']}")
        logger.info(f"Shorts samples: {feature_info['data_splits']['shorts_samples']}")
        logger.info(f"Long-form samples: {feature_info['data_splits']['longform_samples']}")
    
    def _identify_categorical_features(self, df: pd.DataFrame) -> List[str]:
        """Identify categorical features in the DataFrame."""
        categorical_features = []
        
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                if col not in ['video_id', 'channel_id', 'title', 'description', 'tags']:
                    categorical_features.append(col)
            elif col in ['is_short', 'is_weekend', 'title_has_question', 'title_has_exclamation',
                        'high_engagement', 'viral_potential', 'above_channel_average',
                        'title_is_sinhala', 'title_is_tamil', 'title_is_english']:
                categorical_features.append(col)
        
        return categorical_features
    
    def _identify_numerical_features(self, df: pd.DataFrame) -> List[str]:
        """Identify numerical features in the DataFrame."""
        numerical_features = []
        
        exclude_cols = ['video_id', 'channel_id', 'views_at_24h', 'views_at_7d', 'views_at_30d',
                       'published_at', 'title', 'description', 'tags']
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64'] and col not in exclude_cols:
                numerical_features.append(col)
        
        return numerical_features
    
    def _identify_time_series_features(self, df: pd.DataFrame) -> List[str]:
        """Identify time-series derived features."""
        time_series_features = []
        
        for col in df.columns:
            if any(keyword in col for keyword in ['growth', 'velocity', 'consistency', 'peak_day', 'ratio_day']):
                time_series_features.append(col)
        
        return time_series_features
    
    def _identify_content_features(self, df: pd.DataFrame) -> List[str]:
        """Identify content-based features."""
        content_features = []
        
        for col in df.columns:
            if any(keyword in col for keyword in ['title_', 'description_', 'duration_', 'category_', 
                                                 'tag_', 'publish_', 'season', 'language']):
                content_features.append(col)
        
        return content_features
    
    def _identify_engagement_features(self, df: pd.DataFrame) -> List[str]:
        """Identify engagement-based features."""
        engagement_features = []
        
        for col in df.columns:
            if any(keyword in col for keyword in ['like_', 'comment_', 'engagement_', 'viral_']):
                engagement_features.append(col)
        
        return engagement_features
    
    def _identify_channel_features(self, df: pd.DataFrame) -> List[str]:
        """Identify channel-based features."""
        channel_features = []
        
        for col in df.columns:
            if col.startswith('channel_') or col in ['relative_performance', 'above_channel_average']:
                channel_features.append(col)
        
        return channel_features
    
    def generate_comprehensive_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive data processing report.
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Comprehensive report dictionary
        """
        logger.info("Generating comprehensive data report...")
        
        report = {
            'processing_summary': {
                'total_records': len(df),
                'total_features': len(df.columns),
                'shorts_count': int(df['is_short'].sum()) if 'is_short' in df.columns else 0,
                'longform_count': int((~df['is_short']).sum()) if 'is_short' in df.columns else 0,
                'date_range': {
                    'earliest': df['published_at'].min().isoformat() if 'published_at' in df.columns else None,
                    'latest': df['published_at'].max().isoformat() if 'published_at' in df.columns else None
                },
                'unique_channels': df['channel_id'].nunique() if 'channel_id' in df.columns else 0
            },
            'feature_analysis': {
                'categorical_features': len(self._identify_categorical_features(df)),
                'numerical_features': len(self._identify_numerical_features(df)),
                'time_series_features': len(self._identify_time_series_features(df)),
                'content_features': len(self._identify_content_features(df)),
                'engagement_features': len(self._identify_engagement_features(df)),
                'channel_features': len(self._identify_channel_features(df))
            },
            'data_quality': {
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_videos': df.duplicated(subset=['video_id']).sum() if 'video_id' in df.columns else 0,
                'zero_view_videos': int((df['view_count'] == 0).sum()) if 'view_count' in df.columns else 0
            },
            'target_variable_stats': {},
            'content_analysis': {},
            'engagement_analysis': {},
            'temporal_analysis': {},
            'generated_at': datetime.now().isoformat()
        }
        
        # Target variable statistics
        target_vars = ['views_at_24h', 'views_at_7d', 'views_at_30d']
        for target in target_vars:
            if target in df.columns:
                report['target_variable_stats'][target] = {
                    'mean': float(df[target].mean()),
                    'median': float(df[target].median()),
                    'std': float(df[target].std()),
                    'min': int(df[target].min()),
                    'max': int(df[target].max()),
                    'q25': float(df[target].quantile(0.25)),
                    'q75': float(df[target].quantile(0.75))
                }
        
        # Content analysis
        if 'duration_seconds' in df.columns:
            shorts_df = df[df['is_short'] == True] if 'is_short' in df.columns else pd.DataFrame()
            longform_df = df[df['is_short'] == False] if 'is_short' in df.columns else pd.DataFrame()
            
            report['content_analysis']['duration_stats'] = {
                'mean_seconds': float(df['duration_seconds'].mean()),
                'median_seconds': float(df['duration_seconds'].median()),
                'shorts_avg_duration': float(shorts_df['duration_seconds'].mean()) if len(shorts_df) > 0 else 0,
                'longform_avg_duration': float(longform_df['duration_seconds'].mean()) if len(longform_df) > 0 else 0
            }
        
        # Engagement analysis
        if 'engagement_rate' in df.columns:
            report['engagement_analysis'] = {
                'avg_engagement_rate': float(df['engagement_rate'].mean()),
                'high_engagement_videos': int(df['high_engagement'].sum()) if 'high_engagement' in df.columns else 0,
                'viral_potential_videos': int(df['viral_potential'].sum()) if 'viral_potential' in df.columns else 0
            }
        
        # Temporal analysis
        if 'publish_hour' in df.columns:
            report['temporal_analysis'] = {
                'peak_hours': df['publish_hour'].value_counts().head(3).to_dict(),
                'weekend_videos': int(df['is_weekend'].sum()) if 'is_weekend' in df.columns else 0,
                'prime_time_videos': int(df['is_prime_time'].sum()) if 'is_prime_time' in df.columns else 0
            }
        
        return report
    
    def run_complete_pipeline(self, csv_path: str) -> Dict[str, Any]:
        """
        Run the complete CSV processing pipeline.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Pipeline results dictionary
        """
        logger.info("Starting complete CSV processing pipeline...")
        start_time = datetime.now()
        
        try:
            # Load CSV data
            raw_data = self.load_csv_data(csv_path)
            
            # Clean and standardize data
            clean_data = self.clean_and_standardize_data(raw_data)
            
            # Extract time-series features
            ts_data = self.extract_time_series_features(clean_data)
            
            # Extract content features
            content_data = self.extract_content_features(ts_data)
            
            # Extract engagement features
            engagement_data = self.extract_engagement_features(content_data)
            
            # Create channel features
            final_data = self.create_channel_features(engagement_data)
            
            # Split data
            train_df, val_df, test_df = self.split_data(final_data)
            
            # Save processed data
            self.save_processed_data(train_df, val_df, test_df)
            
            # Generate comprehensive report
            data_report = self.generate_comprehensive_report(final_data)
            
            # Save report
            with open(self.output_dir / 'processing_report.json', 'w') as f:
                json.dump(data_report, f, indent=2, default=str)
            
            # Compile results
            end_time = datetime.now()
            processing_duration = (end_time - start_time).total_seconds()
            
            results = {
                'pipeline_status': 'completed',
                'processing_duration_seconds': processing_duration,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'input_file': csv_path,
                'output_directory': str(self.output_dir),
                'data_report': data_report,
                'config_used': self.config
            }
            
            logger.info(f"CSV processing completed in {processing_duration:.1f} seconds")
            logger.info(f"Final dataset: {len(final_data)} records with {len(final_data.columns)} features")
            
            return results
            
        except Exception as e:
            logger.error(f"CSV processing pipeline failed: {e}")
            raise


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""
    
    default_config = {
        'output_dir': 'data/processed',
        'test_size': 0.15,
        'val_size': 0.15,
        'random_state': 42,
        'remove_outliers': True,
        'min_view_count': 1,
        'max_duration_hours': 4,
        'max_video_age_days': 730
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
            
            default_config.update(file_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.warning(f"Error loading config file {config_path}: {e}")
            logger.info("Using default configuration")
    
    return default_config


def main():
    """Main CSV processing script entry point."""
    parser = argparse.ArgumentParser(description='Process ViewTrendsSL CSV data for model training')
    
    parser.add_argument(
        'csv_path',
        help='Path to the CSV file to process'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory to save processed data'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate data without processing'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Override with command line arguments
        if args.output_dir:
            config['output_dir'] = args.output_dir
        
        # Validate input file
        if not os.path.exists(args.csv_path):
            logger.error(f"Input file not found: {args.csv_path}")
            return 1
        
        # Initialize processor
        processor = EnhancedCSVProcessor(config)
        
        if args.dry_run:
            logger.info("Dry run mode - validating data...")
            raw_data = processor.load_csv_data(args.csv_path)
            logger.info(f"Data validation completed. Found {len(raw_data)} records")
            return 0
        
        # Run pipeline
        results = processor.run_complete_pipeline(args.csv_path)
        
        logger.info("CSV processing completed successfully!")
        logger.info(f"Processed data saved to: {results['output_directory']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"CSV processing failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
