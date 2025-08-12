# Notebooks Directory

This directory contains Jupyter notebooks for exploratory data analysis, model development, and research activities.

## 📁 Directory Structure

### `/eda/` - Exploratory Data Analysis
**Purpose**: Data exploration, visualization, and initial insights
**Audience**: Data scientists, researchers, stakeholders
**Output**: Insights, visualizations, data quality reports

**Notebooks**:
- `01_data_overview.ipynb` - Initial data exploration and statistics
- `02_channel_analysis.ipynb` - Sri Lankan channel characteristics analysis
- `03_video_performance_patterns.ipynb` - Video performance trend analysis
- `04_temporal_analysis.ipynb` - Time-based viewing pattern analysis
- `05_content_category_analysis.ipynb` - Category-wise performance analysis
- `06_shorts_vs_longform.ipynb` - Comparison between Shorts and long-form videos
- `07_engagement_analysis.ipynb` - Like, comment, and engagement patterns
- `08_language_impact_analysis.ipynb` - Impact of language on viewership
- `09_data_quality_report.ipynb` - Data quality assessment and issues

**Key Insights Generated**:
- Peak viewing hours for Sri Lankan audience
- Most successful content categories
- Optimal video length ranges
- Seasonal trends and patterns
- Channel growth trajectories

### `/modeling/` - Model Development and Training
**Purpose**: Machine learning model development, training, and evaluation
**Audience**: ML engineers, data scientists
**Output**: Trained models, performance metrics, model comparisons

**Notebooks**:
- `01_feature_engineering.ipynb` - Feature creation and selection process
- `02_baseline_models.ipynb` - Simple baseline model development
- `03_shorts_model_development.ipynb` - YouTube Shorts prediction model
- `04_longform_model_development.ipynb` - Long-form video prediction model
- `05_hyperparameter_tuning.ipynb` - Model optimization and tuning
- `06_ensemble_methods.ipynb` - Ensemble model development
- `07_model_evaluation.ipynb` - Comprehensive model evaluation
- `08_model_interpretation.ipynb` - Feature importance and model explainability
- `09_prediction_validation.ipynb` - Real-world prediction validation

**Model Development Process**:
1. **Data Preparation**: Clean and prepare training data
2. **Feature Engineering**: Create predictive features
3. **Model Selection**: Compare different algorithms
4. **Hyperparameter Tuning**: Optimize model parameters
5. **Validation**: Evaluate model performance
6. **Interpretation**: Understand model decisions

### `/analysis/` - Advanced Analysis and Research
**Purpose**: Deep-dive analysis, research questions, and business insights
**Audience**: Business stakeholders, researchers, product managers
**Output**: Business insights, research findings, recommendations

**Notebooks**:
- `01_creator_success_factors.ipynb` - What makes Sri Lankan creators successful
- `02_viral_video_analysis.ipynb` - Characteristics of viral content
- `03_competition_analysis.ipynb` - Competitive landscape analysis
- `04_market_trends.ipynb` - YouTube market trends in Sri Lanka
- `05_recommendation_engine.ipynb` - Content recommendation analysis
- `06_monetization_insights.ipynb` - Revenue and monetization patterns
- `07_audience_behavior.ipynb` - Sri Lankan audience behavior analysis
- `08_content_strategy.ipynb` - Optimal content strategy recommendations
- `09_platform_comparison.ipynb` - YouTube vs other platforms (future)

**Research Questions Addressed**:
- What content performs best in Sri Lanka?
- How do viewing patterns differ by demographics?
- What are the key success factors for new creators?
- How has the market evolved over time?
- What opportunities exist for content creators?

## 📊 Notebook Standards

### Code Quality
- **PEP-8 Compliance**: Follow Python style guidelines
- **Clear Documentation**: Document analysis steps and findings
- **Reproducible Results**: Set random seeds, document versions
- **Modular Code**: Extract reusable functions to utility modules
- **Version Control**: Track notebook changes meaningfully

### Data Visualization
- **Consistent Styling**: Use consistent color schemes and fonts
- **Clear Labels**: Properly label axes, titles, and legends
- **Interactive Plots**: Use Plotly for interactive visualizations
- **Export Quality**: Ensure plots are publication-ready
- **Accessibility**: Use colorblind-friendly palettes

### Documentation
- **Markdown Cells**: Explain analysis steps and findings
- **Executive Summary**: Include key findings at the top
- **Methodology**: Document data sources and methods
- **Limitations**: Acknowledge analysis limitations
- **Next Steps**: Suggest follow-up analyses

## 🛠️ Setup and Environment

### Required Libraries
```python
# Data manipulation and analysis
import pandas as pd
import numpy as np
import scipy.stats as stats

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Machine learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

# Utilities
import warnings
warnings.filterwarnings('ignore')

# Custom modules
import sys
sys.path.append('../src')
from business.services.data_service import DataService
from business.utils.visualization import create_performance_plot
```

### Notebook Configuration
```python
# Standard notebook setup
%matplotlib inline
%config InlineBackend.figure_format = 'retina'

# Pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', '{:.2f}'.format)

# Plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

## 📈 Common Analysis Patterns

### Data Loading Template
```python
def load_analysis_data():
    """Load and prepare data for analysis"""
    # Load raw data
    videos_df = pd.read_csv('../data/processed/features/features_longform.csv')
    channels_df = pd.read_csv('../data/raw/channels/channel_metadata.csv')
    
    # Basic cleaning
    videos_df['published_at'] = pd.to_datetime(videos_df['published_at'])
    videos_df = videos_df.dropna(subset=['view_count', 'like_count'])
    
    # Merge with channel data
    analysis_df = videos_df.merge(channels_df, on='channel_id', how='left')
    
    return analysis_df

# Usage
df = load_analysis_data()
print(f"Loaded {len(df)} videos from {df['channel_id'].nunique()} channels")
```

### Visualization Template
```python
def create_performance_analysis(df, metric='view_count'):
    """Create comprehensive performance analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Distribution
    axes[0,0].hist(df[metric], bins=50, alpha=0.7)
    axes[0,0].set_title(f'{metric.title()} Distribution')
    axes[0,0].set_xlabel(metric.replace('_', ' ').title())
    
    # Time series
    daily_avg = df.groupby(df['published_at'].dt.date)[metric].mean()
    axes[0,1].plot(daily_avg.index, daily_avg.values)
    axes[0,1].set_title(f'Daily Average {metric.title()}')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Category comparison
    category_stats = df.groupby('category_name')[metric].agg(['mean', 'median'])
    category_stats.plot(kind='bar', ax=axes[1,0])
    axes[1,0].set_title(f'{metric.title()} by Category')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Correlation heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=axes[1,1])
    axes[1,1].set_title('Feature Correlations')
    
    plt.tight_layout()
    return fig

# Usage
fig = create_performance_analysis(df, 'view_count')
plt.show()
```

### Statistical Analysis Template
```python
def perform_statistical_analysis(df, target='view_count'):
    """Perform comprehensive statistical analysis"""
    results = {}
    
    # Descriptive statistics
    results['descriptive'] = df[target].describe()
    
    # Normality test
    stat, p_value = stats.normaltest(df[target])
    results['normality'] = {'statistic': stat, 'p_value': p_value}
    
    # Category comparisons
    categories = df['category_name'].unique()
    if len(categories) > 1:
        category_groups = [df[df['category_name'] == cat][target] for cat in categories]
        f_stat, p_value = stats.f_oneway(*category_groups)
        results['anova'] = {'f_statistic': f_stat, 'p_value': p_value}
    
    # Correlation analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()[target].sort_values(ascending=False)
    results['correlations'] = correlations
    
    return results

# Usage
stats_results = perform_statistical_analysis(df)
print("Statistical Analysis Results:")
for key, value in stats_results.items():
    print(f"\n{key.upper()}:")
    print(value)
```

## 🔍 Analysis Guidelines

### Exploratory Data Analysis
1. **Start with Overview**: Understand data structure and quality
2. **Visualize Distributions**: Check for outliers and patterns
3. **Explore Relationships**: Identify correlations and dependencies
4. **Segment Analysis**: Analyze different groups separately
5. **Time Series Analysis**: Look for temporal patterns

### Model Development
1. **Feature Engineering**: Create meaningful predictive features
2. **Baseline Models**: Start with simple, interpretable models
3. **Model Comparison**: Compare multiple algorithms
4. **Hyperparameter Tuning**: Optimize model performance
5. **Validation**: Use proper cross-validation techniques

### Business Analysis
1. **Define Questions**: Start with clear business questions
2. **Hypothesis Testing**: Test specific hypotheses statistically
3. **Actionable Insights**: Focus on actionable recommendations
4. **Stakeholder Communication**: Present findings clearly
5. **Follow-up Analysis**: Plan next steps based on findings

## 📋 Notebook Checklist

### Before Starting
- [ ] Clear research question or objective defined
- [ ] Required data sources identified and accessible
- [ ] Environment set up with necessary libraries
- [ ] Previous related analyses reviewed

### During Analysis
- [ ] Code is well-documented with markdown cells
- [ ] Visualizations are clear and properly labeled
- [ ] Statistical tests are appropriate for the data
- [ ] Assumptions are validated and documented
- [ ] Results are interpreted in business context

### Before Sharing
- [ ] Notebook runs from top to bottom without errors
- [ ] All outputs are visible and properly formatted
- [ ] Executive summary includes key findings
- [ ] Limitations and caveats are documented
- [ ] Next steps and recommendations are provided

## 🚀 Best Practices

### Performance Optimization
- **Efficient Data Loading**: Use appropriate data types and chunking
- **Memory Management**: Delete unnecessary variables
- **Vectorized Operations**: Use pandas/numpy vectorized functions
- **Caching**: Cache expensive computations
- **Profiling**: Profile code to identify bottlenecks

### Reproducibility
- **Set Random Seeds**: Ensure reproducible results
- **Document Versions**: Record library versions used
- **Data Versioning**: Track data versions and sources
- **Environment Files**: Provide requirements.txt or environment.yml
- **Clear Instructions**: Document how to reproduce analysis

### Collaboration
- **Version Control**: Use meaningful commit messages
- **Code Reviews**: Have analyses reviewed by peers
- **Documentation**: Write for future self and others
- **Modular Code**: Extract reusable functions
- **Consistent Style**: Follow team coding standards

## 🎯 Output and Deliverables

### Analysis Reports
- **Executive Summary**: Key findings and recommendations
- **Methodology**: Data sources and analysis methods
- **Results**: Detailed findings with visualizations
- **Limitations**: Analysis constraints and caveats
- **Next Steps**: Recommended follow-up actions

### Model Artifacts
- **Trained Models**: Serialized model files
- **Performance Metrics**: Model evaluation results
- **Feature Importance**: Key predictive features
- **Validation Results**: Out-of-sample performance
- **Model Documentation**: Usage instructions and limitations

### Visualizations
- **Static Plots**: High-quality PNG/PDF exports
- **Interactive Dashboards**: HTML exports with interactivity
- **Presentation Slides**: Key visualizations for stakeholders
- **Data Stories**: Narrative-driven visual explanations
- **Infographics**: Summary visualizations for broad audiences

## 🔄 Maintenance and Updates

### Regular Reviews
- **Monthly Data Updates**: Refresh analysis with new data
- **Quarterly Model Updates**: Retrain models with recent data
- **Annual Deep Dives**: Comprehensive analysis reviews
- **Ad-hoc Analysis**: Respond to specific business questions
- **Performance Monitoring**: Track model performance over time

### Knowledge Management
- **Analysis Catalog**: Maintain index of completed analyses
- **Best Practices**: Document lessons learned
- **Template Library**: Create reusable analysis templates
- **Training Materials**: Develop onboarding resources
- **External Sharing**: Publish relevant findings externally
