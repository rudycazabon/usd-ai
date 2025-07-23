"""Formatting utilities for USD data structures."""

from typing import Any, Dict

from pxr import Usd, Vt


def format_usd_value(value: Any) -> Any:
    """
    Format USD attribute values for JSON serialization.
    
    Args:
        value: USD attribute value
        
    Returns:
        JSON-serializable representation of the value
    """
    if value is None:
        return None
    
    # Handle USD vector types
    if isinstance(value, (Vt.Vec3fArray, Vt.Vec3dArray)):
        return [[float(v[0]), float(v[1]), float(v[2])] for v in value]
    
    if isinstance(value, (Vt.Vec2fArray, Vt.Vec2dArray)):
        return [[float(v[0]), float(v[1])] for v in value]
    
    if hasattr(value, '__len__') and not isinstance(value, str):
        # Handle arrays
        try:
            return [format_usd_value(item) for item in value]
        except (TypeError, ValueError):
            return str(value)
    
    # Handle basic types
    if isinstance(value, (int, float, bool, str)):
        return value
    
    # Convert other types to string representation
    return str(value)


def format_prim_info(prim: Usd.Prim) -> Dict[str, Any]:
    """
    Format USD prim information for MCP response.
    
    Args:
        prim: USD prim object
        
    Returns:
        Dictionary with formatted prim information
    """
    return {
        "path": str(prim.GetPath()),
        "name": prim.GetName(),
        "type": prim.GetTypeName(),
        "is_valid": prim.IsValid(),
        "is_active": prim.IsActive(),
        "is_defined": prim.IsDefined(),
        "has_authored_references": prim.HasAuthoredReferences(),
        "has_authored_payloads": prim.HasAuthoredPayloads(),
    }


def format_property_info(prop: Usd.Property) -> Dict[str, Any]:
    """
    Format USD property information for MCP response.
    
    Args:
        prop: USD property object
        
    Returns:
        Dictionary with formatted property information
    """
    info = {
        "name": prop.GetName(),
        "type": str(type(prop).__name__),
        "is_custom": prop.IsCustom(),
    }
    
    # Add attribute-specific information
    if isinstance(prop, Usd.Attribute):
        attr = prop
        info.update({
            "value_type": str(attr.GetTypeName()),
            "has_value": attr.HasValue(),
            "has_authored_value": attr.HasAuthoredValue(),
        })
        
        # Get the value if it exists
        if attr.HasValue():
            try:
                value = attr.Get()
                info["value"] = format_usd_value(value)
            except Exception as e:
                info["value_error"] = str(e)
    
    # Add relationship-specific information
    elif isinstance(prop, Usd.Relationship):
        rel = prop
        info.update({
            "has_authored_targets": rel.HasAuthoredTargets(),
        })
        
        # Get targets if they exist
        try:
            targets = rel.GetTargets()
            info["targets"] = [str(target) for target in targets]
        except Exception as e:
            info["targets_error"] = str(e)
    
    return info


def format_stage_info(stage: Usd.Stage) -> Dict[str, Any]:
    """
    Format USD stage information for MCP response.
    
    Args:
        stage: USD stage object
        
    Returns:
        Dictionary with formatted stage information
    """
    root_layer = stage.GetRootLayer()
    
    info = {
        "root_layer_identifier": root_layer.identifier,
        "root_layer_display_name": root_layer.GetDisplayName(),
        "layer_count": len(stage.GetLayerStack()),
        "has_default_prim": stage.HasDefaultPrim(),
        "time_codes_per_second": stage.GetTimeCodesPerSecond(),
        "start_time_code": stage.GetStartTimeCode(),
        "end_time_code": stage.GetEndTimeCode(),
    }
    
    # Add default prim information if it exists
    if stage.HasDefaultPrim():
        default_prim = stage.GetDefaultPrim()
        info["default_prim"] = {
            "path": str(default_prim.GetPath()),
            "name": default_prim.GetName(),
            "type": default_prim.GetTypeName(),
        }
    
    return info


def format_hierarchy_node(prim: Usd.Prim, max_depth: int = -1, current_depth: int = 0) -> Dict[str, Any]:
    """
    Format a prim and its children as a hierarchy node.
    
    Args:
        prim: USD prim object
        max_depth: Maximum depth to traverse (-1 for unlimited)
        current_depth: Current traversal depth
        
    Returns:
        Dictionary representing the hierarchy node
    """
    node = format_prim_info(prim)
    
    # Add children if we haven't reached max depth
    if max_depth == -1 or current_depth < max_depth:
        children = []
        for child in prim.GetChildren():
            child_node = format_hierarchy_node(child, max_depth, current_depth + 1)
            children.append(child_node)
        node["children"] = children
    else:
        node["children"] = []
    
    return node