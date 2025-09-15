# ViewTrendsSL EDA Summary Report
Generated on: 2025-09-16 03:41:24

## Dataset Overview
- Total videos: 20,308
- Date range: 2025-08-06 01:16:25 to 2025-09-14 01:20:04
- Shorts: 6,264 (30.8%)
- Long-form: 14,044 (69.2%)

## Performance Metrics
- Average views: 18,069
- Median views: 1,241
- Average engagement rate: 0.0270
- Top 1% view threshold: 296,056

## Shorts vs Long-form Comparison
- Shorts average views: 11,315
- Long-form average views: 21,081
- Performance ratio (Long-form/Shorts): 1.86

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