# Data models(Schemas) for the log interpretation and final incident report.

from pydantic import BaseModel, Field
from typing import Literal


# Result of the log analysis: summary and severity.
class InterpretedLog(BaseModel):
    summary: str = Field(description="Explanation of the error in simple English")
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(description="Severity level of the issue")

# Final incident report: summary, severity, owner, response time and steps.
class FinalIncidentReport(BaseModel):
    summary: str = Field(description="Explanation of the error in simple English")
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(description="Severity level of the issue")
    assigned_to: str = Field(description="Who should handle this: on-call engineer, support queue, or self-serve")
    response_time: str = Field(description="Expected response time based on severity")
    steps: list[str] = Field(description="List of steps to take to resolve or troubleshoot the issue")