"""Database migration configuration for ViewTrendsSL.

This module provides configuration settings for database migrations,
including Alembic settings and migration management utilities.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

from config.database.database_config import DatabaseConfig


class MigrationConfig:
    """Configuration class for database migrations."""
    
    def __init__(self, environment: str = None):
        """Initialize migration configuration.
        
        Args:
            environment: Environment name (development, testing, production)
        """
        self.environment = environment or os.getenv('FLASK_ENV', 'development')
        self.db_config = DatabaseConfig(self.environment)
        
    @property
    def alembic_config(self) -> Dict[str, Any]:
        """Get Alembic configuration settings.
        
        Returns:
            Dictionary containing Alembic configuration
        """
        return {
            'script_location': str(Path(__file__).parent.parent.parent / 'src' / 'data_access' / 'database' / 'migrations'),
            'prepend_sys_path': ['.'],
            'version_path_separator': 'os',
            'sqlalchemy.url': self.db_config.database_url,
            'sqlalchemy.echo': self.db_config.echo_sql,
            'sqlalchemy.pool_pre_ping': True,
            'sqlalchemy.pool_recycle': self.db_config.pool_recycle,
            'compare_type': True,
            'compare_server_default': True,
            'render_as_batch': True,  # Required for SQLite
        }
    
    @property
    def migration_directory(self) -> Path:
        """Get the migration directory path.
        
        Returns:
            Path to migration directory
        """
        return Path(__file__).parent.parent.parent / 'src' / 'data_access' / 'database' / 'migrations'
    
    @property
    def versions_directory(self) -> Path:
        """Get the versions directory path.
        
        Returns:
            Path to versions directory
        """
        return self.migration_directory / 'versions'
    
    def ensure_migration_directories(self) -> None:
        """Ensure migration directories exist."""
        self.migration_directory.mkdir(parents=True, exist_ok=True)
        self.versions_directory.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py files
        (self.migration_directory / '__init__.py').touch(exist_ok=True)
        (self.versions_directory / '__init__.py').touch(exist_ok=True)
    
    @property
    def env_py_template(self) -> str:
        """Get the env.py template for Alembic.
        
        Returns:
            Template string for env.py
        """
        return '''"""Alembic environment configuration for ViewTrendsSL."""

import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models here
from src.data_access.models import *
from src.data_access.database.connection import Base

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
    
    @property
    def script_py_mako_template(self) -> str:
        """Get the script.py.mako template for Alembic.
        
        Returns:
            Template string for script.py.mako
        """
        return '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade database schema."""
    ${downgrades if downgrades else "pass"}
'''
    
    def get_alembic_ini_content(self) -> str:
        """Get the alembic.ini file content.
        
        Returns:
            Content for alembic.ini file
        """
        return f'''# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = {self.migration_directory}

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# file_template = %%Y%%m%%d_%%H%%M_%%%(rev)s_%%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses
# os.pathsep. If this key is omitted entirely, it falls back to the legacy
# behavior of splitting on spaces and/or commas.
version_path_separator = os

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = {self.db_config.database_url}

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
    
    def create_initial_migration_template(self) -> str:
        """Create template for initial migration.
        
        Returns:
            Template for initial database schema migration
        """
        return '''"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    # Create channels table
    op.create_table('channels',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subscriber_count', sa.BigInteger(), nullable=True),
        sa.Column('video_count', sa.Integer(), nullable=True),
        sa.Column('view_count', sa.BigInteger(), nullable=True),
        sa.Column('country', sa.String(10), nullable=True),
        sa.Column('language', sa.String(10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create videos table
    op.create_table('videos',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('channel_id', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('is_short', sa.Boolean(), nullable=False, default=False),
        sa.Column('view_count', sa.BigInteger(), nullable=True),
        sa.Column('like_count', sa.Integer(), nullable=True),
        sa.Column('comment_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create snapshots table for time-series data
    op.create_table('snapshots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('view_count', sa.BigInteger(), nullable=True),
        sa.Column('like_count', sa.Integer(), nullable=True),
        sa.Column('comment_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create tags table
    op.create_table('tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create video_tags junction table
    op.create_table('video_tags',
        sa.Column('video_id', sa.String(50), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('video_id', 'tag_id')
    )
    
    # Create indexes for performance
    op.create_index('idx_videos_channel_id', 'videos', ['channel_id'])
    op.create_index('idx_videos_published_at', 'videos', ['published_at'])
    op.create_index('idx_videos_is_short', 'videos', ['is_short'])
    op.create_index('idx_snapshots_video_id', 'snapshots', ['video_id'])
    op.create_index('idx_snapshots_timestamp', 'snapshots', ['timestamp'])
    op.create_index('idx_snapshots_video_timestamp', 'snapshots', ['video_id', 'timestamp'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index('idx_snapshots_video_timestamp', table_name='snapshots')
    op.drop_index('idx_snapshots_timestamp', table_name='snapshots')
    op.drop_index('idx_snapshots_video_id', table_name='snapshots')
    op.drop_index('idx_videos_is_short', table_name='videos')
    op.drop_index('idx_videos_published_at', table_name='videos')
    op.drop_index('idx_videos_channel_id', table_name='videos')
    op.drop_table('video_tags')
    op.drop_table('tags')
    op.drop_table('users')
    op.drop_table('snapshots')
    op.drop_table('videos')
    op.drop_table('channels')
'''


# Configuration instances for different environments
development_migration_config = MigrationConfig('development')
testing_migration_config = MigrationConfig('testing')
production_migration_config = MigrationConfig('production')

# Default configuration
migration_config = development_migration_config
