# Converts the final structured incident report into a plain readable text block

def format_incident_report(result: dict) -> str:
    lines = []

    lines.append(f"Severity: {result.get('severity', '')}")
    lines.append(f"Assigned To: {result.get('assigned_to', '')}")
    lines.append(f"Response Time: {result.get('response_time', '')}")
    lines.append("")
    lines.append("Summary:")
    lines.append(result.get("summary", ""))
    lines.append("")
    lines.append("Steps:")

    for i, step in enumerate(result.get("steps", []), start=1):
        lines.append(f"{i}. {step}")

    return "\n".join(lines)