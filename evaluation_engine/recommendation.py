class RecommendationEngine:

    # ==========================================================
    # Generate Recommendation
    # ==========================================================

    def generate(self, overall_score):

        if overall_score >= 90:
            return "Deploy Immediately"

        elif overall_score >= 75:
            return "Deploy After Improvements"

        elif overall_score >= 60:
            return "Prototype First"

        elif overall_score >= 40:
            return "Further Investigation Required"

        else:
            return "Not Recommended"