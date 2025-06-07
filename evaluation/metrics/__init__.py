"""
Evaluation metrics module for AI agent framework comparison.

This module provides comprehensive quality metrics for evaluating AI agent
frameworks across different use cases including Q&A, RAG, and web search.
"""

from .base_metrics import BaseMetric, MetricResult
from .qa_metrics import QAMetrics
from .rag_metrics import RAGMetrics
from .search_metrics import SearchMetrics

__version__ = "1.0.0"
__all__ = [
    "BaseMetric",
    "MetricResult", 
    "QAMetrics",
    "RAGMetrics",
    "SearchMetrics"
]
