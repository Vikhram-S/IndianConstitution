"""Disk caching utilities for persistent memoization."""

import os
from pathlib import Path
from typing import Any, Optional

from diskcache import Cache

CACHE_DIR = Path.home() / ".indianconstitution" / "cache"


def ensure_cache_dir() -> None:
    """Ensure the cache directory exists on local filesystem."""
    os.makedirs(CACHE_DIR, exist_ok=True)


class DiskCache:
    """Wrapper around diskcache for key-value storage and function memoization."""

    def __init__(self, directory: Optional[Path] = None) -> None:
        """Initialize DiskCache instance.

        Args:
            directory: Directory path for disk cache database.
        """
        self.directory = directory or CACHE_DIR
        ensure_cache_dir()
        self.cache = Cache(str(self.directory))

    def memoize(self, name: str) -> Any:  # noqa: ANN401
        """Decorator to memoize function results to disk.

        Args:
            name: Tag for memoized cache entry.

        Returns:
            DiskCache memoize decorator function.
        """
        return self.cache.memoize(tag=name)

    def get(self, key: str) -> Any:  # noqa: ANN401
        """Retrieve value from cache.

        Args:
            key: Cache entry key string.

        Returns:
            Cached value if found, None otherwise.
        """
        return self.cache.get(key)

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:  # noqa: ANN401
        """Store key-value pair in cache.

        Args:
            key: Cache entry key string.
            value: Object to store in cache.
            expire: Expiration time in seconds, if any.
        """
        self.cache.set(key, value, expire=expire)

    def clear(self) -> None:
        """Clear all entries from cache."""
        self.cache.clear()


default_cache = DiskCache()
