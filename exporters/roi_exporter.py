import csv
import os


class ROIExporter:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

    def export_csv(self, roi_results):

        filepath = "data/roi_results.csv"

        with open(filepath, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Rank",
                "Agent ID",
                "Agent Name",
                "Business Domain",
                "Implementation Cost",
                "Operating Cost",
                "Annual Savings",
                "Net Benefit",
                "ROI %",
                "Payback (Months)",
                "ROI Score",
            ])

            for agent in roi_results:

                writer.writerow([
                    agent.ranking,
                    agent.agent_id,
                    agent.agent_name,
                    agent.business_domain,
                    agent.implementation_cost,
                    agent.annual_operating_cost,
                    agent.annual_labor_savings,
                    agent.net_annual_benefit,
                    round(agent.roi_percentage, 2),
                    round(agent.payback_period_months, 2),
                    round(agent.roi_score, 2),
                ])

        print(f"\n📄 ROI Report Saved : {filepath}")