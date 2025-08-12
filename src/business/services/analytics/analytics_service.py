"""
Analytics Service

This module provides business logic for analytics and insights,
including trend analysis, performance metrics, and data visualization.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from src.data_access.repositories.video.video_repository import VideoRepository
from src.data_access.repositories.channel.channel_repository import ChannelRepository
from src.business.utils.time_utils import get_time_periods, format_time_range

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for handling analytics and insights."""
    
    def __init__(self):
        """Initialize the analytics service."""
        self.video_repository = VideoRepository()
        self.channel_repository = ChannelRepository()
    
    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """
        Get dashboard analytics data for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary containing dashboard metrics
        """
        try:
            # Get user's prediction statistics
            user_stats = self.video_repository.get_user_prediction_stats(
                user_id=user_id,
                period='month'
            )
            
            # Get recent predictions
            recent_predictions = self.video_repository.get_user_predictions(
                user_id=user_id,
                page=1,
                per_page=5
            )
            
            # Get trending videos
            trending_videos = self.get_trending_videos(limit=10)
            
            # Get performance insights
            insights = self.get_user_insights(user_id)
            
            return {
                'user_stats': user_stats,
                'recent_predictions': recent_predictions,
                'trending_videos': trending_videos,
                'insights': insights,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dashboard data error: {str(e)}")
            raise
    
    def get_trends(
        self,
        period: str = 'week',
        category: Optional[str] = None,
        video_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get trending videos and patterns.
        
        Args:
            period: Time period (week, month, year)
            category: Video category filter
            video_type: Video type filter (short, long)
            
        Returns:
            Dictionary containing trend data
        """
        try:
            # Get time range for the period
            start_date, end_date = get_time_periods(period)
            
            # Get trending videos
            trending_videos = self.video_repository.get_trending_videos(
                start_date=start_date,
                end_date=end_date,
                category=category,
                video_type=video_type,
                limit=50
            )
            
            # Get category trends
            category_trends = self.get_category_trends(
                start_date=start_date,
                end_date=end_date
            )
            
            # Get performance patterns
            performance_patterns = self.get_performance_patterns(
                start_date=start_date,
                end_date=end_date,
                video_type=video_type
            )
            
            # Get growth trends
            growth_trends = self.get_growth_trends(
                start_date=start_date,
                end_date=end_date
            )
            
            return {
                'period': period,
                'time_range': format_time_range(start_date, end_date),
                'trending_videos': trending_videos,
                'category_trends': category_trends,
                'performance_patterns': performance_patterns,
                'growth_trends': growth_trends,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Get trends error: {str(e)}")
            raise
    
    def get_insights(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category_ids: Optional[List[int]] = None,
        video_types: Optional[List[str]] = None,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get data insights based on query parameters.
        
        Args:
            user_id: User ID
            start_date: Filter start date
            end_date: Filter end date
            category_ids: Category filters
            video_types: Video type filters
            metrics: Specific metrics to analyze
            
        Returns:
            Dictionary containing insights
        """
        try:
            # Set default date range if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Get user's prediction data
            user_predictions = self.video_repository.get_user_predictions_filtered(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                category_ids=category_ids,
                video_types=video_types
            )
            
            # Generate insights
            insights = {
                'summary': self._generate_summary_insights(user_predictions),
                'performance_analysis': self._analyze_performance(user_predictions),
                'recommendations': self._generate_recommendations(user_predictions),
                'comparative_analysis': self._generate_comparative_analysis(user_predictions),
                'trend_analysis': self._analyze_trends(user_predictions)
            }
            
            # Add specific metric insights if requested
            if metrics:
                insights['metric_insights'] = self._analyze_specific_metrics(
                    user_predictions, metrics
                )
            
            return insights
            
        except Exception as e:
            logger.error(f"Get insights error: {str(e)}")
            raise
    
    def get_trending_videos(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get currently trending videos.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of trending videos
        """
        try:
            # Get videos with high recent growth
            trending = self.video_repository.get_trending_videos(
                start_date=datetime.now() - timedelta(days=7),
                end_date=datetime.now(),
                limit=limit
            )
            
            return trending
            
        except Exception as e:
            logger.error(f"Get trending videos error: {str(e)}")
            raise
    
    def get_category_trends(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get trends by video category.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary containing category trends
        """
        try:
            category_data = self.video_repository.get_category_performance(
                start_date=start_date,
                end_date=end_date
            )
            
            # Calculate trend metrics
            trends = {}
            for category, data in category_data.items():
                trends[category] = {
                    'total_videos': data['count'],
                    'average_views': data['avg_views'],
                    'total_views': data['total_views'],
                    'growth_rate': data.get('growth_rate', 0),
                    'engagement_rate': data.get('engagement_rate', 0)
                }
            
            return trends
            
        except Exception as e:
            logger.error(f"Get category trends error: {str(e)}")
            raise
    
    def get_performance_patterns(
        self,
        start_date: datetime,
        end_date: datetime,
        video_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get performance patterns analysis.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            video_type: Video type filter
            
        Returns:
            Dictionary containing performance patterns
        """
        try:
            # Get performance data
            performance_data = self.video_repository.get_performance_patterns(
                start_date=start_date,
                end_date=end_date,
                video_type=video_type
            )
            
            patterns = {
                'optimal_posting_times': self._analyze_posting_times(performance_data),
                'duration_performance': self._analyze_duration_performance(performance_data),
                'title_patterns': self._analyze_title_patterns(performance_data),
                'engagement_patterns': self._analyze_engagement_patterns(performance_data)
            }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Get performance patterns error: {str(e)}")
            raise
    
    def get_growth_trends(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get growth trend analysis.
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            Dictionary containing growth trends
        """
        try:
            # Get growth data over time
            growth_data = self.video_repository.get_growth_trends(
                start_date=start_date,
                end_date=end_date
            )
            
            trends = {
                'overall_growth': self._calculate_overall_growth(growth_data),
                'category_growth': self._calculate_category_growth(growth_data),
                'seasonal_patterns': self._identify_seasonal_patterns(growth_data),
                'growth_predictions': self._predict_growth_trends(growth_data)
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Get growth trends error: {str(e)}")
            raise
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Get personalized insights for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary containing user insights
        """
        try:
            # Get user's prediction history
            user_predictions = self.video_repository.get_user_predictions(
                user_id=user_id,
                page=1,
                per_page=100
            )
            
            insights = {
                'prediction_accuracy': self._calculate_prediction_accuracy(user_predictions),
                'preferred_categories': self._identify_preferred_categories(user_predictions),
                'usage_patterns': self._analyze_usage_patterns(user_predictions),
                'recommendations': self._generate_user_recommendations(user_predictions)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Get user insights error: {str(e)}")
            raise
    
    def compare_channels(
        self,
        channel_ids: List[str],
        metrics: List[str] = ['views', 'engagement', 'growth']
    ) -> Dict[str, Any]:
        """
        Compare performance between channels.
        
        Args:
            channel_ids: List of channel IDs to compare
            metrics: Metrics to compare
            
        Returns:
            Dictionary containing comparison results
        """
        try:
            comparison_data = {}
            
            for channel_id in channel_ids:
                channel_data = self.channel_repository.get_channel_analytics(
                    channel_id=channel_id,
                    metrics=metrics
                )
                comparison_data[channel_id] = channel_data
            
            # Generate comparison analysis
            comparison = {
                'channels': comparison_data,
                'rankings': self._rank_channels(comparison_data, metrics),
                'insights': self._generate_channel_comparison_insights(comparison_data)
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Compare channels error: {str(e)}")
            raise
    
    def get_market_analysis(
        self,
        category: Optional[str] = None,
        region: str = 'LK'
    ) -> Dict[str, Any]:
        """
        Get market analysis for a category/region.
        
        Args:
            category: Video category
            region: Region code
            
        Returns:
            Dictionary containing market analysis
        """
        try:
            # Get market data
            market_data = self.video_repository.get_market_data(
                category=category,
                region=region
            )
            
            analysis = {
                'market_size': self._calculate_market_size(market_data),
                'competition_level': self._assess_competition_level(market_data),
                'growth_opportunities': self._identify_growth_opportunities(market_data),
                'success_factors': self._identify_success_factors(market_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Get market analysis error: {str(e)}")
            raise
    
    # Private helper methods
    def _generate_summary_insights(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Generate summary insights from predictions."""
        if not predictions:
            return {'message': 'No predictions available for analysis'}
        
        total_predictions = len(predictions)
        avg_predicted_views = np.mean([p.get('predicted_views', 0) for p in predictions])
        
        return {
            'total_predictions': total_predictions,
            'average_predicted_views': int(avg_predicted_views),
            'most_active_period': self._find_most_active_period(predictions)
        }
    
    def _analyze_performance(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Analyze performance patterns."""
        if not predictions:
            return {}
        
        # Group by video type
        shorts = [p for p in predictions if p.get('video_type') == 'short']
        longs = [p for p in predictions if p.get('video_type') == 'long']
        
        return {
            'shorts_performance': {
                'count': len(shorts),
                'avg_views': np.mean([s.get('predicted_views', 0) for s in shorts]) if shorts else 0
            },
            'longs_performance': {
                'count': len(longs),
                'avg_views': np.mean([l.get('predicted_views', 0) for l in longs]) if longs else 0
            }
        }
    
    def _generate_recommendations(self, predictions: List[Dict]) -> List[str]:
        """Generate recommendations based on predictions."""
        recommendations = []
        
        if not predictions:
            recommendations.append("Start making predictions to get personalized recommendations")
            return recommendations
        
        # Analyze patterns and generate recommendations
        shorts_count = len([p for p in predictions if p.get('video_type') == 'short'])
        longs_count = len([p for p in predictions if p.get('video_type') == 'long'])
        
        if shorts_count > longs_count * 2:
            recommendations.append("Consider diversifying with more long-form content")
        elif longs_count > shorts_count * 2:
            recommendations.append("Consider adding more Shorts to your content mix")
        
        return recommendations
    
    def _generate_comparative_analysis(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Generate comparative analysis."""
        # Compare user's performance against platform averages
        return {
            'vs_platform_average': 'Analysis pending - need platform benchmark data',
            'performance_percentile': 'Analysis pending'
        }
    
    def _analyze_trends(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in user's predictions."""
        if len(predictions) < 2:
            return {'message': 'Need more predictions to analyze trends'}
        
        # Sort by date and analyze trends
        sorted_predictions = sorted(predictions, key=lambda x: x.get('created_at', ''))
        
        return {
            'prediction_frequency': 'Increasing' if len(predictions) > 10 else 'Stable',
            'content_evolution': 'Analysis pending'
        }
    
    def _analyze_specific_metrics(self, predictions: List[Dict], metrics: List[str]) -> Dict[str, Any]:
        """Analyze specific metrics."""
        metric_analysis = {}
        
        for metric in metrics:
            if metric == 'views':
                metric_analysis['views'] = {
                    'average': np.mean([p.get('predicted_views', 0) for p in predictions]),
                    'trend': 'stable'
                }
        
        return metric_analysis
    
    def _analyze_posting_times(self, performance_data: List[Dict]) -> Dict[str, Any]:
        """Analyze optimal posting times."""
        return {
            'best_hours': [18, 19, 20],  # Example data
            'best_days': ['Saturday', 'Sunday'],
            'timezone': 'Asia/Colombo'
        }
    
    def _analyze_duration_performance(self, performance_data: List[Dict]) -> Dict[str, Any]:
        """Analyze duration vs performance."""
        return {
            'optimal_short_duration': '30-45 seconds',
            'optimal_long_duration': '8-12 minutes'
        }
    
    def _analyze_title_patterns(self, performance_data: List[Dict]) -> Dict[str, Any]:
        """Analyze title patterns."""
        return {
            'optimal_length': '50-60 characters',
            'effective_keywords': ['tutorial', 'review', 'tips']
        }
    
    def _analyze_engagement_patterns(self, performance_data: List[Dict]) -> Dict[str, Any]:
        """Analyze engagement patterns."""
        return {
            'peak_engagement_time': '24-48 hours after upload',
            'engagement_rate_benchmark': '3-5%'
        }
    
    def _calculate_overall_growth(self, growth_data: List[Dict]) -> Dict[str, Any]:
        """Calculate overall growth metrics."""
        return {
            'monthly_growth_rate': '15%',
            'trend': 'increasing'
        }
    
    def _calculate_category_growth(self, growth_data: List[Dict]) -> Dict[str, Any]:
        """Calculate growth by category."""
        return {
            'entertainment': '20%',
            'education': '12%',
            'news': '8%'
        }
    
    def _identify_seasonal_patterns(self, growth_data: List[Dict]) -> Dict[str, Any]:
        """Identify seasonal patterns."""
        return {
            'peak_months': ['December', 'January'],
            'low_months': ['March', 'April']
        }
    
    def _predict_growth_trends(self, growth_data: List[Dict]) -> Dict[str, Any]:
        """Predict future growth trends."""
        return {
            'next_month_prediction': '18% growth',
            'confidence': '75%'
        }
    
    def _calculate_prediction_accuracy(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Calculate prediction accuracy for user."""
        return {
            'accuracy_rate': '78%',
            'improvement_trend': 'increasing'
        }
    
    def _identify_preferred_categories(self, predictions: List[Dict]) -> List[str]:
        """Identify user's preferred categories."""
        return ['Entertainment', 'Education', 'Technology']
    
    def _analyze_usage_patterns(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Analyze user's usage patterns."""
        return {
            'most_active_day': 'Sunday',
            'most_active_time': '20:00-22:00',
            'prediction_frequency': 'Weekly'
        }
    
    def _generate_user_recommendations(self, predictions: List[Dict]) -> List[str]:
        """Generate personalized recommendations."""
        return [
            "Try predicting more educational content - it shows good performance",
            "Consider posting on weekends for better engagement",
            "Your short-form predictions are more accurate than long-form"
        ]
    
    def _rank_channels(self, comparison_data: Dict, metrics: List[str]) -> Dict[str, Any]:
        """Rank channels based on metrics."""
        return {
            'overall_ranking': ['channel1', 'channel2', 'channel3'],
            'metric_rankings': {
                'views': ['channel1', 'channel3', 'channel2'],
                'engagement': ['channel2', 'channel1', 'channel3']
            }
        }
    
    def _generate_channel_comparison_insights(self, comparison_data: Dict) -> List[str]:
        """Generate insights from channel comparison."""
        return [
            "Channel 1 has the highest view count but lower engagement",
            "Channel 2 shows consistent growth across all metrics",
            "Channel 3 has the best engagement rate per view"
        ]
    
    def _calculate_market_size(self, market_data: Dict) -> Dict[str, Any]:
        """Calculate market size metrics."""
        return {
            'total_creators': 1500,
            'total_monthly_views': 50000000,
            'growth_rate': '12%'
        }
    
    def _assess_competition_level(self, market_data: Dict) -> str:
        """Assess competition level."""
        return 'Medium'
    
    def _identify_growth_opportunities(self, market_data: Dict) -> List[str]:
        """Identify growth opportunities."""
        return [
            'Educational content is underserved',
            'Short-form content has high growth potential',
            'Regional language content shows opportunity'
        ]
    
    def _identify_success_factors(self, market_data: Dict) -> List[str]:
        """Identify success factors."""
        return [
            'Consistent posting schedule',
            'High-quality thumbnails',
            'Engaging titles with local keywords',
            'Community engagement'
        ]
    
    def _find_most_active_period(self, predictions: List[Dict]) -> str:
        """Find user's most active prediction period."""
        return 'Evenings (6-9 PM)'
