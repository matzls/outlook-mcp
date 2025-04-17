#!/usr/bin/env python3
"""
Outlook MCP Server - Main entry point

A Model Context Protocol server that provides access to
Microsoft Outlook through the Microsoft Graph API.
"""
import sys
import json
import signal
import asyncio
from modelcontextprotocol.sdk.server import Server
from modelcontextprotocol.sdk.server.stdio import StdioServerTransport

# Import configuration
import config

# Import module tools
from auth import auth_tools
from email import email_tools
from folder import folder_tools
from rules import rules_tools

# Log startup information
print(f"STARTING {config.SERVER_NAME.upper()} MCP SERVER", file=sys.stderr)
print(f"Test mode is {'enabled' if config.USE_TEST_MODE else 'disabled'}", file=sys.stderr)

# Combine all tools
TOOLS = [
    *auth_tools,
    *email_tools,
    *folder_tools,
    *rules_tools
    # Future modules: calendar_tools, contacts_tools, etc.
]

def create_server():
    """Create and configure the MCP server"""
    # Create server with tools capabilities
    server = Server(
        {"name": config.SERVER_NAME, "version": config.SERVER_VERSION},
        {
            "capabilities": {
                "tools": {tool["name"]: {} for tool in TOOLS}
            }
        }
    )
    
    # Set up the fallback request handler
    async def fallback_request_handler(request):
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            print(f"REQUEST: {method} [{request_id}]", file=sys.stderr)
            
            # Initialize handler
            if method == "initialize":
                print(f"INITIALIZE REQUEST: ID [{request_id}]", file=sys.stderr)
                return {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {tool["name"]: {} for tool in TOOLS}
                    },
                    "serverInfo": {"name": config.SERVER_NAME, "version": config.SERVER_VERSION}
                }
            
            # Tools list handler
            if method == "tools/list":
                print(f"TOOLS LIST REQUEST: ID [{request_id}]", file=sys.stderr)
                print(f"TOOLS COUNT: {len(TOOLS)}", file=sys.stderr)
                print(f"TOOLS NAMES: {', '.join(tool['name'] for tool in TOOLS)}", file=sys.stderr)
                
                return {
                    "tools": [{
                        "name": tool["name"],
                        "description": tool["description"],
                        "inputSchema": tool["inputSchema"]
                    } for tool in TOOLS]
                }
            
            # Required empty responses for other capabilities
            if method == "resources/list":
                return {"resources": []}
            if method == "prompts/list":
                return {"prompts": []}
            
            # Tool call handler
            if method == "tools/call":
                try:
                    name = params.get("name", "")
                    args = params.get("arguments", {})
                    
                    print(f"TOOL CALL: {name}", file=sys.stderr)
                    
                    # Find the tool handler
                    tool = next((t for t in TOOLS if t["name"] == name), None)
                    
                    if tool and "handler" in tool:
                        return await tool["handler"](args)
                    
                    # Tool not found
                    return {
                        "error": {
                            "code": -32601,
                            "message": f"Tool not found: {name}"
                        }
                    }
                except Exception as error:
                    print(f"Error in tools/call: {error}", file=sys.stderr)
                    return {
                        "error": {
                            "code": -32603,
                            "message": f"Error processing tool call: {str(error)}"
                        }
                    }
            
            # For any other method, return method not found
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        except Exception as error:
            print(f"Error in fallbackRequestHandler: {error}", file=sys.stderr)
            return {
                "error": {
                    "code": -32603,
                    "message": f"Error processing request: {str(error)}"
                }
            }
    
    server.fallback_request_handler = fallback_request_handler
    return server


async def main():
    """Main entry point for the MCP server"""
    # Make the script executable
    signal.signal(signal.SIGTERM, lambda sig, frame: print('SIGTERM received but staying alive', file=sys.stderr))
    
    # Create and start the server
    server = create_server()
    transport = StdioServerTransport()
    
    try:
        await server.connect(transport)
        print(f"{config.SERVER_NAME} connected and listening", file=sys.stderr)
    except Exception as error:
        print(f"Connection error: {str(error)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())