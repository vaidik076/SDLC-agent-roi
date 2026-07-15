import random

from models.agent import Agent

from config.domains import DOMAINS
from config.skills import SKILLS
from config.inputs import INPUT_TYPES
from config.outputs import OUTPUT_TYPES

from config.constants import (
    PRIORITIES,
    MATURITY_LEVELS,
    VERSIONS,
    STATUS,
)

from config.domain_profiles import DOMAIN_PROFILES

from config.agent_complexity import (
    COMPLEXITY_PROFILES,
    DOMAIN_COMPLEXITY,
    AGENT_COMPLEXITY_OVERRIDE,
)

# ==========================================================
# Domain Prefix Mapping
# ==========================================================

DOMAIN_PREFIX = {
    "Finance": "FIN",
    "Human Resources": "HR",
    "Sales": "SAL",
    "Marketing": "MKT",
    "IT": "IT",
    "Legal": "LEG",
    "Healthcare": "HLT",
    "Manufacturing": "MFG",
    "Supply Chain": "SCM",
    "Customer Support": "CSP",
    "Procurement": "PRC",
    "Banking": "BNK",
    "Insurance": "INS",
    "Retail": "RTL",
    "Education": "EDU",
    "Cybersecurity": "CYB",
    "Telecommunications": "TEL",
    "Energy": "ENG",
    "Data & Analytics": "DAT",
    "Operations": "OPS",
}


class AgentGenerator:

    def __init__(self):
        self.agents = []

    def _create_agent(self, domain, agent_name, index):

        # ==================================================
        # Domain Profile
        # ==================================================

        domain_profile = DOMAIN_PROFILES.get(domain, {})

        skills = domain_profile.get("skills", SKILLS)
        inputs = domain_profile.get("inputs", INPUT_TYPES)
        outputs = domain_profile.get("outputs", OUTPUT_TYPES)

        # ==================================================
        # Complexity Selection
        # ==================================================

        complexity = AGENT_COMPLEXITY_OVERRIDE.get(
            agent_name,
            DOMAIN_COMPLEXITY.get(domain, "MEDIUM"),
        )

        complexity_profile = COMPLEXITY_PROFILES[complexity]

        implementation_cost = random.randint(
            *complexity_profile["implementation_cost"]
        )

        annual_operating_cost = random.randint(
            *complexity_profile["annual_operating_cost"]
        )

        estimated_hours_saved = random.randint(
            *complexity_profile["estimated_hours_saved"]
        )

        automation_percentage = random.randint(
            *complexity_profile["automation_percentage"]
        )

        # ==================================================
        # Create Agent
        # ==================================================

        agent = Agent(

            # -----------------------------
            # Basic Information
            # -----------------------------

            agent_id=f"{DOMAIN_PREFIX.get(domain, 'GEN')}-{index:03d}",
            agent_name=agent_name,
            business_domain=domain,
            business_owner=domain_profile.get(
                "owner",
                "Business Manager"
            ),

            priority=random.choice(PRIORITIES),
            maturity=random.choice(MATURITY_LEVELS),
            version=random.choice(VERSIONS),
            status=random.choice(STATUS),

            # -----------------------------
            # Business Information
            # -----------------------------

            problem_statement=(
                f"Manual process for {agent_name.lower()} "
                f"is slow, repetitive, and prone to human errors."
            ),

            business_goal=(
                f"Automate and optimize {agent_name.lower()} "
                f"using enterprise AI."
            ),

            current_manual_process=(
                f"Employees manually perform {agent_name.lower()} "
                f"using spreadsheets, emails, and business applications."
            ),

            expected_ai_workflow=(
                f"AI receives inputs, processes requests, "
                f"applies business rules, and produces "
                f"automated outputs for {agent_name.lower()}."
            ),

            # -----------------------------
            # AI Capabilities
            # -----------------------------

            llm=random.choice([True, True, True, False]),
            vision=random.choice([True, False]),
            rag=random.choice([True, False]),
            graphrag=random.choice([True, False]),
            memory=random.choice([True, False]),

            # -----------------------------
            # Skills
            # -----------------------------

            skills=random.sample(
                skills,
                min(
                    len(skills),
                    random.randint(4, 6)
                ),
            ),

            # -----------------------------
            # Inputs
            # -----------------------------

            input_types=random.sample(
                inputs,
                min(
                    len(inputs),
                    random.randint(2, 3)
                ),
            ),

            # -----------------------------
            # Outputs
            # -----------------------------

            output_types=random.sample(
                outputs,
                min(
                    len(outputs),
                    random.randint(2, 3)
                ),
            ),

            # -----------------------------
            # Cost Metadata
            # -----------------------------

            implementation_cost=implementation_cost,
            annual_operating_cost=annual_operating_cost,
            estimated_hours_saved=estimated_hours_saved,
            automation_percentage=automation_percentage,

        )

        return agent

    def generate(self):

        self.agents = []

        for domain, agent_names in DOMAINS.items():

            for index, agent_name in enumerate(agent_names, start=1):

                agent = self._create_agent(
                    domain=domain,
                    agent_name=agent_name,
                    index=index,
                )

                self.agents.append(agent)

        return self.agents