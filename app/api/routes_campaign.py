# app/api/routes_campaign.py
from fastapi import APIRouter
from app.schemas.campaign import CampaignCreate
from app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.post("/")
def create_campaign(payload: CampaignCreate):
    service = CampaignService()
    return service.create_campaign(payload)