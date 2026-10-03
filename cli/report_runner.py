# Runs the incident analysis on a error log and prints the report, sending a Slack alert on HIGH/CRITICAL severity.

import json

from chains.incident_pipeline import run_incident_pipeline
from services.formatter import format_incident_report
from services.slack_notifier import send_slack_alert


DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def analyze_and_show(log: str):
    """
        Analyze the log, print the report, and send a Slack alert for CRITICAL/HIGH issues.
    """
    
    print(f"{DIM}Analyzing log...{RESET}\n")

    try:
        result = run_incident_pipeline(log)
    except Exception as e:
        print(f"{BOLD}Something went wrong while analyzing the log: {e} {RESET}")
        print(f"{BOLD}Check your API key in .env and your internet connection, then try again.{RESET}")
        return

    print(json.dumps(result, indent=2, default=str))

    report_text = format_incident_report(result)
    print(f"{BOLD}{DIM} Incident Report {RESET}\n")
    print(report_text)

    if result["severity"] in ("CRITICAL", "HIGH"):
        sent = send_slack_alert(report_text, result["severity"])
        if sent:
            print(f"{BOLD} {DIM}Slack alert sent to on-call channel.{RESET}")
        else:
            print(f"{BOLD} {DIM}Slack alert could not be sent (check webhook configuration).{RESET}")