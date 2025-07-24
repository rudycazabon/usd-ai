"""USD Stage management for MCP server."""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from pxr import Usd

from utils.validation import validate_file_path


class USDStageManager:
    """Manages USD stage loading and caching."""
    
    def __init__(self):
        """Initialize the stage manager with an empty cache."""
        self._stage_cache: Dict[str, Usd.Stage] = {}
    
    def load_stage(self, file_path: str) -> Tuple[Optional[Usd.Stage], Optional[str]]:
        """
        Load a USD stage from file, using cache if available.
        
        Args:
            file_path: Path to the USD file
            
        Returns:
            Tuple of (stage, error_message). Stage is None if loading failed.
        """
        # Validate file path first
        is_valid, error_msg = validate_file_path(file_path)
        if not is_valid:
            return None, error_msg
        
        # Normalize the path for consistent caching
        normalized_path = str(Path(file_path).resolve())
        
        # Check cache first
        if normalized_path in self._stage_cache:
            stage = self._stage_cache[normalized_path]
            # Verify the stage is still valid
            if stage and stage.GetRootLayer():
                return stage, None
            else:
                # Remove invalid stage from cache
                del self._stage_cache[normalized_path]
        
        # Load the stage
        try:
            stage = Usd.Stage.Open(normalized_path)
            if not stage:
                return None, f"Failed to open USD stage: {file_path}"
            
            # Cache the stage
            self._stage_cache[normalized_path] = stage
            return stage, None
            
        except Exception as e:
            return None, f"Error loading USD stage: {str(e)}"
    
    def get_cached_stage(self, file_path: str) -> Optional[Usd.Stage]:
        """
        Get a cached stage without loading.
        
        Args:
            file_path: Path to the USD file
            
        Returns:
            Cached stage or None if not found
        """
        normalized_path = str(Path(file_path).resolve())
        return self._stage_cache.get(normalized_path)
    
    def clear_cache(self) -> None:
        """Clear all cached stages."""
        self._stage_cache.clear()
    
    def remove_from_cache(self, file_path: str) -> bool:
        """
        Remove a specific stage from cache.
        
        Args:
            file_path: Path to the USD file
            
        Returns:
            True if stage was removed, False if not found
        """
        normalized_path = str(Path(file_path).resolve())
        if normalized_path in self._stage_cache:
            del self._stage_cache[normalized_path]
            return True
        return False
    
    def get_cache_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about cached stages.
        
        Returns:
            Dictionary with cache information
        """
        cache_info = {}
        for path, stage in self._stage_cache.items():
            if stage and stage.GetRootLayer():
                cache_info[path] = {
                    "is_valid": True,
                    "root_layer": stage.GetRootLayer().identifier,
                    "has_default_prim": stage.HasDefaultPrim(),
                }
            else:
                cache_info[path] = {
                    "is_valid": False,
                    "error": "Invalid stage in cache"
                }
        
        return cache_info


# Global stage manager instance
_stage_manager = USDStageManager()


def get_stage_manager() -> USDStageManager:
    """Get the global stage manager instance."""
    return _stage_manager