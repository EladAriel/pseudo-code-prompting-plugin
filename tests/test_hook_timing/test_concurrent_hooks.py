"""Concurrent hook execution tests."""
import pytest
import threading
import time


@pytest.mark.hook
@pytest.mark.parallel
class TestConcurrentHooks:
    """Test concurrent hook execution."""

    def test_concurrent_hooks_no_deadlock(self, concurrent_executor):
        """Verify concurrent hooks don't deadlock."""
        def hook_task():
            time.sleep(0.01)
            return "completed"

        functions = [hook_task for _ in range(4)]
        results = concurrent_executor.run_agents(functions, max_workers=4)

        assert len(results) == 4
        assert all(r == "completed" for r in results)

    def test_hook_result_consistency(self, concurrent_executor):
        """Verify hook results are consistent regardless of order."""
        def hook_a():
            return {"id": 1, "name": "hook_a"}

        def hook_b():
            return {"id": 2, "name": "hook_b"}

        functions = [hook_a, hook_b]
        results = concurrent_executor.run_agents(functions)

        # Both hooks should complete and return correct values
        result_ids = sorted([r.get("id") for r in results if isinstance(r, dict)])
        assert result_ids == [1, 2]

    def test_concurrent_hook_isolation(self, concurrent_executor):
        """Verify concurrent hooks don't interfere."""
        state = {"counter": 0}
        lock = threading.Lock()

        def hook_increment():
            with lock:
                state["counter"] += 1
            time.sleep(0.001)
            return state["counter"]

        functions = [hook_increment for _ in range(10)]
        concurrent_executor.run_agents(functions, max_workers=5)

        # All increments should be recorded
        assert state["counter"] == 10

    def test_concurrent_hook_error_isolation(self, concurrent_executor):
        """Verify errors in one hook don't affect others."""
        def hook_success():
            return "success"

        def hook_error():
            raise ValueError("Hook error")

        def hook_success_2():
            return "success_2"

        functions = [hook_success, hook_error, hook_success_2]
        results = concurrent_executor.run_agents(functions, max_workers=3)

        # Should have results for all hooks (some with errors)
        assert len(results) == 3

    def test_concurrent_hook_resource_usage(self, concurrent_executor, performance_monitor):
        """Monitor resource usage during concurrent hooks."""
        def hook_task():
            data = []
            for i in range(1000):
                data.append(i)
            return len(data)

        functions = [hook_task for _ in range(4)]

        with performance_monitor:
            results = concurrent_executor.run_agents(functions, max_workers=4)

        duration = performance_monitor.metrics["duration_ms"]

        # Should complete reasonably fast
        assert duration < 1000
        assert all(isinstance(r, int) for r in results)

    @pytest.mark.parametrize("num_hooks", [2, 4, 8])
    def test_concurrent_scalability(self, concurrent_executor, num_hooks):
        """Test concurrent hook scalability."""
        def hook_task():
            time.sleep(0.01)
            return "done"

        functions = [hook_task for _ in range(num_hooks)]
        results = concurrent_executor.run_agents(functions, max_workers=num_hooks)

        assert len(results) == num_hooks
