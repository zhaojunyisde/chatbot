"""Rate limiting for chat endpoints."""
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import HTTPException, status
from collections import defaultdict
import threading

# Rate limit configuration
GLOBAL_LIMIT_PER_MINUTE = 100
USER_LIMIT_PER_MINUTE = 10


class RateLimiter:
    """
    Custom rate limiter with both global and per-user limits.
    Uses in-memory storage with automatic cleanup of old entries.
    """

    def __init__(self):
        self.global_requests: List[datetime] = []
        self.user_requests: Dict[str, List[datetime]] = defaultdict(list)
        self.lock = threading.Lock()

    def _cleanup_old_requests(self, requests: List[datetime], window_minutes: int = 1) -> List[datetime]:
        """Remove requests older than the time window."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=window_minutes)
        return [req_time for req_time in requests if req_time > cutoff_time]

    def check_rate_limit(self, username: str) -> None:
        """
        Check if the request should be allowed based on rate limits.
        Raises HTTPException if rate limit is exceeded.

        Args:
            username: The username making the request

        Raises:
            HTTPException: If either global or user rate limit is exceeded
        """
        with self.lock:
            current_time = datetime.utcnow()

            # Cleanup old requests
            self.global_requests = self._cleanup_old_requests(self.global_requests)
            if username in self.user_requests:
                self.user_requests[username] = self._cleanup_old_requests(
                    self.user_requests[username]
                )

            # Check global rate limit
            if len(self.global_requests) >= GLOBAL_LIMIT_PER_MINUTE:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Service-wide rate limit exceeded",
                        "message": f"The service has reached its limit of {GLOBAL_LIMIT_PER_MINUTE} requests per minute. Please try again later.",
                        "retry_after": 60
                    }
                )

            # Check per-user rate limit
            user_request_count = len(self.user_requests[username])
            if user_request_count >= USER_LIMIT_PER_MINUTE:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "User rate limit exceeded",
                        "message": f"You have reached your limit of {USER_LIMIT_PER_MINUTE} requests per minute. Please try again later.",
                        "retry_after": 60,
                        "current_usage": user_request_count,
                        "limit": USER_LIMIT_PER_MINUTE
                    }
                )

            # Record this request
            self.global_requests.append(current_time)
            self.user_requests[username].append(current_time)

    def get_rate_limit_status(self, username: str) -> Dict:
        """
        Get the current rate limit status for a user.

        Args:
            username: The username to check

        Returns:
            Dictionary with rate limit information
        """
        with self.lock:
            # Cleanup old requests
            self.global_requests = self._cleanup_old_requests(self.global_requests)
            if username in self.user_requests:
                self.user_requests[username] = self._cleanup_old_requests(
                    self.user_requests[username]
                )

            global_count = len(self.global_requests)
            user_count = len(self.user_requests[username])

            return {
                "global": {
                    "current": global_count,
                    "limit": GLOBAL_LIMIT_PER_MINUTE,
                    "remaining": max(0, GLOBAL_LIMIT_PER_MINUTE - global_count),
                    "window": "1 minute"
                },
                "user": {
                    "current": user_count,
                    "limit": USER_LIMIT_PER_MINUTE,
                    "remaining": max(0, USER_LIMIT_PER_MINUTE - user_count),
                    "window": "1 minute"
                }
            }


# Global rate limiter instance
rate_limiter = RateLimiter()
