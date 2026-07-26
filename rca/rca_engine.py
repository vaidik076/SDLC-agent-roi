"""Root Cause Analysis (RCA) engine.

This module implements deterministic, rule-based RCA suitable for a demo. The
analyzer inspects Trace fields and optional evaluation scores to attribute a
likely root cause label, a confidence percentage, and supporting evidence
pointers for transparency.

The function `analyze_trace_rca` is the public entrypoint.
"""
from typing import Dict, Any, List, Optional

from models.trace import Trace


DEFAULT_CONFIG = {
    "thresholds": {
        "excessive_retries": 3,
        "high_token_usage": 2000,
        "high_latency_seconds": 300.0,
        "low_overall_score": 50.0,
    }
}


def analyze_trace_rca(trace: Trace, scores: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)

    t = trace
    thr = cfg["thresholds"]

    evidence: List[str] = []
    reasons: List[str] = []

    # Basic signals
    if t.human_intervention:
        reasons.append("human_intervention")
        evidence.append("trace.human_intervention == True")

    if t.retries >= thr["excessive_retries"]:
        reasons.append("excessive_retries")
        evidence.append(f"trace.retries == {t.retries} >= {thr['excessive_retries']}")

    if t.token_usage >= thr["high_token_usage"]:
        reasons.append("high_token_consumption")
        evidence.append(f"trace.token_usage == {t.token_usage} >= {thr['high_token_usage']}")

    if t.latency_seconds >= thr["high_latency_seconds"]:
        reasons.append("high_latency")
        evidence.append(f"trace.latency_seconds == {t.latency_seconds} >= {thr['high_latency_seconds']}")

    # Test failure loop heuristic: unresolved and there are test tool calls
    tool_names = [ (c.get("name") or "").lower() for c in (t.tool_calls or []) if isinstance(c, dict) ]
    if not t.resolved and any(n in ("pytest", "unittest", "nose", "test") for n in tool_names):
        reasons.append("test_failure_loop")
        evidence.append("unresolved and test tool calls present")

    # Insufficient evidence: no tool calls, zero tokens, not resolved
    if (not t.tool_calls) and t.token_usage == 0 and not t.resolved:
        reasons.append("insufficient_evidence")
        evidence.append("no tool_calls and token_usage==0 and unresolved")

    # Low overall score increases likelihood of generic underperformance
    overall_score = None
    if scores and isinstance(scores, dict):
        overall_score = scores.get("overall_score")
        if overall_score is not None and overall_score < thr["low_overall_score"]:
            reasons.append("low_overall_performance")
            evidence.append(f"overall_score == {overall_score} < {thr['low_overall_score']}")

    # Decide primary root cause by priority ordering
    priority = [
        "test_failure_loop",
        "excessive_retries",
        "high_token_consumption",
        "high_latency",
        "human_intervention",
        "insufficient_evidence",
        "low_overall_performance",
    ]

    primary = None
    for name in priority:
        if name in reasons:
            primary = name
            break

    if primary is None:
        # If resolved successfully with no flags, report success
        if t.resolved and t.retries == 0:
            primary = "success"
            evidence.append("resolved == True and retries == 0")
        else:
            # Fallback generic label
            primary = "unknown_underperformance" if not t.resolved else "success-with-warnings"
            if not t.resolved:
                evidence.append("unresolved and no clear rule matched")
            else:
                evidence.append("resolved but with warnings (retries/token/latency)")

    # Compute a simple confidence heuristic: base confidence by number of supporting evidence items
    # More evidence items -> higher confidence, up to 95%. If overall_score explicitly low, boost confidence slightly.
    base_confidence = min(80.0, 20.0 + len(evidence) * 20.0)
    if overall_score is not None:
        # if overall score strongly indicates low performance, increase confidence
        if overall_score < thr["low_overall_score"]:
            base_confidence = min(95.0, base_confidence + 10.0)

    confidence = round(base_confidence, 2)

    result: Dict[str, Any] = {
        "task_id": t.task_id,
        "root_cause": primary,
        "confidence": confidence,
        "evidence": evidence,
        "details": {
            "reasons": reasons,
            "overall_score": overall_score,
        },
    }

    return result
