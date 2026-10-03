# Log Intelligence Pipeline

## Problem
Raw system error logs are hard to read and don't clearly indicate what action is required or how urgent the issue is. This project reads a raw system error, explains it in plain English, determines how serious it is, and routes it to the right next step i.e. incident response, a support queue, or basic self-serve troubleshooting.


## What It Does
Given a raw system log, the pipeline produces:
1. **Summary** — the error explained in plain English.
2. **Severity** — classified as LOW, MEDIUM, HIGH, or CRITICAL.
3. **Assigned To** — who should handle it (on-call engineer, support/dev queue, or self-serve).
4. **Response Time** — expected SLA based on severity.
5. **Steps** — a list of steps to take, tailored to the severity level.

For CRITICAL and HIGH severity issues, an alert is automatically sent to a Slack channel so an on-call engineer is notified immediately. The alert only notifies, it does not resolve anything or take any action on its own. A human reviews the steps and decides what to do.


## Model
Uses `openai/gpt-oss-120b`, accessed via Groq's OpenAI-compatible API (through `langchain-openai`'s `ChatOpenAI` class).


## Input Validation
Before running the pipeline, the log text is checked using a separate LLM call to confirm it's actually a meaningful system error log, not random or gibberish text. If invalid, the request is rejected with a reason.


## Severity Routing
| Severity | Assigned To          | Response Time      |
|----------|----------------------|--------------------|
| CRITICAL | On-call engineer     | 15 minutes         |
| HIGH     | On-call engineer     | 1 hour             |
| MEDIUM   | Support/dev queue    | 1 business day     |
| LOW      | Self-serve / backlog | No SLA             |

## Two Ways to Run
- **CLI** (`main.py`) — asks for a log in the terminal, validates it, runs the pipeline, prints the structured report and readable version, and sends a Slack alert if severity is CRITICAL/HIGH.
- **API** (`app.py`) — a FastAPI backend with two endpoints. Comes with an interactive `/docs` page (Swagger UI) to test both endpoints directly in the browser.

## API Endpoints
- **POST `/analyze-log`** — Returns the full result as JSON: `structured_data` and `incident_report` (plain text, shown as a JSON string).
- **POST `/analyze-log/report-text`** — Returns only the incident report as true plain text.

Both endpoints accept the same request body: `{"log": "<raw error text>"}`.


## Slack Alerts
For CRITICAL or HIGH severity, the system sends the incident report to a Slack channel through an Incoming Webhook. This requires a `SLACK_WEBHOOK_URL` set in `.env`. If it's not configured, the pipeline still runs normally, it just skips sending the alert.


## Concepts Used
- LLM-based log interpretation and classification
- Structured output parsing (Pydantic)
- Severity-based routing logic
- LLM-based input validation
- Real-time alerting via Slack webhook integration
- REST API design (FastAPI)
- Centralized error handling


## Project Structure
log_intelligence_pipeline/
├── api/
│ ├── incident_json_routes.py - JSON response endpoint
│ └── incident_text_routes.py - plain text response endpoint
├── chains/
│ └── incident_pipeline.py - main pipeline logic
├── cli/
│ ├── log_input.py - asks for the log and checks it is valid
│ └── report_runner.py - runs the analysis, prints the report, sends the Slack alert
├── schemas/
│ ├── pipeline_schemas.py - InterpretedLog, FinalIncidentReport models
│ ├── request_schemas.py - API request/response models
│ └── validation_schemas.py - LogValidationResult model
├── validations/
│ └── input_validation.py - LLM-based check for meaningful log input
├── services/
│ ├── formatter.py - JSON - readable incident report text
│ └── slack_notifier.py - sends alert to Slack webhook
├── middleware/
│ └── error_handler.py - centralized API error handling
├── prompts.py - prompt templates + parsers
├── main.py - CLI entry point
├── app.py - FastAPI entry point
├── requirements.txt
├── .env.example
└── .gitignore


## Setup

1. Move into the project folder:
cd log_intelligence_pipeline


2. Create a virtual environment:
python3 -m venv venv


3. Activate it:
- macOS/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

4. Install dependencies:
pip install -r requirements.txt

5. Copy `.env.example` to `.env` and add:
GROQ_API_KEY=your_api_key_here
SLACK_WEBHOOK_URL=your_slack_webhook_url_here


## Run (CLI)
python main.py


## Run (API)
**Locally:**
uvicorn app:app --reload

Then open `http://127.0.0.1:8000/docs` to test both endpoints interactively.

**Live (deployed):**
Open `<live-url>/docs` to test both endpoints interactively — no local setup needed.

## Sample Request (API)
```json
{
  "log": "FATAL: Kubernetes pod payment-service crashed with OOMKilled status. Restart loop detected."
}
```
Hitting the base URL (`/`) returns a JSON message with a direct link to `/docs`.


## Sample Response
- `/analyze-log` — returns `structured_data` (summary, severity, assigned_to, response_time, steps) and `incident_report` (readable text version).
- `/analyze-log/report-text` — returns only the readable incident report as plain text.

If severity is CRITICAL or HIGH, an alert is also sent to the configured Slack channel.


## Future Improvements
- Persistent error history (e.g. with Pinecone) if this were used in a real, ongoing system with actual incident history to learn from.
- Batch log processing (analyze multiple logs in one request).
- Rule-based severity overrides, applied after the LLM call. A few of the most common errors are checked in the log text, and if one is found, the severity is raised to at least the level below. Rules only raise the severity, never lower it. Everything else is left to the LLM.
  - `OOMKilled`, `out of memory` → CRITICAL
  - `ECONNREFUSED`, `connection refused` → CRITICAL
  - `no space left on device`, `disk full` → HIGH
  - `segmentation fault`, `stack overflow` → HIGH
  - `timeout`, `timed out` → MEDIUM