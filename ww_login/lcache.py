import time
from collections import OrderedDict
from typing import Any, Optional, Tuple


class TimedCache:
    """A time-based cache implementation with size limit and automatic cleanup."""

    def __init__(self, timeout: int = 5, maxsize: int = 10):
        """
        Initialize the timed cache.

        Args:
            timeout: Time in seconds before entries expire
            maxsize: Maximum number of entries in cache
        """
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self.timeout = timeout
        self.maxsize = maxsize

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache with expiration time.

        Args:
            key: Cache key
            value: Value to store
        """
        if len(self.cache) >= self.maxsize:
            self._clean_up()
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = (value, time.time() + self.timeout)

    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Get a value from the cache if it exists and hasn't expired.

        Args:
            key: Cache key
            default: Default value if key not found or expired

        Returns:
            Cached value if valid, else default value
        """
        if key in self.cache:
            value, expiry = self.cache.pop(key)
            if time.time() < expiry:
                self.cache[key] = (value, expiry)
                return value
        return default

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
            key: Cache key to delete
        """
        self.cache.pop(key, None)

    def _clean_up(self) -> None:
        """Remove expired entries from the cache."""
        current_time = time.time()
        self.cache = OrderedDict(
            (k, v) for k, v in self.cache.items() if v[1] > current_time
        )
