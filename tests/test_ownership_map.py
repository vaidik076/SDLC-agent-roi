from ownership.ownership_map import map_root_cause_to_owner, load_ownership_map


def test_load_default_map():
    mapping = load_ownership_map()
    assert "mappings" in mapping
    assert "default_owner" in mapping


def test_map_known_root_cause():
    out = map_root_cause_to_owner('test_failure_loop')
    assert out['owner'] == 'QA Engineering'
    assert out['priority'] == 'High'


def test_map_unknown_root_cause_uses_default():
    out = map_root_cause_to_owner('some_weird_label')
    assert out['owner'] == 'Platform Engineering'


def test_map_repo_heuristic():
    trace = {"trace": {"repo_path": "/workspace/services/payments"}}
    out = map_root_cause_to_owner('unknown_label', trace=trace)
    assert out['owner'] == 'Dev Team' or out['owner'] == 'Platform Engineering'
