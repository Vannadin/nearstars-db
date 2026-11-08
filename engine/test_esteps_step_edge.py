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
4. Hot water (h2o_hot): its value bounds are P(RHO_MIN, T) and P(RHO_MAX, T), where water_hot.density clamps. Across
   RHO_MIN at 1500 K, on: dT/dP positive and continuous (spread < 1e-2); off (control): 0 far outside, about half 1e-5
   outside; far inside, the stencil is the same on and off. RHO_MAX is not reachable: p_max ≤ P(RHO_MAX, T) from T_MIN on.
5. A mixture whose stencil crosses a part's value bound is not fixed (declared gap): the stencil is returned as is and
   eos.VALUE_BOUND_MIXED counts it (integrate hangs the per-structure count on `value_bound_mixed`). For hot water the
   crossing stencil's lower point reads the part under RHO_MIN, which water_hot.CLAMPED counts, so a converged answer
   with it is refused by C122 R1 (`hot_water_clamped`).
6. Directing 11-08: no shipped, validation or test body reaches a mixture crossing (note 6 §6.2), so a converged answer
   carrying `value_bound_mixed` is refused by name (interior._refuse_if_value_bound_mixed, VALUE_BOUND_MIXED_HEAD).
   A water-free mixture (Mars table + silicate) crossing 1 bar is counted with no hot-water clamp, so C122 R1 does not
   cover it; the refusal does. Both answer sites that call the water refusal call it.
3. Mars 1500 K, sulphur fixing box_ceiling with c8's probe cmf 0.2779053215587793 (a planted input, not the anchor's
   cmf), one fixed p_c, six T_c 2e-5 K apart across the old jump: on, every neighbour
   step in surface T is within 3× the median; off (control), one step is over 100× the median.
"""
from __future__ import annotations

import contextlib
import io
import math
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

print("\n4. 뜨거운 물(h2o_hot) — RHO_MIN · RHO_MAX 클램프 둘레, T 1500 K (값 경계가 T 에 달림)")
import water_hot  # noqa: E402
hot = eos.MATERIALS["h2o_hot"]
TH = 1500.0
for edge, rho_b in (("RHO_MIN", water_hot.RHO_MIN),):
    pb = water_hot.pressure(rho_b, TH)
    lo, hi = hot.value_bounds(pb, TH)
    row(pb == (lo if edge == "RHO_MIN" else hi), f"value_bounds({edge}) = P({edge}, {TH} K) = {pb:.6e} Pa")
    sign = 1.0 if edge == "RHO_MIN" else -1.0
    ps = [pb * (1.0 + sign * f) for f in (-0.5, -1e-4, -1e-5, 0.0, 1e-5, 1e-4, 3e-4)]

    def hd(pp):
        return interior._adiabatic_dtdp(hot, pp, hot.density(pp, TH), TH, 0.0)
    with switch(True):
        on = [hd(pp) for pp in ps]
    with switch(False):
        off = [hd(pp) for pp in ps]
    spread = max(on) / min(on) - 1.0 if min(on) > 0.0 else float("inf")
    row(min(on) > 0.0 and spread < 1e-2, f"on: {edge} 둘레 dT/dP 양수 · 이어짐 (퍼짐 {spread:.2e} < 1e-2)")
    row(off[0] == 0.0 and 0.0 < off[2] < 0.75 * on[2],
        f"off (대조): {edge} 밖 0.5 에서 0 ({off[0]!r}), 밖 1e-5 에서 절반쯤 ({off[2] / on[2]:.3f} × on) — 시험이 결함을 본다")
    # 안쪽 먼 자리: 발판이 같다(기울기 값은 water_hot.density 의 직전 해 출발점(_LAST_DENSITY) 때문에 호출 이력에 따라
    #   마지막 비트가 달라질 수 있어, 같은 발판 → 같은 호출열이라는 것을 발판으로 본다)
    pf = pb * 2.0 if edge == "RHO_MIN" else pb * 0.5
    st = []
    for sw in (True, False):
        with switch(sw):
            st.append(interior._phase_stencil(hot, pf, pf * (1 - 1e-4), pf * (1 + 1e-4), pf * 1e-4, TH))
    row(st[0] == st[1], f"경계에서 먼 안쪽({pf:.3e} Pa)의 발판 on == off {st[0]}")

# RHO_MAX 천장: 재료 상한 p_max 가 T_MIN 이상에서 P(RHO_MAX, T) 를 넘지 않아 발판이 못 닿는다(p_max 에서 자름) — 닿지 않음을 단언
tops = [(tt, water_hot.pressure(water_hot.RHO_MAX, tt)) for tt in (water_hot.T_MIN, 2000.0, 5000.0, 20000.0, 50000.0)]
row(all(hot.p_max <= pt * (1.0 + 1e-6) for _tt, pt in tops),
    f"RHO_MAX 천장은 닿지 않음: p_max {hot.p_max:.6e} ≤ P(RHO_MAX, T) {[f'{pt:.4e}' for _t, pt in tops]} (T_MIN 부터)")

print("\n5. 혼합의 성분 경계 — 선언한 틈: 고치지 않고 센다(VALUE_BOUND_MIXED, 구조의 value_bound_mixed)")
pb = water_hot.pressure(water_hot.RHO_MIN, TH)
mix = eos.mix("h2o_hot_rock_note6", "시험 혼합", (hot, 0.5), (eos.MATERIALS["silicate"], 0.5))
n0, c0 = eos.VALUE_BOUND_MIXED["n"], water_hot.CLAMPED["n"]
with switch(True):
    got = eos.value_floor_stencil(mix, pb, pb * (1 - 1e-4), pb * (1 + 1e-4), pb * 1e-4, math.inf, TH)
row(type(mix).__name__ == "Mixture" and got == (pb * (1 - 1e-4), pb * (1 + 1e-4)) and eos.VALUE_BOUND_MIXED["n"] == n0 + 1,
    f"혼합 발판은 그대로, 셈 +1 (n {n0} → {eos.VALUE_BOUND_MIXED['n']}, 첫 자리 {eos.VALUE_BOUND_MIXED['first']})")
# 그 발판의 아래 끝은 뜨거운 물을 RHO_MIN 밑에서 읽는다 → water_hot.CLAMPED 가 늘고, 수렴한 답이면 C122 R1
#   (`hot_water_clamped`, «혼합 · 외피 경로 포함»)이 이름 대고 거절한다 — 물이 낀 건넘은 답으로 나가지 않는다
mix.density(pb * (1 - 1e-4), TH, 0.0)
row(water_hot.CLAMPED["n"] > c0, f"건넌 발판의 아래 끝 읽기가 뜨거운 물 클램프를 센다 (CLAMPED {c0} → {water_hot.CLAMPED['n']}) "
                                 "— 답이면 C122 R1 거절")

print("\n6. 혼합 건넘은 답이면 이름 댄 거절(지휘석 11-08: 출하 · 검증 · 시험 몸 어느 것도 안 닿음 → STOP)")
# 물 없는 혼합(맨틀 표 + 규산염)은 C122 R1 이 못 잡는다 — 바닥 1 bar 를 건넌 발판은 VALUE_BOUND_MIXED 만 센다
mix2 = eos.mix("table_rock_note6", "시험 혼합 2", (mat, 0.5), (eos.MATERIALS["silicate"], 0.5))
n0, c0 = eos.VALUE_BOUND_MIXED["n"], water_hot.CLAMPED["n"]
with switch(True):
    eos.value_floor_stencil(mix2, FLOOR, FLOOR * (1 - 1e-4), FLOOR * (1 + 1e-4), FLOOR * 1e-4, math.inf, T)
row(eos.VALUE_BOUND_MIXED["n"] == n0 + 1 and water_hot.CLAMPED["n"] == c0,
    f"물 없는 혼합의 바닥 건넘: 셈 +1, 뜨거운 물 클램프 그대로({c0}) — C122 R1 밖")
first = eos.VALUE_BOUND_MIXED["first"]
try:
    interior._refuse_if_value_bound_mixed(types.SimpleNamespace(value_bound_mixed=(3, ("table_rock_note6", FLOOR, FLOOR))))
    got = None
except eos.PhaseGap as e:
    got = e
row(got is not None and got.material == "table_rock_note6" and got.pressure_pa == FLOOR
    and str(got).startswith(interior.VALUE_BOUND_MIXED_HEAD) and "3 번" in str(got),
    f"value_bound_mixed 가 있는 답 → PhaseGap «{interior.VALUE_BOUND_MIXED_HEAD}» (재료 · 압력 · 셈)")
try:
    interior._refuse_if_value_bound_mixed(types.SimpleNamespace(value_bound_mixed=None))
    clean = True
except eos.PhaseGap:
    clean = False
row(clean, "value_bound_mixed 없음(None) → 거절 없음")
# 답을 내는 두 자리(사격 답 · 접힘 답)가 물 거절 바로 뒤에서 부른다 — 소스에서 셈
src = Path(interior.__file__).read_text()
pair = "    _refuse_if_water_filled(st)\n    _refuse_if_value_bound_mixed(st)\n"
row(src.count("_refuse_if_water_filled(st)\n") == 2 and src.count(pair) == 2,
    "물 거절을 부르는 두 답 자리 모두 혼합 거절을 부름")

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
