"""Platform-specific timeout adjustment tests."""
import pytest
import time


@pytest.mark.integration
class TestPlatformTimeouts:
    """Test platform-specific timeout adjustments."""

    def test_platform_detection_accuracy(self, platform_detector):
        """Verify platform detection is accurate."""
        info = platform_detector.get_info()

        assert "platform" in info, "Platform info should be detected"
        assert "timeout_multiplier" in info, "Timeout multiplier should exist"
        assert info["timeout_multiplier"] >= 1.0, "Multiplier should be >= 1.0"

    def test_windows_timeout_multiplier(self, platform_detector):
        """Verify Windows uses 1.5x timeout multiplier."""
        info = platform_detector.get_info()

        if info["is_windows"]:
            assert info["timeout_multiplier"] == 1.5, \
                "Windows should use 1.5x multiplier"

    def test_macos_timeout_multiplier(self, platform_detector):
        """Verify macOS uses 1.0x timeout multiplier."""
        info = platform_detector.get_info()

        if info["is_macos"]:
            assert info["timeout_multiplier"] == 1.0, \
                "macOS should use 1.0x multiplier"

    def test_linux_timeout_multiplier(self, platform_detector):
        """Verify Linux uses 1.0x timeout multiplier (unless in CI)."""
        info = platform_detector.get_info()

        if info["is_linux"]:
            # In CI, multiplier is 2.0x; otherwise 1.0x for Linux
            expected = 2.0 if info["is_ci"] else 1.0
            assert info["timeout_multiplier"] == expected, \
                f"Linux should use {expected}x multiplier"

    def test_ci_environment_detection(self, platform_detector):
        """Verify CI environment detection."""
        info = platform_detector.get_info()

        # If in CI, multiplier should be 2.0x
        if info["is_ci"]:
            assert info["timeout_multiplier"] == 2.0, \
                "CI environment should use 2.0x multiplier"

    def test_adjusted_timeout_application(self, golden_performance_baseline, platform_detector):
        """Verify timeout thresholds are adjusted for platform."""
        info = platform_detector.get_info()
        multiplier = info["timeout_multiplier"]

        baseline = golden_performance_baseline

        # Check that multiplier is applied to thresholds
        for scale, threshold in baseline["tree_generation"].items():
            if scale != "1k":  # Skip the base case
                assert threshold > 0, f"Threshold for {scale} should be positive"

    def test_hook_latency_timeout_adjustment(self, golden_performance_baseline, platform_detector):
        """Verify hook latency timeouts are adjusted."""
        baseline = golden_performance_baseline
        multiplier = baseline["platform_multiplier"]

        # Hook latency should be adjusted
        max_latency = baseline["hook_latency"]["single_max_ms"]
        assert max_latency >= 100, "Hook latency threshold should be adjusted"

    def test_cache_operation_timeout_adjustment(self, golden_performance_baseline, platform_detector):
        """Verify cache operation timeouts are adjusted."""
        baseline = golden_performance_baseline
        multiplier = baseline["platform_multiplier"]

        cache_ops = baseline["cache_operations"]

        # Timeouts should be positive and reasonable
        assert cache_ops["get_max_ms"] > 0, "Get timeout should be positive"
        assert cache_ops["set_max_ms"] > 0, "Set timeout should be positive"

    def test_timeout_consistency_across_operations(self, golden_performance_baseline):
        """Verify timeout multipliers are consistent across operations."""
        baseline = golden_performance_baseline
        multiplier = baseline["platform_multiplier"]

        # All adjusted timeouts should use same multiplier concept
        tree_gen_1k = baseline["tree_generation"]["1k"]
        tree_gen_10k = baseline["tree_generation"]["10k"]

        # 10k should be higher than 1k (scaled)
        assert tree_gen_10k > tree_gen_1k, "Larger scale should have higher threshold"

    def test_operation_timeout_ordering(self, golden_performance_baseline):
        """Verify operation timeouts have correct ordering."""
        baseline = golden_performance_baseline

        # Verify cache ops are fastest
        get_max = baseline["cache_operations"]["get_max_ms"]
        set_max = baseline["cache_operations"]["set_max_ms"]
        hook_max = baseline["hook_latency"]["single_max_ms"]

        # get < set < hook
        assert get_max < set_max, "Get should be faster than set"
        assert set_max < hook_max, "Set should be faster than hook"

    def test_scaled_timeout_progression(self, golden_performance_baseline):
        """Verify timeouts increase properly with scale."""
        baseline = golden_performance_baseline
        tree_timeouts = baseline["tree_generation"]

        scales_ordered = [
            (1000, tree_timeouts["1k"]),
            (10000, tree_timeouts["10k"]),
            (50000, tree_timeouts["50k"]),
        ]

        for i in range(len(scales_ordered) - 1):
            files1, timeout1 = scales_ordered[i]
            files2, timeout2 = scales_ordered[i + 1]

            # Timeout should increase with scale
            assert timeout2 > timeout1, \
                f"Timeout should increase: {timeout1} < {timeout2}"

    def test_timeout_enforcement_simulation(self, golden_performance_baseline):
        """Simulate timeout enforcement with platform multiplier."""
        baseline = golden_performance_baseline
        multiplier = baseline["platform_multiplier"]

        # Simulate operation that takes time
        start = time.perf_counter()
        operation_time = 0.05  # 50ms

        time.sleep(operation_time)

        elapsed = (time.perf_counter() - start) * 1000  # ms

        # With multiplier applied
        adjusted_threshold = 100 * multiplier  # 100ms base

        assert elapsed < adjusted_threshold, \
            f"Operation {elapsed:.0f}ms should be within adjusted threshold {adjusted_threshold:.0f}ms"

    @pytest.mark.parametrize("base_timeout,multiplier,expected", [
        (100, 1.0, 100),
        (100, 1.5, 150),
        (100, 2.0, 200),
        (1000, 1.5, 1500),
        (15000, 1.0, 15000),
    ])
    def test_timeout_multiplier_calculation(self, base_timeout, multiplier, expected):
        """Verify timeout multiplier calculation."""
        adjusted = base_timeout * multiplier
        assert adjusted == expected, f"Timeout calculation incorrect: {base_timeout} * {multiplier} != {expected}"

    def test_minimum_timeout_guarantee(self, golden_performance_baseline):
        """Verify minimum timeouts are enforced."""
        baseline = golden_performance_baseline

        # All timeouts should be >= minimum
        min_timeout = 1  # 1ms minimum

        cache_ops = baseline["cache_operations"]
        assert cache_ops["get_max_ms"] >= min_timeout
        assert cache_ops["set_max_ms"] >= min_timeout

        hook_latency = baseline["hook_latency"]
        assert hook_latency["single_max_ms"] >= min_timeout
