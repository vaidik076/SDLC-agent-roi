from collections import defaultdict
from models.roi import ROIResult


class PortfolioAnalytics:

    def generate_summary(self, roi_results: list[ROIResult]):

        total_agents = len(roi_results)

        total_implementation_cost = sum(
            agent.implementation_cost
            for agent in roi_results
        )

        total_operating_cost = sum(
            agent.annual_operating_cost
            for agent in roi_results
        )

        total_annual_savings = sum(
            agent.annual_labor_savings
            for agent in roi_results
        )

        total_net_benefit = sum(
            agent.net_annual_benefit
            for agent in roi_results
        )

        average_roi = (
            sum(agent.roi_percentage for agent in roi_results)
            / total_agents
        )

        average_payback = (
            sum(agent.payback_period_months for agent in roi_results)
            / total_agents
        )

        highest_roi = max(
            roi_results,
            key=lambda x: x.roi_percentage
        )

        lowest_roi = min(
            roi_results,
            key=lambda x: x.roi_percentage
        )

        # -----------------------------
        # Domain Analytics
        # -----------------------------

        domain_scores = defaultdict(list)

        for agent in roi_results:
            domain_scores[agent.business_domain].append(
                agent.roi_percentage
            )

        average_domain_roi = {}

        for domain, scores in domain_scores.items():

            average_domain_roi[domain] = (
                sum(scores) / len(scores)
            )

        best_domain = max(
            average_domain_roi,
            key=average_domain_roi.get
        )

        worst_domain = min(
            average_domain_roi,
            key=average_domain_roi.get
        )

        return {

            "total_agents": total_agents,

            "total_implementation_cost": round(
                total_implementation_cost,
                2
            ),

            "total_operating_cost": round(
                total_operating_cost,
                2
            ),

            "total_annual_savings": round(
                total_annual_savings,
                2
            ),

            "total_net_benefit": round(
                total_net_benefit,
                2
            ),

            "average_roi": round(
                average_roi,
                2
            ),

            "average_payback": round(
                average_payback,
                2
            ),

            "highest_roi": highest_roi,

            "lowest_roi": lowest_roi,

            "best_domain": best_domain,

            "worst_domain": worst_domain,
        }