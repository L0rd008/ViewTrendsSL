# Enhanced ViewTrendsSL Data Processing and Model Training

This document describes the enhanced data processing and model training pipeline that utilizes all available features from your collected CSV data, including the comprehensive time-series information.

## Overview

The enhanced pipeline consists of two main components:

1. **Enhanced CSV Data Processing** (`scripts/data_processing/process_csv_data.py`)
2. **Enhanced Model Training** (`scripts/model_training/train_enhanced_models.py`)

These scripts are designed to work with your collected CSV data (`data/raw/merged_data_20250904_081116.csv`) and extract maximum value from all available features.

## Features Extracted

### Time-Series Features
- **Target Variables**: Real views at 24h, 7d, and 30d from your time-series data
- **Growth Velocity**: Early growth patterns in the first week
- **Peak Day**: Day with maximum views for each video
- **Growth Consistency**: Measure of how consistent the growth pattern is
- **Engagement Progression**: Like and comment growth rates over time
- **Time-Point Ratios**: Engagement ratios at specific days (1, 7, 30)

### Content Features
- **Title Analysis**: Length, word count, language detection, emoji count, caps ratio
- **Description Analysis**: Length, word count, hashtag count, link detection
- **Duration Features**: Optimal duration flags, duration categories
- **Category Mapping**: YouTube category IDs mapped to meaningful names
- **Temporal Features**: Publish hour, day of week, seasonal patterns, prime time flags

### Engagement Features
- **Basic Ratios**: Like-to-view, comment-to-view, overall engagement rate
- **Quality Indicators**: High engagement flags, viral potential indicators
- **Velocity Metrics**: Engagement growth rates and consistency measures

### Channel Features
- **Authority Metrics**: Channel-level statistics and authority scores
- **Performance Context**: Relative performance compared to channel average
- **Consistency Scores**: How consistent the channel's performance is

## Usage Instructions

### Step 1: Process Your CSV Data

First, process your raw CSV data to extract all features:

```bash
# Basic usage
python scripts/data_processing/process_csv_data.py data/raw/merged_data_20250904_081116.csv

# With custom output directory
python scripts/data_processing/process_csv_data.py data/raw/merged_data_20250904_081116.csv --output-dir data/processed_enhanced

# Dry run to validate data first
python scripts/data_processing/process_csv_data.py data/raw/merged_data_20250904_081116.csv --dry-run
```

**Output Files:**
- `data/processed/train_data.csv` - Training split
- `data/processed/val_data.csv` - Validation split  
- `data/processed/test_data.csv` - Test split
- `data/processed/training_data.csv` - Combined training data
- `data/processed/feature_info.json` - Feature metadata
- `data/processed/processing_report.json` - Comprehensive processing report

### Step 2: Train Enhanced Models

Train models using the processed data with all extracted features:

```bash
# Basic training with separate models for Shorts and Long-form
python scripts/model_training/train_enhanced_models.py data/processed/training_data.csv --feature-info data/processed/feature_info.json

# Train unified models (single model for all content types)
python scripts/model_training/train_enhanced_models.py data/processed/training_data.csv --unified

# Use different model types
python scripts/model_training/train_enhanced_models.py data/processed/training_data.csv --model-type random_forest

# Custom output directories
python scripts/model_training/train_enhanced_models.py data/processed/training_data.csv --models-dir models_enhanced --results-dir results_enhanced
```

**Output Files:**
- `models/shorts_views_at_24h_model.joblib` - Shorts 24h model
- `models/shorts_views_at_7d_model.joblib` - Shorts 7d model
- `models/shorts_views_at_30d_model.joblib` - Shorts 30d model
- `models/longform_views_at_24h_model.joblib` - Long-form 24h model
- `models/longform_views_at_7d_model.joblib` - Long-form 7d model
- `models/longform_views_at_30d_model.joblib` - Long-form 30d model
- `results/training_results_YYYYMMDD_HHMMSS.json` - Training metrics
- `results/training_report_YYYYMMDD_HHMMSS.txt` - Human-readable report

## Complete Workflow Example

Here's a complete example of processing your data and training models:

```bash
# Step 1: Process the CSV data
echo "Processing CSV data..."
python scripts/data_processing/process_csv_data.py data/raw/merged_data_20250904_081116.csv

# Step 2: Train enhanced models
echo "Training enhanced models..."
python scripts/model_training/train_enhanced_models.py data/processed/training_data.csv --feature-info data/processed/feature_info.json

# Step 3: Check results
echo "Training completed! Check the results:"
echo "- Models saved in: models/"
echo "- Results saved in: results/"
echo "- Latest training report:"
ls -la results/training_report_*.txt | tail -1
```

## Configuration Options

### Data Processing Configuration

Create a JSON configuration file for data processing:

```json
{
  "output_dir": "data/processed",
  "test_size": 0.15,
  "val_size": 0.15,
  "random_state": 42,
  "remove_outliers": true,
  "min_view_count": 1,
  "max_duration_hours": 4,
  "max_video_age_days": 730
}
```

Use with: `--config config/data_processing_config.json`

### Model Training Configuration

Create a JSON configuration file for model training:

```json
{
  "models_dir": "models",
  "results_dir": "results",
  "separate_by_content_type": true,
  "save_models": true,
  "save_results": true,
  "model_type": "xgboost",
  "n_estimators": 150,
  "max_depth": 8,
  "learning_rate": 0.1,
  "subsample": 0.8,
  "colsample_bytree": 0.8,
  "val_size": 0.2,
  "min_samples": 50,
  "random_state": 42
}
```

Use with: `--config config/model_training_config.json`

## Key Improvements Over Original Scripts

### 1. Real Time-Series Target Variables
- **Before**: Synthetic targets based on current view counts
- **After**: Real targets from your day_1_views, day_7_views, day_30_views columns

### 2. Comprehensive Feature Engineering
- **Before**: Basic features only
- **After**: 80+ features including time-series patterns, content analysis, engagement metrics, and channel statistics

### 3. Advanced Time-Series Analysis
- **Before**: No time-series features
- **After**: Growth velocity, peak detection, consistency measures, engagement progression

### 4. Content Intelligence
- **Before**: Basic title/description length
- **After**: Language detection, emoji analysis, optimal duration flags, category mapping

### 5. Channel Context
- **Before**: No channel-level features
- **After**: Channel authority, consistency scores, relative performance metrics

### 6. Better Data Splitting
- **Before**: Random splitting
- **After**: Time-based splitting (older data for training, newer for testing)

## Expected Performance Improvements

With the enhanced features, you should expect:

1. **Better MAPE Scores**: Target <25% for Shorts, <30% for Long-form
2. **Higher R² Values**: Target >0.7 for both content types
3. **More Stable Predictions**: Better generalization due to comprehensive features
4. **Content-Aware Models**: Separate models that understand Shorts vs Long-form dynamics

## Feature Importance Analysis

The enhanced pipeline automatically identifies and categorizes features:

- **Time-Series Features**: Growth patterns, velocity, consistency
- **Content Features**: Title, description, duration, category analysis
- **Engagement Features**: Ratios, quality indicators, progression metrics
- **Channel Features**: Authority, consistency, relative performance

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install isodate langdetect
   ```

2. **Memory Issues with Large CSV**
   - Process in chunks or use a machine with more RAM
   - The script uses `low_memory=False` for proper data type inference

3. **Insufficient Data for Content Type**
   - The script requires minimum 50 samples per content type
   - Use `--unified` flag if you have insufficient Shorts or Long-form data

4. **Feature Processing Errors**
   - Check the processing report for data quality issues
   - Use `--dry-run` to validate data before processing

### Performance Optimization

1. **For Large Datasets**:
   - Use `n_jobs=-1` in model configuration
   - Consider using `model_type=linear` for faster training

2. **For Better Accuracy**:
   - Increase `n_estimators` to 200-300
   - Use `max_depth` of 10-12 for complex patterns
   - Enable hyperparameter tuning (can be added to the script)

## Next Steps

After training your enhanced models:

1. **Evaluate Performance**: Check the training reports and metrics
2. **Feature Analysis**: Review feature importance from the models
3. **Model Deployment**: Integrate the trained models into your main application
4. **Continuous Improvement**: Retrain models as you collect more data

## Integration with Existing Scripts

The enhanced scripts are designed to work alongside your existing scripts:

- **Data Collection**: Continue using your existing collection scripts
- **Model Serving**: Update your prediction services to use the new models
- **API Integration**: The models are compatible with your existing API structure

The enhanced models will provide significantly better predictions by utilizing all the rich information in your collected data, especially the valuable time-series patterns that show how videos actually perform over time.
