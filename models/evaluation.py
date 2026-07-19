from pydantic import BaseModel


class Evaluation(BaseModel):

    # ==========================================================
    # Agent Information
    # ==========================================================

    agent_id: str
    agent_name: str
    business_domain: str

    # ==========================================================
    # Evaluation Scores (0-100)
    # ==========================================================

    business_impact_score: float
    data_readiness_score: float
    ai_readiness_score: float
    technical_complexity_score: float
    risk_score: float

    # ==========================================================
    # Overall Evaluation
    # ==========================================================

    overall_score: float
    readiness_level: str
    recommendation: str