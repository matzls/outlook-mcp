"""
Create folder functionality
"""
import sys
from utils.graph_api import call_graph_api
from auth import ensure_authenticated
from email.folder_utils import get_folder_id_by_name

async def handle_create_folder(args):
    """
    Create folder handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    folder_name = args.get('name')
    parent_folder = args.get('parentFolder', '')
    
    if not folder_name:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Folder name is required."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Create folder with appropriate parent
        result = await create_mail_folder(access_token, folder_name, parent_folder)
        
        return {
            "content": [{ 
                "type": "text", 
                "text": result['message']
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
                "text": f"Error creating folder: {str(error)}"
            }]
        }


async def create_mail_folder(access_token, folder_name, parent_folder_name):
    """
    Create a new mail folder
    
    Args:
        access_token: Access token
        folder_name: Name of the folder to create
        parent_folder_name: Name of the parent folder (optional)
        
    Returns:
        Result object with status and message
    """
    try:
        # Check if a folder with this name already exists
        existing_folder = await get_folder_id_by_name(access_token, folder_name)
        if existing_folder:
            return {
                'success': False,
                'message': f'A folder named "{folder_name}" already exists.'
            }
        
        # If parent folder specified, find its ID
        endpoint = 'me/mailFolders'
        if parent_folder_name:
            parent_id = await get_folder_id_by_name(access_token, parent_folder_name)
            if not parent_id:
                return {
                    'success': False,
                    'message': f'Parent folder "{parent_folder_name}" not found. Please specify a valid parent folder or leave it blank to create at the root level.'
                }
            
            endpoint = f"me/mailFolders/{parent_id}/childFolders"
        
        # Create the folder
        folder_data = {
            'displayName': folder_name
        }
        
        response = await call_graph_api(
            access_token,
            'POST',
            endpoint,
            folder_data
        )
        
        if response and 'id' in response:
            location_info = f'inside "{parent_folder_name}"' if parent_folder_name else "at the root level"
                
            return {
                'success': True,
                'message': f'Successfully created folder "{folder_name}" {location_info}.',
                'folderId': response['id']
            }
        else:
            return {
                'success': False,
                'message': "Failed to create folder. The server didn't return a folder ID."
            }
    except Exception as error:
        print(f'Error creating folder "{folder_name}": {str(error)}', file=sys.stderr)
        raise