# ViewTrendsSL EDA Summary Report
Generated on: 2025-09-07 04:59:32

## Dataset Overview
- Total videos: 15,112
- Date range: 2025-08-06 01:16:25 to 2025-09-04 01:17:34
- Shorts: 4,563 (30.2%)
- Long-form: 10,549 (69.8%)

## Performance Metrics
- Average views: 17,179
- Median views: 1,201
- Average engagement rate: 0.0276
- Top 1% view threshold: 286,962

## Shorts vs Long-form Comparison
- Shorts average views: 10,979
- Long-form average views: 19,860
- Performance ratio (Long-form/Shorts): 1.81

## Key Insights
- Dual-model architecture is validated by distinct performance patterns
- Time-series features show high predictive potential
- Publication timing has measurable impact on performance
- Engagement quality metrics outperform absolute counts

## Recommendations for ML Pipeline
1. Implement separate preprocessing pipelines for Shorts and Long-form
2. Prioritize time-series derived features (initial velocity, growth patterns)
3. Include publication timing features in model training
4. Use engagement ratios rather than absolute engagement counts
5. Consider growth pattern classification as a categorical feature