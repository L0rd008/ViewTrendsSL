# ViewTrendsSL
## YouTube Viewership Forecasting for Sri Lankan Audience

**Course**: In22-S5-CS3501 - Data Science and Engineering Project  
**Institution**: University of Moratuwa  
**Team**: Senevirathne S.M.P.U., Sanjula N.G.K., Shaamma M.S.  

---

## 🚀 Quick Start

For complete setup and development instructions, see our **[Development Guide](Docs/Development%20Guide.md)**.

### Prerequisites
- Git, Docker Desktop, Python 3.9+, VS Code

### Get Running in 30 Minutes
```bash
# 1. Clone and setup repository
git clone https://github.com/L0rd008/ViewTrendsSL.git
cd ViewTrendsSL

# 2. Create environment file
cp .env.example .env
# Edit .env with your API keys

# 3. Build and run with Docker
docker-compose up --build

# 4. Access the application
# Web App: http://localhost:8501
# API: http://localhost:5000
```

---

## 📋 Project Overview

ViewTrendsSL is a machine learning-powered tool for predicting YouTube video viewership specifically tailored for Sri Lankan audiences. This project uses advanced data science techniques to forecast video performance based on metadata, channel authority, and temporal patterns.

### 🎯 Key Features
- **Accurate Predictions**: Separate XGBoost models for Shorts and Long-form videos
- **Sri Lankan Focus**: Trained specifically on Sri Lankan YouTube content
- **Real-time Analysis**: Live predictions using YouTube Data API v3
- **Interactive Dashboard**: User-friendly Streamlit interface
- **Comprehensive API**: RESTful endpoints for integration

### 🏗️ Architecture
- **5-Layer Architecture**: Clean separation of concerns
- **Microservices Ready**: Modular design for scalability
- **Docker Containerized**: Consistent deployment across environments
- **PostgreSQL Database**: Robust data storage and retrieval

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[Development Guide](Docs/Development%20Guide.md)** | **Complete implementation reference** |
| [Project Plan](Docs/Project%20Plan.md) | Project overview and requirements |
| [Software Requirements Specification](Docs/Software%20Requirements%20Specification.md) | Detailed system requirements |
| [Software Architecture Document](Docs/Software%20Architecture%20Document.md) | System architecture and design |
| [Feasibility Report](Docs/Feasibility%20Report.md) | Technical and business feasibility |
| [Project Schedule](Docs/Project%20Schedule.md) | Timeline and milestones |

---

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework and API
- **XGBoost** - Machine learning models
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database

### Frontend
- **Streamlit** - Interactive web dashboard
- **Plotly** - Data visualization
- **HTML/CSS/JS** - Custom UI components

### Data & ML
- **YouTube Data API v3** - Data collection
- **Pandas/NumPy** - Data processing
- **Scikit-learn** - ML pipeline
- **TextBlob** - Natural language processing

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **pytest** - Testing framework
- **Black/Flake8** - Code quality

---

## 👥 Team Responsibilities

| Team Member | Role | Primary Focus |
|-------------|------|---------------|
| **Senevirathne S.M.P.U.** | Data Lead | Data collection, EDA, API integration |
| **Sanjula N.G.K.** | Backend Lead | ML models, API, database, DevOps |
| **Shaamma M.S.** | Frontend Lead | UI, documentation, testing |

---

## 🚦 Project Status

### Current Phase: Development (Week 3/10)
- ✅ Project planning and documentation
- ✅ Architecture design and file structure
- 🔄 Environment setup and basic implementation
- ⏳ Data collection pipeline
- ⏳ Machine learning model development

### Upcoming Milestones
- **Week 4**: Core API and database implementation
- **Week 6**: ML model training and evaluation
- **Week 8**: Frontend development and integration
- **Week 10**: Final deployment and presentation

---

## 🔧 Development Setup

### Option 1: Docker (Recommended)
```bash
# Clone repository
git clone https://github.com/L0rd008/ViewTrendsSL.git
cd ViewTrendsSL

# Setup environment
cp .env.example .env
# Add your YouTube API keys to .env

# Run with Docker
docker-compose up --build
```

### Option 2: Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python scripts/database/create_schema.py

# Run application
python src/application/app.py
```

---

## 📊 Usage Examples

### API Usage
```python
import requests

# Predict video performance
response = requests.post('http://localhost:5000/api/v1/predict', 
                        json={'video_url': 'https://youtube.com/watch?v=...'})
prediction = response.json()
print(f"Predicted 7-day views: {prediction['data']['predictions']['7_days']}")
```

### Web Interface
1. Navigate to http://localhost:8501
2. Enter a YouTube video URL
3. Click "Generate Prediction"
4. View interactive forecast chart

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

---

## 📈 Performance Targets

- **Prediction Accuracy**: MAPE < 30% for 7-day forecasts
- **Response Time**: < 30 seconds end-to-end
- **Availability**: 99.5% uptime during evaluation
- **Scalability**: Support 100+ concurrent users

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP-8 style guidelines
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **University of Moratuwa** - Academic support and guidance
- **YouTube Data API** - Data source for model training
- **Open Source Community** - Libraries and frameworks used

---

## 📞 Contact

For questions, issues, or contributions:

- **Project Repository**: [GitHub](https://github.com/L0rd008/ViewTrendsSL)
- **Documentation**: [Development Guide](Docs/Development%20Guide.md)
- **Issues**: [GitHub Issues](https://github.com/L0rd008/ViewTrendsSL/issues)

---

**⚡ Ready to predict the future of YouTube in Sri Lanka? Start with our [Development Guide](Docs/Development%20Guide.md)!**
