from datetime import datetime, timedelta
from models.trace import Trace
from evaluation_engine.trace_scoring import score_trace


def test_score_trace_resolved_no_retries():
    t0 = datetime.utcnow()
    trace = Trace(
        task_id='t1',
        resolved=True,
        retries=0,
        token_usage=200,
        latency_seconds=5.0,
        human_intervention=False,
        tool_calls=[],
        raw_evidence_refs=[],
    )

    scores = score_trace(trace)
    assert scores['reliability'] >= 80
    assert scores['retry_penalty'] == 100
    assert scores['human_effort'] >= 90
    assert scores['overall_score'] >= 85


def test_score_trace_failed_many_retries():
    trace = Trace(
        task_id='t2',
        resolved=False,
        retries=5,
        token_usage=5000,
        latency_seconds=600.0,
        human_intervention=True,
        tool_calls=[],
        raw_evidence_refs=[],
    )

    scores = score_trace(trace)
    assert scores['reliability'] < 50
    assert scores['retry_penalty'] < 50
    assert scores['cost_efficiency'] < 50
    assert scores['human_effort'] < 50
    assert scores['overall_score'] < 60
