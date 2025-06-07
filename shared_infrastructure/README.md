# Shared Infrastructure for AI Agent Frameworks

This directory contains reusable infrastructure templates and tools for deploying isolated environments for each AI agent framework in the comparison project.

## 🎯 Overview

The shared infrastructure provides:

- **Docker Compose Templates**: Standardized infrastructure services (Qdrant, Langfuse, PostgreSQL)
- **Port Allocation Strategy**: Conflict-free port assignments across frameworks
- **External MCP Integration**: Documentation for using external MCP servers
- **Automation Tools**: Scripts for template customization and infrastructure validation
- **Monitoring & Health Checks**: Comprehensive service health monitoring

## 📁 Directory Structure

```
shared_infrastructure/
├── docker-compose.template.yaml    # Main infrastructure template
├── PORT_ALLOCATION.md             # Port allocation strategy
├── EXTERNAL_MCP_INTEGRATION.md    # MCP server integration guide
├── customize_template.py          # Template customization script
├── validate_infrastructure.py     # Infrastructure validation tools
└── README.md                      # This documentation
```

## 🚀 Quick Start

### 1. Customize Templates for a Framework

```bash
# Customize templates for a specific framework
cd shared_infrastructure/
python customize_template.py --framework dspy

# Customize all frameworks at once
python customize_template.py

# Check for port conflicts only
python customize_template.py --check-ports
```

### 2. Deploy Infrastructure

```bash
# Navigate to framework directory
cd ../dspy/

# Start infrastructure services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3. Validate Infrastructure Health

```bash
# Validate specific framework
cd shared_infrastructure/
python validate_infrastructure.py --framework dspy

# Validate all frameworks
python validate_infrastructure.py

# Generate detailed health report
python validate_infrastructure.py --output health_report.md
```

## 🏗️ Infrastructure Components

### Core Services

#### Qdrant Vector Database
- **Purpose**: Vector storage and similarity search
- **Image**: `qdrant/qdrant:latest`
- **Ports**: Framework-specific (6333-6337)
- **Health Check**: `http://localhost:{port}/health`

#### Langfuse Observability Platform
- **Purpose**: LLM tracing and observability
- **Image**: `langfuse/langfuse:latest`
- **Ports**: Framework-specific (3000-3004)
- **Health Check**: `http://localhost:{port}/api/public/health`

#### PostgreSQL Database
- **Purpose**: Backend for Langfuse
- **Image**: `postgres:15-alpine`
- **Ports**: Internal only (5432-5436)
- **Health Check**: `pg_isready` command

### External MCP Services

The project uses external MCP servers instead of custom implementations:

- **Web Search**: Brave Search, Tavily, DuckDuckGo MCP servers
- **Vector Search**: Official Qdrant MCP server
- **File Operations**: Official Filesystem MCP server
- **Repository Access**: GitHub MCP server

See [EXTERNAL_MCP_INTEGRATION.md](EXTERNAL_MCP_INTEGRATION.md) for detailed setup instructions.

## 🔧 Configuration

### Framework Port Allocation

Each framework uses dedicated ports to prevent conflicts:

| Framework   | Qdrant | Langfuse | PostgreSQL | Network Subnet |
|-------------|--------|----------|------------|----------------|
| DSPy        | 6334   | 3001     | 5433       | 172.21.0.0/16  |
| PocketFlow  | 6335   | 3002     | 5434       | 172.22.0.0/16  |
| CrewAI      | 6333   | 3000     | 5432       | 172.20.0.0/16  |
| Google ADK  | 6336   | 3003     | 5435       | 172.23.0.0/16  |
| Pydantic AI | 6337   | 3004     | 5436       | 172.24.0.0/16  |

### Environment Variables

Each framework requires these environment variables:

```bash
# Framework identification
FRAMEWORK_NAME=dspy

# Service ports
QDRANT_PORT=6334
LANGFUSE_PORT=3001

# Database configuration
POSTGRES_USER=langfuse_user
POSTGRES_PASSWORD=langfuse_password
LANGFUSE_DB_URL=postgresql://langfuse_user:langfuse_password@postgres:5432/langfuse

# Authentication secrets
LANGFUSE_NEXTAUTH_SECRET=your_nextauth_secret
LANGFUSE_SALT=your_salt_value

# Network configuration
NETWORK_SUBNET=21
```

## 🛠️ Tools and Scripts

### Template Customization Script

`customize_template.py` provides automated template customization:

**Features:**
- Variable substitution in Docker Compose templates
- Environment variable validation
- Port conflict detection
- Framework-specific configuration generation
- Backup creation for existing files

**Usage:**
```bash
# Basic usage
python customize_template.py --framework dspy

# Custom output directory
python customize_template.py --framework dspy --output-dir /custom/path

# Verbose output
python customize_template.py --framework dspy --verbose
```

### Infrastructure Validation Tool

`validate_infrastructure.py` provides comprehensive health checking:

**Features:**
- Service connectivity testing
- Database connection validation
- Vector database functionality checks
- Observability pipeline validation
- Health report generation

**Usage:**
```bash
# Basic validation
python validate_infrastructure.py --framework dspy

# JSON output
python validate_infrastructure.py --json

# Custom timeout
python validate_infrastructure.py --timeout 30

# Save report to file
python validate_infrastructure.py --output infrastructure_health.md
```

## 📋 Development Workflow

### Single Framework Development

```bash
# 1. Customize templates
cd shared_infrastructure/
python customize_template.py --framework dspy

# 2. Navigate to framework directory
cd ../dspy/

# 3. Start infrastructure
docker-compose up -d

# 4. Validate deployment
cd ../shared_infrastructure/
python validate_infrastructure.py --framework dspy

# 5. Develop and test your framework

# 6. Stop infrastructure when done
cd ../dspy/
docker-compose down
```

### Multi-Framework Development

```bash
# 1. Customize all templates
cd shared_infrastructure/
python customize_template.py

# 2. Start multiple frameworks
cd ../dspy/ && docker-compose up -d && cd ..
cd ../pocketflow/ && docker-compose up -d && cd ..
cd ../crewai/ && docker-compose up -d && cd ..

# 3. Validate all deployments
cd shared_infrastructure/
python validate_infrastructure.py

# 4. Access services at their respective ports
# DSPy Langfuse: http://localhost:3001
# PocketFlow Langfuse: http://localhost:3002
# CrewAI Langfuse: http://localhost:3000
```

## 🔍 Troubleshooting

### Common Issues

#### Port Conflicts
**Symptom**: Services fail to start with "port already in use" errors
**Solution**:
```bash
# Check for port conflicts
python customize_template.py --check-ports

# Find processes using specific ports
lsof -i :6334
netstat -tuln | grep 6334

# Stop conflicting services
docker-compose down  # In the conflicting framework directory
```

#### Service Health Check Failures
**Symptom**: Services start but health checks fail
**Solution**:
```bash
# Run detailed validation
python validate_infrastructure.py --framework dspy --verbose

# Check service logs
docker-compose logs qdrant
docker-compose logs langfuse
docker-compose logs postgres

# Restart services
docker-compose restart
```

#### Database Connection Issues
**Symptom**: Langfuse cannot connect to PostgreSQL
**Solution**:
```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Verify environment variables
cat .env | grep POSTGRES

# Test database connection manually
docker-compose exec postgres psql -U langfuse_user -d langfuse
```

### Network Connectivity Issues
**Symptom**: Services cannot communicate with each other
**Solution**:
```bash
# Check Docker networks
docker network ls | grep dspy

# Inspect network configuration
docker network inspect dspy_network

# Verify service discovery
docker-compose exec qdrant ping postgres
```

## 🔒 Security Considerations

### Default Credentials
- **Change default passwords** in production environments
- **Use strong secrets** for NextAuth and salt values
- **Limit network exposure** by binding services to localhost only

### Network Security
- **Framework isolation** prevents cross-framework communication
- **Dedicated networks** ensure service isolation
- **No external exposure** of internal services (PostgreSQL)

### Data Protection
- **Persistent volumes** ensure data survives container restarts
- **Regular backups** recommended for production data
- **Access controls** should be implemented for sensitive data

## 📊 Monitoring and Observability

### Health Monitoring
- **Automated health checks** for all services
- **Response time tracking** for performance monitoring
- **Service dependency validation** ensures proper startup order

### Logging
- **Structured logging** across all services
- **Centralized log collection** through Docker logging drivers
- **Log rotation** prevents disk space issues

### Metrics Collection
- **Service metrics** available through health endpoints
- **Resource usage** tracked through Docker stats
- **Custom metrics** can be added through Langfuse integration

## 🤝 Contributing

When modifying shared infrastructure:

1. **Test changes** across all frameworks
2. **Update documentation** for any new features
3. **Validate compatibility** with existing deployments
4. **Follow naming conventions** for consistency
5. **Add appropriate error handling** and logging

## 📚 Additional Resources

- [Port Allocation Strategy](PORT_ALLOCATION.md)
- [External MCP Integration Guide](EXTERNAL_MCP_INTEGRATION.md)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Langfuse Documentation](https://langfuse.com/docs)
