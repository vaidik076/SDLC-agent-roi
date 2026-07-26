from datetime import datetime
from models.trace import Trace
from rca.rca_engine import analyze_trace_rca


def make_trace(**kwargs):
    defaults = dict(
        task_id='t1',
        resolved=False,
        retries=0,
        token_usage=0,
        latency_seconds=1.0,
        human_intervention=False,
        tool_calls=[],
        raw_evidence_refs=[],
    )
    defaults.update(kwargs)
    return Trace(**defaults)


def test_rca_excessive_retries():
    tr = make_trace(task_id='r1', retries=4)
    out = analyze_trace_rca(tr)
    assert out['root_cause'] in ('excessive_retries', 'test_failure_loop', 'low_overall_performance')
    assert out['confidence'] >= 20


def test_rca_high_token_consumption():
    tr = make_trace(task_id='r2', token_usage=5000)
    out = analyze_trace_rca(tr)
    assert out['root_cause'] == 'high_token_consumption'
    assert 'trace.token_usage' in out['evidence'][0]


def test_rca_human_intervention():
    tr = make_trace(task_id='r3', human_intervention=True)
    out = analyze_trace_rca(tr)
    assert out['root_cause'] == 'human_intervention'


def test_rca_test_failure_loop():
    tr = make_trace(task_id='r4', resolved=False, retries=2, tool_calls=[{"name": "pytest"}])
    out = analyze_trace_rca(tr)
    assert out['root_cause'] == 'test_failure_loop'


def test_rca_insufficient_evidence():
    tr = make_trace(task_id='r5', resolved=False, token_usage=0, tool_calls=[])
    out = analyze_trace_rca(tr)
    assert out['root_cause'] == 'insufficient_evidence'
