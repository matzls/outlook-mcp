"""
Read email functionality
"""
import sys
from urllib.parse import quote

import config
from utils.graph_api import call_graph_api
from auth import ensure_authenticated

async def handle_read_email(args):
    """
    Read email handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    email_id = args.get('id')
    
    if not email_id:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Email ID is required."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Make API call to get email details
        endpoint = f"me/messages/{quote(email_id)}"
        query_params = {
            '$select': config.EMAIL_DETAIL_FIELDS
        }
        
        try:
            email = await call_graph_api(access_token, 'GET', endpoint, None, query_params)
            
            if not email:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Email with ID {email_id} not found."
                        }
                    ]
                }
            
            # Format sender, recipients, etc.
            sender = f"{email.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')} ({email.get('from', {}).get('emailAddress', {}).get('address', 'unknown')})"
            
            # Format recipient lists
            to_recipients = email.get('toRecipients', [])
            to = ', '.join([f"{r.get('emailAddress', {}).get('name', 'Unknown')} ({r.get('emailAddress', {}).get('address', 'unknown')})" for r in to_recipients]) if to_recipients else 'None'
            
            cc_recipients = email.get('ccRecipients', [])
            cc = ', '.join([f"{r.get('emailAddress', {}).get('name', 'Unknown')} ({r.get('emailAddress', {}).get('address', 'unknown')})" for r in cc_recipients]) if cc_recipients else 'None'
            
            bcc_recipients = email.get('bccRecipients', [])
            bcc = ', '.join([f"{r.get('emailAddress', {}).get('name', 'Unknown')} ({r.get('emailAddress', {}).get('address', 'unknown')})" for r in bcc_recipients]) if bcc_recipients else 'None'
            
            date = email.get('receivedDateTime', 'Unknown date')
            
            # Extract body content
            body = ''
            if 'body' in email:
                body = email['body'].get('content', '')
                if email['body'].get('contentType') == 'html':
                    # Simple HTML-to-text conversion for HTML bodies
                    import re
                    body = re.sub(r'<[^>]*>', '', body)
            else:
                body = email.get('bodyPreview', 'No content')
            
            # Format the email
            formatted_email = f"From: {sender}\n"
            formatted_email += f"To: {to}\n"
            if cc != 'None':
                formatted_email += f"CC: {cc}\n"
            if bcc != 'None':
                formatted_email += f"BCC: {bcc}\n"
            formatted_email += f"Subject: {email.get('subject', 'No subject')}\n"
            formatted_email += f"Date: {date}\n"
            formatted_email += f"Importance: {email.get('importance', 'normal')}\n"
            formatted_email += f"Has Attachments: {'Yes' if email.get('hasAttachments', False) else 'No'}\n\n"
            formatted_email += body
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": formatted_email
                    }
                ]
            }
        except Exception as error:
            print(f"Error reading email: {str(error)}", file=sys.stderr)
            
            # Improved error handling with more specific messages
            error_msg = str(error)
            if "doesn't belong to the targeted mailbox" in error_msg:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"The email ID seems invalid or doesn't belong to your mailbox. Please try with a different email ID."
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Failed to read email: {error_msg}"
                        }
                    ]
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
                "text": f"Error accessing email: {str(error)}"
            }]
        }