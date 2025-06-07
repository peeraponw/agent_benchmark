"""
Base metric interfaces and common utilities for evaluation metrics.

This module provides the abstract base classes and common functionality
that all specific metric implementations should inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import numpy as np


class MetricResult(BaseModel):
    """
    Result of a metric calculation.

    Contains the metric score, confidence interval, and additional metadata.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    name: str = Field(
        ...,
        description="Name of the metric",
        min_length=1,
        max_length=100
    )
    score: float = Field(
        ...,
        description="Calculated metric score",
        ge=0.0,
        le=1.0
    )
    confidence_interval: Optional[tuple[float, float]] = Field(
        default=None,
        description="95% confidence interval for the score (lower_bound, upper_bound)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the metric calculation"
    )


class BaseMetric(ABC):
    """
    Abstract base class for all evaluation metrics.
    
    Defines the standard interface that all metric implementations must follow
    to ensure consistent evaluation across different AI frameworks.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize the metric.
        
        Args:
            name: Name of the metric
            description: Description of what the metric measures
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate the metric score.
        
        Args:
            expected: Expected/ground truth value
            actual: Actual value from the system being evaluated
            **kwargs: Additional parameters specific to the metric
            
        Returns:
            MetricResult containing the score and metadata
        """
        pass
    
    def calculate_batch(self, expected_list: List[Any], actual_list: List[Any], **kwargs) -> List[MetricResult]:
        """
        Calculate metric scores for a batch of inputs.
        
        Args:
            expected_list: List of expected/ground truth values
            actual_list: List of actual values from the system
            **kwargs: Additional parameters specific to the metric
            
        Returns:
            List of MetricResult objects
        """
        if len(expected_list) != len(actual_list):
            raise ValueError("Expected and actual lists must have the same length")
        
        results = []
        for expected, actual in zip(expected_list, actual_list):
            result = self.calculate(expected, actual, **kwargs)
            results.append(result)
        
        return results
    
    def aggregate_results(self, results: List[MetricResult]) -> MetricResult:
        """
        Aggregate multiple metric results into a single result.
        
        Args:
            results: List of MetricResult objects to aggregate
            
        Returns:
            Aggregated MetricResult
        """
        if not results:
            return MetricResult(
                name=f"{self.name}_aggregated",
                score=0.0,
                metadata={"count": 0}
            )
        
        scores = [r.score for r in results]
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        # Calculate 95% confidence interval
        n = len(scores)
        if n > 1:
            se = std_score / np.sqrt(n)
            ci_lower = mean_score - 1.96 * se
            ci_upper = mean_score + 1.96 * se
            confidence_interval = (ci_lower, ci_upper)
        else:
            confidence_interval = None
        
        return MetricResult(
            name=f"{self.name}_aggregated",
            score=mean_score,
            confidence_interval=confidence_interval,
            metadata={
                "count": n,
                "std": std_score,
                "min": min(scores),
                "max": max(scores),
                "individual_results": results
            }
        )


class TextSimilarityMetric(BaseMetric):
    """
    Base class for text similarity metrics.
    
    Provides common functionality for metrics that compare text strings.
    """
    
    def __init__(self, name: str, description: str = "", case_sensitive: bool = False):
        """
        Initialize the text similarity metric.
        
        Args:
            name: Name of the metric
            description: Description of what the metric measures
            case_sensitive: Whether to perform case-sensitive comparison
        """
        super().__init__(name, description)
        self.case_sensitive = case_sensitive
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text before comparison.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Handle case sensitivity
        if not self.case_sensitive:
            text = text.lower()
        
        return text


class NumericalMetric(BaseMetric):
    """
    Base class for numerical metrics.
    
    Provides common functionality for metrics that work with numerical values.
    """
    
    def __init__(self, name: str, description: str = "", normalize: bool = True):
        """
        Initialize the numerical metric.
        
        Args:
            name: Name of the metric
            description: Description of what the metric measures
            normalize: Whether to normalize scores to [0, 1] range
        """
        super().__init__(name, description)
        self.normalize = normalize
    
    def validate_numerical_input(self, value: Any) -> float:
        """
        Validate and convert input to numerical value.
        
        Args:
            value: Input value to validate
            
        Returns:
            Numerical value
            
        Raises:
            ValueError: If value cannot be converted to float
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert {value} to numerical value")


class ListMetric(BaseMetric):
    """
    Base class for metrics that work with lists or sequences.
    
    Provides common functionality for metrics that compare lists of items.
    """
    
    def __init__(self, name: str, description: str = "", order_matters: bool = True):
        """
        Initialize the list metric.
        
        Args:
            name: Name of the metric
            description: Description of what the metric measures
            order_matters: Whether the order of items in lists matters
        """
        super().__init__(name, description)
        self.order_matters = order_matters
    
    def validate_list_input(self, value: Any) -> List[Any]:
        """
        Validate and convert input to list.
        
        Args:
            value: Input value to validate
            
        Returns:
            List representation of the input
        """
        if isinstance(value, list):
            return value
        elif isinstance(value, (tuple, set)):
            return list(value)
        elif isinstance(value, str):
            # Split string into words
            return value.split()
        else:
            # Try to iterate over the value
            try:
                return list(value)
            except TypeError:
                return [value]


def calculate_confidence_interval(scores: List[float], confidence_level: float = 0.95) -> tuple[float, float]:
    """
    Calculate confidence interval for a list of scores.
    
    Args:
        scores: List of numerical scores
        confidence_level: Confidence level (default: 0.95 for 95% CI)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    if len(scores) < 2:
        return (0.0, 0.0)
    
    mean_score = np.mean(scores)
    std_score = np.std(scores, ddof=1)  # Sample standard deviation
    n = len(scores)
    
    # Calculate critical value for given confidence level
    alpha = 1 - confidence_level
    z_score = 1.96  # For 95% confidence interval
    
    if confidence_level == 0.99:
        z_score = 2.576
    elif confidence_level == 0.90:
        z_score = 1.645
    
    # Calculate margin of error
    margin_of_error = z_score * (std_score / np.sqrt(n))
    
    return (mean_score - margin_of_error, mean_score + margin_of_error)


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a score to a specified range.
    
    Args:
        score: Score to normalize
        min_val: Minimum value of the target range
        max_val: Maximum value of the target range
        
    Returns:
        Normalized score
    """
    if score < min_val:
        return min_val
    elif score > max_val:
        return max_val
    else:
        return score


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default value if denominator is zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return if denominator is zero
        
    Returns:
        Division result or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator
