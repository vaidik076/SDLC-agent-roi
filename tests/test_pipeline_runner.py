from datetime import datetime
from models.trace import Trace
from pipeline.runner import process_trace, process_traces


def make_trace(tid='task-x', resolved=True):
    return Trace(
        task_id=tid,
        resolved=resolved,
        retries=1,
        token_usage=1000,
        latency_seconds=10.0,
        human_intervention=False,
        tool_calls=[{"name": "pytest"}],
        raw_evidence_refs=["e1"],
    )


def test_process_trace_integration(tmp_path):
    tr = make_trace('task-123', resolved=True)
    assumptions = {
        'token_price_per_1k': 0.01,
        'dev_hourly_rate': 50.0,
        'hours_saved_per_success': 0.25,
        'executions_per_year': 100,
        'implementation_cost': 100.0,
        'annual_operating_cost': 0.0,
    }

    rec = process_trace(tr, assumptions=assumptions, write_path=str(tmp_path))
    assert rec['task_id'] == 'task-123'
    assert 'scores' in rec and 'overall_score' in rec['scores']
    assert 'roi' in rec and 'roi_percent' in rec['roi']
    assert 'rca' in rec and 'root_cause' in rec['rca']
    assert 'owner' in rec and 'owner' in rec['owner']

    # file written
    out_file = tmp_path / 'task-123.json'
    assert out_file.exists()


def test_process_traces_batch():
    traces = [make_trace('t1'), make_trace('t2', resolved=False)]
    results = process_traces(traces)
    assert isinstance(results, list) and len(results) == 2
    for r in results:
        assert 'scores' in r and 'roi' in r and 'rca' in r and 'owner' in r
