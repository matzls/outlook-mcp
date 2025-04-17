"""
List rules functionality
"""
import sys
from utils.graph_api import call_graph_api
from auth import ensure_authenticated

async def handle_list_rules(args):
    """
    List rules handler
    
    Args:
        args: Tool arguments
        
    Returns:
        MCP response
    """
    include_details = args.get('includeDetails') == True
    
    try:
        # Get access token
        access_token = await ensure_authenticated()
        
        # Get all inbox rules
        rules = await get_inbox_rules(access_token)
        
        # Format the rules based on detail level
        formatted_rules = format_rules_list(rules, include_details)
        
        return {
            "content": [{ 
                "type": "text", 
                "text": formatted_rules
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
                "text": f"Error listing rules: {str(error)}"
            }]
        }


async def get_inbox_rules(access_token):
    """
    Get all inbox rules
    
    Args:
        access_token: Access token
        
    Returns:
        Array of rule objects
    """
    try:
        response = await call_graph_api(
            access_token,
            'GET',
            'me/mailFolders/inbox/messageRules',
            None
        )
        
        return response.get('value', [])
    except Exception as error:
        print(f"Error getting inbox rules: {str(error)}", file=sys.stderr)
        raise


def format_rules_list(rules, include_details):
    """
    Format rules list for display
    
    Args:
        rules: Array of rule objects
        include_details: Whether to include detailed conditions and actions
        
    Returns:
        Formatted rules list
    """
    if not rules or len(rules) == 0:
        return "No inbox rules found.\n\nTip: You can create rules using the 'create-rule' tool. Rules are processed in order of their sequence number (lower numbers are processed first)."
    
    # Sort rules by sequence to show execution order
    sorted_rules = sorted(rules, key=lambda r: r.get('sequence', 9999))
    
    # Format rules based on detail level
    if include_details:
        # Detailed format
        detailed_rules = []
        for index, rule in enumerate(sorted_rules):
            # Format rule header with sequence
            is_enabled = rule.get('isEnabled', True)
            disabled_marker = ' (Disabled)' if not is_enabled else ''
            sequence_value = rule.get('sequence', 'N/A')
            rule_text = f"{index + 1}. {rule.get('displayName')}{disabled_marker} - Sequence: {sequence_value}"
            
            # Format conditions
            conditions = format_rule_conditions(rule)
            if conditions:
                rule_text += f"\n   Conditions: {conditions}"
            
            # Format actions
            actions = format_rule_actions(rule)
            if actions:
                rule_text += f"\n   Actions: {actions}"
            
            detailed_rules.append(rule_text)
        
        return f"Found {len(rules)} inbox rules (sorted by execution order):\n\n" + "\n\n".join(detailed_rules) + "\n\nRules are processed in order of their sequence number. You can change rule order using the 'edit-rule-sequence' tool."
    else:
        # Simple format
        simple_rules = []
        for index, rule in enumerate(sorted_rules):
            is_enabled = rule.get('isEnabled', True)
            disabled_marker = ' (Disabled)' if not is_enabled else ''
            sequence_value = rule.get('sequence', 'N/A')
            simple_rules.append(f"{index + 1}. {rule.get('displayName')}{disabled_marker} - Sequence: {sequence_value}")
        
        return f"Found {len(rules)} inbox rules (sorted by execution order):\n\n" + "\n".join(simple_rules) + "\n\nTip: Use 'list-rules with includeDetails=true' to see more information about each rule."


def format_rule_conditions(rule):
    """
    Format rule conditions for display
    
    Args:
        rule: Rule object
        
    Returns:
        Formatted conditions
    """
    conditions = []
    rule_conditions = rule.get('conditions', {})
    
    # From addresses
    from_addresses = rule_conditions.get('fromAddresses', [])
    if from_addresses:
        senders = ', '.join([addr.get('emailAddress', {}).get('address', 'unknown') for addr in from_addresses])
        conditions.append(f"From: {senders}")
    
    # Subject contains
    subject_contains = rule_conditions.get('subjectContains', [])
    if subject_contains:
        conditions.append(f"Subject contains: \"{', '.join(subject_contains)}\"")
    
    # Contains body text
    body_contains = rule_conditions.get('bodyContains', [])
    if body_contains:
        conditions.append(f"Body contains: \"{', '.join(body_contains)}\"")
    
    # Has attachment
    if rule_conditions.get('hasAttachment') == True:
        conditions.append('Has attachment')
    
    # Importance
    importance = rule_conditions.get('importance')
    if importance:
        conditions.append(f"Importance: {importance}")
    
    return '; '.join(conditions)


def format_rule_actions(rule):
    """
    Format rule actions for display
    
    Args:
        rule: Rule object
        
    Returns:
        Formatted actions
    """
    actions = []
    rule_actions = rule.get('actions', {})
    
    # Move to folder
    if rule_actions.get('moveToFolder'):
        actions.append(f"Move to folder: {rule_actions['moveToFolder']}")
    
    # Copy to folder
    if rule_actions.get('copyToFolder'):
        actions.append(f"Copy to folder: {rule_actions['copyToFolder']}")
    
    # Mark as read
    if rule_actions.get('markAsRead') == True:
        actions.append('Mark as read')
    
    # Mark importance
    if rule_actions.get('markImportance'):
        actions.append(f"Mark importance: {rule_actions['markImportance']}")
    
    # Forward
    forward_to = rule_actions.get('forwardTo', [])
    if forward_to:
        recipients = ', '.join([r.get('emailAddress', {}).get('address', 'unknown') for r in forward_to])
        actions.append(f"Forward to: {recipients}")
    
    # Delete
    if rule_actions.get('delete') == True:
        actions.append('Delete')
    
    return '; '.join(actions)