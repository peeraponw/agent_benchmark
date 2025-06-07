# Model Comparison Guide

This guide explains how to conduct model comparison studies within and across AI agent frameworks using the standardized OpenRouter configuration.

## 🎯 Default Configuration

All frameworks are configured with **DeepSeek R1** (`deepseek/deepseek-r1-0528`) as the default model for:
- Consistent baseline testing
- Reproducible results across frameworks
- Cost-effective evaluation

## 🔄 Model Switching Methods

### Method 1: Environment Variable Change
The simplest way to switch models for testing:

```bash
# In any framework's .env file
DEFAULT_LLM_MODEL=deepseek/deepseek-r1-0528          # Default
DEFAULT_LLM_MODEL=anthropic/claude-sonnet-4          # Switch to Claude
DEFAULT_LLM_MODEL=google/gemini-2.5-pro-preview     # Switch to Gemini
```

### Method 2: Multiple Environment Files
For systematic comparisons, create multiple environment configurations:

```bash
# Framework directory structure
crewai/
├── .env.deepseek     # DeepSeek R1 configuration
├── .env.claude       # Claude Sonnet 4 configuration
├── .env.gemini       # Gemini 2.5 Pro configuration
└── .env              # Symlink to current test configuration
```

### Method 3: Dynamic Configuration
For automated testing across models:

```python
# Example: Dynamic model switching in test scripts
models = [
    "deepseek/deepseek-r1-0528",
    "anthropic/claude-sonnet-4", 
    "google/gemini-2.5-pro-preview"
]

for model in models:
    os.environ["DEFAULT_LLM_MODEL"] = model
    # Run framework tests
    results[model] = run_framework_tests()
```

## 📊 Comparison Study Types

### 1. Single Framework, Multiple Models
Compare how different LLMs perform within the same framework:

```bash
# Test CrewAI with all three models
cd crewai/

# Test with DeepSeek R1 (default)
uv run python tasks/qa_task.py

# Switch to Claude and test
sed -i 's/DEFAULT_LLM_MODEL=.*/DEFAULT_LLM_MODEL=anthropic\/claude-sonnet-4/' .env
uv run python tasks/qa_task.py

# Switch to Gemini and test
sed -i 's/DEFAULT_LLM_MODEL=.*/DEFAULT_LLM_MODEL=google\/gemini-2.5-pro-preview/' .env
uv run python tasks/qa_task.py
```

### 2. Multiple Frameworks, Single Model
Compare how different frameworks perform with the same LLM:

```bash
# Test all frameworks with DeepSeek R1 (default configuration)
for framework in dspy pocketflow crewai google_adk pydantic_ai; do
    cd $framework/
    uv run python use_cases/qa_use_case.py
    cd ..
done
```

### 3. Cross-Framework Model Matrix
Comprehensive comparison across all frameworks and models:

```bash
# Matrix testing script example
frameworks=("dspy" "pocketflow" "crewai" "google_adk" "pydantic_ai")
models=("deepseek/deepseek-r1-0528" "anthropic/claude-sonnet-4" "google/gemini-2.5-pro-preview")

for framework in "${frameworks[@]}"; do
    for model in "${models[@]}"; do
        cd $framework/
        sed -i "s/DEFAULT_LLM_MODEL=.*/DEFAULT_LLM_MODEL=$model/" .env
        echo "Testing $framework with $model"
        uv run python use_cases/qa_use_case.py
        cd ..
    done
done
```

## 🔧 Configuration Templates

### DeepSeek R1 Configuration (Default)
```bash
DEFAULT_LLM_PROVIDER=openrouter
DEFAULT_LLM_MODEL=deepseek/deepseek-r1-0528
DEFAULT_LLM_TEMPERATURE=0.1
```

### Claude Sonnet 4 Configuration
```bash
DEFAULT_LLM_PROVIDER=openrouter
DEFAULT_LLM_MODEL=anthropic/claude-sonnet-4
DEFAULT_LLM_TEMPERATURE=0.1
```

### Gemini 2.5 Pro Configuration
```bash
DEFAULT_LLM_PROVIDER=openrouter
DEFAULT_LLM_MODEL=google/gemini-2.5-pro-preview
DEFAULT_LLM_TEMPERATURE=0.1
```

## 📈 Results Analysis

### Standardized Metrics
All frameworks should report consistent metrics for comparison:

- **Accuracy**: Task completion success rate
- **Latency**: Response time per task
- **Token Usage**: Input/output token consumption
- **Cost**: Estimated cost per task via OpenRouter
- **Quality**: Subjective quality scores

### Results Structure
```json
{
  "framework": "dspy",
  "model": "deepseek/deepseek-r1-0528",
  "use_case": "qa_use_case",
  "timestamp": "2024-12-19T10:00:00Z",
  "metrics": {
    "accuracy": 0.85,
    "avg_latency_ms": 1200,
    "total_tokens": 1500,
    "estimated_cost_usd": 0.003,
    "quality_score": 4.2
  }
}
```

## 🎛️ Advanced Configuration

### Temperature Variations
Test model creativity vs consistency:

```bash
# Conservative (more deterministic)
DEFAULT_LLM_TEMPERATURE=0.0

# Balanced (default)
DEFAULT_LLM_TEMPERATURE=0.1

# Creative (more varied responses)
DEFAULT_LLM_TEMPERATURE=0.7
```

### Framework-Specific Optimizations
Each framework may have optimal settings for different models:

```bash
# DSPy with DeepSeek R1 - optimized for reasoning
DEFAULT_LLM_TEMPERATURE=0.0
DSPY_COMPILE_ENABLED=true

# CrewAI with Claude - optimized for collaboration
DEFAULT_LLM_TEMPERATURE=0.1
CREWAI_AGENT_COOPERATION=enhanced

# PocketFlow with Gemini - optimized for graph reasoning
DEFAULT_LLM_TEMPERATURE=0.1
GRAPH_REASONING_MODE=enhanced
```

## 🚀 Best Practices

### 1. Baseline Testing
- Always start with DeepSeek R1 default configuration
- Establish baseline performance metrics
- Document environmental conditions

### 2. Controlled Variables
- Change only one variable at a time (model OR framework)
- Use identical datasets and tasks
- Maintain consistent infrastructure

### 3. Statistical Significance
- Run multiple iterations per configuration
- Calculate confidence intervals
- Account for model non-determinism

### 4. Documentation
- Record all configuration changes
- Log model versions and parameters
- Track OpenRouter model availability

## 🔍 Validation

Run the validation script to ensure all configurations are correct:

```bash
cd scripts/
uv run python validate_structure.py
```

This will verify:
- All environment templates have correct OpenRouter configuration
- Default models are set to DeepSeek R1
- Alternative model options are documented
- Configuration syntax is valid

## 📝 Example Study

### Research Question
"How do different LLMs perform on Q&A use cases across agent frameworks?"

### Methodology
1. Use default DeepSeek R1 configuration for baseline
2. Test each framework with all three models
3. Measure accuracy, latency, and cost
4. Analyze framework-model interaction effects

### Expected Outcomes
- Identify optimal model-framework combinations
- Understand cost-performance trade-offs
- Document framework-specific model preferences
- Establish benchmarking standards

This standardized approach ensures fair, reproducible comparisons while maintaining the flexibility to explore different model capabilities across frameworks.
