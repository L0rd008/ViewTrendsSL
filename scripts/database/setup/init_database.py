#!/usr/bin/env python3
"""
Database Initialization Script for ViewTrendsSL

This script initializes the database schema, creates necessary tables,
indexes, and sets up initial data for the ViewTrendsSL application.

Usage:
    python init_database.py [--drop-existing] [--sample-data]

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import argparse
import logging
from typing import Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from config.database.database_config import DatabaseConfig
from src.data_access.models.user import User
from src.data_access.models.channel import Channel
from src.data_access.models.video import Video
from src.data_access.models.snapshot import Snapshot
from src.data_access.models.tag import Tag, VideoTag

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handles database initialization and setup."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize the database initializer."""
        self.config = config or DatabaseConfig()
        self.db = None
        
    def connect(self):
        """Establish database connection."""
        try:
            self.db = self.config.get_connection()
            logger.info("✅ Database connection established")
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.db:
            self.db.close()
            logger.info("Database connection closed")
    
    def drop_tables(self):
        """Drop all existing tables."""
        logger.info("🗑️  Dropping existing tables...")
        
        tables_to_drop = [
            'video_tags',
            'snapshots', 
            'videos',
            'tags',
            'channels',
            'users'
        ]
        
        cursor = self.db.cursor()
        
        try:
            # Disable foreign key constraints temporarily
            if self.config.database_type == 'sqlite':
                cursor.execute("PRAGMA foreign_keys = OFF")
            elif self.config.database_type == 'postgresql':
                cursor.execute("SET session_replication_role = 'replica'")
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                    logger.info(f"  Dropped table: {table}")
                except Exception as e:
                    logger.warning(f"  Could not drop table {table}: {e}")
            
            # Re-enable foreign key constraints
            if self.config.database_type == 'sqlite':
                cursor.execute("PRAGMA foreign_keys = ON")
            elif self.config.database_type == 'postgresql':
                cursor.execute("SET session_replication_role = 'origin'")
            
            self.db.commit()
            logger.info("✅ All tables dropped successfully")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error dropping tables: {e}")
            raise
        finally:
            cursor.close()
    
    def create_tables(self):
        """Create all database tables."""
        logger.info("🏗️  Creating database tables...")
        
        cursor = self.db.cursor()
        
        try:
            # Users table
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(100),
                        last_name VARCHAR(100),
                        is_active BOOLEAN DEFAULT 1,
                        is_admin BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:  # PostgreSQL
                cursor.execute("""
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(100),
                        last_name VARCHAR(100),
                        is_active BOOLEAN DEFAULT TRUE,
                        is_admin BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            # Channels table
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    CREATE TABLE channels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_id VARCHAR(50) UNIQUE NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        subscriber_count INTEGER DEFAULT 0,
                        video_count INTEGER DEFAULT 0,
                        view_count INTEGER DEFAULT 0,
                        country VARCHAR(10),
                        language VARCHAR(10),
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:  # PostgreSQL
                cursor.execute("""
                    CREATE TABLE channels (
                        id SERIAL PRIMARY KEY,
                        channel_id VARCHAR(50) UNIQUE NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        subscriber_count BIGINT DEFAULT 0,
                        video_count INTEGER DEFAULT 0,
                        view_count BIGINT DEFAULT 0,
                        country VARCHAR(10),
                        language VARCHAR(10),
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            # Tags table
            cursor.execute("""
                CREATE TABLE tags (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Videos table
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    CREATE TABLE videos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_id VARCHAR(50) UNIQUE NOT NULL,
                        channel_id INTEGER NOT NULL,
                        title VARCHAR(500) NOT NULL,
                        description TEXT,
                        published_at TIMESTAMP NOT NULL,
                        duration_seconds INTEGER,
                        category_id INTEGER,
                        is_short BOOLEAN DEFAULT 0,
                        language VARCHAR(10),
                        view_count INTEGER DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        comment_count INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (channel_id) REFERENCES channels (id) ON DELETE CASCADE
                    )
                """)
            else:  # PostgreSQL
                cursor.execute("""
                    CREATE TABLE videos (
                        id SERIAL PRIMARY KEY,
                        video_id VARCHAR(50) UNIQUE NOT NULL,
                        channel_id INTEGER NOT NULL,
                        title VARCHAR(500) NOT NULL,
                        description TEXT,
                        published_at TIMESTAMP NOT NULL,
                        duration_seconds INTEGER,
                        category_id INTEGER,
                        is_short BOOLEAN DEFAULT FALSE,
                        language VARCHAR(10),
                        view_count BIGINT DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        comment_count INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (channel_id) REFERENCES channels (id) ON DELETE CASCADE
                    )
                """)
            
            # Video Tags junction table
            cursor.execute("""
                CREATE TABLE video_tags (
                    video_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    PRIMARY KEY (video_id, tag_id),
                    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
                )
            """)
            
            # Snapshots table for time-series data
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    CREATE TABLE snapshots (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_id INTEGER NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        view_count INTEGER DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        comment_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
                    )
                """)
            else:  # PostgreSQL
                cursor.execute("""
                    CREATE TABLE snapshots (
                        id SERIAL PRIMARY KEY,
                        video_id INTEGER NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        view_count BIGINT DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        comment_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
                    )
                """)
            
            self.db.commit()
            logger.info("✅ All tables created successfully")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating tables: {e}")
            raise
        finally:
            cursor.close()
    
    def create_indexes(self):
        """Create database indexes for performance."""
        logger.info("📊 Creating database indexes...")
        
        cursor = self.db.cursor()
        
        try:
            indexes = [
                # Users indexes
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)",
                "CREATE INDEX IF NOT EXISTS idx_users_active ON users (is_active)",
                
                # Channels indexes
                "CREATE INDEX IF NOT EXISTS idx_channels_channel_id ON channels (channel_id)",
                "CREATE INDEX IF NOT EXISTS idx_channels_country ON channels (country)",
                "CREATE INDEX IF NOT EXISTS idx_channels_active ON channels (is_active)",
                
                # Videos indexes
                "CREATE INDEX IF NOT EXISTS idx_videos_video_id ON videos (video_id)",
                "CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos (channel_id)",
                "CREATE INDEX IF NOT EXISTS idx_videos_published_at ON videos (published_at)",
                "CREATE INDEX IF NOT EXISTS idx_videos_category ON videos (category_id)",
                "CREATE INDEX IF NOT EXISTS idx_videos_is_short ON videos (is_short)",
                "CREATE INDEX IF NOT EXISTS idx_videos_active ON videos (is_active)",
                "CREATE INDEX IF NOT EXISTS idx_videos_views ON videos (view_count)",
                
                # Snapshots indexes (critical for time-series queries)
                "CREATE INDEX IF NOT EXISTS idx_snapshots_video_timestamp ON snapshots (video_id, timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp ON snapshots (timestamp)",
                
                # Tags indexes
                "CREATE INDEX IF NOT EXISTS idx_tags_name ON tags (name)",
                "CREATE INDEX IF NOT EXISTS idx_video_tags_video ON video_tags (video_id)",
                "CREATE INDEX IF NOT EXISTS idx_video_tags_tag ON video_tags (tag_id)",
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
                logger.info(f"  Created index: {index_sql.split('ON')[1].split('(')[0].strip()}")
            
            self.db.commit()
            logger.info("✅ All indexes created successfully")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating indexes: {e}")
            raise
        finally:
            cursor.close()
    
    def insert_sample_data(self):
        """Insert sample data for testing."""
        logger.info("📝 Inserting sample data...")
        
        cursor = self.db.cursor()
        
        try:
            # Sample admin user
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, is_admin)
                    VALUES (?, ?, ?, ?, ?)
                """, ('admin@viewtrendssl.com', 'hashed_password_here', 'Admin', 'User', True))
            else:  # PostgreSQL
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, is_admin)
                    VALUES (%s, %s, %s, %s, %s)
                """, ('admin@viewtrendssl.com', 'hashed_password_here', 'Admin', 'User', True))
            
            # Sample channels
            sample_channels = [
                ('UCxxxxxx1', 'Sample Sri Lankan News Channel', 'News and current affairs', 100000, 500, 'LK', 'si'),
                ('UCxxxxxx2', 'Sample Entertainment Channel', 'Entertainment content', 50000, 200, 'LK', 'en'),
                ('UCxxxxxx3', 'Sample Educational Channel', 'Educational videos', 25000, 100, 'LK', 'en'),
            ]
            
            for channel_data in sample_channels:
                if self.config.database_type == 'sqlite':
                    cursor.execute("""
                        INSERT INTO channels (channel_id, title, description, subscriber_count, video_count, country, language)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, channel_data)
                else:  # PostgreSQL
                    cursor.execute("""
                        INSERT INTO channels (channel_id, title, description, subscriber_count, video_count, country, language)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, channel_data)
            
            # Sample tags
            sample_tags = ['news', 'entertainment', 'education', 'sri lanka', 'sinhala', 'tamil', 'english']
            for tag in sample_tags:
                if self.config.database_type == 'sqlite':
                    cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
                else:  # PostgreSQL
                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
            
            self.db.commit()
            logger.info("✅ Sample data inserted successfully")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error inserting sample data: {e}")
            raise
        finally:
            cursor.close()
    
    def verify_setup(self):
        """Verify that the database setup is correct."""
        logger.info("🔍 Verifying database setup...")
        
        cursor = self.db.cursor()
        
        try:
            # Check if all tables exist
            if self.config.database_type == 'sqlite':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            else:  # PostgreSQL
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
            
            tables = [row[0] for row in cursor.fetchall()]
            expected_tables = ['users', 'channels', 'videos', 'tags', 'video_tags', 'snapshots']
            
            missing_tables = set(expected_tables) - set(tables)
            if missing_tables:
                logger.error(f"❌ Missing tables: {missing_tables}")
                return False
            
            # Check table counts
            for table in expected_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logger.info(f"  {table}: {count} records")
            
            logger.info("✅ Database verification completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database verification failed: {e}")
            return False
        finally:
            cursor.close()


def main():
    """Main function to initialize the database."""
    parser = argparse.ArgumentParser(description='Initialize ViewTrendsSL database')
    parser.add_argument('--drop-existing', action='store_true',
                       help='Drop existing tables before creating new ones')
    parser.add_argument('--sample-data', action='store_true',
                       help='Insert sample data for testing')
    parser.add_argument('--verify-only', action='store_true',
                       help='Only verify the database setup')
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting ViewTrendsSL database initialization...")
    
    initializer = DatabaseInitializer()
    
    try:
        initializer.connect()
        
        if args.verify_only:
            success = initializer.verify_setup()
            sys.exit(0 if success else 1)
        
        if args.drop_existing:
            initializer.drop_tables()
        
        initializer.create_tables()
        initializer.create_indexes()
        
        if args.sample_data:
            initializer.insert_sample_data()
        
        success = initializer.verify_setup()
        
        if success:
            logger.info("🎉 Database initialization completed successfully!")
        else:
            logger.error("❌ Database initialization failed verification")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    finally:
        initializer.disconnect()


if __name__ == '__main__':
    main()
