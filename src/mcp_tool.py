import os
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter

def get_notion_mcp_tools():
    """Return a list of Notion MCP tools"""
    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "--rm",
            "-i",
            "-e", f"NOTION_TOKEN={os.getenv('NOTION_TOKEN', '')}",
            "mcp/notion"
        ],
        env=os.environ.copy()
    )

    adapter = MCPServerAdapter(server_params, connect_timeout=60)
    return adapter.tools  # ✅ Proper way
