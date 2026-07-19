from models.roi import ROIResult


class ROIRanking:

    def rank(self, roi_results: list[ROIResult]) -> list[ROIResult]:
        """
        Rank agents by ROI Score (Highest to Lowest)
        """

        ranked_results = sorted(
            roi_results,
            key=lambda x: x.roi_score,
            reverse=True,
        )

        for rank, result in enumerate(ranked_results, start=1):
            result.ranking = rank

        return ranked_results

    def top_agents(
        self,
        roi_results: list[ROIResult],
        top_n: int = 10,
    ) -> list[ROIResult]:
        """
        Return Top N Agents
        """

        ranked = self.rank(roi_results)

        return ranked[:top_n]

    def bottom_agents(
        self,
        roi_results: list[ROIResult],
        bottom_n: int = 10,
    ) -> list[ROIResult]:
        """
        Return Bottom N Agents
        """

        ranked = self.rank(roi_results)

        return ranked[-bottom_n:]