"""
Mock data functions for test mode
"""
from datetime import datetime, timedelta
import json

def simulate_graph_api_response(method, path, data, query_params):
    """
    Simulates Microsoft Graph API responses for testing
    
    Args:
        method: HTTP method
        path: API path
        data: Request data
        query_params: Query parameters
        
    Returns:
        Simulated API response
    """
    print(f"Simulating response for: {method} {path}")
    
    if method == 'GET':
        if 'messages' in path and 'sendMail' not in path:
            # Simulate a successful email list/search response
            if '/messages/' in path:
                # Single email response
                return {
                    "id": "simulated-email-id",
                    "subject": "Simulated Email Subject",
                    "from": {
                        "emailAddress": {
                            "name": "Simulated Sender",
                            "address": "sender@example.com"
                        }
                    },
                    "toRecipients": [{
                        "emailAddress": {
                            "name": "Recipient Name",
                            "address": "recipient@example.com"
                        }
                    }],
                    "ccRecipients": [],
                    "bccRecipients": [],
                    "receivedDateTime": datetime.now().isoformat(),
                    "bodyPreview": "This is a simulated email preview...",
                    "body": {
                        "contentType": "text",
                        "content": "This is the full content of the simulated email. Since we can't connect to the real Microsoft Graph API, we're returning this placeholder content instead."
                    },
                    "hasAttachments": False,
                    "importance": "normal",
                    "isRead": False,
                    "internetMessageHeaders": []
                }
            else:
                # Email list response
                return {
                    "value": [
                        {
                            "id": "simulated-email-1",
                            "subject": "Important Meeting Tomorrow",
                            "from": {
                                "emailAddress": {
                                    "name": "John Doe",
                                    "address": "john@example.com"
                                }
                            },
                            "toRecipients": [{
                                "emailAddress": {
                                    "name": "You",
                                    "address": "you@example.com"
                                }
                            }],
                            "ccRecipients": [],
                            "receivedDateTime": datetime.now().isoformat(),
                            "bodyPreview": "Let's discuss the project status...",
                            "hasAttachments": False,
                            "importance": "high",
                            "isRead": False
                        },
                        {
                            "id": "simulated-email-2",
                            "subject": "Weekly Report",
                            "from": {
                                "emailAddress": {
                                    "name": "Jane Smith",
                                    "address": "jane@example.com"
                                }
                            },
                            "toRecipients": [{
                                "emailAddress": {
                                    "name": "You",
                                    "address": "you@example.com"
                                }
                            }],
                            "ccRecipients": [],
                            "receivedDateTime": (datetime.now() - timedelta(days=1)).isoformat(),
                            "bodyPreview": "Please find attached the weekly report...",
                            "hasAttachments": True,
                            "importance": "normal",
                            "isRead": True
                        },
                        {
                            "id": "simulated-email-3",
                            "subject": "Question about the project",
                            "from": {
                                "emailAddress": {
                                    "name": "Bob Johnson",
                                    "address": "bob@example.com"
                                }
                            },
                            "toRecipients": [{
                                "emailAddress": {
                                    "name": "You",
                                    "address": "you@example.com"
                                }
                            }],
                            "ccRecipients": [],
                            "receivedDateTime": (datetime.now() - timedelta(days=2)).isoformat(),
                            "bodyPreview": "I had a question about the timeline...",
                            "hasAttachments": False,
                            "importance": "normal",
                            "isRead": False
                        }
                    ]
                }
        elif 'mailFolders' in path:
            # Simulate a mail folders response
            return {
                "value": [
                    {"id": "inbox", "displayName": "Inbox"},
                    {"id": "drafts", "displayName": "Drafts"},
                    {"id": "sentItems", "displayName": "Sent Items"},
                    {"id": "deleteditems", "displayName": "Deleted Items"}
                ]
            }
    elif method == 'POST' and 'sendMail' in path:
        # Simulate a successful email send
        return {}
    
    # If we get here, we don't have a simulation for this endpoint
    print(f"No simulation available for: {method} {path}")
    return {}