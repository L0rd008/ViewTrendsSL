# Contributing to ViewTrendsSL

Thank you for your interest in contributing to ViewTrendsSL! This document provides guidelines and information for contributors to help maintain code quality and project consistency.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community Guidelines](#community-guidelines)

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.9+** installed
- **Git** for version control
- **Redis** (for caching and rate limiting)
- **PostgreSQL** (for production database)
- **YouTube Data API v3** keys (for data collection)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ViewTrendsSL.git
   cd ViewTrendsSL
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/L0rd008/ViewTrendsSL.git
   ```

## 🛠️ Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Add your YouTube API keys, database URLs, etc.
```

### 3. Database Setup

```bash
# For development (SQLite)
python scripts/setup_database.py

# For production (PostgreSQL)
# Ensure PostgreSQL is running and configured in .env
python scripts/setup_database.py --production
```

### 4. Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files (optional)
pre-commit run --all-files
```

### 5. Verify Setup

```bash
# Run tests to verify setup
pytest

# Start development server
python -m src.application.api.app
```

## 📝 Contributing Guidelines

### Branch Strategy

We use **Git Flow** branching strategy:

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/*`**: New features
- **`bugfix/*`**: Bug fixes
- **`hotfix/*`**: Critical production fixes
- **`release/*`**: Release preparation

### Creating a Feature Branch

```bash
# Update develop branch
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/your-feature-name

# Work on your feature
# ... make changes ...

# Commit changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### Commit Message Convention

We follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(prediction): add support for Shorts prediction
fix(api): resolve authentication token validation
docs(readme): update installation instructions
test(services): add unit tests for prediction service
```

## 🎯 Code Standards

### Python Code Style

We use **Black** for code formatting and **flake8** for linting:

```bash
# Format code
black src/ tests/ scripts/

# Check linting
flake8 src/ tests/ scripts/

# Sort imports
isort src/ tests/ scripts/

# Type checking
mypy src/
```

### Code Quality Requirements

- **Line Length**: Maximum 88 characters
- **Import Organization**: Use isort with Black profile
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style for all public classes and functions
- **Test Coverage**: Minimum 80% overall, 90% for critical components

### Documentation Standards

```python
def predict_viewership(
    video_data: Dict[str, Any],
    model_type: str = "auto"
) -> Dict[str, Union[int, float]]:
    """Predict viewership for a YouTube video.
    
    Args:
        video_data: Dictionary containing video metadata including
            title, description, duration, category, etc.
        model_type: Type of model to use ('shorts', 'longform', 'auto').
            Defaults to 'auto' for automatic detection.
    
    Returns:
        Dictionary containing prediction results with keys:
            - predicted_views_24h: Predicted views after 24 hours
            - predicted_views_7d: Predicted views after 7 days
            - confidence_score: Model confidence (0.0 to 1.0)
            - model_used: Which model was used for prediction
    
    Raises:
        ValueError: If video_data is missing required fields
        ModelNotFoundError: If specified model_type is not available
    
    Example:
        >>> video_data = {
        ...     "title": "Amazing Sri Lankan Recipe",
        ...     "duration": 300,
        ...     "category": "Howto & Style"
        ... }
        >>> result = predict_viewership(video_data)
        >>> print(result["predicted_views_24h"])
        1500
    """
```

### File Organization

```python
"""Module docstring describing the module's purpose.

This module contains functionality for YouTube viewership prediction
using machine learning models trained on Sri Lankan video data.
"""

# Standard library imports
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Third-party imports
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# Local imports
from src.business.services.prediction import PredictionService
from src.business.utils.data_validator import DataValidator
```

## 🧪 Testing Requirements

### Test Categories

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **API Tests**: Test HTTP endpoints
4. **End-to-End Tests**: Test complete workflows

### Writing Tests

```python
"""Test module for prediction service functionality."""

import pytest
from unittest.mock import Mock, patch

from src.business.services.prediction.prediction_service import PredictionService
from tests.fixtures.mock_data import generate_mock_video_data


class TestPredictionService:
    """Test cases for PredictionService."""
    
    @pytest.fixture
    def prediction_service(self):
        """Create PredictionService instance for testing."""
        return PredictionService()
    
    @pytest.fixture
    def mock_video_data(self):
        """Generate mock video data for testing."""
        return generate_mock_video_data(is_short=False)
    
    @pytest.mark.unit
    @pytest.mark.prediction
    def test_predict_viewership_returns_valid_result(
        self, prediction_service, mock_video_data
    ):
        """Test that predict_viewership returns valid prediction result."""
        # Act
        result = prediction_service.predict_viewership(mock_video_data)
        
        # Assert
        assert isinstance(result, dict)
        assert "predicted_views_24h" in result
        assert "predicted_views_7d" in result
        assert "confidence_score" in result
        assert 0 <= result["confidence_score"] <= 1
    
    @pytest.mark.unit
    @pytest.mark.prediction
    def test_predict_viewership_handles_missing_data(self, prediction_service):
        """Test that predict_viewership handles missing required data."""
        # Arrange
        incomplete_data = {"title": "Test Video"}
        
        # Act & Assert
        with pytest.raises(ValueError, match="Missing required field"):
            prediction_service.predict_viewership(incomplete_data)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m api

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_services/test_prediction_service.py -v

# Run tests in parallel
pytest -n auto
```

### Test Coverage Requirements

- **Overall Coverage**: Minimum 80%
- **Critical Components**: Minimum 90%
  - Prediction services
  - ML models
  - API endpoints
  - Data validation
- **New Code**: Must maintain or improve coverage

## 🔄 Pull Request Process

### Before Submitting

1. **Update your branch** with latest develop:
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout feature/your-feature
   git rebase develop
   ```

2. **Run quality checks**:
   ```bash
   # Run tests
   pytest
   
   # Check code quality
   pre-commit run --all-files
   
   # Verify coverage
   pytest --cov=src --cov-fail-under=80
   ```

3. **Update documentation** if needed

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Coverage requirements met
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one team member review required
3. **Testing**: All tests must pass with adequate coverage
4. **Documentation**: Updates must be included if applicable

### Merging

- **Squash and merge** for feature branches
- **Merge commit** for release branches
- **Delete branch** after successful merge

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- Browser: [e.g. Chrome 96.0]

**Additional Context**
Any other context about the problem.
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the feature you'd like to see.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
How would you like this feature to work?

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Any other context or screenshots.
```

### Security Issues

**Do not** create public issues for security vulnerabilities. Instead:

1. Email security concerns to: [security@viewtrendssl.com]
2. Include detailed description and steps to reproduce
3. Allow reasonable time for response before public disclosure

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

- **Be respectful** and considerate
- **Be collaborative** and helpful
- **Be patient** with newcomers
- **Focus on constructive feedback**
- **Respect different viewpoints**

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code review and collaboration
- **Email**: Security issues and private matters

### Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor graphs and statistics

## 📚 Additional Resources

### Documentation

- [Project README](README.md)
- [API Documentation](docs/api.md)
- [Architecture Guide](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)

### Development Tools

- [Black Code Formatter](https://black.readthedocs.io/)
- [flake8 Linter](https://flake8.pycqa.org/)
- [pytest Testing Framework](https://pytest.org/)
- [pre-commit Hooks](https://pre-commit.com/)

### Learning Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

## ❓ Getting Help

If you need help:

1. **Check existing documentation** and issues
2. **Search GitHub discussions** for similar questions
3. **Create a new discussion** with detailed information
4. **Join our community** channels for real-time help

## 🙏 Thank You

Thank you for contributing to ViewTrendsSL! Your contributions help make YouTube analytics more accessible to Sri Lankan creators and the broader community.

---

**Happy Contributing! 🚀**
