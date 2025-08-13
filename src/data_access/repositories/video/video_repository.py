"""Video repository for video-specific database operations."""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc, func, text
from datetime import datetime, timedelta
import logging

from ..base_repository import BaseRepository
from ...models.video import Video
from ...models.channel import Channel
from ...models.snapshot import Snapshot
from ...models.tag import Tag, VideoTag

logger = logging.getLogger(__name__)


class VideoRepository(BaseRepository[Video]):
    """Repository for video-specific database operations."""
    
    def __init__(self, session: Session):
        """Initialize video repository."""
        super().__init__(Video, session)
    
    def get_by_video_id(self, video_id: str) -> Optional[Video]:
        """Get video by YouTube video ID.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video instance or None if not found
        """
        return self.find_one_by(video_id=video_id)
    
    def get_videos_by_channel(self, channel_id: int, limit: Optional[int] = None, 
                             include_deleted: bool = False) -> List[Video]:
        """Get videos by channel ID.
        
        Args:
            channel_id: Channel database ID
            limit: Maximum number of videos to return
            include_deleted: Whether to include deleted videos
            
        Returns:
            List of video instances
        """
        filters = {'channel_id': channel_id}
        if not include_deleted:
            filters['is_deleted'] = False
        
        return self.find_by(
            limit=limit,
            order_by='published_at',
            desc_order=True,
            **filters
        )
    
    def get_videos_by_channel_youtube_id(self, channel_youtube_id: str, 
                                       limit: Optional[int] = None) -> List[Video]:
        """Get videos by channel YouTube ID.
        
        Args:
            channel_youtube_id: YouTube channel ID
            limit: Maximum number of videos to return
            
        Returns:
            List of video instances
        """
        try:
            query = self.session.query(Video).join(Channel).filter(
                Channel.channel_id == channel_youtube_id,
                Video.is_deleted == False
            ).order_by(desc(Video.published_at))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting videos by channel YouTube ID: {e}")
            raise
    
    def get_shorts(self, limit: Optional[int] = None, min_views: int = 0) -> List[Video]:
        """Get YouTube Shorts videos.
        
        Args:
            limit: Maximum number of videos to return
            min_views: Minimum view count filter
            
        Returns:
            List of Shorts videos
        """
        filters = {
            'is_short': True,
            'is_deleted': False
        }
        
        try:
            query = self.session.query(Video).filter(
                Video.is_short == True,
                Video.is_deleted == False,
                Video.view_count >= min_views
            ).order_by(desc(Video.view_count))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting Shorts videos: {e}")
            raise
    
    def get_long_form_videos(self, limit: Optional[int] = None, min_views: int = 0) -> List[Video]:
        """Get long-form videos (not Shorts).
        
        Args:
            limit: Maximum number of videos to return
            min_views: Minimum view count filter
            
        Returns:
            List of long-form videos
        """
        try:
            query = self.session.query(Video).filter(
                Video.is_short == False,
                Video.is_deleted == False,
                Video.view_count >= min_views
            ).order_by(desc(Video.view_count))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting long-form videos: {e}")
            raise
    
    def get_videos_by_category(self, category_name: str, limit: Optional[int] = None) -> List[Video]:
        """Get videos by category.
        
        Args:
            category_name: Category name
            limit: Maximum number of videos to return
            
        Returns:
            List of videos in the category
        """
        return self.find_by(
            category_name=category_name,
            is_deleted=False,
            limit=limit,
            order_by='view_count',
            desc_order=True
        )
    
    def get_trending_videos(self, days: int = 7, limit: int = 50) -> List[Video]:
        """Get trending videos based on recent performance.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of videos to return
            
        Returns:
            List of trending videos
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            query = self.session.query(Video).filter(
                Video.published_at >= cutoff_date,
                Video.is_deleted == False,
                Video.view_count > 0
            ).order_by(desc(Video.view_count)).limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting trending videos: {e}")
            raise
    
    def get_viral_videos(self, threshold_multiplier: float = 10.0, limit: int = 50) -> List[Video]:
        """Get viral videos based on performance relative to channel average.
        
        Args:
            threshold_multiplier: Multiplier for channel average to consider viral
            limit: Maximum number of videos to return
            
        Returns:
            List of viral videos
        """
        try:
            query = self.session.query(Video).join(Channel).filter(
                Video.view_count >= Channel.avg_views_per_video * threshold_multiplier,
                Video.is_deleted == False,
                Channel.avg_views_per_video > 0
            ).order_by(desc(Video.view_count)).limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting viral videos: {e}")
            raise
    
    def get_videos_for_training(self, is_short: Optional[bool] = None, 
                              min_age_days: int = 7, max_age_days: int = 365) -> List[Video]:
        """Get videos suitable for model training.
        
        Args:
            is_short: Filter by video type (True for Shorts, False for long-form, None for all)
            min_age_days: Minimum age in days
            max_age_days: Maximum age in days
            
        Returns:
            List of videos suitable for training
        """
        try:
            min_date = datetime.utcnow() - timedelta(days=max_age_days)
            max_date = datetime.utcnow() - timedelta(days=min_age_days)
            
            query = self.session.query(Video).filter(
                Video.published_at >= min_date,
                Video.published_at <= max_date,
                Video.is_deleted == False,
                Video.is_private == False,
                Video.view_count > 0,
                Video.data_quality_score >= 0.7  # Good data quality
            )
            
            if is_short is not None:
                query = query.filter(Video.is_short == is_short)
            
            return query.order_by(desc(Video.published_at)).all()
        except Exception as e:
            logger.error(f"Error getting videos for training: {e}")
            raise
    
    def get_videos_needing_tracking(self, max_age_days: int = 30) -> List[Video]:
        """Get videos that need performance tracking.
        
        Args:
            max_age_days: Maximum age for tracking
            
        Returns:
            List of videos needing tracking
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
            
            query = self.session.query(Video).filter(
                Video.published_at >= cutoff_date,
                Video.is_tracking_complete == False,
                Video.is_deleted == False,
                Video.is_private == False
            ).order_by(asc(Video.published_at))
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting videos needing tracking: {e}")
            raise
    
    def search_videos(self, query: str, limit: int = 50) -> List[Video]:
        """Search videos by title and description.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching videos
        """
        try:
            search_filter = or_(
                Video.title.ilike(f'%{query}%'),
                Video.description.ilike(f'%{query}%')
            )
            
            return self.session.query(Video).filter(
                search_filter,
                Video.is_deleted == False
            ).order_by(desc(Video.view_count)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            raise
    
    def get_videos_with_tags(self, tag_names: List[str], match_all: bool = False) -> List[Video]:
        """Get videos that have specific tags.
        
        Args:
            tag_names: List of tag names to search for
            match_all: If True, video must have all tags; if False, any tag
            
        Returns:
            List of videos with the specified tags
        """
        try:
            query = self.session.query(Video).join(VideoTag).join(Tag).filter(
                Tag.normalized_name.in_([name.lower().strip() for name in tag_names]),
                Video.is_deleted == False
            )
            
            if match_all:
                # Video must have all specified tags
                query = query.group_by(Video.id).having(
                    func.count(Tag.id) == len(tag_names)
                )
            
            return query.order_by(desc(Video.view_count)).all()
        except Exception as e:
            logger.error(f"Error getting videos with tags: {e}")
            raise
    
    def get_performance_stats(self, channel_id: Optional[int] = None, 
                            days: int = 30) -> Dict[str, Any]:
        """Get performance statistics for videos.
        
        Args:
            channel_id: Optional channel ID to filter by
            days: Number of days to analyze
            
        Returns:
            Dictionary with performance statistics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            query = self.session.query(Video).filter(
                Video.published_at >= cutoff_date,
                Video.is_deleted == False
            )
            
            if channel_id:
                query = query.filter(Video.channel_id == channel_id)
            
            videos = query.all()
            
            if not videos:
                return {
                    'total_videos': 0,
                    'total_views': 0,
                    'avg_views': 0,
                    'avg_engagement_rate': 0,
                    'shorts_count': 0,
                    'longform_count': 0
                }
            
            total_views = sum(v.view_count or 0 for v in videos)
            total_engagement = sum(v.engagement_rate or 0 for v in videos)
            shorts_count = sum(1 for v in videos if v.is_short)
            
            return {
                'total_videos': len(videos),
                'total_views': total_views,
                'avg_views': total_views / len(videos),
                'avg_engagement_rate': total_engagement / len(videos),
                'shorts_count': shorts_count,
                'longform_count': len(videos) - shorts_count,
                'period_days': days
            }
        except Exception as e:
            logger.error(f"Error getting performance stats: {e}")
            raise
    
    def update_video_statistics(self, video_id: str, view_count: int, 
                              like_count: Optional[int] = None, 
                              comment_count: Optional[int] = None) -> Optional[Video]:
        """Update video statistics.
        
        Args:
            video_id: YouTube video ID
            view_count: Current view count
            like_count: Current like count
            comment_count: Current comment count
            
        Returns:
            Updated video instance or None if not found
        """
        try:
            video = self.get_by_video_id(video_id)
            if not video:
                return None
            
            video.update_statistics(view_count, like_count, comment_count)
            self.session.flush()
            
            return video
        except Exception as e:
            logger.error(f"Error updating video statistics: {e}")
            raise
    
    def mark_as_deleted(self, video_id: str) -> bool:
        """Mark a video as deleted.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if marked as deleted, False if not found
        """
        try:
            video = self.get_by_video_id(video_id)
            if not video:
                return False
            
            video.is_deleted = True
            video.updated_at = datetime.utcnow()
            self.session.flush()
            
            return True
        except Exception as e:
            logger.error(f"Error marking video as deleted: {e}")
            raise
    
    def get_videos_with_snapshots(self, limit: Optional[int] = None) -> List[Video]:
        """Get videos that have snapshot data.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of videos with snapshot data
        """
        try:
            query = self.session.query(Video).join(Snapshot).filter(
                Video.is_deleted == False
            ).distinct().order_by(desc(Video.published_at))
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            logger.error(f"Error getting videos with snapshots: {e}")
            raise
    
    def bulk_update_quality_scores(self) -> int:
        """Update data quality scores for all videos.
        
        Returns:
            Number of videos updated
        """
        try:
            videos = self.find_by(is_deleted=False)
            updated_count = 0
            
            for video in videos:
                old_score = video.data_quality_score
                new_score = video.calculate_data_quality_score()
                
                if old_score != new_score:
                    updated_count += 1
            
            self.session.flush()
            logger.info(f"Updated quality scores for {updated_count} videos")
            return updated_count
        except Exception as e:
            logger.error(f"Error updating quality scores: {e}")
            raise
