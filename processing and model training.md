# ViewTrendsSL: Comprehensive Technical Analysis and Documentation

## Overview

ViewTrendsSL is a machine learning project designed to predict YouTube video performance using historical data from the YouTube API v3. The system consists of two main components: data processing (`process_csv_data.py`) and model training (`train_enhanced_models.py`). The goal is to predict view counts at specific time intervals (24 hours, 7 days, and 30 days) using only metadata available at the time of upload.

## Raw Data Structure and Context

The raw data comes from YouTube API v3 and contains 103 columns with rich temporal information:

### Core Video Metadata
- **Basic identifiers**: `id`, `channel_id`, `published_at`, `inserted_at`
- **Content metadata**: `title`, `description`, `localized_title`, `localized_description`
- **Visual assets**: `thumbnail_default`, `thumbnail_medium`, `thumbnail_high`
- **Classification**: `tags`, `category_id`, `live_broadcast_content`
- **Language**: `default_language`, `default_audio_language`
- **Duration**: `video_duration` (ISO 8601 format)

### Current Engagement Metrics
- `view_count`, `likes_count`, `favourite_count`, `comment_count`

### Time-Series Data (30 days each)
- **Views**: `day_1_views` through `day_30_views`
- **Likes**: `day_1_likes` through `day_30_likes` 
- **Comments**: `day_1_comments` through `day_30_comments`

This time-series structure provides a unique opportunity to understand video growth patterns over time, which is crucial for accurate performance prediction.

---

## Part 1: Data Processing Pipeline (`process_csv_data.py`)

### Architecture and Design Philosophy

The `EnhancedCSVProcessor` class follows a modular, pipeline-based approach with clear separation of concerns. Each processing step builds upon the previous one, creating a comprehensive feature engineering pipeline.

### 1. Data Loading and Initial Processing

#### CSV Loading Strategy
```python
df = pd.read_csv(csv_path, low_memory=False)
```

**Why `low_memory=False`?**
- YouTube data has mixed data types across columns
- Prevents pandas from making incorrect type inferences
- Ensures consistent data loading across different file sizes

#### Column Standardization
```python
column_mapping = {
    'id': 'video_id',
    'likes_count': 'like_count',
    'video_duration': 'duration_iso8601'
}
```

**Reasoning**: Creates consistent naming conventions that make the codebase more maintainable and reduces confusion between similar column names.

### 2. Data Cleaning and Standardization

#### Duration Processing
```python
def _parse_duration_to_seconds(self, duration_str: str) -> int:
    try:
        duration = parse_duration(duration_str)
        return int(duration.total_seconds())
    except Exception:
        return 0
```

**Why ISO 8601 parsing?**
- YouTube API returns durations in ISO 8601 format (e.g., "PT3M2S" = 3 minutes 2 seconds)
- Converting to seconds enables numerical analysis and feature engineering
- Standardized format ensures consistency across all videos

#### Missing Data Strategy
**For critical columns**: `dropna()` - Videos without basic metadata can't be properly analyzed
**For engagement metrics**: `fillna(0)` - Zero engagement is meaningful data, not missing data
**For time-series**: `pd.to_numeric(..., errors='coerce')` - Converts invalid entries to NaN, then handles appropriately

#### Outlier Removal Logic
```python
# Remove videos with zero duration
df = df[df['duration_seconds'] > 0]

# Remove videos with unrealistic durations (> 4 hours)
df = df[df['duration_seconds'] <= 14400]

# Remove extreme outliers in view count (top 0.1%)
view_threshold = df['view_count'].quantile(0.999)
df = df[df['view_count'] <= view_threshold]
```

**Mathematical reasoning**:
- **Zero duration**: Invalid videos or processing errors
- **4-hour limit**: Removes outliers like live streams or corrupted data while keeping legitimate long-form content
- **99.9th percentile threshold**: Removes statistical outliers while preserving viral videos (uses quantile-based approach rather than standard deviation to handle non-normal distributions)

#### YouTube Shorts Classification
```python
df['is_short'] = df['duration_seconds'] <= 60
```

**Business logic**: YouTube Shorts have different algorithmic treatment, engagement patterns, and performance characteristics. The 60-second threshold aligns with YouTube's official Shorts definition.

### 3. Time-Series Feature Engineering

This is the most sophisticated part of the processing pipeline, extracting meaningful patterns from the day-by-day engagement data.

#### Target Variable Creation
```python
if 'day_1_views' in df.columns:
    df['views_at_24h'] = df['day_1_views']
if 'day_7_views' in df.columns:
    df['views_at_7d'] = df['day_7_views']
if 'day_30_views' in df.columns:
    df['views_at_30d'] = df['day_30_views']
```

**Why these specific time points?**
- **24 hours**: Critical early indicator of video success
- **7 days**: Captures the initial recommendation cycle
- **30 days**: Long-term performance indicator

#### Growth Velocity Calculation
```python
def _calculate_growth_velocity(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
    growth_rates = []
    for i in range(1, min(len(view_columns), 8)):  # First 7 days
        if i < len(view_columns):
            prev_col = view_columns[i-1]
            curr_col = view_columns[i]
            daily_growth = (df[curr_col] - df[prev_col]) / np.maximum(df[prev_col], 1)
            growth_rates.append(daily_growth)
    
    if growth_rates:
        return pd.concat(growth_rates, axis=1).mean(axis=1)
```

**Mathematical foundation**: 
- Calculates relative daily growth rate: `(current_views - previous_views) / previous_views`
- Uses `np.maximum(..., 1)` to prevent division by zero
- Averages across early days to create a stable velocity metric
- Early growth velocity is a strong predictor of long-term success

#### Peak Day Detection
```python
def _find_peak_day(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
    view_data = df[view_columns]
    peak_days = view_data.idxmax(axis=1)
    peak_day_numbers = peak_days.apply(
        lambda x: int(x.split('_')[1]) if pd.notna(x) else 1
    )
    return peak_day_numbers
```

**Business insight**: Videos that peak early (day 1-3) often rely on immediate audience, while videos that peak later (day 7+) may benefit from algorithmic discovery. This pattern is crucial for understanding video lifecycle.

#### Growth Consistency Measurement
```python
def _calculate_growth_consistency(self, df: pd.DataFrame, view_columns: List[str]) -> pd.Series:
    # Calculate daily growth rates
    growth_rates = []
    for i in range(1, len(view_columns)):
        prev_col = view_columns[i-1]
        curr_col = view_columns[i]
        daily_growth = (df[curr_col] - df[prev_col]) / np.maximum(df[prev_col], 1)
        growth_rates.append(daily_growth)
    
    if growth_rates:
        growth_df = pd.concat(growth_rates, axis=1)
        return growth_df.std(axis=1)  # Standard deviation of growth rates
```

**Statistical reasoning**: Lower standard deviation indicates more consistent growth. Videos with erratic growth patterns (high std) may be driven by external factors, while consistent growth suggests sustainable organic reach.

#### Engagement Ratio Engineering
```python
for day in [1, 7, 30]:
    view_col = f'day_{day}_views'
    like_col = f'day_{day}_likes'
    comment_col = f'day_{day}_comments'
    
    if view_col in df.columns:
        if like_col in df.columns:
            df[f'like_ratio_day_{day}'] = df[like_col] / np.maximum(df[view_col], 1)
        if comment_col in df.columns:
            df[f'comment_ratio_day_{day}'] = df[comment_col] / np.maximum(df[view_col], 1)
```

**Engagement theory**: Ratios normalize engagement across different view counts, allowing comparison between videos of different sizes. These ratios often indicate content quality and audience resonance.

### 4. Content Feature Engineering

#### Title Analysis Features
```python
df['title_length'] = df['title'].str.len()
df['title_word_count'] = df['title'].str.split().str.len()
df['title_has_question'] = df['title'].str.contains(r'\?', na=False)
df['title_has_exclamation'] = df['title'].str.contains(r'!', na=False)
df['title_all_caps_ratio'] = df['title'].apply(self._calculate_caps_ratio)
df['title_has_numbers'] = df['title'].str.contains(r'\d', na=False)
df['title_emoji_count'] = df['title'].apply(self._count_emojis)
```

**Psychological/Marketing reasoning**:
- **Length/Word count**: Optimal title length varies by platform and audience
- **Questions**: Create curiosity and improve click-through rates
- **Exclamations**: Indicate excitement but can appear clickbait-y
- **ALL CAPS ratio**: High ratios may indicate spam or low-quality content
- **Numbers**: Often improve click-through (e.g., "5 Tips", "Top 10")
- **Emojis**: Can improve visibility and emotional connection

#### Language Detection
```python
def _detect_language(self, text: str) -> str:
    if not text or len(text.strip()) == 0:
        return 'unknown'
    try:
        from langdetect import detect
        return detect(text)
    except:
        return 'unknown'

df['title_language'] = df['title'].apply(self._detect_language)
df['title_is_sinhala'] = df['title_language'] == 'si'
df['title_is_tamil'] = df['title_language'] == 'ta'
df['title_is_english'] = df['title_language'] == 'en'
```

**Regional context**: Sri Lankan content spans multiple languages. Language choice affects discoverability, audience reach, and engagement patterns. This is crucial for understanding the local YouTube ecosystem.

#### Temporal Feature Engineering
```python
df['publish_hour'] = df['published_at'].dt.hour
df['publish_day_of_week'] = df['published_at'].dt.dayofweek
df['publish_month'] = df['published_at'].dt.month
df['is_weekend'] = df['publish_day_of_week'].isin([5, 6])
df['is_prime_time'] = df['publish_hour'].isin([19, 20, 21])  # 7-9 PM
```

**Audience behavior insights**:
- **Hour**: Peak viewing times affect initial performance
- **Day of week**: Weekend vs weekday patterns differ significantly
- **Prime time (7-9 PM)**: Aligns with typical Sri Lankan viewing habits
- **Seasonality**: Affects content preferences and viewing time

#### Duration Optimization Features
```python
df['is_optimal_short'] = (df['duration_seconds'] >= 15) & (df['duration_seconds'] <= 60)
df['is_optimal_longform'] = (df['duration_seconds'] >= 180) & (df['duration_seconds'] <= 480)
```

**Algorithmic understanding**: 
- **Optimal Shorts (15-60s)**: Too short may lack content, too long loses Short status
- **Optimal long-form (3-8 minutes)**: Balances watch time and retention based on YouTube's algorithm preferences

### 5. Channel-Level Feature Engineering

```python
def create_channel_features(self, df: pd.DataFrame) -> pd.DataFrame:
    channel_stats = df.groupby('channel_id').agg({
        'view_count': ['mean', 'median', 'std', 'count'],
        'like_count': ['mean', 'median'],
        'comment_count': ['mean', 'median'],
        'duration_seconds': ['mean', 'median'],
        'is_short': 'mean'  # Proportion of shorts
    }).round(2)
    
    # Channel authority score (composite metric)
    channel_stats['channel_authority'] = (
        np.log1p(channel_stats['channel_avg_views']) * 0.4 +
        np.log1p(channel_stats['channel_video_count']) * 0.3 +
        channel_stats['channel_avg_likes'] / np.maximum(channel_stats['channel_avg_views'], 1) * 100 * 0.3
    )
```

**Authority Score Logic**:
- **40% weight on log(avg_views)**: Logarithmic scale handles wide view count ranges
- **30% weight on log(video_count)**: Consistency and prolific content creation
- **30% weight on engagement rate**: Quality over quantity
- This composite metric captures channel influence and quality

#### Relative Performance Metrics
```python
df['relative_performance'] = df['view_count'] / np.maximum(df['channel_avg_views'], 1)
df['above_channel_average'] = df['view_count'] > df['channel_avg_views']
```

**Normalization rationale**: A video with 10K views might be exceptional for a small channel but poor for a large channel. Relative metrics enable fair comparison across channels of different sizes.

### 6. Data Splitting Strategy

#### Time-Based Splitting
```python
if 'published_at' in df.columns:
    df = df.sort_values('published_at').reset_index(drop=True)
    
    total_size = len(df)
    train_end = int(total_size * 0.7)
    val_end = int(total_size * 0.85)
    
    train_df = df[:train_end].copy()
    val_df = df[train_end:val_end].copy()
    test_df = df[val_end:].copy()
```

**Why time-based instead of random splitting?**
- **Temporal consistency**: Prevents data leakage from future to past
- **Realistic evaluation**: Models are tested on truly unseen future data
- **Algorithm evolution**: YouTube's algorithm changes over time; time-based splits capture this
- **Distribution shift**: Content trends and user behavior evolve; models must handle this

#### Split Ratios (70/15/15)
- **70% training**: Sufficient data for complex model training
- **15% validation**: Adequate for hyperparameter tuning without overfitting
- **15% testing**: Unbiased final evaluation

### 7. Output Structure and Organization

```python
# Save training, validation, and test splits
train_df.to_csv(self.training_dir / 'train_data.csv', index=False)
val_df.to_csv(self.validation_dir / 'val_data.csv', index=False)
test_df.to_csv(self.validation_dir / 'test_data.csv', index=False)

# Save combined training data (train + val) for final model training
combined_train = pd.concat([train_df, val_df], ignore_index=True)
combined_train.to_csv(self.training_dir / 'training_data.csv', index=False)
```

**File organization reasoning**:
- **Separate files**: Enable different use cases (hyperparameter tuning vs final training)
- **Combined training file**: For final model training using both train and validation data
- **Structured directories**: Clear separation between different data purposes

---

## Part 2: Model Training Pipeline (`train_enhanced_models.py`)

### Architecture and Design Philosophy

The training pipeline implements an "At-Upload" prediction strategy, using only metadata available when a video is first published. This approach is crucial for practical applications where predictions are needed before performance data is available.

### 1. Model Selection Rationale

#### XGBoost as Primary Algorithm
```python
model = xgb.XGBRegressor(
    n_estimators=self.config.get('n_estimators', 100),
    max_depth=self.config.get('max_depth', 6),
    learning_rate=self.config.get('learning_rate', 0.1),
    subsample=self.config.get('subsample', 0.8),
    colsample_bytree=self.config.get('colsample_bytree', 0.8),
    random_state=self.config.get('random_state', 42),
    n_jobs=-1
)
```

**Why XGBoost over other algorithms?**

1. **Gradient boosting strength**: Excellent for complex non-linear relationships in YouTube data
2. **Robust to outliers**: YouTube data has extreme outliers (viral videos); XGBoost handles these better than linear models
3. **Feature importance**: Built-in feature importance helps understand what drives video success
4. **Missing value handling**: Native support for missing values without imputation
5. **Regularization**: Built-in L1 and L2 regularization prevents overfitting
6. **Speed**: Optimized implementation handles large datasets efficiently

#### Alternative Models Available
- **RandomForestRegressor**: Ensemble method, good baseline, less prone to overfitting
- **LinearRegression**: Simple, interpretable, good for understanding feature relationships

**Hyperparameter choices**:
- **n_estimators=100**: Balance between performance and training time
- **max_depth=6**: Prevents overfitting while allowing complex interactions
- **learning_rate=0.1**: Conservative learning rate for stable training
- **subsample=0.8**: Row sampling reduces overfitting
- **colsample_bytree=0.8**: Feature sampling improves generalization

### 2. Feature Selection Strategy

#### Metadata-Only Approach
```python
METADATA_FEATURES = [
    col for col in self.feature_info.get('content_features', [])
    if col in base_features_train.columns
] + [
    col for col in self.feature_info.get('channel_features', [])
    if col in base_features_train.columns
]

leaky_patterns = ['view', 'like', 'comment', 'growth', 'velocity', 'peak', 'consistency', 'ratio']
METADATA_FEATURES = [
    f for f in METADATA_FEATURES 
    if not any(leak in f for leak in leaky_patterns)
]
```

**Why exclude leaky features?**
- **Temporal logic**: Growth velocity, peak day, engagement ratios depend on future data
- **Practical application**: At upload time, only metadata is available
- **Fair evaluation**: Including future data would artificially inflate model performance

#### Feature Categories Included
1. **Content features**: Title analysis, description length, duration, category
2. **Channel features**: Channel authority, average performance, consistency
3. **Temporal features**: Publish time, day of week, seasonality
4. **Language features**: Title language detection for regional analysis

### 3. Preprocessing Pipeline

#### ColumnTransformer Strategy
```python
def create_preprocessor(self, features_df: pd.DataFrame, feature_info: Dict[str, Any]) -> ColumnTransformer:
    numerical_features = [col for col in numerical_features if col in features_df.columns]
    categorical_features = [col for col in categorical_features if col in features_df.columns]
    
    preprocessor_steps = []
    if numerical_features:
        preprocessor_steps.append(('num', StandardScaler(), numerical_features))
    if categorical_features:
        preprocessor_steps.append(
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        )
```

**Preprocessing decisions**:
- **StandardScaler for numerical**: YouTube metrics have vastly different scales (views in millions, ratios as decimals)
- **OneHotEncoder for categorical**: Handles categorical variables without imposing ordinal relationships
- **handle_unknown='ignore'**: Gracefully handles new categories in production
- **sparse_output=False**: Ensures dense arrays for XGBoost compatibility

### 4. Target Engineering and Transformation

#### Logarithmic Transformation
```python
logger.info(f"Applying log transform to target variable: {target_name}")
y_train_log = np.log1p(y_train)
y_val_log = np.log1p(y_val)

pipeline.fit(X_train, y_train_log)

y_train_pred_log = pipeline.predict(X_train)
y_val_pred_log = pipeline.predict(X_val)

y_train_pred = np.expm1(y_train_pred_log)
y_val_pred = np.expm1(y_val_pred_log)
```

**Mathematical reasoning for log transformation**:
1. **Distribution normalization**: View counts are highly right-skewed; log transform creates more normal distribution
2. **Variance stabilization**: Reduces impact of extreme outliers on model training
3. **Multiplicative relationships**: YouTube growth is often multiplicative (exponential), log transform makes it additive
4. **Error metric**: Relative errors become more important than absolute errors

**Using `log1p` and `expm1`**:
- `log1p(x) = log(1 + x)`: Handles zero values without undefined behavior
- `expm1(x) = exp(x) - 1`: Precise inverse transformation, prevents numerical errors

### 5. Separate Models by Content Type

#### Shorts vs Long-form Strategy
```python
def train_separate_models_by_target(self, features_df_train, target_series_train, features_df_val, target_series_val, target_name):
    # Split by content type
    shorts_mask_train = features_df_train['is_short'] == True
    longform_mask_train = features_df_train['is_short'] == False
    
    if not shorts_features_train.empty and not shorts_features_val.empty:
        shorts_pipeline, shorts_metrics = self.train_model_for_target(...)
    
    if not longform_features_train.empty and not longform_features_val.empty:
        longform_pipeline, longform_metrics = self.train_model_for_target(...)
```

**Why separate models?**
1. **Different algorithms**: YouTube Shorts and long-form content have different recommendation algorithms
2. **Feature importance**: Title optimization matters more for Shorts, while description matters more for long-form
3. **Engagement patterns**: Shorts rely on immediate engagement, long-form on sustained watch time
4. **Duration constraints**: Different optimal ranges require different modeling approaches

#### Safety Checks for Data Availability
```python
if not shorts_features_train.empty and not shorts_features_val.empty:
    # Train shorts model
else:
    logger.warning(f"Skipping Shorts model due to empty dataset")
```

**Robustness reasoning**: Prevents crashes when insufficient data exists for a content type, ensures graceful degradation.

### 6. Evaluation Metrics Strategy

#### SMAPE (Symmetric Mean Absolute Percentage Error)
```python
def calculate_smape(y_true, y_pred):
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    return np.mean(np.abs(y_true - y_pred) / np.maximum(denom, 1)) * 100
```

**Why SMAPE instead of MAPE?**
- **Symmetric**: Equal penalty for over and under-prediction
- **Bounded**: 0-200% range makes interpretation easier
- **Zero-safe**: Doesn't explode with zero actual values
- **Industry standard**: Common in forecasting competitions and business applications

#### Multiple R² Calculations
```python
'val_r2': r2_score(y_val, y_val_pred),           # R² on original scale
'val_r2_log': r2_score(y_val_log, y_val_pred_log)  # R² on log scale
```

**Dual R² reasoning**:
- **Original scale R²**: Directly interpretable business metric
- **Log scale R²**: Better reflects model performance given the log transformation
- **Different insights**: Original scale emphasizes large videos, log scale treats all videos more equally

#### Comprehensive Metrics Suite
- **MAE (Mean Absolute Error)**: Interpretable in original units (views)
- **RMSE (Root Mean Square Error)**: Penalizes large errors more heavily
- **SMAPE**: Percentage-based, scale-independent
- **R²**: Variance explanation, model quality indicator

### 7. Model Persistence and Organization

#### Structured Model Saving
```python
def save_models(self, results: Dict[str, Any], prefix: str) -> None:
    model_types = ['shorts_models', 'longform_models', 'unified_models']
    for model_type in model_types:
        for target_name, model in results[model_type].items():
            model_path = self.models_dir / f'{prefix}_{model_type.replace("_models", "")}_{target_name}_model.joblib'
            joblib.dump(model, model_path)
```

**File naming convention**: `{prefix}_{content_type}_{target}_{model.joblib}`
- Example: `at_upload_shorts_views_at_24h_model.joblib`
- **Prefix**: Indicates prediction scenario (at_upload, after_24h, etc.)
- **Content type**: shorts/longform/unified
- **Target**: specific prediction target
- **Extension**: joblib for efficient serialization

### 8. Error Handling and Robustness

#### Graceful Degradation
```python
min_samples = self.config.get('min_samples_for_training', 50)
if target_name not in all_targets_train or len(all_targets_train[target_name].dropna()) < min_samples:
    logger.warning(f"Skipping '{target_name}': Not enough valid samples")
    continue
```

**Safety mechanisms**:
- **Minimum sample requirements**: Prevents overfitting on tiny datasets
- **Missing target handling**: Gracefully skips unavailable targets
- **Empty dataset checks**: Prevents crashes from data filtering
- **Exception logging**: Comprehensive error tracking for debugging

---

## Integrated System Logic and Workflow

### 1. End-to-End Data Flow

1. **Raw Data Ingestion** → YouTube API v3 CSV with 103 columns
2. **Data Cleaning** → Standardization, outlier removal, type conversion
3. **Feature Engineering** → 50+ engineered features from raw metadata
4. **Time-based Splitting** → Chronological train/val/test splits
5. **Model Training** → Separate models for Shorts/Long-form × 3 targets
6. **Model Persistence** → Structured file organization for production use

### 2. Business Logic Alignment

#### Prediction Scenarios
- **At-upload predictions**: Use only metadata available when video is published
- **Content strategy**: Different models for Shorts vs long-form content
- **Multi-horizon forecasting**: 24h, 7d, 30d predictions for different business needs

#### Regional Considerations
- **Language detection**: Sinhala, Tamil, English content optimization
- **Temporal patterns**: Local peak viewing times and cultural calendar
- **Channel ecosystem**: Authority scoring adapted to Sri Lankan YouTube landscape

### 3. Technical Architecture Decisions

#### Scalability Considerations
- **Modular design**: Easy to add new features or models
- **Configuration-driven**: Hyperparameters externally configurable
- **Efficient processing**: Vectorized operations, minimal loops
- **Memory optimization**: Chunked processing for large datasets

#### Production Readiness
- **Error handling**: Comprehensive exception management
- **Logging**: Detailed operation tracking
- **Reproducibility**: Fixed random seeds, versioned outputs
- **Testing**: Validation splits for unbiased evaluation

### 4. Statistical and Mathematical Foundations

#### Feature Engineering Mathematics
- **Growth rates**: Relative change calculations with zero-division protection
- **Consistency metrics**: Standard deviation of time-series derivatives
- **Engagement ratios**: Normalized metrics for cross-video comparison
- **Authority scoring**: Weighted composite metrics with logarithmic scaling

#### Model Training Mathematics
- **Log transformation**: Address right-skewed distributions and multiplicative relationships
- **Gradient boosting**: Iterative residual fitting for complex non-linear patterns
- **Cross-validation**: Time-aware splitting for temporal data integrity
- **Regularization**: L1/L2 penalties to prevent overfitting

### 5. Domain-Specific Insights

#### YouTube Algorithm Understanding
- **Early momentum**: 24-hour performance heavily influences long-term success
- **Content type differences**: Shorts vs long-form have distinct success patterns
- **Engagement velocity**: Rate of early engagement predicts viral potential
- **Channel authority**: Established channels have different growth dynamics

#### Sri Lankan YouTube Ecosystem
- **Multi-language content**: Language choice significantly affects reach
- **Cultural timing**: Local viewing patterns differ from global averages
- **Channel diversity**: Wide range of channel sizes and content types
- **Regional preferences**: Local content preferences and trends

This comprehensive system represents a sophisticated approach to YouTube video performance prediction, combining rigorous statistical methods with deep domain knowledge and practical engineering considerations. The modular design allows for continuous improvement and adaptation to changing platform dynamics while maintaining robust, production-ready performance.