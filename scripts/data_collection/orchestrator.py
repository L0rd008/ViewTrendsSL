#!/usr/bin/env python3
"""
Data Collection Orchestrator

This script orchestrates the entire data collection process for ViewTrendsSL,
coordinating channel discovery, video collection, performance tracking, and validation.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import json
import logging
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import subprocess

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config.api.api_config import get_youtube_api_key
from scripts.data_collection.youtube.collect_channels import ChannelCollector
from scripts.data_collection.youtube.collect_videos import VideoCollector
from scripts.data_collection.youtube.track_performance import PerformanceTracker
from scripts.data_collection.youtube.api_quota_manager import QuotaManager
from scripts.data_collection.validation.data_validator import DataValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_collection_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataCollectionOrchestrator:
    """Orchestrates the complete data collection pipeline."""
    
    def __init__(self, api_key: str):
        """
        Initialize the orchestrator.
        
        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.quota_manager = QuotaManager()
        
        # Initialize collectors
        self.channel_collector = ChannelCollector(api_key)
        self.video_collector = VideoCollector(api_key)
        self.performance_tracker = PerformanceTracker(api_key)
        self.data_validator = DataValidator()
        
        # Configuration
        self.config = {
            'max_channels': 200,
            'max_videos_per_channel': 50,
            'days_back': 365,
            'min_quality_score': 70,
            'output_base_dir': 'data/raw',
            'validation_reports_dir': 'data/validation_reports'
        }
    
    def run_full_collection_pipeline(self, seed_channels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run the complete data collection pipeline.
        
        Args:
            seed_channels: Optional list of seed channel IDs
            
        Returns:
            Dictionary with pipeline results
        """
        pipeline_start = datetime.now()
        results = {
            'pipeline_start': pipeline_start.isoformat(),
            'stages': {},
            'total_channels': 0,
            'total_videos': 0,
            'quality_scores': {},
            'errors': [],
            'warnings': []
        }
        
        logger.info("Starting full data collection pipeline")
        
        try:
            # Stage 1: Channel Discovery and Collection
            logger.info("Stage 1: Channel Discovery and Collection")
            channel_results = self._run_channel_collection(seed_channels)
            results['stages']['channel_collection'] = channel_results
            results['total_channels'] = channel_results.get('channels_collected', 0)
            
            if channel_results.get('channels_collected', 0) == 0:
                results['errors'].append("No channels collected, cannot proceed")
                return results
            
            # Stage 2: Video Collection
            logger.info("Stage 2: Video Collection")
            video_results = self._run_video_collection(channel_results['output_file'])
            results['stages']['video_collection'] = video_results
            results['total_videos'] = video_results.get('videos_collected', 0)
            
            if video_results.get('videos_collected', 0) == 0:
                results['errors'].append("No videos collected")
                return results
            
            # Stage 3: Data Validation
            logger.info("Stage 3: Data Validation")
            validation_results = self._run_data_validation(video_results['output_files'])
            results['stages']['validation'] = validation_results
            results['quality_scores'] = validation_results.get('quality_scores', {})
            
            # Stage 4: Performance Tracking Setup
            logger.info("Stage 4: Performance Tracking Setup")
            tracking_results = self._setup_performance_tracking(video_results['output_files'])
            results['stages']['performance_tracking'] = tracking_results
            
            # Stage 5: Generate Summary Report
            logger.info("Stage 5: Generating Summary Report")
            self._generate_pipeline_report(results)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            results['errors'].append(f"Pipeline failure: {str(e)}")
        
        pipeline_end = datetime.now()
        results['pipeline_end'] = pipeline_end.isoformat()
        results['duration_minutes'] = (pipeline_end - pipeline_start).total_seconds() / 60
        
        logger.info(f"Pipeline completed in {results['duration_minutes']:.2f} minutes")
        
        return results
    
    def _run_channel_collection(self, seed_channels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run channel collection stage.
        
        Args:
            seed_channels: Optional seed channels
            
        Returns:
            Channel collection results
        """
        stage_start = datetime.now()
        
        try:
            # Check quota availability
            if not self.quota_manager.can_make_request(100):  # Conservative estimate
                return {
                    'success': False,
                    'error': 'Insufficient API quota for channel collection',
                    'channels_collected': 0
                }
            
            # Use seed channels or discover new ones
            if seed_channels:
                logger.info(f"Using {len(seed_channels)} seed channels")
                channels = []
                for channel_id in seed_channels:
                    channel_data = self.channel_collector.get_channel_details([channel_id])
                    channels.extend(channel_data)
            else:
                logger.info("Discovering Sri Lankan channels")
                channels = self.channel_collector.discover_sri_lankan_channels(
                    max_channels=self.config['max_channels']
                )
            
            if not channels:
                return {
                    'success': False,
                    'error': 'No channels found',
                    'channels_collected': 0
                }
            
            # Save channels
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(self.config['output_base_dir'], 'channels', f'channels_{timestamp}.json')
            
            self.channel_collector.save_channels(channels, os.path.dirname(output_file))
            
            return {
                'success': True,
                'channels_collected': len(channels),
                'output_file': output_file,
                'duration_seconds': (datetime.now() - stage_start).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Channel collection failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'channels_collected': 0
            }
    
    def _run_video_collection(self, channels_file: str) -> Dict[str, Any]:
        """
        Run video collection stage.
        
        Args:
            channels_file: Path to channels file
            
        Returns:
            Video collection results
        """
        stage_start = datetime.now()
        
        try:
            # Load channel IDs
            channel_ids = self.video_collector.load_channels_from_file(channels_file)
            if not channel_ids:
                return {
                    'success': False,
                    'error': 'No channel IDs loaded from file',
                    'videos_collected': 0
                }
            
            # Check quota availability
            estimated_quota_needed = len(channel_ids) * 2  # Conservative estimate
            if not self.quota_manager.can_make_request(estimated_quota_needed):
                return {
                    'success': False,
                    'error': 'Insufficient API quota for video collection',
                    'videos_collected': 0
                }
            
            # Collect videos
            videos = self.video_collector.collect_videos_from_channels(
                channel_ids,
                self.config['max_videos_per_channel'],
                self.config['days_back']
            )
            
            if not videos:
                return {
                    'success': False,
                    'error': 'No videos collected',
                    'videos_collected': 0
                }
            
            # Save videos
            output_dir = os.path.join(self.config['output_base_dir'], 'videos')
            self.video_collector.save_videos(videos, output_dir)
            
            # Generate output file paths
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_files = {
                'all_videos': os.path.join(output_dir, f'videos_{timestamp}.csv'),
                'shorts': os.path.join(output_dir, f'shorts_{timestamp}.csv'),
                'longform': os.path.join(output_dir, f'longform_{timestamp}.csv')
            }
            
            return {
                'success': True,
                'videos_collected': len(videos),
                'output_files': output_files,
                'shorts_count': sum(1 for v in videos if v.get('is_short', False)),
                'longform_count': sum(1 for v in videos if not v.get('is_short', False)),
                'duration_seconds': (datetime.now() - stage_start).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Video collection failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'videos_collected': 0
            }
    
    def _run_data_validation(self, output_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Run data validation stage.
        
        Args:
            output_files: Dictionary of output file paths
            
        Returns:
            Validation results
        """
        validation_results = {
            'success': True,
            'quality_scores': {},
            'validation_reports': {},
            'errors': []
        }
        
        os.makedirs(self.config['validation_reports_dir'], exist_ok=True)
        
        for file_type, file_path in output_files.items():
            if not os.path.exists(file_path):
                validation_results['errors'].append(f"File not found: {file_path}")
                continue
            
            try:
                logger.info(f"Validating {file_type}: {file_path}")
                
                # Run validation
                results = self.data_validator.validate_video_data(file_path)
                
                quality_score = results.get('quality_score', 0)
                validation_results['quality_scores'][file_type] = quality_score
                
                # Generate validation report
                report_file = os.path.join(
                    self.config['validation_reports_dir'],
                    f'validation_{file_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                )
                
                self.data_validator.generate_validation_report(report_file)
                validation_results['validation_reports'][file_type] = report_file
                
                # Check quality threshold
                if quality_score < self.config['min_quality_score']:
                    validation_results['errors'].append(
                        f"{file_type} quality score ({quality_score:.2f}) below threshold ({self.config['min_quality_score']})"
                    )
                
            except Exception as e:
                logger.error(f"Validation failed for {file_type}: {e}")
                validation_results['errors'].append(f"Validation failed for {file_type}: {str(e)}")
                validation_results['success'] = False
        
        return validation_results
    
    def _setup_performance_tracking(self, output_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Setup performance tracking for collected videos.
        
        Args:
            output_files: Dictionary of output file paths
            
        Returns:
            Performance tracking setup results
        """
        try:
            # Load video IDs from the main videos file
            main_file = output_files.get('all_videos')
            if not main_file or not os.path.exists(main_file):
                return {
                    'success': False,
                    'error': 'Main videos file not found'
                }
            
            video_ids = self.performance_tracker.load_videos_from_file(main_file)
            if not video_ids:
                return {
                    'success': False,
                    'error': 'No video IDs loaded for tracking'
                }
            
            # Add videos to tracking database
            self.performance_tracker.add_videos_to_track(video_ids)
            
            # Get tracking summary
            summary = self.performance_tracker.get_tracking_summary()
            
            return {
                'success': True,
                'videos_added_to_tracking': len(video_ids),
                'tracking_summary': summary
            }
            
        except Exception as e:
            logger.error(f"Performance tracking setup failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_pipeline_report(self, results: Dict[str, Any]):
        """
        Generate a comprehensive pipeline report.
        
        Args:
            results: Pipeline results dictionary
        """
        report_file = os.path.join(
            self.config['validation_reports_dir'],
            f'pipeline_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        # Add quota usage information
        quota_usage = self.quota_manager.get_usage_report()
        results['quota_usage'] = quota_usage
        
        # Add recommendations
        recommendations = self._generate_recommendations(results)
        results['recommendations'] = recommendations
        
        # Save report
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Pipeline report saved to {report_file}")
        
        # Print summary
        self._print_pipeline_summary(results)
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on pipeline results.
        
        Args:
            results: Pipeline results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check overall success
        if results.get('errors'):
            recommendations.append("Pipeline completed with errors. Review error messages and retry failed stages.")
        
        # Check data quality
        quality_scores = results.get('quality_scores', {})
        low_quality_files = [k for k, v in quality_scores.items() if v < self.config['min_quality_score']]
        
        if low_quality_files:
            recommendations.append(f"Low quality data detected in: {', '.join(low_quality_files)}. Consider data cleaning.")
        
        # Check data volume
        if results.get('total_videos', 0) < 1000:
            recommendations.append("Low video count. Consider expanding channel list or increasing collection period.")
        
        if results.get('total_channels', 0) < 50:
            recommendations.append("Low channel count. Consider improving channel discovery methods.")
        
        # Check quota usage
        quota_usage = results.get('quota_usage', {})
        current_usage = quota_usage.get('current_usage', {})
        if current_usage.get('daily_remaining', 0) < 1000:
            recommendations.append("Low API quota remaining. Consider spreading collection across multiple days.")
        
        # Success recommendations
        if not recommendations:
            recommendations.append("Data collection pipeline completed successfully. Proceed with data preprocessing and model training.")
        
        return recommendations
    
    def _print_pipeline_summary(self, results: Dict[str, Any]):
        """
        Print a summary of pipeline results.
        
        Args:
            results: Pipeline results
        """
        print("\n" + "="*60)
        print("DATA COLLECTION PIPELINE SUMMARY")
        print("="*60)
        
        print(f"Duration: {results.get('duration_minutes', 0):.2f} minutes")
        print(f"Total Channels: {results.get('total_channels', 0)}")
        print(f"Total Videos: {results.get('total_videos', 0)}")
        
        # Quality scores
        quality_scores = results.get('quality_scores', {})
        if quality_scores:
            print(f"\nData Quality Scores:")
            for file_type, score in quality_scores.items():
                print(f"  {file_type}: {score:.2f}/100")
        
        # Errors and warnings
        errors = results.get('errors', [])
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for error in errors[:5]:  # Show first 5
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")
        
        # Recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"\nRecommendations:")
            for rec in recommendations:
                print(f"  - {rec}")
        
        print("="*60)
    
    def run_incremental_collection(self) -> Dict[str, Any]:
        """
        Run incremental data collection (for regular updates).
        
        Returns:
            Incremental collection results
        """
        logger.info("Starting incremental data collection")
        
        results = {
            'type': 'incremental',
            'start_time': datetime.now().isoformat(),
            'new_videos': 0,
            'updated_tracking': 0,
            'success': True,
            'errors': []
        }
        
        try:
            # Run performance tracking update
            self.performance_tracker.track_active_videos()
            
            # Get tracking summary
            summary = self.performance_tracker.get_tracking_summary()
            results['updated_tracking'] = summary.get('videos_tracked_24h', 0)
            
            # TODO: Add logic for discovering new videos from existing channels
            # This would involve checking for new uploads since last collection
            
        except Exception as e:
            logger.error(f"Incremental collection failed: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        results['end_time'] = datetime.now().isoformat()
        
        return results


def main():
    """Main function for data collection orchestrator."""
    parser = argparse.ArgumentParser(description='Orchestrate YouTube data collection')
    parser.add_argument('--mode', choices=['full', 'incremental'], default='full',
                       help='Collection mode')
    parser.add_argument('--seed-channels', help='File containing seed channel IDs')
    parser.add_argument('--max-channels', type=int, default=200,
                       help='Maximum channels to collect')
    parser.add_argument('--max-videos-per-channel', type=int, default=50,
                       help='Maximum videos per channel')
    parser.add_argument('--days-back', type=int, default=365,
                       help='Days back to collect videos')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = get_youtube_api_key()
    if not api_key:
        logger.error("YouTube API key not found. Please set YOUTUBE_API_KEY environment variable.")
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/raw/channels', exist_ok=True)
    os.makedirs('data/raw/videos', exist_ok=True)
    os.makedirs('data/validation_reports', exist_ok=True)
    
    # Initialize orchestrator
    orchestrator = DataCollectionOrchestrator(api_key)
    
    # Update configuration
    orchestrator.config.update({
        'max_channels': args.max_channels,
        'max_videos_per_channel': args.max_videos_per_channel,
        'days_back': args.days_back
    })
    
    try:
        if args.mode == 'full':
            # Load seed channels if provided
            seed_channels = None
            if args.seed_channels:
                with open(args.seed_channels, 'r') as f:
                    if args.seed_channels.endswith('.json'):
                        data = json.load(f)
                        seed_channels = [item.get('channel_id', '') for item in data if 'channel_id' in item]
                    else:
                        seed_channels = [line.strip() for line in f if line.strip()]
            
            # Run full pipeline
            results = orchestrator.run_full_collection_pipeline(seed_channels)
            
            # Exit with appropriate code
            if results.get('errors'):
                sys.exit(1)
            else:
                sys.exit(0)
        
        elif args.mode == 'incremental':
            # Run incremental collection
            results = orchestrator.run_incremental_collection()
            
            if not results.get('success'):
                sys.exit(1)
            else:
                sys.exit(0)
    
    except KeyboardInterrupt:
        logger.info("Data collection stopped by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Data collection orchestrator failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()