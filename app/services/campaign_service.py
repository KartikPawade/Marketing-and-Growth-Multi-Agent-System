import uuid

from app.db.repositories.campaign_repo import (
    create as campaign_repo_create,
    delete as campaign_repo_delete,
    get_by_id as campaign_repo_get_by_id,
    list_all as campaign_repo_list_all,
)
from app.graph.builder import build_campaign_graph
from app.services.brand_service import BrandService


class CampaignService:
    def create_campaign(self, campaign_data):
        graph = build_campaign_graph()
        brand_service = BrandService()
        brand_context = brand_service.get_by_id(campaign_data.brand_id)

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

        payload = {
            "campaign_id": campaign_id,
            "brand_id": campaign_data.brand_id,
            "status": status,
            "goal": campaign_data.goal,
            "target_audience": campaign_data.target_audience,
            "budget": campaign_data.budget,
            "brand_context": brand_context.model_dump(),
            "research": result.get("research"),
            "strategy": result.get("strategy"),
            "content": result.get("content"),
            "qa_report": result.get("qa_report"),
            "analytics": result.get("analytics"),
        }
        campaign_repo_create(payload)

        return {
            "id": campaign_id,
            "status": status,
            "research": result,
        }

    def get_all_campaigns(self, brand_id: str | None = None):
        """Return all campaigns, optionally filtered by brand_id."""
        return campaign_repo_list_all(brand_id=brand_id)

    def get_campaign_by_id(self,brand_id: str, campaign_id: str):
        """Return one campaign by id, or None if not found."""
        return campaign_repo_get_by_id(brand_id=brand_id, campaign_id=campaign_id)

    def delete_campaign_by_id(self, campaign_id: str) -> bool:
        """Delete campaign by id. Returns True if deleted."""
        return campaign_repo_delete(campaign_id)