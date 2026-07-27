"""Recommendation engine: generate concise, prioritized recommendations from RCA, ownership, trace context, scores and ROI.

Design:
- Deterministic templates per root cause with parameter substitution
- Returns: text (short action), priority(High/Medium/Low), expected_impact (qualitative), estimated_effort_hours
- Keep heuristics simple and transparent for demo
"""
from typing import Dict, Any


def generate_recommendation(rca: Dict[str, Any], owner: Dict[str, Any], trace: Dict[str, Any], scores: Dict[str, Any], roi: Dict[str, Any]) -> Dict[str, Any]:
    root = rca.get("root_cause") if isinstance(rca, dict) else str(rca)
    confidence = rca.get("confidence") if isinstance(rca, dict) else None
    owner_name = owner.get("owner") if isinstance(owner, dict) else "Platform Engineering"

    # Default recommendation
    rec_text = "Investigate the task and review recent runs and logs to determine corrective action."
    priority = "Medium"
    expected_impact = "Moderate improvement in reliability and ROI if addressed."
    est_hours = 8

    # Templates by root cause
    if root == "test_failure_loop":
        rec_text = f"Fix failing tests and/or flakiness causing repeated failures; run tests in CI and add assertions or stabilize test fixtures. Owner: {owner_name}."
        priority = "High"
        expected_impact = "High — fixing tests will likely convert failures to passes and improve ROI significantly."
        est_hours = 16
    elif root == "excessive_retries":
        rec_text = f"Investigate retry causes (timeouts, rate limits, brittle integrations). Add backoff/retry guards and reduce unnecessary retries. Owner: {owner_name}."
        priority = "High"
        expected_impact = "High — reducing retries improves reliability and cost efficiency."
        est_hours = 12
    elif root == "high_token_consumption":
        rec_text = f"Optimize model usage: reduce token usage by prompt engineering, lower-cost models, or caching. Owner: {owner_name}."
        priority = "Medium"
        expected_impact = "Medium — cost savings may be noticeable on scale."
        est_hours = 8
    elif root == "high_latency":
        rec_text = f"Investigate platform and infra latency; profile long-running steps and consider async or batch processing. Owner: {owner_name}."
        priority = "Medium"
        expected_impact = "Medium — improved responsiveness and potential cost reductions."
        est_hours = 10
    elif root == "human_intervention":
        rec_text = f"Reduce manual steps: automate approvals or implement guardrails to lower human intervention. Owner: {owner_name}."
        priority = "Medium"
        expected_impact = "Low to Medium — reduces human effort but may require feature work."
        est_hours = 24
    elif root == "insufficient_evidence":
        rec_text = f"Improve telemetry and evidence collection (CI logs, LLM usage) so the platform can evaluate outcomes. Owner: {owner_name}."
        priority = "Low"
        expected_impact = "Low — foundational observability improvement enabling future insights."
        est_hours = 8
    elif root == "low_overall_performance":
        rec_text = f"Comprehensive review: combine logs, traces, and recent changes to identify systemic issues. Owner: {owner_name}."
        priority = "Medium"
        expected_impact = "Medium — depends on identified causes."
        est_hours = 16
    elif root == "success":
        rec_text = f"No action required — task succeeded. Consider automating this success path further. Owner: {owner_name}."
        priority = "Low"
        expected_impact = "Low — maintain operations."
        est_hours = 2
    else:
        rec_text = f"Investigate root cause '{root}'. Owner: {owner_name}."
        priority = "Medium"
        expected_impact = "Unknown — investigation required."
        est_hours = 8

    # Adjust priority upward if confidence is high and ROI negative (urgent)
    try:
        roi_val = float(roi.get("roi_percent", 0) or 0)
    except Exception:
        roi_val = 0

    if roi_val < 0 and priority != "High":
        priority = "High"
        expected_impact = "High impact on cost if resolved."

    recommendation = {
        "text": rec_text,
        "priority": priority,
        "expected_impact": expected_impact,
        "estimated_effort_hours": est_hours,
        "confidence": confidence,
    }

    return recommendation
