from datetime import datetime
from models.trace import Trace
from roi_engine.trace_calculator import calculate_roi_from_trace


def test_roi_resolved_small_tokens():
    trace = Trace(
        task_id='tt1',
        resolved=True,
        retries=0,
        token_usage=500,  # 0.5k tokens
        latency_seconds=2.0,
        human_intervention=False,
        tool_calls=[],
        raw_evidence_refs=[],
    )

    assumptions = {
        'token_price_per_1k': 0.01,  # $0.01 per 1k tokens
        'dev_hourly_rate': 50.0,
        'hours_saved_per_success': 0.5,
        'executions_per_year': 100,
        'implementation_cost': 500.0,
        'annual_operating_cost': 10.0,
    }

    res = calculate_roi_from_trace(trace, assumptions)

    # AI cost per execution = (500/1000)*0.01 = 0.005
    assert abs(res['ai_cost_per_execution_usd'] - 0.005) < 1e-6
    # Annual human avoided = 0.5 * 50 * 100 = 2500
    assert res['annual_human_cost_avoided_usd'] == 2500.0
    # Annual ai cost = 0.005 * 100 = 0.5
    assert res['annual_ai_cost_usd'] == 0.5
    # Net annual benefit ~ 2500 - 0.5 - 10 = 2489.5
    assert abs(res['net_annual_benefit_usd'] - 2489.5) < 0.1
    # ROI percent = net / implementation_cost *100 = 2489.5 / 500 *100 ~= 497.9
    assert res['roi_percent'] > 400


def test_roi_unresolved_no_benefit():
    trace = Trace(
        task_id='tt2',
        resolved=False,
        retries=3,
        token_usage=2000,
        latency_seconds=30.0,
        human_intervention=True,
        tool_calls=[],
        raw_evidence_refs=[],
    )

    assumptions = {
        'token_price_per_1k': 0.02,
        'dev_hourly_rate': 80.0,
        'hours_saved_per_success': 1.0,
        'executions_per_year': 50,
        'implementation_cost': 1000.0,
        'annual_operating_cost': 100.0,
    }

    res = calculate_roi_from_trace(trace, assumptions)
    # Since unresolved, hours_saved assumed 0 => annual_human_cost_avoided == 0
    assert res['annual_human_cost_avoided_usd'] == 0.0
    # annual ai cost > 0
    assert res['annual_ai_cost_usd'] > 0
    # net annual benefit <= 0
    assert res['net_annual_benefit_usd'] <= 0
    # payback_months is None when net benefit <=0
    assert res['payback_months'] is None
