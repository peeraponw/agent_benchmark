# Evaluation Framework

A comprehensive evaluation framework for comparing AI agent frameworks across standardized use cases and metrics.

## Overview

This evaluation framework provides:

- **Standardized Metrics**: Consistent evaluation across Q&A, RAG, and web search use cases
- **Performance Monitoring**: Real-time tracking of CPU, memory, and execution time
- **Cost Tracking**: Comprehensive API cost calculation across multiple providers
- **Quality Assessment**: Advanced metrics including BLEU, ROUGE, semantic similarity, and domain-specific evaluations
- **Result Aggregation**: Automated comparison and ranking across frameworks

## Quick Start

### Basic Usage

```python
from evaluation.evaluator import FrameworkEvaluator
from evaluation.base_evaluator import BaseEvaluator

# Initialize the evaluator
evaluator = FrameworkEvaluator(output_dir="results")

# Define your framework's execution function
def my_framework_execution(input_data):
    # Your framework's implementation
    return f"Processed: {input_data}"

# Evaluate a single task
result = evaluator.evaluate_single_task(
    framework_name="MyFramework",
    use_case_name="simple_qa",
    execution_func=my_framework_execution,
    input_data="What is the capital of France?",
    expected_output="Paris",
    use_case_type="qa"
)

print(f"Execution time: {result.execution_time:.2f}s")
print(f"Quality metrics: {result.quality_metrics}")
```

### Performance Monitoring

```python
from evaluation.performance_monitor import monitor_performance

# Monitor performance of any function
with monitor_performance(sampling_interval=0.1) as monitor:
    # Your code here
    result = expensive_operation()

metrics = monitor.get_metrics()
print(f"Peak memory: {metrics.peak_memory_mb:.2f}MB")
print(f"Average CPU: {metrics.average_cpu_percent:.1f}%")
```

### Cost Tracking

```python
from evaluation.cost_tracker import APIUsageTracker, APIProvider

# Track API usage and costs
tracker = APIUsageTracker()

# Record OpenRouter API usage
tracker.record_usage(
    provider=APIProvider.OPENROUTER,
    model="anthropic/claude-4-sonnet",
    input_tokens=100,
    output_tokens=50
)

# Get cost summary
total_cost = tracker.get_total_cost()
summary = tracker.get_usage_summary()
print(f"Total cost: ${total_cost:.4f}")
```

## Components

### Base Evaluator (`base_evaluator.py`)

The foundation of the evaluation framework:

- `UseCaseResult`: Standardized result structure
- `BaseEvaluator`: Abstract base class for framework evaluators

### Performance Monitor (`performance_monitor.py`)

Real-time performance monitoring:

- CPU usage tracking
- Memory consumption monitoring
- Execution time measurement
- Context manager support
- Export capabilities (JSON, CSV)

### Quality Metrics (`metrics/`)

Comprehensive quality assessment:

#### Q&A Metrics (`qa_metrics.py`)
- **BLEU Score**: N-gram overlap measurement
- **ROUGE Score**: Recall-oriented evaluation
- **Semantic Similarity**: Embedding-based similarity
- **Factual Accuracy**: Keyword and entity preservation

#### RAG Metrics (`rag_metrics.py`)
- **Retrieval Precision/Recall**: Document retrieval accuracy
- **Context Relevance**: Query-context similarity
- **Answer Groundedness**: Answer support in context

#### Search Metrics (`search_metrics.py`)
- **Source Credibility**: Domain and content quality assessment
- **Information Freshness**: Recency evaluation
- **Query-Answer Relevance**: Search result relevance

### Cost Tracker (`cost_tracker.py`)

API cost management:

- OpenRouter provider support (standardized for this project)
- Real-time cost calculation
- Usage aggregation and reporting
- Cost comparison utilities

### Evaluation Orchestrator (`evaluator.py`)

Main coordination system:

- Single task evaluation
- Framework benchmarking
- Result aggregation
- Export functionality
- Error handling and retry logic

## Configuration

### Basic Configuration

```python
from evaluation.config import update_config, get_config

# Update global settings
update_config(
    default_timeout_seconds=300,
    semantic_similarity_model="all-MiniLM-L6-v2",
    enable_cost_tracking=True
)

# Get current configuration
config = get_config()
print(f"Timeout: {config.default_timeout_seconds}s")
```

### Framework-Specific Configuration

```python
from evaluation.config import set_framework_config

# Set framework-specific settings
set_framework_config("MyFramework", {
    "timeout_seconds": 120,
    "enable_retries": True,
    "custom_parameter": "value"
})
```

## Metrics Guide

### Quality Metrics

#### BLEU Score
Measures n-gram overlap between expected and actual text with brevity penalty.
- Range: 0.0 to 1.0
- Higher is better
- Good for: Translation, text generation

#### ROUGE Score
Recall-oriented evaluation focusing on content overlap.
- Range: 0.0 to 1.0
- Higher is better
- Good for: Summarization, content generation

#### Semantic Similarity
Embedding-based similarity using sentence transformers.
- Range: 0.0 to 1.0
- Higher is better
- Good for: Meaning preservation, paraphrasing

#### Factual Accuracy
Preservation of factual information (numbers, entities, keywords).
- Range: 0.0 to 1.0
- Higher is better
- Good for: Fact-based Q&A, information extraction

### Performance Metrics

- **Execution Time**: Task completion latency
- **Memory Usage**: Peak and average memory consumption
- **CPU Usage**: Processing resource utilization
- **API Costs**: LLM and service expenses

## Export Formats

### JSON Export
```python
evaluator.export_results("json", "results.json")
```

### CSV Export
```python
evaluator.export_results("csv", "results.csv")
```

### HTML Report
```python
evaluator.export_results("html", "report.html")
```

## Testing

Run the test suite:

```bash
# Run all tests
uv run pytest evaluation/tests/

# Run specific test file
uv run pytest evaluation/tests/test_base_evaluator.py

# Run with coverage
uv run pytest evaluation/tests/ --cov=evaluation
```

## Performance Benchmarking Guidelines

### Best Practices

1. **Consistent Environment**: Run evaluations in similar conditions
2. **Multiple Runs**: Average results across multiple executions
3. **Warm-up**: Allow frameworks to initialize before measurement
4. **Resource Isolation**: Minimize background processes
5. **Statistical Significance**: Use confidence intervals for comparisons

### Sample Sizes

- **Development Testing**: 10-20 test cases per use case
- **Comprehensive Evaluation**: 100+ test cases per use case
- **Production Benchmarks**: 500+ test cases with statistical analysis

## Troubleshooting

### Common Issues

#### High Memory Usage
```python
# Reduce sampling interval
monitor = PerformanceMonitor(sampling_interval=0.5)

# Disable detailed monitoring
monitor = PerformanceMonitor(
    include_disk_io=False,
    include_network_io=False
)
```

#### Timeout Errors
```python
# Increase timeout
update_config(default_timeout_seconds=600)

# Enable retries
update_config(max_retries=5)
```

#### Cost Tracking Issues
```python
# Update pricing data
tracker.update_pricing(
    provider=APIProvider.OPENROUTER,
    model="anthropic/claude-3.5-sonnet",
    input_rate=0.003,
    output_rate=0.015
)
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or update config
update_config(log_level="DEBUG")
```

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure type hints are included
5. Run the full test suite before submitting

## License

This evaluation framework is part of the AI Agent Frameworks Comparison project.
