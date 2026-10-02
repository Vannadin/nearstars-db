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

print(f"  test_rootfind — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
