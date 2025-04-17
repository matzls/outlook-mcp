"""
Move emails functionality
"""
import sys
from utils.graph_api import call_graph_api
from auth import ensure_authenticated
from email.folder_utils import get_folder_id_by_name

async def handle_move_emails(args):
    """
    Move emails handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    email_ids = args.get('emailIds', '')
    target_folder = args.get('targetFolder', '')
    source_folder = args.get('sourceFolder', '')
    
    if not email_ids:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Email IDs are required. Please provide a comma-separated list of email IDs to move."
            }]
        }
    
    if not target_folder:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Target folder name is required."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Parse email IDs
        ids = [id.strip() for id in email_ids.split(',') if id.strip()]
        
        if not ids:
            return {
                "content": [{ 
                    "type": "text", 
                    "text": "No valid email IDs provided."
                }]
            }
        
        # Move emails
        result = await move_emails_to_folder(access_token, ids, target_folder, source_folder)
        
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
                "text": f"Error moving emails: {str(error)}"
            }]
        }


async def move_emails_to_folder(access_token, email_ids, target_folder_name, source_folder_name):
    """
    Move emails to a folder
    
    Args:
        access_token: Access token
        email_ids: Array of email IDs to move
        target_folder_name: Name of the target folder
        source_folder_name: Name of the source folder (optional)
        
    Returns:
        Result object with status and message
    """
    try:
        # Get the target folder ID
        target_folder_id = await get_folder_id_by_name(access_token, target_folder_name)
        if not target_folder_id:
            return {
                'success': False,
                'message': f'Target folder "{target_folder_name}" not found. Please specify a valid folder name.'
            }
        
        # Track successful and failed moves
        results = {
            'successful': [],
            'failed': []
        }
        
        # Process each email one by one to handle errors independently
        for email_id in email_ids:
            try:
                # Move the email
                await call_graph_api(
                    access_token,
                    'POST',
                    f"me/messages/{email_id}/move",
                    {
                        'destinationId': target_folder_id
                    }
                )
                
                results['successful'].append(email_id)
            except Exception as error:
                print(f"Error moving email {email_id}: {str(error)}", file=sys.stderr)
                results['failed'].append({
                    'id': email_id,
                    'error': str(error)
                })
        
        # Generate result message
        message = ''
        
        if results['successful']:
            message += f"Successfully moved {len(results['successful'])} email(s) to \"{target_folder_name}\"."
        
        if results['failed']:
            if message:
                message += '\n\n'
            message += f"Failed to move {len(results['failed'])} email(s). Errors:"
            
            # Show first few errors with details
            max_errors = min(len(results['failed']), 3)
            for i in range(max_errors):
                failure = results['failed'][i]
                message += f"\n- Email {i+1}: {failure['error']}"
            
            # If there are more errors, just mention the count
            if len(results['failed']) > max_errors:
                message += f"\n...and {len(results['failed']) - max_errors} more."
        
        return {
            'success': len(results['successful']) > 0,
            'message': message,
            'results': results
        }
    except Exception as error:
        print(f"Error in move_emails_to_folder: {str(error)}", file=sys.stderr)
        raise