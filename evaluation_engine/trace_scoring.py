"""Trace-based evaluation scoring.

Provides a function `score_trace` that takes a Trace model and optional
configuration and returns per-dimension scores and an aggregated overall
score in the 0-100 range.

Design principles:
- Deterministic, interpretable heuristics rather than ML
- Configurable weights and normalization constants
- Conservative defaults suitable for a demo
"""
from typing import Dict, Any

from models.trace import Trace


DEFAULT_CONFIG = {
    "weights": {
        "reliability": 0.4,
        "retry_penalty": 0.2,
        "cost_efficiency": 0.2,
        "human_effort": 0.2,
    },
    # Normalization factors used to convert raw metrics into 0-100 scales
    "norm": {
        "tokens_per_point": 1000,  # every 1k tokens reduces cost score
        "latency_seconds_per_point": 60.0,  # each minute reduces cost score
        "retry_penalty_per_retry": 15,  # penalty points per retry for retry_penalty
    },
}


def clamp_0_100(x: float) -> float:
    return max(0.0, min(100.0, round(x, 2)))


def score_trace(trace: Trace, config: Dict[str, Any] = None) -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if config:
        # shallow merge
        cfg.update({k: v for k, v in config.items() if v is not None})
        if "weights" in config:
            cfg["weights"].update(config["weights"])
        if "norm" in config:
            cfg["norm"].update(config["norm"])

    weights = cfg["weights"]
    norm = cfg["norm"]

    # Reliability: favors resolved outcomes and low retries + no human intervention
    if trace.resolved:
        base_reliability = 95.0
    else:
        base_reliability = 40.0

    reliability_penalty = min(80.0, trace.retries * 8.0)
    if trace.human_intervention:
        reliability_penalty += 12.0

    reliability_score = clamp_0_100(base_reliability - reliability_penalty)

    # Retry penalty score: 0 retries => 100, otherwise decreasing
    retry_score = clamp_0_100(max(0.0, 100.0 - trace.retries * float(norm["retry_penalty_per_retry"])))

    # Cost efficiency: lower token usage and shorter latency -> higher score
    token_factor = (trace.token_usage / float(max(1, norm["tokens_per_point"]))) * 5.0
    latency_factor = (trace.latency_seconds / float(max(1.0, norm["latency_seconds_per_point"]))) * 2.0
    cost_penalty = token_factor + latency_factor
    cost_efficiency_score = clamp_0_100(max(0.0, 100.0 - cost_penalty))

    # Human effort: penalize if human intervention occurred and scale with retries
    if trace.human_intervention:
        human_score = clamp_0_100(max(0.0, 100.0 - 40.0 - trace.retries * 4.0))
    else:
        human_score = clamp_0_100(max(0.0, 100.0 - trace.retries * 2.0))

    # Aggregated overall score (weighted)
    overall = (
        reliability_score * weights["reliability"]
        + retry_score * weights["retry_penalty"]
        + cost_efficiency_score * weights["cost_efficiency"]
        + human_score * weights["human_effort"]
    )

    overall_score = clamp_0_100(overall)

    result = {
        "reliability": reliability_score,
        "retry_penalty": retry_score,
        "cost_efficiency": cost_efficiency_score,
        "human_effort": human_score,
        "overall_score": overall_score,
        "config_used": cfg,
    }

    return result
