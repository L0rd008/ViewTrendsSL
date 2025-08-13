"""
YouTube Channel Service for ViewTrendsSL

This module provides high-level operations for YouTube channel data
using the YouTube Data API v3.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.external.youtube_api.client import YouTubeAPIClient
from src.external.youtube_api.models import ChannelData, ChannelStatistics
from src.external.youtube_api.exceptions import YouTubeAPIError, QuotaExceededError
from src.external.youtube_api.quota_manager import QuotaManager

# Configure logging
logger = logging.getLogger(__name__)


class ChannelService:
    """Service for YouTube channel operations."""
    
    def __init__(self, api_client: Optional[YouTubeAPIClient] = None):
        """
        Initialize the channel service.
        
        Args:
            api_client: Optional YouTube API client instance
        """
        self.api_client = api_client or YouTubeAPIClient()
        self.quota_manager = QuotaManager()
    
    def get_channel_by_id(self, channel_id: str) -> Optional[ChannelData]:
        """
        Get channel information by channel ID.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            ChannelData instance or None if not found
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Check quota before making request
            if not self.quota_manager.can_make_request(1):
                raise QuotaExceededError("Insufficient quota for channel request")
            
            response = self.api_client.get_channel_details(channel_id)
            
            if not response or 'items' not in response or not response['items']:
                logger.warning(f"Channel not found: {channel_id}")
                return None
            
            channel_item = response['items'][0]
            
            # Extract channel data
            snippet = channel_item.get('snippet', {})
            statistics = channel_item.get('statistics', {})
            
            channel_data = ChannelData(
                channel_id=channel_item['id'],
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                published_at=snippet.get('publishedAt'),
                country=snippet.get('country'),
                default_language=snippet.get('defaultLanguage'),
                statistics=ChannelStatistics(
                    subscriber_count=int(statistics.get('subscriberCount', 0)),
                    video_count=int(statistics.get('videoCount', 0)),
                    view_count=int(statistics.get('viewCount', 0))
                ),
                thumbnail_url=snippet.get('thumbnails', {}).get('default', {}).get('url'),
                custom_url=snippet.get('customUrl')
            )
            
            # Update quota usage
            self.quota_manager.record_request(1)
            
            logger.info(f"Retrieved channel data: {channel_data.title}")
            return channel_data
            
        except Exception as e:
            logger.error(f"Error getting channel {channel_id}: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting channel: {e}")
            raise YouTubeAPIError(f"Failed to get channel: {e}")
    
    def get_channels_by_ids(self, channel_ids: List[str]) -> List[ChannelData]:
        """
        Get multiple channels by their IDs.
        
        Args:
            channel_ids: List of YouTube channel IDs
            
        Returns:
            List of ChannelData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        if not channel_ids:
            return []
        
        try:
            # Check quota (1 unit per request, can get up to 50 channels per request)
            requests_needed = (len(channel_ids) + 49) // 50  # Ceiling division
            if not self.quota_manager.can_make_request(requests_needed):
                raise QuotaExceededError("Insufficient quota for channels request")
            
            channels = []
            
            # Process channels in batches of 50 (API limit)
            for i in range(0, len(channel_ids), 50):
                batch_ids = channel_ids[i:i+50]
                
                response = self.api_client.get_channels_batch(batch_ids)
                
                if response and 'items' in response:
                    for channel_item in response['items']:
                        snippet = channel_item.get('snippet', {})
                        statistics = channel_item.get('statistics', {})
                        
                        channel_data = ChannelData(
                            channel_id=channel_item['id'],
                            title=snippet.get('title', ''),
                            description=snippet.get('description', ''),
                            published_at=snippet.get('publishedAt'),
                            country=snippet.get('country'),
                            default_language=snippet.get('defaultLanguage'),
                            statistics=ChannelStatistics(
                                subscriber_count=int(statistics.get('subscriberCount', 0)),
                                video_count=int(statistics.get('videoCount', 0)),
                                view_count=int(statistics.get('viewCount', 0))
                            ),
                            thumbnail_url=snippet.get('thumbnails', {}).get('default', {}).get('url'),
                            custom_url=snippet.get('customUrl')
                        )
                        
                        channels.append(channel_data)
                
                # Update quota usage
                self.quota_manager.record_request(1)
            
            logger.info(f"Retrieved {len(channels)} channels from {len(channel_ids)} requested")
            return channels
            
        except Exception as e:
            logger.error(f"Error getting channels batch: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting channels: {e}")
            raise YouTubeAPIError(f"Failed to get channels: {e}")
    
    def search_channels(
        self, 
        query: str, 
        max_results: int = 25,
        region_code: Optional[str] = None,
        relevance_language: Optional[str] = None
    ) -> List[ChannelData]:
        """
        Search for channels by query.
        
        Args:
            query: Search query
            max_results: Maximum number of results (default: 25, max: 50)
            region_code: Region code for localized results (e.g., 'LK' for Sri Lanka)
            relevance_language: Language for relevance (e.g., 'en', 'si', 'ta')
            
        Returns:
            List of ChannelData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Search requests cost 100 units each
            if not self.quota_manager.can_make_request(100):
                raise QuotaExceededError("Insufficient quota for channel search")
            
            # Perform search
            search_response = self.api_client.search_channels(
                query=query,
                max_results=min(max_results, 50),  # API limit
                region_code=region_code,
                relevance_language=relevance_language
            )
            
            if not search_response or 'items' not in search_response:
                logger.warning(f"No search results for query: {query}")
                return []
            
            # Extract channel IDs from search results
            channel_ids = []
            for item in search_response['items']:
                if item['id']['kind'] == 'youtube#channel':
                    channel_ids.append(item['id']['channelId'])
            
            # Update quota for search
            self.quota_manager.record_request(100)
            
            if not channel_ids:
                return []
            
            # Get detailed channel information
            channels = self.get_channels_by_ids(channel_ids)
            
            logger.info(f"Found {len(channels)} channels for query: {query}")
            return channels
            
        except Exception as e:
            logger.error(f"Error searching channels with query '{query}': {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while searching channels: {e}")
            raise YouTubeAPIError(f"Failed to search channels: {e}")
    
    def get_channel_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """
        Get the uploads playlist ID for a channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Uploads playlist ID or None if not found
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Check quota
            if not self.quota_manager.can_make_request(1):
                raise QuotaExceededError("Insufficient quota for channel request")
            
            response = self.api_client.get_channel_content_details(channel_id)
            
            if not response or 'items' not in response or not response['items']:
                logger.warning(f"Channel not found: {channel_id}")
                return None
            
            content_details = response['items'][0].get('contentDetails', {})
            related_playlists = content_details.get('relatedPlaylists', {})
            uploads_playlist_id = related_playlists.get('uploads')
            
            # Update quota usage
            self.quota_manager.record_request(1)
            
            if uploads_playlist_id:
                logger.info(f"Found uploads playlist for channel {channel_id}: {uploads_playlist_id}")
            else:
                logger.warning(f"No uploads playlist found for channel: {channel_id}")
            
            return uploads_playlist_id
            
        except Exception as e:
            logger.error(f"Error getting uploads playlist for channel {channel_id}: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting uploads playlist: {e}")
            raise YouTubeAPIError(f"Failed to get uploads playlist: {e}")
    
    def get_sri_lankan_channels_by_keywords(
        self, 
        keywords: List[str], 
        max_results_per_keyword: int = 10
    ) -> List[ChannelData]:
        """
        Search for Sri Lankan channels using specific keywords.
        
        Args:
            keywords: List of Sri Lankan-specific keywords
            max_results_per_keyword: Maximum results per keyword
            
        Returns:
            List of unique ChannelData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        all_channels = []
        seen_channel_ids = set()
        
        for keyword in keywords:
            try:
                logger.info(f"Searching for Sri Lankan channels with keyword: {keyword}")
                
                # Search with Sri Lankan region code
                channels = self.search_channels(
                    query=keyword,
                    max_results=max_results_per_keyword,
                    region_code='LK',
                    relevance_language='en'
                )
                
                # Add unique channels
                for channel in channels:
                    if channel.channel_id not in seen_channel_ids:
                        all_channels.append(channel)
                        seen_channel_ids.add(channel.channel_id)
                
                logger.info(f"Found {len(channels)} channels for keyword '{keyword}'")
                
            except QuotaExceededError:
                logger.warning(f"Quota exceeded while searching for keyword: {keyword}")
                break
            except Exception as e:
                logger.error(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        logger.info(f"Total unique Sri Lankan channels found: {len(all_channels)}")
        return all_channels
    
    def update_channel_statistics(self, channel_id: str) -> Optional[ChannelStatistics]:
        """
        Get updated statistics for a channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            ChannelStatistics instance or None if not found
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            channel_data = self.get_channel_by_id(channel_id)
            
            if channel_data:
                logger.info(f"Updated statistics for channel: {channel_data.title}")
                return channel_data.statistics
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating statistics for channel {channel_id}: {e}")
            raise
    
    def is_channel_sri_lankan(self, channel_data: ChannelData) -> bool:
        """
        Determine if a channel is Sri Lankan based on various indicators.
        
        Args:
            channel_data: ChannelData instance
            
        Returns:
            True if channel appears to be Sri Lankan, False otherwise
        """
        sri_lankan_indicators = 0
        
        # Check country
        if channel_data.country and channel_data.country.upper() == 'LK':
            sri_lankan_indicators += 3
        
        # Check language
        if channel_data.default_language:
            if channel_data.default_language.lower() in ['si', 'ta', 'sin', 'tam']:
                sri_lankan_indicators += 2
            elif channel_data.default_language.lower() == 'en':
                sri_lankan_indicators += 1
        
        # Check title and description for Sri Lankan keywords
        sri_lankan_keywords = [
            'sri lanka', 'srilanka', 'colombo', 'kandy', 'galle', 'jaffna',
            'sinhala', 'tamil', 'lanka', 'ceylon', 'lk', 'rupee', 'rupees'
        ]
        
        text_to_check = f"{channel_data.title} {channel_data.description}".lower()
        
        for keyword in sri_lankan_keywords:
            if keyword in text_to_check:
                sri_lankan_indicators += 1
                break
        
        # Consider it Sri Lankan if we have strong indicators
        is_sri_lankan = sri_lankan_indicators >= 2
        
        logger.debug(f"Channel '{channel_data.title}' Sri Lankan indicators: {sri_lankan_indicators}, "
                    f"Classified as Sri Lankan: {is_sri_lankan}")
        
        return is_sri_lankan
    
    def get_quota_status(self) -> Dict[str, Any]:
        """
        Get current quota status.
        
        Returns:
            Dictionary with quota information
        """
        return self.quota_manager.get_quota_status()


# Global service instance
_channel_service: Optional[ChannelService] = None

def get_channel_service() -> ChannelService:
    """Get the global channel service instance."""
    global _channel_service
    
    if _channel_service is None:
        _channel_service = ChannelService()
    
    return _channel_service
