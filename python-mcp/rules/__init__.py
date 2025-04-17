"""
Email rules management module for Outlook MCP server
"""
from rules.list import handle_list_rules, get_inbox_rules
from rules.create import handle_create_rule

# Import required for the edit sequence tool
from auth import ensure_authenticated
from utils.graph_api import call_graph_api

async def handle_edit_rule_sequence(args):
    """
    Edit rule sequence handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    rule_name = args.get('ruleName')
    sequence = args.get('sequence')
    
    if not rule_name:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Rule name is required. Please specify the exact name of an existing rule."
            }]
        }
    
    if not sequence or not isinstance(sequence, (int, float)) or sequence < 1:
        return {
            "content": [{ 
                "type": "text", 
                "text": "A positive sequence number is required. Lower numbers run first (higher priority)."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Get all rules
        rules = await get_inbox_rules(access_token)
        
        # Find the rule by name
        rule = next((r for r in rules if r.get('displayName') == rule_name), None)
        if not rule:
            return {
                "content": [{ 
                    "type": "text", 
                    "text": f'Rule with name "{rule_name}" not found.'
                }]
            }
        
        # Update the rule sequence
        await call_graph_api(
            access_token,
            'PATCH',
            f"me/mailFolders/inbox/messageRules/{rule['id']}",
            {
                'sequence': sequence
            }
        )
        
        return {
            "content": [{ 
                "type": "text", 
                "text": f'Successfully updated the sequence of rule "{rule_name}" to {sequence}.'
            }]
        }
    except Exception as error:
        if str(error) == 'Authentication required':
            return {
                "content": [{ 
                    "type": "text", 
                    "text": "Authentication required. Please use the 'authenticate' tool first."
                }]
            }
        
        return {
            "content": [{ 
                "type": "text", 
                "text": f"Error updating rule sequence: {str(error)}"
            }]
        }

# Rules management tool definitions
rules_tools = [
    {
        "name": "list-rules",
        "description": "Lists inbox rules in your Outlook account",
        "inputSchema": {
            "type": "object",
            "properties": {
                "includeDetails": {
                    "type": "boolean",
                    "description": "Include detailed rule conditions and actions"
                }
            },
            "required": []
        },
        "handler": handle_list_rules
    },
    {
        "name": "create-rule",
        "description": "Creates a new inbox rule",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the rule to create"
                },
                "fromAddresses": {
                    "type": "string",
                    "description": "Comma-separated list of sender email addresses for the rule"
                },
                "containsSubject": {
                    "type": "string",
                    "description": "Subject text the email must contain"
                },
                "hasAttachments": {
                    "type": "boolean",
                    "description": "Whether the rule applies to emails with attachments"
                },
                "moveToFolder": {
                    "type": "string",
                    "description": "Name of the folder to move matching emails to"
                },
                "markAsRead": {
                    "type": "boolean", 
                    "description": "Whether to mark matching emails as read"
                },
                "isEnabled": {
                    "type": "boolean",
                    "description": "Whether the rule should be enabled after creation (default: true)"
                },
                "sequence": {
                    "type": "number",
                    "description": "Order in which the rule is executed (lower numbers run first, default: 100)"
                }
            },
            "required": ["name"]
        },
        "handler": handle_create_rule
    },
    {
        "name": "edit-rule-sequence",
        "description": "Changes the execution order of an existing inbox rule",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ruleName": {
                    "type": "string",
                    "description": "Name of the rule to modify"
                },
                "sequence": {
                    "type": "number",
                    "description": "New sequence value for the rule (lower numbers run first)"
                }
            },
            "required": ["ruleName", "sequence"]
        },
        "handler": handle_edit_rule_sequence
    }
]