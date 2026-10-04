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
        trail = {"trials": [(F1, 3200.0, 3.9e10, 0, None, True), (F2, 3201.0, 3.8e10, 0, None, True)], "reclosed": [F1, F2], "closed": [],
                 "answer": F2, "dev": 3e-3, "calls": 1, "returned": {}, "answer_call": 0}
        conv, notes = False, (interior.FAMILY_OSCILLATION_NOTE + " — 가짜",)
    else:
        trail = {"trials": [(F1, 3200.0, 3.9e10, 0, None, True)], "reclosed": [], "closed": [], "answer": F1, "dev": 1e-4,
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
                                trail={"trials": [(F2, 3100.0, 3.8e10, 0, None, True), (None, 3150.0, 3.8e10, 0, None, True)]
                                       + [(F1, 3200.0 + i, 3.9e10, 1, None, True) for i in range(5)],
                                       "answer_call": 1, "calls": 2})
_all = []
for f, *_ in _wander.trail["trials"]:
    if all(interior._family_jump(o, f) for o in _all):
        _all.append(f)
check("덧붙임 58 ② — 초반에만 헤맨 풀이는 가족 검사가 안 섬", not sg._fires(_wander))
check("덧붙임 58 ② 음성 — 같은 풀이를 옛 «모든 시행» 으로 세면 선다", len(_all) >= 2, str(len(_all)))
_raised = types.SimpleNamespace(applicable=False, converged=None, notes=(), values={}, reason="거절 — 가짜",
                                trail={"trials": [(F1, 3200.0, 3.9e10, 0, None, True), (F2, 3300.0, 3.8e10, 0, None, True)], "answer_call": None,
                                       "calls": 2})
check("덧붙임 58 노트 — 첫 시행 전에 거절한 호출은 창 없음(앞 호출을 안 빌림)", sg._settled_trials(_raised) == [])


def _fake58(t, p_hint=None):
    """1005.3 K 위에서 바닥 층이 부분 용융 — 값은 매끄러워 보간은 ε 안."""
    interior._FAMILY_TRAIL.update(trials=[(None, 3000.0, 3e10, 0, None, True)], reclosed=[], closed=[], answer=None, dev=1e-4,
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
    tr = [(F1, 3200.0, 3.9e10, 0, None, True), (F2, 3201.0, 3.8e10, 0, None, True)] * 2 if hot else [(F1, 3200.0, 3.9e10, 0, None, True)]
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

# C162 — 표 짓기에서 이름 댄 거절은 세는 «거절» 구간(멈춤 아님) · 상한(몸 표마다 둘 · 구간마다 2.0 K) · 음성 대조
_JUMP = "표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜)"


def _fake162(bands, why=_JUMP, cmf_at=None):
    """`bands` 안의 온도에서만 이름 댄 거절(applicable False) — 값은 _fake58 처럼 매끄러움."""
    def solve(t, p_hint=None):
        interior._FAMILY_TRAIL.update(trials=[(None, 3000.0, 3e10, 0, None, True)], reclosed=[], closed=[], answer=None,
                                      dev=1e-4, calls=1, returned={}, answer_call=0)
        hit = next((i for i, (lo, hi) in enumerate(bands) if lo <= t <= hi), None)
        if hit is not None:
            w = why[hit] if isinstance(why, (list, tuple)) else why     # C157 메모 7 — 띠마다 다른 문구
            return types.SimpleNamespace(applicable=False, converged=None, notes=(), values={}, reason=w, regime="rocky",
                                         inputs={"core_mass_fraction": 0.3})
        x = t - 1000.0
        v = {"radius": 1.0 + 1e-7 * x, "core_radius": 0.5, "cmb_pressure": 20.0 + 0.001 * x, "cmb_temperature": 1.5 * t,
             "core_pressure": 30.0, "converged": None, "silicate_melt_state": "solid", "basal_silicate_state": "solid"}
        cmf = 0.31 if cmf_at is not None and abs(t - cmf_at) < 1e-9 else 0.3
        return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=True, notes=(),
                                     inputs={"core_mass_fraction": cmf}, values=v)
    return solve


def _build162(solve):
    sg.GRID_POOL = 1
    try:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            res = sg._adaptive("fake", solve, 1000.0, 1008.0, sg.EPS, 6.4e23, 0.3)
        return res, None, out.getvalue()
    except SystemExit as e:
        return None, str(e), ""
    finally:
        sg.GRID_POOL = _pool0


_r162, _e162, _log162 = _build162(_fake162([(1002.9, 1003.1)]))
_gaps162 = _r162[8] if _r162 else []
check("C162 ① — 안쪽 한 점의 C152 거절은 멈춤 없이 «거절» 구간 하나(까닭 · 폭 ≤ 1 K)",
      len(_gaps162) == 1 and _gaps162[0][3] == "refusal" and _gaps162[0][4] is None and _gaps162[0][2].startswith("표면온도 잔차가 뛴다")
      and _gaps162[0][1] - _gaps162[0][0] <= 1.0, (_e162 or str(_gaps162))[:160])
check("C162 ① — 짓기 로그가 그 구간을 «(거절)» 로 찍음", "받을 답 없는 구간(거절)" in _log162)
if _r162:
    _g162 = sg.Grid({"t_pot": _r162[0], "points": _r162[1], "no_answer": _gaps162})
    check("C162 ① — 읽기는 그대로: 구간 안은 gap", _g162.at(1003.0)[0] == "gap", str(_g162.at(1003.0)[0]))
_, _e3, _ = _build162(_fake162([(1000.9, 1001.1), (1002.9, 1003.1), (1004.9, 1005.1)]))
check("C162 ② — 거절 구간 셋이면 상한(둘) 넘음: 구간 전부를 이름 대고 멈춤", _e3 is not None and "상한" in _e3 and _e3.count("폭") >= 3,
      (_e3 or "")[:160])
_, _ew, _ = _build162(_fake162([(1002.6, 1005.4)]))
check("C162 ② — 폭 2.0 K 넘는 거절 구간 하나면 멈춤", _ew is not None and "상한" in _ew and "> 2.0 K" in _ew, (_ew or "")[:160])
# C157 메모 5 §3.1b — 스침 표지가 붙은 거절 구간은 폭 상한만 면제(셈 · 목록 · 폭 인쇄), 표지 없는 3 K 구간은 그대로 멈춤
_GRAZE = _JUMP + " — " + interior.format_graze(6522.0, ("고상선", "silicate", 16.6e9, -0.2))   # 메모 7 규칙 4 — 형식기로
_rg, _eg, _ = _build162(_fake162([(1002.6, 1005.4)], why=_GRAZE))
_gg = _rg[8] if _rg else []
check("C157 메모 5 — 스침 표지 3 K 거절 구간은 멈추지 않음(다섯째 칸 onset_graze · 폭 3 K 그대로 기록)",
      len(_gg) == 1 and _gg[0][3:5] == ["refusal", "onset_graze"] and abs(_gg[0][1] - _gg[0][0] - 3.0) < 1e-9, (_eg or str(_gg))[:160])
check("C157 메모 5 음성 — 같은 폭의 표지 없는 구간은 멈춤(위 «C162 ② 폭» 과 같은 가짜, 표지만 뺌)", _ew is not None and "> 2.0 K" in _ew)
_, _eg3, _ = _build162(_fake162([(1000.9, 1001.1), (1002.9, 1003.1), (1004.9, 1005.1)], why=_GRAZE))
check("C157 메모 5 — 표지 구간도 개수 상한(둘)엔 셈: 셋이면 멈춤", _eg3 is not None and "3 개 > 2" in _eg3, (_eg3 or "")[:120])
check("C157 메모 5 — 문서 판: 표지 구간은 폭 사유 없음, 표지 없는 같은 폭은 사유",
      sg.refusal_over_cap([[1.0, 4.0, "x", "refusal", "onset_graze"]]) == ""
      and "폭" in sg.refusal_over_cap([[1.0, 4.0, "x", "refusal"]]))
# C157 메모 7 — 소속으로 표지: 모두 S > GRAZE_SLOPE 이고 하나라도 스침이면 구간 표지. 문구는 interior.format_graze 로만 짓는다
_STEEP = _JUMP + " — " + interior.format_graze(50.0, None)        # 가파르나 접근 없음
_FLAT = _JUMP + " — " + interior.format_graze(5.0, None)          # S < GRAZE_SLOPE
_r7, _e7, _ = _build162(_fake162([(1002.6, 1003.4), (1003.4001, 1005.4)], why=[_GRAZE, _STEEP]))
_g7 = _r7[8] if _r7 else []
check("메모 7 — 모두 S > 10 · 스침 하나 이상인 3 K 구간은 표지(폭 면제) · 여섯째 칸 셈",
      len(_g7) == 1 and _g7[0][4] == "onset_graze" and _g7[0][5]["graze_points"] >= 1
      and _g7[0][5]["graze_points"] < _g7[0][5]["points"] and _g7[0][5]["s_min"] == 50.0, (_e7 or str(_g7))[:200])
_, _e7a, _ = _build162(_fake162([(1002.6, 1003.4), (1003.4001, 1005.4)], why=[_GRAZE, _FLAT]))
check("메모 7 음성 — 거절 한 점이라도 S < GRAZE_SLOPE 면 표지 없음 → 폭 상한에 멈춤", _e7a is not None and "> 2.0 K" in _e7a, (_e7a or "")[:120])
_, _e7b, _ = _build162(_fake162([(1002.6, 1005.4)], why=_STEEP))
check("메모 7 음성 — 모두 S > 10 이어도 스침 점이 없으면 표지 없음 → 멈춤", _e7b is not None and "> 2.0 K" in _e7b, (_e7b or "")[:120])
check("메모 7 규칙 5 — 쌍이 없는(S 없는) 거절 문구는 S None", interior.parse_graze(_JUMP) == (None, None))
# 메모 7 수락 2b — 실제 풀이의 거절 문구(c157n5 571d1360 지구 표 풀이 T_pot 2081.5667288537124 K, n5-acc1.log 8ecbbbc5 에서 옮김)
_REAL_2081 = ("적분이 실패했다 — 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.41] K 사이에서 0 을 건너뛴다(괄호 폭 9.47e-07 ≤ T_TOL 1e-06, "
              "가까운 끝의 어긋남 0.28 %). 그 사이에 표면 온도가 선언값과 같아지는 해가 없다 (C152). — 경계 스침 — 고상선 · silicate "
              "16.627 GPa (T − T_경계 -0.206 K) · 민감도 S 6522 (C157 메모 5)")
_sr, _gr = interior.parse_graze(_REAL_2081)
check("메모 7 수락 2b — 실제 거절 문구를 같은 파서가 S 6522 · 16.627 GPa 스침으로 읽음", _sr == 6522.0 and _gr is not None and "16.627 GPa" in _gr,
      f"{_sr} {_gr}")
_s_rt, _g_rt = interior.parse_graze(interior.format_graze(1.578e4, ("고상선", "silicate", 16.628e9, -0.308)))
check("메모 7 규칙 4 — 형식기 → 파서 왕복(S 1.578e+04 · 스침)", _s_rt == 15780.0 and _g_rt is not None and "16.628 GPa" in _g_rt, f"{_s_rt} {_g_rt}")
check("C162 ② — 판정 구간(셋째 칸까지)은 상한에 안 셈",sg.refusal_over_cap([[1.0, 9.0, "판정"]] * 3) == "")
check("C162 ② — 문서 판: 거절 구간 셋 · 폭 넘는 하나는 상한 사유",
      "3 개" in sg.refusal_over_cap([[1.0, 1.5, "x", "refusal"]] * 3) and "폭" in sg.refusal_over_cap([[1.0, 3.5, "x", "refusal"]]))
_, _eb, _ = _build162(_fake162([(1002.9, 1003.1)], why=interior.BACKSTOP_REASON_HEAD + " (적분 피적분 불연속) — 가짜"))
check("C162 음성 — C157 뒷받침 거절은 멈춤 그대로(규칙 3)", _eb is not None and interior.BACKSTOP_REASON_HEAD in _eb, (_eb or "")[:120])
_, _el, _ = _build162(_fake162([(999.0, 1000.1)]))
check("C162 음성 — 아래 끝 거절은 멈춤(격자 끝)", _el is not None and "격자 끝" in _el, (_el or "")[:120])
_, _ec, _ = _build162(_fake162([], cmf_at=1004.0))
check("C162 음성 — cmf 어긋남은 멈춤", _ec is not None and "조성이 고정이 아니다" in _ec, (_ec or "")[:120])


def _check162(no_answer):
    """방아쇠가 지금 그대로인 가짜 earth 표 하나로 --check(check_all) 를 돌려 (FAIL 수, 출력)."""
    import tempfile
    body = run.load_body(sg.BODIES_DIR / "earth.yaml")[0]
    saved = sg.GRID_DIR
    with tempfile.TemporaryDirectory() as d:
        sg.GRID_DIR = Path(d)
        (Path(d) / "earth.json").write_text(json.dumps({"body": "Earth", "t_pot": [1.0], "points": [{}],
                                                        "triggers": sg.triggers(body.inputs), "no_answer": no_answer}),
                                            encoding="utf-8")
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                bad = sg.check_all()
        finally:
            sg.GRID_DIR = saved
    return bad, out.getvalue()


_b1, _o1 = _check162([[1002.75, 1003.25, _JUMP, "refusal"], [1005.0, 1005.5, "판정 — 가짜"]])
check("C162 ② — --check 가 구간 전부를 까닭과 찍음: 거절 [WARN] · 판정 [기록], 상한 안이면 FAIL 없음(표 없는 몸 둘만)",
      "[WARN] earth.json — 거절 구간 [1002.75, 1003.25]" in _o1 and "[기록] earth.json — 받을 답 없는 구간 [1005.0, 1005.5]" in _o1
      and "상한" not in _o1, f"bad {_b1}")
_bg, _og = _check162([[2073.0, 2091.0, _GRAZE[:160], "refusal", "onset_graze", {"s_min": 24.99, "graze_points": 15, "points": 19}]])
check("C157 메모 5 — --check 가 표지 구간을 폭 · 표지와 찍고 FAIL 없음(18 K 띠)",
      "폭 18.000 K · 경계 스침(폭 상한 면제" in _og and "최소 S 24.99 · 스침 15/19" in _og and "상한" not in _og.replace("폭 상한 면제", "") and _bg == _b1, f"bad {_bg}")
import core_history  # noqa: E402
_gn = core_history._gap_note({"grid_gap_calls": 2, "grid_gap_steps": 5, "grid_gap_spans": [(2073.0, 2091.0)]})
check("C157 메모 5 — 열진화 메모가 건넌 구간의 폭을 찍음", bool(_gn) and "(폭 18.00 K)" in _gn[0], str(_gn)[:120])
_b3, _o3 = _check162([[1000.0 + i, 1000.5 + i, _JUMP, "refusal"] for i in range(3)])
check("C162 ② — 거절 구간 셋을 든 표는 --check FAIL", "거절 구간이 상한을 넘는다 (3 개 > 2" in _o3 and _b3 == _b1 + 1, f"bad {_b3}")

ghost =copy.deepcopy(run.load_body(sg.BODIES_DIR / "earth.yaml")[0])
ghost.name = "NoSuchBody"
_, why = sg.load_for(ghost)
check("표가 없는 바디 → 이름 대고 거절", why is not None and "구조 표가 없다" in why, (why or "")[:100])

import math                                                              # noqa: E402
# 덧붙임 60 — 자기 점검은 S0 의 T_c 에 고정한 조성 고정 풀이로, 여섯 칸 모두 SHOOT_TOL
_v0 = {"radius": 0.53, "nmoi": 0.3625, "core_radius": 0.27, "core_radius_fraction": 0.51, "cmb_pressure": 19.0,
       "cmb_temperature": 1961.18, "core_temperature": 2440.18, "core_pressure": 39.93}
_seen = {}
def _fake_pin_solve(t, p_hint=None):
    _seen.update(pin=interior._PIN[0], t=t)
    return types.SimpleNamespace(applicable=True, values=dict(_v0))
_pin0 = interior._PIN[0]
_pr = sg._pinned_solve(_fake_pin_solve, 1600.0, _v0)
check("덧붙임 60 — 고정 풀이는 호출 동안만 interior._PIN 에 (S0 T_c · 중심압) 을 걸고 지운다",
      _seen == {"pin": (2440.18, 39.93e9), "t": 1600.0} and interior._PIN[0] == _pin0, str(_seen))
_ok, _line = sg._self_check(_v0, dict(_v0))
check("덧붙임 60 — 같은 T_c 의 같은 풀이는 통과(칸마다 SHOOT_TOL 대비 비율을 찍음)", _ok and "cmb_temperature 0" in _line, _line[:120])
_ok_r, _line_r = sg._self_check(_v0, {**_v0, "radius": 0.53 * (1 + 10 * interior.SHOOT_TOL)})
check("덧붙임 60 음성 — 심은 조성 불일치(반지름 SHOOT_TOL 의 10 배)는 고정 T_c 에서 실패", not _ok_r and "가장 큰 칸 radius" in _line_r, _line_r[:120])
_ok_t, _line_t = sg._self_check(_v0, {**_v0, "core_temperature": 2440.18 * (1 + 1e-6),
                                      "cmb_temperature": 1961.18 * (1 + 1e-6)})
check("덧붙임 60 음성 — 고정 T_c 를 1e-6 흔들면 실패(고정이 안 잡혔다)", not _ok_t and "고정이 안 잡혔다" in _line_t, _line_t[:120])
check("덧붙임 60 — 고정 풀이가 답을 안 내면 실패", not sg._self_check(_v0, None)[0])

print(f"  test_structure_grid — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
