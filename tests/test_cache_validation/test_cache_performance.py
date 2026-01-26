"""Cache performance benchmarking tests."""
import pytest
import time


@pytest.mark.cache
@pytest.mark.performance
class TestCachePerformance:
    """Test cache operation performance."""

    def test_cache_get_latency(self, performance_monitor, golden_performance_baseline):
        """Verify cache get operation latency is within threshold."""
        cache = {}
        cache["key1"] = "value1"

        with performance_monitor:
            for _ in range(1000):
                _ = cache.get("key1")

        duration = performance_monitor.metrics["duration_ms"]
        avg_latency = duration / 1000

        max_latency = golden_performance_baseline["cache_operations"]["get_max_ms"]
        assert avg_latency < max_latency, \
            f"Cache get latency {avg_latency:.2f}ms exceeds threshold {max_latency:.2f}ms"

    def test_cache_set_latency(self, performance_monitor, golden_performance_baseline):
        """Verify cache set operation latency is within threshold."""
        cache = {}

        with performance_monitor:
            for i in range(1000):
                cache[f"key_{i}"] = f"value_{i}"

        duration = performance_monitor.metrics["duration_ms"]
        avg_latency = duration / 1000

        max_latency = golden_performance_baseline["cache_operations"]["set_max_ms"]
        assert avg_latency < max_latency, \
            f"Cache set latency {avg_latency:.2f}ms exceeds threshold {max_latency:.2f}ms"

    def test_cache_throughput(self, performance_monitor, golden_performance_baseline, cache_state_tracker):
        """Verify cache throughput exceeds minimum requirement."""
        cache = {}

        with performance_monitor:
            for i in range(5000):
                cache[f"key_{i}"] = f"value_{i}"
                if i % 2 == 0:
                    cache_state_tracker.record_hit()
                else:
                    cache_state_tracker.record_miss()

        duration_sec = performance_monitor.metrics["duration_ms"] / 1000
        throughput = 5000 / duration_sec if duration_sec > 0 else 0

        min_throughput = golden_performance_baseline["cache_operations"]["throughput_min_ops_per_sec"]
        assert throughput >= min_throughput, \
            f"Cache throughput {throughput:.0f} ops/sec below minimum {min_throughput} ops/sec"

    def test_cache_memory_efficiency(self, performance_monitor, memory_profiler):
        """Verify cache memory usage is reasonable."""
        memory_profiler.start()

        cache = {}
        for i in range(10000):
            cache[f"key_{i}"] = f"value_{i}" * 10

        metrics = memory_profiler.stop()

        memory_used = metrics.get("peak_allocated_mb", 0)
        # For 10k entries with string data, should be reasonable
        assert memory_used < 100, f"Cache using excessive memory: {memory_used:.2f}MB"

    def test_cache_lookup_consistency(self, performance_monitor):
        """Verify cache lookup times are consistent."""
        cache = {}
        for i in range(1000):
            cache[f"key_{i}"] = i

        lookup_times = []
        for _ in range(10):
            with performance_monitor:
                for i in range(100):
                    _ = cache[f"key_{i}"]

            lookup_times.append(performance_monitor.metrics["duration_ms"])

        # Calculate variance
        avg = sum(lookup_times) / len(lookup_times)
        variance = sum((t - avg) ** 2 for t in lookup_times) / len(lookup_times)
        std_dev = variance ** 0.5

        # Lookup times should be consistent (low variance)
        assert std_dev < avg * 0.5, "Cache lookup times have high variance"

    @pytest.mark.parametrize("cache_size", [100, 1000, 10000])
    def test_cache_performance_scaling(self, performance_monitor, cache_size):
        """Verify cache performance scales with size."""
        cache = {}

        # Populate cache
        for i in range(cache_size):
            cache[f"key_{i}"] = i

        # Measure lookup performance
        with performance_monitor:
            for _ in range(1000):
                _ = cache.get("key_0")

        duration = performance_monitor.metrics["duration_ms"]
        # Performance should remain sub-linear with size
        assert duration < 100, f"Cache lookup degraded with {cache_size} entries"

    def test_cache_eviction_performance(self, performance_monitor, cache_state_tracker):
        """Verify cache eviction doesn't significantly impact performance."""
        class LRUCache:
            def __init__(self, max_size):
                self.cache = {}
                self.access_order = []
                self.max_size = max_size

            def get(self, key):
                if key in self.cache:
                    self.access_order.remove(key)
                    self.access_order.append(key)
                    cache_state_tracker.record_hit()
                    return self.cache[key]
                cache_state_tracker.record_miss()
                return None

            def set(self, key, value):
                if len(self.cache) >= self.max_size:
                    lru_key = self.access_order.pop(0)
                    del self.cache[lru_key]
                    cache_state_tracker.record_eviction()

                self.cache[key] = value
                if key in self.access_order:
                    self.access_order.remove(key)
                self.access_order.append(key)

        cache = LRUCache(max_size=100)

        with performance_monitor:
            for i in range(1000):
                cache.set(f"key_{i}", i)

        duration = performance_monitor.metrics["duration_ms"]
        metrics = cache_state_tracker.get_metrics()

        assert metrics["evictions"] > 0, "Cache should have evictions"
        assert duration < 500, "Cache eviction slowed performance significantly"

    def test_cache_batch_operations(self, performance_monitor):
        """Verify cache performance with batch operations."""
        cache = {}

        with performance_monitor:
            batch = {f"key_{i}": i for i in range(1000)}
            cache.update(batch)

        duration = performance_monitor.metrics["duration_ms"]
        assert duration < 100, "Batch cache operations are too slow"

    def test_cache_concurrent_access_performance(self, performance_monitor, concurrent_executor):
        """Verify cache performance under concurrent access."""
        cache = {}
        for i in range(100):
            cache[f"key_{i}"] = i

        def access_cache():
            results = []
            for i in range(100):
                results.append(cache.get(f"key_{i % 100}"))
            return results

        functions = [access_cache for _ in range(4)]

        with performance_monitor:
            results = concurrent_executor.run_agents(functions)

        duration = performance_monitor.metrics["duration_ms"]
        timings = concurrent_executor.get_timings()

        assert duration < 1000, "Concurrent cache access is too slow"
        assert len(results) == 4, "Not all concurrent operations completed"
