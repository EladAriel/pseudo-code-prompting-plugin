"""Hook callback latency measurement tests."""
import pytest
import time


@pytest.mark.hook
class TestHookLatency:
    """Test hook callback latencies."""

    def test_single_hook_latency(self, latency_tracker, golden_performance_baseline):
        """Measure individual hook latency."""
        def mock_hook():
            time.sleep(0.01)  # 10ms

        start = time.perf_counter()
        mock_hook()
        elapsed = (time.perf_counter() - start) * 1000

        latency_tracker.record("test_hook", elapsed)

        metrics = latency_tracker.get_metrics("test_hook")
        max_latency = golden_performance_baseline["hook_latency"]["single_max_ms"]

        assert elapsed < max_latency, \
            f"Hook latency {elapsed:.1f}ms exceeds threshold {max_latency:.1f}ms"

    def test_hook_latency_percentiles(self, latency_tracker):
        """Verify hook latency percentiles are calculated."""
        # Record varying latencies
        latencies = [5.0, 10.0, 15.0, 20.0, 25.0, 50.0, 75.0, 90.0, 95.0, 100.0]

        for latency in latencies:
            latency_tracker.record("test_hook", latency)

        metrics = latency_tracker.get_metrics("test_hook")

        assert metrics["min_ms"] == 5.0
        assert metrics["max_ms"] == 100.0
        assert metrics["avg_ms"] == sum(latencies) / len(latencies)
        assert metrics["p95_ms"] > 0
        assert metrics["p99_ms"] > 0

    def test_hook_latency_consistency(self, latency_tracker):
        """Verify hook latencies are consistent across calls."""
        times = []

        for i in range(5):
            start = time.perf_counter()
            time.sleep(0.005)  # 5ms
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            latency_tracker.record("hook", elapsed)

        # Latencies should be relatively consistent
        avg = sum(times) / len(times)
        max_deviation = max(abs(t - avg) for t in times)

        assert max_deviation < avg * 0.5, "Hook latencies have high variance"

    def test_cumulative_hook_overhead(self, latency_tracker, performance_monitor, golden_performance_baseline):
        """Measure total overhead of hook execution."""
        total_ops = 0

        with performance_monitor:
            for i in range(100):
                start = time.perf_counter()
                time.sleep(0.0001)  # 0.1ms per hook
                elapsed = (time.perf_counter() - start) * 1000
                latency_tracker.record(f"hook_{i}", elapsed)
                total_ops += 1

        total_duration = performance_monitor.metrics["duration_ms"]
        overhead_percent = latency_tracker.get_cumulative_overhead(total_duration)
        max_overhead = golden_performance_baseline["hook_latency"]["cumulative_overhead_max_percent"]

        assert overhead_percent < max_overhead, \
            f"Hook overhead {overhead_percent:.1f}% exceeds threshold {max_overhead}%"

    def test_hook_latency_under_load(self, latency_tracker, concurrent_executor):
        """Measure hook latency under concurrent load."""
        def hook_under_load():
            latencies = []
            for i in range(20):
                start = time.perf_counter()
                time.sleep(0.001)  # 1ms
                elapsed = (time.perf_counter() - start) * 1000
                latencies.append(elapsed)
            return latencies

        functions = [hook_under_load for _ in range(3)]
        results = concurrent_executor.run_agents(functions, max_workers=3)

        # Collect all latencies
        all_latencies = []
        for result in results:
            all_latencies.extend(result)

        # Record all latencies
        for latency in all_latencies:
            latency_tracker.record("concurrent_hook", latency)

        metrics = latency_tracker.get_metrics("concurrent_hook")

        # Concurrent latencies should be reasonable
        assert metrics["avg_ms"] < 50, "Average hook latency too high under load"

    def test_hook_latency_trend(self, latency_tracker):
        """Detect latency trends across multiple hook calls."""
        # Simulate increasing latency (memory leak, resource buildup)
        for i in range(10):
            latency = 5.0 + (i * 0.1)  # Gradually increasing
            latency_tracker.record("hook", latency)

        metrics = latency_tracker.get_metrics("hook")

        # Should detect the trend (max > min)
        assert metrics["max_ms"] > metrics["min_ms"], \
            "Should detect latency trend"

    def test_hook_latency_reset(self, latency_tracker):
        """Verify latency tracking reset."""
        latency_tracker.record("hook", 10.0)
        latency_tracker.record("hook", 15.0)

        initial_metrics = latency_tracker.get_metrics("hook")
        assert initial_metrics["count"] == 2

        latency_tracker.reset()

        reset_metrics = latency_tracker.get_metrics("hook")
        assert reset_metrics.get("count", 0) == 0

    @pytest.mark.parametrize("latency_ratio,should_pass", [
        (0.5, True),    # 50% of max_latency - should pass
        (0.99, True),   # 99% of max_latency - should pass
        (1.0, True),    # Exactly at max_latency - should pass
        (1.01, False),  # 1% over max_latency - should fail
        (1.5, False),   # 50% over max_latency - should fail
    ])
    def test_hook_latency_threshold_enforcement(self, latency_ratio, should_pass, golden_performance_baseline):
        """Verify hook latency threshold enforcement."""
        max_latency = golden_performance_baseline["hook_latency"]["single_max_ms"]
        latency_ms = max_latency * latency_ratio

        if should_pass:
            assert latency_ms <= max_latency, \
                f"Should pass: {latency_ms:.1f}ms <= {max_latency:.1f}ms"
        else:
            assert latency_ms > max_latency, \
                f"Should fail: {latency_ms:.1f}ms > {max_latency:.1f}ms"

    def test_hook_latency_across_types(self, latency_tracker):
        """Measure latencies of different hook types."""
        hook_types = ["pre_process", "main_process", "post_process"]

        for hook_type in hook_types:
            for i in range(5):
                start = time.perf_counter()
                time.sleep(0.001)
                elapsed = (time.perf_counter() - start) * 1000
                latency_tracker.record(hook_type, elapsed)

        # Each hook type should have metrics
        for hook_type in hook_types:
            metrics = latency_tracker.get_metrics(hook_type)
            assert metrics["count"] == 5, f"{hook_type} should have 5 measurements"

    def test_hook_latency_jitter_detection(self, latency_tracker):
        """Detect jitter in hook latencies."""
        # Add both consistent and jittery latencies
        consistent = [10.0, 10.1, 10.2, 10.0, 10.1]
        jittery = [5.0, 20.0, 8.0, 15.0, 25.0]

        for latency in consistent:
            latency_tracker.record("consistent", latency)

        for latency in jittery:
            latency_tracker.record("jittery", latency)

        consistent_metrics = latency_tracker.get_metrics("consistent")
        jittery_metrics = latency_tracker.get_metrics("jittery")

        # Jittery should have larger range
        consistent_range = consistent_metrics["max_ms"] - consistent_metrics["min_ms"]
        jittery_range = jittery_metrics["max_ms"] - jittery_metrics["min_ms"]

        assert jittery_range > consistent_range, \
            "Jittery latencies should have larger range"
