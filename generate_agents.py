from pathlib import Path
import csv
import json

from agent_generator.metadata_generator import AgentGenerator


def main():

    # ==========================================
    # Generate Agents
    # ==========================================

    generator = AgentGenerator()
    agents = generator.generate()

    print(f"\n✅ Generated {len(agents)} Enterprise AI Agents\n")

    # ==========================================
    # Create Output Directory
    # ==========================================

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    # ==========================================
    # Convert Pydantic Objects to Dictionaries
    # ==========================================

    agent_data = [agent.model_dump() for agent in agents]

    # ==========================================
    # Export CSV
    # ==========================================

    csv_file = output_dir / "agents.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=agent_data[0].keys()
        )

        writer.writeheader()
        writer.writerows(agent_data)

    # ==========================================
    # Export JSON
    # ==========================================

    json_file = output_dir / "agents.json"

    with open(json_file, "w", encoding="utf-8") as file:

        json.dump(agent_data, file, indent=4)

    # ==========================================
    # Print Summary
    # ==========================================

    print(f"📄 CSV Saved  : {csv_file}")
    print(f"📄 JSON Saved : {json_file}")

    print("\nFirst 5 Agents\n")

    for agent in agents[:5]:
        print(agent)
        print("-" * 100)


if __name__ == "__main__":
    main()