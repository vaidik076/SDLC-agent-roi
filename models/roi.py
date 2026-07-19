from pydantic import BaseModel


class ROIResult(BaseModel):

    # Agent Information
    agent_id: str
    agent_name: str
    business_domain: str

    # Cost Details
    implementation_cost: float
    annual_operating_cost: float

    # Benefit Details
    annual_labor_savings: float
    net_annual_benefit: float

    # ROI Metrics
    roi_percentage: float
    payback_period_months: float

    # Additional Metrics
    roi_score: float
    ranking: int = 0