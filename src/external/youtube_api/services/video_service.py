"""
YouTube Video Service for ViewTrendsSL

This module provides high-level operations for YouTube video data
using the YouTube Data API v3.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from src.external.youtube_api.client import YouTubeAPIClient
from src.external.youtube_api.models import VideoData, VideoStatistics
from src.external.youtube_api.exceptions import YouTubeAPIError, QuotaExceededError
from src.external.youtube_api.quota_manager import QuotaManager

# Configure logging
logger = logging.getLogger(__name__)


class VideoService:
    """Service for YouTube video operations."""
    
    def __init__(self, api_client: Optional[YouTubeAPIClient] = None):
        """
        Initialize the video service.
        
        Args:
            api_client: Optional YouTube API client instance
        """
        self.api_client = api_client or YouTubeAPIClient()
        self.quota_manager = QuotaManager()
    
    def get_video_by_id(self, video_id: str) -> Optional[VideoData]:
        """
        Get video information by video ID.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            VideoData instance or None if not found
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Check quota before making request
            if not self.quota_manager.can_make_request(1):
                raise QuotaExceededError("Insufficient quota for video request")
            
            response = self.api_client.get_video_details(video_id)
            
            if not response or 'items' not in response or not response['items']:
                logger.warning(f"Video not found: {video_id}")
                return None
            
            video_item = response['items'][0]
            
            # Extract video data
            snippet = video_item.get('snippet', {})
            statistics = video_item.get('statistics', {})
            content_details = video_item.get('contentDetails', {})
            
            # Parse duration
            duration_str = content_details.get('duration', 'PT0S')
            duration_seconds = self._parse_duration(duration_str)
            
            # Determine if it's a Short
            is_short = duration_seconds <= 60
            
            video_data = VideoData(
                video_id=video_item['id'],
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                channel_id=snippet.get('channelId', ''),
                channel_title=snippet.get('channelTitle', ''),
                published_at=snippet.get('publishedAt'),
                duration_seconds=duration_seconds,
                is_short=is_short,
                category_id=snippet.get('categoryId'),
                tags=snippet.get('tags', []),
                default_language=snippet.get('defaultLanguage'),
                statistics=VideoStatistics(
                    view_count=int(statistics.get('viewCount', 0)),
                    like_count=int(statistics.get('likeCount', 0)),
                    comment_count=int(statistics.get('commentCount', 0))
                ),
                thumbnail_url=snippet.get('thumbnails', {}).get('default', {}).get('url')
            )
            
            # Update quota usage
            self.quota_manager.record_request(1)
            
            logger.info(f"Retrieved video data: {video_data.title}")
            return video_data
            
        except Exception as e:
            logger.error(f"Error getting video {video_id}: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting video: {e}")
            raise YouTubeAPIError(f"Failed to get video: {e}")
    
    def get_videos_by_ids(self, video_ids: List[str]) -> List[VideoData]:
        """
        Get multiple videos by their IDs.
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of VideoData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        if not video_ids:
            return []
        
        try:
            # Check quota (1 unit per request, can get up to 50 videos per request)
            requests_needed = (len(video_ids) + 49) // 50  # Ceiling division
            if not self.quota_manager.can_make_request(requests_needed):
                raise QuotaExceededError("Insufficient quota for videos request")
            
            videos = []
            
            # Process videos in batches of 50 (API limit)
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.api_client.get_videos_batch(batch_ids)
                
                if response and 'items' in response:
                    for video_item in response['items']:
                        snippet = video_item.get('snippet', {})
                        statistics = video_item.get('statistics', {})
                        content_details = video_item.get('contentDetails', {})
                        
                        # Parse duration
                        duration_str = content_details.get('duration', 'PT0S')
                        duration_seconds = self._parse_duration(duration_str)
                        
                        # Determine if it's a Short
                        is_short = duration_seconds <= 60
                        
                        video_data = VideoData(
                            video_id=video_item['id'],
                            title=snippet.get('title', ''),
                            description=snippet.get('description', ''),
                            channel_id=snippet.get('channelId', ''),
                            channel_title=snippet.get('channelTitle', ''),
                            published_at=snippet.get('publishedAt'),
                            duration_seconds=duration_seconds,
                            is_short=is_short,
                            category_id=snippet.get('categoryId'),
                            tags=snippet.get('tags', []),
                            default_language=snippet.get('defaultLanguage'),
                            statistics=VideoStatistics(
                                view_count=int(statistics.get('viewCount', 0)),
                                like_count=int(statistics.get('likeCount', 0)),
                                comment_count=int(statistics.get('commentCount', 0))
                            ),
                            thumbnail_url=snippet.get('thumbnails', {}).get('default', {}).get('url')
                        )
                        
                        videos.append(video_data)
                
                # Update quota usage
                self.quota_manager.record_request(1)
            
            logger.info(f"Retrieved {len(videos)} videos from {len(video_ids)} requested")
            return videos
            
        except Exception as e:
            logger.error(f"Error getting videos batch: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting videos: {e}")
            raise YouTubeAPIError(f"Failed to get videos: {e}")
    
    def get_channel_videos(
        self, 
        channel_id: str, 
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None
    ) -> List[VideoData]:
        """
        Get videos from a specific channel.
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            published_after: Only get videos published after this date
            published_before: Only get videos published before this date
            
        Returns:
            List of VideoData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # First, get the channel's uploads playlist ID
            from src.external.youtube_api.services.channel_service import get_channel_service
            channel_service = get_channel_service()
            
            uploads_playlist_id = channel_service.get_channel_uploads_playlist_id(channel_id)
            
            if not uploads_playlist_id:
                logger.warning(f"No uploads playlist found for channel: {channel_id}")
                return []
            
            # Get videos from the uploads playlist
            return self.get_playlist_videos(
                playlist_id=uploads_playlist_id,
                max_results=max_results,
                published_after=published_after,
                published_before=published_before
            )
            
        except Exception as e:
            logger.error(f"Error getting videos for channel {channel_id}: {e}")
            raise
    
    def get_playlist_videos(
        self, 
        playlist_id: str, 
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None
    ) -> List[VideoData]:
        """
        Get videos from a playlist.
        
        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to retrieve
            published_after: Only get videos published after this date
            published_before: Only get videos published before this date
            
        Returns:
            List of VideoData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Check quota for playlist items request (1 unit per request)
            requests_needed = (max_results + 49) // 50  # Ceiling division
            if not self.quota_manager.can_make_request(requests_needed):
                raise QuotaExceededError("Insufficient quota for playlist request")
            
            video_ids = []
            next_page_token = None
            
            # Get video IDs from playlist
            while len(video_ids) < max_results:
                remaining = max_results - len(video_ids)
                page_size = min(remaining, 50)  # API limit
                
                response = self.api_client.get_playlist_items(
                    playlist_id=playlist_id,
                    max_results=page_size,
                    page_token=next_page_token
                )
                
                if not response or 'items' not in response:
                    break
                
                for item in response['items']:
                    video_id = item['snippet']['resourceId']['videoId']
                    
                    # Check date filters if provided
                    if published_after or published_before:
                        published_at_str = item['snippet'].get('publishedAt')
                        if published_at_str:
                            published_at = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                            
                            if published_after and published_at < published_after:
                                continue
                            if published_before and published_at > published_before:
                                continue
                    
                    video_ids.append(video_id)
                
                # Update quota usage
                self.quota_manager.record_request(1)
                
                # Check for next page
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            # Get detailed video information
            if video_ids:
                videos = self.get_videos_by_ids(video_ids)
                logger.info(f"Retrieved {len(videos)} videos from playlist {playlist_id}")
                return videos
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting playlist videos {playlist_id}: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting playlist videos: {e}")
            raise YouTubeAPIError(f"Failed to get playlist videos: {e}")
    
    def search_videos(
        self, 
        query: str, 
        max_results: int = 25,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None,
        region_code: Optional[str] = None,
        relevance_language: Optional[str] = None
    ) -> List[VideoData]:
        """
        Search for videos by query.
        
        Args:
            query: Search query
            max_results: Maximum number of results (default: 25, max: 50)
            published_after: Only get videos published after this date
            published_before: Only get videos published before this date
            region_code: Region code for localized results (e.g., 'LK' for Sri Lanka)
            relevance_language: Language for relevance (e.g., 'en', 'si', 'ta')
            
        Returns:
            List of VideoData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Search requests cost 100 units each
            if not self.quota_manager.can_make_request(100):
                raise QuotaExceededError("Insufficient quota for video search")
            
            # Perform search
            search_response = self.api_client.search_videos(
                query=query,
                max_results=min(max_results, 50),  # API limit
                published_after=published_after,
                published_before=published_before,
                region_code=region_code,
                relevance_language=relevance_language
            )
            
            if not search_response or 'items' not in search_response:
                logger.warning(f"No search results for query: {query}")
                return []
            
            # Extract video IDs from search results
            video_ids = []
            for item in search_response['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_ids.append(item['id']['videoId'])
            
            # Update quota for search
            self.quota_manager.record_request(100)
            
            if not video_ids:
                return []
            
            # Get detailed video information
            videos = self.get_videos_by_ids(video_ids)
            
            logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos
            
        except Exception as e:
            logger.error(f"Error searching videos with query '{query}': {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while searching videos: {e}")
            raise YouTubeAPIError(f"Failed to search videos: {e}")
    
    def update_video_statistics(self, video_id: str) -> Optional[VideoStatistics]:
        """
        Get updated statistics for a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            VideoStatistics instance or None if not found
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            video_data = self.get_video_by_id(video_id)
            
            if video_data:
                logger.info(f"Updated statistics for video: {video_data.title}")
                return video_data.statistics
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating statistics for video {video_id}: {e}")
            raise
    
    def get_trending_videos(
        self, 
        region_code: str = 'LK', 
        category_id: Optional[str] = None,
        max_results: int = 50
    ) -> List[VideoData]:
        """
        Get trending videos for a specific region.
        
        Args:
            region_code: Region code (default: 'LK' for Sri Lanka)
            category_id: Optional category ID to filter by
            max_results: Maximum number of videos to retrieve
            
        Returns:
            List of trending VideoData instances
            
        Raises:
            YouTubeAPIError: If API request fails
            QuotaExceededError: If quota is exceeded
        """
        try:
            # Check quota
            if not self.quota_manager.can_make_request(1):
                raise QuotaExceededError("Insufficient quota for trending videos request")
            
            response = self.api_client.get_trending_videos(
                region_code=region_code,
                category_id=category_id,
                max_results=min(max_results, 50)
            )
            
            if not response or 'items' not in response:
                logger.warning(f"No trending videos found for region: {region_code}")
                return []
            
            videos = []
            for video_item in response['items']:
                snippet = video_item.get('snippet', {})
                statistics = video_item.get('statistics', {})
                content_details = video_item.get('contentDetails', {})
                
                # Parse duration
                duration_str = content_details.get('duration', 'PT0S')
                duration_seconds = self._parse_duration(duration_str)
                
                # Determine if it's a Short
                is_short = duration_seconds <= 60
                
                video_data = VideoData(
                    video_id=video_item['id'],
                    title=snippet.get('title', ''),
                    description=snippet.get('description', ''),
                    channel_id=snippet.get('channelId', ''),
                    channel_title=snippet.get('channelTitle', ''),
                    published_at=snippet.get('publishedAt'),
                    duration_seconds=duration_seconds,
                    is_short=is_short,
                    category_id=snippet.get('categoryId'),
                    tags=snippet.get('tags', []),
                    default_language=snippet.get('defaultLanguage'),
                    statistics=VideoStatistics(
                        view_count=int(statistics.get('viewCount', 0)),
                        like_count=int(statistics.get('likeCount', 0)),
                        comment_count=int(statistics.get('commentCount', 0))
                    ),
                    thumbnail_url=snippet.get('thumbnails', {}).get('default', {}).get('url')
                )
                
                videos.append(video_data)
            
            # Update quota usage
            self.quota_manager.record_request(1)
            
            logger.info(f"Retrieved {len(videos)} trending videos for region {region_code}")
            return videos
            
        except Exception as e:
            logger.error(f"Error getting trending videos for region {region_code}: {e}")
            if "quotaExceeded" in str(e):
                raise QuotaExceededError(f"Quota exceeded while getting trending videos: {e}")
            raise YouTubeAPIError(f"Failed to get trending videos: {e}")
    
    def _parse_duration(self, duration_str: str) -> int:
        """
        Parse ISO 8601 duration string to seconds.
        
        Args:
            duration_str: ISO 8601 duration string (e.g., 'PT1M30S')
            
        Returns:
            Duration in seconds
        """
        try:
            import re
            
            # Remove 'PT' prefix
            duration_str = duration_str[2:] if duration_str.startswith('PT') else duration_str
            
            # Extract hours, minutes, seconds
            hours = 0
            minutes = 0
            seconds = 0
            
            # Hours
            h_match = re.search(r'(\d+)H', duration_str)
            if h_match:
                hours = int(h_match.group(1))
            
            # Minutes
            m_match = re.search(r'(\d+)M', duration_str)
            if m_match:
                minutes = int(m_match.group(1))
            
            # Seconds
            s_match = re.search(r'(\d+)S', duration_str)
            if s_match:
                seconds = int(s_match.group(1))
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
            
        except Exception as e:
            logger.warning(f"Error parsing duration '{duration_str}': {e}")
            return 0
    
    def get_quota_status(self) -> Dict[str, Any]:
        """
        Get current quota status.
        
        Returns:
            Dictionary with quota information
        """
        return self.quota_manager.get_quota_status()


# Global service instance
_video_service: Optional[VideoService] = None

def get_video_service() -> VideoService:
    """Get the global video service instance."""
    global _video_service
    
    if _video_service is None:
        _video_service = VideoService()
    
    return _video_service
