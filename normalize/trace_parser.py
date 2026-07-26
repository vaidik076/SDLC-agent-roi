"""Trace parser: normalize a list of Evidence records into a canonical Trace model.

This parser is intentionally conservative and rules-based so it works with
heterogeneous evidence inputs. It sums token usage where available, infers
latency from timestamps when explicit latency fields are absent, counts retry
like events, and detects human intervention through metadata flags or evidence
types.
"""
from typing import List
import datetime

from models.evidence import Evidence
from models.trace import Trace


def parse_trace_from_evidence(task_id: str, evidences: List[Evidence]) -> Trace:
    if not evidences:
        return Trace(task_id=task_id, resolved=False)

    # Sort evidences by timestamp
    sorted_e = sorted(evidences, key=lambda e: e.timestamp)

    first_ts = sorted_e[0].timestamp
    last_ts = sorted_e[-1].timestamp
    latency_seconds = (last_ts - first_ts).total_seconds()

    token_usage = 0
    retries = 0
    human_intervention = False
    tool_calls = []
    raw_refs = []

    resolved = False

    for ev in sorted_e:
        raw_refs.append(ev.evidence_id)
        # token usage may appear in content under a few possible keys
        t = ev.content.get('token_usage') if isinstance(ev.content, dict) else None
        if t is None:
            # try nested llm usage
            t = ev.content.get('llm', {}).get('token_usage') if isinstance(ev.content.get('llm'), dict) else None
        if isinstance(t, (int, float)):
            token_usage += int(t)

        # retries: look for explicit 'retry' type or metadata flags
        if ev.type.lower() in ('retry', 'attempt'):
            retries += 1
        if ev.metadata.get('retry'):
            try:
                retries += int(ev.metadata.get('retry'))
            except Exception:
                retries += 1

        # human intervention heuristics
        if ev.type.lower() in ('human_review', 'manual_intervention'):
            human_intervention = True

        if ev.metadata.get('human') in (True, 'true', 'True'):
            human_intervention = True

        # tool calls
        calls = ev.content.get('tool_calls')
        if isinstance(calls, list):
            tool_calls.extend(calls)

        # resolved: look for test_result evidence or final status
        if ev.type.lower() in ('test_result', 'test'):
            status = ev.content.get('status') or ev.metadata.get('status')
            if isinstance(status, str) and status.lower() in ('pass', 'passed', 'ok'):
                resolved = True
        if ev.metadata.get('final_status') in ('pass', 'passed', 'ok'):
            resolved = True

    # A weaker heuristic: if there is an explicit `passed` LLM run in content
    for ev in sorted_e[::-1]:
        # some traces embed final outcome in content under 'outcome' or 'result'
        outcome = ev.content.get('outcome') or ev.content.get('result')
        if isinstance(outcome, str) and outcome.lower() in ('pass', 'passed', 'ok'):
            resolved = True
            break

    trace = Trace(
        task_id=task_id,
        resolved=bool(resolved),
        retries=int(retries),
        token_usage=int(token_usage),
        latency_seconds=float(latency_seconds),
        human_intervention=bool(human_intervention),
        tool_calls=tool_calls,
        raw_evidence_refs=raw_refs,
        first_timestamp=first_ts,
        last_timestamp=last_ts,
    )

    return trace
