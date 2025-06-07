# Detailed Project Structure and Architecture

## Framework-Isolated Project Architecture

The proposed project structure creates **complete framework isolation** while enabling **shared infrastructure within each framework ecosystem**. This architecture provides several key advantages for comprehensive framework comparison.

## Detailed Directory Structure

```
agent_benchmark/
├── README.md                          # Main project documentation
├── .gitignore                         # Global Git ignore rules
├── evaluation/                        # Cross-framework evaluation tools
│   ├── metrics_collector.py
│   ├── benchmark_runner.py
│   └── comparison_reports/
├── shared_datasets/                   # Common test data across all frameworks
│   ├── qa_datasets/
│   ├── rag_documents/
│   └── web_search_queries/
│
├── crewai/                            # CrewAI Framework Implementation
│   ├── pyproject.toml                 # CrewAI-specific dependencies
│   ├── uv.lock                        # Locked dependency versions
│   ├── docker-compose.yaml            # CrewAI infrastructure stack
│   ├── .env                           # Environment variables
│   ├── shared/                        # Framework-internal shared components
│   │   ├── __init__.py
│   │   ├── config.py                  # Common configuration
│   │   ├── utils.py                   # Shared utilities
│   │   ├── database.py                # Qdrant connection management
│   │   ├── tracing.py                 # Langfuse integration
│   │   └── mcp_client.py              # MCP protocol implementation
│   ├── task1_qa/                      # Question/Answering Implementation
│   │   ├── __init__.py
│   │   ├── main.py                    # Task entry point
│   │   ├── agents.py                  # CrewAI agents definition
│   │   ├── crews.py                   # Crew orchestration
│   │   ├── tools.py                   # Custom tools
│   │   └── evaluation.py             # Task-specific metrics
│   ├── task2_simple_rag/              # Simple RAG Implementation
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── agents.py
│   │   ├── document_processor.py      # Document ingestion
│   │   ├── retrieval.py               # Vector search logic
│   │   └── evaluation.py
│   ├── task3_agentic_rag/             # Agentic RAG Implementation
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── research_agent.py          # Specialized research agent
│   │   ├── synthesis_agent.py         # Information synthesis
│   │   ├── coordination.py            # Multi-agent coordination
│   │   └── evaluation.py
│   ├── task4_web_search/              # Web Search Integration
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── search_agents.py           # Web search agents
│   │   ├── verification_agent.py      # Fact verification
│   │   └── evaluation.py
│   ├── task5_multi_agent/             # Multi-Agent Collaboration
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── specialized_agents.py      # Role-specific agents
│   │   ├── workflows.py               # Collaboration workflows
│   │   └── evaluation.py
│   └── task6_advanced/                # Advanced Agentic Tasks
│       ├── __init__.py
│       ├── main.py
│       ├── multimedia_crew.py         # Content generation crew
│       ├── helpdesk_crew.py           # IT automation crew
│       └── evaluation.py
│
├── dspy/                              # DSPy Framework Implementation
│   ├── pyproject.toml                 # DSPy-specific dependencies
│   ├── uv.lock
│   ├── docker-compose.yaml
│   ├── .env
│   ├── shared/                        # Framework-internal shared components
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── programs.py                # DSPy compiled programs
│   │   ├── signatures.py              # DSPy signatures
│   │   ├── database.py
│   │   ├── tracing.py
│   │   └── mcp_client.py
│   ├── task1_qa/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── qa_signature.py            # DSPy QA signature
│   │   ├── compiled_program.py        # Optimized DSPy program
│   │   └── evaluation.py
│   ├── task2_simple_rag/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── retrieval_signature.py
│   │   ├── rag_program.py
│   │   └── evaluation.py
│   └── [similar structure for remaining tasks]
│
├── pocketflow/                        # PocketFlow Framework Implementation
│   ├── pyproject.toml                 # PocketFlow-specific dependencies
│   ├── uv.lock
│   ├── docker-compose.yaml
│   ├── .env
│   ├── shared/                        # Framework-internal shared components
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── graph_definitions.py       # Nested directed graphs
│   │   ├── api_discovery.py           # Dynamic API discovery
│   │   ├── database.py
│   │   ├── tracing.py
│   │   └── mcp_client.py
│   ├── task1_qa/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── qa_graph.py                # Question-answering graph
│   │   ├── pocket_ai_integration.py   # Pocket AI assistant
│   │   └── evaluation.py
│   └── [similar structure for remaining tasks]
│
├── google_adk/                        # Google ADK Framework Implementation
│   ├── pyproject.toml                 # Google ADK-specific dependencies
│   ├── uv.lock
│   ├── docker-compose.yaml
│   ├── .env
│   ├── shared/                        # Framework-internal shared components
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── orchestration.py           # ADK orchestration patterns
│   │   ├── state_management.py        # State handling
│   │   ├── database.py
│   │   ├── tracing.py
│   │   └── mcp_client.py
│   ├── task1_qa/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── agents.py                  # ADK agents
│   │   ├── tools.py                   # ADK tools
│   │   └── evaluation.py
│   └── [similar structure for remaining tasks]
│
└── pydantic_ai/                       # Pydantic AI Framework Implementation
    ├── pyproject.toml                 # Pydantic AI-specific dependencies
    ├── uv.lock
    ├── docker-compose.yaml
    ├── .env
    ├── shared/                        # Framework-internal shared components
    │   ├── __init__.py
    │   ├── config.py
    │   ├── type_definitions.py        # Pydantic models
    │   ├── validation.py              # Input/output validation
    │   ├── database.py
    │   ├── tracing.py
    │   └── mcp_client.py
    ├── task1_qa/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── agents.py                  # Type-safe agents
    │   ├── models.py                  # Pydantic data models
    │   └── evaluation.py
    └── [similar structure for remaining tasks]
```

## Framework Isolation Benefits

### Complete Dependency Isolation
Each framework maintains its **own dependency ecosystem**:
- **Independent pyproject.toml**: Framework-specific package versions and requirements
- **Isolated virtual environments**: No dependency conflicts between frameworks
- **Framework-specific optimizations**: Each can use optimal versions of supporting libraries
- **Version locking**: `uv.lock` ensures reproducible builds per framework

### Infrastructure Independence
Each framework deploys its **own infrastructure stack**:
- **Dedicated Qdrant instance**: Framework-specific vector database configuration
- **Isolated Langfuse deployment**: Separate observability stacks for clear attribution
- **Independent networking**: No port conflicts or service interference
- **Resource allocation**: Framework-specific resource limits and optimization

### Development Workflow Isolation
- **Parallel development**: Teams can work on different frameworks simultaneously
- **Independent testing**: Framework changes don't affect others
- **Deployment isolation**: Issues in one framework don't cascade
- **Configuration management**: Framework-specific environment variables and settings

## Shared Components Within Framework

### Common Infrastructure per Framework
Each framework's `docker-compose.yaml` includes:
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: "${FRAMEWORK_NAME}_qdrant"
    ports:
      - "${QDRANT_PORT}:6333"
    volumes:
      - ${FRAMEWORK_NAME}_qdrant_data:/qdrant/storage
    networks:
      - ${FRAMEWORK_NAME}_network

  langfuse:
    image: langfuse/langfuse:latest
    container_name: "${FRAMEWORK_NAME}_langfuse"
    ports:
      - "${LANGFUSE_PORT}:3000"
    environment:
      - DATABASE_URL=${LANGFUSE_DB_URL}
    networks:
      - ${FRAMEWORK_NAME}_network

  mcp_server:
    build: ./shared/mcp_server
    container_name: "${FRAMEWORK_NAME}_mcp"
    ports:
      - "${MCP_PORT}:8080"
    networks:
      - ${FRAMEWORK_NAME}_network

volumes:
  ${FRAMEWORK_NAME}_qdrant_data:
  ${FRAMEWORK_NAME}_postgres_data:

networks:
  ${FRAMEWORK_NAME}_network:
    driver: bridge
```

### Framework-Internal Shared Resources
The `shared/` directory within each framework provides:
- **Configuration Management**: Centralized settings for all tasks
- **Database Connections**: Unified Qdrant and Langfuse integration
- **Utility Functions**: Common helper functions and classes
- **MCP Client**: Standardized Model Context Protocol implementation
- **Evaluation Framework**: Consistent metrics collection across tasks

## Task Implementation Strategy

### Consistent Task Interface
Each task directory implements a **standardized interface**:
```python
# main.py structure for each task
from shared.config import get_config
from shared.database import get_qdrant_client
from shared.tracing import setup_langfuse
from shared.mcp_client import get_mcp_client

class TaskImplementation:
    def __init__(self):
        self.config = get_config()
        self.qdrant = get_qdrant_client()
        self.langfuse = setup_langfuse()
        self.mcp_client = get_mcp_client()
    
    def execute(self, input_data):
        # Framework-specific implementation
        pass
    
    def evaluate(self, results):
        # Task-specific evaluation
        pass
```

### Cross-Task Data Sharing
Within each framework, tasks can share:
- **Vector embeddings**: Reuse document embeddings across RAG tasks
- **Configuration**: Consistent LLM settings and API keys
- **Evaluation data**: Shared test datasets and benchmarks
- **Learned optimizations**: DSPy compiled programs can be reused

## Development and Deployment Workflow

### Framework-Specific Development
```bash
# Navigate to specific framework
cd crewai/

# Install dependencies using UV
uv sync

# Start framework infrastructure
docker-compose up -d

# Run specific task
cd task1_qa/
python main.py

# Run all tasks
python ../shared/run_all_tasks.py
```

### Cross-Framework Comparison
```bash
# From project root
python evaluation/benchmark_runner.py --frameworks all --tasks all
python evaluation/metrics_collector.py --generate-report
```

### Environment Management
Each framework maintains isolated environments:
- **Environment variables**: `.env` files with framework-specific settings
- **Port allocation**: Non-conflicting port ranges per framework
- **Data persistence**: Separate Docker volumes for data isolation
- **Logging**: Framework-specific log files and trace data

## Evaluation and Comparison Strategy

### Standardized Metrics Collection
Each framework implements identical evaluation interfaces:
- **Performance metrics**: Execution time, resource usage, API costs
- **Quality metrics**: Accuracy, relevance, completeness scores
- **Framework-specific metrics**: Utilization of unique features

### Cross-Framework Analysis
The root-level `evaluation/` directory provides:
- **Benchmark orchestration**: Run identical tests across all frameworks
- **Metrics aggregation**: Collect and normalize results for comparison
- **Report generation**: Automated comparative analysis reports
- **Statistical analysis**: Significance testing and confidence intervals

This architecture ensures **fair, isolated comparison** while maintaining **operational consistency** across the evaluation process, enabling robust framework assessment and selection guidance.