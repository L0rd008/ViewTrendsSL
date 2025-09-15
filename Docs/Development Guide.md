# ViewTrendsSL Development Guide
## Complete Implementation Reference for YouTube Viewership Forecasting System

**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  
**Team**: Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S.  

---

## Document Overview

This Development Guide serves as the **single source of truth** for implementing the ViewTrendsSL system. It consolidates all implementation steps, code examples, and development workflows into one comprehensive reference document.

**Target Audience**: All team members, future contributors, and academic evaluators  
**Document Status**: Living document - updated throughout development  
**Last Updated**: August 6, 2025  

---

## Table of Contents

- [ViewTrendsSL Development Guide](#viewtrendssl-development-guide)
  - [Complete Implementation Reference for YouTube Viewership Forecasting System](#complete-implementation-reference-for-youtube-viewership-forecasting-system)
  - [Document Overview](#document-overview)
  - [Table of Contents](#table-of-contents)
  - [1. Quick Start Guide](#1-quick-start-guide)
    - [1.1 Get Running in 30 Minutes](#11-get-running-in-30-minutes)
    - [1.2 Development Workflow Overview](#12-development-workflow-overview)
    - [1.3 Team Responsibilities Quick Reference](#13-team-responsibilities-quick-reference)
  - [2. Environment Setup](#2-environment-setup)
    - [2.1 Development Environment Installation](#21-development-environment-installation)
    - [2.2 Docker Environment Setup](#22-docker-environment-setup)
    - [2.3 API Keys and Environment Variables](#23-api-keys-and-environment-variables)
    - [2.4 Database Setup](#24-database-setup)
  - [3. File Structure Implementation](#3-file-structure-implementation)
    - [3.1 Complete Directory Structure](#31-complete-directory-structure)
    - [3.2 Core Configuration Files](#32-core-configuration-files)
  - [4. Layer-by-Layer Development](#4-layer-by-layer-development)
    - [4.1 Data Access Layer (Layer 4)](#41-data-access-layer-layer-4)
    - [4.2 Business Logic Layer (Layer 3)](#42-business-logic-layer-layer-3)
    - [4.3 Application Layer (Layer 2)](#43-application-layer-layer-2)
    - [4.4 Presentation Layer (Layer 1)](#44-presentation-layer-layer-1)
  - [5. Data Collection Pipeline](#5-data-collection-pipeline)
    - [5.1 YouTube API Integration](#51-youtube-api-integration)
    - [5.2 Data Collection Scripts](#52-data-collection-scripts)
  - [6. Machine Learning Development](#6-machine-learning-development)
    - [6.1 Model Training Pipeline](#61-model-training-pipeline)
  - [7. Testing Implementation](#7-testing-implementation)
    - [7.1 Testing Strategy](#71-testing-strategy)
    - [7.2 Unit Tests](#72-unit-tests)
    - [7.3 Integration Tests](#73-integration-tests)
  - [8. Deployment \& DevOps](#8-deployment--devops)
    - [8.1 Docker Deployment](#81-docker-deployment)
    - [8.2 Cloud Deployment Script](#82-cloud-deployment-script)
  - [9. Team Collaboration Workflow](#9-team-collaboration-workflow)
    - [9.1 Git Workflow](#91-git-workflow)
    - [9.2 Code Review Checklist](#92-code-review-checklist)
  - [10. Troubleshooting Guide](#10-troubleshooting-guide)
    - [10.1 Common Issues](#101-common-issues)
    - [10.2 Performance Optimization](#102-performance-optimization)
  - [11. Quality Assurance](#11-quality-assurance)
    - [11.1 Code Quality Tools](#111-code-quality-tools)
    - [11.2 Continuous Integration](#112-continuous-integration)
  - [12. Final Implementation Checklist](#12-final-implementation-checklist)
    - [12.1 MVP Completion Checklist](#121-mvp-completion-checklist)
    - [12.2 Success Criteria](#122-success-criteria)
  - [Conclusion](#conclusion)
    - [12.2 Success Criteria](#122-success-criteria-1)
    - [12.2 Success Criteria](#122-success-criteria-2)

---

## 1. Quick Start Guide

### 1.1 Get Running in 30 Minutes

**Prerequisites**: Git, Docker Desktop, Python 3.9+, VS Code

```bash
# 1. Clone and setup repository
git clone https://github.com/L0rd008/ViewTrendsSL.git
cd ViewTrendsSL

# 2. Create environment file
cp .env.example .env
# Edit .env with your API keys (see section 2.3)

# 3. Build and run with Docker
docker-compose up --build

# 4. Access the application
# Web App: http://localhost:8501
# API: http://localhost:5000
```

### 1.2 Development Workflow Overview

```mermaid
graph TD
    A[Setup Environment] --> B[Create Feature Branch]
    B --> C[Implement Layer Components]
    C --> D[Write Tests]
    D --> E[Run Quality Checks]
    E --> F[Create Pull Request]
    F --> G[Code Review]
    G --> H[Merge to Development]
```

### 1.3 Team Responsibilities Quick Reference

| Team Member | Primary Focus | Key Directories |
|-------------|---------------|-----------------|
| **Senevirathne** (Data Lead) | Data collection, EDA, API integration | `scripts/data_collection/`, `src/external/`, `notebooks/` |
| **Sanjula** (Backend Lead) | ML models, API, database, DevOps | `src/business/`, `src/data_access/`, `scripts/model_training/` |
| **Shaamma** (Frontend Lead) | UI, documentation, testing | `src/presentation/`, `docs/`, `tests/` |

---

## 2. Environment Setup

### 2.1 Development Environment Installation

**Step 1: Install Required Software**

```bash
# Install Docker Desktop
# Windows: Download from docker.com
# Ubuntu: 
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Logout and login again

# Install Python 3.9+ (if not using Docker exclusively)
# Windows: Download from python.org
# Ubuntu:
sudo apt install python3.9 python3.9-venv python3-pip

# Install VS Code with extensions
# Required extensions:
# - Python
# - Docker
# - GitLens
# - Jupyter
```

**Step 2: Clone and Setup Repository**

```bash
# Clone repository
git clone https://github.com/L0rd008/ViewTrendsSL.git
cd ViewTrendsSL

# Create development branch
git checkout -b development
git push -u origin development

# Set up Git hooks (optional but recommended)
cp scripts/git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### 2.2 Docker Environment Setup

**Create Docker Configuration Files**

```dockerfile
# config/docker/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Expose ports
EXPOSE 5000 8501

# Default command
CMD ["python", "src/application/app.py"]
```

```yaml
# config/docker/docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: ../..
      dockerfile: config/docker/Dockerfile
    ports:
      - "5000:5000"
      - "8501:8501"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://viewtrends:password@db:5432/viewtrends_dev
    volumes:
      - ../../src:/app/src
      - ../../data:/app/data
    depends_on:
      - db
    command: python src/application/app.py

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=viewtrends_dev
      - POSTGRES_USER=viewtrends
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ../../scripts/database:/docker-entrypoint-initdb.d

  streamlit:
    build:
      context: ../..
      dockerfile: config/docker/Dockerfile
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://web:5000
    volumes:
      - ../../src:/app/src
    depends_on:
      - web
    command: streamlit run src/presentation/streamlit_app.py --server.port=8501 --server.address=0.0.0.0

volumes:
  postgres_data:
```

### 2.3 API Keys and Environment Variables

**Create Environment Configuration**

```bash
# .env.example (template)
# YouTube Data API Keys (get from Google Cloud Console)
YOUTUBE_API_KEY_1=your_api_key_here
YOUTUBE_API_KEY_2=your_api_key_here
YOUTUBE_API_KEY_3=your_api_key_here

# Database Configuration
DATABASE_URL=postgresql://viewtrends:password@localhost:5432/viewtrends_dev
DATABASE_SSL_MODE=prefer

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# Security
JWT_SECRET_KEY=your-jwt-secret-here
BCRYPT_LOG_ROUNDS=12

# External Services
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO

# Model Configuration
MODEL_PATH=data/models/
CACHE_TTL=3600
```

**YouTube API Setup Instructions**

1. **Create Google Cloud Project**:
   ```bash
   # Go to: https://console.cloud.google.com/
   # Create new project: "ViewTrendsSL-[YourName]"
   # Enable YouTube Data API v3
   # Create API Key with YouTube Data API access
   ```

2. **Configure API Keys**:
   ```python
   # Each team member should create their own API key
   # This triples our daily quota (30,000 units total)
   # Add all three keys to .env file
   ```

### 2.4 Database Setup

**Local Development Database**

```bash
# Start PostgreSQL with Docker
docker-compose up db

# Create database schema
python scripts/database/create_schema.py

# Run initial migrations
python scripts/database/migrate.py

# Seed with sample data (optional)
python scripts/database/seed_sample_data.py
```

**Database Schema Creation Script**

```python
# scripts/database/create_schema.py
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="viewtrends",
        password="password"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'viewtrends_dev'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute('CREATE DATABASE viewtrends_dev')
        print("Database 'viewtrends_dev' created successfully")
    else:
        print("Database 'viewtrends_dev' already exists")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
```

---

## 3. File Structure Implementation

### 3.1 Complete Directory Structure

**Create the full directory structure:**

```bash
# Run this script to create all directories
mkdir -p {docs/{api,user-guide,diagrams},src/{presentation/{pages,components,static/{css,js,images}},application/{api,middleware},business/{services,ml,utils},data_access/{repositories,models,database/{migrations,seeds}},external/{youtube_api,monitoring}},scripts/{data_collection,model_training,database,deployment},data/{raw/{channels,videos,snapshots},processed/{features,training,validation},models,logs},tests/{unit/{test_services,test_repositories,test_ml,test_utils},integration/{test_api,test_database,test_external},fixtures,performance},notebooks,config/docker}

# Create __init__.py files for Python packages
find src/ -type d -exec touch {}/__init__.py \;
find tests/ -type d -exec touch {}/__init__.py \;
```

### 3.2 Core Configuration Files

**requirements.txt**

```txt
# Web Framework
flask==2.3.3
streamlit==1.28.0
gunicorn==21.2.0

# Database
sqlalchemy==2.0.21
psycopg2-binary==2.9.7
alembic==1.12.0

# Machine Learning
xgboost==1.7.6
scikit-learn==1.3.0
pandas==2.1.1
numpy==1.24.3

# Data Collection
google-api-python-client==2.100.0
requests==2.31.0
python-dotenv==1.0.0

# Data Processing
isodate==0.6.1
langdetect==1.0.9
textblob==0.17.1

# Visualization
plotly==5.17.0
matplotlib==3.7.2
seaborn==0.12.2

# Utilities
schedule==1.2.0
apscheduler==3.10.4
redis==5.0.0
celery==5.3.2

# Development
pytest==7.4.2
pytest-cov==4.1.0
black==23.9.1
flake8==6.1.0
mypy==1.5.1

# Security
bcrypt==4.0.1
pyjwt==2.8.0
cryptography==41.0.8
```

**pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "viewtrendssl"
version = "1.0.0"
description = "YouTube Viewership Forecasting for Sri Lankan Audience"
authors = [
    {name = "Senevirathne S.M.P.U.", email = "senevirathne@example.com"},
    {name = "Sanjula N.G.K.", email = "sanjula@example.com"},
    {name = "Shaamma M.S.", email = "shaamma@example.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## 4. Layer-by-Layer Development

### 4.1 Data Access Layer (Layer 4)

**Start with the foundation - database models and repositories**

**Step 1: Create SQLAlchemy Models**

```python
# src/data_access/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

```python
# src/data_access/models/channel.py
from sqlalchemy import Column, String, Integer, DateTime
from .base import BaseModel

class Channel(BaseModel):
    __tablename__ = 'channels'
    
    channel_id = Column(String(50), unique=True, nullable=False, index=True)
    channel_name = Column(String(255), nullable=False)
    subscriber_count = Column(Integer)
    video_count = Column(Integer)
    country = Column(String(10))
    description = Column(String)
    
    def __repr__(self):
        return f"<Channel(channel_id='{self.channel_id}', name='{self.channel_name}')>"
```

```python
# src/data_access/models/video.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Video(BaseModel):
    __tablename__ = 'videos'
    
    video_id = Column(String(50), unique=True, nullable=False, index=True)
    channel_id = Column(String(50), ForeignKey('channels.channel_id'), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    published_at = Column(DateTime, nullable=False, index=True)
    duration_seconds = Column(Integer)
    category_id = Column(Integer)
    is_short = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    
    # Relationships
    channel = relationship("Channel", backref="videos")
    snapshots = relationship("Snapshot", back_populates="video")
    
    def __repr__(self):
        return f"<Video(video_id='{self.video_id}', title='{self.title[:50]}...')>"
```

**Step 2: Create Repository Pattern**

```python
# src/data_access/repositories/base_repository.py
from typing import List, Optional, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database.connection import get_db_session
from ..models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new record"""
        with get_db_session() as session:
            try:
                instance = self.model(**kwargs)
                session.add(instance)
                session.commit()
                session.refresh(instance)
                return instance
            except SQLAlchemyError as e:
                session.rollback()
                raise e
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get record by ID"""
        with get_db_session() as session:
            return session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Get all records with pagination"""
        with get_db_session() as session:
            return session.query(self.model).offset(offset).limit(limit).all()
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update record by ID"""
        with get_db_session() as session:
            try:
                instance = session.query(self.model).filter(self.model.id == id).first()
                if instance:
                    for key, value in kwargs.items():
                        setattr(instance, key, value)
                    session.commit()
                    session.refresh(instance)
                return instance
            except SQLAlchemyError as e:
                session.rollback()
                raise e
    
    def delete(self, id: int) -> bool:
        """Delete record by ID"""
        with get_db_session() as session:
            try:
                instance = session.query(self.model).filter(self.model.id == id).first()
                if instance:
                    session.delete(instance)
                    session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                session.rollback()
                raise e
```

```python
# src/data_access/repositories/video_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.video import Video
from ..database.connection import get_db_session

class VideoRepository(BaseRepository[Video]):
    def __init__(self):
        super().__init__(Video)
    
    def get_by_video_id(self, video_id: str) -> Optional[Video]:
        """Get video by YouTube video ID"""
        with get_db_session() as session:
            return session.query(Video).filter(Video.video_id == video_id).first()
    
    def get_by_channel(self, channel_id: str, limit: int = 50) -> List[Video]:
        """Get videos by channel ID"""
        with get_db_session() as session:
            return (session.query(Video)
                   .filter(Video.channel_id == channel_id)
                   .order_by(Video.published_at.desc())
                   .limit(limit)
                   .all())
    
    def get_shorts(self, limit: int = 1000) -> List[Video]:
        """Get all short videos (≤60 seconds)"""
        with get_db_session() as session:
            return (session.query(Video)
                   .filter(Video.is_short == True)
                   .limit(limit)
                   .all())
    
    def get_long_form(self, limit: int = 1000) -> List[Video]:
        """Get all long-form videos (>60 seconds)"""
        with get_db_session() as session:
            return (session.query(Video)
                   .filter(Video.is_short == False)
                   .limit(limit)
                   .all())
    
    def update_statistics(self, video_id: str, view_count: int, 
                         like_count: int, comment_count: int) -> Optional[Video]:
        """Update video statistics"""
        with get_db_session() as session:
            video = session.query(Video).filter(Video.video_id == video_id).first()
            if video:
                video.view_count = view_count
                video.like_count = like_count
                video.comment_count = comment_count
                session.commit()
                session.refresh(video)
            return video
```

**Step 3: Database Connection Management**

```python
# src/data_access/database/connection.py
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from ..models.base import Base

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://viewtrends:password@localhost:5432/viewtrends_dev')

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session() -> Session:
    """Get database session with automatic cleanup"""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_db():
    """Dependency for FastAPI/Flask route injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.2 Business Logic Layer (Layer 3)

**Step 1: Create Core Services**

```python
# src/business/services/prediction_service.py
from typing import Dict, List, Optional, Tuple
import logging
from ..ml.prediction_engine import PredictionEngine
from ..ml.feature_extractor import FeatureExtractor
from ...data_access.repositories.video_repository import VideoRepository
from ...external.youtube_api.client import YouTubeAPIClient

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.prediction_engine = PredictionEngine()
        self.feature_extractor = FeatureExtractor()
        self.video_repository = VideoRepository()
        self.youtube_client = YouTubeAPIClient()
    
    def predict_video_performance(self, video_url: str) -> Dict:
        """
        Main prediction workflow for a YouTube video
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Dictionary containing predictions and metadata
        """
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            
            # Check if video exists in database
            video = self.video_repository.get_by_video_id(video_id)
            
            if not video:
                # Fetch video metadata from YouTube API
                video_data = self.youtube_client.get_video_details(video_id)
                
                # Store video in database
                video = self._store_video_data(video_data)
            
            # Extract features for prediction
            features = self.feature_extractor.extract_features(video)
            
            # Generate predictions
            predictions = self.prediction_engine.predict(features, video.is_short)
            
            # Format response
            return {
                'video_id': video_id,
                'video_title': video.title,
                'channel_name': video.channel.channel_name if video.channel else 'Unknown',
                'is_short': video.is_short,
                'current_views': video.view_count,
                'predictions': {
                    '24_hours': predictions['24h'],
                    '7_days': predictions['7d'],
                    '30_days': predictions['30d']
                },
                'confidence_score': predictions['confidence'],
                'prediction_date': predictions['timestamp']
            }
            
        except Exception as e:
            logger.error(f"Prediction failed for video {video_url}: {str(e)}")
            raise
    
    def _extract_video_id(self, video_url: str) -> str:
        """Extract video ID from YouTube URL"""
        import re
        
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video_url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Invalid YouTube URL: {video_url}")
    
    def _store_video_data(self, video_data: Dict) -> 'Video':
        """Store video data in database"""
        # Determine if video is a Short
        duration_seconds = video_data.get('duration_seconds', 0)
        is_short = duration_seconds <= 60
        
        # Create video record
        video = self.video_repository.create(
            video_id=video_data['video_id'],
            channel_id=video_data['channel_id'],
            title=video_data['title'],
            description=video_data.get('description', ''),
            published_at=video_data['published_at'],
            duration_seconds=duration_seconds,
            category_id=video_data.get('category_id'),
            is_short=is_short,
            view_count=video_data.get('view_count', 0),
            like_count=video_data.get('like_count', 0),
            comment_count=video_data.get('comment_count', 0)
        )
        
        return video
```

**Step 2: Feature Engineering Service**

```python
# src/business/ml/feature_extractor.py
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
import re
from textblob import TextBlob
from langdetect import detect

class FeatureExtractor:
    def __init__(self):
        self.feature_definitions = self._load_feature_definitions()
    
    def extract_features(self, video) -> Dict:
        """
        Extract all features for a video
        
        Args:
            video: Video model instance
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Temporal features
        features.update(self._extract_temporal_features(video.published_at))
        
        # Content features
        features.update(self._extract_content_features(video.title, video.description))
        
        # Video metadata features
        features.update(self._extract_metadata_features(video))
        
        # Channel authority features
        if video.channel:
            features.update(self._extract_channel_features(video.channel))
        
        return features
    
    def _extract_temporal_features(self, published_at: datetime) -> Dict:
        """Extract time-based features"""
        return {
            'publish_hour': published_at.hour,
            'publish_day_of_week': published_at.weekday(),
            'publish_day_of_month': published_at.day,
            'publish_month': published_at.month,
            'is_weekend': published_at.weekday() >= 5,
            'is_prime_time': 18 <= published_at.hour <= 22,
            'is_morning': 6 <= published_at.hour <= 12,
            'is_afternoon': 12 <= published_at.hour <= 18,
            'is_evening': 18 <= published_at.hour <= 24
        }
    
    def _extract_content_features(self, title: str, description: str = '') -> Dict:
        """Extract features from title and description"""
        features = {}
        
        # Title features
        if title:
            features.update({
                'title_length': len(title),
                'title_word_count': len(title.split()),
                'title_char_count': len(title),
                'title_uppercase_ratio': sum(1 for c in title if c.isupper()) / len(title) if title else 0,
                'title_has_question': '?' in title,
                'title_has_exclamation': '!' in title,
                'title_has_numbers': bool(re.search(r'\d', title)),
                'title_has_brackets': bool(re.search(r'[\[\]()]', title)),
                'title_sentiment': self._get_sentiment_score(title)
            })
            
            # Language detection
            try:
                detected_lang = detect(title)
                features['title_language'] = detected_lang
                features['is_sinhala'] = detected_lang == 'si'
                features['is_tamil'] = detected_lang == 'ta'
                features['is_english'] = detected_lang == 'en'
            except:
                features['title_language'] = 'unknown'
                features['is_sinhala'] = False
                features['is_tamil'] = False
                features['is_english'] = False
        
        # Description features
        if description:
            features.update({
                'description_length': len(description),
                'description_word_count': len(description.split()),
                'description_line_count': len(description.split('\n')),
                'description_has_links': bool(re.search(r'http[s]?://', description)),
                'description_hashtag_count': len(re.findall(r'#\w+', description)),
                'description_mention_count': len(re.findall(r'@\w+', description))
            })
        
        return features
    
    def _extract_metadata_features(self, video) -> Dict:
        """Extract features from video metadata"""
        return {
            'duration_seconds': video.duration_seconds or 0,
            'duration_minutes': (video.duration_seconds or 0) / 60,
            'is_short': video.is_short,
            'category_id': video.category_id or 0,
            'current_view_count': video.view_count or 0,
            'current_like_count': video.like_count or 0,
            'current_comment_count': video.comment_count or 0,
            'like_to_view_ratio': (video.like_count or 0) / max(video.view_count or 1, 1),
            'comment_to_view_ratio': (video.comment_count or 0) / max(video.view_count or 1, 1)
        }
    
    def _extract_channel_features(self, channel) -> Dict:
        """Extract features from channel information"""
        return {
            'channel_subscriber_count': channel.subscriber_count or 0,
            'channel_video_count': channel.video_count or 0,
            'channel_authority_score': self._calculate_authority_score(channel),
            'is_verified_channel': channel.subscriber_count and channel.subscriber_count > 100000
        }
    
    def _get_sentiment_score(self, text: str) -> float:
        """Get sentiment score using TextBlob"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except:
            return 0.0
    
    def _calculate_authority_score(self, channel) -> float:
        """Calculate channel authority score"""
        if not channel.subscriber_count:
            return 0.0
        
        # Simple authority score based on subscribers and video count
        subscriber_score = min(channel.subscriber_count / 1000000, 1.0)  # Max 1.0 for 1M+ subs
        video_count_score = min(channel.video_count / 1000, 1.0) if channel.video_count else 0
        
        return (subscriber_score * 0.7) + (video_count_score * 0.3)
    
    def _load_feature_definitions(self) -> Dict:
        """Load feature definitions for consistency"""
        return {
            'temporal_features': [
                'publish_hour', 'publish_day_of_week', 'is_weekend', 'is_prime_time'
            ],
            'content_features': [
                'title_length', 'title_word_count', 'title_sentiment', 'title_language'
            ],
            'metadata_features': [
                'duration_seconds', 'is_short', 'category_id'
            ],
            'channel_features': [
                'channel_subscriber_count', 'channel_authority_score'
            ]
        }
```

**Step 3: Machine Learning Pipeline**

```python
# src/business/ml/prediction_engine.py
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class PredictionEngine:
    def __init__(self):
        self.models = {}
        self.preprocessors = {}
        self.model_path = os.getenv('MODEL_PATH', 'data/models/')
        self._load_models()
    
    def _load_models(self):
        """Load trained models and preprocessors"""
        try:
            # Load Shorts model
            shorts_model_path = os.path.join(self.model_path, 'shorts_model.joblib')
            if os.path.exists(shorts_model_path):
                self.models['shorts'] = joblib.load(shorts_model_path)
                logger.info("Shorts model loaded successfully")
            
            # Load Long-form model
            longform_model_path = os.path.join(self.model_path, 'longform_model.joblib')
            if os.path.exists(longform_model_path):
                self.models['longform'] = joblib.load(longform_model_path)
                logger.info("Long-form model loaded successfully")
            
            # Load preprocessor
            preprocessor_path = os.path.join(self.model_path, 'preprocessing_pipeline.joblib')
            if os.path.exists(preprocessor_path):
                self.preprocessors['main'] = joblib.load(preprocessor_path)
                logger.info("Preprocessor loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            # Initialize with dummy models for development
            self._initialize_dummy_models()
    
    def predict(self, features: Dict, is_short: bool) -> Dict:
        """
        Generate predictions for a video
        
        Args:
            features: Extracted features dictionary
            is_short: Whether the video is a Short
            
        Returns:
            Dictionary with predictions and confidence
        """
        try:
            # Select appropriate model
            model_key = 'shorts' if is_short else 'longform'
            model = self.models.get(model_key)
            
            if not model:
                logger.warning(f"Model {model_key} not available, using fallback")
                return self._fallback_prediction(features, is_short)
            
            # Preprocess features
            processed_features = self._preprocess_features(features)
            
            # Generate predictions for different time intervals
            predictions = {}
            
            # Predict for 24 hours, 7 days, 30 days
            for interval in ['24h', '7d', '30d']:
                # Modify features based on time interval
                interval_features = self._adjust_features_for_interval(processed_features, interval)
                
                # Make prediction
                prediction = model.predict([interval_features])[0]
                predictions[interval] = max(0, int(prediction))  # Ensure non-negative
            
            # Calculate confidence score
            confidence = self._calculate_confidence(processed_features, predictions)
            
            return {
                '24h': predictions['24h'],
                '7d': predictions['7d'],
                '30d': predictions['30d'],
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'model_used': model_key
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return self._fallback_prediction(features, is_short)
    
    def _preprocess_features(self, features: Dict) -> List:
        """Preprocess features for model input"""
        if 'main' in self.preprocessors:
            # Convert to DataFrame for preprocessing
            df = pd.DataFrame([features])
            processed = self.preprocessors['main'].transform(df)
            return processed[0].tolist()
        else:
            # Manual preprocessing for development
            return self._manual_preprocessing(features)
    
    def _manual_preprocessing(self, features: Dict) -> List:
        """Manual feature preprocessing when preprocessor not available"""
        # Define expected feature order
        feature_order = [
            'publish_hour', 'publish_day_of_week', 'is_weekend', 'is_prime_time',
            'title_length', 'title_word_count', 'title_sentiment',
            'duration_seconds', 'is_short', 'category_id',
            'channel_subscriber_count', 'channel_authority_score'
        ]
        
        processed = []
        for feature_name in feature_order:
            value = features.get(feature_name, 0)
            # Convert boolean to int
            if isinstance(value, bool):
                value = int(value)
            processed.append(value)
        
        return processed
    
    def _adjust_features_for_interval(self, features: List, interval: str) -> List:
        """Adjust features based on prediction interval"""
        # For now, return features as-is
        # In a more sophisticated model, you might adjust features
        # based on the prediction timeframe
        return features
    
    def _calculate_confidence(self, features: List, predictions: Dict) -> float:
        """Calculate confidence score for predictions"""
        # Simple confidence calculation based on feature completeness
        feature_completeness = sum(1 for f in features if f != 0) / len(features)
        
        # Adjust confidence based on prediction consistency
        pred_values = list(predictions.values())
        if len(pred_values) > 1:
            consistency = 1.0 - (np.std(pred_values) / np.mean(pred_values))
            consistency = max(0, min(1, consistency))
        else:
            consistency = 0.5
        
        confidence = (feature_completeness * 0.6) + (consistency * 0.4)
        return round(confidence, 2)
    
    def _fallback_prediction(self, features: Dict, is_short: bool) -> Dict:
        """Fallback prediction when models are not available"""
        # Simple heuristic-based prediction
        base_views = 1000 if is_short else 500
        
        # Adjust based on channel authority
        authority_multiplier = features.get('channel_authority_score', 0.1) * 10
        
        # Adjust based on publish time
        time_multiplier = 1.5 if features.get('is_prime_time', False) else 1.0
        
        predicted_24h = int(base_views * authority_multiplier * time_multiplier)
        predicted_7d = int(predicted_24h * 3.5)
        predicted_30d = int(predicted_7d * 2.0)
        
        return {
            '24h': predicted_24h,
            '7d': predicted_7d,
            '30d': predicted_30d,
            'confidence': 0.3,  # Low confidence for fallback
            'timestamp': datetime.now().isoformat(),
            'model_used': 'fallback'
        }
    
    def _initialize_dummy_models(self):
        """Initialize dummy models for development"""
        logger.warning("Initializing dummy models for development")
        # This would be replaced with actual trained models
        self.models['shorts'] = None
        self.models['longform'] = None
```

### 4.3 Application Layer (Layer 2)

**Step 1: Flask Application Setup**

```python
# src/application/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from .api.routes import api_bp
from .middleware.auth import auth_bp
from .error_handlers import register_error_handlers
from ..data_access.database.connection import create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # Enable CORS for frontend integration
    CORS(app, origins=['http://localhost:8501', 'http://localhost:3000'])
    
    # Initialize database
    create_tables()
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'ViewTrendsSL API'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
```

```python
# src/application/api/routes.py
from flask import Blueprint, request, jsonify
from ...business.services.prediction_service import PredictionService
import logging

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

# Initialize services
prediction_service = PredictionService()

@api_bp.route('/predict', methods=['POST'])
def predict_video():
    """Predict video viewership"""
    try:
        data = request.get_json()
        
        if not data or 'video_url' not in data:
            return jsonify({'error': 'video_url is required'}), 400
        
        video_url = data['video_url']
        
        # Generate prediction
        result = prediction_service.predict_video_performance(video_url)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/video/<video_id>', methods=['GET'])
def get_video_info(video_id):
    """Get video information"""
    try:
        # Implementation for getting video info
        return jsonify({
            'success': True,
            'data': {'video_id': video_id, 'message': 'Not implemented yet'}
        })
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
```

### 4.4 Presentation Layer (Layer 1)

**Step 1: Streamlit Application**

```python
# src/presentation/streamlit_app.py
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="ViewTrendsSL - YouTube Viewership Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

def main():
    """Main application function"""
    st.title("📈 ViewTrendsSL")
    st.subheader("YouTube Viewership Forecasting for Sri Lankan Audience")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Choose a page", ["Prediction", "Analytics", "About"])
    
    if page == "Prediction":
        prediction_page()
    elif page == "Analytics":
        analytics_page()
    else:
        about_page()

def prediction_page():
    """Video prediction page"""
    st.header("🎯 Video Performance Prediction")
    
    # Input form
    with st.form("prediction_form"):
        video_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Enter a YouTube video URL to get viewership predictions"
        )
        
        submitted = st.form_submit_button("Generate Prediction")
    
    if submitted and video_url:
        with st.spinner("Analyzing video and generating predictions..."):
            try:
                # Call API
                response = requests.post(
                    f"{API_BASE_URL}/api/v1/predict",
                    json={"video_url": video_url},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()['data']
                    display_prediction_results(data)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def display_prediction_results(data):
    """Display prediction results"""
    st.success("Prediction generated successfully!")
    
    # Video information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Video Information")
        st.write(f"**Title:** {data['video_title']}")
        st.write(f"**Channel:** {data['channel_name']}")
        st.write(f"**Type:** {'Short' if data['is_short'] else 'Long-form'}")
        st.write(f"**Current Views:** {data['current_views']:,}")
    
    with col2:
        st.metric(
            "Confidence Score",
            f"{data['confidence_score']:.0%}",
            help="Model confidence in the prediction"
        )
    
    # Predictions
    st.subheader("📊 Viewership Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "24 Hours",
            f"{data['predictions']['24_hours']:,}",
            delta=f"+{data['predictions']['24_hours'] - data['current_views']:,}"
        )
    
    with col2:
        st.metric(
            "7 Days",
            f"{data['predictions']['7_days']:,}",
            delta=f"+{data['predictions']['7_days'] - data['current_views']:,}"
        )
    
    with col3:
        st.metric(
            "30 Days",
            f"{data['predictions']['30_days']:,}",
            delta=f"+{data['predictions']['30_days'] - data['current_views']:,}"
        )
    
    # Visualization
    create_prediction_chart(data)

def create_prediction_chart(data):
    """Create prediction visualization"""
    st.subheader("📈 Predicted Growth Curve")
    
    # Prepare data for chart
    dates = [
        datetime.now(),
        datetime.now() + timedelta(days=1),
        datetime.now() + timedelta(days=7),
        datetime.now() + timedelta(days=30)
    ]
    
    views = [
        data['current_views'],
        data['predictions']['24_hours'],
        data['predictions']['7_days'],
        data['predictions']['30_days']
    ]
    
    # Create chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=views,
        mode='lines+markers',
        name='Predicted Views',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Viewership Forecast",
        xaxis_title="Date",
        yaxis_title="View Count",
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def analytics_page():
    """Analytics dashboard page"""
    st.header("📊 Analytics Dashboard")
    st.info("Analytics features will be implemented in future versions")
    
    # Placeholder for analytics
    st.subheader("Coming Soon:")
    st.write("- Channel performance analysis")
    st.write("- Trending topics identification")
    st.write("- Competitor analysis")
    st.write("- Historical accuracy metrics")

def about_page():
    """About page"""
    st.header("ℹ️ About ViewTrendsSL")
    
    st.write("""
    ViewTrendsSL is a machine learning-powered tool for predicting YouTube video viewership 
    specifically tailored for Sri Lankan audiences. This project is developed as part of 
    the Data Science and Engineering Project course at the University of Moratuwa.
    """)
    
    st.subheader("🎯 Features")
    st.write("- Accurate viewership predictions for Sri Lankan content")
    st.write("- Separate models for Shorts and Long-form videos")
    st.write("- Real-time analysis using YouTube Data API")
    st.write("- Interactive visualizations and insights")
    
    st.subheader("👥 Development Team")
    st.write("- **Senevirathne S.M.P.U.** - Data Lead")
    st.write("- **Sanjula N.G.K.** - Backend & Model Lead")
    st.write("- **Shaamma M.S.** - Frontend & Documentation Lead")
    
    st.subheader("🔧 Technology Stack")
    st.write("- **Backend:** Python, Flask, XGBoost")
    st.write("- **Frontend:** Streamlit, Plotly")
    st.write("- **Database:** PostgreSQL")
    st.write("- **Deployment:** Docker, Cloud Platform")

if __name__ == "__main__":
    main()
```

---

## 5. Data Collection Pipeline

### 5.1 YouTube API Integration

```python
# src/external/youtube_api/client.py
import os
import time
import logging
from typing import Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
from datetime import datetime

logger = logging.getLogger(__name__)

class YouTubeAPIClient:
    def __init__(self):
        self.api_keys = [
            os.getenv('YOUTUBE_API_KEY_1'),
            os.getenv('YOUTUBE_API_KEY_2'),
            os.getenv('YOUTUBE_API_KEY_3')
        ]
        self.current_key_index = 0
        self.youtube = self._build_service()
        self.quota_usage = 0
        self.daily_limit = 10000
    
    def _build_service(self):
        """Build YouTube API service"""
        api_key = self.api_keys[self.current_key_index]
        if not api_key:
            raise ValueError("YouTube API key not found")
        
        return build('youtube', 'v3', developerKey=api_key)
    
    def _rotate_api_key(self):
        """Rotate to next API key when quota is exceeded"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.youtube = self._build_service()
        self.quota_usage = 0
        logger.info(f"Rotated to API key {self.current_key_index + 1}")
    
    def get_video_details(self, video_id: str) -> Dict:
        """Get detailed video information"""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            )
            
            response = request.execute()
            self.quota_usage += 1
            
            if not response['items']:
                raise ValueError(f"Video not found: {video_id}")
            
            video = response['items'][0]
            return self._parse_video_data(video)
            
        except HttpError as e:
            if e.resp.status == 403:  # Quota exceeded
                logger.warning("Quota exceeded, rotating API key")
                self._rotate_api_key()
                return self.get_video_details(video_id)  # Retry with new key
            else:
                logger.error(f"YouTube API error: {e}")
                raise
    
    def _parse_video_data(self, video: Dict) -> Dict:
        """Parse video data from API response"""
        snippet = video['snippet']
        statistics = video.get('statistics', {})
        content_details = video['contentDetails']
        
        # Parse duration
        duration_iso = content_details.get('duration', 'PT0S')
        duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())
        
        # Parse publish date
        published_at = datetime.fromisoformat(
            snippet['publishedAt'].replace('Z', '+00:00')
        )
        
        return {
            'video_id': video['id'],
            'channel_id': snippet['channelId'],
            'title': snippet['title'],
            'description': snippet.get('description', ''),
            'published_at': published_at,
            'duration_seconds': duration_seconds,
            'category_id': int(snippet.get('categoryId', 0)),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'tags': snippet.get('tags', [])
        }
```

### 5.2 Data Collection Scripts

```python
# scripts/data_collection/collect_videos.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.external.youtube_api.client import YouTubeAPIClient
from src.data_access.repositories.video_repository import VideoRepository
from src.data_access.repositories.channel_repository import ChannelRepository
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoCollector:
    def __init__(self):
        self.youtube_client = YouTubeAPIClient()
        self.video_repo = VideoRepository()
        self.channel_repo = ChannelRepository()
    
    def collect_channel_videos(self, channel_id: str, max_videos: int = 50):
        """Collect recent videos from a channel"""
        try:
            logger.info(f"Collecting videos for channel: {channel_id}")
            
            # Get channel's uploads playlist
            channel_response = self.youtube_client.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                logger.warning(f"Channel not found: {channel_id}")
                return
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            videos_collected = 0
            next_page_token = None
            
            while videos_collected < max_videos:
                playlist_response = self.youtube_client.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_videos - videos_collected),
                    pageToken=next_page_token
                ).execute()
                
                video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
                
                # Get detailed video information
                for video_id in video_ids:
                    try:
                        # Check if video already exists
                        if self.video_repo.get_by_video_id(video_id):
                            logger.info(f"Video {video_id} already exists, skipping")
                            continue
                        
                        video_data = self.youtube_client.get_video_details(video_id)
                        
                        # Store video
                        self._store_video(video_data)
                        videos_collected += 1
                        
                        # Rate limiting
                        time.sleep(0.1)
                        
                    except Exception as e:
                        logger.error(f"Error collecting video {video_id}: {str(e)}")
                        continue
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            logger.info(f"Collected {videos_collected} videos for channel {channel_id}")
            
        except Exception as e:
            logger.error(f"Error collecting videos for channel {channel_id}: {str(e)}")
    
    def _store_video(self, video_data: Dict):
        """Store video data in database"""
        # Determine if video is a Short
        is_short = video_data['duration_seconds'] <= 60
        
        self.video_repo.create(
            video_id=video_data['video_id'],
            channel_id=video_data['channel_id'],
            title=video_data['title'],
            description=video_data['description'],
            published_at=video_data['published_at'],
            duration_seconds=video_data['duration_seconds'],
            category_id=video_data['category_id'],
            is_short=is_short,
            view_count=video_data['view_count'],
            like_count=video_data['like_count'],
            comment_count=video_data['comment_count']
        )

def main():
    """Main collection function"""
    collector = VideoCollector()
    
    # Sri Lankan channels to collect from
    sri_lankan_channels = [
        'UCjGe8SE-Zy1-wUjDt5w8LzA',  # Example channel ID
        # Add more channel IDs here
    ]
    
    for channel_id in sri_lankan_channels:
        collector.collect_channel_videos(channel_id)
        time.sleep(1)  # Rate limiting between channels

if __name__ == "__main__":
    main()
```

---

## 6. Machine Learning Development

### 6.1 Model Training Pipeline

```python
# scripts/model_training/train_models.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import joblib
from datetime import datetime
import logging

from src.data_access.repositories.video_repository import VideoRepository
from src.business.ml.feature_extractor import FeatureExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.video_repo = VideoRepository()
        self.feature_extractor = FeatureExtractor()
        self.models = {}
        self.preprocessors = {}
    
    def prepare_training_data(self):
        """Prepare training data from database"""
        logger.info("Preparing training data...")
        
        # Get all videos
        shorts = self.video_repo.get_shorts(limit=5000)
        longform = self.video_repo.get_long_form(limit=5000)
        
        # Extract features for each dataset
        shorts_data = self._extract_features_for_videos(shorts)
        longform_data = self._extract_features_for_videos(longform)
        
        return shorts_data, longform_data
    
    def _extract_features_for_videos(self, videos):
        """Extract features for a list of videos"""
        data = []
        
        for video in videos:
            try:
                features = self.feature_extractor.extract_features(video)
                
                # Add target variables (simulated for now)
                features['target_24h'] = video.view_count * 1.2  # Simulated
                features['target_7d'] = video.view_count * 2.0   # Simulated
                features['target_30d'] = video.view_count * 3.0  # Simulated
                
                data.append(features)
                
            except Exception as e:
                logger.error(f"Error extracting features for video {video.video_id}: {str(e)}")
                continue
        
        return pd.DataFrame(data)
    
    def train_model(self, data: pd.DataFrame, model_name: str):
        """Train XGBoost model"""
        logger.info(f"Training {model_name} model...")
        
        # Prepare features and targets
        feature_columns = [col for col in data.columns if not col.startswith('target_')]
        X = data[feature_columns]
        
        # Train separate models for different time intervals
        models = {}
        
        for interval in ['24h', '7d', '30d']:
            target_col = f'target_{interval}'
            if target_col not in data.columns:
                continue
            
            y = data[target_col]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Preprocess features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train XGBoost model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            logger.info(f"{model_name} {interval} - MAE: {mae:.2f}, RMSE: {rmse:.2f}")
            
            models[interval] = {
                'model': model,
                'scaler': scaler,
                'mae': mae,
                'rmse': rmse
            }
        
        # Save models
        self._save_models(models, model_name)
        return models
    
    def _save_models(self, models: Dict, model_name: str):
        """Save trained models to disk"""
        model_dir = 'data/models'
        os.makedirs(model_dir, exist_ok=True)
        
        # Save combined model (for simplicity, use 7d model as primary)
        if '7d' in models:
            model_path = os.path.join(model_dir, f'{model_name}_model.joblib')
            joblib.dump(models['7d']['model'], model_path)
            
            # Save preprocessor
            preprocessor_path = os.path.join(model_dir, f'{model_name}_preprocessor.joblib')
            joblib.dump(models['7d']['scaler'], preprocessor_path)
            
            logger.info(f"Saved {model_name} model to {model_path}")

def main():
    """Main training function"""
    trainer = ModelTrainer()
    
    # Prepare data
    shorts_data, longform_data = trainer.prepare_training_data()
    
    # Train models
    if not shorts_data.empty:
        trainer.train_model(shorts_data, 'shorts')
    
    if not longform_data.empty:
        trainer.train_model(longform_data, 'longform')
    
    logger.info("Model training completed")

if __name__ == "__main__":
    main()
```

---

## 7. Testing Implementation

### 7.1 Testing Strategy

**Testing Pyramid for ViewTrendsSL:**

```python
# tests/conftest.py
import pytest
import os
import sys
from unittest.mock import Mock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_youtube_client():
    """Mock YouTube API client for testing"""
    mock_client = Mock()
    mock_client.get_video_details.return_value = {
        'video_id': 'test_video_id',
        'channel_id': 'test_channel_id',
        'title': 'Test Video Title',
        'description': 'Test description',
        'published_at': '2025-01-01T12:00:00Z',
        'duration_seconds': 120,
        'category_id': 22,
        'view_count': 1000,
        'like_count': 50,
        'comment_count': 10,
        'tags': ['test', 'video']
    }
    return mock_client

@pytest.fixture
def sample_video_data():
    """Sample video data for testing"""
    return {
        'video_id': 'test123',
        'title': 'Test Video',
        'channel_name': 'Test Channel',
        'is_short': False,
        'current_views': 1000,
        'predictions': {
            '24_hours': 1200,
            '7_days': 2000,
            '30_days': 3000
        },
        'confidence_score': 0.85
    }
```

### 7.2 Unit Tests

```python
# tests/unit/test_services/test_prediction_service.py
import pytest
from unittest.mock import Mock, patch
from src.business.services.prediction_service import PredictionService

class TestPredictionService:
    def setup_method(self):
        """Setup test fixtures"""
        self.service = PredictionService()
    
    def test_extract_video_id_youtube_watch(self):
        """Test video ID extraction from youtube.com/watch URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = self.service._extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_youtu_be(self):
        """Test video ID extraction from youtu.be URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = self.service._extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self):
        """Test error handling for invalid URL"""
        url = "https://invalid-url.com"
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            self.service._extract_video_id(url)
    
    @patch('src.business.services.prediction_service.YouTubeAPIClient')
    @patch('src.business.services.prediction_service.VideoRepository')
    def test_predict_video_performance_success(self, mock_repo, mock_client):
        """Test successful video prediction"""
        # Setup mocks
        mock_video = Mock()
        mock_video.video_id = "test123"
        mock_video.title = "Test Video"
        mock_video.is_short = False
        mock_video.view_count = 1000
        mock_video.channel.channel_name = "Test Channel"
        
        mock_repo.return_value.get_by_video_id.return_value = mock_video
        
        # Mock feature extraction and prediction
        with patch.object(self.service.feature_extractor, 'extract_features') as mock_extract:
            with patch.object(self.service.prediction_engine, 'predict') as mock_predict:
                mock_extract.return_value = {'test_feature': 1.0}
                mock_predict.return_value = {
                    '24h': 1200,
                    '7d': 2000,
                    '30d': 3000,
                    'confidence': 0.85,
                    'timestamp': '2025-01-01T12:00:00'
                }
                
                result = self.service.predict_video_performance("https://youtube.com/watch?v=test123")
                
                assert result['video_id'] == "test123"
                assert result['predictions']['24_hours'] == 1200
                assert result['confidence_score'] == 0.85
```

### 7.3 Integration Tests

```python
# tests/integration/test_api/test_prediction_endpoints.py
import pytest
import json
from src.application.app import create_app

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestPredictionEndpoints:
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_predict_missing_video_url(self, client):
        """Test prediction endpoint with missing video URL"""
        response = client.post('/api/v1/predict', 
                             json={},
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'video_url is required' in data['error']
    
    def test_predict_invalid_video_url(self, client):
        """Test prediction endpoint with invalid video URL"""
        response = client.post('/api/v1/predict',
                             json={'video_url': 'invalid-url'},
                             content_type='application/json')
        assert response.status_code == 400
```

---

## 8. Deployment & DevOps

### 8.1 Docker Deployment

**Complete Docker Setup:**

```dockerfile
# config/docker/Dockerfile.prod
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p data/models data/logs && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose port
EXPOSE 5000

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "src.application.app:create_app()"]
```

### 8.2 Cloud Deployment Script

```bash
#!/bin/bash
# scripts/deployment/deploy.sh

set -e

echo "🚀 Starting ViewTrendsSL deployment..."

# Configuration
PROJECT_NAME="viewtrendssl"
DOCKER_IMAGE="$PROJECT_NAME:latest"
CONTAINER_NAME="$PROJECT_NAME-app"

# Build Docker image
echo "📦 Building Docker image..."
docker build -f config/docker/Dockerfile.prod -t $DOCKER_IMAGE .

# Stop existing container
echo "🛑 Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run new container
echo "▶️ Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p 5000:5000 \
    -p 8501:8501 \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    $DOCKER_IMAGE

# Wait for container to be ready
echo "⏳ Waiting for application to start..."
sleep 10

# Health check
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Deployment successful! Application is running at http://localhost:5000"
else
    echo "❌ Deployment failed! Check container logs:"
    docker logs $CONTAINER_NAME
    exit 1
fi
```

---

## 9. Team Collaboration Workflow

### 9.1 Git Workflow

**Branch Strategy:**
```bash
# Main branches
main          # Production-ready code
development   # Integration branch
feature/*     # Feature development
hotfix/*      # Critical bug fixes

# Example workflow
git checkout development
git pull origin development
git checkout -b feature/prediction-engine
# ... make changes ...
git add .
git commit -m "feat: implement XGBoost prediction engine"
git push origin feature/prediction-engine
# Create pull request to development
```

### 9.2 Code Review Checklist

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows PEP-8 style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data exposed
```

---

## 10. Troubleshooting Guide

### 10.1 Common Issues

**Issue: YouTube API Quota Exceeded**
```python
# Solution: Implement API key rotation
def handle_quota_exceeded():
    logger.warning("API quota exceeded, rotating key")
    self._rotate_api_key()
    return self.get_video_details(video_id)  # Retry
```

**Issue: Database Connection Errors**
```python
# Solution: Connection pooling and retry logic
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_db_connection():
    return create_engine(DATABASE_URL, pool_pre_ping=True)
```

**Issue: Model Loading Failures**
```python
# Solution: Fallback prediction mechanism
def _fallback_prediction(self, features, is_short):
    logger.warning("Using fallback prediction")
    base_views = 1000 if is_short else 500
    return {
        '24h': base_views,
        '7d': base_views * 3,
        '30d': base_views * 5,
        'confidence': 0.3
    }
```

### 10.2 Performance Optimization

**Database Query Optimization:**
```sql
-- Create indexes for common queries
CREATE INDEX idx_videos_channel_published ON videos(channel_id, published_at DESC);
CREATE INDEX idx_videos_is_short ON videos(is_short);
CREATE INDEX idx_snapshots_video_timestamp ON snapshots(video_id, timestamp);
```

**Caching Strategy:**
```python
# Redis caching for predictions
import redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_prediction(video_id):
    cached = cache.get(f"prediction:{video_id}")
    if cached:
        return json.loads(cached)
    return None

def cache_prediction(video_id, prediction, ttl=3600):
    cache.setex(f"prediction:{video_id}", ttl, json.dumps(prediction))
```

---

## 11. Quality Assurance

### 11.1 Code Quality Tools

**Setup Pre-commit Hooks:**
```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.9
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
```

### 11.2 Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main, development ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: password
          POSTGRES_DB: viewtrends_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 12. Final Implementation Checklist

### 12.1 MVP Completion Checklist

**Week 1-2: Foundation**
- [ ] Environment setup (Docker, APIs, Database)
- [ ] File structure implementation
- [ ] Database models and repositories
- [ ] Basic YouTube API integration

**Week 3-4: Core Development**
- [ ] Feature extraction pipeline
- [ ] Basic prediction engine (fallback)
- [ ] Flask API endpoints
- [ ] Streamlit UI foundation

**Week 5-6: Machine Learning**
- [ ] Data collection scripts
- [ ] Model training pipeline
- [ ] XGBoost model implementation
- [ ] Model evaluation and validation

**Week 7-8: Integration & Testing**
- [ ] End-to-end integration
- [ ] Unit and integration tests
- [ ] Performance optimization
- [ ] Bug fixes and refinements

**Week 9-10: Deployment & Documentation**
- [ ] Production deployment
- [ ] Final documentation
- [ ] Presentation preparation
- [ ] Academic report completion

### 12.2 Success Criteria

**Technical Metrics:**
- [ ] MAPE < 30% for 7-day predictions
- [ ] API response time < 30 seconds
- [ ] 99% uptime during evaluation period
- [ ] 80%+ test coverage

**Academic Requirements:**
- [ ] All documentation completed
- [ ] Live demonstration ready
- [ ] Research paper draft
- [ ] Dataset published

---

## Conclusion

This Development Guide provides a comprehensive roadmap for implementing the ViewTrendsSL system. Follow the layer-by-layer approach, maintain code quality standards, and ensure thorough testing throughout the development process.
- [ ] Academic report completion

### 12.2 Success Criteria

**Technical Metrics:**
- [ ] MAPE < 30% for 7-day predictions
- [ ] API response time < 30 seconds

**Week 7-8: Integration & Testing**
- [ ] End-to-end integration
- [ ] Unit and integration tests
- [ ] Performance optimization
- [ ] Bug fixes and refinements

**Week 9-10: Deployment & Documentation**
- [ ] Production deployment
- [ ] Final documentation
- [ ] Presentation preparation
- [ ] Academic report completion

### 12.2 Success Criteria

