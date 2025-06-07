# Shared Dataset Manager

This directory contains the shared dataset management system for the AI Agent Framework Comparison project. It provides standardized test datasets and management utilities that ensure consistent evaluation across all AI agent frameworks.

## Overview

The Shared Dataset Manager provides:

- **Standardized Data Models**: Pydantic-based models for consistent data validation
- **Multi-format Support**: Load and save datasets in JSON, JSONL, and CSV formats
- **Quality Validation**: Comprehensive validation and quality control
- **Statistics & Analysis**: Detailed dataset statistics and distribution analysis
- **Import/Export Utilities**: Tools for dataset migration and sharing

## Directory Structure

```
shared_datasets/
├── dataset_manager.py      # Core dataset management functionality
├── validator.py           # Dataset validation and quality control
├── config.py              # Configuration settings and constants
├── README.md              # This documentation file
├── qa/                    # Question & Answer datasets
│   ├── questions.json     # Test questions with metadata
│   ├── answers.json       # Expected answers with confidence scores
│   └── metadata.json      # Dataset metadata and statistics
├── rag_documents/         # RAG (Retrieval Augmented Generation) datasets
│   ├── documents/         # Source documents in various formats
│   ├── ground_truth/      # Expected retrieval results
│   └── embeddings/        # Pre-computed vector embeddings
├── web_search/           # Web search query datasets
│   ├── queries.json      # Search queries with complexity levels
│   └── expected_sources.json  # Expected source types and credibility
└── multi_agent/          # Multi-agent scenario datasets
    ├── research_tasks.json     # Research pipeline scenarios
    ├── customer_service.json   # Customer service simulations
    └── content_creation.json   # Content creation workflows
```

## Quick Start

### Basic Usage

```python
from pathlib import Path
from shared_datasets.dataset_manager import DatasetManager
from shared_datasets.config import DatasetConfig

# Initialize the dataset manager
config = DatasetConfig()
manager = DatasetManager(config.dataset_root)

# Load Q&A dataset
qa_items = manager.load_qa_dataset()
print(f"Loaded {len(qa_items)} Q&A items")

# Load RAG documents
rag_docs = manager.load_rag_documents()
print(f"Loaded {len(rag_docs)} RAG documents")

# Get comprehensive statistics
stats = manager.get_dataset_stats()
print(f"Total items across all datasets: {stats['overall_stats']['total_items']}")
```

### Dataset Validation

```python
from shared_datasets.validator import DatasetValidator

# Initialize validator
validator = DatasetValidator(config)

# Validate Q&A dataset
qa_items = manager.load_qa_dataset()
result = validator.validate_dataset_items(qa_items)

if result.is_valid:
    print("Dataset validation passed!")
else:
    print(f"Validation failed with {len(result.errors)} errors")
    for error in result.errors:
        print(f"  - {error}")

# Generate quality report
report = validator.generate_quality_report(result)
print(report)
```

### Export and Import

```python
# Export Q&A dataset to CSV
output_path = Path("exported_qa_dataset.csv")
manager.export_dataset("qa", "csv", output_path)

# Import dataset from external source
source_path = Path("external_dataset.json")
manager.import_dataset(source_path, "json", "qa", merge=True)
```

## Dataset Types

### 1. Q&A Dataset (`qa/`)

**Purpose**: Evaluate question-answering capabilities across different domains and difficulty levels.

**Structure**:
- `questions.json`: Contains questions with metadata
- `answers.json`: Contains expected answers with confidence scores
- `metadata.json`: Dataset-level metadata and statistics

**Example Question**:
```json
{
  "id": "qa_001",
  "question": "What is the capital of France?",
  "category": "factual",
  "difficulty": "easy",
  "expected_response_type": "short_answer"
}
```

**Example Answer**:
```json
{
  "id": "qa_001",
  "answer": "Paris",
  "explanation": "Paris is the capital and largest city of France.",
  "sources": ["general_knowledge"],
  "confidence": 1.0
}
```

### 2. RAG Documents (`rag_documents/`)

**Purpose**: Test retrieval-augmented generation capabilities with diverse document types.

**Structure**:
- `documents/`: Source documents in various formats (TXT, MD, JSON, CSV, XML)
- `ground_truth/`: Expected retrieval results for test queries
- `embeddings/`: Pre-computed vector embeddings for consistency

**Document Categories**:
- Technology and software development
- Business and finance
- Science and research
- Legal and policy documents
- Educational content

### 3. Web Search Queries (`web_search/`)

**Purpose**: Evaluate web search and real-time information retrieval capabilities.

**Structure**:
- `queries.json`: Search queries with complexity and freshness requirements
- `expected_sources.json`: Expected source types and credibility levels

**Query Types**:
- Factual information queries
- Current events and time-sensitive queries
- Research and comparison queries
- Source credibility verification

### 4. Multi-Agent Scenarios (`multi_agent/`)

**Purpose**: Test multi-agent coordination and collaboration capabilities.

**Structure**:
- `research_tasks.json`: Research pipeline scenarios
- `customer_service.json`: Customer service simulations
- `content_creation.json`: Content creation workflows

**Complexity Levels**:
- **Simple**: 2 agents, linear workflow
- **Medium**: 3 agents, some parallelism
- **Complex**: 4+ agents, dynamic roles
- **Advanced**: Adaptive coordination patterns

## Data Quality Guidelines

### Best Practices

1. **Unique IDs**: Every dataset item must have a unique identifier
2. **Consistent Metadata**: Use standardized metadata fields across items
3. **Balanced Distribution**: Ensure good coverage across categories and difficulty levels
4. **Quality Sources**: Use reliable, verifiable sources for ground truth data
5. **Regular Updates**: Keep datasets current and relevant

### Validation Rules

- **Schema Compliance**: All items must conform to the DatasetItem model
- **Completeness**: Required fields must not be empty
- **Consistency**: Metadata structure should be consistent across items
- **No Duplicates**: Check for duplicate IDs and similar content
- **Size Limits**: Respect configured size limits for questions and answers

### Quality Metrics

- **Coverage**: Distribution across categories and difficulty levels
- **Accuracy**: Confidence scores and source reliability
- **Freshness**: Last update timestamps and content relevance
- **Diversity**: Variety in content types and domains

## Configuration

The dataset manager uses `config.py` for configuration settings:

```python
from shared_datasets.config import DatasetConfig

config = DatasetConfig()

# Customize settings
config.max_question_length = 2000  # Increase question length limit
config.min_confidence_score = 0.8  # Require higher confidence
config.required_qa_categories = ["factual", "reasoning", "creative"]
```

### Environment Variables

You can override configuration using environment variables with the `DATASET_` prefix:

```bash
export DATASET_MAX_QUESTION_LENGTH=2000
export DATASET_MIN_CONFIDENCE_SCORE=0.8
export DATASET_ENABLE_VERSIONING=true
```

## Troubleshooting

### Common Issues

**1. FileNotFoundError when loading datasets**
- Ensure the dataset directory structure exists
- Check file permissions
- Verify the dataset_path configuration

**2. ValidationError during dataset loading**
- Check JSON file syntax
- Ensure required fields are present
- Validate data types match expected schema

**3. Memory issues with large datasets**
- Use streaming for large file operations
- Consider dataset chunking for processing
- Monitor memory usage during validation

**4. Inconsistent metadata across items**
- Use the validator to identify inconsistencies
- Standardize metadata fields
- Consider migration utilities for updates

### Performance Tips

1. **Caching**: Enable caching for frequently accessed datasets
2. **Lazy Loading**: Load datasets only when needed
3. **Batch Processing**: Process large datasets in batches
4. **Compression**: Use compressed formats for storage
5. **Indexing**: Create indexes for frequently queried fields

## Contributing

When adding new datasets or modifying existing ones:

1. **Follow Schema**: Use the DatasetItem model for consistency
2. **Validate Data**: Run validation before committing changes
3. **Update Metadata**: Keep metadata files current
4. **Test Changes**: Verify all dataset operations work correctly
5. **Document Updates**: Update this README for significant changes

## API Reference

### DatasetManager

- `load_qa_dataset()`: Load Q&A dataset items
- `save_qa_dataset(items)`: Save Q&A dataset items
- `load_rag_documents()`: Load RAG documents
- `load_rag_ground_truth()`: Load RAG ground truth data
- `load_search_queries()`: Load web search queries
- `load_multiagent_scenarios()`: Load multi-agent scenarios
- `get_dataset_stats()`: Get comprehensive statistics
- `export_dataset(type, format, path)`: Export dataset
- `import_dataset(path, format, type)`: Import dataset

### DatasetValidator

- `validate_dataset_items(items)`: Validate dataset items
- `generate_quality_report(result)`: Generate quality report

### DatasetItem Model

- `id`: Unique identifier
- `input_data`: Input data for the test case
- `expected_output`: Expected output or ground truth
- `metadata`: Additional context and metadata
- `difficulty_level`: Difficulty categorization
- `category`: Category or type classification

For detailed API documentation, see the docstrings in the source code.
