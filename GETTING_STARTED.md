# Getting Started Guide

Welcome to the AI Agent Frameworks Comparison Project! This guide will help you quickly set up and start exploring the different AI agent frameworks.

## 🚀 Quick Setup (5 minutes)

### Prerequisites Check

Before starting, ensure you have:

```bash
# Check Python version (3.11+ required)
python --version

# Check UV installation
uv --version

# Check Docker installation
docker --version
docker-compose --version

# Check Git
git --version
```

If any tools are missing, see the [Installation Guide](#installation-guide) below.

### 1. Clone and Navigate

```bash
git clone https://github.com/your-org/agent_benchmark.git
cd agent_benchmark
```

### 2. Choose Your Framework

Pick one framework to start with (in priority order):

```bash
# Priority 1: DSPy (programming framework for LMs - HIGHEST PRIORITY)
cd dspy/

# Priority 2: PocketFlow (nested directed graph framework)
cd pocketflow/

# Priority 3: CrewAI (multi-agent orchestration framework)
cd crewai/

# Priority 4: Google ADK (Google's Agent Development Kit)
cd google_adk/

# Priority 5: Pydantic AI (type-safe agent framework - LOWEST PRIORITY)
cd pydantic_ai/
```

### 3. Setup Environment

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.template .env

# Edit OpenRouter API key (optional for basic testing)
nano .env
```

### 4. Start Infrastructure

```bash
# Start required services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 5. Run Your First Use Case

```bash
# Navigate to Q&A use case
cd usecase1_qa/

# Run the use case
uv run python main.py

# Check results
ls -la outputs/
```

🎉 **Congratulations!** You've successfully run your first AI agent use case.

## 📋 What's Next?

### Explore More Use Cases

```bash
# Try different use cases
cd ../usecase2_simple_rag/
uv run python main.py

cd ../usecase4_web_search/
uv run python main.py
```

### Compare Frameworks

```bash
# Return to project root
cd ../../

# Run comparison across frameworks (start with highest priority)
python evaluation/benchmark_runner.py --frameworks dspy,pocketflow --use-cases qa

# Generate comparison report
python evaluation/report_generator.py
```

### Customize and Experiment

```bash
# Modify use case parameters (using highest priority framework)
nano dspy/usecase1_qa/config.yaml

# Add your own test data
nano shared_datasets/qa/questions.json

# Re-run with custom data
cd dspy/usecase1_qa/
uv run python main.py
```

## 🛠️ Installation Guide

### Python 3.11+

**macOS (using Homebrew):**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) or use Windows Store.

### UV Package Manager

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Verify installation
uv --version
```

### Docker and Docker Compose

**macOS:**
```bash
# Install Docker Desktop
brew install --cask docker
```

**Ubuntu/Debian:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin
```

**Windows:**
Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/).

## 🔧 Configuration Guide

### Environment Variables

Each framework requires specific environment variables:

```bash
# Framework identification (example using highest priority framework)
FRAMEWORK_NAME=dspy

# Infrastructure ports (adjust to avoid conflicts)
QDRANT_PORT=6333
LANGFUSE_PORT=3000
MCP_PORT=8080

# Database configuration
POSTGRES_USER=langfuse_user
POSTGRES_PASSWORD=your_secure_password
LANGFUSE_DB_URL=postgresql://langfuse_user:your_secure_password@postgres:5432/langfuse

# OpenRouter API Key (single LLM provider)
OPENROUTER_API_KEY=sk-or-your-openrouter-api-key-here
```

### Port Management

To run multiple frameworks simultaneously, use different ports:

| Framework | Qdrant | Langfuse | MCP | Postgres | Priority |
|-----------|--------|----------|-----|----------|----------|
| DSPy | 6334 | 3001 | 8081 | 5433 | 🥇 1st |
| PocketFlow | 6335 | 3002 | 8082 | 5434 | 🥈 2nd |
| CrewAI | 6333 | 3000 | 8080 | 5432 | 🥉 3rd |
| Google ADK | 6336 | 3003 | 8083 | 5435 | 4th |
| Pydantic AI | 6337 | 3004 | 8084 | 5436 | 5th |

### OpenRouter API Setup

**Single LLM Provider Configuration**

1. **OpenRouter API Key**
   - Visit [openrouter.ai](https://openrouter.ai/)
   - Create an account and generate API key
   - Add to `.env` file as `OPENROUTER_API_KEY`

2. **Available Models via OpenRouter**
   - **DeepSeek R1**: `deepseek/deepseek-r1-0528` [DEFAULT]
   - **Claude Sonnet 4**: `anthropic/claude-sonnet-4`
   - **Google Gemini 2.5 Pro**: `google/gemini-2.5-pro-preview`

3. **Model Switching for Comparisons**
   - **Default Testing**: All frameworks use DeepSeek R1 for consistent baseline testing
   - **Easy Switching**: Change `DEFAULT_LLM_MODEL` in `.env` to test different models
   - **Framework Comparison**: Compare same framework with different models
   - **Cross-Framework Studies**: Test different frameworks with same model

4. **Benefits of OpenRouter**
   - Single API key for multiple LLM providers
   - Unified interface and billing
   - Automatic failover and load balancing
   - Cost optimization across providers

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the port
lsof -i :6333

# Kill the process or change port in .env
```

**2. Docker Services Not Starting**
```bash
# Check Docker daemon
docker info

# Restart Docker services
docker-compose down
docker-compose up -d
```

**3. UV Dependencies Issues**
```bash
# Clear UV cache
uv cache clean

# Reinstall dependencies
rm uv.lock
uv sync
```

**4. Permission Errors**
```bash
# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Fix file permissions
chmod +x scripts/*.sh
```

### Getting Help

**Check Logs:**
```bash
# Framework logs
docker-compose logs

# Specific service logs
docker-compose logs qdrant
docker-compose logs langfuse
```

**Validate Setup:**
```bash
# Run validation script
python scripts/validate_setup.py

# Check framework health (example using highest priority framework)
python scripts/health_check.py --framework dspy
```

**Community Support:**
- [GitHub Issues](https://github.com/your-org/agent_benchmark/issues)
- [GitHub Discussions](https://github.com/your-org/agent_benchmark/discussions)
- [Project Wiki](https://github.com/your-org/agent_benchmark/wiki)

## 📚 Next Steps

### Learn More
- [Architecture Guide](ARCHITECTURE.md) - Understand the system design
- [Framework Guides](docs/frameworks/) - Deep dive into each framework
- [Use Case Documentation](docs/use_cases/) - Detailed use case descriptions
- [Evaluation Guide](docs/evaluation/) - Understanding metrics and benchmarks

### Contribute
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Development Setup](docs/development/) - Advanced development setup
- [Testing Guide](docs/testing/) - Running and writing tests

### Advanced Usage
- [Custom Use Cases](docs/custom_use_cases.md) - Creating new evaluation use cases
- [Framework Integration](docs/integration.md) - Adding new frameworks
- [Production Deployment](docs/deployment.md) - Enterprise deployment guide

---

**Need help?** Don't hesitate to [open an issue](https://github.com/your-org/agent_benchmark/issues) or start a [discussion](https://github.com/your-org/agent_benchmark/discussions)!
