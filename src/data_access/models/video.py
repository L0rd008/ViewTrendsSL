"""Video model for YouTube video data."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
import re

from . import BaseModel


class Video(BaseModel):
    """YouTube Video model for storing video metadata and statistics.
    
    This model stores information about individual YouTube videos including
    metadata, statistics, and features used for viewership prediction.
    """
    
    __tablename__ = 'videos'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # YouTube video identifiers
    video_id = Column(String(20), unique=True, nullable=False, index=True)
    
    # Foreign key to channel
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False, index=True)
    
    # Basic video information
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    
    # Video metadata
    published_at = Column(DateTime, nullable=False, index=True)
    duration_seconds = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=True)  # YouTube category ID
    category_name = Column(String(50), nullable=True)  # Human-readable category
    
    # Video type classification
    is_short = Column(Boolean, nullable=False, default=False, index=True)
    is_live = Column(Boolean, nullable=False, default=False)
    is_premiere = Column(Boolean, nullable=False, default=False)
    
    # Video content features
    thumbnail_url = Column(String(500), nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    default_language = Column(String(10), nullable=True)
    
    # Current statistics (most recent snapshot)
    view_count = Column(BigInteger, nullable=True, default=0, index=True)
    like_count = Column(Integer, nullable=True, default=0)
    comment_count = Column(Integer, nullable=True, default=0)
    
    # Engagement metrics (calculated)
    engagement_rate = Column(Float, nullable=True)  # (likes + comments) / views
    like_to_view_ratio = Column(Float, nullable=True)
    comment_to_view_ratio = Column(Float, nullable=True)
    
    # Content analysis features
    title_length = Column(Integer, nullable=True)
    description_length = Column(Integer, nullable=True)
    tag_count = Column(Integer, nullable=True)
    
    # Language and sentiment analysis
    language_detected = Column(String(10), nullable=True)
    title_sentiment = Column(Float, nullable=True)  # -1.0 to 1.0
    description_sentiment = Column(Float, nullable=True)
    
    # Publishing time features
    publish_hour = Column(Integer, nullable=True)  # 0-23
    publish_day_of_week = Column(Integer, nullable=True)  # 0=Monday, 6=Sunday
    publish_day_of_month = Column(Integer, nullable=True)  # 1-31
    publish_month = Column(Integer, nullable=True)  # 1-12
    is_weekend = Column(Boolean, nullable=True)
    
    # Performance indicators
    views_in_first_24h = Column(BigInteger, nullable=True)
    views_in_first_week = Column(BigInteger, nullable=True)
    peak_daily_views = Column(BigInteger, nullable=True)
    days_to_peak = Column(Integer, nullable=True)
    
    # Data tracking
    last_stats_update = Column(DateTime, nullable=True)
    is_tracking_complete = Column(Boolean, nullable=False, default=False)
    tracking_end_date = Column(DateTime, nullable=True)
    
    # Quality and status
    data_quality_score = Column(Float, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_private = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    channel = relationship("Channel", back_populates="videos")
    snapshots = relationship("Snapshot", back_populates="video", cascade="all, delete-orphan")
    video_tags = relationship("VideoTag", back_populates="video", cascade="all, delete-orphan")
    
    def __init__(self, video_id: str, channel_id: int, title: str, published_at: datetime, **kwargs):
        """Initialize a new video with required fields."""
        super().__init__(**kwargs)
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.published_at = published_at
        self.last_stats_update = datetime.utcnow()
        
        # Extract publishing time features
        self._extract_time_features()
        
        # Calculate basic content features
        self._calculate_content_features()
    
    def _extract_time_features(self) -> None:
        """Extract time-based features from published_at."""
        if self.published_at:
            self.publish_hour = self.published_at.hour
            self.publish_day_of_week = self.published_at.weekday()
            self.publish_day_of_month = self.published_at.day
            self.publish_month = self.published_at.month
            self.is_weekend = self.publish_day_of_week >= 5  # Saturday=5, Sunday=6
    
    def _calculate_content_features(self) -> None:
        """Calculate content-based features."""
        if self.title:
            self.title_length = len(self.title)
        
        if self.description:
            self.description_length = len(self.description)
        
        if self.tags:
            try:
                tag_list = json.loads(self.tags) if isinstance(self.tags, str) else self.tags
                self.tag_count = len(tag_list) if isinstance(tag_list, list) else 0
            except (json.JSONDecodeError, TypeError):
                self.tag_count = 0
    
    def update_statistics(self, view_count: int, like_count: int = None, comment_count: int = None) -> None:
        """Update video statistics and calculate engagement metrics."""
        self.view_count = view_count
        if like_count is not None:
            self.like_count = like_count
        if comment_count is not None:
            self.comment_count = comment_count
        
        self.last_stats_update = datetime.utcnow()
        
        # Calculate engagement metrics
        self._calculate_engagement_metrics()
        
        # Update performance indicators based on video age
        self._update_performance_indicators()
    
    def _calculate_engagement_metrics(self) -> None:
        """Calculate engagement rate and ratios."""
        if self.view_count and self.view_count > 0:
            total_engagement = (self.like_count or 0) + (self.comment_count or 0)
            self.engagement_rate = total_engagement / self.view_count
            
            if self.like_count is not None:
                self.like_to_view_ratio = self.like_count / self.view_count
            
            if self.comment_count is not None:
                self.comment_to_view_ratio = self.comment_count / self.view_count
    
    def _update_performance_indicators(self) -> None:
        """Update performance indicators based on video age."""
        if not self.published_at:
            return
        
        now = datetime.utcnow()
        video_age = now - self.published_at
        
        # Track views in first 24 hours
        if video_age <= timedelta(hours=24) and self.views_in_first_24h is None:
            self.views_in_first_24h = self.view_count
        
        # Track views in first week
        if video_age <= timedelta(days=7) and self.views_in_first_week is None:
            self.views_in_first_week = self.view_count
        elif video_age > timedelta(days=7) and self.views_in_first_week is None:
            # Estimate first week views if we missed the window
            self.views_in_first_week = self.view_count
    
    def classify_video_type(self) -> None:
        """Classify video type based on duration and other factors."""
        if self.duration_seconds:
            # YouTube Shorts are typically <= 60 seconds
            self.is_short = self.duration_seconds <= 60
    
    def get_video_age_days(self) -> int:
        """Get video age in days."""
        if not self.published_at:
            return 0
        return (datetime.utcnow() - self.published_at).days
    
    def get_video_age_hours(self) -> float:
        """Get video age in hours."""
        if not self.published_at:
            return 0.0
        return (datetime.utcnow() - self.published_at).total_seconds() / 3600
    
    def is_viral(self, threshold_multiplier: float = 10.0) -> bool:
        """Check if video is viral based on channel's average performance."""
        if not self.channel or not self.channel.avg_views_per_video:
            return False
        
        expected_views = self.channel.avg_views_per_video
        return self.view_count >= (expected_views * threshold_multiplier)
    
    def get_performance_category(self) -> str:
        """Get performance category relative to channel average."""
        if not self.channel or not self.channel.avg_views_per_video:
            return 'unknown'
        
        ratio = self.view_count / self.channel.avg_views_per_video
        
        if ratio >= 10.0:
            return 'viral'
        elif ratio >= 2.0:
            return 'high'
        elif ratio >= 0.5:
            return 'normal'
        else:
            return 'low'
    
    def get_tag_list(self) -> List[str]:
        """Get list of video tags."""
        if not self.tags:
            return []
        
        try:
            if isinstance(self.tags, str):
                return json.loads(self.tags)
            elif isinstance(self.tags, list):
                return self.tags
        except (json.JSONDecodeError, TypeError):
            pass
        
        return []
    
    def set_tags(self, tags: List[str]) -> None:
        """Set video tags as JSON array."""
        self.tags = json.dumps(tags) if tags else None
        self.tag_count = len(tags) if tags else 0
    
    def extract_title_features(self) -> Dict[str, Any]:
        """Extract advanced features from video title."""
        if not self.title:
            return {}
        
        title = self.title.lower()
        
        features = {
            'has_question': '?' in self.title,
            'has_exclamation': '!' in self.title,
            'has_numbers': bool(re.search(r'\d', self.title)),
            'has_caps_words': bool(re.search(r'\b[A-Z]{2,}\b', self.title)),
            'word_count': len(self.title.split()),
            'char_count': len(self.title),
            'has_emoji': bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', self.title)),
        }
        
        # Common clickbait indicators
        clickbait_words = ['amazing', 'shocking', 'unbelievable', 'secret', 'trick', 'hack', 'you won\'t believe']
        features['clickbait_score'] = sum(1 for word in clickbait_words if word in title) / len(clickbait_words)
        
        return features
    
    def calculate_data_quality_score(self) -> float:
        """Calculate data quality score based on available information."""
        score = 0.0
        max_score = 10.0
        
        # Basic information
        if self.title: score += 1.0
        if self.description: score += 1.0
        if self.published_at: score += 1.0
        if self.duration_seconds: score += 1.0
        if self.category_name: score += 1.0
        
        # Statistics
        if self.view_count is not None: score += 1.0
        if self.like_count is not None: score += 1.0
        if self.comment_count is not None: score += 1.0
        
        # Recent update
        if self.last_stats_update:
            hours_since_update = (datetime.utcnow() - self.last_stats_update).total_seconds() / 3600
            if hours_since_update <= 24: score += 1.0
            elif hours_since_update <= 168: score += 0.5  # 1 week
        
        # Content features
        if self.tags and self.tag_count and self.tag_count > 0: score += 1.0
        
        self.data_quality_score = score / max_score
        return self.data_quality_score
    
    def to_dict(self, include_stats: bool = True, include_features: bool = False) -> Dict[str, Any]:
        """Convert video to dictionary."""
        data = {
            'id': self.id,
            'video_id': self.video_id,
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'duration_seconds': self.duration_seconds,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'is_short': self.is_short,
            'is_live': self.is_live,
            'is_premiere': self.is_premiere,
            'thumbnail_url': self.thumbnail_url,
            'tags': self.get_tag_list(),
            'default_language': self.default_language,
            'language_detected': self.language_detected,
            'video_age_days': self.get_video_age_days(),
            'video_age_hours': self.get_video_age_hours(),
            'performance_category': self.get_performance_category(),
            'data_quality_score': self.data_quality_score,
            'is_deleted': self.is_deleted,
            'is_private': self.is_private,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_stats:
            data.update({
                'view_count': self.view_count,
                'like_count': self.like_count,
                'comment_count': self.comment_count,
                'engagement_rate': self.engagement_rate,
                'like_to_view_ratio': self.like_to_view_ratio,
                'comment_to_view_ratio': self.comment_to_view_ratio,
                'views_in_first_24h': self.views_in_first_24h,
                'views_in_first_week': self.views_in_first_week,
                'peak_daily_views': self.peak_daily_views,
                'days_to_peak': self.days_to_peak,
                'last_stats_update': self.last_stats_update.isoformat() if self.last_stats_update else None,
            })
        
        if include_features:
            data.update({
                'title_length': self.title_length,
                'description_length': self.description_length,
                'tag_count': self.tag_count,
                'title_sentiment': self.title_sentiment,
                'description_sentiment': self.description_sentiment,
                'publish_hour': self.publish_hour,
                'publish_day_of_week': self.publish_day_of_week,
                'publish_day_of_month': self.publish_day_of_month,
                'publish_month': self.publish_month,
                'is_weekend': self.is_weekend,
                'title_features': self.extract_title_features(),
            })
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the video."""
        return f"<Video(id={self.id}, video_id='{self.video_id}', title='{self.title[:50]}...')>"
