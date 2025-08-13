"""Custom exceptions for YouTube API integration."""

from typing import Optional, Dict, Any
import json


class YouTubeAPIError(Exception):
    """Base exception for YouTube API related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        """Initialize YouTube API error.
        
        Args:
            message: Error message
            status_code: HTTP status code if available
            response_data: Raw response data from API
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.status_code:
            return f"YouTube API Error ({self.status_code}): {self.message}"
        return f"YouTube API Error: {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'status_code': self.status_code,
            'response_data': self.response_data
        }


class QuotaExceededError(YouTubeAPIError):
    """Raised when YouTube API quota is exceeded."""
    
    def __init__(self, message: str = "YouTube API quota exceeded", 
                 daily_limit_exceeded: bool = False,
                 quota_cost: Optional[int] = None,
                 remaining_quota: Optional[int] = None):
        """Initialize quota exceeded error.
        
        Args:
            message: Error message
            daily_limit_exceeded: Whether daily limit was exceeded
            quota_cost: Cost of the failed request
            remaining_quota: Remaining quota before the request
        """
        super().__init__(message, status_code=403)
        self.daily_limit_exceeded = daily_limit_exceeded
        self.quota_cost = quota_cost
        self.remaining_quota = remaining_quota
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data.update({
            'daily_limit_exceeded': self.daily_limit_exceeded,
            'quota_cost': self.quota_cost,
            'remaining_quota': self.remaining_quota
        })
        return data


class AuthenticationError(YouTubeAPIError):
    """Raised when YouTube API authentication fails."""
    
    def __init__(self, message: str = "YouTube API authentication failed", 
                 api_key: Optional[str] = None):
        """Initialize authentication error.
        
        Args:
            message: Error message
            api_key: Masked API key that failed (for logging)
        """
        super().__init__(message, status_code=401)
        self.api_key = api_key
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        if self.api_key:
            # Mask API key for security
            masked_key = f"{self.api_key[:8]}...{self.api_key[-4:]}" if len(self.api_key) > 12 else "***"
            data['api_key'] = masked_key
        return data


class RateLimitError(YouTubeAPIError):
    """Raised when YouTube API rate limit is hit."""
    
    def __init__(self, message: str = "YouTube API rate limit exceeded", 
                 retry_after: Optional[int] = None):
        """Initialize rate limit error.
        
        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
        """
        super().__init__(message, status_code=429)
        self.retry_after = retry_after
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data['retry_after'] = self.retry_after
        return data


class VideoNotFoundError(YouTubeAPIError):
    """Raised when a requested video is not found or not accessible."""
    
    def __init__(self, video_id: str, message: Optional[str] = None):
        """Initialize video not found error.
        
        Args:
            video_id: YouTube video ID that was not found
            message: Custom error message
        """
        if message is None:
            message = f"Video not found or not accessible: {video_id}"
        super().__init__(message, status_code=404)
        self.video_id = video_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data['video_id'] = self.video_id
        return data


class ChannelNotFoundError(YouTubeAPIError):
    """Raised when a requested channel is not found or not accessible."""
    
    def __init__(self, channel_id: str, message: Optional[str] = None):
        """Initialize channel not found error.
        
        Args:
            channel_id: YouTube channel ID that was not found
            message: Custom error message
        """
        if message is None:
            message = f"Channel not found or not accessible: {channel_id}"
        super().__init__(message, status_code=404)
        self.channel_id = channel_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data['channel_id'] = self.channel_id
        return data


class InvalidRequestError(YouTubeAPIError):
    """Raised when the API request is invalid."""
    
    def __init__(self, message: str, parameter: Optional[str] = None, 
                 parameter_value: Optional[str] = None):
        """Initialize invalid request error.
        
        Args:
            message: Error message
            parameter: Invalid parameter name
            parameter_value: Invalid parameter value
        """
        super().__init__(message, status_code=400)
        self.parameter = parameter
        self.parameter_value = parameter_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data.update({
            'parameter': self.parameter,
            'parameter_value': self.parameter_value
        })
        return data


class NetworkError(YouTubeAPIError):
    """Raised when network-related errors occur."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        """Initialize network error.
        
        Args:
            message: Error message
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.original_error = original_error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        if self.original_error:
            data['original_error'] = str(self.original_error)
            data['original_error_type'] = type(self.original_error).__name__
        return data


class DataValidationError(YouTubeAPIError):
    """Raised when API response data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 expected_type: Optional[str] = None, 
                 actual_value: Optional[Any] = None):
        """Initialize data validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            expected_type: Expected data type
            actual_value: Actual value that failed validation
        """
        super().__init__(message)
        self.field = field
        self.expected_type = expected_type
        self.actual_value = actual_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data.update({
            'field': self.field,
            'expected_type': self.expected_type,
            'actual_value': str(self.actual_value) if self.actual_value is not None else None
        })
        return data


class ServiceUnavailableError(YouTubeAPIError):
    """Raised when YouTube API service is temporarily unavailable."""
    
    def __init__(self, message: str = "YouTube API service temporarily unavailable", 
                 retry_after: Optional[int] = None):
        """Initialize service unavailable error.
        
        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
        """
        super().__init__(message, status_code=503)
        self.retry_after = retry_after
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging."""
        data = super().to_dict()
        data['retry_after'] = self.retry_after
        return data


def parse_youtube_api_error(response_data: Dict[str, Any], 
                           status_code: Optional[int] = None) -> YouTubeAPIError:
    """Parse YouTube API error response and return appropriate exception.
    
    Args:
        response_data: Raw error response from YouTube API
        status_code: HTTP status code
        
    Returns:
        Appropriate YouTubeAPIError subclass instance
    """
    # Extract error information from response
    error_info = response_data.get('error', {})
    message = error_info.get('message', 'Unknown YouTube API error')
    code = error_info.get('code', status_code)
    
    # Get detailed error information
    errors = error_info.get('errors', [])
    reason = None
    domain = None
    
    if errors:
        first_error = errors[0]
        reason = first_error.get('reason')
        domain = first_error.get('domain')
    
    # Map to specific exception types based on reason or status code
    if reason == 'quotaExceeded' or code == 403:
        daily_limit = reason == 'dailyLimitExceeded'
        return QuotaExceededError(
            message=message,
            daily_limit_exceeded=daily_limit
        )
    
    elif reason == 'keyInvalid' or code == 401:
        return AuthenticationError(message=message)
    
    elif reason == 'rateLimitExceeded' or code == 429:
        return RateLimitError(message=message)
    
    elif reason == 'videoNotFound' or (code == 404 and 'video' in message.lower()):
        # Try to extract video ID from message
        video_id = "unknown"
        return VideoNotFoundError(video_id=video_id, message=message)
    
    elif reason == 'channelNotFound' or (code == 404 and 'channel' in message.lower()):
        # Try to extract channel ID from message
        channel_id = "unknown"
        return ChannelNotFoundError(channel_id=channel_id, message=message)
    
    elif code == 400:
        return InvalidRequestError(message=message)
    
    elif code == 503:
        return ServiceUnavailableError(message=message)
    
    else:
        # Generic YouTube API error
        return YouTubeAPIError(
            message=message,
            status_code=code,
            response_data=response_data
        )


def is_retryable_error(error: Exception) -> bool:
    """Check if an error is retryable.
    
    Args:
        error: Exception to check
        
    Returns:
        True if the error is retryable
    """
    if isinstance(error, (RateLimitError, ServiceUnavailableError, NetworkError)):
        return True
    
    if isinstance(error, YouTubeAPIError):
        # Retry on server errors (5xx)
        if error.status_code and 500 <= error.status_code < 600:
            return True
    
    return False


def get_retry_delay(error: Exception, attempt: int = 1) -> int:
    """Get the recommended retry delay for an error.
    
    Args:
        error: Exception that occurred
        attempt: Current retry attempt number
        
    Returns:
        Delay in seconds before retrying
    """
    if isinstance(error, (RateLimitError, ServiceUnavailableError)):
        if error.retry_after:
            return error.retry_after
    
    # Exponential backoff: 2^attempt seconds, max 300 seconds (5 minutes)
    delay = min(2 ** attempt, 300)
    return delay
