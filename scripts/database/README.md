# Database Management Scripts

This directory contains scripts for managing the ViewTrendsSL database, including setup, backup, and maintenance operations.

## 📁 Directory Structure

```
scripts/database/
├── setup/
│   └── init_database.py          # Database initialization and schema creation
├── backup/
│   └── backup_database.py        # Database backup and recovery
├── maintenance/
│   └── cleanup.py                # Database maintenance and cleanup
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Initialize Database

Create the database schema and tables:

```bash
# Basic initialization
python scripts/database/setup/init_database.py

# Drop existing tables and recreate
python scripts/database/setup/init_database.py --drop-existing

# Initialize with sample data
python scripts/database/setup/init_database.py --sample-data

# Verify database setup only
python scripts/database/setup/init_database.py --verify-only
```

### 2. Create Database Backup

```bash
# Create compressed backup with rotation
python scripts/database/backup/backup_database.py --rotate

# Create uncompressed backup
python scripts/database/backup/backup_database.py --no-compress

# Show backup information
python scripts/database/backup/backup_database.py --info
```

### 3. Database Maintenance

```bash
# Full maintenance (recommended weekly)
python scripts/database/maintenance/cleanup.py --all

# Dry run to see what would be done
python scripts/database/maintenance/cleanup.py --all --dry-run

# Specific maintenance tasks
python scripts/database/maintenance/cleanup.py --cleanup-old-data --vacuum
```

## 📋 Detailed Usage

### Database Initialization (`init_database.py`)

This script sets up the complete database schema for ViewTrendsSL.

**Features:**
- Creates all required tables with proper relationships
- Sets up indexes for optimal performance
- Supports both SQLite and PostgreSQL
- Can insert sample data for testing
- Verifies database setup

**Usage Examples:**

```bash
# Complete setup with sample data
python scripts/database/setup/init_database.py --drop-existing --sample-data

# Production setup (no sample data)
python scripts/database/setup/init_database.py --drop-existing

# Check if database is properly set up
python scripts/database/setup/init_database.py --verify-only
```

**Tables Created:**
- `users` - User accounts and authentication
- `channels` - YouTube channel information
- `videos` - Video metadata and statistics
- `tags` - Video tags and keywords
- `video_tags` - Many-to-many relationship between videos and tags
- `snapshots` - Time-series data for tracking video performance

### Database Backup (`backup_database.py`)

Automated backup solution with compression and rotation.

**Features:**
- Supports SQLite and PostgreSQL
- Automatic compression with gzip
- Backup rotation (keeps N most recent backups)
- Backup verification
- Detailed backup information

**Usage Examples:**

```bash
# Daily backup with compression and rotation
python scripts/database/backup/backup_database.py --rotate

# Weekly backup without compression
python scripts/database/backup/backup_database.py --no-compress --max-backups 4

# Check existing backups
python scripts/database/backup/backup_database.py --info
```

**Backup Location:** `data/backups/`

**Backup Naming:** `viewtrendssl_{db_type}_backup_{timestamp}.sql[.gz]`

### Database Maintenance (`cleanup.py`)

Routine maintenance tasks to keep the database optimized.

**Features:**
- Clean up old snapshot data (configurable retention period)
- Mark inactive videos
- Remove orphaned records
- Database vacuum/optimization
- Update statistics for query optimization
- Comprehensive maintenance reports

**Usage Examples:**

```bash
# Complete maintenance
python scripts/database/maintenance/cleanup.py --all

# Preview what would be cleaned up
python scripts/database/maintenance/cleanup.py --all --dry-run

# Only clean up old data
python scripts/database/maintenance/cleanup.py --cleanup-old-data

# Only optimize database
python scripts/database/maintenance/cleanup.py --vacuum --analyze

# Generate maintenance report
python scripts/database/maintenance/cleanup.py --report
```

**Configuration (Environment Variables):**
- `SNAPSHOT_RETENTION_DAYS` - How long to keep snapshot data (default: 90)
- `INACTIVE_VIDEO_DAYS` - When to mark videos as inactive (default: 365)
- `LOG_RETENTION_DAYS` - Log file retention period (default: 30)
- `MAX_BACKUPS` - Number of backups to keep (default: 7)

## 🔧 Configuration

### Database Connection

The scripts use the database configuration from `config/database/database_config.py`. Make sure your `.env` file contains:

```env
# For SQLite (Development)
DATABASE_URL=sqlite:///data/viewtrendssl.db

# For PostgreSQL (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/viewtrendssl
```

### Environment Variables

```env
# Backup settings
MAX_BACKUPS=7

# Maintenance settings
SNAPSHOT_RETENTION_DAYS=90
INACTIVE_VIDEO_DAYS=365
LOG_RETENTION_DAYS=30
```

## 📅 Recommended Schedule

### Daily Tasks
```bash
# Create backup with rotation
python scripts/database/backup/backup_database.py --rotate
```

### Weekly Tasks
```bash
# Full maintenance
python scripts/database/maintenance/cleanup.py --all
```

### Monthly Tasks
```bash
# Deep cleanup and optimization
python scripts/database/maintenance/cleanup.py --cleanup-old-data --cleanup-orphaned --vacuum --analyze
```

## 🐳 Docker Integration

These scripts are designed to work within Docker containers. The entrypoint script (`scripts/deployment/docker/entrypoint.sh`) can automatically run database initialization:

```bash
# Initialize database on container startup
docker run -e INIT_DB=true viewtrendssl:latest

# Run backup from container
docker exec viewtrendssl-container python scripts/database/backup/backup_database.py --rotate
```

## 🔍 Troubleshooting

### Common Issues

**1. Permission Denied (SQLite)**
```bash
# Ensure the data directory exists and is writable
mkdir -p data
chmod 755 data
```

**2. PostgreSQL Connection Failed**
```bash
# Check connection string and credentials
python -c "from config.database.database_config import DatabaseConfig; DatabaseConfig().get_connection()"
```

**3. Backup Command Not Found**
```bash
# Install required tools
# For SQLite: sqlite3 should be available
# For PostgreSQL: install postgresql-client
sudo apt-get install postgresql-client  # Ubuntu/Debian
brew install postgresql                  # macOS
```

### Logging

All scripts use Python logging. To increase verbosity:

```bash
# Set log level to DEBUG
export PYTHONPATH=.
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" scripts/database/setup/init_database.py
```

### Dry Run Mode

Always test maintenance operations with `--dry-run` first:

```bash
python scripts/database/maintenance/cleanup.py --all --dry-run
```

## 🔒 Security Considerations

1. **Backup Security**: Backup files contain sensitive data. Store them securely and consider encryption for production.

2. **Database Credentials**: Never commit database credentials to version control. Use environment variables.

3. **Access Control**: Limit access to database management scripts in production environments.

4. **Audit Trail**: All operations are logged. Review logs regularly for security monitoring.

## 📊 Monitoring

### Health Checks

```bash
# Verify database connectivity and schema
python scripts/database/setup/init_database.py --verify-only

# Check backup status
python scripts/database/backup/backup_database.py --info

# Generate maintenance report
python scripts/database/maintenance/cleanup.py --report
```

### Metrics to Monitor

- Database size growth
- Number of active videos/channels
- Backup success rate
- Query performance (via database logs)
- Maintenance task completion time

## 🤝 Contributing

When modifying database scripts:

1. Test with both SQLite and PostgreSQL
2. Include proper error handling and logging
3. Support dry-run mode for destructive operations
4. Update this README with any new features
5. Add appropriate tests in the `tests/` directory

## 📚 Additional Resources

- [SQLite Documentation](https://sqlite.org/docs.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Design Best Practices](../../../docs/database-design.md)
- [Backup and Recovery Guide](../../../docs/backup-recovery.md)
