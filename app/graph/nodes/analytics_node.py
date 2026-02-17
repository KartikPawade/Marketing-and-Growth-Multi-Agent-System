from app.graph.node_wrapper import node_logger
from app.schemas.analytics import AnalyticsReport, ChannelPerformance


@node_logger("analytics")
def analytics_node(state):
    content = state.get("content")
    channel_breakdown: list[ChannelPerformance] = []

    if isinstance(content, dict) and content.get("assets"):
        for asset in content["assets"]:
            channel = asset.get("channel", "unknown")
            # Placeholder metrics; replace with real predictions or API later
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

    report = AnalyticsReport(
        total_impressions=0,
        total_clicks=0,
        overall_ctr=0.0,
        conversion_rate=0.0,
        channel_breakdown=channel_breakdown,
    )
    state["analytics"] = report.model_dump()
    return state