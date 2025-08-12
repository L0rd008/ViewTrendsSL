#!/usr/bin/env python3
"""
Data Validation Script

This script validates collected YouTube data for quality, completeness,
and consistency before it's used for model training.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import json
import csv
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import argparse
import re

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataValidator:
    """Validates YouTube data quality and consistency."""
    
    def __init__(self):
        """Initialize the data validator."""
        self.validation_results = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'warnings': [],
            'errors': [],
            'quality_score': 0.0,
            'validation_timestamp': datetime.now().isoformat()
        }
    
    def validate_video_data(self, data_file: str) -> Dict[str, Any]:
        """
        Validate video data from a CSV or JSON file.
        
        Args:
            data_file: Path to the data file
            
        Returns:
            Dictionary containing validation results
        """
        logger.info(f"Starting validation of {data_file}")
        
        # Load data
        df = self._load_data(data_file)
        if df is None:
            return self.validation_results
        
        self.validation_results['total_records'] = len(df)
        
        # Run validation checks
        self._validate_required_fields(df)
        self._validate_data_types(df)
        self._validate_value_ranges(df)
        self._validate_consistency(df)
        self._validate_sri_lankan_content(df)
        self._check_duplicates(df)
        self._validate_temporal_data(df)
        
        # Calculate quality score
        self._calculate_quality_score()
        
        logger.info(f"Validation completed. Quality score: {self.validation_results['quality_score']:.2f}")
        
        return self.validation_results
    
    def _load_data(self, data_file: str) -> Optional[pd.DataFrame]:
        """
        Load data from file into pandas DataFrame.
        
        Args:
            data_file: Path to the data file
            
        Returns:
            DataFrame or None if loading fails
        """
        try:
            if data_file.endswith('.csv'):
                df = pd.read_csv(data_file, encoding='utf-8')
            elif data_file.endswith('.json'):
                df = pd.read_json(data_file, encoding='utf-8')
            else:
                self.validation_results['errors'].append(f"Unsupported file format: {data_file}")
                return None
            
            logger.info(f"Loaded {len(df)} records from {data_file}")
            return df
            
        except Exception as e:
            self.validation_results['errors'].append(f"Failed to load data file: {e}")
            logger.error(f"Failed to load data file: {e}")
            return None
    
    def _validate_required_fields(self, df: pd.DataFrame):
        """
        Validate that required fields are present and not empty.
        
        Args:
            df: DataFrame to validate
        """
        required_fields = [
            'video_id', 'channel_id', 'title', 'published_at',
            'view_count', 'duration_seconds'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in df.columns:
                missing_fields.append(field)
            elif df[field].isnull().sum() > 0:
                null_count = df[field].isnull().sum()
                self.validation_results['warnings'].append(
                    f"Field '{field}' has {null_count} null values"
                )
        
        if missing_fields:
            self.validation_results['errors'].append(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
    
    def _validate_data_types(self, df: pd.DataFrame):
        """
        Validate data types of key fields.
        
        Args:
            df: DataFrame to validate
        """
        type_validations = {
            'view_count': 'numeric',
            'like_count': 'numeric',
            'comment_count': 'numeric',
            'duration_seconds': 'numeric',
            'title_length': 'numeric',
            'tag_count': 'numeric'
        }
        
        for field, expected_type in type_validations.items():
            if field not in df.columns:
                continue
            
            if expected_type == 'numeric':
                non_numeric = pd.to_numeric(df[field], errors='coerce').isnull().sum()
                if non_numeric > 0:
                    self.validation_results['warnings'].append(
                        f"Field '{field}' has {non_numeric} non-numeric values"
                    )
    
    def _validate_value_ranges(self, df: pd.DataFrame):
        """
        Validate that values are within expected ranges.
        
        Args:
            df: DataFrame to validate
        """
        range_validations = [
            ('view_count', 0, float('inf')),
            ('like_count', 0, float('inf')),
            ('comment_count', 0, float('inf')),
            ('duration_seconds', 0, 86400),  # Max 24 hours
            ('title_length', 0, 200),  # Reasonable title length
            ('tag_count', 0, 100),  # Reasonable tag count
            ('publish_hour', 0, 23),
            ('publish_day_of_week', 0, 6)
        ]
        
        for field, min_val, max_val in range_validations:
            if field not in df.columns:
                continue
            
            # Convert to numeric, handling errors
            numeric_series = pd.to_numeric(df[field], errors='coerce')
            
            # Check for values outside range
            out_of_range = ((numeric_series < min_val) | (numeric_series > max_val)).sum()
            if out_of_range > 0:
                self.validation_results['warnings'].append(
                    f"Field '{field}' has {out_of_range} values outside range [{min_val}, {max_val}]"
                )
    
    def _validate_consistency(self, df: pd.DataFrame):
        """
        Validate data consistency and logical relationships.
        
        Args:
            df: DataFrame to validate
        """
        # Check if Shorts classification is consistent with duration
        if 'is_short' in df.columns and 'duration_seconds' in df.columns:
            duration_numeric = pd.to_numeric(df['duration_seconds'], errors='coerce')
            
            # Shorts should be <= 60 seconds
            inconsistent_shorts = df[
                (df['is_short'] == True) & (duration_numeric > 60)
            ]
            
            if len(inconsistent_shorts) > 0:
                self.validation_results['warnings'].append(
                    f"{len(inconsistent_shorts)} videos marked as Shorts but duration > 60 seconds"
                )
            
            # Long-form videos should be > 60 seconds
            inconsistent_longform = df[
                (df['is_short'] == False) & (duration_numeric <= 60) & (duration_numeric > 0)
            ]
            
            if len(inconsistent_longform) > 0:
                self.validation_results['warnings'].append(
                    f"{len(inconsistent_longform)} videos marked as long-form but duration <= 60 seconds"
                )
        
        # Check engagement rate consistency
        if all(col in df.columns for col in ['view_count', 'like_count', 'comment_count']):
            view_numeric = pd.to_numeric(df['view_count'], errors='coerce')
            like_numeric = pd.to_numeric(df['like_count'], errors='coerce')
            comment_numeric = pd.to_numeric(df['comment_count'], errors='coerce')
            
            # Likes/comments should not exceed views
            invalid_likes = (like_numeric > view_numeric).sum()
            invalid_comments = (comment_numeric > view_numeric).sum()
            
            if invalid_likes > 0:
                self.validation_results['warnings'].append(
                    f"{invalid_likes} videos have more likes than views"
                )
            
            if invalid_comments > 0:
                self.validation_results['warnings'].append(
                    f"{invalid_comments} videos have more comments than views"
                )
    
    def _validate_sri_lankan_content(self, df: pd.DataFrame):
        """
        Validate Sri Lankan content identification.
        
        Args:
            df: DataFrame to validate
        """
        sri_lankan_indicators = [
            'sri lanka', 'sinhala', 'tamil', 'colombo', 'kandy', 'galle',
            'sri lankan', 'lanka', 'ceylon', 'lk'
        ]
        
        sinhala_pattern = r'[\u0D80-\u0DFF]'
        tamil_pattern = r'[\u0B80-\u0BFF]'
        
        if 'title' in df.columns and 'description' in df.columns:
            sri_lankan_count = 0
            
            for _, row in df.iterrows():
                title = str(row.get('title', '')).lower()
                description = str(row.get('description', '')).lower()
                text = f"{title} {description}"
                
                # Check for keywords
                has_keywords = any(keyword in text for keyword in sri_lankan_indicators)
                
                # Check for Sinhala/Tamil characters
                has_sinhala = bool(re.search(sinhala_pattern, text))
                has_tamil = bool(re.search(tamil_pattern, text))
                
                if has_keywords or has_sinhala or has_tamil:
                    sri_lankan_count += 1
            
            sri_lankan_percentage = (sri_lankan_count / len(df)) * 100
            
            if sri_lankan_percentage < 50:
                self.validation_results['warnings'].append(
                    f"Only {sri_lankan_percentage:.1f}% of videos appear to be Sri Lankan content"
                )
            
            logger.info(f"Sri Lankan content: {sri_lankan_percentage:.1f}% ({sri_lankan_count}/{len(df)})")
    
    def _check_duplicates(self, df: pd.DataFrame):
        """
        Check for duplicate records.
        
        Args:
            df: DataFrame to validate
        """
        if 'video_id' in df.columns:
            duplicate_count = df['video_id'].duplicated().sum()
            if duplicate_count > 0:
                self.validation_results['warnings'].append(
                    f"Found {duplicate_count} duplicate video IDs"
                )
        
        # Check for near-duplicate titles
        if 'title' in df.columns:
            # Simple check for exact title matches
            title_duplicates = df['title'].duplicated().sum()
            if title_duplicates > 0:
                self.validation_results['warnings'].append(
                    f"Found {title_duplicates} videos with duplicate titles"
                )
    
    def _validate_temporal_data(self, df: pd.DataFrame):
        """
        Validate temporal data consistency.
        
        Args:
            df: DataFrame to validate
        """
        if 'published_at' in df.columns:
            try:
                # Convert to datetime
                df['published_at_dt'] = pd.to_datetime(df['published_at'], errors='coerce')
                
                # Check for invalid dates
                invalid_dates = df['published_at_dt'].isnull().sum()
                if invalid_dates > 0:
                    self.validation_results['warnings'].append(
                        f"{invalid_dates} videos have invalid published_at dates"
                    )
                
                # Check for future dates
                future_dates = (df['published_at_dt'] > datetime.now()).sum()
                if future_dates > 0:
                    self.validation_results['warnings'].append(
                        f"{future_dates} videos have future publication dates"
                    )
                
                # Check date range
                if not df['published_at_dt'].isnull().all():
                    min_date = df['published_at_dt'].min()
                    max_date = df['published_at_dt'].max()
                    date_range = (max_date - min_date).days
                    
                    logger.info(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')} ({date_range} days)")
                
            except Exception as e:
                self.validation_results['errors'].append(f"Error validating temporal data: {e}")
    
    def _calculate_quality_score(self):
        """Calculate overall data quality score (0-100)."""
        total_issues = len(self.validation_results['errors']) + len(self.validation_results['warnings'])
        
        if self.validation_results['total_records'] == 0:
            self.validation_results['quality_score'] = 0.0
            return
        
        # Base score
        base_score = 100.0
        
        # Deduct points for errors (more severe)
        error_penalty = len(self.validation_results['errors']) * 10
        
        # Deduct points for warnings (less severe)
        warning_penalty = len(self.validation_results['warnings']) * 2
        
        # Calculate final score
        final_score = max(0.0, base_score - error_penalty - warning_penalty)
        
        self.validation_results['quality_score'] = final_score
        self.validation_results['valid_records'] = self.validation_results['total_records']
        self.validation_results['invalid_records'] = 0  # We don't remove records, just flag issues
    
    def validate_channel_data(self, data_file: str) -> Dict[str, Any]:
        """
        Validate channel data from a CSV or JSON file.
        
        Args:
            data_file: Path to the channel data file
            
        Returns:
            Dictionary containing validation results
        """
        logger.info(f"Starting channel data validation of {data_file}")
        
        # Reset results
        self.validation_results = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'warnings': [],
            'errors': [],
            'quality_score': 0.0,
            'validation_timestamp': datetime.now().isoformat()
        }
        
        # Load data
        df = self._load_data(data_file)
        if df is None:
            return self.validation_results
        
        self.validation_results['total_records'] = len(df)
        
        # Validate channel-specific fields
        self._validate_channel_fields(df)
        self._validate_channel_consistency(df)
        
        # Calculate quality score
        self._calculate_quality_score()
        
        logger.info(f"Channel validation completed. Quality score: {self.validation_results['quality_score']:.2f}")
        
        return self.validation_results
    
    def _validate_channel_fields(self, df: pd.DataFrame):
        """
        Validate channel-specific required fields.
        
        Args:
            df: DataFrame to validate
        """
        required_fields = ['channel_id', 'title', 'subscriber_count', 'video_count']
        
        for field in required_fields:
            if field not in df.columns:
                self.validation_results['errors'].append(f"Missing required field: {field}")
            elif df[field].isnull().sum() > 0:
                null_count = df[field].isnull().sum()
                self.validation_results['warnings'].append(
                    f"Field '{field}' has {null_count} null values"
                )
    
    def _validate_channel_consistency(self, df: pd.DataFrame):
        """
        Validate channel data consistency.
        
        Args:
            df: DataFrame to validate
        """
        # Check subscriber and video counts
        if 'subscriber_count' in df.columns:
            sub_numeric = pd.to_numeric(df['subscriber_count'], errors='coerce')
            negative_subs = (sub_numeric < 0).sum()
            if negative_subs > 0:
                self.validation_results['warnings'].append(
                    f"{negative_subs} channels have negative subscriber counts"
                )
        
        if 'video_count' in df.columns:
            vid_numeric = pd.to_numeric(df['video_count'], errors='coerce')
            negative_vids = (vid_numeric < 0).sum()
            if negative_vids > 0:
                self.validation_results['warnings'].append(
                    f"{negative_vids} channels have negative video counts"
                )
    
    def generate_validation_report(self, output_file: str):
        """
        Generate a detailed validation report.
        
        Args:
            output_file: Path to save the report
        """
        report = {
            'validation_summary': self.validation_results,
            'recommendations': self._generate_recommendations()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation report saved to {output_file}")
    
    def _generate_recommendations(self) -> List[str]:
        """
        Generate recommendations based on validation results.
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if self.validation_results['quality_score'] < 70:
            recommendations.append("Data quality is below acceptable threshold. Consider data cleaning.")
        
        if len(self.validation_results['errors']) > 0:
            recommendations.append("Critical errors found. Data cannot be used for training without fixes.")
        
        if len(self.validation_results['warnings']) > 10:
            recommendations.append("Many warnings detected. Review data collection process.")
        
        # Check for specific issues
        warning_text = ' '.join(self.validation_results['warnings'])
        
        if 'duplicate' in warning_text.lower():
            recommendations.append("Remove duplicate records before model training.")
        
        if 'sri lankan' in warning_text.lower():
            recommendations.append("Improve Sri Lankan content identification in data collection.")
        
        if 'null values' in warning_text.lower():
            recommendations.append("Handle missing values through imputation or removal.")
        
        if not recommendations:
            recommendations.append("Data quality is good. Proceed with preprocessing and training.")
        
        return recommendations


def main():
    """Main function for data validation."""
    parser = argparse.ArgumentParser(description='Validate YouTube data quality')
    parser.add_argument('--data-file', required=True, help='Path to data file to validate')
    parser.add_argument('--data-type', choices=['videos', 'channels'], default='videos',
                       help='Type of data to validate')
    parser.add_argument('--output-report', help='Path to save validation report')
    
    args = parser.parse_args()
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Initialize validator
    validator = DataValidator()
    
    try:
        # Run validation
        if args.data_type == 'videos':
            results = validator.validate_video_data(args.data_file)
        else:
            results = validator.validate_channel_data(args.data_file)
        
        # Print summary
        print(f"\nValidation Results:")
        print(f"Total records: {results['total_records']}")
        print(f"Quality score: {results['quality_score']:.2f}/100")
        print(f"Errors: {len(results['errors'])}")
        print(f"Warnings: {len(results['warnings'])}")
        
        if results['errors']:
            print(f"\nErrors:")
            for error in results['errors']:
                print(f"  - {error}")
        
        if results['warnings']:
            print(f"\nWarnings:")
            for warning in results['warnings'][:10]:  # Show first 10
                print(f"  - {warning}")
            if len(results['warnings']) > 10:
                print(f"  ... and {len(results['warnings']) - 10} more warnings")
        
        # Save report if requested
        if args.output_report:
            validator.generate_validation_report(args.output_report)
        
        # Exit with appropriate code
        if results['errors']:
            sys.exit(1)
        elif results['quality_score'] < 70:
            sys.exit(2)
        else:
            sys.exit(0)
    
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
