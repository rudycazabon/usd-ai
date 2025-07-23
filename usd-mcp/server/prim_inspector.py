"""USD Prim inspection utilities for MCP server."""

from typing import Any, Dict, List, Optional, Tuple

from server.stage_manager import get_stage_manager
from server.utils.formatting import (
    format_hierarchy_node,
    format_prim_info,
    format_property_info,
)
from server.utils.validation import validate_prim_path


class USDPrimInspector:
    """Handles USD prim inspection and hierarchy traversal."""
    
    def __init__(self):
        """Initialize the prim inspector."""
        self.stage_manager = get_stage_manager()
    
    def get_prim_info(self, file_path: str, prim_path: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Get detailed information about a specific prim.
        
        Args:
            file_path: Path to the USD file
            prim_path: Path to the prim within the stage
            
        Returns:
            Tuple of (prim_info, error_message)
        """
        # Validate prim path
        is_valid, error_msg = validate_prim_path(prim_path)
        if not is_valid:
            return None, error_msg
        
        # Load stage
        stage, error_msg = self.stage_manager.load_stage(file_path)
        if not stage:
            return None, error_msg
        
        # Get the prim
        prim = stage.GetPrimAtPath(prim_path)
        if not prim:
            return None, f"Prim not found at path: {prim_path}"
        
        if not prim.IsValid():
            return None, f"Invalid prim at path: {prim_path}"
        
        # Build detailed prim information
        prim_info = format_prim_info(prim)
        
        # Add properties information
        properties = []
        for prop_name in prim.GetPropertyNames():
            prop = prim.GetProperty(prop_name)
            if prop:
                prop_info = format_property_info(prop)
                properties.append(prop_info)
        
        prim_info["properties"] = properties
        prim_info["property_count"] = len(properties)
        
        # Add children information
        children = []
        for child in prim.GetChildren():
            child_info = format_prim_info(child)
            children.append(child_info)
        
        prim_info["children"] = children
        prim_info["child_count"] = len(children)
        
        # Add parent information
        parent = prim.GetParent()
        if parent and parent.IsValid():
            prim_info["parent"] = format_prim_info(parent)
        else:
            prim_info["parent"] = None
        
        return prim_info, None
    
    def get_stage_hierarchy(self, file_path: str, max_depth: int = -1) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Get the complete hierarchy of prims in a stage.
        
        Args:
            file_path: Path to the USD file
            max_depth: Maximum depth to traverse (-1 for unlimited)
            
        Returns:
            Tuple of (hierarchy, error_message)
        """
        # Load stage
        stage, error_msg = self.stage_manager.load_stage(file_path)
        if not stage:
            return None, error_msg
        
        # Start from the pseudo-root
        pseudo_root = stage.GetPseudoRoot()
        if not pseudo_root:
            return None, "Could not get stage pseudo-root"
        
        # Build hierarchy starting from root
        hierarchy = format_hierarchy_node(pseudo_root, max_depth)
        
        return hierarchy, None
    
    def list_prims(self, file_path: str, prim_type: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        List all prims in a stage, optionally filtered by type.
        
        Args:
            file_path: Path to the USD file
            prim_type: Optional prim type to filter by (e.g., 'Sphere', 'Xform')
            
        Returns:
            Tuple of (prim_list, error_message)
        """
        # Load stage
        stage, error_msg = self.stage_manager.load_stage(file_path)
        if not stage:
            return None, error_msg
        
        prims = []
        
        # Traverse all prims in the stage
        for prim in stage.Traverse():
            if not prim.IsValid():
                continue
            
            # Apply type filter if specified
            if prim_type and prim.GetTypeName() != prim_type:
                continue
            
            prim_info = format_prim_info(prim)
            
            # Add some additional useful information for listing
            prim_info["property_count"] = len(prim.GetPropertyNames())
            prim_info["child_count"] = len(prim.GetChildren())
            
            prims.append(prim_info)
        
        return prims, None
    
    def get_prim_properties(self, file_path: str, prim_path: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Get all properties of a specific prim.
        
        Args:
            file_path: Path to the USD file
            prim_path: Path to the prim within the stage
            
        Returns:
            Tuple of (properties_list, error_message)
        """
        # Validate prim path
        is_valid, error_msg = validate_prim_path(prim_path)
        if not is_valid:
            return None, error_msg
        
        # Load stage
        stage, error_msg = self.stage_manager.load_stage(file_path)
        if not stage:
            return None, error_msg
        
        # Get the prim
        prim = stage.GetPrimAtPath(prim_path)
        if not prim or not prim.IsValid():
            return None, f"Invalid prim at path: {prim_path}"
        
        # Get all properties
        properties = []
        for prop_name in prim.GetPropertyNames():
            prop = prim.GetProperty(prop_name)
            if prop:
                prop_info = format_property_info(prop)
                properties.append(prop_info)
        
        return properties, None
    
    def find_prims_by_name(self, file_path: str, name_pattern: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Find prims by name pattern.
        
        Args:
            file_path: Path to the USD file
            name_pattern: Name pattern to search for (exact match for now)
            
        Returns:
            Tuple of (matching_prims, error_message)
        """
        # Load stage
        stage, error_msg = self.stage_manager.load_stage(file_path)
        if not stage:
            return None, error_msg
        
        matching_prims = []
        
        # Traverse all prims and check names
        for prim in stage.Traverse():
            if not prim.IsValid():
                continue
            
            if prim.GetName() == name_pattern:
                prim_info = format_prim_info(prim)
                prim_info["property_count"] = len(prim.GetPropertyNames())
                prim_info["child_count"] = len(prim.GetChildren())
                matching_prims.append(prim_info)
        
        return matching_prims, None


# Global prim inspector instance
_prim_inspector = USDPrimInspector()


def get_prim_inspector() -> USDPrimInspector:
    """Get the global prim inspector instance."""
    return _prim_inspector