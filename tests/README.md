# Tests Directory

This directory contains comprehensive test suites for the ViewTrendsSL project, organized by testing type and scope.

## 📁 Directory Structure

### `/unit/` - Unit Tests
**Purpose**: Test individual components in isolation
**Framework**: pytest, unittest
**Coverage Target**: >90% code coverage
**Execution**: Fast, isolated, no external dependencies

#### `/unit/test_services/`
**Purpose**: Test business logic services
**Files**:
- `test_prediction_service.py` - Video prediction service tests
- `test_data_collection_service.py` - Data collection service tests
- `test_feature_engineering_service.py` - Feature engineering tests
- `test_model_service.py` - ML model service tests
- `test_analytics_service.py` - Analytics service tests

**Test Examples**:
```python
def test_prediction_service_shorts():
    """Test prediction service for YouTube Shorts"""
    service = PredictionService()
    video_data = create_mock_shorts_data()
    prediction = service.predict_views(video_data)
    assert prediction > 0
    assert isinstance(prediction, dict)
    assert 'views_24h' in prediction
```

#### `/unit/test_repositories/`
**Purpose**: Test data access layer components
**Files**:
- `test_video_repository.py` - Video data repository tests
- `test_channel_repository.py` - Channel data repository tests
- `test_user_repository.py` - User data repository tests
- `test_snapshot_repository.py` - Performance snapshot tests

**Test Examples**:
```python
def test_video_repository_create():
    """Test video creation in repository"""
    repo = VideoRepository()
    video_data = create_test_video_data()
    video_id = repo.create(video_data)
    assert video_id is not None
    retrieved = repo.get_by_id(video_id)
    assert retrieved.title == video_data['title']
```

#### `/unit/test_ml/`
**Purpose**: Test machine learning components
**Files**:
- `test_feature_engineer.py` - Feature engineering tests
- `test_model_trainer.py` - Model training tests
- `test_model_evaluator.py` - Model evaluation tests
- `test_preprocessor.py` - Data preprocessing tests
- `test_prediction_pipeline.py` - End-to-end prediction tests

**Test Examples**:
```python
def test_feature_engineer_temporal_features():
    """Test temporal feature extraction"""
    engineer = FeatureEngineer()
    video_data = create_test_video_with_timestamp()
    features = engineer.extract_temporal_features(video_data)
    assert 'publish_hour' in features
    assert 'day_of_week' in features
    assert 0 <= features['publish_hour'] <= 23
```

#### `/unit/test_utils/`
**Purpose**: Test utility functions and helpers
**Files**:
- `test_data_validators.py` - Data validation utility tests
- `test_api_helpers.py` - API helper function tests
- `test_time_utils.py` - Time utility function tests
- `test_config_manager.py` - Configuration management tests
- `test_logging_utils.py` - Logging utility tests

### `/integration/` - Integration Tests
**Purpose**: Test component interactions and external integrations
**Framework**: pytest with fixtures
**Coverage**: Critical integration points
**Execution**: Slower, may use external services (with mocking)

#### `/integration/test_api/`
**Purpose**: Test API endpoint integrations
**Files**:
- `test_prediction_endpoints.py` - Prediction API integration tests
- `test_auth_endpoints.py` - Authentication API tests
- `test_analytics_endpoints.py` - Analytics API tests
- `test_middleware_integration.py` - Middleware integration tests

**Test Examples**:
```python
def test_prediction_api_end_to_end():
    """Test complete prediction API workflow"""
    client = TestClient(app)
    video_url = "https://youtube.com/watch?v=test123"
    response = client.post("/api/predict", json={"video_url": video_url})
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert 'confidence' in data
```

#### `/integration/test_database/`
**Purpose**: Test database operations and transactions
**Files**:
- `test_database_operations.py` - Database CRUD operations
- `test_migrations.py` - Database migration tests
- `test_transaction_handling.py` - Transaction management tests
- `test_connection_pooling.py` - Connection pool tests

**Test Examples**:
```python
def test_video_channel_relationship():
    """Test video-channel relationship integrity"""
    with test_db_session() as session:
        channel = create_test_channel(session)
        video = create_test_video(session, channel_id=channel.id)
        session.commit()
        
        retrieved_video = session.query(Video).filter_by(id=video.id).first()
        assert retrieved_video.channel.id == channel.id
```

#### `/integration/test_external/`
**Purpose**: Test external service integrations
**Files**:
- `test_youtube_api_integration.py` - YouTube API integration tests
- `test_monitoring_integration.py` - Monitoring service tests
- `test_cache_integration.py` - Cache service integration tests
- `test_email_service.py` - Email notification tests

**Test Examples**:
```python
@pytest.mark.integration
def test_youtube_api_video_fetch():
    """Test YouTube API video data fetching"""
    api_client = YouTubeAPIClient()
    video_id = "dQw4w9WgXcQ"  # Test video ID
    video_data = api_client.get_video_details(video_id)
    assert video_data is not None
    assert video_data['id'] == video_id
    assert 'title' in video_data
```

### `/fixtures/` - Test Data and Fixtures
**Purpose**: Shared test data, fixtures, and utilities
**Contents**: Mock data, test databases, fixture factories

**Files**:
- `conftest.py` - pytest configuration and shared fixtures
- `mock_data.py` - Mock data generators
- `test_database.py` - Test database setup and teardown
- `api_fixtures.py` - API response fixtures
- `model_fixtures.py` - ML model test fixtures

**Example Fixtures**:
```python
@pytest.fixture
def test_video_data():
    """Fixture providing test video data"""
    return {
        'video_id': 'test123',
        'title': 'Test Video Title',
        'duration': 'PT3M45S',
        'published_at': '2023-08-01T14:30:00Z',
        'view_count': 1000,
        'like_count': 50,
        'comment_count': 10
    }

@pytest.fixture
def mock_youtube_api():
    """Fixture providing mocked YouTube API"""
    with patch('src.external.youtube_api.YouTubeAPIClient') as mock:
        mock.return_value.get_video_details.return_value = test_video_data()
        yield mock
```

### `/performance/` - Performance Tests
**Purpose**: Test system performance, load handling, and scalability
**Framework**: pytest-benchmark, locust
**Metrics**: Response time, throughput, resource usage

**Files**:
- `test_prediction_performance.py` - Prediction endpoint performance
- `test_database_performance.py` - Database query performance
- `test_model_inference_speed.py` - ML model inference speed
- `test_concurrent_users.py` - Concurrent user handling
- `load_test_scenarios.py` - Load testing scenarios

**Performance Test Examples**:
```python
def test_prediction_response_time(benchmark):
    """Test prediction API response time"""
    def make_prediction():
        service = PredictionService()
        return service.predict_views(test_video_data)
    
    result = benchmark(make_prediction)
    assert result is not None
    # Benchmark automatically measures execution time

def test_concurrent_predictions():
    """Test handling multiple concurrent predictions"""
    import concurrent.futures
    
    def make_prediction(video_data):
        service = PredictionService()
        return service.predict_views(video_data)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_prediction, test_video_data) 
                  for _ in range(100)]
        results = [f.result() for f in futures]
    
    assert len(results) == 100
    assert all(r is not None for r in results)
```

## 🧪 Testing Standards

### Test Organization
- **One test file per source file**: `src/services/prediction.py` → `tests/unit/test_services/test_prediction.py`
- **Descriptive test names**: Use `test_function_name_expected_behavior` format
- **Arrange-Act-Assert pattern**: Clear test structure
- **Single assertion per test**: Focus on one behavior per test

### Test Data Management
- **Use fixtures**: Centralize test data creation
- **Isolate tests**: Each test should be independent
- **Clean up**: Ensure tests clean up after themselves
- **Realistic data**: Use data that resembles production data

### Mocking Strategy
- **Mock external dependencies**: APIs, databases, file systems
- **Don't mock what you own**: Test your own code without mocking
- **Mock at boundaries**: Mock at the edge of your system
- **Verify interactions**: Assert that mocks are called correctly

## 🚀 Running Tests

### Local Development
```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_services/test_prediction_service.py

# Run tests matching pattern
pytest -k "test_prediction"
```

### Continuous Integration
```bash
# Fast test suite (unit tests only)
pytest tests/unit/ --maxfail=1

# Full test suite
pytest tests/ --cov=src --cov-fail-under=90

# Performance regression tests
pytest tests/performance/ --benchmark-only
```

### Test Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    slow: Slow running tests
```

## 📊 Test Coverage

### Coverage Targets
- **Overall Coverage**: >90%
- **Critical Components**: >95%
- **New Code**: 100%
- **Integration Points**: >85%

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Generate terminal coverage report
pytest --cov=src --cov-report=term-missing

# Generate XML coverage report (for CI)
pytest --cov=src --cov-report=xml
```

### Coverage Exclusions
```python
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🔧 Test Utilities

### Custom Assertions
```python
def assert_valid_prediction(prediction):
    """Assert that prediction has valid structure"""
    assert isinstance(prediction, dict)
    assert 'views_24h' in prediction
    assert 'views_7d' in prediction
    assert 'confidence' in prediction
    assert 0 <= prediction['confidence'] <= 1

def assert_video_data_complete(video_data):
    """Assert that video data has all required fields"""
    required_fields = ['video_id', 'title', 'duration', 'published_at']
    for field in required_fields:
        assert field in video_data
        assert video_data[field] is not None
```

### Test Helpers
```python
class TestDataBuilder:
    """Builder pattern for creating test data"""
    
    def __init__(self):
        self.data = {}
    
    def with_video_id(self, video_id):
        self.data['video_id'] = video_id
        return self
    
    def with_title(self, title):
        self.data['title'] = title
        return self
    
    def build(self):
        return self.data.copy()

# Usage
video_data = (TestDataBuilder()
              .with_video_id('test123')
              .with_title('Test Video')
              .build())
```

## 🎯 Best Practices

### Writing Effective Tests
1. **Test behavior, not implementation**: Focus on what the code does, not how
2. **Use descriptive names**: Test names should explain the scenario
3. **Keep tests simple**: Each test should be easy to understand
4. **Test edge cases**: Include boundary conditions and error cases
5. **Maintain tests**: Update tests when code changes

### Test Maintenance
1. **Regular review**: Review and update tests regularly
2. **Remove obsolete tests**: Delete tests for removed functionality
3. **Refactor test code**: Apply same quality standards as production code
4. **Document complex tests**: Add comments for complex test scenarios
5. **Monitor test performance**: Keep test suite execution time reasonable

### Debugging Failed Tests
1. **Read the error message**: Understand what the test is checking
2. **Check test data**: Verify test data is correct and up-to-date
3. **Run in isolation**: Run failing test alone to isolate the issue
4. **Use debugger**: Step through code to understand the failure
5. **Check recent changes**: Consider what code changes might have caused the failure

## 🔄 Continuous Testing

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    pytest tests/unit/ --cov=src
    pytest tests/integration/
    pytest tests/performance/ --benchmark-only
```

### Test Automation
- **Automated test execution**: Run tests on every commit
- **Test result reporting**: Generate and publish test reports
- **Performance monitoring**: Track test execution time trends
- **Coverage tracking**: Monitor code coverage over time
- **Failure notifications**: Alert team of test failures
