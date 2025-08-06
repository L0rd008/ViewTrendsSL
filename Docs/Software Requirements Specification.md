# Software Requirements Specification
## ViewTrendsSL: YouTube Viewership Forecasting System

**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  

---

## Revision History

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 06/Aug/2025 | 1.0 | Initial SRS document creation | Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S. |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Scope](#12-scope)
   - 1.3 [Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
   - 1.4 [References](#14-references)
   - 1.5 [Overview](#15-overview)

2. [Overall Description](#2-overall-description)

3. [Specific Requirements](#3-specific-requirements)
   - 3.1 [Functionality](#31-functionality)
   - 3.2 [Usability](#32-usability)
   - 3.3 [Reliability](#33-reliability)
   - 3.4 [Performance and Security](#34-performance-and-security)
   - 3.5 [Supportability](#35-supportability)
   - 3.6 [Design Constraints](#36-design-constraints)
   - 3.7 [On-line User Documentation and Help System Requirements](#37-on-line-user-documentation-and-help-system-requirements)
   - 3.8 [Purchased Components](#38-purchased-components)
   - 3.9 [Interfaces](#39-interfaces)
   - 3.10 [Database Requirements](#310-database-requirements)
   - 3.11 [Licensing, Legal, Copyright, and Other Notices](#311-licensing-legal-copyright-and-other-notices)
   - 3.12 [Applicable Standards](#312-applicable-standards)

4. [Supporting Information](#4-supporting-information)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) fully describes the external behavior of the ViewTrendsSL application - a machine learning-powered web system for predicting YouTube video viewership specifically tailored for Sri Lankan audiences. This document describes nonfunctional requirements, design constraints, and other factors necessary to provide a complete and comprehensive description of the requirements for the software.

**Intended Audience:**
- Development team members (Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S.)
- Project mentors and academic evaluators
- System testers and quality assurance personnel
- Future maintainers and contributors
- Academic researchers and stakeholders

The SRS serves as the definitive specification for system development, testing, and evaluation throughout the 10-week project timeline.

### 1.2 Scope

ViewTrendsSL is a specialized analytics platform that addresses the critical gap in region-specific YouTube viewership prediction tools. The software application leverages machine learning research to provide accurate forecasting capabilities tailored to Sri Lankan audience behavior and content consumption patterns.

**Key Features Included:**
- Automated YouTube data collection and processing system
- Machine learning prediction engine with separate models for Shorts and Long-form videos
- Web-based user interface for prediction requests and visualization
- User authentication and session management
- Interactive prediction result visualization with downloadable reports
- Database management system for storing video metadata and predictions
- API services for external integrations

**System Boundaries:**
- The system processes only public YouTube videos accessible via YouTube Data API v3
- Predictions are generated for 24-hour, 7-day, and 30-day intervals
- Primary focus on Sri Lankan content but supports international videos
- Web-based deployment accessible through standard browsers
- Integration limited to YouTube Data API v3 and cloud hosting services

### 1.3 Definitions, Acronyms, and Abbreviations

**Technical Acronyms:**
- **API**: Application Programming Interface - Set of protocols enabling software component communication
- **ETL**: Extract, Transform, Load - Data processing pipeline for collection, cleaning, and storage
- **MAPE**: Mean Absolute Percentage Error - Prediction accuracy metric expressed as percentage
- **MAE**: Mean Absolute Error - Average magnitude of prediction errors
- **RMSE**: Root Mean Squared Error - Standard deviation of prediction residuals
- **SRS**: Software Requirements Specification
- **UI**: User Interface
- **UX**: User Experience
- **REST**: Representational State Transfer - Architectural style for web services

**Domain-Specific Terms:**
- **Shorts**: YouTube videos with duration ≤ 60 seconds
- **Long-form**: YouTube videos with duration > 60 seconds
- **Channel Authority**: Composite metric of channel influence and reach
- **Early Engagement**: User interactions within first 24 hours of video publication
- **Viewership Curve**: Temporal visualization of video view count progression
- **Feature Engineering**: Process of creating predictive variables from raw data

**System Components:**
- **Data Collector**: Automated YouTube API integration module
- **Prediction Engine**: Machine learning model inference system
- **Web Dashboard**: User interface for prediction requests and visualization
- **Database Manager**: Data storage and retrieval system

### 1.4 References

**Academic Literature:**
1. "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms" - Journal of Retailing and Consumer Services (2024)
2. "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity" - arXiv:2503.04446v1 (2025)
3. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications

**Technical Documentation:**
- YouTube Data API v3 Documentation: https://developers.google.com/youtube/v3 (Accessed on 06/Aug/2025)
- Flask Web Framework Documentation: https://flask.palletsprojects.com/ (Accessed on 06/Aug/2025)
- XGBoost Documentation: https://xgboost.readthedocs.io/ (Accessed on 06/Aug/2025)
- PostgreSQL Documentation: https://www.postgresql.org/docs/ (Accessed on 06/Aug/2025)

**Development Standards:**
- PEP 8 - Style Guide for Python Code
- REST API Design Guidelines
- Web Content Accessibility Guidelines (WCAG) 2.1

### 1.5 Overview

This SRS document is organized into four main sections following IEEE 830-1998 standards:

**Section 1 (Introduction)** provides an overview of the entire SRS, including purpose, scope, definitions, references, and document organization.

**Section 2 (Overall Description)** describes the general factors that affect the product and its requirements, providing background context for the detailed requirements.

**Section 3 (Specific Requirements)** contains all software requirements to a level of detail sufficient to enable designers to design a system to satisfy those requirements, and testers to test that the system satisfies those requirements.

**Section 4 (Supporting Information)** includes appendices, diagrams, and additional documentation that supports the requirements specification.

---

## 2. Overall Description

ViewTrendsSL operates as an independent web-based system that integrates with YouTube Data API v3 to collect video metadata and generate viewership predictions using trained machine learning models. The system serves multiple user classes including content creators, digital marketers, media companies, and academic researchers.

**Product Perspective:**
The system follows a layered architecture pattern with clear separation between presentation (web interface), business logic (prediction engine), and data layers (database and API integration). It operates within the constraints of YouTube API quotas and cloud hosting limitations while providing accurate, region-specific predictions for Sri Lankan audiences.

**Product Functions:**
- Automated data collection from YouTube channels popular in Sri Lanka
- Feature engineering and data preprocessing for machine learning
- Separate model training and inference for Shorts and Long-form videos
- Interactive web interface for prediction requests and result visualization
- User authentication and session management
- System monitoring and performance tracking

**User Characteristics:**
- **Content Creators**: Basic to intermediate technical skills, occasional usage for strategic planning
- **Digital Marketers**: Intermediate to advanced analytical skills, regular usage for campaign optimization
- **Media Companies**: Advanced technical capabilities, intensive usage for portfolio management
- **Academic Researchers**: Advanced technical knowledge, research-focused usage with dataset access

**Operating Environment:**
- **Client-side**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Server-side**: Linux-based cloud hosting with Python 3.9+, PostgreSQL 13+, Docker containerization
- **Development**: Cross-platform compatibility (Windows 11, Ubuntu 24.04)

**Design and Implementation Constraints:**
- YouTube Data API v3 quota limitations (10,000 units/day per key)
- 10-week development timeline with academic milestones
- Zero-cost approach using free-tier services
- Three-person development team with distributed responsibilities
- University research ethics and YouTube API Terms of Service compliance

**Assumptions and Dependencies:**
- YouTube Data API v3 remains stable and accessible
- Cloud hosting services maintain reliable uptime
- Sri Lankan YouTube content maintains consistent metadata patterns
- User internet connections support real-time web application usage

---

## 3. Specific Requirements

### 3.1 Functionality

This section describes the functional requirements of the ViewTrendsSL system, organized by major system features and user activities.

#### 3.1.1 User Authentication and Session Management

**Description:** The system shall provide secure user registration, authentication, and session management capabilities to enable personalized access to prediction services.

**Detailed Functionality:**

**User Registration Process:**
- The system shall provide a registration form requiring email address, password, and password confirmation
- The system shall validate email format using standard email validation patterns
- The system shall enforce password complexity requirements (minimum 8 characters, mixed case, numbers, special characters)
- The system shall send email verification for account activation
- The system shall prevent duplicate email registrations and provide appropriate error messages
- The system shall store user credentials securely using bcrypt hashing with cost factor 12

**User Authentication Process:**
- The system shall authenticate users via email/password combination
- The system shall implement secure session management with JWT tokens
- The system shall maintain user sessions with automatic timeout after 2 hours of inactivity
- The system shall provide secure logout functionality that invalidates session tokens
- The system shall implement account lockout after 5 consecutive failed login attempts
- The system shall provide "Remember Me" functionality for extended sessions (optional)

**Password Management:**
- The system shall provide password reset functionality via email verification
- The system shall generate secure password reset tokens with 1-hour expiration
- The system shall enforce password complexity requirements for new passwords
- The system shall prevent password reuse for the last 3 passwords
- The system shall provide password strength indicators during registration and password changes

#### 3.1.2 Video Prediction Generation

**Description:** The core functionality that processes YouTube video URLs and generates viewership predictions using trained machine learning models.

**Detailed Functionality:**

**Video URL Processing:**
- The system shall accept YouTube video URLs in multiple formats (youtube.com/watch?v=, youtu.be/, mobile links)
- The system shall extract video ID from various URL formats using regex patterns
- The system shall validate video accessibility and public status via YouTube Data API v3
- The system shall retrieve comprehensive video metadata including title, description, duration, category, tags, and statistics
- The system shall handle private, deleted, or restricted videos with appropriate error messages

**Feature Extraction and Processing:**
- The system shall extract temporal features including publish_hour (0-23), day_of_week (0-6), and is_weekend (boolean)
- The system shall calculate content features including title_length, tag_count, description_length, and category_id
- The system shall determine video type classification (Shorts ≤60 seconds vs Long-form >60 seconds)
- The system shall retrieve channel authority metrics including subscriber_count, video_count, and channel_age
- The system shall normalize and scale features according to trained model requirements
- The system shall handle missing or null values using appropriate imputation strategies

**Model Inference and Prediction:**
- The system shall select the appropriate trained model based on video type (separate models for Shorts and Long-form)
- The system shall generate predictions for three time intervals: 24 hours, 7 days, and 30 days after publication
- The system shall calculate prediction confidence intervals using model uncertainty quantification
- The system shall validate prediction reasonableness against historical patterns and flag outliers
- The system shall provide fallback predictions using baseline models if primary models fail
- The system shall log all prediction requests with timestamps for model improvement and monitoring

**Prediction Output and Validation:**
- The system shall format predictions with appropriate precision (integer view counts)
- The system shall provide prediction accuracy indicators based on model performance metrics
- The system shall generate prediction metadata including model version, confidence score, and processing time
- The system shall implement prediction caching to avoid redundant API calls for the same video
- The system shall handle edge cases such as very new videos or videos with unusual characteristics

#### 3.1.3 Data Collection and Management

**Description:** Automated system for collecting, processing, and storing YouTube video and channel data for model training and system operation.

**Detailed Functionality:**

**Automated Data Collection:**
- The system shall maintain a curated list of Sri Lankan YouTube channels across multiple categories (news, entertainment, education, lifestyle)
- The system shall implement scheduled data collection running daily to gather new video metadata
- The system shall efficiently manage YouTube API quota across multiple API keys (team members' keys)
- The system shall collect video-level metadata including title, description, duration, category, tags, thumbnail URL, and publication date
- The system shall collect channel-level metadata including subscriber count, video count, country, and channel description
- The system shall implement robust error handling for API failures, rate limiting, and network issues
- The system shall validate and clean collected data automatically, removing duplicates and handling missing values

**Data Storage and Organization:**
- The system shall store collected data in a normalized PostgreSQL database schema
- The system shall implement efficient database indexing for fast query performance on frequently accessed columns
- The system shall maintain data integrity using foreign key constraints and data validation rules
- The system shall implement data versioning to track changes in video statistics over time
- The system shall provide data backup and recovery mechanisms with automated daily backups
- The system shall implement data archiving strategies for old or irrelevant data

**Data Quality Assurance:**
- The system shall validate data completeness and accuracy using predefined quality rules
- The system shall detect and handle corrupted, missing, or inconsistent data entries
- The system shall implement data deduplication mechanisms to prevent duplicate records
- The system shall generate automated data quality reports highlighting issues and statistics
- The system shall monitor data collection success rates and alert administrators of failures
- The system shall implement data lineage tracking to trace data from source to usage

#### 3.1.4 Interactive Data Visualization

**Description:** Web-based interface for displaying prediction results, video metadata, and analytical insights through interactive charts and visualizations.

**Detailed Functionality:**

**Prediction Results Display:**
- The system shall display video thumbnail, title, channel name, and basic metadata in a structured layout
- The system shall generate interactive line charts showing predicted viewership curves over time
- The system shall highlight key prediction milestones (24-hour, 7-day, 30-day) with distinct markers
- The system shall provide numerical prediction values with appropriate formatting (e.g., "1.2K", "1.2M")
- The system shall display prediction confidence intervals as shaded areas around the main prediction line
- The system shall show current video statistics (if available) as baseline comparison points

**Interactive Chart Features:**
- The system shall enable chart zoom and pan functionality for detailed examination
- The system shall provide hover tooltips displaying exact values, timestamps, and additional context
- The system shall allow users to toggle between different time scales (hours, days, weeks)
- The system shall support chart export functionality in multiple formats (PNG, SVG, PDF)
- The system shall implement responsive chart design that adapts to different screen sizes
- The system shall provide chart customization options including color schemes and display preferences

**Comparative Analysis Tools:**
- The system shall enable comparison between multiple video predictions on the same chart
- The system shall display category-based performance benchmarks and industry averages
- The system shall show channel performance context and historical comparison data
- The system shall provide trend analysis insights highlighting patterns and anomalies
- The system shall implement filtering and sorting capabilities for prediction history
- The system shall generate downloadable prediction summary reports in PDF format

#### 3.1.5 System Administration and Monitoring

**Description:** Administrative interface and monitoring system for system health tracking, performance optimization, and maintenance operations.

**Detailed Functionality:**

**System Health Monitoring:**
- The system shall continuously monitor YouTube API quota usage across all API keys
- The system shall track system performance metrics including response times, error rates, and throughput
- The system shall implement automated alerting for critical system issues via email notifications
- The system shall log all system events with appropriate severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- The system shall monitor database performance including query execution times and connection pool status
- The system shall track user activity patterns and system usage statistics

**Performance Analytics and Reporting:**
- The system shall generate automated system performance reports on a weekly basis
- The system shall track prediction accuracy over time and alert on degradation
- The system shall monitor user engagement metrics including session duration and feature usage
- The system shall identify and alert on performance bottlenecks and resource constraints
- The system shall provide real-time dashboards for system administrators
- The system shall implement capacity planning tools to predict resource requirements

**Maintenance and Operations:**
- The system shall provide database backup and restore functionality with point-in-time recovery
- The system shall support model retraining and deployment without system downtime
- The system shall enable configuration updates through environment variables without restart
- The system shall provide system status pages for users during maintenance periods
- The system shall implement automated log rotation and cleanup to manage disk space
- The system shall support graceful shutdown and startup procedures for maintenance windows

### 3.2 Usability

This section specifies requirements that affect the usability and user experience of the ViewTrendsSL system.

#### 3.2.1 Learning Curve and Training Requirements

**Requirement:** The system shall be designed for intuitive use with minimal training requirements.

**Specifications:**
- New users shall be able to generate their first video prediction within 5 minutes of account creation
- The system shall provide contextual help and tooltips for all major interface elements
- Users shall achieve 95% task completion rate for core prediction workflow after initial use
- The system shall include an interactive tutorial or walkthrough for first-time users
- Power users shall be able to access advanced features without cluttering the basic interface

#### 3.2.2 User Interface Standards and Consistency

**Requirement:** The system shall conform to modern web usability standards and maintain consistent design patterns.

**Specifications:**
- The system shall follow Google Material Design principles for visual consistency
- All interactive elements shall provide clear visual feedback (hover states, loading indicators, success/error messages)
- The system shall maintain consistent navigation patterns across all pages
- Form validation shall provide real-time feedback with clear, actionable error messages
- The system shall use standard web conventions for common actions (login, search, export)

#### 3.2.3 Accessibility and Inclusive Design

**Requirement:** The system shall be accessible to users with diverse abilities and technical backgrounds.

**Specifications:**
- The system shall comply with WCAG 2.1 AA accessibility standards
- All interface elements shall be keyboard navigable with logical tab order
- The system shall provide alternative text for images and meaningful labels for form elements
- Color shall not be the only means of conveying information (colorblind-friendly design)
- The system shall support screen readers and assistive technologies
- Text shall maintain minimum contrast ratios of 4.5:1 for normal text and 3:1 for large text

#### 3.2.4 Responsive Design and Multi-Device Support

**Requirement:** The system shall provide optimal user experience across different devices and screen sizes.

**Specifications:**
- The system shall be fully functional on desktop computers (1920x1080 and above)
- The system shall provide optimized layouts for tablet devices (768x1024)
- The system shall maintain core functionality on mobile devices (375x667 minimum)
- Charts and visualizations shall adapt appropriately to different screen sizes
- Touch interfaces shall have appropriately sized interactive elements (minimum 44px touch targets)

### 3.3 Reliability

This section specifies requirements for system reliability, availability, and fault tolerance.

#### 3.3.1 System Availability Requirements

**Requirement:** The system shall maintain high availability during operational hours with minimal downtime.

**Specifications:**
- The system shall achieve 99.5% uptime during operational hours (allowing for 3.6 hours downtime per month)
- Planned maintenance windows shall be scheduled during low-usage periods and communicated 48 hours in advance
- The system shall implement graceful degradation, maintaining core functionality even when non-critical components fail
- Database connections shall be pooled and managed to prevent connection exhaustion
- The system shall automatically recover from transient failures without manual intervention

#### 3.3.2 Error Handling and Recovery

**Requirement:** The system shall handle errors gracefully and provide meaningful feedback to users.

**Specifications:**
- All user-facing errors shall display helpful messages with suggested corrective actions
- The system shall log all errors with sufficient detail for debugging and resolution
- API failures shall be handled with appropriate retry logic and exponential backoff
- The system shall implement circuit breaker patterns for external service dependencies
- Database transaction failures shall be rolled back completely to maintain data consistency
- The system shall provide fallback mechanisms for critical functionality when external services are unavailable

#### 3.3.3 Data Integrity and Consistency

**Requirement:** The system shall maintain data accuracy and consistency across all operations.

**Specifications:**
- All database operations shall use ACID-compliant transactions
- Data validation shall occur at both client-side and server-side levels
- The system shall implement foreign key constraints to maintain referential integrity
- Backup and recovery procedures shall be tested monthly to ensure data recoverability
- The system shall detect and prevent data corruption through checksums and validation routines
- Concurrent access to shared resources shall be managed through appropriate locking mechanisms

#### 3.3.4 Fault Tolerance and Resilience

**Requirement:** The system shall continue operating effectively in the presence of component failures.

**Specifications:**
- The system shall implement health checks for all critical components
- Failed components shall be automatically restarted when possible
- The system shall maintain operation even if individual prediction models fail
- Network timeouts shall be handled gracefully with appropriate user feedback
- The system shall implement rate limiting to prevent resource exhaustion from excessive requests
- Critical system functions shall have redundant implementations or fallback mechanisms

### 3.4 Performance and Security

This section outlines performance benchmarks and security requirements for the ViewTrendsSL system.

#### 3.4.1 Response Time Requirements

**Requirement:** The system shall provide responsive user experience with acceptable response times for all operations.

**Specifications:**
- Video prediction generation shall complete within 30 seconds end-to-end
- Initial page load time shall not exceed 3 seconds on broadband connections
- Standard API calls shall respond within 5 seconds under normal load
- Database queries shall execute within 1 second for standard operations
- Chart rendering and visualization updates shall complete within 2 seconds
- User authentication operations shall complete within 2 seconds

#### 3.4.2 Throughput and Scalability

**Requirement:** The system shall handle expected user load and scale appropriately with demand.

**Specifications:**
- The system shall support minimum 10 concurrent users without performance degradation
- The system shall process at least 100 video predictions per hour
- Database operations shall handle 1000+ video metadata records per hour
- The system architecture shall support horizontal scaling to accommodate growth
- API rate limiting shall prevent individual users from overwhelming system resources
- The system shall maintain performance standards up to 80% of maximum capacity

#### 3.4.3 Security and Authentication

**Requirement:** The system shall implement comprehensive security measures to protect user data and system integrity.

**Specifications:**
- All data transmission shall use HTTPS with TLS 1.3 encryption
- User passwords shall be hashed using bcrypt with minimum cost factor of 12
- Session tokens shall be cryptographically secure and expire after 2 hours of inactivity
- The system shall implement CSRF protection for all state-changing operations
- API keys shall be stored securely using environment variables and never exposed in code
- The system shall validate and sanitize all user inputs to prevent injection attacks
- Failed authentication attempts shall be logged and monitored for suspicious activity

#### 3.4.4 Data Protection and Privacy

**Requirement:** The system shall protect user privacy and comply with data protection requirements.

**Specifications:**
- Personal user data shall be encrypted at rest using AES-256 encryption
- The system shall implement role-based access control for administrative functions
- User data shall be retained only as long as necessary for system operation
- The system shall provide mechanisms for users to delete their accounts and associated data
- All data processing shall comply with YouTube API Terms of Service
- The system shall implement audit logging for all data access and modifications
- Privacy policy and terms of service shall be clearly displayed and regularly updated

### 3.5 Supportability

This section defines requirements that enhance the maintainability and supportability of the ViewTrendsSL system.

#### 3.5.1 Code Quality and Documentation

**Requirement:** The system shall be developed with high code quality standards to ensure long-term maintainability.

**Specifications:**
- All Python code shall comply with PEP 8 style guidelines
- Code coverage shall maintain minimum 80% for unit tests
- All public functions and classes shall include comprehensive docstrings
- Complex algorithms and business logic shall be thoroughly commented
- The system shall use meaningful variable and function names following established conventions
- Code reviews shall be mandatory for all changes to the main branch

#### 3.5.2 Logging and Monitoring

**Requirement:** The system shall provide comprehensive logging and monitoring capabilities for operational support.

**Specifications:**
- All system events shall be logged with appropriate severity levels and timestamps
- Log files shall be automatically rotated and archived to prevent disk space issues
- The system shall implement structured logging with consistent format across all components
- Performance metrics shall be collected and stored for trend analysis
- Error tracking shall provide stack traces and context information for debugging
- System health metrics shall be exposed through monitoring endpoints

#### 3.5.3 Configuration Management

**Requirement:** The system shall support flexible configuration management for different deployment environments.

**Specifications:**
- All configuration parameters shall be externalized using environment variables
- The system shall support different configuration profiles for development, testing, and production
- Configuration changes shall not require code modifications or system rebuilds
- Sensitive configuration data shall be encrypted and securely managed
- The system shall validate configuration parameters at startup and provide clear error messages for invalid settings
- Configuration documentation shall be maintained and kept current with system changes

#### 3.5.4 Deployment and Operations

**Requirement:** The system shall support automated deployment and operational procedures.

**Specifications:**
- The system shall be containerized using Docker for consistent deployment across environments
- Database schema migrations shall be automated and version-controlled
- The system shall support zero-downtime deployments for minor updates
- Rollback procedures shall be documented and tested for rapid recovery from failed deployments
- System dependencies shall be clearly documented with specific version requirements
- Operational runbooks shall be maintained for common maintenance and troubleshooting procedures

### 3.6 Design Constraints

This section identifies design decisions and constraints that must be adhered to during system development.

#### 3.6.1 Standards Compliance

**Requirement:** The system shall comply with established technical and academic standards.

**Specifications:**
- Web development shall follow W3C standards for HTML5, CSS3, and JavaScript ES6+
- REST API design shall conform to standard RESTful principles and HTTP status code usage
- Database design shall follow Third Normal Form (3NF) principles for relational schema
- Security implementation shall align with OWASP Top 10 security guidelines
- Code documentation shall follow IEEE standards for software documentation
- Academic deliverables shall comply with University of Moratuwa formatting and citation requirements

#### 3.6.2 Hardware Limitations

**Requirement:** The system shall operate within the constraints of available hardware resources.

**Specifications:**
- Development shall be conducted on team laptops with 16GB RAM and mid-range processors
- Production deployment shall utilize free-tier cloud hosting with resource limitations
- Machine learning models shall be optimized for CPU-only inference (no GPU requirements)
- Database operations shall be optimized for single-instance deployment
- File storage shall be minimized to work within cloud storage limitations
- Memory usage shall be optimized to prevent out-of-memory errors on constrained systems

#### 3.6.3 Technology Stack Constraints

**Requirement:** The system shall use specified technologies and frameworks as mandated by project requirements.

**Specifications:**
- Backend development shall use Python 3.9+ with Flask web framework
- Database shall use PostgreSQL for production and SQLite for development
- Frontend shall use modern web technologies (HTML5, CSS3, JavaScript) with optional framework integration
- Machine learning shall utilize scikit-learn and XGBoost libraries
- Containerization shall use Docker with Docker Compose for orchestration
- Version control shall use Git with GitHub for repository hosting
- Cloud deployment shall use free-tier services (Heroku, Railway, or equivalent)

#### 3.6.4 Timeline and Resource Constraints

**Requirement:** The system shall be developed within the specified academic timeline and resource constraints.

**Specifications:**
- Total development time shall not exceed 10 weeks (August 24 - November 1, 2025)
- Development team shall consist of exactly three members with defined roles
- Budget constraints require use of free-tier services and open-source tools only
- Academic milestones shall be met according to university schedule
- Feature scope shall be limited to MVP requirements to ensure timely completion
- Documentation shall be completed concurrently with development to meet submission deadlines

### 3.7 On-line User Documentation and Help System Requirements

This section describes requirements for user assistance and documentation within the system.

#### 3.7.1 Integrated Help System

**Requirement:** The system shall provide contextual help and guidance for users.

**Specifications:**
- The system shall include tooltips for all major interface elements explaining their purpose and usage
- A comprehensive FAQ section shall address common user questions and troubleshooting steps
- Interactive tutorials shall guide new users through the prediction generation process
- Help documentation shall be searchable and organized by topic and user type
- Video demonstrations shall be provided for complex workflows and features
- Help content shall be accessible from any page in the application

#### 3.7.2 User Guide and Documentation

**Requirement:** The system shall provide comprehensive user documentation for all functionality.

**Specifications:**
- A complete user manual shall be available in PDF format for download
- Step-by-step guides shall be provided for all major system functions
- Screenshots and examples shall illustrate proper usage of system features
- Troubleshooting guides shall help users resolve common issues independently
- API documentation shall be provided for technical users and potential integrators
- Documentation shall be maintained and updated with each system release

### 3.8 Purchased Components

This section describes any third-party components or services used by the system.

#### 3.8.1 Third-Party Services

**Requirement:** The system shall integrate with external services as needed for functionality.

**Specifications:**
- YouTube Data API v3 shall be used for video and channel metadata retrieval
- Cloud hosting services (Heroku or equivalent) shall be used for production deployment
- Email service providers shall be used for user verification and notifications
- SSL certificate providers shall be used for HTTPS encryption
- All third-party services shall be used within their free-tier limitations
- Service level agreements and terms of service shall be reviewed and complied with

#### 3.8.2 Open Source Libraries

**Requirement:** The system shall utilize appropriate open-source libraries and frameworks.

**Specifications:**
- All open-source components shall use GPL-compatible licenses
- Library versions shall be pinned to specific versions for reproducible builds
- Security vulnerabilities in dependencies shall be monitored and addressed promptly
- License compliance shall be maintained for all third-party components
- Dependency management shall use standard package managers (pip for Python, npm for JavaScript)
- Regular updates shall be applied to maintain security and compatibility

### 3.9 Interfaces

This section defines the interfaces that must be supported by the application.

#### 3.9.1 User Interfaces

**Requirement:** The system shall provide intuitive and responsive user interfaces for all functionality.

**Main Dashboard Interface:**
- Clean, professional layout with ViewTrendsSL branding and navigation
- Prominent video URL input field with clear placeholder text and validation
- "Generate Prediction" button with loading states and progress indicators
- Results section displaying video metadata, thumbnail, and prediction charts
- User account menu with profile, settings, and logout options
- Responsive design adapting to desktop, tablet, and mobile screen sizes

**Authentication Interfaces:**
- Login page with email/password fields and "Remember Me" option
- Registration page with email, password, and confirmation fields
- Password reset page with email input and instructions
- Email verification page with status messages and resend options
- All forms include real-time validation and clear error messaging

**Prediction Results Interface:**
- Video information panel showing thumbnail, title, channel, and metadata
- Interactive prediction chart with zoom, pan, and export capabilities
- Key metrics display for 24-hour, 7-day, and 30-day predictions
- Confidence indicators and prediction accuracy information
- Export options for charts and prediction data
- Social sharing capabilities for prediction results

#### 3.9.2 Hardware Interfaces

**Requirement:** The system shall specify minimum hardware requirements for optimal operation.

**Client-Side Requirements:**
- Minimum 4GB RAM for smooth browser operation with multiple tabs
- Modern multi-core processor (Intel i3 equivalent or better)
- Minimum 100MB available storage for browser cache and temporary files
- Stable internet connection with minimum 1 Mbps bandwidth
- Display resolution minimum 1024x768, optimized for 1920x1080
- Standard input devices (keyboard, mouse, or touch interface)

**Server-Side Requirements:**
- Minimum 2 vCPU cores for concurrent request handling
- 4GB RAM minimum, 8GB recommended for optimal performance
- 20GB SSD storage for application, database, and log files
- High-speed internet connection for API calls and user requests

#### 3.9.3 Software Interfaces

**Requirement:** The system shall integrate with external software systems and services as specified.

**YouTube Data API v3 Interface:**
- Protocol: HTTPS REST API with JSON request/response format
- Authentication: API key-based authentication with secure key management
- Rate Limiting: 10,000 units per day per API key with efficient quota management
- Error Handling: Comprehensive error code handling with retry logic and exponential backoff
- Data Format: Structured JSON responses with video and channel metadata
- Endpoints Used: videos.list, channels.list, search.list for data collection

**Database Interface:**
- Database System: PostgreSQL 13+ for production, SQLite for development
- Connection Management: SQLAlchemy ORM with connection pooling for optimal performance
- Schema Design: Normalized relational schema following Third Normal Form (3NF)
- Transaction Management: ACID-compliant transactions with rollback capabilities
- Backup and Recovery: Automated daily backups with point-in-time recovery
- Performance Optimization: Indexed queries with sub-second response times

**Machine Learning Model Interface:**
- Model Format: Serialized XGBoost models stored as .pkl files using joblib
- Model Loading: Models loaded at application startup for optimal performance
- Inference Pipeline: Real-time prediction generation with preprocessing and postprocessing
- Model Versioning: Version tracking and rollback capability for model management
- Performance Requirements: Prediction generation within 5 seconds per request
- Fallback Mechanisms: Baseline models available if primary models fail

#### 3.9.4 Communications Interfaces

**Requirement:** The system shall support specified communication protocols and interfaces.

**HTTP/HTTPS Protocol:**
- All client-server communication shall use HTTPS with TLS 1.3 encryption
- RESTful API design following standard HTTP methods (GET, POST, PUT, DELETE)
- Comprehensive HTTP status code implementation for proper error handling
- CORS (Cross-Origin Resource Sharing) support for web application integration
- Content-Type headers properly set for JSON and form data transmission

**REST API Interface:**
- Base URL: https://viewtrendssl.herokuapp.com/api/v1
- Authentication: JWT token-based authentication with secure token management
- Rate Limiting: 100 requests per minute per authenticated user
- API Documentation: OpenAPI 3.0 specification with interactive documentation
- Error Responses: Standardized error format with descriptive messages and error codes

**Key API Endpoints:**
```
POST /api/v1/auth/login          # User authentication
POST /api/v1/auth/register       # User registration
POST /api/v1/auth/logout         # User logout
POST /api/v1/predict             # Generate video prediction
GET  /api/v1/predictions/history # User prediction history
GET  /api/v1/user/profile        # User profile information
PUT  /api/v1/user/profile        # Update user profile
GET  /api/v1/system/health       # System health check
GET  /api/v1/system/status       # System status information
```

**Email Communication Interface:**
- SMTP protocol for sending verification and notification emails
- Email templates for user registration, password reset, and system notifications
- Secure email configuration with authentication and encryption
- Email delivery tracking and error handling for failed deliveries

### 3.10 Database Requirements

This section defines the database requirements and specifications for the ViewTrendsSL system.

#### 3.10.1 Database System Requirements

**Requirement:** The system shall use a robust, scalable database system for data storage and retrieval.

**Database Technology:**
- Production Environment: PostgreSQL 13+ with ACID compliance and advanced features
- Development Environment: SQLite 3.36+ for local development and testing
- Connection Management: Connection pooling with maximum 50 concurrent connections
- Performance Requirements: Sub-second response times for standard queries
- Scalability: Support for millions of video records with efficient indexing
- Backup Strategy: Automated daily backups with 30-day retention period

#### 3.10.2 Database Schema Design

**Requirement:** The system shall implement a normalized database schema following relational design principles.

**Core Database Schema:**

```sql
-- Channels table for storing YouTube channel information
CREATE TABLE channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    subscriber_count INTEGER DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    country VARCHAR(10),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Videos table for storing YouTube video metadata
CREATE TABLE videos (
    video_id VARCHAR(50) PRIMARY KEY,
    channel_id VARCHAR(50) NOT NULL REFERENCES channels(channel_id),
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP NOT NULL,
    duration_seconds INTEGER NOT NULL,
    category_id INTEGER,
    is_short BOOLEAN NOT NULL DEFAULT FALSE,
    tags TEXT[],
    thumbnail_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Snapshots table for time-series video statistics
CREATE TABLE snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) NOT NULL REFERENCES videos(video_id),
    timestamp TIMESTAMP NOT NULL,
    view_count BIGINT DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table for user authentication and management
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table for storing user prediction requests and results
CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    video_id VARCHAR(50) NOT NULL,
    video_title TEXT,
    channel_name VARCHAR(255),
    prediction_24h INTEGER,
    prediction_7d INTEGER,
    prediction_30d INTEGER,
    confidence_score FLOAT,
    model_version VARCHAR(50),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table for session management
CREATE TABLE user_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.10.3 Database Indexing Strategy

**Requirement:** The system shall implement efficient indexing for optimal query performance.

**Index Specifications:**
```sql
-- Primary indexes for foreign key relationships
CREATE INDEX idx_videos_channel_id ON videos(channel_id);
CREATE INDEX idx_snapshots_video_id ON snapshots(video_id);
CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);

-- Composite indexes for time-series queries
CREATE INDEX idx_snapshots_video_timestamp ON snapshots(video_id, timestamp);
CREATE INDEX idx_videos_published_at ON videos(published_at);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Indexes for search and filtering
CREATE INDEX idx_videos_is_short ON videos(is_short);
CREATE INDEX idx_videos_category_id ON videos(category_id);
CREATE INDEX idx_channels_country ON channels(country);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_email_verified ON users(email_verified);

-- Partial indexes for active records
CREATE INDEX idx_users_active ON users(user_id) WHERE is_active = TRUE;
CREATE INDEX idx_sessions_active ON user_sessions(session_id) WHERE expires_at > NOW();
```

#### 3.10.4 Data Integrity and Constraints

**Requirement:** The system shall enforce data integrity through database constraints and validation rules.

**Constraint Specifications:**
```sql
-- Check constraints for data validation
ALTER TABLE videos ADD CONSTRAINT chk_duration_positive 
    CHECK (duration_seconds > 0);
ALTER TABLE snapshots ADD CONSTRAINT chk_counts_non_negative 
    CHECK (view_count >= 0 AND like_count >= 0 AND comment_count >= 0);
ALTER TABLE predictions ADD CONSTRAINT chk_predictions_positive 
    CHECK (prediction_24h >= 0 AND prediction_7d >= 0 AND prediction_30d >= 0);
ALTER TABLE predictions ADD CONSTRAINT chk_confidence_range 
    CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

-- Unique constraints
ALTER TABLE users ADD CONSTRAINT uk_users_email UNIQUE (email);
ALTER TABLE channels ADD CONSTRAINT uk_channels_id UNIQUE (channel_id);
ALTER TABLE videos ADD CONSTRAINT uk_videos_id UNIQUE (video_id);

-- Foreign key constraints with cascading actions
ALTER TABLE videos ADD CONSTRAINT fk_videos_channel 
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE;
ALTER TABLE snapshots ADD CONSTRAINT fk_snapshots_video 
    FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE;
ALTER TABLE predictions ADD CONSTRAINT fk_predictions_user 
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
```

### 3.11 Licensing, Legal, Copyright, and Other Notices

This section addresses legal requirements, licensing, and compliance issues for the ViewTrendsSL system.

#### 3.11.1 Software Licensing

**Requirement:** The system shall comply with all applicable software licenses and intellectual property requirements.

**Open Source License Compliance:**
- The ViewTrendsSL system shall be released under the MIT License for academic and research use
- All third-party open-source libraries shall be used in compliance with their respective licenses
- License compatibility shall be verified for all dependencies to ensure GPL compatibility
- A comprehensive LICENSE file shall be included in the project repository
- All source code files shall include appropriate copyright headers

**Third-Party Library Licenses:**
- Flask (BSD-3-Clause License) - Web framework
- XGBoost (Apache License 2.0) - Machine learning library
- PostgreSQL (PostgreSQL License) - Database system
- Pandas (BSD-3-Clause License) - Data manipulation library
- NumPy (BSD-3-Clause License) - Numerical computing library
- All licenses shall be documented in a LICENSES.md file

#### 3.11.2 YouTube API Terms of Service Compliance

**Requirement:** The system shall comply with YouTube Data API v3 Terms of Service and usage policies.

**API Usage Compliance:**
- The system shall not store or cache YouTube data beyond the permitted retention periods
- All data usage shall comply with YouTube's Developer Policies and Terms of Service
- The system shall include proper attribution to YouTube for data sources
- User privacy shall be protected in accordance with YouTube's privacy requirements
- The system shall not attempt to circumvent API rate limits or usage restrictions
- Regular review of YouTube API terms shall be conducted to ensure ongoing compliance

#### 3.11.3 Data Privacy and Protection

**Requirement:** The system shall implement appropriate data privacy and protection measures.

**Privacy Policy Requirements:**
- A comprehensive privacy policy shall be displayed prominently on the website
- Users shall be informed about data collection, usage, and retention practices
- The system shall provide mechanisms for users to access, modify, and delete their personal data
- Data processing shall be limited to the minimum necessary for system functionality
- User consent shall be obtained for all data processing activities
- The system shall implement data anonymization for research and analytics purposes

**Data Protection Measures:**
- Personal user data shall be encrypted at rest using industry-standard encryption
- Data transmission shall be secured using HTTPS/TLS encryption
- Access to personal data shall be restricted to authorized personnel only
- Data breach notification procedures shall be established and documented
- Regular security audits shall be conducted to ensure data protection compliance

#### 3.11.4 Academic and Research Ethics

**Requirement:** The system shall comply with academic research ethics and institutional requirements.

**University Compliance:**
- The project shall comply with University of Moratuwa research ethics guidelines
- All research activities shall be conducted with appropriate ethical oversight
- Data collection and analysis shall follow established academic research standards
- The system shall support reproducible research through open-source availability
- Academic attribution shall be provided for all research sources and methodologies

**Research Publication Rights:**
- The development team retains rights to publish research findings based on the system
- The dataset created may be made available for academic research purposes
- Proper citation requirements shall be established for use of the system or dataset
- Commercial use restrictions may apply to protect academic research interests

#### 3.11.5 Disclaimer and Limitation of Liability

**Requirement:** The system shall include appropriate disclaimers and liability limitations.

**System Disclaimers:**
- Predictions are statistical forecasts and not guarantees of actual performance
- The system is provided "as-is" without warranties of any kind
- Users are responsible for their own use of prediction results
- The system may experience downtime or service interruptions
- Prediction accuracy may vary based on data quality and model limitations

**Liability Limitations:**
- The development team shall not be liable for business decisions based on predictions
- Users assume all risks associated with using the system for commercial purposes
- The system is intended for educational and research purposes primarily
- No warranties are provided regarding system availability or performance
- Users are responsible for compliance with applicable laws and regulations

### 3.12 Applicable Standards

This section identifies the technical, academic, and industry standards that apply to the ViewTrendsSL system.

#### 3.12.1 Software Development Standards

**Requirement:** The system shall be developed in accordance with established software engineering standards.

**Coding Standards:**
- Python code shall comply with PEP 8 - Style Guide for Python Code
- JavaScript code shall follow ES6+ standards and best practices
- HTML markup shall be valid according to W3C HTML5 standards
- CSS styling shall comply with W3C CSS3 standards
- SQL queries shall follow ANSI SQL standards for database portability
- Code documentation shall follow IEEE Std 1016-2009 for software design descriptions

**Software Engineering Standards:**
- Requirements specification shall follow IEEE Std 830-1998 guidelines
- Software architecture shall comply with IEEE Std 1471-2000 architectural description standards
- Testing procedures shall follow IEEE Std 829-2008 software test documentation standards
- Configuration management shall comply with IEEE Std 828-2012 standards
- Quality assurance shall follow ISO/IEC 25010:2011 software quality model

#### 3.12.2 Web Development Standards

**Requirement:** The system shall comply with web development and accessibility standards.

**Web Standards Compliance:**
- Web Content Accessibility Guidelines (WCAG) 2.1 AA compliance for inclusive design
- Responsive Web Design principles for multi-device compatibility
- Progressive Web App (PWA) standards for enhanced user experience
- Search Engine Optimization (SEO) best practices for discoverability
- Cross-browser compatibility with modern browsers (Chrome, Firefox, Safari, Edge)

**Security Standards:**
- OWASP Top 10 security guidelines for web application security
- Transport Layer Security (TLS) 1.3 for encrypted communications
- Content Security Policy (CSP) implementation for XSS protection
- Secure authentication practices following NIST guidelines
- Data encryption standards (AES-256) for data at rest protection

#### 3.12.3 Database Standards

**Requirement:** The system shall implement database design and management according to established standards.

**Database Design Standards:**
- Third Normal Form (3NF) compliance for relational database design
- ACID (Atomicity, Consistency, Isolation, Durability) transaction properties
- SQL standards compliance for database portability
- Database security standards for access control and data protection
- Backup and recovery standards for data preservation

#### 3.12.4 Machine Learning and Data Science Standards

**Requirement:** The system shall follow established standards for machine learning and data science practices.

**ML Development Standards:**
- Cross-validation standards for model evaluation and validation
- Feature engineering best practices for data preprocessing
- Model versioning and deployment standards for production systems
- Ethical AI guidelines for responsible machine learning
- Reproducible research standards for scientific validity

**Data Quality Standards:**
- Data validation and cleansing standards for high-quality datasets
- Statistical analysis standards for data exploration and insights
- Data lineage and provenance tracking for transparency
- Privacy-preserving data processing standards
- Open data standards for research dataset publication

#### 3.12.5 Academic and Documentation Standards

**Requirement:** The system shall comply with academic and documentation standards appropriate for university projects.

**Academic Standards:**
- University of Moratuwa project documentation requirements
- IEEE citation standards for academic references
- Research methodology standards for empirical studies
- Peer review standards for academic quality assurance
- Open science standards for research transparency and reproducibility

**Documentation Standards:**
- Technical writing standards for clear and comprehensive documentation
- API documentation standards (OpenAPI 3.0) for interface specifications
- User documentation standards for effective user guidance
- Code documentation standards for maintainable software
- Version control standards (Git) for collaborative development

---

## 4. Supporting Information

This section provides additional information and resources that support the requirements specification.

### 4.1 Appendices

**Appendix A: Glossary of Terms**
A comprehensive glossary of technical terms, acronyms, and domain-specific terminology used throughout the system.

**Appendix B: Use Case Diagrams**
Visual representations of system use cases showing interactions between users and system components.

**Appendix C: System Architecture Diagrams**
Detailed architectural diagrams showing system components, interfaces, and data flow.

**Appendix D: Database Entity-Relationship Diagrams**
Complete ERD showing database schema, relationships, and constraints.

**Appendix E: User Interface Mockups**
Wireframes and mockups of key user interface screens and interactions.

**Appendix F: API Specification**
Complete OpenAPI 3.0 specification for all system APIs and endpoints.

### 4.2 References and Bibliography

**Academic References:**
1. Chen, X., et al. (2024). "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms." Journal of Retailing and Consumer Services, 78, 103-115.
2. Zhang, Y., et al. (2025). "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity." arXiv preprint arXiv:2503.04446v1.
3. IEEE Computer Society. (1998). IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.

**Technical Documentation:**
- Google LLC. (2025). YouTube Data API v3 Documentation. Retrieved from https://developers.google.com/youtube/v3
- Pallets Projects. (2025). Flask Documentation. Retrieved from https://flask.palletsprojects.com/
- XGBoost Developers. (2025). XGBoost Documentation. Retrieved from https://xgboost.readthedocs.io/

### 4.3 Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 06/Aug/2025 | Development Team | Initial comprehensive SRS document |
| | | | |
| | | | |

### 4.4 Approval and Sign-off

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Data Lead | Senevirathne S.M.P.U. (220599M) | | 06/Aug/2025 |
| Backend Lead | Sanjula N.G.K. (220578A) | | 06/Aug/2025 |
| Frontend Lead | Shaamma M.S. (220602U) | | 06/Aug/2025 |
| Project Mentor | [To be assigned] | | |
| Course Coordinator | [To be assigned] | | |

---

**Document Status**: Complete and Ready for Academic Submission  
**Last Updated**: August 6, 2025  
**Next Review**: August 13, 2025 (Week 1 Team Review)  
**Document Classification**: Academic Project Documentation  

---

*This Software Requirements Specification document represents the complete and authoritative specification for the ViewTrendsSL system. It serves as the foundation for all development, testing, and evaluation activities throughout the project lifecycle.*
