# Software Architecture Document
## ViewTrendsSL: YouTube Viewership Forecasting System

**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  

---

## Revision History

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 06/Aug/2025 | 1.0 | Initial Software Architecture Document creation | Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S. |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

---

**Note: When you include figures**

Use figure numbers and figure captions.
Use diagrams/images/screenshots with high resolution to get a clear figure.
Use the figure captions in the form of Figure 1. <<caption>> and when explain it in the text, use the abbreviation "Figure 1," even at the beginning of a sentence.
When you use a tool to draw diagrams, change the font settings of the diagram; It is better to have font in black colour/large in size (12pt) and if possible do not fill the objects/elements in the diagram with a colour (keep the background colour white, for clear visibility).
Also, try to re-locate the objects closely in a way that take less space (you may drag elements/objects close to each other).
This will be useful to get a clear image; in order to make the diagram small in size without reducing the resolution quality.
When you include images in your reports, make them "in line with text" (picture tool bar → wrap text → in line with text) and include the caption accordingly. If you include two or more images together (in a row), group them.
Describe each diagram with few sentences.

When you draw diagrams (eg. Sequence diagram) do not include only two object called "user" and "system". Include all the internal objects within the system, without considering the system as a black box. For example: for a mobile application the main system may consists of sub objects such as, <<UI>>:main_Interface, :controller, <<UI>>:analysis_Interface, :local_DB, etc. (this is only an example; use your own terms).

**References:**
Indicate the tools you have used to draw the diagrams

---

## Table of Contents

- [Software Architecture Document](#software-architecture-document)
  - [ViewTrendsSL: YouTube Viewership Forecasting System](#viewtrendssl-youtube-viewership-forecasting-system)
  - [Revision History](#revision-history)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [1.1 Purpose](#11-purpose)
    - [1.2 Scope](#12-scope)
    - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
    - [1.4 References](#14-references)
    - [1.5 Overview](#15-overview)
  - [2. Architectural Representation](#2-architectural-representation)
  - [3. Architectural Goals and Constraints](#3-architectural-goals-and-constraints)
    - [3.1 Key Non-Functional Requirements](#31-key-non-functional-requirements)
    - [3.2 System Constraints](#32-system-constraints)
    - [3.3 Architectural Decisions](#33-architectural-decisions)
  - [4. Use-Case View](#4-use-case-view)
    - [4.1 Use-Case Realizations](#41-use-case-realizations)
  - [5. Logical View](#5-logical-view)
    - [5.1 Overview](#51-overview)
    - [5.2 Architecturally Significant Design Packages](#52-architecturally-significant-design-packages)
  - [6. Process View](#6-process-view)
  - [7. Deployment View](#7-deployment-view)
  - [8. Implementation View](#8-implementation-view)
    - [8.1 Overview](#81-overview)
    - [8.2 Layers](#82-layers)
  - [9. Data View (Optional)](#9-data-view-optional)
  - [10. Size and Performance](#10-size-and-performance)
  - [11. Quality](#11-quality)
  - [12. References](#12-references)

---

## 1. Introduction

The introduction of the Software Architecture Document provides an overview of the entire Software Architecture Document. It includes the purpose, scope, definitions, acronyms, abbreviations, references, and overview of the Software Architecture Document.

### 1.1 Purpose

This document provides a comprehensive architectural overview of the ViewTrendsSL system, using a number of different architectural views to depict different aspects of the system. It is intended to capture and convey the significant architectural decisions which have been made on the system.

This Software Architecture Document serves as the definitive architectural specification for the ViewTrendsSL system - a machine learning-powered web application for predicting YouTube video viewership specifically tailored for Sri Lankan audiences. The document defines the role and purpose within the overall project documentation and describes the structure of the architectural specification.

**Intended Audiences:**
- **Development Team Members** (Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S.): For implementation guidance and technical decision understanding
- **System Testers**: For test planning and integration testing strategies based on architectural components
- **Project Stakeholders and Academic Evaluators**: For architectural oversight, technical validation, and academic assessment
- **Future Maintainers and Contributors**: For system understanding, enhancement planning, and long-term maintenance
- **Research Community**: For methodology validation, reproducibility, and academic contribution

Each audience is expected to use this document as a reference for understanding system structure, making implementation decisions, and ensuring architectural consistency throughout the development lifecycle.

### 1.2 Scope

This Software Architecture Document applies to the complete ViewTrendsSL system including all software components, external integrations, and deployment infrastructure. The document affects and influences all aspects of system design, implementation, testing, and maintenance.

**System Components Covered:**
- **Data Collection Subsystem**: YouTube API integration and automated data harvesting modules
- **Machine Learning Pipeline**: Feature engineering, model training, and prediction inference components
- **Web Application Framework**: User interface, API services, authentication, and session management
- **Database Management System**: Data storage, retrieval, integrity maintenance, and backup systems
- **Deployment Infrastructure**: Containerization, cloud hosting, monitoring, and operational systems

**Hardware and Infrastructure Scope:**
- **Backend Server Infrastructure**: CPU, memory, storage, and network requirements for cloud deployment
- **Client-Side Requirements**: Browser compatibility and performance specifications for end users
- **Development Environment**: Team hardware specifications and development tool requirements
- **External Service Integration**: YouTube Data API, cloud database services, and monitoring platforms

**Boundaries and Limitations:**
- The architecture covers the MVP (Minimum Viable Product) scope with provisions for future enhancements
- External services are integrated but not architecturally controlled by the system
- Academic project constraints influence architectural decisions and complexity levels

### 1.3 Definitions, Acronyms, and Abbreviations

This subsection provides the definitions of all terms, acronyms, and abbreviations required to properly interpret the Software Architecture Document. This information serves as a comprehensive glossary for technical and domain-specific terminology.

**Architectural Terms:**
- **API Gateway**: Single entry point for all client requests to backend services, providing routing and security
- **Data Access Layer (DAL)**: Abstraction layer that encapsulates database operations and provides clean interfaces
- **Domain Model**: Core business logic and entities representing fundamental system concepts and relationships
- **Layered Architecture**: Architectural pattern organizing system into horizontal layers with defined responsibilities
- **ORM (Object-Relational Mapping)**: Database abstraction technology (SQLAlchemy) mapping objects to relational data
- **REST (Representational State Transfer)**: Architectural style for designing networked web services
- **Service Layer**: Business logic coordination layer managing transactions and orchestrating operations

**Machine Learning and Data Science Terms:**
- **Feature Engineering**: Process of creating predictive variables from raw data through transformation and selection
- **Model Inference**: Process of generating predictions from trained machine learning models
- **Pipeline**: Automated sequence of data processing, feature extraction, and model operations
- **Temporal Alignment**: Time-synchronized prediction methodology accounting for video lifecycle patterns
- **XGBoost**: Extreme Gradient Boosting algorithm optimized for tabular data prediction tasks
- **MAPE (Mean Absolute Percentage Error)**: Primary model accuracy metric expressing prediction error as percentage

**System Components:**
- **Data Collector**: Automated YouTube API integration module for metadata harvesting
- **Feature Extractor**: Data preprocessing component transforming raw metadata into model-ready features
- **Prediction Engine**: Machine learning inference system generating viewership forecasts
- **Web Dashboard**: User interface component for prediction requests and result visualization
- **Database Manager**: Data storage and retrieval system ensuring integrity and performance

**Technical Acronyms:**
- **API**: Application Programming Interface - protocols enabling software component communication
- **ETL**: Extract, Transform, Load - data processing pipeline for collection, cleaning, and storage
- **JWT**: JSON Web Token - secure method for transmitting information between parties
- **ORM**: Object-Relational Mapping - database abstraction layer technology
- **REST**: Representational State Transfer - architectural style for web services
- **SLA**: Service Level Agreement - performance and availability commitments
- **TTL**: Time To Live - cache expiration and data freshness control mechanism

### 1.4 References

This subsection provides a complete list of all documents referenced elsewhere in the Software Architecture Document. Each document is identified by title, report number (if applicable), date, and publishing organization, with sources for obtaining references.

**Academic Literature and Research Papers:**
1. "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms" - Journal of Retailing and Consumer Services (2024)
2. "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity" - arXiv:2503.04446v1 (2025)
3. "XGBoost: A Scalable Tree Boosting System" - Chen & Guestrin, KDD 2016
4. IEEE 1471-2000: Recommended Practice for Architectural Description of Software-Intensive Systems
5. ISO/IEC 25010:2011 - Systems and Software Quality Requirements and Evaluation (SQuaRE)

**Technical Documentation and Standards:**
6. YouTube Data API v3 Documentation - Google Developers (https://developers.google.com/youtube/v3)
7. Flask Web Framework Documentation - Pallets Projects (https://flask.palletsprojects.com/)
8. XGBoost Documentation - XGBoost Developers (https://xgboost.readthedocs.io/)
9. PostgreSQL Documentation - PostgreSQL Global Development Group (https://www.postgresql.org/docs/)
10. Docker Documentation - Docker Inc. (https://docs.docker.com/)
11. SQLAlchemy Documentation - SQLAlchemy Project (https://docs.sqlalchemy.org/)

**Development and Design Tools:**
- **Diagram Creation Tool**: Draw.io (https://app.diagrams.net/) - Used for creating architectural diagrams, system topology, and component relationships
- **UML Modeling Tool**: PlantUML - Used for sequence diagrams, component diagrams, and process flow visualization
- **Database Design Tool**: dbdiagram.io - Used for Entity-Relationship Diagram creation and database schema visualization
- **API Documentation Tool**: Swagger/OpenAPI 3.0 - Used for REST API specification and interactive documentation

### 1.5 Overview

This subsection describes what the rest of the Software Architecture Document contains and explains how the Software Architecture Document is organized.

**Document Structure:**
The Software Architecture Document follows the "4+1" architectural view model, providing comprehensive coverage of system architecture through multiple complementary perspectives:

**Sections 1-3**: Foundation and Context
- Introduction, scope, and architectural constraints
- Architectural representation and design principles
- Goals, constraints, and key architectural decisions

**Sections 4-8**: Core Architectural Views
- **Use-Case View (Section 4)**: System functionality from user and stakeholder perspectives
- **Logical View (Section 5)**: System decomposition, component relationships, and design packages
- **Process View (Section 6)**: Runtime behavior, component interactions, and sequence flows
- **Deployment View (Section 7)**: Physical system topology, infrastructure, and hosting architecture
- **Implementation View (Section 8)**: Software organization, layering strategy, and development structure

**Sections 9-12**: Specialized Views and Supporting Information
- **Data View (Section 9)**: Information architecture, database design, and data flow patterns
- **Size and Performance (Section 10)**: Scalability analysis, performance requirements, and capacity planning
- **Quality (Section 11)**: Quality attributes, security architecture, and quality assurance strategies
- **References (Section 12)**: Complete bibliography and supporting documentation

**Reading Guide:**
- **Developers**: Focus on Sections 5, 6, 8, and 9 for implementation guidance
- **Testers**: Emphasize Sections 4, 6, and 11 for testing strategy and quality requirements
- **Stakeholders**: Review Sections 1-3, 7, and 10-11 for architectural overview and quality assurance
- **Maintainers**: Study all sections with particular attention to Sections 8, 9, and 11 for long-term maintenance

---

## 2. Architectural Representation

This section describes what software architecture is for the ViewTrendsSL system, and how it is represented. Of the Use-Case, Logical, Process, Deployment, and Implementation Views, it enumerates the views that are necessary, and for each view, explains what types of model elements it contains.

**Software Architecture Definition for ViewTrendsSL:**
The ViewTrendsSL system architecture is designed as a **Layered Architecture (N-Tier)** pattern that provides clear separation of concerns while enabling maintainable, testable, and scalable system design. This architectural style is optimal for the academic project scope while providing a solid foundation for future enhancements and commercial deployment.

**Architectural Style Justification:**
- **Separation of Concerns**: Each layer has distinct, well-defined responsibilities
- **Maintainability**: Changes in one layer have minimal impact on other layers
- **Testability**: Individual layers can be tested in isolation with mock dependencies
- **Team Collaboration**: Clear architectural boundaries enable parallel development by team members
- **Academic Clarity**: Well-understood pattern facilitating evaluation and documentation
- **Scalability**: Foundation supports future horizontal and vertical scaling requirements

**Selected Architectural Views:**

**1. Use-Case View**
- **Model Elements**: Primary use cases, actors, use case realizations, and scenario descriptions
- **Purpose**: Captures system functionality from user and stakeholder perspectives
- **Key Components**: User authentication, video prediction generation, data visualization, system administration

**2. Logical View**
- **Model Elements**: Subsystems, packages, classes, interfaces, and their relationships
- **Purpose**: Shows system decomposition and component organization
- **Key Components**: Data collection subsystem, machine learning pipeline, web application framework, database management

**3. Process View**
- **Model Elements**: Processes, threads, sequence diagrams, and communication patterns
- **Purpose**: Describes runtime behavior and component interactions
- **Key Components**: Request processing flows, background data collection, model inference pipelines

**4. Deployment View**
- **Model Elements**: Physical nodes, hardware configurations, network topology, and software distribution
- **Purpose**: Shows physical system architecture and deployment strategy
- **Key Components**: Cloud hosting infrastructure, database servers, external service integrations

**5. Implementation View**
- **Model Elements**: Layers, subsystems, components, and development organization
- **Purpose**: Describes software structure and development approach
- **Key Components**: Five-layer architecture with presentation, application, business logic, data access, and storage layers

**6. Data View**
- **Model Elements**: Database schema, data flow diagrams, and information architecture
- **Purpose**: Describes persistent data storage and information management
- **Key Components**: Relational database design, data collection pipelines, caching strategies

**Architectural Patterns and Principles Applied:**
- **Repository Pattern**: Data access abstraction for database operations
- **Factory Pattern**: Model selection based on video type (Shorts vs Long-form videos)
- **Strategy Pattern**: Different prediction algorithms for different content types
- **Observer Pattern**: Real-time system monitoring and alerting mechanisms
- **Singleton Pattern**: Configuration management and database connection management

---

## 3. Architectural Goals and Constraints

This section describes the software requirements and objectives that have some significant impact on the architecture; for example, safety, security, privacy, use of an off-the-shelf product, portability, distribution, and reuse. It also captures the special constraints that may apply: design and implementation strategy, development tools, team structure, schedule, legacy code, and so on.

### 3.1 Key Non-Functional Requirements

**Performance Requirements:**
- **Response Time**: Video predictions must be delivered within 30 seconds end-to-end
- **Throughput**: System must support minimum 10 concurrent users with 100+ predictions per hour
- **Scalability**: Architecture must support scaling to 100+ concurrent users for future growth
- **Availability**: 99.5% uptime during operational hours with graceful degradation capabilities

**Quality Attributes:**
- **Reliability**: MAPE < 30% for 7-day view forecasts (research-validated target for academic project)
- **Usability**: Intuitive interface with 5-minute learning curve for new users
- **Maintainability**: Modular design with 80%+ code coverage and comprehensive documentation
- **Security**: OWASP Top 10 compliance with secure authentication and data protection

**Compatibility Requirements:**
- **Cross-Platform**: Web-based interface accessible from any OS with modern browser
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Responsiveness**: Functional interface on tablets and mobile devices
- **API Compatibility**: RESTful design following OpenAPI 3.0 specifications

### 3.2 System Constraints

**Technical Constraints:**
- **API Limitations**: YouTube Data API v3 quota restrictions (10,000 units/day per key)
- **Processing Power**: Limited computational resources on free-tier cloud hosting
- **Memory Constraints**: 4GB RAM limitation for model loading and concurrent operations
- **Storage Limitations**: 20GB storage capacity on free-tier hosting services

**Development Constraints:**
- **Timeline**: 10-week development period with academic milestone requirements
- **Team Size**: Three-person development team with distributed skill sets
- **Budget**: Zero-cost approach utilizing free-tier services and open-source tools
- **Hardware**: Development limited to team laptops (Windows 11, Ubuntu 24.04)

**Regulatory Constraints:**
- **Data Privacy**: Compliance with YouTube API Terms of Service for data usage
- **Academic Ethics**: University of Moratuwa research ethics guidelines
- **Open Source**: GPL-compatible licensing for academic and community use
- **Security**: Basic security measures appropriate for academic project scope

### 3.3 Architectural Decisions

**ADR-001: Layered Architecture Selection**
- **Decision**: Adopt 5-layer architecture (Presentation, Application, Business Logic, Data Access, Data Storage)
- **Rationale**: Provides clear separation of concerns suitable for team collaboration and academic evaluation
- **Alternatives Considered**: Microservices (too complex), MVC (insufficient separation)
- **Consequences**: Enables parallel development, clear testing boundaries, potential performance overhead

**ADR-002: XGBoost Algorithm Selection**
- **Decision**: Use XGBoost for prediction models based on AMPS research validation
- **Rationale**: State-of-the-art performance on tabular data, robust to outliers, excellent feature importance
- **Alternatives Considered**: Random Forest (less accurate), Neural Networks (overly complex)
- **Consequences**: High accuracy potential, interpretable results, manageable computational requirements

---

## 4. Use-Case View

This section lists use cases or scenarios from the use-case model if they represent some significant, central functionality of the final system, or if they have a large architectural coverage—they exercise many architectural elements or if they stress or illustrate a specific, delicate point of the architecture.

The ViewTrendsSL system supports five primary use cases that represent the core functionality and architectural coverage:

1. **User Registration and Authentication** - Critical for system security and user management
2. **Generate Video Prediction** - Core system functionality exercising all major components
3. **Visualize Prediction Results** - Key user interface and data presentation capability
4. **System Data Collection** - Background process essential for model training and accuracy
5. **Model Training and Deployment** - Administrative function for system maintenance and improvement

### 4.1 Use-Case Realizations

This section illustrates how the software actually works by giving a few selected use-case (or scenario) realizations, and explains how the various design model elements contribute to their functionality.

**Use Case 1: User Registration and Authentication**

**Use case name:** User Registration and Authentication

**Actor:** Content Creator, Digital Marketer, Media Company Representative

**Description:** New users create accounts and existing users authenticate to access the ViewTrendsSL prediction services. This use case establishes secure user sessions and manages access control throughout the system.

**Preconditions:**
- User has access to a web browser with internet connectivity
- System is operational and accessible via HTTPS
- Database is available for user data storage

**Main flow:**
1. User navigates to ViewTrendsSL registration page
2. User enters email address, password, and confirmation password
3. System validates email format and password complexity requirements
4. System checks for existing account with same email address
5. System creates new user account with encrypted password hash
6. System sends email verification link to user's email address
7. User clicks verification link to activate account
8. User logs in with email and password credentials
9. System authenticates user and creates secure session token
10. User is redirected to main dashboard with active session

**Successful end/post condition:**
- User account is created and verified in the database
- User is authenticated with active session token
- User has access to prediction services and dashboard features

**Fail end/post condition:**
- User account is not created due to validation errors
- User receives clear error messages with corrective guidance
- System maintains security and prevents unauthorized access

**Extensions:**
- **3a**: Invalid email format → System displays validation error and input guidance
- **4a**: Email already exists → System provides login option or password reset
- **6a**: Email delivery fails → System provides alternative verification methods
- **9a**: Authentication fails → System implements lockout after multiple attempts

---

**Use Case 2: Generate Video Prediction (Primary Use Case)**

**Use case name:** Generate Video Prediction

**Actor:** Authenticated User (Primary), YouTube Data API (Secondary), Prediction Engine (Secondary)

**Description:** User submits a YouTube video URL and receives a comprehensive viewership forecast with interactive visualization showing predicted view counts at 24-hour, 7-day, and 30-day intervals. This use case exercises all major system components and represents the core value proposition.

**Preconditions:**
- User is authenticated and has active session
- User has remaining prediction quota for current period
- YouTube video URL is valid and publicly accessible
- Prediction models are loaded and operational
- YouTube Data API is accessible and within quota limits

**Main flow:**
1. User navigates to prediction dashboard
2. User enters YouTube video URL in input field
3. System validates URL format and extracts video ID
4. System calls YouTube Data API to retrieve video metadata
5. System extracts features (temporal, content, channel authority)
6. System determines video type (Shorts ≤60s vs Long-form >60s)
7. System selects appropriate trained model (XGBoost Shorts or Long-form)
8. System generates predictions for 24h, 7d, 30d intervals
9. System calculates confidence intervals and accuracy indicators
10. System renders interactive visualization with prediction curve
11. System displays video metadata and key prediction metrics
12. User views results and optionally exports or shares

**Successful end/post condition:**
- User receives accurate prediction with confidence indicators
- Prediction is logged for system improvement and caching
- User quota is decremented appropriately
- Results are cached for potential future requests

**Fail end/post condition:**
- User receives clear error message with suggested corrective actions
- System logs error details for debugging and system improvement
- User quota is not decremented for failed requests
- System maintains stability and continues serving other users

**Extensions:**
- **3a**: Invalid URL format → System displays validation error and input guidance
- **4a**: YouTube API error → System retries with exponential backoff, fallback to cached data
- **6a**: Insufficient metadata → System provides prediction with lower confidence indicator
- **8a**: Model inference error → System uses fallback model or provides error message
- **11a**: Visualization rendering error → System provides tabular results as fallback

---

## 5. Logical View

This section describes the architecturally significant parts of the design model, such as its decomposition into subsystems and packages. And for each significant package, its decomposition into classes and class utilities. You should introduce architecturally significant classes and describe their responsibilities, as well as a few very important relationships, operations, and attributes.

### 5.1 Overview

This subsection describes the overall decomposition of the design model in terms of its package hierarchy and layers.

The ViewTrendsSL system is decomposed into five primary subsystems organized in a layered architecture pattern. Each subsystem has distinct responsibilities and clear interfaces, enabling maintainable and scalable system design.

**System Decomposition:**
```
ViewTrendsSL System
├── Presentation Layer (Web Interface)
├── Application Layer (API Gateway)
├── Business Logic Layer (Core Services)
├── Data Access Layer (Repository Pattern)
└── Data Storage Layer (Database)
```

**Subsystem Organization:**
1. **Data Collection Subsystem**: YouTube API integration and data harvesting
2. **Machine Learning Subsystem**: Feature engineering, model training, and prediction inference
3. **Web Application Subsystem**: User interface, authentication, and session management
4. **Database Management Subsystem**: Data storage, retrieval, and integrity maintenance
5. **System Administration Subsystem**: Monitoring, logging, and maintenance operations

### 5.2 Architecturally Significant Design Packages

For each significant package, include a subsection with its name, its brief description, and a diagram with all significant classes and packages contained within the package. For each significant class in the package, include its name, brief description, and, optionally, a description of some of its major responsibilities, operations, and attributes.

**Package 1: Data Collection (`data_collection`)**

**Purpose:** Automated collection and preprocessing of YouTube video and channel metadata for model training and system operation.

**Key Classes:**
- **`YouTubeAPIClient`**: Manages API authentication, quota tracking, and request handling
  - **Responsibilities**: API key management, request rate limiting, error handling and retry logic
  - **Key Operations**: `fetch_video_metadata()`, `fetch_channel_info()`, `check_quota_usage()`
  - **Attributes**: `api_key`, `quota_remaining`, `request_count`

- **`ChannelCollector`**: Identifies and validates Sri Lankan YouTube channels
  - **Responsibilities**: Channel discovery, validation, and metadata collection
  - **Key Operations**: `discover_channels()`, `validate_sri_lankan_channel()`, `collect_channel_stats()`
  - **Attributes**: `channel_list`, `validation_criteria`, `collection_status`

- **`VideoCollector`**: Harvests video metadata from monitored channels
  - **Responsibilities**: Video discovery, metadata extraction, and batch processing
  - **Key Operations**: `collect_recent_videos()`, `extract_video_features()`, `batch_process()`
  - **Attributes**: `video_queue`, `processing_status`, `error_log`

- **`DataValidator`**: Ensures data quality and completeness
  - **Responsibilities**: Data validation, quality scoring, and error detection
  - **Key Operations**: `validate_video_data()`, `check_completeness()`, `generate_quality_report()`
  - **Attributes**: `validation_rules`, `quality_thresholds`, `error_counts`

**Design Patterns Applied:**
- **Factory Pattern**: `APIClientFactory` creates appropriate client instances for different API versions
- **Strategy Pattern**: Different collection strategies for channels vs videos
- **Observer Pattern**: `DataQualityMonitor` observes collection processes and reports issues

---

**Package 2: Machine Learning (`machine_learning`)**

**Purpose:** Feature engineering, model training, and prediction generation using XGBoost algorithms optimized for YouTube viewership forecasting.

**Key Classes:**
- **`FeatureExtractor`**: Transforms raw video metadata into model-ready features
  - **Responsibilities**: Feature engineering, data preprocessing, and normalization
  - **Key Operations**: `extract_temporal_features()`, `extract_content_features()`, `normalize_features()`
  - **Attributes**: `feature_definitions`, `preprocessing_pipeline`, `normalization_params`

- **`ModelTrainer`**: Handles XGBoost model training and evaluation
  - **Responsibilities**: Model training, hyperparameter tuning, and performance evaluation
  - **Key Operations**: `train_model()`, `evaluate_performance()`, `tune_hyperparameters()`
  - **Attributes**: `training_data`, `model_parameters`, `evaluation_metrics`

- **`PredictionEngine`**: Generates viewership forecasts using trained models
  - **Responsibilities**: Model inference, prediction generation, and confidence calculation
  - **Key Operations**: `predict_viewership()`, `calculate_confidence()`, `generate_forecast_curve()`
  - **Attributes**: `loaded_models`, `prediction_cache`, `confidence_thresholds`

- **`ModelManager`**: Manages model versioning and deployment
  - **Responsibilities**: Model storage, versioning, and deployment coordination
  - **Key Operations**: `save_model()`, `load_model()`, `deploy_model()`, `rollback_model()`
  - **Attributes**: `model_registry`, `version_history`, `deployment_status`

**Design Patterns Applied:**
- **Strategy Pattern**: `ModelStrategy` for Shorts vs Long-form models
- **Factory Pattern**: `ModelFactory` creates appropriate model instances based on video type
- **Template Method**: `TrainingPipeline` defines standard training workflow
- **Singleton Pattern**: `ModelRegistry` maintains single model instance registry

---

**Package 3: Web Application (`web_application`)**

**Purpose:** User interface, authentication, and API services providing the primary user interaction layer.

**Key Classes:**
- **`AuthenticationManager`**: Handles user registration, login, and session management
  - **Responsibilities**: User authentication, session management, and security enforcement
  - **Key Operations**: `register_user()`, `authenticate_user()`, `manage_session()`, `logout_user()`
  - **Attributes**: `user_sessions`, `security_config`, `authentication_tokens`

- **`PredictionController`**: Processes prediction requests and coordinates responses
  - **Responsibilities**: Request validation, service coordination, and response formatting
  - **Key Operations**: `handle_prediction_request()`, `validate_input()`, `format_response()`
  - **Attributes**: `request_queue`, `response_cache`, `error_handlers`

- **`VisualizationRenderer`**: Generates interactive charts and graphs
  - **Responsibilities**: Chart generation, data visualization, and interactive features
  - **Key Operations**: `render_prediction_chart()`, `create_interactive_graph()`, `export_visualization()`
  - **Attributes**: `chart_templates`, `visualization_config`, `export_formats`

- **`APIGateway`**: Manages REST API endpoints and request routing
  - **Responsibilities**: Request routing, API versioning, and rate limiting
  - **Key Operations**: `route_request()`, `apply_rate_limiting()`, `handle_api_versioning()`
  - **Attributes**: `route_definitions`, `rate_limits`, `api_versions`

**Design Patterns Applied:**
- **MVC Pattern**: Controllers, Models, and Views for web interface organization
- **Facade Pattern**: `APIGateway` provides simplified interface to backend services
- **Decorator Pattern**: Authentication and authorization decorators for endpoints
- **Command Pattern**: Request processing and validation commands

---

## 6. Process View

This section describes the system's decomposition into lightweight processes (single threads of control) and heavyweight processes (groupings of lightweight processes). Organize the section by groups of processes that communicate or interact. Describe the main modes of communication between processes, such as message passing, interrupts, and rendezvous.

**Primary System Processes:**

**1. Web Server Process (Main Application Thread)**
- **Purpose**: Handles HTTP requests and responses, manages user sessions
- **Threading Model**: Single-threaded with async I/O for concurrent request handling
- **Communication**: HTTP/HTTPS with clients, database connections, internal API calls
- **Responsibilities**: Request routing, authentication, session management, response coordination

**2. Data Collection Process (Background Service)**
- **Purpose**: Scheduled YouTube API data harvesting and preprocessing
- **Threading Model**: Multi-threaded for parallel API calls and data processing
- **Communication**: YouTube API calls, database writes, internal messaging
- **Responsibilities**: Automated data collection, validation, and storage

**3. Model Inference Process (On-Demand Service)**
- **Purpose**: Feature extraction and prediction generation for user requests
- **Threading Model**: Single-threaded per request with process pooling for scalability
- **Communication**: Synchronous calls from web server, database reads, model loading
- **Responsibilities**: Feature engineering, model inference, result caching

**4. System Monitoring Process (Background Service)**
- **Purpose**: Performance metrics collection, error logging, and health monitoring
- **Threading Model**: Single-threaded with periodic execution and event-driven alerts
- **Communication**: Log file writes, database monitoring, external alerting services
- **Responsibilities**: System health tracking, performance monitoring, alert generation

**Process Communication Patterns:**
- **Synchronous API Calls**: Web application to machine learning subsystem for real-time predictions
- **Asynchronous Messaging**: Data collection to database storage for batch operations
- **Event-Driven Updates**: System monitoring and alerting based on system events
- **Batch Processing**: Model training and data preprocessing during off-peak hours

**Figure 1. Process Interaction Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Server    │    │ Data Collection │    │ Model Inference │
│    Process      │◄──►│    Process      │◄──►│    Process      │
│  (Main Thread)  │    │ (Multi-Thread)  │    │ (Process Pool)  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │              ┌───────▼───────┐              │
          │              │   Database    │              │
          └─────────────►│   Storage     │◄─────────────┘
                         │   Process     │
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │ System Monitor│
                         │   Process     │
                         └───────────────┘
```

Figure 1 illustrates the main process interactions in the ViewTrendsSL system. The Web Server Process handles user requests and coordinates with other processes. The Data Collection Process runs independently to gather YouTube data. The Model Inference Process generates predictions on-demand. All processes interact with the Database Storage Process, while the System Monitor Process observes overall system health.

**Sequence Diagram: User Prediction Request Flow**

**Figure 2. Prediction Request Sequence**
```
User → WebApp → APIGateway → PredictionController → YouTubeAPI → FeatureExtractor → PredictionEngine → Database → WebApp → User

1. User submits video URL
2. WebApp validates authentication and session
3. APIGateway routes request to PredictionController
4. PredictionController calls YouTubeAPI for metadata
5. FeatureExtractor processes raw data into model features
6. PredictionEngine generates forecast using appropriate model
7. Database stores prediction for caching and analytics
8. WebApp renders interactive visualization
9. User receives prediction results with confidence indicators
```

Figure 2 shows the complete sequence of interactions when a user requests a video prediction. The process involves multiple system components working together to deliver accurate forecasts with appropriate visualizations.

---

## 7. Deployment View

This section describes one or more physical network (hardware) configurations on which the software is deployed and run. It is a view of the Deployment Model. At a minimum for each configuration it should indicate the physical nodes (computers, CPUs) that execute the software and their interconnections (bus, LAN, point-to-point, and so on.) Also include a mapping of the processes of the Process View onto the physical nodes.

**Target Deployment Environment: Cloud Platform (Heroku/PythonAnywhere)**

**Deployment Architecture:**

**Figure 3. Physical Deployment Architecture**
```
┌─────────────────────────────────────────────────────────────────┐
│                        Internet                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTPS/TLS 1.3
┌─────────────────────▼───────────────────────────────────────────┐
│                 Load Balancer / CDN                             │
│                 (Cloud Provider)                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/HTTPS
┌─────────────────────▼───────────────────────────────────────────┐
│                 Web Server Instance                             │
│                 (2 vCPU, 4GB RAM, 20GB SSD)                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Docker Container                               ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ ││
│  │  │    Flask    │  │   XGBoost   │  │    Static Files     │ ││
│  │  │ Application │  │   Models    │  │   (CSS/JS/Images)   │ ││
│  │  │   (Gunicorn)│  │  (Joblib)   │  │                     │ ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────────────┘
                      │ PostgreSQL Protocol
┌─────────────────────▼───────────────────────────────────────────┐
│                PostgreSQL Database                              │
│                (1 vCPU, 2GB RAM, 10GB SSD)                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Channels │ Videos │ Snapshots │ Users │ Predictions        ││
│  │  Tables with Indexes and Constraints                       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                External Services                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  YouTube Data   │  │   Monitoring    │  │     Backup      │ │
│  │     API v3      │  │    Service      │  │    Service      │ │
│  │  (Google APIs)  │  │  (Cloud Logs)   │  │ (Automated DB)  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

Figure 3 shows the complete deployment architecture for ViewTrendsSL. The system uses a cloud-based deployment with load balancing, containerized application hosting, managed database services, and external API integrations.

**Hardware Specifications:**

**Production Server Node:**
- **CPU**: 2 vCPU cores minimum (Intel/AMD equivalent)
- **Memory**: 4GB RAM minimum (8GB recommended for optimal performance)
- **Storage**: 20GB SSD (10GB application, 10GB temporary files)
- **Network**: High-speed internet with 99.9% uptime SLA
- **Operating System**: Linux-based container runtime (Docker)

**Database Server Node:**
- **CPU**: 1 vCPU dedicated for database operations
- **Memory**: 2GB RAM for query caching and connection pooling
- **Storage**: 10GB SSD with automatic scaling capability
- **IOPS**: 3000 IOPS for concurrent read/write operations
- **Backup**: Automated daily backups with 30-day retention

**Process Mapping to Physical Nodes:**

**Web Server Instance:**
- Web Server Process (Flask/Gunicorn)
- Model Inference Process (XGBoost prediction)
- System Monitoring Process (logging and metrics)
- Static File Serving (CSS, JavaScript, images)

**Database Server Instance:**
- Database Storage Process (PostgreSQL)
- Backup Process (automated daily backups)
- Connection Management (connection pooling)

**External Services:**
- Data Collection Process (YouTube API integration)
- Monitoring Services (cloud-based logging and alerting)
- Email Services (user verification and notifications)

**Network Interconnections:**
- **Client to Load Balancer**: HTTPS over internet (TLS 1.3 encryption)
- **Load Balancer to Web Server**: HTTP/HTTPS over private network
- **Web Server to Database**: PostgreSQL protocol over encrypted connection
- **Web Server to External APIs**: HTTPS REST calls with API key authentication
- **Monitoring**: Cloud logging and metrics collection via secure channels

---

## 8. Implementation View

This section describes the overall structure of the implementation model, the decomposition of the software into layers and subsystems in the implementation model, and any architecturally significant components.

### 8.1 Overview

This subsection names and defines the various layers and their contents, the rules that govern the inclusion to a given layer, and the boundaries between layers. Include a component diagram that shows the relations between layers.

**5-Layer Architecture Implementation:**

The ViewTrendsSL system implements a strict layered architecture with five distinct layers, each with specific responsibilities and clear boundaries. Dependencies flow downward only, ensuring maintainable and testable system design.

**Layer Definitions and Rules:**

**Layer 1: Presentation Layer**
- **Technology**: Streamlit (primary) or HTML/CSS/JavaScript (alternative)
- **Responsibility**: User interface rendering, user input handling, result visualization
- **Inclusion Rules**: Only UI components, no business logic or data access
- **Components**: Dashboard pages, authentication forms, interactive charts, static assets
- **Boundary**: Communicates only with Application Layer via HTTP/REST

**Layer 2: Application Layer (API Gateway)**
- **Technology**: Flask REST API with Gunicorn WSGI server
- **Responsibility**: HTTP request handling, routing, authentication, session management
- **Inclusion Rules**: Request/response handling, no business logic implementation
- **Components**: API endpoints, middleware, request validation, authentication handlers
- **Boundary**: Receives from Presentation, delegates to Business Logic Layer

**Layer 3: Business Logic Layer**
- **Technology**: Python modules with XGBoost, Pandas, NumPy
- **Responsibility**: Core business logic, feature engineering, model inference
- **Inclusion Rules**: Domain logic only, no UI concerns or data persistence details
- **Components**: Prediction engine, data processing, model management, business rules
- **Boundary**: Called by Application Layer, uses Data Access Layer for persistence

**Layer 4: Data Access Layer**
- **Technology**: SQLAlchemy ORM with PostgreSQL drivers
- **Responsibility**: Database operations, query optimization, transaction management
- **Inclusion Rules**: Data persistence only, no business logic or UI concerns
- **Components**: Repository classes, database models, connection management, query builders
- **Boundary**: Serves Business Logic Layer, communicates with Data Storage Layer

**Layer 5: Data Storage Layer**
- **Technology**: PostgreSQL database with automated backups
- **Responsibility**: Persistent data storage, data integrity, backup/recovery
- **Inclusion Rules**: Pure data storage, constraints, and database-level operations
- **Components**: Database tables, indexes, constraints, stored procedures, triggers
- **Boundary**: Accessed only through Data Access Layer

**Figure 4. Layer Component Diagram**
```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Streamlit  │  │    HTML     │  │    Interactive         │ │
│  │  Dashboard  │  │  Templates  │  │    Charts (Plotly)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/REST API Calls
┌─────────────────────▼───────────────────────────────────────────┐
│                  Application Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │    Flask    │  │    API      │  │    Authentication      │ │
│  │   Routes    │  │  Gateway    │  │     Middleware         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Function Calls
┌─────────────────────▼───────────────────────────────────────────┐
│                 Business Logic Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Prediction  │  │   Feature   │  │      Model             │ │
│  │  Service    │  │ Engineering │  │   Management           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Repository Pattern
┌─────────────────────▼───────────────────────────────────────────┐
│                  Data Access Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Video     │  │   Channel   │  │       User             │ │
│  │ Repository  │  │ Repository  │  │    Repository          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ SQL/ORM Queries
┌─────────────────────▼───────────────────────────────────────────┐
│                  Data Storage Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ PostgreSQL  │  │   Indexes   │  │     Constraints        │ │
│  │   Tables    │  │    & Keys   │  │    & Triggers          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

Figure 4 illustrates the five-layer architecture with clear separation of concerns and unidirectional dependencies flowing from top to bottom.

### 8.2 Layers

For each layer, include a subsection with its name, an enumeration of the subsystems located in the layer, and a component diagram.

**Layer 1: Presentation Layer Components**

**Subsystems:**
- **Streamlit Dashboard**: Main user interface for prediction requests and results
- **HTML Templates**: Alternative web interface components (if Flask templates used)
- **Static Assets**: CSS stylesheets, JavaScript files, images, and fonts
- **Interactive Visualizations**: Plotly charts and graphs for prediction display

**Key Components:**
- `streamlit_app.py`: Main dashboard application
- `pages/`: Individual page components (login, dashboard, results)
- `static/css/`: Stylesheet files for visual design
- `static/js/`: JavaScript for interactive features
- `components/`: Reusable UI components

---

**Layer 2: Application Layer Components**

**Subsystems:**
- **Flask Application**: Web server and request handling
- **API Gateway**: REST endpoint management and routing
- **Authentication Middleware**: User authentication and session management
- **Request Validation**: Input validation and sanitization

**Key Components:**
- `app.py`: Main Flask application entry point
- `api/routes.py`: API endpoint definitions
- `middleware/auth.py`: Authentication middleware
- `middleware/validation.py`: Request validation middleware
- `api/error_handlers.py`: Error handling and response formatting

---

**Layer 3: Business Logic Layer Components**

**Subsystems:**
- **Prediction Service**: Core prediction logic and model coordination
- **Feature Engineering Service**: Data preprocessing and feature extraction
- **Model Management Service**: Model loading, versioning, and deployment
- **Data Processing Service**: YouTube data processing and validation

**Key Components:**
- `services/prediction_service.py`: Main prediction orchestration
- `services/feature_service.py`: Feature engineering pipeline
- `services/model_service.py`: Model management and inference
- `ml/prediction_engine.py`: XGBoost model inference
- `utils/data_processor.py`: Data cleaning and preprocessing

---

**Layer 4: Data Access Layer Components**

**Subsystems:**
- **Repository Pattern Implementation**: Data access abstraction
- **Database Connection Management**: Connection pooling and transaction handling
- **Query Optimization**: Efficient database queries and caching
- **Data Mapping**: ORM configuration and entity mapping

**Key Components:**
- `repositories/video_repository.py`: Video data operations
- `repositories/channel_repository.py`: Channel data operations
- `repositories/user_repository.py`: User account operations
- `repositories/prediction_repository.py`: Prediction caching operations
- `database/models.py`: SQLAlchemy ORM models
- `database/connection.py`: Database connection management

---

**Layer 5: Data Storage Layer Components**

**Subsystems:**
- **PostgreSQL Database**: Primary data storage system
- **Database Schema**: Table definitions, relationships, and constraints
- **Indexing Strategy**: Performance optimization through strategic indexing
- **Backup and Recovery**: Automated backup and disaster recovery systems

**Key Components:**
- **Tables**: `channels`, `videos`, `snapshots`, `users`, `predictions`
- **Indexes**: Composite indexes on frequently queried columns
- **Constraints**: Foreign key relationships and data integrity rules
- **Triggers**: Automated data validation and audit logging

---

## 9. Data View (Optional)

This section describes the persistent data in the system and includes a description of this data. Significant and architecturally relevant persistent data should be described. This includes files, databases, and repositories.

**Database Schema Overview:**

The ViewTrendsSL system uses a PostgreSQL relational database designed for efficient storage and retrieval of YouTube metadata, user information, and prediction results. The schema is optimized for the specific query patterns required by the machine learning pipeline and web application.

**Figure 5. Entity-Relationship Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Users       │    │    Channels     │    │     Videos      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ user_id (PK)    │    │ channel_id (PK) │    │ video_id (PK)   │
│ email           │    │ channel_name    │    │ channel_id (FK) │
│ password_hash   │    │ subscriber_count│    │ title           │
│ created_at      │    │ video_count     │    │ description     │
│ last_login      │    │ country         │    │ published_at    │
│ is_active       │    │ created_at      │    │ duration        │
└─────────────────┘    └─────────────────┘    │ category_id     │
                                              │ is_short        │
                                              │ view_count      │
                                              │ like_count      │
                                              │ comment_count   │
                                              └─────────────────┘
                                                       │
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Predictions   │    │    Snapshots    │    │      Tags       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ prediction_id   │    │ snapshot_id (PK)│    │ tag_id (PK)     │
│ user_id (FK)    │    │ video_id (FK)   │    │ tag_name        │
│ video_id (FK)   │    │ timestamp       │    └─────────────────┘
│ predicted_24h   │    │ view_count      │             │
│ predicted_7d    │    │ like_count      │             │
│ predicted_30d   │    │ comment_count   │    ┌─────────────────┐
│ confidence      │    │ created_at      │    │   Video_Tags    │
│ created_at      │    └─────────────────┘    ├─────────────────┤
└─────────────────┘                          │ video_id (FK)   │
                                              │ tag_id (FK)     │
                                              └─────────────────┘
```

Figure 5 shows the complete database schema with primary keys (PK), foreign keys (FK), and relationships between entities. The design supports efficient querying for both real-time predictions and historical analysis.

**Table Specifications:**

**Channels Table:**
- **Purpose**: Stores Sri Lankan YouTube channel metadata and statistics
- **Key Indexes**: Primary key on `channel_id`, index on `country` for filtering
- **Data Volume**: ~500-1000 channels for MVP scope
- **Update Frequency**: Weekly batch updates for subscriber counts and statistics

**Videos Table:**
- **Purpose**: Stores individual video metadata and current statistics
- **Key Indexes**: Primary key on `video_id`, composite index on `(channel_id, published_at)`
- **Data Volume**: ~50,000-100,000 videos for comprehensive training dataset
- **Update Frequency**: Daily updates for view counts, likes, and comments

**Snapshots Table:**
- **Purpose**: Time-series data tracking video performance over time
- **Key Indexes**: Composite index on `(video_id, timestamp)` for efficient time-series queries
- **Data Volume**: ~1-5 million records (multiple snapshots per video over time)
- **Update Frequency**: Hourly or daily snapshots for active video monitoring

**Users Table:**
- **Purpose**: User account management and authentication
- **Key Indexes**: Primary key on `user_id`, unique index on `email`
- **Data Volume**: ~100-1000 users for MVP deployment
- **Update Frequency**: Real-time updates for login activity and preferences

**Predictions Table:**
- **Purpose**: Caches prediction results for performance and analytics
- **Key Indexes**: Composite index on `(user_id, video_id)`, index on `created_at`
- **Data Volume**: ~10,000-50,000 prediction records
- **Update Frequency**: Real-time inserts for new predictions, periodic cleanup

**Data Flow Patterns:**

**1. Data Collection Flow:**
```
YouTube API → Raw JSON → Data Validation → Feature Extraction → Database Storage
```

**2. Prediction Generation Flow:**
```
User Request → Video Metadata Fetch → Feature Engineering → Model Inference → Result Caching → Response
```

**3. Model Training Flow:**
```
Historical Data → Feature Engineering → Train/Test Split → Model Training → Model Validation → Model Deployment
```

---

## 10. Size and Performance

This section describes the major dimensioning characteristics of the software that impact the architecture, as well as the target performance constraints.

**System Dimensioning:**

**Data Volume Projections:**
- **Training Dataset**: 50,000-100,000 Sri Lankan YouTube videos with complete metadata
- **Time-Series Data**: 1-5 million snapshot records tracking video performance over time
- **User Base**: 100-1,000 registered users for MVP deployment phase
- **Daily Predictions**: 500-2,000 prediction requests during peak usage periods
- **Database Size**: 5-20 GB total storage including indexes and temporary data

**Performance Requirements:**

**Response Time Targets:**
- **Video Prediction**: ≤ 30 seconds end-to-end (including API calls and model inference)
- **Dashboard Loading**: ≤ 5 seconds for authenticated user dashboard
- **User Authentication**: ≤ 2 seconds for login/logout operations
- **Data Visualization**: ≤ 10 seconds for interactive chart rendering
- **API Endpoints**: ≤ 3 seconds for standard REST API responses

**Throughput Specifications:**
- **Concurrent Users**: 10-50 simultaneous users with acceptable performance degradation
- **Prediction Capacity**: 100+ predictions per hour during peak usage
- **Data Collection**: 1,000+ API calls per hour for background data harvesting
- **Database Operations**: 500+ queries per minute with sub-second response times

**Scalability Considerations:**

**Horizontal Scaling Potential:**
- **Web Application**: Stateless design enables multiple server instances behind load balancer
- **Database**: Read replicas for query performance, connection pooling for concurrent access
- **Model Inference**: Process pooling and caching strategies for prediction scalability
- **Static Assets**: CDN integration for global content delivery and reduced server load

**Performance Optimization Strategies:**
- **Caching**: Redis-based caching for frequently requested predictions and metadata
- **Database Indexing**: Strategic composite indexes on high-frequency query patterns
- **Model Optimization**: Lightweight XGBoost models with optimized hyperparameters
- **API Rate Limiting**: Intelligent quota management for YouTube API integration
- **Asynchronous Processing**: Background tasks for data collection and model training

**Resource Utilization Monitoring:**
- **CPU Usage**: Target ≤ 70% average utilization with burst capacity to 90%
- **Memory Usage**: Target ≤ 80% RAM utilization with efficient garbage collection
- **Disk I/O**: Optimized database queries and SSD storage for performance
- **Network Bandwidth**: Efficient API usage and compressed data transfer

---

## 11. Quality

This section describes how the software architecture contributes to all capabilities (other than functionality) of the system: extensibility, reliability, portability, and so forth. If these characteristics have special significance, such as safety, security or privacy implications, they should be clearly described.

**Quality Attributes Implementation:**

**Security Architecture:**
- **Authentication**: JWT-based session management with secure password hashing (bcrypt)
- **Authorization**: Role-based access control with user permission validation
- **Data Protection**: HTTPS/TLS encryption for all client-server communication
- **API Security**: Rate limiting, input validation, and SQL injection prevention
- **Privacy Compliance**: YouTube API Terms of Service adherence and user data protection

**Reliability and Fault Tolerance:**
- **Error Handling**: Comprehensive exception handling with graceful degradation
- **Data Integrity**: Database constraints, transaction management, and backup strategies
- **Service Resilience**: Retry mechanisms for external API calls with exponential backoff
- **Monitoring**: Real-time system health monitoring with automated alerting
- **Recovery**: Automated backup systems with point-in-time recovery capabilities

**Maintainability and Extensibility:**
- **Modular Design**: Clear separation of concerns through layered architecture
- **Code Quality**: PEP-8 compliance, comprehensive documentation, and unit testing
- **Version Control**: Git-based development with feature branching and code reviews
- **Configuration Management**: Environment-based configuration with Docker containerization
- **API Design**: RESTful interfaces enabling future integration and extension

**Performance and Scalability:**
- **Caching Strategy**: Multi-level caching for database queries and prediction results
- **Database Optimization**: Strategic indexing and query optimization for performance
- **Resource Management**: Efficient memory usage and connection pooling
- **Load Distribution**: Stateless application design enabling horizontal scaling
- **Monitoring**: Performance metrics collection and bottleneck identification

**Portability and Compatibility:**
- **Cross-Platform**: Docker containerization ensuring consistent deployment environments
- **Browser Compatibility**: Modern web standards supporting major browser versions
- **Database Portability**: SQLAlchemy ORM enabling database engine flexibility
- **Cloud Agnostic**: Architecture supporting multiple cloud deployment platforms
- **API Standards**: RESTful design following industry best practices

**Usability and Accessibility:**
- **User Interface**: Intuitive design with minimal learning curve requirements
- **Responsive Design**: Mobile-friendly interface supporting various screen sizes
- **Error Messages**: Clear, actionable error messages with user guidance
- **Documentation**: Comprehensive user guides and API documentation
- **Performance Feedback**: Real-time progress indicators for long-running operations

**Testing and Quality Assurance:**
- **Unit Testing**: Comprehensive test coverage for individual components
- **Integration Testing**: End-to-end testing of system workflows and API integrations
- **Performance Testing**: Load testing and performance benchmarking
- **Security Testing**: Vulnerability assessment and penetration testing
- **User Acceptance Testing**: Stakeholder validation and usability testing

---

## 12. References

This section provides a complete list of all documents and resources referenced in the Software Architecture Document, organized by category for easy reference and verification.

**Academic Literature and Research Papers:**
1. Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.
2. Kumar, S., et al. (2024). "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms." *Journal of Retailing and Consumer Services*, 78, 103-115.
3. Zhang, L., et al. (2025). "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity." *arXiv preprint arXiv:2503.04446v1*.
4. IEEE Computer Society. (2000). "IEEE Recommended Practice for Architectural Description of Software-Intensive Systems." *IEEE Std 1471-2000*.
5. ISO/IEC. (2011). "Systems and Software Quality Requirements and Evaluation (SQuaRE) - System and Software Quality Models." *ISO/IEC 25010:2011*.

**Technical Documentation and API References:**
6. Google Developers. (2024). "YouTube Data API v3 Documentation." Retrieved from https://developers.google.com/youtube/v3
7. Pallets Projects. (2024). "Flask Web Development Framework Documentation." Retrieved from https://flask.palletsprojects.com/
8. XGBoost Developers. (2024). "XGBoost Documentation - Python API Reference." Retrieved from https://xgboost.readthedocs.io/
9. PostgreSQL Global Development Group. (2024). "PostgreSQL Documentation." Retrieved from https://www.postgresql.org/docs/
10. SQLAlchemy Project. (2024). "SQLAlchemy Documentation - The Database Toolkit for Python." Retrieved from https://docs.sqlalchemy.org/

**Development Tools and Frameworks:**
11. Docker Inc. (2024). "Docker Documentation - Containerization Platform." Retrieved from https://docs.docker.com/
12. Plotly Technologies Inc. (2024). "Plotly Python Documentation - Interactive Visualization." Retrieved from https://plotly.com/python/
13. Streamlit Inc. (2024). "Streamlit Documentation - Data App Framework." Retrieved from https://docs.streamlit.io/
14. Pandas Development Team. (2024). "Pandas Documentation - Data Analysis Library." Retrieved from https://pandas.pydata.org/docs/
15. NumPy Developers. (2024). "NumPy Documentation - Scientific Computing." Retrieved from https://numpy.org/doc/

**Architectural and Design Resources:**
16. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
17. Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice* (3rd ed.). Addison-Wesley Professional.
18. Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley Professional.
19. Newman, S. (2015). *Building Microservices: Designing Fine-Grained Systems*. O'Reilly Media.
20. Richardson, C. (2018). *Microservices Patterns: With Examples in Java*. Manning Publications.

**Diagram Creation and Documentation Tools:**
- **Draw.io (app.diagrams.net)**: Used for creating architectural diagrams, system topology diagrams, and component relationship visualizations
- **PlantUML**: Used for generating UML sequence diagrams, component diagrams, and process flow visualizations
- **dbdiagram.io**: Used for Entity-Relationship Diagram creation and database schema visualization
- **Mermaid**: Used for creating flowcharts and process diagrams embedded in documentation

**University and Project Resources:**
21. University of Moratuwa. (2024). "In22-S5-CS3501 - Data Science and Engineering Project Guidelines." Department of Computer Science and Engineering.
22. ViewTrendsSL Project Team. (2025). "Project Plan and Requirements Specification." University of Moratuwa Academic Project Documentation.
23. ViewTrendsSL Project Team. (2025). "Software Requirements Specification." University of Moratuwa Academic Project Documentation.

---

**Document Information:**
- **Total Pages**: 47
- **Word Count**: ~15,000 words
- **Figures**: 5 architectural diagrams
- **Last Updated**: August 6, 2025
- **Document Version**: 1.0
- **Review Status**: Initial Draft for Academic Review

---

