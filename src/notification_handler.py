import json
import boto3
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Initialize AWS clients
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# Environment variables
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    """
    Check for upcoming departures and send notifications
    """
    table = dynamodb.Table(TABLE_NAME)
    
    # Get current date and dates to check (today, tomorrow, 1 week, 2 weeks)
    today = datetime.now().date()
    notification_windows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]  # days before departure
    
    notifications_sent = 0
    
    try:
        # Scan the table for all departure events
        response = table.scan()
        events = response.get('Items', [])
        
        for item in events:
            departure_date_str = item.get('departureDate')
            if not departure_date_str:
                continue
            
            # Parse departure date
            departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
            days_until = (departure_date - today).days
            
            # Check if we should send a notification
            if days_until in notification_windows and days_until >= 0:
                send_notification(item, days_until)
                notifications_sent += 1
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Checked {len(events)} events, sent {notifications_sent} notifications',
                'events_checked': len(events),
                'notifications_sent': notifications_sent
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

def send_notification(event_data, days_until):
    """
    Send SNS notification for a departure event
    """
    country = event_data.get('country', 'Unknown')
    departure_date = event_data.get('departureDate', 'Unknown')
    return_date = event_data.get('returnDate', 'Not specified')
    purpose = event_data.get('purpose', 'Travel')
    notes = event_data.get('notes', '')
    
    # Create message based on days until departure
    if days_until == 0:
        subject = f"🛫 TODAY: Departure to {country}"
        urgency = "Your departure is TODAY!"
    elif days_until == 1:
        subject = f"🛫 TOMORROW: Departure to {country}"
        urgency = "Your departure is TOMORROW!"
    elif days_until == 7:
        subject = f"📅 1 Week Reminder: Departure to {country}"
        urgency = "Your departure is in 1 week."
    elif days_until == 14:
        subject = f"📅 2 Week Reminder: Departure to {country}"
        urgency = "Your departure is in 2 weeks."
    elif days_until == 21:
        subject = f"📅 21 Week Reminder: Departure to {country}"
        urgency = "Your departure is in 3 weeks."
    elif days_until == 30:
        subject = f"📅 1 Month Reminder: Departure to {country}"
        urgency = "Your departure is in 1 month."
    else:
        subject = f"📅 Departure Reminder: {country}"
        urgency = f"Your departure is in {days_until} days."
    
    message = f"""
{urgency}

DEPARTURE DETAILS:
==================
Destination: {country}
Departure Date: {departure_date}
{f'Return Date: {return_date}' if return_date and return_date != 'Not specified' else ''}
Purpose: {purpose}

{f'Notes: {notes}' if notes else ''}

Days until departure: {days_until}

---
This is an automated reminder from your Departure Notification System.
    """.strip()
    
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        print(f"Notification sent for {country} departure (MessageId: {response['MessageId']})")
        return response
    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
        raise