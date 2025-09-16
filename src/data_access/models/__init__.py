"""Database models for ViewTrendsSL.

This module contains all SQLAlchemy models for the application,
including User, Channel, Video, Snapshot, and Tag models.
"""

# Import base classes first
from .base import Base, BaseModel, TimestampMixin

# Import all models to ensure they're registered with SQLAlchemy
from .user import User
from .channel import Channel
from .video import Video
from .snapshot import Snapshot
from .tag import Tag, VideoTag

# Export all models for easy importing
__all__ = [
    'Base',
    'BaseModel',
    'TimestampMixin',
    'User',
    'Channel', 
    'Video',
    'Snapshot',
    'Tag',
    'VideoTag'
]
