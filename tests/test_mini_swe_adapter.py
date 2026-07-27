import os
import json
from ingest.adapters.mini_swe_adapter import parse_mini_swe_trajectory


def make_sample_trajectory(path):
    traj = {
        "instance_id": "task-demo-1",
        "events": [
            {"type": "commit", "timestamp": "2026-07-27T12:00:00Z", "author": "dev", "message": "initial commit"},
            {"type": "llm_run", "timestamp": "2026-07-27T12:00:02Z", "llm": {"token_usage": 120}, "tool": {"name": "formatter"}},
            {"type": "test_result", "timestamp": "2026-07-27T12:00:05Z", "status": "pass"}
        ],
        "final_status": "pass"
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(traj, f)


def test_parse_mini_swe_trajectory(tmp_path):
    p = tmp_path / 'traj.json'
    make_sample_trajectory(str(p))

    evidences = parse_mini_swe_trajectory(str(p))
    assert isinstance(evidences, list)
    # expect at least 4 evidences: 3 events + summary
    assert len(evidences) >= 4
    # last evidence should be the summary
    summary = evidences[-1]
    assert summary.type == 'trajectory_summary'
    assert 'total_token_usage' in summary.content
    assert summary.content['total_token_usage'] == 120
    assert summary.metadata.get('final_status') == 'pass'
