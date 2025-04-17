"""
Email module for Outlook MCP server
"""
from email.list import handle_list_emails
from email.search import handle_search_emails
from email.read import handle_read_email
from email.send import handle_send_email

# Email tool definitions
email_tools = [
    {
        "name": "list-emails",
        "description": "Lists recent emails from your inbox",
        "inputSchema": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "Email folder to list (e.g., 'inbox', 'sent', 'drafts', default: 'inbox')"
                },
                "count": {
                    "type": "number",
                    "description": "Number of emails to retrieve (default: 10, max: 50)"
                }
            },
            "required": []
        },
        "handler": handle_list_emails
    },
    {
        "name": "search-emails",
        "description": "Search for emails using various criteria",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query text to find in emails"
                },
                "folder": {
                    "type": "string",
                    "description": "Email folder to search in (default: 'inbox')"
                },
                "from": {
                    "type": "string",
                    "description": "Filter by sender email address or name"
                },
                "to": {
                    "type": "string",
                    "description": "Filter by recipient email address or name"
                },
                "subject": {
                    "type": "string",
                    "description": "Filter by email subject"
                },
                "hasAttachments": {
                    "type": "boolean",
                    "description": "Filter to only emails with attachments"
                },
                "unreadOnly": {
                    "type": "boolean",
                    "description": "Filter to only unread emails"
                },
                "count": {
                    "type": "number",
                    "description": "Number of results to return (default: 10, max: 50)"
                }
            },
            "required": []
        },
        "handler": handle_search_emails
    },
    {
        "name": "read-email",
        "description": "Reads the content of a specific email",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID of the email to read"
                }
            },
            "required": ["id"]
        },
        "handler": handle_read_email
    },
    {
        "name": "send-email",
        "description": "Composes and sends a new email",
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Comma-separated list of recipient email addresses"
                },
                "cc": {
                    "type": "string",
                    "description": "Comma-separated list of CC recipient email addresses"
                },
                "bcc": {
                    "type": "string",
                    "description": "Comma-separated list of BCC recipient email addresses"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },
                "body": {
                    "type": "string",
                    "description": "Email body content (can be plain text or HTML)"
                },
                "importance": {
                    "type": "string",
                    "description": "Email importance (normal, high, low)",
                    "enum": ["normal", "high", "low"]
                },
                "saveToSentItems": {
                    "type": "boolean",
                    "description": "Whether to save the email to sent items"
                }
            },
            "required": ["to", "subject", "body"]
        },
        "handler": handle_send_email
    }
]