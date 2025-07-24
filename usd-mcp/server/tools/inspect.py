"""USD prim inspection tool implementation."""

from typing import Any, Dict, List

import mcp.types as types

from prim_inspector import get_prim_inspector


async def inspect_prim_tool(arguments: Dict[str, Any]) -> List[types.ContentBlock]:
    """
    Get detailed information about a specific USD prim.
    
    Args:
        arguments: Tool arguments containing 'file_path' and 'prim_path'
        
    Returns:
        List of content blocks with prim information or error
    """
    if "file_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'file_path'"
        )]
    
    if "prim_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'prim_path'"
        )]
    
    file_path = arguments["file_path"]
    prim_path = arguments["prim_path"]
    
    prim_inspector = get_prim_inspector()
    
    # Get prim information
    prim_info, error_msg = prim_inspector.get_prim_info(file_path, prim_path)
    if not prim_info:
        return [types.TextContent(
            type="text",
            text=f"Error inspecting prim: {error_msg}"
        )]
    
    try:
        # Format prim information as readable text
        prim_text = _format_prim_info_text(prim_info)
        
        return [types.TextContent(
            type="text",
            text=f"USD Prim Inspection: {prim_path}\n\n{prim_text}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error formatting prim information: {str(e)}"
        )]


def _format_prim_info_text(prim_info: Dict[str, Any]) -> str:
    """Format prim info as readable text."""
    lines = []
    
    # Basic prim information
    lines.append("=== PRIM DETAILS ===")
    lines.append(f"Path: {prim_info.get('path', 'Unknown')}")
    lines.append(f"Name: {prim_info.get('name', 'Unknown')}")
    lines.append(f"Type: {prim_info.get('type', 'Unknown')}")
    lines.append(f"Valid: {prim_info.get('is_valid', False)}")
    lines.append(f"Active: {prim_info.get('is_active', False)}")
    lines.append(f"Defined: {prim_info.get('is_defined', False)}")
    lines.append(f"Has References: {prim_info.get('has_authored_references', False)}")
    lines.append(f"Has Payloads: {prim_info.get('has_authored_payloads', False)}")
    
    # Parent information
    lines.append("\n=== PARENT ===")
    parent = prim_info.get('parent')
    if parent:
        lines.append(f"Parent: {parent.get('path', 'Unknown')} [{parent.get('type', 'Unknown')}]")
    else:
        lines.append("Parent: None (root level)")
    
    # Children information
    lines.append(f"\n=== CHILDREN ({prim_info.get('child_count', 0)}) ===")
    children = prim_info.get('children', [])
    if children:
        for child in children[:10]:  # Limit to first 10 children
            lines.append(f"  • {child.get('name', 'Unknown')} [{child.get('type', 'Unknown')}] ({child.get('path', 'Unknown')})")
        if len(children) > 10:
            lines.append(f"  ... and {len(children) - 10} more children")
    else:
        lines.append("  No children")
    
    # Properties information
    lines.append(f"\n=== PROPERTIES ({prim_info.get('property_count', 0)}) ===")
    properties = prim_info.get('properties', [])
    if properties:
        # Group properties by type
        attributes = [p for p in properties if p.get('type') == 'Attribute']
        relationships = [p for p in properties if p.get('type') == 'Relationship']
        
        if attributes:
            lines.append(f"\nAttributes ({len(attributes)}):")
            for attr in attributes:
                name = attr.get('name', 'Unknown')
                value_type = attr.get('value_type', 'Unknown')
                has_value = attr.get('has_value', False)
                
                if has_value and 'value' in attr:
                    value = attr['value']
                    if isinstance(value, list) and len(value) > 3:
                        value_str = f"[{', '.join(map(str, value[:3]))}...] ({len(value)} items)"
                    else:
                        value_str = str(value)
                    lines.append(f"  • {name} ({value_type}): {value_str}")
                else:
                    lines.append(f"  • {name} ({value_type}): <no value>")
        
        if relationships:
            lines.append(f"\nRelationships ({len(relationships)}):")
            for rel in relationships:
                name = rel.get('name', 'Unknown')
                targets = rel.get('targets', [])
                if targets:
                    targets_str = ', '.join(targets[:3])
                    if len(targets) > 3:
                        targets_str += f" ... ({len(targets)} total)"
                    lines.append(f"  • {name}: {targets_str}")
                else:
                    lines.append(f"  • {name}: <no targets>")
    else:
        lines.append("  No properties")
    
    return "\n".join(lines)


# Tool definition for MCP server
INSPECT_PRIM_TOOL = types.Tool(
    name="inspect_prim",
    title="Inspect USD Prim",
    description="Get detailed information about a specific USD prim including its properties, attributes, relationships, parent, and children",
    inputSchema={
        "type": "object",
        "required": ["file_path", "prim_path"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the USD file"
            },
            "prim_path": {
                "type": "string",
                "description": "Path to the prim within the USD stage (e.g., '/hello/world')"
            }
        }
    }
)