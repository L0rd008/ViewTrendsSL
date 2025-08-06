# TODO - Immediate Action Items
## ViewTrendsSL: Task Management and Priority Tracking

**Document Version**: 1.0  
**Date**: August 6, 2025  
**Last Updated**: August 6, 2025  
**Next Review**: August 13, 2025

> **📋 IMPORTANT: For detailed implementation instructions, see our [Development Guide](Development%20Guide.md)**
> 
> The Development Guide contains step-by-step implementation instructions, code examples, and complete workflows. Use this TODO list for task tracking and the Development Guide for implementation details.

---

## Document Overview

This document tracks immediate actionable tasks for the ViewTrendsSL project. Tasks are organized by priority and timeline, with clear ownership and dependencies. This document is updated daily during active development phases.

**Priority Legend:**
- 🔥 **Critical** - Must complete this week for project success
- ⚡ **High** - Important for timeline, complete within 2 weeks
- 📋 **Medium** - Planned but flexible timing (2-4 weeks)
- 💡 **Low** - Nice to have, backlog items

**Status Legend:**
- 🆕 **New** - Just identified, not yet started
- 🏃 **In Progress** - Currently being worked on
- ⏸️ **Blocked** - Waiting for dependencies
- ✅ **Complete** - Finished and verified
- ❌ **Cancelled** - No longer needed

---

## Current Week Focus (Week 1: Aug 6-12, 2025)

### 🔥 Critical Tasks - Must Complete This Week

#### **TASK-001: Development Environment Setup**
**Priority**: 🔥 Critical  
**Owner**: All Team Members  
**Status**: 🆕 New  
**Deadline**: August 8, 2025  
**Estimated Effort**: 4-6 hours per person  

**Description**: Set up consistent development environment across all team members using Docker.

**Subtasks**:
- [ ] Install Docker Desktop on all development machines
- [ ] Create project Dockerfile with Python 3.9+ base image
- [ ] Set up docker-compose.yml for development services
- [ ] Configure VS Code with Python extensions and Docker integration
- [ ] Test environment consistency across Windows and Ubuntu systems
- [ ] Document setup process in README.md

**Dependencies**: None  
**Acceptance Criteria**: All team members can run `docker-compose up` and access the application locally

---

#### **TASK-002: GitHub Repository Organization**
**Priority**: 🔥 Critical  
**Owner**: Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: August 7, 2025  
**Estimated Effort**: 2-3 hours  

**Description**: Organize GitHub repository with proper structure, branching strategy, and collaboration guidelines.

**Subtasks**:
- [ ] Create feature branch protection rules for main branch
- [ ] Set up development branch as default for pull requests
- [ ] Create issue templates for bugs and feature requests
- [ ] Set up pull request template with checklist
- [ ] Configure GitHub Actions for basic CI (linting, testing)
- [ ] Create CONTRIBUTING.md with development guidelines
- [ ] Set up project board for task tracking

**Dependencies**: None  
**Acceptance Criteria**: Team can follow Git workflow with proper code review process

---

#### **TASK-003: YouTube API Key Setup and Testing**
**Priority**: 🔥 Critical  
**Owner**: Senevirathne (Data Lead)  
**Status**: 🆕 New  
**Deadline**: August 8, 2025  
**Estimated Effort**: 3-4 hours  

**Description**: Set up YouTube Data API v3 access for all team members and implement basic testing.

**Subtasks**:
- [ ] Create Google Cloud Projects for all 3 team members
- [ ] Enable YouTube Data API v3 for each project
- [ ] Generate API keys and set up quota monitoring
- [ ] Create .env template file for API key management
- [ ] Implement basic API connection test script
- [ ] Test quota usage and rate limiting
- [ ] Document API key rotation strategy

**Dependencies**: Google accounts for all team members  
**Acceptance Criteria**: All team members can successfully call YouTube API and retrieve video data

---

#### **TASK-004: Database Schema Design and Implementation**
**Priority**: 🔥 Critical  
**Owner**: Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: August 9, 2025  
**Estimated Effort**: 6-8 hours  

**Description**: Design and implement the core database schema for storing YouTube data.

**Subtasks**:
- [ ] Design Entity-Relationship Diagram (ERD)
- [ ] Create SQLite database schema for development
- [ ] Implement database migration scripts
- [ ] Set up SQLAlchemy models and relationships
- [ ] Create database initialization and seeding scripts
- [ ] Test database operations (CRUD)
- [ ] Plan PostgreSQL migration for production

**Dependencies**: Development environment setup  
**Acceptance Criteria**: Database schema supports all required data types and relationships

---

#### **TASK-005: Project Documentation Framework**
**Priority**: 🔥 Critical  
**Owner**: Shaamma (Documentation Lead)  
**Status**: 🆕 New  
**Deadline**: August 9, 2025  
**Estimated Effort**: 4-5 hours  

**Description**: Establish comprehensive documentation structure and standards.

**Subtasks**:
- [ ] Create README.md with project overview and setup instructions
- [ ] Set up documentation structure in /docs folder
- [ ] Create templates for meeting notes and progress reports
- [ ] Establish code documentation standards (docstrings, comments)
- [ ] Set up automated documentation generation (Sphinx or similar)
- [ ] Create user guide template for final deliverable

**Dependencies**: Repository organization  
**Acceptance Criteria**: Clear documentation structure that supports project requirements

---

### ⚡ High Priority - Complete Within 2 Weeks

#### **TASK-006: Sri Lankan Channel Identification**
**Priority**: ⚡ High  
**Owner**: Senevirathne (Data Lead)  
**Status**: 🆕 New  
**Deadline**: August 15, 2025  
**Estimated Effort**: 8-10 hours  

**Description**: Create curated list of 100+ Sri Lankan YouTube channels across different categories.

**Subtasks**:
- [ ] Research popular Sri Lankan channels using Social Blade
- [ ] Categorize channels (News, Entertainment, Education, Lifestyle, etc.)
- [ ] Verify channel authenticity and Sri Lankan connection
- [ ] Create channel metadata collection script
- [ ] Validate channel data quality and completeness
- [ ] Document channel selection criteria and methodology

**Dependencies**: YouTube API setup  
**Acceptance Criteria**: Curated list of 100+ verified Sri Lankan channels with metadata

---

#### **TASK-007: Data Collection Scripts Development**
**Priority**: ⚡ High  
**Owner**: Senevirathne (Data Lead)  
**Status**: 🆕 New  
**Deadline**: August 16, 2025  
**Estimated Effort**: 12-15 hours  

**Description**: Develop automated scripts for collecting YouTube video and channel data.

**Subtasks**:
- [ ] Implement `collect_channels.py` for channel metadata
- [ ] Implement `collect_videos.py` for video metadata and statistics
- [ ] Create `track_performance.py` for time-series data collection
- [ ] Add error handling and retry logic for API failures
- [ ] Implement quota management and rate limiting
- [ ] Create data validation and quality checks
- [ ] Set up logging and monitoring for data collection

**Dependencies**: Database schema, YouTube API setup, Channel identification  
**Acceptance Criteria**: Scripts can collect and store data from target channels reliably

---

#### **TASK-008: Initial Data Processing Pipeline**
**Priority**: ⚡ High  
**Owner**: Senevirathne (Data Lead) + Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: August 18, 2025  
**Estimated Effort**: 10-12 hours  

**Description**: Create data preprocessing and feature engineering pipeline.

**Subtasks**:
- [ ] Implement `process_data.py` for data cleaning and preprocessing
- [ ] Create feature engineering functions (time-based, text-based)
- [ ] Implement data validation and quality metrics
- [ ] Add support for Shorts vs Long-form video classification
- [ ] Create data export functions for ML model training
- [ ] Set up automated data processing workflows

**Dependencies**: Data collection scripts, Database schema  
**Acceptance Criteria**: Clean, processed dataset ready for exploratory data analysis

---

#### **TASK-009: System Requirements Specification (SRS) Completion**
**Priority**: ⚡ High  
**Owner**: Shaamma (Documentation Lead)  
**Status**: 🆕 New  
**Deadline**: August 15, 2025  
**Estimated Effort**: 8-10 hours  

**Description**: Complete the System Requirements Specification document based on project plan.

**Subtasks**:
- [ ] Finalize functional requirements based on MVP scope
- [ ] Define non-functional requirements (performance, security, usability)
- [ ] Create use case diagrams and user stories
- [ ] Specify system interfaces and integration requirements
- [ ] Document data requirements and constraints
- [ ] Review and validate requirements with team and mentor

**Dependencies**: Project plan review  
**Acceptance Criteria**: Complete SRS document approved by team and mentor

---

#### **TASK-010: Software Architecture Document (SAD) Development**
**Priority**: ⚡ High  
**Owner**: Sanjula (Backend Lead) + Shaamma (Documentation Lead)  
**Status**: 🆕 New  
**Deadline**: August 16, 2025  
**Estimated Effort**: 10-12 hours  

**Description**: Create comprehensive software architecture document.

**Subtasks**:
- [ ] Design system architecture diagrams (layered architecture)
- [ ] Create component interaction diagrams
- [ ] Document technology stack and rationale
- [ ] Design API specifications and endpoints
- [ ] Create deployment architecture diagrams
- [ ] Document security and performance considerations

**Dependencies**: SRS completion, Technology stack decisions  
**Acceptance Criteria**: Complete SAD document with clear architectural vision

---

### 📋 Medium Priority - Complete Within 4 Weeks

#### **TASK-011: Exploratory Data Analysis (EDA) Framework**
**Priority**: 📋 Medium  
**Owner**: Senevirathne (Data Lead)  
**Status**: 🆕 New  
**Deadline**: August 25, 2025  
**Estimated Effort**: 8-10 hours  

**Description**: Set up framework for comprehensive exploratory data analysis.

**Subtasks**:
- [ ] Create Jupyter notebook templates for EDA
- [ ] Implement data visualization functions
- [ ] Create statistical analysis utilities
- [ ] Set up correlation analysis and feature importance tools
- [ ] Document EDA methodology and best practices

**Dependencies**: Initial data collection and processing  
**Acceptance Criteria**: EDA framework ready for analyzing collected data

---

#### **TASK-012: Machine Learning Model Framework**
**Priority**: 📋 Medium  
**Owner**: Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: August 30, 2025  
**Estimated Effort**: 12-15 hours  

**Description**: Set up machine learning model development and training framework.

**Subtasks**:
- [ ] Create model training pipeline structure
- [ ] Implement data splitting and validation strategies
- [ ] Set up model evaluation metrics and reporting
- [ ] Create model serialization and versioning system
- [ ] Implement baseline model for comparison
- [ ] Set up hyperparameter tuning framework

**Dependencies**: Data processing pipeline, EDA insights  
**Acceptance Criteria**: ML framework ready for model development and training

---

#### **TASK-013: Web Application Foundation**
**Priority**: 📋 Medium  
**Owner**: Shaamma (Frontend Lead)  
**Status**: 🆕 New  
**Deadline**: September 1, 2025  
**Estimated Effort**: 10-12 hours  

**Description**: Create foundation for web application user interface.

**Subtasks**:
- [ ] Choose between Streamlit and HTML/CSS/JS approach
- [ ] Create basic application structure and routing
- [ ] Implement user authentication system
- [ ] Design responsive layout and navigation
- [ ] Set up data visualization components
- [ ] Create form handling for video URL input

**Dependencies**: Backend API design, UI/UX planning  
**Acceptance Criteria**: Basic web application with authentication and core UI components

---

#### **TASK-014: Testing Framework Setup**
**Priority**: 📋 Medium  
**Owner**: All Team Members  
**Status**: 🆕 New  
**Deadline**: August 28, 2025  
**Estimated Effort**: 6-8 hours  

**Description**: Establish comprehensive testing framework for all components.

**Subtasks**:
- [ ] Set up pytest for unit testing
- [ ] Create test data fixtures and mocks
- [ ] Implement API testing framework
- [ ] Set up code coverage reporting
- [ ] Create integration testing strategies
- [ ] Document testing standards and practices

**Dependencies**: Core development frameworks  
**Acceptance Criteria**: Testing framework supports all major components

---

### 💡 Low Priority - Backlog Items

#### **TASK-015: Performance Monitoring Setup**
**Priority**: 💡 Low  
**Owner**: Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: September 15, 2025  
**Estimated Effort**: 4-6 hours  

**Description**: Implement basic performance monitoring and logging.

**Subtasks**:
- [ ] Set up application logging framework
- [ ] Implement performance metrics collection
- [ ] Create basic monitoring dashboard
- [ ] Set up error tracking and alerting

**Dependencies**: Core application development  
**Acceptance Criteria**: Basic monitoring provides visibility into system performance

---

#### **TASK-016: Security Hardening**
**Priority**: 💡 Low  
**Owner**: Sanjula (Backend Lead)  
**Status**: 🆕 New  
**Deadline**: September 20, 2025  
**Estimated Effort**: 6-8 hours  

**Description**: Implement security best practices and hardening measures.

**Subtasks**:
- [ ] Implement input validation and sanitization
- [ ] Set up HTTPS and secure headers
- [ ] Add rate limiting and abuse prevention
- [ ] Implement secure session management
- [ ] Create security audit checklist

**Dependencies**: Core application functionality  
**Acceptance Criteria**: Application follows security best practices

---

## Weekly Planning and Review

### Week 1 (Aug 6-12): Foundation Setup
**Focus**: Development environment, repository organization, API setup, database design
**Key Deliverables**: Working development environment, API access, database schema
**Success Criteria**: All team members can develop locally with consistent environment

### Week 2 (Aug 13-19): Data Infrastructure
**Focus**: Channel identification, data collection scripts, initial data processing
**Key Deliverables**: Channel list, data collection pipeline, processed dataset
**Success Criteria**: Automated data collection from 50+ channels

### Week 3 (Aug 20-26): Documentation and Analysis
**Focus**: Complete SRS/SAD documents, EDA framework, initial data analysis
**Key Deliverables**: SRS, SAD, EDA insights, data quality report
**Success Criteria**: Complete project documentation and data understanding

### Week 4 (Aug 27-Sep 2): Model and Application Foundation
**Focus**: ML framework setup, web application foundation, testing framework
**Key Deliverables**: Model training pipeline, basic web app, testing suite
**Success Criteria**: End-to-end development pipeline established

---

## Task Dependencies and Critical Path

### Critical Path Analysis
1. **Environment Setup** → **Repository Organization** → **API Setup**
2. **API Setup** → **Channel Identification** → **Data Collection Scripts**
3. **Database Schema** → **Data Collection Scripts** → **Data Processing**
4. **Data Processing** → **EDA Framework** → **Model Framework**
5. **Model Framework** → **Web Application** → **Integration Testing**

### Dependency Matrix
| Task | Depends On | Blocks |
|------|------------|--------|
| TASK-001 | None | TASK-004, TASK-007 |
| TASK-002 | None | TASK-005, TASK-014 |
| TASK-003 | None | TASK-006, TASK-007 |
| TASK-004 | TASK-001 | TASK-007, TASK-008 |
| TASK-006 | TASK-003 | TASK-007 |
| TASK-007 | TASK-003, TASK-004, TASK-006 | TASK-008, TASK-011 |
| TASK-008 | TASK-007 | TASK-011, TASK-012 |

---

## Risk Mitigation Tasks

### High-Risk Areas Requiring Attention

#### **RISK-001: YouTube API Quota Management**
**Mitigation Tasks**:
- [ ] Implement quota monitoring and alerting
- [ ] Create API key rotation system
- [ ] Optimize API call efficiency
- [ ] Set up backup data sources

#### **RISK-002: Data Quality Issues**
**Mitigation Tasks**:
- [ ] Implement comprehensive data validation
- [ ] Create data quality monitoring dashboard
- [ ] Set up automated data quality alerts
- [ ] Establish data cleaning procedures

#### **RISK-003: Team Coordination Challenges**
**Mitigation Tasks**:
- [ ] Establish daily standup meetings
- [ ] Create clear communication channels
- [ ] Set up shared development practices
- [ ] Implement code review processes

---

## Completed Tasks Archive

### ✅ Completed This Week
*No completed tasks yet - project just started*

### ✅ Completed Last Week
*No previous week - project initialization*

---

## Task Assignment Summary

### Senevirathne S.M.P.U. (Data Lead)
**Active Tasks**: 4 tasks (TASK-003, TASK-006, TASK-007, TASK-008, TASK-011)  
**Total Effort**: ~35-40 hours over 3 weeks  
**Focus Areas**: YouTube API, data collection, channel identification, EDA

### Sanjula N.G.K. (Backend Lead)
**Active Tasks**: 5 tasks (TASK-002, TASK-004, TASK-008, TASK-010, TASK-012)  
**Total Effort**: ~35-40 hours over 3 weeks  
**Focus Areas**: Repository setup, database, architecture, ML framework

### Shaamma M.S. (Frontend/Documentation Lead)
**Active Tasks**: 4 tasks (TASK-005, TASK-009, TASK-010, TASK-013)  
**Total Effort**: ~30-35 hours over 3 weeks  
**Focus Areas**: Documentation, SRS/SAD, web application, UI/UX

### All Team Members
**Shared Tasks**: 2 tasks (TASK-001, TASK-014)  
**Total Effort**: ~10-14 hours over 2 weeks  
**Focus Areas**: Environment setup, testing framework

---

## Notes and Reminders

### Daily Standup Questions
1. What did you complete yesterday?
2. What are you working on today?
3. Are there any blockers or dependencies?
4. Do you need help from team members?

### Weekly Review Questions
1. Did we meet our weekly goals?
2. What tasks need to be reprioritized?
3. Are there new risks or dependencies?
4. What can we improve for next week?

### Important Deadlines
- **August 15**: SRS Document Due
- **August 16**: SAD Document Due
- **August 20**: Mentor Meetup 1
- **September 1**: Mid-evaluation Preparation
- **September 15**: Mid-evaluation Demo

---

**Document Status**: Active - Updated Daily During Development  
**Last Review**: August 6, 2025  
**Next Review**: August 7, 2025  
**Review Frequency**: Daily during active development, weekly during planning phases

---

*This document is the primary task management tool for the ViewTrendsSL project. All team members should review and update their task status daily. New tasks should be added with proper priority, ownership, and dependency information.*
