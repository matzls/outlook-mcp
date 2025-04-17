"""
OData helper functions for Microsoft Graph API
"""
import re

def escape_odata_string(string):
    """
    Escapes a string for use in OData queries
    
    Args:
        string: The string to escape
        
    Returns:
        The escaped string
    """
    if not string:
        return string
    
    # Replace single quotes with double single quotes (OData escaping)
    # And remove any special characters that could cause OData syntax errors
    string = string.replace("'", "''")
    
    # Escape other potentially problematic characters
    string = re.sub(r'[\(\)\{\}\[\]\:\;\,\/\?\&\=\+\*\%\$\#\@\!\^]', '', string)
    
    print(f"Escaped OData string: '{string}'")
    return string


def build_odata_filter(conditions):
    """
    Builds an OData filter from filter conditions
    
    Args:
        conditions: Array of filter conditions
        
    Returns:
        Combined OData filter expression
    """
    if not conditions or len(conditions) == 0:
        return ''
    
    return ' and '.join(conditions)