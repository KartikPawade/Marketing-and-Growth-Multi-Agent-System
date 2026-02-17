from app.graph.builder import build_campaign_graph
from app.services.brand_service import BrandService
class CampaignService:

    def create_campaign(self, campaign_data):
        graph = build_campaign_graph()
        brand_service = BrandService()
        brand_context = brand_service.get_by_id(campaign_data.brand_id)
        result = graph.invoke({
            "brand_context": brand_context.model_dump(),
            "research": None,
            "strategy": None,
            "content": None,
            "qa_report": None,
            "analytics": None
        })

        return {
            "id": "cmp_123",
            "status": "completed",
            "research": result
        }