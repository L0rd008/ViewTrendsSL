#!/usr/bin/env python3
"""
YouTube Video Collection Script

This script collects video metadata from Sri Lankan YouTube channels.
It fetches video details, statistics, and content information.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import json
import csv
import logging
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import argparse
import isodate

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
        logging.FileHandler('logs/video_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VideoCollector:
    """Collects video metadata from YouTube channels."""
    
    def __init__(self, api_key: str):
        """
        Initialize the video collector.
        
        Args:
            api_key: YouTube Data API key
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_manager = QuotaManager()
        self.collected_videos = set()
        
    def get_channel_uploads_playlist(self, channel_id: str) -> Optional[str]:
        """
        Get the uploads playlist ID for a channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Uploads playlist ID or None if not found
        """
        try:
            if not self.quota_manager.can_make_request(1):
                logger.warning("API quota exhausted, cannot get uploads playlist")
                return None
            
            response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            self.quota_manager.record_request(1, 'channels')
            
            if response.get('items'):
                uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                return uploads_playlist_id
            
        except HttpError as e:
            logger.error(f"API error getting uploads playlist for {channel_id}: {e}")
        
        return None
    
    def get_videos_from_playlist(self, playlist_id: str, max_results: int = 50, 
                                published_after: Optional[datetime] = None) -> List[str]:
        """
        Get video IDs from a playlist.
        
        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to retrieve
            published_after: Only get videos published after this date
            
        Returns:
            List of video IDs
        """
        video_ids = []
        next_page_token = None
        
        while len(video_ids) < max_results:
            try:
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping playlist retrieval")
                    break
                
                request_params = {
                    'part': 'snippet',
                    'playlistId': playlist_id,
                    'maxResults': min(50, max_results - len(video_ids))
                }
                
                if next_page_token:
                    request_params['pageToken'] = next_page_token
                
                response = self.youtube.playlistItems().list(**request_params).execute()
                
                self.quota_manager.record_request(1, 'playlistItems')
                
                for item in response.get('items', []):
                    video_id = item['snippet']['resourceId']['videoId']
                    published_at = datetime.fromisoformat(
                        item['snippet']['publishedAt'].replace('Z', '+00:00')
                    )
                    
                    # Filter by publish date if specified
                    if published_after and published_at < published_after:
                        continue
                    
                    if video_id not in self.collected_videos:
                        video_ids.append(video_id)
                        self.collected_videos.add(video_id)
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Rate limiting
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting videos from playlist {playlist_id}: {e}")
                break
        
        return video_ids
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information for a list of video IDs.
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of video data dictionaries
        """
        videos = []
        
        # Process videos in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            try:
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping video details retrieval")
                    break
                
                response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails,status',
                    id=','.join(batch)
                ).execute()
                
                self.quota_manager.record_request(1, 'videos')
                
                for item in response.get('items', []):
                    video_data = self._extract_video_data(item)
                    videos.append(video_data)
                
                # Rate limiting
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting video details: {e}")
                continue
        
        return videos
    
    def _extract_video_data(self, video_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from YouTube API video response.
        
        Args:
            video_item: Video item from YouTube API
            
        Returns:
            Extracted video data dictionary
        """
        snippet = video_item.get('snippet', {})
        statistics = video_item.get('statistics', {})
        content_details = video_item.get('contentDetails', {})
        status = video_item.get('status', {})
        
        # Parse duration
        duration_iso = content_details.get('duration', 'PT0S')
        try:
            duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())
        except:
            duration_seconds = 0
        
        # Determine if it's a Short
        is_short = duration_seconds <= 60 and duration_seconds > 0
        
        # Extract tags
        tags = snippet.get('tags', [])
        tags_str = '|'.join(tags) if tags else ''
        
        # Extract thumbnail URLs
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = ''
        for quality in ['maxres', 'high', 'medium', 'default']:
            if quality in thumbnails:
                thumbnail_url = thumbnails[quality]['url']
                break
        
        return {
            'video_id': video_item['id'],
            'channel_id': snippet.get('channelId', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
            'duration_seconds': duration_seconds,
            'is_short': is_short,
            'category_id': snippet.get('categoryId', ''),
            'default_language': snippet.get('defaultLanguage', ''),
            'default_audio_language': snippet.get('defaultAudioLanguage', ''),
            'tags': tags_str,
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'thumbnail_url': thumbnail_url,
            'privacy_status': status.get('privacyStatus', ''),
            'upload_status': status.get('uploadStatus', ''),
            'license': status.get('license', ''),
            'embeddable': status.get('embeddable', True),
            'public_stats_viewable': status.get('publicStatsViewable', True),
            'made_for_kids': status.get('madeForKids', False),
            'collected_at': datetime.now().isoformat(),
            
            # Derived features
            'title_length': len(snippet.get('title', '')),
            'description_length': len(snippet.get('description', '')),
            'tag_count': len(tags),
            'publish_hour': self._extract_publish_hour(snippet.get('publishedAt', '')),
            'publish_day_of_week': self._extract_day_of_week(snippet.get('publishedAt', '')),
            'publish_is_weekend': self._is_weekend(snippet.get('publishedAt', '')),
            'has_custom_thumbnail': thumbnail_url != '',
            'title_has_caps': self._has_caps(snippet.get('title', '')),
            'title_has_numbers': self._has_numbers(snippet.get('title', '')),
            'title_has_question': '?' in snippet.get('title', ''),
            'title_has_exclamation': '!' in snippet.get('title', ''),
            'engagement_rate': self._calculate_engagement_rate(statistics),
            'like_to_view_ratio': self._calculate_like_to_view_ratio(statistics),
            'comment_to_view_ratio': self._calculate_comment_to_view_ratio(statistics)
        }
    
    def _extract_publish_hour(self, published_at: str) -> int:
        """Extract hour from published_at timestamp."""
        try:
            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            # Convert to Sri Lanka time (UTC+5:30)
            sri_lanka_time = dt + timedelta(hours=5, minutes=30)
            return sri_lanka_time.hour
        except:
            return 0
    
    def _extract_day_of_week(self, published_at: str) -> int:
        """Extract day of week from published_at timestamp (0=Monday, 6=Sunday)."""
        try:
            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            sri_lanka_time = dt + timedelta(hours=5, minutes=30)
            return sri_lanka_time.weekday()
        except:
            return 0
    
    def _is_weekend(self, published_at: str) -> bool:
        """Check if published on weekend."""
        day_of_week = self._extract_day_of_week(published_at)
        return day_of_week >= 5  # Saturday (5) or Sunday (6)
    
    def _has_caps(self, text: str) -> bool:
        """Check if text has capital letters."""
        return any(c.isupper() for c in text)
    
    def _has_numbers(self, text: str) -> bool:
        """Check if text has numbers."""
        return any(c.isdigit() for c in text)
    
    def _calculate_engagement_rate(self, statistics: Dict[str, Any]) -> float:
        """Calculate engagement rate (likes + comments) / views."""
        try:
            views = int(statistics.get('viewCount', 0))
            likes = int(statistics.get('likeCount', 0))
            comments = int(statistics.get('commentCount', 0))
            
            if views == 0:
                return 0.0
            
            return (likes + comments) / views
        except:
            return 0.0
    
    def _calculate_like_to_view_ratio(self, statistics: Dict[str, Any]) -> float:
        """Calculate like to view ratio."""
        try:
            views = int(statistics.get('viewCount', 0))
            likes = int(statistics.get('likeCount', 0))
            
            if views == 0:
                return 0.0
            
            return likes / views
        except:
            return 0.0
    
    def _calculate_comment_to_view_ratio(self, statistics: Dict[str, Any]) -> float:
        """Calculate comment to view ratio."""
        try:
            views = int(statistics.get('viewCount', 0))
            comments = int(statistics.get('commentCount', 0))
            
            if views == 0:
                return 0.0
            
            return comments / views
        except:
            return 0.0
    
    def collect_videos_from_channels(self, channel_ids: List[str], 
                                   max_videos_per_channel: int = 50,
                                   days_back: int = 365) -> List[Dict[str, Any]]:
        """
        Collect videos from multiple channels.
        
        Args:
            channel_ids: List of channel IDs
            max_videos_per_channel: Maximum videos to collect per channel
            days_back: How many days back to collect videos
            
        Returns:
            List of video data dictionaries
        """
        all_videos = []
        published_after = datetime.now() - timedelta(days=days_back)
        
        logger.info(f"Collecting videos from {len(channel_ids)} channels")
        logger.info(f"Looking for videos published after {published_after.strftime('%Y-%m-%d')}")
        
        for i, channel_id in enumerate(channel_ids):
            logger.info(f"Processing channel {i+1}/{len(channel_ids)}: {channel_id}")
            
            # Get uploads playlist
            uploads_playlist_id = self.get_channel_uploads_playlist(channel_id)
            if not uploads_playlist_id:
                logger.warning(f"Could not get uploads playlist for channel {channel_id}")
                continue
            
            # Get video IDs from playlist
            video_ids = self.get_videos_from_playlist(
                uploads_playlist_id, 
                max_videos_per_channel, 
                published_after
            )
            
            if not video_ids:
                logger.warning(f"No videos found for channel {channel_id}")
                continue
            
            logger.info(f"Found {len(video_ids)} videos for channel {channel_id}")
            
            # Get detailed video information
            videos = self.get_video_details(video_ids)
            all_videos.extend(videos)
            
            logger.info(f"Collected {len(videos)} video details for channel {channel_id}")
            
            # Rate limiting between channels
            time.sleep(0.5)
        
        logger.info(f"Total videos collected: {len(all_videos)}")
        return all_videos
    
    def load_channels_from_file(self, file_path: str) -> List[str]:
        """
        Load channel IDs from a file.
        
        Args:
            file_path: Path to file containing channel data
            
        Returns:
            List of channel IDs
        """
        channel_ids = []
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        channel_ids = [item.get('channel_id', '') for item in data if 'channel_id' in item]
                    else:
                        logger.error("JSON file should contain a list of channel objects")
            
            elif file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    channel_ids = [row.get('channel_id', '') for row in reader if 'channel_id' in row]
            
            else:
                # Assume plain text file with one channel ID per line
                with open(file_path, 'r', encoding='utf-8') as f:
                    channel_ids = [line.strip() for line in f if line.strip()]
            
            # Filter out empty channel IDs
            channel_ids = [cid for cid in channel_ids if cid]
            
            logger.info(f"Loaded {len(channel_ids)} channel IDs from {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading channels from {file_path}: {e}")
        
        return channel_ids
    
    def save_videos(self, videos: List[Dict[str, Any]], output_dir: str = 'data/raw/videos'):
        """
        Save collected videos to files.
        
        Args:
            videos: List of video data
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_file = os.path.join(output_dir, f'videos_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_file = os.path.join(output_dir, f'videos_{timestamp}.csv')
        if videos:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=videos[0].keys())
                writer.writeheader()
                writer.writerows(videos)
        
        # Save separate files for Shorts and Long-form videos
        shorts = [v for v in videos if v.get('is_short', False)]
        longform = [v for v in videos if not v.get('is_short', False)]
        
        if shorts:
            shorts_file = os.path.join(output_dir, f'shorts_{timestamp}.csv')
            with open(shorts_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=shorts[0].keys())
                writer.writeheader()
                writer.writerows(shorts)
            logger.info(f"Saved {len(shorts)} Shorts to {shorts_file}")
        
        if longform:
            longform_file = os.path.join(output_dir, f'longform_{timestamp}.csv')
            with open(longform_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=longform[0].keys())
                writer.writeheader()
                writer.writerows(longform)
            logger.info(f"Saved {len(longform)} long-form videos to {longform_file}")
        
        logger.info(f"Saved {len(videos)} total videos to {json_file} and {csv_file}")


def main():
    """Main function to run video collection."""
    parser = argparse.ArgumentParser(description='Collect YouTube video metadata')
    parser.add_argument('--channels-file', required=True,
                       help='File containing channel IDs (JSON, CSV, or text)')
    parser.add_argument('--max-videos-per-channel', type=int, default=50,
                       help='Maximum videos to collect per channel')
    parser.add_argument('--days-back', type=int, default=365,
                       help='How many days back to collect videos')
    parser.add_argument('--output-dir', default='data/raw/videos',
                       help='Output directory for collected data')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = get_youtube_api_key()
    if not api_key:
        logger.error("YouTube API key not found. Please set YOUTUBE_API_KEY environment variable.")
        sys.exit(1)
    
    # Create output directory
    os.makedirs('logs', exist_ok=True)
    
    # Initialize collector
    collector = VideoCollector(api_key)
    
    try:
        # Load channel IDs
        channel_ids = collector.load_channels_from_file(args.channels_file)
        if not channel_ids:
            logger.error("No channel IDs found in the specified file")
            sys.exit(1)
        
        # Collect videos
        videos = collector.collect_videos_from_channels(
            channel_ids,
            args.max_videos_per_channel,
            args.days_back
        )
        
        if not videos:
            logger.warning("No videos were collected")
            sys.exit(0)
        
        # Save results
        collector.save_videos(videos, args.output_dir)
        
        # Print summary
        shorts_count = sum(1 for v in videos if v.get('is_short', False))
        longform_count = len(videos) - shorts_count
        
        logger.info("Video collection completed successfully")
        logger.info(f"Summary: {len(videos)} total videos ({shorts_count} Shorts, {longform_count} long-form)")
        
    except Exception as e:
        logger.error(f"Video collection failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
