"""
MCP (Model Context Protocol) Server
Provides standardized tool and resource access for AI agent frameworks
"""

import os
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="MCP Server",
    description="Model Context Protocol Server for AI Agent Frameworks",
    version="1.0.0"
)

class ToolRequest(BaseModel):
    """Request model for tool execution"""
    tool_name: str
    parameters: Dict[str, Any]

class ToolResponse(BaseModel):
    """Response model for tool execution"""
    success: bool
    result: Any
    error: str = None

class ResourceRequest(BaseModel):
    """Request model for resource access"""
    resource_uri: str
    parameters: Dict[str, Any] = {}

# Available tools registry
AVAILABLE_TOOLS = {
    "web_search": {
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {
            "query": {"type": "string", "description": "Search query"},
            "max_results": {"type": "integer", "description": "Maximum number of results", "default": 5}
        }
    },
    "file_read": {
        "name": "file_read", 
        "description": "Read content from shared datasets",
        "parameters": {
            "file_path": {"type": "string", "description": "Path to file in shared_datasets"}
        }
    },
    "vector_search": {
        "name": "vector_search",
        "description": "Search vectors in Qdrant database",
        "parameters": {
            "collection_name": {"type": "string", "description": "Qdrant collection name"},
            "query_vector": {"type": "array", "description": "Query vector"},
            "limit": {"type": "integer", "description": "Number of results", "default": 5}
        }
    }
}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "framework": os.getenv("FRAMEWORK_NAME", "unknown")}

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {"tools": list(AVAILABLE_TOOLS.values())}

@app.post("/tools/execute", response_model=ToolResponse)
async def execute_tool(request: ToolRequest):
    """Execute a tool through MCP protocol"""
    if request.tool_name not in AVAILABLE_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found")
    
    try:
        # Route to appropriate tool handler
        if request.tool_name == "web_search":
            result = await handle_web_search(request.parameters)
        elif request.tool_name == "file_read":
            result = await handle_file_read(request.parameters)
        elif request.tool_name == "vector_search":
            result = await handle_vector_search(request.parameters)
        else:
            raise HTTPException(status_code=501, detail=f"Tool '{request.tool_name}' not implemented")
        
        return ToolResponse(success=True, result=result)
    
    except Exception as e:
        return ToolResponse(success=False, result=None, error=str(e))

@app.get("/resources")
async def list_resources():
    """List available MCP resources"""
    resources = []
    
    # Scan shared_datasets directory
    datasets_path = "/app/shared_datasets"
    if os.path.exists(datasets_path):
        for root, dirs, files in os.walk(datasets_path):
            for file in files:
                if file.endswith(('.json', '.txt', '.md')):
                    rel_path = os.path.relpath(os.path.join(root, file), datasets_path)
                    resources.append({
                        "uri": f"dataset://{rel_path}",
                        "name": file,
                        "type": "file",
                        "description": f"Shared dataset file: {rel_path}"
                    })
    
    return {"resources": resources}

@app.post("/resources/access")
async def access_resource(request: ResourceRequest):
    """Access external resource through MCP"""
    try:
        if request.resource_uri.startswith("dataset://"):
            # Handle dataset resource access
            file_path = request.resource_uri.replace("dataset://", "")
            full_path = f"/app/shared_datasets/{file_path}"
            
            if not os.path.exists(full_path):
                raise HTTPException(status_code=404, detail=f"Resource not found: {request.resource_uri}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Try to parse as JSON if it's a JSON file
            if file_path.endswith('.json'):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    pass  # Return as string if JSON parsing fails
            
            return {"success": True, "content": content}
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported resource URI: {request.resource_uri}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tool handler functions
async def handle_web_search(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle web search tool execution"""
    # Placeholder implementation - would integrate with actual search API
    query = parameters.get("query", "")
    max_results = parameters.get("max_results", 5)
    
    return {
        "query": query,
        "results": [
            {
                "title": f"Mock result for: {query}",
                "url": "https://example.com",
                "snippet": f"This is a mock search result for the query: {query}"
            }
        ],
        "total_results": 1
    }

async def handle_file_read(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle file read tool execution"""
    file_path = parameters.get("file_path", "")
    full_path = f"/app/shared_datasets/{file_path}"
    
    if not os.path.exists(full_path):
        raise Exception(f"File not found: {file_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "file_path": file_path,
        "content": content,
        "size": len(content)
    }

async def handle_vector_search(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Handle vector search tool execution"""
    # Placeholder implementation - would integrate with Qdrant
    collection_name = parameters.get("collection_name", "")
    query_vector = parameters.get("query_vector", [])
    limit = parameters.get("limit", 5)
    
    return {
        "collection": collection_name,
        "query_vector_size": len(query_vector),
        "results": [],
        "message": "Vector search not yet implemented - placeholder response"
    }

if __name__ == "__main__":
    port = int(os.getenv("MCP_SERVER_PORT", 8080))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
