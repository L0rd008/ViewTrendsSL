"""
Data Validation Utilities

This module provides utility functions for validating various types of data
including user input, video metadata, and API responses.

Author: ViewTrendsSL Team
Date: 2025
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse
import validators

logger = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(email_pattern, email.strip()))


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        True if valid password, False otherwise
    """
    if not password or not isinstance(password, str):
        return False
    
    # Check minimum length
    if len(password) < 8:
        return False
    
    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check for digit
    if not re.search(r'\d', password):
        return False
    
    # Check for special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True


def validate_youtube_url(url: str) -> Dict[str, Any]:
    """
    Validate and extract information from YouTube URL.
    
    Args:
        url: YouTube URL to validate
        
    Returns:
        Dictionary containing validation result and extracted info
    """
    result = {
        'is_valid': False,
        'video_id': None,
        'url_type': None,
        'error': None
    }
    
    if not url or not isinstance(url, str):
        result['error'] = 'URL is required'
        return result
    
    try:
        # Clean the URL
        url = url.strip()
        
        # Parse URL
        parsed = urlparse(url)
        
        # Check if it's a YouTube domain
        if parsed.netloc not in ['www.youtube.com', 'youtube.com', 'youtu.be', 'm.youtube.com']:
            result['error'] = 'Not a valid YouTube URL'
            return result
        
        video_id = None
        
        # Extract video ID based on URL format
        if parsed.netloc == 'youtu.be':
            # Short URL format: https://youtu.be/VIDEO_ID
            video_id = parsed.path[1:]  # Remove leading slash
            result['url_type'] = 'short'
        elif 'watch' in parsed.path:
            # Standard URL format: https://www.youtube.com/watch?v=VIDEO_ID
            from urllib.parse import parse_qs
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                video_id = query_params['v'][0]
                result['url_type'] = 'standard'
        elif '/embed/' in parsed.path:
            # Embed URL format: https://www.youtube.com/embed/VIDEO_ID
            video_id = parsed.path.split('/embed/')[-1].split('?')[0]
            result['url_type'] = 'embed'
        
        if video_id and len(video_id) == 11:  # YouTube video IDs are 11 characters
            result['is_valid'] = True
            result['video_id'] = video_id
        else:
            result['error'] = 'Could not extract valid video ID'
        
    except Exception as e:
        result['error'] = f'URL parsing error: {str(e)}'
    
    return result


def validate_video_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate video metadata structure and content.
    
    Args:
        metadata: Video metadata dictionary
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    required_fields = ['title', 'duration_seconds', 'published_at']
    
    # Check required fields
    for field in required_fields:
        if field not in metadata or metadata[field] is None:
            result['errors'].append(f'Missing required field: {field}')
            result['is_valid'] = False
    
    # Validate specific fields
    if 'title' in metadata:
        title = metadata['title']
        if not isinstance(title, str) or len(title.strip()) == 0:
            result['errors'].append('Title must be a non-empty string')
            result['is_valid'] = False
        elif len(title) > 200:
            result['warnings'].append('Title is very long (>200 characters)')
    
    if 'duration_seconds' in metadata:
        duration = metadata['duration_seconds']
        if not isinstance(duration, (int, float)) or duration <= 0:
            result['errors'].append('Duration must be a positive number')
            result['is_valid'] = False
        elif duration > 43200:  # 12 hours
            result['warnings'].append('Video duration is very long (>12 hours)')
    
    if 'category_id' in metadata:
        category_id = metadata['category_id']
        if not isinstance(category_id, int) or category_id < 1:
            result['errors'].append('Category ID must be a positive integer')
            result['is_valid'] = False
    
    if 'view_count' in metadata:
        view_count = metadata['view_count']
        if not isinstance(view_count, int) or view_count < 0:
            result['errors'].append('View count must be a non-negative integer')
            result['is_valid'] = False
    
    return result


def validate_prediction_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate prediction request data.
    
    Args:
        request_data: Prediction request data
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check if video_url or video_metadata is provided
    if 'video_url' not in request_data and 'video_metadata' not in request_data:
        result['errors'].append('Either video_url or video_metadata is required')
        result['is_valid'] = False
        return result
    
    # Validate video URL if provided
    if 'video_url' in request_data:
        url_validation = validate_youtube_url(request_data['video_url'])
        if not url_validation['is_valid']:
            result['errors'].append(f"Invalid video URL: {url_validation['error']}")
            result['is_valid'] = False
    
    # Validate video metadata if provided
    if 'video_metadata' in request_data:
        metadata_validation = validate_video_metadata(request_data['video_metadata'])
        if not metadata_validation['is_valid']:
            result['errors'].extend(metadata_validation['errors'])
            result['is_valid'] = False
        result['warnings'].extend(metadata_validation['warnings'])
    
    # Validate timeframe if provided
    if 'timeframe' in request_data:
        timeframe = request_data['timeframe']
        if not isinstance(timeframe, int) or timeframe < 1 or timeframe > 365:
            result['errors'].append('Timeframe must be between 1 and 365 days')
            result['is_valid'] = False
    
    return result


def validate_user_registration(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate user registration data.
    
    Args:
        user_data: User registration data
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    required_fields = ['email', 'password', 'full_name']
    
    # Check required fields
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            result['errors'].append(f'Missing required field: {field}')
            result['is_valid'] = False
    
    # Validate email
    if 'email' in user_data:
        if not validate_email(user_data['email']):
            result['errors'].append('Invalid email address format')
            result['is_valid'] = False
    
    # Validate password
    if 'password' in user_data:
        if not validate_password(user_data['password']):
            result['errors'].append(
                'Password must be at least 8 characters long and contain uppercase, '
                'lowercase, digit, and special character'
            )
            result['is_valid'] = False
    
    # Validate full name
    if 'full_name' in user_data:
        full_name = user_data['full_name']
        if not isinstance(full_name, str) or len(full_name.strip()) < 2:
            result['errors'].append('Full name must be at least 2 characters long')
            result['is_valid'] = False
        elif len(full_name) > 100:
            result['warnings'].append('Full name is very long (>100 characters)')
    
    return result


def validate_channel_data(channel_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate channel data structure and content.
    
    Args:
        channel_data: Channel data dictionary
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    required_fields = ['channel_id', 'channel_title']
    
    # Check required fields
    for field in required_fields:
        if field not in channel_data or not channel_data[field]:
            result['errors'].append(f'Missing required field: {field}')
            result['is_valid'] = False
    
    # Validate channel ID format
    if 'channel_id' in channel_data:
        channel_id = channel_data['channel_id']
        if not isinstance(channel_id, str) or len(channel_id) != 24:
            result['errors'].append('Channel ID must be a 24-character string')
            result['is_valid'] = False
    
    # Validate subscriber count
    if 'subscriber_count' in channel_data:
        subscriber_count = channel_data['subscriber_count']
        if not isinstance(subscriber_count, int) or subscriber_count < 0:
            result['errors'].append('Subscriber count must be a non-negative integer')
            result['is_valid'] = False
    
    return result


def validate_numeric_range(value: Any, min_val: float, max_val: float, field_name: str) -> Optional[str]:
    """
    Validate that a numeric value is within a specified range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field for error messages
        
    Returns:
        Error message if invalid, None if valid
    """
    if not isinstance(value, (int, float)):
        return f'{field_name} must be a number'
    
    if value < min_val or value > max_val:
        return f'{field_name} must be between {min_val} and {max_val}'
    
    return None


def validate_string_length(value: Any, min_len: int, max_len: int, field_name: str) -> Optional[str]:
    """
    Validate string length.
    
    Args:
        value: Value to validate
        min_len: Minimum length
        max_len: Maximum length
        field_name: Name of the field for error messages
        
    Returns:
        Error message if invalid, None if valid
    """
    if not isinstance(value, str):
        return f'{field_name} must be a string'
    
    if len(value) < min_len or len(value) > max_len:
        return f'{field_name} must be between {min_len} and {max_len} characters'
    
    return None


def validate_list_items(items: List[Any], item_validator: callable, field_name: str) -> List[str]:
    """
    Validate items in a list using a validator function.
    
    Args:
        items: List of items to validate
        item_validator: Function to validate each item
        field_name: Name of the field for error messages
        
    Returns:
        List of error messages
    """
    errors = []
    
    if not isinstance(items, list):
        errors.append(f'{field_name} must be a list')
        return errors
    
    for i, item in enumerate(items):
        try:
            if not item_validator(item):
                errors.append(f'{field_name}[{i}] is invalid')
        except Exception as e:
            errors.append(f'{field_name}[{i}] validation error: {str(e)}')
    
    return errors


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by removing dangerous characters and trimming.
    
    Args:
        value: String to sanitize
        max_length: Maximum length to truncate to
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return str(value)
    
    # Remove null bytes and control characters
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Truncate if necessary
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_api_response(response_data: Dict[str, Any], expected_fields: List[str]) -> Dict[str, Any]:
    """
    Validate API response structure.
    
    Args:
        response_data: API response data
        expected_fields: List of expected fields
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': [],
        'missing_fields': []
    }
    
    if not isinstance(response_data, dict):
        result['errors'].append('Response data must be a dictionary')
        result['is_valid'] = False
        return result
    
    # Check for expected fields
    for field in expected_fields:
        if field not in response_data:
            result['missing_fields'].append(field)
            result['is_valid'] = False
    
    if result['missing_fields']:
        result['errors'].append(f"Missing required fields: {', '.join(result['missing_fields'])}")
    
    return result


def validate_pagination_params(page: Any, per_page: Any) -> Dict[str, Any]:
    """
    Validate pagination parameters.
    
    Args:
        page: Page number
        per_page: Items per page
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': []
    }
    
    # Validate page number
    if not isinstance(page, int) or page < 1:
        result['errors'].append('Page must be a positive integer')
        result['is_valid'] = False
    
    # Validate per_page
    if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
        result['errors'].append('Per page must be between 1 and 100')
        result['is_valid'] = False
    
    return result


def is_safe_filename(filename: str) -> bool:
    """
    Check if filename is safe (no path traversal, etc.).
    
    Args:
        filename: Filename to check
        
    Returns:
        True if safe, False otherwise
    """
    if not filename or not isinstance(filename, str):
        return False
    
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Check for dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\0']
    if any(char in filename for char in dangerous_chars):
        return False
    
    # Check length
    if len(filename) > 255:
        return False
    
    return True


def validate_json_structure(data: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate JSON data against a simple schema.
    
    Args:
        data: Data to validate
        schema: Schema definition
        
    Returns:
        Dictionary containing validation result and errors
    """
    result = {
        'is_valid': True,
        'errors': []
    }
    
    def validate_field(value, field_schema, field_path):
        field_type = field_schema.get('type')
        required = field_schema.get('required', False)
        
        if value is None:
            if required:
                result['errors'].append(f'{field_path} is required')
                result['is_valid'] = False
            return
        
        if field_type == 'string' and not isinstance(value, str):
            result['errors'].append(f'{field_path} must be a string')
            result['is_valid'] = False
        elif field_type == 'integer' and not isinstance(value, int):
            result['errors'].append(f'{field_path} must be an integer')
            result['is_valid'] = False
        elif field_type == 'number' and not isinstance(value, (int, float)):
            result['errors'].append(f'{field_path} must be a number')
            result['is_valid'] = False
        elif field_type == 'boolean' and not isinstance(value, bool):
            result['errors'].append(f'{field_path} must be a boolean')
            result['is_valid'] = False
        elif field_type == 'array' and not isinstance(value, list):
            result['errors'].append(f'{field_path} must be an array')
            result['is_valid'] = False
        elif field_type == 'object' and not isinstance(value, dict):
            result['errors'].append(f'{field_path} must be an object')
            result['is_valid'] = False
    
    # Validate each field in schema
    for field_name, field_schema in schema.items():
        field_value = data.get(field_name) if isinstance(data, dict) else None
        validate_field(field_value, field_schema, field_name)
    
    return result
