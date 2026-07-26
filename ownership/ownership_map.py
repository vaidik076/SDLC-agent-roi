import json
from typing import Dict, Any, Optional
import os

DEFAULT_MAP_PATH = os.path.join(os.path.dirname(__file__), "default_map.json")


def load_ownership_map(path: Optional[str] = None) -> Dict[str, Any]:
    p = path or DEFAULT_MAP_PATH
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Return minimal default when loading fails
        return {
            "mappings": {},
            "default_owner": {"owner": "Platform Engineering", "contact": "platform-eng@example.com", "priority": "Medium", "rationale": "Default owner."}
        }


def map_root_cause_to_owner(root_cause: str, trace: Optional[Dict[str, Any]] = None, ownership_map: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Map a root cause label to an owning team entry.

    Args:
        root_cause: root cause label (from RCA)
        trace: optional trace dict for additional heuristics (repo/component)
        ownership_map: optional pre-loaded mapping dict (overrides default file)

    Returns:
        dict with keys: owner, contact, priority, rationale, mapped_name
    """
    mapping = ownership_map or load_ownership_map()
    maps = mapping.get("mappings", {})
    default = mapping.get("default_owner", {"owner": "Platform Engineering", "contact": "platform-eng@example.com", "priority": "Medium", "rationale": "Default owner."})

    entry = maps.get(root_cause)

    # Heuristic: if trace specifies a repo name, map certain repos to Dev Team
    if not entry and trace and isinstance(trace, dict):
        repo = trace.get("repo") or trace.get("trace", {}).get("repo_path")
        if repo and "/services/" in str(repo):
            return {**{"mapped_name": root_cause}, **{"owner": "Dev Team", "contact": "dev-team@example.com", "priority": "High", "rationale": f"Repo-specific: {repo}"}}

    if entry:
        return {**{"mapped_name": root_cause}, **entry}

    # Fallback
    return {**{"mapped_name": root_cause}, **default}
