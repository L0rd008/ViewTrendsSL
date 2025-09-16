"""Snapshot model for time-series video statistics."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from . import BaseModel


class Snapshot(BaseModel):
    """Video statistics snapshot model for time-series data.
    
    This model stores periodic snapshots of video statistics to track
    viewership growth over time, which is essential for training
    prediction models and analyzing video performance patterns.
    """
    
    __tablename__ = 'snapshots'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to video
    video_id = Column(Integer, ForeignKey('videos.id'), nullable=False, index=True)
    
    # Snapshot timestamp
    snapshot_time = Column(DateTime, nullable=False, index=True)
    
    # Video statistics at this point in time
    view_count = Column(BigInteger, nullable=False, default=0)
    like_count = Column(Integer, nullable=True, default=0)
    comment_count = Column(Integer, nullable=True, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, nullable=True)  # (likes + comments) / views
    views_since_last_snapshot = Column(BigInteger, nullable=True, default=0)
    
    # Time-based features
    hours_since_published = Column(Float, nullable=True)
    days_since_published = Column(Float, nullable=True)
    
    # Growth metrics (calculated from previous snapshot)
    view_growth_rate = Column(Float, nullable=True)  # Views per hour since last snapshot
    like_growth_rate = Column(Float, nullable=True)
    comment_growth_rate = Column(Float, nullable=True)
    
    # Snapshot metadata
    snapshot_type = Column(String(20), nullable=False, default='scheduled')  # scheduled, manual, api_trigger
    data_source = Column(String(50), nullable=True)  # youtube_api, manual_entry, etc.
    
    # Data quality indicators
    is_complete = Column(Boolean, nullable=False, default=True)
    has_anomaly = Column(Boolean, nullable=False, default=False)
    anomaly_reason = Column(String(200), nullable=True)
    
    # Relationships
    video = relationship("Video", back_populates="snapshots")
    
    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('idx_video_snapshot_time', 'video_id', 'snapshot_time'),
        Index('idx_snapshot_time_type', 'snapshot_time', 'snapshot_type'),
    )
    
    def __init__(self, video_id: int, view_count: int, snapshot_time: datetime = None, **kwargs):
        """Initialize a new snapshot with required fields."""
        super().__init__(**kwargs)
        self.video_id = video_id
        self.view_count = view_count
        self.snapshot_time = snapshot_time or datetime.utcnow()
        
        # Calculate time-based features
        self._calculate_time_features()
        
        # Calculate engagement rate if like/comment data available
        self._calculate_engagement_rate()
    
    def _calculate_time_features(self) -> None:
        """Calculate time-based features relative to video publication."""
        if hasattr(self, 'video') and self.video and self.video.published_at:
            time_diff = self.snapshot_time - self.video.published_at
            self.hours_since_published = time_diff.total_seconds() / 3600
            self.days_since_published = time_diff.total_seconds() / (24 * 3600)
    
    def _calculate_engagement_rate(self) -> None:
        """Calculate engagement rate from current statistics."""
        if self.view_count and self.view_count > 0:
            total_engagement = (self.like_count or 0) + (self.comment_count or 0)
            self.engagement_rate = total_engagement / self.view_count
    
    def calculate_growth_rates(self, previous_snapshot: Optional['Snapshot']) -> None:
        """Calculate growth rates compared to previous snapshot.
        
        Args:
            previous_snapshot: The previous snapshot to compare against
        """
        if not previous_snapshot:
            return
        
        # Calculate time difference in hours
        time_diff_hours = (self.snapshot_time - previous_snapshot.snapshot_time).total_seconds() / 3600
        
        if time_diff_hours <= 0:
            return
        
        # Calculate view growth
        view_diff = self.view_count - previous_snapshot.view_count
        self.views_since_last_snapshot = view_diff
        self.view_growth_rate = view_diff / time_diff_hours
        
        # Calculate like growth
        if self.like_count is not None and previous_snapshot.like_count is not None:
            like_diff = self.like_count - previous_snapshot.like_count
            self.like_growth_rate = like_diff / time_diff_hours
        
        # Calculate comment growth
        if self.comment_count is not None and previous_snapshot.comment_count is not None:
            comment_diff = self.comment_count - previous_snapshot.comment_count
            self.comment_growth_rate = comment_diff / time_diff_hours
    
    def detect_anomalies(self, previous_snapshots: List['Snapshot'], threshold_multiplier: float = 3.0) -> bool:
        """Detect if this snapshot contains anomalous data.
        
        Args:
            previous_snapshots: List of previous snapshots for comparison
            threshold_multiplier: How many standard deviations to consider anomalous
            
        Returns:
            True if anomaly detected, False otherwise
        """
        if not previous_snapshots or len(previous_snapshots) < 3:
            return False
        
        # Calculate average growth rate from previous snapshots
        growth_rates = [s.view_growth_rate for s in previous_snapshots if s.view_growth_rate is not None]
        
        if not growth_rates:
            return False
        
        import statistics
        
        try:
            avg_growth = statistics.mean(growth_rates)
            std_growth = statistics.stdev(growth_rates) if len(growth_rates) > 1 else 0
            
            # Check if current growth rate is anomalous
            if self.view_growth_rate is not None and std_growth > 0:
                z_score = abs(self.view_growth_rate - avg_growth) / std_growth
                
                if z_score > threshold_multiplier:
                    self.has_anomaly = True
                    self.anomaly_reason = f"View growth rate anomaly (z-score: {z_score:.2f})"
                    return True
            
            # Check for negative growth (views decreasing)
            if self.views_since_last_snapshot and self.views_since_last_snapshot < -100:
                self.has_anomaly = True
                self.anomaly_reason = "Negative view growth detected"
                return True
                
        except statistics.StatisticsError:
            pass
        
        return False
    
    def get_growth_velocity(self) -> Optional[float]:
        """Get growth velocity (views per hour) at this snapshot."""
        return self.view_growth_rate
    
    def get_cumulative_engagement(self) -> int:
        """Get total engagement (likes + comments) at this snapshot."""
        return (self.like_count or 0) + (self.comment_count or 0)
    
    def is_peak_performance(self, window_snapshots: List['Snapshot']) -> bool:
        """Check if this snapshot represents peak performance in a time window.
        
        Args:
            window_snapshots: List of snapshots in the comparison window
            
        Returns:
            True if this is the peak performance snapshot
        """
        if not window_snapshots:
            return True
        
        # Compare view growth rate
        max_growth = max((s.view_growth_rate or 0) for s in window_snapshots)
        return (self.view_growth_rate or 0) >= max_growth
    
    def get_performance_tier(self) -> str:
        """Get performance tier based on growth rate."""
        if self.view_growth_rate is None:
            return 'unknown'
        elif self.view_growth_rate >= 1000:  # 1000+ views per hour
            return 'viral'
        elif self.view_growth_rate >= 100:   # 100+ views per hour
            return 'high'
        elif self.view_growth_rate >= 10:    # 10+ views per hour
            return 'medium'
        elif self.view_growth_rate >= 1:     # 1+ views per hour
            return 'low'
        else:
            return 'stagnant'
    
    def calculate_momentum_score(self, recent_snapshots: List['Snapshot']) -> float:
        """Calculate momentum score based on recent growth trend.
        
        Args:
            recent_snapshots: List of recent snapshots (including this one)
            
        Returns:
            Momentum score between 0.0 and 1.0
        """
        if not recent_snapshots or len(recent_snapshots) < 2:
            return 0.5
        
        # Sort by time
        sorted_snapshots = sorted(recent_snapshots, key=lambda s: s.snapshot_time)
        
        # Calculate trend
        growth_rates = [s.view_growth_rate for s in sorted_snapshots if s.view_growth_rate is not None]
        
        if len(growth_rates) < 2:
            return 0.5
        
        # Simple momentum: is growth rate increasing?
        recent_avg = sum(growth_rates[-3:]) / len(growth_rates[-3:])  # Last 3 snapshots
        earlier_avg = sum(growth_rates[:-3]) / len(growth_rates[:-3]) if len(growth_rates) > 3 else recent_avg
        
        if earlier_avg == 0:
            return 0.5
        
        momentum_ratio = recent_avg / earlier_avg
        
        # Normalize to 0-1 scale
        return min(max(momentum_ratio / 2, 0.0), 1.0)
    
    @classmethod
    def get_snapshots_in_timeframe(cls, session, video_id: int, 
                                 start_time: datetime, end_time: datetime) -> List['Snapshot']:
        """Get all snapshots for a video within a timeframe.
        
        Args:
            session: Database session
            video_id: Video ID to filter by
            start_time: Start of timeframe
            end_time: End of timeframe
            
        Returns:
            List of snapshots ordered by time
        """
        return session.query(cls).filter(
            cls.video_id == video_id,
            cls.snapshot_time >= start_time,
            cls.snapshot_time <= end_time
        ).order_by(cls.snapshot_time).all()
    
    @classmethod
    def get_latest_snapshot(cls, session, video_id: int) -> Optional['Snapshot']:
        """Get the most recent snapshot for a video.
        
        Args:
            session: Database session
            video_id: Video ID to get snapshot for
            
        Returns:
            Latest snapshot or None if no snapshots exist
        """
        return session.query(cls).filter(
            cls.video_id == video_id
        ).order_by(cls.snapshot_time.desc()).first()
    
    def to_dict(self, include_growth: bool = True) -> Dict[str, Any]:
        """Convert snapshot to dictionary."""
        data = {
            'id': self.id,
            'video_id': self.video_id,
            'snapshot_time': self.snapshot_time.isoformat() if self.snapshot_time else None,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'engagement_rate': self.engagement_rate,
            'hours_since_published': self.hours_since_published,
            'days_since_published': self.days_since_published,
            'snapshot_type': self.snapshot_type,
            'data_source': self.data_source,
            'is_complete': self.is_complete,
            'has_anomaly': self.has_anomaly,
            'anomaly_reason': self.anomaly_reason,
            'performance_tier': self.get_performance_tier(),
            'cumulative_engagement': self.get_cumulative_engagement(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_growth:
            data.update({
                'views_since_last_snapshot': self.views_since_last_snapshot,
                'view_growth_rate': self.view_growth_rate,
                'like_growth_rate': self.like_growth_rate,
                'comment_growth_rate': self.comment_growth_rate,
            })
        
        return data
    
    def __repr__(self) -> str:
        """String representation of the snapshot."""
        return f"<Snapshot(id={self.id}, video_id={self.video_id}, views={self.view_count}, time='{self.snapshot_time}')>"
