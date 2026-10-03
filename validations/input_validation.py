# Uses an LLM to check that the input is a real system error log, not random text.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from schemas.validation_schemas import LogValidationResult

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
)

parser = JsonOutputParser(pydantic_object=LogValidationResult)

template = PromptTemplate(
    template=(
        "Check if the following text is a real, meaningful system error log "
        "(not random text or gibberish):\n\n"
        "{log}\n\n"
        "{format_instruction}"
    ),
    input_variables=["log"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

validation_chain = template | model | parser


def validate_log(log: str) -> dict:
    return validation_chain.invoke({"log": log})