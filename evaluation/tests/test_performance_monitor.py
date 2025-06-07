"""
Tests for the performance monitoring module.

Tests performance monitoring accuracy and context manager functionality.
"""

import pytest
import time
import threading
from unittest.mock import patch, MagicMock

from evaluation.performance_monitor import (
    PerformanceMonitor, 
    PerformanceSnapshot, 
    PerformanceMetrics,
    monitor_performance
)


class TestPerformanceSnapshot:
    """Test cases for PerformanceSnapshot."""
    
    def test_snapshot_creation(self):
        """Test creating a performance snapshot."""
        from datetime import datetime
        
        timestamp = datetime.now()
        snapshot = PerformanceSnapshot(
            timestamp=timestamp,
            cpu_percent=50.0,
            memory_mb=100.0,
            memory_percent=25.0
        )
        
        assert snapshot.timestamp == timestamp
        assert snapshot.cpu_percent == 50.0
        assert snapshot.memory_mb == 100.0
        assert snapshot.memory_percent == 25.0
        assert snapshot.disk_io_read_mb == 0.0
        assert snapshot.disk_io_write_mb == 0.0


class TestPerformanceMetrics:
    """Test cases for PerformanceMetrics."""
    
    def test_metrics_creation(self):
        """Test creating performance metrics."""
        metrics = PerformanceMetrics(
            execution_time=2.5,
            peak_memory_mb=150.0,
            average_memory_mb=120.0,
            peak_cpu_percent=80.0,
            average_cpu_percent=60.0
        )
        
        assert metrics.execution_time == 2.5
        assert metrics.peak_memory_mb == 150.0
        assert metrics.average_memory_mb == 120.0
        assert metrics.peak_cpu_percent == 80.0
        assert metrics.average_cpu_percent == 60.0
        assert len(metrics.snapshots) == 0
        assert len(metrics.metadata) == 0


class TestPerformanceMonitor:
    """Test cases for PerformanceMonitor."""
    
    def test_monitor_initialization(self):
        """Test PerformanceMonitor initialization."""
        monitor = PerformanceMonitor(
            sampling_interval=0.1,
            include_disk_io=True,
            include_network_io=True
        )
        
        assert monitor.sampling_interval == 0.1
        assert monitor.include_disk_io is True
        assert monitor.include_network_io is True
        assert monitor._monitoring is False
        assert monitor._monitor_thread is None
        assert len(monitor._snapshots) == 0
    
    def test_context_manager(self):
        """Test PerformanceMonitor as context manager."""
        with PerformanceMonitor(sampling_interval=0.05) as monitor:
            assert monitor._monitoring is True
            time.sleep(0.2)  # Let it collect some samples
        
        assert monitor._monitoring is False
        metrics = monitor.get_metrics()
        assert metrics.execution_time > 0.1
        assert len(metrics.snapshots) > 0
    
    def test_manual_start_stop(self):
        """Test manual start and stop of monitoring."""
        monitor = PerformanceMonitor(sampling_interval=0.05)
        
        assert monitor._monitoring is False
        
        monitor.start_monitoring()
        assert monitor._monitoring is True
        
        time.sleep(0.2)
        
        monitor.stop_monitoring()
        assert monitor._monitoring is False
        
        metrics = monitor.get_metrics()
        assert metrics.execution_time > 0.1
        assert len(metrics.snapshots) > 0
    
    def test_get_metrics_no_monitoring(self):
        """Test getting metrics without monitoring."""
        monitor = PerformanceMonitor()
        metrics = monitor.get_metrics()
        
        assert metrics.execution_time == 0.0
        assert metrics.peak_memory_mb == 0.0
        assert metrics.average_memory_mb == 0.0
        assert metrics.peak_cpu_percent == 0.0
        assert metrics.average_cpu_percent == 0.0
    
    @patch('evaluation.performance_monitor.psutil.Process')
    def test_capture_snapshot_mock(self, mock_process_class):
        """Test snapshot capture with mocked psutil."""
        # Mock process instance
        mock_process = MagicMock()
        mock_process.cpu_percent.return_value = 50.0
        mock_process.memory_info.return_value = MagicMock(rss=100 * 1024 * 1024)  # 100 MB
        mock_process.memory_percent.return_value = 25.0
        mock_process_class.return_value = mock_process
        
        monitor = PerformanceMonitor(sampling_interval=0.1)
        snapshot = monitor._capture_snapshot()
        
        assert snapshot.cpu_percent == 50.0
        assert snapshot.memory_mb == 100.0
        assert snapshot.memory_percent == 25.0
    
    def test_export_json(self):
        """Test JSON export functionality."""
        monitor = PerformanceMonitor(sampling_interval=0.05)
        
        with monitor:
            time.sleep(0.1)
        
        json_data = monitor.export_data("json")
        assert isinstance(json_data, str)
        assert "summary" in json_data
        assert "snapshots" in json_data
        assert "metadata" in json_data
    
    def test_export_csv(self):
        """Test CSV export functionality."""
        monitor = PerformanceMonitor(sampling_interval=0.05)
        
        with monitor:
            time.sleep(0.1)
        
        csv_data = monitor.export_data("csv")
        assert isinstance(csv_data, str)
        assert "timestamp,cpu_percent,memory_mb" in csv_data
        lines = csv_data.split('\n')
        assert len(lines) > 1  # Header + at least one data line
    
    def test_export_invalid_format(self):
        """Test export with invalid format."""
        monitor = PerformanceMonitor()
        
        with pytest.raises(ValueError, match="Unsupported export format"):
            monitor.export_data("invalid_format")


class TestMonitorPerformanceFunction:
    """Test cases for the monitor_performance convenience function."""
    
    def test_monitor_performance_context(self):
        """Test monitor_performance context manager function."""
        with monitor_performance(sampling_interval=0.05) as monitor:
            assert isinstance(monitor, PerformanceMonitor)
            assert monitor._monitoring is True
            time.sleep(0.1)
        
        assert monitor._monitoring is False
        metrics = monitor.get_metrics()
        assert metrics.execution_time > 0.05
    
    def test_monitor_performance_with_options(self):
        """Test monitor_performance with various options."""
        with monitor_performance(
            sampling_interval=0.02,
            include_disk_io=True,
            include_network_io=True
        ) as monitor:
            assert monitor.sampling_interval == 0.02
            assert monitor.include_disk_io is True
            assert monitor.include_network_io is True
            time.sleep(0.1)
        
        metrics = monitor.get_metrics()
        assert metrics.execution_time > 0.05


class TestPerformanceMonitorIntegration:
    """Integration tests for performance monitoring."""
    
    def test_cpu_intensive_task(self):
        """Test monitoring a CPU-intensive task."""
        def cpu_intensive_task():
            # Simple CPU-intensive operation
            total = 0
            for i in range(100000):
                total += i * i
            return total
        
        with monitor_performance(sampling_interval=0.01) as monitor:
            result = cpu_intensive_task()
        
        metrics = monitor.get_metrics()
        assert result > 0
        assert metrics.execution_time > 0
        assert metrics.peak_cpu_percent >= 0  # Should capture some CPU usage
        assert len(metrics.snapshots) > 0
    
    def test_memory_allocation_task(self):
        """Test monitoring a memory allocation task."""
        def memory_allocation_task():
            # Allocate some memory
            data = []
            for i in range(10000):
                data.append([0] * 100)
            return len(data)
        
        with monitor_performance(sampling_interval=0.01) as monitor:
            result = memory_allocation_task()
        
        metrics = monitor.get_metrics()
        assert result == 10000
        assert metrics.execution_time > 0
        assert metrics.peak_memory_mb >= 0
        assert len(metrics.snapshots) > 0
    
    def test_concurrent_monitoring(self):
        """Test that multiple monitors can run concurrently."""
        results = []
        
        def monitored_task(task_id):
            with monitor_performance(sampling_interval=0.01) as monitor:
                time.sleep(0.1)
                results.append((task_id, monitor.get_metrics()))
        
        # Run multiple tasks concurrently
        threads = []
        for i in range(3):
            thread = threading.Thread(target=monitored_task, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        assert len(results) == 3
        for task_id, metrics in results:
            assert metrics.execution_time > 0.05
            assert len(metrics.snapshots) > 0


if __name__ == "__main__":
    pytest.main([__file__])
