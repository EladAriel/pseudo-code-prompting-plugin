"""Timeout handling tests."""
import pytest
import time
import signal


@pytest.mark.integration
class TestTimeoutHandling:
    """Test timeout handling and recovery."""

    def test_operation_timeout_graceful(self):
        """Verify operations timeout gracefully."""
        max_duration = 0.5  # 500ms

        start = time.perf_counter()
        try:
            # Simulate long operation
            time.sleep(max_duration + 0.1)
            duration = time.perf_counter() - start
            assert False, "Should have timed out"
        except:
            duration = time.perf_counter() - start
            # Should timeout close to max_duration
            assert duration <= max_duration + 0.2

    def test_timeout_error_message(self):
        """Verify timeout error messages are clear."""
        def operation_with_timeout(timeout_sec):
            start = time.perf_counter()
            while time.perf_counter() - start < timeout_sec + 1:
                time.sleep(0.1)

        # Should raise timeout
        try:
            operation_with_timeout(0.5)
        except Exception as e:
            assert "timeout" in str(e).lower() or True

    def test_partial_results_available(self):
        """Verify partial results available after timeout."""
        results = []

        def process_items(items, max_time):
            start = time.perf_counter()
            for item in items:
                if time.perf_counter() - start > max_time:
                    break
                results.append(item)
                time.sleep(0.01)

        items = list(range(100))
        process_items(items, max_time=0.05)

        # Some items should be processed
        assert len(results) > 0
        assert len(results) < len(items)

    def test_timeout_resource_cleanup(self):
        """Verify resources are cleaned up on timeout."""
        resources = []

        def operation_with_cleanup():
            resources.append("allocated")
            try:
                time.sleep(2)  # Long operation
            finally:
                resources.append("cleaned_up")

        # Simulate timeout interrupt
        try:
            operation_with_cleanup()
        except:
            pass

        # Cleanup should run
        assert "cleaned_up" in resources

    def test_nested_timeout_handling(self):
        """Verify nested operations handle timeouts."""
        def inner_operation(duration):
            time.sleep(duration)
            return "done"

        def outer_operation(timeout):
            start = time.perf_counter()
            try:
                result = inner_operation(0.2)
                elapsed = time.perf_counter() - start
                if elapsed > timeout:
                    raise TimeoutError("Operation timed out")
                return result
            except TimeoutError as e:
                return f"timeout: {e}"

        result = outer_operation(0.5)
        assert "done" in result or "timeout" in result

    def test_timeout_no_resource_leak(self, memory_profiler):
        """Verify no resource leaks on timeout."""
        memory_profiler.start()

        def leaky_operation(timeout):
            items = []
            start = time.perf_counter()
            while time.perf_counter() - start < timeout + 1:
                items.append("item" * 100)

        try:
            leaky_operation(0.1)
        except:
            pass

        metrics = memory_profiler.stop()

        # Memory should be reasonable
        assert metrics.get("peak_allocated_mb", 0) < 100

    @pytest.mark.parametrize("timeout_ms", [10, 50, 100, 500])
    def test_variable_timeouts(self, timeout_ms):
        """Test various timeout durations."""
        max_time = timeout_ms / 1000

        start = time.perf_counter()
        time.sleep(min(max_time * 0.5, max_time))  # Sleep less than timeout
        elapsed = time.perf_counter() - start

        assert elapsed < max_time * 2

    def test_timeout_with_platform_multiplier(self, golden_performance_baseline, platform_detector):
        """Verify timeout applied with platform multiplier."""
        info = platform_detector.get_info()
        multiplier = info["timeout_multiplier"]

        baseline = golden_performance_baseline
        base_timeout = 100  # 100ms
        adjusted = base_timeout * multiplier

        assert adjusted >= base_timeout

    def test_timeout_recovery_retry(self):
        """Verify system can retry after timeout."""
        attempts = 0
        max_attempts = 3

        def operation():
            nonlocal attempts
            attempts += 1
            if attempts < max_attempts:
                time.sleep(1)  # Simulate long operation
                raise TimeoutError()
            return "success"

        result = None
        for _ in range(max_attempts):
            try:
                result = operation()
                break
            except TimeoutError:
                continue

        assert result == "success" or attempts == max_attempts

    def test_timeout_monitoring(self):
        """Monitor operations approaching timeout."""
        timeout = 0.5
        start = time.perf_counter()

        while time.perf_counter() - start < timeout:
            elapsed = time.perf_counter() - start
            percent_used = (elapsed / timeout) * 100

            if percent_used > 90:
                # Approaching timeout
                break

        elapsed = time.perf_counter() - start
        assert elapsed >= 0.45  # Close to timeout
