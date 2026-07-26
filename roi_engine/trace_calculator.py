"""ROI calculator that converts a Trace into business-relevant financial metrics.

Design:
- Uses explicit, configurable assumptions (token price per 1k tokens, developer hourly rate,
  hours_saved per successful execution, executions_per_year, implementation_cost, annual_operating_cost).
- Computes per-execution AI cost and annualized costs/benefits.
- Returns a clear dict with all assumptions echoed so they are not silent.
"""
from typing import Dict, Any

from models.trace import Trace


DEFAULT_ASSUMPTIONS = {
    # Price in USD per 1,000 tokens (must be stated explicitly)
    "token_price_per_1k": 0.002,  # USD per 1k tokens (default example)
    # Developer fully-burdened hourly rate in USD
    "dev_hourly_rate": 60.0,
    # Estimated hours saved per successful execution (if None, use heuristic)
    "hours_saved_per_success": 0.5,  # 30 minutes
    # Number of executions per year (to annualize costs/benefits)
    "executions_per_year": 250,
    # One-time implementation cost for automation (USD)
    "implementation_cost": 1000.0,
    # Annual operating cost aside from token costs (USD/year)
    "annual_operating_cost": 0.0,
    # Optional compute hourly cost to account for runtime (USD/hour)
    "compute_hourly_cost": 0.0,
}


def calculate_roi_from_trace(trace: Trace, assumptions: Dict[str, Any] = None) -> Dict[str, Any]:
    cfg = DEFAULT_ASSUMPTIONS.copy()
    if assumptions:
        cfg.update(assumptions)

    # Per-execution AI cost from tokens
    token_price_per_1k = float(cfg["token_price_per_1k"])
    ai_cost_per_execution = (trace.token_usage / 1000.0) * token_price_per_1k

    # Optional compute time cost: assume compute cost proportional to latency_seconds
    compute_hourly_cost = float(cfg.get("compute_hourly_cost", 0.0))
    compute_cost = (trace.latency_seconds / 3600.0) * compute_hourly_cost
    ai_cost_per_execution += compute_cost

    # How many hours saved per success; if task unresolved assume 0 saved
    if trace.resolved:
        hours_saved = float(cfg.get("hours_saved_per_success", 0.0))
    else:
        hours_saved = 0.0

    dev_hourly_rate = float(cfg["dev_hourly_rate"])

    # Annualize over executions per year
    executions_per_year = float(cfg["executions_per_year"])

    annual_ai_cost = ai_cost_per_execution * executions_per_year
    annual_human_cost_avoided = hours_saved * dev_hourly_rate * executions_per_year

    annual_operating_cost = float(cfg.get("annual_operating_cost", 0.0))
    implementation_cost = float(cfg.get("implementation_cost", 0.0))

    net_annual_benefit = annual_human_cost_avoided - annual_ai_cost - annual_operating_cost

    if implementation_cost > 0:
        roi_percent = (net_annual_benefit / implementation_cost) * 100.0
    else:
        roi_percent = float('inf') if net_annual_benefit > 0 else 0.0

    if net_annual_benefit > 0:
        payback_months = (implementation_cost / net_annual_benefit) * 12.0 if implementation_cost > 0 else 0.0
    else:
        payback_months = None

    result = {
        "trace_task_id": trace.task_id,
        "ai_cost_per_execution_usd": round(ai_cost_per_execution, 6),
        "annual_ai_cost_usd": round(annual_ai_cost, 2),
        "annual_human_cost_avoided_usd": round(annual_human_cost_avoided, 2),
        "annual_operating_cost_usd": round(annual_operating_cost, 2),
        "implementation_cost_usd": round(implementation_cost, 2),
        "net_annual_benefit_usd": round(net_annual_benefit, 2),
        "roi_percent": round(roi_percent, 2) if roi_percent not in (float('inf'),) else float('inf'),
        "payback_months": round(payback_months, 2) if isinstance(payback_months, (int, float)) else None,
        "assumptions_used": cfg,
        "trace_summary": {
            "resolved": bool(trace.resolved),
            "retries": int(trace.retries),
            "token_usage": int(trace.token_usage),
            "latency_seconds": float(trace.latency_seconds),
            "human_intervention": bool(trace.human_intervention),
        },
    }

    return result
