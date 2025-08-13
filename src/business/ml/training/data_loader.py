"""
Data Loading Utilities for ML Training

This module provides utilities for loading and preparing data for machine learning
model training, including train/validation/test splits and data filtering.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sqlite3
from sklearn.model_selection import train_test_split

from src.data_access.repositories.video.video_repository import VideoRepository
from src.business.utils.data_validator import DataValidator

logger = logging.getLogger(__name__)


class DataLoader:
    """Data loading and preparation utilities for ML training."""
    
    def __init__(self, database_path: str = "data/viewtrendssl.db"):
        """
        Initialize the data loader.
        
        Args:
            database_path: Path to the SQLite database
        """
        self.database_path = database_path
        self.video_repository = VideoRepository()
        self.data_validator = DataValidator()
        
        # Data loading configuration
        self.config = {
            'min_views_threshold': 10,  # Minimum views to include video
            'max_duration_shorts': 60,  # Maximum duration for Shorts (seconds)
            'min_duration_longform': 61,  # Minimum duration for long-form
            'min_channel_subscribers': 100,  # Minimum channel subscribers
            'exclude_categories': [29, 30],  # Categories to exclude (e.g., non-profits)
            'min_data_points': 5,  # Minimum snapshots per video
            'test_size': 0.2,  # Test set proportion
            'val_size': 0.2,  # Validation set proportion (of remaining data)
            'random_state': 42
        }
        
        logger.info("DataLoader initialized")
    
    def load_training_data(self, 
                          video_type: str = 'all',
                          target_timeframe: int = 7,
                          min_age_days: int = 30,
                          max_age_days: int = 365,
                          include_features: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load training data from the database.
        
        Args:
            video_type: Type of videos ('shorts', 'longform', 'all')
            target_timeframe: Target prediction timeframe in days
            min_age_days: Minimum video age in days
            max_age_days: Maximum video age in days
            include_features: Optional list of specific features to include
            
        Returns:
            DataFrame with training data
        """
        try:
            logger.info(f"Loading training data for {video_type} videos")
            
            # Calculate date range
            end_date = datetime.now() - timedelta(days=min_age_days)
            start_date = datetime.now() - timedelta(days=max_age_days)
            
            # Load raw data
            query = self._build_training_query(video_type, start_date, end_date, target_timeframe)
            
            with sqlite3.connect(self.database_path) as conn:
                df = pd.read_sql_query(query, conn)
            
            if df.empty:
                logger.warning("No training data found matching criteria")
                return df
            
            logger.info(f"Loaded {len(df)} raw training samples")
            
            # Apply filters and validation
            df = self._apply_filters(df, video_type)
            df = self._validate_and_clean_data(df)
            
            # Engineer features
            df = self._engineer_features(df, include_features)
            
            # Create target variable
            df = self._create_target_variable(df, target_timeframe)
            
            logger.info(f"Final training dataset: {len(df)} samples, {len(df.columns)} features")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
            raise
    
    def split_data(self, 
                   data: pd.DataFrame,
                   stratify_column: Optional[str] = None,
                   time_based_split: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data into train, validation, and test sets.
        
        Args:
            data: Input dataset
            stratify_column: Column to use for stratification
            time_based_split: Whether to use time-based splitting
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        try:
            logger.info("Splitting data into train/validation/test sets")
            
            if time_based_split and 'published_at' in data.columns:
                # Time-based split (most recent data for test)
                data_sorted = data.sort_values('published_at')
                
                n_total = len(data_sorted)
                n_test = int(n_total * self.config['test_size'])
                n_val = int((n_total - n_test) * self.config['val_size'])
                
                test_df = data_sorted.tail(n_test).copy()
                remaining_df = data_sorted.head(n_total - n_test).copy()
                val_df = remaining_df.tail(n_val).copy()
                train_df = remaining_df.head(len(remaining_df) - n_val).copy()
                
            else:
                # Random split
                stratify = data[stratify_column] if stratify_column else None
                
                # First split: train+val vs test
                train_val_df, test_df = train_test_split(
                    data,
                    test_size=self.config['test_size'],
                    random_state=self.config['random_state'],
                    stratify=stratify
                )
                
                # Second split: train vs val
                if stratify_column:
                    stratify_train_val = train_val_df[stratify_column]
                else:
                    stratify_train_val = None
                
                train_df, val_df = train_test_split(
                    train_val_df,
                    test_size=self.config['val_size'],
                    random_state=self.config['random_state'],
                    stratify=stratify_train_val
                )
            
            logger.info(f"Data split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
            
            return train_df, val_df, test_df
            
        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            raise
    
    def load_prediction_data(self, 
                           video_ids: List[str],
                           include_features: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load data for making predictions on specific videos.
        
        Args:
            video_ids: List of video IDs
            include_features: Optional list of specific features to include
            
        Returns:
            DataFrame with prediction data
        """
        try:
            logger.info(f"Loading prediction data for {len(video_ids)} videos")
            
            # Build query for specific videos
            placeholders = ','.join(['?' for _ in video_ids])
            query = f"""
            SELECT 
                v.video_id,
                v.title,
                v.description,
                v.published_at,
                v.duration_seconds,
                v.category_id,
                v.channel_id,
                c.subscriber_count as channel_subscriber_count,
                c.video_count as channel_video_count,
                c.country as channel_country,
                GROUP_CONCAT(t.tag_name) as tags,
                vs.view_count,
                vs.like_count,
                vs.comment_count
            FROM videos v
            LEFT JOIN channels c ON v.channel_id = c.channel_id
            LEFT JOIN video_tags vt ON v.video_id = vt.video_id
            LEFT JOIN tags t ON vt.tag_id = t.tag_id
            LEFT JOIN video_statistics vs ON v.video_id = vs.video_id
            WHERE v.video_id IN ({placeholders})
            GROUP BY v.video_id
            """
            
            with sqlite3.connect(self.database_path) as conn:
                df = pd.read_sql_query(query, conn, params=video_ids)
            
            if df.empty:
                logger.warning("No prediction data found for provided video IDs")
                return df
            
            # Engineer features
            df = self._engineer_features(df, include_features)
            
            logger.info(f"Loaded prediction data: {len(df)} videos, {len(df.columns)} features")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading prediction data: {str(e)}")
            raise
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for the dataset.
        
        Args:
            data: Input dataset
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            summary = {
                'total_samples': len(data),
                'features': len(data.columns),
                'missing_values': data.isnull().sum().sum(),
                'date_range': {},
                'video_types': {},
                'categories': {},
                'channels': {}
            }
            
            # Date range
            if 'published_at' in data.columns:
                summary['date_range'] = {
                    'earliest': data['published_at'].min(),
                    'latest': data['published_at'].max(),
                    'span_days': (pd.to_datetime(data['published_at'].max()) - 
                                pd.to_datetime(data['published_at'].min())).days
                }
            
            # Video types
            if 'is_short' in data.columns:
                summary['video_types'] = {
                    'shorts': int(data['is_short'].sum()),
                    'longform': int(len(data) - data['is_short'].sum())
                }
            
            # Categories
            if 'category_id' in data.columns:
                summary['categories'] = data['category_id'].value_counts().head(10).to_dict()
            
            # Channels
            if 'channel_id' in data.columns:
                summary['channels'] = {
                    'unique_channels': data['channel_id'].nunique(),
                    'avg_videos_per_channel': len(data) / data['channel_id'].nunique()
                }
            
            # Target variable statistics
            target_cols = [col for col in data.columns if col.startswith('views_')]
            if target_cols:
                target_col = target_cols[0]
                summary['target_stats'] = {
                    'mean': float(data[target_col].mean()),
                    'median': float(data[target_col].median()),
                    'std': float(data[target_col].std()),
                    'min': float(data[target_col].min()),
                    'max': float(data[target_col].max())
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating data summary: {str(e)}")
            return {}
    
    def save_processed_data(self, 
                          data: pd.DataFrame, 
                          filename: str,
                          data_type: str = 'training') -> bool:
        """
        Save processed data to disk.
        
        Args:
            data: DataFrame to save
            filename: Output filename
            data_type: Type of data ('training', 'validation', 'test')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_dir = Path("data/processed")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / filename
            
            # Save as both CSV and Parquet for flexibility
            data.to_csv(output_path.with_suffix('.csv'), index=False)
            data.to_parquet(output_path.with_suffix('.parquet'), index=False)
            
            # Save metadata
            metadata = {
                'data_type': data_type,
                'samples': len(data),
                'features': len(data.columns),
                'created_at': datetime.now().isoformat(),
                'columns': list(data.columns)
            }
            
            import json
            with open(output_path.with_suffix('.json'), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Saved {data_type} data to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            return False
    
    # Private helper methods
    def _build_training_query(self, 
                            video_type: str, 
                            start_date: datetime, 
                            end_date: datetime,
                            target_timeframe: int) -> str:
        """Build SQL query for training data."""
        
        # Base query
        query = """
        SELECT 
            v.video_id,
            v.title,
            v.description,
            v.published_at,
            v.duration_seconds,
            v.category_id,
            v.channel_id,
            c.subscriber_count as channel_subscriber_count,
            c.video_count as channel_video_count,
            c.country as channel_country,
            GROUP_CONCAT(t.tag_name) as tags,
            
            -- Get view counts at different time points
            MAX(CASE WHEN s.days_since_published = 1 THEN s.view_count END) as views_1_day,
            MAX(CASE WHEN s.days_since_published = 3 THEN s.view_count END) as views_3_days,
            MAX(CASE WHEN s.days_since_published = 7 THEN s.view_count END) as views_7_days,
            MAX(CASE WHEN s.days_since_published = 30 THEN s.view_count END) as views_30_days,
            
            -- Get engagement metrics
            MAX(CASE WHEN s.days_since_published = {target_timeframe} THEN s.like_count END) as likes_target,
            MAX(CASE WHEN s.days_since_published = {target_timeframe} THEN s.comment_count END) as comments_target
            
        FROM videos v
        LEFT JOIN channels c ON v.channel_id = c.channel_id
        LEFT JOIN video_tags vt ON v.video_id = vt.video_id
        LEFT JOIN tags t ON vt.tag_id = t.tag_id
        LEFT JOIN (
            SELECT 
                video_id,
                view_count,
                like_count,
                comment_count,
                CAST((julianday(recorded_at) - julianday(published_at)) AS INTEGER) as days_since_published
            FROM snapshots s2
            JOIN videos v2 ON s2.video_id = v2.video_id
        ) s ON v.video_id = s.video_id
        
        WHERE v.published_at BETWEEN ? AND ?
        """.format(target_timeframe=target_timeframe)
        
        # Add video type filter
        if video_type == 'shorts':
            query += f" AND v.duration_seconds <= {self.config['max_duration_shorts']}"
        elif video_type == 'longform':
            query += f" AND v.duration_seconds > {self.config['min_duration_longform']}"
        
        query += """
        GROUP BY v.video_id
        HAVING COUNT(s.video_id) >= ?
        ORDER BY v.published_at DESC
        """
        
        return query
    
    def _apply_filters(self, df: pd.DataFrame, video_type: str) -> pd.DataFrame:
        """Apply data quality filters."""
        
        initial_count = len(df)
        
        # Remove videos with insufficient views
        df = df[df['views_7_days'] >= self.config['min_views_threshold']]
        
        # Remove videos from channels with too few subscribers
        df = df[df['channel_subscriber_count'] >= self.config['min_channel_subscribers']]
        
        # Remove excluded categories
        df = df[~df['category_id'].isin(self.config['exclude_categories'])]
        
        # Remove videos with missing critical data
        critical_columns = ['views_7_days', 'duration_seconds', 'channel_subscriber_count']
        df = df.dropna(subset=critical_columns)
        
        logger.info(f"Applied filters: {initial_count} -> {len(df)} samples")
        
        return df
    
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the data."""
        
        # Convert data types
        df['published_at'] = pd.to_datetime(df['published_at'])
        df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
        
        # Handle missing values
        df['description'] = df['description'].fillna('')
        df['tags'] = df['tags'].fillna('')
        df['channel_country'] = df['channel_country'].fillna('Unknown')
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['video_id'])
        
        # Validate data ranges
        df = df[df['duration_seconds'] > 0]
        df = df[df['views_7_days'] >= 0]
        
        return df
    
    def _engineer_features(self, df: pd.DataFrame, include_features: Optional[List[str]] = None) -> pd.DataFrame:
        """Engineer features for ML training."""
        
        # Time-based features
        df['publish_hour'] = df['published_at'].dt.hour
        df['publish_day_of_week'] = df['published_at'].dt.dayofweek
        df['is_weekend'] = (df['publish_day_of_week'] >= 5).astype(int)
        
        # Video type
        df['is_short'] = (df['duration_seconds'] <= self.config['max_duration_shorts']).astype(int)
        df['duration_minutes'] = df['duration_seconds'] / 60
        
        # Text features
        df['title_length'] = df['title'].str.len()
        df['description_length'] = df['description'].str.len()
        df['title_word_count'] = df['title'].str.split().str.len()
        df['description_word_count'] = df['description'].str.split().str.len()
        
        # Title analysis
        df['has_question_in_title'] = df['title'].str.contains(r'\?', na=False).astype(int)
        df['has_exclamation_in_title'] = df['title'].str.contains(r'!', na=False).astype(int)
        df['title_caps_ratio'] = df['title'].apply(lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(str(x)), 1))
        
        # Tag features
        df['tag_count'] = df['tags'].str.split(',').str.len()
        df['has_tags'] = (df['tag_count'] > 0).astype(int)
        
        # Channel features
        df['channel_authority_score'] = np.log1p(df['channel_subscriber_count']) * np.log1p(df['channel_video_count'])
        
        # Sri Lankan content detection (basic)
        sri_lankan_keywords = ['sri lanka', 'srilanka', 'colombo', 'kandy', 'galle', 'sinhala', 'tamil']
        df['is_sri_lankan_content'] = df.apply(
            lambda row: any(keyword in str(row['title']).lower() + ' ' + str(row['description']).lower() 
                          for keyword in sri_lankan_keywords), axis=1
        ).astype(int)
        
        # Filter features if specified
        if include_features:
            available_features = [col for col in include_features if col in df.columns]
            essential_cols = ['video_id', 'published_at']  # Always keep these
            df = df[essential_cols + available_features]
        
        return df
    
    def _create_target_variable(self, df: pd.DataFrame, target_timeframe: int) -> pd.DataFrame:
        """Create target variable for the specified timeframe."""
        
        target_col = f'views_{target_timeframe}_days'
        
        if target_col not in df.columns:
            # If exact timeframe not available, interpolate or use closest
            available_timeframes = [col for col in df.columns if col.startswith('views_') and col.endswith('_days')]
            
            if available_timeframes:
                # Use the closest available timeframe
                timeframe_nums = []
                for col in available_timeframes:
                    try:
                        num = int(col.split('_')[1])
                        timeframe_nums.append((abs(num - target_timeframe), col))
                    except:
                        continue
                
                if timeframe_nums:
                    closest_col = min(timeframe_nums)[1]
                    df[target_col] = df[closest_col]
                    logger.info(f"Using {closest_col} as target for {target_timeframe}-day prediction")
                else:
                    # Fallback to views_7_days
                    df[target_col] = df.get('views_7_days', 0)
            else:
                # No timeframe columns available
                logger.warning("No timeframe view columns found, using current view_count")
                df[target_col] = df.get('view_count', 0)
        
        return df
