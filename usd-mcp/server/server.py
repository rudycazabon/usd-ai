"""USD MCP Server - Main server implementation using FastMCP."""

from typing import Optional

from mcp.server.fastmcp import FastMCP

from tools.hierarchy import get_stage_hierarchy_tool
from tools.inspect import inspect_prim_tool
from tools.list_prims import find_prims_by_name_tool, list_stage_prims_tool
from tools.load_stage import load_usd_stage_tool

# Create FastMCP server
mcp = FastMCP("USD MCP Server")


def _extract_text_from_content(content_blocks) -> str:
    """Extract text from MCP content blocks."""
    if not content_blocks:
        return "No content returned"
    
    # Get the first content block and extract text
    content = content_blocks[0]
    if hasattr(content, 'text'):
        return content.text
    else:
        return str(content)


@mcp.tool()
async def load_usd_stage(file_path: str) -> str:
    """
    Load a USD file and return basic stage information.
    
    Args:
        file_path: Path to the USD file to load (.usd, .usda, .usdc, .usdz)
    
    Returns:
        Stage information including layer count, prim count, and default prim details
    """
    result = await load_usd_stage_tool({"file_path": file_path})
    return _extract_text_from_content(result)


@mcp.tool()
async def get_stage_hierarchy(file_path: str, max_depth: int = -1) -> str:
    """
    Get the complete prim hierarchy of a USD stage.
    
    Args:
        file_path: Path to the USD file
        max_depth: Maximum depth to traverse (-1 for unlimited, default: -1)
    
    Returns:
        Tree structure of all prims with their types and paths
    """
    arguments = {"file_path": file_path}
    if max_depth != -1:
        arguments["max_depth"] = str(max_depth)
    result = await get_stage_hierarchy_tool(arguments)
    return _extract_text_from_content(result)


@mcp.tool()
async def inspect_prim(file_path: str, prim_path: str) -> str:
    """
    Get detailed information about a specific USD prim.
    
    Args:
        file_path: Path to the USD file
        prim_path: Path to the prim within the USD stage (e.g., '/hello/world')
    
    Returns:
        Detailed prim information including properties, attributes, relationships, parent, and children
    """
    result = await inspect_prim_tool({"file_path": file_path, "prim_path": prim_path})
    return _extract_text_from_content(result)


@mcp.tool()
async def list_stage_prims(file_path: str, prim_type: Optional[str] = None) -> str:
    """
    List all prims in a USD stage with optional filtering.
    
    Args:
        file_path: Path to the USD file
        prim_type: Optional prim type to filter by (e.g., 'Sphere', 'Xform', 'Mesh')
    
    Returns:
        List of all prims with their basic information, optionally filtered by type
    """
    arguments = {"file_path": file_path}
    if prim_type:
        arguments["prim_type"] = prim_type
    result = await list_stage_prims_tool(arguments)
    return _extract_text_from_content(result)


@mcp.tool()
async def find_prims_by_name(file_path: str, name_pattern: str) -> str:
    """
    Find prims in a USD stage that match a specific name pattern.
    
    Args:
        file_path: Path to the USD file
        name_pattern: Name pattern to search for (exact match)
    
    Returns:
        List of prims that match the name pattern with their information
    """
    result = await find_prims_by_name_tool({"file_path": file_path, "name_pattern": name_pattern})
    return _extract_text_from_content(result)


# Export the server instance
server = mcp
