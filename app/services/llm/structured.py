# app/services/llm/structured.py
"""Helpers for schema-constrained LLM output: prompt instruction + parse/validate."""
import json
import re
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def schema_instruction(schema: type[BaseModel]) -> str:
    """Return system-prompt text asking the LLM to respond with JSON matching the schema."""
    return (
        "\n\nRespond with a single JSON object only (no markdown, no code fence, no explanation). "
        "The JSON must match this schema: "
        + json.dumps(schema.model_json_schema())
    )


def parse_structured_response(raw: str, schema: type[T]) -> T:
    """Extract JSON from raw LLM content (strip markdown if present) and validate with schema."""
    text = raw.strip()
    # Remove optional markdown code block
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()
    return schema.model_validate_json(text)
