"""USD stage prim listing tool implementation."""

from typing import Any, Dict, List, Optional

import mcp.types as types

from ..prim_inspector import get_prim_inspector


async def list_stage_prims_tool(arguments: Dict[str, Any]) -> List[types.ContentBlock]:
    """
    List all prims in a USD stage, optionally filtered by type.
    
    Args:
        arguments: Tool arguments containing 'file_path' and optional 'prim_type'
        
    Returns:
        List of content blocks with prim list or error
    """
    if "file_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'file_path'"
        )]
    
    file_path = arguments["file_path"]
    prim_type = arguments.get("prim_type")
    
    prim_inspector = get_prim_inspector()
    
    # Get the prim list
    prims, error_msg = prim_inspector.list_prims(file_path, prim_type)
    if prims is None:
        return [types.TextContent(
            type="text",
            text=f"Error listing prims: {error_msg}"
        )]
    
    try:
        # Format prim list as readable text
        prims_text = _format_prims_list_text(prims, prim_type)
        
        filter_text = f" (filtered by type: {prim_type})" if prim_type else ""
        return [types.TextContent(
            type="text",
            text=f"USD Stage Prims{filter_text}: {file_path}\n\n{prims_text}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error formatting prim list: {str(e)}"
        )]


def _format_prims_list_text(prims: List[Dict[str, Any]], prim_type: Optional[str] = None) -> str:
    """Format prims list as readable text."""
    if not prims:
        filter_text = f" of type '{prim_type}'" if prim_type else ""
        return f"No prims found{filter_text}."
    
    lines = []
    lines.append(f"Found {len(prims)} prim(s):")
    lines.append("")
    
    # Group prims by type for better organization
    prims_by_type = {}
    for prim in prims:
        prim_type_name = prim.get('type', 'Unknown')
        if prim_type_name not in prims_by_type:
            prims_by_type[prim_type_name] = []
        prims_by_type[prim_type_name].append(prim)
    
    # Sort types alphabetically
    for type_name in sorted(prims_by_type.keys()):
        type_prims = prims_by_type[type_name]
        lines.append(f"=== {type_name} ({len(type_prims)}) ===")
        
        for prim in type_prims:
            path = prim.get('path', 'Unknown')
            name = prim.get('name', 'Unknown')
            is_active = prim.get('is_active', True)
            is_defined = prim.get('is_defined', True)
            property_count = prim.get('property_count', 0)
            child_count = prim.get('child_count', 0)
            
            # Create status indicators
            status_parts = []
            if not is_active:
                status_parts.append("inactive")
            if not is_defined:
                status_parts.append("undefined")
            
            status_text = f" ({', '.join(status_parts)})" if status_parts else ""
            
            lines.append(f"  • {name} - {path}{status_text}")
            lines.append(f"    Properties: {property_count}, Children: {child_count}")
        
        lines.append("")
    
    return "\n".join(lines)


async def find_prims_by_name_tool(arguments: Dict[str, Any]) -> List[types.ContentBlock]:
    """
    Find prims by name pattern in a USD stage.
    
    Args:
        arguments: Tool arguments containing 'file_path' and 'name_pattern'
        
    Returns:
        List of content blocks with matching prims or error
    """
    if "file_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'file_path'"
        )]
    
    if "name_pattern" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'name_pattern'"
        )]
    
    file_path = arguments["file_path"]
    name_pattern = arguments["name_pattern"]
    
    prim_inspector = get_prim_inspector()
    
    # Find prims by name
    prims, error_msg = prim_inspector.find_prims_by_name(file_path, name_pattern)
    if prims is None:
        return [types.TextContent(
            type="text",
            text=f"Error finding prims: {error_msg}"
        )]
    
    try:
        # Format results
        if not prims:
            return [types.TextContent(
                type="text",
                text=f"No prims found with name '{name_pattern}' in {file_path}"
            )]
        
        prims_text = _format_prims_list_text(prims)
        
        return [types.TextContent(
            type="text",
            text=f"Prims named '{name_pattern}' in {file_path}:\n\n{prims_text}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error formatting search results: {str(e)}"
        )]


# Tool definitions for MCP server
LIST_PRIMS_TOOL = types.Tool(
    name="list_stage_prims",
    title="List USD Stage Prims",
    description="List all prims in a USD stage with their basic information, optionally filtered by prim type",
    inputSchema={
        "type": "object",
        "required": ["file_path"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the USD file"
            },
            "prim_type": {
                "type": "string",
                "description": "Optional prim type to filter by (e.g., 'Sphere', 'Xform', 'Mesh')"
            }
        }
    }
)

FIND_PRIMS_TOOL = types.Tool(
    name="find_prims_by_name",
    title="Find USD Prims by Name",
    description="Find prims in a USD stage that match a specific name pattern",
    inputSchema={
        "type": "object",
        "required": ["file_path", "name_pattern"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the USD file"
            },
            "name_pattern": {
                "type": "string",
                "description": "Name pattern to search for (exact match)"
            }
        }
    }
)