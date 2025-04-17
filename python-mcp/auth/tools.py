"""
Authentication-related tools for the Outlook MCP server
"""
import config
from auth.token_manager import create_test_tokens, load_token_cache

async def handle_about():
    """
    About tool handler
    
    Returns:
        MCP response
    """
    return {
        "content": [{
            "type": "text",
            "text": f"📧 MODULAR Outlook Assistant MCP Server v{config.SERVER_VERSION} 📧\n\n"
                   f"Provides access to Microsoft Outlook email, calendar, and contacts through Microsoft Graph API.\n"
                   f"Implemented with a modular architecture for improved maintainability."
        }]
    }


async def handle_authenticate(args):
    """
    Authentication tool handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    force = args and args.get('force') == True
    
    # For test mode, create a test token
    if config.USE_TEST_MODE:
        # Create a test token with a 1-hour expiry
        create_test_tokens()
        
        return {
            "content": [{
                "type": "text",
                "text": 'Successfully authenticated with Microsoft Graph API (test mode)'
            }]
        }
    
    # For real authentication, generate an auth URL and instruct the user to visit it
    auth_url = f"{config.AUTH_CONFIG['authServerUrl']}/auth?client_id={config.AUTH_CONFIG['clientId']}"
    
    return {
        "content": [{
            "type": "text",
            "text": f"Authentication required. Please visit the following URL to authenticate with Microsoft: {auth_url}\n\n"
                   f"After authentication, you will be redirected back to this application."
        }]
    }


async def handle_check_auth_status():
    """
    Check authentication status tool handler
    
    Returns:
        MCP response
    """
    print('[CHECK-AUTH-STATUS] Starting authentication status check')
    
    tokens = load_token_cache()
    
    print(f"[CHECK-AUTH-STATUS] Tokens loaded: {'YES' if tokens else 'NO'}")
    
    if not tokens or 'access_token' not in tokens:
        print('[CHECK-AUTH-STATUS] No valid access token found')
        return {
            "content": [{"type": "text", "text": "Not authenticated"}]
        }
    
    print('[CHECK-AUTH-STATUS] Access token present')
    print(f"[CHECK-AUTH-STATUS] Token expires at: {tokens.get('expires_at')}")
    print(f"[CHECK-AUTH-STATUS] Current time: {int(time.time() * 1000)}")
    
    return {
        "content": [{"type": "text", "text": "Authenticated and ready"}]
    }


# Tool definitions
auth_tools = [
    {
        "name": "about",
        "description": "Returns information about this Outlook Assistant server",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "handler": handle_about
    },
    {
        "name": "authenticate",
        "description": "Authenticate with Microsoft Graph API to access Outlook data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "force": {
                    "type": "boolean",
                    "description": "Force re-authentication even if already authenticated"
                }
            },
            "required": []
        },
        "handler": handle_authenticate
    },
    {
        "name": "check-auth-status",
        "description": "Check the current authentication status with Microsoft Graph API",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "handler": handle_check_auth_status
    }
]