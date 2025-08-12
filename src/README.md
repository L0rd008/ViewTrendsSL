# Source Code Directory

This directory contains the main application source code organized using a **Layered Architecture** pattern for maximum scalability and maintainability.

## 🏗️ Architecture Overview

The application follows a **4-Layer Architecture**:
1. **Presentation Layer** (`/presentation/`) - User Interface
2. **Application Layer** (`/application/`) - API and Request Handling
3. **Business Layer** (`/business/`) - Core Business Logic and ML
4. **Data Access Layer** (`/data_access/`) - Database Operations
5. **External Layer** (`/external/`) - Third-party Integrations

## 📁 Directory Structure

### `/presentation/` - UI Layer
**Purpose**: User interface components and static assets
**Technology**: Streamlit, HTML/CSS/JavaScript
**Responsibilities**:
- Web pages and user interfaces
- User input validation and formatting
- Data visualization and charts
- Static assets (CSS, JS, images)

**Key Components**:
- `pages/` - Individual web pages
- `components/` - Reusable UI components
- `static/` - CSS, JavaScript, and image assets

### `/application/` - API Layer
**Purpose**: HTTP request handling and API endpoints
**Technology**: Flask, REST APIs
**Responsibilities**:
- REST API endpoint definitions
- Request/response handling
- Authentication and authorization
- Input validation and sanitization
- API middleware and interceptors

**Key Components**:
- `api/auth/` - Authentication endpoints
- `api/prediction/` - Video prediction endpoints
- `api/analytics/` - Analytics and reporting endpoints
- `middleware/` - Request/response middleware

### `/business/` - Business Logic Layer
**Purpose**: Core application logic and machine learning
**Technology**: Python, XGBoost, Scikit-learn
**Responsibilities**:
- Business rules and logic
- Machine learning models and training
- Data processing and feature engineering
- Service orchestration
- Utility functions

**Key Components**:
- `services/` - Business service classes
- `ml/` - Machine learning components
- `utils/` - Shared utility functions

### `/data_access/` - Data Access Layer
**Purpose**: Database operations and data persistence
**Technology**: SQLAlchemy, PostgreSQL/SQLite
**Responsibilities**:
- Database model definitions
- Data repository patterns
- Database migrations and seeds
- Query optimization
- Data validation

**Key Components**:
- `repositories/` - Data access repositories
- `models/` - Database model definitions
- `database/` - Migration and seed scripts

### `/external/` - External Integrations
**Purpose**: Third-party API integrations and external services
**Technology**: Various APIs and SDKs
**Responsibilities**:
- YouTube Data API integration
- Monitoring and logging services
- Future platform integrations (TikTok, Instagram)
- External service abstractions

**Key Components**:
- `youtube_api/` - YouTube API client and utilities
- `monitoring/` - System monitoring integrations
- `tiktok_api/` - Future TikTok integration
- `instagram_api/` - Future Instagram integration

## 🔄 Data Flow

```
User Request → Presentation Layer → Application Layer → Business Layer → Data Access Layer → Database
                     ↓                    ↓                 ↓                ↓
              Static Assets        API Endpoints    Business Logic    Data Operations
                     ↓                    ↓                 ↓                ↓
              UI Components        Middleware       ML Models        Repositories
                     ↓                    ↓                 ↓                ↓
              User Interface       Authentication   Predictions      Database Models
```

## 🧩 Module Dependencies

- **Presentation** depends on **Application** (API calls)
- **Application** depends on **Business** (service calls)
- **Business** depends on **Data Access** (data operations)
- **All layers** can use **External** (third-party services)
- **No reverse dependencies** (maintains clean architecture)

## 📦 Package Structure

Each directory contains:
- `__init__.py` - Package initialization
- Module-specific Python files
- `README.md` - Directory-specific documentation
- Configuration files (where applicable)

## 🚀 Getting Started

1. **Environment Setup**: Ensure Python 3.9+ is installed
2. **Dependencies**: Install requirements from `requirements.txt`
3. **Database**: Set up database using scripts in `data_access/database/`
4. **Configuration**: Configure environment variables
5. **Run Application**: Start the Flask application from `application/api/app.py`

## 🔧 Development Guidelines

- **Single Responsibility**: Each module should have one clear purpose
- **Dependency Injection**: Use dependency injection for testability
- **Error Handling**: Implement comprehensive error handling
- **Logging**: Add appropriate logging at each layer
- **Testing**: Write unit tests for each component
- **Documentation**: Document all public interfaces

## 🎯 Future Scalability

This architecture supports:
- **Microservices Migration**: Each layer can become a separate service
- **Horizontal Scaling**: Stateless design enables load balancing
- **Feature Addition**: New features fit cleanly into existing layers
- **Technology Changes**: Layers can be replaced independently
- **Multi-Platform Support**: External layer abstracts platform differences
