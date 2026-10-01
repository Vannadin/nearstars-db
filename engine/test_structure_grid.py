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

# 덧붙임 50 — 받을 답 없는 구간: 안에서는 높은 T 쪽 끝(t₊)의 값 · 종류 «gap», 밖은 보간 그대로(합성 표)
_row = lambda v: {k: float(v) for k in sg.FIELDS}
_syn = sg.Grid({"t_pot": [1000.0, 1010.0, 1010.5, 1020.0], "points": [_row(1), _row(2), _row(3), _row(4)],
                "t_ok": None, "no_answer": [[1010.0, 1010.5, "합성"]]})
kind, got = _syn.at(1010.2)
check("받을 답 없는 구간 안 → gap · 높은 T 끝 값", kind == "gap" and all(got[k] == 3.0 for k in sg.FIELDS), f"{kind} {got and got['r_b']}")
kind, got = _syn.at(1005.0)
check("구간 밖 → 보간 그대로", kind == "ok" and all(got[k] == 1.5 for k in sg.FIELDS), f"{kind} {got and got['r_b']}")
kind, got = _syn.at(1010.5)
check("구간 끝점 t₊ → 그 점의 값(ok)", kind == "ok" and all(got[k] == 3.0 for k in sg.FIELDS), kind)

# 덧붙임 55 — 이분을 판 단위로 미리 풀기: 풀 크기와 무관한 바이트 · 버린 점은 캐시 밖 · 음성 대조 둘(가짜 풀이)
import contextlib   # noqa: E402
import io           # noqa: E402
import types        # noqa: E402


def _fake(t, p_hint=None):
    """1002.8–1003.4 K 는 받을 답 아님(겉 False) · 값이 힌트를 작은 항으로 탄다(힌트 규칙이 바이트에 보이게)."""
    x = t - 1000.0
    bad = 1002.8 < t < 1003.4
    v = {"radius": 1.0 + 1e-6 * x * x, "core_radius": 0.5, "cmb_pressure": 20.0 + 0.01 * x + 1e-15 * (p_hint or 0.0),
         "cmb_temperature": 1.5 * t, "core_pressure": 30.0 + 0.001 * x, "converged": None}
    return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=not bad, notes=(),
                                 inputs={"core_mass_fraction": 0.3}, values=v)


def _build(pool, levels=2, rounds=None):
    sg.GRID_POOL, sg.SPEC_LEVELS = pool, levels
    real = sg._spec_rounds
    if rounds is not None:
        sg._spec_rounds = rounds
    try:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            got = sg._adaptive("fake", _fake, 1000.0, 1008.0, sg.EPS, 6.4e23, 0.3)
        return json.dumps(got), out.getvalue(), None
    except SystemExit as e:
        return None, "", str(e)
    finally:
        sg._spec_rounds = real


def _leaky(chains, fetch):
    """N1 — 보낸 마디를 곧바로 찾아(사슬 사본의 결정으로) 캐시에 넣는 판 — ④ 위반."""
    chosen = set()
    while any(c.live() for c in chains):
        nodes, owner = [], []
        for c in chains:
            if not c.live():
                continue
            level = [(c.x, c.y, None)]
            for _ in range(sg.SPEC_LEVELS):
                nxt = []
                for a, b, parent in level:
                    if b - a <= c.width:
                        continue
                    m = 0.5 * (a + b)
                    nodes.append((m, a, b, parent))
                    owner.append((c, m, a, b))
                    nxt += [(a, m, m), (m, b, m)]
                level = nxt
        fetch(nodes)
        for c, m, a, b in owner:
            tmp = copy.copy(c)
            tmp.x, tmp.y = a, b
            c.step(tmp, m)
        for c in chains:
            for _ in range(sg.SPEC_LEVELS):
                if not c.live():
                    break
                m = 0.5 * (c.x + c.y)
                chosen.add(m)
                c.step(c, m)
    return chosen


_levels0, _pool0 = sg.SPEC_LEVELS, sg.GRID_POOL
b1, log1, e1 = _build(1)
b3, log3, e3 = _build(3)
check("덧붙임 55 — 풀 1 · 풀 3 바이트 같음 · 받을 답 없는 구간 있음", e1 is None and b1 == b3
      and json.loads(b1)[-1] != [], (e1 or e3 or "")[:120])
_disc = [int(w.split()[1]) for w in log1.split("·") if w.strip().startswith("버림")]
check("덧붙임 55 — 버린 미리 풀기 > 0", bool(_disc) and _disc[0] > 0, str(_disc))
bn2a, _, _ = _build(1, levels=1)
bn2b, _, _ = _build(3, levels=2)
# 덧붙임 57 ① — 표가 힌트를 버려 판 깊이는 벽시계만 바꾼다: 옛 음성 N2(힌트로 갈림)는 이제 같아야 한다
check("덧붙임 57 ① — 판 깊이 1 · 2, 풀 1 · 3 바이트 같음(힌트 없음)", bn2a is not None and bn2a == bn2b)
bn1, _, en1 = _build(3, rounds=_leaky)
check("덧붙임 55 음성 N1 — 찾기 전 캐시에 넣으면 ④ 대조가 떨어진다", bn1 is None and "덧붙임 55 ④" in (en1 or ""), (en1 or "")[:120])
sg.SPEC_LEVELS, sg.GRID_POOL = _levels0, _pool0

# 덧붙임 57 — 경로와 무관한 판정: 힌트 없으면 두 가족을 오가다 거절, 힌트가 있으면 답인 점(2074 꼴) · 음성 대조
import interior     # noqa: E402

F1, F2 = (8.0, 17.0), (6.5, 15.4)


def _fake57(t, p_hint=None):
    bad = 2074.5 < t < 2077.5
    entry = interior._ENTRY[0]
    if bad and p_hint is None and entry is None:
        trail = {"trials": [(F1, 3200.0, 3.9e10, 0), (F2, 3201.0, 3.8e10, 0)], "reclosed": [F1, F2], "closed": [],
                 "answer": F2, "dev": 3e-3, "calls": 1, "returned": {}, "answer_call": 0}
        conv, notes = False, (interior.FAMILY_OSCILLATION_NOTE + " — 가짜",)
    else:
        trail = {"trials": [(F1, 3200.0, 3.9e10, 0)], "reclosed": [], "closed": [], "answer": F1, "dev": 1e-4,
                 "calls": 1, "returned": {}, "answer_call": 0}
        conv, notes = True, ()
    interior._FAMILY_TRAIL.update(trail)
    x = t - 2066.0
    v = {"radius": 0.53 + 1e-6 * x, "core_radius": 0.28, "cmb_pressure": 19.0 + 0.01 * x + 1e-15 * (p_hint or 0.0),
         "cmb_temperature": 1.5 * t, "core_pressure": 39.4 + 0.001 * x, "converged": None}
    return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=conv, notes=notes,
                                 inputs={"core_mass_fraction": 0.3}, values=v)


def _rows57(order, pool, hinted=False):
    sg.GRID_POOL = pool
    aux, rows, prev = {}, {}, None
    with contextlib.redirect_stdout(io.StringIO()):
        for t in order:
            r = sg._pool_solve(_fake57, [(t, prev if hinted else None)], aux)[0]
            prev = r.values.get("core_pressure", 0.0) * 1e9
            rows[t] = (interior.answer_verdict(r), sorted(r.values.items()))
    return json.dumps(sorted(rows.items()))


_ts57 = [float(t) for t in range(2070, 2082)]
r_up, r_down = _rows57(_ts57, 1), _rows57(_ts57[::-1], 1)
r_hint, r_pool = _rows57(_ts57, 1, hinted=True), _rows57(_ts57, 3)
check("덧붙임 57 — 오름 · 내림 · 힌트 · 풀 3 판정 줄 바이트 같음", r_up == r_down == r_hint == r_pool)
check("덧붙임 57 — 힌트 없으면 거절될 점이 고정 출발 셋으로 답(2075 꼴)", json.loads(r_up)[5][1][0] is None, str(json.loads(r_up)[5][:1]))
_raw0 = sg._solve_raw
_last = {"p": None}


def _leaky57(solve, jobs):
    """음성 — 빌드 순서의 직전 중심압을 a 멤버에 흘림(규칙 ① 위반)."""
    out = []
    for t, h, e in jobs:
        r = _raw0(solve, [(t, h if h is not None else (_last["p"] if e is None else None), e)])[0]
        _last["p"] = r.values.get("core_pressure", 0.0) * 1e9 if interior.answer_verdict(r) is None else _last["p"]
        out.append(r)
    return out


sg._solve_raw = _leaky57
try:
    n_up, n_down = _rows57(_ts57, 1), _rows57(_ts57[::-1], 1)
finally:
    sg._solve_raw = _raw0
check("덧붙임 57 음성 — 힌트가 a 멤버에 새면 오름 · 내림이 갈린다", n_up != n_down)

# 덧붙임 58 — ② 정착 창: 초반에만 헤맨 풀이는 안 섬(음성: 옛 «모든 시행» 은 섬) · ① 용융 상태가 바뀌면 0.25 K 까지 쪼갬
_wander = types.SimpleNamespace(applicable=True, converged=True, notes=(), values={}, reason=None,
                                trail={"trials": [(F2, 3100.0, 3.8e10, 0), (None, 3150.0, 3.8e10, 0)]
                                       + [(F1, 3200.0 + i, 3.9e10, 1) for i in range(5)],
                                       "answer_call": 1, "calls": 2})
_all = []
for f, *_ in _wander.trail["trials"]:
    if all(interior._family_jump(o, f) for o in _all):
        _all.append(f)
check("덧붙임 58 ② — 초반에만 헤맨 풀이는 가족 검사가 안 섬", not sg._fires(_wander))
check("덧붙임 58 ② 음성 — 같은 풀이를 옛 «모든 시행» 으로 세면 선다", len(_all) >= 2, str(len(_all)))
_raised = types.SimpleNamespace(applicable=False, converged=None, notes=(), values={}, reason="거절 — 가짜",
                                trail={"trials": [(F1, 3200.0, 3.9e10, 0), (F2, 3300.0, 3.8e10, 0)], "answer_call": None,
                                       "calls": 2})
check("덧붙임 58 노트 — 첫 시행 전에 거절한 호출은 창 없음(앞 호출을 안 빌림)", sg._settled_trials(_raised) == [])


def _fake58(t, p_hint=None):
    """1005.3 K 위에서 바닥 층이 부분 용융 — 값은 매끄러워 보간은 ε 안."""
    interior._FAMILY_TRAIL.update(trials=[(None, 3000.0, 3e10, 0)], reclosed=[], closed=[], answer=None, dev=1e-4,
                                  calls=1, returned={}, answer_call=0)
    x = t - 1000.0
    v = {"radius": 1.0 + 1e-7 * x, "core_radius": 0.5, "cmb_pressure": 20.0 + 0.001 * x, "cmb_temperature": 1.5 * t,
         "core_pressure": 30.0, "converged": None, "silicate_melt_state": "molten",
         "basal_silicate_state": "partial-melt" if t > 1005.3 else "solid"}
    return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=True, notes=(),
                                 inputs={"core_mass_fraction": 0.3}, values=v)




def _fake59(t, p_hint=None):
    """1003 K(시작 구간 [1002, 1004] 의 가운데)에서만 정착 창에 가족 둘 — 답은 한 가족, 값은 매끄러움."""
    hot = abs(t - 1003.0) < 1e-9 and p_hint is None and interior._ENTRY[0] is None
    tr = [(F1, 3200.0, 3.9e10, 0), (F2, 3201.0, 3.8e10, 0)] * 2 if hot else [(F1, 3200.0, 3.9e10, 0)]
    interior._FAMILY_TRAIL.update(trials=tr, reclosed=[F1, F2] if hot else [], closed=[], answer=F1, dev=1e-4,
                                  calls=1, returned={}, answer_call=0)
    x = t - 1000.0
    v = {"radius": 1.0 + 1e-7 * x, "core_radius": 0.5, "cmb_pressure": 20.0 + 0.001 * x, "cmb_temperature": 1.5 * t,
         "core_pressure": 30.0, "converged": None, "silicate_melt_state": "solid", "basal_silicate_state": "solid"}
    return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=True, notes=(),
                                 inputs={"core_mass_fraction": 0.3}, values=v)


def _build59(levels=2):
    sg.GRID_POOL, sg.SPEC_LEVELS = 1, levels
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return json.dumps(sg._adaptive("fake", _fake59, 1000.0, 1008.0, sg.EPS, 6.4e23, 0.3)), None
    except SystemExit as e:
        return None, str(e)


_b59, _e59 = _build59()
_pts59 = json.loads(_b59)[0] if _b59 else []
check("덧붙임 59 ② — 가운데 점에서만 선 가족 검사도 그 구간을 1 K 까지 쪼갬(1003 이 표 점)", 1003.0 in _pts59, (_e59 or str(_pts59))[:120])
_hold0 = sg._holds_fire
sg._holds_fire = lambda a, b, fs: a in fs or b in fs        # 음성 — 덧붙임 58 의 끝점 판
try:
    _bn59, _en59 = _build59()
finally:
    sg._holds_fire = _hold0
check("덧붙임 59 음성 — 끝점 판이면 같은 가짜에서 구간이 닫혀 끝 점검이 이름 대고 거절", _bn59 is None and "덧붙임 59 ④" in (_en59 or ""),
      (_en59 or "")[:120])
check("덧붙임 59 ① — 미리 풀기 깊이 1 · 2 바이트 같음(버린 미리 풀기는 F 밖)", _build59(1)[0] == _build59(2)[0] == _b59)

sg.GRID_POOL = 1
try:
    with contextlib.redirect_stdout(io.StringIO()):
        _g58 = sg._adaptive("fake", _fake58, 1000.0, 1008.0, sg.EPS, 6.4e23, 0.3)
    _near = [t for t in _g58[0] if abs(t - 1005.3) <= 0.25]
    check("덧붙임 58 ① — 용융 상태가 바뀌는 구간을 거절 없이 0.25 K 까지 쪼갬", len(_near) >= 1, str(_near))
except SystemExit as e:
    check("덧붙임 58 ① — 용융 상태가 바뀌는 구간을 거절 없이 0.25 K 까지 쪼갬", False, str(e)[:120])
sg.SPEC_LEVELS, sg.GRID_POOL = _levels0, _pool0
sg.SPEC_LEVELS, sg.GRID_POOL = _levels0, _pool0

ghost = copy.deepcopy(run.load_body(sg.BODIES_DIR / "earth.yaml")[0])
ghost.name = "NoSuchBody"
_, why = sg.load_for(ghost)
check("표가 없는 바디 → 이름 대고 거절", why is not None and "구조 표가 없다" in why, (why or "")[:100])

print(f"  test_structure_grid — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
