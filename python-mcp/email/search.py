"""
Improved search emails functionality
"""
import sys
import time

import config
from utils.graph_api import call_graph_api
from auth import ensure_authenticated
from email.folder_utils import resolve_folder_path

async def handle_search_emails(args):
    """
    Search emails handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    folder = args.get('folder', 'inbox')
    count = min(args.get('count', 10), config.MAX_RESULT_COUNT)
    query = args.get('query', '')
    from_addr = args.get('from', '')
    to_addr = args.get('to', '')
    subject = args.get('subject', '')
    has_attachments = args.get('hasAttachments')
    unread_only = args.get('unreadOnly')
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Resolve the folder path
        endpoint = await resolve_folder_path(access_token, folder)
        print(f"Using endpoint: {endpoint} for folder: {folder}", file=sys.stderr)
        
        # Execute progressive search
        response = await progressive_search(
            endpoint, 
            access_token, 
            {'query': query, 'from': from_addr, 'to': to_addr, 'subject': subject},
            {'hasAttachments': has_attachments, 'unreadOnly': unread_only},
            count
        )
        
        return format_search_results(response)
    except Exception as error:
        # Handle authentication errors
        if str(error) == 'Authentication required':
            return {
                "content": [{ 
                    "type": "text", 
                    "text": "Authentication required. Please use the 'authenticate' tool first."
                }]
            }
        
        # General error response
        return {
            "content": [{ 
                "type": "text", 
                "text": f"Error searching emails: {str(error)}"
            }]
        }


async def progressive_search(endpoint, access_token, search_terms, filter_terms, count):
    """
    Execute a search with progressively simpler fallback strategies
    
    Args:
        endpoint: API endpoint
        access_token: Access token
        search_terms: Search terms (query, from, to, subject)
        filter_terms: Filter terms (hasAttachments, unreadOnly)
        count: Maximum number of results
        
    Returns:
        Search results
    """
    # Track search strategies attempted
    search_attempts = []
    
    # 1. Try combined search (most specific)
    try:
        params = build_search_params(search_terms, filter_terms, count)
        print(f"Attempting combined search with params: {params}", file=sys.stderr)
        search_attempts.append("combined-search")
        
        response = await call_graph_api(access_token, 'GET', endpoint, None, params)
        if response.get('value') and len(response['value']) > 0:
            print(f"Combined search successful: found {len(response['value'])} results", file=sys.stderr)
            return response
    except Exception as error:
        print(f"Combined search failed: {str(error)}", file=sys.stderr)
    
    # 2. Try each search term individually, starting with most specific
    search_priority = ['subject', 'from', 'to', 'query']
    
    for term in search_priority:
        if search_terms.get(term):
            try:
                print(f"Attempting search with only {term}: \"{search_terms[term]}\"", file=sys.stderr)
                search_attempts.append(f"single-term-{term}")
                
                # For single term search, only use $search with that term
                simplified_params = {
                    '$top': count,
                    '$select': config.EMAIL_SELECT_FIELDS,
                    '$orderby': 'receivedDateTime desc'
                }
                
                # Add the search term in the appropriate KQL syntax
                if term == 'query':
                    # General query doesn't need a prefix
                    simplified_params['$search'] = f"\"{search_terms[term]}\""
                else:
                    # Specific field searches use field:value syntax
                    simplified_params['$search'] = f"{term}:\"{search_terms[term]}\""
                
                # Add boolean filters if applicable
                add_boolean_filters(simplified_params, filter_terms)
                
                response = await call_graph_api(access_token, 'GET', endpoint, None, simplified_params)
                if response.get('value') and len(response['value']) > 0:
                    print(f"Search with {term} successful: found {len(response['value'])} results", file=sys.stderr)
                    return response
            except Exception as error:
                print(f"Search with {term} failed: {str(error)}", file=sys.stderr)
    
    # 3. Try with only boolean filters
    if filter_terms.get('hasAttachments') == True or filter_terms.get('unreadOnly') == True:
        try:
            print("Attempting search with only boolean filters", file=sys.stderr)
            search_attempts.append("boolean-filters-only")
            
            filter_only_params = {
                '$top': count,
                '$select': config.EMAIL_SELECT_FIELDS,
                '$orderby': 'receivedDateTime desc'
            }
            
            # Add the boolean filters
            add_boolean_filters(filter_only_params, filter_terms)
            
            response = await call_graph_api(access_token, 'GET', endpoint, None, filter_only_params)
            value_count = len(response.get('value', [])) if response else 0
            print(f"Boolean filter search found {value_count} results", file=sys.stderr)
            return response
        except Exception as error:
            print(f"Boolean filter search failed: {str(error)}", file=sys.stderr)
    
    # 4. Final fallback: just get recent emails
    print("All search strategies failed, falling back to recent emails", file=sys.stderr)
    search_attempts.append("recent-emails")
    
    basic_params = {
        '$top': count,
        '$select': config.EMAIL_SELECT_FIELDS,
        '$orderby': 'receivedDateTime desc'
    }
    
    response = await call_graph_api(access_token, 'GET', endpoint, None, basic_params)
    value_count = len(response.get('value', [])) if response else 0
    print(f"Fallback to recent emails found {value_count} results", file=sys.stderr)
    
    # Add a note to the response about the search attempts
    response['_searchInfo'] = {
        'attemptsCount': len(search_attempts),
        'strategies': search_attempts,
        'originalTerms': search_terms,
        'filterTerms': filter_terms
    }
    
    return response


def build_search_params(search_terms, filter_terms, count):
    """
    Build search parameters from search terms and filter terms
    
    Args:
        search_terms: Search terms (query, from, to, subject)
        filter_terms: Filter terms (hasAttachments, unreadOnly)
        count: Maximum number of results
        
    Returns:
        Query parameters
    """
    params = {
        '$top': count,
        '$select': config.EMAIL_SELECT_FIELDS,
        '$orderby': 'receivedDateTime desc'
    }
    
    # Handle search terms
    kql_terms = []
    
    if search_terms.get('query'):
        # General query doesn't need a prefix
        kql_terms.append(search_terms['query'])
    
    if search_terms.get('subject'):
        kql_terms.append(f"subject:\"{search_terms['subject']}\"")
    
    if search_terms.get('from'):
        kql_terms.append(f"from:\"{search_terms['from']}\"")
    
    if search_terms.get('to'):
        kql_terms.append(f"to:\"{search_terms['to']}\"")
    
    # Add $search if we have any search terms
    if kql_terms:
        params['$search'] = ' '.join(kql_terms)
    
    # Add boolean filters
    add_boolean_filters(params, filter_terms)
    
    return params


def add_boolean_filters(params, filter_terms):
    """
    Add boolean filters to query parameters
    
    Args:
        params: Query parameters
        filter_terms: Filter terms (hasAttachments, unreadOnly)
    """
    filter_conditions = []
    
    if filter_terms.get('hasAttachments') == True:
        filter_conditions.append('hasAttachments eq true')
    
    if filter_terms.get('unreadOnly') == True:
        filter_conditions.append('isRead eq false')
    
    # Add $filter parameter if we have any filter conditions
    if filter_conditions:
        params['$filter'] = ' and '.join(filter_conditions)


def format_search_results(response):
    """
    Format search results into a readable text format
    
    Args:
        response: The API response object
        
    Returns:
        MCP response object
    """
    if not response.get('value') or len(response['value']) == 0:
        return {
            "content": [{ 
                "type": "text", 
                "text": "No emails found matching your search criteria."
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
    
    # Add search strategy info if available
    additional_info = ''
    if '_searchInfo' in response:
        search_info = response['_searchInfo']
        strategy = search_info['strategies'][-1] if search_info['strategies'] else 'unknown'
        additional_info = f"\n(Search used {strategy} strategy)"
    
    return {
        "content": [{ 
            "type": "text", 
            "text": f"Found {len(response['value'])} emails matching your search criteria:{additional_info}\n\n" + "\n".join(email_list)
        }]
    }