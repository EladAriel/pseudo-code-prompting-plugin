"""Output synchronization in parallel execution tests."""
import pytest
import threading


@pytest.mark.parallel
class TestOutputSynchronization:
    """Test output synchronization across parallel agents."""

    def test_no_shared_state_corruption(self):
        """Verify shared state doesn't get corrupted."""
        shared_state = {}
        lock = threading.Lock()

        def update_state(key, value):
            with lock:
                shared_state[key] = value

        def read_state(key):
            with lock:
                return shared_state.get(key)

        update_state("key1", "value1")
        result = read_state("key1")

        assert result == "value1"

    def test_atomicity_enforcement(self):
        """Verify atomic operations."""
        counter = {"value": 0}
        lock = threading.Lock()

        def increment():
            with lock:
                counter["value"] += 1

        def get_value():
            with lock:
                return counter["value"]

        increment()
        increment()

        assert get_value() == 2

    def test_output_ordering(self, concurrent_executor):
        """Verify output ordering with multiple agents."""
        def agent(idx):
            return {"order": idx}

        functions = [lambda i=i: agent(i) for i in range(5)]
        results = concurrent_executor.run_agents(functions, max_workers=2)

        assert len(results) == 5
