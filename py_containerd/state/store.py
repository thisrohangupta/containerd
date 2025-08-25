import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class JsonStateStore:
    def __init__(self, root_dir: str) -> None:
        self.root = Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, ns: str, key: str) -> Path:
        return self.root / ns / f"{key}.json"

    def get(self, ns: str, key: str) -> Optional[Dict[str, Any]]:
        p = self._path(ns, key)
        if not p.exists():
            return None
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

    def put(self, ns: str, key: str, value: Dict[str, Any]) -> None:
        p = self._path(ns, key)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(value, f)
        os.replace(tmp, p)

    def delete(self, ns: str, key: str) -> None:
        p = self._path(ns, key)
        if p.exists():
            p.unlink()

