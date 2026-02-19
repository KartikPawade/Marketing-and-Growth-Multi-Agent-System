# app/schemas/qa.py
from pydantic import BaseModel, ConfigDict, Field


class QAReport(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    passed: bool = Field(
        ...,
        description=(
            "True only if there are zero critical issues across all assets. "
            "A single asset failing any quality dimension is sufficient to fail the entire report. "
            "Do not pass a campaign that has generic copy, missing brand identity, or misaligned CTAs."
        ),
    )
    issues: list[str] = Field(
        default_factory=list,
        description=(
            "Specific issues found during review. Each entry must identify: which asset (by channel), "
            "what the problem is, and why it matters in practice. "
            "Example: 'TikTok asset — brand name absent; a viewer would not know whose product this is.' "
            "Vague entries like 'copy could be improved' are not acceptable."
        ),
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description=(
            "Concrete, actionable fixes for each issue raised. Each recommendation should be specific "
            "enough that a copywriter could act on it immediately without further clarification. "
            "Example: 'Add brand name to TikTok headline and reference the 24-hour adaptive plan USP "
            "in the first sentence of body copy.'"
        ),
    )