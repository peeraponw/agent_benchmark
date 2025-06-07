# Port Allocation Strategy

This document defines the port allocation strategy to prevent conflicts between framework infrastructure services.

## Framework Port Ranges

Each framework is allocated a specific range of ports to ensure complete isolation (ordered by priority):

### DSPy Framework (Priority 1 - Base: 6334, 3001, 5433)
- **Qdrant**: 6334
- **Langfuse**: 3001
- **PostgreSQL**: 5433
- **Network Subnet**: 172.21.0.0/16

### PocketFlow Framework (Priority 2 - Base: 6335, 3002, 5434)
- **Qdrant**: 6335
- **Langfuse**: 3002
- **PostgreSQL**: 5434
- **Network Subnet**: 172.22.0.0/16

### CrewAI Framework (Priority 3 - Base: 6333, 3000, 5432)
- **Qdrant**: 6333
- **Langfuse**: 3000
- **PostgreSQL**: 5432
- **Network Subnet**: 172.20.0.0/16

### Google ADK Framework (Priority 4 - Base: 6336, 3003, 5435)
- **Qdrant**: 6336
- **Langfuse**: 3003
- **PostgreSQL**: 5435
- **Network Subnet**: 172.23.0.0/16

### Pydantic AI Framework (Priority 5 - Base: 6337, 3004, 5436)
- **Qdrant**: 6337
- **Langfuse**: 3004
- **PostgreSQL**: 5436
- **Network Subnet**: 172.24.0.0/16

## Port Allocation Rules

### 1. Service-Specific Port Ranges
- **Qdrant**: 6333-6337 (Vector database)
- **Langfuse**: 3000-3004 (Observability web interface)
- **PostgreSQL**: 5432-5436 (Database backend)

### 2. External MCP Services
This project uses external MCP servers instead of custom implementations:
- **Web Search**: External MCP servers (Brave, Tavily, DuckDuckGo)
- **Vector Search**: Official Qdrant MCP server
- **File Operations**: Official Filesystem MCP server
- **Repository Access**: GitHub MCP server

### 2. Network Isolation
- Each framework uses a dedicated Docker network
- Network subnets are allocated sequentially: 172.20-24.0.0/16
- No cross-framework network communication allowed

### 3. Container Naming Convention
All containers follow the pattern: `{FRAMEWORK_NAME}_{SERVICE_NAME}`

Examples:
- `crewai_qdrant`
- `dspy_langfuse`
- `pocketflow_postgres`
- `google_adk_mcp`
- `pydantic_ai_qdrant`

### 4. Volume Naming Convention
All volumes follow the pattern: `{FRAMEWORK_NAME}_{SERVICE_NAME}_data`

Examples:
- `crewai_qdrant_data`
- `dspy_postgres_data`
- `pocketflow_langfuse_data`

## Environment Variable Mapping

Each framework's `.env.template` file includes:

```bash
# Framework identification
FRAMEWORK_NAME={framework_name}

# Port configuration
QDRANT_PORT={qdrant_port}
LANGFUSE_PORT={langfuse_port}
POSTGRES_PORT={postgres_port}  # Internal port, not exposed
MCP_PORT={mcp_port}

# Network configuration
NETWORK_SUBNET={subnet_number}
```

## Conflict Prevention

### 1. Port Checking
Before starting any framework infrastructure:
```bash
# Check if ports are available
netstat -tuln | grep -E ':(6333|6334|6335|6336|6337|3000|3001|3002|3003|3004|8080|8081|8082|8083|8084)'
```

### 2. Service Health Checks
All services include health checks to verify proper startup:
- **Qdrant**: `curl -f http://localhost:{port}/health`
- **Langfuse**: `curl -f http://localhost:{port}/api/public/health`
- **PostgreSQL**: `pg_isready -U {user} -d {database}`
- **MCP Server**: `curl -f http://localhost:{port}/health`

### 3. Graceful Shutdown
Use proper shutdown commands to free ports:
```bash
# Stop framework infrastructure
docker-compose down

# Remove volumes if needed
docker-compose down -v
```

## Development Workflow

### 1. Single Framework Development
```bash
cd {framework_name}/
docker-compose up -d
# Develop and test
docker-compose down
```

### 2. Multi-Framework Development
```bash
# Start multiple frameworks simultaneously
cd crewai/ && docker-compose up -d && cd ..
cd dspy/ && docker-compose up -d && cd ..
cd pocketflow/ && docker-compose up -d && cd ..

# Access services at their respective ports
# CrewAI Langfuse: http://localhost:3000
# DSPy Langfuse: http://localhost:3001
# PocketFlow Langfuse: http://localhost:3002
```

### 3. Port Conflict Resolution
If port conflicts occur:

1. **Check running services**:
   ```bash
   docker ps
   lsof -i :6333  # Check specific port
   ```

2. **Stop conflicting services**:
   ```bash
   docker-compose down  # In the conflicting framework directory
   ```

3. **Verify port availability**:
   ```bash
   telnet localhost 6333  # Should fail if port is free
   ```

## Monitoring and Troubleshooting

### 1. Service Status Check
```bash
# Check all framework services
for framework in crewai dspy pocketflow google_adk pydantic_ai; do
    echo "=== $framework ==="
    cd $framework
    docker-compose ps
    cd ..
done
```

### 2. Port Usage Summary
```bash
# Show all allocated ports
echo "Framework Port Usage:"
echo "CrewAI:     Qdrant:6333, Langfuse:3000, MCP:8080"
echo "DSPy:       Qdrant:6334, Langfuse:3001, MCP:8081"
echo "PocketFlow: Qdrant:6335, Langfuse:3002, MCP:8082"
echo "Google ADK: Qdrant:6336, Langfuse:3003, MCP:8083"
echo "Pydantic AI:Qdrant:6337, Langfuse:3004, MCP:8084"
```

### 3. Network Isolation Verification
```bash
# Verify network isolation
docker network ls | grep -E "(crewai|dspy|pocketflow|google_adk|pydantic_ai)"
```

This port allocation strategy ensures complete framework isolation while enabling parallel development and testing across all AI agent frameworks.
