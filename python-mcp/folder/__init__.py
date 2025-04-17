"""
Folder management module for Outlook MCP server
"""
from folder.list import handle_list_folders
from folder.create import handle_create_folder
from folder.move import handle_move_emails

# Folder management tool definitions
folder_tools = [
    {
        "name": "list-folders",
        "description": "Lists mail folders in your Outlook account",
        "inputSchema": {
            "type": "object",
            "properties": {
                "includeItemCounts": {
                    "type": "boolean",
                    "description": "Include counts of total and unread items"
                },
                "includeChildren": {
                    "type": "boolean",
                    "description": "Include child folders in hierarchy"
                }
            },
            "required": []
        },
        "handler": handle_list_folders
    },
    {
        "name": "create-folder",
        "description": "Creates a new mail folder",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the folder to create"
                },
                "parentFolder": {
                    "type": "string",
                    "description": "Optional parent folder name (default is root)"
                }
            },
            "required": ["name"]
        },
        "handler": handle_create_folder
    },
    {
        "name": "move-emails",
        "description": "Moves emails from one folder to another",
        "inputSchema": {
            "type": "object",
            "properties": {
                "emailIds": {
                    "type": "string",
                    "description": "Comma-separated list of email IDs to move"
                },
                "targetFolder": {
                    "type": "string",
                    "description": "Name of the folder to move emails to"
                },
                "sourceFolder": {
                    "type": "string",
                    "description": "Optional name of the source folder (default is inbox)"
                }
            },
            "required": ["emailIds", "targetFolder"]
        },
        "handler": handle_move_emails
    }
]