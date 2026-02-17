from app.graph.builder import build_campaign_graph

class CampaignService:

    def create_campaign(self, campaign_data):
        graph = build_campaign_graph()

        result = graph.invoke({
            "brand_context": None,
            "research": None,
            "strategy": None,
            "content": None,
            "qa_report": None,
            "analytics": None
        })

        return {
            "id": "cmp_123",
            "status": "completed",
            "research": result["research"]
        }