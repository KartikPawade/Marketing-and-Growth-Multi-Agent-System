# app/schemas/strategy.py
from pydantic import BaseModel, ConfigDict, Field


class StrategyOutput(BaseModel):
    model_config = ConfigDict(strict=True)

    summary: str = Field(..., description="Executive summary of the growth strategy")
    objectives: list[str] = Field(..., description="Key objectives")
    tactics: list[str] = Field(..., description="Tactical recommendations")
    channels: list[str] = Field(..., description="Recommended channels")
