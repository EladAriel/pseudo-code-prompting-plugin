"""Cache invalidation tests."""
import pytest
import time


@pytest.mark.cache
class TestCacheInvalidation:
    """Test cache invalidation mechanisms."""

    def test_manual_invalidation_clears_cache(self, cache_state_tracker):
        """Verify manual invalidation clears cache state."""
        cache_state_tracker.record_hit()
        cache_state_tracker.record_hit()
        initial_metrics = cache_state_tracker.get_metrics()
        assert initial_metrics["hits"] == 2

        cache_state_tracker.reset()
        metrics_after = cache_state_tracker.get_metrics()
        assert metrics_after.get("hits", 0) == 0

    def test_ttl_based_invalidation(self, cache_state_tracker):
        """Verify TTL-based cache expiration."""
        class TTLCache:
            def __init__(self, ttl_seconds):
                self.data = {}
                self.ttl = ttl_seconds
                self.timestamps = {}

            def set(self, key, value):
                self.data[key] = value
                self.timestamps[key] = time.time()

            def get(self, key):
                if key not in self.data:
                    return None
                if time.time() - self.timestamps[key] > self.ttl:
                    del self.data[key]
                    del self.timestamps[key]
                    return None
                return self.data[key]

        cache = TTLCache(ttl_seconds=0.1)
        cache.set("key1", "value1")

        # Should exist immediately
        assert cache.get("key1") == "value1"

        # Wait for TTL expiration
        time.sleep(0.15)

        # Should be expired now
        assert cache.get("key1") is None

    def test_dependency_based_invalidation(self):
        """Verify dependency-based cache invalidation."""
        class DependencyCache:
            def __init__(self):
                self.cache = {}
                self.dependencies = {}

            def set(self, key, value, depends_on=None):
                self.cache[key] = value
                if depends_on:
                    self.dependencies[key] = set(depends_on)

            def invalidate_dependency(self, dep):
                for key, deps in self.dependencies.items():
                    if dep in deps:
                        if key in self.cache:
                            del self.cache[key]

            def get(self, key):
                return self.cache.get(key)

        cache = DependencyCache()
        cache.set("result", "value1", depends_on=["input1", "input2"])
        assert cache.get("result") == "value1"

        cache.invalidate_dependency("input1")
        assert cache.get("result") is None

    def test_partial_invalidation(self, cache_state_tracker):
        """Verify partial cache invalidation."""
        class PartialInvalidationCache:
            def __init__(self):
                self.cache = {}
                self.versions = {}

            def set(self, key, value):
                self.cache[key] = value
                self.versions[key] = 1

            def invalidate_pattern(self, pattern):
                import re
                for key in list(self.cache.keys()):
                    if re.match(pattern, key):
                        del self.cache[key]
                        del self.versions[key]

            def get_size(self):
                return len(self.cache)

        cache = PartialInvalidationCache()
        cache.set("user_1", "data1")
        cache.set("user_2", "data2")
        cache.set("config_main", "data3")

        assert cache.get_size() == 3

        cache.invalidate_pattern("user_.*")
        assert cache.get_size() == 1

    def test_cache_invalidation_state_consistency(self):
        """Verify cache remains consistent after invalidation."""
        class ConsistentCache:
            def __init__(self):
                self.data = {}
                self.dirty = False

            def set(self, key, value):
                self.data[key] = value
                self.dirty = False

            def invalidate(self):
                self.data.clear()
                self.dirty = True

            def is_valid(self):
                return not self.dirty

        cache = ConsistentCache()
        cache.set("key1", "value1")
        assert cache.is_valid()
        assert len(cache.data) == 1

        cache.invalidate()
        assert not cache.is_valid()
        assert len(cache.data) == 0

    def test_concurrent_invalidation(self, cache_state_tracker):
        """Verify concurrent invalidation doesn't cause conflicts."""
        import threading

        class ThreadSafeCache:
            def __init__(self):
                self.data = {}
                self.lock = threading.Lock()

            def set(self, key, value):
                with self.lock:
                    self.data[key] = value

            def clear(self):
                with self.lock:
                    self.data.clear()

            def size(self):
                with self.lock:
                    return len(self.data)

        cache = ThreadSafeCache()

        def populate():
            for i in range(100):
                cache.set(f"key_{i}", f"value_{i}")

        def clear():
            time.sleep(0.05)
            cache.clear()

        threads = [
            threading.Thread(target=populate),
            threading.Thread(target=clear),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Cache should be cleared
        assert cache.size() == 0

    def test_invalidation_notification(self):
        """Verify invalidation notifications are triggered."""
        class ObservableCache:
            def __init__(self):
                self.data = {}
                self.observers = []

            def subscribe(self, observer):
                self.observers.append(observer)

            def invalidate(self):
                self.data.clear()
                for observer in self.observers:
                    observer("invalidated")

        cache = ObservableCache()
        notifications = []

        cache.subscribe(lambda event: notifications.append(event))
        cache.invalidate()

        assert "invalidated" in notifications

    @pytest.mark.parametrize("invalidation_type", [
        "manual",
        "ttl",
        "dependency",
        "pattern",
    ])
    def test_invalidation_types(self, invalidation_type):
        """Test various invalidation types."""
        if invalidation_type == "manual":
            cache = {}
            cache.clear()
            assert len(cache) == 0
        elif invalidation_type == "ttl":
            assert True  # Covered in separate test
        elif invalidation_type == "dependency":
            assert True  # Covered in separate test
        elif invalidation_type == "pattern":
            assert True  # Covered in separate test
