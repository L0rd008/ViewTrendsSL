# ViewTrendsSL: YouTube Viewership Forecasting System
## Software Requirements Specification (SRS)

**Document Version**: 1.0  
**Date**: August 6, 2025  
**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  

**Prepared by:**
- Senevirathne S.M.P.U. (220599M) - Data Lead
- Sanjula N.G.K. (220578A) - Backend & Model Lead  
- Shaamma M.S. (220602U) - Frontend & Documentation Lead

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Other Requirements](#6-other-requirements)
7. [Appendices](#7-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive description of the ViewTrendsSL system - a machine learning-powered web application for predicting YouTube video viewership specifically for Sri Lankan audiences. This document serves as the definitive specification for system development, testing, and evaluation.

**Intended Audience:**
- Development team members
- Project mentors and academic evaluators
- System testers and quality assurance personnel
- Future maintainers and contributors
- Academic researchers and stakeholders

**Document Scope:**
This SRS covers the complete ViewTrendsSL system including:
- Data collection and processing subsystem
- Machine learning prediction engine
- Web-based user interface
- Database management system
- API services and external integrations

### 1.2 Product Scope

**Product Overview:**
ViewTrendsSL is a specialized analytics platform that addresses the critical gap in region-specific YouTube viewership prediction tools. The system leverages cutting-edge machine learning research to provide accurate forecasting capabilities tailored to Sri Lankan audience behavior and content consumption patterns.

**Primary Objectives:**
- Provide accurate viewership predictions for YouTube videos at 24-hour, 7-day, and 30-day intervals
- Deliver region-specific insights based on Sri Lankan audience data
- Offer an intuitive web-based interface for content creators and marketers
- Establish a foundation for academic research in regional social media analytics

**Key Benefits:**
- **For Content Creators**: Data-driven content strategy optimization
- **For Marketers**: Improved campaign planning and budget allocation
- **For Researchers**: Novel dataset and methodology for regional analytics
- **For Industry**: Foundation for specialized social media tools

### 1.3 Definitions, Acronyms, and Abbreviations

**Technical Terms:**
- **API (Application Programming Interface)**: Set of protocols enabling software component communication
- **ETL (Extract, Transform, Load)**: Data processing pipeline for collection, cleaning, and storage
- **Feature Engineering**: Process of creating predictive variables from raw data
- **MAPE (Mean Absolute Percentage Error)**: Prediction accuracy metric expressed as percentage
- **MAE (Mean Absolute Error)**: Average magnitude of prediction errors
- **RMSE (Root Mean Squared Error)**: Standard deviation of prediction residuals
- **SRC (Spearman Rank Correlation)**: Statistical measure of monotonic relationship strength
- **XGBoost**: Extreme Gradient Boosting machine learning algorithm
- **Viewership Curve**: Temporal visualization of video view count progression

**Domain-Specific Terms:**
- **Shorts**: YouTube videos with duration ≤ 60 seconds
- **Long-form**: YouTube videos with duration > 60 seconds
- **Channel Authority**: Composite metric of channel influence and reach
- **Early Engagement**: User interactions within first 24 hours of video publication
- **Temporal Alignment**: Time-synchronized prediction methodology
- **Growth Velocity**: Rate of viewership increase during initial publication period

**System Components:**
- **Data Collector**: Automated YouTube API integration module
- **Feature Extractor**: Data preprocessing and feature engineering component
- **Prediction Engine**: Machine learning model inference system
- **Web Dashboard**: User interface for prediction requests and visualization
- **Database Manager**: Data storage and retrieval system

### 1.4 References

**Academic Literature:**
1. "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms" - Journal of Retailing and Consumer Services (2024)
2. "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity" - arXiv:2503.04446v1 (2025)
3. "XGBoost: A Scalable Tree Boosting System" - KDD 2016
4. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications

**Technical Documentation:**
- YouTube Data API v3 Documentation: https://developers.google.com/youtube/v3
- Flask Web Framework Documentation: https://flask.palletsprojects.com/
- XGBoost Documentation: https://xgboost.readthedocs.io/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

**Development Standards:**
- PEP 8 - Style Guide for Python Code
- REST API Design Guidelines
- Web Content Accessibility Guidelines (WCAG) 2.1

### 1.5 Overview

This SRS document is organized into seven main sections:
- **Section 1**: Introduction and document context
- **Section 2**: Overall system description and constraints
- **Section 3**: Detailed functional requirements and use cases
- **Section 4**: External interface specifications
- **Section 5**: Non-functional requirements and quality attributes
- **Section 6**: Additional requirements and constraints
- **Section 7**: Supporting diagrams and appendices

---

## 2. Overall Description

### 2.1 Product Perspective

**System Context:**
ViewTrendsSL operates as an independent web-based system with external dependencies on YouTube Data API v3 and cloud hosting infrastructure. The system follows a layered architecture pattern with clear separation between presentation, business logic, and data layers.

**System Interfaces:**
- **External API Integration**: YouTube Data API v3 for video and channel metadata
- **Web Browser Interface**: Cross-platform web application accessible via standard browsers
- **Database Interface**: PostgreSQL for production data storage
- **Cloud Hosting**: Containerized deployment on cloud platforms

**Future Integration Potential:**
- Browser extension development for direct YouTube integration
- Mobile application development for enhanced accessibility
- Third-party analytics platform integration
- Social media management tool integration

### 2.2 Product Functions

**Core System Functions:**

1. **Data Collection and Management**
   - Automated YouTube metadata harvesting
   - Real-time data quality validation
   - Efficient API quota management
   - Historical data processing and storage

2. **Machine Learning Pipeline**
   - Feature engineering from raw video metadata
   - Separate model training for Shorts and Long-form content
   - Model evaluation and performance monitoring
   - Prediction generation with confidence intervals

3. **User Interface and Visualization**
   - Intuitive video URL input interface
   - Interactive prediction result visualization
   - User authentication and session management
   - Responsive design for multiple device types

4. **System Administration**
   - Automated data pipeline monitoring
   - System performance tracking
   - Error logging and alerting
   - Database backup and recovery

### 2.3 User Classes and Characteristics

**Primary User Classes:**

1. **Content Creators (Primary Users)**
   - **Profile**: Individual YouTubers, influencers, and independent creators
   - **Technical Expertise**: Basic to intermediate computer skills
   - **Usage Patterns**: Occasional use for strategic content planning
   - **Key Needs**: Simple interface, accurate predictions, actionable insights

2. **Digital Marketers (Secondary Users)**
   - **Profile**: Marketing professionals and agency personnel
   - **Technical Expertise**: Intermediate to advanced analytical skills
   - **Usage Patterns**: Regular use for campaign planning and optimization
   - **Key Needs**: Detailed analytics, export capabilities, trend analysis

3. **Media Companies (Secondary Users)**
   - **Profile**: Production houses, media agencies, and content networks
   - **Technical Expertise**: Advanced technical and analytical capabilities
   - **Usage Patterns**: Intensive use for portfolio optimization
   - **Key Needs**: Bulk analysis, API access, custom reporting

4. **Academic Researchers (Tertiary Users)**
   - **Profile**: University researchers and data scientists
   - **Technical Expertise**: Advanced technical and statistical knowledge
   - **Usage Patterns**: Research-focused usage with dataset access
   - **Key Needs**: Data export, methodology transparency, reproducibility

### 2.4 Operating Environment

**Client-Side Requirements:**
- **Web Browser**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **JavaScript**: Enabled for interactive features
- **Screen Resolution**: Minimum 1024x768, optimized for 1920x1080
- **Internet Connection**: Stable broadband connection (minimum 1 Mbps)

**Server-Side Environment:**
- **Operating System**: Linux-based cloud hosting (Ubuntu 20.04 LTS or equivalent)
- **Runtime Environment**: Python 3.9+ with virtual environment
- **Web Server**: Gunicorn WSGI server with Nginx reverse proxy
- **Database**: PostgreSQL 13+ with connection pooling
- **Containerization**: Docker with Docker Compose for orchestration

**Development Environment:**
- **Version Control**: Git with GitHub repository
- **Development OS**: Windows 11 and Ubuntu 24.04 (team compatibility)
- **IDE**: Visual Studio Code with Python extensions
- **Testing**: pytest framework with coverage reporting

### 2.5 Design and Implementation Constraints

**Technical Constraints:**
- **API Limitations**: YouTube Data API v3 quota restrictions (10,000 units/day per key)
- **Processing Power**: Limited computational resources for model training
- **Storage Capacity**: Database size limitations on free-tier hosting
- **Network Bandwidth**: Potential latency issues for real-time predictions

**Development Constraints:**
- **Timeline**: 10-week development period with academic milestones
- **Team Size**: Three-person development team with distributed responsibilities
- **Budget**: Zero-cost approach using free-tier services and open-source tools
- **Platform Compatibility**: Cross-platform development across Windows and Linux

**Regulatory Constraints:**
- **Data Privacy**: Compliance with YouTube API Terms of Service
- **Academic Ethics**: University research ethics guidelines
- **Open Source**: GPL-compatible licensing for academic use

**Performance Constraints:**
- **Response Time**: Predictions must be delivered within 30 seconds
- **Concurrent Users**: Support for minimum 10 simultaneous users
- **Data Processing**: Handle 1000+ video predictions per hour
- **Model Accuracy**: Achieve MAPE < 30% for 7-day forecasts

### 2.6 Assumptions and Dependencies

**System Assumptions:**
- YouTube Data API v3 remains stable and accessible throughout development
- Sri Lankan YouTube content maintains consistent metadata patterns
- User internet connections support real-time web application usage
- Cloud hosting services maintain reliable uptime and performance

**External Dependencies:**
- **YouTube Data API v3**: Primary data source for video and channel metadata
- **Cloud Hosting Platform**: Heroku or equivalent for application deployment
- **PostgreSQL Service**: Database hosting with backup capabilities
- **Python Ecosystem**: Stability of core libraries (Flask, XGBoost, Pandas)

**Data Dependencies:**
- **Channel Identification**: Availability of Sri Lankan channel metadata
- **Historical Data**: Access to 6-12 months of video performance data
- **API Quota**: Sufficient quota allocation for initial data collection
- **Data Quality**: Consistent and accurate metadata from YouTube API

---

## 3. System Features

### 3.1 User Authentication and Management

**Feature ID**: F001  
**Priority**: High  
**Risk**: Medium  

**Description:**
Secure user registration, authentication, and session management system enabling personalized access to prediction services.

**Functional Requirements:**

**FR-001**: User Registration
- System shall provide user registration with email and password
- System shall validate email format and password strength (minimum 8 characters, mixed case, numbers)
- System shall send email verification for account activation
- System shall prevent duplicate email registrations

**FR-002**: User Authentication
- System shall authenticate users via email/password combination
- System shall implement secure password hashing using bcrypt algorithm
- System shall maintain user sessions with automatic timeout (2 hours)
- System shall provide secure logout functionality

**FR-003**: Password Management
- System shall provide password reset functionality via email
- System shall enforce password complexity requirements
- System shall prevent password reuse for last 3 passwords
- System shall implement account lockout after 5 failed login attempts

**Input/Output Specifications:**
- **Input**: Email address, password, confirmation password
- **Output**: Authentication token, user session, success/error messages
- **Data Validation**: Email format, password complexity, CSRF protection

### 3.2 Video Prediction Engine

**Feature ID**: F002  
**Priority**: Critical  
**Risk**: High  

**Description:**
Core machine learning system that generates viewership predictions for YouTube videos based on metadata analysis and trained models.

**Functional Requirements:**

**FR-004**: Video URL Processing
- System shall accept YouTube video URLs in standard formats
- System shall extract video ID from various URL formats (youtube.com, youtu.be, mobile links)
- System shall validate video accessibility and public status
- System shall retrieve video metadata via YouTube Data API v3

**FR-005**: Feature Extraction
- System shall extract temporal features (publish_hour, day_of_week, is_weekend)
- System shall calculate content features (title_length, tag_count, description_length)
- System shall determine video type (Shorts ≤60s vs Long-form >60s)
- System shall retrieve channel authority metrics (subscriber_count, video_count)

**FR-006**: Model Inference
- System shall select appropriate model based on video type (Shorts/Long-form)
- System shall generate predictions for 24-hour, 7-day, and 30-day intervals
- System shall calculate prediction confidence intervals
- System shall handle edge cases and provide fallback predictions

**FR-007**: Prediction Validation
- System shall validate prediction reasonableness against historical patterns
- System shall flag potentially unreliable predictions
- System shall provide prediction accuracy indicators
- System shall log prediction requests for model improvement

**Input/Output Specifications:**
- **Input**: YouTube video URL, prediction timeframes
- **Output**: Predicted view counts, confidence intervals, video metadata
- **Performance**: Response time < 30 seconds, accuracy MAPE < 30%

### 3.3 Data Visualization Dashboard

**Feature ID**: F003  
**Priority**: High  
**Risk**: Medium  

**Description:**
Interactive web interface for displaying prediction results, video metadata, and analytical insights through charts and visualizations.

**Functional Requirements:**

**FR-008**: Prediction Results Display
- System shall display video thumbnail, title, and basic metadata
- System shall generate interactive line chart showing predicted viewership curve
- System shall highlight key prediction milestones (24h, 7d, 30d)
- System shall provide downloadable prediction summary

**FR-009**: Interactive Visualizations
- System shall enable chart zoom and pan functionality
- System shall provide hover tooltips with detailed information
- System shall allow timeframe selection for prediction display
- System shall support chart export in PNG/SVG formats

**FR-010**: Comparative Analysis
- System shall enable comparison between multiple video predictions
- System shall display category-based performance benchmarks
- System shall show channel performance context
- System shall provide trend analysis insights

**Input/Output Specifications:**
- **Input**: Prediction data, user interaction events
- **Output**: Interactive charts, downloadable reports, visual insights
- **Responsiveness**: Support for desktop, tablet, and mobile devices

### 3.4 Data Collection and Management

**Feature ID**: F004  
**Priority**: Critical  
**Risk**: High  

**Description:**
Automated system for collecting, processing, and storing YouTube video and channel data for model training and system operation.

**Functional Requirements:**

**FR-011**: Automated Data Collection
- System shall collect video metadata from curated Sri Lankan channels
- System shall implement efficient API quota management across multiple keys
- System shall perform daily data collection with error handling
- System shall validate and clean collected data automatically

**FR-012**: Data Storage and Retrieval
- System shall store video metadata in normalized database schema
- System shall implement efficient indexing for fast query performance
- System shall maintain data integrity with foreign key constraints
- System shall provide data backup and recovery mechanisms

**FR-013**: Data Quality Assurance
- System shall validate data completeness and accuracy
- System shall detect and handle missing or corrupted data
- System shall implement data deduplication mechanisms
- System shall generate data quality reports

**Input/Output Specifications:**
- **Input**: YouTube API responses, channel lists, configuration parameters
- **Output**: Structured database records, quality reports, error logs
- **Performance**: Process 1000+ videos per hour, 99.9% data accuracy

### 3.5 System Administration and Monitoring

**Feature ID**: F005  
**Priority**: Medium  
**Risk**: Low  

**Description:**
Administrative interface and monitoring system for system health tracking, performance optimization, and maintenance operations.

**Functional Requirements:**

**FR-014**: System Health Monitoring
- System shall monitor API quota usage and alert on threshold breach
- System shall track system performance metrics (response time, error rate)
- System shall log all system events with appropriate severity levels
- System shall provide automated alerting for critical system issues

**FR-015**: Performance Analytics
- System shall track user engagement and usage patterns
- System shall monitor prediction accuracy over time
- System shall generate system performance reports
- System shall identify and alert on performance degradation

**FR-016**: Maintenance Operations
- System shall provide database backup and restore functionality
- System shall support model retraining and deployment
- System shall enable configuration updates without system restart
- System shall provide system status dashboard for administrators

**Input/Output Specifications:**
- **Input**: System metrics, configuration changes, maintenance commands
- **Output**: Status reports, alerts, performance dashboards
- **Availability**: 24/7 monitoring with 99.5% uptime target

---

## 4. External Interface Requirements

### 4.1 User Interfaces

**UI-001: Login/Registration Interface**
- **Description**: Clean, professional authentication interface
- **Layout**: Centered form with ViewTrendsSL branding
- **Elements**: Email field, password field, login/register buttons, forgot password link
- **Validation**: Real-time form validation with clear error messages
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation support

**UI-002: Main Dashboard Interface**
- **Description**: Primary user interface for video URL input and prediction display
- **Layout**: Header with navigation, central input area, results section below
- **Elements**: 
  - Prominent URL input field with placeholder text
  - "Generate Prediction" button with loading state
  - Video metadata display area
  - Interactive prediction chart container
- **Responsiveness**: Adaptive layout for desktop (1920x1080), tablet (768x1024), mobile (375x667)

**UI-003: Prediction Results Interface**
- **Description**: Comprehensive display of prediction results and analytics
- **Layout**: Split layout with video info sidebar and main chart area
- **Elements**:
  - Video thumbnail and metadata panel
  - Interactive line chart with prediction curve
  - Key metrics summary (24h, 7d, 30d predictions)
  - Export and share functionality
- **Interactivity**: Chart zoom, hover tooltips, timeframe selection

**UI Design Standards:**
- **Color Scheme**: Professional blue/white theme with red YouTube accents
- **Typography**: Roboto font family for consistency with Google Material Design
- **Icons**: Material Design icon set for consistency
- **Loading States**: Skeleton screens and progress indicators
- **Error Handling**: User-friendly error messages with suggested actions

### 4.2 Hardware Interfaces

**Client Hardware Requirements:**
- **Minimum RAM**: 4GB for smooth browser operation
- **Storage**: 100MB browser cache for optimal performance
- **Network**: Broadband internet connection (minimum 1 Mbps)
- **Display**: Minimum 1024x768 resolution, optimized for 1920x1080

**Server Hardware Specifications:**
- **CPU**: Minimum 2 vCPU cores for concurrent request handling
- **RAM**: 4GB minimum, 8GB recommended for model inference
- **Storage**: 20GB SSD for database and application files
- **Network**: High-speed internet connection for API calls and user requests

### 4.3 Software Interfaces

**SI-001: YouTube Data API v3 Interface**
- **Purpose**: Primary data source for video and channel metadata
- **Protocol**: HTTPS REST API
- **Authentication**: API key-based authentication
- **Rate Limiting**: 10,000 units per day per API key
- **Data Format**: JSON responses with structured metadata
- **Error Handling**: Comprehensive error code handling and retry logic

**SI-002: Database Interface**
- **Database System**: PostgreSQL 13+
- **Connection**: SQLAlchemy ORM with connection pooling
- **Schema**: Normalized relational schema with foreign key constraints
- **Backup**: Automated daily backups with point-in-time recovery
- **Performance**: Indexed queries with sub-second response times

**SI-003: Machine Learning Model Interface**
- **Model Format**: Serialized XGBoost models (.pkl files)
- **Loading**: Models loaded at application startup
- **Inference**: Real-time prediction generation
- **Versioning**: Model version tracking and rollback capability
- **Performance**: Prediction generation within 5 seconds

### 4.4 Communication Interfaces

**CI-001: HTTP/HTTPS Protocol**
- **Protocol**: HTTPS for all client-server communication
- **Security**: TLS 1.3 encryption with valid SSL certificates
- **Methods**: GET, POST, PUT, DELETE for RESTful API operations
- **Headers**: Standard HTTP headers with CORS support
- **Status Codes**: Comprehensive HTTP status code implementation

**CI-002: REST API Interface**
- **Base URL**: https://viewtrendssl.herokuapp.com/api/v1
- **Authentication**: JWT token-based authentication
- **Content Type**: JSON for request/response bodies
- **Rate Limiting**: 100 requests per minute per user
- **Documentation**: OpenAPI 3.0 specification with interactive docs

**API Endpoints:**
```
POST /api/v1/auth/login          # User authentication
POST /api/v1/auth/register       # User registration
POST /api/v1/predict             # Generate video prediction
GET  /api/v1/user/profile        # User profile information
GET  /api/v1/system/health       # System health check
```

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

**PR-001: Response Time Requirements**
- **Prediction Generation**: Maximum 30 seconds end-to-end response time
- **Page Load Time**: Maximum 3 seconds for initial page load
- **API Response Time**: Maximum 5 seconds for standard API calls
- **Database Query Time**: Maximum 1 second for standard queries

**PR-002: Throughput Requirements**
- **Concurrent Users**: Support minimum 10 simultaneous users
- **Prediction Volume**: Process 100+ predictions per hour
- **Data Processing**: Handle 1000+ video metadata records per hour
- **API Calls**: Efficient quota usage with batch processing where possible

**PR-003: Scalability Requirements**
- **User Growth**: Architecture supports scaling to 100+ concurrent users
- **Data Volume**: Database design supports millions of video records
- **Model Performance**: Prediction accuracy maintained with increased data volume
- **Infrastructure**: Containerized deployment for horizontal scaling

### 5.2 Safety Requirements

**SR-001: Data Protection**
- System shall implement secure data storage with encryption at rest
- System shall protect user passwords with bcrypt hashing (cost factor 12)
- System shall sanitize all user inputs to prevent injection attacks
- System shall implement secure session management with CSRF protection

**SR-002: API Security**
- System shall protect API keys using environment variables
- System shall implement rate limiting to prevent API abuse
- System shall validate all external API responses before processing
- System shall implement circuit breaker pattern for external service failures

**SR-003: System Reliability**
- System shall implement graceful error handling for all failure scenarios
- System shall provide automatic recovery from transient failures
- System shall maintain system stability under high load conditions
- System shall implement comprehensive logging for security monitoring

### 5.3 Security Requirements

**SEC-001: Authentication and Authorization**
- System shall implement secure user authentication with password complexity requirements
- System shall enforce session timeout after 2 hours of inactivity
- System shall implement account lockout after 5 failed login attempts
- System shall provide secure password reset functionality

**SEC-002: Data Security**
- System shall encrypt all data transmission using HTTPS/TLS 1.3
- System shall implement input validation and sanitization for all user inputs
- System shall protect against common web vulnerabilities (OWASP Top 10)
- System shall implement secure API key management and rotation

**SEC-003: Privacy Protection**
- System shall comply with YouTube API Terms of Service for data usage
- System shall implement user data privacy controls
- System shall provide clear privacy policy and terms of service
- System shall enable user data deletion upon request

### 5.4 Software Quality Attributes

**QA-001: Reliability**
- **Availability**: 99.5% uptime during operational hours
- **Mean Time Between Failures (MTBF)**: Minimum 720 hours
- **Mean Time To Recovery (MTTR)**: Maximum 4 hours
- **Error Rate**: Less than 1% of requests result in system errors

**QA-002: Usability**
- **Learning Curve**: New users can generate predictions within 5 minutes
- **Task Completion Rate**: 95% success rate for core prediction workflow
- **User Satisfaction**: Target satisfaction score of 4.0/5.0
- **Accessibility**: WCAG 2.1 AA compliance for inclusive design

**QA-003: Maintainability**
- **Code Quality**: Minimum 80% code coverage with automated tests
- **Documentation**: Comprehensive inline documentation and API docs
- **Modularity**: Clear separation of concerns with modular architecture
- **Deployment**: Automated deployment pipeline with rollback capability

**QA-004: Portability**
- **Browser Compatibility**: Support for Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Operating System**: Cross-platform web application (Windows, macOS, Linux)
- **Mobile Responsiveness**: Functional interface on mobile devices
- **Containerization**: Docker-based deployment for environment consistency

---

## 6. Other Requirements

### 6.1 Legal Requirements

**LR-001: Intellectual Property**
- System shall comply with YouTube Data API Terms of Service
- System shall respect copyright and intellectual property rights
- System shall implement proper attribution for third-party libraries
- System shall use GPL-compatible licensing for open-source distribution

**LR-002: Data Usage Compliance**
- System shall not store or redistribute raw YouTube data beyond API terms
- System shall implement data retention policies in compliance with regulations
- System shall provide user data deletion capabilities
- System shall maintain audit logs for compliance verification

**LR-003: Academic Ethics**
- System shall comply with University of Moratuwa research ethics guidelines
- System shall ensure transparent methodology for academic reproducibility
- System shall provide proper citation and attribution for research sources
- System shall enable open-source contribution for academic community

### 6.2 Standards Compliance

**SC-001: Development Standards**
- **Code Style**: PEP 8 compliance for all Python code
- **API Design**: RESTful API design principles
- **Database Design**: Third Normal Form (3NF) for relational schema
- **Version Control**: Git workflow with feature branches and code review

**SC-002: Web Standards**
- **HTML/CSS**: W3C standards compliance
- **JavaScript**: ES6+ standards with modern browser support
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Google PageSpeed Insights score > 90

**SC-003: Security Standards**
- **OWASP**: Compliance with OWASP Top 10 security guidelines
- **Encryption**: Industry-standard encryption algorithms (AES-256, RSA-2048)
- **Authentication**: OAuth 2.0 compatible authentication framework
- **Data Protection**: GDPR-inspired privacy protection measures

### 6.3 Business Rules

**BR-001: User Access Rules**
- Free tier users limited to 10 predictions per day
- Registered users receive higher prediction quotas
- System administrators have unrestricted access to all features
- Guest users can view demo predictions without registration

**BR-002: Data Processing Rules**
- Only public YouTube videos are processed for predictions
- Videos must be accessible via YouTube Data API v3
- Predictions are generated only for videos with sufficient metadata
- System prioritizes Sri Lankan content but supports international videos

**BR-003: Model Performance Rules**
- Models are retrained monthly with new data
- Prediction accuracy is monitored and reported
- Models with accuracy below threshold are flagged for review
- System provides confidence indicators for all predictions

### 6.4 Database Requirements

**DB-001: Data Storage Requirements**
- **Primary Database**: PostgreSQL 13+ with ACID compliance
- **Backup Strategy**: Daily automated backups with 30-day retention
- **Data Integrity**: Foreign key constraints and data validation
- **Performance**: Indexed queries with sub-second response times

**DB-002: Schema Requirements**
```sql
-- Core database schema
CREATE TABLE channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    subscriber_count INTEGER,
    video_count INTEGER,
    country VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) REFERENCES videos(video_id),
    timestamp TIMESTAMP NOT NULL,
    view_count BIGINT,
    like_count INTEGER,
    comment_count INTEGER,
    INDEX(video_id, timestamp)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    video_id VARCHAR(50),
    prediction_24h INTEGER,
    prediction_7d INTEGER,
    prediction_30d INTEGER,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**DB-003: Performance Requirements**
- **Query Response Time**: < 1 second for standard queries
- **Concurrent Connections**: Support 50+ simultaneous database connections
- **Data Volume**: Efficiently handle 1M+ video records
- **Indexing Strategy**: Composite indexes on frequently queried columns

---

## 7. Appendices

### Appendix A: Use Case Diagrams

**Primary Use Cases:**
1. **User Registration and Authentication**
2. **Video Prediction Generation**
3. **Prediction Result Visualization**
4. **System Administration**

### Appendix B: System Architecture Diagram

**Layered Architecture Components:**
- **Presentation Layer**: Web UI (Streamlit/HTML+CSS+JS)
- **Application Layer**: REST API (Flask)
- **Business Logic Layer**: ML Models and Data Processing
- **Data Access Layer**: Database Operations (SQLAlchemy)
- **Data Storage Layer**: PostgreSQL Database

### Appendix C: Data Flow Diagrams

**Level 0 DFD**: System context showing external entities
**Level 1 DFD**: Major system processes and data stores
**Level 2 DFD**: Detailed process decomposition

### Appendix D: Entity Relationship Diagram

**Core Entities:**
- Users, Channels, Videos, Snapshots, Predictions
- Relationships and cardinalities
- Attribute specifications and constraints

### Appendix E: User Interface Mockups

**Wireframes for:**
- Login/Registration pages
- Main dashboard interface
- Prediction results display
- Mobile responsive layouts

### Appendix F: API Specification

**OpenAPI 3.0 Specification:**
- Endpoint definitions
- Request/response schemas
- Authentication requirements
- Error response formats

### Appendix G: Test Cases

**Test Categories:**
- Unit tests for core functions
- Integration tests for API endpoints
- User acceptance test scenarios
- Performance test specifications

### Appendix H: Deployment Guide

**Deployment Requirements:**
- Docker containerization setup
- Environment configuration
- Database migration scripts
- Monitoring and logging setup

---

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Data Lead | Senevirathne S.M.P.U. | | |
| Backend Lead | Sanjula N.G.K. | | |
| Frontend Lead | Shaamma M.S. | | |
| Project Mentor | [To be assigned] | | |

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-08-06 | Team | Initial comprehensive SRS document |

---

*This document represents the complete software requirements specification for the ViewTrendsSL system and serves as the authoritative reference for all development, testing, and evaluation activities.*
