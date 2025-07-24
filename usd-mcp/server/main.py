"""Main entry point for USD MCP Server using FastMCP."""

import os
import sys

# Add the usd-mcp directory to Python path for module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(current_dir)
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Import the FastMCP server instance directly from the server module
import sys
import os

# Add current directory to path to avoid import conflicts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the server module file directly
import server as server_module


def main():
    """Main entry point for the USD MCP server."""
    # Get the FastMCP server instance from the server module
    server_instance = server_module.server
    # FastMCP servers use run() for stdio communication
    server_instance.run()


if __name__ == "__main__":
    main()