"""USD MCP Client implementation."""

import asyncio
import os
from contextlib import AsyncExitStack
from typing import Any, Dict, Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()  # load environment variables from .env

class USDMCPClient:
    """Client for interacting with the USD MCP Server."""

    def __init__(self, server_script_path: Optional[str] = None):
        """
        Initialize the USD MCP client.
        
        Args:
            server_script_path: Path to the server script (default: None, will use environment variable)
        """
        self.server_script_path = server_script_path or os.getenv("USD_MCP_SERVER_PATH")

        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        ######## YOU HAVE TO SET UP ANTHROPIC API KEY IN .env ########
        self.anthropic = Anthropic()

    async def connect(self, server_script_path: str) -> Dict[str, Any]:
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        self.server_script_path = server_script_path
        if not os.path.exists(self.server_script_path):
            raise FileNotFoundError(f"Server script not found: {self.server_script_path}")
            
        is_python = self.server_script_path.endswith('.py')
        if not is_python:
            raise ValueError("Server script must be a .py file")
            
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        return {
            "name": "USD MCP Server",
            "tools": [tool.name for tool in tools],
            "tool_count": len(tools)
        }
    
    async def load_usd_stage(self, file_path: str) -> Dict[str, Any]:
        """
        Load a USD file and return basic stage information.
        
        Args:
            file_path: Path to the USD file to load (.usd, .usda, .usdc, .usdz)
            
        Returns:
            Stage information including layer count, prim count, and default prim details
        """
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect() first.")
            
        result = await self.session.call_tool("load_usd_stage", {"file_path": file_path})
        return result.content
    
    async def get_stage_hierarchy(self, file_path: str, max_depth: int = -1) -> Dict[str, Any]:
        """
        Get the complete prim hierarchy of a USD stage.
        
        Args:
            file_path: Path to the USD file
            max_depth: Maximum depth to traverse (-1 for unlimited, default: -1)
            
        Returns:
            Tree structure of all prims with their types and paths
        """
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect() first.")
            
        params = {"file_path": file_path}
        if max_depth != -1:
            params["max_depth"] = str(max_depth)
            
        result = await self.session.call_tool("get_stage_hierarchy", params)
        return result.content
    
    async def inspect_prim(self, file_path: str, prim_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific USD prim.
        
        Args:
            file_path: Path to the USD file
            prim_path: Path to the prim within the USD stage (e.g., '/hello/world')
            
        Returns:
            Detailed prim information including properties, attributes, relationships, parent, and children
        """
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect() first.")
            
        params = {"file_path": file_path, "prim_path": prim_path}
        result = await self.session.call_tool("inspect_prim", params)
        return result.content
    
    async def list_stage_prims(self, file_path: str, prim_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all prims in a USD stage with optional filtering.
        
        Args:
            file_path: Path to the USD file
            prim_type: Optional prim type to filter by (e.g., 'Sphere', 'Xform', 'Mesh')
            
        Returns:
            List of all prims with their basic information, optionally filtered by type
        """
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect() first.")
            
        params = {"file_path": file_path}
        if prim_type:
            params["prim_type"] = prim_type
            
        result = await self.session.call_tool("list_stage_prims", params)
        return result.content
    
    async def find_prims_by_name(self, file_path: str, name_pattern: str) -> Dict[str, Any]:
        """
        Find prims in a USD stage that match a specific name pattern.
        
        Args:
            file_path: Path to the USD file
            name_pattern: Name pattern to search for (exact match)
            
        Returns:
            List of prims that match the name pattern with their information
        """
        if not self.session:
            raise RuntimeError("Not connected to server. Call connect() first.")
            
        params = {"file_path": file_path, "name_pattern": name_pattern}
        result = await self.session.call_tool("find_prims_by_name", params)
        return result.content
    
    async def close(self) -> None:
        """Close the client connection."""
        await self.exit_stack.aclose()

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{ 
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        # Process response and handle tool calls
        final_text = []

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input
                
                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                if hasattr(content, 'text') and content.text:
                    messages.append({
                      "role": "assistant",
                      "content": content.text
                    })
                messages.append({
                    "role": "user", 
                    "content": result.content
                })

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

# Synchronous wrapper functions for convenience
def run_async(coro):
    """Run an async function synchronously."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

class USDMCPClientSync:
    """Synchronous wrapper for USDMCPClient."""
    
    def __init__(self, server_script_path: Optional[str] = None):
        """Initialize the synchronous USD MCP client."""
        self.async_client = USDMCPClient(server_script_path)
    
    def connect(self) -> Dict[str, Any]:
        """Connect to the MCP server and get server information."""
        return run_async(self.async_client.connect())
    
    def load_usd_stage(self, file_path: str) -> Dict[str, Any]:
        """Load a USD file and return basic stage information."""
        return run_async(self.async_client.load_usd_stage(file_path))
    
    def get_stage_hierarchy(self, file_path: str, max_depth: int = -1) -> Dict[str, Any]:
        """Get the complete prim hierarchy of a USD stage."""
        return run_async(self.async_client.get_stage_hierarchy(file_path, max_depth))
    
    def inspect_prim(self, file_path: str, prim_path: str) -> Dict[str, Any]:
        """Get detailed information about a specific USD prim."""
        return run_async(self.async_client.inspect_prim(file_path, prim_path))
    
    def list_stage_prims(self, file_path: str, prim_type: Optional[str] = None) -> Dict[str, Any]:
        """List all prims in a USD stage with optional filtering."""
        return run_async(self.async_client.list_stage_prims(file_path, prim_type))
    
    def find_prims_by_name(self, file_path: str, name_pattern: str) -> Dict[str, Any]:
        """Find prims in a USD stage that match a specific name pattern."""
        return run_async(self.async_client.find_prims_by_name(file_path, name_pattern))
    
    def close(self) -> None:
        """Close the client connection."""
        run_async(self.async_client.close())

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to__script>")
        sys.exit(1)
        
    client = USDMCPClient()
    try:
        # await client.connect("C:/Users/rudyc/projects/usd-ai/usd-mcp//main.py")
        await client.connect(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
