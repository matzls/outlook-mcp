"""
Send email functionality
"""
import sys
import config
from utils.graph_api import call_graph_api
from auth import ensure_authenticated

async def handle_send_email(args):
    """
    Send email handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    to = args.get('to')
    cc = args.get('cc')
    bcc = args.get('bcc')
    subject = args.get('subject')
    body = args.get('body')
    importance = args.get('importance', 'normal')
    save_to_sent_items = args.get('saveToSentItems', True)
    
    # Validate required parameters
    if not to:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Recipient (to) is required."
            }]
        }
    
    if not subject:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Subject is required."
            }]
        }
    
    if not body:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Body content is required."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Format recipients
        to_recipients = [
            {
                "emailAddress": {
                    "address": email.strip()
                }
            } for email in to.split(',')
        ]
        
        cc_recipients = []
        if cc:
            cc_recipients = [
                {
                    "emailAddress": {
                        "address": email.strip()
                    }
                } for email in cc.split(',')
            ]
        
        bcc_recipients = []
        if bcc:
            bcc_recipients = [
                {
                    "emailAddress": {
                        "address": email.strip()
                    }
                } for email in bcc.split(',')
            ]
        
        # Determine content type (HTML or text)
        content_type = 'html' if '<html' in body else 'text'
        
        # Prepare email object
        email_object = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": content_type,
                    "content": body
                },
                "toRecipients": to_recipients,
                "importance": importance
            },
            "saveToSentItems": save_to_sent_items
        }
        
        # Add CC and BCC recipients if any
        if cc_recipients:
            email_object["message"]["ccRecipients"] = cc_recipients
        
        if bcc_recipients:
            email_object["message"]["bccRecipients"] = bcc_recipients
        
        # Make API call to send email
        await call_graph_api(access_token, 'POST', 'me/sendMail', email_object)
        
        # Build confirmation message
        recipients_count = f"{len(to_recipients)}"
        if cc_recipients:
            recipients_count += f" + {len(cc_recipients)} CC"
        if bcc_recipients:
            recipients_count += f" + {len(bcc_recipients)} BCC"
        
        return {
            "content": [{ 
                "type": "text", 
                "text": f"Email sent successfully!\n\nSubject: {subject}\nRecipients: {recipients_count}\nMessage Length: {len(body)} characters"
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
                "text": f"Error sending email: {str(error)}"
            }]
        }