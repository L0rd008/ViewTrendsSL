"""
Base Repository Classes for ViewTrendsSL

This module provides base classes for implementing the repository pattern
with common CRUD operations and query utilities.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any, Type, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, desc, asc, func

from src.data_access.database.session import get_db_session, get_db_transaction

# Configure logging
logger = logging.getLogger(__name__)

# Type variables for generic repository
ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')


class BaseRepository(Generic[ModelType], ABC):
    """
    Abstract base repository class providing common CRUD operations.
    
    This class implements the Repository pattern to abstract database operations
    and provide a consistent interface for data access.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the repository with a model class.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    # Abstract methods that must be implemented by subclasses
    @abstractmethod
    def create(self, obj_in: CreateSchemaType, session: Optional[Session] = None) -> ModelType:
        """Create a new record."""
        pass
    
    @abstractmethod
    def update(self, db_obj: ModelType, obj_in: UpdateSchemaType, session: Optional[Session] = None) -> ModelType:
        """Update an existing record."""
        pass
    
    # Common CRUD operations
    def get(self, id: Any, session: Optional[Session] = None) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            id: Primary key value
            session: Optional database session
            
        Returns:
            Model instance or None if not found
        """
        def _get(session: Session) -> Optional[ModelType]:
            return session.query(self.model).filter(self.model.id == id).first()
        
        if session:
            return _get(session)
        else:
            with get_db_session() as session:
                return _get(session)
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        session: Optional[Session] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of model instances
        """
        def _get_multi(session: Session) -> List[ModelType]:
            return session.query(self.model).offset(skip).limit(limit).all()
        
        if session:
            return _get_multi(session)
        else:
            with get_db_session() as session:
                return _get_multi(session)
    
    def get_by_field(
        self, 
        field_name: str, 
        value: Any, 
        session: Optional[Session] = None
    ) -> Optional[ModelType]:
        """
        Get a single record by a specific field.
        
        Args:
            field_name: Name of the field to filter by
            value: Value to match
            session: Optional database session
            
        Returns:
            Model instance or None if not found
        """
        def _get_by_field(session: Session) -> Optional[ModelType]:
            field = getattr(self.model, field_name)
            return session.query(self.model).filter(field == value).first()
        
        if session:
            return _get_by_field(session)
        else:
            with get_db_session() as session:
                return _get_by_field(session)
    
    def get_multi_by_field(
        self, 
        field_name: str, 
        value: Any, 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[ModelType]:
        """
        Get multiple records by a specific field.
        
        Args:
            field_name: Name of the field to filter by
            value: Value to match
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of model instances
        """
        def _get_multi_by_field(session: Session) -> List[ModelType]:
            field = getattr(self.model, field_name)
            return session.query(self.model).filter(field == value).offset(skip).limit(limit).all()
        
        if session:
            return _get_multi_by_field(session)
        else:
            with get_db_session() as session:
                return _get_multi_by_field(session)
    
    def delete(self, id: Any, session: Optional[Session] = None) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Primary key value
            session: Optional database session
            
        Returns:
            True if deleted, False if not found
        """
        def _delete(session: Session) -> bool:
            obj = session.query(self.model).filter(self.model.id == id).first()
            if obj:
                session.delete(obj)
                return True
            return False
        
        if session:
            return _delete(session)
        else:
            with get_db_transaction() as session:
                return _delete(session)
    
    def delete_multi(self, ids: List[Any], session: Optional[Session] = None) -> int:
        """
        Delete multiple records by IDs.
        
        Args:
            ids: List of primary key values
            session: Optional database session
            
        Returns:
            Number of deleted records
        """
        def _delete_multi(session: Session) -> int:
            count = session.query(self.model).filter(self.model.id.in_(ids)).count()
            session.query(self.model).filter(self.model.id.in_(ids)).delete(synchronize_session=False)
            return count
        
        if session:
            return _delete_multi(session)
        else:
            with get_db_transaction() as session:
                return _delete_multi(session)
    
    def count(self, session: Optional[Session] = None) -> int:
        """
        Count total number of records.
        
        Args:
            session: Optional database session
            
        Returns:
            Total count of records
        """
        def _count(session: Session) -> int:
            return session.query(self.model).count()
        
        if session:
            return _count(session)
        else:
            with get_db_session() as session:
                return _count(session)
    
    def exists(self, id: Any, session: Optional[Session] = None) -> bool:
        """
        Check if a record exists by ID.
        
        Args:
            id: Primary key value
            session: Optional database session
            
        Returns:
            True if exists, False otherwise
        """
        def _exists(session: Session) -> bool:
            return session.query(self.model).filter(self.model.id == id).first() is not None
        
        if session:
            return _exists(session)
        else:
            with get_db_session() as session:
                return _exists(session)
    
    def exists_by_field(self, field_name: str, value: Any, session: Optional[Session] = None) -> bool:
        """
        Check if a record exists by a specific field.
        
        Args:
            field_name: Name of the field to check
            value: Value to match
            session: Optional database session
            
        Returns:
            True if exists, False otherwise
        """
        def _exists_by_field(session: Session) -> bool:
            field = getattr(self.model, field_name)
            return session.query(self.model).filter(field == value).first() is not None
        
        if session:
            return _exists_by_field(session)
        else:
            with get_db_session() as session:
                return _exists_by_field(session)


class QueryBuilder:
    """
    Helper class for building complex queries with method chaining.
    
    Usage:
        query = QueryBuilder(session, User)
        users = query.filter_by(active=True).order_by('created_at', desc=True).limit(10).all()
    """
    
    def __init__(self, session: Session, model: Type[ModelType]):
        """Initialize query builder."""
        self.session = session
        self.model = model
        self.query = session.query(model)
    
    def filter_by(self, **kwargs) -> 'QueryBuilder':
        """Add filter conditions."""
        for field_name, value in kwargs.items():
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                self.query = self.query.filter(field == value)
        return self
    
    def filter(self, *conditions) -> 'QueryBuilder':
        """Add custom filter conditions."""
        self.query = self.query.filter(*conditions)
        return self
    
    def filter_and(self, *conditions) -> 'QueryBuilder':
        """Add AND filter conditions."""
        self.query = self.query.filter(and_(*conditions))
        return self
    
    def filter_or(self, *conditions) -> 'QueryBuilder':
        """Add OR filter conditions."""
        self.query = self.query.filter(or_(*conditions))
        return self
    
    def order_by(self, field_name: str, desc: bool = False) -> 'QueryBuilder':
        """Add ordering."""
        if hasattr(self.model, field_name):
            field = getattr(self.model, field_name)
            if desc:
                self.query = self.query.order_by(field.desc())
            else:
                self.query = self.query.order_by(field.asc())
        return self
    
    def limit(self, limit: int) -> 'QueryBuilder':
        """Add limit."""
        self.query = self.query.limit(limit)
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Add offset."""
        self.query = self.query.offset(offset)
        return self
    
    def join(self, *args, **kwargs) -> 'QueryBuilder':
        """Add join."""
        self.query = self.query.join(*args, **kwargs)
        return self
    
    def outerjoin(self, *args, **kwargs) -> 'QueryBuilder':
        """Add outer join."""
        self.query = self.query.outerjoin(*args, **kwargs)
        return self
    
    def group_by(self, *fields) -> 'QueryBuilder':
        """Add group by."""
        self.query = self.query.group_by(*fields)
        return self
    
    def having(self, condition) -> 'QueryBuilder':
        """Add having condition."""
        self.query = self.query.having(condition)
        return self
    
    def distinct(self) -> 'QueryBuilder':
        """Add distinct."""
        self.query = self.query.distinct()
        return self
    
    def all(self) -> List[ModelType]:
        """Execute query and return all results."""
        return self.query.all()
    
    def first(self) -> Optional[ModelType]:
        """Execute query and return first result."""
        return self.query.first()
    
    def one(self) -> ModelType:
        """Execute query and return exactly one result."""
        return self.query.one()
    
    def one_or_none(self) -> Optional[ModelType]:
        """Execute query and return one result or None."""
        return self.query.one_or_none()
    
    def count(self) -> int:
        """Execute query and return count."""
        return self.query.count()
    
    def paginate(self, page: int, per_page: int) -> Dict[str, Any]:
        """
        Paginate query results.
        
        Args:
            page: Page number (1-based)
            per_page: Number of items per page
            
        Returns:
            Dictionary with pagination info and results
        """
        total = self.query.count()
        items = self.query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'has_prev': page > 1,
            'has_next': page * per_page < total
        }


class AdvancedRepository(BaseRepository[ModelType]):
    """
    Advanced repository with additional query capabilities.
    
    This class extends BaseRepository with more sophisticated query methods
    and bulk operations.
    """
    
    def get_query_builder(self, session: Optional[Session] = None) -> QueryBuilder:
        """
        Get a query builder for complex queries.
        
        Args:
            session: Optional database session
            
        Returns:
            QueryBuilder instance
        """
        if session:
            return QueryBuilder(session, self.model)
        else:
            # Note: This creates a new session that should be managed by the caller
            session = get_db_session().__enter__()
            return QueryBuilder(session, self.model)
    
    def bulk_create(self, objects: List[CreateSchemaType], session: Optional[Session] = None) -> List[ModelType]:
        """
        Create multiple records in bulk.
        
        Args:
            objects: List of objects to create
            session: Optional database session
            
        Returns:
            List of created model instances
        """
        def _bulk_create(session: Session) -> List[ModelType]:
            created_objects = []
            for obj_data in objects:
                created_obj = self.create(obj_data, session)
                created_objects.append(created_obj)
            return created_objects
        
        if session:
            return _bulk_create(session)
        else:
            with get_db_transaction() as session:
                return _bulk_create(session)
    
    def bulk_update(self, updates: List[Dict[str, Any]], session: Optional[Session] = None) -> int:
        """
        Update multiple records in bulk.
        
        Args:
            updates: List of dictionaries with 'id' and update fields
            session: Optional database session
            
        Returns:
            Number of updated records
        """
        def _bulk_update(session: Session) -> int:
            count = 0
            for update_data in updates:
                obj_id = update_data.pop('id')
                result = session.query(self.model).filter(self.model.id == obj_id).update(update_data)
                count += result
            return count
        
        if session:
            return _bulk_update(session)
        else:
            with get_db_transaction() as session:
                return _bulk_update(session)
    
    def search(
        self, 
        search_term: str, 
        search_fields: List[str], 
        skip: int = 0, 
        limit: int = 100,
        session: Optional[Session] = None
    ) -> List[ModelType]:
        """
        Search records across multiple fields.
        
        Args:
            search_term: Term to search for
            search_fields: List of field names to search in
            skip: Number of records to skip
            limit: Maximum number of records to return
            session: Optional database session
            
        Returns:
            List of matching model instances
        """
        def _search(session: Session) -> List[ModelType]:
            conditions = []
            for field_name in search_fields:
                if hasattr(self.model, field_name):
                    field = getattr(self.model, field_name)
                    conditions.append(field.ilike(f'%{search_term}%'))
            
            if conditions:
                return session.query(self.model).filter(or_(*conditions)).offset(skip).limit(limit).all()
            else:
                return []
        
        if session:
            return _search(session)
        else:
            with get_db_session() as session:
                return _search(session)
    
    def get_statistics(self, session: Optional[Session] = None) -> Dict[str, Any]:
        """
        Get basic statistics about the model.
        
        Args:
            session: Optional database session
            
        Returns:
            Dictionary with statistics
        """
        def _get_statistics(session: Session) -> Dict[str, Any]:
            stats = {
                'total_count': session.query(self.model).count()
            }
            
            # Add created_at statistics if the field exists
            if hasattr(self.model, 'created_at'):
                stats.update({
                    'oldest_record': session.query(func.min(self.model.created_at)).scalar(),
                    'newest_record': session.query(func.max(self.model.created_at)).scalar()
                })
            
            return stats
        
        if session:
            return _get_statistics(session)
        else:
            with get_db_session() as session:
                return _get_statistics(session)
