# 취미용 표 가속(C161)이 값을 안 바꾸는가 — 압력식 재배열 · 따뜻한 근 찾기 · 풀이마다 초기화 · 빠른 판 표시
"""prereg-c161-hobby-table (frozen 19d4fd42): H-exact, H-scope, H-quick (the fixtures; wall times are run separately).

    python3 engine/test_hobby_table.py
"""
from __future__ import annotations

import contextlib
import io
import json
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
    """(4a) 압력식: |Δ| ≤ 1e-12 × Σ|항| 또는 1e-3 Pa — 섞은 경계(감사 e2). (4b) 부피: 근 찾기 허용 1e-12·V₀ 안, 같은 거절."""
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
    # (4b): 따뜻한 출발과 차가운 출발이 1e-12·V₀ 안에서 같고, 거절은 같은 점에서
    worst_v, same_ref = 0.0, True
    for _ in range(400):
        p, t = rnd.uniform(0.0, 200.0), rnd.uniform(2200.0, 9000.0)
        rtpress.reset_solve_state()
        try:
            cold = rtpress.volume(p, t); e_cold = None
        except Exception as e:
            cold, e_cold = None, type(e).__name__
        rtpress._VOLUME_WARM = (cold or rtpress.V0) * (1.0 + 5e-4)
        try:
            warm = rtpress.volume(p, t); e_warm = None
        except Exception as e:
            warm, e_warm = None, type(e).__name__
        same_ref &= e_cold == e_warm
        if cold and warm:
            worst_v = max(worst_v, abs(warm - cold) / rtpress.V0)
    rtpress.reset_solve_state()
    ok(worst_v <= 2e-12 and same_ref, f"H-exact (4b): warm vs cold volume within 2e-12·V₀ (worst {worst_v:.2e}); "
                                      f"the same refusals at the same points: {same_ref}")


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


if __name__ == "__main__":
    h_exact()
    h_quick()
    h_scope()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
