import random

from models.agent import Agent

from config.domains import DOMAINS
from config.skills import SKILLS
from config.inputs import INPUT_TYPES
from config.outputs import OUTPUT_TYPES
from config.owners import BUSINESS_OWNERS
from config.constants import (
    PRIORITIES,
    MATURITY_LEVELS,
    VERSIONS,
    STATUS,
)


class AgentGenerator:

    def __init__(self):
        self.agents = []

    def _create_agent(self, domain, agent_name):

        agent = Agent(
            # Basic Information
            agent_id="",
            agent_name=agent_name,
            business_domain=domain,
            business_owner=random.choice(BUSINESS_OWNERS),
    
            priority=random.choice(PRIORITIES),
            maturity=random.choice(MATURITY_LEVELS),
            version=random.choice(VERSIONS),
            status=random.choice(STATUS),
    
            # Business Information
            problem_statement="",
            business_goal="",
            current_manual_process="",
            expected_ai_workflow="",
    
            # AI Capabilities
            llm=False,
            vision=False,
            rag=False,
            graphrag=False,
            memory=False,
    
            # Skills
            skills=[],
    
            # Input / Output
            input_types=[],
            output_types=[],
    
            # Cost Metadata
            implementation_cost=0,
            annual_operating_cost=0,
            estimated_hours_saved=0,
            automation_percentage=0,
        )

        return agent
    def generate(self):
        pass