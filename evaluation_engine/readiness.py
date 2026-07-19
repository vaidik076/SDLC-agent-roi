class ReadinessEngine:

    # ==========================================================
    # Readiness Level
    # ==========================================================

    def evaluate(self, overall_score):

        if overall_score >= 90:
            return "Excellent"

        elif overall_score >= 75:
            return "Ready"

        elif overall_score >= 60:
            return "Moderate"

        elif overall_score >= 40:
            return "Needs Improvement"

        else:
            return "Not Ready"