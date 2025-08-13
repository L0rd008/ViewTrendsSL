"""Base repository class providing common database operations."""

from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, desc, asc
from datetime import datetime
import logging

from ..models import BaseModel

T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class BaseRepository(Generic[T]):
    """Base repository class providing common CRUD operations.
    
    This class implements the Repository pattern, providing a consistent
    interface for database operations across all models.
    """
    
    def __init__(self, model_class: Type[T], session: Session):
        """Initialize repository with model class and database session.
        
        Args:
            model_class: The SQLAlchemy model class
            session: Database session
        """
        self.model_class = model_class
        self.session = session
    
    def create(self, **kwargs) -> T:
        """Create a new instance of the model.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            instance = self.model_class(**kwargs)
            self.session.add(instance)
            self.session.flush()  # Get the ID without committing
            logger.debug(f"Created {self.model_class.__name__} with ID {instance.id}")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            self.session.rollback()
            raise
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a model instance by ID.
        
        Args:
            id: Model ID
            
        Returns:
            Model instance or None if not found
        """
        try:
            return self.session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model_class.__name__} by ID {id}: {e}")
            raise
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Get all instances of the model.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model instances
        """
        try:
            query = self.session.query(self.model_class)
            
            if offset > 0:
                query = query.offset(offset)
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all {self.model_class.__name__}: {e}")
            raise
    
    def update(self, instance: T, **kwargs) -> T:
        """Update a model instance.
        
        Args:
            instance: Model instance to update
            **kwargs: Attributes to update
            
        Returns:
            Updated model instance
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            # Update timestamp if available
            if hasattr(instance, 'updated_at'):
                instance.updated_at = datetime.utcnow()
            
            self.session.flush()
            logger.debug(f"Updated {self.model_class.__name__} with ID {instance.id}")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Error updating {self.model_class.__name__}: {e}")
            self.session.rollback()
            raise
    
    def delete(self, instance: T) -> bool:
        """Delete a model instance.
        
        Args:
            instance: Model instance to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            self.session.delete(instance)
            self.session.flush()
            logger.debug(f"Deleted {self.model_class.__name__} with ID {instance.id}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.model_class.__name__}: {e}")
            self.session.rollback()
            raise
    
    def delete_by_id(self, id: int) -> bool:
        """Delete a model instance by ID.
        
        Args:
            id: Model ID
            
        Returns:
            True if deleted successfully, False if not found
        """
        instance = self.get_by_id(id)
        if instance:
            return self.delete(instance)
        return False
    
    def exists(self, **filters) -> bool:
        """Check if a record exists with the given filters.
        
        Args:
            **filters: Filter conditions
            
        Returns:
            True if record exists
        """
        try:
            query = self.session.query(self.model_class)
            
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence in {self.model_class.__name__}: {e}")
            raise
    
    def count(self, **filters) -> int:
        """Count records matching the given filters.
        
        Args:
            **filters: Filter conditions
            
        Returns:
            Number of matching records
        """
        try:
            query = self.session.query(self.model_class)
            
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            
            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model_class.__name__}: {e}")
            raise
    
    def find_by(self, limit: Optional[int] = None, offset: int = 0, 
                order_by: Optional[str] = None, desc_order: bool = False, **filters) -> List[T]:
        """Find records by filters.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            order_by: Field to order by
            desc_order: Whether to order in descending order
            **filters: Filter conditions
            
        Returns:
            List of matching model instances
        """
        try:
            query = self.session.query(self.model_class)
            
            # Apply filters
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    if isinstance(value, list):
                        # Handle IN queries
                        query = query.filter(getattr(self.model_class, key).in_(value))
                    else:
                        query = query.filter(getattr(self.model_class, key) == value)
            
            # Apply ordering
            if order_by and hasattr(self.model_class, order_by):
                order_field = getattr(self.model_class, order_by)
                if desc_order:
                    query = query.order_by(desc(order_field))
                else:
                    query = query.order_by(asc(order_field))
            
            # Apply pagination
            if offset > 0:
                query = query.offset(offset)
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error finding {self.model_class.__name__}: {e}")
            raise
    
    def find_one_by(self, **filters) -> Optional[T]:
        """Find a single record by filters.
        
        Args:
            **filters: Filter conditions
            
        Returns:
            Model instance or None if not found
        """
        results = self.find_by(limit=1, **filters)
        return results[0] if results else None
    
    def bulk_create(self, instances: List[Dict[str, Any]]) -> List[T]:
        """Create multiple instances in bulk.
        
        Args:
            instances: List of dictionaries with model attributes
            
        Returns:
            List of created model instances
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            created_instances = []
            for instance_data in instances:
                instance = self.model_class(**instance_data)
                self.session.add(instance)
                created_instances.append(instance)
            
            self.session.flush()
            logger.debug(f"Bulk created {len(created_instances)} {self.model_class.__name__} instances")
            return created_instances
        except SQLAlchemyError as e:
            logger.error(f"Error bulk creating {self.model_class.__name__}: {e}")
            self.session.rollback()
            raise
    
    def bulk_update(self, updates: List[Dict[str, Any]], id_field: str = 'id') -> int:
        """Update multiple instances in bulk.
        
        Args:
            updates: List of dictionaries with ID and update data
            id_field: Field name to use as identifier
            
        Returns:
            Number of updated records
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            updated_count = 0
            for update_data in updates:
                if id_field not in update_data:
                    continue
                
                id_value = update_data.pop(id_field)
                result = self.session.query(self.model_class).filter(
                    getattr(self.model_class, id_field) == id_value
                ).update(update_data)
                
                updated_count += result
            
            self.session.flush()
            logger.debug(f"Bulk updated {updated_count} {self.model_class.__name__} instances")
            return updated_count
        except SQLAlchemyError as e:
            logger.error(f"Error bulk updating {self.model_class.__name__}: {e}")
            self.session.rollback()
            raise
    
    def get_or_create(self, defaults: Optional[Dict[str, Any]] = None, **kwargs) -> tuple[T, bool]:
        """Get an existing instance or create a new one.
        
        Args:
            defaults: Default values for creation
            **kwargs: Filter conditions for lookup
            
        Returns:
            Tuple of (instance, created) where created is True if instance was created
        """
        try:
            instance = self.find_one_by(**kwargs)
            
            if instance:
                return instance, False
            
            # Create new instance
            create_data = kwargs.copy()
            if defaults:
                create_data.update(defaults)
            
            instance = self.create(**create_data)
            return instance, True
        except SQLAlchemyError as e:
            logger.error(f"Error in get_or_create for {self.model_class.__name__}: {e}")
            raise
    
    def refresh(self, instance: T) -> T:
        """Refresh an instance from the database.
        
        Args:
            instance: Model instance to refresh
            
        Returns:
            Refreshed model instance
        """
        try:
            self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Error refreshing {self.model_class.__name__}: {e}")
            raise
    
    def commit(self) -> None:
        """Commit the current transaction."""
        try:
            self.session.commit()
            logger.debug("Transaction committed successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error committing transaction: {e}")
            self.session.rollback()
            raise
    
    def rollback(self) -> None:
        """Rollback the current transaction."""
        try:
            self.session.rollback()
            logger.debug("Transaction rolled back")
        except SQLAlchemyError as e:
            logger.error(f"Error rolling back transaction: {e}")
            raise
