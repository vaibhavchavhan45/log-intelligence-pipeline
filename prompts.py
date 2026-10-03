# Prompt templates that tells LLM how to analyze a log and what steps to suggest for each severity.

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.pipeline_schemas import InterpretedLog

interpret_parser = PydanticOutputParser(pydantic_object=InterpretedLog)

interpret_prompt = PromptTemplate(
    template=(
        "Analyze the system log below.\n"
        "1. Explain what happened in simple English\n"
        "2. Classify severity as one of: LOW, MEDIUM, HIGH, CRITICAL\n\n"
        "{format_instruction}\n"
        "System log:\n{log}"
    ),
    input_variables=["log"],
    partial_variables={"format_instruction": interpret_parser.get_format_instructions()},
)

high_severity_prompt = PromptTemplate(
    template=(
        "The following issue is {severity}.\n"
        "Provide clear incident response steps for an on-call engineer, as a numbered list.\n\n"
        "Summary:\n{summary}"
    ),
    input_variables=["summary", "severity"],
)

medium_severity_prompt = PromptTemplate(
    template=(
        "The following issue is MEDIUM severity.\n"
        "Provide steps for the support/dev team to resolve this during regular hours, as a numbered list.\n\n"
        "Summary:\n{summary}"
    ),
    input_variables=["summary"],
)

low_severity_prompt = PromptTemplate(
    template=(
        "The following issue is LOW severity.\n"
        "Provide basic self-serve troubleshooting steps, as a numbered list.\n\n"
        "Summary:\n{summary}"
    ),
    input_variables=["summary"],
)