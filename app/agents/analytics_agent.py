# app/agents/analytics_agent.py
from app.schemas.analytics import AnalyticsReport, ChannelPerformance


class AnalyticsAgent:
    def __init__(self) -> None:
        pass

    def run(self, content: dict | None) -> AnalyticsReport:
        channel_breakdown: list[ChannelPerformance] = []

        if isinstance(content, dict) and content.get("assets"):
            for asset in content["assets"]:
                channel = asset.get("channel", "unknown")
                channel_breakdown.append(
                    ChannelPerformance(
                        channel_name=channel,
                        impressions=0,
                        clicks=0,
                        ctr=0.0,
                    )
                )

        if not channel_breakdown:
            channel_breakdown = [
                ChannelPerformance(
                    channel_name="placeholder",
                    impressions=0,
                    clicks=0,
                    ctr=0.0,
                )
            ]

        return AnalyticsReport(
            total_impressions=0,
            total_clicks=0,
            overall_ctr=0.0,
            conversion_rate=0.0,
            channel_breakdown=channel_breakdown,
        )
