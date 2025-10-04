import os
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter


def get_obsidian_mcp_tools():
    """Return a list of Obsidian MCP tools"""

    # Get environment variables
    obsidian_host = os.getenv("OBSIDIAN_HOST", "http://localhost:27124")
    obsidian_key = os.getenv("OBSIDIAN_API_KEY", "")

    print(f"🔍 Obsidian Host: {obsidian_host}")
    print(f"🔍 API Key exists: {bool(obsidian_key)}")

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "--network=host",  # Use host network
            "-e",
            f"OBSIDIAN_HOST={obsidian_host}",
            "-e",
            f"OBSIDIAN_API_KEY={obsidian_key}",
            "mcp/obsidian",
        ],
        env=None,  # Don't pass full environment, just what we specify
    )

    adapter = MCPServerAdapter(server_params, connect_timeout=60)
    return adapter.tools
