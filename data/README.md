# Data Directory

This directory contains all data assets for the ViewTrendsSL project, organized by processing stage and purpose.

## 📁 Directory Structure

### `/raw/` - Raw Data from APIs
**Purpose**: Unprocessed data directly from external sources
**Format**: JSON, CSV files with original API response structure
**Retention**: Permanent (for reproducibility and reprocessing)

#### `/raw/channels/`
**Contents**: Sri Lankan YouTube channel information
**Files**:
- `channels_YYYY-MM-DD.json` - Daily channel data snapshots
- `channel_metadata.csv` - Consolidated channel information
- `channel_validation.json` - Channel validation results
- `sri_lankan_channels_master.json` - Curated list of verified channels

**Data Schema**:
```json
{
  "channel_id": "UCxxxxxxxx",
  "title": "Channel Name",
  "description": "Channel description",
  "subscriber_count": 150000,
  "video_count": 1250,
  "view_count": 50000000,
  "country": "LK",
  "created_at": "2020-01-15T10:30:00Z",
  "custom_url": "@channelname",
  "thumbnails": {...}
}
```

#### `/raw/videos/`
**Contents**: Video metadata and statistics
**Files**:
- `videos_YYYY-MM-DD.csv` - Daily video data collection
- `video_metadata_full.json` - Complete video information
- `shorts_videos.csv` - YouTube Shorts specific data
- `longform_videos.csv` - Long-form video data

**Data Schema**:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "channel_id": "UCxxxxxxxx",
  "title": "Video Title",
  "description": "Video description",
  "published_at": "2023-08-01T14:30:00Z",
  "duration": "PT3M45S",
  "category_id": 10,
  "tags": ["music", "entertainment"],
  "view_count": 1000000,
  "like_count": 50000,
  "comment_count": 2500,
  "is_short": false
}
```

#### `/raw/snapshots/`
**Contents**: Time-series performance tracking data
**Files**:
- `snapshots_YYYY-MM-DD.csv` - Daily performance snapshots
- `hourly_tracking/` - Subdirectory for hourly tracking data
- `video_growth_curves.json` - Complete growth curve data

**Data Schema**:
```json
{
  "snapshot_id": "uuid",
  "video_id": "dQw4w9WgXcQ",
  "timestamp": "2023-08-01T15:00:00Z",
  "view_count": 1000000,
  "like_count": 50000,
  "comment_count": 2500,
  "hours_since_published": 24
}
```

### `/processed/` - Cleaned and Engineered Data
**Purpose**: Data ready for machine learning and analysis
**Format**: CSV, Parquet files optimized for ML workflows
**Retention**: Keep latest version + major milestones

#### `/processed/features/`
**Contents**: Engineered features for machine learning
**Files**:
- `features_shorts.csv` - Features for YouTube Shorts
- `features_longform.csv` - Features for long-form videos
- `feature_definitions.json` - Feature documentation
- `feature_importance.csv` - Feature importance rankings

**Feature Categories**:
- **Temporal Features**: `publish_hour`, `day_of_week`, `is_weekend`
- **Content Features**: `title_length`, `tag_count`, `description_length`
- **Channel Features**: `subscriber_count`, `channel_authority_score`
- **Engagement Features**: `early_engagement_rate`, `likes_per_view`
- **Language Features**: `detected_language`, `contains_sinhala`

#### `/processed/training/`
**Contents**: Training datasets for machine learning models
**Files**:
- `train_shorts.csv` - Training data for Shorts model
- `train_longform.csv` - Training data for long-form model
- `validation_shorts.csv` - Validation data for Shorts
- `validation_longform.csv` - Validation data for long-form
- `dataset_statistics.json` - Dataset summary statistics

**Data Split**:
- Training: 70% of data
- Validation: 15% of data
- Test: 15% of data (stored separately)

#### `/processed/validation/`
**Contents**: Test datasets for model evaluation
**Files**:
- `test_shorts.csv` - Test data for Shorts model evaluation
- `test_longform.csv` - Test data for long-form model evaluation
- `holdout_dataset.csv` - Holdout data for final evaluation
- `evaluation_results.json` - Model evaluation results

### `/models/` - Trained Machine Learning Models
**Purpose**: Serialized ML models and related artifacts
**Format**: Joblib, Pickle files with model metadata
**Retention**: Keep all versions for comparison and rollback

#### `/models/shorts/`
**Contents**: Models for YouTube Shorts prediction
**Files**:
- `shorts_model_v1.0.joblib` - Production Shorts model
- `shorts_preprocessor_v1.0.joblib` - Data preprocessing pipeline
- `shorts_model_metadata.json` - Model training metadata
- `shorts_performance_metrics.json` - Model performance results

**Model Artifacts**:
- Trained XGBoost model
- Feature preprocessing pipeline
- Feature scaler/encoder
- Model performance metrics
- Training configuration

#### `/models/longform/`
**Contents**: Models for long-form video prediction
**Files**:
- `longform_model_v1.0.joblib` - Production long-form model
- `longform_preprocessor_v1.0.joblib` - Data preprocessing pipeline
- `longform_model_metadata.json` - Model training metadata
- `longform_performance_metrics.json` - Model performance results

#### `/models/archived/`
**Contents**: Previous model versions and experimental models
**Files**:
- `shorts_model_v0.x.joblib` - Previous Shorts model versions
- `longform_model_v0.x.joblib` - Previous long-form model versions
- `experimental_models/` - Experimental model artifacts
- `model_comparison.json` - Performance comparison across versions

### `/logs/` - Application and Process Logs
**Purpose**: Logging for debugging, monitoring, and auditing
**Format**: Text log files with structured logging
**Retention**: Keep recent logs, archive older ones

#### `/logs/data_collection/`
**Contents**: Data collection process logs
**Files**:
- `collection_YYYY-MM-DD.log` - Daily collection logs
- `api_errors.log` - API error tracking
- `quota_usage.log` - API quota monitoring
- `data_quality.log` - Data quality issues

**Log Format**:
```
2023-08-01 14:30:00 INFO [collect_videos.py] Starting video collection for 150 channels
2023-08-01 14:30:15 DEBUG [youtube_api.py] API call successful: videos.list
2023-08-01 14:30:16 WARNING [data_validator.py] Missing tags for video dQw4w9WgXcQ
2023-08-01 14:30:30 ERROR [youtube_api.py] API quota exceeded, switching to key 2
```

#### `/logs/training/`
**Contents**: Model training process logs
**Files**:
- `training_YYYY-MM-DD.log` - Training session logs
- `hyperparameter_tuning.log` - Hyperparameter optimization logs
- `model_evaluation.log` - Model evaluation results
- `feature_engineering.log` - Feature engineering process logs

#### `/logs/application/`
**Contents**: Web application runtime logs
**Files**:
- `app_YYYY-MM-DD.log` - Daily application logs
- `api_requests.log` - API request/response logs
- `prediction_requests.log` - Prediction request tracking
- `error.log` - Application error logs

## 📊 Data Flow Pipeline

```
Raw Data Collection → Data Validation → Feature Engineering → Model Training → Model Deployment
       ↓                    ↓                 ↓                 ↓               ↓
   /raw/videos/      /processed/clean/   /processed/features/  /models/shorts/  Production API
   /raw/channels/    Data Quality        Feature Selection     /models/longform/ Web Application
   /raw/snapshots/   Validation          Target Creation       Model Artifacts   Predictions
```

## 🔧 Data Management

### Data Quality Standards
- **Completeness**: <5% missing values in critical fields
- **Accuracy**: >95% accuracy in automated validation checks
- **Consistency**: Standardized formats and schemas
- **Timeliness**: Data freshness within 24 hours
- **Validity**: All data passes schema validation

### Data Retention Policy
- **Raw Data**: Permanent retention for reproducibility
- **Processed Data**: Keep latest + quarterly snapshots
- **Models**: Keep all versions for 1 year, then archive best performers
- **Logs**: Keep 90 days online, archive for 1 year

### Backup Strategy
- **Daily Backups**: Automated backup of all data directories
- **Weekly Full Backups**: Complete data directory backup
- **Monthly Archives**: Compressed archives for long-term storage
- **Cloud Sync**: Sync critical data to cloud storage

## 📋 Data Governance

### Access Control
- **Raw Data**: Read-only access for data scientists
- **Processed Data**: Read/write for ML engineers
- **Models**: Controlled deployment process
- **Logs**: Monitoring team access

### Data Privacy
- **No PII**: No personally identifiable information stored
- **Public Data Only**: Only public YouTube data collected
- **Anonymization**: Channel/video IDs used instead of names where possible
- **Compliance**: Adherence to YouTube API Terms of Service

### Data Documentation
- **Schema Documentation**: Complete schema definitions
- **Data Dictionary**: Field definitions and descriptions
- **Lineage Tracking**: Data source and transformation tracking
- **Change Log**: Documentation of data structure changes

## 🚀 Usage Guidelines

### For Data Scientists
```bash
# Access training data
pandas.read_csv('data/processed/training/train_shorts.csv')

# Load feature definitions
with open('data/processed/features/feature_definitions.json') as f:
    features = json.load(f)
```

### For ML Engineers
```bash
# Load trained model
import joblib
model = joblib.load('data/models/shorts/shorts_model_v1.0.joblib')

# Load preprocessing pipeline
preprocessor = joblib.load('data/models/shorts/shorts_preprocessor_v1.0.joblib')
```

### For Application Developers
```bash
# Access latest model
model_path = 'data/models/shorts/shorts_model_v1.0.joblib'
model = joblib.load(model_path)

# Make predictions
predictions = model.predict(features)
```

## 🎯 Future Enhancements

- **Real-time Data Streaming**: Implement streaming data pipeline
- **Data Lake Architecture**: Migrate to cloud-based data lake
- **Advanced Analytics**: Add real-time analytics capabilities
- **Multi-platform Data**: Extend to TikTok, Instagram data
- **Data Versioning**: Implement comprehensive data versioning
- **Automated Quality Monitoring**: Real-time data quality monitoring
