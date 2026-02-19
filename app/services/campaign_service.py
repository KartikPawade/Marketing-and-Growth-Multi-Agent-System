import uuid

from app.graph.builder import build_campaign_graph
from app.services.brand_service import BrandService


class CampaignService:
    def create_campaign(self, campaign_data):
        graph = build_campaign_graph()
        brand_service = BrandService()
        brand_context = brand_service.get_by_id_or_raise(campaign_data.brand_id)

        campaign_id = str(uuid.uuid4())
        result = graph.invoke({
            "campaign_id": campaign_id,
            "brand_context": brand_context.model_dump(),
            "research": None,
            "strategy": None,
            "content": None,
            "qa_report": None,
            "analytics": None,
        })

        qa_passed = (result.get("qa_report") or {}).get("passed", False)
        status = "completed" if qa_passed else "failed"

        return {
            "id": campaign_id,
            "status": status,
            "research": result,
        }