# External MCP Server Integration Guide

This project uses external Model Context Protocol (MCP) servers instead of custom implementations to provide web search, vector search, and file access capabilities to AI agent frameworks.

## 🎯 Recommended MCP Servers

### Web Search Capabilities
- **Brave Search MCP**: Privacy-focused search with no tracking
  ```bash
  uvx mcp-server-brave-search
  ```

- **Tavily Search MCP**: Premium search with enhanced features
  ```bash
  uvx mcp-server-tavily
  ```

- **DuckDuckGo MCP**: No API key required, privacy-focused
  ```bash
  uvx mcp-server-duckduckgo
  ```

### Vector Search Integration
- **Official Qdrant MCP**: Direct integration with Qdrant vector database
  ```bash
  uvx mcp-server-qdrant --host localhost --port 6334
  ```

- **Typesense MCP**: Alternative vector search capabilities
  ```bash
  uvx mcp-server-typesense
  ```

### File Operations
- **Official Filesystem MCP**: Secure file access with sandboxing
  ```bash
  uvx mcp-server-filesystem --allowed-dirs /path/to/shared_datasets
  ```

- **GitHub MCP**: Repository access and code search
  ```bash
  uvx mcp-server-github
  ```

## 🔧 Framework-Specific Integration

### DSPy Framework (Priority 1)
```bash
# Start required MCP servers for DSPy
uvx mcp-server-qdrant --host localhost --port 6334
uvx mcp-server-filesystem --allowed-dirs ./shared_datasets
uvx mcp-server-brave-search

# Configure DSPy to use external MCP services
cd dspy/
# Update configuration to point to external MCP endpoints
```

### PocketFlow Framework (Priority 2)
```bash
# PocketFlow benefits from graph-based search capabilities
uvx mcp-server-github  # For code repository access
uvx mcp-server-qdrant --host localhost --port 6335
uvx mcp-server-tavily  # Enhanced search for graph workflows
```

### CrewAI Framework (Priority 3)
```bash
# Multi-agent coordination benefits from diverse search capabilities
uvx mcp-server-brave-search
uvx mcp-server-filesystem --allowed-dirs ./shared_datasets
uvx mcp-server-qdrant --host localhost --port 6333
```

### Google ADK Framework (Priority 4)
```bash
# Enterprise-focused MCP integration
uvx mcp-server-qdrant --host localhost --port 6336
uvx mcp-server-filesystem --allowed-dirs ./shared_datasets
uvx mcp-server-brave-search
```

### Pydantic AI Framework (Priority 5)
```bash
# Type-safe integration with MCP services
uvx mcp-server-filesystem --allowed-dirs ./shared_datasets
uvx mcp-server-qdrant --host localhost --port 6337
uvx mcp-server-duckduckgo
```

## 🚀 Quick Setup

### 1. Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Required MCP Servers
```bash
# Essential MCP servers for all frameworks
uvx mcp-server-filesystem
uvx mcp-server-brave-search
uvx mcp-server-qdrant

# Optional enhanced capabilities
uvx mcp-server-github
uvx mcp-server-tavily
```

### 3. Configure Claude Desktop (Optional)
Add MCP servers to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "--allowed-dirs", "/path/to/shared_datasets"]
    },
    "brave-search": {
      "command": "uvx", 
      "args": ["mcp-server-brave-search"]
    },
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant", "--host", "localhost", "--port", "6334"]
    }
  }
}
```

## 🔒 Security Considerations

### File Access Security
- Always use `--allowed-dirs` parameter to restrict filesystem access
- Never allow access to system directories or sensitive files
- Use read-only access when possible

### API Key Management
- Store API keys securely using environment variables
- Use different API keys for different environments (dev/staging/prod)
- Rotate API keys regularly

### Network Security
- Run MCP servers on localhost only for local development
- Use proper authentication for production deployments
- Monitor MCP server logs for suspicious activity

## 📊 Performance Optimization

### Caching Strategies
- Enable caching for search results to reduce API calls
- Use local caching for frequently accessed files
- Implement TTL (Time To Live) for cached data

### Resource Management
- Monitor memory usage of MCP servers
- Set appropriate timeouts for external API calls
- Use connection pooling for database connections

## 🛠️ Development Workflow

### Local Development
```bash
# Start infrastructure services
docker-compose up -d

# Start required MCP servers in separate terminals
uvx mcp-server-filesystem --allowed-dirs ./shared_datasets
uvx mcp-server-qdrant --host localhost --port 6334
uvx mcp-server-brave-search

# Run framework tests
cd dspy/
uv run python tasks/qa_task.py
```

### Testing MCP Integration
```bash
# Test MCP server connectivity
curl http://localhost:8080/health  # If running HTTP MCP server

# Test file access
uvx mcp-server-filesystem --test-mode

# Test search capabilities
uvx mcp-server-brave-search --test-query "AI agent frameworks"
```

## 📚 Additional Resources

### Official MCP Documentation
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [MCP Examples and Tutorials](https://modelcontextprotocol.io/examples)

### Community Resources
- [MCP Index - Server Directory](https://mcpindex.net/)
- [Awesome MCP Servers](https://mcpservers.org/)
- [MCP Hub - Community Servers](https://www.mcphub.ai/servers)

### Framework-Specific Integration Guides
- DSPy: See `dspy/docs/mcp_integration.md`
- PocketFlow: See `pocketflow/docs/mcp_setup.md`
- CrewAI: See `crewai/docs/external_tools.md`
- Google ADK: See `google_adk/docs/mcp_configuration.md`
- Pydantic AI: See `pydantic_ai/docs/tool_integration.md`

## 🔄 Migration from Custom MCP

If you previously used the custom MCP server implementation:

1. **Remove custom MCP references** from Docker Compose files
2. **Update environment variables** to remove MCP_PORT configurations
3. **Install external MCP servers** using the commands above
4. **Update framework configurations** to use external MCP endpoints
5. **Test integration** with each framework to ensure functionality

This approach provides better maintainability, security, and feature coverage compared to custom MCP implementations.
