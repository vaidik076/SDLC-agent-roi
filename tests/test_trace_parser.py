from datetime import datetime, timedelta
from models.evidence import Evidence
from normalize.trace_parser import parse_trace_from_evidence


def make_ev(eid, typ, ts, content=None, metadata=None):
    return Evidence(
        evidence_id=eid,
        source='test',
        type=typ,
        timestamp=ts,
        metadata=metadata or {},
        content=content or {},
        confidence=1.0,
    )


def test_parse_trace_basic():
    t0 = datetime.utcnow()
    ev1 = make_ev('c1', 'commit', t0, content={'repo': 'x'})
    ev2 = make_ev('run1', 'llm_run', t0 + timedelta(seconds=2), content={'llm': {'token_usage': 120}, 'tool_calls': [{'name': 'pytest'}]})
    ev3 = make_ev('test1', 'test_result', t0 + timedelta(seconds=5), content={'status': 'pass'})

    trace = parse_trace_from_evidence('task-1', [ev1, ev2, ev3])

    assert trace.task_id == 'task-1'
    assert trace.resolved is True
    assert trace.token_usage == 120
    assert trace.retries == 0
    assert trace.human_intervention is False
    assert len(trace.tool_calls) == 1
    assert trace.latency_seconds >= 5
    assert trace.raw_evidence_refs == ['c1', 'run1', 'test1']
