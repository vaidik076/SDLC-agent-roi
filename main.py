from agent_generator.metadata_generator import AgentGenerator

from roi_engine.calculator import ROICalculator
from roi_engine.ranking import ROIRanking
from roi_engine.analytics import PortfolioAnalytics
from roi_engine.recommendation import RecommendationEngine
from exporters.roi_exporter import ROIExporter

from evaluation_engine.evaluator import EvaluationEngine

import csv
import os


def main():

    # ==========================================================
    # Generate Enterprise AI Agents
    # ==========================================================

    generator = AgentGenerator()
    agents = generator.generate()

    print("=" * 90)
    print(f"Generated {len(agents)} Enterprise AI Agents")
    print("=" * 90)

    # ==========================================================
    # ROI Calculation
    # ==========================================================

    calculator = ROICalculator()

    roi_results = []

    for agent in agents:
        roi_results.append(calculator.calculate(agent))

    # ==========================================================
    # ROI Ranking
    # ==========================================================

    ranking_engine = ROIRanking()

    ranked_agents = ranking_engine.rank(roi_results)

    top_agents = ranked_agents[:10]

    # ==========================================================
    # Portfolio Analytics
    # ==========================================================

    analytics = PortfolioAnalytics()

    summary = analytics.generate_summary(ranked_agents)

    # ==========================================================
    # Recommendation Engine
    # ==========================================================

    recommendation_engine = RecommendationEngine()

    recommendations = recommendation_engine.categorize(ranked_agents)

    # ==========================================================
    # Export ROI Report
    # ==========================================================

    exporter = ROIExporter()
    exporter.export_csv(ranked_agents)

    # ==========================================================
    # Evaluation Engine
    # ==========================================================

    evaluation_engine = EvaluationEngine()

    evaluations = evaluation_engine.evaluate_all(
        agents
    )

    # ==========================================================
    # Export Evaluation Report
    # ==========================================================

    os.makedirs("output", exist_ok=True)

    with open(
        "output/evaluation_results.csv",
        "w",
        newline="",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Agent ID",
            "Agent Name",
            "Business Domain",
            "Business Impact",
            "Data Readiness",
            "AI Readiness",
            "Technical Complexity",
            "Risk Score",
            "Overall Score",
            "Readiness",
            "Recommendation",
        ])

        for evaluation in evaluations:

            writer.writerow([
                evaluation.agent_id,
                evaluation.agent_name,
                evaluation.business_domain,
                evaluation.business_impact_score,
                evaluation.data_readiness_score,
                evaluation.ai_readiness_score,
                evaluation.technical_complexity_score,
                evaluation.risk_score,
                evaluation.overall_score,
                evaluation.readiness_level,
                evaluation.recommendation,
            ])

    # ==========================================================
    # TOP 10 AI AGENTS
    # ==========================================================

    print()
    print("=" * 90)
    print("TOP 10 AI AGENTS BY ROI SCORE")
    print("=" * 90)

    for agent in top_agents:

        print()
        print(f"Rank #{agent.ranking}")
        print("-" * 90)

        print(f"Agent Name          : {agent.agent_name}")
        print(f"Agent ID            : {agent.agent_id}")
        print(f"Business Domain     : {agent.business_domain}")

        print()

        print(f"Implementation Cost : ${agent.implementation_cost:,.2f}")
        print(f"Operating Cost      : ${agent.annual_operating_cost:,.2f}")

        print()

        print(f"Annual Savings      : ${agent.annual_labor_savings:,.2f}")
        print(f"Net Annual Benefit  : ${agent.net_annual_benefit:,.2f}")

        print()

        print(f"ROI                 : {agent.roi_percentage:.2f}%")
        print(f"Payback Period      : {agent.payback_period_months:.2f} Months")
        print(f"ROI Score           : {agent.roi_score:.2f}")

    # ==========================================================
    # PORTFOLIO SUMMARY
    # ==========================================================

    print()
    print("=" * 90)
    print("ENTERPRISE ROI PORTFOLIO SUMMARY")
    print("=" * 90)

    print(f"Total Agents               : {summary['total_agents']}")
    print(f"Implementation Cost        : ${summary['total_implementation_cost']:,.2f}")
    print(f"Operating Cost             : ${summary['total_operating_cost']:,.2f}")
    print(f"Annual Savings             : ${summary['total_annual_savings']:,.2f}")
    print(f"Net Annual Benefit         : ${summary['total_net_benefit']:,.2f}")

    print()

    print(f"Average ROI                : {summary['average_roi']:.2f}%")
    print(f"Average Payback            : {summary['average_payback']:.2f} Months")

    print()

    print(f"Highest ROI Agent          : {summary['highest_roi'].agent_name}")
    print(f"Highest ROI                : {summary['highest_roi'].roi_percentage:.2f}%")

    print()

    print(f"Lowest ROI Agent           : {summary['lowest_roi'].agent_name}")
    print(f"Lowest ROI                 : {summary['lowest_roi'].roi_percentage:.2f}%")

    print()

    print(f"Best Performing Domain     : {summary['best_domain']}")
    print(f"Worst Performing Domain    : {summary['worst_domain']}")

    print("=" * 90)

    # ==========================================================
    # IMPLEMENTATION RECOMMENDATIONS
    # ==========================================================

    print()
    print("=" * 90)
    print("IMPLEMENTATION RECOMMENDATIONS")
    print("=" * 90)

    print(f"🟢 Build Now      : {len(recommendations['build_now'])}")
    print(f"🟡 Consider       : {len(recommendations['consider'])}")
    print(f"🔴 Low Priority   : {len(recommendations['low_priority'])}")

    print()

    print("Top 5 Recommended Agents")
    print("-" * 90)

    for agent in recommendations["build_now"][:5]:

        print(
            f"{agent.ranking:>2}. "
            f"{agent.agent_name:<35}"
            f"ROI {agent.roi_percentage:>7.2f}%   "
            f"Payback {agent.payback_period_months:>6.2f} Months"
        )

    # ==========================================================
    # EVALUATION SUMMARY
    # ==========================================================

    print()
    print("=" * 90)
    print("EVALUATION SUMMARY")
    print("=" * 90)

    for evaluation in evaluations[:10]:

        print()
        print(f"{evaluation.agent_name}")
        print("-" * 90)

        print(f"Business Impact        : {evaluation.business_impact_score:.0f}")
        print(f"Data Readiness         : {evaluation.data_readiness_score:.0f}")
        print(f"AI Readiness           : {evaluation.ai_readiness_score:.0f}")
        print(f"Technical Complexity   : {evaluation.technical_complexity_score:.0f}")
        print(f"Risk Score             : {evaluation.risk_score:.0f}")

        print()

        print(f"Overall Score          : {evaluation.overall_score:.2f}")
        print(f"Readiness              : {evaluation.readiness_level}")
        print(f"Recommendation         : {evaluation.recommendation}")

    # ==========================================================
    # Generated Files
    # ==========================================================

    print()
    print("=" * 90)
    print("FILES GENERATED")
    print("=" * 90)

    print("✔ data/agents.csv")
    print("✔ data/agents.json")
    print("✔ data/roi_results.csv")
    print("✔ output/evaluation_results.csv")

    print()

    print("=" * 90)
    print("ROI ENGINE + EVALUATION ENGINE COMPLETED SUCCESSFULLY")
    print("=" * 90)


if __name__ == "__main__":
    main()