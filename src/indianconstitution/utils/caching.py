import os
from pathlib import Path
from typing import Any, Callable, Optional
import functools
from diskcache import Cache

CACHE_DIR = Path.home() / ".indianconstitution" / "cache"

def ensure_cache_dir():
    """Ensure the cache directory exists."""
    os.makedirs(CACHE_DIR, exist_ok=True)

class DiskCache:
    """Wrapper around diskcache for easy use in the library."""
    
    def __init__(self, directory: Optional[Path] = None):
        self.directory = directory or CACHE_DIR
        ensure_cache_dir()
        self.cache = Cache(str(self.directory))

    def memoize(self, name: str):
        """Decorator to memoize function results to disk."""
        return self.cache.memoize(tag=name)

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def set(self, key: str, value: Any, expire: Optional[int] = None):
        self.cache.set(key, value, expire=expire)

    def clear(self):
        self.cache.clear()

# Global cache instance
default_cache = DiskCache()
