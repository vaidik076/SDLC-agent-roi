from pydantic import BaseModel
from typing import List


class Agent(BaseModel):
    agent_id: str
    agent_name: str
    business_domain: str
    business_owner: str

    priority: str
    maturity: str
    version: str
    status: str

    problem_statement: str
    business_goal: str
    current_manual_process: str
    expected_ai_workflow: str

    llm: bool
    vision: bool
    rag: bool
    graphrag: bool
    memory: bool

    skills: List[str]

    input_types: List[str]
    output_types: List[str]

    implementation_cost: float
    annual_operating_cost: float
    estimated_hours_saved: int
    automation_percentage: int