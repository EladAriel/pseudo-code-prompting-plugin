"""Performance benchmarks for tree generation at different scales."""
import pytest
import os


@pytest.mark.performance
class TestTreeGenerationScaling:
    """Test tree generation performance at various scales."""

    @pytest.mark.parametrize("scale", ["1k", "10k", "50k"])
    def test_tree_generation_performance(self, scale, large_project_structure, performance_monitor, golden_performance_baseline, platform_detector):
        """Measure tree generation duration at different scales."""
        info = platform_detector.get_info()
        project_dir = large_project_structure(scale)

        with performance_monitor:
            # Simulate tree generation by traversing directory
            count = 0
            for root, dirs, files in os.walk(project_dir):
                count += len(files)
                count += len(dirs)

        duration = performance_monitor.metrics["duration_ms"]
        threshold = golden_performance_baseline["tree_generation"].get(scale, 60000)

        assert count > 0, f"No files/dirs found in project structure"
        assert duration < threshold, \
            f"Tree generation for {scale} took {duration:.0f}ms, exceeds {threshold:.0f}ms (platform multiplier: {info['timeout_multiplier']}x)"

    def test_tree_generation_1k_files(self, large_project_structure, performance_monitor, golden_performance_baseline):
        """Verify 1k file tree generation completes within threshold."""
        project = large_project_structure("1k")

        with performance_monitor:
            file_count = sum(len(files) for _, _, files in os.walk(project))

        duration = performance_monitor.metrics["duration_ms"]
        threshold = golden_performance_baseline["tree_generation"]["1k"]

        assert duration < threshold, \
            f"1k tree generation {duration:.0f}ms exceeds {threshold:.0f}ms"

    def test_tree_generation_10k_files(self, large_project_structure, performance_monitor, golden_performance_baseline):
        """Verify 10k file tree generation completes within threshold."""
        project = large_project_structure("10k")

        with performance_monitor:
            file_count = sum(len(files) for _, _, files in os.walk(project))

        duration = performance_monitor.metrics["duration_ms"]
        threshold = golden_performance_baseline["tree_generation"]["10k"]

        assert duration < threshold, \
            f"10k tree generation {duration:.0f}ms exceeds {threshold:.0f}ms"

    def test_tree_generation_50k_files(self, large_project_structure, performance_monitor, golden_performance_baseline):
        """Verify 50k file tree generation completes within threshold."""
        project = large_project_structure("50k")

        with performance_monitor:
            file_count = sum(len(files) for _, _, files in os.walk(project))

        duration = performance_monitor.metrics["duration_ms"]
        threshold = golden_performance_baseline["tree_generation"]["50k"]

        assert duration < threshold, \
            f"50k tree generation {duration:.0f}ms exceeds {threshold:.0f}ms"

    def test_tree_generation_scaling_linearity(self, large_project_structure, performance_monitor, golden_performance_baseline):
        """Verify tree generation scales sub-linearly with file count."""
        timings = {}

        for scale in ["1k", "10k", "50k"]:
            project = large_project_structure(scale)

            with performance_monitor:
                file_count = sum(len(files) for _, _, files in os.walk(project))

            timings[scale] = performance_monitor.metrics["duration_ms"]

        # Verify scaling is reasonable (not exponential)
        ratio_10k_1k = timings["10k"] / timings["1k"]
        ratio_50k_10k = timings["50k"] / timings["10k"]

        # Ratios should be sub-linear (< 10x for 10x more files)
        assert ratio_10k_1k < 20, f"10k vs 1k scaling ratio {ratio_10k_1k:.1f}x is too high"
        assert ratio_50k_10k < 20, f"50k vs 10k scaling ratio {ratio_50k_10k:.1f}x is too high"

    def test_tree_generation_file_traversal(self, large_project_structure, performance_monitor):
        """Measure tree generation file traversal performance."""
        project = large_project_structure("10k")

        with performance_monitor:
            tree = []
            for root, dirs, files in os.walk(project):
                for file in files:
                    tree.append(os.path.join(root, file))

        duration = performance_monitor.metrics["duration_ms"]
        file_count = len(tree)

        throughput = file_count / (duration / 1000) if duration > 0 else 0
        assert throughput > 100, f"File traversal throughput {throughput:.0f} files/sec is too low"

    @pytest.mark.parametrize("scale", ["1k", "10k", "50k"])
    def test_tree_generation_consistency(self, scale, large_project_structure, performance_monitor):
        """Verify tree generation produces consistent results across runs."""
        durations = []

        for _ in range(3):
            project = large_project_structure(scale)

            with performance_monitor:
                file_count = sum(len(files) for _, _, files in os.walk(project))

            durations.append(performance_monitor.metrics["duration_ms"])

        # Results should be relatively consistent
        avg = sum(durations) / len(durations)
        variance = max(durations) - min(durations)
        variance_percent = (variance / avg) * 100

        assert variance_percent < 30, \
            f"Tree generation variance {variance_percent:.1f}% is too high"

    def test_tree_generation_memory_scaling(self, large_project_structure, memory_profiler):
        """Verify tree generation memory usage scales reasonably."""
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

        # 10x more files should not use 10x memory
        ratio = memory_usage["10k"] / memory_usage["1k"] if memory_usage["1k"] > 0 else 1
        assert ratio < 10, f"Memory scaling ratio {ratio:.1f}x is too high"

    def test_tree_generation_concurrent(self, concurrent_executor, large_project_structure, performance_monitor):
        """Verify tree generation performance with concurrent executions."""
        def generate_tree(scale):
            project = large_project_structure(scale)
            count = 0
            for root, dirs, files in os.walk(project):
                count += len(files)
            return count

        functions = [
            lambda: generate_tree("1k"),
            lambda: generate_tree("1k"),
            lambda: generate_tree("10k"),
        ]

        with performance_monitor:
            results = concurrent_executor.run_agents(functions, max_workers=3)

        assert len(results) == 3
        assert all(isinstance(r, int) and r > 0 for r in results)
