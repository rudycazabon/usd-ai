"""USD stage hierarchy tool implementation."""

from typing import Any, Dict, List

import mcp.types as types

from ..prim_inspector import get_prim_inspector


async def get_stage_hierarchy_tool(arguments: Dict[str, Any]) -> List[types.ContentBlock]:
    """
    Get the complete hierarchy of prims in a USD stage.
    
    Args:
        arguments: Tool arguments containing 'file_path' and optional 'max_depth'
        
    Returns:
        List of content blocks with hierarchy information or error
    """
    if "file_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'file_path'"
        )]
    
    file_path = arguments["file_path"]
    max_depth = arguments.get("max_depth", -1)
    
    # Validate max_depth if provided
    if max_depth is not None and max_depth < -1:
        return [types.TextContent(
            type="text",
            text="Error: max_depth must be -1 (unlimited) or a positive integer"
        )]
    
    prim_inspector = get_prim_inspector()
    
    # Get the hierarchy
    hierarchy, error_msg = prim_inspector.get_stage_hierarchy(file_path, max_depth)
    if not hierarchy:
        return [types.TextContent(
            type="text",
            text=f"Error getting stage hierarchy: {error_msg}"
        )]
    
    try:
        # Format hierarchy as readable text
        hierarchy_text = _format_hierarchy_text(hierarchy, max_depth)
        
        return [types.TextContent(
            type="text",
            text=f"USD Stage Hierarchy for: {file_path}\n\n{hierarchy_text}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error formatting hierarchy: {str(e)}"
        )]


def _format_hierarchy_text(node: Dict[str, Any], max_depth: int, current_depth: int = 0) -> str:
    """Format hierarchy node as readable text with indentation."""
    lines = []
    indent = "  " * current_depth
    
    # Format current node
    name = node.get("name", "unnamed")
    prim_type = node.get("type", "Unknown")
    path = node.get("path", "")
    is_active = node.get("is_active", True)
    
    # Create node representation
    status = "" if is_active else " (inactive)"
    if path == "":
        # This is the pseudo-root
        lines.append(f"{indent}/ (Root){status}")
    else:
        lines.append(f"{indent}{name} [{prim_type}] ({path}){status}")
    
    # Add children if present and within depth limit
    children = node.get("children", [])
    if children and (max_depth == -1 or current_depth < max_depth):
        for child in children:
            child_text = _format_hierarchy_text(child, max_depth, current_depth + 1)
            lines.append(child_text)
    elif children and max_depth != -1 and current_depth >= max_depth:
        # Indicate there are more children but depth limit reached
        lines.append(f"{indent}  ... ({len(children)} children - depth limit reached)")
    
    return "\n".join(lines)


def _count_total_prims(node: Dict[str, Any]) -> int:
    """Count total number of prims in hierarchy."""
    count = 1  # Count current node
    for child in node.get("children", []):
        count += _count_total_prims(child)
    return count


# Tool definition for MCP server
GET_HIERARCHY_TOOL = types.Tool(
    name="get_stage_hierarchy",
    title="Get USD Stage Hierarchy",
    description="Get the complete prim hierarchy of a USD stage, showing the tree structure of all prims with their types and paths",
    inputSchema={
        "type": "object",
        "required": ["file_path"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the USD file"
            },
            "max_depth": {
                "type": "integer",
                "description": "Maximum depth to traverse (-1 for unlimited, default: -1)",
                "default": -1
            }
        }
    }
)