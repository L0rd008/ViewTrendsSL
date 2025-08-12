"""
Prediction API Module

This module provides prediction-related API endpoints for the ViewTrendsSL application,
including video viewership forecasting and prediction analytics.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint
from .routes import prediction_bp

# Export the prediction blueprint
__all__ = ['prediction_bp']
