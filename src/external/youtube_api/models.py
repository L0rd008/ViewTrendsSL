"""Pydantic models for YouTube API responses."""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator, root_validator
import re
from urllib.parse import parse_qs, urlparse


class VideoThumbnail(BaseModel):
    """YouTube video thumbnail information."""
    url: str
    width: Optional[int] = None
    height: Optional[int] = None


class VideoThumbnails(BaseModel):
    """Collection of video thumbnails in different sizes."""
    default: Optional[VideoThumbnail] = None
    medium: Optional[VideoThumbnail] = None
    high: Optional[VideoThumbnail] = None
    standard: Optional[VideoThumbnail] = None
    maxres: Optional[VideoThumbnail] = None


class VideoSnippet(BaseModel):
    """YouTube video snippet information."""
    published_at: datetime = Field(alias='publishedAt')
    channel_id: str = Field(alias='channelId')
    title: str
    description: str
    thumbnails: VideoThumbnails
    channel_title: str = Field(alias='channelTitle')
    tags: Optional[List[str]] = None
    category_id: str = Field(alias='categoryId')
    live_broadcast_content: Optional[str] = Field(alias='liveBroadcastContent', default=None)
    default_language: Optional[str] = Field(alias='defaultLanguage', default=None)
    default_audio_language: Optional[str] = Field(alias='defaultAudioLanguage', default=None)
    
    # Computed fields
    title_length: Optional[int] = None
    description_length: Optional[int] = None
    tag_count: Optional[int] = None
    has_sinhala_text: Optional[bool] = None
    has_tamil_text: Optional[bool] = None
    
    @validator('published_at', pre=True)
    def parse_published_at(cls, v):
        """Parse published_at from string to datetime."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
    
    @root_validator
    def compute_derived_fields(cls, values):
        """Compute derived fields from the snippet data."""
        title = values.get('title', '')
        description = values.get('description', '')
        tags = values.get('tags', [])
        
        # Compute lengths
        values['title_length'] = len(title) if title else 0
        values['description_length'] = len(description) if description else 0
        values['tag_count'] = len(tags) if tags else 0
        
        # Detect Sri Lankan languages (basic detection)
        combined_text = f"{title} {description}".lower()
        
        # Simple Sinhala detection (Unicode range)
        sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]')
        values['has_sinhala_text'] = bool(sinhala_pattern.search(combined_text))
        
        # Simple Tamil detection (Unicode range)
        tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
        values['has_tamil_text'] = bool(tamil_pattern.search(combined_text))
        
        return values


class VideoStatistics(BaseModel):
    """YouTube video statistics."""
    view_count: int = Field(alias='viewCount', default=0)
    like_count: Optional[int] = Field(alias='likeCount', default=None)
    comment_count: Optional[int] = Field(alias='commentCount', default=None)
    
    # Computed fields
    engagement_rate: Optional[float] = None
    likes_per_view: Optional[float] = None
    comments_per_view: Optional[float] = None
    
    @validator('view_count', 'like_count', 'comment_count', pre=True)
    def parse_counts(cls, v):
        """Parse count fields from string to int."""
        if v is None:
            return None
        if isinstance(v, str):
            return int(v) if v.isdigit() else 0
        return v
    
    @root_validator
    def compute_engagement_metrics(cls, values):
        """Compute engagement metrics."""
        view_count = values.get('view_count', 0)
        like_count = values.get('like_count', 0) or 0
        comment_count = values.get('comment_count', 0) or 0
        
        if view_count > 0:
            total_engagement = like_count + comment_count
            values['engagement_rate'] = total_engagement / view_count
            values['likes_per_view'] = like_count / view_count
            values['comments_per_view'] = comment_count / view_count
        else:
            values['engagement_rate'] = 0.0
            values['likes_per_view'] = 0.0
            values['comments_per_view'] = 0.0
        
        return values


class VideoContentDetails(BaseModel):
    """YouTube video content details."""
    duration: str
    dimension: Optional[str] = None
    definition: Optional[str] = None
    caption: Optional[str] = None
    licensed_content: Optional[bool] = Field(alias='licensedContent', default=None)
    
    # Computed fields
    duration_seconds: Optional[int] = None
    is_short: Optional[bool] = None
    
    @root_validator
    def parse_duration(cls, values):
        """Parse ISO 8601 duration to seconds and determine if it's a Short."""
        duration_str = values.get('duration', '')
        
        if duration_str:
            # Parse ISO 8601 duration (e.g., PT1M30S)
            duration_seconds = cls._parse_iso_duration(duration_str)
            values['duration_seconds'] = duration_seconds
            
            # Determine if it's a YouTube Short (≤ 60 seconds)
            values['is_short'] = duration_seconds <= 60 if duration_seconds else False
        else:
            values['duration_seconds'] = None
            values['is_short'] = None
        
        return values
    
    @staticmethod
    def _parse_iso_duration(duration: str) -> Optional[int]:
        """Parse ISO 8601 duration string to seconds."""
        if not duration.startswith('PT'):
            return None
        
        # Remove PT prefix
        duration = duration[2:]
        
        # Extract hours, minutes, seconds
        hours = 0
        minutes = 0
        seconds = 0
        
        # Hours
        if 'H' in duration:
            hours_str, duration = duration.split('H', 1)
            hours = int(hours_str) if hours_str else 0
        
        # Minutes
        if 'M' in duration:
            minutes_str, duration = duration.split('M', 1)
            minutes = int(minutes_str) if minutes_str else 0
        
        # Seconds
        if 'S' in duration:
            seconds_str = duration.split('S')[0]
            seconds = int(seconds_str) if seconds_str else 0
        
        return hours * 3600 + minutes * 60 + seconds


class VideoResponse(BaseModel):
    """Complete YouTube video response."""
    kind: str
    etag: str
    id: str
    snippet: VideoSnippet
    statistics: Optional[VideoStatistics] = None
    content_details: Optional[VideoContentDetails] = Field(alias='contentDetails', default=None)
    
    # Computed fields
    sri_lankan_relevance_score: Optional[float] = None
    content_category: Optional[str] = None
    
    @root_validator
    def compute_relevance_score(cls, values):
        """Compute Sri Lankan relevance score."""
        snippet = values.get('snippet')
        if not snippet:
            values['sri_lankan_relevance_score'] = 0.0
            return values
        
        score = 0.0
        
        # Language indicators
        if snippet.has_sinhala_text:
            score += 0.4
        if snippet.has_tamil_text:
            score += 0.3
        
        # Sri Lankan keywords in title/description
        sri_lankan_keywords = [
            'sri lanka', 'srilanka', 'colombo', 'kandy', 'galle', 'jaffna',
            'sinhala', 'tamil', 'lk', 'ceylon', 'lanka'
        ]
        
        combined_text = f"{snippet.title} {snippet.description}".lower()
        keyword_matches = sum(1 for keyword in sri_lankan_keywords if keyword in combined_text)
        score += min(keyword_matches * 0.1, 0.3)
        
        values['sri_lankan_relevance_score'] = min(score, 1.0)
        return values


class ChannelSnippet(BaseModel):
    """YouTube channel snippet information."""
    title: str
    description: str
    custom_url: Optional[str] = Field(alias='customUrl', default=None)
    published_at: datetime = Field(alias='publishedAt')
    thumbnails: VideoThumbnails
    default_language: Optional[str] = Field(alias='defaultLanguage', default=None)
    country: Optional[str] = None
    
    # Computed fields
    is_sri_lankan: Optional[bool] = None
    
    @validator('published_at', pre=True)
    def parse_published_at(cls, v):
        """Parse published_at from string to datetime."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
    
    @root_validator
    def detect_sri_lankan_channel(cls, values):
        """Detect if this is a Sri Lankan channel."""
        country = values.get('country')
        title = values.get('title', '').lower()
        description = values.get('description', '').lower()
        
        # Direct country indicator
        if country == 'LK':
            values['is_sri_lankan'] = True
            return values
        
        # Language detection
        combined_text = f"{title} {description}"
        sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]')
        tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
        
        has_sinhala = bool(sinhala_pattern.search(combined_text))
        has_tamil = bool(tamil_pattern.search(combined_text))
        
        # Sri Lankan keywords
        sri_lankan_indicators = [
            'sri lanka', 'srilanka', 'colombo', 'kandy', 'galle',
            'sinhala', 'tamil', 'ceylon', 'lanka'
        ]
        
        keyword_matches = sum(1 for indicator in sri_lankan_indicators 
                            if indicator in combined_text)
        
        # Scoring logic
        score = 0
        if has_sinhala or has_tamil:
            score += 2
        score += keyword_matches
        
        values['is_sri_lankan'] = score >= 2
        return values


class ChannelStatistics(BaseModel):
    """YouTube channel statistics."""
    view_count: int = Field(alias='viewCount', default=0)
    subscriber_count: int = Field(alias='subscriberCount', default=0)
    hidden_subscriber_count: bool = Field(alias='hiddenSubscriberCount', default=False)
    video_count: int = Field(alias='videoCount', default=0)
    
    # Computed fields
    avg_views_per_video: Optional[float] = None
    
    @validator('view_count', 'subscriber_count', 'video_count', pre=True)
    def parse_counts(cls, v):
        """Parse count fields from string to int."""
        if isinstance(v, str):
            return int(v) if v.isdigit() else 0
        return v
    
    @root_validator
    def compute_averages(cls, values):
        """Compute average metrics."""
        view_count = values.get('view_count', 0)
        video_count = values.get('video_count', 0)
        
        if video_count > 0:
            values['avg_views_per_video'] = view_count / video_count
        else:
            values['avg_views_per_video'] = 0.0
        
        return values


class ChannelContentDetails(BaseModel):
    """YouTube channel content details."""
    related_playlists: Dict[str, str] = Field(alias='relatedPlaylists')
    
    @property
    def uploads_playlist_id(self) -> Optional[str]:
        """Get the uploads playlist ID."""
        return self.related_playlists.get('uploads')


class ChannelResponse(BaseModel):
    """Complete YouTube channel response."""
    kind: str
    etag: str
    id: str
    snippet: ChannelSnippet
    statistics: Optional[ChannelStatistics] = None
    content_details: Optional[ChannelContentDetails] = Field(alias='contentDetails', default=None)
    
    # Computed fields
    channel_quality_score: Optional[float] = None
    
    @root_validator
    def compute_quality_score(cls, values):
        """Compute channel quality score."""
        snippet = values.get('snippet')
        statistics = values.get('statistics')
        
        if not snippet or not statistics:
            values['channel_quality_score'] = 0.0
            return values
        
        score = 0.0
        
        # Subscriber count factor (normalized)
        if statistics.subscriber_count > 0:
            # Log scale for subscribers (max score 0.3)
            import math
            subscriber_score = min(math.log10(statistics.subscriber_count) / 7, 0.3)
            score += subscriber_score
        
        # Video count factor
        if statistics.video_count > 0:
            video_score = min(statistics.video_count / 1000, 0.2)
            score += video_score
        
        # Engagement factor
        if statistics.avg_views_per_video and statistics.avg_views_per_video > 0:
            # Normalized engagement score
            engagement_score = min(statistics.avg_views_per_video / 100000, 0.3)
            score += engagement_score
        
        # Content completeness
        if snippet.description:
            score += 0.1
        if snippet.custom_url:
            score += 0.1
        
        values['channel_quality_score'] = min(score, 1.0)
        return values


class SearchResultSnippet(BaseModel):
    """YouTube search result snippet."""
    published_at: datetime = Field(alias='publishedAt')
    channel_id: str = Field(alias='channelId')
    title: str
    description: str
    thumbnails: VideoThumbnails
    channel_title: str = Field(alias='channelTitle')
    live_broadcast_content: Optional[str] = Field(alias='liveBroadcastContent', default=None)
    
    @validator('published_at', pre=True)
    def parse_published_at(cls, v):
        """Parse published_at from string to datetime."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v


class SearchResultId(BaseModel):
    """YouTube search result ID."""
    kind: str
    video_id: Optional[str] = Field(alias='videoId', default=None)
    channel_id: Optional[str] = Field(alias='channelId', default=None)
    playlist_id: Optional[str] = Field(alias='playlistId', default=None)


class SearchResult(BaseModel):
    """Individual YouTube search result."""
    kind: str
    etag: str
    id: SearchResultId
    snippet: SearchResultSnippet


class SearchResponse(BaseModel):
    """YouTube search API response."""
    kind: str
    etag: str
    next_page_token: Optional[str] = Field(alias='nextPageToken', default=None)
    prev_page_token: Optional[str] = Field(alias='prevPageToken', default=None)
    region_code: Optional[str] = Field(alias='regionCode', default=None)
    page_info: Dict[str, int] = Field(alias='pageInfo')
    items: List[SearchResult]
    
    @property
    def total_results(self) -> int:
        """Get total number of results."""
        return self.page_info.get('totalResults', 0)
    
    @property
    def results_per_page(self) -> int:
        """Get results per page."""
        return self.page_info.get('resultsPerPage', 0)


class PlaylistItemSnippet(BaseModel):
    """YouTube playlist item snippet."""
    published_at: datetime = Field(alias='publishedAt')
    channel_id: str = Field(alias='channelId')
    title: str
    description: str
    thumbnails: VideoThumbnails
    channel_title: str = Field(alias='channelTitle')
    playlist_id: str = Field(alias='playlistId')
    position: int
    resource_id: Dict[str, str] = Field(alias='resourceId')
    
    @validator('published_at', pre=True)
    def parse_published_at(cls, v):
        """Parse published_at from string to datetime."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
    
    @property
    def video_id(self) -> Optional[str]:
        """Get video ID from resource ID."""
        return self.resource_id.get('videoId')


class PlaylistItem(BaseModel):
    """YouTube playlist item."""
    kind: str
    etag: str
    id: str
    snippet: PlaylistItemSnippet


class PlaylistItemsResponse(BaseModel):
    """YouTube playlist items API response."""
    kind: str
    etag: str
    next_page_token: Optional[str] = Field(alias='nextPageToken', default=None)
    prev_page_token: Optional[str] = Field(alias='prevPageToken', default=None)
    page_info: Dict[str, int] = Field(alias='pageInfo')
    items: List[PlaylistItem]


class BatchVideoResponse(BaseModel):
    """Batch response for multiple videos."""
    kind: str
    etag: str
    page_info: Dict[str, int] = Field(alias='pageInfo')
    items: List[VideoResponse]


class BatchChannelResponse(BaseModel):
    """Batch response for multiple channels."""
    kind: str
    etag: str
    page_info: Dict[str, int] = Field(alias='pageInfo')
    items: List[ChannelResponse]


def extract_video_id_from_url(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats.
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID if found, None otherwise
    """
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If it's already just a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    return None


def extract_channel_id_from_url(url: str) -> Optional[str]:
    """Extract channel ID from various YouTube channel URL formats.
    
    Args:
        url: YouTube channel URL
        
    Returns:
        Channel ID if found, None otherwise
    """
    # Channel ID pattern
    channel_id_match = re.search(r'youtube\.com/channel/([a-zA-Z0-9_-]+)', url)
    if channel_id_match:
        return channel_id_match.group(1)
    
    # If it's already just a channel ID
    if re.match(r'^UC[a-zA-Z0-9_-]{22}$', url):
        return url
    
    return None


def validate_video_id(video_id: str) -> bool:
    """Validate YouTube video ID format.
    
    Args:
        video_id: Video ID to validate
        
    Returns:
        True if valid format
    """
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))


def validate_channel_id(channel_id: str) -> bool:
    """Validate YouTube channel ID format.
    
    Args:
        channel_id: Channel ID to validate
        
    Returns:
        True if valid format
    """
    return bool(re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id))
