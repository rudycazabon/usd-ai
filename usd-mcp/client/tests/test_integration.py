"""Integration tests for the USD MCP Client with the actual server."""

import os
import pytest
import asyncio
from pathlib import Path

# Import the client classes
import sys
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)
from client import USDMCPClient, USDMCPClientSync


# Skip all tests if integration tests are not enabled
pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "1",
    reason="Integration tests are disabled. Set RUN_INTEGRATION_TESTS=1 to enable."
)


class TestIntegration:
    """Integration tests for the USD MCP Client."""

    @pytest.mark.asyncio
    async def test_connect(self, async_client):
        """Test connecting to the server."""
        result = await async_client.connect()
        assert "name" in result
        assert result["name"] == "USD MCP Server"
        assert "tools" in result
        assert len(result["tools"]) > 0

    @pytest.mark.asyncio
    async def test_load_usd_stage(self, async_client, sample_usd_file):
        """Test loading a USD stage."""
        # First connect to the server
        await async_client.connect()
        
        # Load the stage
        result = await async_client.load_usd_stage(sample_usd_file)
        assert "success" in result
        assert result["success"] is True
        assert "stage_info" in result
        assert result["file_path"] == sample_usd_file

    @pytest.mark.asyncio
    async def test_get_stage_hierarchy(self, async_client, sample_usd_file):
        """Test getting the stage hierarchy."""
        # First connect to the server
        await async_client.connect()
        
        # Get the hierarchy
        result = await async_client.get_stage_hierarchy(sample_usd_file, max_depth=2)
        assert "success" in result
        assert result["success"] is True
        assert "hierarchy" in result
        assert "children" in result["hierarchy"]

    @pytest.mark.asyncio
    async def test_inspect_prim(self, async_client, sample_usd_file):
        """Test inspecting a prim."""
        # First connect to the server
        await async_client.connect()
        
        # First, load the stage to get a valid prim path
        stage_result = await async_client.load_usd_stage(sample_usd_file)
        assert stage_result["success"] is True
        
        # Get the default prim path if available, otherwise use "/"
        prim_path = "/"
        if "default_prim" in stage_result.get("stage_info", {}):
            prim_path = stage_result["stage_info"]["default_prim"]["path"]
        
        # Inspect the prim
        result = await async_client.inspect_prim(sample_usd_file, prim_path)
        assert "success" in result
        assert result["success"] is True
        assert "prim_info" in result
        assert result["prim_info"]["path"] == prim_path

    @pytest.mark.asyncio
    async def test_list_stage_prims(self, async_client, sample_usd_file):
        """Test listing stage prims."""
        # First connect to the server
        await async_client.connect()
        
        # List all prims
        result = await async_client.list_stage_prims(sample_usd_file)
        assert "success" in result
        assert result["success"] is True
        assert "prims" in result
        assert isinstance(result["prims"], list)

    @pytest.mark.asyncio
    async def test_find_prims_by_name(self, async_client, sample_usd_file):
        """Test finding prims by name."""
        # First connect to the server
        await async_client.connect()
        
        # First, list all prims to find a valid name
        list_result = await async_client.list_stage_prims(sample_usd_file)
        assert list_result["success"] is True
        assert len(list_result["prims"]) > 0
        
        # Use the name of the first prim
        name_pattern = list_result["prims"][0]["name"]
        
        # Find prims by name
        result = await async_client.find_prims_by_name(sample_usd_file, name_pattern)
        assert "success" in result
        assert result["success"] is True
        assert "prims" in result
        assert len(result["prims"]) > 0
        assert result["prims"][0]["name"] == name_pattern


class TestIntegrationSync:
    """Integration tests for the synchronous USD MCP Client."""

    def test_connect(self, sync_client):
        """Test connecting to the server."""
        result = sync_client.connect()
        assert "name" in result
        assert result["name"] == "USD MCP Server"
        assert "tools" in result
        assert len(result["tools"]) > 0

    def test_load_usd_stage(self, sync_client, sample_usd_file):
        """Test loading a USD stage."""
        # First connect to the server
        sync_client.connect()
        
        # Load the stage
        result = sync_client.load_usd_stage(sample_usd_file)
        assert "success" in result
        assert result["success"] is True
        assert "stage_info" in result
        assert result["file_path"] == sample_usd_file

    def test_get_stage_hierarchy(self, sync_client, sample_usd_file):
        """Test getting the stage hierarchy."""
        # First connect to the server
        sync_client.connect()
        
        # Get the hierarchy
        result = sync_client.get_stage_hierarchy(sample_usd_file, max_depth=2)
        assert "success" in result
        assert result["success"] is True
        assert "hierarchy" in result
        assert "children" in result["hierarchy"]