"""Base model classes for ViewTrendsSL database models."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime

# Create the declarative base
Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )
    
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )


class BaseModel(Base, TimestampMixin):
    """Abstract base model with common functionality."""
    
    __abstract__ = True
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: dict) -> None:
        """Update model instance from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            return f"<{class_name}(id={self.id})>"
        return f"<{class_name}()>"
