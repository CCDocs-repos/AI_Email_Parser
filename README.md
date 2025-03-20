# Email Forwarding Automation to Slack

This repository contains a Python script that automates the process of forwarding specific emails from an inbox to a Slack channel using **Slack Incoming Webhooks**. The script checks for unread emails from a specified sender, extracts the email content, and forwards it to a Slack channel in real-time.

## Features

- Monitors your email inbox for unread emails from a specific sender.
- Forwards those emails to a Slack channel using Slack's Incoming Webhooks.
- Can be run continuously in the background, checking for new emails in real-time.
- Easy to configure and run.

## Prerequisites

To use this system, you'll need:
1. **Python 3.x** installed on your system.
2. **Slack Webhook URL** from your Slack workspace.
3. **Google account with IMAP enabled** (or any other email provider that supports IMAP).
4. **App password for Gmail** (if you're using Gmail with Two-Factor Authentication).

## Setup Instructions

Follow the steps below to set up the email forwarding system:

### 1. Set Up Slack Webhook
1. Go to your **Slack workspace**.
2. Click on **Apps** in the sidebar, then search for **Incoming Webhooks** and add it.
3. Choose the **Slack channel** where you want to forward the emails (e.g., `#general`).
4. **Copy the Webhook URL** provided, which will be used in the script.

### 2. Install Python Libraries

Open your terminal or command prompt and run the following commands to install the necessary dependencies:

```bash
pip install requests imaplib email
