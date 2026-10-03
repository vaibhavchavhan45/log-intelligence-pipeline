# API endpoint that analyzes a system log and returns the incident report as plain text.

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from schemas.request_schemas import LogRequest
from chains.incident_pipeline import run_incident_pipeline
from services.formatter import format_incident_report
from services.slack_notifier import send_slack_alert
from validations.input_validation import validate_log

router = APIRouter()


@router.post("/analyze-log/report-text", response_class=PlainTextResponse, summary="Analyze Log Plain Text")
def analyze_log_plain_text(request: LogRequest):
    validation = validate_log(request.log)

    if not validation["log_valid"]:
        raise HTTPException(status_code=400, detail=validation["log_reason"])

    try:
        result = run_incident_pipeline(request.log)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log analysis failed: {e}")

    report_text = format_incident_report(result)

    if result["severity"] in ("CRITICAL", "HIGH"):
        send_slack_alert(report_text, result["severity"])

    return report_text