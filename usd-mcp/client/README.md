# USD MCP Client

A Python client for interacting with the USD MCP Server using the Model Context Protocol (MCP).

## Installation

1. Make sure you have the Python virtual environment activated:

```bash
# From the project root directory
cd C:\Users\rudyc\projects\usd-ai
.\.venv\Scripts\activate
```

2. Install the client requirements:

```bash
cd usd-mcp\client
pip install -r requirements.txt
```

## Usage

### Asynchronous Client

```python
import asyncio
from client import USDMCPClient

async def main():
    # Create a client with the path to the server script
    server_script_path = "path/to/server/main.py"
    client = USDMCPClient(server_script_path)
    
    try:
        # Connect to the server
        server_info = await client.connect()
        print(f"Connected to {server_info['name']}")
        print(f"Available tools: {server_info['tools']}")
        
        # Load a USD stage
        file_path = r"C:\path\to\your\file.usda"
        stage_info = await client.load_usd_stage(file_path)
        print(f"Loaded stage with {stage_info['prim_count']} prims")
        
        # Get the stage hierarchy
        hierarchy = await client.get_stage_hierarchy(file_path, max_depth=2)
        print(f"Stage hierarchy: {hierarchy}")
        
        # Inspect a prim
        prim_info = await client.inspect_prim(file_path, "/hello")
        print(f"Prim info: {prim_info}")
        
        # List stage prims
        prims = await client.list_stage_prims(file_path, prim_type="Xform")
        print(f"Found {len(prims['prims'])} prims of type Xform")
        
        # Find prims by name
        found_prims = await client.find_prims_by_name(file_path, "hello")
        print(f"Found {len(found_prims['prims'])} prims with name 'hello'")
    
    finally:
        # Close the client
        await client.close()

# Run the async function
asyncio.run(main())
```

### Synchronous Client

```python
from client import USDMCPClientSync

# Create a client with the path to the server script
server_script_path = "path/to/server/main.py"
client = USDMCPClientSync(server_script_path)

try:
    # Connect to the server
    server_info = client.connect()
    print(f"Connected to {server_info['name']}")
    print(f"Available tools: {server_info['tools']}")
    
    # Load a USD stage
    file_path = r"C:\path\to\your\file.usda"
    stage_info = client.load_usd_stage(file_path)
    print(f"Loaded stage with {stage_info['prim_count']} prims")
    
    # Get the stage hierarchy
    hierarchy = client.get_stage_hierarchy(file_path, max_depth=2)
    print(f"Stage hierarchy: {hierarchy}")
    
    # Inspect a prim
    prim_info = client.inspect_prim(file_path, "/hello")
    print(f"Prim info: {prim_info}")
    
    # List stage prims
    prims = client.list_stage_prims(file_path, prim_type="Xform")
    print(f"Found {len(prims['prims'])} prims of type Xform")
    
    # Find prims by name
    found_prims = client.find_prims_by_name(file_path, "hello")
    print(f"Found {len(found_prims['prims'])} prims with name 'hello'")

finally:
    # Close the client
    client.close()
```

## Running the Example

```bash
cd usd-mcp\client
python example.py
```

## Running Tests

### Unit Tests

```bash
cd usd-mcp\client
pytest tests\test_client.py -v
```

### Integration Tests

To run integration tests, you need to have the USD MCP Server script available:

```bash
cd usd-mcp\client
set RUN_INTEGRATION_TESTS=1
pytest tests\test_integration.py -v
```

## API Reference

### USDMCPClient

- `__init__(server_script_path=None)` - Initialize the client with the server script path
- `connect()` - Connect to the server and get server information
- `load_usd_stage(file_path)` - Load a USD file and return basic stage information
- `get_stage_hierarchy(file_path, max_depth=-1)` - Get the complete prim hierarchy of a USD stage
- `inspect_prim(file_path, prim_path)` - Get detailed information about a specific USD prim
- `list_stage_prims(file_path, prim_type=None)` - List all prims in a USD stage with optional filtering
- `find_prims_by_name(file_path, name_pattern)` - Find prims in a USD stage that match a specific name pattern
- `close()` - Close the client connection

### USDMCPClientSync

Synchronous wrapper for USDMCPClient with the same methods.

## How It Works

The USD MCP Client uses the Model Context Protocol (MCP) to communicate with the USD MCP Server. The client:

1. Launches the server script as a subprocess
2. Communicates with the server via standard input/output (stdio)
3. Uses the MCP protocol to initialize the connection and call tools
4. Provides both asynchronous and synchronous interfaces for ease of use

The client supports all the tools provided by the USD MCP Server, including loading USD stages, inspecting prims, and more.