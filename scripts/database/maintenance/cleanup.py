#!/usr/bin/env python3
"""
Database Maintenance and Cleanup Script for ViewTrendsSL

This script performs routine database maintenance tasks including:
- Cleaning up old data
- Optimizing database performance
- Analyzing table statistics
- Removing orphaned records

Usage:
    python cleanup.py [--dry-run] [--vacuum] [--analyze] [--cleanup-old-data]

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from config.database.database_config import DatabaseConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseMaintenance:
    """Handles database maintenance and cleanup operations."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize the database maintenance handler."""
        self.config = config or DatabaseConfig()
        self.db = None
        
        # Maintenance settings
        self.snapshot_retention_days = int(os.getenv('SNAPSHOT_RETENTION_DAYS', '90'))
        self.inactive_video_days = int(os.getenv('INACTIVE_VIDEO_DAYS', '365'))
        self.log_retention_days = int(os.getenv('LOG_RETENTION_DAYS', '30'))
        
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
    
    def get_table_stats(self) -> Dict[str, Dict]:
        """Get statistics for all tables."""
        logger.info("📊 Gathering table statistics...")
        
        cursor = self.db.cursor()
        stats = {}
        
        try:
            tables = ['users', 'channels', 'videos', 'tags', 'video_tags', 'snapshots']
            
            for table in tables:
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                
                # Get table size (database-specific)
                if self.config.database_type == 'sqlite':
                    # For SQLite, we can't easily get table size
                    table_size = 0
                elif self.config.database_type == 'postgresql':
                    cursor.execute(f"""
                        SELECT pg_total_relation_size('{table}') as size
                    """)
                    result = cursor.fetchone()
                    table_size = result[0] if result else 0
                else:
                    table_size = 0
                
                stats[table] = {
                    'rows': row_count,
                    'size_bytes': table_size,
                    'size_mb': round(table_size / (1024 * 1024), 2) if table_size > 0 else 0
                }
                
                logger.info(f"  {table}: {row_count:,} rows ({stats[table]['size_mb']} MB)")
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error gathering table statistics: {e}")
            return {}
        finally:
            cursor.close()
    
    def cleanup_old_snapshots(self, dry_run: bool = False) -> int:
        """Remove old snapshot records beyond retention period."""
        logger.info(f"🧹 Cleaning up snapshots older than {self.snapshot_retention_days} days...")
        
        cursor = self.db.cursor()
        
        try:
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=self.snapshot_retention_days)
            
            # First, count how many records will be affected
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    SELECT COUNT(*) FROM snapshots 
                    WHERE timestamp < ?
                """, (cutoff_date,))
            else:  # PostgreSQL
                cursor.execute("""
                    SELECT COUNT(*) FROM snapshots 
                    WHERE timestamp < %s
                """, (cutoff_date,))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("  No old snapshots to clean up")
                return 0
            
            logger.info(f"  Found {count:,} old snapshot records")
            
            if not dry_run:
                # Delete old snapshots
                if self.config.database_type == 'sqlite':
                    cursor.execute("""
                        DELETE FROM snapshots 
                        WHERE timestamp < ?
                    """, (cutoff_date,))
                else:  # PostgreSQL
                    cursor.execute("""
                        DELETE FROM snapshots 
                        WHERE timestamp < %s
                    """, (cutoff_date,))
                
                self.db.commit()
                logger.info(f"✅ Deleted {count:,} old snapshot records")
            else:
                logger.info(f"  [DRY RUN] Would delete {count:,} old snapshot records")
            
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error cleaning up old snapshots: {e}")
            return 0
        finally:
            cursor.close()
    
    def cleanup_inactive_videos(self, dry_run: bool = False) -> int:
        """Mark videos as inactive if they haven't been updated recently."""
        logger.info(f"🧹 Marking videos inactive after {self.inactive_video_days} days...")
        
        cursor = self.db.cursor()
        
        try:
            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=self.inactive_video_days)
            
            # Count videos that will be marked inactive
            if self.config.database_type == 'sqlite':
                cursor.execute("""
                    SELECT COUNT(*) FROM videos 
                    WHERE updated_at < ? AND is_active = 1
                """, (cutoff_date,))
            else:  # PostgreSQL
                cursor.execute("""
                    SELECT COUNT(*) FROM videos 
                    WHERE updated_at < %s AND is_active = TRUE
                """, (cutoff_date,))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("  No videos to mark as inactive")
                return 0
            
            logger.info(f"  Found {count:,} videos to mark as inactive")
            
            if not dry_run:
                # Mark videos as inactive
                if self.config.database_type == 'sqlite':
                    cursor.execute("""
                        UPDATE videos 
                        SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                        WHERE updated_at < ? AND is_active = 1
                    """, (cutoff_date,))
                else:  # PostgreSQL
                    cursor.execute("""
                        UPDATE videos 
                        SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                        WHERE updated_at < %s AND is_active = TRUE
                    """, (cutoff_date,))
                
                self.db.commit()
                logger.info(f"✅ Marked {count:,} videos as inactive")
            else:
                logger.info(f"  [DRY RUN] Would mark {count:,} videos as inactive")
            
            return count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error marking videos as inactive: {e}")
            return 0
        finally:
            cursor.close()
    
    def cleanup_orphaned_records(self, dry_run: bool = False) -> Dict[str, int]:
        """Remove orphaned records that reference non-existent parent records."""
        logger.info("🧹 Cleaning up orphaned records...")
        
        cursor = self.db.cursor()
        cleanup_counts = {}
        
        try:
            # Clean up orphaned video_tags (tags that reference non-existent videos)
            cursor.execute("""
                SELECT COUNT(*) FROM video_tags vt
                LEFT JOIN videos v ON vt.video_id = v.id
                WHERE v.id IS NULL
            """)
            orphaned_video_tags = cursor.fetchone()[0]
            
            if orphaned_video_tags > 0:
                logger.info(f"  Found {orphaned_video_tags:,} orphaned video_tags records")
                
                if not dry_run:
                    cursor.execute("""
                        DELETE FROM video_tags 
                        WHERE video_id NOT IN (SELECT id FROM videos)
                    """)
                    logger.info(f"✅ Deleted {orphaned_video_tags:,} orphaned video_tags")
                else:
                    logger.info(f"  [DRY RUN] Would delete {orphaned_video_tags:,} orphaned video_tags")
            
            cleanup_counts['video_tags'] = orphaned_video_tags
            
            # Clean up orphaned snapshots (snapshots for non-existent videos)
            cursor.execute("""
                SELECT COUNT(*) FROM snapshots s
                LEFT JOIN videos v ON s.video_id = v.id
                WHERE v.id IS NULL
            """)
            orphaned_snapshots = cursor.fetchone()[0]
            
            if orphaned_snapshots > 0:
                logger.info(f"  Found {orphaned_snapshots:,} orphaned snapshot records")
                
                if not dry_run:
                    cursor.execute("""
                        DELETE FROM snapshots 
                        WHERE video_id NOT IN (SELECT id FROM videos)
                    """)
                    logger.info(f"✅ Deleted {orphaned_snapshots:,} orphaned snapshots")
                else:
                    logger.info(f"  [DRY RUN] Would delete {orphaned_snapshots:,} orphaned snapshots")
            
            cleanup_counts['snapshots'] = orphaned_snapshots
            
            # Clean up unused tags (tags not referenced by any video)
            cursor.execute("""
                SELECT COUNT(*) FROM tags t
                LEFT JOIN video_tags vt ON t.id = vt.tag_id
                WHERE vt.tag_id IS NULL
            """)
            unused_tags = cursor.fetchone()[0]
            
            if unused_tags > 0:
                logger.info(f"  Found {unused_tags:,} unused tag records")
                
                if not dry_run:
                    cursor.execute("""
                        DELETE FROM tags 
                        WHERE id NOT IN (SELECT DISTINCT tag_id FROM video_tags)
                    """)
                    logger.info(f"✅ Deleted {unused_tags:,} unused tags")
                else:
                    logger.info(f"  [DRY RUN] Would delete {unused_tags:,} unused tags")
            
            cleanup_counts['tags'] = unused_tags
            
            if not dry_run:
                self.db.commit()
            
            return cleanup_counts
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error cleaning up orphaned records: {e}")
            return {}
        finally:
            cursor.close()
    
    def vacuum_database(self) -> bool:
        """Perform database vacuum/optimization."""
        logger.info("🔧 Performing database vacuum/optimization...")
        
        cursor = self.db.cursor()
        
        try:
            if self.config.database_type == 'sqlite':
                # SQLite VACUUM
                cursor.execute("VACUUM")
                logger.info("✅ SQLite VACUUM completed")
                
            elif self.config.database_type == 'postgresql':
                # PostgreSQL VACUUM ANALYZE
                # Note: VACUUM cannot be run inside a transaction
                self.db.autocommit = True
                cursor.execute("VACUUM ANALYZE")
                self.db.autocommit = False
                logger.info("✅ PostgreSQL VACUUM ANALYZE completed")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Database vacuum failed: {e}")
            return False
        finally:
            cursor.close()
    
    def analyze_database(self) -> bool:
        """Update database statistics for query optimization."""
        logger.info("📈 Analyzing database statistics...")
        
        cursor = self.db.cursor()
        
        try:
            if self.config.database_type == 'sqlite':
                # SQLite ANALYZE
                cursor.execute("ANALYZE")
                logger.info("✅ SQLite ANALYZE completed")
                
            elif self.config.database_type == 'postgresql':
                # PostgreSQL ANALYZE
                cursor.execute("ANALYZE")
                logger.info("✅ PostgreSQL ANALYZE completed")
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Database analysis failed: {e}")
            return False
        finally:
            cursor.close()
    
    def get_maintenance_report(self) -> Dict:
        """Generate a comprehensive maintenance report."""
        logger.info("📋 Generating maintenance report...")
        
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'database_type': self.config.database_type,
                'table_stats': self.get_table_stats(),
                'settings': {
                    'snapshot_retention_days': self.snapshot_retention_days,
                    'inactive_video_days': self.inactive_video_days,
                    'log_retention_days': self.log_retention_days
                }
            }
            
            # Calculate totals
            total_rows = sum(stats['rows'] for stats in report['table_stats'].values())
            total_size_mb = sum(stats['size_mb'] for stats in report['table_stats'].values())
            
            report['totals'] = {
                'total_rows': total_rows,
                'total_size_mb': total_size_mb
            }
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating maintenance report: {e}")
            return {}


def main():
    """Main function to perform database maintenance."""
    parser = argparse.ArgumentParser(description='ViewTrendsSL database maintenance')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--vacuum', action='store_true',
                       help='Perform database vacuum/optimization')
    parser.add_argument('--analyze', action='store_true',
                       help='Update database statistics')
    parser.add_argument('--cleanup-old-data', action='store_true',
                       help='Clean up old snapshots and inactive videos')
    parser.add_argument('--cleanup-orphaned', action='store_true',
                       help='Remove orphaned records')
    parser.add_argument('--report', action='store_true',
                       help='Generate maintenance report')
    parser.add_argument('--all', action='store_true',
                       help='Perform all maintenance tasks')
    
    args = parser.parse_args()
    
    # If no specific tasks are specified, show help
    if not any([args.vacuum, args.analyze, args.cleanup_old_data, 
                args.cleanup_orphaned, args.report, args.all]):
        parser.print_help()
        return
    
    maintenance = DatabaseMaintenance()
    
    try:
        maintenance.connect()
        
        logger.info("🚀 Starting ViewTrendsSL database maintenance...")
        
        if args.dry_run:
            logger.info("🔍 DRY RUN MODE - No changes will be made")
        
        # Generate initial report
        if args.report or args.all:
            report = maintenance.get_maintenance_report()
            logger.info(f"📊 Database contains {report['totals']['total_rows']:,} total rows "
                       f"({report['totals']['total_size_mb']:.2f} MB)")
        
        # Cleanup tasks
        if args.cleanup_old_data or args.all:
            snapshots_cleaned = maintenance.cleanup_old_snapshots(dry_run=args.dry_run)
            videos_marked_inactive = maintenance.cleanup_inactive_videos(dry_run=args.dry_run)
            
            logger.info(f"📊 Cleanup summary: {snapshots_cleaned:,} snapshots, "
                       f"{videos_marked_inactive:,} videos marked inactive")
        
        if args.cleanup_orphaned or args.all:
            orphaned_counts = maintenance.cleanup_orphaned_records(dry_run=args.dry_run)
            total_orphaned = sum(orphaned_counts.values())
            logger.info(f"📊 Orphaned records cleaned: {total_orphaned:,} total")
        
        # Optimization tasks (skip in dry-run mode)
        if not args.dry_run:
            if args.vacuum or args.all:
                maintenance.vacuum_database()
            
            if args.analyze or args.all:
                maintenance.analyze_database()
        
        logger.info("🎉 Database maintenance completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database maintenance failed: {e}")
        sys.exit(1)
    finally:
        maintenance.disconnect()


if __name__ == '__main__':
    main()
