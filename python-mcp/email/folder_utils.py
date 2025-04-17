"""
Email folder utilities
"""
import sys
from utils.graph_api import call_graph_api

async def get_folder_id_by_name(access_token, folder_name):
    """
    Gets a folder ID by its display name
    
    Args:
        access_token: Access token for authentication
        folder_name: The display name of the folder
        
    Returns:
        The folder ID or None if not found
    """
    try:
        # Handle special case for inbox (case-insensitive)
        if folder_name.lower() == 'inbox':
            return 'inbox'
        
        # Query for the folder by name
        response = await call_graph_api(
            access_token,
            'GET',
            f"me/mailFolders?$filter=displayName eq '{folder_name}'",
            None
        )
        
        if response.get('value') and len(response['value']) > 0:
            return response['value'][0]['id']
        
        return None
    except Exception as error:
        print(f"Error getting folder ID for '{folder_name}': {error}", file=sys.stderr)
        return None


async def resolve_folder_path(access_token, folder_name):
    """
    Resolves a folder name to its Graph API endpoint path
    
    Args:
        access_token: Access token for authentication
        folder_name: The name of the folder
        
    Returns:
        The API endpoint path for the folder's messages
    """
    # Default endpoint is inbox
    endpoint = 'me/messages'
    
    # If not inbox, resolve the folder ID
    if folder_name.lower() != 'inbox':
        folder_id = await get_folder_id_by_name(access_token, folder_name)
        
        if folder_id:
            endpoint = f"me/mailFolders/{folder_id}/messages"
    
    return endpoint