"""Example usage of the USD MCP Client."""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from client import USDMCPClient, USDMCPClientSync


async def async_example():
    """Example using the asynchronous client."""
    print("\n=== Asynchronous Client Example ===\n")
    
    # Create a client
    # You can specify the server script path or use the default
    server_script_path = os.path.join(
        Path(__file__).parents[2], 
        "usd-mcp", 
        "server", 
        "main.py"
    )
    client = USDMCPClient()
    
    try:
        # Connect to the server
        print("Connecting to server...")
        server_info = await client.connect(server_script_path)
        print(f"Connected to {server_info.get('name', 'Unknown Server')}")
        print(f"Available tools: {server_info.get('tools', [])}")
        
        # Sample USD file path - adjust as needed
        file_path = str(Path(__file__).parents[1] / "data" / "HelloWorld.usda")
        print(f"Using USD file: {file_path}")
        
        # Load a USD stage
        print("\nLoading USD stage...")
        stage_info = await client.load_usd_stage(file_path)
        print(f"Stage info: {stage_info}")
        
        # Get the stage hierarchy
        print("\nGetting stage hierarchy...")
        hierarchy = await client.get_stage_hierarchy(file_path, max_depth=2)
        print(f"Hierarchy: {hierarchy}")
        
        # List all prims
        print("\nListing all prims...")
        prims = await client.list_stage_prims(file_path)
        print(f"Prims: {prims}")
        
        # If we have prims, inspect the first one
        if prims and "prims" in prims and len(prims["prims"]) > 0:
            prim_path = prims["prims"][0]["path"]
            print(f"\nInspecting prim: {prim_path}")
            prim_info = await client.inspect_prim(file_path, prim_path)
            print(f"Prim info: {prim_info}")
            
            # Find prims by name
            name = prims["prims"][0]["name"]
            print(f"\nFinding prims with name: {name}")
            found_prims = await client.find_prims_by_name(file_path, name)
            print(f"Found prims: {found_prims}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the client
        await client.close()
        print("\nClient closed")


def sync_example():
    """Example using the synchronous client."""
    print("\n=== Synchronous Client Example ===\n")
    
    # Create a client
    # You can specify the server script path or use the default
    server_script_path = os.path.join(
        Path(__file__).parents[2], 
        "usd-mcp", 
        "server", 
        "main.py"
    )
    client = USDMCPClientSync(server_script_path)
    
    try:
        # Connect to the server
        print("Connecting to server...")
        server_info = client.connect()
        print(f"Connected to {server_info.get('name', 'Unknown Server')}")
        print(f"Available tools: {server_info.get('tools', [])}")
        
        # Sample USD file path - adjust as needed
        file_path = str(Path(__file__).parents[2] / "data" / "HelloWorld.usda")
        print(f"Using USD file: {file_path}")
        
        # Load a USD stage
        print("\nLoading USD stage...")
        stage_info = client.load_usd_stage(file_path)
        print(f"Stage info: {stage_info}")
        
        # Get the stage hierarchy
        print("\nGetting stage hierarchy...")
        hierarchy = client.get_stage_hierarchy(file_path, max_depth=2)
        print(f"Hierarchy: {hierarchy}")
        
        # List all prims
        print("\nListing all prims...")
        prims = client.list_stage_prims(file_path)
        print(f"Prims: {prims}")
        
        # If we have prims, inspect the first one
        if prims and "prims" in prims and len(prims["prims"]) > 0:
            prim_path = prims["prims"][0]["path"]
            print(f"\nInspecting prim: {prim_path}")
            prim_info = client.inspect_prim(file_path, prim_path)
            print(f"Prim info: {prim_info}")
            
            # Find prims by name
            name = prims["prims"][0]["name"]
            print(f"\nFinding prims with name: {name}")
            found_prims = client.find_prims_by_name(file_path, name)
            print(f"Found prims: {found_prims}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the client
        client.close()
        print("\nClient closed")


if __name__ == "__main__":
    # Run the async example
    asyncio.run(async_example())
    
    # Run the sync example
    # sync_example()  # Uncomment to run the sync example