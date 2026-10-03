# Sends an incident report to Slack channel for CRITICAL/HIGH issues to notify a human.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(report_text: str, severity: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        return False

    message = {
        "text": f"{severity} incident detected:\n\n{report_text}"
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False