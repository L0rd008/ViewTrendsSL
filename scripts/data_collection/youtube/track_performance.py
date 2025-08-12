#!/usr/bin/env python3
"""
YouTube Performance Tracking Script

This script tracks the performance of YouTube videos over time by collecting
view counts, likes, comments, and other metrics at regular intervals.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import json
import csv
import logging
import time
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
import argparse
import schedule

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.api.api_config import get_youtube_api_key
from scripts.data_collection.youtube.api_quota_manager import QuotaManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/performance_tracking.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PerformanceTracker:
    """Tracks YouTube video performance over time."""
    
    def __init__(self, api_key: str, db_path: str = 'data/performance_tracking.db'):
        """
        Initialize the performance tracker.
        
        Args:
            api_key: YouTube Data API key
            db_path: Path to SQLite database for storing snapshots
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_manager = QuotaManager()
        self.db_path = db_path
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database for storing performance snapshots."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create videos table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    channel_id TEXT,
                    title TEXT,
                    published_at TEXT,
                    duration_seconds INTEGER,
                    is_short BOOLEAN,
                    category_id TEXT,
                    added_at TEXT,
                    last_tracked TEXT,
                    tracking_status TEXT DEFAULT 'active'
                )
            ''')
            
            # Create snapshots table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT,
                    timestamp TEXT,
                    view_count INTEGER,
                    like_count INTEGER,
                    comment_count INTEGER,
                    hours_since_publish REAL,
                    collected_at TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos (video_id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_video_id ON snapshots (video_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp ON snapshots (timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_tracking_status ON videos (tracking_status)')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def add_videos_to_track(self, video_ids: List[str]):
        """
        Add videos to the tracking database.
        
        Args:
            video_ids: List of video IDs to track
        """
        if not video_ids:
            return
        
        # Get video details from API
        video_details = self._get_video_details(video_ids)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for video in video_details:
                cursor.execute('''
                    INSERT OR REPLACE INTO videos 
                    (video_id, channel_id, title, published_at, duration_seconds, 
                     is_short, category_id, added_at, tracking_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')
                ''', (
                    video['video_id'],
                    video['channel_id'],
                    video['title'],
                    video['published_at'],
                    video['duration_seconds'],
                    video['is_short'],
                    video['category_id'],
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            logger.info(f"Added {len(video_details)} videos to tracking database")
    
    def _get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get video details from YouTube API.
        
        Args:
            video_ids: List of video IDs
            
        Returns:
            List of video details
        """
        videos = []
        
        # Process in batches of 50
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            try:
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping video details retrieval")
                    break
                
                response = self.youtube.videos().list(
                    part='snippet,contentDetails',
                    id=','.join(batch)
                ).execute()
                
                self.quota_manager.record_request(1, 'videos')
                
                for item in response.get('items', []):
                    snippet = item.get('snippet', {})
                    content_details = item.get('contentDetails', {})
                    
                    # Parse duration
                    duration_iso = content_details.get('duration', 'PT0S')
                    try:
                        import isodate
                        duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())
                    except:
                        duration_seconds = 0
                    
                    videos.append({
                        'video_id': item['id'],
                        'channel_id': snippet.get('channelId', ''),
                        'title': snippet.get('title', ''),
                        'published_at': snippet.get('publishedAt', ''),
                        'duration_seconds': duration_seconds,
                        'is_short': duration_seconds <= 60 and duration_seconds > 0,
                        'category_id': snippet.get('categoryId', '')
                    })
                
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting video details: {e}")
                continue
        
        return videos
    
    def track_active_videos(self, max_age_days: int = 30):
        """
        Track performance of active videos.
        
        Args:
            max_age_days: Maximum age of videos to track (in days)
        """
        # Get active videos from database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get videos that are still within tracking period
            cutoff_date = (datetime.now() - timedelta(days=max_age_days)).isoformat()
            
            cursor.execute('''
                SELECT video_id, published_at 
                FROM videos 
                WHERE tracking_status = 'active' 
                AND published_at > ?
                ORDER BY published_at DESC
            ''', (cutoff_date,))
            
            active_videos = cursor.fetchall()
        
        if not active_videos:
            logger.info("No active videos to track")
            return
        
        logger.info(f"Tracking {len(active_videos)} active videos")
        
        # Get current statistics for all active videos
        video_ids = [video[0] for video in active_videos]
        current_stats = self._get_current_statistics(video_ids)
        
        # Store snapshots
        self._store_snapshots(current_stats)
        
        # Update videos that are too old
        self._update_old_videos(max_age_days)
    
    def _get_current_statistics(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get current statistics for videos.
        
        Args:
            video_ids: List of video IDs
            
        Returns:
            List of video statistics
        """
        stats = []
        
        # Process in batches of 50
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            try:
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping statistics retrieval")
                    break
                
                response = self.youtube.videos().list(
                    part='statistics,snippet',
                    id=','.join(batch)
                ).execute()
                
                self.quota_manager.record_request(1, 'videos')
                
                for item in response.get('items', []):
                    snippet = item.get('snippet', {})
                    statistics = item.get('statistics', {})
                    
                    # Calculate hours since publish
                    published_at = snippet.get('publishedAt', '')
                    hours_since_publish = 0
                    if published_at:
                        try:
                            pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                            hours_since_publish = (datetime.now(pub_time.tzinfo) - pub_time).total_seconds() / 3600
                        except:
                            pass
                    
                    stats.append({
                        'video_id': item['id'],
                        'view_count': int(statistics.get('viewCount', 0)),
                        'like_count': int(statistics.get('likeCount', 0)),
                        'comment_count': int(statistics.get('commentCount', 0)),
                        'hours_since_publish': hours_since_publish
                    })
                
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting video statistics: {e}")
                continue
        
        return stats
    
    def _store_snapshots(self, stats: List[Dict[str, Any]]):
        """
        Store performance snapshots in database.
        
        Args:
            stats: List of video statistics
        """
        if not stats:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            for stat in stats:
                cursor.execute('''
                    INSERT INTO snapshots 
                    (video_id, timestamp, view_count, like_count, comment_count, 
                     hours_since_publish, collected_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    stat['video_id'],
                    timestamp,
                    stat['view_count'],
                    stat['like_count'],
                    stat['comment_count'],
                    stat['hours_since_publish'],
                    timestamp
                ))
            
            conn.commit()
            logger.info(f"Stored {len(stats)} performance snapshots")
    
    def _update_old_videos(self, max_age_days: int):
        """
        Update tracking status for videos that are too old.
        
        Args:
            max_age_days: Maximum age for active tracking
        """
        cutoff_date = (datetime.now() - timedelta(days=max_age_days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE videos 
                SET tracking_status = 'completed', last_tracked = ?
                WHERE tracking_status = 'active' 
                AND published_at <= ?
            ''', (datetime.now().isoformat(), cutoff_date))
            
            updated_count = cursor.rowcount
            conn.commit()
            
            if updated_count > 0:
                logger.info(f"Marked {updated_count} videos as completed tracking")
    
    def get_video_performance_history(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get performance history for a specific video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of performance snapshots
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, view_count, like_count, comment_count, hours_since_publish
                FROM snapshots 
                WHERE video_id = ?
                ORDER BY timestamp
            ''', (video_id,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    'timestamp': row[0],
                    'view_count': row[1],
                    'like_count': row[2],
                    'comment_count': row[3],
                    'hours_since_publish': row[4]
                }
                for row in rows
            ]
    
    def export_tracking_data(self, output_dir: str = 'data/raw/snapshots'):
        """
        Export tracking data to CSV files.
        
        Args:
            output_dir: Output directory for exported data
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with sqlite3.connect(self.db_path) as conn:
            # Export videos
            videos_df = conn.execute('SELECT * FROM videos').fetchall()
            videos_columns = [desc[0] for desc in conn.execute('SELECT * FROM videos LIMIT 1').description]
            
            videos_file = os.path.join(output_dir, f'tracked_videos_{timestamp}.csv')
            with open(videos_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(videos_columns)
                writer.writerows(videos_df)
            
            # Export snapshots
            snapshots_df = conn.execute('SELECT * FROM snapshots').fetchall()
            snapshots_columns = [desc[0] for desc in conn.execute('SELECT * FROM snapshots LIMIT 1').description]
            
            snapshots_file = os.path.join(output_dir, f'performance_snapshots_{timestamp}.csv')
            with open(snapshots_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(snapshots_columns)
                writer.writerows(snapshots_df)
            
            logger.info(f"Exported tracking data to {videos_file} and {snapshots_file}")
    
    def get_tracking_summary(self) -> Dict[str, Any]:
        """
        Get a summary of tracking status.
        
        Returns:
            Dictionary with tracking statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count videos by status
            cursor.execute('SELECT tracking_status, COUNT(*) FROM videos GROUP BY tracking_status')
            status_counts = dict(cursor.fetchall())
            
            # Count total snapshots
            cursor.execute('SELECT COUNT(*) FROM snapshots')
            total_snapshots = cursor.fetchone()[0]
            
            # Get latest snapshot time
            cursor.execute('SELECT MAX(timestamp) FROM snapshots')
            latest_snapshot = cursor.fetchone()[0]
            
            # Get videos tracked in last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            cursor.execute('SELECT COUNT(DISTINCT video_id) FROM snapshots WHERE timestamp > ?', (yesterday,))
            recent_videos = cursor.fetchone()[0]
            
            return {
                'video_counts': status_counts,
                'total_snapshots': total_snapshots,
                'latest_snapshot': latest_snapshot,
                'videos_tracked_24h': recent_videos,
                'database_path': self.db_path
            }
    
    def load_videos_from_file(self, file_path: str) -> List[str]:
        """
        Load video IDs from a file.
        
        Args:
            file_path: Path to file containing video data
            
        Returns:
            List of video IDs
        """
        video_ids = []
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        video_ids = [item.get('video_id', '') for item in data if 'video_id' in item]
            
            elif file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    video_ids = [row.get('video_id', '') for row in reader if 'video_id' in row]
            
            else:
                # Plain text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    video_ids = [line.strip() for line in f if line.strip()]
            
            # Filter out empty IDs
            video_ids = [vid for vid in video_ids if vid]
            
            logger.info(f"Loaded {len(video_ids)} video IDs from {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading videos from {file_path}: {e}")
        
        return video_ids


def run_scheduled_tracking():
    """Run scheduled performance tracking."""
    api_key = get_youtube_api_key()
    if not api_key:
        logger.error("YouTube API key not found")
        return
    
    tracker = PerformanceTracker(api_key)
    tracker.track_active_videos()


def main():
    """Main function for performance tracking."""
    parser = argparse.ArgumentParser(description='Track YouTube video performance')
    parser.add_argument('--add-videos', help='File containing video IDs to add to tracking')
    parser.add_argument('--track-once', action='store_true', help='Run tracking once')
    parser.add_argument('--schedule', action='store_true', help='Run scheduled tracking')
    parser.add_argument('--export', action='store_true', help='Export tracking data')
    parser.add_argument('--summary', action='store_true', help='Show tracking summary')
    parser.add_argument('--max-age-days', type=int, default=30, help='Maximum age of videos to track')
    parser.add_argument('--db-path', default='data/performance_tracking.db', help='Database path')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = get_youtube_api_key()
    if not api_key:
        logger.error("YouTube API key not found. Please set YOUTUBE_API_KEY environment variable.")
        sys.exit(1)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Initialize tracker
    tracker = PerformanceTracker(api_key, args.db_path)
    
    try:
        if args.add_videos:
            # Add videos to tracking
            video_ids = tracker.load_videos_from_file(args.add_videos)
            if video_ids:
                tracker.add_videos_to_track(video_ids)
            else:
                logger.error("No video IDs found in the specified file")
        
        elif args.track_once:
            # Run tracking once
            tracker.track_active_videos(args.max_age_days)
        
        elif args.schedule:
            # Run scheduled tracking
            logger.info("Starting scheduled performance tracking...")
            logger.info("Tracking will run every 6 hours")
            
            # Schedule tracking every 6 hours
            schedule.every(6).hours.do(run_scheduled_tracking)
            
            # Run once immediately
            run_scheduled_tracking()
            
            # Keep running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        elif args.export:
            # Export tracking data
            tracker.export_tracking_data()
        
        elif args.summary:
            # Show tracking summary
            summary = tracker.get_tracking_summary()
            print(json.dumps(summary, indent=2))
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        logger.info("Performance tracking stopped by user")
    except Exception as e:
        logger.error(f"Performance tracking failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
