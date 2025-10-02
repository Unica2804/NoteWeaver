"""
tools/notion_mcp_tool.py - Custom CrewAI tool for Notion MCP via Docker Gateway
"""

from crewai_tools import BaseTool
from typing import Type, Any, Dict, List, Optional
from pydantic import BaseModel, Field
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os


class NotionMCPInput(BaseModel):
    """Input schema for Notion MCP operations"""
    tool_name: str = Field(
        ..., 
        description="Name of the MCP tool to call (e.g., 'create-database', 'create-page', 'update-page', 'query-database')"
    )
    arguments: Dict[str, Any] = Field(
        ..., 
        description="Arguments to pass to the MCP tool"
    )


class NotionMCPTool(BaseTool):
    name: str = "Notion MCP Tool"
    description: str = (
        "Interacts with Notion via Docker MCP gateway using stdio. "
        "Calls any tool available in the Notion MCP server. "
        "Input must include 'tool_name' (the MCP tool to call) and 'arguments' (tool parameters)."
    )
    args_schema: Type[BaseModel] = NotionMCPInput
    
    # MCP Docker configuration
    docker_command: str = "docker"
    docker_args: List[str] = Field(
        default_factory=lambda: [
            "run",
            "--rm",
            "-i",
            "-e", "NOTION_TOKEN",
            "mcp/notion"
        ]
    )
    notion_token: str = Field(default_factory=lambda: os.getenv("NOTION_TOKEN", ""))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session: Optional[ClientSession] = None
        self._available_tools: List[Dict[str, Any]] = []
    
    async def _connect_mcp(self) -> ClientSession:
        """Establish connection to Docker MCP gateway via stdio"""
        server_params = StdioServerParameters(
            command=self.docker_command,
            args=self.docker_args,
            env={"NOTION_TOKEN": self.notion_token}
        )
        
        read, write = await stdio_client(server_params)
        self._session = ClientSession(read, write)
        await self._session.initialize()
        
        # List available tools from the MCP server
        tools_result = await self._session.list_tools()
        self._available_tools = tools_result.tools
        
        return self._session
    
    async def _disconnect_mcp(self):
        """Close MCP connection"""
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except:
                pass
            self._session = None
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool on the Notion server"""
        session = await self._connect_mcp()
        
        try:
            # Verify tool exists
            tool_exists = any(tool.name == tool_name for tool in self._available_tools)
            if not tool_exists:
                available_names = [tool.name for tool in self._available_tools]
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found. Available tools: {available_names}"
                }
            
            # Call the MCP tool
            result = await session.call_tool(tool_name, arguments=arguments)
            
            return {
                "success": True,
                "tool_name": tool_name,
                "result": result.content if hasattr(result, 'content') else result
            }
        
        except Exception as e:
            return {
                "success": False,
                "tool_name": tool_name,
                "error": str(e)
            }
        
        finally:
            await self._disconnect_mcp()
    
    async def _list_available_tools(self) -> Dict[str, Any]:
        """List all available tools from the MCP server"""
        session = await self._connect_mcp()
        
        try:
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description if hasattr(tool, 'description') else "",
                    "inputSchema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                }
                for tool in self._available_tools
            ]
            
            return {
                "success": True,
                "tools": tools
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        
        finally:
            await self._disconnect_mcp()
    
    def _run(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Synchronous run method required by CrewAI"""
        try:
            # Handle special command to list tools
            if tool_name == "list_tools":
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._list_available_tools())
                loop.close()
                return json.dumps(result, indent=2)
            
            # Run async MCP tool call in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self._call_mcp_tool(tool_name, arguments)
            )
            loop.close()
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            })


# Helper functions
def create_notion_mcp_tool(notion_token: Optional[str] = None) -> NotionMCPTool:
    """
    Factory function to create NotionMCPTool instance
    
    Args:
        notion_token: Notion API token (if not provided, reads from NOTION_TOKEN env var)
        
    Returns:
        Configured NotionMCPTool instance
    """
    if notion_token:
        return NotionMCPTool(notion_token=notion_token)
    return NotionMCPTool()


# Example usage helper for common operations
class NotionOperations:
    """Helper class with common Notion operations"""
    
    @staticmethod
    def create_database(parent_page_id: str, title: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Format arguments for creating a Notion database"""
        return {
            "tool_name": "create-database",
            "arguments": {
                "parent_page_id": parent_page_id,
                "title": title,
                "properties": properties
            }
        }
    
    @staticmethod
    def create_page(database_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Format arguments for creating a Notion page"""
        return {
            "tool_name": "create-page",
            "arguments": {
                "database_id": database_id,
                "properties": properties
            }
        }
    
    @staticmethod
    def update_page(page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Format arguments for updating a Notion page"""
        return {
            "tool_name": "update-page",
            "arguments": {
                "page_id": page_id,
                "properties": properties
            }
        }
    
    @staticmethod
    def query_database(database_id: str, filter_conditions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format arguments for querying a Notion database"""
        args = {"database_id": database_id}
        if filter_conditions:
            args["filter"] = filter_conditions
        return {
            "tool_name": "query-database",
            "arguments": args
        }
    
    @staticmethod
    def list_available_tools() -> Dict[str, Any]:
        """Get list of all available MCP tools"""
        return {
            "tool_name": "list_tools",
            "arguments": {}
        }