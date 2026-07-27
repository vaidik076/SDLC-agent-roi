"""Adapter to convert mini-swe-agent trajectory JSON files into canonical Evidence records.

The adapter is defensive about the trace schema: it supports common fields found in
agent trajectory outputs such as `task_id`/`instance_id`, `events`/`steps`,
per-event timestamps, tool calls, model responses with token usage, and a final
`outcome` or `status` field. It returns a list of models.evidence.Evidence
objects so the rest of the pipeline can consume them uniformly.
"""
from typing import List, Dict, Any
import json
import os
from datetime import datetime

from models.evidence import Evidence


def _parse_ts(ts_val: Any) -> datetime:
    if isinstance(ts_val, datetime):
        return ts_val
    if ts_val is None:
        return datetime.utcnow()
    # try common ISO formats
    try:
        return datetime.fromisoformat(str(ts_val))
    except Exception:
        try:
            # fallback: numeric epoch
            return datetime.utcfromtimestamp(float(ts_val))
        except Exception:
            return datetime.utcnow()


def parse_mini_swe_trajectory(path: str) -> List[Evidence]:
    """Read a mini-swe-agent trajectory JSON file and convert it to Evidence list.

    Each event in the trajectory becomes one Evidence item. Additionally a
    summary Evidence with the final outcome and aggregated token usage is
    emitted with evidence_id '<instance_id>-summary' when available.

    Args:
        path: path to trajectory JSON file
    Returns:
        List[Evidence]
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    evidences: List[Evidence] = []

    # Top-level ids
    instance_id = data.get('instance_id') or data.get('task_id') or os.path.basename(path)
    traj_id = instance_id

    events = data.get('events') or data.get('steps') or data.get('trajectory') or []

    total_tokens = 0
    first_ts = None
    last_ts = None

    for idx, ev in enumerate(events):
        # ev can be a string or dict
        if isinstance(ev, str):
            ev_dict = {'type': 'log', 'text': ev}
        else:
            ev_dict = ev

        ts = _parse_ts(ev_dict.get('timestamp') or ev_dict.get('time') or ev_dict.get('ts'))
        if first_ts is None or ts < first_ts:
            first_ts = ts
        if last_ts is None or ts > last_ts:
            last_ts = ts

        ev_type = ev_dict.get('type') or ev_dict.get('event') or ev_dict.get('name') or 'event'

        metadata: Dict[str, Any] = {}
        content: Dict[str, Any] = {}

        # Common fields: tool calls
        tool = ev_dict.get('tool') or ev_dict.get('tool_call') or ev_dict.get('action')
        if tool:
            content['tool_calls'] = [tool] if isinstance(tool, str) else tool

        # LLM response / token usage
        # Accept several possible keys that may contain token numbers
        token_usage = None
        for key in ('token_usage', 'tokens', 'usage', 'llm_token_usage', 'llm_usage'):
            if key in ev_dict and ev_dict[key] is not None:
                try:
                    token_usage = int(ev_dict[key])
                    break
                except Exception:
                    pass

        # Some traces embed llm info under 'llm' or 'model'
        if token_usage is None and isinstance(ev_dict.get('llm'), dict):
            token_usage = ev_dict['llm'].get('token_usage') or ev_dict['llm'].get('tokens')
            if isinstance(token_usage, (str, float)):
                try:
                    token_usage = int(token_usage)
                except Exception:
                    token_usage = None

        if isinstance(token_usage, int):
            content['token_usage'] = token_usage
            total_tokens += token_usage

        # Execution outputs / status
        outcome = ev_dict.get('outcome') or ev_dict.get('result') or ev_dict.get('status')
        if outcome is not None:
            content['outcome'] = outcome
            metadata['final_status'] = outcome

        # Include raw event payload for traceability
        content['raw_event'] = ev_dict

        evidence = Evidence(
            evidence_id=f"{traj_id}-e{idx}",
            source='mini-swe',
            type=str(ev_type),
            timestamp=ts,
            metadata=metadata,
            content=content,
            confidence=0.9,
        )
        evidences.append(evidence)

    # Add a summary evidence
    summary_metadata: Dict[str, Any] = {}
    summary_content: Dict[str, Any] = {}
    if first_ts:
        summary_content['first_timestamp'] = first_ts.isoformat()
    if last_ts:
        summary_content['last_timestamp'] = last_ts.isoformat()
    summary_content['total_token_usage'] = total_tokens

    # Infer overall outcome from data if present
    final_status = data.get('final_status') or data.get('outcome')
    if final_status is None:
        # try to find last explicit status in events
        for ev in reversed(events):
            if isinstance(ev, dict):
                s = ev.get('status') or ev.get('outcome') or ev.get('result')
                if s is not None:
                    final_status = s
                    break

    if final_status is not None:
        summary_content['outcome'] = final_status
        summary_metadata['final_status'] = final_status

    summary_ev = Evidence(
        evidence_id=f"{traj_id}-summary",
        source='mini-swe',
        type='trajectory_summary',
        timestamp=last_ts or datetime.utcnow(),
        metadata=summary_metadata,
        content=summary_content,
        confidence=0.95,
    )
    evidences.append(summary_ev)

    return evidences


# Convenience: parse from a loaded JSON dict
def parse_mini_swe_trajectory_dict(data: Dict[str, Any], base_id: str = None) -> List[Evidence]:
    tmp_path = None
    if base_id is not None:
        # write to a temporary file path isn't necessary; reuse logic by constructing dict similar to file loader
        data_copy = data.copy()
        if 'instance_id' not in data_copy and base_id:
            data_copy['instance_id'] = base_id
        # emulate file-based flow
        # here we just use the same in-memory data
    # reuse code paths by writing a small wrapper: but simpler to implement directly
    events = data.get('events') or data.get('steps') or data.get('trajectory') or []
    # build minimal compat object and call parse_mini_swe_trajectory via a temporary file would be heavy; instead duplicate simple logic
    # For tests use parse_mini_swe_trajectory by writing a temp file; keeping this function minimal for completeness
    raise NotImplementedError("Use parse_mini_swe_trajectory with a file path for now")
