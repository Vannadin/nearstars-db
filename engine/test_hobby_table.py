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
    found = _phase_density_overrides()
    ok(found == KNOWN_PHASE_DENSITY_OVERRIDES,
       f"H-exact (4a): census — Phase subclasses that override density are exactly the known set {sorted(found)} "
       "(they get the old 3-arg call, no p_th; a new one must be checked against `_solid_density_at`)")
    n, same, refusals = _eos_density_exact(rnd)
    ok(same == n and refusals > 0, f"H-exact (4a): eos Material.density bit-identical to the C160 path on {n} (material, P, T) "
                                   f"— equal {same}, the same refusals included ({refusals})")


#: C161 (4a) — `eos.Phase` 를 이어받아 `density` 를 다시 쓴 클래스(파일::클래스 — check_refs 가 인용으로 읽지 않는 기호 꼴). 이들은 `_solid_density_at` 에서 `p_th` 를
#: 받지 않는다(옛 세 인자 그대로 — 바뀐 동작 없음). 새 하위 클래스가 생기면 이 목록과 어긋나 실패한다: 그 서명을 보고 더한다.
KNOWN_PHASE_DENSITY_OVERRIDES = {"mantle_composition.py::TablePhase"}


def _phase_density_overrides() -> set[str]:
    """엔진 소스 전부에서 `Phase` / `eos.Phase` 를 밑으로 둔 클래스 중 `density` 를 정의한 것(함수 안 클래스 포함)."""
    import ast
    out = set()
    for path in sorted(HERE.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.ClassDef):
                continue
            bases = {b.id if isinstance(b, ast.Name) else b.attr if isinstance(b, ast.Attribute) else "" for b in node.bases}
            if "Phase" in bases and any(isinstance(f, ast.FunctionDef) and f.name == "density" for f in node.body):
                out.add(f"{path.name}::{node.name}")
    return out


def _eos_density_exact(rnd) -> tuple[int, int, int]:
    """C161 (4a) eos — 상을 한 번 찾고 가드의 열압력을 넘기는 새 `Material.density` 를 C160 의 몸통(아래 `ref`)과 비트로 대조."""
    import eos

    def ref_solid(m, p, t, t_pot):
        eos._below_t_window(m.name, p, t)
        m.check_temperature(p, t)
        ph = m.phase_at(p)
        if ph.graded_below_ref:
            cold = p - ph.thermal_pressure(t, t_pot, p)
            if cold <= 0.0 or cold < ph.p_min:
                raise eos.PhaseGap(m.name, p, "ref")
        return ph.density(p, t, t_pot)

    def ref(m, p, t, t_pot):
        rho_s = ref_solid(m, p, t, t_pot)
        phi = m.melt_phi(p, t)
        if phi <= 0.0:
            return rho_s
        rho_l = eos.rtpress.liquid(p, t)[0]
        return rho_l if phi >= 1.0 else 1.0 / ((1.0 - phi) / rho_s + phi / rho_l)

    def run(fn, *args):
        try:
            return fn(*args)
        except Exception as e:                    # 거절은 종류로 대조(문구는 같은 자리에서 만든다)
            return type(e).__name__
    mats = [m for m in eos.MATERIALS.values() if type(m) is eos.Material]
    # density 를 세 인자로 다시 쓴 상(C59 의 `mantle_composition.TablePhase` 꼴)을 든 재질도 — 열압력 넘김이 그 상을 건너야 한다
    import dataclasses

    class _Override(eos.Phase):
        def density(self, p, t=0.0, t_pot=0.0):
            return eos.Phase.density(self, p, t, t_pot)
    for m in [m for m in mats if any(ph.graded_below_ref for ph in m.phases)][:3]:
        phs = tuple(_Override(**{f.name: getattr(ph, f.name) for f in dataclasses.fields(ph)}) for ph in m.phases)
        mats.append(dataclasses.replace(m, name=m.name + "_override", phases=phs))
    n = same = refusals = 0
    for _ in range(6000):
        m = rnd.choice(mats)
        p = 10.0 ** rnd.uniform(5.0, 12.5)
        t = rnd.choice((0.0, rnd.uniform(200.0, 6000.0)))
        t_pot = rnd.choice((0.0, 1600.0, rnd.uniform(1200.0, 2600.0)))
        a, b = run(m.density, p, t, t_pot), run(ref, m, p, t, t_pot)
        n += 1
        same += a == b
        refusals += isinstance(a, str)
    return n, same, refusals


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
    # C159 규칙 3 — 임시 폴더엔 화성 표만 있어 열진화 선언 천체의 «표 없음» FAIL 이 더해진다. 빠른 판 줄만 본다.
    quick_line = [l for l in out.getvalue().splitlines() if "[FAIL] mars.json" in l and "mode quick" in l]
    ok(bad >= 1 and len(quick_line) == 1, "H-quick: --check refuses a committed quick table")
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


def h_judge() -> None:
    """C161 덧붙임 3 — J-fire: 빠른 판 a 만 길은 `fired` 를 달고 판정 멤버를 안 푼다. J-neg: 비교가 심은 «답 둘» 을 잡는다."""
    import copy
    import interior
    import structure_grid as sg
    calls = []

    def fake_raw(solve, jobs):
        calls.append(len(jobs))
        return [types.SimpleNamespace(t=t, applicable=True, trail={"answer_call": 0, "trials": []}) for t, _h, _e in jobs]
    saved = (sg._solve_raw, sg._fires, sg._settled_trials, sg._families_visited, sg.JUDGE_A_ONLY)
    sg._solve_raw, sg._fires = fake_raw, (lambda r: r.t == 2.0)
    sg._settled_trials, sg._families_visited = (lambda r: []), (lambda r: [])
    sg.JUDGE_A_ONLY = True
    sg.SOLVE_KINDS.clear()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            out = sg._pool_solve(None, [(1.0, None), (2.0, None), (3.0, None)], {}, kind="refine")
    finally:
        sg._solve_raw, sg._fires, sg._settled_trials, sg._families_visited, sg.JUDGE_A_ONLY = saved
    judged = {k: v for k, v in sg.SOLVE_KINDS.items() if k.startswith("judge")}
    ok(calls == [3] and not judged and getattr(out[1], "fired", False) and not hasattr(out[0], "fired"),
       f"J-fire: a-only marks the firing point fired and runs no judge member (pool calls {calls}, judge kinds {judged})")
    doc = json.loads((sg.GRID_DIR / "mars.json").read_text(encoding="utf-8"))
    same, worst = sg.judge_compare(doc, copy.deepcopy(doc))
    full = copy.deepcopy(doc)
    t0, t1 = doc["t_pot"][10], doc["t_pot"][11]
    full.setdefault("no_answer", []).append([t0, t1, interior.FAMILY_TWO_NOTE + " — 심은 c 의 둘째 가족"])
    planted, _ = sg.judge_compare(full, doc)
    ok(not same and worst == 0.0 and len(planted) == 1 and "구간 수" in planted[0],
       f"J-neg: the comparison passes identical tables and catches a planted «답 둘» span from member c — {planted}")


if __name__ == "__main__":
    h_exact()
    h_par()
    h_judge()
    h_quick()
    h_scope()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
