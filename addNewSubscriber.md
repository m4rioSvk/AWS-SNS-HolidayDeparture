# Option A
## Edit template.yaml

DepartureNotificationTopic:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: DepartureNotifications
    DisplayName: Country Departure Reminders
    Subscription:
      - Endpoint: !Ref EmailAddress
        Protocol: email
      - Endpoint: second-email@example.com  # Add this line
        Protocol: email

# Option B
## Method B: Subscribe manually via AWS CLI

```sh
aws sns subscribe \
--topic-arn arn:aws:sns:REGION:ACCOUNT-ID:DepartureNotifications \  #arn:aws:sns:ap-northeast-3:794038257497:DepartureNotifications
--protocol email \
--notification-endpoint second-email@example.com
```

## Get TOPIC ARN 
```sh
aws sns list-topics
```

aws sns subscribe \
--topic-arn arn:aws:sns:ap-northeast-3:794038257497:DepartureNotifications \
--protocol email \
--notification-endpoint XXX