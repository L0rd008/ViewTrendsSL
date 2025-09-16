"""Tag models for video categorization and analysis."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any, List

from . import BaseModel


class Tag(BaseModel):
    """Tag model for storing unique video tags.
    
    This model stores unique tags that can be associated with videos
    for categorization, analysis, and feature engineering.
    """
    
    __tablename__ = 'tags'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Tag information
    name = Column(String(100), unique=True, nullable=False, index=True)
    normalized_name = Column(String(100), nullable=False, index=True)  # Lowercase, trimmed
    
    # Tag metadata
    category = Column(String(50), nullable=True)  # topic, language, format, etc.
    language = Column(String(10), nullable=True)  # Language of the tag
    
    # Usage statistics
    usage_count = Column(Integer, nullable=False, default=0)
    first_used = Column(DateTime, nullable=True)
    last_used = Column(DateTime, nullable=True)
    
    # Tag analysis
    is_trending = Column(Boolean, nullable=False, default=False)
    trend_score = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # Sri Lankan relevance
    is_sri_lankan = Column(Boolean, nullable=False, default=False)
    sri_lankan_confidence = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # Performance metrics
    avg_views_per_video = Column(Float, nullable=True)
    avg_engagement_rate = Column(Float, nullable=True)
    
    # Relationships
    video_tags = relationship("VideoTag", back_populates="tag", cascade="all, delete-orphan")
    
    def __init__(self, name: str, **kwargs):
        """Initialize a new tag with name."""
        super().__init__(**kwargs)
        self.name = name.strip()
        self.normalized_name = name.lower().strip()
        self.first_used = datetime.utcnow()
        self.last_used = datetime.utcnow()
        self.usage_count = 0
    
    def increment_usage(self) -> None:
        """Increment usage count and update last used timestamp."""
        self.usage_count += 1
        self.last_used = datetime.utcnow()
    
    def calculate_sri_lankan_relevance(self) -> float:
        """Calculate Sri Lankan relevance score based on tag content."""
        name_lower = self.normalized_name
        
        # Sri Lankan keywords and phrases
        sri_lankan_indicators = {
            'direct': ['sri lanka', 'srilanka', 'lk', 'colombo', 'kandy', 'galle', 'jaffna', 'negombo'],
            'language': ['sinhala', 'tamil', 'sinhalese'],
            'culture': ['buddhist', 'temple', 'poya', 'vesak', 'avurudu', 'perahera'],
            'food': ['rice and curry', 'kottu', 'hoppers', 'string hoppers', 'pol sambol'],
            'places': ['sigiriya', 'anuradhapura', 'polonnaruwa', 'ella', 'nuwara eliya'],
        }
        
        score = 0.0
        max_score = 1.0
        
        # Check for direct matches
        for category, keywords in sri_lankan_indicators.items():
            for keyword in keywords:
                if keyword in name_lower:
                    if category == 'direct':
                        score += 0.8
                    elif category == 'language':
                        score += 0.6
                    else:
                        score += 0.4
                    break  # Only count once per category
        
        self.sri_lankan_confidence = min(score, max_score)
        self.is_sri_lankan = self.sri_lankan_confidence >= 0.5
        
        return self.sri_lankan_confidence
    
    def calculate_trend_score(self, recent_usage_count: int, total_videos: int) -> float:
        """Calculate trend score based on recent usage patterns.
        
        Args:
            recent_usage_count: Usage count in recent period (e.g., last 30 days)
            total_videos: Total videos in the same period
            
        Returns:
            Trend score between 0.0 and 1.0
        """
        if total_videos == 0:
            return 0.0
        
        # Calculate usage frequency
        usage_frequency = recent_usage_count / total_videos
        
        # Normalize to 0-1 scale (assuming max 10% usage is trending)
        self.trend_score = min(usage_frequency * 10, 1.0)
        self.is_trending = self.trend_score >= 0.1  # 1% usage threshold
        
        return self.trend_score
    
    def update_performance_metrics(self, videos_data: List[Dict[str, Any]]) -> None:
        """Update performance metrics based on associated videos.
        
        Args:
            videos_data: List of video data dictionaries with view_count and engagement_rate
        """
        if not videos_data:
            return
        
        # Calculate average views
        view_counts = [v.get('view_count', 0) for v in videos_data if v.get('view_count')]
        if view_counts:
            self.avg_views_per_video = sum(view_counts) / len(view_counts)
        
        # Calculate average engagement rate
        engagement_rates = [v.get('engagement_rate', 0) for v in videos_data if v.get('engagement_rate')]
        if engagement_rates:
            self.avg_engagement_rate = sum(engagement_rates) / len(engagement_rates)
    
    def get_performance_tier(self) -> str:
        """Get performance tier based on average views."""
        if not self.avg_views_per_video:
            return 'unknown'
        elif self.avg_views_per_video >= 1000000:
            return 'viral'
        elif self.avg_views_per_video >= 100000:
            return 'high'
        elif self.avg_views_per_video >= 10000:
            return 'medium'
        else:
            return 'low'
    
    @classmethod
    def get_or_create(cls, session, name: str) -> 'Tag':
        """Get existing tag or create new one.
        
        Args:
            session: Database session
            name: Tag name
            
        Returns:
            Tag instance
        """
        normalized = name.lower().strip()
        tag = session.query(cls).filter(cls.normalized_name == normalized).first()
        
        if not tag:
            tag = cls(name=name)
            session.add(tag)
            session.flush()  # Get the ID
        
        return tag
    
    def to_dict(self, include_stats: bool = True) -> Dict[str, Any]:
        """Convert tag to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'normalized_name': self.normalized_name,
            'category': self.category,
            'language': self.language,
            'is_sri_lankan': self.is_sri_lankan,
            'sri_lankan_confidence': self.sri_lankan_confidence,
            'is_trending': self.is_trending,
            'trend_score': self.trend_score,
            'performance_tier': self.get_performance_tier(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_stats:
            data.update({
                'usage_count': self.usage_count,
                'first_used': self.first_used.isoformat() if self.first_used else None,
                'last_used': self.last_used.isoformat() if self.last_used else None,
                'avg_views_per_video': self.avg_views_per_video,
                'avg_engagement_rate': self.avg_engagement_rate,
            })
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the tag."""
        return f"<Tag(id={self.id}, name='{self.name}', usage={self.usage_count})>"


class VideoTag(BaseModel):
    """Association model for video-tag many-to-many relationship.
    
    This model represents the relationship between videos and tags,
    allowing for additional metadata about the association.
    """
    
    __tablename__ = 'video_tags'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys
    video_id = Column(Integer, ForeignKey('videos.id'), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    
    # Association metadata
    source = Column(String(50), nullable=False, default='youtube_api')  # youtube_api, manual, auto_detected
    confidence = Column(Float, nullable=True)  # Confidence score if auto-detected
    
    # Position and relevance
    position = Column(Integer, nullable=True)  # Position in original tag list
    relevance_score = Column(Float, nullable=True)  # How relevant this tag is to the video
    
    # Relationships
    video = relationship("Video", back_populates="video_tags")
    tag = relationship("Tag", back_populates="video_tags")
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_video_tag_unique', 'video_id', 'tag_id', unique=True),
        Index('idx_tag_video', 'tag_id', 'video_id'),
    )
    
    def __init__(self, video_id: int, tag_id: int, **kwargs):
        """Initialize a new video-tag association."""
        super().__init__(**kwargs)
        self.video_id = video_id
        self.tag_id = tag_id
    
    def calculate_relevance_score(self, video_title: str, video_description: str = None) -> float:
        """Calculate how relevant this tag is to the video content.
        
        Args:
            video_title: Video title
            video_description: Video description (optional)
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        if not hasattr(self, 'tag') or not self.tag:
            return 0.0
        
        tag_name = self.tag.normalized_name
        title_lower = video_title.lower()
        desc_lower = (video_description or '').lower()
        
        score = 0.0
        
        # Exact match in title (highest relevance)
        if tag_name in title_lower:
            score += 0.8
        
        # Partial match in title
        elif any(word in title_lower for word in tag_name.split()):
            score += 0.4
        
        # Match in description
        if desc_lower and tag_name in desc_lower:
            score += 0.3
        elif desc_lower and any(word in desc_lower for word in tag_name.split()):
            score += 0.1
        
        # Position bonus (earlier tags are often more relevant)
        if self.position is not None and self.position <= 5:
            score += 0.1 * (6 - self.position) / 5
        
        self.relevance_score = min(score, 1.0)
        return self.relevance_score
    
    @classmethod
    def create_association(cls, session, video_id: int, tag_name: str, 
                          position: int = None, source: str = 'youtube_api') -> 'VideoTag':
        """Create a video-tag association.
        
        Args:
            session: Database session
            video_id: Video ID
            tag_name: Tag name
            position: Position in tag list
            source: Source of the tag
            
        Returns:
            VideoTag instance
        """
        # Get or create tag
        tag = Tag.get_or_create(session, tag_name)
        
        # Check if association already exists
        existing = session.query(cls).filter(
            cls.video_id == video_id,
            cls.tag_id == tag.id
        ).first()
        
        if existing:
            return existing
        
        # Create new association
        video_tag = cls(
            video_id=video_id,
            tag_id=tag.id,
            position=position,
            source=source
        )
        
        # Increment tag usage
        tag.increment_usage()
        
        session.add(video_tag)
        return video_tag
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert video-tag association to dictionary."""
        data = {
            'id': self.id,
            'video_id': self.video_id,
            'tag_id': self.tag_id,
            'source': self.source,
            'confidence': self.confidence,
            'position': self.position,
            'relevance_score': self.relevance_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        # Include tag information if available
        if hasattr(self, 'tag') and self.tag:
            data['tag'] = self.tag.to_dict(include_stats=False)
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the video-tag association."""
        return f"<VideoTag(id={self.id}, video_id={self.video_id}, tag_id={self.tag_id})>"
