from models.roi import ROIResult


class RecommendationEngine:

    def categorize(self, roi_results: list[ROIResult]):

        build_now = []
        consider = []
        low_priority = []

        for agent in roi_results:

            # ---------------------------------------
            # High Priority
            # ---------------------------------------

            if (
                agent.roi_percentage >= 100
                and agent.payback_period_months <= 12
            ):
                build_now.append(agent)

            # ---------------------------------------
            # Medium Priority
            # ---------------------------------------

            elif (
                agent.roi_percentage >= 50
                and agent.payback_period_months <= 24
            ):
                consider.append(agent)

            # ---------------------------------------
            # Low Priority
            # ---------------------------------------

            else:
                low_priority.append(agent)

        return {
            "build_now": build_now,
            "consider": consider,
            "low_priority": low_priority,
        }