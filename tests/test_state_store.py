import os
import json
from pathlib import Path

from py_containerd.state.store import JsonStateStore


def test_json_state_store_put_get_delete(tmp_path: Path) -> None:
    store = JsonStateStore(str(tmp_path))
    ns = "default"
    key = "abc"
    value = {"x": 1, "y": "z"}

    # get missing
    assert store.get(ns, key) is None

    # put
    store.put(ns, key, value)
    p = tmp_path / ns / f"{key}.json"
    assert p.exists()

    # get existing
    read = store.get(ns, key)
    assert read == value

    # delete
    store.delete(ns, key)
    assert store.get(ns, key) is None
    assert not p.exists()