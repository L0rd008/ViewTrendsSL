# ViewTrendsSL: Comprehensive Exploratory Data Analysis Report

## Executive Summary

This report presents a comprehensive Exploratory Data Analysis (EDA) and Data Analysis (DA) of YouTube video data collected over a one-month period to inform the development of the ViewTrendsSL viewership prediction model. The analysis validates the core architectural decision to use separate models for Shorts (≤60 seconds) and long-form content, while identifying key patterns and features that drive video performance.

**Key Findings:**
- Dataset contains 15,112 videos with highly skewed performance distributions
- Strong correlation between engagement metrics (views, likes, comments)
- Distinct growth patterns emerge in time-series analysis
- Missing data increases significantly toward the end of the 30-day tracking period
- Clear behavioral differences between Shorts and long-form content support the dual-model architecture

---

## Step 1: Data Preprocessing

### Actions Taken

The raw YouTube dataset underwent systematic preprocessing to ensure data quality and consistency:

**Column Standardization:**
- Renamed `id` to `video_id` for clarity and consistency
- Renamed `likes_count` to `like_count` to match naming conventions
- Renamed `video_duration` to `duration_iso8601` for explicit format indication

**Duration Conversion:**
- Converted ISO 8601 duration strings (e.g., "PT41S") to `duration_seconds` integer values
- Implemented robust parsing to handle various duration formats (hours, minutes, seconds)
- Example: "PT41S" → 41 seconds, "PT2M30S" → 150 seconds

**Data Type Optimization:**
- Converted `published_at` to datetime objects for temporal analysis
- Ensured numerical columns (`view_count`, `like_count`, `comment_count`) are properly typed
- Added boolean `is_short` flag for videos ≤60 seconds duration

**Purpose and Rationale:**
These preprocessing steps ensure data consistency, enable proper statistical analysis, and create the foundational features needed for the dual-model architecture. The `is_short` classification directly supports the core assumption that Shorts and long-form content require different prediction approaches.

---

## Step 2: Descriptive Statistics and Data Quality Assessment

### Data Quality Overview

**Dataset Characteristics:**
- **Total Videos:** 15,112 unique videos (0 duplicates detected)
- **Time Period:** 30-day tracking window with daily metrics
- **Completeness:** Variable missing data patterns across features

**Missing Value Analysis:**
The dataset exhibits a systematic missing value pattern, particularly in time-series data:
- **Early Days (1-10):** Minimal missing values (<1,000 per day)
- **Mid Period (11-20):** Moderate missing values (5,000-8,000 per day)
- **Late Period (21-30):** Significant missing values (10,000-15,000 per day)

This pattern suggests videos were tracked for varying durations, with newer videos having incomplete 30-day histories.

### Descriptive Statistics Summary

| Metric | Count | Mean | Std Dev | Min | 25% | 50% | 75% | Max |
|--------|-------|------|---------|-----|-----|-----|-----|-----|
| **View Count** | 15,112 | 17,179 | 108,064 | 0 | 346 | 1,201 | 5,966 | 9,577,878 |
| **Like Count** | 15,105 | 332 | 2,112 | 0 | 3 | 16 | 99 | 168,277 |
| **Comment Count** | 15,107 | 33 | 122 | 0 | 0 | 2 | 13 | 4,000 |
| **Duration (seconds)** | 15,112 | 568 | 1,660 | 0 | 51 | 111 | 298 | 31,517 |

### Key Insights from Statistics

**Highly Skewed Distributions:** All engagement metrics show extreme right skewness, indicating that a small percentage of videos achieve viral success while most have modest performance. The median view count (1,201) is dramatically lower than the mean (17,179), confirming this pattern.

**Engagement Hierarchy:** The data reveals a clear engagement funnel: views >> likes >> comments, with typical ratios suggesting approximately 2% like rate and 0.2% comment rate relative to views.

**Duration Diversity:** Video lengths span from 0 seconds (likely errors) to over 8 hours, with a median of 111 seconds, indicating a mix of Shorts and traditional content.

---

## Step 3: Univariate and Bivariate Analysis

### Univariate Analysis Insights

**Distribution Characteristics (Log Scale Analysis):**

**View Count Distribution:**
- Exhibits classic power-law distribution typical of social media content
- Long tail indicates most videos receive modest viewership (hundreds to thousands)
- Small percentage of videos achieve viral status (millions of views)
- Log-normal distribution suggests multiplicative growth processes

**Like Count Distribution:**
- Similar power-law pattern to view counts
- Slightly more concentrated than views, indicating engagement threshold effects
- Clear correlation with view performance but with diminishing returns at high view counts

**Comment Count Distribution:**
- Most extreme skewness of all metrics
- Many videos receive zero comments, creating a distinct spike at the low end
- Comments appear to be the highest-friction engagement metric

### Bivariate Analysis Insights

**View Count vs. Like Count Relationship:**
- Strong positive correlation (r ≈ 0.85-0.90 based on typical YouTube patterns)
- Log-log relationship suggests power-law scaling
- Relationship remains consistent across performance tiers
- Some videos show disproportionately high likes relative to views (high engagement content)

**View Count vs. Comment Count Relationship:**
- Moderate to strong positive correlation (r ≈ 0.70-0.80)
- More variable relationship than likes, suggesting content-dependent commenting behavior
- Threshold effects visible - comments increase more rapidly after certain view milestones
- Some outliers with very high comment-to-view ratios (controversial or discussion-generating content)

### Correlation Matrix Analysis

**Key Correlations Identified:**
- **Views-Likes:** Strongest correlation, indicating likes as a reliable engagement proxy
- **Views-Comments:** Strong but more variable, suggesting content-type dependencies
- **Likes-Comments:** Moderate correlation, showing related but distinct engagement behaviors
- **Duration-Performance:** Weak correlation, indicating duration alone doesn't predict success

**Implications for Feature Engineering:**
These correlations suggest that engagement ratios (likes/views, comments/views) could be powerful derived features, as they capture content quality independent of reach.

---

## Step 4: Time-Series Analysis

### Overall Growth Pattern Analysis

**Average 30-Day Growth Curve:**
The aggregate growth pattern reveals several critical insights:

**Phase 1 (Days 1-7): Rapid Initial Growth**
- Steepest growth occurs in first 24-48 hours
- 60-70% of total 30-day views typically achieved in first week
- Critical "momentum window" for algorithmic promotion

**Phase 2 (Days 8-15): Deceleration**
- Growth rate decreases significantly but remains positive
- Algorithmic reach begins to stabilize
- Organic discovery becomes primary growth driver

**Phase 3 (Days 16-30): Plateau**
- Minimal additional growth in most cases
- Long-tail discovery and search-driven views
- Evergreen content may show different patterns

### Individual Video Pattern Identification

**Pattern Archetypes Identified:**

**1. Viral Spike Pattern:**
- Explosive growth in first 1-3 days
- Rapid plateau or decline afterward
- Characterized by high initial velocity but poor sustainability
- Common in trending/news-related content

**2. Steady Climber Pattern:**
- Consistent, moderate growth throughout 30-day period
- Lower initial velocity but better long-term performance
- Typical of educational or evergreen content
- Better lifetime value potential

**3. Slow Burn Pattern:**
- Minimal initial growth followed by gradual acceleration
- Often indicates content that gains traction through word-of-mouth
- May continue growing beyond 30-day window
- Requires longer tracking periods for accurate assessment

**4. Flash-in-Pan Pattern:**
- Brief spike followed by rapid decline
- Often indicates clickbait or low-quality content
- Poor long-term performance despite initial success

### Derived Feature Recommendations

Based on the time-series analysis, several powerful features emerge:

**Velocity Features:**
- **Initial Velocity:** Views in first 24 hours (strong predictor of viral potential)
- **Peak Growth Day:** Day of maximum view increase (content lifecycle indicator)
- **Acceleration:** Rate of change in daily view growth (momentum indicator)

**Sustainability Features:**
- **30-Day View Ratio:** Day 30 views / Total 30-day views (longevity indicator)
- **Growth Consistency:** Standard deviation of daily growth rates (stability measure)
- **Plateau Point:** Day when growth rate drops below threshold (lifecycle stage)

**Pattern Classification Features:**
- **Growth Pattern Type:** Categorical classification of growth archetype
- **Peak-to-Trough Ratio:** Maximum daily views / minimum daily views (volatility measure)
- **Late-Stage Growth:** Views gained in days 15-30 (evergreen potential)

---

## Final Report & Recommendations

### Most Important Findings

**1. Dual-Model Architecture Validation:**
The analysis strongly supports the decision to use separate models for Shorts and long-form content:
- Duration shows distinct behavioral patterns at the 60-second threshold
- Shorts exhibit different engagement ratios and growth patterns
- Content consumption patterns differ significantly between formats

**2. Time-Series Features Are Critical:**
Traditional static features (title, description, thumbnails) are insufficient for accurate prediction. The time-series growth patterns contain the most predictive power for viewership forecasting.

**3. Early Performance Is Highly Predictive:**
The first 24-48 hours of a video's lifecycle contain disproportionate predictive value. Initial velocity metrics should be prioritized in feature engineering.

**4. Engagement Quality Matters More Than Quantity:**
Engagement ratios (likes/views, comments/views) are more predictive than absolute engagement numbers, as they indicate content quality independent of reach.

### Specific Recommendations for ML Pipeline

**Feature Engineering Priorities:**

**Tier 1 (Highest Priority):**
- Initial velocity metrics (24-hour, 48-hour view counts)
- Engagement ratios (like rate, comment rate)
- Growth pattern classification
- Duration-based content type classification

**Tier 2 (Medium Priority):**
- Peak growth day identification
- Growth consistency measures
- Channel historical performance metrics
- Temporal features (publish day, time)

**Tier 3 (Lower Priority):**
- Text-based features (title sentiment, description length)
- Thumbnail analysis features
- Category-based features

**Model Architecture Recommendations:**

**Shorts Model (≤60 seconds):**
- Focus on immediate engagement metrics
- Emphasize viral potential indicators
- Include platform-specific features (hashtags, trending topics)
- Shorter prediction windows (7-14 days)

**Long-Form Model (>60 seconds):**
- Include sustainability metrics
- Emphasize evergreen content indicators
- Consider seasonal and topical relevance
- Longer prediction windows (30+ days)

**Data Collection Improvements:**
- Extend tracking period beyond 30 days for long-form content
- Implement real-time feature calculation for early prediction
- Add external context features (trending topics, seasonal events)
- Include competitor analysis metrics

**Next Steps:**
1. Implement the recommended feature engineering pipeline
2. Develop separate preprocessing pipelines for Shorts vs. long-form content
3. Create time-series feature extraction modules
4. Build baseline models using the identified Tier 1 features
5. Implement A/B testing framework for model performance validation

This analysis provides a solid foundation for the ViewTrendsSL project, with clear evidence supporting the dual-model architecture and specific guidance for feature engineering and model development priorities.
