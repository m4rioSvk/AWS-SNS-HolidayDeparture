import json
import boto3
import os
import uuid
from datetime import datetime

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

# Environment variables
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    """
    Manage departure events (add, update, delete, list)
    """
    table = dynamodb.Table(TABLE_NAME)
    
    # Parse the incoming event
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event
    except:
        body = event
    
    action = body.get('action', 'list')
    
    try:
        if action == 'add':
            return add_event(table, body)
        elif action == 'update':
            return update_event(table, body)
        elif action == 'delete':
            return delete_event(table, body)
        elif action == 'list':
            return list_events(table)
        elif action == 'get':
            return get_event(table, body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Unknown action: {action}',
                    'valid_actions': ['add', 'update', 'delete', 'list', 'get']
                })
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def add_event(table, data):
    """
    Add a new departure event
    """
    event_id = str(uuid.uuid4())
    
    # Validate required fields
    required_fields = ['country', 'departureDate']
    for field in required_fields:
        if field not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Missing required field: {field}'
                })
            }
    
    # Validate date format
    try:
        datetime.strptime(data['departureDate'], '%Y-%m-%d')
        if data.get('returnDate'):
            datetime.strptime(data['returnDate'], '%Y-%m-%d')
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            })
        }
    
    item = {
        'eventId': event_id,
        'country': data['country'],
        'departureDate': data['departureDate'],
        'returnDate': data.get('returnDate', ''),
        'purpose': data.get('purpose', 'Travel'),
        'notes': data.get('notes', ''),
        'createdAt': datetime.now().isoformat()
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Event added successfully',
            'eventId': event_id,
            'event': item
        })
    }

def update_event(table, data):
    """
    Update an existing departure event
    """
    event_id = data.get('eventId')
    if not event_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'eventId is required for update'
            })
        }
    
    # Build update expression
    update_fields = {}
    expression_parts = []
    expression_values = {}
    expression_names = {}
    
    updatable_fields = ['country', 'departureDate', 'returnDate', 'purpose', 'notes']
    
    for field in updatable_fields:
        if field in data:
            field_key = f"#{field}"
            value_key = f":{field}"
            expression_parts.append(f"{field_key} = {value_key}")
            expression_values[value_key] = data[field]
            expression_names[field_key] = field
    
    if not expression_parts:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'No fields to update'
            })
        }
    
    update_expression = "SET " + ", ".join(expression_parts)
    
    response = table.update_item(
        Key={'eventId': event_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Event updated successfully',
            'event': response['Attributes']
        })
    }

def delete_event(table, data):
    """
    Delete a departure event
    """
    event_id = data.get('eventId')
    if not event_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'eventId is required for delete'
            })
        }
    
    table.delete_item(Key={'eventId': event_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Event deleted successfully',
            'eventId': event_id
        })
    }

def list_events(table):
    """
    List all departure events
    """
    response = table.scan()
    items = response.get('Items', [])
    
    # Sort by departure date
    items.sort(key=lambda x: x.get('departureDate', ''))
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'events': items,
            'count': len(items)
        })
    }

def get_event(table, data):
    """
    Get a specific departure event
    """
    event_id = data.get('eventId')
    if not event_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'eventId is required'
            })
        }
    
    response = table.get_item(Key={'eventId': event_id})
    item = response.get('Item')
    
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'error': 'Event not found'
            })
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'event': item
        })
    }