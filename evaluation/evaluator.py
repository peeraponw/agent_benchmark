"""
Main evaluation orchestrator for AI agent framework comparison.

This module provides the central orchestration for running evaluations across
different frameworks, aggregating results, and generating comparison reports.
"""

import json
import csv
import time
from typing import Dict, Any, List, Optional, Callable, Union
from pathlib import Path
from datetime import datetime
import traceback

from .base_evaluator import BaseEvaluator, UseCaseResult
from .performance_monitor import PerformanceMonitor
from .cost_tracker import APIUsageTracker, APIProvider
from .metrics.qa_metrics import QAMetrics
from .metrics.rag_metrics import RAGMetrics
from .metrics.search_metrics import SearchMetrics


class FrameworkEvaluator:
    """
    Main orchestrator for evaluating AI agent frameworks.
    
    Coordinates performance monitoring, cost tracking, quality metrics,
    and result aggregation across multiple frameworks and use cases.
    """
    
    def __init__(self, 
                 output_dir: str = "evaluation_results",
                 enable_performance_monitoring: bool = True,
                 enable_cost_tracking: bool = True):
        """
        Initialize the framework evaluator.
        
        Args:
            output_dir: Directory to store evaluation results
            enable_performance_monitoring: Whether to monitor performance metrics
            enable_cost_tracking: Whether to track API costs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.enable_performance_monitoring = enable_performance_monitoring
        self.enable_cost_tracking = enable_cost_tracking
        
        # Initialize tracking systems
        self.cost_tracker = APIUsageTracker() if enable_cost_tracking else None
        
        # Initialize metric suites
        self.qa_metrics = QAMetrics()
        self.rag_metrics = RAGMetrics()
        self.search_metrics = SearchMetrics()
        
        # Store evaluation results
        self.evaluation_results: List[UseCaseResult] = []
        self.framework_summaries: Dict[str, Dict[str, Any]] = {}
    
    def evaluate_single_task(self,
                            framework_name: str,
                            use_case_name: str,
                            execution_func: Callable,
                            input_data: Any,
                            expected_output: Any = None,
                            use_case_type: str = "general",
                            **kwargs) -> UseCaseResult:
        """
        Evaluate a single task execution.
        
        Args:
            framework_name: Name of the framework being evaluated
            use_case_name: Name of the use case
            execution_func: Function that executes the use case
            input_data: Input data for the use case
            expected_output: Expected output for quality evaluation
            use_case_type: Type of use case ("qa", "rag", "search", "general")
            **kwargs: Additional parameters for evaluation
            
        Returns:
            UseCaseResult with comprehensive evaluation metrics
        """
        print(f"Evaluating {framework_name} - {use_case_name}")
        
        # Initialize performance monitoring
        performance_monitor = None
        if self.enable_performance_monitoring:
            performance_monitor = PerformanceMonitor(
                sampling_interval=0.1,
                include_disk_io=True,
                include_network_io=True
            )
        
        start_time = time.time()
        
        try:
            # Start monitoring
            if performance_monitor:
                performance_monitor.start_monitoring()
            
            # Execute the use case
            raw_output = execution_func(input_data)
            
            # Stop monitoring
            if performance_monitor:
                performance_monitor.stop_monitoring()
                perf_metrics = performance_monitor.get_metrics()
            else:
                perf_metrics = None
            
            execution_time = time.time() - start_time
            
            # Calculate quality metrics based on use case type
            quality_metrics = self._calculate_quality_metrics(
                use_case_type, expected_output, raw_output, input_data, **kwargs
            )
            
            # Get API costs if tracking is enabled
            api_costs = {}
            if self.enable_cost_tracking and self.cost_tracker:
                # Get costs since start of evaluation
                api_costs = self._get_recent_api_costs(start_time)
            
            # Create result
            result = UseCaseResult(
                framework_name=framework_name,
                use_case_name=use_case_name,
                execution_time=execution_time,
                memory_usage=perf_metrics.peak_memory_mb if perf_metrics else 0.0,
                cpu_usage=perf_metrics.average_cpu_percent if perf_metrics else 0.0,
                api_costs=api_costs,
                quality_metrics=quality_metrics,
                raw_output=raw_output,
                metadata={
                    "use_case_type": use_case_type,
                    "input_data_size": len(str(input_data)) if input_data else 0,
                    "output_data_size": len(str(raw_output)) if raw_output else 0,
                    "performance_details": perf_metrics.__dict__ if perf_metrics else {},
                    **kwargs
                },
                success=True
            )
            
            self.evaluation_results.append(result)
            print(f"✓ Completed {framework_name} - {use_case_name} in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Stop monitoring on error
            if performance_monitor:
                performance_monitor.stop_monitoring()
            
            execution_time = time.time() - start_time
            error_result = UseCaseResult(
                framework_name=framework_name,
                use_case_name=use_case_name,
                execution_time=execution_time,
                memory_usage=0.0,
                cpu_usage=0.0,
                api_costs={},
                quality_metrics={},
                raw_output=None,
                metadata={
                    "use_case_type": use_case_type,
                    "error_details": str(e),
                    "traceback": traceback.format_exc()
                },
                success=False,
                error_message=str(e)
            )
            
            self.evaluation_results.append(error_result)
            print(f"✗ Failed {framework_name} - {use_case_name}: {str(e)}")
            
            return error_result
    
    def run_framework_benchmark(self,
                               framework_name: str,
                               evaluator: BaseEvaluator,
                               test_cases: List[Dict[str, Any]],
                               retry_failed: bool = True,
                               max_retries: int = 2) -> List[UseCaseResult]:
        """
        Run a complete benchmark for a framework across multiple test cases.
        
        Args:
            framework_name: Name of the framework
            evaluator: Framework-specific evaluator instance
            test_cases: List of test case dictionaries
            retry_failed: Whether to retry failed test cases
            max_retries: Maximum number of retries for failed cases
            
        Returns:
            List of UseCaseResult objects
        """
        print(f"\n🚀 Starting benchmark for {framework_name}")
        print(f"Running {len(test_cases)} test cases")
        
        results = []
        failed_cases = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] Running: {test_case.get('name', 'Unnamed test')}")
            
            try:
                result = evaluator.execute_with_monitoring(
                    use_case_name=test_case.get('name', f'test_{i}'),
                    execution_func=test_case['execution_func'],
                    input_data=test_case.get('input_data'),
                    expected_output=test_case.get('expected_output')
                )
                
                results.append(result)
                
                if not result.success:
                    failed_cases.append((test_case, 0))  # (test_case, retry_count)
                    
            except Exception as e:
                print(f"✗ Test case failed with exception: {str(e)}")
                failed_cases.append((test_case, 0))
        
        # Retry failed cases if enabled
        if retry_failed and failed_cases:
            print(f"\n🔄 Retrying {len(failed_cases)} failed test cases")
            
            for test_case, retry_count in failed_cases:
                if retry_count < max_retries:
                    print(f"Retry {retry_count + 1}/{max_retries}: {test_case.get('name', 'Unnamed test')}")
                    
                    try:
                        result = evaluator.execute_with_monitoring(
                            use_case_name=test_case.get('name', f'retry_{retry_count + 1}'),
                            execution_func=test_case['execution_func'],
                            input_data=test_case.get('input_data'),
                            expected_output=test_case.get('expected_output')
                        )
                        
                        results.append(result)
                        
                    except Exception as e:
                        print(f"✗ Retry failed: {str(e)}")
        
        # Store framework summary
        self.framework_summaries[framework_name] = self._calculate_framework_summary(
            framework_name, results
        )
        
        print(f"\n✅ Completed benchmark for {framework_name}")
        print(f"Success rate: {self.framework_summaries[framework_name]['success_rate']:.1%}")
        
        return results
    
    def compare_frameworks(self, 
                          framework_results: Dict[str, List[UseCaseResult]]) -> Dict[str, Any]:
        """
        Compare results across multiple frameworks.
        
        Args:
            framework_results: Dictionary mapping framework names to their results
            
        Returns:
            Comprehensive comparison analysis
        """
        comparison = {
            "frameworks": {},
            "metrics_comparison": {},
            "rankings": {},
            "summary": {}
        }
        
        # Analyze each framework
        for framework_name, results in framework_results.items():
            framework_summary = self._calculate_framework_summary(framework_name, results)
            comparison["frameworks"][framework_name] = framework_summary
        
        # Compare metrics across frameworks
        comparison["metrics_comparison"] = self._compare_metrics(framework_results)
        
        # Generate rankings
        comparison["rankings"] = self._generate_rankings(comparison["frameworks"])
        
        # Overall summary
        comparison["summary"] = self._generate_comparison_summary(comparison)
        
        return comparison
    
    def export_results(self, 
                      format_type: str = "json",
                      filename: Optional[str] = None) -> str:
        """
        Export evaluation results to file.
        
        Args:
            format_type: Export format ("json", "csv", "html")
            filename: Optional custom filename
            
        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename is None:
            filename = f"evaluation_results_{timestamp}.{format_type}"
        
        filepath = self.output_dir / filename
        
        if format_type.lower() == "json":
            self._export_json(filepath)
        elif format_type.lower() == "csv":
            self._export_csv(filepath)
        elif format_type.lower() == "html":
            self._export_html(filepath)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        print(f"Results exported to: {filepath}")
        return str(filepath)
    
    def _calculate_quality_metrics(self,
                                  use_case_type: str,
                                  expected: Any,
                                  actual: Any,
                                  input_data: Any,
                                  **kwargs) -> Dict[str, float]:
        """Calculate quality metrics based on use case type."""
        quality_metrics = {}
        
        if expected is None:
            return quality_metrics
        
        try:
            if use_case_type == "qa":
                qa_results = self.qa_metrics.evaluate(expected, actual)
                quality_metrics.update({
                    name: result.score for name, result in qa_results.items()
                })
                
            elif use_case_type == "rag":
                # RAG evaluation requires additional context
                query = kwargs.get('query', str(input_data))
                context = kwargs.get('context', '')
                relevant_docs = kwargs.get('relevant_docs', [])
                retrieved_docs = kwargs.get('retrieved_docs', [])
                
                if relevant_docs and retrieved_docs:
                    retrieval_results = self.rag_metrics.evaluate_retrieval(relevant_docs, retrieved_docs)
                    quality_metrics.update({
                        name: result.score for name, result in retrieval_results.items()
                    })
                
                if query and context:
                    generation_results = self.rag_metrics.evaluate_generation(query, context, str(actual))
                    quality_metrics.update({
                        name: result.score for name, result in generation_results.items()
                    })
                    
            elif use_case_type == "search":
                query = kwargs.get('query', str(input_data))
                search_results = kwargs.get('search_results', [])
                
                if query and search_results:
                    search_eval_results = self.search_metrics.evaluate(query, search_results, str(actual))
                    quality_metrics.update({
                        name: result.score for name, result in search_eval_results.items()
                    })
                    
        except Exception as e:
            print(f"Warning: Quality metric calculation failed: {str(e)}")
        
        return quality_metrics
    
    def _get_recent_api_costs(self, start_time: float) -> Dict[str, float]:
        """Get API costs since the specified start time."""
        if not self.cost_tracker:
            return {}
        
        start_datetime = datetime.fromtimestamp(start_time)
        summary = self.cost_tracker.get_usage_summary(start_time=start_datetime)
        
        return {
            provider: data["cost"]
            for provider, data in summary.get("providers", {}).items()
        }
    
    def _calculate_framework_summary(self, 
                                   framework_name: str,
                                   results: List[UseCaseResult]) -> Dict[str, Any]:
        """Calculate summary statistics for a framework."""
        if not results:
            return {"success_rate": 0.0, "total_tests": 0}
        
        successful_results = [r for r in results if r.success]
        
        summary = {
            "framework_name": framework_name,
            "total_tests": len(results),
            "successful_tests": len(successful_results),
            "success_rate": len(successful_results) / len(results),
            "average_execution_time": sum(r.execution_time for r in successful_results) / len(successful_results) if successful_results else 0.0,
            "average_memory_usage": sum(r.memory_usage for r in successful_results) / len(successful_results) if successful_results else 0.0,
            "average_cpu_usage": sum(r.cpu_usage for r in successful_results) / len(successful_results) if successful_results else 0.0,
            "total_api_costs": sum(sum(r.api_costs.values()) for r in successful_results),
            "quality_metrics": {}
        }
        
        # Aggregate quality metrics
        if successful_results:
            all_metrics = set()
            for result in successful_results:
                all_metrics.update(result.quality_metrics.keys())
            
            for metric in all_metrics:
                scores = [r.quality_metrics.get(metric, 0.0) for r in successful_results if metric in r.quality_metrics]
                if scores:
                    summary["quality_metrics"][metric] = {
                        "average": sum(scores) / len(scores),
                        "min": min(scores),
                        "max": max(scores),
                        "count": len(scores)
                    }
        
        return summary
    
    def _compare_metrics(self, framework_results: Dict[str, List[UseCaseResult]]) -> Dict[str, Any]:
        """Compare metrics across frameworks."""
        # Implementation for metric comparison
        return {}
    
    def _generate_rankings(self, framework_summaries: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate rankings for different metrics."""
        # Implementation for ranking generation
        return {}
    
    def _generate_comparison_summary(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall comparison summary."""
        # Implementation for summary generation
        return {}
    
    def _export_json(self, filepath: Path) -> None:
        """Export results as JSON."""
        data = {
            "evaluation_results": [
                {
                    "framework_name": r.framework_name,
                    "use_case_name": r.use_case_name,
                    "execution_time": r.execution_time,
                    "memory_usage": r.memory_usage,
                    "cpu_usage": r.cpu_usage,
                    "api_costs": r.api_costs,
                    "quality_metrics": r.quality_metrics,
                    "success": r.success,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp.isoformat(),
                    "metadata": r.metadata
                }
                for r in self.evaluation_results
            ],
            "framework_summaries": self.framework_summaries,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _export_csv(self, filepath: Path) -> None:
        """Export results as CSV."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'framework_name', 'use_case_name', 'execution_time', 'memory_usage',
                'cpu_usage', 'total_api_cost', 'success', 'error_message', 'timestamp'
            ])
            
            # Write data
            for result in self.evaluation_results:
                writer.writerow([
                    result.framework_name,
                    result.use_case_name,
                    result.execution_time,
                    result.memory_usage,
                    result.cpu_usage,
                    sum(result.api_costs.values()),
                    result.success,
                    result.error_message or '',
                    result.timestamp.isoformat()
                ])
    
    def _export_html(self, filepath: Path) -> None:
        """Export results as HTML report."""
        # Implementation for HTML export
        html_content = "<html><body><h1>Evaluation Results</h1></body></html>"
        
        with open(filepath, 'w') as f:
            f.write(html_content)
