"""Pytest fixtures for USD MCP Client tests."""

import asyncio
import os

# Import directly from the client.py file
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from pytest_testconfig import config

parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)
from client import USDMCPClient, USDMCPClientSync  # noqa: E402

USD_MCP_SERVER_PATH = "../../server/main.py"

@pytest.fixture
def sample_usd_file():
    """Return the path to a sample USD file."""
    # Using the HelloWorld.usda file from the project
    base_dir = Path(__file__).parents[3]  # Go up 3 levels from tests dir
    sample_file = base_dir / "data" / "HelloWorld.usda"
    
    if not sample_file.exists():
        pytest.skip(f"Sample USD file not found: {sample_file}")
    
    return str(sample_file)


@pytest.fixture
def server_script_path():
    """Return the path to the server script."""
    # Allow overriding via environment variable
    # env_path = os.environ.get("USD_MCP_SERVER_PATH")
    env_path = USD_MCP_SERVER_PATH
    if env_path:
        return env_path
        
    # Default path
    base_dir = Path(__file__).parents[3]  # Go up 3 levels from tests dir
    server_script = base_dir / "usd-mcp" / "server" / "main.py"
    
    if not server_script.exists():
        pytest.skip(f"Server script not found: {server_script}")
    
    return str(server_script)


@pytest_asyncio.fixture
async def async_client(server_script_path):
    """Return an async USD MCP client."""
    client = USDMCPClient(server_script_path)
    # For tests, we'll mock the session and exit_stack
    # so we don't need to actually connect to the server
    client.exit_stack = AsyncMock()
    client.session = None
    yield client
    # No need to close since we're mocking


@pytest.fixture
def sync_client(server_script_path):
    """Return a synchronous USD MCP client."""
    client = USDMCPClientSync(server_script_path)
    yield client
    client.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()