"""Tests for utility modules like caching."""

from pathlib import Path

from indianconstitution.utils.caching import DiskCache, default_cache


def test_disk_cache(tmp_path: Path):
    """DiskCache set, get, clear functionality."""
    cache = DiskCache(directory=tmp_path / "cache")
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    cache.clear()
    assert cache.get("key1") is None


def test_default_cache_exists():
    """default_cache instance is created."""
    assert default_cache is not None

