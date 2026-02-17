# app/schemas/analytics.py
# app/schemas/analytics.py
from pydantic import BaseModel, ConfigDict, Field


class ChannelPerformance(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    channel_name: str = Field(
        ...,
        description="Name of the marketing channel"
    )

    impressions: int = Field(
        ...,
        ge=0,
        description="Total impressions generated on this channel"
    )

    clicks: int = Field(
        ...,
        ge=0,
        description="Total clicks generated on this channel"
    )

    ctr: float = Field(
        ...,
        ge=0,
        le=100,
        description="Click-through rate percentage"
    )


class AnalyticsReport(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    total_impressions: int = Field(..., ge=0)
    total_clicks: int = Field(..., ge=0)
    overall_ctr: float = Field(..., ge=0, le=100)
    conversion_rate: float = Field(..., ge=0, le=100)

    channel_breakdown: list[ChannelPerformance] = Field(
        ...,
        description="Performance metrics per marketing channel"
    )