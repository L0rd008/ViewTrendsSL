"""Enhanced quota management for YouTube API integration."""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class APIEndpoint(Enum):
    """YouTube API endpoints with their quota costs."""
    VIDEOS_LIST = ("videos", 1)
    CHANNELS_LIST = ("channels", 1)
    SEARCH_LIST = ("search", 100)
    PLAYLIST_ITEMS_LIST = ("playlistItems", 1)
    COMMENTS_LIST = ("comments", 1)
    COMMENT_THREADS_LIST = ("commentThreads", 1)
    
    def __init__(self, endpoint_name: str, quota_cost: int):
        self.endpoint_name = endpoint_name
        self.quota_cost = quota_cost


@dataclass
class APIKeyInfo:
    """Information about an API key."""
    key: str
    name: str
    daily_quota: int = 10000
    used_quota: int = 0
    last_reset: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    error_count: int = 0
    last_error: Optional[datetime] = None
    
    @property
    def remaining_quota(self) -> int:
        """Get remaining quota for this key."""
        return max(0, self.daily_quota - self.used_quota)
    
    @property
    def usage_percentage(self) -> float:
        """Get quota usage percentage."""
        return (self.used_quota / self.daily_quota) * 100 if self.daily_quota > 0 else 0
    
    @property
    def is_quota_available(self) -> bool:
        """Check if quota is available."""
        return self.is_active and self.remaining_quota > 0
    
    def reset_daily_quota(self) -> None:
        """Reset daily quota usage."""
        self.used_quota = 0
        self.last_reset = datetime.now(timezone.utc)
        self.error_count = 0
        self.last_error = None
        logger.info(f"Reset daily quota for API key: {self.name}")
    
    def add_usage(self, cost: int) -> None:
        """Add quota usage."""
        self.used_quota += cost
        logger.debug(f"Added {cost} quota usage to {self.name}. Total: {self.used_quota}")
    
    def record_error(self) -> None:
        """Record an API error for this key."""
        self.error_count += 1
        self.last_error = datetime.now(timezone.utc)
        
        # Temporarily disable key if too many errors
        if self.error_count >= 5:
            self.is_active = False
            logger.warning(f"Disabled API key {self.name} due to too many errors")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'daily_quota': self.daily_quota,
            'used_quota': self.used_quota,
            'last_reset': self.last_reset.isoformat(),
            'is_active': self.is_active,
            'error_count': self.error_count,
            'last_error': self.last_error.isoformat() if self.last_error else None
        }
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'APIKeyInfo':
        """Create from dictionary."""
        return cls(
            key=key,
            name=data['name'],
            daily_quota=data.get('daily_quota', 10000),
            used_quota=data.get('used_quota', 0),
            last_reset=datetime.fromisoformat(data.get('last_reset', datetime.now(timezone.utc).isoformat())),
            is_active=data.get('is_active', True),
            error_count=data.get('error_count', 0),
            last_error=datetime.fromisoformat(data['last_error']) if data.get('last_error') else None
        )


@dataclass
class QuotaUsageStats:
    """Statistics for quota usage."""
    total_requests: int = 0
    total_quota_used: int = 0
    requests_by_endpoint: Dict[str, int] = field(default_factory=dict)
    quota_by_endpoint: Dict[str, int] = field(default_factory=dict)
    errors_by_key: Dict[str, int] = field(default_factory=dict)
    
    def add_request(self, endpoint: APIEndpoint, key_name: str, success: bool = True) -> None:
        """Record a request."""
        self.total_requests += 1
        self.total_quota_used += endpoint.quota_cost
        
        endpoint_name = endpoint.endpoint_name
        self.requests_by_endpoint[endpoint_name] = self.requests_by_endpoint.get(endpoint_name, 0) + 1
        self.quota_by_endpoint[endpoint_name] = self.quota_by_endpoint.get(endpoint_name, 0) + endpoint.quota_cost
        
        if not success:
            self.errors_by_key[key_name] = self.errors_by_key.get(key_name, 0) + 1


class QuotaManager:
    """Enhanced quota manager for YouTube API keys."""
    
    def __init__(self, api_keys: Dict[str, str], storage_path: Optional[str] = None):
        """Initialize quota manager.
        
        Args:
            api_keys: Dictionary of {key_name: api_key}
            storage_path: Path to store quota usage data
        """
        self.api_keys: Dict[str, APIKeyInfo] = {}
        self.storage_path = Path(storage_path) if storage_path else Path("data/quota_usage.json")
        self.stats = QuotaUsageStats()
        self._lock = threading.Lock()
        
        # Initialize API keys
        for name, key in api_keys.items():
            self.api_keys[name] = APIKeyInfo(key=key, name=name)
        
        # Load existing usage data
        self._load_usage_data()
        
        # Check for quota resets
        self._check_quota_resets()
        
        logger.info(f"Initialized quota manager with {len(self.api_keys)} API keys")
    
    def get_best_key_for_request(self, endpoint: APIEndpoint, required_quota: Optional[int] = None) -> Optional[APIKeyInfo]:
        """Get the best API key for a request.
        
        Args:
            endpoint: API endpoint to call
            required_quota: Required quota (defaults to endpoint cost)
            
        Returns:
            Best API key info or None if no key available
        """
        if required_quota is None:
            required_quota = endpoint.quota_cost
        
        with self._lock:
            # Filter available keys
            available_keys = [
                key_info for key_info in self.api_keys.values()
                if key_info.is_quota_available and key_info.remaining_quota >= required_quota
            ]
            
            if not available_keys:
                logger.warning("No API keys with sufficient quota available")
                return None
            
            # Sort by remaining quota (descending) and error count (ascending)
            available_keys.sort(
                key=lambda k: (-k.remaining_quota, k.error_count)
            )
            
            best_key = available_keys[0]
            logger.debug(f"Selected API key: {best_key.name} (remaining: {best_key.remaining_quota})")
            return best_key
    
    def reserve_quota(self, key_info: APIKeyInfo, endpoint: APIEndpoint) -> bool:
        """Reserve quota for a request.
        
        Args:
            key_info: API key info
            endpoint: API endpoint
            
        Returns:
            True if quota reserved successfully
        """
        with self._lock:
            if key_info.remaining_quota >= endpoint.quota_cost:
                key_info.add_usage(endpoint.quota_cost)
                self.stats.add_request(endpoint, key_info.name, success=True)
                self._save_usage_data()
                return True
            return False
    
    def record_request_success(self, key_info: APIKeyInfo, endpoint: APIEndpoint) -> None:
        """Record a successful API request.
        
        Args:
            key_info: API key info
            endpoint: API endpoint
        """
        # Quota already reserved in reserve_quota
        logger.debug(f"Successful request to {endpoint.endpoint_name} using {key_info.name}")
    
    def record_request_error(self, key_info: APIKeyInfo, endpoint: APIEndpoint, error: Exception) -> None:
        """Record a failed API request.
        
        Args:
            key_info: API key info
            endpoint: API endpoint
            error: Exception that occurred
        """
        with self._lock:
            key_info.record_error()
            self.stats.add_request(endpoint, key_info.name, success=False)
            self._save_usage_data()
            
            logger.error(f"Request error for {endpoint.endpoint_name} using {key_info.name}: {error}")
    
    def get_quota_summary(self) -> Dict[str, Any]:
        """Get quota usage summary.
        
        Returns:
            Dictionary with quota usage information
        """
        with self._lock:
            total_quota = sum(key.daily_quota for key in self.api_keys.values())
            total_used = sum(key.used_quota for key in self.api_keys.values())
            total_remaining = sum(key.remaining_quota for key in self.api_keys.values())
            
            key_summaries = []
            for key_info in self.api_keys.values():
                key_summaries.append({
                    'name': key_info.name,
                    'quota_used': key_info.used_quota,
                    'quota_remaining': key_info.remaining_quota,
                    'usage_percentage': key_info.usage_percentage,
                    'is_active': key_info.is_active,
                    'error_count': key_info.error_count
                })
            
            return {
                'total_quota': total_quota,
                'total_used': total_used,
                'total_remaining': total_remaining,
                'overall_usage_percentage': (total_used / total_quota * 100) if total_quota > 0 else 0,
                'active_keys': sum(1 for k in self.api_keys.values() if k.is_active),
                'keys': key_summaries,
                'stats': {
                    'total_requests': self.stats.total_requests,
                    'total_quota_used': self.stats.total_quota_used,
                    'requests_by_endpoint': self.stats.requests_by_endpoint,
                    'quota_by_endpoint': self.stats.quota_by_endpoint
                }
            }
    
    def estimate_quota_cost(self, operation: str, **kwargs) -> int:
        """Estimate quota cost for an operation.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Estimated quota cost
        """
        if operation == "get_videos":
            video_count = kwargs.get('video_count', 1)
            # videos.list costs 1 unit per request, max 50 videos per request
            return max(1, (video_count + 49) // 50)
        
        elif operation == "get_channels":
            channel_count = kwargs.get('channel_count', 1)
            # channels.list costs 1 unit per request, max 50 channels per request
            return max(1, (channel_count + 49) // 50)
        
        elif operation == "search_videos":
            max_results = kwargs.get('max_results', 50)
            # search.list costs 100 units per request, max 50 results per request
            return max(100, (max_results + 49) // 50 * 100)
        
        elif operation == "get_channel_videos":
            max_results = kwargs.get('max_results', 50)
            # playlistItems.list costs 1 unit per request, max 50 items per request
            return max(1, (max_results + 49) // 50)
        
        else:
            # Default to 1 unit for unknown operations
            return 1
    
    def can_afford_operation(self, operation: str, **kwargs) -> Tuple[bool, int]:
        """Check if we can afford an operation with current quota.
        
        Args:
            operation: Operation type
            **kwargs: Operation parameters
            
        Returns:
            Tuple of (can_afford, estimated_cost)
        """
        estimated_cost = self.estimate_quota_cost(operation, **kwargs)
        total_remaining = sum(key.remaining_quota for key in self.api_keys.values() if key.is_active)
        
        return total_remaining >= estimated_cost, estimated_cost
    
    def get_optimal_batch_size(self, endpoint: APIEndpoint, desired_items: int) -> int:
        """Get optimal batch size for an operation.
        
        Args:
            endpoint: API endpoint
            desired_items: Desired number of items
            
        Returns:
            Optimal batch size
        """
        # Maximum items per request for different endpoints
        max_per_request = {
            APIEndpoint.VIDEOS_LIST: 50,
            APIEndpoint.CHANNELS_LIST: 50,
            APIEndpoint.SEARCH_LIST: 50,
            APIEndpoint.PLAYLIST_ITEMS_LIST: 50,
        }
        
        max_items = max_per_request.get(endpoint, 50)
        total_remaining = sum(key.remaining_quota for key in self.api_keys.values() if key.is_active)
        
        # Calculate how many requests we can afford
        max_requests = total_remaining // endpoint.quota_cost
        max_affordable_items = max_requests * max_items
        
        return min(desired_items, max_affordable_items, max_items)
    
    def reset_key_quota(self, key_name: str) -> bool:
        """Manually reset quota for a specific key.
        
        Args:
            key_name: Name of the API key
            
        Returns:
            True if reset successful
        """
        with self._lock:
            if key_name in self.api_keys:
                self.api_keys[key_name].reset_daily_quota()
                self.api_keys[key_name].is_active = True
                self._save_usage_data()
                return True
            return False
    
    def disable_key(self, key_name: str) -> bool:
        """Disable a specific API key.
        
        Args:
            key_name: Name of the API key
            
        Returns:
            True if disabled successfully
        """
        with self._lock:
            if key_name in self.api_keys:
                self.api_keys[key_name].is_active = False
                self._save_usage_data()
                logger.info(f"Disabled API key: {key_name}")
                return True
            return False
    
    def enable_key(self, key_name: str) -> bool:
        """Enable a specific API key.
        
        Args:
            key_name: Name of the API key
            
        Returns:
            True if enabled successfully
        """
        with self._lock:
            if key_name in self.api_keys:
                self.api_keys[key_name].is_active = True
                self.api_keys[key_name].error_count = 0
                self._save_usage_data()
                logger.info(f"Enabled API key: {key_name}")
                return True
            return False
    
    def _check_quota_resets(self) -> None:
        """Check if any quotas need to be reset (daily reset at midnight PST)."""
        now = datetime.now(timezone.utc)
        
        for key_info in self.api_keys.values():
            # Check if it's been more than 24 hours since last reset
            time_since_reset = now - key_info.last_reset
            
            if time_since_reset >= timedelta(days=1):
                # Check if we've passed midnight PST (UTC-8)
                pst_now = now - timedelta(hours=8)
                pst_last_reset = key_info.last_reset - timedelta(hours=8)
                
                if pst_now.date() > pst_last_reset.date():
                    key_info.reset_daily_quota()
    
    def _load_usage_data(self) -> None:
        """Load quota usage data from storage."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                
                # Load key data
                for key_name, key_data in data.get('keys', {}).items():
                    if key_name in self.api_keys:
                        # Update existing key info with stored data
                        stored_key = APIKeyInfo.from_dict(self.api_keys[key_name].key, key_data)
                        stored_key.key = self.api_keys[key_name].key  # Keep the actual key
                        self.api_keys[key_name] = stored_key
                
                # Load stats
                stats_data = data.get('stats', {})
                self.stats.total_requests = stats_data.get('total_requests', 0)
                self.stats.total_quota_used = stats_data.get('total_quota_used', 0)
                self.stats.requests_by_endpoint = stats_data.get('requests_by_endpoint', {})
                self.stats.quota_by_endpoint = stats_data.get('quota_by_endpoint', {})
                self.stats.errors_by_key = stats_data.get('errors_by_key', {})
                
                logger.info("Loaded quota usage data from storage")
        except Exception as e:
            logger.warning(f"Failed to load quota usage data: {e}")
    
    def _save_usage_data(self) -> None:
        """Save quota usage data to storage."""
        try:
            # Ensure directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'keys': {name: key_info.to_dict() for name, key_info in self.api_keys.items()},
                'stats': {
                    'total_requests': self.stats.total_requests,
                    'total_quota_used': self.stats.total_quota_used,
                    'requests_by_endpoint': self.stats.requests_by_endpoint,
                    'quota_by_endpoint': self.stats.quota_by_endpoint,
                    'errors_by_key': self.stats.errors_by_key
                },
                'last_updated': datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save quota usage data: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - save data."""
        self._save_usage_data()


class QuotaMonitor:
    """Monitor quota usage and provide alerts."""
    
    def __init__(self, quota_manager: QuotaManager):
        """Initialize quota monitor.
        
        Args:
            quota_manager: QuotaManager instance to monitor
        """
        self.quota_manager = quota_manager
        self.alert_thresholds = {
            'warning': 0.8,  # 80% usage
            'critical': 0.95  # 95% usage
        }
    
    def check_quota_health(self) -> Dict[str, Any]:
        """Check quota health and return status.
        
        Returns:
            Dictionary with health status
        """
        summary = self.quota_manager.get_quota_summary()
        
        health_status = {
            'status': 'healthy',
            'alerts': [],
            'recommendations': []
        }
        
        # Check overall usage
        overall_usage = summary['overall_usage_percentage'] / 100
        
        if overall_usage >= self.alert_thresholds['critical']:
            health_status['status'] = 'critical'
            health_status['alerts'].append(
                f"Critical: Overall quota usage at {overall_usage:.1%}"
            )
        elif overall_usage >= self.alert_thresholds['warning']:
            health_status['status'] = 'warning'
            health_status['alerts'].append(
                f"Warning: Overall quota usage at {overall_usage:.1%}"
            )
        
        # Check individual keys
        for key_info in summary['keys']:
            key_usage = key_info['usage_percentage'] / 100
            
            if not key_info['is_active']:
                health_status['alerts'].append(
                    f"Key '{key_info['name']}' is disabled"
                )
            elif key_usage >= self.alert_thresholds['critical']:
                health_status['alerts'].append(
                    f"Key '{key_info['name']}' at {key_usage:.1%} usage"
                )
            elif key_info['error_count'] > 3:
                health_status['alerts'].append(
                    f"Key '{key_info['name']}' has {key_info['error_count']} errors"
                )
        
        # Generate recommendations
        if summary['active_keys'] < len(summary['keys']):
            health_status['recommendations'].append(
                "Consider re-enabling disabled API keys if errors are resolved"
            )
        
        if overall_usage > 0.7:
            health_status['recommendations'].append(
                "Consider optimizing API usage or adding more API keys"
            )
        
        return health_status
    
    def get_usage_forecast(self, hours_ahead: int = 24) -> Dict[str, Any]:
        """Forecast quota usage based on current trends.
        
        Args:
            hours_ahead: Hours to forecast ahead
            
        Returns:
            Usage forecast
        """
        summary = self.quota_manager.get_quota_summary()
        
        # Simple linear projection based on current usage
        # In a real implementation, you might use more sophisticated forecasting
        
        current_usage_rate = summary['total_used'] / 24  # Assume usage over 24 hours
        projected_usage = current_usage_rate * hours_ahead
        
        return {
            'hours_ahead': hours_ahead,
            'current_usage_rate_per_hour': current_usage_rate,
            'projected_additional_usage': projected_usage,
            'projected_total_usage': summary['total_used'] + projected_usage,
            'projected_usage_percentage': ((summary['total_used'] + projected_usage) / summary['total_quota']) * 100,
            'estimated_quota_exhaustion_hours': (summary['total_remaining'] / current_usage_rate) if current_usage_rate > 0 else float('inf')
        }
