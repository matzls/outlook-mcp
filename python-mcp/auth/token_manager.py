"""
Token management for Microsoft Graph API authentication
"""
import os
import json
import time
from pathlib import Path

import config

# Global variable to store tokens
cached_tokens = None

def load_token_cache():
    """
    Loads authentication tokens from the token file
    
    Returns:
        The loaded tokens or None if not available
    """
    global cached_tokens
    try:
        token_path = config.AUTH_CONFIG["tokenStorePath"]
        print(f"[DEBUG] Attempting to load tokens from: {token_path}")
        print(f"[DEBUG] HOME directory: {os.environ.get('HOME', '')}")
        print(f"[DEBUG] Full resolved path: {token_path}")
        
        # Log file existence and details
        token_path_obj = Path(token_path)
        if not token_path_obj.exists():
            print('[DEBUG] Token file does not exist')
            return None
        
        stats = token_path_obj.stat()
        print(f"[DEBUG] Token file stats:\n"
              f"  Size: {stats.st_size} bytes\n"
              f"  Created: {stats.st_ctime}\n"
              f"  Modified: {stats.st_mtime}")
        
        token_data = token_path_obj.read_text(encoding='utf-8')
        print(f'[DEBUG] Token file contents length: {len(token_data)}')
        print(f'[DEBUG] Token file first 200 characters: {token_data[:200]}')
        
        try:
            tokens = json.loads(token_data)
            print(f'[DEBUG] Parsed tokens keys: {list(tokens.keys())}')
            
            # Log each key's value to see what's present
            for key, value in tokens.items():
                print(f'[DEBUG] {key}: {type(value)}')
            
            # Check for access token presence
            if 'access_token' not in tokens:
                print('[DEBUG] No access_token found in tokens')
                return None
            
            # Check token expiration
            now = int(time.time() * 1000)  # Current time in milliseconds
            expires_at = tokens.get('expires_at', 0)
            
            print(f'[DEBUG] Current time: {now}')
            print(f'[DEBUG] Token expires at: {expires_at}')
            
            if now > expires_at:
                print('[DEBUG] Token has expired')
                return None
            
            # Update the cache
            cached_tokens = tokens
            return tokens
        except json.JSONDecodeError as parse_error:
            print(f'[DEBUG] Error parsing token JSON: {parse_error}')
            return None
    except Exception as error:
        print(f'[DEBUG] Error loading token cache: {error}')
        return None


def save_token_cache(tokens):
    """
    Saves authentication tokens to the token file
    
    Args:
        tokens: The tokens to save
        
    Returns:
        Whether the save was successful
    """
    global cached_tokens
    try:
        token_path = config.AUTH_CONFIG["tokenStorePath"]
        print(f"Saving tokens to: {token_path}")
        
        # Ensure directory exists
        Path(token_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write tokens to file
        with open(token_path, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2)
        
        print('Tokens saved successfully')
        
        # Update the cache
        cached_tokens = tokens
        return True
    except Exception as error:
        print(f'Error saving token cache: {error}')
        return False


def get_access_token():
    """
    Gets the current access token, loading from cache if necessary
    
    Returns:
        The access token or None if not available
    """
    global cached_tokens
    if cached_tokens and 'access_token' in cached_tokens:
        return cached_tokens['access_token']
    
    tokens = load_token_cache()
    return tokens['access_token'] if tokens else None


def create_test_tokens():
    """
    Creates a test access token for use in test mode
    
    Returns:
        The test tokens
    """
    test_tokens = {
        'access_token': f"test_access_token_{int(time.time())}",
        'refresh_token': f"test_refresh_token_{int(time.time())}",
        'expires_at': int(time.time() * 1000) + (3600 * 1000)  # 1 hour
    }
    
    save_token_cache(test_tokens)
    return test_tokens