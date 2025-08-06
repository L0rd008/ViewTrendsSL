# ViewTrendsSL: YouTube Viewership Forecasting System
## Project Feasibility Study

**Document Version**: 1.0  
**Date**: August 6, 2025  
**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  

**Prepared by:**
- Senevirathne S.M.P.U. (220599M) - Data Lead
- Sanjula N.G.K. (220578A) - Backend & Model Lead  
- Shaamma M.S. (220602U) - Frontend & Documentation Lead

---

## Executive Summary

This feasibility study evaluates the viability of developing ViewTrendsSL, a machine learning-powered web application for predicting YouTube video viewership specifically for Sri Lankan audiences. The study examines technical, financial, operational, and legal feasibility aspects to determine project viability within the constraints of a 10-week university project.

**Key Findings:**
- **Technical Feasibility**: High - Leveraging proven XGBoost algorithms and established web technologies
- **Financial Feasibility**: Excellent - Zero-cost implementation using free-tier services
- **Operational Feasibility**: Good - Manageable scope with clear team role allocation
- **Legal Feasibility**: Acceptable - Compliant with YouTube API terms and academic ethics
- **Overall Recommendation**: **PROCEED** with recommended risk mitigation strategies

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Market Analysis](#2-market-analysis)
3. [Technical Feasibility](#3-technical-feasibility)
4. [Financial Feasibility](#4-financial-feasibility)
5. [Operational Feasibility](#5-operational-feasibility)
6. [Risk Assessment](#6-risk-assessment)
7. [Legal and Compliance Analysis](#7-legal-and-compliance-analysis)
8. [Success Criteria and Evaluation](#8-success-criteria-and-evaluation)
9. [Recommendations](#9-recommendations)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Project Overview

**Project Name**: ViewTrendsSL - YouTube Viewership Forecasting for Sri Lankan Audience  
**Project Type**: Applied research with practical implementation  
**Duration**: 10 weeks (August 24 - November 1, 2025)  
**Team Size**: 3 undergraduate students  
**Primary Objective**: Develop a localized YouTube viewership prediction system for Sri Lankan content creators

### 1.2 Problem Statement

The digital content creation landscape in Sri Lanka faces a critical information gap. Content creators, digital marketers, and media companies lack access to predictive analytics tools that understand local viewing patterns, cultural contexts, and regional engagement behaviors. Existing global platforms like VidIQ, TubeBuddy, and Social Blade provide historical analytics but fail to capture the nuances of Sri Lankan audience behavior or provide accurate predictive insights for this specific market.

**Quantified Problem Impact:**
- **Market Gap**: No existing tools specifically designed for Sri Lankan YouTube analytics
- **Creator Disadvantage**: Local creators rely on intuition rather than data-driven decisions
- **Economic Impact**: Suboptimal content strategies result in reduced monetization potential
- **Research Gap**: Lack of academic research on regional YouTube viewership patterns

### 1.3 Proposed Solution

ViewTrendsSL addresses this gap through a comprehensive machine learning system that:

**Core Value Propositions:**
1. **Hyper-Local Focus**: Models trained specifically on Sri Lankan viewership data
2. **Predictive Analytics**: Forward-looking insights rather than historical reporting
3. **Cultural Context**: Understanding of local language, trends, and viewing patterns
4. **Academic Rigor**: Research-backed methodology with transparent algorithms
5. **Accessibility**: Free, web-based tool accessible to all creators

**Technical Innovation:**
- Separate XGBoost models for Shorts (≤60s) and Long-form (>60s) videos based on AMPS research
- Temporal prediction framework following SMTPD methodology
- Multi-modal feature engineering incorporating metadata, temporal, and engagement signals
- Real-time prediction delivery through optimized web interface

### 1.4 Project Objectives

#### 1.4.1 Primary Objectives
1. **Develop Predictive Models**: Create accurate ML models for 24h, 7d, and 30d view forecasting
2. **Build Data Infrastructure**: Establish automated data collection from 100+ Sri Lankan channels
3. **Create User Interface**: Develop intuitive web application for prediction requests
4. **Achieve Performance Targets**: MAPE < 30% for 7-day predictions (research-validated target)

#### 1.4.2 Secondary Objectives
1. **Academic Contribution**: Create research-grade dataset for community use
2. **Knowledge Transfer**: Comprehensive documentation and open-source release
3. **Research Publication**: Submit findings to academic conferences
4. **Industry Impact**: Demonstrate practical value for Sri Lankan creator ecosystem

### 1.5 Success Criteria

**Technical Success Metrics:**
- Model accuracy: MAPE < 30% for 7-day view predictions
- System performance: 95% of predictions delivered within 30 seconds
- Data coverage: 5,000+ videos from 100+ Sri Lankan channels
- System reliability: 95% uptime during evaluation period

**Academic Success Metrics:**
- Comprehensive documentation meeting university standards
- Successful final presentation and demonstration
- Research contribution with potential for publication
- Open-source release with community adoption potential

---

## 2. Market Analysis

### 2.1 Target Market Assessment

#### 2.1.1 Primary Market Segments

**Sri Lankan Content Creators (Primary)**
- **Market Size**: 500+ active YouTube channels with 1K+ subscribers
- **Pain Points**: Lack of predictive insights, reliance on trial-and-error approaches
- **Value Proposition**: Data-driven content strategy optimization
- **Willingness to Pay**: High interest in free tools, potential for premium features

**Digital Marketing Agencies (Secondary)**
- **Market Size**: 50+ agencies serving local businesses
- **Pain Points**: Limited regional analytics tools, client reporting challenges
- **Value Proposition**: Enhanced client services and campaign optimization
- **Business Impact**: Improved ROI for video marketing campaigns

**Media Companies and Production Houses (Tertiary)**
- **Market Size**: 20+ established media organizations
- **Pain Points**: Content performance uncertainty, resource allocation challenges
- **Value Proposition**: Strategic content planning and investment decisions
- **Economic Impact**: Reduced production risks and improved content ROI

#### 2.1.2 Market Demand Validation

**Quantitative Indicators:**
- **YouTube Growth in Sri Lanka**: 40% YoY increase in content creation (2023-2024)
- **Creator Economy**: $2M+ estimated annual revenue for top Sri Lankan channels
- **Digital Marketing Spend**: 25% increase in video marketing budgets (2024)
- **Tool Adoption**: 70% of surveyed creators use at least one analytics tool

**Qualitative Evidence:**
- Creator community discussions highlighting need for local insights
- Marketing agency requests for regional analytics capabilities
- Academic interest in regional social media research
- Government initiatives supporting digital content creation

### 2.2 Competitive Landscape Analysis

#### 2.2.1 Global Competitors

**VidIQ**
- **Strengths**: Comprehensive SEO tools, large user base, established brand
- **Weaknesses**: Global focus lacks regional specificity, expensive premium tiers
- **Market Position**: Dominant player with 2M+ users globally
- **Sri Lankan Relevance**: Limited - generic insights don't capture local nuances

**TubeBuddy**
- **Strengths**: Chrome extension integration, A/B testing capabilities
- **Weaknesses**: Platform dependency, limited predictive features
- **Market Position**: Strong among individual creators
- **Sri Lankan Relevance**: Moderate - some features applicable but not localized

**Social Blade**
- **Strengths**: Historical data tracking, free basic tier
- **Weaknesses**: Reactive analytics, limited prediction capabilities
- **Market Position**: Popular for channel comparison and tracking
- **Sri Lankan Relevance**: Low - provides rankings but no predictive insights

#### 2.2.2 Regional Competitors

**Viewstats**
- **Strengths**: Some regional focus, basic analytics
- **Weaknesses**: Limited accuracy, outdated interface, minimal features
- **Market Position**: Niche player with limited adoption
- **Competitive Threat**: Low - significant opportunity for improvement

**Local Analytics Services**
- **Market Presence**: Minimal - no established regional players
- **Service Quality**: Basic reporting without predictive capabilities
- **Technology Gap**: Significant opportunity for ML-powered solution

#### 2.2.3 Competitive Advantages

**ViewTrendsSL Differentiators:**

1. **Regional Specialization**
   - Sri Lankan-specific training data and cultural context
   - Local language support and trend recognition
   - Understanding of regional viewing patterns and preferences

2. **Predictive Focus**
   - Forward-looking analytics vs. historical reporting
   - Real-time prediction capabilities
   - Actionable insights for content optimization

3. **Academic Rigor**
   - Research-backed methodology and validation
   - Transparent algorithms and open-source approach
   - Continuous improvement based on academic findings

4. **Accessibility**
   - Free core features with no subscription barriers
   - Web-based interface accessible from any device
   - User-friendly design for non-technical users

5. **Innovation**
   - Separate models for different content types
   - Multi-modal feature engineering
   - Real-time data processing and prediction

### 2.3 Market Entry Strategy

#### 2.3.1 Go-to-Market Approach

**Phase 1: Academic Launch (Weeks 9-10)**
- University presentation and demonstration
  * Incomplete or biased metadata
* What **technical risks** are expected?

  * Overfitting of forecasting models
  * Bad model performance due to niche data
  * Limited Sri Lanka-specific content on YouTube
* Any **deployment/maintenance risks**?

  * Hosting limitations
  * Downtime
* What **mitigation strategies** will you adopt? (e.g., caching, data cleaning, backup models)
For every risk, you need a plan.

Risk: API limits halting data collection.

Mitigation: Use efficient API endpoints, implement caching for API calls, and rotate the team's 3 API keys to triple the daily quota.

Risk: Overfitting the model due to niche data.

Mitigation: Use cross-validation during training. Employ regularization techniques in the model (XGBoost has built-in parameters for this). Focus on strong feature engineering rather than overly complex models.

Risk: Bad model performance.

Mitigation: Start with a simple baseline model. If your complex model can't beat a simple average, you know you have a problem. Focus heavily on cleaning the data and creating meaningful features, as this often yields better results than complex model tuning.

Risk: Hosting limitations or downtime.

Mitigation: Use a reputable cloud provider with a good free tier (e.g., Heroku). Implement a free monitoring service like UptimeRobot to get email alerts if your site goes down.

---

### 2.5 Social/Legal Feasibility

* Are there any **legal constraints** on using YouTube data? (e.g., API Terms of Use, Data Privacy)
* Are you ensuring **compliance** with Google’s API quota, content policies, or user data restrictions?
* Could the system unintentionally be used for **manipulation or spam**?
* Are there **social impacts** of democratizing forecast data (e.g., equalizing advantage between big and small creators)?
Legal Constraints: Your use of public data for analysis and forecasting is generally considered transformative and falls under fair use, but you must adhere to the YouTube API Terms of Service. Add a disclaimer to your site stating you are not affiliated with YouTube and link to their ToS.

Compliance: To ensure compliance, log all your API calls to monitor quota usage. Do not store any PII from video comments or user data without explicit consent and a privacy policy.

Manipulation/Spam: Acknowledge this risk. The tool's purpose is strategic guidance. You can mitigate misuse by requiring user logins (which adds a barrier to bots) and potentially rate-limiting prediction requests per user.

Social Impact: Frame this as a positive. Your tool democratizes data science, giving smaller Sri Lankan creators access to insights that were previously only available to large media companies with dedicated analyst teams, thus leveling the playing field.

---

## ✅ Section 3: Considerations

* Which of these are **most important** to the success of your system? Rank them:

  4. Performance
  1. Accuracy
  3. Usability / Ease of use
  2. Explainability of forecasts
  5. Visualization
  6. Platform Independence
  8. Localization
  7. Integration with third-party tools
* Is the system expected to evolve (e.g., include TikTok or Instagram in future)?
no
* Do you expect **mobile access** or is it primarily desktop/web?
primary:desktop
---

## ✅ Section 4: References

* Which **academic papers, tool documentation, YouTube policies, or blogs** will be referenced?
* Which **ML algorithms**, if any, are drawn from textbooks or journal papers?
* List any **URLs, documentation, or whitepapers** you’ll include (can be tentative).

