# Scripts Directory

This directory contains automation scripts for data collection, model training, database management, and deployment operations.

## 📁 Directory Structure

### `/data_collection/` - Data Harvesting Scripts
**Purpose**: Automated data collection from YouTube and other sources
**Technology**: Python, YouTube Data API v3
**Execution**: Scheduled (cron jobs) or manual execution

#### `/data_collection/youtube/`
**Scripts**:
- `collect_channels.py` - Discover and validate Sri Lankan YouTube channels
- `collect_videos.py` - Extract video metadata and statistics
- `track_performance.py` - Monitor video performance over time
- `channel_validator.py` - Validate channel relevance to Sri Lankan audience
- `api_quota_manager.py` - Manage API key rotation and quota tracking

**Key Features**:
- API key rotation for quota management
- Error handling and retry logic
- Data validation and quality checks
- Rate limiting to respect API constraints
- Logging and monitoring

#### `/data_collection/monitoring/`
**Scripts**:
- `data_quality_monitor.py` - Monitor data collection quality
- `api_health_check.py` - Check API availability and performance
- `collection_metrics.py` - Generate data collection reports
- `alert_system.py` - Send alerts for collection failures

#### `/data_collection/validation/`
**Scripts**:
- `data_validator.py` - Validate collected data integrity
- `duplicate_detector.py` - Identify and handle duplicate records
- `schema_validator.py` - Ensure data conforms to expected schema
- `quality_scorer.py` - Score data quality metrics

### `/model_training/` - Machine Learning Pipeline Scripts
**Purpose**: Automated ML model training, evaluation, and deployment
**Technology**: Python, XGBoost, Scikit-learn
**Execution**: Scheduled retraining or manual execution

#### `/model_training/preprocessing/`
**Scripts**:
- `feature_engineer.py` - Create features from raw data
- `data_cleaner.py` - Clean and preprocess training data
- `train_test_split.py` - Split data for training and validation
- `feature_selector.py` - Select optimal features for training
- `data_transformer.py` - Apply transformations (scaling, encoding)

**Key Features**:
- Automated feature engineering pipeline
- Data quality validation
- Feature importance analysis
- Preprocessing pipeline serialization

#### `/model_training/training/`
**Scripts**:
- `train_shorts_model.py` - Train model for YouTube Shorts
- `train_longform_model.py` - Train model for long-form videos
- `hyperparameter_tuner.py` - Optimize model hyperparameters
- `ensemble_trainer.py` - Train ensemble models
- `model_validator.py` - Validate trained models

**Key Features**:
- Cross-validation for robust training
- Hyperparameter optimization
- Model versioning and serialization
- Training progress monitoring

#### `/model_training/evaluation/`
**Scripts**:
- `model_evaluator.py` - Comprehensive model evaluation
- `performance_analyzer.py` - Analyze model performance metrics
- `comparison_tool.py` - Compare different model versions
- `prediction_validator.py` - Validate predictions on test data
- `report_generator.py` - Generate evaluation reports

**Key Features**:
- Multiple evaluation metrics (MAPE, MAE, RMSE)
- Performance visualization
- Model comparison reports
- Prediction confidence analysis

### `/database/` - Database Management Scripts
**Purpose**: Database setup, maintenance, and backup operations
**Technology**: Python, SQLAlchemy, PostgreSQL/SQLite
**Execution**: Manual or scheduled maintenance

#### `/database/setup/`
**Scripts**:
- `init_database.py` - Initialize database schema
- `create_tables.py` - Create database tables
- `setup_indexes.py` - Create database indexes for performance
- `seed_data.py` - Insert initial/test data
- `migration_runner.py` - Run database migrations

#### `/database/backup/`
**Scripts**:
- `backup_database.py` - Create database backups
- `restore_database.py` - Restore from backup
- `backup_scheduler.py` - Schedule automated backups
- `backup_validator.py` - Validate backup integrity
- `cleanup_old_backups.py` - Remove old backup files

#### `/database/maintenance/`
**Scripts**:
- `optimize_database.py` - Optimize database performance
- `cleanup_old_data.py` - Remove outdated data
- `update_statistics.py` - Update database statistics
- `health_check.py` - Check database health
- `reindex_tables.py` - Rebuild database indexes

### `/deployment/` - Deployment Automation Scripts
**Purpose**: Automated deployment and infrastructure management
**Technology**: Docker, Cloud platforms, Shell scripts
**Execution**: CI/CD pipelines or manual deployment

#### `/deployment/docker/`
**Scripts**:
- `build_image.py` - Build Docker images
- `deploy_container.py` - Deploy Docker containers
- `health_check.py` - Check container health
- `update_deployment.py` - Update running deployments
- `cleanup_images.py` - Clean up old Docker images

#### `/deployment/cloud/`
**Scripts**:
- `deploy_to_heroku.py` - Deploy to Heroku platform
- `deploy_to_aws.py` - Deploy to AWS (future)
- `setup_environment.py` - Set up cloud environment
- `configure_scaling.py` - Configure auto-scaling
- `manage_secrets.py` - Manage environment secrets

#### `/deployment/monitoring/`
**Scripts**:
- `setup_monitoring.py` - Set up application monitoring
- `log_aggregator.py` - Aggregate application logs
- `alert_configurator.py` - Configure monitoring alerts
- `performance_monitor.py` - Monitor application performance
- `uptime_checker.py` - Check application uptime

## 🚀 Usage Examples

### Data Collection
```bash
# Collect data from Sri Lankan channels
python scripts/data_collection/youtube/collect_videos.py --channels=config/sri_lankan_channels.json

# Monitor video performance
python scripts/data_collection/youtube/track_performance.py --days=7
```

### Model Training
```bash
# Train models for both video types
python scripts/model_training/training/train_shorts_model.py
python scripts/model_training/training/train_longform_model.py

# Evaluate model performance
python scripts/model_training/evaluation/model_evaluator.py --model=shorts
```

### Database Operations
```bash
# Initialize database
python scripts/database/setup/init_database.py

# Create backup
python scripts/database/backup/backup_database.py --output=backups/
```

### Deployment
```bash
# Deploy to production
python scripts/deployment/docker/deploy_container.py --environment=production

# Check deployment health
python scripts/deployment/monitoring/health_check.py
```

## 📋 Script Standards

### Code Quality
- Follow PEP-8 style guidelines
- Include comprehensive error handling
- Add logging for debugging and monitoring
- Write docstrings for all functions
- Include type hints where appropriate

### Configuration
- Use environment variables for configuration
- Support command-line arguments
- Include configuration validation
- Provide sensible defaults
- Document all configuration options

### Error Handling
- Implement retry logic for external APIs
- Log errors with appropriate detail
- Provide meaningful error messages
- Handle edge cases gracefully
- Include cleanup on failure

### Monitoring
- Log script execution start/end
- Track execution time and performance
- Monitor resource usage
- Alert on failures
- Generate execution reports

## 🔧 Development Guidelines

1. **Modularity**: Keep scripts focused on single responsibilities
2. **Reusability**: Create shared utilities for common operations
3. **Testing**: Write unit tests for critical script functions
4. **Documentation**: Document script purpose, usage, and parameters
5. **Logging**: Implement comprehensive logging for debugging
6. **Configuration**: Make scripts configurable through environment variables
7. **Error Handling**: Implement robust error handling and recovery
8. **Performance**: Optimize scripts for efficiency and resource usage

## 📅 Execution Schedule

### Daily Scripts
- `track_performance.py` - Monitor video performance
- `data_quality_monitor.py` - Check data quality
- `backup_database.py` - Create daily backups

### Weekly Scripts
- `collect_videos.py` - Collect new video data
- `train_models.py` - Retrain ML models
- `cleanup_old_data.py` - Clean up outdated data

### Monthly Scripts
- `optimize_database.py` - Database optimization
- `model_evaluator.py` - Comprehensive model evaluation
- `cleanup_old_backups.py` - Remove old backups

## 🎯 Future Enhancements

- **Parallel Processing**: Implement multiprocessing for large-scale operations
- **Cloud Integration**: Add support for cloud-based execution
- **Real-time Processing**: Implement streaming data processing
- **Advanced Monitoring**: Add comprehensive monitoring and alerting
- **Auto-scaling**: Implement automatic resource scaling
- **Multi-platform Support**: Extend to other social media platforms
