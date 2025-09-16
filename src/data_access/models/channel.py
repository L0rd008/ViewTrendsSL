"""Channel model for YouTube channel data."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List, Dict, Any

from . import BaseModel


class Channel(BaseModel):
    """YouTube Channel model for storing channel metadata and statistics.
    
    This model stores information about YouTube channels that are being tracked
    for viewership analysis, including channel statistics, metadata, and
    Sri Lankan relevance indicators.
    """
    
    __tablename__ = 'channels'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # YouTube channel identifiers
    channel_id = Column(String(50), unique=True, nullable=False, index=True)
    channel_handle = Column(String(100), nullable=True, index=True)  # @channelname
    custom_url = Column(String(100), nullable=True)  # youtube.com/c/customname
    
    # Basic channel information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Channel statistics (updated periodically)
    subscriber_count = Column(BigInteger, nullable=True, default=0)
    video_count = Column(Integer, nullable=True, default=0)
    view_count = Column(BigInteger, nullable=True, default=0)
    
    # Channel metadata
    published_at = Column(DateTime, nullable=True)  # Channel creation date
    country = Column(String(10), nullable=True)  # ISO country code
    default_language = Column(String(10), nullable=True)  # ISO language code
    
    # Channel branding
    thumbnail_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    
    # Sri Lankan relevance indicators
    is_sri_lankan = Column(Boolean, nullable=False, default=False)
    sri_lankan_confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    language_detected = Column(String(50), nullable=True)  # Detected primary language
    
    # Channel categorization
    primary_category = Column(String(50), nullable=True)  # News, Entertainment, Education, etc.
    secondary_categories = Column(Text, nullable=True)  # JSON array of additional categories
    
    # Tracking metadata
    is_active = Column(Boolean, nullable=False, default=True)
    last_video_check = Column(DateTime, nullable=True)
    last_stats_update = Column(DateTime, nullable=True)
    
    # Data quality indicators
    data_quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    has_sufficient_data = Column(Boolean, nullable=False, default=False)
    
    # Monitoring settings
    is_monitored = Column(Boolean, nullable=False, default=True)
    monitoring_priority = Column(Integer, nullable=False, default=1)  # 1=high, 2=medium, 3=low
    
    # Performance metrics (calculated periodically)
    avg_views_per_video = Column(Float, nullable=True)
    avg_engagement_rate = Column(Float, nullable=True)  # (likes + comments) / views
    upload_frequency_days = Column(Float, nullable=True)  # Average days between uploads
    
    # Relationships
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
    
    def __init__(self, channel_id: str, title: str, **kwargs):
        """Initialize a new channel with required fields."""
        super().__init__(**kwargs)
        self.channel_id = channel_id
        self.title = title
        self.last_stats_update = datetime.utcnow()
    
    def update_statistics(self, subscriber_count: int, video_count: int, view_count: int) -> None:
        """Update channel statistics."""
        self.subscriber_count = subscriber_count
        self.video_count = video_count
        self.view_count = view_count
        self.last_stats_update = datetime.utcnow()
        
        # Calculate average views per video
        if video_count > 0:
            self.avg_views_per_video = view_count / video_count
    
    def calculate_sri_lankan_confidence(self, 
                                      country_weight: float = 0.4,
                                      language_weight: float = 0.3,
                                      keyword_weight: float = 0.3) -> float:
        """Calculate confidence score for Sri Lankan relevance.
        
        Args:
            country_weight: Weight for country indicator
            language_weight: Weight for language indicator  
            keyword_weight: Weight for keyword/content indicator
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        score = 0.0
        
        # Country indicator
        if self.country == 'LK':
            score += country_weight
        
        # Language indicator
        if self.language_detected in ['si', 'ta', 'sinhala', 'tamil']:
            score += language_weight
        elif self.default_language in ['si', 'ta']:
            score += language_weight * 0.8
        
        # Keyword/content indicator (simplified - would need more sophisticated analysis)
        sri_lankan_keywords = ['sri lanka', 'colombo', 'kandy', 'galle', 'sinhala', 'tamil']
        title_lower = self.title.lower()
        desc_lower = (self.description or '').lower()
        
        keyword_matches = sum(1 for keyword in sri_lankan_keywords 
                            if keyword in title_lower or keyword in desc_lower)
        
        if keyword_matches > 0:
            score += keyword_weight * min(keyword_matches / len(sri_lankan_keywords), 1.0)
        
        self.sri_lankan_confidence_score = min(score, 1.0)
        return self.sri_lankan_confidence_score
    
    def update_data_quality_score(self) -> float:
        """Calculate and update data quality score based on available information."""
        score = 0.0
        max_score = 10.0
        
        # Basic information completeness
        if self.title: score += 1.0
        if self.description: score += 1.0
        if self.published_at: score += 1.0
        if self.country: score += 1.0
        if self.thumbnail_url: score += 1.0
        
        # Statistics availability
        if self.subscriber_count is not None and self.subscriber_count > 0: score += 1.0
        if self.video_count is not None and self.video_count > 0: score += 1.0
        if self.view_count is not None and self.view_count > 0: score += 1.0
        
        # Recent data updates
        if self.last_stats_update:
            days_since_update = (datetime.utcnow() - self.last_stats_update).days
            if days_since_update <= 7: score += 1.0
            elif days_since_update <= 30: score += 0.5
        
        # Sufficient video data
        if self.video_count and self.video_count >= 10: score += 1.0
        
        self.data_quality_score = score / max_score
        self.has_sufficient_data = self.data_quality_score >= 0.6
        
        return self.data_quality_score
    
    def get_category_list(self) -> List[str]:
        """Get list of all categories (primary + secondary)."""
        categories = []
        if self.primary_category:
            categories.append(self.primary_category)
        
        if self.secondary_categories:
            try:
                import json
                secondary = json.loads(self.secondary_categories)
                if isinstance(secondary, list):
                    categories.extend(secondary)
            except (json.JSONDecodeError, TypeError):
                pass
        
        return categories
    
    def set_secondary_categories(self, categories: List[str]) -> None:
        """Set secondary categories as JSON array."""
        import json
        self.secondary_categories = json.dumps(categories) if categories else None
    
    def is_high_quality_channel(self) -> bool:
        """Check if this is a high-quality channel worth monitoring."""
        return (
            self.data_quality_score and self.data_quality_score >= 0.7 and
            self.subscriber_count and self.subscriber_count >= 1000 and
            self.video_count and self.video_count >= 5 and
            self.is_active
        )
    
    def get_engagement_tier(self) -> str:
        """Get engagement tier based on subscriber count."""
        if not self.subscriber_count:
            return 'unknown'
        elif self.subscriber_count >= 1000000:
            return 'mega'
        elif self.subscriber_count >= 100000:
            return 'large'
        elif self.subscriber_count >= 10000:
            return 'medium'
        elif self.subscriber_count >= 1000:
            return 'small'
        else:
            return 'micro'
    
    def to_dict(self, include_stats: bool = True) -> Dict[str, Any]:
        """Convert channel to dictionary."""
        data = {
            'id': self.id,
            'channel_id': self.channel_id,
            'channel_handle': self.channel_handle,
            'custom_url': self.custom_url,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'country': self.country,
            'default_language': self.default_language,
            'thumbnail_url': self.thumbnail_url,
            'banner_url': self.banner_url,
            'is_sri_lankan': self.is_sri_lankan,
            'sri_lankan_confidence_score': self.sri_lankan_confidence_score,
            'language_detected': self.language_detected,
            'primary_category': self.primary_category,
            'categories': self.get_category_list(),
            'is_active': self.is_active,
            'is_monitored': self.is_monitored,
            'monitoring_priority': self.monitoring_priority,
            'data_quality_score': self.data_quality_score,
            'has_sufficient_data': self.has_sufficient_data,
            'engagement_tier': self.get_engagement_tier(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_stats:
            data.update({
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count,
                'avg_views_per_video': self.avg_views_per_video,
                'avg_engagement_rate': self.avg_engagement_rate,
                'upload_frequency_days': self.upload_frequency_days,
                'last_video_check': self.last_video_check.isoformat() if self.last_video_check else None,
                'last_stats_update': self.last_stats_update.isoformat() if self.last_stats_update else None,
            })
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the channel."""
        return f"<Channel(id={self.id}, channel_id='{self.channel_id}', title='{self.title[:50]}...')>"
