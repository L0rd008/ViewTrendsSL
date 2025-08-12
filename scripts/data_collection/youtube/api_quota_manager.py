#!/usr/bin/env python3
"""
YouTube API Quota Manager

This module manages YouTube Data API quota usage to prevent exceeding daily limits.
It tracks quota consumption and provides intelligent quota management.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading

logger = logging.getLogger(__name__)


class QuotaManager:
    """Manages YouTube Data API quota usage and limits."""
    
    # YouTube Data API v3 quota costs
    QUOTA_COSTS = {
        'search': 100,
        'videos': 1,
        'channels': 1,
        'playlistItems': 1,
        'playlists': 1,
        'commentThreads': 1,
        'comments': 1
    }
    
    def __init__(self, daily_quota: int = 10000, quota_file: str = 'data/quota_usage.json'):
        """
        Initialize the quota manager.
        
        Args:
            daily_quota: Daily quota limit (default: 10,000 units)
            quota_file: File to store quota usage data
        """
        self.daily_quota = daily_quota
        self.quota_file = quota_file
        self.lock = threading.Lock()
        
        # Load existing quota data
        self.quota_data = self._load_quota_data()
        
        # Clean old data
        self._cleanup_old_data()
    
    def _load_quota_data(self) -> Dict[str, Any]:
        """
        Load quota usage data from file.
        
        Returns:
            Dictionary containing quota usage data
        """
        if os.path.exists(self.quota_file):
            try:
                with open(self.quota_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load quota data: {e}")
        
        return {
            'daily_usage': {},
            'hourly_usage': {},
            'last_reset': datetime.now().isoformat()
        }
    
    def _save_quota_data(self):
        """Save quota usage data to file."""
        try:
            os.makedirs(os.path.dirname(self.quota_file), exist_ok=True)
            with open(self.quota_file, 'w') as f:
                json.dump(self.quota_data, f, indent=2)
        except IOError as e:
            logger.error(f"Could not save quota data: {e}")
    
    def _cleanup_old_data(self):
        """Remove quota data older than 7 days."""
        cutoff_date = datetime.now() - timedelta(days=7)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        # Clean daily usage
        daily_usage = self.quota_data.get('daily_usage', {})
        old_dates = [date for date in daily_usage.keys() if date < cutoff_str]
        for date in old_dates:
            del daily_usage[date]
        
        # Clean hourly usage
        hourly_usage = self.quota_data.get('hourly_usage', {})
        cutoff_hour = cutoff_date.strftime('%Y-%m-%d-%H')
        old_hours = [hour for hour in hourly_usage.keys() if hour < cutoff_hour]
        for hour in old_hours:
            del hourly_usage[hour]
        
        self._save_quota_data()
    
    def get_current_usage(self) -> Dict[str, int]:
        """
        Get current quota usage for today.
        
        Returns:
            Dictionary with usage statistics
        """
        today = datetime.now().strftime('%Y-%m-%d')
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        
        daily_usage = self.quota_data.get('daily_usage', {}).get(today, 0)
        hourly_usage = self.quota_data.get('hourly_usage', {}).get(current_hour, 0)
        
        return {
            'daily_used': daily_usage,
            'daily_remaining': max(0, self.daily_quota - daily_usage),
            'hourly_used': hourly_usage,
            'daily_limit': self.daily_quota
        }
    
    def can_make_request(self, quota_cost: int) -> bool:
        """
        Check if a request can be made without exceeding quota.
        
        Args:
            quota_cost: Quota cost of the request
            
        Returns:
            True if request can be made, False otherwise
        """
        with self.lock:
            usage = self.get_current_usage()
            return usage['daily_remaining'] >= quota_cost
    
    def record_request(self, quota_cost: int, endpoint: str = 'unknown'):
        """
        Record a quota usage for a request.
        
        Args:
            quota_cost: Quota cost of the request
            endpoint: API endpoint used
        """
        with self.lock:
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            current_hour = now.strftime('%Y-%m-%d-%H')
            
            # Update daily usage
            daily_usage = self.quota_data.setdefault('daily_usage', {})
            daily_usage[today] = daily_usage.get(today, 0) + quota_cost
            
            # Update hourly usage
            hourly_usage = self.quota_data.setdefault('hourly_usage', {})
            hourly_usage[current_hour] = hourly_usage.get(current_hour, 0) + quota_cost
            
            # Record endpoint usage
            endpoint_usage = self.quota_data.setdefault('endpoint_usage', {})
            endpoint_daily = endpoint_usage.setdefault(today, {})
            endpoint_daily[endpoint] = endpoint_daily.get(endpoint, 0) + quota_cost
            
            # Save data
            self._save_quota_data()
            
            logger.debug(f"Recorded {quota_cost} quota units for {endpoint}")
    
    def get_quota_cost(self, endpoint: str) -> int:
        """
        Get the quota cost for a specific endpoint.
        
        Args:
            endpoint: API endpoint name
            
        Returns:
            Quota cost in units
        """
        return self.QUOTA_COSTS.get(endpoint, 1)
    
    def estimate_requests_remaining(self, endpoint: str) -> int:
        """
        Estimate how many requests can still be made for an endpoint.
        
        Args:
            endpoint: API endpoint name
            
        Returns:
            Estimated number of requests remaining
        """
        usage = self.get_current_usage()
        quota_cost = self.get_quota_cost(endpoint)
        
        if quota_cost == 0:
            return float('inf')
        
        return usage['daily_remaining'] // quota_cost
    
    def get_usage_report(self) -> Dict[str, Any]:
        """
        Generate a detailed usage report.
        
        Returns:
            Dictionary containing usage statistics
        """
        today = datetime.now().strftime('%Y-%m-%d')
        usage = self.get_current_usage()
        
        # Get endpoint breakdown for today
        endpoint_usage = self.quota_data.get('endpoint_usage', {}).get(today, {})
        
        # Get hourly usage for today
        hourly_pattern = {}
        for hour_key, usage_val in self.quota_data.get('hourly_usage', {}).items():
            if hour_key.startswith(today):
                hour = hour_key.split('-')[-1]
                hourly_pattern[hour] = usage_val
        
        return {
            'current_usage': usage,
            'endpoint_breakdown': endpoint_usage,
            'hourly_pattern': hourly_pattern,
            'efficiency_score': self._calculate_efficiency_score()
        }
    
    def _calculate_efficiency_score(self) -> float:
        """
        Calculate quota efficiency score (0-100).
        
        Returns:
            Efficiency score as percentage
        """
        usage = self.get_current_usage()
        
        if usage['daily_limit'] == 0:
            return 0.0
        
        usage_ratio = usage['daily_used'] / usage['daily_limit']
        
        # Efficiency is higher when quota is used more evenly throughout the day
        # and when high-value endpoints are prioritized
        
        # Simple efficiency calculation - can be improved
        if usage_ratio < 0.1:
            return 20.0  # Very low usage
        elif usage_ratio < 0.5:
            return 60.0  # Moderate usage
        elif usage_ratio < 0.8:
            return 85.0  # Good usage
        elif usage_ratio < 0.95:
            return 95.0  # Excellent usage
        else:
            return 100.0  # Maximum usage
    
    def reset_daily_quota(self):
        """Reset daily quota usage (for testing purposes)."""
        with self.lock:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Clear today's usage
            if 'daily_usage' in self.quota_data:
                self.quota_data['daily_usage'].pop(today, None)
            
            if 'endpoint_usage' in self.quota_data:
                self.quota_data['endpoint_usage'].pop(today, None)
            
            # Clear today's hourly usage
            if 'hourly_usage' in self.quota_data:
                today_hours = [k for k in self.quota_data['hourly_usage'].keys() 
                              if k.startswith(today)]
                for hour in today_hours:
                    del self.quota_data['hourly_usage'][hour]
            
            self._save_quota_data()
            logger.info("Daily quota usage reset")
    
    def get_quota_status(self) -> str:
        """
        Get a human-readable quota status.
        
        Returns:
            Status string
        """
        usage = self.get_current_usage()
        percentage = (usage['daily_used'] / usage['daily_limit']) * 100
        
        if percentage < 25:
            return f"Low usage: {percentage:.1f}% ({usage['daily_used']}/{usage['daily_limit']})"
        elif percentage < 50:
            return f"Moderate usage: {percentage:.1f}% ({usage['daily_used']}/{usage['daily_limit']})"
        elif percentage < 75:
            return f"High usage: {percentage:.1f}% ({usage['daily_used']}/{usage['daily_limit']})"
        elif percentage < 90:
            return f"Very high usage: {percentage:.1f}% ({usage['daily_used']}/{usage['daily_limit']})"
        else:
            return f"Critical usage: {percentage:.1f}% ({usage['daily_used']}/{usage['daily_limit']})"


def main():
    """Main function for testing quota manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube API Quota Manager')
    parser.add_argument('--status', action='store_true', help='Show quota status')
    parser.add_argument('--report', action='store_true', help='Show detailed usage report')
    parser.add_argument('--reset', action='store_true', help='Reset daily quota (for testing)')
    
    args = parser.parse_args()
    
    quota_manager = QuotaManager()
    
    if args.status:
        print(quota_manager.get_quota_status())
    
    if args.report:
        report = quota_manager.get_usage_report()
        print(json.dumps(report, indent=2))
    
    if args.reset:
        quota_manager.reset_daily_quota()
        print("Daily quota usage has been reset")


if __name__ == '__main__':
    main()
