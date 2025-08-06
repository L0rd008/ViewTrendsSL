# Project Schedule
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

## Project Timeline Overview

**Project Duration**: 10 weeks (August 24 - November 1, 2025)  
**Development Methodology**: Hybrid approach combining Traditional SDLC with Agile practices  
**Total Effort**: 204 person-hours across 3 team members  

---

## Gantt Chart - ViewTrendsSL Development Schedule

### Phase 1: Preliminary Analysis & Project Setup (Weeks 1-2)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Conducting project kickoff meeting** | 2 days | Aug 24 | Aug 25 | All Team | - |
| **Setting up development environments** | 3 days | Aug 24 | Aug 26 | All Team | - |
| **Integrating YouTube Data API** | 4 days | Aug 25 | Aug 28 | Senevirathne | Dev Environment |
| **Designing database schema** | 3 days | Aug 26 | Aug 28 | Sanjula | - |
| **Creating UI/UX wireframes** | 3 days | Aug 26 | Aug 28 | Shaamma | - |
| **Conducting literature review** | 4 days | Aug 25 | Aug 28 | All Team | - |
| **Preparing project proposal** | 3 days | Aug 29 | Aug 31 | All Team | Research Complete |
| **Establishing team coordination protocols** | 2 days | Aug 29 | Aug 30 | All Team | - |

### Phase 2: Systems Requirements Analysis (Week 3)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Analyzing system requirements** | 3 days | Sep 7 | Sep 9 | All Team | Proposal Approved |
| **Writing System Requirements Specification** | 4 days | Sep 8 | Sep 11 | Shaamma | Requirements Analysis |
| **Designing system architecture** | 4 days | Sep 8 | Sep 11 | Sanjula | Requirements Analysis |
| **Creating Software Architecture Document** | 3 days | Sep 10 | Sep 12 | All Team | Architecture Design |
| **Preparing feasibility study** | 3 days | Sep 9 | Sep 11 | All Team | Requirements Complete |
| **Developing project schedule** | 2 days | Sep 11 | Sep 12 | All Team | Feasibility Study |
| **Reviewing and finalizing documentation** | 2 days | Sep 12 | Sep 13 | All Team | All Documents Draft |

### Phase 3: Systems Design & Data Infrastructure (Week 4)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Implementing database structure** | 4 days | Sep 14 | Sep 17 | Sanjula | Architecture Approved |
| **Developing data collection scripts** | 5 days | Sep 14 | Sep 18 | Senevirathne | API Integration |
| **Building data validation pipeline** | 3 days | Sep 16 | Sep 18 | Senevirathne | Collection Scripts |
| **Setting up automated data harvesting** | 4 days | Sep 15 | Sep 18 | Senevirathne | Database Ready |
| **Creating ETL processing pipeline** | 3 days | Sep 17 | Sep 19 | Sanjula + Senevirathne | Data Collection |
| **Testing data infrastructure** | 2 days | Sep 19 | Sep 20 | All Team | Pipeline Complete |
| **Optimizing database performance** | 2 days | Sep 18 | Sep 19 | Sanjula | Database Implemented |

### Phase 4: Development & Implementation - ML Models (Week 5)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Performing exploratory data analysis** | 3 days | Sep 21 | Sep 23 | Senevirathne | Data Available |
| **Engineering predictive features** | 4 days | Sep 22 | Sep 25 | Sanjula + Senevirathne | EDA Complete |
| **Training baseline models** | 3 days | Sep 23 | Sep 25 | Sanjula | Features Ready |
| **Developing XGBoost models** | 4 days | Sep 24 | Sep 27 | Sanjula | Baseline Models |
| **Evaluating model performance** | 3 days | Sep 25 | Sep 27 | Sanjula + Senevirathne | Models Trained |
| **Preparing mid-evaluation materials** | 3 days | Sep 25 | Sep 27 | All Team | Models Evaluated |

### Phase 5: Development & Implementation - Backend API (Week 6)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Building Flask backend application** | 4 days | Sep 28 | Oct 1 | Sanjula | Models Ready |
| **Integrating ML models with API** | 3 days | Sep 29 | Oct 1 | Sanjula | Backend Structure |
| **Implementing user authentication** | 3 days | Sep 30 | Oct 2 | Sanjula | API Framework |
| **Testing API endpoints** | 2 days | Oct 1 | Oct 2 | Sanjula | Integration Complete |
| **Conducting mid-evaluation demo** | 1 day | Oct 4 | Oct 4 | All Team | System Functional |
| **Documenting API specifications** | 2 days | Oct 2 | Oct 3 | Sanjula | API Testing |

### Phase 6: Development & Implementation - Frontend (Week 7)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Developing Streamlit dashboard** | 4 days | Oct 5 | Oct 8 | Shaamma | API Available |
| **Integrating frontend with backend** | 4 days | Oct 6 | Oct 9 | Shaamma + Sanjula | Dashboard Base |
| **Implementing data visualizations** | 3 days | Oct 7 | Oct 9 | Shaamma | Integration Working |
| **Optimizing user experience** | 3 days | Oct 8 | Oct 10 | Shaamma | Visualizations Ready |
| **Testing system integration** | 2 days | Oct 9 | Oct 10 | All Team | Frontend Complete |

### Phase 7: Integration and Testing (Week 8)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Executing unit testing** | 3 days | Oct 12 | Oct 14 | All Team | System Integrated |
| **Performing integration testing** | 3 days | Oct 13 | Oct 15 | All Team | Unit Tests Pass |
| **Conducting performance testing** | 3 days | Oct 14 | Oct 16 | Sanjula + Senevirathne | Integration Tests |
| **Running user acceptance testing** | 2 days | Oct 15 | Oct 16 | Shaamma | Performance Validated |
| **Preparing Testing & Evaluation Document** | 3 days | Oct 16 | Oct 18 | Shaamma | Testing Complete |
| **Fixing identified bugs** | 3 days | Oct 16 | Oct 18 | All Team | Testing Results |

### Phase 8: Deployment (Week 9)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Configuring production environment** | 3 days | Oct 19 | Oct 21 | Sanjula | Testing Complete |
| **Deploying system to cloud platform** | 3 days | Oct 20 | Oct 22 | Sanjula | Environment Ready |
| **Implementing Docker containerization** | 2 days | Oct 21 | Oct 22 | Sanjula | Deployment Working |
| **Testing production system** | 2 days | Oct 22 | Oct 23 | All Team | System Deployed |
| **Creating user documentation** | 3 days | Oct 22 | Oct 24 | Shaamma | System Stable |
| **Preparing final presentation** | 3 days | Oct 23 | Oct 25 | All Team | Documentation Ready |

### Phase 9: Final Evaluation & Documentation (Week 10)

| Activity | Duration | Start Date | End Date | Responsible | Dependencies |
|----------|----------|------------|----------|-------------|--------------|
| **Compiling final project report** | 4 days | Oct 26 | Oct 29 | Shaamma | All Components Ready |
| **Rehearsing final presentation** | 2 days | Oct 27 | Oct 28 | All Team | Report Draft |
| **Validating final system** | 2 days | Oct 28 | Oct 29 | All Team | Presentation Ready |
| **Reviewing all documentation** | 2 days | Oct 29 | Oct 30 | All Team | System Validated |
| **Conducting final evaluation** | 1 day | Nov 1 | Nov 1 | All Team | Everything Complete |
| **Submitting final deliverables** | 1 day | Nov 1 | Nov 1 | All Team | Evaluation Done |

---

## Document Preparation Schedule

### Academic Deliverables Timeline

| Document | Preparation Period | Review Period | Submission Date | Primary Author |
|----------|-------------------|---------------|-----------------|----------------|
| **Project Proposal** | Aug 29-31 | Sep 1-5 | Sep 6 | All Team |
| **Feasibility Document** | Sep 9-11 | Sep 12-13 | Sep 13 | All Team |
| **Project Schedule** | Sep 11-12 | Sep 13 | Sep 13 | All Team |
| **System Requirements Specification** | Sep 8-11 | Sep 12-13 | Sep 20 | Shaamma |
| **Software Architecture Document** | Sep 10-12 | Sep 13-19 | Sep 20 | Sanjula |
| **Mid-Evaluation Materials** | Sep 25-27 | Oct 1-3 | Oct 4 | All Team |
| **Testing & Evaluation Document** | Oct 16-18 | Oct 19-20 | Oct 18 | Shaamma |
| **Final Project Report** | Oct 26-29 | Oct 30-31 | Nov 1 | Shaamma |
| **Final Presentation** | Oct 23-25 | Oct 26-31 | Nov 1 | All Team |

---

## Resource Allocation & Parallel Activities

### Team Member Workload Distribution

**Senevirathne S.M.P.U. (Data Lead)**
- **Peak Periods**: Weeks 3-4 (Data Infrastructure), Week 5 (EDA & Features)
- **Primary Focus**: Data collection, API management, feature engineering
- **Parallel Activities**: Can work on data analysis while others develop backend/frontend

**Sanjula N.G.K. (Backend & Model Lead)**
- **Peak Periods**: Weeks 5-6 (ML Models & API), Week 9 (Deployment)
- **Primary Focus**: Machine learning, backend development, system architecture
- **Parallel Activities**: Database work can overlap with data collection

**Shaamma M.S. (Frontend & Documentation Lead)**
- **Peak Periods**: Weeks 7-8 (Frontend & Testing), Weeks 9-10 (Documentation)
- **Primary Focus**: User interface, testing coordination, documentation
- **Parallel Activities**: Documentation can be prepared throughout development

### Overlapping Activities Strategy

**Weeks 3-4**: Data collection (Senevirathne) + Database setup (Sanjula) + Documentation (Shaamma)
**Weeks 5-6**: Model training (Sanjula) + Data analysis (Senevirathne) + Mid-eval prep (Shaamma)
**Weeks 7-8**: Frontend dev (Shaamma) + Backend polish (Sanjula) + Data optimization (Senevirathne)

---

## Risk Management & Contingency

### Critical Path Activities
1. **YouTube API Integration** (Week 1-2) - Foundation for all data work
2. **Data Collection Pipeline** (Week 4) - Required for model training
3. **Model Development** (Week 5) - Core system functionality
4. **System Integration** (Week 7) - Complete system assembly

### Risk Mitigation Strategies
- **API Quota Issues**: Multiple API keys, efficient usage patterns
- **Model Performance**: Baseline models, multiple approaches
- **Integration Problems**: Modular development, early testing
- **Timeline Delays**: Parallel development, scope adjustment protocols

### Buffer Time Allocation
- **Week 2**: 1 day buffer for environment setup issues
- **Week 4**: 1 day buffer for data collection challenges
- **Week 6**: 1 day buffer for model performance optimization
- **Week 8**: 2 days buffer for integration and testing issues

---

## Quality Gates & Milestones

### Weekly Quality Checkpoints
- **Week 2**: Development environment and API integration validated
- **Week 4**: Data infrastructure operational with quality validation
- **Week 6**: ML models trained and mid-evaluation completed successfully
- **Week 8**: System integration complete with comprehensive testing
- **Week 10**: Production deployment and final evaluation completed

### Success Criteria
- **Mid-Evaluation**: Working prototype with basic prediction capability
- **Final Evaluation**: Complete web application with <30% MAPE accuracy
- **Documentation**: All academic requirements met with professional quality
- **Deployment**: System accessible and stable for demonstration

---

## Mentor Meeting Integration

### Scheduled Mentor Interactions
- **Mentor Meetup 1** (Aug 30, Week 1): Project scope validation and guidance
- **Mentor Meetup 2** (Sep 20, Week 4): Architecture review and progress assessment
- **Mentor Meetup 3** (Oct 25, Week 9): Final review and presentation feedback

### Continuous Mentor Engagement
- **Weekly Progress Reports**: Brief updates on achievements and challenges
- **Issue Escalation**: Immediate consultation for blocking technical issues
- **Academic Guidance**: Regular validation of deliverable quality and compliance

---

*This schedule follows the Traditional Software Development Life Cycle methodology with integrated agile practices, ensuring both academic compliance and technical excellence. All activities are named using action verbs and allocated sufficient time to account for potential risks and learning curves.*

**Schedule Status**: Approved by Team  
**Last Updated**: August 6, 2025  
**Next Review**: August 13, 2025 (Week 1 Progress Review)
