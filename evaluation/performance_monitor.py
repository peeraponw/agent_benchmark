"""
Performance monitoring utilities for AI agent framework evaluation.

This module provides comprehensive performance monitoring capabilities including
CPU usage, memory consumption, and execution time tracking with context manager support.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, List, Callable
from contextlib import contextmanager
from datetime import datetime
import json
try:
    from pydantic import BaseModel, Field, validator
except ImportError:
    # Fallback for older Pydantic versions
    from pydantic import BaseModel, Field
    from pydantic import validator


class PerformanceSnapshot(BaseModel):
    """
    A snapshot of system performance metrics at a specific point in time.
    """
    timestamp: datetime
    cpu_percent: float = Field(..., ge=0.0, le=100.0, description="CPU usage percentage")
    memory_mb: float = Field(..., ge=0.0, description="Memory usage in MB")
    memory_percent: float = Field(..., ge=0.0, le=100.0, description="Memory usage percentage")
    disk_io_read_mb: float = Field(default=0.0, ge=0.0, description="Disk I/O read in MB")
    disk_io_write_mb: float = Field(default=0.0, ge=0.0, description="Disk I/O write in MB")
    network_io_sent_mb: float = Field(default=0.0, ge=0.0, description="Network I/O sent in MB")
    network_io_recv_mb: float = Field(default=0.0, ge=0.0, description="Network I/O received in MB")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PerformanceMetrics(BaseModel):
    """
    Aggregated performance metrics over a monitoring period.
    """
    execution_time: float = Field(..., ge=0.0, description="Total execution time in seconds")
    peak_memory_mb: float = Field(..., ge=0.0, description="Peak memory usage in MB")
    average_memory_mb: float = Field(..., ge=0.0, description="Average memory usage in MB")
    peak_cpu_percent: float = Field(..., ge=0.0, le=100.0, description="Peak CPU usage percentage")
    average_cpu_percent: float = Field(..., ge=0.0, le=100.0, description="Average CPU usage percentage")
    total_disk_read_mb: float = Field(default=0.0, ge=0.0, description="Total disk read in MB")
    total_disk_write_mb: float = Field(default=0.0, ge=0.0, description="Total disk write in MB")
    total_network_sent_mb: float = Field(default=0.0, ge=0.0, description="Total network sent in MB")
    total_network_recv_mb: float = Field(default=0.0, ge=0.0, description="Total network received in MB")
    snapshots: List[PerformanceSnapshot] = Field(default_factory=list, description="Individual performance snapshots")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @validator('average_memory_mb')
    def validate_average_memory(cls, v, values):
        """Ensure average memory doesn't exceed peak memory."""
        if 'peak_memory_mb' in values and v > values['peak_memory_mb']:
            raise ValueError('Average memory cannot exceed peak memory')
        return v

    @validator('average_cpu_percent')
    def validate_average_cpu(cls, v, values):
        """Ensure average CPU doesn't exceed peak CPU."""
        if 'peak_cpu_percent' in values and v > values['peak_cpu_percent']:
            raise ValueError('Average CPU cannot exceed peak CPU')
        return v

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PerformanceMonitor:
    """
    Context manager for monitoring system performance during code execution.
    
    Provides real-time tracking of CPU usage, memory consumption, disk I/O,
    and network I/O with configurable sampling intervals.
    """
    
    def __init__(self, 
                 sampling_interval: float = 0.1,
                 include_disk_io: bool = False,
                 include_network_io: bool = False,
                 process_id: Optional[int] = None):
        """
        Initialize the performance monitor.
        
        Args:
            sampling_interval: Time between performance samples in seconds
            include_disk_io: Whether to monitor disk I/O metrics
            include_network_io: Whether to monitor network I/O metrics
            process_id: Specific process ID to monitor (defaults to current process)
        """
        self.sampling_interval = sampling_interval
        self.include_disk_io = include_disk_io
        self.include_network_io = include_network_io
        
        # Initialize process monitoring
        self.process = psutil.Process(process_id) if process_id else psutil.Process()
        
        # Monitoring state
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._snapshots: List[PerformanceSnapshot] = []
        self._start_time: Optional[float] = None
        self._initial_disk_io: Optional[psutil._common.pio] = None
        self._initial_network_io: Optional[psutil._common.snetio] = None
    
    def __enter__(self) -> 'PerformanceMonitor':
        """Start monitoring when entering context."""
        self.start_monitoring()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop monitoring when exiting context."""
        self.stop_monitoring()
    
    def start_monitoring(self) -> None:
        """Start performance monitoring in a background thread."""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._snapshots.clear()
        self._start_time = time.time()
        
        # Capture initial I/O states
        if self.include_disk_io:
            try:
                self._initial_disk_io = self.process.io_counters()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self._initial_disk_io = None
        
        if self.include_network_io:
            try:
                self._initial_network_io = psutil.net_io_counters()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self._initial_network_io = None
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        if not self._monitoring:
            return
        
        self._monitoring = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop that runs in background thread."""
        while self._monitoring:
            try:
                snapshot = self._capture_snapshot()
                self._snapshots.append(snapshot)
                time.sleep(self.sampling_interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process may have ended or access denied
                break
            except Exception:
                # Continue monitoring despite errors
                continue
    
    def _capture_snapshot(self) -> PerformanceSnapshot:
        """Capture a single performance snapshot."""
        timestamp = datetime.now()
        
        # CPU and memory metrics
        try:
            cpu_percent = self.process.cpu_percent()
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024  # Convert to MB
            memory_percent = self.process.memory_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            cpu_percent = 0.0
            memory_mb = 0.0
            memory_percent = 0.0
        
        # Disk I/O metrics
        disk_read_mb = 0.0
        disk_write_mb = 0.0
        if self.include_disk_io and self._initial_disk_io:
            try:
                current_io = self.process.io_counters()
                disk_read_mb = (current_io.read_bytes - self._initial_disk_io.read_bytes) / 1024 / 1024
                disk_write_mb = (current_io.write_bytes - self._initial_disk_io.write_bytes) / 1024 / 1024
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Network I/O metrics
        network_sent_mb = 0.0
        network_recv_mb = 0.0
        if self.include_network_io and self._initial_network_io:
            try:
                current_net = psutil.net_io_counters()
                network_sent_mb = (current_net.bytes_sent - self._initial_network_io.bytes_sent) / 1024 / 1024
                network_recv_mb = (current_net.bytes_recv - self._initial_network_io.bytes_recv) / 1024 / 1024
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return PerformanceSnapshot(
            timestamp=timestamp,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
            memory_percent=memory_percent,
            disk_io_read_mb=disk_read_mb,
            disk_io_write_mb=disk_write_mb,
            network_io_sent_mb=network_sent_mb,
            network_io_recv_mb=network_recv_mb
        )
    
    def get_metrics(self) -> PerformanceMetrics:
        """
        Calculate and return aggregated performance metrics.
        
        Returns:
            PerformanceMetrics object with aggregated statistics
        """
        if not self._snapshots or self._start_time is None:
            return PerformanceMetrics(
                execution_time=0.0,
                peak_memory_mb=0.0,
                average_memory_mb=0.0,
                peak_cpu_percent=0.0,
                average_cpu_percent=0.0
            )
        
        execution_time = time.time() - self._start_time
        
        # Calculate memory metrics
        memory_values = [s.memory_mb for s in self._snapshots]
        peak_memory_mb = max(memory_values) if memory_values else 0.0
        average_memory_mb = sum(memory_values) / len(memory_values) if memory_values else 0.0
        
        # Calculate CPU metrics
        cpu_values = [s.cpu_percent for s in self._snapshots]
        peak_cpu_percent = max(cpu_values) if cpu_values else 0.0
        average_cpu_percent = sum(cpu_values) / len(cpu_values) if cpu_values else 0.0
        
        # Calculate I/O metrics
        total_disk_read_mb = max([s.disk_io_read_mb for s in self._snapshots], default=0.0)
        total_disk_write_mb = max([s.disk_io_write_mb for s in self._snapshots], default=0.0)
        total_network_sent_mb = max([s.network_io_sent_mb for s in self._snapshots], default=0.0)
        total_network_recv_mb = max([s.network_io_recv_mb for s in self._snapshots], default=0.0)
        
        return PerformanceMetrics(
            execution_time=execution_time,
            peak_memory_mb=peak_memory_mb,
            average_memory_mb=average_memory_mb,
            peak_cpu_percent=peak_cpu_percent,
            average_cpu_percent=average_cpu_percent,
            total_disk_read_mb=total_disk_read_mb,
            total_disk_write_mb=total_disk_write_mb,
            total_network_sent_mb=total_network_sent_mb,
            total_network_recv_mb=total_network_recv_mb,
            snapshots=self._snapshots.copy(),
            metadata={
                "sampling_interval": self.sampling_interval,
                "total_samples": len(self._snapshots),
                "process_id": self.process.pid
            }
        )
    
    def export_data(self, format_type: str = "json") -> str:
        """
        Export performance data in specified format.
        
        Args:
            format_type: Export format ("json" or "csv")
            
        Returns:
            Formatted performance data as string
        """
        metrics = self.get_metrics()
        
        if format_type.lower() == "json":
            return self._export_json(metrics)
        elif format_type.lower() == "csv":
            return self._export_csv(metrics)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _export_json(self, metrics: PerformanceMetrics) -> str:
        """Export metrics as JSON string."""
        return metrics.json(indent=2)
    
    def _export_csv(self, metrics: PerformanceMetrics) -> str:
        """Export metrics as CSV string."""
        lines = [
            "timestamp,cpu_percent,memory_mb,memory_percent,disk_io_read_mb,disk_io_write_mb,network_io_sent_mb,network_io_recv_mb"
        ]

        for snapshot in metrics.snapshots:
            lines.append(
                f"{snapshot.timestamp.isoformat()},"
                f"{snapshot.cpu_percent},"
                f"{snapshot.memory_mb},"
                f"{snapshot.memory_percent},"
                f"{snapshot.disk_io_read_mb},"
                f"{snapshot.disk_io_write_mb},"
                f"{snapshot.network_io_sent_mb},"
                f"{snapshot.network_io_recv_mb}"
            )

        return "\n".join(lines)


@contextmanager
def monitor_performance(sampling_interval: float = 0.1,
                       include_disk_io: bool = False,
                       include_network_io: bool = False):
    """
    Convenience context manager for performance monitoring.
    
    Args:
        sampling_interval: Time between performance samples in seconds
        include_disk_io: Whether to monitor disk I/O metrics
        include_network_io: Whether to monitor network I/O metrics
        
    Yields:
        PerformanceMonitor instance
        
    Example:
        with monitor_performance(sampling_interval=0.05) as monitor:
            # Your code here
            result = some_expensive_operation()
        
        metrics = monitor.get_metrics()
        print(f"Execution time: {metrics.execution_time:.2f}s")
        print(f"Peak memory: {metrics.peak_memory_mb:.2f}MB")
    """
    monitor = PerformanceMonitor(
        sampling_interval=sampling_interval,
        include_disk_io=include_disk_io,
        include_network_io=include_network_io
    )
    
    with monitor:
        yield monitor
