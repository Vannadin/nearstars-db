# C152 시험 — 공용 Brent 가 근을 좁히고, 근 없는 잔차는 거절로 남고, 실오라기 용융은 가족 뜀이 아닌가
"""python3 engine/test_rootfind.py — prereg-c152-straddle-root acceptance 5 (unit part; the loop-level runs are on the PC)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior  # noqa: E402
import rootfind  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def drive(f, a, b, xtol, budget=200):
    g = rootfind.brent(a, f(a), b, f(b), xtol)
    n = 0
    try:
        x = next(g)
        while n < budget:
            n += 1
            x = g.send(f(x))
    except StopIteration as fin:
        return fin.value, n
    return None, n


# ① 아는 근을 xtol 안에 · 매끄러운 잔차는 이분보다 적은 걸음
(x, fx, lo, hi), n = drive(lambda t: t ** 3 - 2.0, 0.0, 2.0, 1e-12)
check("Brent — x³ = 2 의 근을 xtol 안에", abs(x - 2.0 ** (1 / 3)) < 1e-11 and hi - lo <= 2e-12, f"{x!r} · {n} 걸음")
check("Brent — 매끄러운 잔차는 이분(≈ 41 걸음)보다 적게", n < 20, str(n))
# ② 로그 온도 1 K 괄호(화성 꼴): T_TOL 까지 T_PASSES 안
f_mars = lambda lt: (lt - 8.0798) * 1.5 + 4.0 * max(0.0, lt - 8.0799)      # 근 근처에서 기울기가 바뀌는 잔차
(x, fx, lo, hi), n = drive(f_mars, 8.0795, 8.0802, interior.T_TOL)
check("Brent — 기울기가 꺾이는 1 K 괄호를 T_PASSES 안에", n <= interior.T_PASSES and abs(fx) < 1e-6, f"{n} 걸음")
# ③ 음성 대조 — 근이 없는(같은 부호) 잔차는 이름 대고 거절, 뛰는 잔차는 뜀으로 좁혀지고 |f| 가 남는다
try:
    rootfind.brent(0.0, 1.0, 1.0, 2.0, 1e-9)
    check("음성 대조 — 같은 부호 양 끝은 거절", False, "통과함")
except ValueError as e:
    check("음성 대조 — 같은 부호 양 끝은 거절", "straddle" in str(e), str(e))
(x, fx, lo, hi), n = drive(lambda t: -1.0 if t < 1.3 else 1.0, 0.0, 2.0, 1e-9)
check("음성 대조 — 뛰는 잔차는 뜀 자리로 좁혀지고 |f| 가 허용 밖으로 남음", abs(x - 1.3) < 1e-8 and abs(fx) == 1.0, f"{x!r}")
# ④ 가족 판정 — 표본 하나짜리 실오라기는 뜀 아님, 표본 둘은 뜀, 화성 간격에서 문턱 0.5 GPa 그대로
dps = 0.39
check("가족 — 실오라기(한 표본)와 고체는 같은 가족", not interior._family_jump(None, (0.17, 0.17, dps)))
check("가족 — 두 표본 폭의 용융과 고체는 다른 가족", interior._family_jump(None, (0.17, 0.17 + dps, dps)))
check("가족 — 화성 간격에서 0.45 GPa 이동은 같은 가족(문턱 0.5)", not interior._family_jump((7.0, 15.0, dps), (7.45, 15.0, dps)))
check("가족 — 화성 간격에서 0.55 GPa 이동은 뜀(문턱 0.5 그대로)", interior._family_jump((7.0, 15.0, dps), (7.55, 15.0, dps)))
check("가족 — 성긴 표본(0.8 GPa)에서는 문턱 1.2 GPa", not interior._family_jump((7.0, 15.0, 0.8), (8.0, 15.0, 0.8))
      and interior._family_jump((7.0, 15.0, 0.8), (8.3, 15.0, 0.8)))
check("가족 — 207x 의 두 가족(p_hi 15.36 대 17.06)은 여전히 뜀", interior._family_jump((6.49, 15.36, dps), (6.87, 17.06, dps)))

# ⑤ 고리 수준 음성 대조(감사 e2 HOLD 4) — 가짜 사격으로 §1 의 세 고리를 직접 돌린다
import types  # noqa: E402

import eos  # noqa: E402

T_POT = 1000.0


def _fake_st(t_c, t_surf):
    return types.SimpleNamespace(t_surface=t_surf, p_center=1e11, rock_samples=(), radius_m=6.4e6, mass_kg=6e24,
                                 floor_truncated=None, p_cmb=None, hot_water_filled=None, crust_blocked=False,
                                 surface_reached=True, ice_samples=(), t_center=t_c, boiling_flips=None)


def _run_shoot(surface, wall=None):
    """surface(T_c) → T_surf. wall 가 있으면 그 위의 T_c 는 뜨거운 온도 벽(PhaseGap, too_cold False)."""
    real = interior._shoot_pressure

    def fake(*a, t_center=None, t_pot=None, p_hint=None, tol=None, **k):
        if wall is not None and t_center > wall:
            raise eos.PhaseGap("fake_envelope", 1e9, "가짜 뜨거운 벽", temperature_k=t_center, too_cold=False)
        return _fake_st(t_center, surface(t_center)), True
    interior._shoot_pressure = fake
    try:
        st, ok = interior.shoot(6e24, 0.3, 0.0, "fe_prem", potential_temperature=T_POT)
        return "answer", (st.t_center, st.t_surface, ok)
    except (ValueError, eos.PhaseGap) as e:
        return "refusal", str(e)
    finally:
        interior._shoot_pressure = real


import contextlib  # noqa: E402
import io  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    k_a, v_a = _run_shoot(lambda t: 0.5 * T_POT)                                   # 근 없음(늘 차다), 0 을 안 사이에 둠
    k_b, v_b = _run_shoot(lambda t: T_POT * t / 1700.0 * (0.999 if t < 1700.0 else 1.001))   # 뜀(근 없음), 좁은 괄호
    _passes0 = interior.T_PASSES
    interior.T_PASSES = 4                                                            # 예산을 줄여 괄호 안에서 끝나게
    try:
        k_e, v_e = _run_shoot(lambda t: T_POT * (0.99 if t < 1990.0 else 1.01))    # 둘째 시행에서 0 을 사이에 둠
    finally:
        interior.T_PASSES = _passes0
    k_c, v_c = _run_shoot(lambda t: T_POT * 0.5 * t / 1500.0, wall=1500.0)          # 벽 아래로 못 닿음
    k_d, v_d = _run_shoot(lambda t: T_POT * (t / 1650.0) ** 3)                      # 가파른 근(1650 K)
check("고리 #1 음성 — 0 을 안 사이에 둔 근 없는 잔차는 오늘의 길(C152 문구 없음)",
      k_a == "refusal" and "C152" not in str(v_a) or k_a == "answer" and not v_a[2], str(v_a)[:90])
check("고리 #1 음성 — 0 을 사이에 둔 뜀은 «잔차가 뛴다» 로 이름 대고 거절", k_b == "refusal" and "잔차가 뛴다" in v_b, str(v_b)[:90])
check("고리 #1 음성 — 괄호 안에서 예산이 끝나면 오늘의 이름 댄 거절에 괄호를 적음", k_e == "refusal" and "0 을 사이에 둔 괄호" in v_e,
      str(v_e)[:90])
check("고리 #2 음성 — 재시도가 벽에 막히면 벽을 찾아 «닿는 해가 없다» 로 거절, 벽 자리가 1.6 배 걸음이 아님",
      k_c == "refusal" and "닿는 해가 없다" in v_c and "1500 K" in v_c, str(v_c)[:120])
check("고리 #1 양성 — 가파른 근은 닫힘(비례 갱신이 넘나들던 꼴)", k_d == "answer" and abs(v_d[0] - 1650.0) / 1650.0 < 1e-5,
      str(v_d)[:90])
# 고리 #3 — 세 층 역산의 좁힘(근 없음: 같은 부호 → 오늘의 할선, 닫히지 않음 · 근 있음: Brent 로 닫힘)
best, closed = interior._three_layer_close(0.1, 0.02, 0.3, 0.01, lambda x: (0.0, None, 0.01 + 0 * x), 0.33)
check("고리 #3 음성 — 0 을 안 사이에 둔 잔차는 오늘의 할선으로 닫히지 않음", not closed)
best, closed = interior._three_layer_close(0.1, -0.02, 0.3, 0.02, lambda x: (0.0, None, (x - 0.2137) * 0.2), 0.33)
check("고리 #3 양성 — 0 을 사이에 두면 Brent 로 닫힘", closed and abs(best[0] - 0.2137) < 2e-3, str(best and best[0]))

# ⑥ C152 메모 1 — 접힘 탐지기 (iii): 근 셋 → «답 둘», (iii) 끄면 답, 단조(207x 꼴)는 안 섬, 띠(3b) · 안 닫힌 사격(3c)
import math  # noqa: E402

import structure_grid as sg  # noqa: E402

FA, FB = (6.49, 15.36, 0.39), (6.87, 17.06, 0.39)


def _trial(f, t, y, ok=True, call=0, tau=1e-6):
    return (f, t, 3.9e10, call, y, ok, tau)


def _fake_fold(trials, answer_fam):
    """trials: a 멤버의 시행 · answer_fam: 힌트 없는 풀이의 답 가족. 입구(c)로 풀면 다른 가족의 답."""
    def solve(t, p_hint=None):
        if interior._ENTRY[0] is not None:
            fam, tr = (FB if answer_fam == FA else FA), [_trial(FB, 3230.0, 0.0)]
        elif p_hint is not None:
            fam, tr = answer_fam, [_trial(answer_fam, 3229.0, 0.0)]
        else:
            fam, tr = answer_fam, trials
        interior._FAMILY_TRAIL.update(trials=list(tr), reclosed=[], closed=[], answer=fam, dev=1e-5, calls=1,
                                      returned={}, answer_call=0)
        v = {"radius": 0.55, "core_radius": 0.28, "cmb_pressure": 19.0, "cmb_temperature": 1.5 * t,
             "core_pressure": 39.4, "converged": None}
        return types.SimpleNamespace(applicable=True, reason=None, regime="rocky", converged=True, notes=(),
                                     inputs={"core_mass_fraction": 0.3}, values=v)
    return solve


def _verdict(trials, answer_fam=FA):
    sg.GRID_POOL = 1
    with contextlib.redirect_stdout(io.StringIO()):
        r = sg._pool_solve(_fake_fold(trials, answer_fam), [(2076.0, None)], {})[0]
    return interior.answer_verdict(r)


# 근 셋(부호 − + − +), 끝 네 시행은 한 가족(정착 창 (i) 은 안 섬)
fold = [_trial(FB, 3220.0, -0.01), _trial(FB, 3224.0, +0.01), _trial(FB, 3226.0, -0.01)] + \
       [_trial(FA, 3228.0 + 0.2 * i, (+0.004 if i % 2 == 0 else +0.003)) for i in range(4)]
w = _verdict(fold)
check("메모 1 — 근 셋인 접힘은 (iii) 으로 서서 «답 둘»", bool(w) and w.startswith(interior.FAMILY_TWO_NOTE), str(w)[:80])
fold0 = sg._fold
sg._fold = lambda r: False
try:
    w0 = _verdict(fold)
finally:
    sg._fold = fold0
check("메모 1 음성 — (iii) 을 끄면 같은 접힘이 한 근으로 닫혀 답", w0 is None, str(w0)[:80])
# 207x 꼴: 근 하나, 단조, 괄호 두 끝은 다른 «가족», 끝 네 시행 한 가족
mono = [_trial(FA, 3226.0, -0.006), _trial(FA, 3228.0, -0.004), _trial(FA, 3229.3, -0.0018)] + \
       [_trial(FB, 3230.3 + 0.3 * i, 0.0013 + 0.001 * i) for i in range(4)]
check("메모 1 — 단조(207x 꼴)는 (iii) 안 섬", not sg._fold(types.SimpleNamespace(trail={"trials": mono, "answer_call": 0, "calls": 1})))
# 3b — 근 옆에 몰린 시행 + 허용 밑 잔물결: 띠가 막고, 띠를 0 으로 끄면 선다
ripple = mono[:3] + [_trial(FB, 3229.45 + 1e-4 * i, (2e-4 if i % 2 else -2e-4)) for i in range(6)] + mono[3:]
rr = types.SimpleNamespace(trail={"trials": ripple, "answer_call": 0, "calls": 1})
band0 = sg._fold_band
check("메모 1 3b — 허용 밑 잔물결로는 안 섬(띠)", not sg._fold(rr))
sg._fold_band = lambda: 0.0
try:
    check("메모 1 3b 음성 — 띠를 0 으로 끄면 같은 잔물결에 선다", sg._fold(rr))
finally:
    sg._fold_band = band0
# 3c — 안 닫힌 사격의 가짜 반대 부호는 안 셈
bad = mono[:3] + [_trial(FA, 3229.0, +0.02, ok=False), _trial(FA, 3229.1, -0.02, ok=False)] + mono[3:]
check("메모 1 3c — 안 닫힌 사격(ok False)의 가짜 부호는 안 셈",
      not sg._fold(types.SimpleNamespace(trail={"trials": bad, "answer_call": 0, "calls": 1})))
good = mono[:3] + [_trial(FA, 3229.0, +0.02), _trial(FA, 3229.1, -0.02)] + mono[3:]
check("메모 1 3c 음성 — 같은 시행이 닫힌 사격이면 선다(자가 떨어질 수 있음)",
      sg._fold(types.SimpleNamespace(trail={"trials": good, "answer_call": 0, "calls": 1})))

# ⑦ C152 메모 2 — 시행마다 오차 막대(τ ≤ 1e-2 → e = S_max·τ, 그 위는 판단 불가)
def _fr(trials):
    return sg._fold(types.SimpleNamespace(trail={"trials": trials, "answer_call": 0, "calls": 1}))


edge = [_trial(None, 4549.2, 2e-7, tau=8.6e-8), _trial(None, 4563.5, 0.0023, tau=8.2e-4),
        _trial(None, 4736.0, 0.0289, tau=8.0e-3), _trial(None, 5131.9, 0.0803, tau=3.85e-3)]
check("메모 2 ① — 먼 끝 역전이 τ 0.1 시행이면 안 섬(2666 꼴)", not _fr(edge + [_trial(None, 5333.4, 0.0385, tau=0.1)]))
check("메모 2 ② — 같은 꼴을 모두 정밀하게 쏘면 섬(진짜 먼 끝 추세)", _fr(edge + [_trial(None, 5333.4, 0.0385, tau=1e-4)]))
base = [_trial(None, 4600.0, 0.010, tau=1e-3), _trial(None, 4700.0, 0.020, tau=1e-3), _trial(None, 4800.0, 0.030, tau=1e-3)]
inside = 0.030 - (1e-3 + 1e-3 + 1e-3) + 1e-4           # 역전이 e_i + e_j + 띠 = 3e-3 보다 조금 작음
outside = 0.030 - (1e-3 + 1e-3 + 1e-3) - 1e-4
check("메모 2 ③ — 오차 + 띠 안쪽 역전은 안 섬", not _fr(base + [_trial(None, 4900.0, inside, tau=1e-3)]))
check("메모 2 ③ — 오차 + 띠 바깥 역전은 섬", _fr(base + [_trial(None, 4900.0, outside, tau=1e-3)]))
flipper = [_trial(FA, 3226.0, -0.006), _trial(FA, 3228.0, -0.004), _trial(FB, 3230.3, +0.002), _trial(FB, 3231.0, +0.004)]
check("메모 2 ④ — 느슨한(τ > 1e-2) 시행의 가짜 부호 바뀜은 무시",
      not _fr(flipper + [_trial(FB, 3232.0, -0.02, tau=0.05), _trial(FB, 3233.0, +0.006)]))
check("메모 2 ④ — 같은 시행이 정밀하면 셈(부호 바뀜 2 번)",
      _fr(flipper + [_trial(FB, 3232.0, -0.02, tau=1e-4), _trial(FB, 3233.0, +0.006)]))

# ⑦ C152 메모 3 — 마무리 사격(SHOOT_TOL)이 안 닫히면 닫히고 닿은 가까운 시행으로 바꾼다 · 표지 · 상한 없음
def _run_finish(fail):
    """y = 0.9 ln(T_c/1650), 위에서 단조로 다가감(괄호 없음 · C138 대체 없음): 시행 2000 · 1682.05 · 1653.18 K.
    T_TOL 3e-2 · T_SURFACE_TOL 5e-2 로 고리가 느슨한 시행 1653.18 K 에서 끝나 마무리 사격을 탄다. 닿는 다른 시행은 1682.05 K 뿐.
    fail(T_c) 이 참이면 SHOOT_TOL 사격이 안 닫힌다(mass(p_c) 뜀의 꼴)."""
    real, tt, ts = interior._shoot_pressure, interior.T_TOL, interior.T_SURFACE_TOL

    def fake(*a, t_center=None, t_pot=None, p_hint=None, tol=None, **k):
        st = _fake_st(t_center, T_POT * (t_center / 1650.0) ** 0.9)
        st.finish_subst = None
        return st, not (tol <= interior.SHOOT_TOL and fail(t_center))
    interior._shoot_pressure, interior.T_TOL, interior.T_SURFACE_TOL = fake, 3e-2, 5e-2
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            st, ok = interior.shoot(6e24, 0.3, 0.0, "fe_prem", potential_temperature=T_POT)
        return "answer", (st.t_center, ok, st.finish_subst)
    except (ValueError, eos.PhaseGap) as e:
        return "refusal", str(e)
    finally:
        interior._shoot_pressure, interior.T_TOL, interior.T_SURFACE_TOL = real, tt, ts


k_n, v_n = _run_finish(lambda t: False)
check("메모 3 ④ — 마무리 사격이 닫히면 대체 길에 안 들어감", k_n == "answer" and v_n[1] and v_n[2] is None, str(v_n)[:90])
k_f, v_f = _run_finish(lambda t: t > 1600.0)
check("메모 3 ② — 닫히는 후보가 없으면 오늘의 결과(미수렴 거절)", k_f == "refusal" or k_f == "answer" and not v_f[1], str(v_f)[:90])
k_s, v_s = _run_finish(lambda t: t < 1670.0)
check("메모 3 ③ — 먼 쪽만 닫히면 그 시행이 답, 대체가 기록됨",
      k_s == "answer" and v_s[1] and v_s[2] is not None and abs(v_s[2][0] - 1653.18) < 0.01 and abs(v_s[2][1] - 1682.05) < 0.01
      and v_s[0] == v_s[2][1], str(v_s)[:120])
_kv = interior._finish_subst_values(types.SimpleNamespace(finish_subst=None))
check("메모 3 — 대체 없으면 네 칸 모두 None", set(_kv) == {"finish_subst_from_tc", "finish_subst_to_tc", "finish_subst_delta_tc",
                                                    "finish_subst_y"} and all(v is None for v in _kv.values()))

from payload import Result, tagged_with_unconverged  # noqa: E402
from state import BodyState  # noqa: E402


def _consumer(substituted):
    st = BodyState(name="fixture", kind="planet")
    vals = {"radius": 1.13, "converged": True, "substituted_solvers": substituted, "trial_unconverged": ["interior._shoot_pressure"],
            **interior._finish_subst_values(types.SimpleNamespace(finish_subst=(3227.76165, 3227.76004, -9.2e-7)))}
    st.record("interior_layers", Result(recipe="interior-structure", version="0", regime="solved", reason="fixture",
                                        grade="calibrated", inputs={}, values=vals, units={k: "" for k in vals}))
    st.current_node = "tidal_heating"
    st["radius"]
    return tagged_with_unconverged(Result(recipe="tidal-heating", version="0", regime="fixed_q", reason="fixture",
                                          grade="measured", inputs={}, values={"power": 1.0}, units={"power": "W"}), st)


_c = _consumer([])
check("메모 3 ⑦ — 마무리 대체는 «best-of-budget» 표지도 등급 상한도 없음", _c.unconverged_inputs == () and _c.grade == "measured",
      f"{_c.unconverged_inputs} · {_c.grade}")
_c = _consumer(["interior._t_loop@시행3"])
check("메모 3 ⑦ 음성 — 같은 결과를 note_substituted 길로 적으면 표지와 상한이 붙음",
      _c.unconverged_inputs == ("best-of-budget:interior_layers.radius",) and _c.grade == "judgment",
      f"{_c.unconverged_inputs} · {_c.grade}")

# ⑧ C152 메모 4 — 부호는 오차 밖에서만 읽는다: 느슨한(τ > τ_lin) 첫 사격의 반대 부호는 Brent 괄호를 못 연다 · 규칙 3/4 선후
def _run_tol(y_of, wall=None):
    """y_of(T_c, tol) → ln(T_surf/T_pot). 결과 · Brent 호출 수 · 벽 찾기 사격 수."""
    real, rb, nb = interior._shoot_pressure, rootfind.brent, [0]
    w0 = interior.WALL_LOCATE_SHOTS[0]

    def fake(*a, t_center=None, t_pot=None, p_hint=None, tol=None, **k):
        if wall is not None and t_center > wall:
            raise eos.PhaseGap("fake_envelope", 1e9, "가짜 뜨거운 벽", temperature_k=t_center, too_cold=False)
        return _fake_st(t_center, T_POT * math.exp(y_of(t_center, tol))), True

    def bspy(*a, **k):
        nb[0] += 1
        return rb(*a, **k)
    interior._shoot_pressure, rootfind.brent = fake, bspy
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            st, ok = interior.shoot(6e24, 0.3, 0.0, "fe_prem", potential_temperature=T_POT)
        out = ("answer", (st.t_center, ok))
    except (ValueError, eos.PhaseGap) as e:
        out = ("refusal", str(e))
    finally:
        interior._shoot_pressure, rootfind.brent = real, rb
    return out, nb[0], interior.WALL_LOCATE_SHOTS[0] - w0


_y = lambda t: 0.9 * math.log(t / 2100.0)                 # 참 근 2100 K, 출발 2000 K 의 위
(k_w, v_w), nb_w, _ = _run_tol(lambda t, tol: _y(t) + (0.06 if tol > interior.SIGN_TAU_LIN else 0.0))
check("메모 4 ① — 느슨한 첫 사격의 반대 부호(따뜻한 지구 꼴)는 괄호를 못 열고 참 근에서 답", k_w == "answer" and v_w[1]
      and abs(v_w[0] / 2100.0 - 1.0) < 1e-5 and nb_w == 0, f"{str(v_w)[:80]} · brent {nb_w}")
_tl0, _sm0 = interior.SIGN_TAU_LIN, interior.SIGN_S_MAX
interior.SIGN_TAU_LIN, interior.SIGN_S_MAX = 1.0, 0.0     # 규칙 끔: 느슨한 시행도 부호를 읽음(925e1851 의 꼴)
_tr0 = interior.TIGHT_RERUN
interior.TIGHT_RERUN = False                              # C152 메모 6 도 끔 — 이 대조는 메모 4 만의 몫을 본다
try:
    (k_o, v_o), nb_o, _ = _run_tol(lambda t, tol: _y(t) + (0.06 if tol > _tl0 else 0.0))
    interior.TIGHT_RERUN = True
    (k_o8, v_o8), _nb_o8, _ = _run_tol(lambda t, tol: _y(t) + (0.06 if tol > _tl0 else 0.0))
finally:
    interior.SIGN_TAU_LIN, interior.SIGN_S_MAX = _tl0, _sm0
    interior.TIGHT_RERUN = _tr0
check("메모 4 ① 끔 · 메모 6 켬 [기록] — 메모 4 를 꺼도 메모 6 이 그 가짜 괄호를 SHOOT_TOL 고리로 다시 돌려 답(두 규칙이 겹쳐 지킴)",
      k_o8 == "answer" and abs(v_o8[0] / 2100.0 - 1.0) < 1e-5, str(v_o8)[:60])
check("메모 4 ① 끔 대조 — 같은 꼴에서 τ 규칙을 끄면 가짜 괄호로 «잔차가 뛴다» 거절(규칙이 지키는 것)",
      k_o == "refusal" and "잔차가 뛴다" in v_o, str(v_o)[:80])
(k_t, v_t), nb_t, _ = _run_tol(lambda t, tol: _y(t) + (0.06 if t >= 1990.0 else 0.0))
check("메모 4 ① 음성 — 같은 반대 부호가 정밀한 시행이면 괄호가 열려 «잔차가 뛴다» 로 거절", k_t == "refusal" and "잔차가 뛴다" in v_t
      and nb_t >= 1, f"{str(v_t)[:80]} · brent {nb_t}")
(k_r, v_r), nb_r, _ = _run_tol(lambda t, tol: 1.8 * math.log(t / 2100.0))   # 선형 잔차: Brent 첫 걸음이 근에 바로 떨어짐(|y| ≤ S_max·τ)
check("메모 4 ③ — Brent 요청이 오차 안(근 위)에 떨어지면 SHOOT_TOL 재사격이 닿아 답, 거절 아님",
      k_r == "answer" and v_r[1] and abs(v_r[0] / 2100.0 - 1.0) < 1e-6 and nb_r >= 1, f"{str(v_r)[:80]} · brent {nb_r}")
(k_3, v_3), nb_3, ws_3 = _run_tol(lambda t, tol: _y(t))
check("메모 4 ② — 괄호도 벽도 없는 고리(규칙 3): Brent 0 · 벽 찾기 0", k_3 == "answer" and nb_3 == 0 and ws_3 == 0,
      f"{str(v_3)[:60]} · brent {nb_3} · 벽 {ws_3}")
(k_4, v_4), nb_4, ws_4 = _run_tol(lambda t, tol: 0.5 * math.log(t / 3000.0), wall=2050.0)
check("메모 4 ② — 괄호 없이 벽을 만나면 규칙 4 가 이김: 벽 찾기 사격 > 0", k_4 == "refusal" and nb_4 == 0 and ws_4 > 0,
      f"{str(v_4)[:60]} · brent {nb_4} · 벽 {ws_4}")

# ⑩ C152 메모 6 — 느슨한 통과 · 빡빡한 놓침: 뜀 · 예산 거절은 SHOOT_TOL 고리만 낸다. 빡빡한 y 는 매끈(근 2100 K, 기울기 S),
#   느슨한 시행은 −B·τ 로 치우친다(화성 1850 K: S 147 · τ 3.0e-3 에서 −0.0107). J 는 빡빡해도 남는 진짜 뜀.
def _y8(S, B, J=0.0):
    return lambda t, tol: (0.3 * math.tanh(S * math.log(t / 2100.0) / 0.3) + (J if t > 2100.0 else -J)
                           - (B * tol if tol > interior.SHOOT_TOL else 0.0))


def _run8(y_of, on=True):
    keep, k0 = interior.TIGHT_RERUN, interior.TIGHT_RECHECKS[0]
    interior.TIGHT_RERUN = on
    try:
        out, _nb, _ws = _run_tol(y_of)
    finally:
        interior.TIGHT_RERUN = keep
    return out, interior.TIGHT_RECHECKS[0] - k0


(k8, v8), n8 = _run8(_y8(30.0, 3.5))
check("메모 6 ① — 느슨한 끝이 괄호를 잘못 잡은 «뜀» 은 SHOOT_TOL 고리로 다시 돌아 참 근에서 답",
      k8 == "answer" and v8[1] and abs(v8[0] / 2100.0 - 1.0) < 1e-5 and n8 == 1, f"{str(v8)[:60]} · 다시 {n8}")
(k8o, v8o), n8o = _run8(_y8(30.0, 3.5), on=False)
check("메모 6 ① 끔 대조 — 같은 꼴에서 스위치를 끄면 «잔차가 뛴다» 거절(실제 화성 1850 K 의 꼴)",
      k8o == "refusal" and "잔차가 뛴다" in v8o and n8o == 0, str(v8o)[:60])
(k8b, v8b), n8b = _run8(_y8(100.0, 2.0))
check("메모 6 ② — 느슨한 고리의 남은 예산만 물려받은 이어 돌기의 예산 거절은 새 예산의 SHOOT_TOL 고리로 다시 돌아 답",
      k8b == "answer" and v8b[1] and abs(v8b[0] / 2100.0 - 1.0) < 1e-5 and n8b == 1, f"{str(v8b)[:60]} · 다시 {n8b}")
(k8bo, v8bo), _ = _run8(_y8(100.0, 2.0), on=False)
check("메모 6 ② 끔 대조 — 스위치를 끄면 예산 거절", k8bo == "refusal" and "예산 안에" in v8bo, str(v8bo)[:60])
(k8j, v8j), n8j = _run8(_y8(100.0, 2.0, J=0.01))
check("메모 6 음성 — 빡빡해도 남는 뜀(±1 %)은 SHOOT_TOL 고리로 다시 돈 뒤에도 «잔차가 뛴다» 로 거절",
      k8j == "refusal" and "잔차가 뛴다" in v8j and n8j == 1, f"{str(v8j)[:60]} · 다시 {n8j}")
(k8t, v8t), n8t = _run8(_y8(30.0, 3.5, J=0.01))
check("메모 6 음성 — 괄호 두 끝이 이미 SHOOT_TOL 시행이면 다시 돌지 않고 그대로 거절",
      k8t == "refusal" and "잔차가 뛴다" in v8t and n8t == 0, f"{str(v8t)[:60]} · 다시 {n8t}")

# ⑨ C157 — 피적분의 불연속은 이어지거나 찾아진다: 차분 발판은 상 경계를 안 넘고 · 사건은 새 쪽에 착지 · 사격은 뜀을 이름 댄다
P_B = 23.83e9                                              # 가짜 두 상 재료의 경계(지구 en/PREM 자리)


class _TwoPhase(eos.Material):
    """C157 시험용 — 상 둘(경계 P_B 에서 밀도 +200 kg/m³), 각 상 안에서 dρ/dP = 1e-8 로 매끄러움."""

    def __init__(self, phases):
        object.__setattr__(self, "phases", phases)
        object.__setattr__(self, "name", "c157_two_phase")

    @property
    def shoot_lo(self):
        return 0.0

    def solid_density(self, p, t=0.0, t_pot=0.0):
        return 3000.0 + 1e-8 * p + (200.0 if p > P_B else 0.0)


_ph = [types.SimpleNamespace(p_min=1e9, p_max=P_B, gamma_sets=()), types.SimpleNamespace(p_min=P_B, p_max=1e12, gamma_sets=())]
_two, _one = _TwoPhase(_ph), _TwoPhase([types.SimpleNamespace(p_min=1e9, p_max=1e12, gamma_sets=())])
_p = P_B - 1e6                                             # 경계 아래 h(2.4 MPa) 안
_k_ref = _two.solid_density(_p) / 1e-8                     # 상 안의 참 K_T = ρ / (dρ/dP)
_lo, _hi = interior._phase_stencil(_two, _p, _p - _p * 1e-4, _p + _p * 1e-4, _p * 1e-4)
check("C157 ① — 경계 h 안에서 발판이 상 구간 안으로 잘림", _hi <= P_B and _lo >= _ph[0].p_min and _hi - _lo > 0.0, f"[{_lo:.6e}, {_hi:.6e}]")
check("C157 ① — 잘린 k_t 는 상 안의 값(경계를 걸친 차분과 같지 않음)", abs(_two.k_t(_p) / _k_ref - 1.0) < 1e-6, f"{_two.k_t(_p) / _k_ref:.9f}")
check("C157 ① 음성 — 상 하나로 보면(자르기 없음) 발판이 경계를 걸쳐 K_T 가 10 배 넘게 틀어짐", _one.k_t(_p) < 0.1 * _k_ref,
      f"{_one.k_t(_p) / _k_ref:.3e}")

_seamed = _TwoPhase([types.SimpleNamespace(p_min=1e9, p_max=1e12, gamma_sets=(
    types.SimpleNamespace(p_min=19e9, p_max=35e9), types.SimpleNamespace(p_min=35e9, p_max=float("inf"))))])
check("C157 메모 1 C — 열 세트 이음매도 경계: 19 · 35 GPa 사이의 구간을 냄", _seamed.stencil_bounds(25e9) == (19e9, 35e9)
      and _seamed.stencil_bounds(19e9 * (1 - 4e-12))[1] == 19e9, str(_seamed.stencil_bounds(25e9)))
check("C157 메모 1 C — 걸음 자르기 경계(_cut_floor)가 이음매를 봄, 재료 바닥은 안 봄",
      interior._cut_floor(_seamed, 25e9) == 19e9 and interior._cut_floor(_seamed, 10e9) == 0.0)

# 수락 3(메모 1 D) — 적분 수준: 코어 없는 0.05 M⊕ 시험체, T_c 2300 K(고상선 9.05 · 3.0 GPa 를 지남), p_c 를 단계 교차 자리에 걸쳐 훑음
def _sweep_y(bounds):
    keep = interior.STENCIL_BOUNDS
    interior.STENCIL_BOUNDS = bounds
    try:
        ys = []
        for i in range(6, 16):
            st = interior.integrate(15.0e9 + i * 0.002e9, 0.05 * interior.EARTH_MASS_KG, 0.0, 0.0, "fe_prem", 0.0, None, 0.0, 0.0,
                                    1.0, True, 2300.0, 1900.0)
            ys.append(math.log(st.t_surface / 1900.0))
    finally:
        interior.STENCIL_BOUNDS = keep
    d = sorted(b - a for a, b in zip(ys, ys[1:]))
    md = d[len(d) // 2]
    return max(abs(x - md) for x in d)


_on, _off = _sweep_y(True), _sweep_y(False)
check("C157 수락 3 — 녹는 경계를 지나는 적분의 y 가 p_c 에 이어짐(이웃 2 MPa, |dy − 중앙| ≤ 1e-6)", _on <= 1e-6, f"{_on:.2e}")
check("C157 수락 3 음성 — C157 앞 발판(STENCIL_BOUNDS = False)이면 뜀(> 1e-5)", _off > 1e-5, f"{_off:.2e}")

_M, _P0 = 6e24, 3.5e11


def _jump_integ(jump, short_marker=None, short_surface=True):
    def f(p, mass_kg, *a, **k):
        above = p > _P0 * 1.0000001
        return types.SimpleNamespace(mass_kg=_M * (p / _P0) ** 0.3 * (1.0 + (jump if above else 0.0)),
                                     surface_reached=True if above else short_surface,
                                     p_center=p, floor_truncated=None if above else short_marker, t_surface=1000.0)
    return f


def _shot(jump, tol, short_marker=None, short_surface=True):
    real = interior.integrate
    interior.integrate = _jump_integ(jump, short_marker, short_surface)
    try:
        st, ok = interior._shoot_pressure(_M * 1.0000001 ** 0.3 * (1.0 + jump / 2.0), 0.3, 0.0, "fe_prem",
                                          t_center=3000.0, t_pot=1600.0, tol=tol)
        return "answer", ok
    except ValueError as e:
        return "refusal", str(e)
    finally:
        interior.integrate = real


k9, v9 = _shot(1e-5, interior.SHOOT_TOL)
check("C157 ③ — 목표가 겉질량 뜀(1e-5) 안이면 이름 대며 거절", k9 == "refusal" and "사격 질량이 p_c 에서 뛴다" in v9, str(v9)[:80])
k9, v9 = _shot(0.0, interior.SHOOT_TOL)
check("C157 ③ 음성 — 같은 함수가 매끄러우면 닫힘", k9 == "answer" and v9 is True, str(v9))
k9, v9 = _shot(1e-5, 1e-3)
check("C157 ③ — 허용(1e-3)보다 작은 뜀은 느슨한 사격이 오늘처럼 닫음(문턱은 그 사격의 허용)", k9 == "answer" and v9 is True, str(v9))

# C157 메모 2 — 짧은 끝이 이름 댄 잘림 표지(floor_truncated)를 들면 뒷받침은 물러나 ok False, 표지 없이 멈춘 끝은 그대로 섬
k9, v9 = _shot(0.25, interior.SHOOT_TOL, short_marker=("fe_core_fit_test", 6.716e9, 0.9986), short_surface=False)
check("C157 메모 2 — 짧은 끝이 적합 바닥 잘림(floor_truncated)이면 뒷받침이 안 서고 오늘처럼 ok False", k9 == "answer" and v9 is False,
      str(v9)[:60])
k9, v9 = _shot(0.25, interior.SHOOT_TOL, short_marker=None, short_surface=False)
check("C157 메모 2 음성 — 표지 없이 표면 못 닿은 짧은 끝은 여전히 이름 대며 거절", k9 == "refusal" and "사격 질량이 p_c 에서 뛴다" in v9,
      str(v9)[:60])

# C157 한 스위치(PC 발견: 규칙 3 대상 416) — STENCIL_BOUNDS = False 면 eos.Material.k_t 도 C157 앞 식과 비트까지 같고, 사격 뒷받침도 꺼진다
def _kt_pre_c157(m, p):
    h = p * 1e-4
    rho = m.solid_density(p)
    p_hi, p_lo = min(p + h, m.p_max), max(p - h, 1.0, m.shoot_lo)
    d_hi, d_lo = m.solid_density(p_hi), m.solid_density(p_lo)
    return 0.0 if d_hi <= d_lo else rho * (p_hi - p_lo) / (d_hi - d_lo)


_keep = interior.STENCIL_BOUNDS
try:
    interior.STENCIL_BOUNDS = False
    _kt_off, _kt_old = _two.k_t(_p), _kt_pre_c157(_two, _p)
    _shot_off = _shot(1e-5, interior.SHOOT_TOL)
finally:
    interior.STENCIL_BOUNDS = _keep
check("C157 한 스위치 — False 면 발판이 경계를 만나는 자리의 k_t 가 C157 앞 식과 비트까지 같음(eos 쪽 자르기도 꺼짐)",
      _kt_off == _kt_old and _kt_off != _two.k_t(_p), f"{_kt_off!r} vs {_kt_old!r}")
check("C157 한 스위치 — False 면 사격 뒷받침도 꺼져 뜀 앞에서 오늘처럼 ok False", _shot_off == ("answer", False), str(_shot_off)[:60])

print(f"  test_rootfind — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
