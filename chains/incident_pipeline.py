# Single pipeline: Analyzes a system log, finds its severity, and builds the srtuctured incident report with steps to follow.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from prompts import (
    interpret_prompt,
    interpret_parser,
    high_severity_prompt,
    medium_severity_prompt,
    low_severity_prompt,
)
from schemas.pipeline_schemas import FinalIncidentReport

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
    temperature=0.5,
)

str_parser = StrOutputParser()

SEVERITY_ROUTING = {
    "CRITICAL": {"assigned_to": "On-call engineer", "response_time": "15 minutes"},
    "HIGH": {"assigned_to": "On-call engineer", "response_time": "1 hour"},
    "MEDIUM": {"assigned_to": "Support/dev queue", "response_time": "1 business day"},
    "LOW": {"assigned_to": "Self-serve / backlog", "response_time": "No SLA"},
}


def run_incident_pipeline(log: str) -> dict:
    """
        Analyze the log, find its severity, and return the incident report as a dict.
    """
    # step 1: interpret the log and classify severity
    interpreted = (interpret_prompt | model | interpret_parser).invoke({"log": log})

    severity = interpreted.severity
    summary = interpreted.summary

    # step 2: generate steps based on severity
    if severity in ("CRITICAL", "HIGH"):
        steps_text = (high_severity_prompt | model | str_parser).invoke({
            "summary": summary,
            "severity": severity,
        })
    elif severity == "MEDIUM":
        steps_text = (medium_severity_prompt | model | str_parser).invoke({"summary": summary})
    else:
        steps_text = (low_severity_prompt | model | str_parser).invoke({"summary": summary})

    steps = [line.strip() for line in steps_text.split("\n") if line.strip()]

    # step 3: build the final structured report
    routing = SEVERITY_ROUTING.get(severity, SEVERITY_ROUTING["LOW"])

    report = FinalIncidentReport(
        summary=summary,
        severity=severity,
        assigned_to=routing["assigned_to"],
        response_time=routing["response_time"],
        steps=steps,
    )

    return report.model_dump()