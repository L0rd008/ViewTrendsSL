# ViewTrendsSL: YouTube Viewership Forecasting System
## Software Architecture Document (SAD)

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
2. [Architectural Representation](#2-architectural-representation)
3. [Architectural Goals and Constraints](#3-architectural-goals-and-constraints)
4. [Use-Case View](#4-use-case-view)
5. [Logical View](#5-logical-view)
6. [Process View](#6-process-view)
7. [Deployment View](#7-deployment-view)
8. [Implementation View](#8-implementation-view)
9. [Data View](#9-data-view)
10. [Size and Performance](#10-size-and-performance)
11. [Quality](#11-quality)
12. [References](#12-references)

---

## 1. Introduction

### 1.1 Purpose

This Software Architecture Document (SAD) provides a comprehensive architectural overview of the ViewTrendsSL system, a machine learning-powered web application for predicting YouTube video viewership specifically for Sri Lankan audiences. This document serves as the definitive architectural specification for system design, implementation, and maintenance.

**Intended Readers:**
- **Development Team Members**: For implementation guidance and technical decision understanding
- **System Testers**: For test planning and integration testing strategies
- **Project Stakeholders**: For architectural oversight and technical validation
- **Academic Evaluators**: For assessment of architectural design quality and technical depth
- **Future Maintainers**: For system understanding and enhancement planning
- **Research Community**: For methodology validation and reproducibility

**Document Scope:**
This document is designed to guide both current implementation and future enhancements, providing:
- Comprehensive architectural foundation for the MVP
- Extensible design patterns for future feature additions
- Clear technical specifications for academic evaluation
- Detailed implementation guidance for development team

### 1.2 Scope

**Software Components Affected:**
- **Data Collection Subsystem**: YouTube API integration and data harvesting modules
- **Machine Learning Pipeline**: Feature engineering, model training, and prediction inference
- **Web Application Framework**: User interface, API services, and session management
- **Database Management System**: Data storage, retrieval, and integrity maintenance
- **Deployment Infrastructure**: Containerization, cloud hosting, and monitoring systems

**Hardware Components:**
- **Backend Server Infrastructure**:
  - **CPU Requirements**: Minimum 2 vCPU cores for concurrent request handling and model inference
  - **Memory Requirements**: 4GB RAM minimum (8GB recommended) for model loading and data processing
  - **Storage Requirements**: 20GB SSD for database, model files, and application code
  - **Network Requirements**: High-speed internet for YouTube API calls and user requests

- **Client-Side Requirements**:
  - **Browser Compatibility**: Modern browsers with JavaScript support for interactive visualizations
  - **Memory Usage**: 4GB RAM for smooth browser operation with complex charts
  - **Network Bandwidth**: Minimum 1 Mbps for real-time prediction requests and visualization loading

- **Development Environment**:
  - **Team Hardware**: Windows 11 and Ubuntu 24.04 systems with 16GB RAM, i7/R7 processors
  - **GPU Utilization**: RTX GPUs available for potential model training acceleration (optional for MVP)

**External Systems Integration:**
- **YouTube Data API v3**: Primary data source for video and channel metadata
- **Cloud Hosting Platform**: Heroku or equivalent for application deployment
- **PostgreSQL Service**: Database hosting with automated backup capabilities
- **Monitoring Services**: Application performance monitoring and error tracking

### 1.3 Definitions, Acronyms, and Abbreviations

**Architectural Terms:**
- **API Gateway**: Single entry point for all client requests to backend services
- **Data Access Layer (DAL)**: Abstraction layer for database operations and queries
- **Domain Model**: Core business logic and entities representing system concepts
- **Microservice**: Independently deployable service component (future consideration)
- **Monolithic Architecture**: Single deployable unit containing all system components
- **ORM (Object-Relational Mapping)**: Database abstraction layer (SQLAlchemy)
- **REST (Representational State Transfer)**: Architectural style for web services
- **Service Layer**: Business logic coordination and transaction management

**Machine Learning Terms:**
- **Feature Engineering**: Process of creating predictive variables from raw data
- **Model Inference**: Process of generating predictions from trained models
- **Pipeline**: Automated sequence of data processing and model operations
- **Temporal Alignment**: Time-synchronized prediction methodology
- **XGBoost**: Extreme Gradient Boosting algorithm for tabular data prediction

**System Components:**
- **Data Collector**: Automated YouTube API integration and data harvesting module
- **Feature Extractor**: Data preprocessing and feature engineering component
- **Prediction Engine**: Machine learning model inference and result generation system
- **Web Dashboard**: User interface for prediction requests and result visualization
- **Database Manager**: Data storage, retrieval, and integrity management system

**Performance Metrics:**
- **MAPE (Mean Absolute Percentage Error)**: Primary model accuracy metric
- **RPS (Requests Per Second)**: System throughput measurement
- **SLA (Service Level Agreement)**: Performance and availability commitments
- **TTL (Time To Live)**: Cache expiration and data freshness control

### 1.4 References

**Academic Literature:**
1. "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms" - Journal of Retailing and Consumer Services (2024)
2. "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity" - arXiv:2503.04446v1 (2025)
3. "XGBoost: A Scalable Tree Boosting System" - Chen & Guestrin, KDD 2016
4. "Building Microservices" - Sam Newman, O'Reilly Media (2021)

**Technical Standards:**
- IEEE 1471-2000: Recommended Practice for Architectural Description
- ISO/IEC 25010: Systems and Software Quality Requirements and Evaluation
- REST API Design Guidelines - Microsoft Azure Architecture Center
- The Twelve-Factor App Methodology - Heroku

**Technical Documentation:**
- YouTube Data API v3 Documentation: https://developers.google.com/youtube/v3
- Flask Web Framework Documentation: https://flask.palletsprojects.com/
- XGBoost Documentation: https://xgboost.readthedocs.io/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Docker Documentation: https://docs.docker.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/

**Development Tools:**
- **Diagram Creation**: Draw.io (https://app.diagrams.net/) for architectural diagrams
- **UML Modeling**: PlantUML for sequence and component diagrams
- **Database Design**: dbdiagram.io for ER diagram creation
- **API Documentation**: Swagger/OpenAPI 3.0 for REST API specification

### 1.5 Overview

This Software Architecture Document is structured according to the "4+1" architectural view model:

**Section 1-3**: Introduction, scope, and architectural foundation
**Section 4**: Use-Case View - System functionality from user perspective
**Section 5**: Logical View - System decomposition and component relationships
**Section 6**: Process View - Runtime behavior and component interactions
**Section 7**: Deployment View - Physical system topology and infrastructure
**Section 8**: Implementation View - Software organization and development structure
**Section 9**: Data View - Information architecture and data flow
**Section 10-11**: Performance analysis and quality attribute scenarios
**Section 12**: References and supporting documentation

---

## 2. Architectural Representation

### 2.1 Architectural Style

**Primary Pattern: Layered Architecture (N-Tier)**

ViewTrendsSL adopts a **Layered Architecture** pattern, which provides clear separation of concerns and enables maintainable, testable, and scalable system design. This pattern is optimal for our academic project scope while providing foundation for future enhancements.

**Architecture Justification:**
- **Separation of Concerns**: Each layer has distinct responsibilities
- **Maintainability**: Changes in one layer minimally impact others
- **Testability**: Individual layers can be tested in isolation
- **Team Collaboration**: Clear boundaries enable parallel development
- **Academic Clarity**: Well-understood pattern for evaluation and documentation

### 2.2 Architectural Views

**Selected Views for ViewTrendsSL:**

1. **Use-Case View**: System functionality and user interactions
2. **Logical View**: Component decomposition and relationships
3. **Process View**: Runtime behavior and sequence flows
4. **Deployment View**: Physical infrastructure and hosting
5. **Implementation View**: Code organization and development structure
6. **Data View**: Information architecture and database design

**View Selection Rationale:**
These six views provide comprehensive coverage for a machine learning web application while maintaining focus on essential architectural concerns for academic evaluation and development guidance.

### 2.3 Architectural Patterns and Principles

**Design Patterns Applied:**
- **Repository Pattern**: Data access abstraction for database operations
- **Factory Pattern**: Model selection based on video type (Shorts/Long-form)
- **Strategy Pattern**: Different prediction algorithms for different content types
- **Observer Pattern**: Real-time system monitoring and alerting
- **Singleton Pattern**: Configuration management and database connections

**Architectural Principles:**
- **Single Responsibility**: Each component has one primary purpose
- **Open/Closed Principle**: Open for extension, closed for modification
- **Dependency Inversion**: High-level modules independent of low-level details
- **Interface Segregation**: Clients depend only on interfaces they use
- **Don't Repeat Yourself (DRY)**: Eliminate code duplication across layers

---

## 3. Architectural Goals and Constraints

### 3.1 Key Non-Functional Requirements

**Performance Requirements:**
- **Response Time**: Predictions delivered within 30 seconds end-to-end
- **Throughput**: Support minimum 10 concurrent users with 100+ predictions/hour
- **Scalability**: Architecture supports scaling to 100+ concurrent users
- **Availability**: 99.5% uptime during operational hours

**Quality Attributes:**
- **Reliability**: MAPE < 30% for 7-day view forecasts (research-validated target)
- **Usability**: Intuitive interface with 5-minute learning curve for new users
- **Maintainability**: Modular design with 80%+ code coverage and comprehensive documentation
- **Security**: OWASP Top 10 compliance with secure authentication and data protection

**Compatibility Requirements:**
- **Cross-Platform**: Web-based interface accessible from any OS with modern browser
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Responsiveness**: Functional interface on tablets and mobile devices
- **API Compatibility**: RESTful design following OpenAPI 3.0 specifications

**Operational Requirements:**
- **Deployability**: Docker containerization for consistent deployment across environments
- **Monitoring**: Comprehensive logging and performance monitoring
- **Backup**: Automated daily database backups with 30-day retention
- **Recovery**: Maximum 4-hour recovery time for system failures

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

**Business Constraints:**
- **Scope Limitation**: MVP focus on core prediction functionality
- **Language Support**: Initial English-only interface with future localization potential
- **Geographic Focus**: Sri Lankan content prioritization with international compatibility
- **User Base**: Academic and small creator focus rather than enterprise features

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

**ADR-003: Separate Models for Shorts vs Long-form**
- **Decision**: Train distinct models for videos ≤60s and >60s based on SMTPD research
- **Rationale**: Fundamentally different consumption patterns require specialized approaches
- **Alternatives Considered**: Single unified model (lower accuracy), category-based models (too complex)
- **Consequences**: Higher accuracy, increased model management complexity, clear feature differentiation

---

## 4. Use-Case View

### 4.1 Primary Use Cases

**UC-001: User Registration and Authentication**
- **Actor**: Content Creator, Digital Marketer
- **Description**: User creates account and authenticates to access prediction services
- **Priority**: High
- **Complexity**: Medium

**UC-002: Generate Video Prediction**
- **Actor**: Authenticated User
- **Description**: User inputs YouTube video URL and receives viewership forecast
- **Priority**: Critical
- **Complexity**: High

**UC-003: Visualize Prediction Results**
- **Actor**: Authenticated User
- **Description**: User views interactive charts and analytics for prediction results
- **Priority**: High
- **Complexity**: Medium

**UC-004: System Data Collection**
- **Actor**: System (Automated)
- **Description**: Automated collection of YouTube video metadata for model training
- **Priority**: Critical
- **Complexity**: High

**UC-005: Model Training and Deployment**
- **Actor**: System Administrator
- **Description**: Retrain models with new data and deploy updated versions
- **Priority**: Medium
- **Complexity**: High

### 4.2 Use-Case Realizations

**UC-002: Generate Video Prediction (Detailed)**

**Actors**: Authenticated User (Primary), YouTube Data API (Secondary), Prediction Engine (Secondary)

**Description**: User submits a YouTube video URL and receives a comprehensive viewership forecast with interactive visualization showing predicted view counts at 24-hour, 7-day, and 30-day intervals.

**Preconditions**:
- User is authenticated and has active session
- User has remaining prediction quota for current period
- YouTube video URL is valid and publicly accessible
- Prediction models are loaded and operational

**Main Flow**:
1. User navigates to prediction dashboard
2. User enters YouTube video URL in input field
3. System validates URL format and extracts video ID
4. System calls YouTube Data API to retrieve video metadata
5. System extracts features (temporal, content, channel authority)
6. System determines video type (Shorts ≤60s vs Long-form >60s)
7. System selects appropriate trained model
8. System generates predictions for 24h, 7d, 30d intervals
9. System calculates confidence intervals and accuracy indicators
10. System renders interactive visualization with prediction curve
11. System displays video metadata and key prediction metrics
12. User views results and optionally exports or shares

**Successful Postcondition**:
- User receives accurate prediction with confidence indicators
- Prediction is logged for system improvement
- User quota is decremented appropriately
- Results are cached for potential future requests

**Failure Postcondition**:
- User receives clear error message with suggested actions
- System logs error details for debugging
- User quota is not decremented for failed requests
- System maintains stability and continues serving other users

**Extensions/Alternative Flows**:
- **3a**: Invalid URL format → System displays validation error and input guidance
- **4a**: YouTube API error → System retries with exponential backoff, fallback to cached data
- **6a**: Insufficient metadata → System provides prediction with lower confidence indicator
- **8a**: Model inference error → System uses fallback model or provides error message
- **11a**: Visualization rendering error → System provides tabular results as fallback

---

## 5. Logical View

### 5.1 System Overview

The ViewTrendsSL system is decomposed into five primary subsystems, each with distinct responsibilities and clear interfaces:

**Core Subsystems:**
1. **Data Collection Subsystem**: YouTube API integration and data harvesting
2. **Machine Learning Subsystem**: Feature engineering, model training, and prediction inference
3. **Web Application Subsystem**: User interface, authentication, and session management
4. **Database Management Subsystem**: Data storage, retrieval, and integrity maintenance
5. **System Administration Subsystem**: Monitoring, logging, and maintenance operations

### 5.2 Architecturally Significant Design Packages

**Package 1: Data Collection (`data_collection`)**

**Purpose**: Automated collection and preprocessing of YouTube video and channel metadata

**Key Classes:**
- `YouTubeAPIClient`: Manages API authentication, quota, and request handling
- `ChannelCollector`: Identifies and validates Sri Lankan YouTube channels
- `VideoCollector`: Harvests video metadata from monitored channels
- `DataValidator`: Ensures data quality and completeness
- `DataCleaner`: Preprocesses raw API responses for storage

**Design Patterns**:
- **Factory Pattern**: `APIClientFactory` creates appropriate client instances
- **Strategy Pattern**: Different collection strategies for channels vs videos
- **Observer Pattern**: `DataQualityMonitor` observes collection processes

**Relationships**:
- Depends on `database_access` for data storage
- Provides data to `machine_learning` subsystem
- Monitored by `system_administration` subsystem

**Package 2: Machine Learning (`machine_learning`)**

**Purpose**: Feature engineering, model training, and prediction generation

**Key Classes**:
- `FeatureExtractor`: Transforms raw video metadata into model features
- `ModelTrainer`: Handles XGBoost model training and evaluation
- `PredictionEngine`: Generates viewership forecasts using trained models
- `ModelManager`: Manages model versioning and deployment
- `PerformanceEvaluator`: Monitors model accuracy and performance

**Design Patterns**:
- **Strategy Pattern**: `ModelStrategy` for Shorts vs Long-form models
- **Factory Pattern**: `ModelFactory` creates appropriate model instances
- **Template Method**: `TrainingPipeline` defines training workflow
- **Singleton Pattern**: `ModelRegistry` maintains single model instance registry

**Relationships**:
- Consumes data from `data_collection` subsystem
- Provides predictions to `web_application` subsystem
- Stores models and metrics in `database_management` subsystem

**Package 3: Web Application (`web_application`)**

**Purpose**: User interface, authentication, and API services

**Key Classes**:
- `AuthenticationManager`: Handles user registration, login, and session management
- `PredictionController`: Processes prediction requests and coordinates responses
- `VisualizationRenderer`: Generates interactive charts and graphs
- `APIGateway`: Manages REST API endpoints and request routing
- `SessionManager`: Maintains user sessions and security context

**Design Patterns**:
- **MVC Pattern**: Controllers, Models, and Views for web interface
- **Facade Pattern**: `APIGateway` provides simplified interface to backend services
- **Decorator Pattern**: Authentication and authorization decorators
- **Command Pattern**: Request processing and validation commands

**Relationships**:
- Interfaces with `machine_learning` for predictions
- Uses `database_management` for user data and session storage
- Monitored by `system_administration` for performance tracking

**Package 4: Database Management (`database_management`)**

**Purpose**: Data storage, retrieval, and integrity maintenance

**Key Classes**:
- `DatabaseConnection`: Manages PostgreSQL connections and pooling
- `ChannelRepository`: Data access layer for channel information
- `VideoRepository`: Data access layer for video metadata and snapshots
- `UserRepository`: Data access layer for user accounts and sessions
- `PredictionRepository`: Data access layer for prediction history and caching

**Design Patterns**:
- **Repository Pattern**: Abstracts database operations behind interfaces
- **Unit of Work Pattern**: Manages transactions and data consistency
- **Data Mapper Pattern**: Maps between domain objects and database records
- **Connection Pool Pattern**: Efficient database connection management

**Relationships**:
- Serves all other subsystems with data persistence
- Implements data integrity constraints and validation
- Provides backup and recovery capabilities

**Package 5: System Administration (`system_administration`)**

**Purpose**: Monitoring, logging, maintenance, and operational support

**Key Classes**:
- `SystemMonitor`: Tracks system performance and health metrics
- `LogManager`: Centralized logging and error tracking
- `BackupManager`: Automated database backup and recovery
- `AlertManager`: System alerting and notification services
- `ConfigurationManager`: System configuration and environment management

**Design Patterns**:
- **Observer Pattern**: Monitoring components observe system events
- **Singleton Pattern**: Single instances for logging and configuration
- **Command Pattern**: Administrative commands and operations
- **Strategy Pattern**: Different backup and monitoring strategies

**Relationships**:
- Monitors all other subsystems for health and performance
- Provides operational support and maintenance capabilities
- Integrates with external monitoring and alerting services

### 5.3 Component Interaction Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  YouTube API    │    │  Cloud Database │
│   (Client)      │    │   (External)    │    │   (External)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ HTTPS/REST           │ HTTPS/JSON           │ SQL/TLS
          │                      │                      │
┌─────────▼───────────────────────▼──────────────────────▼───────┐
│                    ViewTrendsSL System                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │    Web      │  │    Data     │  │     Machine Learning    │ │
│  │ Application │◄─┤ Collection  │◄─┤       Subsystem         │ │
│  │ Subsystem   │  │ Subsystem   │  │                         │ │
│  └─────┬───────┘  └─────┬───────┘  └───────────┬─────────────┘ │
│        │                │                      │               │
│        │                │                      │               │
│  ┌─────▼────────────────▼──────────────────────▼─────────────┐ │
│  │              Database Management Subsystem                │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │            System Administration Subsystem                │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Process View

### 6.1 Main Processes and Threads

**Primary Processes:**

1. **Web Server Process** (Main Thread)
   - Handles HTTP requests and responses
   - Manages user sessions and authentication
   - Coordinates between subsystems
   - **Threading**: Single-threaded with async I/O for concurrent requests

2. **Data Collection Process** (Background)
   - Scheduled YouTube API data harvesting
   - Data validation and preprocessing
   - Database storage operations
   - **Threading**: Multi-threaded for parallel API calls

3. **Model Inference Process** (On-Demand)
   - Feature extraction from video metadata
   - Model prediction generation
   - Result caching and storage
   - **Threading**: Single-threaded per request with process pooling

4. **System Monitoring Process** (Background)
   - Performance metrics collection
   - Error logging and alerting
   - Health check operations
   - **Threading**: Single-threaded with periodic execution

### 6.2 Component Communication

**Communication Patterns:**

- **Synchronous API Calls**: Web application to machine learning subsystem
- **Asynchronous Messaging**: Data collection to database storage
- **Event-Driven Updates**: System monitoring and alerting
- **Batch Processing**: Model training and data preprocessing

**Inter-Process Communication:**
- **HTTP/REST**: Client-server communication
- **Database Connections**: Shared data access via connection pooling
- **File System**: Model persistence and configuration management
- **Memory Sharing**: Cached predictions and session data

### 6.3 Key Sequence Diagrams

**Sequence Diagram: User Prediction Request Flow**

```
User → WebApp → APIGateway → PredictionController → YouTubeAPI → FeatureExtractor → PredictionEngine → Database → WebApp → User

1. User submits video URL
2. WebApp validates authentication
3. APIGateway routes to PredictionController
4. PredictionController calls YouTubeAPI for metadata
5. FeatureExtractor processes raw data
6. PredictionEngine generates forecast
7. Database stores prediction for caching
8. WebApp renders visualization
9. User receives interactive results
```

**Sequence Diagram: Data Collection Pipeline**

```
Scheduler → DataCollector → YouTubeAPI → DataValidator → DataCleaner → Database → ModelTrainer

1. Scheduler triggers daily collection
2. DataCollector fetches new videos
3. YouTubeAPI returns metadata
4. DataValidator checks quality
5. DataCleaner preprocesses data
6. Database stores clean data
7. ModelTrainer updates models (weekly)
```

### 6.4 Concurrency and Parallelism

**Concurrent Operations:**
- Multiple user prediction requests handled simultaneously
- Background data collection while serving user requests
- Parallel API calls for batch data collection
- Asynchronous database operations with connection pooling

**Thread Safety Measures:**
- Database connection pooling with thread-safe access
- Immutable model objects for concurrent prediction requests
- Synchronized access to shared caches and configuration
- Atomic operations for user session management

---

## 7. Deployment View

### 7.1 Deployment Environment

**Target Environment**: Cloud Platform (Heroku/PythonAnywhere)
- **Rationale**: Zero-cost deployment with automatic scaling and maintenance
- **Benefits**: Simplified deployment, built-in monitoring, SSL certificates
- **Limitations**: Resource constraints, potential cold starts

**Development Environment**: Local Development with Docker
- **Rationale**: Consistent environment across team members (Windows/Ubuntu)
- **Benefits**: Eliminates "works on my machine" issues, production parity
- **Implementation**: Docker Compose for multi-container orchestration

### 7.2 Physical Architecture

**Deployment Architecture Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                        Internet                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                 Load Balancer / CDN                             │
│                 (Cloud Provider)                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                 Web Server Instance                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Docker Container                               ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ ││
│  │  │    Flask    │  │   XGBoost   │  │    Static Files     │ ││
│  │  │ Application │  │   Models    │  │   (CSS/JS/Images)   │ ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                PostgreSQL Database                              │
│                (Cloud Database Service)                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Channels │ Videos │ Snapshots │ Users │ Predictions        ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                External Services                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  YouTube Data   │  │   Monitoring    │  │     Backup      │ │
│  │     API v3      │  │    Service      │  │    Service      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Hardware Specifications

**Production Server Requirements:**
- **CPU**: 2 vCPU cores minimum (4 vCPU recommended)
- **Memory**: 4GB RAM minimum (8GB recommended for model caching)
- **Storage**: 20GB SSD (10GB application, 10GB database)
- **Network**: High-speed internet with 99.9% uptime SLA
- **Backup**: Automated daily backups with 30-day retention

**Database Server Specifications:**
- **CPU**: 1 vCPU dedicated for database operations
- **Memory**: 2GB RAM for query caching and connection pooling
- **Storage**: 10GB SSD with automatic scaling
- **IOPS**: 3000 IOPS for concurrent read/write operations
- **Replication**: Master-slave setup for high availability

### 7.4 Deployment Strategy

**Containerization with Docker:**
```dockerfile
# Multi-stage build for optimized production image
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Docker Compose for Development:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/viewtrendssl
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=viewtrendssl
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 7.5 System Distribution

**Monolithic Deployment (MVP)**:
- Single application instance containing all components
- Simplified deployment and maintenance
- Suitable for academic project scope and timeline
- Cost-effective for expected user load

**Future Distribution Considerations**:
- **API Gateway**: Separate service for request routing and authentication
- **Model Service**: Dedicated service for machine learning inference
- **Data Service**: Separate service for data collection and processing
- **Cache Layer**: Redis for improved performance and session management

---

## 8. Implementation View

### 8.1 Layering Strategy

**5-Layer Architecture Implementation:**

**Layer 1: Presentation Layer**
- **Technology**: Streamlit (primary) or HTML/CSS/JavaScript (alternative)
- **Responsibility**: User interface rendering, user input handling, result visualization
- **Components**: Dashboard pages, authentication forms, interactive charts
- **Key Files**: `app.py`, `pages/`, `static/css/`, `static/js/`

**Layer 2: Application Layer (API Gateway)**
- **Technology**: Flask REST API with Gunicorn WSGI server
- **Responsibility**: HTTP request handling, routing, authentication, session management
- **Components**: API endpoints, middleware, request validation
- **Key Files**: `api/`, `middleware/`, `auth/`, `routes.py`

**Layer 3: Business Logic Layer**
- **Technology**: Python modules with XGBoost, Pandas, NumPy
- **Responsibility**: Core business logic, feature engineering, model inference
- **Components**: Prediction engine, data processing, model management
- **Key Files**: `services/`, `models/`, `utils/`, `feature_engineering.py`

**Layer 4: Data Access Layer**
- **Technology**: SQLAlchemy ORM with PostgreSQL drivers
- **Responsibility**: Database operations, query optimization, transaction management
- **Components**: Repository classes, database models, connection management
- **Key Files**: `repositories/`, `database/`, `models.py`, `db_config.py`

**Layer 5: Data Storage Layer**
- **Technology**: PostgreSQL database with automated backups
- **Responsibility**: Persistent data storage, data integrity, backup/recovery
- **Components**: Database tables, indexes, constraints, stored procedures
- **Key Files**: Database schema, migration scripts, backup configurations

### 8.2 Technology Assignment per Layer

**Development Standards:**
- **Code Style**: PEP-8 compliance enforced with flake8 linter
- **Documentation**: Comprehensive docstrings following Google style
- **Testing**: pytest framework with minimum 80% code coverage
- **Version Control**: Git with feature branch workflow and code review

**Layer Dependencies:**
```python
# Dependency flow (top to bottom)
Presentation Layer
    ↓ (HTTP/REST)
Application Layer
    ↓ (Function calls)
Business Logic Layer
    ↓ (ORM/Repository pattern)
Data Access Layer
    ↓ (SQL/Database connections)
Data Storage Layer
```

### 8.3 Package Structure

```
viewtrendssl/
├── app.py                          # Main application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py                 # Configuration management
│   └── database.py                 # Database configuration
├── presentation/                   # Layer 1: Presentation
│   ├── __init__.py
│   ├── streamlit_app.py           # Streamlit dashboard
│   ├── templates/                  # HTML templates (if using Flask)
│   └── static/                     # CSS, JS, images
├── api/                           # Layer 2: Application
│   ├── __init__.py
│   ├── routes.py                  # API endpoint definitions
│   ├── middleware.py              # Request/response middleware
│   └── auth.py                    # Authentication handlers
├── services/                      # Layer 3: Business Logic
│   ├── __init__.py
│   ├── prediction_service.py      # Core prediction logic
│   ├── data_collection_service.py # Data harvesting logic
│   └── model_service.py           # Model management
├── repositories/                  # Layer 4: Data Access
│   ├── __init__.py
│   ├── video_repository.py        # Video data operations
│   ├── channel_repository.py      # Channel data operations
│   └── user_repository.py         # User data operations
├── models/                        # Database models
│   ├── __init__.py
│   ├── video.py                   # Video entity model
│   ├── channel.py                 # Channel entity model
│   └── user.py                    # User entity model
├── ml/                           # Machine Learning components
│   ├── __init__.py
│   ├── feature_extractor.py       # Feature engineering
│   ├── model_trainer.py           # Model training pipeline
│   ├── prediction_engine.py       # Inference engine
│   └── trained_models/            # Serialized model files
├── utils/                        # Utility functions
│   ├── __init__.py
│   ├── youtube_api.py             # YouTube API client
│   ├── validators.py              # Input validation
│   └── helpers.py                 # Common utilities
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_services/
│   ├── test_repositories/
│   └── test_utils/
├── migrations/                   # Database migrations
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # Project documentation
```

---

## 9. Data View

### 9.1 Database Schema

**Entity-Relationship Diagram:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Channels     │    │     Videos      │    │   Snapshots     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ channel_id (PK) │◄──┤ video_id (PK)   │◄──┤ snapshot_id (PK)│
│ channel_name    │   │ channel_id (FK) │   │ video_id (FK)   │
│ subscriber_count│   │ title           │   │ timestamp       │
│ video_count     │   │ published_at    │   │ view_count      │
│ country         │   │ duration_seconds│   │ like_count      │
│ created_at      │   │ category_id     │   │ comment_count   │
│ updated_at      │   │ is_short        │   │ created_at      │
└─────────────────┘   │ created_at      │   └─────────────────┘
                      │ updated_at      │
                      └─────────────────┘
                               │
                      ┌─────────────────┐
                      │      Tags       │
                      ├─────────────────┤
                      │ tag_id (PK)     │
                      │ tag_name        │
                      └─────────────────┘
                               │
                      ┌─────────────────┐
                      │   Video_Tags    │
                      ├─────────────────┤
                      │ video_id (FK)   │
                      │ tag_id (FK)     │
                      └─────────────────┘

┌─────────────────┐    ┌─────────────────┐
│     Users       │    │  Predictions    │
├─────────────────┤    ├─────────────────┤
│ user_id (PK)    │◄──┤ prediction_id   │
│ email           │   │ user_id (FK)    │
│ password_hash   │   │ video_id        │
│ created_at      │   │ predicted_24h   │
│ last_login      │   │ predicted_7d    │
│ is_active       │   │ predicted_30d   │
└─────────────────┘   │ confidence      │
                      │ created_at      │
                      └─────────────────┘
```

### 9.2 Data Storage Strategy

**Primary Tables:**

**Channels Table:**
```sql
CREATE TABLE channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    subscriber_count BIGINT DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    country VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_channels_country ON channels(country);
CREATE INDEX idx_channels_subscriber_count ON channels(subscriber_count);
```

**Videos Table:**
```sql
CREATE TABLE videos (
    video_id VARCHAR(50) PRIMARY KEY,
    channel_id VARCHAR(50) REFERENCES channels(channel_id),
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP NOT NULL,
    duration_seconds INTEGER NOT NULL,
    category_id INTEGER,
    is_short BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_videos_channel_id ON videos(channel_id);
CREATE INDEX idx_videos_published_at ON videos(published_at);
CREATE INDEX idx_videos_is_short ON videos(is_short);
CREATE INDEX idx_videos_category_id ON videos(category_id);
```

**Snapshots Table:**
```sql
CREATE TABLE snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) REFERENCES videos(video_id),
    timestamp TIMESTAMP NOT NULL,
    view_count BIGINT NOT NULL,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_snapshots_video_timestamp ON snapshots(video_id, timestamp);
CREATE INDEX idx_snapshots_timestamp ON snapshots(timestamp);
```

### 9.3 Data Flow Architecture

**Data Collection Flow:**
1. **YouTube API** → Raw JSON responses
2. **Data Validator** → Validated metadata
3. **Data Cleaner** → Processed records
4. **Database Storage** → Normalized tables
5. **Feature Extractor** → ML-ready features

**Prediction Flow:**
1. **User Input** → Video URL
2. **YouTube API** → Video metadata
3. **Feature Engineering** → Model features
4. **Model Inference** → Predictions
5. **Result Caching** → Database storage
6. **Visualization** → User interface

---

## 10. Size and Performance

### 10.1 Expected Data Volume

**Database Growth Projections:**
- **Channels**: 500-1000 Sri Lankan channels monitored
- **Videos**: 50,000-100,000 videos collected over 6 months
- **Snapshots**: 1-5 million time-series data points
- **Users**: 100-500 registered users for MVP
- **Predictions**: 1,000-10,000 prediction requests

**Storage Requirements:**
- **Database Size**: 5-10 GB for complete dataset
- **Model Files**: 100-500 MB for trained XGBoost models
- **Application Code**: 50-100 MB
- **Logs and Backups**: 1-2 GB

### 10.2 Performance Expectations

**Response Time Targets:**
- **Prediction Generation**: < 30 seconds end-to-end
- **Dashboard Loading**: < 5 seconds initial load
- **API Responses**: < 2 seconds for cached results
- **Database Queries**: < 1 second for indexed lookups

**Throughput Requirements:**
- **Concurrent Users**: 10-50 simultaneous users
- **Predictions per Hour**: 100-500 requests
- **API Calls per Day**: 1,000-5,000 requests
- **Data Collection**: 1,000-5,000 videos per day

### 10.3 Performance Optimization Strategies

**Caching Implementation:**
- **Prediction Results**: 24-hour TTL for video predictions
- **Model Loading**: In-memory model caching
- **Database Queries**: Query result caching for common lookups
- **Static Assets**: CDN caching for CSS/JS files

**Database Optimization:**
- **Indexing Strategy**: Composite indexes on frequently queried columns
- **Connection Pooling**: 10-20 concurrent database connections
- **Query Optimization**: Efficient JOIN operations and pagination
- **Partitioning**: Time-based partitioning for snapshots table

---

## 11. Quality

### 11.1 Quality Attributes

**Reliability:**
- **Model Accuracy**: MAPE < 30% for 7-day predictions
- **System Uptime**: 99.5% availability during operational hours
- **Error Recovery**: Graceful degradation with fallback mechanisms
- **Data Integrity**: ACID compliance for all database transactions

**Performance:**
- **Response Time**: 95th percentile < 30 seconds for predictions
- **Throughput**: Support 50 concurrent users with acceptable performance
- **Scalability**: Horizontal scaling capability for future growth
- **Resource Efficiency**: Optimal memory and CPU utilization

**Security:**
- **Authentication**: Secure user registration and login system
- **Authorization**: Role-based access control for different user types
- **Data Protection**: Encryption for sensitive data and API keys
- **Input Validation**: Comprehensive validation for all user inputs

**Maintainability:**
- **Code Quality**: 80%+ test coverage with comprehensive unit tests
- **Documentation**: Complete API documentation and architectural guides
- **Modularity**: Loosely coupled components with clear interfaces
- **Monitoring**: Comprehensive logging and performance monitoring

### 11.2 Security Architecture

**Authentication and Authorization:**
```python
# JWT-based authentication with secure password hashing
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

class AuthenticationService:
    def register_user(self, email, password):
        password_hash = generate_password_hash(password)
        # Store user with hashed password
    
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return create_access_token(identity=user.id)
        return None
```

**API Key Protection:**
```python
# Environment-based configuration management
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    @classmethod
    def validate_config(cls):
        required_vars = ['YOUTUBE_API_KEY', 'DATABASE_URL', 'SECRET_KEY']
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
```

**Input Validation:**
```python
from pydantic import BaseModel, HttpUrl, validator

class PredictionRequest(BaseModel):
    video_url: HttpUrl
    
    @validator('video_url')
    def validate_youtube_url(cls, v):
        if 'youtube.com' not in str(v) and 'youtu.be' not in str(v):
            raise ValueError('Must be a valid YouTube URL')
        return v
```

### 11.3 Quality Assurance Strategy

**Testing Framework:**
- **Unit Tests**: pytest with fixtures for isolated component testing
- **Integration Tests**: End-to-end API testing with test database
- **Performance Tests**: Load testing with simulated user requests
- **Security Tests**: Automated vulnerability scanning and penetration testing

**Code Quality Measures:**
- **Static Analysis**: flake8, pylint for code quality enforcement
- **Code Coverage**: pytest-cov with minimum 80% coverage requirement
- **Code Review**: Mandatory peer review for all code changes
- **Continuous Integration**: Automated testing on every commit

---

## 12. References

### 12.1 Academic and Research References

**Primary Research Papers:**
1. Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.

2. Kumar, S., et al. (2024). "AMPS: Predicting popularity of short-form videos using multi-modal attention mechanisms." *Journal of Retailing and Consumer Services*, 78, 103-115.

3. Zhang, L., et al. (2025). "SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity." *arXiv preprint arXiv:2503.04446v1*.

4. Szabo, G., & Huberman, B. A. (2010). "Predicting the popularity of online content." *Communications of the ACM*, 53(8), 80-88.

**Technical Standards and Guidelines:**
5. IEEE Computer Society. (2000). "IEEE Recommended Practice for Architectural Description of Software-Intensive Systems." *IEEE Std 1471-2000*.

6. ISO/IEC. (2011). "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE)." *ISO/IEC 25010:2011*.

7. Fielding, R. T. (2000). "Architectural Styles and the Design of Network-based Software Architectures." *Doctoral dissertation, University of California, Irvine*.

### 12.2 Technical Documentation

**API and Framework Documentation:**
8. Google Developers. (2024). "YouTube Data API v3 Reference." Retrieved from https://developers.google.com/youtube/v3/docs/

9. Pallets Projects. (2024). "Flask Documentation." Retrieved from https://flask.palletsprojects.com/

10. XGBoost Developers. (2024). "XGBoost Documentation." Retrieved from https://xgboost.readthedocs.io/

11. PostgreSQL Global Development Group. (2024). "PostgreSQL Documentation." Retrieved from https://www.postgresql.org/docs/

**Development and Deployment Tools:**
12. Docker Inc. (2024). "Docker Documentation." Retrieved from https://docs.docker.com/

13. SQLAlchemy. (2024). "SQLAlchemy Documentation." Retrieved from https://docs.sqlalchemy.org/

14. Streamlit Inc. (2024). "Streamlit Documentation." Retrieved from https://docs.streamlit.io/

### 12.3 Architectural and Design References

**Software Architecture:**
15. Newman, S. (2021). *Building Microservices: Designing Fine-Grained Systems* (2nd ed.). O'Reilly Media.

16. Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley Professional.

17. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.

**Machine Learning Engineering:**
18. Géron, A. (2019). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (2nd ed.). O'Reilly Media.

19. Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.

### 12.4 Project-Specific Resources

**University Guidelines:**
20. University of Moratuwa. (2024). "CS3501 Data Science and Engineering Project Guidelines." *Department of Computer Science and Engineering*.

21. University of Moratuwa. (2024). "Research Ethics Guidelines for Undergraduate Projects." *Faculty of Engineering*.

**Development Tools and Platforms:**
22. Heroku. (2024). "Heroku Platform Documentation." Retrieved from https://devcenter.heroku.com/

23. GitHub. (2024). "GitHub Documentation." Retrieved from https://docs.github.com/

24. Draw.io. (2024). "Diagrams.net User Guide." Retrieved from https://www.diagrams.net/doc/

---

**Document Control:**
- **Version**: 1.0
- **Last Updated**: August 6, 2025
- **Next Review**: September 6, 2025
- **Approved By**: Development Team Lead
- **Distribution**: Development Team, Project Mentor, Academic Evaluators

---

*This Software Architecture Document serves as the definitive architectural specification for the ViewTrendsSL system. All implementation decisions should align with the architectural principles and patterns defined in this document. For questions or clarifications, contact the development team leads.*
