from models.agent import Agent
from models.roi import ROIResult


class ROICalculator:

    # Average employee hourly cost (USD)
    HOURLY_RATE = 30

    def calculate(self, agent: Agent) -> ROIResult:
        """
        Calculate ROI metrics for a single AI agent.
        """

        # ==========================================
        # Annual Labor Savings
        # ==========================================

        annual_labor_savings = (
            agent.estimated_hours_saved * self.HOURLY_RATE
        )

        # ==========================================
        # Net Annual Benefit
        # ==========================================

        net_annual_benefit = (
            annual_labor_savings
            - agent.annual_operating_cost
        )

        # ==========================================
        # ROI Percentage
        # ==========================================

        if agent.implementation_cost > 0:
            roi_percentage = (
                (net_annual_benefit / agent.implementation_cost)
                * 100
            )
        else:
            roi_percentage = 0

        # ==========================================
        # Payback Period
        # ==========================================

        if net_annual_benefit > 0:
            payback_period_months = (
                agent.implementation_cost
                / net_annual_benefit
            ) * 12
        else:
            payback_period_months = 999

        # ==========================================
        # ROI Score
        # ==========================================

        roi_score = (
            roi_percentage * 0.6
            + agent.automation_percentage * 0.4
        )

        # ==========================================
        # Return ROI Result
        # ==========================================

        return ROIResult(

            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            business_domain=agent.business_domain,

            implementation_cost=agent.implementation_cost,
            annual_operating_cost=agent.annual_operating_cost,

            annual_labor_savings=round(
                annual_labor_savings, 2
            ),

            net_annual_benefit=round(
                net_annual_benefit, 2
            ),

            roi_percentage=round(
                roi_percentage, 2
            ),

            payback_period_months=round(
                payback_period_months, 2
            ),

            roi_score=round(
                roi_score, 2
            ),

        )