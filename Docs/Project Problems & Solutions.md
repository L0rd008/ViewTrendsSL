# Project Problems & Solutions
## ViewTrendsSL: YouTube Viewership Forecasting System

**Document Version**: 1.0  
**Date**: August 6, 2025  
**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  

**Prepared by:**
- Senevirathne S.M.P.U. (220599M) - Data Lead
- Sanjula N.G.K. (220578A) - Backend & Model Lead  
- Shaamma M.S. (220602U) - Frontend & Documentation Lead

---

## Document Overview

This document serves as a comprehensive tracking system for all problems identified during the ViewTrendsSL project development, along with their corresponding solutions, implementation status, and ownership assignments. Problems are categorized by severity and project phase, with clear timelines for identification and resolution.

**Status Legend:**
- 🔴 **Critical** - Project blocker requiring immediate attention
- 🟡 **High** - Significant impact on timeline or quality
- 🟢 **Medium** - Manageable impact with planned solutions
- 🔵 **Low** - Minor issues or future considerations

---

## Table of Contents

- [Critical Problems (Project Blockers)](#critical-problems-project-blockers)
- [High Priority Problems](#high-priority-problems)
- [Medium Priority Problems](#medium-priority-problems)
- [Low Priority Problems](#low-priority-problems)
- [Future Considerations](#future-considerations)
- [Problem Resolution Tracking](#problem-resolution-tracking)
- [Lessons Learned](#lessons-learned)

---

## Critical Problems (Project Blockers)

### PROB-001: YouTube API Quota Catastrophe 🔴
**Identified**: August 6, 2025  
**Category**: Data Collection  
**Phase**: Week 1-4 (Data Infrastructure)  
**Owner**: Senevirathne S.M.P.U.

**Problem Description:**
Daily API quota limit of 10,000 units per key severely constrains data collection. A single search query costs 100 units, potentially exhausting quota in hours and halting data collection for 24 hours.

**Impact Assessment:**
- **Severity**: Critical - Could delay entire project timeline
- **Affected Components**: Data collection pipeline, model training dataset
- **Timeline Risk**: 2-3 week delay if not properly managed

**Solutions Identified:**
1. **Multi-Key Strategy** (Solution Date: August 6, 2025)
   - Use 3 team member API keys (30,000 units total daily)
   - Implement automatic key rotation in collection scripts
   - Monitor quota usage with automated alerts

2. **Efficient API Usage Pattern** (Solution Date: August 6, 2025)
   - Avoid expensive search.list calls (100 units each)
   - Use playlistItems.list for channel videos (1 unit per page)
   - Implement comprehensive response caching

3. **Rate Limiting Implementation** (Solution Date: August 6, 2025)
   - Add time.sleep(1) between API calls
   - Implement exponential backoff for rate limit errors
   - Queue-based request management system

**Implementation Status**: Planned for Week 1
**Dependencies**: Google Cloud API key setup for all team members
**Success Criteria**: Sustained data collection without quota exhaustion

---

### PROB-002: Sri Lankan Channel Identification Crisis 🔴
**Identified**: August 6, 2025  
**Category**: Data Quality  
**Phase**: Week 3-4 (Data Collection)  
**Owner**: Senevirathne S.M.P.U.

**Problem Description:**
Keyword-based approach for identifying Sri Lankan channels will capture irrelevant global content mentioning "Sri Lanka" while missing relevant Sri Lankan creators without explicit location indicators.

**Impact Assessment:**
- **Severity**: Critical - Affects model training data quality
- **Affected Components**: Dataset accuracy, model performance
- **Quality Risk**: Biased predictions due to contaminated training data

**Solutions Identified:**
1. **Multi-Factor Scoring System** (Solution Date: August 6, 2025)
   - Combine API country code (channel.snippet.country = "LK")
   - Language detection using langdetect library for Sinhala/Tamil content
   - Manual curation of "Gold Standard" seed list (50-100 verified channels)

2. **Confidence-Based Filtering** (Solution Date: August 6, 2025)
   - Implement scoring algorithm: Country code (40%) + Language (40%) + Manual verification (20%)
   - Set minimum confidence threshold (70%) for dataset inclusion
   - Regular manual review of edge cases

**Implementation Status**: Planned for Week 3
**Dependencies**: Language detection library integration, manual channel research
**Success Criteria**: >90% accuracy in Sri Lankan channel identification

---

### PROB-003: Data Leakage in Model Training 🔴
**Identified**: August 6, 2025  
**Category**: Machine Learning  
**Phase**: Week 5 (Model Development)  
**Owner**: Sanjula N.G.K.

**Problem Description:**
Risk of accidentally including future information (e.g., 24-hour view counts) as features to predict future performance, creating artificially high accuracy that fails in production.

**Impact Assessment:**
- **Severity**: Critical - Renders model useless for real predictions
- **Affected Components**: Model accuracy, system credibility
- **Business Risk**: Complete system failure in production environment

**Solutions Identified:**
1. **Time Zero Feature Set Definition** (Solution Date: August 6, 2025)
   - Strictly limit features to upload-time information only
   - Video features: title, description, tags, category, duration, is_short
   - Channel features: subscriber count, total videos, channel age
   - Temporal features: publish_day_of_week, publish_hour_of_day

2. **Feature Engineering Pipeline Validation** (Solution Date: August 6, 2025)
   - Implement automated checks for temporal consistency
   - Create separate feature sets for different prediction timeframes
   - Comprehensive testing with holdout validation sets

**Implementation Status**: Planned for Week 5
**Dependencies**: Clear feature engineering guidelines, validation framework
**Success Criteria**: Model performance validated on truly unseen data

---

## High Priority Problems

### PROB-004: Development Environment Inconsistency 🟡
**Identified**: August 6, 2025  
**Category**: Technical Infrastructure  
**Phase**: Week 1-2 (Setup)  
**Owner**: Sanjula N.G.K.

**Problem Description:**
Team members using different operating systems (Windows 11, Ubuntu 24.04) and Python versions may encounter library compatibility issues and environment-specific bugs.

**Impact Assessment:**
- **Severity**: High - Could cause significant development delays
- **Affected Components**: All development activities
- **Timeline Risk**: 1-2 week delay for environment debugging

**Solutions Identified:**
1. **Docker Containerization** (Solution Date: August 6, 2025)
   - Create comprehensive Dockerfile with exact Python version and dependencies
   - Implement docker-compose.yml for complete development environment
   - Standardize all development through containerized environment

2. **Requirements Management** (Solution Date: August 6, 2025)
   - Generate requirements.txt with exact version pinning
   - Regular synchronization of development environments
   - Automated environment validation scripts

**Implementation Status**: Planned for Week 1
**Dependencies**: Docker installation on all team machines
**Success Criteria**: Identical development environment across all team members

---

### PROB-005: Model Performance Uncertainty 🟡
**Identified**: August 6, 2025  
**Category**: Machine Learning  
**Phase**: Week 5-6 (Model Training)  
**Owner**: Sanjula N.G.K.

**Problem Description:**
Ambitious accuracy targets (85% accuracy / 15% MAPE) may be unrealistic for YouTube viewership prediction, especially with limited Sri Lankan data and algorithm volatility.

**Impact Assessment:**
- **Severity**: High - Could lead to project failure or scope reduction
- **Affected Components**: Core system value proposition
- **Academic Risk**: Insufficient performance for academic evaluation

**Solutions Identified:**
1. **Realistic Performance Targets** (Solution Date: August 6, 2025)
   - Adjust target to MAPE < 30% for 7-day predictions (academically acceptable)
   - Implement baseline models for performance comparison
   - Focus on feature engineering over algorithm complexity

2. **Multi-Model Strategy** (Solution Date: August 6, 2025)
   - Separate models for Shorts vs Long-form content
   - Category-specific model variations if needed
   - Ensemble methods for improved robustness

3. **Performance Monitoring Framework** (Solution Date: August 6, 2025)
   - Comprehensive evaluation metrics (MAPE, MAE, RMSE)
   - Cross-validation with temporal splits
   - Regular model performance tracking

**Implementation Status**: Planned for Week 5
**Dependencies**: Sufficient training data, evaluation framework
**Success Criteria**: Consistent MAPE < 30% on validation sets

---

### PROB-006: System Integration Complexity 🟡
**Identified**: August 6, 2025  
**Category**: System Architecture  
**Phase**: Week 7-8 (Integration & Testing)  
**Owner**: All Team Members

**Problem Description:**
Complex integration between data collection, ML models, Flask backend, and Streamlit frontend may create compatibility issues and performance bottlenecks.

**Impact Assessment:**
- **Severity**: High - Could prevent system completion
- **Affected Components**: End-to-end system functionality
- **Timeline Risk**: 1-2 week delay for integration debugging

**Solutions Identified:**
1. **Modular Development Approach** (Solution Date: August 6, 2025)
   - Clear API contracts between components
   - Independent testing of each module
   - Gradual integration with comprehensive testing

2. **Performance Optimization Strategy** (Solution Date: August 6, 2025)
   - Implement caching for API responses and predictions
   - Database query optimization with proper indexing
   - Asynchronous processing for long-running operations

3. **Integration Testing Framework** (Solution Date: August 6, 2025)
   - End-to-end testing scenarios
   - Load testing for concurrent users
   - Error handling and graceful degradation

**Implementation Status**: Planned for Week 7
**Dependencies**: Completed individual modules, testing framework
**Success Criteria**: Stable end-to-end system with <30 second response times

---

## Medium Priority Problems

### PROB-007: Database Performance Optimization 🟢
**Identified**: August 6, 2025  
**Category**: Database Management  
**Phase**: Week 4 (Database Implementation)  
**Owner**: Sanjula N.G.K.

**Problem Description:**
Large dataset (50K+ videos, 1M+ snapshots) may cause slow query performance without proper indexing and optimization strategies.

**Impact Assessment:**
- **Severity**: Medium - Affects user experience but not core functionality
- **Affected Components**: Data retrieval, prediction generation
- **Performance Risk**: Slow response times, poor user experience

**Solutions Identified:**
1. **Strategic Indexing** (Solution Date: August 6, 2025)
   - Composite index on (video_id, timestamp) for snapshots table
   - Foreign key indexes on channel_id, category_id
   - Full-text search indexes for title/description queries

2. **Query Optimization** (Solution Date: August 6, 2025)
   - Efficient SQLAlchemy query patterns
   - Database connection pooling
   - Query result caching for frequent requests

**Implementation Status**: Planned for Week 4
**Dependencies**: Database schema finalization
**Success Criteria**: Sub-second query response times for typical operations

---

### PROB-008: User Authentication Security 🟢
**Identified**: August 6, 2025  
**Category**: Security  
**Phase**: Week 6 (Backend Development)  
**Owner**: Sanjula N.G.K.

**Problem Description:**
Basic authentication system needs proper security measures including password hashing, session management, and protection against common attacks.

**Impact Assessment:**
- **Severity**: Medium - Security vulnerability but not project blocker
- **Affected Components**: User management, data protection
- **Security Risk**: Potential data breaches, unauthorized access

**Solutions Identified:**
1. **Secure Authentication Implementation** (Solution Date: August 6, 2025)
   - bcrypt password hashing with proper salt rounds
   - JWT-based session management with expiration
   - Input validation and SQL injection prevention

2. **Security Best Practices** (Solution Date: August 6, 2025)
   - HTTPS enforcement for all communications
   - Rate limiting for login attempts
   - Secure API key storage using environment variables

**Implementation Status**: Planned for Week 6
**Dependencies**: Flask-Login integration, security library setup
**Success Criteria**: Secure authentication passing basic penetration testing

---

### PROB-009: Data Validation Pipeline 🟢
**Identified**: August 6, 2025  
**Category**: Data Quality  
**Phase**: Week 4 (Data Processing)  
**Owner**: Senevirathne S.M.P.U.

**Problem Description:**
YouTube API responses may contain missing fields, disabled features (comments/likes), or malformed data that could crash processing pipelines.

**Impact Assessment:**
- **Severity**: Medium - Affects data quality but manageable
- **Affected Components**: Data collection, feature engineering
- **Quality Risk**: Incomplete datasets, processing failures

**Solutions Identified:**
1. **Defensive Data Processing** (Solution Date: August 6, 2025)
   - Safe dictionary access with .get() method and default values
   - Comprehensive error handling for API response variations
   - Data type validation and conversion

2. **Quality Indicators** (Solution Date: August 6, 2025)
   - Boolean features for disabled comments/likes
   - Data completeness scoring
   - Automated quality reports and alerts

**Implementation Status**: Planned for Week 4
**Dependencies**: Data collection scripts, error handling framework
**Success Criteria**: Robust processing of all API response variations

---

### PROB-010: Shorts vs Long-form Classification 🟢
**Identified**: August 6, 2025  
**Category**: Data Processing  
**Phase**: Week 4-5 (Feature Engineering)  
**Owner**: Senevirathne S.M.P.U.

**Problem Description:**
YouTube API doesn't provide explicit Shorts classification. Duration-based inference (≤60 seconds) may misclassify some content, affecting model training.

**Impact Assessment:**
- **Severity**: Medium - Affects model accuracy but not system functionality
- **Affected Components**: Model training, prediction accuracy
- **Accuracy Risk**: Contaminated training sets for both content types

**Solutions Identified:**
1. **Multi-Factor Classification** (Solution Date: August 6, 2025)
   - Primary rule: duration ≤ 61 seconds
   - Secondary validation: aspect ratio if available (height/width > 1)
   - Manual verification for edge cases

2. **Classification Confidence Tracking** (Solution Date: August 6, 2025)
   - Confidence scores for classification decisions
   - Regular manual review of borderline cases
   - Model performance tracking by content type

**Implementation Status**: Planned for Week 4
**Dependencies**: Duration parsing implementation, aspect ratio data availability
**Success Criteria**: >95% accuracy in Shorts vs Long-form classification

---

## Low Priority Problems

### PROB-011: UI/UX Optimization 🔵
**Identified**: August 6, 2025  
**Category**: User Interface  
**Phase**: Week 7-8 (Frontend Development)  
**Owner**: Shaamma M.S.

**Problem Description:**
Streamlit default styling may not provide optimal user experience for professional presentation and mobile responsiveness.

**Impact Assessment:**
- **Severity**: Low - Cosmetic issue not affecting core functionality
- **Affected Components**: User interface, user experience
- **Presentation Risk**: Less professional appearance for academic evaluation

**Solutions Identified:**
1. **Custom Styling** (Solution Date: August 6, 2025)
   - Custom CSS for improved visual design
   - Responsive layout for mobile compatibility
   - Professional color scheme and typography

2. **User Experience Enhancements** (Solution Date: August 6, 2025)
   - Loading indicators for long operations
   - Clear error messages and user guidance
   - Intuitive navigation and workflow

**Implementation Status**: Planned for Week 7
**Dependencies**: Streamlit customization capabilities
**Success Criteria**: Professional appearance suitable for academic presentation

---

### PROB-012: Documentation Completeness 🔵
**Identified**: August 6, 2025  
**Category**: Documentation  
**Phase**: Week 9-10 (Final Documentation)  
**Owner**: Shaamma M.S.

**Problem Description:**
Comprehensive documentation required for academic evaluation, future maintenance, and open-source contribution may be time-consuming to complete.

**Impact Assessment:**
- **Severity**: Low - Important for evaluation but not system functionality
- **Affected Components**: Academic assessment, future maintenance
- **Academic Risk**: Reduced evaluation scores for incomplete documentation

**Solutions Identified:**
1. **Continuous Documentation** (Solution Date: August 6, 2025)
   - Document components during development
   - Automated documentation generation where possible
   - Regular documentation review and updates

2. **Documentation Standards** (Solution Date: August 6, 2025)
   - Consistent formatting and structure
   - Code comments and docstrings
   - User guides and API documentation

**Implementation Status**: Ongoing throughout project
**Dependencies**: Development progress, documentation templates
**Success Criteria**: Complete documentation meeting academic standards

---

## Future Considerations

### FUTURE-001: Scalability Planning
**Identified**: August 6, 2025  
**Category**: System Architecture  
**Priority**: Future Enhancement

**Consideration Description:**
Current architecture designed for MVP scale (100 concurrent users). Future growth requires horizontal scaling, load balancing, and distributed processing capabilities.

**Potential Solutions:**
- Microservices architecture migration
- Container orchestration with Kubernetes
- Database sharding and read replicas
- CDN integration for static assets

---

### FUTURE-002: Advanced Feature Integration
**Identified**: August 6, 2025  
**Category**: Machine Learning  
**Priority**: Version 2.0

**Consideration Description:**
Integration of thumbnail analysis, audio sentiment analysis, and transcript processing could significantly improve prediction accuracy.

**Potential Solutions:**
- Computer vision models for thumbnail analysis
- NLP models for content sentiment analysis
- Multi-modal machine learning approaches
- Real-time content analysis pipelines

---

### FUTURE-003: Regional Expansion
**Identified**: August 6, 2025  
**Category**: Business Development  
**Priority**: Long-term Growth

**Consideration Description:**
Expansion to other South Asian markets (India, Bangladesh, Pakistan) requires localized models and cultural understanding.

**Potential Solutions:**
- Multi-region data collection strategies
- Localized model training approaches
- Cultural context integration
- Regional partnership development

---

## Problem Resolution Tracking

### Weekly Problem Review Schedule

| Week | Focus Areas | Review Date | Responsible |
|------|-------------|-------------|-------------|
| Week 1 | PROB-001, PROB-004 | Aug 30, 2025 | All Team |
| Week 2 | Environment Setup Issues | Sep 6, 2025 | Sanjula |
| Week 3 | PROB-002, Data Quality | Sep 13, 2025 | Senevirathne |
| Week 4 | PROB-007, PROB-009, PROB-010 | Sep 20, 2025 | Senevirathne + Sanjula |
| Week 5 | PROB-003, PROB-005 | Sep 27, 2025 | Sanjula |
| Week 6 | PROB-008, Backend Issues | Oct 4, 2025 | Sanjula |
| Week 7 | PROB-006, PROB-011 | Oct 11, 2025 | All Team |
| Week 8 | Integration & Testing Issues | Oct 18, 2025 | All Team |
| Week 9 | Deployment & Performance | Oct 25, 2025 | All Team |
| Week 10 | PROB-012, Final Issues | Nov 1, 2025 | Shaamma |

### Problem Escalation Protocol

**Level 1 - Team Resolution** (0-2 days)
- Team member attempts resolution using documented solutions
- Consult with relevant team member expertise
- Update problem status and document attempts

**Level 2 - Team Collaboration** (2-5 days)
- Involve entire team in problem-solving session
- Consider alternative approaches and scope adjustments
- Document lessons learned and update solutions

**Level 3 - Mentor Consultation** (5+ days)
- Escalate to project mentor for guidance
- Consider external resources or expert consultation
- Evaluate impact on project timeline and scope

### Success Metrics

**Problem Resolution Efficiency:**
- Target: 80% of problems resolved within planned timeframe
- Critical problems resolved within 48 hours of identification
- No more than 2 critical problems active simultaneously

**Quality Metrics:**
- Solution effectiveness rate >90%
- Problem recurrence rate <10%
- Team satisfaction with problem resolution process >80%

---

## Lessons Learned

### Key Insights from Problem Analysis

1. **Proactive Problem Identification**: Early identification of potential issues through comprehensive planning significantly reduces project risk.

2. **Multi-layered Solutions**: Most critical problems require multiple complementary solutions rather than single fixes.

3. **Team Ownership**: Clear ownership assignment for problems ensures accountability and faster resolution.

4. **Documentation Value**: Comprehensive problem documentation enables faster resolution of similar issues.

5. **Risk Mitigation**: Having backup solutions and contingency plans is essential for critical project components.

### Best Practices Established

1. **Regular Problem Review**: Weekly problem assessment prevents issues from becoming critical.

2. **Solution Validation**: All solutions must be tested and validated before implementation.

3. **Knowledge Sharing**: Problem resolution knowledge must be shared across the entire team.

4. **Continuous Improvement**: Problem resolution processes should be continuously refined based on experience.

5. **Stakeholder Communication**: Regular updates on problem status maintain project transparency.

---

**Document Status**: Active - Updated Weekly  
**Last Review**: August 6, 2025  
**Next Review**: August 13, 2025  
**Review Frequency**: Weekly during development, monthly post-deployment

---

*This document serves as a living record of project challenges and solutions. All team members are responsible for updating problem status and contributing to solution development. Regular review and updates ensure the document remains current and valuable for project success.*
