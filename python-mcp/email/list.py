"""
List emails functionality
"""
import sys
import config
from utils.graph_api import call_graph_api
from auth import ensure_authenticated
from email.folder_utils import resolve_folder_path

async def handle_list_emails(args):
    """
    List emails handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    folder = args.get('folder', 'inbox')
    count = min(args.get('count', 10), config.MAX_RESULT_COUNT)
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Resolve the folder path
        endpoint = await resolve_folder_path(access_token, folder)
        
        # Add query parameters
        query_params = {
            '$top': count,
            '$orderby': 'receivedDateTime desc',
            '$select': config.EMAIL_SELECT_FIELDS
        }
        
        # Make API call
        response = await call_graph_api(access_token, 'GET', endpoint, None, query_params)
        
        if not response.get('value') or len(response['value']) == 0:
            return {
                "content": [{ 
                    "type": "text", 
                    "text": f"No emails found in {folder}."
                }]
            }
        
        # Format results
        email_list = []
        for index, email in enumerate(response['value']):
            sender = email.get('from', {}).get('emailAddress', {'name': 'Unknown', 'address': 'unknown'})
            date = email.get('receivedDateTime', '')
            read_status = '' if email.get('isRead', True) else '[UNREAD] '
            
            email_entry = (
                f"{index + 1}. {read_status}{date} - From: {sender['name']} ({sender['address']})\n"
                f"Subject: {email.get('subject', 'No Subject')}\n"
                f"ID: {email.get('id', 'unknown')}\n"
            )
            email_list.append(email_entry)
        
        return {
            "content": [{ 
                "type": "text", 
                "text": f"Found {len(response['value'])} emails in {folder}:\n\n" + "\n".join(email_list)
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
                "text": f"Error listing emails: {str(error)}"
            }]
        }