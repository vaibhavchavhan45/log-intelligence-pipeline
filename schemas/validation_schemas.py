from pydantic import BaseModel, Field   


# Stores the log check result. (whether the log is valid or Not?)
class LogValidationResult(BaseModel):
    log_valid: bool = Field(description="True if this looks like a real system error log")
    log_reason: str = Field(description="Short reason if invalid, empty string if valid")