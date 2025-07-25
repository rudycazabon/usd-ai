"""Main entry point for USD MCP Server using FastMCP."""

import os
import sys

from .server import server

# Add the usd-mcp directory to Python path for module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(current_dir)
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Add current directory to path to avoid import conflicts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the USD MCP server."""
    # Get the FastMCP server instance from the server module
    server_instance = server
    # FastMCP servers use run() for stdio communication
    server_instance.run()


if __name__ == "__main__":
    main()