"""
List folders functionality
"""
import sys
from utils.graph_api import call_graph_api
from auth import ensure_authenticated

async def handle_list_folders(args):
    """
    List folders handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    include_item_counts = args.get('includeItemCounts') == True
    include_children = args.get('includeChildren') == True
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Get all mail folders
        folders = await get_all_folders_hierarchy(access_token, include_item_counts)
        
        # If including children, format as hierarchy
        if include_children:
            return {
                "content": [{ 
                    "type": "text", 
                    "text": format_folder_hierarchy(folders, include_item_counts)
                }]
            }
        else:
            # Otherwise, format as flat list
            return {
                "content": [{ 
                    "type": "text", 
                    "text": format_folder_list(folders, include_item_counts)
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
                "text": f"Error listing folders: {str(error)}"
            }]
        }


async def get_all_folders_hierarchy(access_token, include_item_counts):
    """
    Get all mail folders with hierarchy information
    
    Args:
        access_token: Access token
        include_item_counts: Include item counts in response
        
    Returns:
        Array of folder objects with hierarchy
    """
    try:
        # Determine select fields based on whether to include counts
        select_fields = 'id,displayName,parentFolderId,childFolderCount,totalItemCount,unreadItemCount' if include_item_counts else 'id,displayName,parentFolderId,childFolderCount'
        
        # Get all mail folders
        response = await call_graph_api(
            access_token,
            'GET',
            'me/mailFolders',
            None,
            { 
                '$top': 100,
                '$select': select_fields
            }
        )
        
        if not response.get('value'):
            return []
        
        # Get child folders for folders with children
        folders_with_children = [f for f in response['value'] if f.get('childFolderCount', 0) > 0]
        
        all_child_folders = []
        for folder in folders_with_children:
            try:
                child_response = await call_graph_api(
                    access_token,
                    'GET',
                    f"me/mailFolders/{folder['id']}/childFolders",
                    None,
                    {'$select': select_fields}
                )
                
                # Add parent folder info to each child
                child_folders = child_response.get('value', [])
                for child in child_folders:
                    child['parentFolder'] = folder.get('displayName')
                
                all_child_folders.extend(child_folders)
            except Exception as error:
                print(f"Error getting child folders for \"{folder.get('displayName', 'Unknown')}\": {str(error)}", file=sys.stderr)
        
        # Add top-level flag to parent folders
        top_level_folders = []
        for folder in response['value']:
            folder['isTopLevel'] = True
            top_level_folders.append(folder)
        
        # Combine all folders
        return top_level_folders + all_child_folders
    except Exception as error:
        print(f"Error getting all folders: {str(error)}", file=sys.stderr)
        raise


def format_folder_list(folders, include_item_counts):
    """
    Format folders as a flat list
    
    Args:
        folders: Array of folder objects
        include_item_counts: Whether to include item counts
        
    Returns:
        Formatted list
    """
    if not folders or len(folders) == 0:
        return "No folders found."
    
    # Sort folders alphabetically, with well-known folders first
    well_known_folder_names = ['Inbox', 'Drafts', 'Sent Items', 'Deleted Items', 'Junk Email', 'Archive']
    
    def folder_sort_key(folder):
        name = folder.get('displayName', '')
        if name in well_known_folder_names:
            # Well-known folders come first, sorted by their index in the array
            return (0, well_known_folder_names.index(name))
        else:
            # Other folders come later, sorted alphabetically
            return (1, name.lower())
    
    sorted_folders = sorted(folders, key=folder_sort_key)
    
    # Format each folder
    folder_lines = []
    for folder in sorted_folders:
        folder_info = folder.get('displayName', 'Unknown')
        
        # Add parent folder info if available
        if 'parentFolder' in folder:
            folder_info += f" (in {folder['parentFolder']})"
        
        # Add item counts if requested
        if include_item_counts:
            unread_count = folder.get('unreadItemCount', 0)
            total_count = folder.get('totalItemCount', 0)
            folder_info += f" - {total_count} items"
            
            if unread_count > 0:
                folder_info += f" ({unread_count} unread)"
        
        folder_lines.append(folder_info)
    
    return f"Found {len(folders)} folders:\n\n" + "\n".join(folder_lines)


def format_folder_hierarchy(folders, include_item_counts):
    """
    Format folders as a hierarchical tree
    
    Args:
        folders: Array of folder objects
        include_item_counts: Whether to include item counts
        
    Returns:
        Formatted hierarchy
    """
    if not folders or len(folders) == 0:
        return "No folders found."
    
    # Build folder hierarchy
    folder_map = {}
    root_folders = []
    
    # First pass: create map of all folders
    for folder in folders:
        folder_id = folder.get('id')
        if folder_id:
            folder_map[folder_id] = {
                **folder,
                'children': []
            }
            
            if folder.get('isTopLevel'):
                root_folders.append(folder_id)
    
    # Second pass: build hierarchy
    for folder in folders:
        if not folder.get('isTopLevel') and folder.get('parentFolderId'):
            parent = folder_map.get(folder['parentFolderId'])
            if parent:
                parent['children'].append(folder['id'])
            else:
                # Fallback for orphaned folders
                root_folders.append(folder['id'])
    
    # Format hierarchy recursively
    def format_subtree(folder_id, level=0):
        folder = folder_map.get(folder_id)
        if not folder:
            return ''
        
        indent = '  ' * level
        line = f"{indent}{folder.get('displayName', 'Unknown')}"
        
        # Add item counts if requested
        if include_item_counts:
            unread_count = folder.get('unreadItemCount', 0)
            total_count = folder.get('totalItemCount', 0)
            line += f" - {total_count} items"
            
            if unread_count > 0:
                line += f" ({unread_count} unread)"
        
        # Add children
        child_lines = []
        for child_id in folder.get('children', []):
            child_line = format_subtree(child_id, level + 1)
            if child_line:
                child_lines.append(child_line)
        
        if child_lines:
            return line + '\n' + '\n'.join(child_lines)
        else:
            return line
    
    # Format all root folders
    formatted_hierarchy = []
    for folder_id in root_folders:
        formatted_hierarchy.append(format_subtree(folder_id))
    
    return "Folder Hierarchy:\n\n" + "\n".join(formatted_hierarchy)