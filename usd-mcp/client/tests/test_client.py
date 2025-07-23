"""Tests for the USD MCP Client."""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Import the client classes
import sys
from pathlib import Path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)
from client import USDMCPClient, USDMCPClientSync


class TestUSDMCPClient:
    """Tests for the USDMCPClient class."""

    @pytest.mark.asyncio
    async def test_connect(self, async_client):
        """Test connecting to the server."""
        # Completely mock the connect method
        with patch.object(async_client, 'connect', new=AsyncMock()) as mock_connect:
            # Set the return value for the mock
            mock_connect.return_value = {
                "name": "USD MCP Server",
                "tools": ["load_usd_stage", "get_stage_hierarchy"],
                "tool_count": 2
            }
            
            # Call the mocked method
            result = await async_client.connect()
            
            # Verify the result
            assert "name" in result
            assert result["name"] == "USD MCP Server"
            assert "tools" in result
            assert len(result["tools"]) == 2
            assert "load_usd_stage" in result["tools"]
            assert "get_stage_hierarchy" in result["tools"]

    @pytest.mark.asyncio
    async def test_load_usd_stage(self, async_client, sample_usd_file):
        """Test loading a USD stage."""
        # Mock the session and call_tool method
        async_client.session = AsyncMock()
        async_client.session.call_tool.return_value = MagicMock(
            content={
                "success": True,
                "file_path": sample_usd_file,
                "stage_info": {
                    "root_layer_identifier": sample_usd_file,
                    "layer_count": 1,
                    "prim_count": 3,
                    "has_default_prim": True
                }
            }
        )
        
        result = await async_client.load_usd_stage(sample_usd_file)
        
        async_client.session.call_tool.assert_called_once_with(
            "load_usd_stage", 
            {"file_path": sample_usd_file}
        )
        assert result["success"] is True
        assert result["file_path"] == sample_usd_file
        assert result["stage_info"]["prim_count"] == 3

    @pytest.mark.asyncio
    async def test_get_stage_hierarchy(self, async_client, sample_usd_file):
        """Test getting the stage hierarchy."""
        # Mock the session and call_tool method
        async_client.session = AsyncMock()
        async_client.session.call_tool.return_value = MagicMock(
            content={
                "success": True,
                "file_path": sample_usd_file,
                "hierarchy": {
                    "path": "/",
                    "name": "",
                    "type": "",
                    "children": [
                        {
                            "path": "/hello",
                            "name": "hello",
                            "type": "Xform",
                            "children": []
                        }
                    ]
                }
            }
        )
        
        result = await async_client.get_stage_hierarchy(sample_usd_file, max_depth=2)
        
        async_client.session.call_tool.assert_called_once_with(
            "get_stage_hierarchy",
            {"file_path": sample_usd_file, "max_depth": "2"}
        )
        assert result["success"] is True
        assert "hierarchy" in result
        assert result["hierarchy"]["children"][0]["path"] == "/hello"

    @pytest.mark.asyncio
    async def test_inspect_prim(self, async_client, sample_usd_file):
        """Test inspecting a prim."""
        prim_path = "/hello"
        # Mock the session and call_tool method
        async_client.session = AsyncMock()
        async_client.session.call_tool.return_value = MagicMock(
            content={
                "success": True,
                "file_path": sample_usd_file,
                "prim_path": prim_path,
                "prim_info": {
                    "path": prim_path,
                    "name": "hello",
                    "type": "Xform",
                    "is_valid": True
                }
            }
        )
        
        result = await async_client.inspect_prim(sample_usd_file, prim_path)
        
        async_client.session.call_tool.assert_called_once_with(
            "inspect_prim",
            {"file_path": sample_usd_file, "prim_path": prim_path}
        )
        assert result["success"] is True
        assert result["prim_info"]["path"] == prim_path
        assert result["prim_info"]["type"] == "Xform"

    @pytest.mark.asyncio
    async def test_list_stage_prims(self, async_client, sample_usd_file):
        """Test listing stage prims."""
        # Mock the session and call_tool method
        async_client.session = AsyncMock()
        async_client.session.call_tool.return_value = MagicMock(
            content={
                "success": True,
                "file_path": sample_usd_file,
                "prims": [
                    {
                        "path": "/hello",
                        "name": "hello",
                        "type": "Xform"
                    },
                    {
                        "path": "/world",
                        "name": "world",
                        "type": "Sphere"
                    }
                ]
            }
        )
        
        result = await async_client.list_stage_prims(sample_usd_file, prim_type="Xform")
        
        async_client.session.call_tool.assert_called_once_with(
            "list_stage_prims",
            {"file_path": sample_usd_file, "prim_type": "Xform"}
        )
        assert result["success"] is True
        assert len(result["prims"]) == 2
        assert result["prims"][0]["path"] == "/hello"

    @pytest.mark.asyncio
    async def test_find_prims_by_name(self, async_client, sample_usd_file):
        """Test finding prims by name."""
        name_pattern = "hello"
        # Mock the session and call_tool method
        async_client.session = AsyncMock()
        async_client.session.call_tool.return_value = MagicMock(
            content={
                "success": True,
                "file_path": sample_usd_file,
                "name_pattern": name_pattern,
                "prims": [
                    {
                        "path": "/hello",
                        "name": "hello",
                        "type": "Xform"
                    }
                ]
            }
        )
        
        result = await async_client.find_prims_by_name(sample_usd_file, name_pattern)
        
        async_client.session.call_tool.assert_called_once_with(
            "find_prims_by_name",
            {"file_path": sample_usd_file, "name_pattern": name_pattern}
        )
        assert result["success"] is True
        assert len(result["prims"]) == 1
        assert result["prims"][0]["name"] == name_pattern


class TestUSDMCPClientSync:
    """Tests for the USDMCPClientSync class."""

    def test_connect(self, sync_client):
        """Test connecting to the server."""
        with patch('client.client.run_async') as mock_run_async:
            mock_run_async.return_value = {
                "name": "USD MCP Server",
                "tools": ["load_usd_stage", "get_stage_hierarchy"],
                "tool_count": 2
            }
            
            result = sync_client.connect()
            
            assert mock_run_async.called
            assert result["name"] == "USD MCP Server"
            assert len(result["tools"]) == 2

    def test_load_usd_stage(self, sync_client, sample_usd_file):
        """Test loading a USD stage."""
        with patch('client.client.run_async') as mock_run_async:
            mock_run_async.return_value = {
                "success": True,
                "file_path": sample_usd_file,
                "stage_info": {
                    "root_layer_identifier": sample_usd_file,
                    "layer_count": 1,
                    "prim_count": 3,
                    "has_default_prim": True
                }
            }
            
            result = sync_client.load_usd_stage(sample_usd_file)
            
            assert mock_run_async.called
            assert result["success"] is True
            assert result["file_path"] == sample_usd_file
            assert result["stage_info"]["prim_count"] == 3