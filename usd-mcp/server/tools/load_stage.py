"""Load USD stage tool implementation."""

from typing import Any, Dict, List

import mcp.types as types

from ..stage_manager import get_stage_manager
from ..utils.formatting import format_stage_info


async def load_usd_stage_tool(arguments: Dict[str, Any]) -> List[types.ContentBlock]:
    """
    Load a USD stage and return basic stage information.
    
    Args:
        arguments: Tool arguments containing 'file_path'
        
    Returns:
        List of content blocks with stage information or error
    """
    if "file_path" not in arguments:
        return [types.TextContent(
            type="text",
            text="Error: Missing required argument 'file_path'"
        )]
    
    file_path = arguments["file_path"]
    stage_manager = get_stage_manager()
    
    # Load the stage
    stage, error_msg = stage_manager.load_stage(file_path)
    if not stage:
        return [types.TextContent(
            type="text",
            text=f"Error loading USD stage: {error_msg}"
        )]
    
    # Format stage information
    try:
        stage_info = format_stage_info(stage)
        
        # Count total prims
        prim_count = 0
        for prim in stage.Traverse():
            if prim.IsValid():
                prim_count += 1
        
        stage_info["prim_count"] = prim_count
        
        response = {
            "success": True,
            "file_path": file_path,
            "stage_info": stage_info
        }
        
        return [types.TextContent(
            type="text",
            text=f"Successfully loaded USD stage: {file_path}\n\nStage Information:\n{_format_stage_info_text(stage_info)}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error processing stage information: {str(e)}"
        )]


def _format_stage_info_text(stage_info: Dict[str, Any]) -> str:
    """Format stage info as readable text."""
    lines = []
    lines.append(f"• Root Layer: {stage_info.get('root_layer_identifier', 'Unknown')}")
    lines.append(f"• Layer Count: {stage_info.get('layer_count', 0)}")
    lines.append(f"• Prim Count: {stage_info.get('prim_count', 0)}")
    lines.append(f"• Has Default Prim: {stage_info.get('has_default_prim', False)}")
    lines.append(f"• Time Codes Per Second: {stage_info.get('time_codes_per_second', 24.0)}")
    
    if stage_info.get('has_default_prim') and 'default_prim' in stage_info:
        default_prim = stage_info['default_prim']
        lines.append(f"• Default Prim: {default_prim.get('path', 'Unknown')} ({default_prim.get('type', 'Unknown')})")
    
    return "\n".join(lines)


# Tool definition for MCP server
LOAD_STAGE_TOOL = types.Tool(
    name="load_usd_stage",
    title="Load USD Stage",
    description="Load a USD file and return basic stage information including layer count, prim count, and default prim details",
    inputSchema={
        "type": "object",
        "required": ["file_path"],
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the USD file to load (.usd, .usda, .usdc, .usdz)"
            }
        }
    }
)