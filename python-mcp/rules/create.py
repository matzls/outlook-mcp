"""
Create rule functionality
"""
import sys
import math
from utils.graph_api import call_graph_api
from auth import ensure_authenticated
from email.folder_utils import get_folder_id_by_name
from rules.list import get_inbox_rules

async def handle_create_rule(args):
    """
    Create rule handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    name = args.get('name')
    from_addresses = args.get('fromAddresses')
    contains_subject = args.get('containsSubject')
    has_attachments = args.get('hasAttachments')
    move_to_folder = args.get('moveToFolder')
    mark_as_read = args.get('markAsRead')
    is_enabled = args.get('isEnabled', True)
    sequence = args.get('sequence')
    
    # Add validation for sequence parameter
    if sequence is not None and (not isinstance(sequence, (int, float)) or sequence < 1):
        return {
            "content": [{ 
                "type": "text", 
                "text": "Sequence must be a positive number greater than zero."
            }]
        }
    
    if not name:
        return {
            "content": [{ 
                "type": "text", 
                "text": "Rule name is required."
            }]
        }
    
    # Validate that at least one condition or action is specified
    has_condition = bool(from_addresses or contains_subject or has_attachments is True)
    has_action = bool(move_to_folder or mark_as_read is True)
    
    if not has_condition:
        return {
            "content": [{ 
                "type": "text", 
                "text": "At least one condition is required. Specify fromAddresses, containsSubject, or hasAttachments."
            }]
        }
    
    if not has_action:
        return {
            "content": [{ 
                "type": "text", 
                "text": "At least one action is required. Specify moveToFolder or markAsRead."
            }]
        }
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Create rule
        result = await create_inbox_rule(access_token, {
            'name': name,
            'fromAddresses': from_addresses,
            'containsSubject': contains_subject,
            'hasAttachments': has_attachments,
            'moveToFolder': move_to_folder,
            'markAsRead': mark_as_read,
            'isEnabled': is_enabled,
            'sequence': sequence
        })
        
        response_text = result['message']
        
        # Add a tip about sequence if it wasn't provided
        if sequence is None and not result.get('error'):
            response_text += "\n\nTip: You can specify a 'sequence' parameter when creating rules to control their execution order. Lower sequence numbers run first."
        
        return {
            "content": [{ 
                "type": "text", 
                "text": response_text
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
                "text": f"Error creating rule: {str(error)}"
            }]
        }


async def create_inbox_rule(access_token, rule_options):
    """
    Create a new inbox rule
    
    Args:
        access_token: Access token
        rule_options: Rule creation options
        
    Returns:
        Result object with status and message
    """
    try:
        name = rule_options.get('name')
        from_addresses = rule_options.get('fromAddresses')
        contains_subject = rule_options.get('containsSubject')
        has_attachments = rule_options.get('hasAttachments')
        move_to_folder = rule_options.get('moveToFolder')
        mark_as_read = rule_options.get('markAsRead')
        is_enabled = rule_options.get('isEnabled', True)
        sequence = rule_options.get('sequence')
        
        # Get existing rules to determine sequence if not provided
        rule_sequence = sequence
        if rule_sequence is None:
            try:
                # Default to 100 if we can't get existing rules
                rule_sequence = 100
                
                # Get existing rules to find highest sequence
                existing_rules = await get_inbox_rules(access_token)
                if existing_rules and len(existing_rules) > 0:
                    # Find the highest sequence
                    highest_sequence = max([r.get('sequence', 0) for r in existing_rules])
                    # Set new rule sequence to be higher
                    rule_sequence = max(highest_sequence + 1, 100)
                    print(f"Auto-generated sequence: {rule_sequence} (based on highest existing: {highest_sequence})", file=sys.stderr)
            except Exception as sequence_error:
                print(f"Error determining rule sequence: {str(sequence_error)}", file=sys.stderr)
                # Fall back to default value
                rule_sequence = 100
        
        print(f"Using rule sequence: {rule_sequence}", file=sys.stderr)
        
        # Make sure sequence is a positive integer
        rule_sequence = max(1, math.floor(rule_sequence))
        
        # Build rule object with sequence
        rule = {
            'displayName': name,
            'isEnabled': is_enabled == True,
            'sequence': rule_sequence,
            'conditions': {},
            'actions': {}
        }
        
        # Add conditions
        if from_addresses:
            # Parse email addresses
            email_addresses = []
            for email in from_addresses.split(','):
                email = email.strip()
                if email:
                    email_addresses.append({
                        'emailAddress': {
                            'address': email
                        }
                    })
            
            if email_addresses:
                rule['conditions']['fromAddresses'] = email_addresses
        
        if contains_subject:
            rule['conditions']['subjectContains'] = [contains_subject]
        
        if has_attachments == True:
            rule['conditions']['hasAttachment'] = True
        
        # Add actions
        if move_to_folder:
            # Get folder ID
            try:
                folder_id = await get_folder_id_by_name(access_token, move_to_folder)
                if not folder_id:
                    return {
                        'success': False,
                        'message': f'Target folder "{move_to_folder}" not found. Please specify a valid folder name.'
                    }
                
                rule['actions']['moveToFolder'] = folder_id
            except Exception as folder_error:
                print(f'Error resolving folder "{move_to_folder}": {str(folder_error)}', file=sys.stderr)
                return {
                    'success': False,
                    'message': f'Error resolving folder "{move_to_folder}": {str(folder_error)}'
                }
        
        if mark_as_read == True:
            rule['actions']['markAsRead'] = True
        
        # Create the rule
        response = await call_graph_api(
            access_token,
            'POST',
            'me/mailFolders/inbox/messageRules',
            rule
        )
        
        if response and 'id' in response:
            return {
                'success': True,
                'message': f'Successfully created rule "{name}" with sequence {rule_sequence}.',
                'ruleId': response['id']
            }
        else:
            return {
                'success': False,
                'message': "Failed to create rule. The server didn't return a rule ID."
            }
    except Exception as error:
        print(f"Error creating rule: {str(error)}", file=sys.stderr)
        raise