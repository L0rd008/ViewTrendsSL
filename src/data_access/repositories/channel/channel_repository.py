"""
Channel Repository for ViewTrendsSL

This module provides data access operations for Channel entities,
including channel management, statistics, and Sri Lankan channel operations.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc

from src.data_access.database.base import AdvancedRepository
from src.data_access.models.channel import Channel
from src.business.utils.time_utils import get_current_utc_time

# Configure logging
logger = logging.getLogger(__name__)


class ChannelCreateSchema:
    """Schema for creating a new channel."""
    
    def __init__(
        self,
        channel_id: str,
        title: str,
        description: Optional[str] = None,
        subscriber_count: int = 0,
        video_count: int = 0,
        view_count: int = 0,
        country: Optional[str] = None,
        language: Optional[str] = None,
        is_sri_lankan: bool = False,
        category: Optional[str] = None,
        is_active: bool = True
    ):
        self.channel_id = channel_id
        self.title = title
        self.description = description
        self.subscriber_count = subscriber_count
        self.video_count = video_count
        self.view_count = view_count
        self.country = country
        self.language = language
        self.is_sri_lankan = is_sri_lankan
        self.category = category
        self.is_active = is_active


class ChannelUpdateSchema:
    """Schema for updating channel information."""
    
    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        subscriber_count: Optional[int] = None,
        video_count: Optional[int] = None,
        view_count: Optional[int] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        is_sri_lankan: Optional[bool] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        last_updated: Optional[datetime] = None
    ):
        self.title = title
        self.description = description
        self.subscriber_count = subscriber_count
        self.video_count = video_count
        self.view_count = view_count
        self.country = country
        self.language = language
        self.is_sri_lankan = is_sri_lankan
        self.category = category
        self.is_active = is_active
        self.last_updated = last_updated


class ChannelRepository(AdvancedRepository[Channel]):
    """Repository for Channel entity operations."""
    
    def __init__(self):
        """Initialize the channel repository."""
        super().__init__(Channel)
    
    def create(self, obj_in: ChannelCreateSchema, session: Optional[Session] = None) -> Channel:
        """
        Create a new channel.
        
        Args:
            obj_in: Channel creation data
            session: Optional database session
            
        Returns:
            Created Channel instance
        """
        def _create(session: Session) -> Channel:
            # Check if channel already exists
            existing_channel = session.query(Channel).filter(
                Channel.channel_id == obj_in.channel_id
            ).first()
            
            if existing_channel:
                raise ValueError(f"Channel with ID {obj_in.channel_id} already exists")
            
            # Create new channel
            db_channel = Channel(
                channel_id=obj_in.channel_id,
                title=obj_in.title,
                description=obj_in.description,
                subscriber_count=obj_in.subscriber_count,
                video_count=obj_in.video_count,
                view_count=obj_in.view_count,
                country=obj_in.country,
                language=obj_in.language,
                is_sri_lankan=obj_in.is_sri_lankan,
                category=obj_in.category,
                is_active=obj_in.is_active,
                created_at=get_current_utc_time(),
                updated_at=get_current_utc_time()
            )
            
            session.add(db_channel)
            session.flush()  # Get the ID without committing
            logger.info(f"Created new channel: {db_channel.title} (ID: {db_channel.channel_id})")
            return db_channel
        
        if session:
            return _create(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _create(session)
    
    def update(self, db_obj: Channel, obj_in: ChannelUpdateSchema, session: Optional[Session] = None) -> Channel:
        """
        Update an existing channel.
        
        Args:
            db_obj: Existing Channel instance
            obj_in: Channel update data
            session: Optional database session
            
        Returns:
            Updated Channel instance
        """
        def _update(session: Session) -> Channel:
            # Update fields if provided
            if obj_in.title is not None:
                db_obj.title = obj_in.title
            
            if obj_in.description is not None:
                db_obj.description = obj_in.description
            
            if obj_in.subscriber_count is not None:
                db_obj.subscriber_count = obj_in.subscriber_count
            
            if obj_in.video_count is not None:
                db_obj.video_count = obj_in.video_count
            
            if obj_in.view_count is not None:
                db_obj.view_count = obj_in.view_count
            
            if obj_in.country is not None:
                db_obj.country = obj_in.country
            
            if obj_in.language is not None:
                db_obj.language = obj_in.language
            
            if obj_in.is_sri_lankan is not None:
                db_obj.is_sri_lankan = obj_in.is_sri_lankan
            
            if obj_in.category is not None:
                db_obj.category = obj_in.category
            
            if obj_in.is_active is not None:
                db_obj.is_active = obj_in.is_active
            
            if obj_in.last_updated is not None:
                db_obj.last_updated = obj_in.last_updated
            
            db_obj.updated_at = get_current_utc_time()
            
            logger.info(f"Updated channel: {db_obj.title} (ID: {db_obj.channel_id})")
            return db_obj
        
        if session:
            return _update(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _update(session)
    
    def get_by_channel_id(self, channel_id: str, session: Optional[Session] = None) -> Optional[Channel]:
        """
        Get channel by YouTube channel ID.
        
        Args:
            channel_id: YouTube channel ID
            session: Optional database session
            
        Returns:
            Channel instance or None if not found
        """
        return self.get_by_field('channel_id', channel_id, session)
    
    def get_sri_lankan_channels(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get all Sri Lankan channels.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of Sri Lankan Channel instances
        """
        return self.get_multi_by_field('is_sri_lankan', True, skip, limit, session)
    
    def get_channels_by_category(
        self, 
        category: str, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get channels by category.
        
        Args:
            category: Channel category
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of Channel instances
        """
        return self.get_multi_by_field('category', category, skip, limit, session)
    
    def get_channels_by_language(
        self, 
        language: str, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get channels by language.
        
        Args:
            language: Channel language
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of Channel instances
        """
        return self.get_multi_by_field('language', language, skip, limit, session)
    
    def get_top_channels_by_subscribers(
        self, 
        limit: int = 50,
        sri_lankan_only: bool = False,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get top channels by subscriber count.
        
        Args:
            limit: Maximum number of channels to return
            sri_lankan_only: Whether to filter for Sri Lankan channels only
            session: Optional database session
            
        Returns:
            List of top Channel instances
        """
        def _get_top_channels(session: Session) -> List[Channel]:
            query = session.query(Channel).filter(Channel.is_active == True)
            
            if sri_lankan_only:
                query = query.filter(Channel.is_sri_lankan == True)
            
            return query.order_by(desc(Channel.subscriber_count)).limit(limit).all()
        
        if session:
            return _get_top_channels(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_top_channels(session)
    
    def get_top_channels_by_views(
        self, 
        limit: int = 50,
        sri_lankan_only: bool = False,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get top channels by total view count.
        
        Args:
            limit: Maximum number of channels to return
            sri_lankan_only: Whether to filter for Sri Lankan channels only
            session: Optional database session
            
        Returns:
            List of top Channel instances
        """
        def _get_top_channels(session: Session) -> List[Channel]:
            query = session.query(Channel).filter(Channel.is_active == True)
            
            if sri_lankan_only:
                query = query.filter(Channel.is_sri_lankan == True)
            
            return query.order_by(desc(Channel.view_count)).limit(limit).all()
        
        if session:
            return _get_top_channels(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_top_channels(session)
    
    def get_channels_by_subscriber_range(
        self, 
        min_subscribers: int, 
        max_subscribers: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get channels within a subscriber count range.
        
        Args:
            min_subscribers: Minimum subscriber count
            max_subscribers: Maximum subscriber count (optional)
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of Channel instances
        """
        def _get_channels_by_range(session: Session) -> List[Channel]:
            query = session.query(Channel).filter(
                Channel.subscriber_count >= min_subscribers
            )
            
            if max_subscribers is not None:
                query = query.filter(Channel.subscriber_count <= max_subscribers)
            
            return query.offset(skip).limit(limit).all()
        
        if session:
            return _get_channels_by_range(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_channels_by_range(session)
    
    def update_channel_statistics(
        self, 
        channel_id: str, 
        subscriber_count: int, 
        video_count: int, 
        view_count: int,
        session: Optional[Session] = None
    ) -> bool:
        """
        Update channel statistics.
        
        Args:
            channel_id: YouTube channel ID
            subscriber_count: New subscriber count
            video_count: New video count
            view_count: New view count
            session: Optional database session
            
        Returns:
            True if updated successfully, False otherwise
        """
        def _update_stats(session: Session) -> bool:
            channel = session.query(Channel).filter(Channel.channel_id == channel_id).first()
            if channel:
                channel.subscriber_count = subscriber_count
                channel.video_count = video_count
                channel.view_count = view_count
                channel.last_updated = get_current_utc_time()
                channel.updated_at = get_current_utc_time()
                logger.info(f"Updated statistics for channel: {channel.title}")
                return True
            return False
        
        if session:
            return _update_stats(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _update_stats(session)
    
    def mark_as_sri_lankan(self, channel_id: str, session: Optional[Session] = None) -> bool:
        """
        Mark a channel as Sri Lankan.
        
        Args:
            channel_id: YouTube channel ID
            session: Optional database session
            
        Returns:
            True if updated successfully, False otherwise
        """
        def _mark_sri_lankan(session: Session) -> bool:
            channel = session.query(Channel).filter(Channel.channel_id == channel_id).first()
            if channel:
                channel.is_sri_lankan = True
                channel.updated_at = get_current_utc_time()
                logger.info(f"Marked channel as Sri Lankan: {channel.title}")
                return True
            return False
        
        if session:
            return _mark_sri_lankan(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _mark_sri_lankan(session)
    
    def get_channel_statistics(self, session: Optional[Session] = None) -> Dict[str, Any]:
        """
        Get channel statistics.
        
        Args:
            session: Optional database session
            
        Returns:
            Dictionary with channel statistics
        """
        def _get_stats(session: Session) -> Dict[str, Any]:
            total_channels = session.query(Channel).count()
            active_channels = session.query(Channel).filter(Channel.is_active == True).count()
            sri_lankan_channels = session.query(Channel).filter(Channel.is_sri_lankan == True).count()
            
            # Channels by category
            categories = session.query(
                Channel.category, 
                func.count(Channel.id)
            ).filter(Channel.category.isnot(None)).group_by(Channel.category).all()
            
            # Channels by language
            languages = session.query(
                Channel.language, 
                func.count(Channel.id)
            ).filter(Channel.language.isnot(None)).group_by(Channel.language).all()
            
            # Average statistics
            avg_stats = session.query(
                func.avg(Channel.subscriber_count).label('avg_subscribers'),
                func.avg(Channel.video_count).label('avg_videos'),
                func.avg(Channel.view_count).label('avg_views')
            ).filter(Channel.is_active == True).first()
            
            # Top performing channels
            top_channel = session.query(Channel).filter(
                Channel.is_active == True
            ).order_by(desc(Channel.subscriber_count)).first()
            
            return {
                'total_channels': total_channels,
                'active_channels': active_channels,
                'inactive_channels': total_channels - active_channels,
                'sri_lankan_channels': sri_lankan_channels,
                'international_channels': total_channels - sri_lankan_channels,
                'categories': dict(categories),
                'languages': dict(languages),
                'average_subscribers': float(avg_stats.avg_subscribers) if avg_stats.avg_subscribers else 0,
                'average_videos': float(avg_stats.avg_videos) if avg_stats.avg_videos else 0,
                'average_views': float(avg_stats.avg_views) if avg_stats.avg_views else 0,
                'top_channel': {
                    'title': top_channel.title,
                    'subscribers': top_channel.subscriber_count
                } if top_channel else None
            }
        
        if session:
            return _get_stats(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_stats(session)
    
    def search_channels(
        self, 
        search_term: str, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Search channels by title or description.
        
        Args:
            search_term: Term to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of matching Channel instances
        """
        search_fields = ['title', 'description']
        return self.search(search_term, search_fields, skip, limit, session)
    
    def get_channels_needing_update(
        self, 
        hours_threshold: int = 24,
        session: Optional[Session] = None
    ) -> List[Channel]:
        """
        Get channels that haven't been updated recently.
        
        Args:
            hours_threshold: Hours since last update to consider as needing update
            session: Optional database session
            
        Returns:
            List of Channel instances needing update
        """
        def _get_stale_channels(session: Session) -> List[Channel]:
            cutoff_time = get_current_utc_time() - timedelta(hours=hours_threshold)
            return session.query(Channel).filter(
                and_(
                    Channel.is_active == True,
                    or_(
                        Channel.last_updated < cutoff_time,
                        Channel.last_updated.is_(None)
                    )
                )
            ).all()
        
        if session:
            return _get_stale_channels(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_stale_channels(session)
    
    def bulk_update_statistics(
        self, 
        updates: List[Dict[str, Any]], 
        session: Optional[Session] = None
    ) -> int:
        """
        Bulk update channel statistics.
        
        Args:
            updates: List of dictionaries with channel_id and statistics
            session: Optional database session
            
        Returns:
            Number of updated channels
        """
        def _bulk_update(session: Session) -> int:
            count = 0
            current_time = get_current_utc_time()
            
            for update_data in updates:
                channel_id = update_data.get('channel_id')
                if not channel_id:
                    continue
                
                channel = session.query(Channel).filter(Channel.channel_id == channel_id).first()
                if channel:
                    if 'subscriber_count' in update_data:
                        channel.subscriber_count = update_data['subscriber_count']
                    if 'video_count' in update_data:
                        channel.video_count = update_data['video_count']
                    if 'view_count' in update_data:
                        channel.view_count = update_data['view_count']
                    
                    channel.last_updated = current_time
                    channel.updated_at = current_time
                    count += 1
            
            logger.info(f"Bulk updated {count} channels")
            return count
        
        if session:
            return _bulk_update(session)
        else:
            from src.data_access.database.session import get_db_transaction
            with get_db_transaction() as session:
                return _bulk_update(session)
    
    def get_channel_growth_data(
        self, 
        channel_id: str, 
        session: Optional[Session] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get channel growth data (requires historical tracking).
        
        Args:
            channel_id: YouTube channel ID
            session: Optional database session
            
        Returns:
            Dictionary with growth data or None if not found
        """
        def _get_growth_data(session: Session) -> Optional[Dict[str, Any]]:
            channel = session.query(Channel).filter(Channel.channel_id == channel_id).first()
            if not channel:
                return None
            
            # This is a placeholder for growth calculation
            # In a real implementation, you would query historical snapshots
            return {
                'channel_id': channel.channel_id,
                'title': channel.title,
                'current_subscribers': channel.subscriber_count,
                'current_videos': channel.video_count,
                'current_views': channel.view_count,
                'last_updated': channel.last_updated,
                # Growth metrics would be calculated from historical data
                'subscriber_growth_rate': 0.0,  # Placeholder
                'video_upload_rate': 0.0,  # Placeholder
                'view_growth_rate': 0.0  # Placeholder
            }
        
        if session:
            return _get_growth_data(session)
        else:
            from src.data_access.database.session import get_db_session
            with get_db_session() as session:
                return _get_growth_data(session)


# Global repository instance
_channel_repository: Optional[ChannelRepository] = None

def get_channel_repository() -> ChannelRepository:
    """Get the global channel repository instance."""
    global _channel_repository
    
    if _channel_repository is None:
        _channel_repository = ChannelRepository()
    
    return _channel_repository
