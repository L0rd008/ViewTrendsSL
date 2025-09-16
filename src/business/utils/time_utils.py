"""
Time Utilities

This module provides utility functions for time-related operations,
including date parsing, timezone handling, and time period calculations.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional, Dict, Any
import pytz
from dateutil import parser

logger = logging.getLogger(__name__)

# Sri Lanka timezone
SL_TIMEZONE = pytz.timezone('Asia/Colombo')


def get_current_time_sl() -> datetime:
    """
    Get current time in Sri Lanka timezone.
    
    Returns:
        Current datetime in Sri Lanka timezone
    """
    return datetime.now(SL_TIMEZONE)


def get_current_utc_time() -> datetime:
    """
    Get current time in UTC timezone.
    
    Returns:
        Current datetime in UTC timezone
    """
    return datetime.now(timezone.utc)


def convert_to_sl_time(dt: datetime) -> datetime:
    """
    Convert datetime to Sri Lanka timezone.
    
    Args:
        dt: Datetime to convert
        
    Returns:
        Datetime in Sri Lanka timezone
    """
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.astimezone(SL_TIMEZONE)


def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Parse datetime string to datetime object.
    
    Args:
        date_string: Date string to parse
        
    Returns:
        Parsed datetime or None if parsing fails
    """
    try:
        return parser.parse(date_string)
    except Exception as e:
        logger.error(f"Failed to parse datetime string '{date_string}': {str(e)}")
        return None


def get_time_periods(period: str) -> Tuple[datetime, datetime]:
    """
    Get start and end dates for a time period.
    
    Args:
        period: Time period ('day', 'week', 'month', 'quarter', 'year')
        
    Returns:
        Tuple of (start_date, end_date)
    """
    now = get_current_time_sl()
    
    if period == 'day':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif period == 'week':
        days_since_monday = now.weekday()
        start_date = (now - timedelta(days=days_since_monday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_date = start_date + timedelta(days=7)
    elif period == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            end_date = start_date.replace(year=now.year + 1, month=1)
        else:
            end_date = start_date.replace(month=now.month + 1)
    elif period == 'quarter':
        quarter_start_month = ((now.month - 1) // 3) * 3 + 1
        start_date = now.replace(
            month=quarter_start_month, day=1, 
            hour=0, minute=0, second=0, microsecond=0
        )
        if quarter_start_month == 10:
            end_date = start_date.replace(year=now.year + 1, month=1)
        else:
            end_date = start_date.replace(month=quarter_start_month + 3)
    elif period == 'year':
        start_date = now.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end_date = start_date.replace(year=now.year + 1)
    else:
        # Default to last 7 days
        end_date = now
        start_date = now - timedelta(days=7)
    
    return start_date, end_date


def format_time_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format time range as human-readable string.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Formatted time range string
    """
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    return f"{start_str} to {end_str}"


def get_optimal_posting_times() -> Dict[str, Any]:
    """
    Get optimal posting times for Sri Lankan audience.
    
    Returns:
        Dictionary containing optimal posting times
    """
    return {
        'weekdays': {
            'morning': [8, 9, 10],  # 8-10 AM
            'afternoon': [13, 14, 15],  # 1-3 PM
            'evening': [18, 19, 20, 21]  # 6-9 PM
        },
        'weekends': {
            'morning': [9, 10, 11],  # 9-11 AM
            'afternoon': [14, 15, 16],  # 2-4 PM
            'evening': [19, 20, 21, 22]  # 7-10 PM
        },
        'timezone': 'Asia/Colombo'
    }


def is_optimal_posting_time(dt: datetime) -> bool:
    """
    Check if datetime is an optimal posting time.
    
    Args:
        dt: Datetime to check
        
    Returns:
        True if optimal posting time, False otherwise
    """
    sl_time = convert_to_sl_time(dt)
    hour = sl_time.hour
    is_weekend = sl_time.weekday() >= 5
    
    optimal_times = get_optimal_posting_times()
    
    if is_weekend:
        all_optimal_hours = (
            optimal_times['weekends']['morning'] +
            optimal_times['weekends']['afternoon'] +
            optimal_times['weekends']['evening']
        )
    else:
        all_optimal_hours = (
            optimal_times['weekdays']['morning'] +
            optimal_times['weekdays']['afternoon'] +
            optimal_times['weekdays']['evening']
        )
    
    return hour in all_optimal_hours


def get_time_since_upload(upload_time: datetime) -> Dict[str, Any]:
    """
    Calculate time since video upload.
    
    Args:
        upload_time: Video upload datetime
        
    Returns:
        Dictionary containing time since upload information
    """
    now = get_current_time_sl()
    upload_time_sl = convert_to_sl_time(upload_time)
    
    time_diff = now - upload_time_sl
    
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    return {
        'total_seconds': int(time_diff.total_seconds()),
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'human_readable': format_time_since(time_diff)
    }


def format_time_since(time_diff: timedelta) -> str:
    """
    Format timedelta as human-readable string.
    
    Args:
        time_diff: Time difference
        
    Returns:
        Human-readable time difference string
    """
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    if days > 0:
        if days == 1:
            return "1 day ago"
        else:
            return f"{days} days ago"
    elif hours > 0:
        if hours == 1:
            return "1 hour ago"
        else:
            return f"{hours} hours ago"
    elif minutes > 0:
        if minutes == 1:
            return "1 minute ago"
        else:
            return f"{minutes} minutes ago"
    else:
        return "Just now"


def get_video_age_category(upload_time: datetime) -> str:
    """
    Categorize video by age.
    
    Args:
        upload_time: Video upload datetime
        
    Returns:
        Age category string
    """
    time_info = get_time_since_upload(upload_time)
    days = time_info['days']
    
    if days == 0:
        return 'new'  # Less than 1 day
    elif days <= 7:
        return 'recent'  # 1-7 days
    elif days <= 30:
        return 'month_old'  # 1-30 days
    elif days <= 90:
        return 'quarter_old'  # 1-3 months
    elif days <= 365:
        return 'year_old'  # 3-12 months
    else:
        return 'old'  # More than 1 year


def get_peak_viewing_hours() -> Dict[str, list]:
    """
    Get peak viewing hours for Sri Lankan audience.
    
    Returns:
        Dictionary containing peak viewing hours
    """
    return {
        'weekdays': [19, 20, 21, 22],  # 7-10 PM
        'weekends': [14, 15, 16, 19, 20, 21, 22],  # 2-4 PM and 7-10 PM
        'timezone': 'Asia/Colombo'
    }


def calculate_time_to_peak_hours(current_time: datetime) -> Dict[str, Any]:
    """
    Calculate time until next peak viewing hours.
    
    Args:
        current_time: Current datetime
        
    Returns:
        Dictionary containing time to peak hours information
    """
    sl_time = convert_to_sl_time(current_time)
    is_weekend = sl_time.weekday() >= 5
    
    peak_hours = get_peak_viewing_hours()
    target_hours = peak_hours['weekends'] if is_weekend else peak_hours['weekdays']
    
    current_hour = sl_time.hour
    
    # Find next peak hour
    next_peak_hour = None
    for hour in target_hours:
        if hour > current_hour:
            next_peak_hour = hour
            break
    
    if next_peak_hour is None:
        # Next peak hour is tomorrow
        next_peak_hour = target_hours[0]
        next_peak_time = sl_time.replace(
            hour=next_peak_hour, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
    else:
        next_peak_time = sl_time.replace(
            hour=next_peak_hour, minute=0, second=0, microsecond=0
        )
    
    time_diff = next_peak_time - sl_time
    
    return {
        'next_peak_hour': next_peak_hour,
        'next_peak_time': next_peak_time.isoformat(),
        'hours_until_peak': time_diff.total_seconds() / 3600,
        'is_currently_peak': current_hour in target_hours
    }


def get_day_type(dt: datetime) -> str:
    """
    Get day type (weekday/weekend).
    
    Args:
        dt: Datetime to check
        
    Returns:
        Day type string
    """
    sl_time = convert_to_sl_time(dt)
    return 'weekend' if sl_time.weekday() >= 5 else 'weekday'


def get_time_features(dt: datetime) -> Dict[str, Any]:
    """
    Extract time-based features from datetime.
    
    Args:
        dt: Datetime to extract features from
        
    Returns:
        Dictionary containing time features
    """
    sl_time = convert_to_sl_time(dt)
    
    return {
        'hour': sl_time.hour,
        'day_of_week': sl_time.weekday(),
        'day_of_month': sl_time.day,
        'month': sl_time.month,
        'quarter': (sl_time.month - 1) // 3 + 1,
        'year': sl_time.year,
        'is_weekend': sl_time.weekday() >= 5,
        'is_optimal_posting_time': is_optimal_posting_time(dt),
        'day_type': get_day_type(dt),
        'time_period': get_time_period_of_day(sl_time.hour)
    }


def get_time_period_of_day(hour: int) -> str:
    """
    Get time period of day based on hour.
    
    Args:
        hour: Hour (0-23)
        
    Returns:
        Time period string
    """
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}m"
        else:
            return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        if remaining_minutes == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {remaining_minutes}m"


def parse_iso_duration(iso_duration: str) -> int:
    """
    Parse ISO 8601 duration string to seconds.
    
    Args:
        iso_duration: ISO 8601 duration string (e.g., 'PT1M30S')
        
    Returns:
        Duration in seconds
    """
    try:
        # Remove 'PT' prefix
        duration_str = iso_duration[2:] if iso_duration.startswith('PT') else iso_duration
        
        total_seconds = 0
        current_number = ''
        
        for char in duration_str:
            if char.isdigit():
                current_number += char
            elif char in ['H', 'M', 'S']:
                if current_number:
                    value = int(current_number)
                    if char == 'H':
                        total_seconds += value * 3600
                    elif char == 'M':
                        total_seconds += value * 60
                    elif char == 'S':
                        total_seconds += value
                    current_number = ''
        
        return total_seconds
        
    except Exception as e:
        logger.error(f"Failed to parse ISO duration '{iso_duration}': {str(e)}")
        return 0
