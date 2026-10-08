# Enterprise Agent ROI Evaluation System

Enterprise AI platform for generating, evaluating, and prioritizing synthetic AI agents using ROI analytics, scoring, and an interactive dashboard.

## Current status (as of now)

This repository is at a working MVP checkpoint for the enterprise-agent ROI platform. The core project structure is in place, including:

- synthetic agent generation and scoring flow
- ROI calculation and ranking logic
- evaluation engine with trace-based scoring
- RCA, ownership mapping, and recommendation generation
- JSON output generation for demo runs
- dashboard support for reviewing campaign results

This is a good stopping point to continue from on the next machine/project setup. The next phase should focus on hardening the system, improving persistence, UI/UX polish, and mapping the demo into a production-ready workflow.

Recommended next steps for continuation:

- connect the pipeline to real enterprise data sources
- add persistent storage and export/import workflows
- improve dashboard filtering and analytics views
- add tests for scoring, ROI, and recommendation modules
- package the app for deployment and operational use

## What is included

- Synthetic enterprise agent generation
- ROI calculation and ranking
- Evaluation and readiness scoring
- Demo pipeline output written to JSON
- Streamlit dashboard for reviewing demo results

## Requirements

- Python 3.10 or newer
- `pip`
- Optional: Docker for the containerized demo

## Install

From the repository root, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks script execution, run this first in the same session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Run the main pipeline

This script generates agents, calculates ROI, ranks them, and writes CSV outputs into `output/`:

```powershell
python main.py
```

## Run the demo pipeline

This creates sample trace data and writes JSON outputs into `output/demo/`:

```powershell
python run_demo.py
```

## Run the dashboard

The dashboard reads JSON files from `output/demo/` by default. Run the demo first so the dashboard has data to display:

```powershell
streamlit run dashboard/app.py
```

Then open the local URL shown in the terminal, usually `http://localhost:8501`.

## Run with Docker

Use Docker if you want a single command that runs the demo and dashboard together:

```powershell
docker build -t enterprise-agent-roi:demo .
docker run --rm -p 8501:8501 -v "%cd%:/app/output" enterprise-agent-roi:demo
```

Open `http://localhost:8501` in your browser after the container starts.

## Output files

- `output/roi_results.csv` from the ROI pipeline
- `output/evaluation_results.csv` from the evaluation engine
- `output/demo/*.json` from the demo pipeline

## Troubleshooting

- If imports fail, make sure you are running commands from the repository root and that the virtual environment is active.
- If `streamlit` is not found, install dependencies again with `pip install -r requirements.txt`.
- If package installation is blocked in your environment, use the Docker option above.
