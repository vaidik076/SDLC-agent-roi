import os
from ingest.adapters.git_adapter import get_commits


def test_get_commits_smoke():
    """Smoke test: fetch a small number of commits from the current repo root.

    This test does not assert on exact commit content because the local repo
    will vary; it only validates the adapter returns Evidence-like records.
    """
    repo_root = os.getcwd()
    commits = get_commits(repo_root, max_count=5)
    assert isinstance(commits, list)
    # If the repo has at least one commit, ensure structure looks correct
    if commits:
        first = commits[0]
        assert getattr(first, 'evidence_id', None)
        assert getattr(first, 'source', None) == 'git'
        assert getattr(first, 'type', None) == 'commit'
