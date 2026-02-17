# app/schemas/qa.py
# app/schemas/qa.py
from pydantic import BaseModel, ConfigDict, Field


class QAReport(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    passed: bool = Field(
        ...,
        description="Indicates whether campaign passed QA checks"
    )

    issues: list[str] = Field(
        default_factory=list,
        description="List of issues identified during QA"
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Suggested improvements"
    )