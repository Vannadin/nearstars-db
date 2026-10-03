# C159 — 구조 표 짓기가 실제로 여는 파일과 읽는 chain.yaml 칸을 기록해, 방아쇠 밖 데이터 읽기를 멈춤으로 센다
"""python3 engine/tools/table_reads_guard.py [body ...] [--n N]   (기본: 열진화 입력을 선언한 출하 몸 전부, N = 2)

prereg-c159-table-trigger-reads (e0ab5682) §1 and rule 1b. For each body, a small uniform build (`structure_grid.build(name, n=N)`)
runs into a scratch `STRUCTURE_GRID_DIR`, with
- an audit hook on `open` recording every file read under `engine/`;
- `graph.load()` returning access-recording mappings, recording every chain.yaml key path the runner reads.
Every data file read anywhere (repository root and outside it; Python and system paths aside) must be a byte trigger (`structure_grid.BYTE_FILES`) or on `structure_grid.FILE_EXEMPT`, and every chain
key read must lie inside `structure_grid.CHAIN_READS`. Anything else is printed as a stop and the exit code is 1.
A build that refuses is reported with its reason; the reads up to the refusal are still checked.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
os.environ["STRUCTURE_GRID_DIR"] = tempfile.mkdtemp(prefix="c159_guard_")
sys.path.insert(0, str(ENGINE))

import structure_grid as _sg  # noqa: E402  (stdlib-only at import; the hook is added before the engine loads)

opened = _sg._READS             # C159 메모 1 — 저장소 전체 · 밖(환경 변수 역할)까지, structure_grid 의 훅과 같은 규칙
_hook = _sg._reads_hook


class _Rec(dict):
    """읽힌 키 경로를 남기는 dict. 노드 이름 자리는 `nodes.*` 로, 간선 목록은 `root.edges[]` 로 접는다."""

    def __init__(self, d, path, log):
        super().__init__(d)
        self._path, self._log = path, log

    def _child(self, k):
        return "nodes.*" if self._path == "root.nodes" else f"{self._path}.{k}"

    def _note(self, k):
        self._log.add("nodes.*" if self._path == "root.nodes" else f"{self._path}.{k}")

    def _wrap(self, k, v):
        sub = self._child(k)
        if isinstance(v, dict):
            return _Rec(v, sub, self._log)
        if isinstance(v, list):
            return [(_Rec(x, sub + "[]", self._log) if isinstance(x, dict) else x) for x in v]
        return v

    def __getitem__(self, k):
        self._note(k)
        return self._wrap(k, super().__getitem__(k))

    def get(self, k, default=None):
        self._note(k)
        return self._wrap(k, super().get(k)) if k in self else default

    def items(self):
        for k in self:
            self._note(k)
        return [(k, self._wrap(k, dict.__getitem__(self, k))) for k in self]

    def values(self):
        return [v for _k, v in self.items()]


def _allowed_chain(path: str) -> bool:
    import structure_grid as sg
    parts = path.split(".")
    if path in ("root.nodes", "root.edges", "root.coupled_core", "nodes.*"):
        return True
    if parts[:2] == ["nodes", "*"] and len(parts) == 3:
        return parts[2] in sg.CHAIN_READS["node"]
    if parts[:2] == ["root", "edges[]"] and len(parts) == 3:
        return parts[2] in sg.CHAIN_READS["edge"]
    if parts[:2] == ["root", "coupled_core"] and len(parts) == 3:
        return parts[2] in sg.CHAIN_READS["coupled_core"]
    return False


def guard(name: str, n: int) -> int:
    import graph
    import structure_grid as sg
    keys: set[str] = set()
    real = graph.load
    graph.load = lambda: _Rec(real(), "root", keys)
    opened.clear()
    status = "built"
    try:
        sg.build(name, n=n)
    except SystemExit as e:
        status = f"refused: {str(e)[:160]}"
    except Exception as e:                       # noqa: BLE001 — a crash is reported, not hidden
        status = f"error {type(e).__name__}: {str(e)[:160]}"
    finally:
        graph.load = real
    data = sorted(opened)
    bad = sg.guard_reads(opened)
    bad_keys = sorted(k for k in keys if not _allowed_chain(k))
    print(f"== {name} · {status}")
    print(f"   data files read: {data}")
    print(f"   chain keys read: {sorted(keys)}")
    for f in bad:
        print(f"   [STOP] data file read outside the triggers and the exemption list: {f}")
    for k in bad_keys:
        print(f"   [STOP] chain key read outside CHAIN_READS: {k}")
    if not bad and not bad_keys:
        print("   [PASS] every data read is a trigger or exempt; every chain key is in the projection")
    return 1 if (bad or bad_keys) else 0


def main(argv: list[str]) -> int:
    import structure_grid as sg
    n = 2
    if "--n" in argv:
        i = argv.index("--n")
        n = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    sys.addaudithook(_hook)
    names = argv or sg.history_bodies()
    return 1 if sum(guard(nm, n) for nm in names) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
