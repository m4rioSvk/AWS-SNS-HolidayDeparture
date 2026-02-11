## Change Notification Times
Edit the NotificationSchedule parameter in samconfig.toml:

```sh
# Daily at 8 AM UTC
"NotificationSchedule=cron(0 8 * * ? *)"

# Daily at 6 PM UTC
"NotificationSchedule=cron(0 18 * * ? *)"

# Twice daily at 9 AM and 6 PM UTC
# (You'll need to create two EventBridge rules for this)
```

## Modify Notification Windows
Edit notification_handler.py line 18:

```sh
# Current: 0, 1, 7, 14, 30 days before
notification_windows = [0, 1, 7, 14, 30]

# Example: Add 3-day reminder
notification_windows = [0, 1, 3, 7, 14, 30]
```

## Change AWS Region

Change AWS Region
Edit samconfig.toml:

```sh
region = "eu-west-1"  # Or your preferred region
```

## After every change run sam build and then sam deploy