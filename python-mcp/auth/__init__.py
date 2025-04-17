"""
Authentication module for Outlook MCP server
"""
from auth.token_manager import get_access_token
from auth.tools import auth_tools

async def ensure_authenticated(force_new=False):
    """
    Ensures the user is authenticated and returns an access token
    
    Args:
        force_new: Whether to force a new authentication
        
    Returns:
        Access token
        
    Raises:
        Exception: If authentication fails
    """
    if force_new:
        # Force re-authentication
        raise Exception('Authentication required')
    
    # Check for existing token
    access_token = get_access_token()
    if not access_token:
        raise Exception('Authentication required')
    
    return access_token