from typing import TypedDict, Optional, List, Dict


class CampaignState(TypedDict):
    campaign_id: str
    brand_context: Optional[str]

    research: Optional[str]
    strategy: Optional[str]
    content: Optional[str]
    qa_report: Optional[Dict]
    analytics: Optional[Dict]

    validation_errors: Optional[List[str]]
    status: Optional[str]