"""
Test Database Setup

This module provides utilities for setting up and managing test databases
for the ViewTrendsSL application.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sqlite3
import tempfile
from typing import Dict, Any, List, Optional
from contextlib import contextmanager
from datetime import datetime

from tests.fixtures.mock_data import (
    generate_bulk_mock_data,
    create_sri_lankan_content_scenario,
    create_mixed_content_scenario
)


class TestDatabaseManager:
    """Manages test database creation and population."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize test database manager.
        
        Args:
            db_path: Path to database file. If None, creates temporary file.
        """
        if db_path is None:
            self.temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            self.db_path = self.temp_file.name
            self.temp_file.close()
        else:
            self.db_path = db_path
            self.temp_file = None
    
    def create_schema(self) -> None:
        """Create the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Channels table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    subscriber_count INTEGER DEFAULT 0,
                    video_count INTEGER DEFAULT 0,
                    country TEXT,
                    view_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT
                )
            ''')
            
            # Videos table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT UNIQUE NOT NULL,
                    channel_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    published_at TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    is_short BOOLEAN NOT NULL,
                    category_id TEXT,
                    view_count INTEGER DEFAULT 0,
                    like_count INTEGER DEFAULT 0,
                    comment_count INTEGER DEFAULT 0,
                    tags TEXT,
                    thumbnail_url TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
                )
            ''')
            
            # Predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    user_id INTEGER,
                    prediction_type TEXT NOT NULL,
                    predicted_views_24h INTEGER,
                    predicted_views_7d INTEGER,
                    predicted_views_30d INTEGER,
                    confidence_score REAL,
                    features TEXT,
                    model_version TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (video_id) REFERENCES videos (video_id)
                )
            ''')
            
            # Performance snapshots table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    view_count INTEGER NOT NULL,
                    like_count INTEGER DEFAULT 0,
                    comment_count INTEGER DEFAULT 0,
                    hours_since_publish REAL,
                    collected_at TEXT NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos (video_id)
                )
            ''')
            
            # API usage tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key_hash TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    quota_cost INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos (channel_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_published_at ON videos (published_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_videos_is_short ON videos (is_short)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_video_id ON predictions (video_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions (user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_video_id ON performance_snapshots (video_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp ON performance_snapshots (timestamp)')
            
            conn.commit()
    
    def populate_with_mock_data(self, scenario: str = 'mixed') -> Dict[str, Any]:
        """
        Populate database with mock data.
        
        Args:
            scenario: Type of scenario ('mixed', 'sri_lankan', 'bulk')
            
        Returns:
            Dictionary containing the inserted data
        """
        if scenario == 'sri_lankan':
            data = create_sri_lankan_content_scenario()
        elif scenario == 'mixed':
            data = create_mixed_content_scenario()
        elif scenario == 'bulk':
            data = generate_bulk_mock_data(num_videos=200, num_channels=50, num_users=20)
        else:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert channels
            for channel in data.get('channels', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO channels 
                    (channel_id, title, description, subscriber_count, video_count, 
                     country, view_count, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    channel['channel_id'],
                    channel['title'],
                    channel.get('description', ''),
                    channel['subscriber_count'],
                    channel['video_count'],
                    channel.get('country', 'LK'),
                    channel.get('view_count', 0),
                    channel['created_at']
                ))
            
            # Insert videos
            for video in data.get('videos', []):
                tags_str = ','.join(video.get('tags', [])) if video.get('tags') else ''
                cursor.execute('''
                    INSERT OR REPLACE INTO videos 
                    (video_id, channel_id, title, description, published_at, 
                     duration_seconds, is_short, category_id, view_count, 
                     like_count, comment_count, tags, thumbnail_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video['video_id'],
                    video['channel_id'],
                    video['title'],
                    video.get('description', ''),
                    video['published_at'],
                    video['duration_seconds'],
                    video['is_short'],
                    video.get('category_id', '22'),
                    video.get('view_count', 0),
                    video.get('like_count', 0),
                    video.get('comment_count', 0),
                    tags_str,
                    video.get('thumbnail_url', ''),
                    video.get('created_at', datetime.now().isoformat())
                ))
            
            # Insert users
            for user in data.get('users', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO users 
                    (email, password_hash, created_at, is_active)
                    VALUES (?, ?, ?, ?)
                ''', (
                    user['email'],
                    user.get('password', 'hashed_password'),
                    user.get('created_at', datetime.now().isoformat()),
                    user.get('is_active', True)
                ))
            
            # Insert predictions
            for prediction in data.get('predictions', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO predictions 
                    (video_id, user_id, prediction_type, predicted_views_24h, 
                     predicted_views_7d, predicted_views_30d, confidence_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    prediction['video_id'],
                    prediction.get('user_id'),
                    prediction['prediction_type'],
                    prediction.get('predicted_views_24h', 0),
                    prediction.get('predicted_views_7d', 0),
                    prediction.get('predicted_views_30d', 0),
                    prediction.get('confidence_score', 0.5),
                    prediction['created_at']
                ))
            
            # Insert performance data
            for snapshot in data.get('performance_data', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO performance_snapshots 
                    (video_id, timestamp, view_count, like_count, comment_count, 
                     hours_since_publish, collected_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    snapshot['video_id'],
                    snapshot['timestamp'],
                    snapshot['view_count'],
                    snapshot.get('like_count', 0),
                    snapshot.get('comment_count', 0),
                    snapshot.get('hours_since_publish', 0),
                    snapshot.get('collected_at', snapshot['timestamp'])
                ))
            
            conn.commit()
        
        return data
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Count records in each table
            tables = ['users', 'channels', 'videos', 'predictions', 'performance_snapshots']
            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                stats[table] = cursor.fetchone()[0]
            
            # Additional stats
            cursor.execute('SELECT COUNT(*) FROM videos WHERE is_short = 1')
            stats['shorts_videos'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM videos WHERE is_short = 0')
            stats['longform_videos'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT channel_id) FROM videos')
            stats['active_channels'] = cursor.fetchone()[0]
            
            return stats
    
    def clear_data(self) -> None:
        """Clear all data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Clear all tables
            tables = [
                'performance_snapshots', 'predictions', 'videos', 
                'channels', 'users', 'api_usage'
            ]
            
            for table in tables:
                cursor.execute(f'DELETE FROM {table}')
            
            conn.commit()
    
    def cleanup(self) -> None:
        """Clean up the test database."""
        if self.temp_file and os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    @contextmanager
    def get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List of result dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
    
    def insert_test_user(self, email: str = "test@example.com", password_hash: str = "hashed") -> int:
        """Insert a test user and return the user ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (email, password_hash, created_at, is_active)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, datetime.now().isoformat(), True))
            conn.commit()
            return cursor.lastrowid
    
    def insert_test_channel(self, channel_id: str = None, title: str = "Test Channel") -> str:
        """Insert a test channel and return the channel ID."""
        if channel_id is None:
            from tests.fixtures.mock_data import generate_channel_id
            channel_id = generate_channel_id()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO channels 
                (channel_id, title, subscriber_count, video_count, country, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (channel_id, title, 10000, 100, 'LK', datetime.now().isoformat()))
            conn.commit()
            return channel_id
    
    def insert_test_video(
        self, 
        video_id: str = None, 
        channel_id: str = None, 
        is_short: bool = False
    ) -> str:
        """Insert a test video and return the video ID."""
        if video_id is None:
            from tests.fixtures.mock_data import generate_video_id
            video_id = generate_video_id()
        
        if channel_id is None:
            channel_id = self.insert_test_channel()
        
        duration = 45 if is_short else 300
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO videos 
                (video_id, channel_id, title, published_at, duration_seconds, 
                 is_short, category_id, view_count, like_count, comment_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_id, channel_id, "Test Video", 
                datetime.now().isoformat() + 'Z',
                duration, is_short, '22', 1000, 50, 10,
                datetime.now().isoformat()
            ))
            conn.commit()
            return video_id


def create_test_database(scenario: str = 'mixed') -> TestDatabaseManager:
    """
    Create and populate a test database.
    
    Args:
        scenario: Type of scenario to populate with
        
    Returns:
        TestDatabaseManager instance
    """
    db_manager = TestDatabaseManager()
    db_manager.create_schema()
    db_manager.populate_with_mock_data(scenario)
    return db_manager


def create_empty_test_database() -> TestDatabaseManager:
    """
    Create an empty test database with schema only.
    
    Returns:
        TestDatabaseManager instance
    """
    db_manager = TestDatabaseManager()
    db_manager.create_schema()
    return db_manager


@contextmanager
def temporary_test_database(scenario: str = 'mixed'):
    """
    Context manager for temporary test database.
    
    Args:
        scenario: Type of scenario to populate with
        
    Yields:
        TestDatabaseManager instance
    """
    db_manager = create_test_database(scenario)
    try:
        yield db_manager
    finally:
        db_manager.cleanup()


@contextmanager
def empty_test_database():
    """
    Context manager for empty test database.
    
    Yields:
        TestDatabaseManager instance
    """
    db_manager = create_empty_test_database()
    try:
        yield db_manager
    finally:
        db_manager.cleanup()


class DatabaseAssertion:
    """Helper class for database assertions in tests."""
    
    def __init__(self, db_manager: TestDatabaseManager):
        self.db_manager = db_manager
    
    def assert_table_count(self, table: str, expected_count: int) -> None:
        """Assert that a table has the expected number of records."""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            actual_count = cursor.fetchone()[0]
            
        assert actual_count == expected_count, \
            f"Expected {expected_count} records in {table}, got {actual_count}"
    
    def assert_record_exists(self, table: str, **conditions) -> None:
        """Assert that a record exists with the given conditions."""
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(conditions.values()))
            count = cursor.fetchone()[0]
        
        assert count > 0, f"No record found in {table} with conditions {conditions}"
    
    def assert_record_not_exists(self, table: str, **conditions) -> None:
        """Assert that no record exists with the given conditions."""
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(conditions.values()))
            count = cursor.fetchone()[0]
        
        assert count == 0, f"Found {count} records in {table} with conditions {conditions}"
    
    def get_record(self, table: str, **conditions) -> Optional[Dict[str, Any]]:
        """Get a single record with the given conditions."""
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
        
        results = self.db_manager.execute_query(query, tuple(conditions.values()))
        return results[0] if results else None
