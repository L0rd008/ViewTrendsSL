"""
Analytics API Module

This module provides analytics-related API endpoints for the ViewTrendsSL application,
including data insights, trend analysis, and performance metrics.

Author: ViewTrendsSL Team
Date: 2025
"""

from flask import Blueprint
from .routes import analytics_bp

# Export the analytics blueprint
__all__ = ['analytics_bp']
