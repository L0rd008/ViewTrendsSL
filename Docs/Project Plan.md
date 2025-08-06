# ViewTrendsSL: YouTube Viewership Forecasting for Sri Lankan Audience
## Comprehensive Project Plan

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Technical Specifications](#3-technical-specifications)
4. [Team Structure & Responsibilities](#4-team-structure--responsibilities)
5. [Project Timeline & Milestones](#5-project-timeline--milestones)
6. [Implementation Strategy](#6-implementation-strategy)
7. [Risk Management](#7-risk-management)
8. [Quality Assurance & Testing](#8-quality-assurance--testing)
9. [Deployment & Maintenance](#9-deployment--maintenance)
10. [Future Roadmap](#10-future-roadmap)
11. [Success Metrics & Evaluation](#11-success-metrics--evaluation)
12. [Resources & References](#12-resources--references)

---

## 1. Executive Summary

### 1.1 Project Vision
ViewTrendsSL aims to democratize YouTube analytics for Sri Lankan content creators by providing localized viewership forecasting capabilities. This data-driven tool will enable creators, marketers, and media companies to make informed decisions about content strategy before publishing.

### 1.2 Problem Statement
Currently, there is a critical gap in tools that can predict YouTube video performance specifically for Sri Lankan audiences. Existing global analytics tools lack the cultural context, viewing patterns, and regional nuances that significantly impact video success in Sri Lanka. This project addresses this gap by creating a specialized forecasting model trained on Sri Lankan YouTube data.

### 1.3 Project Objectives
**Primary Objectives:**
- Develop a machine learning model to forecast YouTube video viewership for Sri Lankan audiences
- Create a comprehensive dataset of Sri Lankan YouTube video analytics
- Build a user-friendly web application for viewership prediction
- Achieve prediction accuracy with MAPE < 30% for 7-day forecasts

**Secondary Objectives:**
- Publish a research-grade dataset for academic use
- Contribute to the field of regional social media analytics
- Develop a scalable system architecture for future expansion

### 1.4 Key Deliverables
1. **Data Collection System**: Automated scripts for YouTube data harvesting
2. **Machine Learning Models**: Separate models for Shorts and Long-form content
3. **Web Application**: User-friendly interface for viewership forecasting
4. **Dataset**: Clean, labeled dataset of Sri Lankan YouTube analytics
5. **Documentation**: Comprehensive technical and user documentation
6. **Research Output**: Academic paper and presentation materials

---

## 2. Project Overview

### 2.1 Project Context
**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  
**Duration**: 10 weeks (3 months)  
**Team Size**: 3 members  
**Project Type**: Applied research with practical implementation  

### 2.2 Scope Definition

#### 2.2.1 In Scope (MVP)
- **Data Collection**: YouTube Data API v3 integration for Sri Lankan channels
- **Core Features**:
  - Video metadata extraction (title, duration, category, tags, publish time)
  - Channel statistics (subscriber count, video count, country)
  - Engagement metrics (views, likes, comments) with time-series tracking
- **Machine Learning**:
  - Feature engineering from video metadata
  - Separate XGBoost models for Shorts (≤60s) and Long-form (>60s) videos
  - Prediction targets: 24-hour, 7-day, and 30-day view counts
- **Web Application**:
  - User authentication system
  - Video URL input interface
  - Interactive forecast visualization
  - Basic dashboard with prediction results
- **Database**: SQLite for development, PostgreSQL for production
- **Deployment**: Cloud hosting with Docker containerization

#### 2.2.2 Out of Scope (Future Versions)
- Advanced content analysis (thumbnail, audio, transcript)
- Real-time model retraining
- Competitor analysis tools
- SEO optimization features
- Mobile application
- Multi-platform support (TikTok, Instagram)
- Monetization features

### 2.3 Target Users
**Primary Users:**
- Sri Lankan YouTube content creators
- Digital marketing agencies
- Media production companies
- Independent filmmakers and artists

**Secondary Users:**
- Academic researchers
- Social media analysts
- Business strategists

### 2.4 Success Criteria
1. **Technical Performance**: Achieve MAPE < 30% for 7-day view predictions
2. **Data Quality**: Collect and process data from 100+ Sri Lankan channels
3. **System Reliability**: 95% uptime for web application
4. **User Experience**: Prediction results delivered within 30 seconds
5. **Academic Impact**: Successful project presentation and documentation

---

## 3. Technical Specifications

### 3.1 System Architecture

#### 3.1.1 Architecture Pattern
**Layered Architecture (N-Tier)**
- **Presentation Layer**: Web interface (Streamlit/HTML+CSS+JS)
- **Application Layer**: REST API (Flask)
- **Business Logic Layer**: ML models and data processing (Python)
- **Data Access Layer**: Database operations (SQLAlchemy)
- **Data Storage**: PostgreSQL database

#### 3.1.2 Technology Stack
**Backend:**
- **Language**: Python 3.9+
- **Web Framework**: Flask
- **ML Libraries**: XGBoost, Scikit-learn, Pandas, NumPy
- **API Integration**: google-api-python-client
- **Database ORM**: SQLAlchemy
- **Task Scheduling**: APScheduler

**Frontend:**
- **Primary**: Streamlit (for rapid development)
- **Alternative**: HTML/CSS/JavaScript with Chart.js
- **Visualization**: Plotly, Matplotlib, Seaborn

**Database:**
- **Development**: SQLite
- **Production**: PostgreSQL
- **Caching**: Redis (future implementation)

**DevOps:**
- **Containerization**: Docker
- **Version Control**: Git + GitHub
- **Deployment**: Heroku/PythonAnywhere (free tier)
- **Monitoring**: Basic logging and error tracking

### 3.2 Data Architecture

#### 3.2.1 Database Schema
```sql
-- Channels table
CREATE TABLE channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    subscriber_count INTEGER,
    video_count INTEGER,
    country VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Videos table
CREATE TABLE videos (
    video_id VARCHAR(50) PRIMARY KEY,
    channel_id VARCHAR(50) REFERENCES channels(channel_id),
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP,
    duration_seconds INTEGER,
    category_id INTEGER,
    is_short BOOLEAN,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Snapshots table (time-series data)
CREATE TABLE snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) REFERENCES videos(video_id),
    timestamp TIMESTAMP NOT NULL,
    view_count BIGINT,
    like_count INTEGER,
    comment_count INTEGER,
    INDEX(video_id, timestamp)
);

-- Users table (for web app)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.2 Data Collection Strategy
**Phase 1: Historical Data Collection**
- Target: 100-200 curated Sri Lankan channels
- Timeframe: Videos from last 6-12 months
- Method: One-time bulk collection using efficient API calls

**Phase 2: Active Monitoring**
- Target: New videos from monitored channels
- Frequency: Daily checks for new uploads
- Tracking: Hourly snapshots for first 7 days, then daily for 30 days

**Phase 3: Feature Engineering**
- Time-based features: publish_hour, day_of_week, is_weekend
- Content features: title_length, tag_count, category
- Channel features: subscriber_count, channel_authority_score
- Engagement features: early_engagement_rate, growth_velocity

### 3.3 Machine Learning Pipeline

#### 3.3.1 Model Architecture
**Separate Models Approach:**
- **Shorts Model**: XGBoost for videos ≤60 seconds
- **Long-form Model**: XGBoost for videos >60 seconds
- **Rationale**: Different consumption patterns and discovery mechanisms

**Feature Categories:**
1. **Static Features** (available at upload):
   - Video metadata (title, duration, category, tags)
   - Channel statistics (subscribers, video count)
   - Temporal features (publish time, day of week)

2. **Dynamic Features** (for advanced models):
   - Early engagement metrics (first 6 hours)
   - Growth velocity indicators

#### 3.3.2 Model Training Process
1. **Data Preprocessing**:
   - Handle missing values and outliers
   - Normalize numerical features using Z-score normalization
   - Encode categorical variables (category, language)
   - Apply log transformation to view counts for better distribution
   - Create derived features based on research findings

2. **Feature Engineering** (Based on AMPS & SMTPD Research):
   - **Early Popularity Features**: First 24-hour engagement metrics (critical predictor)
   - **Temporal Features**: publish_hour, day_of_week, is_weekend
   - **Content Features**: title_length, tag_count, description_length
   - **Channel Authority**: subscriber_count, video_count, channel_age
   - **Language Features**: Detected language from title/description
   - **Engagement Ratios**: likes_per_view, comments_per_view

3. **Model Training**:
   - Train/validation/test split (70/15/15)
   - Cross-validation for hyperparameter tuning
   - Feature importance analysis using XGBoost built-in methods
   - Model serialization using joblib
   - Separate training pipelines for Shorts and Long-form videos

4. **Model Evaluation** (Following SMTPD Methodology):
   - **Primary Metrics**: 
     - MAPE (Mean Absolute Percentage Error)
     - MAE (Mean Absolute Error)
     - SRC (Spearman Rank Correlation)
   - **Secondary Metrics**: RMSE, R² Score
   - **Temporal Evaluation**: Performance across different prediction horizons (1d, 7d, 30d)
   - **Category Analysis**: Performance by content category and video type

### 3.4 API Design

#### 3.4.1 Core Endpoints
```python
# Authentication
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout

# Prediction
POST /api/predict
{
    "video_url": "https://youtube.com/watch?v=...",
    "prediction_days": [1, 7, 30]
}

# Response
{
    "video_info": {...},
    "predictions": {
        "1_day": 1500,
        "7_day": 8500,
        "30_day": 15000
    },
    "confidence_intervals": {...},
    "model_version": "v1.0"
}

# Analytics (future)
GET /api/analytics/trends
GET /api/analytics/categories
```

---

## 4. Team Structure & Responsibilities

### 4.1 Team Composition
**Team Members:**
- **Senevirathne S.M.P.U. (220599M)** - Data Lead & YouTube Specialist
- **Sanjula N.G.K. (220578A)** - Backend & Model Lead
- **Shaamma M.S. (220602U)** - Frontend & Documentation Lead

### 4.2 Role Definitions

#### 4.2.1 Senevirathne S.M.P.U. - Data Lead
**Primary Responsibilities:**
- YouTube Data API integration and management
- Data collection strategy and implementation
- Exploratory Data Analysis (EDA)
- Data quality assurance and validation
- Sri Lankan channel identification and curation

**Key Deliverables:**
- Data collection scripts (`collect_channels.py`, `collect_videos.py`)
- Data preprocessing pipeline (`process_data.py`)
- EDA notebooks and insights
- Data quality reports

**Technical Skills Focus:**
- YouTube Data API v3
- Data cleaning and preprocessing
- Statistical analysis and visualization
- Domain expertise in Sri Lankan YouTube landscape

#### 4.2.2 Sanjula N.G.K. - Backend & Model Lead
**Primary Responsibilities:**
- Machine learning model development and training
- Backend API development (Flask)
- Database design and implementation
- System architecture and DevOps
- Performance optimization

**Key Deliverables:**
- Trained ML models (XGBoost for Shorts and Long-form)
- Flask API with authentication and prediction endpoints
- Database schema and migration scripts
- Docker configuration and deployment setup
- Model evaluation and performance reports

**Technical Skills Focus:**
- Machine learning (XGBoost, Scikit-learn)
- Backend development (Flask, SQLAlchemy)
- Database management (PostgreSQL, SQLite)
- DevOps and containerization (Docker)

#### 4.2.3 Shaamma M.S. - Frontend & Documentation Lead
**Primary Responsibilities:**
- Web application user interface development
- Data visualization and dashboard creation
- Project documentation and reporting
- User experience design and testing
- Presentation preparation

**Key Deliverables:**
- Web application frontend (Streamlit or HTML/CSS/JS)
- Interactive data visualizations and charts
- Comprehensive project documentation
- User guide and system documentation
- Final presentation materials

**Technical Skills Focus:**
- Frontend development (Streamlit, HTML/CSS/JavaScript)
- Data visualization (Plotly, Chart.js)
- Technical writing and documentation
- UI/UX design principles

### 4.3 Collaboration Framework

#### 4.3.1 Communication Structure
- **Team Meetings**: Twice weekly (Monday planning, Friday review)
- **Mentor Meetings**: Bi-weekly as per university schedule
- **Daily Standups**: Brief progress updates via team chat
- **Code Reviews**: All major changes require peer review

#### 4.3.2 Development Workflow
1. **Version Control**: Git with feature branch workflow
2. **Code Standards**: PEP-8 for Python, consistent formatting
3. **Documentation**: Inline comments and README updates
4. **Testing**: Unit tests for critical functions
5. **Integration**: Regular integration testing

---

## 5. Project Timeline & Milestones

### 5.1 Project Phases Overview
**Total Duration**: 10 weeks (August 24, 2025 - November 1, 2025)

### 5.2 Detailed Timeline

#### **Week 1-2: Project Foundation & Planning**
**Milestone**: Project Setup Complete

**Week 1 Activities:**
- [ ] Project repository setup and team onboarding
- [ ] Development environment configuration (Docker, Python, APIs)
- [ ] Initial documentation framework
- [ ] YouTube API key setup and quota management
- [ ] Literature review and competitive analysis

**Week 2 Activities:**
- [ ] Finalize project scope and requirements
- [ ] Complete System Requirements Specification (SRS)
- [ ] Database schema design and implementation
- [ ] Initial Sri Lankan channel identification (seed list of 50+ channels)

**Deliverables:**
- Project Proposal ✓ (Completed)
- Project Feasibility Document
- Project Schedule (Gantt Chart)
- Development environment setup

#### **Week 3-4: Data Collection & Infrastructure**
**Milestone**: Data Pipeline Operational

**Week 3 Activities:**
- [ ] Implement core data collection scripts
- [ ] YouTube API integration and testing
- [ ] Database setup and initial data ingestion
- [ ] Data validation and quality checks
- [ ] System Requirements Specification finalization

**Week 4 Activities:**
- [ ] Scale data collection to 100+ channels
- [ ] Implement automated data monitoring
- [ ] Begin historical data collection (6-month backlog)
- [ ] Software Architecture Document completion
- [ ] **Mentor Meetup 1**

**Deliverables:**
- System Requirement Specification (SRS)
- System Architecture and Design (SAD)
- Functional data collection pipeline
- Initial dataset (1000+ videos)

#### **Week 5-6: Model Development & Mid-Evaluation**
**Milestone**: Working ML Models

**Week 5 Activities:**
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering and selection
- [ ] Initial model training (baseline models)
- [ ] Model evaluation framework setup
- [ ] **Mid-evaluation Preparation**

**Week 6 Activities:**
- [ ] **Mid-evaluation (Prototype Demo)**
- [ ] Advanced model development (XGBoost optimization)
- [ ] Model validation and testing
- [ ] Performance tuning and optimization
- [ ] Backend API development initiation

**Deliverables:**
- Mid-evaluation Prototype Demo
- Trained baseline models
- EDA report and insights
- Feature engineering documentation

#### **Week 7-8: System Integration & Testing**
**Milestone**: Integrated System

**Week 7 Activities:**
- [ ] Backend API development and testing
- [ ] Frontend development initiation
- [ ] Model-API integration
- [ ] Database optimization and indexing
- [ ] **Mentor Meetup 2**

**Week 8 Activities:**
- [ ] Frontend-backend integration
- [ ] End-to-end system testing
- [ ] User interface refinement
- [ ] Performance optimization
- [ ] Testing & Evaluation Document preparation

**Deliverables:**
- Functional web application
- Testing & Evaluation Document
- Integrated system with all components

#### **Week 9-10: Deployment & Finalization**
**Milestone**: Production-Ready System

**Week 9 Activities:**
- [ ] System deployment to cloud platform
- [ ] Final testing and bug fixes
- [ ] Documentation completion
- [ ] User acceptance testing
- [ ] **Mentor Meetup 3**

**Week 10 Activities:**
- [ ] **Final Evaluation (Live Demo)**
- [ ] Final Report completion
- [ ] Presentation preparation and delivery
- [ ] **Final Product Resources submission**
- [ ] **Final Report Submission**

**Deliverables:**
- Final Evaluation (Live Demo)
- Final Product Resources
- Final Report Submission
- Deployed production system

### 5.3 Critical Path Analysis
**Critical Dependencies:**
1. YouTube API quota management → Data collection success
2. Data quality → Model performance
3. Model performance → System value proposition
4. Integration testing → Deployment readiness

**Risk Mitigation Timeline:**
- Week 2: API quota optimization strategies
- Week 4: Data quality validation checkpoints
- Week 6: Model performance evaluation gates
- Week 8: Integration testing completion

---

## 6. Implementation Strategy

### 6.1 Development Methodology
**Hybrid Approach**: Structured phases with iterative development
- **Planning Phase**: Traditional waterfall for documentation and architecture
- **Development Phase**: Agile iterations with weekly sprints
- **Integration Phase**: Continuous integration and testing

### 6.2 MVP Definition

#### 6.2.1 Core MVP Features
1. **Data Collection System**:
   - Automated YouTube API data harvesting
   - Support for 100+ Sri Lankan channels
   - Historical and real-time data collection

2. **Machine Learning Models**:
   - Separate models for Shorts and Long-form videos
   - Prediction targets: 24h, 7d, 30d view counts
   - Feature engineering from video metadata

3. **Web Application**:
   - User authentication (email/password)
   - Video URL input interface
   - Forecast visualization (line charts)
   - Basic prediction results display

4. **Database System**:
   - Structured data storage (PostgreSQL)
   - Efficient querying and indexing
   - Data backup and recovery

#### 6.2.2 MVP Success Criteria
- **Functionality**: All core features working end-to-end
- **Performance**: Predictions delivered within 30 seconds
- **Accuracy**: MAPE < 35% for 7-day forecasts (realistic target)
- **Reliability**: System handles 10+ concurrent users
- **Usability**: Intuitive interface requiring minimal training

### 6.3 Development Phases

#### 6.3.1 Phase 1: Foundation (Weeks 1-2)
**Objective**: Establish development infrastructure and project foundation

**Key Activities:**
- Environment setup and team onboarding
- API integration and testing
- Database design and implementation
- Documentation framework establishment

**Success Criteria:**
- All team members can run the project locally
- YouTube API integration working
- Database schema implemented and tested
- Project documentation structure in place

#### 6.3.2 Phase 2: Data Pipeline (Weeks 3-4)
**Objective**: Build robust data collection and processing pipeline

**Key Activities:**
- Implement data collection scripts
- Scale to 100+ channels
- Data quality validation
- Historical data backfill

**Success Criteria:**
- Automated data collection from target channels
- Clean, structured dataset with 1000+ videos
- Data quality metrics within acceptable ranges
- Monitoring and alerting for data pipeline

#### 6.3.3 Phase 3: Model Development (Weeks 5-6)
**Objective**: Develop and validate machine learning models

**Key Activities:**
- Exploratory data analysis
- Feature engineering and selection
- Model training and optimization
- Performance evaluation

**Success Criteria:**
- Trained models for Shorts and Long-form videos
- Model performance meets minimum thresholds
- Feature importance analysis completed
- Model serialization and versioning implemented

#### 6.3.4 Phase 4: System Integration (Weeks 7-8)
**Objective**: Integrate all components into working system

**Key Activities:**
- Backend API development
- Frontend interface creation
- Component integration testing
- Performance optimization

**Success Criteria:**
- End-to-end system functionality
- API endpoints working correctly
- User interface intuitive and responsive
- System performance within acceptable limits

#### 6.3.5 Phase 5: Deployment & Finalization (Weeks 9-10)
**Objective**: Deploy production system and complete project

**Key Activities:**
- Cloud deployment and configuration
- Final testing and optimization
- Documentation completion
- Presentation preparation

**Success Criteria:**
- Production system deployed and accessible
- All documentation completed
- Final presentation delivered successfully
- Project meets all academic requirements

---

## 7. Risk Management

### 7.1 Risk Assessment Matrix

#### 7.1.1 High-Priority Risks

**Risk 1: YouTube API Quota Exhaustion**
- **Probability**: High
- **Impact**: Critical
- **Description**: Daily API quota (10,000 units) insufficient for data collection needs
- **Mitigation Strategies**:
  - Use 3 team member API keys (30,000 total units)
  - Implement efficient API call patterns (avoid search.list)
  - Cache API responses to prevent redundant calls
  - Implement rate limiting and quota monitoring
- **Contingency Plan**: Use Social Blade or alternative data sources if API limits persist

**Risk 2: Model Performance Below Expectations**
- **Probability**: Medium
- **Impact**: High
- **Description**: ML models fail to achieve acceptable prediction accuracy
- **Mitigation Strategies**:
  - Start with simple baseline models for comparison
  - Focus on feature engineering over complex algorithms
  - Use cross-validation and proper evaluation metrics
  - Implement ensemble methods if single models underperform
- **Contingency Plan**: Adjust success criteria or focus on specific video categories

**Risk 3: Data Quality Issues**
- **Probability**: Medium
- **Impact**: High
- **Description**: Collected data contains errors, missing values, or biases
- **Mitigation Strategies**:
  - Implement comprehensive data validation checks
  - Use multiple data sources for verification
  - Create data quality monitoring dashboards
  - Establish data cleaning and preprocessing pipelines
- **Contingency Plan**: Manual data curation for critical datasets

#### 7.1.2 Medium-Priority Risks

**Risk 4: Team Coordination Challenges**
- **Probability**: Medium
- **Impact**: Medium
- **Description**: Different operating systems and development environments cause integration issues
- **Mitigation Strategies**:
  - Use Docker for consistent development environments
  - Implement clear Git workflow and code review processes
  - Regular team meetings and communication
  - Shared documentation and knowledge transfer
- **Contingency Plan**: Designate integration lead and establish conflict resolution process

**Risk 5: Deployment and Hosting Issues**
- **Probability**: Medium
- **Impact**: Medium
- **Description**: Cloud deployment fails or hosting costs exceed budget
- **Mitigation Strategies**:
  - Use free-tier cloud services (Heroku, PythonAnywhere)
  - Implement Docker for consistent deployment
  - Test deployment process early and frequently
  - Have backup hosting options identified
- **Contingency Plan**: Local deployment for demonstration if cloud deployment fails

**Risk 6: Scope Creep**
- **Probability**: Medium
- **Impact**: Medium
- **Description**: Team attempts to implement too many features, compromising MVP delivery
- **Mitigation Strategies**:
  - Clearly defined MVP scope with feature prioritization
  - Regular scope review meetings
  - "MVP/V2/Backlog" feature categorization
  - Strong project management and timeline adherence
- **Contingency Plan**: Feature freeze and focus on core functionality

#### 7.1.3 Low-Priority Risks

**Risk 7: External API Changes**
- **Probability**: Low
- **Impact**: Medium
- **Description**: YouTube API changes break data collection scripts
- **Mitigation Strategies**:
  - Monitor API documentation and announcements
  - Implement robust error handling
  - Version control for API integration code
  - Test API calls regularly
- **Contingency Plan**: Rapid code updates or alternative data sources

**Risk 8: Hardware/Software Failures**
- **Probability**: Low
- **Impact**: Low
- **Description**: Development machine failures or software corruption
- **Mitigation Strategies**:
  - Regular code commits to GitHub
  - Cloud-based development environments
  - Automated backups of data and models
  - Distributed development across team members
- **Contingency Plan**: Restore from backups and redistribute work

### 7.2 Risk Monitoring and Response

#### 7.2.1 Risk Monitoring Framework
- **Weekly Risk Reviews**: Assess risk status during team meetings
- **Risk Indicators**: Define measurable indicators for each risk
- **Escalation Procedures**: Clear process for escalating risks to mentors
- **Risk Log**: Maintain detailed log of risks, responses, and outcomes

#### 7.2.2 Communication Plan
- **Internal**: Team members report risks immediately
- **External**: Mentor notification for high-impact risks
- **Documentation**: All risk responses documented for future reference

---

## 8. Quality Assurance & Testing

### 8.1 Testing Strategy

#### 8.1.1 Testing Levels
1. **Unit Testing**: Individual functions and components
2. **Integration Testing**: Component interactions and data flow
3. **System Testing**: End-to-end functionality
4. **User Acceptance Testing**: Real-world usage scenarios

#### 8.1.2 Testing Framework
**Tools and Libraries:**
- **Python Testing**: pytest for unit tests
- **API Testing**: Postman or requests library
- **Frontend Testing**: Manual testing with user scenarios
- **Performance Testing**: Load testing with concurrent users

### 8.2 Quality Metrics

#### 8.2.1 Code Quality
- **Code Coverage**: Minimum 70% for critical functions
- **Code Style**: PEP-8 compliance using flake8
- **Documentation**: Inline comments and docstrings
- **Code Review**: All major changes peer-reviewed

#### 8.2.2 System Quality
- **Performance**: Response time < 30 seconds for predictions
- **Reliability**: 95% uptime during testing period
- **Accuracy**: Model performance metrics within targets
- **Usability**: User interface intuitive and error-free

### 8.3 Testing Schedule

#### 8.3.1 Continuous Testing (Weeks 3-8)
- Daily unit testing during development
- Weekly integration testing
- Continuous code quality monitoring

#### 8.3.2 Formal Testing Phase (Week 8)
- Comprehensive system testing
- Performance and load testing
- User acceptance testing with stakeholders
- Bug fixing and optimization

#### 8.3.3 Pre-Deployment Testing (Week 9)
- Final system validation
- Deployment environment testing
- Backup and recovery testing

---

## 9. Deployment & Maintenance

### 9.1 Deployment Strategy

#### 9.1.1 Deployment Architecture
**Target Environment**: Cloud-based deployment
- **Primary Option**: Heroku (free tier)
- **Alternative Options**: PythonAnywhere, Vercel
- **Containerization**: Docker for consistent deployment
- **Database**: PostgreSQL (cloud-hosted)

#### 9.1.2 Deployment Process
1. **Containerization**: Create Docker images for application
2. **Environment Configuration**: Set up production environment variables
3. **Database Migration**: Deploy database schema and initial data
4. **Application Deployment**: Deploy containerized application
5. **Testing**: Validate deployment with smoke tests
6. **Monitoring**: Set up basic monitoring and logging

### 9.2 Production Configuration

#### 9.2.1 Environment Variables
```bash
# Database
DATABASE_URL=postgresql://...
DATABASE_SSL_MODE=require

# API Keys
YOUTUBE_API_KEY_1=...
YOUTUBE_API_KEY_2=...
YOUTUBE_API_KEY_3=...

# Application
FLASK_ENV=production
SECRET_KEY=...
DEBUG=False

# Monitoring
LOG_LEVEL=INFO
```

#### 9.2.2 Security Considerations
- **API Key Protection**: Environment variables, never in code
- **Password Hashing**: bcrypt for user passwords
- **HTTPS**: SSL/TLS encryption for all communications
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent API abuse

### 9.3 Monitoring and Maintenance

#### 9.3.1 Monitoring Strategy
**Basic Monitoring (MVP):**
- Application logs for error tracking
- Basic uptime monitoring
- Performance metrics (response times)
- API quota usage tracking

**Advanced Monitoring (Future):**
- Real-time performance dashboards
- Automated alerting for system issues
- User analytics and usage patterns
- Model performance drift detection

#### 9.3.2 Maintenance Plan
**During Project Period:**
- Daily monitoring of system health
- Weekly performance reviews
- Immediate bug fixes for critical issues
- Regular data backup verification

**Post-Project:**
- Monthly system health checks
- Quarterly model performance reviews
- Annual security updates
- Data retention policy implementation

---

## 10. Future Roadmap

### 10.1 Version 2.0 Features

#### 10.1.1 Advanced Analytics
**Content Analysis:**
- Thumbnail analysis using computer vision
- Audio sentiment analysis
- Transcript processing and keyword extraction
- Video content categorization

**Competitive Intelligence:**
- Competitor channel analysis
- Market trend identification
- Performance benchmarking
- Content gap analysis

**SEO Optimization:**
- Title optimization suggestions
- Tag recommendation engine
- Optimal publishing time analysis
- Hashtag performance tracking

#### 10.1.2 Enhanced User Experience
**Dashboard Improvements:**
- Advanced data visualizations
- Customizable analytics dashboards
- Export functionality (PDF, CSV)
- Mobile-responsive design

**Collaboration Features:**
- Team accounts and permissions
- Shared analytics and reports
- Comment and annotation system
- Project management integration

### 10.2 Platform Expansion

#### 10.2.1 Multi-Platform Support
- **TikTok Integration**: Short-form video analytics
- **Instagram Reels**: Cross-platform comparison
- **Facebook Videos**: Extended social media coverage
- **LinkedIn Videos**: Professional content analysis

#### 10.2.2 Geographic Expansion
- **Regional Models**: Country-specific prediction models
- **Language Support**: Multi-language interface and analysis
- **Cultural Adaptation**: Region-specific features and insights
- **Local Partnerships**: Collaboration with regional creators

### 10.3 Technical Enhancements

#### 10.3.1 Architecture Improvements
**Scalability:**
- Microservices architecture
- Load balancing and auto-scaling
- Distributed computing for model training
- Real-time data processing pipelines

**Performance:**
- Advanced caching strategies
- Model optimization and quantization
- Database sharding and optimization
- CDN integration for global access

#### 10.3.2 Advanced Machine Learning
**Model Improvements:**
- Deep learning models (LSTMs, Transformers)
- Multi-modal learning (text, image, audio)
- Transfer learning from global models
- Ensemble methods and model stacking

**Real-time Features:**
- Live prediction updates
- Streaming data processing
- Real-time model retraining
- Dynamic feature engineering

### 10.4 Business Development

#### 10.4.1 Monetization Strategy
**Freemium Model:**
- Basic predictions (free)
- Advanced analytics (premium)
- API access (enterprise)
- Custom model training (enterprise)

**Partnership Opportunities:**
- YouTube creator program integration
- Marketing agency partnerships
- Educational institution licensing
- Research collaboration agreements

#### 10.4.2 Research and Publication
**Academic Contributions:**
- Research paper publication
- Conference presentations
- Open-source dataset release
- Academic collaboration opportunities

**Industry Impact:**
- Industry reports and whitepapers
- Best practices documentation
- Case studies and success stories
- Thought leadership content

---

## 11. Success Metrics & Evaluation

### 11.1 Technical Performance Metrics

#### 11.1.1 Model Performance
**Primary Metrics:**
- **MAPE (Mean Absolute Percentage Error)**: Target < 30% for 7-day predictions
- **MAE (Mean Absolute Error)**: Average prediction error in view count
- **RMSE (Root Mean Squared Error)**: Overall prediction accuracy
- **R² Score**: Variance explained by the model

**Performance by Category:**
- Shorts vs. Long-form video accuracy
- Category-specific performance (News, Entertainment, Education)
- Channel size impact on prediction accuracy
- Time-based performance (weekday vs. weekend predictions)

#### 11.1.2 System Performance
**Response Time Metrics:**
- **Prediction Generation**: < 30 seconds end-to-end
- **API Response Time**: < 5 seconds for standard requests
- **Page Load Time**: < 3 seconds for web interface
- **Database Query Time**: < 1 second for standard queries

**Scalability Metrics:**
- **Concurrent Users**: Support 10+ simultaneous users
- **Data Throughput**: Process 1000+ videos per hour
- **Storage Efficiency**: Optimize database size and query performance
- **API Quota Utilization**: Maintain <80% of daily quota usage

### 11.2 Business Impact Metrics

#### 11.2.1 User Engagement
**Usage Metrics:**
- **Active Users**: Track daily and weekly active users
- **Prediction Requests**: Monitor prediction volume and patterns
- **User Retention**: Measure return user percentage
- **Session Duration**: Average time spent on platform

**User Satisfaction:**
- **Prediction Accuracy Feedback**: User-reported accuracy ratings
- **User Interface Usability**: Task completion rates and error rates
- **Feature Adoption**: Usage statistics for different features
- **Support Requests**: Volume and resolution time for user issues

#### 11.2.2 Academic Success
**Project Deliverables:**
- **Documentation Quality**: Comprehensive and well-structured documentation
- **Presentation Impact**: Successful final presentation and demo
- **Code Quality**: Clean, maintainable, and well-documented codebase
- **Innovation Factor**: Novel approaches and technical contributions

**Research Contributions:**
- **Dataset Quality**: Comprehensive Sri Lankan YouTube dataset
- **Model Innovation**: Novel approaches to regional viewership prediction
- **Academic Publications**: Research papers and conference presentations
- **Open Source Impact**: Community adoption and contributions

### 11.3 Data Quality Metrics

#### 11.3.1 Dataset Completeness
**Coverage Metrics:**
- **Channel Diversity**: 100+ channels across multiple categories
- **Video Volume**: 5000+ videos in training dataset
- **Temporal Coverage**: 6-12 months of historical data
- **Geographic Relevance**: >90% Sri Lankan-focused content

**Data Integrity:**
- **Missing Data Rate**: <5% missing values in critical fields
- **Data Accuracy**: >95% accuracy in automated data validation
- **Update Frequency**: Daily data collection with <24h latency
- **Error Rate**: <1% errors in data processing pipeline

#### 11.3.2 Feature Quality
**Feature Engineering Success:**
- **Feature Importance**: Clear ranking of predictive features
- **Feature Correlation**: Optimal balance of informative vs. redundant features
- **Feature Stability**: Consistent feature performance across time periods
- **Domain Relevance**: Features align with YouTube algorithm factors

### 11.4 Evaluation Framework

#### 11.4.1 Testing Methodology
**Model Evaluation:**
1. **Cross-Validation**: 5-fold cross-validation for robust performance estimates
2. **Temporal Validation**: Test on future data to simulate real-world usage
3. **Category-Specific Testing**: Evaluate performance across different content types
4. **Baseline Comparison**: Compare against simple heuristic and statistical models

**System Testing:**
1. **Functional Testing**: Verify all features work as specified
2. **Performance Testing**: Validate response times and scalability
3. **Integration Testing**: Ensure seamless component interaction
4. **User Acceptance Testing**: Real-world usage scenarios with stakeholders

#### 11.4.2 Success Thresholds
**Minimum Viable Product (MVP) Thresholds:**
- **Model Accuracy**: MAPE < 35% for 7-day predictions
- **System Performance**: 95% of predictions delivered within 30 seconds
- **User Experience**: 90% task completion rate for core features
- **System Reliability**: 95% uptime during testing period

**Stretch Goals:**
- **Model Accuracy**: MAPE < 25% for 7-day predictions
- **Advanced Features**: Implement 2+ future roadmap features
- **Research Impact**: Submit paper to academic conference
- **Community Adoption**: 50+ external users during beta testing

---

## 12. Resources & References

### 12.1 Technical Resources

#### 12.1.1 APIs and Services
**Primary APIs:**
- **YouTube Data API v3**: https://developers.google.com/youtube/v3/getting-started
  - Video metadata and statistics
  - Channel information and analytics
  - Search and discovery functionality
  - Quota management and optimization

**Supporting Services:**
- **Google Cloud Platform**: Authentication and API management
- **Social Blade API**: Alternative data source for validation
- **Google Trends API**: Trending topics and keyword analysis

#### 12.1.2 Development Tools and Libraries
**Backend Development:**
```python
# Core Libraries
pandas>=1.5.0          # Data manipulation and analysis
numpy>=1.21.0           # Numerical computing
scikit-learn>=1.1.0     # Machine learning algorithms
xgboost>=1.6.0          # Gradient boosting framework
flask>=2.2.0            # Web framework
sqlalchemy>=1.4.0       # Database ORM

# API and Data Collection
google-api-python-client>=2.0.0  # YouTube API client
requests>=2.28.0                  # HTTP requests
python-dotenv>=0.19.0            # Environment variable management
schedule>=1.1.0                  # Task scheduling
apscheduler>=3.9.0               # Advanced scheduling

# Data Processing
isodate>=0.6.0          # ISO 8601 date parsing
langdetect>=1.0.9       # Language detection
textblob>=0.17.1        # Text processing and sentiment analysis
nltk>=3.7               # Natural language processing

# Visualization and Analysis
matplotlib>=3.5.0       # Plotting library
seaborn>=0.11.0         # Statistical visualization
plotly>=5.10.0          # Interactive visualizations
jupyter>=1.0.0          # Notebook environment

# Database and Caching
psycopg2-binary>=2.9.0  # PostgreSQL adapter
redis>=4.3.0            # Caching (future implementation)

# Testing and Quality
pytest>=7.1.0           # Testing framework
flake8>=4.0.0           # Code linting
black>=22.0.0           # Code formatting
coverage>=6.4.0         # Code coverage analysis

# Deployment and DevOps
docker>=5.0.0           # Containerization
gunicorn>=20.1.0        # WSGI HTTP Server
```

**Frontend Development:**
```javascript
// Core Frontend (if using HTML/CSS/JS)
chart.js>=3.9.0         // Data visualization
axios>=0.27.0           // HTTP client
bootstrap>=5.2.0        // CSS framework

// Alternative: Streamlit
streamlit>=1.12.0       // Rapid web app development
streamlit-plotly>=0.1.0 // Plotly integration
```

#### 12.1.3 Infrastructure and Deployment
**Development Environment:**
- **Docker**: Containerization for consistent environments
- **Git + GitHub**: Version control and collaboration
- **VS Code**: Recommended IDE with Python extensions
- **Jupyter Lab**: Data analysis and experimentation

**Production Environment:**
- **Heroku**: Primary deployment platform (free tier)
- **PythonAnywhere**: Alternative deployment option
- **PostgreSQL**: Production database (Heroku Postgres)
- **GitHub Actions**: CI/CD pipeline (future implementation)

### 12.2 Academic References

#### 12.2.1 Research Papers
**Primary Academic Foundation:**
1. **"AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms"** - Journal of Retailing and Consumer Services (2024)
   - https://www.sciencedirect.com/science/article/abs/pii/S0969698924000742
   - **Key Contributions**: 
     - CDF-based popularity standard for realistic real-world distribution
     - Multi-modal attention mechanism (BiLSTM + Self-Attention + Co-Attention)
     - Separate treatment of Shorts vs Long-form videos
     - 13K YouTube Shorts dataset with comprehensive metadata
   - **Relevance**: Direct validation of our separate models approach and multi-modal feature engineering strategy

2. **"SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity"** - arXiv:2503.04446v1 (2025)
   - https://arxiv.org/html/2503.04446v1
   - **Key Contributions**:
     - 282K multilingual YouTube samples across 90+ languages
     - Temporal alignment importance for accurate predictions
     - Early popularity as the most critical predictive feature
     - 30-day prediction framework with daily tracking
   - **Relevance**: Validates our temporal prediction approach and emphasizes early engagement metrics

**Supporting Literature:**
3. "Social Media Analytics: A Survey of Techniques, Tools and Platforms" - ACM Computing Surveys
   - Relevance: Comprehensive overview of social media analytics methodologies

4. "Regional Social Media Behavior Analysis: A Cross-Cultural Study" - Journal of Computer-Mediated Communication
   - Relevance: Regional differences in social media consumption patterns

**Machine Learning for Time Series and Regression:**
5. "XGBoost: A Scalable Tree Boosting System" - KDD 2016
   - Relevance: Technical foundation for chosen ML algorithm

6. "Feature Engineering for Machine Learning: Principles and Techniques" - O'Reilly Media
   - Relevance: Best practices for feature engineering in ML projects

#### 12.2.2 Industry Reports and Whitepapers
**YouTube and Video Content Industry:**
1. "YouTube Creator Economy Report 2024" - YouTube Official
2. "Social Media Trends in South Asia" - We Are Social & Kepios
3. "Digital 2024: Sri Lanka" - DataReportal
4. "Video Content Marketing Trends" - Wistia State of Video Report

**Data Science and Analytics:**
5. "State of Data Science 2024" - Kaggle
6. "Machine Learning in Production" - Google AI
7. "Best Practices for ML Engineering" - Google Developers

### 12.3 Educational Resources

#### 12.3.1 Online Courses and Tutorials
**Machine Learning and Data Science:**
- **Coursera**: Machine Learning Specialization (Andrew Ng)
- **edX**: MIT Introduction to Machine Learning
- **Kaggle Learn**: Practical machine learning courses
- **YouTube**: 3Blue1Brown Neural Networks series

**Web Development:**
- **Flask Documentation**: Official Flask tutorial and guides
- **Streamlit Documentation**: Building data apps with Streamlit
- **MDN Web Docs**: HTML, CSS, and JavaScript fundamentals

**YouTube API Development:**
- **Google Developers**: YouTube Data API v3 documentation
- **YouTube Creators**: API best practices and case studies
- **GitHub**: Open source projects using YouTube API

#### 12.3.2 Books and Publications
**Technical References:**
1. "Hands-On Machine Learning" by Aurélien Géron
2. "Python for Data Analysis" by Wes McKinney
3. "Flask Web Development" by Miguel Grinberg
4. "Designing Data-Intensive Applications" by Martin Kleppmann

**Project Management and Software Engineering:**
5. "The Pragmatic Programmer" by David Thomas and Andrew Hunt
6. "Clean Code" by Robert C. Martin
7. "Agile Software Development" by Robert C. Martin

### 12.4 Tools and Platforms

#### 12.4.1 Development and Collaboration Tools
**Project Management:**
- **GitHub Projects**: Task tracking and project management
- **Trello**: Visual project organization (alternative)
- **Google Workspace**: Document collaboration and communication
- **Slack/Discord**: Team communication (if needed)

**Documentation and Presentation:**
- **Markdown**: Documentation format
- **Jupyter Notebooks**: Analysis and experimentation documentation
- **Google Slides**: Presentation preparation
- **Draw.io**: System architecture diagrams

#### 12.4.2 Data Analysis and Visualization Tools
**Analysis Platforms:**
- **Jupyter Lab**: Interactive data analysis
- **Google Colab**: Cloud-based notebook environment
- **Kaggle Notebooks**: Collaborative data science platform

**Visualization Tools:**
- **Plotly**: Interactive web-based visualizations
- **Tableau Public**: Advanced data visualization (if needed)
- **Google Data Studio**: Dashboard creation (alternative)

### 12.5 Competitive Analysis

#### 12.5.1 Existing YouTube Analytics Tools
**Global Platforms:**
1. **VidIQ**
   - Features: SEO optimization, competitor analysis, trend tracking
   - Limitations: Global focus, limited regional customization
   - Pricing: Freemium model with premium features

2. **TubeBuddy**
   - Features: Channel management, A/B testing, analytics
   - Limitations: Chrome extension only, limited prediction capabilities
   - Pricing: Subscription-based with multiple tiers

3. **Social Blade**
   - Features: Channel statistics, growth tracking, rankings
   - Limitations: Historical data focus, limited predictive features
   - Pricing: Free with premium options

**Regional/Local Tools:**
4. **Viewstats**
   - Features: Basic analytics and statistics
   - Limitations: Limited accuracy, basic feature set
   - Relevance: Demonstrates market need for better tools

#### 12.5.2 Competitive Advantages
**ViewTrendsSL Differentiators:**
1. **Regional Specialization**: Sri Lankan-specific data and insights
2. **Predictive Focus**: Forward-looking analytics vs. historical reporting
3. **Academic Rigor**: Research-based methodology and validation
4. **Open Source Approach**: Transparent algorithms and community contribution
5. **Cultural Context**: Understanding of local content and audience behavior

### 12.6 Legal and Compliance Resources

#### 12.6.1 API Terms of Service
**YouTube Data API:**
- **Terms of Service**: https://developers.google.com/youtube/terms/api-services-terms-of-service
- **Developer Policies**: https://developers.google.com/youtube/terms/developer-policies
- **Quota and Usage Guidelines**: https://developers.google.com/youtube/v3/getting-started#quota

**Compliance Requirements:**
- Data usage restrictions and attribution requirements
- Rate limiting and quota management
- User privacy and data protection guidelines

#### 12.6.2 Privacy and Data Protection
**Relevant Regulations:**
- **GDPR**: European data protection regulation (if applicable)
- **Sri Lankan Data Protection Laws**: Local privacy requirements
- **University Ethics Guidelines**: Academic research ethics

**Implementation Requirements:**
- Privacy policy and terms of service
- User consent mechanisms
- Data retention and deletion policies
- Security measures for user data

### 12.7 Support and Community Resources

#### 12.7.1 Technical Support
**Official Support Channels:**
- **Google Developers Support**: YouTube API technical support
- **Stack Overflow**: Community-driven technical Q&A
- **GitHub Issues**: Open source project support
- **University Mentors**: Academic guidance and support

**Community Resources:**
- **Reddit**: r/MachineLearning, r/datascience, r/YouTube
- **Discord/Slack**: ML and data science communities
- **LinkedIn Groups**: Professional networking and knowledge sharing

#### 12.7.2 Academic Support
**University Resources:**
- **Project Mentors**: Regular guidance and feedback
- **Library Resources**: Access to academic papers and books
- **Computing Resources**: University servers and software licenses
- **Peer Support**: Collaboration with other student projects

**External Academic Support:**
- **Research Conferences**: Opportunities for paper submission
- **Academic Networks**: Connections with researchers in the field
- **Open Source Community**: Contribution opportunities and feedback

---

## Appendices

### Appendix A: Project Charter
**Project Name**: ViewTrendsSL - YouTube Viewership Forecasting for Sri Lankan Audience  
**Project Manager**: Team Collaborative Leadership  
**Sponsor**: University of Moratuwa - CS3501 Course  
**Start Date**: August 24, 2025  
**End Date**: November 1, 2025  
**Budget**: Zero-cost (utilizing free-tier services)  

### Appendix B: Glossary of Terms
- **API**: Application Programming Interface
- **EDA**: Exploratory Data Analysis
- **MAPE**: Mean Absolute Percentage Error
- **MVP**: Minimum Viable Product
- **SRS**: System Requirements Specification
- **SAD**: Software Architecture Document
- **XGBoost**: Extreme Gradient Boosting

### Appendix C: Contact Information
**Team Members:**
- **Senevirathne S.M.P.U.**: [email] - Data Lead
- **Sanjula N.G.K.**: [email] - Backend & Model Lead  
- **Shaamma M.S.**: [email] - Frontend & Documentation Lead

**Project Repository**: https://github.com/L0rd008/ViewTrendsSL  
**Documentation**: Available in project repository under `/Docs`

---

*This document is a living document and will be updated throughout the project lifecycle to reflect changes in scope, timeline, and requirements.*

**Document Version**: 1.0  
**Last Updated**: August 6, 2025  
**Next Review**: August 13, 2025
