"""
Data Preparation Script for ViewTrendsSL

This script handles the preprocessing and preparation of raw YouTube data
for machine learning model training. It includes data cleaning, feature engineering,
and dataset splitting.

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

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from src.business.ml.preprocessing.feature_pipeline import FeaturePipeline
from src.business.utils.data_validator import DataValidator
from src.business.utils.feature_extractor import FeatureExtractor
from src.business.utils.time_utils import get_current_utc_time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataPreparationPipeline:
    """Complete pipeline for preparing YouTube data for model training."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data preparation pipeline.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.validator = DataValidator()
        self.feature_extractor = FeatureExtractor()
        self.feature_pipeline = FeaturePipeline()
        
        # Create output directories
        self.output_dir = Path(config.get('output_dir', 'data/processed'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Data preparation pipeline initialized. Output: {self.output_dir}")
    
    def load_raw_data(self, data_paths: List[str]) -> pd.DataFrame:
        """
        Load raw data from multiple sources.
        
        Args:
            data_paths: List of paths to raw data files
            
        Returns:
            Combined DataFrame with raw data
        """
        logger.info("Loading raw data...")
        
        all_data = []
        
        for data_path in data_paths:
            if not os.path.exists(data_path):
                logger.warning(f"Data file not found: {data_path}")
                continue
            
            try:
                if data_path.endswith('.csv'):
                    df = pd.read_csv(data_path)
                elif data_path.endswith('.json'):
                    df = pd.read_json(data_path)
                else:
                    logger.warning(f"Unsupported file format: {data_path}")
                    continue
                
                logger.info(f"Loaded {len(df)} records from {data_path}")
                all_data.append(df)
                
            except Exception as e:
                logger.error(f"Error loading {data_path}: {e}")
                continue
        
        if not all_data:
            raise ValueError("No data could be loaded from the provided paths")
        
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Remove duplicates based on video_id
        if 'video_id' in combined_data.columns:
            initial_count = len(combined_data)
            combined_data = combined_data.drop_duplicates(subset=['video_id'])
            final_count = len(combined_data)
            
            if initial_count != final_count:
                logger.info(f"Removed {initial_count - final_count} duplicate videos")
        
        logger.info(f"Total combined data: {len(combined_data)} records")
        return combined_data
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the raw data.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data...")
        
        initial_count = len(df)
        
        # Validate required columns
        required_columns = [
            'video_id', 'title', 'channel_id', 'published_at',
            'view_count', 'like_count', 'comment_count', 'duration_seconds'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['video_id', 'title', 'view_count'])
        logger.info(f"Removed {initial_count - len(df)} rows with missing critical data")
        
        # Clean numeric columns
        numeric_columns = ['view_count', 'like_count', 'comment_count', 'duration_seconds']
        for col in numeric_columns:
            if col in df.columns:
                # Convert to numeric, replacing invalid values with 0
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                # Ensure non-negative values
                df[col] = df[col].clip(lower=0)
        
        # Clean text columns
        text_columns = ['title', 'description']
        for col in text_columns:
            if col in df.columns:
                # Fill missing values with empty string
                df[col] = df[col].fillna('')
                
                # Remove excessive whitespace
                df[col] = df[col].str.strip()
        
        # Parse published_at to datetime
        if 'published_at' in df.columns:
            df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
            
            # Remove rows with invalid dates
            before_date_clean = len(df)
            df = df.dropna(subset=['published_at'])
            logger.info(f"Removed {before_date_clean - len(df)} rows with invalid dates")
        
        # Determine if video is a Short
        if 'duration_seconds' in df.columns:
            df['is_short'] = df['duration_seconds'] <= 60
        
        # Remove outliers
        df = self._remove_outliers(df)
        
        logger.info(f"Data cleaning completed. Final count: {len(df)} records")
        return df
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove statistical outliers from the data."""
        
        initial_count = len(df)
        
        # Remove videos with extremely high view counts (likely viral outliers)
        view_threshold = df['view_count'].quantile(0.99)
        df = df[df['view_count'] <= view_threshold]
        
        # Remove videos with zero engagement (likely deleted or private)
        df = df[df['view_count'] > 0]
        
        # Remove videos with unrealistic durations
        if 'duration_seconds' in df.columns:
            # Remove videos longer than 4 hours (14400 seconds)
            df = df[df['duration_seconds'] <= 14400]
            
            # Remove videos with 0 duration
            df = df[df['duration_seconds'] > 0]
        
        # Remove very old videos (older than 2 years)
        if 'published_at' in df.columns:
            cutoff_date = datetime.now() - timedelta(days=730)
            df = df[df['published_at'] >= cutoff_date]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} outlier records")
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for machine learning.
        
        Args:
            df: Cleaned DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering features...")
        
        # Extract basic features
        df = self.feature_extractor.extract_all_features(df)
        
        # Add time-based features
        if 'published_at' in df.columns:
            df['publish_hour'] = df['published_at'].dt.hour
            df['publish_day_of_week'] = df['published_at'].dt.dayofweek
            df['publish_month'] = df['published_at'].dt.month
            df['is_weekend'] = df['publish_day_of_week'].isin([5, 6])
            
            # Time since publication (in days)
            df['days_since_published'] = (
                pd.Timestamp.now() - df['published_at']
            ).dt.days
        
        # Engagement ratios
        df['like_to_view_ratio'] = df['like_count'] / np.maximum(df['view_count'], 1)
        df['comment_to_view_ratio'] = df['comment_count'] / np.maximum(df['view_count'], 1)
        df['engagement_rate'] = (df['like_count'] + df['comment_count']) / np.maximum(df['view_count'], 1)
        
        # Video length categories
        if 'duration_seconds' in df.columns:
            df['duration_category'] = pd.cut(
                df['duration_seconds'],
                bins=[0, 60, 300, 600, 1800, float('inf')],
                labels=['short', 'brief', 'medium', 'long', 'very_long']
            )
        
        # Title and description features
        if 'title' in df.columns:
            df['title_length'] = df['title'].str.len()
            df['title_word_count'] = df['title'].str.split().str.len()
            df['title_has_question'] = df['title'].str.contains(r'\?', na=False)
            df['title_has_exclamation'] = df['title'].str.contains(r'!', na=False)
            df['title_all_caps_ratio'] = df['title'].apply(self._calculate_caps_ratio)
        
        if 'description' in df.columns:
            df['description_length'] = df['description'].str.len()
            df['description_word_count'] = df['description'].str.split().str.len()
        
        # Channel-level features (if available)
        if 'subscriber_count' in df.columns:
            df['subscriber_category'] = pd.cut(
                df['subscriber_count'],
                bins=[0, 1000, 10000, 100000, 1000000, float('inf')],
                labels=['micro', 'small', 'medium', 'large', 'mega']
            )
        
        logger.info(f"Feature engineering completed. Total features: {len(df.columns)}")
        return df
    
    def _calculate_caps_ratio(self, text: str) -> float:
        """Calculate the ratio of uppercase characters in text."""
        if not text or len(text) == 0:
            return 0.0
        
        uppercase_count = sum(1 for c in text if c.isupper())
        return uppercase_count / len(text)
    
    def create_target_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create target variables for prediction.
        
        Args:
            df: DataFrame with features
            
        Returns:
            DataFrame with target variables
        """
        logger.info("Creating target variables...")
        
        # For this implementation, we'll use current view_count as proxy
        # In a real scenario, you would have time-series data
        
        # Create synthetic time-based targets based on current metrics
        # This is a simplified approach for demonstration
        
        base_views = df['view_count'].copy()
        
        # Simulate views at different time points
        # These would normally come from your time-series tracking data
        df['views_at_24h'] = base_views * np.random.uniform(0.1, 0.3, len(df))
        df['views_at_7d'] = base_views * np.random.uniform(0.5, 0.8, len(df))
        df['views_at_30d'] = base_views * np.random.uniform(0.8, 1.0, len(df))
        
        # Ensure logical progression (24h <= 7d <= 30d <= total)
        df['views_at_24h'] = np.minimum(df['views_at_24h'], df['views_at_7d'])
        df['views_at_7d'] = np.minimum(df['views_at_7d'], df['views_at_30d'])
        df['views_at_30d'] = np.minimum(df['views_at_30d'], base_views)
        
        logger.warning("Using synthetic target variables. Replace with real time-series data.")
        
        return df
    
    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data into train, validation, and test sets.
        
        Args:
            df: Complete DataFrame
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        logger.info("Splitting data...")
        
        # Shuffle the data
        df = df.sample(frac=1, random_state=self.config.get('random_state', 42)).reset_index(drop=True)
        
        # Calculate split sizes
        total_size = len(df)
        test_size = int(total_size * self.config.get('test_size', 0.2))
        val_size = int(total_size * self.config.get('val_size', 0.2))
        train_size = total_size - test_size - val_size
        
        # Split the data
        train_df = df[:train_size].copy()
        val_df = df[train_size:train_size + val_size].copy()
        test_df = df[train_size + val_size:].copy()
        
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
            'created_at': get_current_utc_time().isoformat(),
            'data_splits': {
                'train_samples': len(train_df),
                'val_samples': len(val_df),
                'test_samples': len(test_df),
                'total_samples': len(train_df) + len(val_df) + len(test_df)
            }
        }
        
        import json
        with open(self.output_dir / 'feature_info.json', 'w') as f:
            json.dump(feature_info, f, indent=2)
        
        logger.info(f"Processed data saved to {self.output_dir}")
    
    def _identify_categorical_features(self, df: pd.DataFrame) -> List[str]:
        """Identify categorical features in the DataFrame."""
        categorical_features = []
        
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                categorical_features.append(col)
            elif col in ['is_short', 'is_weekend', 'title_has_question', 'title_has_exclamation']:
                categorical_features.append(col)
        
        return categorical_features
    
    def _identify_numerical_features(self, df: pd.DataFrame) -> List[str]:
        """Identify numerical features in the DataFrame."""
        numerical_features = []
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64'] and col not in [
                'video_id', 'channel_id', 'views_at_24h', 'views_at_7d', 'views_at_30d'
            ]:
                numerical_features.append(col)
        
        return numerical_features
    
    def generate_data_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive data report.
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Data report dictionary
        """
        logger.info("Generating data report...")
        
        report = {
            'dataset_summary': {
                'total_records': len(df),
                'total_features': len(df.columns),
                'shorts_count': int(df['is_short'].sum()) if 'is_short' in df.columns else 0,
                'longform_count': int((~df['is_short']).sum()) if 'is_short' in df.columns else 0,
                'date_range': {
                    'earliest': df['published_at'].min().isoformat() if 'published_at' in df.columns else None,
                    'latest': df['published_at'].max().isoformat() if 'published_at' in df.columns else None
                }
            },
            'data_quality': {
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_videos': df.duplicated(subset=['video_id']).sum() if 'video_id' in df.columns else 0
            },
            'statistics': {
                'view_count': {
                    'mean': float(df['view_count'].mean()),
                    'median': float(df['view_count'].median()),
                    'std': float(df['view_count'].std()),
                    'min': int(df['view_count'].min()),
                    'max': int(df['view_count'].max())
                } if 'view_count' in df.columns else {},
                'duration_seconds': {
                    'mean': float(df['duration_seconds'].mean()),
                    'median': float(df['duration_seconds'].median()),
                    'std': float(df['duration_seconds'].std()),
                    'min': int(df['duration_seconds'].min()),
                    'max': int(df['duration_seconds'].max())
                } if 'duration_seconds' in df.columns else {}
            },
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def run_complete_pipeline(self, data_paths: List[str]) -> Dict[str, Any]:
        """
        Run the complete data preparation pipeline.
        
        Args:
            data_paths: List of paths to raw data files
            
        Returns:
            Pipeline results dictionary
        """
        logger.info("Starting complete data preparation pipeline...")
        start_time = datetime.now()
        
        try:
            # Load raw data
            raw_data = self.load_raw_data(data_paths)
            
            # Clean data
            clean_data = self.clean_data(raw_data)
            
            # Engineer features
            featured_data = self.engineer_features(clean_data)
            
            # Create target variables
            final_data = self.create_target_variables(featured_data)
            
            # Split data
            train_df, val_df, test_df = self.split_data(final_data)
            
            # Save processed data
            self.save_processed_data(train_df, val_df, test_df)
            
            # Generate report
            data_report = self.generate_data_report(final_data)
            
            # Save report
            import json
            with open(self.output_dir / 'data_report.json', 'w') as f:
                json.dump(data_report, f, indent=2, default=str)
            
            # Compile results
            end_time = datetime.now()
            processing_duration = (end_time - start_time).total_seconds()
            
            results = {
                'pipeline_status': 'completed',
                'processing_duration_seconds': processing_duration,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'input_files': data_paths,
                'output_directory': str(self.output_dir),
                'data_report': data_report,
                'config_used': self.config
            }
            
            logger.info(f"Data preparation completed in {processing_duration:.1f} seconds")
            logger.info(f"Final dataset: {len(final_data)} records with {len(final_data.columns)} features")
            
            return results
            
        except Exception as e:
            logger.error(f"Data preparation pipeline failed: {e}")
            raise


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""
    
    default_config = {
        'output_dir': 'data/processed',
        'test_size': 0.2,
        'val_size': 0.2,
        'random_state': 42,
        'remove_outliers': True,
        'min_view_count': 1,
        'max_duration_hours': 4,
        'max_video_age_days': 730
    }
    
    if config_path and os.path.exists(config_path):
        try:
            import json
            with open(config_path, 'r') as f:
                file_config = json.load(f)
            
            default_config.update(file_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.warning(f"Error loading config file {config_path}: {e}")
            logger.info("Using default configuration")
    
    return default_config


def main():
    """Main data preparation script entry point."""
    parser = argparse.ArgumentParser(description='Prepare YouTube data for model training')
    
    parser.add_argument(
        'data_paths',
        nargs='+',
        help='Paths to raw data files (CSV or JSON)'
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
        
        # Validate input files
        for data_path in args.data_paths:
            if not os.path.exists(data_path):
                logger.error(f"Input file not found: {data_path}")
                return 1
        
        # Initialize pipeline
        pipeline = DataPreparationPipeline(config)
        
        if args.dry_run:
            logger.info("Dry run mode - validating data...")
            raw_data = pipeline.load_raw_data(args.data_paths)
            logger.info(f"Data validation completed. Found {len(raw_data)} records")
            return 0
        
        # Run pipeline
        results = pipeline.run_complete_pipeline(args.data_paths)
        
        logger.info("Data preparation completed successfully!")
        logger.info(f"Processed data saved to: {results['output_directory']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Data preparation failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
