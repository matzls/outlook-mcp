"""
Microsoft Graph API helper functions
"""
import json
import requests

import config
from utils import mock_data


async def call_graph_api(access_token, method, path, data=None, query_params=None):
    """
    Makes a request to the Microsoft Graph API
    
    Args:
        access_token: The access token for authentication
        method: HTTP method (GET, POST, etc.)
        path: API endpoint path
        data: Data to send for POST/PUT requests
        query_params: Query parameters
        
    Returns:
        The API response as a dictionary
    """
    # For test tokens, we'll simulate the API call
    if config.USE_TEST_MODE and access_token.startswith('test_access_token_'):
        print(f"TEST MODE: Simulating {method} {path} API call", file=sys.stderr)
        return mock_data.simulate_graph_api_response(method, path, data, query_params)
    
    try:
        print(f"Making real API call: {method} {path}", file=sys.stderr)
        
        # Build the full URL
        url = f"{config.GRAPH_API_ENDPOINT}{path}"
        
        # Configure headers
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        
        # Make the API call using requests
        response = None
        if method == 'GET':
            response = requests.get(url, headers=headers, params=query_params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, params=query_params)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, params=query_params)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, params=query_params)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, params=query_params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Check for success
        response.raise_for_status()
        
        # Parse JSON response
        if response.text:
            return response.json()
        else:
            return {}
        
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 401:
            raise Exception("UNAUTHORIZED")
        
        # Try to get error details from response
        error_message = str(http_err)
        try:
            error_data = http_err.response.json()
            if 'error' in error_data:
                error_message = error_data['error'].get('message', str(http_err))
        except:
            pass
        
        raise Exception(f"API call failed: {error_message}")
    
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Network error during API call: {str(req_err)}")
    
    except Exception as err:
        raise Exception(f"Error calling Graph API: {str(err)}")