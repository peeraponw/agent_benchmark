# Master Plan: AI Agent Frameworks Comparison Project

## Project Overview

This project systematically compares five leading Python AI agent frameworks (DSPy, PocketFlow, CrewAI, Google ADK, and Pydantic AI) across six standardized use cases. The architecture ensures complete framework isolation while enabling fair comparison through shared infrastructure components and evaluation metrics.

**Current Status**: Phase 1 (Foundation Setup) is fully complete with significant enhancements beyond the original plan. The project has evolved to include sophisticated evaluation capabilities, external MCP integration, standardized OpenRouter-based LLM access, and comprehensive test datasets ready for framework evaluation.

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

### Step 1.2: Shared Global Components Development ✅ **COMPLETED**
**Objective**: Build reusable components that will be consistent across all frameworks.

**Status**: All major components have been implemented with significant enhancements beyond the original specification.

**Global Code Components Created:**

#### 1.2.1: Evaluation Framework (`evaluation/`) ✅ **IMPLEMENTED & ENHANCED**
**Status**: Fully implemented with comprehensive features including:
- Advanced performance monitoring with CPU/memory tracking
- Sophisticated cost tracking across multiple API providers
- Quality metrics for Q&A, RAG, and web search use cases
- Automated benchmark runners and comparative analysis
- Result aggregation and report generation

**Key Components**:
- `evaluation/base_evaluator.py` - Core evaluation interfaces
- `evaluation/evaluator.py` - Main evaluation orchestrator
- `evaluation/performance_monitor.py` - Resource usage tracking
- `evaluation/cost_tracker.py` - API cost calculation
- `evaluation/metrics/` - Use case-specific quality metrics
- `evaluation/benchmarks/` - Automated benchmark scripts

#### 1.2.2: Shared Dataset Manager (`shared_datasets/`) ✅ **IMPLEMENTED & ENHANCED**
**Status**: Fully implemented with advanced features including:
- Comprehensive dataset loading for Q&A, RAG, web search, and multi-agent scenarios
- Data validation and quality assurance
- Import/export capabilities with multiple formats (JSON, JSONL, CSV)
- Dataset statistics and analysis
- Compression and caching support

**Key Features**:
- `shared_datasets/dataset_manager.py` - Main dataset management class
- Support for multiple dataset types with validation
- Automatic data quality checks and statistics
- Flexible import/export with format conversion
- Comprehensive logging and error handling

#### 1.2.3: Common Infrastructure Templates ✅ **IMPLEMENTED & ENHANCED**
**Status**: Fully implemented with comprehensive infrastructure support including:
- Complete Docker Compose template with all required services
- Framework-specific port allocation strategy
- External MCP server integration documentation
- Health checks and resource management
- Network isolation and security configurations

**Key Components**:
- `shared_infrastructure/docker-compose.template.yaml` - Complete infrastructure template
- `shared_infrastructure/PORT_ALLOCATION.md` - Detailed port allocation strategy
- `shared_infrastructure/EXTERNAL_MCP_INTEGRATION.md` - MCP server integration guide
- Framework-specific `.env.template` files for all frameworks

**Major Architectural Decision**: The project has adopted **external MCP servers** instead of custom implementation, providing better reliability and maintenance.

### Step 1.3: Test Data Preparation ✅ **COMPLETED**
**Objective**: Create comprehensive, standardized datasets for all use cases.

**Status**: Fully completed with comprehensive datasets exceeding original requirements.

**Completed**:
- ✅ Dataset management infrastructure with validation
- ✅ Import/export capabilities for multiple formats
- ✅ Data quality assurance and statistics
- ✅ Framework for Q&A, RAG, web search, and multi-agent datasets
- ✅ Q&A dataset: 100 questions with complete answers across all categories
- ✅ RAG document collection: 50+ ground truth queries with 35+ documents
- ✅ Web search query sets: 75 diverse queries with verification criteria
- ✅ Multi-agent scenarios: 19 scenarios across complexity levels
- ✅ Comprehensive validation tools and quality metrics
- ✅ Complete dataset documentation and usage guides

**Achievements**:
- Comprehensive test data ready for framework evaluation
- Quality validation framework with automated checking
- Documentation with methodology and licensing information

## 🔄 Key Architectural Changes and Enhancements

### LLM Provider Standardization
**Decision**: Standardized on **OpenRouter** as the single LLM provider across all frameworks.
- **Default Model**: DeepSeek R1 for consistent testing
- **Alternative Models**: Claude Sonnet 4, Gemini 2.5 Pro available via environment configuration
- **Benefits**: Simplified API management, consistent cost tracking, unified access patterns

### External MCP Integration Strategy
**Decision**: Use external MCP servers instead of custom implementation.
- **Web Search**: Brave Search, Tavily, DuckDuckGo MCP servers
- **Vector Search**: Official Qdrant MCP server
- **File Operations**: Official Filesystem MCP server
- **Benefits**: Better reliability, reduced maintenance, community support

### Enhanced Evaluation Framework
**Enhancement**: Significantly expanded beyond original specification.
- **Performance Monitoring**: Real-time CPU/memory tracking
- **Cost Analysis**: Comprehensive API cost calculation
- **Quality Metrics**: Advanced metrics including BLEU, ROUGE, semantic similarity
- **Automated Benchmarking**: Complete benchmark suite with comparative analysis

### Framework Priority Order
**Established Priority**: Based on project goals and framework maturity.
1. **DSPy** (Highest Priority) - Programming framework for language models
2. **PocketFlow** - Nested directed graph framework
3. **CrewAI** - Multi-agent orchestration framework
4. **Google ADK** - Google's Agent Development Kit
5. **Pydantic AI** (Lowest Priority) - Type-safe agent framework

## Phase 2: Framework Infrastructure Setup ✅ **LARGELY COMPLETED**

### Step 2.1: Framework Directory Initialization ✅ **COMPLETED**
**Objective**: Set up isolated environments for each framework with proper dependency management.

**Status**: All frameworks have been initialized with standardized configurations.

**Completed for All Frameworks (DSPy, PocketFlow, CrewAI, Google ADK, Pydantic AI):**

#### 2.1.1: Environment Setup ✅ **COMPLETED**
**Status**: All frameworks have standardized UV-based environments with comprehensive configurations.

**Implemented Features**:
- ✅ UV project initialization for all frameworks
- ✅ Framework-specific `pyproject.toml` configurations
- ✅ Comprehensive `.env.template` files with:
  - Framework identification and port allocation
  - OpenRouter API configuration (standardized LLM access)
  - Infrastructure service configurations
  - Observability and monitoring settings
  - Security and performance configurations

**Key Enhancement**: Standardized on OpenRouter for LLM access instead of multiple providers:
```bash
# Standardized LLM Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEFAULT_LLM_MODEL=deepseek/deepseek-r1-0528  # Default across all frameworks
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

#### 2.1.2: Docker Infrastructure ✅ **COMPLETED**
**Status**: Complete infrastructure templates with framework-specific customizations.

**Implemented Features**:
- ✅ Comprehensive Docker Compose template with all required services
- ✅ Framework-specific port allocation (DSPy: 6334, PocketFlow: 6335, CrewAI: 6333, etc.)
- ✅ Network isolation with dedicated subnets per framework
- ✅ Health checks and resource management
- ✅ External MCP server integration documentation

**Infrastructure Services**:
- **Qdrant**: Vector database for embeddings and similarity search
- **Langfuse**: Observability platform for LLM tracing
- **PostgreSQL**: Backend database for Langfuse
- **External MCP Servers**: Web search, file operations, vector search capabilities

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

## 📊 Current Project Status Summary

### ✅ Completed Components (Phase 1 Complete)
1. **Infrastructure Foundation**: Complete Docker templates, port allocation, external MCP integration
2. **Evaluation Framework**: Sophisticated evaluation system with performance monitoring and cost tracking
3. **Dataset Management**: Advanced dataset manager with import/export and validation capabilities
4. **Framework Standardization**: All frameworks configured with OpenRouter and standardized environments
5. **Documentation**: Comprehensive guides for infrastructure, MCP integration, and port allocation
6. **Test Data**: Comprehensive datasets with 100+ Q&A pairs, 75+ web search queries, 50+ RAG scenarios, 19 multi-agent tasks
7. **Quality Validation**: Complete validation tools with automated checking and quality metrics

### 🚀 Ready for Phase 2
**Phase 1 Status**: ✅ FULLY COMPLETE - All foundation tasks finished

### 📋 Next Priority Tasks (Phase 2)
1. **Framework Implementation**: Begin use case development starting with DSPy (highest priority)
2. **Use Case Development**: Implement Q&A, RAG, web search, and multi-agent scenarios
3. **Integration Testing**: Validate framework isolation and infrastructure deployment
4. **Performance Benchmarking**: Execute comprehensive evaluation across all frameworks

### 🎯 Project Evolution
The project has evolved significantly beyond the original master plan with enhanced evaluation capabilities, external MCP integration, and standardized LLM access through OpenRouter. The foundation is now robust and ready for use case implementation across all frameworks.

This master plan provides a systematic approach to building the AI Agent Frameworks Comparison Project, ensuring thorough evaluation while maintaining framework isolation and enabling fair comparison. The enhanced infrastructure and evaluation capabilities position the project for comprehensive and reliable framework comparison.
