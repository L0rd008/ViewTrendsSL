"""
YouTube Analytics Service for ViewTrendsSL

This module provides analytics and aggregation operations for YouTube data
using the collected data and API services.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from src.external.youtube_api.services.channel_service import get_channel_service
from src.external.youtube_api.services.video_service import get_video_service
from src.external.youtube_api.models import ChannelData, VideoData
from src.external.youtube_api.exceptions import YouTubeAPIError, QuotaExceededError

# Configure logging
logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for YouTube data analytics and insights."""
    
    def __init__(self):
        """Initialize the analytics service."""
        self.channel_service = get_channel_service()
        self.video_service = get_video_service()
    
    def analyze_channel_performance(self, channel_id: str) -> Dict[str, Any]:
        """
        Analyze performance metrics for a specific channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Dictionary with channel performance analytics
            
        Raises:
            YouTubeAPIError: If API request fails
        """
        try:
            # Get channel data
            channel_data = self.channel_service.get_channel_by_id(channel_id)
            if not channel_data:
                raise YouTubeAPIError(f"Channel not found: {channel_id}")
            
            # Get recent videos (last 50)
            videos = self.video_service.get_channel_videos(
                channel_id=channel_id,
                max_results=50
            )
            
            if not videos:
                logger.warning(f"No videos found for channel: {channel_id}")
                return self._empty_channel_analysis(channel_data)
            
            # Separate shorts and long-form videos
            shorts = [v for v in videos if v.is_short]
            long_form = [v for v in videos if not v.is_short]
            
            # Calculate metrics
            total_views = sum(v.statistics.view_count for v in videos)
            total_likes = sum(v.statistics.like_count for v in videos)
            total_comments = sum(v.statistics.comment_count for v in videos)
            
            avg_views = total_views / len(videos) if videos else 0
            avg_likes = total_likes / len(videos) if videos else 0
            avg_comments = total_comments / len(videos) if videos else 0
            
            # Engagement rate (likes + comments) / views
            engagement_rate = ((total_likes + total_comments) / total_views * 100) if total_views > 0 else 0
            
            # Top performing videos
            top_videos = sorted(videos, key=lambda v: v.statistics.view_count, reverse=True)[:5]
            
            # Category analysis
            category_stats = self._analyze_categories(videos)
            
            # Upload frequency analysis
            upload_frequency = self._analyze_upload_frequency(videos)
            
            # Performance comparison
            shorts_performance = self._analyze_video_group(shorts, "Shorts")
            long_form_performance = self._analyze_video_group(long_form, "Long-form")
            
            analysis = {
                'channel_info': {
                    'channel_id': channel_data.channel_id,
                    'title': channel_data.title,
                    'subscriber_count': channel_data.statistics.subscriber_count,
                    'total_videos': channel_data.statistics.video_count,
                    'total_views': channel_data.statistics.view_count
                },
                'analyzed_videos': {
                    'total_analyzed': len(videos),
                    'shorts_count': len(shorts),
                    'long_form_count': len(long_form)
                },
                'performance_metrics': {
                    'total_views': total_views,
                    'total_likes': total_likes,
                    'total_comments': total_comments,
                    'average_views': round(avg_views, 2),
                    'average_likes': round(avg_likes, 2),
                    'average_comments': round(avg_comments, 2),
                    'engagement_rate': round(engagement_rate, 2)
                },
                'top_videos': [
                    {
                        'video_id': v.video_id,
                        'title': v.title,
                        'views': v.statistics.view_count,
                        'likes': v.statistics.like_count,
                        'comments': v.statistics.comment_count,
                        'is_short': v.is_short
                    } for v in top_videos
                ],
                'category_analysis': category_stats,
                'upload_frequency': upload_frequency,
                'shorts_performance': shorts_performance,
                'long_form_performance': long_form_performance
            }
            
            logger.info(f"Completed performance analysis for channel: {channel_data.title}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing channel performance for {channel_id}: {e}")
            raise
    
    def compare_channels(self, channel_ids: List[str]) -> Dict[str, Any]:
        """
        Compare performance metrics across multiple channels.
        
        Args:
            channel_ids: List of YouTube channel IDs
            
        Returns:
            Dictionary with channel comparison data
            
        Raises:
            YouTubeAPIError: If API request fails
        """
        try:
            if len(channel_ids) < 2:
                raise ValueError("At least 2 channels required for comparison")
            
            channel_analyses = []
            
            for channel_id in channel_ids:
                try:
                    analysis = self.analyze_channel_performance(channel_id)
                    channel_analyses.append(analysis)
                except Exception as e:
                    logger.warning(f"Failed to analyze channel {channel_id}: {e}")
                    continue
            
            if len(channel_analyses) < 2:
                raise YouTubeAPIError("Insufficient channel data for comparison")
            
            # Create comparison metrics
            comparison = {
                'channels': [],
                'metrics_comparison': {},
                'rankings': {}
            }
            
            # Extract channel summaries
            for analysis in channel_analyses:
                channel_summary = {
                    'channel_id': analysis['channel_info']['channel_id'],
                    'title': analysis['channel_info']['title'],
                    'subscribers': analysis['channel_info']['subscriber_count'],
                    'avg_views': analysis['performance_metrics']['average_views'],
                    'engagement_rate': analysis['performance_metrics']['engagement_rate'],
                    'shorts_count': analysis['analyzed_videos']['shorts_count'],
                    'long_form_count': analysis['analyzed_videos']['long_form_count']
                }
                comparison['channels'].append(channel_summary)
            
            # Calculate rankings
            comparison['rankings'] = {
                'by_subscribers': sorted(comparison['channels'], 
                                       key=lambda x: x['subscribers'], reverse=True),
                'by_avg_views': sorted(comparison['channels'], 
                                     key=lambda x: x['avg_views'], reverse=True),
                'by_engagement': sorted(comparison['channels'], 
                                      key=lambda x: x['engagement_rate'], reverse=True)
            }
            
            # Calculate comparison metrics
            subscribers = [c['subscribers'] for c in comparison['channels']]
            avg_views = [c['avg_views'] for c in comparison['channels']]
            engagement_rates = [c['engagement_rate'] for c in comparison['channels']]
            
            comparison['metrics_comparison'] = {
                'subscribers': {
                    'min': min(subscribers),
                    'max': max(subscribers),
                    'avg': sum(subscribers) / len(subscribers)
                },
                'average_views': {
                    'min': min(avg_views),
                    'max': max(avg_views),
                    'avg': sum(avg_views) / len(avg_views)
                },
                'engagement_rate': {
                    'min': min(engagement_rates),
                    'max': max(engagement_rates),
                    'avg': sum(engagement_rates) / len(engagement_rates)
                }
            }
            
            logger.info(f"Completed comparison of {len(channel_analyses)} channels")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing channels: {e}")
            raise
    
    def analyze_trending_content(
        self, 
        region_code: str = 'LK', 
        category_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze trending content patterns.
        
        Args:
            region_code: Region code for trending analysis
            category_id: Optional category filter
            
        Returns:
            Dictionary with trending content analysis
            
        Raises:
            YouTubeAPIError: If API request fails
        """
        try:
            # Get trending videos
            trending_videos = self.video_service.get_trending_videos(
                region_code=region_code,
                category_id=category_id,
                max_results=50
            )
            
            if not trending_videos:
                logger.warning(f"No trending videos found for region: {region_code}")
                return {'error': 'No trending videos found'}
            
            # Analyze trending patterns
            analysis = {
                'region': region_code,
                'category_filter': category_id,
                'total_videos': len(trending_videos),
                'content_analysis': self._analyze_trending_patterns(trending_videos),
                'top_channels': self._get_top_trending_channels(trending_videos),
                'duration_analysis': self._analyze_duration_patterns(trending_videos),
                'engagement_patterns': self._analyze_engagement_patterns(trending_videos)
            }
            
            logger.info(f"Completed trending analysis for region {region_code}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trending content: {e}")
            raise
    
    def get_sri_lankan_insights(self) -> Dict[str, Any]:
        """
        Get insights specific to Sri Lankan YouTube content.
        
        Returns:
            Dictionary with Sri Lankan content insights
            
        Raises:
            YouTubeAPIError: If API request fails
        """
        try:
            # Sri Lankan keywords for discovery
            sri_lankan_keywords = [
                'sri lanka', 'sinhala', 'tamil', 'colombo', 'kandy',
                'lanka', 'ceylon', 'lk news', 'sri lankan'
            ]
            
            # Search for Sri Lankan content
            all_channels = []
            all_videos = []
            
            for keyword in sri_lankan_keywords[:3]:  # Limit to avoid quota issues
                try:
                    # Search channels
                    channels = self.channel_service.search_channels(
                        query=keyword,
                        max_results=10,
                        region_code='LK'
                    )
                    all_channels.extend(channels)
                    
                    # Search videos
                    videos = self.video_service.search_videos(
                        query=keyword,
                        max_results=10,
                        region_code='LK'
                    )
                    all_videos.extend(videos)
                    
                except QuotaExceededError:
                    logger.warning("Quota exceeded during Sri Lankan content discovery")
                    break
                except Exception as e:
                    logger.warning(f"Error searching for keyword '{keyword}': {e}")
                    continue
            
            # Remove duplicates
            unique_channels = {c.channel_id: c for c in all_channels}.values()
            unique_videos = {v.video_id: v for v in all_videos}.values()
            
            # Analyze Sri Lankan content patterns
            insights = {
                'discovery_summary': {
                    'channels_found': len(unique_channels),
                    'videos_found': len(unique_videos),
                    'keywords_used': sri_lankan_keywords[:3]
                },
                'channel_insights': self._analyze_sri_lankan_channels(list(unique_channels)),
                'content_patterns': self._analyze_sri_lankan_content(list(unique_videos)),
                'language_distribution': self._analyze_language_distribution(list(unique_videos)),
                'popular_categories': self._analyze_popular_categories(list(unique_videos))
            }
            
            logger.info("Completed Sri Lankan content insights analysis")
            return insights
            
        except Exception as e:
            logger.error(f"Error getting Sri Lankan insights: {e}")
            raise
    
    def _empty_channel_analysis(self, channel_data: ChannelData) -> Dict[str, Any]:
        """Create empty analysis structure for channels with no videos."""
        return {
            'channel_info': {
                'channel_id': channel_data.channel_id,
                'title': channel_data.title,
                'subscriber_count': channel_data.statistics.subscriber_count,
                'total_videos': channel_data.statistics.video_count,
                'total_views': channel_data.statistics.view_count
            },
            'analyzed_videos': {'total_analyzed': 0, 'shorts_count': 0, 'long_form_count': 0},
            'performance_metrics': {
                'total_views': 0, 'total_likes': 0, 'total_comments': 0,
                'average_views': 0, 'average_likes': 0, 'average_comments': 0,
                'engagement_rate': 0
            },
            'top_videos': [],
            'category_analysis': {},
            'upload_frequency': {},
            'shorts_performance': {},
            'long_form_performance': {}
        }
    
    def _analyze_categories(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze video performance by category."""
        category_stats = defaultdict(lambda: {'count': 0, 'total_views': 0, 'total_likes': 0})
        
        for video in videos:
            category = video.category_id or 'Unknown'
            category_stats[category]['count'] += 1
            category_stats[category]['total_views'] += video.statistics.view_count
            category_stats[category]['total_likes'] += video.statistics.like_count
        
        # Calculate averages
        result = {}
        for category, stats in category_stats.items():
            result[category] = {
                'video_count': stats['count'],
                'total_views': stats['total_views'],
                'average_views': stats['total_views'] / stats['count'],
                'total_likes': stats['total_likes'],
                'average_likes': stats['total_likes'] / stats['count']
            }
        
        return result
    
    def _analyze_upload_frequency(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze upload frequency patterns."""
        if not videos:
            return {}
        
        # Group videos by month
        monthly_uploads = defaultdict(int)
        
        for video in videos:
            if video.published_at:
                try:
                    published_date = datetime.fromisoformat(video.published_at.replace('Z', '+00:00'))
                    month_key = published_date.strftime('%Y-%m')
                    monthly_uploads[month_key] += 1
                except Exception:
                    continue
        
        if not monthly_uploads:
            return {}
        
        # Calculate statistics
        upload_counts = list(monthly_uploads.values())
        
        return {
            'monthly_uploads': dict(monthly_uploads),
            'average_per_month': sum(upload_counts) / len(upload_counts),
            'max_per_month': max(upload_counts),
            'min_per_month': min(upload_counts),
            'total_months': len(monthly_uploads)
        }
    
    def _analyze_video_group(self, videos: List[VideoData], group_name: str) -> Dict[str, Any]:
        """Analyze performance metrics for a group of videos."""
        if not videos:
            return {'group_name': group_name, 'count': 0}
        
        total_views = sum(v.statistics.view_count for v in videos)
        total_likes = sum(v.statistics.like_count for v in videos)
        total_comments = sum(v.statistics.comment_count for v in videos)
        
        return {
            'group_name': group_name,
            'count': len(videos),
            'total_views': total_views,
            'average_views': total_views / len(videos),
            'total_likes': total_likes,
            'average_likes': total_likes / len(videos),
            'total_comments': total_comments,
            'average_comments': total_comments / len(videos),
            'engagement_rate': ((total_likes + total_comments) / total_views * 100) if total_views > 0 else 0
        }
    
    def _analyze_trending_patterns(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze patterns in trending videos."""
        shorts_count = sum(1 for v in videos if v.is_short)
        long_form_count = len(videos) - shorts_count
        
        # Analyze titles
        title_words = []
        for video in videos:
            title_words.extend(video.title.lower().split())
        
        common_words = Counter(title_words).most_common(10)
        
        return {
            'format_distribution': {
                'shorts': shorts_count,
                'long_form': long_form_count,
                'shorts_percentage': (shorts_count / len(videos)) * 100
            },
            'common_title_words': common_words,
            'average_title_length': sum(len(v.title) for v in videos) / len(videos)
        }
    
    def _get_top_trending_channels(self, videos: List[VideoData]) -> List[Dict[str, Any]]:
        """Get top channels from trending videos."""
        channel_stats = defaultdict(lambda: {'count': 0, 'total_views': 0})
        
        for video in videos:
            channel_stats[video.channel_id]['count'] += 1
            channel_stats[video.channel_id]['total_views'] += video.statistics.view_count
            channel_stats[video.channel_id]['title'] = video.channel_title
        
        # Sort by video count
        top_channels = sorted(
            channel_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:10]
        
        return [
            {
                'channel_id': channel_id,
                'channel_title': stats['title'],
                'trending_videos': stats['count'],
                'total_views': stats['total_views']
            }
            for channel_id, stats in top_channels
        ]
    
    def _analyze_duration_patterns(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze duration patterns in videos."""
        durations = [v.duration_seconds for v in videos if v.duration_seconds > 0]
        
        if not durations:
            return {}
        
        return {
            'average_duration': sum(durations) / len(durations),
            'max_duration': max(durations),
            'min_duration': min(durations),
            'shorts_count': sum(1 for d in durations if d <= 60),
            'medium_count': sum(1 for d in durations if 60 < d <= 600),
            'long_count': sum(1 for d in durations if d > 600)
        }
    
    def _analyze_engagement_patterns(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze engagement patterns in videos."""
        engagement_rates = []
        
        for video in videos:
            if video.statistics.view_count > 0:
                engagement = ((video.statistics.like_count + video.statistics.comment_count) 
                            / video.statistics.view_count) * 100
                engagement_rates.append(engagement)
        
        if not engagement_rates:
            return {}
        
        return {
            'average_engagement_rate': sum(engagement_rates) / len(engagement_rates),
            'max_engagement_rate': max(engagement_rates),
            'min_engagement_rate': min(engagement_rates),
            'high_engagement_count': sum(1 for e in engagement_rates if e > 5),
            'medium_engagement_count': sum(1 for e in engagement_rates if 1 < e <= 5),
            'low_engagement_count': sum(1 for e in engagement_rates if e <= 1)
        }
    
    def _analyze_sri_lankan_channels(self, channels: List[ChannelData]) -> Dict[str, Any]:
        """Analyze Sri Lankan channel characteristics."""
        if not channels:
            return {}
        
        total_subscribers = sum(c.statistics.subscriber_count for c in channels)
        total_videos = sum(c.statistics.video_count for c in channels)
        
        # Language analysis
        languages = [c.default_language for c in channels if c.default_language]
        language_dist = Counter(languages)
        
        return {
            'total_channels': len(channels),
            'total_subscribers': total_subscribers,
            'average_subscribers': total_subscribers / len(channels),
            'total_videos': total_videos,
            'average_videos_per_channel': total_videos / len(channels),
            'language_distribution': dict(language_dist),
            'channels_with_country_lk': sum(1 for c in channels if c.country == 'LK')
        }
    
    def _analyze_sri_lankan_content(self, videos: List[VideoData]) -> Dict[str, Any]:
        """Analyze Sri Lankan video content patterns."""
        if not videos:
            return {}
        
        total_views = sum(v.statistics.view_count for v in videos)
        shorts_count = sum(1 for v in videos if v.is_short)
        
        return {
            'total_videos': len(videos),
            'total_views': total_views,
            'average_views': total_views / len(videos),
            'shorts_percentage': (shorts_count / len(videos)) * 100,
            'average_duration': sum(v.duration_seconds for v in videos) / len(videos)
        }
    
    def _analyze_language_distribution(self, videos: List[VideoData]) -> Dict[str, int]:
        """Analyze language distribution in videos."""
        languages = [v.default_language for v in videos if v.default_language]
        return dict(Counter(languages))
    
    def _analyze_popular_categories(self, videos: List[VideoData]) -> Dict[str, int]:
        """Analyze popular categories in videos."""
        categories = [v.category_id for v in videos if v.category_id]
        return dict(Counter(categories))


# Global service instance
_analytics_service: Optional[AnalyticsService] = None

def get_analytics_service() -> AnalyticsService:
    """Get the global analytics service instance."""
    global _analytics_service
    
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    
    return _analytics_service
