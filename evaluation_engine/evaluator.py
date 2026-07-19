from models.evaluation import Evaluation

from evaluation_engine.scoring import EvaluationScoring
from evaluation_engine.readiness import ReadinessEngine
from evaluation_engine.recommendation import RecommendationEngine


class EvaluationEngine:

    def __init__(self):

        self.scoring = EvaluationScoring()
        self.readiness = ReadinessEngine()
        self.recommendation = RecommendationEngine()

    # ==========================================================
    # Evaluate Single Agent
    # ==========================================================

    def evaluate(self, agent):

        # ------------------------------------------
        # Individual Scores
        # ------------------------------------------

        business_score = self.scoring.business_impact(agent)

        data_score = self.scoring.data_readiness(agent)

        ai_score = self.scoring.ai_readiness(agent)

        complexity_score = self.scoring.technical_complexity(agent)

        risk_score = self.scoring.risk_score(agent)

        # ------------------------------------------
        # Overall Score
        # ------------------------------------------

        overall_score = self.scoring.overall_score(
            business=business_score,
            data=data_score,
            ai=ai_score,
            complexity=complexity_score,
            risk=risk_score,
        )

        # ------------------------------------------
        # Readiness
        # ------------------------------------------

        readiness_level = self.readiness.evaluate(
            overall_score
        )

        # ------------------------------------------
        # Recommendation
        # ------------------------------------------

        recommendation = self.recommendation.generate(
            overall_score
        )

        # ------------------------------------------
        # Return Evaluation Object
        # ------------------------------------------

        return Evaluation(

            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            business_domain=agent.business_domain,

            business_impact_score=business_score,
            data_readiness_score=data_score,
            ai_readiness_score=ai_score,
            technical_complexity_score=complexity_score,
            risk_score=risk_score,

            overall_score=overall_score,

            readiness_level=readiness_level,

            recommendation=recommendation,
        )

    # ==========================================================
    # Evaluate All Agents
    # ==========================================================

    def evaluate_all(self, agents):

        evaluations = []

        for agent in agents:

            evaluation = self.evaluate(agent)

            evaluations.append(evaluation)

        return evaluations