# 노드 실행 id — 명세의 물리 투영 · 코드 blob · 위쪽 run id · 읽은 출처·기록 해시 · 천체 바이트 · 옵션을 묶는 해시 (계약 §6)
"""The run id of one node run (contract `node-contract.frozen.md` §6). No clock, no hand-bumped version.

    run_id = sha256(canonical({projection, code blobs, upstream run ids, override records, held-source sha256s,
                               DB record entry sha256s, body bytes, options}))

The physics projection keeps only the spec keys that can change a value, so adding a consumer to a producer's `to`
(the both-ends rule), or editing a label, test list or check, leaves the run id where it was (prereg N6 (a)).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

#: Spec keys that can change a value (contract §6). Everything else is excluded.
PROJECTED_TOP = ("id", "kind", "inputs", "host_combine", "selects", "reads", "domain", "refusals", "iterate")
PROJECTED_OUTPUT = ("quantity", "unit", "kind", "method_grade")
PROJECTED_SOURCE = ("cache", "sha256", "page", "formula", "identity", "user_declared", "library", "doi")
REPO = Path(__file__).resolve().parent.parent


def canonical_bytes(x) -> bytes:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode()


def entry_sha256(entry) -> str:
    """sha256 of one DB record entry's canonical bytes: an edit elsewhere in the file does not move it (§4.2)."""
    return hashlib.sha256(canonical_bytes(entry)).hexdigest()


def git_blob_id(path) -> str:
    """The git blob id of a file, computed the way `git hash-object` does (no subprocess)."""
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def projection(spec: dict) -> dict:
    out = {k: spec[k] for k in PROJECTED_TOP if k in spec}
    out["outputs"] = {k: {f: o[f] for f in PROJECTED_OUTPUT} for k, o in spec["outputs"].items()}
    out["sources"] = [{f: s[f] for f in PROJECTED_SOURCE if f in s} for s in spec["sources"] if "to_fetch" not in s]
    return out


def code_blobs(spec: dict, repo: Path = REPO) -> dict:
    """The spec's code files plus the solver types every node imports (prereg §1, C2)."""
    paths = list(spec["code"]) + ["solver/result.py", "solver/refusals.py", "nodes/types.py", "nodes/runner.py"]
    return {p: git_blob_id(repo / p) for p in sorted(set(paths))}


def run_id(spec: dict, *, upstream: dict, records: dict, body: dict, options: dict | None = None,
           overrides: tuple = (), repo: Path = REPO) -> str:
    """`upstream`: input key -> producing run id(s); `records`: record key -> entry sha256."""
    payload = {
        "projection": projection(spec),
        "code": code_blobs(spec, repo),
        "upstream": upstream,
        "overrides": [hashlib.sha256(canonical_bytes(o)).hexdigest() for o in overrides],
        "records": records,
        "body": body,
        "options": options or {},
    }
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()
