"""Main entry point for USD MCP Server using FastMCP."""

import os
import sys

# Add the usd-mcp directory to Python path for module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(current_dir)
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

# Try relative import first, then absolute import
try:
    from .server import server
except ImportError:
    from server import server


def main():
    """Main entry point for the USD MCP server."""
    server.run()


if __name__ == "__main__":
    main()