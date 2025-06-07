# Dataset Documentation and Usage Guide

## Overview

This document provides comprehensive documentation for all datasets used in the AI Agent Framework Comparison Project. These datasets are designed to enable fair and consistent evaluation across different AI agent frameworks.

## Data Collection Methodology

### Q&A Dataset (`qa/`)

**Collection Approach**: 
- Questions were sourced from diverse domains including science, history, geography, technology, and current events
- Difficulty levels were assigned based on cognitive complexity and domain expertise required
- Categories were designed to test different reasoning capabilities

**Quality Assurance**:
- All questions reviewed for clarity and accuracy
- Answers verified against authoritative sources
- Alternative acceptable answers documented where applicable
- Metadata includes confidence scores and source attribution

**Coverage Statistics**:
- Total Questions: 100
- Factual Questions: 30 (30%)
- Reasoning Questions: 30 (30%)
- Contextual Questions: 25 (25%)
- Multi-step Questions: 15 (15%)

### Web Search Query Dataset (`web_search/`)

**Collection Approach**:
- Queries designed to test real-world search scenarios
- Time sensitivity categorized (high/medium/low)
- Expected sources identified for verification
- Categories cover current events, fact-checking, research, local information, and comparative analysis

**Quality Assurance**:
- Expected sources verified for authority and reliability
- Time-sensitive queries include freshness requirements
- Credibility scoring rubrics developed for each query type
- Negative examples included to test discrimination

**Coverage Statistics**:
- Total Queries: 75
- Current Events: 25 (33%)
- Fact-checking: 15 (20%)
- Research: 15 (20%)
- Local Information: 10 (13%)
- Comparative: 10 (13%)

### RAG Document Collection (`rag_documents/`)

**Collection Approach**:
- Documents sourced from multiple domains and formats
- Ground truth queries designed to test retrieval accuracy
- Cross-document synthesis scenarios included
- Negative examples provided for discrimination testing

**Document Categories**:
- Technical Documentation: 15 documents (Programming, APIs, Software Architecture)
- Business Documents: 9 documents (Strategy, Management, Finance)
- Scientific Papers: 9 documents (Climate, Quantum Computing, Neuroscience)
- Legal Documents: 4 documents (Privacy, Employment, Corporate Law)
- Educational Content: 7 documents (Machine Learning, Assessment, Online Learning)

**Ground Truth Statistics**:
- Total Queries: 50
- Single Document Queries: 35 (70%)
- Multi-document Queries: 10 (20%)
- Cross-domain Synthesis: 5 (10%)
- Negative Examples: 5 (10%)

### Multi-Agent Scenarios (`multi_agent/`)

**Collection Approach**:
- Scenarios designed to test agent collaboration and coordination
- Complexity levels range from simple to expert
- Agent roles and responsibilities clearly defined
- Expected deliverables and success criteria specified

**Scenario Categories**:
- Research Tasks: 15 scenarios (Literature review, Market analysis, Technical research)
- Customer Service: 2 scenarios (Returns, Billing disputes)
- Content Creation: 2 scenarios (Blog posts, Marketing campaigns)

**Complexity Distribution**:
- Simple: 5 scenarios (15-minute tasks)
- Medium: 4 scenarios (30-45 minute tasks)
- Complex: 3 scenarios (60-120 minute tasks)
- Expert: 2 scenarios (120+ minute tasks)

## Categorization and Tagging Systems

### Difficulty Levels

**Easy**: Basic factual recall, simple calculations, straightforward procedures
- Examples: "What is the capital of France?", "Current weather in New York"
- Expected completion time: < 30 seconds

**Medium**: Requires domain knowledge, multi-step reasoning, or interpretation
- Examples: "Compare renewable vs non-renewable energy", "Analyze sentiment in social media"
- Expected completion time: 30 seconds - 2 minutes

**Hard**: Complex analysis, synthesis of multiple sources, expert domain knowledge
- Examples: "Design sustainable transportation system", "Analyze economic policy effectiveness"
- Expected completion time: 2-10 minutes

**Expert**: Highly specialized knowledge, complex multi-step reasoning, research-level analysis
- Examples: "Quantum computing cryptography applications", "AI ethics framework development"
- Expected completion time: 10+ minutes

**Creative**: Open-ended problems requiring innovation and original thinking
- Examples: "Novel climate change solutions", "Redesign human society principles"
- Expected completion time: Variable

### Category Classifications

**Q&A Categories**:
- `factual`: Direct factual questions with definitive answers
- `reasoning`: Questions requiring logical thinking and analysis
- `contextual`: Questions requiring interpretation and inference
- `multi_step`: Complex questions requiring multiple reasoning steps
- `creative`: Open-ended questions requiring innovation

**Web Search Categories**:
- `current_events`: Time-sensitive information requiring recent data
- `fact_checking`: Verification of claims against authoritative sources
- `research`: Academic or technical information requiring credible sources
- `local_information`: Location-specific data and services
- `comparative`: Analysis comparing multiple options or approaches

**RAG Query Types**:
- `definition`: Basic concept explanations
- `application`: Practical uses and implementations
- `comparison`: Comparative analysis between concepts
- `synthesis`: Integration of information from multiple sources
- `technical`: Specialized technical information

## Usage Guidelines

### For Framework Developers

1. **Dataset Loading**: Use the `DatasetManager` class to load datasets consistently
2. **Evaluation Metrics**: Apply appropriate metrics based on dataset type and difficulty
3. **Error Handling**: Implement robust error handling for missing or malformed data
4. **Caching**: Consider caching strategies for large datasets to improve performance

### For Evaluators

1. **Baseline Establishment**: Run validation tools to establish baseline performance
2. **Comparative Analysis**: Use identical datasets across all frameworks for fair comparison
3. **Statistical Significance**: Ensure sufficient sample sizes for meaningful comparisons
4. **Bias Detection**: Monitor for systematic biases in framework performance

### For Researchers

1. **Reproducibility**: Document exact dataset versions and configurations used
2. **Extension**: Follow established patterns when adding new test cases
3. **Validation**: Use provided validation tools to ensure data quality
4. **Attribution**: Cite dataset sources and methodology in publications

## Data Licensing and Attribution

### Source Attribution

- **Q&A Questions**: Derived from public knowledge sources, educational materials, and expert knowledge
- **Web Search Queries**: Based on common search patterns and information needs
- **RAG Documents**: Synthesized from publicly available technical documentation and educational content
- **Multi-Agent Scenarios**: Designed based on real-world business and research use cases

### Usage Rights

- All datasets are provided for research and evaluation purposes
- Commercial use requires appropriate licensing of underlying sources
- Attribution to the AI Agent Framework Comparison Project is requested
- Modifications and extensions are encouraged with proper documentation

### Privacy and Ethics

- No personally identifiable information (PII) included in any dataset
- All scenarios are fictional and do not represent real individuals or organizations
- Ethical considerations reviewed for all content, especially in AI ethics scenarios
- Bias mitigation strategies applied during dataset creation

## Quality Metrics and Validation

### Automated Validation

The project includes comprehensive validation tools (`validation_tools.py`) that check:

- **Schema Compliance**: Ensures all items follow the expected data structure
- **Duplicate Detection**: Identifies and reports duplicate content
- **Completeness Verification**: Validates coverage across required categories
- **Data Integrity**: Checks for missing fields and invalid data types

### Quality Thresholds

- **Minimum Dataset Sizes**: Q&A (100), Web Search (75), RAG (50), Multi-Agent (15)
- **Category Coverage**: All required categories must be represented
- **Difficulty Distribution**: Balanced representation across difficulty levels
- **Accuracy Requirements**: All answers and expected results manually verified

### Continuous Improvement

- Regular reviews and updates based on framework evaluation results
- Community feedback integration for dataset enhancement
- Version control for tracking changes and improvements
- Performance monitoring to identify areas for expansion

## Version History

- **v1.0** (2024-12-19): Initial comprehensive dataset release
  - 100 Q&A pairs across all categories
  - 75 web search queries with verification criteria
  - 50 RAG ground truth queries with 35+ documents
  - 19 multi-agent scenarios across complexity levels
  - Complete validation and documentation framework

## Contact and Support

For questions, issues, or contributions related to the datasets:

- Review the dataset validation reports for quality metrics
- Use the provided validation tools to verify data integrity
- Follow the established patterns when extending datasets
- Document any modifications or customizations made

This documentation ensures consistent and effective use of the evaluation datasets across all AI agent framework implementations.
