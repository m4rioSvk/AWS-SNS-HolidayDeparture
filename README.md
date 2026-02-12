# 🌍 Departure Notification System

An AWS serverless application that sends automated email notifications for upcoming country departures. Never miss a travel date again!

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20SNS%20%7C%20DynamoDB-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 About

This project was created for personal use to ensure I never forget about my upcoming travels. It automatically sends email reminders at timely intervals before each departure date.

## ✨ Features

- 📧 **Email notifications** via AWS SNS
- 📅 **Automatic reminders** at:
  - 30 days before departure
  - 14 days before (2 weeks)
  - 7 days before (1 week)
  - 1 day before (tomorrow)
  - Day of departure (today)
- 🗄️ **Store multiple departure events** in DynamoDB
- ⏰ **Daily scheduled checks** using EventBridge
- 🔧 **Easy event management** (add, update, delete, list)
- 💰 **Cost-effective** - runs on AWS Free Tier

## 🏗️ Architecture
```
┌─────────────────┐
│  EventBridge    │  Triggers daily at scheduled time
│   (Schedule)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Lambda      │  Checks DynamoDB for upcoming departures
│ (Notification)  │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│    DynamoDB     │  │    SNS Topic    │
│ (Events Store)  │  │   (Email Send)  │
└─────────────────┘  └─────────────────┘
         ▲
         │
┌─────────────────┐
│     Lambda      │  Manages events (CRUD operations)
│ (Event Manager) │
└─────────────────┘
```

**Components:**
- **SNS Topic**: Sends email notifications to subscribed addresses
- **DynamoDB Table**: Stores departure events with dates and details
- **Lambda Functions**:
  - `NotificationChecker`: Runs daily to check for upcoming departures
  - `ManageEvents`: Add/update/delete departure events
- **EventBridge Rule**: Triggers daily notification checks

## 🚀 Prerequisites

- AWS CLI configured with credentials
- AWS SAM CLI installed ([Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
- Python 3.11+
- Active AWS account

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

## ⭐ Acknowledgments

Built with AWS SAM, Python

---

