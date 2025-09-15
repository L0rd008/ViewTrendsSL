# Model Training Scripts for ViewTrendsSL

This directory contains scripts for training, evaluating, and managing machine learning models for YouTube viewership prediction.

## Overview

The model training pipeline consists of three main components:

1. **Data Preparation** (`preprocessing/prepare_data.py`) - Cleans and prepares raw YouTube data for training
2. **Model Training** (`training/train_models.py`) - Trains separate models for Shorts and Long-form videos
3. **Model Evaluation** (`evaluation/evaluate_models.py`) - Evaluates trained models and generates performance reports

## Directory Structure

```
scripts/model_training/
├── preprocessing/
│   └── prepare_data.py          # Data cleaning and feature engineering
├── training/
│   └── train_models.py          # Model training pipeline
├── evaluation/
│   └── evaluate_models.py       # Model evaluation and analysis
└── README.md                    # This file
```

## Prerequisites

Before running the training scripts, ensure you have:

1. **Raw YouTube data** collected using the data collection scripts
2. **Python environment** with all required dependencies installed
3. **Sufficient disk space** for processed data and trained models

## Usage Guide

### Step 1: Data Preparation

First, prepare your raw YouTube data for training:

```bash
# Basic usage
python scripts/model_training/preprocessing/prepare_data.py data/raw/videos.csv

# Multiple data files
python scripts/model_training/preprocessing/prepare_data.py data/raw/videos_*.csv

# With custom output directory
python scripts/model_training/preprocessing/prepare_data.py data/raw/videos.csv --output-dir data/processed

# Dry run to validate data
python scripts/model_training/preprocessing/prepare_data.py data/raw/videos.csv --dry-run
```

**Output:**
- `data/processed/train_data.csv` - Training data
- `data/processed/val_data.csv` - Validation data  
- `data/processed/test_data.csv` - Test data
- `data/processed/training_data.csv` - Combined training data
- `data/processed/feature_info.json` - Feature metadata
- `data/processed/data_report.json` - Data quality report

### Step 2: Model Training

Train the prediction models using the prepared data:

```bash
# Basic training
python scripts/model_training/training/train_models.py

# With custom data path
python scripts/model_training/training/train_models.py --data-path data/processed/training_data.csv

# With custom output directory
python scripts/model_training/training/train_models.py --output-dir models/trained

# Dry run to validate setup
python scripts/model_training/training/train_models.py --dry-run
```

**Output:**
- `models/trained/shorts_model.joblib` - Trained Shorts model
- `models/trained/longform_model.joblib` - Trained Long-form model
- `models/metrics/shorts_metrics.json` - Shorts model metrics
- `models/metrics/longform_metrics.json` - Long-form model metrics
- `models/metrics/training_summary.json` - Overall training summary

### Step 3: Model Evaluation

Evaluate the trained models on test data:

```bash
# Basic evaluation
python scripts/model_training/evaluation/evaluate_models.py --test-data data/processed/test_data.csv

# With custom model directory
python scripts/model_training/evaluation/evaluate_models.py --test-data data/processed/test_data.csv --models-dir models/trained

# With custom output directory
python scripts/model_training/evaluation/evaluate_models.py --test-data data/processed/test_data.csv --output-dir models/evaluation
```

**Output:**
- `models/evaluation/evaluation_results.json` - Detailed evaluation results
- `models/evaluation/plots/` - Performance visualization plots
- `models/evaluation/reports/evaluation_summary.txt` - Human-readable summary

## Configuration

### Data Preparation Configuration

Create a JSON configuration file for data preparation:

```json
{
  "output_dir": "data/processed",
  "test_size": 0.2,
  "val_size": 0.2,
  "random_state": 42,
  "remove_outliers": true,
  "min_view_count": 1,
  "max_duration_hours": 4,
  "max_video_age_days": 730
}
```

Use with: `--config config/data_prep_config.json`

### Training Configuration

Create a JSON configuration file for model training:

```json
{
  "data_path": "data/processed/training_data.csv",
  "output_dir": "models/trained",
  "metrics_dir": "models/metrics",
  "test_size": 0.2,
  "validation_size": 0.2,
  "random_state": 42,
  "target_columns": ["views_at_24h", "views_at_7d", "views_at_30d"],
  "model_params": {
    "shorts": {
      "n_estimators": 100,
      "max_depth": 10,
      "learning_rate": 0.1
    },
    "longform": {
      "n_estimators": 150,
      "max_depth": 12,
      "learning_rate": 0.1
    }
  }
}
```

Use with: `--config config/training_config.json`

## Data Requirements

### Input Data Format

The raw data should be in CSV or JSON format with the following required columns:

- `video_id` - Unique YouTube video identifier
- `title` - Video title
- `channel_id` - YouTube channel identifier
- `published_at` - Publication timestamp
- `view_count` - Current view count
- `like_count` - Current like count
- `comment_count` - Current comment count
- `duration_seconds` - Video duration in seconds

### Optional Columns

- `description` - Video description
- `tags` - Video tags (comma-separated)
- `category_id` - YouTube category ID
- `subscriber_count` - Channel subscriber count
- `channel_title` - Channel name

## Model Architecture

### Shorts Model
- **Target**: Videos ≤ 60 seconds
- **Algorithm**: XGBoost Regressor
- **Features**: Title analysis, timing, engagement ratios
- **Prediction**: Views at 24h, 7d, 30d

### Long-form Model
- **Target**: Videos > 60 seconds
- **Algorithm**: XGBoost Regressor  
- **Features**: Duration, content analysis, channel metrics
- **Prediction**: Views at 24h, 7d, 30d

## Performance Metrics

The models are evaluated using:

- **MAPE** (Mean Absolute Percentage Error) - Primary metric
- **RMSE** (Root Mean Squared Error) - Scale-dependent error
- **MAE** (Mean Absolute Error) - Average absolute error
- **R² Score** - Coefficient of determination

### Target Performance

- **Good**: MAPE < 30%
- **Acceptable**: MAPE < 50%
- **Needs Improvement**: MAPE ≥ 50%

## Troubleshooting

### Common Issues

1. **Insufficient Data**
   ```
   Error: Limited shorts data: 45 samples
   ```
   - **Solution**: Collect more data or reduce minimum threshold in code

2. **Memory Issues**
   ```
   Error: Unable to allocate memory for model training
   ```
   - **Solution**: Reduce dataset size or use a machine with more RAM

3. **Feature Mismatch**
   ```
   Error: Feature names length mismatch
   ```
   - **Solution**: Ensure consistent feature engineering between training and evaluation

4. **Missing Dependencies**
   ```
   ModuleNotFoundError: No module named 'xgboost'
   ```
   - **Solution**: Install missing packages: `pip install -r requirements.txt`

### Data Quality Issues

1. **Check data completeness**:
   ```bash
   python scripts/model_training/preprocessing/prepare_data.py data/raw/videos.csv --dry-run
   ```

2. **Validate feature extraction**:
   ```bash
   python scripts/model_training/training/train_models.py --dry-run
   ```

3. **Review data report**:
   ```bash
   cat data/processed/data_report.json
   ```

## Advanced Usage

### Custom Feature Engineering

To add custom features, modify the `engineer_features` method in `prepare_data.py`:

```python
def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
    # Existing feature engineering...
    
    # Add your custom features
    df['custom_feature'] = df['title'].str.contains('trending')
    
    return df
```

### Model Hyperparameter Tuning

Modify the model parameters in the training configuration:

```json
{
  "model_params": {
    "shorts": {
      "n_estimators": 200,
      "max_depth": 15,
      "learning_rate": 0.05,
      "subsample": 0.8,
      "colsample_bytree": 0.8
    }
  }
}
```

### Batch Processing

For large datasets, process data in batches:

```bash
# Process multiple files
for file in data/raw/batch_*.csv; do
    python scripts/model_training/preprocessing/prepare_data.py "$file" --output-dir "data/processed/$(basename "$file" .csv)"
done
```

## Integration with Main Application

The trained models are automatically loaded by the main application:

1. **Model Loading**: Models are loaded from `models/trained/` directory
2. **Prediction Service**: Uses the trained models for real-time predictions
3. **API Endpoints**: Serve predictions through REST API

## Monitoring and Maintenance

### Model Performance Monitoring

1. **Regular Evaluation**: Run evaluation scripts monthly
2. **Performance Tracking**: Monitor MAPE trends over time
3. **Data Drift Detection**: Compare feature distributions

### Model Retraining

Retrain models when:
- Performance degrades (MAPE increases by >10%)
- New data patterns emerge
- YouTube algorithm changes significantly

### Automated Retraining Pipeline

```bash
#!/bin/bash
# Automated retraining script

# 1. Prepare new data
python scripts/model_training/preprocessing/prepare_data.py data/raw/latest_*.csv

# 2. Train models
python scripts\model_training\training\train_enhanced_models.py --train-data data\processed\training\train_data.csv --val-data data\processed\validation\val_data.csv --feature-info data\processed\features\feature_info.json

# 3. Evaluate performance
python scripts/model_training/evaluation/evaluate_models.py --test-data data/processed/test_data.csv

# 4. Deploy if performance is acceptable
# (Add deployment logic here)
```

## Support

For issues with the training scripts:

1. Check the logs in `training.log`
2. Review the troubleshooting section above
3. Ensure all dependencies are installed
4. Verify data format and completeness

## Next Steps

After successful model training:

1. **Deploy Models**: Copy trained models to production environment
2. **Set up Monitoring**: Implement performance tracking
3. **Schedule Retraining**: Set up automated retraining pipeline
4. **Optimize Performance**: Fine-tune hyperparameters based on results
