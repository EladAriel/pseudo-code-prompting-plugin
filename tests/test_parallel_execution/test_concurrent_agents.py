"""Concurrent agent execution tests."""
import pytest
import time


@pytest.mark.parallel
class TestConcurrentAgents:
    """Test concurrent agent invocation."""

    def test_concurrent_agent_execution(self, concurrent_executor):
        """Verify agents execute concurrently."""
        def agent_transform():
            time.sleep(0.05)
            return "transform_result"

        def agent_validate():
            time.sleep(0.05)
            return "validate_result"

        functions = [agent_transform, agent_validate]

        start = time.perf_counter()
        results = concurrent_executor.run_agents(functions, max_workers=2)
        duration = (time.perf_counter() - start) * 1000

        # Should complete faster than sequential (2x 50ms = 100ms)
        assert duration < 150, f"Concurrent execution too slow: {duration:.0f}ms"
        assert len(results) == 2

    def test_agent_completion_order(self, concurrent_executor):
        """Verify all agents complete."""
        def agent_1():
            time.sleep(0.02)
            return "agent_1"

        def agent_2():
            time.sleep(0.01)
            return "agent_2"

        def agent_3():
            time.sleep(0.015)
            return "agent_3"

        functions = [agent_1, agent_2, agent_3]
        results = concurrent_executor.run_agents(functions, max_workers=3)

        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    def test_agent_result_correctness(self, concurrent_executor):
        """Verify concurrent agent results are correct."""
        def agent_add(a=5, b=3):
            return a + b

        def agent_multiply(a=5, b=3):
            return a * b

        def agent_power(a=5, b=3):
            return a ** b

        # Wrap with lambda to pass data
        functions = [
            lambda: agent_add(),
            lambda: agent_multiply(),
            lambda: agent_power(),
        ]

        results = concurrent_executor.run_agents(functions)

        assert 8 in results  # 5 + 3
        assert 15 in results  # 5 * 3
        assert 125 in results  # 5 ** 3

    def test_agent_error_isolation(self, concurrent_executor):
        """Verify agent errors don't affect others."""
        def agent_success():
            return "success"

        def agent_failing():
            raise RuntimeError("Agent failed")

        def agent_success_2():
            return "success_2"

        functions = [agent_success, agent_failing, agent_success_2]
        results = concurrent_executor.run_agents(functions, max_workers=3)

        # Should have 3 results (one with error)
        assert len(results) == 3

    def test_agent_timing_distribution(self, concurrent_executor):
        """Verify agent timings are tracked."""
        def agent_fast():
            time.sleep(0.01)
            return "fast"

        def agent_slow():
            time.sleep(0.05)
            return "slow"

        functions = [agent_fast, agent_slow]
        concurrent_executor.run_agents(functions)

        timings = concurrent_executor.get_timings()
        assert len(timings) == 2

    @pytest.mark.parametrize("num_agents", [2, 4, 8])
    def test_agent_concurrency_levels(self, concurrent_executor, num_agents):
        """Test different concurrency levels."""
        def agent_task():
            time.sleep(0.01)
            return "done"

        functions = [agent_task for _ in range(num_agents)]

        start = time.perf_counter()
        results = concurrent_executor.run_agents(functions, max_workers=min(num_agents, 4))
        duration = (time.perf_counter() - start) * 1000

        assert len(results) == num_agents

    def test_agent_output_consistency(self, concurrent_executor):
        """Verify agent outputs are consistent."""
        def agent_json():
            return {"type": "json", "value": 42}

        def agent_list():
            return [1, 2, 3, 4, 5]

        def agent_string():
            return "result_string"

        functions = [agent_json, agent_list, agent_string]
        results = concurrent_executor.run_agents(functions)

        assert len(results) == 3
        assert any(isinstance(r, dict) for r in results)
        assert any(isinstance(r, list) for r in results)
        assert any(isinstance(r, str) for r in results)
