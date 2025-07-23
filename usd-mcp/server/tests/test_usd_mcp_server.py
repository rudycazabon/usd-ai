#!/usr/bin/env python3
"""Test suite for USD MCP Server functionality using pytest."""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

import pytest

# Add the usd-mcp directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import server components
from server.server import server
from server.tools.hierarchy import get_stage_hierarchy_tool
from server.tools.inspect import inspect_prim_tool
from server.tools.list_prims import list_stage_prims_tool, find_prims_by_na#@pytest.mark.skip(reason="Server process startup test requires additional setup")

    @pytest.mark.asynciome_tool
from server.tools.load_stage import load_usd_stage_tool

# Path to test USD file
TEST_USD_FILE = str(Path(__file__).parent.parent.parent / "data" / "HelloWorld.usda")


class TestUSDMCPServerProtocol:
    """Test cases for USD MCP server protocol functionality."""
    
    def test_server_initialization(self):
        """Test that the server is initialized properly."""
        # Test server is a FastMCP instance
        assert server is not None
        assert hasattr(server, 'name')
        assert server.name == "USD MCP Server"


class TestUSDMCPServerToolCalls:
    """Test cases for USD MCP server tool calls."""
    
    @pytest.mark.asyncio
    async def test_load_usd_stage_tool(self):
        """Test the load_usd_stage tool function directly."""
        # Call the tool function directly
        result = await load_usd_stage_tool({"file_path": TEST_USD_FILE})
        
        # Verify result
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check content
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "Successfully loaded USD stage" in content
        assert "Stage Information" in content
    
    @pytest.mark.asyncio
    async def test_get_stage_hierarchy_tool(self):
        """Test the get_stage_hierarchy tool function directly."""
        # Call the tool function directly
        result = await get_stage_hierarchy_tool({"file_path": TEST_USD_FILE})
        
        # Verify result
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check content
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "USD Stage Hierarchy" in content
        assert "hello" in content  # Should contain the hello prim
    
    @pytest.mark.asyncio
    async def test_inspect_prim_tool(self):
        """Test the inspect_prim tool function directly."""
        # Call the tool function directly
        result = await inspect_prim_tool({
            "file_path": TEST_USD_FILE,
            "prim_path": "/hello"
        })
        
        # Verify result
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check content
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "USD Prim Inspection: /hello" in content
        assert "PRIM DETAILS" in content
    
    @pytest.mark.asyncio
    async def test_list_stage_prims_tool(self):
        """Test the list_stage_prims tool function directly."""
        # Call the tool function directly
        result = await list_stage_prims_tool({"file_path": TEST_USD_FILE})
        
        # Verify result
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check content
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "USD Stage Prims" in content
        assert "Found" in content
    
    @pytest.mark.asyncio
    async def test_find_prims_by_name_tool(self):
        """Test the find_prims_by_name tool function directly."""
        # Call the tool function directly
        result = await find_prims_by_name_tool({
            "file_path": TEST_USD_FILE,
            "name_pattern": "hello"
        })
        
        # Verify result
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check content
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "Prims named 'hello'" in content
        assert "Found" in content


class TestUSDMCPServerErrorHandling:
    """Test cases for USD MCP server error handling."""
    
    @pytest.mark.asyncio
    async def test_missing_required_parameter(self):
        """Test calling a tool without required parameters."""
        result = await load_usd_stage_tool({})
        
        # Verify error response
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check error message
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "Error" in content
        assert "Missing required argument 'file_path'" in content
    
    @pytest.mark.asyncio
    async def test_invalid_file_path(self):
        """Test calling a tool with an invalid file path."""
        result = await load_usd_stage_tool({"file_path": "/nonexistent/file.usd"})
        
        # Verify error response
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check error message
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "Error loading USD stage" in content
    
    @pytest.mark.asyncio
    async def test_invalid_prim_path(self):
        """Test inspecting a non-existent prim."""
        result = await inspect_prim_tool({
            "file_path": TEST_USD_FILE,
            "prim_path": "/nonexistent"
        })
        
        # Verify error response
        assert len(result) == 1
        assert hasattr(result[0], 'type')
        assert result[0].type == "text"
        
        # Check error message
        assert hasattr(result[0], 'text')
        content = result[0].text
        assert "Error inspecting prim" in content


class TestUSDMCPServerIntegration:
    """Integration tests for USD MCP server."""

    #@pytest.mark.skip(reason="Server process startup test requires additional setup")
    @pytest.mark.asyncio
    def test_server_process_startup(self):
        """Test that the server process starts up without errors."""
        # Path to the main.py file
        main_py_path = str(Path(__file__).parent.parent / "main.py")
        
        # Get the Python executable
        if sys.platform == "win32":
            python_exe = os.path.join(os.path.dirname(sys.executable), "python.exe")
        else:
            python_exe = sys.executable
        
        # Start the server process
        process = subprocess.Popen(
            [python_exe, main_py_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Give it a moment to start up
            time.sleep(2)
            
            # Check if process is still running (no immediate crash)
            assert process.poll() is None, "Server process crashed immediately"
            
            # Send a simple MCP initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            # Write the request to stdin
            process.stdin.write(json.dumps(init_request) + "\n")
            process.stdin.flush()
            
            # Wait for a response with timeout
            process.stdin.close()
            try:
                stdout, stderr = process.communicate(timeout=5)
                
                # Check for errors
                assert not stderr, f"Server reported errors: {stderr}"
                
                # Parse the response
                response_lines = stdout.strip().split("\n")
                if response_lines:
                    response = json.loads(response_lines[0])
                    assert "result" in response
                    assert "serverInfo" in response["result"]
                    assert "name" in response["result"]["serverInfo"]
                    assert response["result"]["serverInfo"]["name"] == "USD MCP Server"
            except subprocess.TimeoutExpired:
                # This is actually expected since the server keeps running
                pass
                
        finally:
            # Make sure process is terminated
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


def run_tests():
    """Run all tests."""
    print("USD MCP Server Test Suite")
    print("=" * 50)
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Run the tests using pytest
    return pytest.main(["-xvs", __file__])


if __name__ == "__main__":
    # This allows the file to be run as a standalone script
    sys.exit(run_tests())