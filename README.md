# Enterprise Agent ROI Evaluation System

Enterprise AI platform for generating, evaluating, and prioritizing 100+ synthetic AI agents using ROI analytics, LLM-powered reviews, and interactive business dashboards.

## 🚀 Features

- Synthetic Enterprise Agent Generator
- ROI Evaluation Engine
- Agent Scoring & Ranking
- LLM-based Meta Review Engine
- Executive Dashboard
- ROI Copilot

## 🛠️ Tech Stack

- Python
- Pydantic
- Pandas
- Faker
- Streamlit
- OpenAI / LLM APIs

> 🚧 Project currently under active development.


Quick demo
----------
A tiny convenience script is provided to run a short demo pipeline on example Trace records and write JSON outputs to output/demo.

1. Activate your virtual environment (PowerShell example):

   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned ; .\.venv\Scripts\Activate.ps1

2. Install dependencies (if not already installed):

   pip install pydantic pandas pytest

3. Run the demo script from the repo root:

   python run_demo.py

This writes output/demo/<task_id>.json for each demo task and prints a short summary.

Troubleshooting
- If `pip` is blocked by an Application Control policy (common in enterprise environments), ask your IT or security team to allow python package installation in your environment or provide an approved environment with required packages installed. Alternatives include using a pre-built container image, Conda environments provisioned by IT, or running the demo on a developer machine with fewer policy restrictions.
- If imports fail when running run_demo.py, double-check you're running the command from the repository root and that the virtualenv is active.


Streamlit dashboard (demo)
-------------------------
A minimal Streamlit app is provided at dashboard/app.py that reads the JSON outputs (default folder: output/demo) and displays a summary table plus task-level drill-down.

To run locally (requires streamlit to be installed):

1. Activate your venv (PowerShell):
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned ; .\.venv\Scripts\Activate.ps1

2. Install Streamlit if allowed:
   pip install streamlit

3. Run the app from the repo root:
   streamlit run dashboard/app.py

If installing packages is blocked locally, run the dashboard inside Docker (recommended). A Dockerfile is included — build and run the container as described below.
