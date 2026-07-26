"""Lightweight Git adapter that converts local commit history into Evidence records.

This adapter uses the `git` CLI to avoid adding extra Python runtime dependencies.
It returns a list of models.evidence.Evidence instances so the rest of the
pipeline can treat all inputs uniformly.
"""
from typing import List
import subprocess
import datetime
import os

from models.evidence import Evidence


def get_commits(repo_path: str, max_count: int = 100) -> List[Evidence]:
    """Return recent commits from repo_path as a list of Evidence objects.

    Args:
        repo_path: Path to the git repository.
        max_count: Maximum number of commits to return.

    Returns:
        List[Evidence]
    """
    # Use a compact, machine-friendly pretty format: fields separated by US (Unit Separator) and RS (Record Separator)
    fmt = r"%H%x1f%an%x1f%ae%x1f%ad%x1f%s%x1e"
    cmd = ["git", "-C", repo_path, "log", f"--max-count={max_count}", "--pretty=format:" + fmt, "--date=iso"]

    try:
        out = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return []

    commits: List[Evidence] = []
    if not out.strip():
        return commits

    for rec in out.split('\x1e'):
        rec = rec.strip()
        if not rec:
            continue
        parts = rec.split('\x1f')
        if len(parts) < 5:
            continue
        sha, author, email, date_str, subject = parts[:5]
        try:
            ts = datetime.datetime.fromisoformat(date_str)
        except Exception:
            # Fallback if the date parsing fails
            ts = datetime.datetime.utcnow()

        ev = Evidence(
            evidence_id=sha,
            source="git",
            type="commit",
            timestamp=ts,
            metadata={
                "author": author,
                "email": email,
                "subject": subject,
            },
            content={
                "repo_path": os.path.abspath(repo_path),
            },
            confidence=1.0,
        )
        commits.append(ev)

    return commits
