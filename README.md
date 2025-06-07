# AI Agent Frameworks Comparison Project

A comprehensive evaluation and comparison of leading Python AI agent frameworks across standardized tasks and metrics.

## 🎯 Project Overview

This project systematically compares five leading Python AI agent frameworks:
- **CrewAI** - Multi-agent orchestration framework
- **DSPy** - Programming framework for language models
- **PocketFlow** - Nested directed graph framework
- **Google ADK** - Google's Agent Development Kit
- **Pydantic AI** - Type-safe agent framework

Each framework is evaluated across six standardized tasks with complete isolation to ensure fair comparison.

## 🏗️ Architecture

The project uses a **framework-isolated architecture** where each AI framework operates in its own environment with dedicated infrastructure, preventing cross-contamination while enabling fair comparison.

```
agent_benchmark/
├── crewai/           # CrewAI framework implementation
├── dspy/             # DSPy framework implementation
├── pocketflow/       # PocketFlow framework implementation
├── google_adk/       # Google ADK framework implementation
├── pydantic_ai/      # Pydantic AI framework implementation
├── shared_datasets/  # Common test data across frameworks
├── evaluation/       # Cross-framework evaluation tools
└── docs/            # Project documentation
```

## 📊 Framework Comparison Matrix

| Framework | Multi-Agent | Type Safety | Learning | Web Search | RAG Support | Complexity |
|-----------|-------------|-------------|----------|------------|-------------|------------|
| CrewAI | ✅ Excellent | ⚠️ Basic | ❌ Limited | ✅ Good | ✅ Good | Medium |
| DSPy | ⚠️ Limited | ✅ Good | ✅ Excellent | ⚠️ Basic | ✅ Good | High |
| PocketFlow | ✅ Good | ⚠️ Basic | ⚠️ Basic | ✅ Excellent | ⚠️ Basic | Medium |
| Google ADK | ✅ Good | ✅ Good | ⚠️ Basic | ✅ Good | ✅ Good | Medium |
| Pydantic AI | ⚠️ Limited | ✅ Excellent | ❌ Limited | ⚠️ Basic | ⚠️ Basic | Low |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/agent_benchmark.git
   cd agent_benchmark
   ```

2. **Choose a framework to explore**
   ```bash
   cd crewai/  # or dspy/, pocketflow/, google_adk/, pydantic_ai/
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Start infrastructure**
   ```bash
   docker-compose up -d
   ```

5. **Run a task**
   ```bash
   cd task1_qa/
   uv run python main.py
   ```

### Running Evaluations

```bash
# Run all frameworks on all tasks
python evaluation/benchmark_runner.py --frameworks all --tasks all

# Run specific framework
python evaluation/benchmark_runner.py --frameworks crewai --tasks all

# Generate comparison report
python evaluation/report_generator.py
```

## 📋 Evaluation Tasks

### Task 1: Question & Answer System
Simple Q&A implementation testing basic agent capabilities.

### Task 2: Simple RAG (Retrieval-Augmented Generation)
Document retrieval and answer generation with vector databases.

### Task 3: Agentic RAG
Advanced RAG with multiple specialized agents for research and synthesis.

### Task 4: Web Search Integration
Real-time information retrieval and fact verification.

### Task 5: Multi-Agent Collaboration
Complex workflows requiring agent coordination and specialization.

### Task 6: Advanced Agentic Tasks
Framework-specific advanced capabilities and optimizations.

## 📈 Evaluation Metrics

### Quality Metrics
- **Accuracy**: Correctness against ground truth
- **Relevance**: Response appropriateness to queries
- **Completeness**: Coverage of required information
- **Coherence**: Logical consistency and flow

### Performance Metrics
- **Execution Time**: Task completion speed
- **Resource Usage**: Memory and CPU consumption
- **API Costs**: LLM and service expenses
- **Scalability**: Performance under load

### Framework-Specific Metrics
- **Ease of Implementation**: Development complexity
- **Code Maintainability**: Framework abstractions
- **Documentation Quality**: Available resources
- **Community Support**: Ecosystem maturity

## 🔧 Development Setup

### Framework Development

Each framework maintains its own development environment:

```bash
# Navigate to framework directory
cd crewai/

# Install dependencies
uv sync

# Start development infrastructure
docker-compose up -d

# Run tests
uv run pytest

# Run specific task
cd task1_qa/
uv run python main.py
```

### Adding New Tasks

1. Create task directory in each framework
2. Implement standardized task interface
3. Add evaluation metrics
4. Update benchmark configurations
5. Test across all frameworks

## 📚 Documentation

- [Architecture Guide](ARCHITECTURE.md) - Detailed system design
- [Getting Started](GETTING_STARTED.md) - Quick setup guide
- [Framework Guides](docs/) - Framework-specific documentation
- [API Reference](docs/api/) - Code documentation
- [Evaluation Guide](docs/evaluation/) - Metrics and benchmarking

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Run evaluation suite
5. Submit pull request

### Code Standards

- Python 3.11+ with type hints
- UV for dependency management
- Pydantic for data validation
- Comprehensive docstrings
- 95%+ test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Framework maintainers and communities
- Open source contributors
- Research institutions and papers
- Beta testers and early adopters

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/agent_benchmark/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/agent_benchmark/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-org/agent_benchmark/wiki)
- **Email**: support@your-org.com

---

**Status**: 🚧 In Development | **Version**: 1.0.0 | **Last Updated**: December 2024