"""
Base evaluation framework for AI agent frameworks comparison.

This module provides the abstract base classes and data models for evaluating
AI agent frameworks across different use cases and metrics.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field
from datetime import datetime
import time
import psutil
import os


class UseCaseResult(BaseModel):
    """
    Standardized result structure for use case execution across all frameworks.
    
    This model ensures consistent data collection and comparison across
    different AI agent frameworks.
    """
    framework_name: str = Field(..., description="Name of the AI framework used")
    use_case_name: str = Field(..., description="Name of the executed use case")
    execution_time: float = Field(..., description="Use case execution time in seconds")
    memory_usage: float = Field(..., description="Peak memory usage in MB")
    cpu_usage: float = Field(..., description="Average CPU usage percentage")
    api_costs: Dict[str, float] = Field(default_factory=dict, description="API costs by provider")
    quality_metrics: Dict[str, float] = Field(default_factory=dict, description="Use case-specific quality scores")
    raw_output: Any = Field(..., description="Raw output from the framework")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional execution metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Execution timestamp")
    success: bool = Field(default=True, description="Whether use case completed successfully")
    error_message: Optional[str] = Field(default=None, description="Error message if use case failed")


class BaseEvaluator(ABC):
    """
    Abstract base class for framework evaluation.
    
    This class defines the standard interface that all framework evaluators
    must implement to ensure consistent evaluation across different AI frameworks.
    """
    
    def __init__(self, framework_name: str):
        """
        Initialize the evaluator for a specific framework.
        
        Args:
            framework_name: Name of the AI framework being evaluated
        """
        self.framework_name = framework_name
        self.current_process = psutil.Process(os.getpid())
    
    @abstractmethod
    def evaluate_response_quality(self, expected: Any, actual: Any) -> Dict[str, float]:
        """
        Evaluate the quality of a framework's response against expected output.
        
        Args:
            expected: Expected output or ground truth
            actual: Actual output from the framework
            
        Returns:
            Dictionary of quality metrics with scores between 0.0 and 1.0
        """
        pass
    
    @abstractmethod
    def measure_performance(self, execution_func: Callable) -> Dict[str, float]:
        """
        Measure performance metrics during use case execution.

        Args:
            execution_func: Function to execute and measure

        Returns:
            Dictionary of performance metrics
        """
        pass
    
    def execute_with_monitoring(self, use_case_name: str, execution_func: Callable,
                              input_data: Any, expected_output: Any = None) -> UseCaseResult:
        """
        Execute a use case with comprehensive monitoring and evaluation.

        Args:
            use_case_name: Name of the use case being executed
            execution_func: Function that executes the use case
            input_data: Input data for the use case
            expected_output: Expected output for quality evaluation (optional)

        Returns:
            UseCaseResult with comprehensive metrics and evaluation
        """
        # Initialize monitoring
        start_time = time.time()
        initial_memory = self.current_process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent_start = self.current_process.cpu_percent()
        
        try:
            # Execute the use case
            raw_output = execution_func(input_data)
            
            # Calculate execution metrics
            execution_time = time.time() - start_time
            final_memory = self.current_process.memory_info().rss / 1024 / 1024  # MB
            memory_usage = final_memory - initial_memory
            cpu_usage = self.current_process.cpu_percent()
            
            # Evaluate quality if expected output is provided
            quality_metrics = {}
            if expected_output is not None:
                quality_metrics = self.evaluate_response_quality(expected_output, raw_output)
            
            # Get performance metrics
            performance_metrics = self.measure_performance(execution_func)
            
            return UseCaseResult(
                framework_name=self.framework_name,
                use_case_name=use_case_name,
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                api_costs={},  # To be populated by framework-specific implementations
                quality_metrics=quality_metrics,
                raw_output=raw_output,
                metadata={
                    "input_data_size": len(str(input_data)) if input_data else 0,
                    "output_data_size": len(str(raw_output)) if raw_output else 0,
                    **performance_metrics
                },
                success=True
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return UseCaseResult(
                framework_name=self.framework_name,
                use_case_name=use_case_name,
                execution_time=execution_time,
                memory_usage=0.0,
                cpu_usage=0.0,
                api_costs={},
                quality_metrics={},
                raw_output=None,
                metadata={"error_details": str(e)},
                success=False,
                error_message=str(e)
            )
    
    def calculate_aggregate_metrics(self, results: List[UseCaseResult]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics across multiple use case results.

        Args:
            results: List of UseCaseResult objects

        Returns:
            Dictionary of aggregate metrics
        """
        if not results:
            return {}
        
        successful_results = [r for r in results if r.success]
        
        if not successful_results:
            return {"success_rate": 0.0, "total_use_cases": len(results)}
        
        return {
            "success_rate": len(successful_results) / len(results),
            "total_use_cases": len(results),
            "average_execution_time": sum(r.execution_time for r in successful_results) / len(successful_results),
            "average_memory_usage": sum(r.memory_usage for r in successful_results) / len(successful_results),
            "average_cpu_usage": sum(r.cpu_usage for r in successful_results) / len(successful_results),
            "total_api_costs": sum(sum(r.api_costs.values()) for r in successful_results),
            "average_quality_scores": self._calculate_average_quality_scores(successful_results)
        }
    
    def _calculate_average_quality_scores(self, results: List[UseCaseResult]) -> Dict[str, float]:
        """Calculate average quality scores across results."""
        if not results:
            return {}
        
        all_metrics = set()
        for result in results:
            all_metrics.update(result.quality_metrics.keys())
        
        avg_scores = {}
        for metric in all_metrics:
            scores = [r.quality_metrics.get(metric, 0.0) for r in results if metric in r.quality_metrics]
            if scores:
                avg_scores[metric] = sum(scores) / len(scores)
        
        return avg_scores
