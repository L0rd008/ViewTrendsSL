
import sys
import os
import argparse
import pandas as pd
import numpy as np
import re
from pathlib import Path
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, Any, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Perform EDA and DA on raw YouTube data.'
    )
    parser.add_argument(
        '--input-file',
        type=str,
        required=True,
        help='Path to the raw input CSV file.'
    )
    return parser.parse_args()

def _parse_iso8601_duration(duration_str: str) -> int:
    """Parses an ISO 8601 duration string into total seconds."""
    if not isinstance(duration_str, str):
        return 0
    
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0

    hours, minutes, seconds = match.groups()
    total_seconds = 0
    if hours:
        total_seconds += int(hours) * 3600
    if minutes:
        total_seconds += int(minutes) * 60
    if seconds:
        total_seconds += int(seconds)
    
    return total_seconds

def _load_and_clean_data(input_path: str) -> pd.DataFrame:
    """Loads and performs initial cleaning on the raw CSV data."""
    if not Path(input_path).exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
        
    logger.info(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    logger.info(f"Successfully loaded {len(df)} rows.")

    # 1. Rename columns to a consistent schema
    df = df.rename(columns={
        'id': 'video_id',
        'likes_count': 'like_count',
        'video_duration': 'duration_iso8601'
    })
    
    # 2. Convert video_duration from ISO 8601 format to seconds
    if 'duration_iso8601' in df.columns:
        df['duration_seconds'] = df['duration_iso8601'].apply(_parse_iso8601_duration)
    else:
        df['duration_seconds'] = 0
        logger.warning("The 'video_duration' column was not found.")
        
    # 3. Convert relevant columns to appropriate data types
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce')
    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce')
    df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce')
    
    # Add a flag for video type
    df['is_short'] = df['duration_seconds'] <= 60
    
    logger.info("Initial data cleaning and type conversions completed.")
    return df

def _analyze_data_quality(df: pd.DataFrame):
    """Identifies and reports on data quality issues."""
    logger.info("-" * 50)
    logger.info("Data Quality Assessment")
    logger.info("-" * 50)
    
    # Missing values
    missing_data = df.isnull().sum()
    logger.info("Missing values per column:\n" + str(missing_data[missing_data > 0]))
    
    # Duplicates
    if 'video_id' in df.columns:
        duplicates = df.duplicated(subset=['video_id']).sum()
        logger.info(f"\nDuplicate videos found: {duplicates}")
    else:
        logger.warning("No 'video_id' column to check for duplicates.")
        
    # Data types
    logger.info("\nData types:\n" + str(df.dtypes))

def _perform_descriptive_stats(df: pd.DataFrame):
    """Generates and prints descriptive statistics for key numerical features."""
    logger.info("-" * 50)
    logger.info("Descriptive Statistics")
    logger.info("-" * 50)
    
    numerical_features = [
        'view_count', 'like_count', 'comment_count', 'duration_seconds'
    ]
    
    stats = df[numerical_features].describe().T
    logger.info("Summary Statistics:\n" + str(stats))
    
    # Engagement ratios
    df['engagement_rate'] = (df['like_count'] + df['comment_count']) / df['view_count']
    logger.info(f"Mean engagement rate: {df['engagement_rate'].mean():.4f}")
    
    # Video type distribution
    shorts_count = df['is_short'].sum()
    total_count = len(df)
    logger.info(f"Shorts videos: {shorts_count} ({shorts_count/total_count:.2%})")
    logger.info(f"Long-form videos: {total_count - shorts_count} ({(total_count - shorts_count)/total_count:.2%})")

def _visualize_univariate(df: pd.DataFrame):
    """Generates univariate plots."""
    logger.info("-" * 50)
    logger.info("Generating Univariate Plots...")
    
    # Histograms for key numerical features (log scale for better visibility)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    df['view_count'].replace(0, np.nan).dropna().hist(ax=axes[0], bins=50, log=True)
    axes[0].set_title('View Count Distribution (Log Scale)')
    axes[0].set_xlabel('View Count')
    axes[0].set_ylabel('Frequency')
    
    df['like_count'].replace(0, np.nan).dropna().hist(ax=axes[1], bins=50, log=True)
    axes[1].set_title('Like Count Distribution (Log Scale)')
    axes[1].set_xlabel('Like Count')
    axes[1].set_ylabel('Frequency')
    
    df['comment_count'].replace(0, np.nan).dropna().hist(ax=axes[2], bins=50, log=True)
    axes[2].set_title('Comment Count Distribution (Log Scale)')
    axes[2].set_xlabel('Comment Count')
    axes[2].set_ylabel('Frequency')
    
    plt.suptitle("Univariate Analysis of Key Metrics")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('univariate_metrics_plots.png')
    plt.close()
    
    logger.info("Saved 'univariate_metrics_plots.png'")

def _visualize_bivariate(df: pd.DataFrame):
    """Generates bivariate plots and correlation matrix."""
    logger.info("-" * 50)
    logger.info("Generating Bivariate Plots...")
    
    # Scatter plots with log scales
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    sns.scatterplot(x='like_count', y='view_count', data=df, ax=axes[0])
    axes[0].set_title('View Count vs. Like Count')
    axes[0].set_xlabel('Likes')
    axes[0].set_ylabel('Views')
    axes[0].set_xscale('log')
    axes[0].set_yscale('log')
    
    sns.scatterplot(x='comment_count', y='view_count', data=df, ax=axes[1])
    axes[1].set_title('View Count vs. Comment Count')
    axes[1].set_xlabel('Comments')
    axes[1].set_ylabel('Views')
    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    
    plt.suptitle("Bivariate Analysis of Engagement Metrics")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('bivariate_plots.png')
    plt.close()
    logger.info("Saved 'bivariate_plots.png'")
    
    # Correlation matrix
    numerical_cols = ['view_count', 'like_count', 'comment_count', 'duration_seconds']
    corr_matrix = df[numerical_cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Key Numerical Features')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()
    logger.info("Saved 'correlation_matrix.png'")
    
def _analyze_time_series(df: pd.DataFrame):
    """Analyzes and visualizes time-series growth patterns."""
    logger.info("-" * 50)
    logger.info("Analyzing Time-Series Growth Patterns...")
    
    # Select view columns for analysis
    view_columns = [col for col in df.columns if col.startswith('day_') and col.endswith('_views')]
    if not view_columns:
        logger.warning("No time-series view data columns found (e.g., 'day_1_views'). Skipping this analysis.")
        return
        
    df_ts = df[view_columns].copy()
    
    # Average growth curve
    avg_growth = df_ts.mean()
    plt.figure(figsize=(10, 6))
    avg_growth.plot(title='Average Viewership Growth Over 30 Days')
    plt.xlabel('Day')
    plt.ylabel('Average Views')
    plt.grid(True)
    plt.xticks(np.arange(0, len(view_columns), 5), labels=np.arange(1, len(view_columns)+1, 5))
    plt.tight_layout()
    plt.savefig('average_growth_curve.png')
    plt.close()
    logger.info("Saved 'average_growth_curve.png'")
    
    # Plotting growth curves of sample videos
    plt.figure(figsize=(12, 8))
    sample_videos = df_ts.sample(n=5, random_state=42)
    for index, row in sample_videos.iterrows():
        plt.plot(row.values, label=f"Video {index}", alpha=0.7)
    
    plt.title('Sample Viewership Growth Curves')
    plt.xlabel('Day')
    plt.ylabel('Views')
    plt.legend()
    plt.grid(True)
    plt.xticks(np.arange(0, len(view_columns), 5), labels=np.arange(1, len(view_columns)+1, 5))
    plt.tight_layout()
    plt.savefig('sample_growth_curves.png')
    plt.close()
    logger.info("Saved 'sample_growth_curves.png'")

def run_eda_pipeline(input_file: str):
    """Main function to run the complete EDA pipeline."""
    df = _load_and_clean_data(input_file)
    
    _analyze_data_quality(df)
    
    _perform_descriptive_stats(df)
    
    _visualize_univariate(df)
    
    _visualize_bivariate(df)
    
    _analyze_time_series(df)
    
    logger.info("-" * 50)
    logger.info("EDA and DA pipeline completed successfully.")
    logger.info("Please check the generated plots and console output for insights.")

def main():
    """Entry point of the script."""
    args = parse_arguments()
    run_eda_pipeline(args.input_file)

if __name__ == '__main__':
    main()
