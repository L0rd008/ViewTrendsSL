"""Main YouTube API client for ViewTrendsSL."""

from typing import Dict, List, Optional, Union, Any
import asyncio
import time
import logging
from datetime import datetime, timezone
import httpx
from urllib.parse import urlencode

from .exceptions import (
    YouTubeAPIError, QuotaExceededError, AuthenticationError,
    RateLimitError, NetworkError, parse_youtube_api_error,
    is_retryable_error, get_retry_delay
)
from .models import (
    VideoResponse, ChannelResponse, SearchResponse,
    BatchVideoResponse, BatchChannelResponse, PlaylistItemsResponse,
    extract_video_id_from_url, extract_channel_id_from_url,
    validate_video_id, validate_channel_id
)
from .quota_manager import QuotaManager, APIEndpoint

logger = logging.getLogger(__name__)


class YouTubeAPIClient:
    """Enhanced YouTube API client with quota management and retry logic."""
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self, api_keys: Dict[str, str], quota_storage_path: Optional[str] = None,
                 timeout: int = 30, max_retries: int = 3):
        """Initialize YouTube API client.
        
        Args:
            api_keys: Dictionary of {key_name: api_key}
            quota_storage_path: Path to store quota usage data
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.quota_manager = QuotaManager(api_keys, quota_storage_path)
        self.timeout = timeout
        self.max_retries = max_retries
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
        )
        
        logger.info(f"Initialized YouTube API client with {len(api_keys)} API keys")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def _make_request(self, endpoint: APIEndpoint, params: Dict[str, Any],
                          expected_response_type: type) -> Any:
        """Make a request to the YouTube API with retry logic.
        
        Args:
            endpoint: API endpoint to call
            params: Request parameters
            expected_response_type: Expected response model type
            
        Returns:
            Parsed response object
            
        Raises:
            YouTubeAPIError: If request fails after all retries
        """
        # Get the best API key for this request
        key_info = self.quota_manager.get_best_key_for_request(endpoint)
        if not key_info:
            raise QuotaExceededError("No API keys with sufficient quota available")
        
        # Reserve quota
        if not self.quota_manager.reserve_quota(key_info, endpoint):
            raise QuotaExceededError(f"Failed to reserve quota for {endpoint.endpoint_name}")
        
        # Add API key to parameters
        params['key'] = key_info.key
        
        # Build URL
        url = f"{self.BASE_URL}/{endpoint.endpoint_name}"
        
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.debug(f"Making request to {endpoint.endpoint_name} (attempt {attempt + 1})")
                
                response = await self.client.get(url, params=params)
                
                # Check for HTTP errors
                if response.status_code == 200:
                    # Success
                    data = response.json()
                    self.quota_manager.record_request_success(key_info, endpoint)
                    
                    # Parse and return response
                    return expected_response_type.parse_obj(data)
                
                else:
                    # API error
                    try:
                        error_data = response.json()
                    except:
                        error_data = {'error': {'message': f'HTTP {response.status_code}'}}
                    
                    api_error = parse_youtube_api_error(error_data, response.status_code)
                    
                    # Record error
                    self.quota_manager.record_request_error(key_info, endpoint, api_error)
                    
                    # Check if we should retry
                    if not is_retryable_error(api_error) or attempt == self.max_retries:
                        raise api_error
                    
                    last_error = api_error
                    
                    # Wait before retry
                    delay = get_retry_delay(api_error, attempt + 1)
                    logger.warning(f"Request failed, retrying in {delay}s: {api_error}")
                    await asyncio.sleep(delay)
            
            except httpx.RequestError as e:
                # Network error
                network_error = NetworkError(f"Network error: {str(e)}", original_error=e)
                self.quota_manager.record_request_error(key_info, endpoint, network_error)
                
                if attempt == self.max_retries:
                    raise network_error
                
                last_error = network_error
                
                # Wait before retry
                delay = get_retry_delay(network_error, attempt + 1)
                logger.warning(f"Network error, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)
        
        # If we get here, all retries failed
        raise last_error or YouTubeAPIError("Request failed after all retries")
    
    async def get_video(self, video_id: str, parts: List[str] = None) -> VideoResponse:
        """Get information about a single video.
        
        Args:
            video_id: YouTube video ID
            parts: List of parts to retrieve (default: snippet, statistics, contentDetails)
            
        Returns:
            VideoResponse object
            
        Raises:
            YouTubeAPIError: If request fails
        """
        if not validate_video_id(video_id):
            # Try to extract video ID from URL
            extracted_id = extract_video_id_from_url(video_id)
            if not extracted_id:
                raise YouTubeAPIError(f"Invalid video ID or URL: {video_id}")
            video_id = extracted_id
        
        if parts is None:
            parts = ['snippet', 'statistics', 'contentDetails']
        
        params = {
            'part': ','.join(parts),
            'id': video_id
        }
        
        response = await self._make_request(APIEndpoint.VIDEOS_LIST, params, BatchVideoResponse)
        
        if not response.items:
            from .exceptions import VideoNotFoundError
            raise VideoNotFoundError(video_id)
        
        return response.items[0]
    
    async def get_videos(self, video_ids: List[str], parts: List[str] = None) -> List[VideoResponse]:
        """Get information about multiple videos.
        
        Args:
            video_ids: List of YouTube video IDs
            parts: List of parts to retrieve
            
        Returns:
            List of VideoResponse objects
            
        Raises:
            YouTubeAPIError: If request fails
        """
        if not video_ids:
            return []
        
        if parts is None:
            parts = ['snippet', 'statistics', 'contentDetails']
        
        # Validate and clean video IDs
        clean_ids = []
        for video_id in video_ids:
            if validate_video_id(video_id):
                clean_ids.append(video_id)
            else:
                extracted_id = extract_video_id_from_url(video_id)
                if extracted_id:
                    clean_ids.append(extracted_id)
                else:
                    logger.warning(f"Invalid video ID skipped: {video_id}")
        
        if not clean_ids:
            return []
        
        # Process in batches of 50 (API limit)
        all_videos = []
        for i in range(0, len(clean_ids), 50):
            batch_ids = clean_ids[i:i+50]
            
            params = {
                'part': ','.join(parts),
                'id': ','.join(batch_ids)
            }
            
            response = await self._make_request(APIEndpoint.VIDEOS_LIST, params, BatchVideoResponse)
            all_videos.extend(response.items)
        
        return all_videos
    
    async def get_channel(self, channel_id: str, parts: List[str] = None) -> ChannelResponse:
        """Get information about a single channel.
        
        Args:
            channel_id: YouTube channel ID
            parts: List of parts to retrieve
            
        Returns:
            ChannelResponse object
            
        Raises:
            YouTubeAPIError: If request fails
        """
        if not validate_channel_id(channel_id):
            # Try to extract channel ID from URL
            extracted_id = extract_channel_id_from_url(channel_id)
            if not extracted_id:
                raise YouTubeAPIError(f"Invalid channel ID or URL: {channel_id}")
            channel_id = extracted_id
        
        if parts is None:
            parts = ['snippet', 'statistics', 'contentDetails']
        
        params = {
            'part': ','.join(parts),
            'id': channel_id
        }
        
        response = await self._make_request(APIEndpoint.CHANNELS_LIST, params, BatchChannelResponse)
        
        if not response.items:
            from .exceptions import ChannelNotFoundError
            raise ChannelNotFoundError(channel_id)
        
        return response.items[0]
    
    async def get_channels(self, channel_ids: List[str], parts: List[str] = None) -> List[ChannelResponse]:
        """Get information about multiple channels.
        
        Args:
            channel_ids: List of YouTube channel IDs
            parts: List of parts to retrieve
            
        Returns:
            List of ChannelResponse objects
            
        Raises:
            YouTubeAPIError: If request fails
        """
        if not channel_ids:
            return []
        
        if parts is None:
            parts = ['snippet', 'statistics', 'contentDetails']
        
        # Validate and clean channel IDs
        clean_ids = []
        for channel_id in channel_ids:
            if validate_channel_id(channel_id):
                clean_ids.append(channel_id)
            else:
                extracted_id = extract_channel_id_from_url(channel_id)
                if extracted_id:
                    clean_ids.append(extracted_id)
                else:
                    logger.warning(f"Invalid channel ID skipped: {channel_id}")
        
        if not clean_ids:
            return []
        
        # Process in batches of 50 (API limit)
        all_channels = []
        for i in range(0, len(clean_ids), 50):
            batch_ids = clean_ids[i:i+50]
            
            params = {
                'part': ','.join(parts),
                'id': ','.join(batch_ids)
            }
            
            response = await self._make_request(APIEndpoint.CHANNELS_LIST, params, BatchChannelResponse)
            all_channels.extend(response.items)
        
        return all_channels
    
    async def search_videos(self, query: str, max_results: int = 50, 
                          published_after: Optional[datetime] = None,
                          published_before: Optional[datetime] = None,
                          region_code: str = 'LK',
                          relevance_language: str = 'en') -> SearchResponse:
        """Search for videos.
        
        Args:
            query: Search query
            max_results: Maximum number of results (max 50 per request)
            published_after: Only return videos published after this date
            published_before: Only return videos published before this date
            region_code: Region code for localized results
            relevance_language: Language for relevance ranking
            
        Returns:
            SearchResponse object
            
        Raises:
            YouTubeAPIError: If request fails
        """
        params = {
            'part': 'snippet',
            'type': 'video',
            'q': query,
            'maxResults': min(max_results, 50),
            'regionCode': region_code,
            'relevanceLanguage': relevance_language,
            'order': 'relevance'
        }
        
        if published_after:
            params['publishedAfter'] = published_after.isoformat()
        
        if published_before:
            params['publishedBefore'] = published_before.isoformat()
        
        return await self._make_request(APIEndpoint.SEARCH_LIST, params, SearchResponse)
    
    async def get_channel_videos(self, channel_id: str, max_results: int = 50,
                               published_after: Optional[datetime] = None) -> List[VideoResponse]:
        """Get videos from a channel's uploads playlist.
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            published_after: Only return videos published after this date
            
        Returns:
            List of VideoResponse objects
            
        Raises:
            YouTubeAPIError: If request fails
        """
        # First get the channel to find the uploads playlist
        channel = await self.get_channel(channel_id, parts=['contentDetails'])
        
        if not channel.content_details or not channel.content_details.uploads_playlist_id:
            return []
        
        uploads_playlist_id = channel.content_details.uploads_playlist_id
        
        # Get video IDs from the playlist
        video_ids = []
        next_page_token = None
        
        while len(video_ids) < max_results:
            params = {
                'part': 'snippet',
                'playlistId': uploads_playlist_id,
                'maxResults': min(50, max_results - len(video_ids))
            }
            
            if next_page_token:
                params['pageToken'] = next_page_token
            
            response = await self._make_request(APIEndpoint.PLAYLIST_ITEMS_LIST, params, PlaylistItemsResponse)
            
            for item in response.items:
                if item.snippet.video_id:
                    # Check published date filter
                    if published_after and item.snippet.published_at < published_after:
                        continue
                    video_ids.append(item.snippet.video_id)
            
            next_page_token = response.next_page_token
            if not next_page_token or len(video_ids) >= max_results:
                break
        
        # Get full video details
        if video_ids:
            return await self.get_videos(video_ids[:max_results])
        
        return []
    
    async def search_sri_lankan_channels(self, query: str = "", max_results: int = 50) -> List[ChannelResponse]:
        """Search for Sri Lankan channels using various strategies.
        
        Args:
            query: Additional search query
            max_results: Maximum number of channels to return
            
        Returns:
            List of ChannelResponse objects
            
        Raises:
            YouTubeAPIError: If request fails
        """
        sri_lankan_keywords = [
            "sri lanka", "srilanka", "colombo", "kandy", "galle",
            "sinhala", "tamil", "ceylon", "lanka"
        ]
        
        all_channels = []
        seen_channel_ids = set()
        
        # Search with different keyword combinations
        for keyword in sri_lankan_keywords:
            if len(all_channels) >= max_results:
                break
            
            search_query = f"{keyword} {query}".strip()
            
            try:
                # Search for channels
                params = {
                    'part': 'snippet',
                    'type': 'channel',
                    'q': search_query,
                    'maxResults': min(25, max_results - len(all_channels)),
                    'regionCode': 'LK',
                    'relevanceLanguage': 'en'
                }
                
                search_response = await self._make_request(APIEndpoint.SEARCH_LIST, params, SearchResponse)
                
                # Extract channel IDs
                channel_ids = []
                for item in search_response.items:
                    if item.id.channel_id and item.id.channel_id not in seen_channel_ids:
                        channel_ids.append(item.id.channel_id)
                        seen_channel_ids.add(item.id.channel_id)
                
                # Get full channel details
                if channel_ids:
                    channels = await self.get_channels(channel_ids)
                    
                    # Filter for Sri Lankan channels
                    for channel in channels:
                        if channel.snippet.is_sri_lankan:
                            all_channels.append(channel)
                
            except Exception as e:
                logger.warning(f"Failed to search with keyword '{keyword}': {e}")
                continue
        
        return all_channels[:max_results]
    
    def get_quota_summary(self) -> Dict[str, Any]:
        """Get quota usage summary.
        
        Returns:
            Dictionary with quota usage information
        """
        return self.quota_manager.get_quota_summary()
    
    def estimate_operation_cost(self, operation: str, **kwargs) -> int:
        """Estimate quota cost for an operation.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Estimated quota cost
        """
        return self.quota_manager.estimate_quota_cost(operation, **kwargs)
    
    def can_afford_operation(self, operation: str, **kwargs) -> tuple[bool, int]:
        """Check if we can afford an operation.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Tuple of (can_afford, estimated_cost)
        """
        return self.quota_manager.can_afford_operation(operation, **kwargs)


# Synchronous wrapper for backward compatibility
class YouTubeAPIClientSync:
    """Synchronous wrapper for YouTubeAPIClient."""
    
    def __init__(self, api_keys: Dict[str, str], quota_storage_path: Optional[str] = None,
                 timeout: int = 30, max_retries: int = 3):
        """Initialize synchronous YouTube API client.
        
        Args:
            api_keys: Dictionary of {key_name: api_key}
            quota_storage_path: Path to store quota usage data
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_keys = api_keys
        self.quota_storage_path = quota_storage_path
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = None
    
    def _get_client(self) -> YouTubeAPIClient:
        """Get or create async client."""
        if self._client is None:
            self._client = YouTubeAPIClient(
                self.api_keys, self.quota_storage_path, 
                self.timeout, self.max_retries
            )
        return self._client
    
    def get_video(self, video_id: str, parts: List[str] = None) -> VideoResponse:
        """Get information about a single video (synchronous).
        
        Args:
            video_id: YouTube video ID
            parts: List of parts to retrieve
            
        Returns:
            VideoResponse object
        """
        async def _get_video():
            async with self._get_client() as client:
                return await client.get_video(video_id, parts)
        
        return asyncio.run(_get_video())
    
    def get_videos(self, video_ids: List[str], parts: List[str] = None) -> List[VideoResponse]:
        """Get information about multiple videos (synchronous).
        
        Args:
            video_ids: List of YouTube video IDs
            parts: List of parts to retrieve
            
        Returns:
            List of VideoResponse objects
        """
        async def _get_videos():
            async with self._get_client() as client:
                return await client.get_videos(video_ids, parts)
        
        return asyncio.run(_get_videos())
    
    def get_channel(self, channel_id: str, parts: List[str] = None) -> ChannelResponse:
        """Get information about a single channel (synchronous).
        
        Args:
            channel_id: YouTube channel ID
            parts: List of parts to retrieve
            
        Returns:
            ChannelResponse object
        """
        async def _get_channel():
            async with self._get_client() as client:
                return await client.get_channel(channel_id, parts)
        
        return asyncio.run(_get_channel())
    
    def get_channels(self, channel_ids: List[str], parts: List[str] = None) -> List[ChannelResponse]:
        """Get information about multiple channels (synchronous).
        
        Args:
            channel_ids: List of YouTube channel IDs
            parts: List of parts to retrieve
            
        Returns:
            List of ChannelResponse objects
        """
        async def _get_channels():
            async with self._get_client() as client:
                return await client.get_channels(channel_ids, parts)
        
        return asyncio.run(_get_channels())
    
    def search_videos(self, query: str, max_results: int = 50, 
                     published_after: Optional[datetime] = None,
                     published_before: Optional[datetime] = None,
                     region_code: str = 'LK',
                     relevance_language: str = 'en') -> SearchResponse:
        """Search for videos (synchronous).
        
        Args:
            query: Search query
            max_results: Maximum number of results
            published_after: Only return videos published after this date
            published_before: Only return videos published before this date
            region_code: Region code for localized results
            relevance_language: Language for relevance ranking
            
        Returns:
            SearchResponse object
        """
        async def _search_videos():
            async with self._get_client() as client:
                return await client.search_videos(
                    query, max_results, published_after, 
                    published_before, region_code, relevance_language
                )
        
        return asyncio.run(_search_videos())
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50,
                          published_after: Optional[datetime] = None) -> List[VideoResponse]:
        """Get videos from a channel (synchronous).
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            published_after: Only return videos published after this date
            
        Returns:
            List of VideoResponse objects
        """
        async def _get_channel_videos():
            async with self._get_client() as client:
                return await client.get_channel_videos(channel_id, max_results, published_after)
        
        return asyncio.run(_get_channel_videos())
    
    def search_sri_lankan_channels(self, query: str = "", max_results: int = 50) -> List[ChannelResponse]:
        """Search for Sri Lankan channels (synchronous).
        
        Args:
            query: Additional search query
            max_results: Maximum number of channels to return
            
        Returns:
            List of ChannelResponse objects
        """
        async def _search_sri_lankan_channels():
            async with self._get_client() as client:
                return await client.search_sri_lankan_channels(query, max_results)
        
        return asyncio.run(_search_sri_lankan_channels())
    
    def get_quota_summary(self) -> Dict[str, Any]:
        """Get quota usage summary.
        
        Returns:
            Dictionary with quota usage information
        """
        return self._get_client().get_quota_summary()
    
    def estimate_operation_cost(self, operation: str, **kwargs) -> int:
        """Estimate quota cost for an operation.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Estimated quota cost
        """
        return self._get_client().estimate_operation_cost(operation, **kwargs)
    
    def can_afford_operation(self, operation: str, **kwargs) -> tuple[bool, int]:
        """Check if we can afford an operation.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Tuple of (can_afford, estimated_cost)
        """
        return self._get_client().can_afford_operation(operation, **kwargs)
