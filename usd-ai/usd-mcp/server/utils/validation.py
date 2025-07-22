"""Validation utilities for USD MCP server."""

import os
from pathlib import Path
from typing import Tuple


def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """
    Validate that a file path exists and is readable.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path:
        return False, "File path cannot be empty"
    
    path = Path(file_path)
    
    if not path.exists():
        return False, f"File does not exist: {file_path}"
    
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"
    
    if not os.access(path, os.R_OK):
        return False, f"File is not readable: {file_path}"
    
    # Check if it's a USD file by extension
    valid_extensions = {'.usd', '.usda', '.usdc', '.usdz'}
    if path.suffix.lower() not in valid_extensions:
        return False, f"File does not have a valid USD extension: {file_path}"
    
    return True, ""


def validate_prim_path(prim_path: str) -> Tuple[bool, str]:
    """
    Validate that a prim path has correct USD format.
    
    Args:
        prim_path: USD prim path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not prim_path:
        return False, "Prim path cannot be empty"
    
    if not prim_path.startswith('/'):
        return False, "Prim path must start with '/'"
    
    # Basic validation - USD paths should not contain certain characters
    invalid_chars = ['<', '>', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in prim_path:
            return False, f"Prim path contains invalid character '{char}': {prim_path}"
    
    return True, ""