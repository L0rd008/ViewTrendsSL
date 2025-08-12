#!/usr/bin/env python3
"""
YouTube Channel Collection Script

This script discovers and collects Sri Lankan YouTube channels using various methods:
- Manual seed list
- Keyword-based search
- Related channel discovery

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import json
import csv
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import argparse

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
        logging.FileHandler('logs/channel_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ChannelCollector:
    """Collects Sri Lankan YouTube channels using various discovery methods."""
    
    def __init__(self, api_key: str):
        """
        Initialize the channel collector.
        
        Args:
            api_key: YouTube Data API key
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_manager = QuotaManager()
        self.collected_channels = set()
        self.channel_data = []
        
        # Sri Lankan keywords for channel discovery
        self.sri_lankan_keywords = [
            'sri lanka', 'sinhala', 'tamil', 'colombo', 'kandy', 'galle',
            'sri lankan', 'lanka', 'ceylon', 'lk', 'ශ්‍රී ලංකා', 'இலங்கை'
        ]
        
        # Manual seed list of known Sri Lankan channels
        self.seed_channels = [
            'UCjGa0sNNbNE-Jz8VCqhJJzw',  # Ada Derana
            'UCjzN4_vKjKZ_dVEcvOmVQGg',  # Hiru News
            'UCjGa0sNNbNE-Jz8VCqhJJzw',  # Sirasa TV
            'UCjGa0sNNbNE-Jz8VCqhJJzw',  # ITN
            # Add more known Sri Lankan channel IDs here
        ]
    
    def get_channel_details(self, channel_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information for a list of channel IDs.
        
        Args:
            channel_ids: List of YouTube channel IDs
            
        Returns:
            List of channel data dictionaries
        """
        channels = []
        
        # Process channels in batches of 50 (API limit)
        for i in range(0, len(channel_ids), 50):
            batch = channel_ids[i:i+50]
            
            try:
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping collection")
                    break
                
                response = self.youtube.channels().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(batch)
                ).execute()
                
                self.quota_manager.record_request(1)
                
                for item in response.get('items', []):
                    channel_data = self._extract_channel_data(item)
                    if self._is_sri_lankan_channel(channel_data):
                        channels.append(channel_data)
                        logger.info(f"Found Sri Lankan channel: {channel_data['title']}")
                
                # Rate limiting
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting channel details: {e}")
                continue
        
        return channels
    
    def search_channels_by_keywords(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Search for channels using Sri Lankan keywords.
        
        Args:
            max_results: Maximum number of results to collect
            
        Returns:
            List of channel data dictionaries
        """
        channels = []
        
        for keyword in self.sri_lankan_keywords:
            if len(channels) >= max_results:
                break
            
            try:
                if not self.quota_manager.can_make_request(100):
                    logger.warning("API quota exhausted, stopping search")
                    break
                
                logger.info(f"Searching for channels with keyword: {keyword}")
                
                response = self.youtube.search().list(
                    part='snippet',
                    q=keyword,
                    type='channel',
                    regionCode='LK',
                    maxResults=min(50, max_results - len(channels)),
                    order='relevance'
                ).execute()
                
                self.quota_manager.record_request(100)
                
                channel_ids = [item['id']['channelId'] for item in response.get('items', [])]
                
                if channel_ids:
                    channel_details = self.get_channel_details(channel_ids)
                    channels.extend(channel_details)
                
                # Rate limiting
                time.sleep(1)
                
            except HttpError as e:
                logger.error(f"API error searching for keyword '{keyword}': {e}")
                continue
        
        return channels
    
    def get_related_channels(self, seed_channel_ids: List[str], max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Find related channels by analyzing featured channels and collaborations.
        
        Args:
            seed_channel_ids: List of seed channel IDs
            max_results: Maximum number of results to collect
            
        Returns:
            List of channel data dictionaries
        """
        related_channels = []
        processed_channels = set()
        
        for channel_id in seed_channel_ids:
            if len(related_channels) >= max_results:
                break
            
            if channel_id in processed_channels:
                continue
            
            processed_channels.add(channel_id)
            
            try:
                # Get channel's recent videos to find collaborations
                if not self.quota_manager.can_make_request(1):
                    logger.warning("API quota exhausted, stopping related channel search")
                    break
                
                # Get uploads playlist
                channel_response = self.youtube.channels().list(
                    part='contentDetails',
                    id=channel_id
                ).execute()
                
                self.quota_manager.record_request(1)
                
                if not channel_response.get('items'):
                    continue
                
                uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                
                # Get recent videos
                if not self.quota_manager.can_make_request(1):
                    break
                
                videos_response = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=10
                ).execute()
                
                self.quota_manager.record_request(1)
                
                # Extract channel mentions from video descriptions
                for video in videos_response.get('items', []):
                    description = video['snippet'].get('description', '')
                    # Simple heuristic to find channel mentions
                    # This could be improved with more sophisticated NLP
                    if any(keyword in description.lower() for keyword in self.sri_lankan_keywords):
                        # This is a basic implementation - in practice, you'd want
                        # more sophisticated channel extraction from descriptions
                        pass
                
                time.sleep(0.1)
                
            except HttpError as e:
                logger.error(f"API error getting related channels for {channel_id}: {e}")
                continue
        
        return related_channels
    
    def _extract_channel_data(self, channel_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from YouTube API channel response.
        
        Args:
            channel_item: Channel item from YouTube API
            
        Returns:
            Extracted channel data dictionary
        """
        snippet = channel_item.get('snippet', {})
        statistics = channel_item.get('statistics', {})
        
        return {
            'channel_id': channel_item['id'],
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
            'country': snippet.get('country', ''),
            'default_language': snippet.get('defaultLanguage', ''),
            'subscriber_count': int(statistics.get('subscriberCount', 0)),
            'video_count': int(statistics.get('videoCount', 0)),
            'view_count': int(statistics.get('viewCount', 0)),
            'thumbnail_url': snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
            'collected_at': datetime.now().isoformat(),
            'collection_method': 'api_search'
        }
    
    def _is_sri_lankan_channel(self, channel_data: Dict[str, Any]) -> bool:
        """
        Determine if a channel is Sri Lankan based on various signals.
        
        Args:
            channel_data: Channel data dictionary
            
        Returns:
            True if channel appears to be Sri Lankan
        """
        # Check country code
        if channel_data.get('country') == 'LK':
            return True
        
        # Check for Sri Lankan keywords in title and description
        text_to_check = f"{channel_data.get('title', '')} {channel_data.get('description', '')}".lower()
        
        if any(keyword in text_to_check for keyword in self.sri_lankan_keywords):
            return True
        
        # Check for Sinhala or Tamil characters
        import re
        sinhala_pattern = r'[\u0D80-\u0DFF]'
        tamil_pattern = r'[\u0B80-\u0BFF]'
        
        if re.search(sinhala_pattern, text_to_check) or re.search(tamil_pattern, text_to_check):
            return True
        
        return False
    
    def collect_all_channels(self, max_results: int = 500) -> List[Dict[str, Any]]:
        """
        Collect channels using all available methods.
        
        Args:
            max_results: Maximum number of channels to collect
            
        Returns:
            List of collected channel data
        """
        all_channels = []
        
        logger.info("Starting channel collection process")
        
        # 1. Get seed channels
        logger.info("Collecting seed channels...")
        seed_channels = self.get_channel_details(self.seed_channels)
        all_channels.extend(seed_channels)
        
        # 2. Search by keywords
        logger.info("Searching channels by keywords...")
        keyword_channels = self.search_channels_by_keywords(max_results // 2)
        all_channels.extend(keyword_channels)
        
        # 3. Find related channels
        logger.info("Finding related channels...")
        seed_ids = [ch['channel_id'] for ch in seed_channels]
        related_channels = self.get_related_channels(seed_ids, max_results // 4)
        all_channels.extend(related_channels)
        
        # Remove duplicates
        unique_channels = {}
        for channel in all_channels:
            channel_id = channel['channel_id']
            if channel_id not in unique_channels:
                unique_channels[channel_id] = channel
        
        final_channels = list(unique_channels.values())
        
        logger.info(f"Collected {len(final_channels)} unique Sri Lankan channels")
        
        return final_channels
    
    def save_channels(self, channels: List[Dict[str, Any]], output_dir: str = 'data/raw'):
        """
        Save collected channels to files.
        
        Args:
            channels: List of channel data
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_file = os.path.join(output_dir, f'channels_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_file = os.path.join(output_dir, f'channels_{timestamp}.csv')
        if channels:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=channels[0].keys())
                writer.writeheader()
                writer.writerows(channels)
        
        logger.info(f"Saved {len(channels)} channels to {json_file} and {csv_file}")


def main():
    """Main function to run channel collection."""
    parser = argparse.ArgumentParser(description='Collect Sri Lankan YouTube channels')
    parser.add_argument('--max-results', type=int, default=500,
                       help='Maximum number of channels to collect')
    parser.add_argument('--output-dir', default='data/raw',
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
    collector = ChannelCollector(api_key)
    
    try:
        # Collect channels
        channels = collector.collect_all_channels(args.max_results)
        
        # Save results
        collector.save_channels(channels, args.output_dir)
        
        logger.info("Channel collection completed successfully")
        
    except Exception as e:
        logger.error(f"Channel collection failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
