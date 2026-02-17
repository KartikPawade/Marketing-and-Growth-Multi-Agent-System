# app/schemas/content.py
from pydantic import BaseModel, ConfigDict, Field


class ContentAsset(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    headline: str = Field(
        ...,
        description="Primary headline"
    )

    body: str = Field(
        ...,
        description="Main body copy"
    )

    call_to_action: str = Field(
        ...,
        description="Call-to-action statement"
    )

    channel: str = Field(
        ...,
        description="Publishing channel"
    )


class ContentOutput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    assets: list[ContentAsset] = Field(
        ...,
        description="Generated content assets"
    )