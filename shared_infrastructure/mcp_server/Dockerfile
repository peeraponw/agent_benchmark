# MCP Server Dockerfile
# Provides a standardized Model Context Protocol server for all frameworks

FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration first for better Docker layer caching
COPY pyproject.toml .

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy MCP server code
COPY . .

# Sync the project (install in editable mode if needed)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mcp_user && \
    chown -R mcp_user:mcp_user /app
USER mcp_user

# Expose MCP server port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start MCP server using uv run
CMD ["uv", "run", "python", "server.py"]
