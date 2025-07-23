# USD MCP Server Setup Guide

## Configuration for Claude Desktop

The corrected configuration for Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "usd-mcp": {
      "command": "C:\\Users\\rudyc\\projects\\usd-ai\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\rudyc\\projects\\usd-ai\\usd-mcp\\server\\main.py"],
      "cwd": "C:\\Users\\rudyc\\projects\\usd-ai"
    }
  }
}
```

### Key Changes Made:
1. **Updated main.py**: Modified the main.py file to handle Python path resolution automatically
2. **Simplified Configuration**: Direct execution of main.py file with proper import handling
3. **Working Directory**: Set to the project root where dependencies are available

## Configuration for MCP Inspector

To test with MCP Inspector, use this command:

```bash
npx @modelcontextprotocol/inspector "C:\\Users\\rudyc\\projects\\usd-ai\\.venv\\Scripts\\python.exe" "C:\\Users\\rudyc\\projects\\usd-ai\\usd-mcp\\server\\main.py"
```

Or use the provided batch file `test_mcp_inspector.bat` for easier execution.

## Alternative Configuration Options

### Option 1: Using the script entry point (if installed)
If you've installed the package with `pip install -e .`, you can use:

```json
{
  "mcpServers": {
    "usd-mcp": {
      "command": "C:\\Users\\rudyc\\projects\\usd-ai\\.venv\\Scripts\\usd-mcp.exe",
      "args": [],
      "cwd": "C:\\Users\\rudyc\\projects\\usd-ai"
    }
  }
}
```

### Option 2: Direct Python execution
```json
{
  "mcpServers": {
    "usd-mcp": {
      "command": "C:\\Users\\rudyc\\projects\\usd-ai\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\rudyc\\projects\\usd-ai\\usd-mcp\\server\\main.py"],
      "cwd": "C:\\Users\\rudyc\\projects\\usd-ai"
    }
  }
}
```

## Troubleshooting

### Common Issues:
1. **Virtual Environment**: Ensure the virtual environment path is correct and activated
2. **Dependencies**: Make sure all dependencies are installed in the virtual environment
3. **Python Path**: Verify the Python executable path exists
4. **Working Directory**: The working directory should be the project root where pyproject.toml is located

### Testing the Server Manually:
```bash
cd "C:\\Users\\rudyc\\projects\\usd-ai"
.venv\\Scripts\\python.exe -c "import sys; sys.path.insert(0, 'C:\\Users\\rudyc\\projects\\usd-ai\\usd-mcp'); from server.server import server; server.run()"
```

### Installing Dependencies (if needed):
```bash
cd "C:\\Users\\rudyc\\projects\\usd-ai"
.venv\\Scripts\\pip install -r requirements.txt
```

## Available Tools

The USD MCP Server provides these tools:
- `load_usd_stage`: Load a USD file and return basic stage information
- `get_stage_hierarchy`: Get the complete prim hierarchy of a USD stage
- `inspect_prim`: Get detailed information about a specific USD prim
- `list_stage_prims`: List all prims in a USD stage with optional filtering
- `find_prims_by_name`: Find prims that match a specific name pattern