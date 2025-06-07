"""
Tests for the base evaluator module.

Tests the UseCaseResult model validation and BaseEvaluator functionality.
"""

import pytest
from datetime import datetime
from typing import Any, Dict

from evaluation.base_evaluator import UseCaseResult, BaseEvaluator


class TestUseCaseResult:
    """Test cases for UseCaseResult model."""
    
    def test_valid_result_creation(self):
        """Test creating a valid UseCaseResult."""
        result = UseCaseResult(
            framework_name="test_framework",
            use_case_name="test_case",
            execution_time=1.5,
            memory_usage=100.0,
            cpu_usage=50.0,
            raw_output="test output"
        )
        
        assert result.framework_name == "test_framework"
        assert result.use_case_name == "test_case"
        assert result.execution_time == 1.5
        assert result.memory_usage == 100.0
        assert result.cpu_usage == 50.0
        assert result.raw_output == "test output"
        assert result.success is True
        assert result.error_message is None
        assert isinstance(result.timestamp, datetime)
        assert isinstance(result.api_costs, dict)
        assert isinstance(result.quality_metrics, dict)
        assert isinstance(result.metadata, dict)
    
    def test_failed_result_creation(self):
        """Test creating a failed UseCaseResult."""
        result = UseCaseResult(
            framework_name="test_framework",
            use_case_name="test_case",
            execution_time=0.5,
            memory_usage=0.0,
            cpu_usage=0.0,
            raw_output=None,
            success=False,
            error_message="Test error"
        )
        
        assert result.success is False
        assert result.error_message == "Test error"
        assert result.raw_output is None
    
    def test_result_with_metrics(self):
        """Test UseCaseResult with quality metrics and API costs."""
        result = UseCaseResult(
            framework_name="test_framework",
            use_case_name="test_case",
            execution_time=2.0,
            memory_usage=150.0,
            cpu_usage=75.0,
            api_costs={"openai": 0.05, "anthropic": 0.03},
            quality_metrics={"bleu": 0.8, "rouge": 0.75},
            raw_output="test output",
            metadata={"test_param": "value"}
        )
        
        assert result.api_costs["openai"] == 0.05
        assert result.api_costs["anthropic"] == 0.03
        assert result.quality_metrics["bleu"] == 0.8
        assert result.quality_metrics["rouge"] == 0.75
        assert result.metadata["test_param"] == "value"


class MockEvaluator(BaseEvaluator):
    """Mock evaluator for testing BaseEvaluator functionality."""
    
    def evaluate_response_quality(self, expected: Any, actual: Any) -> Dict[str, float]:
        """Mock quality evaluation."""
        if expected == actual:
            return {"accuracy": 1.0}
        else:
            return {"accuracy": 0.5}
    
    def measure_performance(self, execution_func) -> Dict[str, float]:
        """Mock performance measurement."""
        return {"custom_metric": 1.0}


class TestBaseEvaluator:
    """Test cases for BaseEvaluator functionality."""
    
    def test_evaluator_initialization(self):
        """Test BaseEvaluator initialization."""
        evaluator = MockEvaluator("test_framework")
        assert evaluator.framework_name == "test_framework"
        assert evaluator.current_process is not None
    
    def test_execute_with_monitoring_success(self):
        """Test successful execution with monitoring."""
        evaluator = MockEvaluator("test_framework")
        
        def mock_execution(input_data):
            return f"processed: {input_data}"
        
        result = evaluator.execute_with_monitoring(
            use_case_name="test_case",
            execution_func=mock_execution,
            input_data="test input",
            expected_output="processed: test input"
        )
        
        assert result.framework_name == "test_framework"
        assert result.use_case_name == "test_case"
        assert result.success is True
        assert result.raw_output == "processed: test input"
        assert result.quality_metrics["accuracy"] == 1.0
        assert result.execution_time > 0
    
    def test_execute_with_monitoring_failure(self):
        """Test execution with monitoring when function fails."""
        evaluator = MockEvaluator("test_framework")
        
        def failing_execution(input_data):
            raise ValueError("Test error")
        
        result = evaluator.execute_with_monitoring(
            use_case_name="test_case",
            execution_func=failing_execution,
            input_data="test input"
        )
        
        assert result.framework_name == "test_framework"
        assert result.use_case_name == "test_case"
        assert result.success is False
        assert result.error_message == "Test error"
        assert result.raw_output is None
        assert result.execution_time > 0
    
    def test_calculate_aggregate_metrics(self):
        """Test aggregate metrics calculation."""
        evaluator = MockEvaluator("test_framework")
        
        # Create test results
        results = [
            UseCaseResult(
                framework_name="test_framework",
                use_case_name="test1",
                execution_time=1.0,
                memory_usage=100.0,
                cpu_usage=50.0,
                quality_metrics={"accuracy": 0.8},
                raw_output="output1"
            ),
            UseCaseResult(
                framework_name="test_framework",
                use_case_name="test2",
                execution_time=2.0,
                memory_usage=200.0,
                cpu_usage=60.0,
                quality_metrics={"accuracy": 0.9},
                raw_output="output2"
            ),
            UseCaseResult(
                framework_name="test_framework",
                use_case_name="test3",
                execution_time=1.5,
                memory_usage=150.0,
                cpu_usage=55.0,
                quality_metrics={"accuracy": 0.7},
                raw_output="output3",
                success=False  # Failed result should be excluded
            )
        ]
        
        aggregate = evaluator.calculate_aggregate_metrics(results)
        
        assert aggregate["success_rate"] == 2/3  # 2 successful out of 3
        assert aggregate["total_use_cases"] == 3
        assert aggregate["average_execution_time"] == 1.5  # (1.0 + 2.0) / 2
        assert aggregate["average_memory_usage"] == 150.0  # (100.0 + 200.0) / 2
        assert aggregate["average_cpu_usage"] == 55.0  # (50.0 + 60.0) / 2
        assert aggregate["average_quality_scores"]["accuracy"] == 0.85  # (0.8 + 0.9) / 2
    
    def test_calculate_aggregate_metrics_empty(self):
        """Test aggregate metrics calculation with empty results."""
        evaluator = MockEvaluator("test_framework")
        aggregate = evaluator.calculate_aggregate_metrics([])
        
        assert aggregate == {}
    
    def test_calculate_aggregate_metrics_all_failed(self):
        """Test aggregate metrics calculation with all failed results."""
        evaluator = MockEvaluator("test_framework")
        
        results = [
            UseCaseResult(
                framework_name="test_framework",
                use_case_name="test1",
                execution_time=1.0,
                memory_usage=0.0,
                cpu_usage=0.0,
                raw_output=None,
                success=False
            )
        ]
        
        aggregate = evaluator.calculate_aggregate_metrics(results)
        
        assert aggregate["success_rate"] == 0.0
        assert aggregate["total_use_cases"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
