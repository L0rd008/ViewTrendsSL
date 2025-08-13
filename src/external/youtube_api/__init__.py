"""YouTube API integration package for ViewTrendsSL.

This package provides a comprehensive interface to the YouTube Data API v3,
optimized for Sri Lankan content analysis and viewership forecasting.

Features:
- Intelligent quota management across multiple API keys
- Automatic retry logic with exponential backoff
- Sri Lankan content detection and filtering
- Comprehensive error handling and logging
- Both async and sync client interfaces
- Pydantic models for type safety and validation
"""

from .client import YouTubeAPIClient, YouTubeAPIClientSync
from .exceptions import (
    YouTubeAPIError,
    QuotaExceededError,
    AuthenticationError,
    VideoNotFoundError,
    ChannelNotFoundError,
    RateLimitError,
    InvalidRequestError,
    NetworkError,
    parse_youtube_api_error,
    is_retryable_error,
    get_retry_delay
)
from .quota_manager import QuotaManager, QuotaMonitor, APIEndpoint, APIKeyInfo
from .models import (
    # Video models
    VideoResponse,
    VideoSnippet,
    VideoStatistics,
    VideoContentDetails,
    VideoThumbnail,
    VideoThumbnails,
    
    # Channel models
    ChannelResponse,
    ChannelSnippet,
    ChannelStatistics,
    ChannelContentDetails,
    
    # Search models
    SearchResponse,
    SearchResult,
    SearchResultSnippet,
    SearchResultId,
    
    # Playlist models
    PlaylistItemsResponse,
    PlaylistItem,
    PlaylistItemSnippet,
    
    # Batch response models
    BatchVideoResponse,
    BatchChannelResponse,
    
    # Utility functions
    extract_video_id_from_url,
    extract_channel_id_from_url,
    validate_video_id,
    validate_channel_id
)

__all__ = [
    # Client classes
    'YouTubeAPIClient',
    'YouTubeAPIClientSync',
    
    # Exception classes
    'YouTubeAPIError',
    'QuotaExceededError',
    'AuthenticationError',
    'VideoNotFoundError',
    'ChannelNotFoundError',
    'RateLimitError',
    'InvalidRequestError',
    'NetworkError',
    'parse_youtube_api_error',
    'is_retryable_error',
    'get_retry_delay',
    
    # Quota management
    'QuotaManager',
    'QuotaMonitor',
    'APIEndpoint',
    'APIKeyInfo',
    
    # Video models
    'VideoResponse',
    'VideoSnippet',
    'VideoStatistics',
    'VideoContentDetails',
    'VideoThumbnail',
    'VideoThumbnails',
    
    # Channel models
    'ChannelResponse',
    'ChannelSnippet',
    'ChannelStatistics',
    'ChannelContentDetails',
    
    # Search models
    'SearchResponse',
    'SearchResult',
    'SearchResultSnippet',
    'SearchResultId',
    
    # Playlist models
    'PlaylistItemsResponse',
    'PlaylistItem',
    'PlaylistItemSnippet',
    
    # Batch response models
    'BatchVideoResponse',
    'BatchChannelResponse',
    
    # Utility functions
    'extract_video_id_from_url',
    'extract_channel_id_from_url',
    'validate_video_id',
    'validate_channel_id'
]

__version__ = "1.0.0"
__author__ = "ViewTrendsSL Team"
__description__ = "Enhanced YouTube API client for Sri Lankan content analysis"

# Package-level configuration
import logging

# Set up logging for the package
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Default configuration
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_QUOTA_STORAGE_PATH = "data/quota_usage.json"

def create_client(api_keys: dict, **kwargs) -> YouTubeAPIClient:
    """Create a YouTube API client with default configuration.
    
    Args:
        api_keys: Dictionary of {key_name: api_key}
        **kwargs: Additional client configuration
        
    Returns:
        Configured YouTubeAPIClient instance
    """
    return YouTubeAPIClient(
        api_keys=api_keys,
        quota_storage_path=kwargs.get('quota_storage_path', DEFAULT_QUOTA_STORAGE_PATH),
        timeout=kwargs.get('timeout', DEFAULT_TIMEOUT),
        max_retries=kwargs.get('max_retries', DEFAULT_MAX_RETRIES)
    )

def create_sync_client(api_keys: dict, **kwargs) -> YouTubeAPIClientSync:
    """Create a synchronous YouTube API client with default configuration.
    
    Args:
        api_keys: Dictionary of {key_name: api_key}
        **kwargs: Additional client configuration
        
    Returns:
        Configured YouTubeAPIClientSync instance
    """
    return YouTubeAPIClientSync(
        api_keys=api_keys,
        quota_storage_path=kwargs.get('quota_storage_path', DEFAULT_QUOTA_STORAGE_PATH),
        timeout=kwargs.get('timeout', DEFAULT_TIMEOUT),
        max_retries=kwargs.get('max_retries', DEFAULT_MAX_RETRIES)
    )

# Add convenience functions to __all__
__all__.extend(['create_client', 'create_sync_client'])
