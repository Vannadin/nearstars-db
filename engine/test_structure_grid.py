# 구조 표(structure_grid) 시험 — 굳힌 표의 방아쇠 · 거절 문구 · 보간 (풀이 없음, 가볍다)
"""prereg-structure-grid 덧붙임 7 ⑥ 의 가벼운 쪽.

    python3 engine/test_structure_grid.py

① 굳힌 표마다 방아쇠가 그대로다 (`--check` 와 같은 대조).
② 거절 넷 — 격자 아래 · 격자 위(구조가 풀리는 표) · 방아쇠 움직임 · 표 없음.
③ 보간 — 격자 점에서 그 점의 값을 비트로 돌려주고, 두 점 사이는 두 값 사이에 있다.
④ «못 봄» — T_ok 가 있는 표는 위 끝 밖에서 붙든다.
무거운 쪽(노드 출력이 연구판 ⓑ 와 등록 폭 안인가)은 착지 전 한 번, 스크래치에서 — 결과는 사전등록 덧붙임에.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run                             # noqa: E402
import structure_grid as sg            # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


tables = sorted(sg.GRID_DIR.glob("*.json"))
check("굳힌 표가 있다", bool(tables), ", ".join(p.name for p in tables))
for path in tables:
    doc = json.loads(path.read_text(encoding="utf-8"))
    body, _ = run.load_body(sg.BODIES_DIR / f"{doc['body'].lower()}.yaml")
    grid, why = sg.load_for(body)
    check(f"{path.name} — 방아쇠 그대로", why is None, why or f"격자 {doc['t_pot'][0]:.1f}–{doc['t_pot'][-1]:.1f} K · T_ok {doc['t_ok']}")
    if grid is None:
        continue
    kind, got = grid.at(grid.t[0] - 1.0)
    check(f"{path.name} — 격자 아래 거절", kind == "refused" and "격자 아래" in got, got if kind == "refused" else kind)
    kind, got = grid.at(grid.t[-1] + 1.0)
    if doc["t_ok"] is None:
        check(f"{path.name} — 격자 위 거절(구조가 풀리는 표)", kind == "refused" and "격자 위" in got, str(got))
    else:
        check(f"{path.name} — 격자 위 붙들기(T_ok {doc['t_ok']!r})", kind == "hold", kind)
    kind, got = grid.at(grid.t[3])
    check(f"{path.name} — 격자 점에서 그 점의 값(비트)", kind == "ok" and all(got[k] == grid.rows[3][k] for k in sg.FIELDS))
    mid = 0.5 * (grid.t[3] + grid.t[4])
    kind, got = grid.at(mid)
    check(f"{path.name} — 두 점 사이는 두 값 사이", kind == "ok" and all(
        min(grid.rows[3][k], grid.rows[4][k]) <= got[k] <= max(grid.rows[3][k], grid.rows[4][k]) for k in sg.FIELDS))
    moved = copy.deepcopy(body)
    moved.inputs["potential_temperature"] = float(moved.inputs["potential_temperature"]) + 1.0
    _, why = sg.load_for(moved)
    check(f"{path.name} — 선언이 움직이면 낡은 표로 거절", why is not None and "potential_temperature" in why, (why or "")[:100])

ghost = copy.deepcopy(run.load_body(sg.BODIES_DIR / "earth.yaml")[0])
ghost.name = "NoSuchBody"
_, why = sg.load_for(ghost)
check("표가 없는 바디 → 이름 대고 거절", why is not None and "구조 표가 없다" in why, (why or "")[:100])

print(f"  test_structure_grid — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
