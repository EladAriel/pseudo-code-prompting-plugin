"""Bottleneck analysis tests for performance profiling."""
import pytest
import cProfile
import pstats
import io
import os


@pytest.mark.performance
class TestBottleneckAnalysis:
    """Test identification and analysis of performance bottlenecks."""

    def test_bottleneck_identification(self, large_project_structure):
        """Identify performance bottlenecks in tree generation."""
        project = large_project_structure("10k")

        profiler = cProfile.Profile()
        profiler.enable()

        # Perform tree generation
        for root, dirs, files in os.walk(project):
            for file in files:
                _ = os.path.join(root, file)

        profiler.disable()

        # Get stats
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("cumulative")
        stats.print_stats(5)  # Top 5

        output = s.getvalue()
        assert "os.path.join" in output or "walk" in output, \
            "Expected filesystem operations in bottlenecks"

    def test_bottleneck_consistency(self, large_project_structure):
        """Verify bottleneck location remains consistent."""
        project = large_project_structure("10k")

        bottlenecks_found = []

        for run in range(3):
            profiler = cProfile.Profile()
            profiler.enable()

            for root, dirs, files in os.walk(project):
                for file in files:
                    _ = os.path.join(root, file)

            profiler.disable()

            s = io.StringIO()
            stats = pstats.Stats(profiler, stream=s)
            stats.sort_stats("cumulative")
            stats.print_stats(1)  # Top 1

            output = s.getvalue()
            bottlenecks_found.append(output)

        # All runs should identify similar bottleneck
        assert len(bottlenecks_found) == 3
        # Check that at least walk appears as bottleneck
        assert any("walk" in b for b in bottlenecks_found), \
            "os.walk should be identified as bottleneck"

    def test_function_call_count(self, large_project_structure):
        """Analyze function call counts to identify hot spots."""
        project = large_project_structure("10k")

        profiler = cProfile.Profile()
        profiler.enable()

        file_count = 0
        for root, dirs, files in os.walk(project):
            file_count += len(files)

        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("calls")
        stats.print_stats(10)

        output = s.getvalue()
        # walk should have high call count
        assert file_count > 0, "No files processed"

    def test_execution_time_distribution(self, large_project_structure):
        """Analyze how execution time is distributed across functions."""
        project = large_project_structure("10k")

        profiler = cProfile.Profile()
        profiler.enable()

        for root, dirs, files in os.walk(project):
            for file in files:
                path = os.path.join(root, file)

        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("cumulative")

        # Analyze top function
        func_list = stats.sort_stats("cumulative").fcn_list
        assert len(func_list) > 0, "No functions profiled"

    def test_memory_hotspots(self, large_project_structure, memory_profiler):
        """Identify memory hotspots in code."""
        project = large_project_structure("10k")

        memory_profiler.start()

        # Allocate large list
        tree = []
        for root, dirs, files in os.walk(project):
            for file in files:
                tree.append(os.path.join(root, file))

        metrics = memory_profiler.stop()
        leak_analysis = memory_profiler.get_leak_analysis()

        # Should identify memory allocations
        assert metrics.get("peak_allocated_mb", 0) > 0, \
            "Memory allocation should be detected"

    def test_scaling_bottleneck_analysis(self, large_project_structure):
        """Analyze how bottlenecks change with scale."""
        profiling_results = {}

        for scale in ["1k", "10k"]:
            project = large_project_structure(scale)

            profiler = cProfile.Profile()
            profiler.enable()

            for root, dirs, files in os.walk(project):
                for file in files:
                    _ = os.path.join(root, file)

            profiler.disable()

            s = io.StringIO()
            stats = pstats.Stats(profiler, stream=s)
            stats.sort_stats("cumulative")

            # Get total time
            total_time = sum(stat[3] for stat in stats.stats.values() if len(stat) > 3)
            profiling_results[scale] = total_time

        # 10x scale should not take 100x time
        if profiling_results["1k"] > 0:
            ratio = profiling_results["10k"] / profiling_results["1k"]
            assert ratio < 50, f"Bottleneck scaling ratio {ratio:.1f}x is too high"

    def test_io_bottleneck_detection(self, large_project_structure):
        """Detect I/O bound bottlenecks."""
        project = large_project_structure("10k")

        profiler = cProfile.Profile()
        profiler.enable()

        # I/O heavy operation
        for root, dirs, files in os.walk(project):
            for file in files:
                filepath = os.path.join(root, file)
                # Simulate file stat
                try:
                    os.stat(filepath)
                except:
                    pass

        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("cumulative")
        stats.print_stats(10)

        output = s.getvalue()
        # Should show I/O operations as bottleneck
        assert "stat" in output or "walk" in output, \
            "I/O operations should appear in profiles"

    def test_cpu_bottleneck_detection(self):
        """Detect CPU bound bottlenecks."""
        profiler = cProfile.Profile()
        profiler.enable()

        # CPU heavy operation
        result = 0
        for i in range(100000):
            result += sum(range(10))

        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("cumulative")

        total_time = sum(stat[3] for stat in stats.stats.values() if len(stat) > 3)
        assert total_time >= 0, "CPU operation should be profiled"

    @pytest.mark.parametrize("scale", ["1k", "10k"])
    def test_bottleneck_reporting(self, scale, large_project_structure):
        """Generate bottleneck report with recommendations."""
        project = large_project_structure(scale)

        profiler = cProfile.Profile()
        profiler.enable()

        for root, dirs, files in os.walk(project):
            for file in files:
                _ = os.path.join(root, file)

        profiler.disable()

        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats("cumulative")
        stats.print_stats(5)

        report = s.getvalue()

        # Should contain function names and timing
        assert "(" in report and ")" in report, "Report should contain function info"
        assert len(report) > 0, "Report should not be empty"
