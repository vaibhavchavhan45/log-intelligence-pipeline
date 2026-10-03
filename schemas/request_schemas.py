# Request and response models for the API.

from pydantic import BaseModel, Field

# Input for API req : the raw system log.
class LogRequest(BaseModel):
    log: str = Field(..., min_length=5, description="Raw system error log")


# Output for API resp : structured data and the plain text incident report.
class IncidentResponse(BaseModel):
    structured_data: dict
    incident_report: str