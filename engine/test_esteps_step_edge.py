# E-steps 걸음 가장자리 — 차분 발판이 맨틀 표의 값 바닥(1 bar 첫 점)을 넘지 않는다: 바닥 둘레 dT/dP · K_T 이어짐, 바닥 위 비트 동일, 화성 1500 K 마지막 걸음 뜀 소거
"""E-steps note (step edge): difference stencils stay above a phase's value floor.

    python3 engine/test_esteps_step_edge.py

The declared-mantle table phase reads its grid at max(p, 1e5 Pa), so every value is constant below 1 bar. A K_T stencil
(p ± 1e-4 p) straddling that floor sees half or none of the density slope, and dT/dP = γT/K_S goes to half or 0.
Under E-steps (T as an RK4 state) a last-step stage that lands within ~10 Pa of 1 bar reads that slope, and Mars
1500 K's surface T jumps by 0.08 K as T_c moves by 2e-5 K (c8 ESTEPS-C152-RAMP; the C152 note 6 tight rerun).

1. Real Mars table material: with the switch on, `_adiabatic_dtdp` and `Material.k_t` are positive and continuous
   (spread < 1e-3) across 0.5–1.0003 bar; off (control), dT/dP is 0 and K_T is 0 just under the floor.
2. Above the floor's band (p ≥ floor · (1 + 3e-4)) on and off are bit-identical: the fix touches only the band.
3. Mars 1500 K, sulphur fixing box_ceiling with c8's probe cmf 0.2779053215587793 (a planted input, not the anchor's
   cmf), one fixed p_c, six T_c 2e-5 K apart across the old jump: on, every neighbour
   step in surface T is within 3× the median; off (control), one step is over 100× the median.
"""
from __future__ import annotations

import contextlib
import io
import statistics
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos  # noqa: E402
import interior  # noqa: E402
import mantle_composition as mc  # noqa: E402

fails = 0
T, T_POT = 1499.96, 1500.0
FLOOR = mc.P_FLOOR
NEAR = (0.5e5, 0.9999e5, 0.99999e5, 1.0e5, 1.00001e5, 1.00005e5, 1.0001e5, 1.0003e5)
ABOVE = (1.0003e5 * 1.0001, 1.0e6, 1.0e9, 2.0e10)


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


@contextlib.contextmanager
def switch(on):
    saved = interior.STENCIL_VALUE_FLOOR
    interior.STENCIL_VALUE_FLOOR = on
    try:
        yield
    finally:
        interior.STENCIL_VALUE_FLOOR = saved


def table_mat():
    tab, why = mc.load(mc._body_wt("mars"))
    if why:
        raise SystemExit(f"STOP: Mars mantle table not loadable — {why}")
    return mc.table_material(eos.MATERIALS["silicate"], tab.key)


def dtdp(mat, p):
    return interior._adiabatic_dtdp(mat, p, mat.density(p, T, T_POT), T, T_POT)


mat = table_mat()
print(f"1. 값 바닥 둘레 — {mat.name}, T {T} K")
row(mat.value_floor(0.5e5) == FLOOR and mat.value_floor(1e9) == FLOOR and mat.value_floor(3e10) == 0.0,
    f"value_floor: 0.5 bar → {mat.value_floor(0.5e5)}, 1 GPa → {mat.value_floor(1e9)}, 30 GPa (다음 상) → "
    f"{mat.value_floor(3e10)}")
with switch(True):
    g_on = [dtdp(mat, p) for p in NEAR]
    k_on = [mat.k_t(p, T, T_POT) for p in NEAR]
with switch(False):
    g_off = [dtdp(mat, p) for p in NEAR]
    k_off = [mat.k_t(p, T, T_POT) for p in NEAR]
for name, on in (("dT/dP", g_on), ("K_T", k_on)):
    spread = max(on) / min(on) - 1.0 if min(on) > 0.0 else float("inf")
    row(min(on) > 0.0 and spread < 1e-3, f"on: {name} 양수 · 이어짐 0.5–1.0003 bar (퍼짐 {spread:.2e} < 1e-3)")
row(g_off[1] == 0.0 and k_off[1] == 0.0,
    f"off (대조): 0.9999 bar 에서 dT/dP {g_off[1]!r} · K_T {k_off[1]!r} — 둘 다 0 이어야 시험이 결함을 본다")

print("\n2. 바닥 띠 위는 비트 동일")
with switch(True):
    a = [(dtdp(mat, p), mat.k_t(p, T, T_POT)) for p in ABOVE]
with switch(False):
    b = [(dtdp(mat, p), mat.k_t(p, T, T_POT)) for p in ABOVE]
row(a == b, f"on == off at {[f'{p:.4g}' for p in ABOVE]} Pa")

print("\n3. 화성 1500 K (cmf 0.27790532, 심은 입력) — 고정 중심압에서 T_c 여섯 점(2e-5 K 간격, 옛 뜀을 가로지름)의 표면 T")
TCS = [2487.84860 + 2e-5 * i for i in range(6)]
#: 심은 고정 입력 — c8 탐침(ESTEPS-C152-RAMP, s4r-probes 60c7b925b)의 cmf, 10-07 전 화성 리터럴. 앵커 값(VR-base 6)이 아니다:
#   이 cmf 에서 마지막 걸음의 k2 단계가 이 T_c 격자 안에서 1 bar 를 건넌다(ramp_locate). off 대조가 뜀을 못 보면 뜀이 옮겨 간 것 —
#   격자를 다시 잡는다(시험이 빨개지는 것이 맞다).
CMF = 0.2779053215587793


def scan(on):
    import registry
    import run
    import structure_grid as sg
    registry.load_all()
    cap, got = {}, {}
    raw = interior._integrate_raw

    def capture(*a, **k):
        cap["a"], cap["k"] = a, dict(k)
        return raw(*a, **k)

    class Got(Exception):
        pass

    shoot = interior._shoot_pressure

    def once(*a, **kw):
        k = dict(kw)
        k.update(t_center=TCS[2], tol=1e-8)
        shoot(*a, **k)
        interior._integrate_raw = raw
        for tc in TCS:
            a2, kk = list(cap["a"]), dict(cap["k"])
            if "t_center" in kk:
                kk["t_center"] = tc
            elif len(a2) > 11:                   # `_integrate_raw`'s 12th positional is t_center
                a2[11] = tc
            else:
                raise SystemExit("STOP: the captured integrate call carries no t_center — the scan would not move T_c")
            got[tc] = raw(*a2, **kk).t_surface
        raise Got()

    body, _ = run.load_body(sg.BODIES_DIR / "mars.yaml")
    solve, _how, _ = sg._solver(body, types.SimpleNamespace(values={"core_mass_fraction": CMF}))
    interior._integrate_raw, interior._shoot_pressure = capture, once
    try:
        with switch(on), contextlib.redirect_stdout(io.StringIO()):
            solve(1500.0)
    except Got:
        pass
    finally:
        interior._integrate_raw, interior._shoot_pressure = raw, shoot
    if len(got) != len(TCS):
        raise SystemExit(f"STOP: the scan read {len(got)} of {len(TCS)} T_c")
    return [got[tc] for tc in TCS]


for on in (True, False):
    ts = scan(on)
    steps = [abs(b - a) for a, b in zip(ts, ts[1:])]
    med = statistics.median(steps)
    worst = max(steps) / med if med > 0.0 else float("inf")
    if on:
        row(worst < 3.0, f"on: 이웃 차 최대 / 중앙값 = {worst:.2f} < 3 (표면 T {ts[0]:.6f} … {ts[-1]:.6f} K)")
    else:
        row(worst > 100.0, f"off (대조): 이웃 차 최대 / 중앙값 = {worst:.0f} > 100 — 옛 뜀이 이 격자에 있다")

print(f"\n{'모두 통과' if not fails else f'{fails} 실패'}")
sys.exit(1 if fails else 0)
