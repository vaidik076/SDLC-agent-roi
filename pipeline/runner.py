"""Pipeline runner: integrate trace scoring and ROI calculation to produce per-task records.

Provides:
- process_trace(trace, assumptions=None, scoring_config=None, write_path=None) -> dict
- process_traces(traces, ...) -> list[dict]

Each returned record contains:
- trace: the serialized Trace dict
- scores: per-dimension scores and overall_score
- roi: ROI result dict

Optionally writes each record as JSON to write_path directory as <task_id>.json
"""
from typing import List, Dict, Any, Optional
import os
import json

from models.trace import Trace
from evaluation_engine.trace_scoring import score_trace
from roi_engine.trace_calculator import calculate_roi_from_trace
from rca.rca_engine import analyze_trace_rca
from ownership.ownership_map import map_root_cause_to_owner
from recommendation.recommender import generate_recommendation


def process_trace(trace: Trace, assumptions: Optional[Dict[str, Any]] = None, scoring_config: Optional[Dict[str, Any]] = None, write_path: Optional[str] = None) -> Dict[str, Any]:
    scores = score_trace(trace, scoring_config)
    roi = calculate_roi_from_trace(trace, assumptions)

    # Root cause analysis and ownership mapping
    try:
        rca = analyze_trace_rca(trace, scores)
    except Exception as e:
        rca = {"task_id": trace.task_id, "root_cause": "rca_error", "confidence": 0.0, "evidence": [str(e)], "details": {}}

    try:
        owner = map_root_cause_to_owner(rca.get("root_cause"), trace=trace.dict())
    except Exception:
        owner = {"mapped_name": rca.get("root_cause"), "owner": "Platform Engineering", "contact": "platform-eng@example.com", "priority": "Medium", "rationale": "Ownership lookup failed"}

    # Recommendation generation
    try:
        recommendation = generate_recommendation(rca, owner, trace.dict(), scores, roi)
    except Exception as e:
        recommendation = {"text": f"Recommendation generation failed: {e}", "priority": "Low", "expected_impact": "Unknown", "estimated_effort_hours": None}

    record = {
        "task_id": trace.task_id,
        "trace": trace.dict(),
        "scores": scores,
        "roi": roi,
        "rca": rca,
        "owner": owner,
        "recommendation": recommendation,
    }

    if write_path:
        os.makedirs(write_path, exist_ok=True)
        out_file = os.path.join(write_path, f"{trace.task_id}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

    return record


def process_traces(traces: List[Trace], assumptions: Optional[Dict[str, Any]] = None, scoring_config: Optional[Dict[str, Any]] = None, write_path: Optional[str] = None) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for tr in traces:
        rec = process_trace(tr, assumptions=assumptions, scoring_config=scoring_config, write_path=write_path)
        results.append(rec)
    return results
