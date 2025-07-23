# USD AI 
The contents of this repository are a collection of OpenUSD tools that interface with MCP (modelcontextprotocol) and A2A (agent2agent). The goal of this effort is to give large language models and agentic workflows the tools to work directly with OpenUSD objects, e.g., UsdStage, prims, hierarchies, and others and integrate them into comprehensive asset creation workflows.

# Introduction 

## Setup
Currently this project has been tested to work on Windows 11 with usd-core from PyPi and NVidia USD v25.05 with Python 3.11.11. 

- Install UV package manager from https://astral.sh
- Execute the following:
  - git clone https://github.com/rudycazabon/usd-ai.git
  - cd usd-ai
  - uv python install "3.11.11"
  - uv venv --python="3.11.11"
  - ./.venv/Scripts/activate.ps1
  - uv pip install -r .\requirements.txt
- To test out the server
  - python -m pytest usd-mcp/server/tests/test_server.py
  - python -m pytest usd-mcp/server/tests/test_usd_mcp_server.py
- Adding to the Claude Desktop (Windows)
  - Open %APPDATA%\claude_desktop_config.json
  - Add/Modify the file with the following:
```
{
  "mcpServers": {
    "usd-mcp": {
      "command": "<FULL PATH>\\usd-ai\\.venv\\Scripts\\python.exe",
      "args": ["<FULL PATH>\\usd-ai\\usd-mcp\\usd_mcp\\main.py"],
      "cwd": "<FULL PATH>\\usd-ai"
    }
  }
}
```

## Usage
Within the context for Claude Desktop (Windows) you will have access to the following USD tools:
- load_usd_stage
- get_stage_hierarchy
- inspect_prim
- list_stage_prims
- find_prims_by_name

For the purposes of this repo I have included usd-mcp\data\HelloWorld.usda. I have loaded the Pixar KitchenSet, however, your milage _will_ vary (trust me).

A sample prompt session that has worked"

```
Load the USD file at <FULL PATH>\\usd-ai\\usd-mcp\\data\\HelloWorld.usda.
<will see load of file>

Show me the hierarchy and present in formatted JSON.
```
## Contents
### usd-mcp - OpenUSD tools exposed with MCP protocols.
[usd-mcp README.md](./usd-ai/README.md)

### usd-a2a - OpenUSD tools exposed to agentic workflows with the a2a protocol.
