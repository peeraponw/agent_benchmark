# Master Plan: AI Agent Frameworks Comparison Project

## Project Overview

This project will systematically compare five leading Python AI agent frameworks (DSPy, PocketFlow, CrewAI, Google ADK, and Pydantic AI) across six standardized use cases. The architecture ensures complete framework isolation while enabling fair comparison through shared infrastructure components and evaluation metrics.

## Phase 1: Foundation Setup (Weeks 1-2)

### Step 1.1: Repository Initialization and Global Structure
**Objective**: Create the foundational project structure with proper isolation boundaries.

**Tasks:**
1. **Initialize main repository** with the directory structure from `project_structure.md`
2. **Create global `.gitignore`** with framework-agnostic patterns
3. **Set up shared datasets directory** with placeholder subdirectories
4. **Initialize evaluation framework** at the root level

**Deliverables:**
- Complete directory structure matching the specification
- Global `.gitignore` file
- Root-level `README.md` with project overview

### Step 1.2: Shared Global Components Development
**Objective**: Build reusable components that will be consistent across all frameworks.

**Global Code Components to Create:**

#### 1.2.1: Evaluation Framework (`evaluation/`)
```python
# evaluation/base_evaluator.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class UseCaseResult(BaseModel):
    framework_name: str
    use_case_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    api_costs: Dict[str, float]
    quality_metrics: Dict[str, float]
    raw_output: Any
    metadata: Dict[str, Any]

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate_response_quality(self, expected: Any, actual: Any) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def measure_performance(self, execution_func) -> Dict[str, float]:
        pass
```

#### 1.2.2: Shared Dataset Manager (`shared_datasets/`)
```python
# shared_datasets/dataset_manager.py
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel

class DatasetItem(BaseModel):
    id: str
    input_data: Any
    expected_output: Any
    metadata: Dict[str, Any]

class DatasetManager:
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
    
    def load_qa_dataset(self) -> List[DatasetItem]:
        """Load standardized Q&A test data"""
        pass
    
    def load_rag_documents(self) -> List[Dict[str, Any]]:
        """Load documents for RAG testing"""
        pass
```

#### 1.2.3: Common Infrastructure Templates
Create template files that each framework will customize:

```yaml
# shared_infrastructure/docker-compose.template.yaml
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
    depends_on:
      - postgres
    networks:
      - ${FRAMEWORK_NAME}_network

  postgres:
    image: postgres:15
    container_name: "${FRAMEWORK_NAME}_postgres"
    environment:
      - POSTGRES_DB=langfuse
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ${FRAMEWORK_NAME}_postgres_data:/var/lib/postgresql/data
    networks:
      - ${FRAMEWORK_NAME}_network

volumes:
  ${FRAMEWORK_NAME}_qdrant_data:
  ${FRAMEWORK_NAME}_postgres_data:

networks:
  ${FRAMEWORK_NAME}_network:
    driver: bridge
```

### Step 1.3: Test Data Preparation
**Objective**: Create comprehensive, standardized datasets for all use cases.

**Tasks:**
1. **Q&A Dataset Creation**:
   - Compile 100+ question-answer pairs across different categories
   - Include factual, reasoning, and contextual questions
   - Add difficulty levels and expected response types

2. **RAG Document Collection**:
   - Gather diverse document types (PDF, text, markdown)
   - Create ground truth for expected retrievals
   - Prepare both simple and complex multi-document scenarios

3. **Web Search Query Sets**:
   - Design queries requiring real-time information
   - Include fact-checking scenarios
   - Prepare expected source verification cases

4. **Multi-Agent Use Case Definitions**:
   - Define research pipeline scenarios
   - Create customer service simulation data
   - Prepare content creation workflows

**Deliverables:**
- Structured datasets in `shared_datasets/`
- Documentation for each dataset's purpose and structure
- Validation scripts to ensure data quality

## Phase 2: Framework Infrastructure Setup (Weeks 3-4)

### Step 2.1: Framework Directory Initialization
**Objective**: Set up isolated environments for each framework with proper dependency management.

**For Each Framework (DSPy, PocketFlow, CrewAI, Google ADK, Pydantic AI):**

#### 2.1.1: Environment Setup
1. **Navigate to framework directory** (e.g., `crewai/`)
2. **Initialize UV project**:
   ```bash
   cd crewai/
   uv init --python 3.11
   ```
3. **Configure `pyproject.toml`** with framework-specific dependencies:
   ```toml
   [project]
   name = "dspy-comparison"
   version = "0.1.0"
   requires-python = ">=3.11"
   dependencies = [
       "dspy-ai>=2.0.0",
       "pydantic>=2.0.0",
       "qdrant-client>=1.7.0",
       "langfuse>=2.0.0",
       # Add framework-specific dependencies
   ]
   ```

4. **Create framework-specific environment file**:
   ```bash
   # .env template for each framework
   FRAMEWORK_NAME=dspy
   QDRANT_PORT=6334
   LANGFUSE_PORT=3001
   POSTGRES_USER=langfuse_user
   POSTGRES_PASSWORD=langfuse_password
   LANGFUSE_DB_URL=postgresql://langfuse_user:langfuse_password@postgres:5432/langfuse
   
   # API Keys (will be filled during implementation)
   OPENAI_API_KEY=
   ANTHROPIC_API_KEY=
   GOOGLE_API_KEY=
   ```

#### 2.1.2: Docker Infrastructure
1. **Copy and customize docker-compose template**:
   - Replace placeholder values with framework-specific configurations
   - Adjust port numbers to prevent conflicts (DSPy: 6334, PocketFlow: 6335, CrewAI: 6333, etc.)
   - Set unique container names and volume names

2. **Test infrastructure deployment**:
   ```bash
   docker-compose up -d
   docker-compose ps  # Verify all services are running
   ```

### Step 2.2: Shared Framework Components
**Objective**: Create the `shared/` directory within each framework with common utilities.

**For Each Framework, Create:**

#### 2.2.1: Configuration Management (`shared/config.py`)
```python
from pydantic import BaseSettings
from typing import Dict, Any

class FrameworkConfig(BaseSettings):
    framework_name: str
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str = "http://localhost:3000"
    
    # LLM API configurations
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    
    class Config:
        env_file = ".env"

def get_config() -> FrameworkConfig:
    return FrameworkConfig()
```

#### 2.2.2: Database Integration (`shared/database.py`)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from typing import Optional

class QdrantManager:
    def __init__(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)
    
    def create_collection(self, collection_name: str, vector_size: int):
        """Create a new collection with specified vector dimensions"""
        pass
    
    def upsert_vectors(self, collection_name: str, vectors: list, payloads: list):
        """Insert or update vectors with metadata"""
        pass
    
    def search_similar(self, collection_name: str, query_vector: list, limit: int = 5):
        """Perform similarity search"""
        pass

def get_qdrant_client() -> QdrantManager:
    config = get_config()
    return QdrantManager(config.qdrant_host, config.qdrant_port)
```

#### 2.2.3: Observability Setup (`shared/tracing.py`)
```python
from langfuse import Langfuse
from typing import Any, Dict

class TracingManager:
    def __init__(self, public_key: str, secret_key: str, host: str):
        self.langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host
        )
    
    def create_trace(self, name: str, metadata: Dict[str, Any]):
        """Create a new trace for task execution"""
        pass
    
    def log_generation(self, trace_id: str, input_data: Any, output_data: Any, model: str):
        """Log LLM generation within a trace"""
        pass
    
    def finalize_trace(self, trace_id: str, metrics: Dict[str, float]):
        """Complete trace with final metrics"""
        pass

def setup_langfuse() -> TracingManager:
    config = get_config()
    return TracingManager(
        config.langfuse_public_key,
        config.langfuse_secret_key,
        config.langfuse_host
    )
```

#### 2.2.4: MCP Client (`shared/mcp_client.py`)
```python
from typing import Dict, Any, List

class MCPClient:
    """Model Context Protocol client for standardized tool interactions"""
    
    def __init__(self):
        self.available_tools: Dict[str, Any] = {}
        self.available_resources: Dict[str, Any] = {}
    
    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available MCP tools"""
        pass
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool through MCP protocol"""
        pass
    
    def access_resource(self, resource_uri: str) -> Any:
        """Access external resource through MCP"""
        pass

def get_mcp_client() -> MCPClient:
    return MCPClient()
```

### Step 2.3: Use Case Structure Template
**Objective**: Create standardized use case directories with consistent interfaces.

**For Each Framework, Create Use Case Template Structure:**

```python
# Template for each use case's main.py
from abc import ABC, abstractmethod
from typing import Any, Dict
from shared.config import get_config
from shared.database import get_qdrant_client
from shared.tracing import setup_langfuse
from shared.mcp_client import get_mcp_client

class BaseUseCase(ABC):
    def __init__(self):
        self.config = get_config()
        self.qdrant = get_qdrant_client()
        self.langfuse = setup_langfuse()
        self.mcp_client = get_mcp_client()
        self.use_case_name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute the main use case logic"""
        pass

    @abstractmethod
    def evaluate(self, input_data: Any, output_data: Any) -> Dict[str, float]:
        """Evaluate use case performance"""
        pass

    def run_with_tracing(self, input_data: Any) -> Dict[str, Any]:
        """Execute use case with full observability"""
        trace = self.langfuse.create_trace(
            name=f"{self.config.framework_name}_{self.use_case_name}",
            metadata={"framework": self.config.framework_name, "use_case": self.use_case_name}
        )
        
        try:
            result = self.execute(input_data)
            metrics = self.evaluate(input_data, result)
            
            self.langfuse.finalize_trace(trace.id, metrics)
            
            return {
                "result": result,
                "metrics": metrics,
                "trace_id": trace.id
            }
        except Exception as e:
            self.langfuse.finalize_trace(trace.id, {"error": str(e)})
            raise
```

## Phase 3: Use Case Implementation (Weeks 5-9)

### Step 3.1: Use Case Implementation Strategy
**Objective**: Implement each use case across all frameworks following a systematic approach.

**Implementation Order:**
1. **Use Case 1: Q&A System** (Week 5) - Simplest use case to validate infrastructure
2. **Use Case 2: Simple RAG** (Week 6) - Builds on Q&A, introduces vector operations
3. **Use Case 4: Web Search** (Week 7) - Independent use case, tests external integrations
4. **Use Case 3: Agentic RAG** (Week 8) - Complex use case building on Simple RAG
5. **Use Case 5: Multi-Agent** (Week 9) - Tests framework collaboration features
6. **Use Case 6: Advanced Use Cases** (Week 9) - Showcase framework-specific strengths

### Step 3.2: Use Case Implementation Process
**For Each Use Case, Follow This Process:**

#### 3.2.1: Requirements Analysis
1. **Review use case specification** from PRD2.md
2. **Identify framework-specific approaches** for implementation
3. **Define success criteria** and evaluation metrics
4. **Plan testing strategy** with shared datasets

#### 3.2.2: Implementation Workflow
1. **Create use case directory structure** in each framework
2. **Implement framework-specific logic** following each framework's patterns
3. **Integrate with shared infrastructure** (Qdrant, Langfuse, MCP)
4. **Add comprehensive error handling** and logging

#### 3.2.3: Validation Process
1. **Run against shared test datasets** to ensure consistency
2. **Collect performance metrics** through Langfuse
3. **Validate framework isolation** - ensure no cross-contamination
4. **Document implementation decisions** and framework-specific optimizations

### Step 3.3: Cross-Framework Consistency Checks
**Objective**: Ensure fair comparison across frameworks.

**Consistency Requirements:**
1. **Same input datasets** for all frameworks
2. **Identical evaluation criteria** and metrics
3. **Comparable infrastructure resources** (memory, CPU limits)
4. **Consistent API usage patterns** where possible
5. **Standardized output formats** for comparison

## Phase 4: Evaluation and Analysis (Weeks 10-12)

### Step 4.1: Automated Benchmarking System
**Objective**: Create comprehensive evaluation automation.

#### 4.1.1: Benchmark Runner (`evaluation/benchmark_runner.py`)
```python
from typing import List, Dict, Any
import asyncio
import json
from pathlib import Path

class BenchmarkRunner:
    def __init__(self, frameworks: List[str], tasks: List[str]):
        self.frameworks = frameworks
        self.tasks = tasks
        self.results: Dict[str, Any] = {}
    
    async def run_all_benchmarks(self) -> Dict[str, Any]:
        """Execute all task-framework combinations"""
        pass
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Aggregate performance metrics from Langfuse"""
        pass
    
    def generate_comparison_report(self) -> None:
        """Create comprehensive comparison analysis"""
        pass
```

### Step 4.2: Performance Analysis
**Objective**: Analyze quantitative metrics across frameworks.

**Metrics to Collect:**
1. **Execution Time**: Use case completion latency
2. **Resource Usage**: CPU, memory, network utilization
3. **API Costs**: LLM API call expenses
4. **Accuracy Scores**: Use case-specific quality metrics
5. **Scalability Metrics**: Performance under load

### Step 4.3: Qualitative Assessment
**Objective**: Evaluate developer experience and framework characteristics.

**Assessment Areas:**
1. **Ease of Implementation**: Learning curve and development speed
2. **Code Maintainability**: Framework abstractions and modularity
3. **Documentation Quality**: Available resources and examples
4. **Community Support**: Ecosystem and community activity
5. **Production Readiness**: Enterprise deployment considerations

### Step 4.4: Reporting and Documentation
**Objective**: Create comprehensive project deliverables.

**Final Deliverables:**
1. **Comparative Analysis Report**: Detailed framework comparison with recommendations
2. **Performance Benchmark Results**: Quantitative metrics and analysis
3. **Implementation Guide**: Best practices for each framework
4. **Production Deployment Guide**: Enterprise considerations and strategies

## Development Guidelines and Best Practices

### Code Quality Standards
1. **Type Hints**: Use comprehensive type annotations
2. **Error Handling**: Implement robust exception handling
4. **Documentation**: Document all public APIs and complex logic
5. **Logging**: Implement structured logging throughout

### Framework Isolation Enforcement
1. **No Shared Dependencies**: Each framework maintains independent dependencies
2. **Port Isolation**: Use different ports for each framework's services
3. **Data Isolation**: Separate vector collections and trace data
4. **Environment Separation**: Framework-specific environment variables

### Monitoring and Observability
1. **Comprehensive Tracing**: Capture all LLM interactions
2. **Resource Monitoring**: Track system resource usage
3. **Error Tracking**: Log and analyze all failures
4. **Performance Metrics**: Measure and compare execution times

This master plan provides a systematic approach to building the AI Agent Frameworks Comparison Project, ensuring thorough evaluation while maintaining framework isolation and enabling fair comparison. Each step includes clear objectives, deliverables, and quality standards that junior developers can follow successfully.
