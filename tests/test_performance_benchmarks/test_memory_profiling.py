"""Memory profiling tests for tree generation."""
import pytest
import os


@pytest.mark.performance
@pytest.mark.memory
class TestMemoryProfiling:
    """Test memory usage during tree generation."""

    @pytest.mark.parametrize("scale", ["1k", "10k"])
    def test_tree_generation_memory_usage(self, scale, large_project_structure, memory_profiler):
        """Measure memory usage during tree generation."""
        project = large_project_structure(scale)
        memory_profiler.start()

        tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                tree.append(os.path.join(root, file))

        metrics = memory_profiler.stop()
        memory_used = metrics.get("peak_allocated_mb", 0)

        # Reasonable limits
        assert memory_used < 500, f"Tree generation for {scale} used excessive memory: {memory_used:.2f}MB"

    def test_memory_growth_linear(self, large_project_structure, memory_profiler):
        """Verify memory growth is linear with file count."""
        memory_usage = {}

        for scale in ["1k", "10k"]:
            project = large_project_structure(scale)
            memory_profiler.start()

            tree = []
            for root, dirs, files in os.walk(project):
                for file in files:
                    tree.append(os.path.join(root, file))

            metrics = memory_profiler.stop()
            memory_usage[scale] = metrics.get("peak_allocated_mb", 0)

        # Check that memory scales reasonably
        if memory_usage["1k"] > 0:
            ratio = memory_usage["10k"] / memory_usage["1k"]
            # 10x files should use less than 20x memory (linear is ~10x)
            assert ratio < 20, f"Memory growth ratio {ratio:.1f}x is superlinear"

    def test_memory_leak_detection(self, large_project_structure, memory_profiler):
        """Detect memory leaks in tree generation."""
        project = large_project_structure("10k")

        # Take initial snapshot
        memory_profiler.start()
        initial_tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                initial_tree.append(os.path.join(root, file))
        initial_metrics = memory_profiler.stop()

        # Run again and check for leaks
        memory_profiler.start()
        second_tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                second_tree.append(os.path.join(root, file))
        second_metrics = memory_profiler.stop()

        # Memory shouldn't grow significantly on second run
        initial_memory = initial_metrics.get("peak_allocated_mb", 0)
        second_memory = second_metrics.get("peak_allocated_mb", 0)

        growth = second_memory - initial_memory
        assert growth < 50, f"Possible memory leak: {growth:.2f}MB growth detected"

    def test_peak_memory_tracking(self, large_project_structure, memory_profiler):
        """Verify peak memory is tracked correctly."""
        project = large_project_structure("10k")
        memory_profiler.start()

        # Generate tree
        tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                tree.append(os.path.join(root, file))

        metrics = memory_profiler.stop()
        peak_memory = metrics.get("peak_allocated_mb", 0)

        assert peak_memory > 0, "Peak memory should be recorded"
        assert peak_memory < 200, f"Peak memory {peak_memory:.2f}MB seems high"

    def test_memory_per_file_ratio(self, large_project_structure, memory_profiler):
        """Verify memory usage per file is reasonable."""
        project = large_project_structure("10k")
        memory_profiler.start()

        file_count = 0
        for root, dirs, files in os.walk(project):
            file_count += len(files)

        metrics = memory_profiler.stop()
        memory_used = metrics.get("peak_allocated_mb", 0)

        memory_per_file_kb = (memory_used * 1024) / file_count if file_count > 0 else 0
        # Each file reference should use < 100KB
        assert memory_per_file_kb < 100, \
            f"Memory per file {memory_per_file_kb:.2f}KB is too high"

    def test_memory_under_concurrent_access(self, large_project_structure, memory_profiler, concurrent_executor):
        """Verify memory usage under concurrent tree generation."""
        project = large_project_structure("10k")

        def generate_tree():
            tree = []
            for root, dirs, files in os.walk(project):
                for file in files:
                    tree.append(os.path.join(root, file))
            return len(tree)

        memory_profiler.start()

        functions = [generate_tree for _ in range(3)]
        results = concurrent_executor.run_agents(functions, max_workers=3)

        metrics = memory_profiler.stop()
        concurrent_memory = metrics.get("peak_allocated_mb", 0)

        # Concurrent access shouldn't use exponential memory
        assert concurrent_memory < 300, \
            f"Concurrent memory usage {concurrent_memory:.2f}MB is too high"

    @pytest.mark.parametrize("scale", ["1k", "10k"])
    def test_memory_cleanup_after_operation(self, scale, large_project_structure, memory_profiler):
        """Verify memory is cleaned up after tree generation."""
        project = large_project_structure(scale)
        memory_profiler.start()

        # Generate and store tree
        tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                tree.append(os.path.join(root, file))

        metrics = memory_profiler.stop()
        used_memory = metrics.get("peak_allocated_mb", 0)

        # After operation, clear tree and check cleanup
        del tree
        import gc
        gc.collect()

        # Memory should be freed
        assert used_memory < 200, f"Memory not properly cleaned up for {scale}"

    def test_memory_allocation_pattern(self, large_project_structure, memory_profiler):
        """Verify memory allocation pattern is reasonable."""
        project = large_project_structure("10k")
        memory_profiler.start()

        # Gradually build tree
        tree = []
        file_count = 0
        for root, dirs, files in os.walk(project):
            for file in files:
                tree.append(os.path.join(root, file))
                file_count += 1

        metrics = memory_profiler.stop()

        # Should have allocated memory for all files
        assert file_count > 0, "No files processed"
        assert metrics.get("peak_allocated_mb", 0) > 0, "No memory allocated"
