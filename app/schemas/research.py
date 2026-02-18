# app/schemas/research.py
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Competitor(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str = Field(..., description="Name of the competitor")
    positioning: str = Field(..., description="Positioning statement of the competitor")


class ResearchOutput(BaseModel):
    model_config = ConfigDict(strict=True)

    target_audience: str = Field(
    ...,
    min_length=3,
    max_length=500,
    description="Detailed description of demographic and psychographic profile"
    )
    market_size: str = Field(..., description="Market size in USD millions")
    growth_rate: str = Field(..., description="Annual growth rate percentage")
    key_insights: list[str] = Field(..., description="Key insights identified during research")
    competitors: list[Competitor] = Field(..., description="List of major competitors")

    