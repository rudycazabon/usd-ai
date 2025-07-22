#!/usr/bin/env python3
"""Basic tests for USD MCP server functionality."""

import os
import sys
from pathlib import Path

import pytest

# Add the usd-mcp directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Now we can import from the server package
from server.tools.hierarchy import get_stage_hierarchy_tool
from server.tools.inspect import inspect_prim_tool
from server.tools.list_prims import list_stage_prims_tool
from server.tools.load_stage import load_usd_stage_tool

# Path to test USD file from tutorials
TEST_USD_FILE = str(Path(__file__).parent.parent.parent / "data" / "HelloWorld.usda")


class TestUSDMCPServer:
    """Test cases for USD MCP server tools."""
    
    @pytest.mark.asyncio
    async def test_load_stage_tool(self):
        """Test loading a USD stage."""
        arguments = {"file_path": TEST_USD_FILE}
        result = await load_usd_stage_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully loaded USD stage" in result[0].text
        assert "Stage Information" in result[0].text
    
    @pytest.mark.asyncio
    async def test_load_stage_missing_file(self):
        """Test loading a non-existent USD file."""
        arguments = {"file_path": "/nonexistent/file.usd"}
        result = await load_usd_stage_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error loading USD stage" in result[0].text
    
    @pytest.mark.asyncio
    async def test_load_stage_missing_argument(self):
        """Test loading without file_path argument."""
        arguments = {}
        result = await load_usd_stage_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Missing required argument 'file_path'" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_hierarchy_tool(self):
        """Test getting stage hierarchy."""
        arguments = {"file_path": TEST_USD_FILE}
        result = await get_stage_hierarchy_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "USD Stage Hierarchy" in result[0].text
        assert "hello" in result[0].text  # Should contain the hello prim
    
    @pytest.mark.asyncio
    async def test_get_hierarchy_with_depth_limit(self):
        """Test getting stage hierarchy with depth limit."""
        arguments = {"file_path": TEST_USD_FILE, "max_depth": 1}
        result = await get_stage_hierarchy_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "USD Stage Hierarchy" in result[0].text
    
    @pytest.mark.asyncio
    async def test_inspect_prim_tool(self):
        """Test inspecting a specific prim."""
        arguments = {"file_path": TEST_USD_FILE, "prim_path": "/hello"}
        result = await inspect_prim_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "USD Prim Inspection: /hello" in result[0].text
        assert "PRIM DETAILS" in result[0].text
    
    @pytest.mark.asyncio
    async def test_inspect_prim_invalid_path(self):
        """Test inspecting a non-existent prim."""
        arguments = {"file_path": TEST_USD_FILE, "prim_path": "/nonexistent"}
        result = await inspect_prim_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error inspecting prim" in result[0].text
    
    @pytest.mark.asyncio
    async def test_inspect_prim_missing_arguments(self):
        """Test inspecting prim without required arguments."""
        # Missing file_path
        arguments = {"prim_path": "/hello"}
        result = await inspect_prim_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Missing required argument 'file_path'" in result[0].text
        
        # Missing prim_path
        arguments = {"file_path": TEST_USD_FILE}
        result = await inspect_prim_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Missing required argument 'prim_path'" in result[0].text
    
    @pytest.mark.asyncio
    async def test_list_prims_tool(self):
        """Test listing all prims in a stage."""
        arguments = {"file_path": TEST_USD_FILE}
        result = await list_stage_prims_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "USD Stage Prims" in result[0].text
        assert "Found" in result[0].text
    
    @pytest.mark.asyncio
    async def test_list_prims_with_filter(self):
        """Test listing prims filtered by type."""
        arguments = {"file_path": TEST_USD_FILE, "prim_type": "Xform"}
        result = await list_stage_prims_tool(arguments)
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "filtered by type: Xform" in result[0].text


if __name__ == "__main__":
    # This allows the file to be run as a standalone script
    print(f"Running tests from {__file__}")
    sys.exit(pytest.main([__file__]))