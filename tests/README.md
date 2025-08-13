# ViewTrendsSL Testing Framework

This directory contains the comprehensive testing suite for the ViewTrendsSL project, including unit tests, integration tests, fixtures, and testing utilities.

## 📁 Directory Structure

```
tests/
├── __init__.py                     # Test package initialization
├── README.md                       # This file
├── pytest.ini                     # Pytest configuration
├── requirements-test.txt           # Testing dependencies
├── fixtures/                       # Test fixtures and utilities
│   ├── conftest.py                # Global pytest fixtures
│   ├── mock_data.py               # Mock data generators
│   └── test_database.py           # Database testing utilities
├── unit/                          # Unit tests
│   ├── test_services/             # Service layer tests
│   └── test_ml/                   # ML component tests
└── integration/                   # Integration tests
    └── test_api_endpoints.py      # API endpoint tests
```

## 🚀 Quick Start

### 1. Install Testing Dependencies

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Or install with main dependencies
pip install -r requirements.txt -r tests/requirements-test.txt
```

### 2. Run All Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api          # API tests only
```

### 3. Generate Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View coverage report
open tests/coverage_html/index.html
```

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **Service Tests**: Business logic and service layer functionality
- **ML Tests**: Machine learning models and feature engineering
- **Utility Tests**: Helper functions and utilities

```bash
# Run unit tests
pytest tests/unit/ -v

# Run specific unit test files
pytest tests/unit/test_services/test_prediction_service.py -v
pytest tests/unit/test_ml/test_feature_extractor.py -v
```

### Integration Tests (`tests/integration/`)

Test component interactions and API endpoints:

- **API Endpoint Tests**: Complete request-response cycles
- **Database Integration**: Real database operations
- **End-to-End Workflows**: Complete user journeys

```bash
# Run integration tests
pytest tests/integration/ -v

# Run API tests specifically
pytest tests/integration/test_api_endpoints.py -v
```

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

Key configuration options:

- **Coverage**: Minimum 80% coverage required
- **Markers**: Organized test categorization
- **Timeouts**: 300-second test timeout
- **Output**: Verbose reporting with coverage

### Test Markers

Use markers to categorize and run specific test types:

```bash
pytest -m "unit and prediction"     # Unit tests for prediction
pytest -m "integration and api"     # Integration API tests
pytest -m "not slow"               # Skip slow tests
pytest -m "database"               # Database-related tests
```

Available markers:
- `unit`: Unit tests
- `integration`: Integration tests
- `slow`: Slow running tests
- `api`: API endpoint tests
- `database`: Database related tests
- `ml`: Machine learning tests
- `auth`: Authentication tests
- `prediction`: Prediction service tests
- `analytics`: Analytics service tests
- `data_collection`: Data collection tests
- `feature_engineering`: Feature engineering tests
- `performance`: Performance tests
- `security`: Security tests

## 🛠️ Test Utilities

### Mock Data Generation (`fixtures/mock_data.py`)

Generate realistic test data:

```python
from tests.fixtures.mock_data import (
    generate_mock_video_data,
    generate_mock_channel_data,
    generate_video_id
)

# Generate mock video data
video_data = generate_mock_video_data(is_short=True)
channel_data = generate_mock_channel_data()
```

### Database Testing (`fixtures/test_database.py`)

Temporary test databases:

```python
from tests.fixtures.test_database import temporary_test_database

# Use temporary database in tests
with temporary_test_database('mixed') as db:
    # Test database operations
    result = db.execute_query("SELECT * FROM videos")
```

### Global Fixtures (`fixtures/conftest.py`)

Shared test fixtures:

```python
# Available fixtures:
# - sample_video_data
# - sample_channel_data
# - mock_youtube_api
# - test_database
# - authenticated_user
```

## 📊 Coverage Requirements

### Minimum Coverage Targets

- **Overall**: 80% minimum coverage
- **Critical Components**: 90%+ coverage
  - Prediction services
  - ML models
  - API endpoints
  - Data validation

### Coverage Reports

```bash
# Generate different coverage report formats
pytest --cov=src --cov-report=html      # HTML report
pytest --cov=src --cov-report=term      # Terminal report
pytest --cov=src --cov-report=xml       # XML report (for CI)
```

## 🔍 Testing Best Practices

### 1. Test Structure

Follow the AAA pattern:
- **Arrange**: Set up test data and conditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results

```python
def test_prediction_service():
    # Arrange
    video_data = generate_mock_video_data()
    service = PredictionService()
    
    # Act
    result = service.predict_viewership(video_data)
    
    # Assert
    assert result['confidence_score'] > 0
    assert 'predicted_views_24h' in result
```

### 2. Test Isolation

- Each test should be independent
- Use fixtures for setup and teardown
- Mock external dependencies

### 3. Descriptive Test Names

```python
def test_prediction_service_returns_valid_forecast_for_shorts():
    """Test that prediction service returns valid forecast for short videos."""
    pass

def test_feature_extractor_handles_missing_description_gracefully():
    """Test that feature extractor handles missing video description."""
    pass
```

### 4. Mock External Dependencies

```python
@patch('src.business.services.prediction.prediction_service.YouTubeAPI')
def test_prediction_with_mocked_api(mock_api):
    mock_api.return_value.get_video_data.return_value = mock_data
    # Test implementation
```

## 🚨 Continuous Integration

### GitHub Actions Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Scheduled runs (daily)

### Test Commands for CI

```bash
# Install dependencies
pip install -r requirements.txt -r tests/requirements-test.txt

# Run tests with coverage
pytest --cov=src --cov-report=xml --cov-fail-under=80

# Run security tests
bandit -r src/
safety check

# Run code quality checks
flake8 src/
black --check src/
isort --check-only src/
mypy src/
```

## 🐛 Debugging Tests

### Running Individual Tests

```bash
# Run specific test
pytest tests/unit/test_services/test_prediction_service.py::TestPredictionService::test_predict_viewership -v

# Run with debugging
pytest --pdb tests/unit/test_services/test_prediction_service.py

# Run with print statements
pytest -s tests/unit/test_services/test_prediction_service.py
```

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes project root
2. **Database Errors**: Check test database setup
3. **Mock Issues**: Verify mock paths and return values
4. **Fixture Errors**: Check fixture dependencies and scope

## 📈 Performance Testing

### Benchmark Tests

```bash
# Run performance benchmarks
pytest --benchmark-only

# Generate benchmark report
pytest --benchmark-histogram
```

### Load Testing

```bash
# Run load tests (requires locust)
locust -f tests/load/locustfile.py --host=http://localhost:5000
```

## 🔒 Security Testing

### Security Test Suite

```bash
# Run security tests
pytest -m security

# Run bandit security linter
bandit -r src/

# Check for known vulnerabilities
safety check
```

## 📝 Writing New Tests

### 1. Choose Test Type

- **Unit Test**: Testing individual functions/methods
- **Integration Test**: Testing component interactions
- **End-to-End Test**: Testing complete workflows

### 2. Create Test File

```python
"""
Test module for [component name]

Description of what this module tests.
"""

import pytest
from unittest.mock import Mock, patch

from src.path.to.component import ComponentClass
from tests.fixtures.mock_data import generate_mock_data


class TestComponentClass:
    """Test cases for ComponentClass."""
    
    @pytest.fixture
    def component(self):
        """Create component instance for testing."""
        return ComponentClass()
    
    def test_method_name(self, component):
        """Test description."""
        # Arrange
        test_data = generate_mock_data()
        
        # Act
        result = component.method(test_data)
        
        # Assert
        assert result is not None
        assert isinstance(result, dict)
```

### 3. Add Appropriate Markers

```python
@pytest.mark.unit
@pytest.mark.prediction
def test_prediction_functionality():
    """Test prediction functionality."""
    pass
```

## 🤝 Contributing to Tests

### Before Submitting

1. **Run Full Test Suite**: `pytest`
2. **Check Coverage**: Ensure new code has adequate coverage
3. **Follow Naming Conventions**: Use descriptive test names
4. **Add Documentation**: Document complex test scenarios
5. **Update Fixtures**: Add new mock data if needed

### Test Review Checklist

- [ ] Tests are isolated and independent
- [ ] External dependencies are mocked
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Performance implications considered
- [ ] Security aspects addressed

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [Mock Library Documentation](https://docs.python.org/3/library/unittest.mock.html)

## 🆘 Getting Help

If you encounter issues with tests:

1. Check this README for common solutions
2. Review existing test examples
3. Ask team members for guidance
4. Create an issue with detailed error information

---

**Happy Testing! 🧪✨**
