#!/usr/bin/env python3
"""
Database Backup Script for ViewTrendsSL

This script creates backups of the ViewTrendsSL database with support for
both SQLite and PostgreSQL databases. It includes compression, rotation,
and cloud storage options.

Usage:
    python backup_database.py [--compress] [--rotate] [--upload-cloud]

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import argparse
import logging
import gzip
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from config.database.database_config import DatabaseConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseBackup:
    """Handles database backup operations."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize the database backup handler."""
        self.config = config or DatabaseConfig()
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup settings
        self.max_backups = int(os.getenv('MAX_BACKUPS', '7'))  # Keep 7 days by default
        self.compress_backups = True
        
    def create_backup_filename(self, compressed: bool = True) -> str:
        """Create a timestamped backup filename."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        db_type = self.config.database_type
        
        if compressed:
            return f"viewtrendssl_{db_type}_backup_{timestamp}.sql.gz"
        else:
            return f"viewtrendssl_{db_type}_backup_{timestamp}.sql"
    
    def backup_sqlite(self, output_file: Path) -> bool:
        """Create a backup of SQLite database."""
        try:
            logger.info(f"Creating SQLite backup: {output_file}")
            
            # Get database file path
            db_path = self.config.database_url.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                logger.error(f"Database file not found: {db_path}")
                return False
            
            # Create SQL dump using sqlite3 command
            with open(output_file, 'w') as f:
                result = subprocess.run([
                    'sqlite3', db_path, '.dump'
                ], stdout=f, stderr=subprocess.PIPE, text=True)
                
                if result.returncode != 0:
                    logger.error(f"SQLite dump failed: {result.stderr}")
                    return False
            
            logger.info(f"✅ SQLite backup created: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ SQLite backup failed: {e}")
            return False
    
    def backup_postgresql(self, output_file: Path) -> bool:
        """Create a backup of PostgreSQL database."""
        try:
            logger.info(f"Creating PostgreSQL backup: {output_file}")
            
            # Parse database URL
            db_url = self.config.database_url
            if not db_url.startswith('postgresql://'):
                logger.error("Invalid PostgreSQL URL")
                return False
            
            # Extract connection details
            # Format: postgresql://user:password@host:port/database
            url_parts = db_url.replace('postgresql://', '').split('/')
            db_name = url_parts[-1]
            connection_part = url_parts[0]
            
            if '@' in connection_part:
                auth_part, host_part = connection_part.split('@')
                if ':' in auth_part:
                    username, password = auth_part.split(':')
                else:
                    username = auth_part
                    password = ''
            else:
                host_part = connection_part
                username = 'postgres'
                password = ''
            
            if ':' in host_part:
                host, port = host_part.split(':')
            else:
                host = host_part
                port = '5432'
            
            # Set environment variables for pg_dump
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            # Create backup using pg_dump
            cmd = [
                'pg_dump',
                '-h', host,
                '-p', port,
                '-U', username,
                '-d', db_name,
                '--no-password',
                '--verbose',
                '--clean',
                '--if-exists',
                '--create'
            ]
            
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd, 
                    stdout=f, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    env=env
                )
                
                if result.returncode != 0:
                    logger.error(f"pg_dump failed: {result.stderr}")
                    return False
            
            logger.info(f"✅ PostgreSQL backup created: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL backup failed: {e}")
            return False
    
    def compress_backup(self, sql_file: Path) -> Optional[Path]:
        """Compress a SQL backup file using gzip."""
        try:
            compressed_file = sql_file.with_suffix('.sql.gz')
            
            logger.info(f"Compressing backup: {sql_file} -> {compressed_file}")
            
            with open(sql_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original uncompressed file
            sql_file.unlink()
            
            # Calculate compression ratio
            original_size = sql_file.stat().st_size if sql_file.exists() else 0
            compressed_size = compressed_file.stat().st_size
            
            if original_size > 0:
                ratio = (1 - compressed_size / original_size) * 100
                logger.info(f"✅ Compression completed: {ratio:.1f}% reduction")
            
            return compressed_file
            
        except Exception as e:
            logger.error(f"❌ Compression failed: {e}")
            return None
    
    def rotate_backups(self) -> None:
        """Remove old backup files based on retention policy."""
        try:
            logger.info(f"Rotating backups (keeping {self.max_backups} most recent)")
            
            # Get all backup files
            backup_files = list(self.backup_dir.glob("viewtrendssl_*_backup_*.sql*"))
            
            if len(backup_files) <= self.max_backups:
                logger.info(f"Only {len(backup_files)} backups found, no rotation needed")
                return
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest files
            files_to_remove = backup_files[:-self.max_backups]
            
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    logger.info(f"  Removed old backup: {file_path.name}")
                except Exception as e:
                    logger.warning(f"  Could not remove {file_path.name}: {e}")
            
            logger.info(f"✅ Backup rotation completed")
            
        except Exception as e:
            logger.error(f"❌ Backup rotation failed: {e}")
    
    def get_backup_info(self) -> dict:
        """Get information about existing backups."""
        try:
            backup_files = list(self.backup_dir.glob("viewtrendssl_*_backup_*.sql*"))
            
            backups = []
            total_size = 0
            
            for backup_file in backup_files:
                stat = backup_file.stat()
                size_mb = stat.st_size / (1024 * 1024)
                total_size += size_mb
                
                backups.append({
                    'filename': backup_file.name,
                    'size_mb': round(size_mb, 2),
                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'compressed': backup_file.suffix == '.gz'
                })
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return {
                'total_backups': len(backups),
                'total_size_mb': round(total_size, 2),
                'backups': backups
            }
            
        except Exception as e:
            logger.error(f"Error getting backup info: {e}")
            return {'total_backups': 0, 'total_size_mb': 0, 'backups': []}
    
    def verify_backup(self, backup_file: Path) -> bool:
        """Verify that a backup file is valid."""
        try:
            logger.info(f"Verifying backup: {backup_file}")
            
            if not backup_file.exists():
                logger.error("Backup file does not exist")
                return False
            
            # Check file size
            size = backup_file.stat().st_size
            if size == 0:
                logger.error("Backup file is empty")
                return False
            
            # For compressed files, try to read the header
            if backup_file.suffix == '.gz':
                try:
                    with gzip.open(backup_file, 'rt') as f:
                        # Read first few lines to verify it's a valid SQL dump
                        first_lines = [f.readline() for _ in range(5)]
                        
                    # Check for SQL dump indicators
                    content = ''.join(first_lines).lower()
                    if 'sql' not in content and 'dump' not in content:
                        logger.warning("Backup file may not be a valid SQL dump")
                        
                except Exception as e:
                    logger.error(f"Cannot read compressed backup: {e}")
                    return False
            
            logger.info(f"✅ Backup verification passed: {size} bytes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Backup verification failed: {e}")
            return False
    
    def create_backup(self, compress: bool = True, verify: bool = True) -> Optional[Path]:
        """Create a database backup."""
        try:
            # Create backup filename
            filename = self.create_backup_filename(compressed=False)
            backup_file = self.backup_dir / filename
            
            logger.info(f"🔄 Starting database backup...")
            logger.info(f"Database type: {self.config.database_type}")
            logger.info(f"Output file: {backup_file}")
            
            # Create backup based on database type
            success = False
            if self.config.database_type == 'sqlite':
                success = self.backup_sqlite(backup_file)
            elif self.config.database_type == 'postgresql':
                success = self.backup_postgresql(backup_file)
            else:
                logger.error(f"Unsupported database type: {self.config.database_type}")
                return None
            
            if not success:
                logger.error("❌ Backup creation failed")
                return None
            
            # Compress if requested
            final_file = backup_file
            if compress:
                compressed_file = self.compress_backup(backup_file)
                if compressed_file:
                    final_file = compressed_file
                else:
                    logger.warning("Compression failed, keeping uncompressed backup")
            
            # Verify backup
            if verify:
                if not self.verify_backup(final_file):
                    logger.error("❌ Backup verification failed")
                    return None
            
            logger.info(f"🎉 Backup completed successfully: {final_file}")
            return final_file
            
        except Exception as e:
            logger.error(f"❌ Backup creation failed: {e}")
            return None


def main():
    """Main function to create database backup."""
    parser = argparse.ArgumentParser(description='Create ViewTrendsSL database backup')
    parser.add_argument('--no-compress', action='store_true',
                       help='Do not compress the backup file')
    parser.add_argument('--no-verify', action='store_true',
                       help='Skip backup verification')
    parser.add_argument('--rotate', action='store_true',
                       help='Rotate old backups after creating new one')
    parser.add_argument('--info', action='store_true',
                       help='Show information about existing backups')
    parser.add_argument('--max-backups', type=int, default=7,
                       help='Maximum number of backups to keep (default: 7)')
    
    args = parser.parse_args()
    
    backup_handler = DatabaseBackup()
    backup_handler.max_backups = args.max_backups
    
    try:
        if args.info:
            # Show backup information
            info = backup_handler.get_backup_info()
            print(f"\n📊 Backup Information:")
            print(f"Total backups: {info['total_backups']}")
            print(f"Total size: {info['total_size_mb']:.2f} MB")
            print(f"\nBackup files:")
            
            for backup in info['backups']:
                compressed_indicator = "📦" if backup['compressed'] else "📄"
                print(f"  {compressed_indicator} {backup['filename']} "
                      f"({backup['size_mb']:.2f} MB) - {backup['created']}")
            
            return
        
        logger.info("🚀 Starting ViewTrendsSL database backup...")
        
        # Create backup
        backup_file = backup_handler.create_backup(
            compress=not args.no_compress,
            verify=not args.no_verify
        )
        
        if not backup_file:
            logger.error("❌ Backup failed")
            sys.exit(1)
        
        # Rotate backups if requested
        if args.rotate:
            backup_handler.rotate_backups()
        
        # Show final status
        info = backup_handler.get_backup_info()
        logger.info(f"📊 Total backups: {info['total_backups']} "
                   f"({info['total_size_mb']:.2f} MB)")
        
        logger.info("🎉 Database backup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database backup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
