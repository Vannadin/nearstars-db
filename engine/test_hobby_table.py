# 취미용 표 가속(C161)이 값을 안 바꾸는가 — 압력식 재배열 · 풀이마다 기억 초기화 · 빠른 판 표시
"""prereg-c161-hobby-table (frozen 19d4fd42): H-exact, H-scope, H-quick (the fixtures; wall times are run separately).

    python3 engine/test_hobby_table.py
"""
from __future__ import annotations

import contextlib
import io
import json
import math
import random
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rtpress   # noqa: E402

fails: list[str] = []


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def h_exact() -> None:
    """(4a) 압력식: |Δ| ≤ 1e-12 × Σ|항| 또는 1e-3 Pa — 섞은 경계(감사 e2). (4b) 따뜻한 출발은 철회 (C161 덧붙임 1)."""
    rnd = random.Random(161)
    worst = 0.0
    for _ in range(20000):
        v, t = rtpress.V0 * rnd.uniform(0.25, 1.5), rnd.uniform(1500.0, 14000.0)
        a, b = rtpress.pressure(v, t), rtpress.pressure_reference(v, t)
        dpe = abs(rtpress.db_of(v) * (rtpress.f_t(t) - rtpress.f_t(rtpress.T0)))
        dps = abs(t * rtpress._ds_dv(v, t)) + abs(rtpress.T0 * rtpress._ds_dv(v, rtpress.T0))
        scale = abs(rtpress.p0t(v)) + (dpe + dps) * rtpress.PV
        bound = max(1e-12 * scale, 1e-12)                     # 1e-3 Pa = 1e-12 GPa
        worst = max(worst, abs(a - b) / bound)
    ok(worst <= 1.0, f"H-exact (4a): pressure within the mixed bound on 20 000 (V, T) — worst {worst:.3f} of the bound")
    import fe_liquid as fl
    worst_fe = 0.0
    for col in (fl.LIQUID, fl.HCP):
        for _ in range(10000):
            v, t = col.v0 * rnd.uniform(0.3, 1.4), rnd.uniform(300.0, 9000.0)
            a, b = fl.pressure(v, t, col), fl.pressure_reference(v, t, col)
            scale = (abs(fl._p_cold(col, v)) + abs(fl._p_th(col, v, t)) + abs(fl._p_th(col, v, col.t_ref))
                     + abs(fl._p_el(col, v, t)) + abs(fl._p_el(col, v, col.t_ref)))
            worst_fe = max(worst_fe, abs(a - b) / max(1e-12 * scale, 1e-3))          # Pa
    ok(worst_fe <= 1.0, f"H-exact (4a): fe_liquid pressure (liquid, hcp) within the mixed bound — worst {worst_fe:.3f}")
    fl.reset_solve_state()
    v1 = fl.volume_at(300e9, 5000.0); v2 = fl.volume_at(300e9, 5000.0); fl.reset_solve_state()
    ok(v1 == v2 == fl._volume_at(300e9, 5000.0), "H-exact (4a): the fe_liquid volume memo returns the solve's own value")


def h_scope() -> None:
    """같은 점을 앞서 다른 점을 푼 뒤에 풀어도 비트까지 같다 — 화성 1800 K, 앞 점 1500 K 대 2060 K."""
    import registry
    import run
    import structure_grid as sg
    registry.load_all()
    body, _ = run.load_body(sg.BODIES_DIR / "mars.yaml")
    solve, _how, _ = sg._solver(body, types.SimpleNamespace(values={"core_mass_fraction": 0.2779053215587793}))
    keys = ("radius", "nmoi", "cmb_temperature", "core_pressure", "core_radius")
    got = []
    for prior in (1500.0, 2060.0):
        with contextlib.redirect_stdout(io.StringIO()):
            solve(prior)
            r = solve(1800.0)
        got.append(tuple(r.values.get(k) for k in keys))
    ok(got[0] == got[1], f"H-scope: Mars 1800 K after 1500 K and after 2060 K — byte-identical {got[0] == got[1]}")


def h_quick() -> None:
    """빠른 판은 `--check` 가 거절하고, 열진화 note 가 그 사실을 한 줄로 적는다."""
    import core_history
    import structure_grid as sg
    saved = sg.GRID_DIR
    with tempfile.TemporaryDirectory() as d:
        sg.GRID_DIR = Path(d)
        doc = json.loads((saved / "mars.json").read_text(encoding="utf-8"))
        doc["mode"] = "quick"
        (Path(d) / "mars.json").write_text(json.dumps(doc), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            bad = sg.check_all()
        sg.GRID_DIR = saved
    ok(bad == 1 and "mode quick" in out.getvalue(), "H-quick: --check refuses a committed quick table")
    note = core_history._quick_note(sg.Grid(doc))
    ok(len(note) == 1 and "quick" in note[0] and core_history._quick_note(None) == (),
       "H-quick: a history read through a quick table carries the note; a reference table adds nothing")


def _fake_result(t: float):
    """가짜 풀이 — 매끈한 곡선 + 꺾임(1900 K) + 뜀(2400 K, r_b) + 받을 답 없는 띠(2101–2104 K) + 가족 검사 점 + 용융 상태 갈림."""
    rad = 0.53 + 2e-5 * (t - 1500.0) + (3e-6 * (t - 1900.0) if t > 1900.0 else 0.0) + 1e-7 * math.sin(t / 37.0)
    t_cmb = 1.15 * t + (0.5 * t if t > 2400.0 else 0.0)
    values = {"radius": rad, "core_radius": 0.27 + 1e-6 * t, "cmb_pressure": 19.0 + 1e-3 * t + 0.5 * math.sin(t / 40.0),
              "cmb_temperature": t_cmb, "silicate_melt_state": "partial" if t > 2250.0 else "solid",
              "basal_silicate_state": None, "ice_column_state": None, "core_status": "liquid"}
    bad = 2101.0 < t < 2104.0
    return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=False if bad else True,
                                 notes=(), inputs={"core_mass_fraction": 0.25}, values=values,
                                 fired=2600.0 < t < 2620.0)


def h_par() -> None:
    """(7) 판 단위 정밀화가 옛 차례 루프와 바이트까지 같은 표를 낸다 — 가짜 풀이로 4766ca7a 의 `_adaptive` 와 대조."""
    import structure_grid as sg
    import subprocess
    src = subprocess.run(["git", "show", "4766ca7a:engine/structure_grid.py"], cwd=HERE, capture_output=True,
                         text=True, check=True).stdout
    old = types.ModuleType("structure_grid_4766ca7a")
    old.__file__ = str(HERE / "structure_grid.py")
    exec(compile(src, "structure_grid@4766ca7a", "exec"), old.__dict__)
    got = {}
    for tag, mod in (("old", old), ("new", sg)):
        batches = []

        def fake_pool(solve, jobs, aux=None, kind="single", _b=batches):
            _b.append(len(jobs))
            return [_fake_result(t) for t, _h in jobs]
        saved = mod._pool_solve
        mod._pool_solve = fake_pool
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                out = mod._adaptive("fake", None, 1500.0, 2900.0, mod.EPS, 6.4e23, 0.25)
        finally:
            mod._pool_solve = saved
        got[tag] = (json.dumps(out, sort_keys=True), batches)
    same = got["old"][0] == got["new"][0]
    n_old, n_new = len(got["old"][1]), len(got["new"][1])
    ok(same and n_new < n_old, f"H-par (7, fixture): rounds give the byte-identical table ({same}); "
                               f"pool dispatches {n_old} → {n_new}, largest batch {max(got['old'][1])} → {max(got['new'][1])}")


if __name__ == "__main__":
    h_exact()
    h_par()
    h_quick()
    h_scope()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
