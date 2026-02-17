# app/services/llm/structured.py
"""Helpers for schema-constrained LLM output: prompt instruction + parse/validate."""
import json
import re
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def schema_instruction(schema: type[BaseModel]) -> str:
    """Ask the LLM for a JSON data object with the required keys; do not send the schema (model may echo it)."""
    js = schema.model_json_schema()
    props = js.get("properties", {})
    required = js.get("required", list(props.keys()))
    key_types = []
    for k in required:
        p = props.get(k, {})
        t = p.get("type") or (p.get("anyOf") or [{}])[0].get("type") if p.get("anyOf") else "any"
        if not t:
            t = "array" if p.get("items") else "object"
        key_types.append(f'"{k}" ({t})')
    keys_desc = ", ".join(key_types)
    return (
        "\n\nRespond with exactly one JSON object: real data (your analysis) with these keys only: "
        + keys_desc
        + ". Do NOT output the schema or a definition—only the filled-in object. "
        "No markdown, no code fence, no extra text. "
        "Numeric fields must be plain numbers only (no currency symbols, units, or prose; e.g. use 1400 for 1.4 billion, 25 for 25%). "
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
