"""Simple demo runner for the pipeline.

Creates a few sample Trace records, runs the pipeline (scoring, ROI, RCA, ownership),
and writes per-task JSON outputs to output/demo/. Prints a short summary to the console.

Usage:
  python run_demo.py

Note: the script imports project modules (pydantic, etc). Ensure project dependencies are
installed in your active Python environment (see README). If imports fail, the script
prints a helpful message and exits.
"""
from datetime import datetime, timedelta
import os
import json
import sys

try:
    from models.trace import Trace
    from pipeline.runner import process_traces
except Exception as e:
    print("ERROR: Could not import project modules. Make sure dependencies are installed and you're running from the repo root.")
    print("Import error:", e)
    sys.exit(2)


def make_trace(tid: str, resolved: bool, retries: int, token_usage: int, latency_seconds: float, human: bool, tool_calls=None):
    return Trace(
        task_id=tid,
        resolved=resolved,
        retries=retries,
        token_usage=token_usage,
        latency_seconds=latency_seconds,
        human_intervention=human,
        tool_calls=tool_calls or [],
        raw_evidence_refs=[f"ev-{tid}-1"],
    )


def main():
    traces = [
        make_trace('demo-1', resolved=True, retries=0, token_usage=300, latency_seconds=5.0, human=False, tool_calls=[{"name":"pytest"}]),
        make_trace('demo-2', resolved=False, retries=4, token_usage=6000, latency_seconds=120.0, human=True, tool_calls=[{"name":"pytest"}]),
        make_trace('demo-3', resolved=False, retries=0, token_usage=0, latency_seconds=1.0, human=False, tool_calls=[]),
    ]

    assumptions = {
        'token_price_per_1k': 0.01,
        'dev_hourly_rate': 50.0,
        'hours_saved_per_success': 0.5,
        'executions_per_year': 100,
        'implementation_cost': 500.0,
        'annual_operating_cost': 10.0,
    }

    out_dir = os.path.join('output', 'demo')
    results = process_traces(traces, assumptions=assumptions, write_path=out_dir)

    print('\nDemo pipeline run complete. Results written to:', os.path.abspath(out_dir))
    print('Summary:')
    for r in results:
        tid = r.get('task_id')
        scores = r.get('scores', {})
        roi = r.get('roi', {})
        rca = r.get('rca', {})
        owner = r.get('owner', {})
        print(f"- {tid}: overall_score={scores.get('overall_score')}, roi%={roi.get('roi_percent')}, root_cause={rca.get('root_cause')}, owner={owner.get('owner')}")

    print('\nTo inspect full output JSON files, open the files in the output/demo directory.')


if __name__ == '__main__':
    main()
