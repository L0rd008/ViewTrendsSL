# ViewTrendsSL: YouTube Viewership Forecasting for Sri Lankan Audience
## Project Proposal

**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  
**Team Members**: 
- Senevirathne S.M.P.U. (220599M) - Data Lead
- Sanjula N.G.K. (220578A) - Backend & Model Lead  
- Shaamma M.S. (220602U) - Frontend & Documentation Lead

**Project Duration**: 10 weeks (August 24, 2025 - November 1, 2025)

---

## 1. Executive Summary

### 1.1 Project Vision
ViewTrendsSL addresses a critical gap in the Sri Lankan digital content landscape by providing the first localized YouTube viewership forecasting tool specifically designed for Sri Lankan creators and audiences. This data-driven solution will democratize access to predictive analytics, enabling content creators, marketers, and media companies to make informed strategic decisions before publishing content.

### 1.2 Problem Statement
Currently, Sri Lankan YouTube creators lack access to region-specific predictive analytics tools. Existing global platforms like VidIQ and TubeBuddy provide historical analytics but fail to capture the unique cultural context, viewing patterns, and algorithmic behaviors specific to Sri Lankan audiences. This results in suboptimal content strategies and missed opportunities for creators in the rapidly growing Sri Lankan digital economy.

### 1.3 Proposed Solution
We propose to develop a comprehensive machine learning system that:
- **Predicts viewership** for YouTube videos at 24-hour, 7-day, and 30-day intervals
- **Focuses specifically** on Sri Lankan audience behavior and content patterns
- **Provides actionable insights** through an intuitive web-based dashboard
- **Leverages cutting-edge research** in social media popularity prediction

### 1.4 Expected Impact
- **For Creators**: Strategic content planning with data-driven insights
- **For Marketers**: Optimized campaign planning and budget allocation
- **For Academia**: First comprehensive Sri Lankan YouTube dataset and research contribution
- **For Industry**: Foundation for regional social media analytics tools

---

## 2. Literature Review & Research Foundation

### 2.1 Academic Foundation
Our approach is grounded in recent breakthrough research in social media popularity prediction:

**Primary Research Validation:**
1. **AMPS Study (2024)**: "Predicting popularity of short-form videos using multi-modal attention mechanisms" validates our separate modeling approach for Shorts vs Long-form content and confirms the effectiveness of multi-modal feature engineering.

2. **SMTPD Benchmark (2025)**: "A New Benchmark for Temporal Prediction of Social Media Popularity" demonstrates the critical importance of temporal alignment and early popularity features, directly supporting our prediction methodology.

**Key Research Insights Applied:**
- **Early Popularity Principle**: First 24-hour engagement metrics are the strongest predictors of long-term performance
- **Content Type Differentiation**: Shorts (≤60s) and Long-form videos require separate prediction models due to fundamentally different consumption patterns
- **Temporal Alignment**: Time-synchronized predictions significantly outperform retrospective analysis
- **Multi-modal Features**: Combination of textual, numerical, and categorical features provides optimal prediction accuracy

### 2.2 Competitive Analysis
**Existing Global Tools:**
- **VidIQ**: Global focus, limited regional customization, subscription-based
- **TubeBuddy**: Chrome extension only, historical analytics focus
- **Social Blade**: Basic statistics, no predictive capabilities

**Market Gap Identified:**
No existing tool provides predictive analytics specifically trained on Sri Lankan audience behavior, creating a clear opportunity for regional specialization.

---

## 3. Technical Methodology

### 3.1 System Architecture
**Layered Architecture Pattern:**
- **Presentation Layer**: Web interface (Streamlit/HTML+CSS+JS)
- **Application Layer**: REST API (Flask)
- **Business Logic Layer**: ML models and data processing (Python)
- **Data Access Layer**: Database operations (SQLAlchemy)
- **Data Storage**: PostgreSQL database

### 3.2 Machine Learning Approach
**Model Selection (Research-Validated):**
- **Algorithm**: XGBoost (Extreme Gradient Boosting)
- **Rationale**: State-of-the-art performance on tabular data, robust to outliers, excellent feature importance analysis
- **Architecture**: Separate models for Shorts (≤60s) and Long-form (>60s) videos

**Feature Engineering Strategy:**
Based on AMPS and SMTPD research findings:
- **Early Engagement Features**: 24-hour view/like/comment metrics
- **Temporal Features**: publish_hour, day_of_week, is_weekend
- **Content Features**: title_length, tag_count, description_length, language
- **Channel Authority**: subscriber_count, video_count, channel_age
- **Engagement Ratios**: likes_per_view, comments_per_view

**Prediction Targets:**
- 24-hour view count
- 7-day view count  
- 30-day view count

### 3.3 Data Collection Strategy
**Phase 1: Historical Data Collection**
- **Target**: 100-200 curated Sri Lankan channels across all categories
- **Timeframe**: Videos from last 6-12 months
- **Method**: Efficient YouTube Data API v3 calls with quota optimization

**Phase 2: Active Monitoring**
- **Target**: New videos from monitored channels
- **Frequency**: Daily checks for new uploads, hourly tracking for first 7 days
- **Purpose**: Generate time-series data for model training

**Sri Lankan Channel Identification:**
- Manual curation of known Sri Lankan channels
- Country code verification via API metadata
- Language detection (Sinhala, Tamil, English) using langdetect library
- Keyword-based discovery with verification

### 3.4 Technology Stack
**Backend:**
- Python 3.9+, Flask, XGBoost, Scikit-learn, Pandas, NumPy
- YouTube Data API v3, SQLAlchemy, APScheduler

**Frontend:**
- Streamlit (primary), HTML/CSS/JavaScript (alternative)
- Plotly for interactive visualizations

**Database:**
- SQLite (development), PostgreSQL (production)

**DevOps:**
- Docker containerization, Git + GitHub, Heroku deployment

---

## 4. Team Structure & Responsibilities

### 4.1 Role Definitions
**Senevirathne S.M.P.U. - Data Lead & YouTube Specialist**
- YouTube Data API integration and management
- Sri Lankan channel identification and curation
- Data collection strategy implementation
- Exploratory Data Analysis (EDA)
- Data quality assurance and validation

**Sanjula N.G.K. - Backend & Model Lead**
- Machine learning model development and training
- Backend API development (Flask)
- Database design and implementation
- System architecture and DevOps
- Performance optimization and deployment

**Shaamma M.S. - Frontend & Documentation Lead**
- Web application user interface development
- Data visualization and dashboard creation
- Project documentation and reporting
- User experience design and testing
- Presentation preparation and delivery

### 4.2 Collaboration Framework
- **Team Meetings**: Twice weekly (Monday planning, Friday review)
- **Mentor Meetings**: Bi-weekly as per university schedule
- **Development Workflow**: Git feature branches with peer code review
- **Communication**: Shared documentation and regular progress updates

---

## 5. Project Timeline & Deliverables

### 5.1 10-Week Project Schedule

**Weeks 1-2: Foundation & Planning**
- Development environment setup and API integration
- Database schema design and implementation
- Project documentation framework establishment
- **Deliverables**: Project Feasibility Document, Project Schedule (Gantt Chart)

**Weeks 3-4: Data Collection & Infrastructure**
- Data collection pipeline implementation
- Historical data gathering (1000+ videos)
- Data quality validation and preprocessing
- **Deliverables**: System Requirements Specification, System Architecture Document

**Weeks 5-6: Model Development & Mid-Evaluation**
- Exploratory Data Analysis and feature engineering
- Machine learning model training and optimization
- Model evaluation and validation
- **Deliverables**: Mid-evaluation Prototype Demo, trained baseline models

**Weeks 7-8: System Integration & Testing**
- Backend API development and frontend integration
- End-to-end system testing and optimization
- User interface refinement
- **Deliverables**: Testing & Evaluation Document, integrated system

**Weeks 9-10: Deployment & Finalization**
- Cloud deployment and production configuration
- Final testing and documentation completion
- Presentation preparation and delivery
- **Deliverables**: Final Evaluation, Final Product Resources, Final Report

### 5.2 Key Milestones
- **Week 2**: Project foundation complete
- **Week 4**: Data pipeline operational (Mentor Meetup 1)
- **Week 6**: Working ML models (Mid-evaluation)
- **Week 8**: Integrated system (Mentor Meetup 2)
- **Week 10**: Production deployment (Final Evaluation, Mentor Meetup 3)

---

## 6. Success Metrics & Evaluation

### 6.1 Technical Performance Targets
**Primary Success Criteria:**
- **Model Accuracy**: MAPE < 30% for 7-day view forecasts (research-standard metric)
- **System Performance**: Predictions delivered within 30 seconds
- **Data Quality**: Successfully collect and process 5000+ videos from 100+ channels
- **System Reliability**: 95% uptime during testing period

**Evaluation Methodology:**
- **Cross-Validation**: 5-fold cross-validation for robust performance estimates
- **Temporal Validation**: Test on future data to simulate real-world usage
- **Category Analysis**: Performance evaluation across different content types
- **Baseline Comparison**: Compare against simple heuristic models

### 6.2 Academic Success Criteria
- **Documentation Quality**: Comprehensive technical and user documentation
- **Presentation Impact**: Successful final demonstration and academic presentation
- **Research Contribution**: Novel dataset and methodology for regional social media analytics
- **Code Quality**: Clean, maintainable, and well-documented codebase

### 6.3 Business Impact Potential
- **User Adoption**: Demonstrate practical value for Sri Lankan creators
- **Dataset Contribution**: Release research-grade dataset for academic use
- **Publication Opportunity**: Potential for academic paper submission
- **Industry Relevance**: Foundation for commercial social media analytics tools

---

## 7. Risk Management & Mitigation

### 7.1 Technical Risks
**High-Priority Risks:**
1. **YouTube API Quota Exhaustion**
   - **Mitigation**: Use 3 team member API keys (30,000 total units), implement efficient API patterns, cache responses
   - **Contingency**: Alternative data sources (Social Blade) if needed

2. **Model Performance Below Expectations**
   - **Mitigation**: Research-validated approach, focus on feature engineering, baseline model comparison
   - **Contingency**: Adjust success criteria or focus on specific video categories

3. **Data Quality Issues**
   - **Mitigation**: Comprehensive validation checks, multiple verification sources, automated quality monitoring
   - **Contingency**: Manual curation for critical datasets

### 7.2 Project Management Risks
**Medium-Priority Risks:**
1. **Team Coordination Challenges**
   - **Mitigation**: Docker for consistent environments, clear Git workflow, regular communication
   - **Contingency**: Designated integration lead and conflict resolution process

2. **Scope Creep**
   - **Mitigation**: Clearly defined MVP scope, regular scope reviews, feature prioritization framework
   - **Contingency**: Feature freeze and focus on core functionality

### 7.3 Risk Monitoring
- Weekly risk assessment during team meetings
- Clear escalation procedures for high-impact risks
- Detailed risk log with responses and outcomes

---

## 8. Innovation & Contribution

### 8.1 Technical Innovation
- **Regional Specialization**: First YouTube prediction model specifically trained on Sri Lankan data
- **Research Integration**: Application of cutting-edge social media analytics research
- **Multi-modal Approach**: Comprehensive feature engineering combining text, temporal, and engagement data
- **Temporal Alignment**: Time-synchronized predictions for improved accuracy

### 8.2 Academic Contribution
- **Novel Dataset**: Comprehensive Sri Lankan YouTube analytics dataset for research use
- **Methodology Validation**: Regional application of global social media prediction techniques
- **Open Source**: Transparent algorithms and reproducible research
- **Knowledge Transfer**: Bridge between academic research and practical application

### 8.3 Industry Impact
- **Market Gap**: Address unmet need in Sri Lankan digital content industry
- **Democratization**: Provide enterprise-level analytics to individual creators
- **Economic Impact**: Enable better content strategies and improved creator revenues
- **Foundation**: Establish groundwork for regional social media analytics industry

---

## 9. Resource Requirements & Budget

### 9.1 Technical Resources
**Development Infrastructure:**
- **Hardware**: Team laptops (existing) - Windows 11 and Ubuntu systems
- **Software**: Free and open-source tools (Python, Git, Docker)
- **APIs**: YouTube Data API v3 (free tier with quota management)
- **Hosting**: Free-tier cloud services (Heroku, PostgreSQL)

**Estimated Costs:**
- **Development**: $0 (utilizing free-tier services and existing hardware)
- **Deployment**: $0 (free-tier cloud hosting)
- **APIs**: $0 (within free quota limits with optimization)
- **Total Project Cost**: $0 (zero-cost MVP approach)

### 9.2 Human Resources
**Team Commitment:**
- **Total Effort**: 360 person-hours (10 hours/week/person × 3 people × 12 weeks)
- **Skill Development**: Significant learning opportunity in ML, web development, and data science
- **Mentorship**: Regular guidance from university faculty

---

## 10. Expected Outcomes & Future Potential

### 10.1 Immediate Deliverables
1. **Functional Web Application**: User-friendly interface for viewership prediction
2. **Trained ML Models**: Separate optimized models for Shorts and Long-form content
3. **Comprehensive Dataset**: 5000+ Sri Lankan YouTube videos with metadata and engagement metrics
4. **Technical Documentation**: Complete system documentation and user guides
5. **Academic Presentation**: Final project demonstration and report

### 10.2 Long-term Impact
**Academic Impact:**
- Research paper submission to relevant conferences
- Open-source dataset for academic community
- Methodology replication for other regional markets

**Industry Impact:**
- Foundation for commercial social media analytics tools
- Potential startup opportunity in regional digital marketing
- Collaboration opportunities with Sri Lankan media companies

**Social Impact:**
- Democratize access to advanced analytics for Sri Lankan creators
- Support growth of local digital content industry
- Contribute to Sri Lanka's digital economy development

### 10.3 Scalability Potential
**Geographic Expansion:**
- Methodology applicable to other South Asian markets
- Framework for country-specific social media analytics

**Platform Expansion:**
- Extension to TikTok, Instagram Reels, and other short-form platforms
- Multi-platform content strategy optimization

**Feature Enhancement:**
- Advanced content analysis (thumbnail, audio, transcript)
- Real-time trend detection and alert systems
- Competitive analysis and market intelligence tools

---

## 11. Conclusion

ViewTrendsSL represents a unique opportunity to bridge the gap between cutting-edge academic research and practical industry needs in the Sri Lankan digital content landscape. By leveraging recent breakthroughs in social media popularity prediction and focusing specifically on regional audience behavior, this project will deliver both immediate practical value and long-term research contributions.

The project's success is ensured through:
- **Strong Academic Foundation**: Grounded in peer-reviewed research and validated methodologies
- **Clear Technical Approach**: Research-backed technology choices and implementation strategy
- **Experienced Team**: Complementary skills and clear role definitions
- **Realistic Scope**: Achievable MVP with clear success criteria and risk mitigation
- **Significant Impact Potential**: Both academic and industry contributions

We are confident that ViewTrendsSL will not only meet the academic requirements of the CS3501 course but also establish a foundation for ongoing research and potential commercial development in the rapidly growing field of regional social media analytics.

---

**Project Repository**: https://github.com/L0rd008/ViewTrendsSL  
**Contact**: Available through university channels and project repository

*This proposal represents our commitment to delivering a high-quality, research-driven solution that addresses real-world needs while contributing to academic knowledge in the field of social media analytics.*
