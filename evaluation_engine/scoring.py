class EvaluationScoring:

    # ==========================================================
    # Business Impact Score
    # ==========================================================

    def business_impact(self, agent):

        score = 0

        if agent.automation_percentage >= 85:
            score += 35
        elif agent.automation_percentage >= 70:
            score += 25
        else:
            score += 15

        if agent.estimated_hours_saved >= 3000:
            score += 35
        elif agent.estimated_hours_saved >= 1500:
            score += 25
        else:
            score += 15

        if agent.priority == "Critical":
            score += 30
        elif agent.priority == "High":
            score += 25
        elif agent.priority == "Medium":
            score += 18
        else:
            score += 10

        return min(score, 100)

    # ==========================================================
    # Data Readiness Score
    # ==========================================================

    def data_readiness(self, agent):

        score = 40

        score += len(agent.input_types) * 10

        if agent.rag:
            score += 10

        if agent.graphrag:
            score += 10

        return min(score, 100)

    # ==========================================================
    # AI Readiness Score
    # ==========================================================

    def ai_readiness(self, agent):

        score = 0

        if agent.llm:
            score += 30

        if agent.rag:
            score += 20

        if agent.graphrag:
            score += 15

        if agent.memory:
            score += 15

        if agent.vision:
            score += 20

        return min(score, 100)

    # ==========================================================
    # Technical Complexity Score
    # ==========================================================

    def technical_complexity(self, agent):

        score = 20

        score += len(agent.skills) * 5
        score += len(agent.input_types) * 5
        score += len(agent.output_types) * 5

        if agent.memory:
            score += 10

        if agent.graphrag:
            score += 10

        return min(score, 100)

    # ==========================================================
    # Risk Score
    # ==========================================================

    def risk_score(self, agent):

        score = 20

        HIGH_RISK_DOMAINS = [
            "Healthcare",
            "Banking",
            "Finance",
            "Legal",
            "Cybersecurity",
        ]

        if agent.business_domain in HIGH_RISK_DOMAINS:
            score += 30

        if agent.priority == "Critical":
            score += 20

        if agent.graphrag:
            score += 10

        if agent.memory:
            score += 10

        if agent.status != "Active":
            score += 10

        return min(score, 100)

    # ==========================================================
    # Overall Evaluation Score
    # ==========================================================

    def overall_score(
        self,
        business,
        data,
        ai,
        complexity,
        risk,
    ):

        score = (
            business * 0.30
            + data * 0.20
            + ai * 0.20
            + complexity * 0.15
            + (100 - risk) * 0.15
        )

        return round(score, 2)