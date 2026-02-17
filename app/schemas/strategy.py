# app/schemas/strategy.py
from pydantic import BaseModel, ConfigDict, Field


class StrategyOutput(BaseModel):
    model_config = ConfigDict(strict=True)

    summary: str = Field(..., description="Executive summary of the growth strategy, should be a single string")
    objectives: list[str] = Field(..., description="Key objectives, should be list of strings")
    tactics: list[str] = Field(..., description="Tactical recommendations, should be list of strings")
    channels: list[str] = Field(..., description="Recommended channels, should be list of strings")
