# 얼음 VII·X 의 French & Redmer 2015 열 세트 — 인쇄된 퍼텐셜을 우리가 미분한 것이 맞는가 (브리프 190)
"""Gate: the ice VII / ice X thermal set built from the paper's printed free energy.

    python3 engine/test_ice_fr2015.py

앵커는 실행 전에 적혔다 (`190-h2o-ice-thermal-prereg.md`, 8fb5c45c3fbfac9f):

J1  D(z) 구적이 급수 전개와 맞는다 — 작은 z 와 큰 z 양쪽에서.
J2  ⚠ **스플라인 대조는 열이 다르다.** SeaFreeze 의 `VII_X_French` 는 **PBE** 열이고 이 세트는
    **HSE** 다 (저자 권고, §VI p9). 그래서 이 검사는 **우리 산수**만 본다 — 같은 퍼텐셜의 두 평가가
    맞는가이고, 논문이 맞는가가 아니다. 시스템 파이썬에는 seafreeze 가 없으므로 게이트에서는
    이름을 대고 건너뛴다 (venv 에만 있다).
J3  창은 적합 격자다 — 안이면 `ok`, 압력이나 온도로 밖이면 `graded-extrapolation`.
J4  격자 안에서 c_p·γ·K_T 가 유한하고 양수다.
J5  **이 항목이 사는 것**: 오늘의 두 상수 답과 세트의 답이 같은 (P, T) 에서 얼마나 다른가 —
    인쇄만 하고 판정하지 않는다 (예측을 등록하지 않았다).
J6  `density_at` 가 압력을 되돌린다 (왕복 1e-6 상대).
"""
from __future__ import annotations

from pathlib import Path

import sys

import eos
import ice_fr2015 as F

GPA = 1e9


def _j7_every_integrate_counted(fails: list[str]) -> None:
    """J7 — 적분 한 번마다 그 구조의 격자 이탈 수가 남는가 (브리프 190 C).

    ⚠ **소스를 정규식으로 훑지 않는다** (감사석, 2026-09-13). «모든 호출부가 세는 판을 쓴다» 를
    글자로 지키면 줄 나눔·별칭·다른 모듈에서 조용히 새고, 같은 이름의 다른 함수(`core_history`
    에도 `integrate` 가 있다)를 세다가 엉뚱한 이유로 실패한다. 그래서 **행동**을 본다: 공개
    이름으로 한 번 부르고, 돌아온 구조에 자기 칸이 생겼는지 확인한다. 세지 않는 호출은 이제
    **적을 수가 없다** — `integrate` 자신이 세는 자리다."""
    import interior
    interior._ICE_GRID_DELTA.clear()
    st = interior.integrate(300e9, 1.0 * interior.EARTH_MASS_KG, 0.3, 0.0, "fe_prem",
                            t_center=3000.0, t_pot=1600.0)
    if id(st) not in interior._ICE_GRID_DELTA:
        fails.append("J7: `integrate` 가 돌려준 구조에 격자 이탈 칸이 없다 — "
                     "세는 자리가 공개 이름에서 빠졌다")
    if interior._integrate_raw is interior.integrate:
        fails.append("J7: `integrate` 가 세지 않는 원본 그대로다")


def _j8_seam_by_temperature(fails: list[str], notes: list[str]) -> None:
    """J8 — **세트의 이음매가 T 마다 정확히 한 번**이다 (C82-2, 2026-09-14).

    얼음 열 세트는 둘이고 경계가 상수였다. 이제 위끝은 **그 T 에서의 적합 사거리**
    `P(FIT_RHO_MAX, T)` 이고, 위 구간은 **그 자리에서** 시작한다. 둘이 같은 함수를 읽으니
    **틈도 겹침도 없어야** 하고, 그 「없음」을 **T 격자에서 실제로 밟아 본다** — 예전에는 둘이
    같은 상수를 읽어서 공짜로 맞았다.

    ⚠ **`t=None` 은 여기서 시험하지 않는다** — 그 경로의 답은 `engine/test_fe_hcp.py`@«「온도 모름」은 통과가 아니라 등급이다» 가 고정한
    C58·180 B 의 «온도 없이 물었을 때의 답» 이고, 이 시험의 주제가 아니다."""
    import eos as E
    ph = E.MATERIALS["h2o"].phase_at(100.0 * E.GPA)
    sets = [ts for ts in ph.gamma_sets if getattr(ts, "p_edge", "")]
    if len(sets) != 2:
        fails.append(f"J8 `p_edge` 를 단 얼음 세트가 {len(sets)} 개다 — 둘이어야 한다")
        return
    grid_t = [295.0, 400.0, 700.0, 1200.0, 1800.0, 2000.0, 2500.0]
    checked = 0
    for t in grid_t:
        edge = E.P_EDGE_EVALUATORS["fr2015_rho_edge"](t)
        probes = [edge * 0.5, edge - 1.0e6, edge, edge + 1.0e6, edge * 1.5]
        for q in probes:
            hit = [ts for ts in ph.gamma_sets if ts.covers(q, t)]
            checked += 1
            if len(hit) != 1:
                fails.append(f"J8 T {t:.0f} K · P {q / E.GPA:.4f} GPa 를 {len(hit)} 개 세트가 "
                             "덮는다 — 하나여야 한다 (틈이거나 겹침이다)")
    notes.append(f"  [기록 · C82-2] J8 이음매 — T 격자 {len(grid_t)} × 점 5 = {checked} 칸에서 "
                 f"덮는 세트가 언제나 하나. 위끝은 T 마다 다르다: "
                 f"{E.P_EDGE_EVALUATORS['fr2015_rho_edge'](295.0) / E.GPA:.4f} GPa @ 295 K · "
                 f"{E.P_EDGE_EVALUATORS['fr2015_rho_edge'](2000.0) / E.GPA:.4f} GPa @ 2000 K "
                 f"(선언 상수 {E.FR2015_FIT_P_MAX / E.GPA:.4f} 는 그 어느 끝도 아니다)")


def main() -> int:
    fails: list[str] = []
    notes: list[str] = []
    _j7_every_integrate_counted(fails)
    _j8_seam_by_temperature(fails, notes)

    # ── J1 ────────────────────────────────────────────────────────────────
    # D(z) → 1 − 3z/8 (z → 0) 이고, 큰 z 에서는 π⁴/(5z³).
    import math
    if abs(F._debye(1e-4) - (1.0 - 3e-4 / 8)) > 1e-8:
        fails.append(f"J1 D(z→0) = {F._debye(1e-4)!r}, 급수는 {1.0 - 3e-4/8!r}")
    big = F._debye(60.0)
    if abs(big / (math.pi ** 4 / (5 * 60.0 ** 3)) - 1.0) > 1e-6:
        fails.append(f"J1 D(60) = {big!r} 이 π⁴/(5z³) 과 1e-6 밖이다")

    # ── J2 ────────────────────────────────────────────────────────────────
    try:
        import seafreeze.seafreeze as S       # noqa: F401
        import numpy as np
        pt = np.empty((1,), dtype=object)
        pt[0] = (30000.0, 1000.0)             # MPa, K
        out = S.getProp(pt, "VII_X_French")
        rho_spline = float(out.rho[0]) / 1e3
        p_pbe = F.pressure(rho_spline, 1000.0, "PBE")
        k_pbe = F.k_t(rho_spline, 1000.0, "PBE")
        if abs(p_pbe / 30.0 - 1.0) > 1e-3:
            fails.append(f"J2 PBE 압력 {p_pbe:.4f} GPa 가 스플라인의 30.000 과 0.1 % 밖이다")
        if abs(k_pbe / (float(out.Kt[0]) / 1e3) - 1.0) > 2e-3:
            fails.append(f"J2 PBE K_T {k_pbe:.3f} 가 스플라인의 {float(out.Kt[0])/1e3:.3f} 과 0.2 % 밖이다")
        notes.append(f"  J2 스플라인(PBE) 대 우리 평가(PBE): P 30.000 / {p_pbe:.4f} GPa · "
                     f"K_T {float(out.Kt[0])/1e3:.2f} / {k_pbe:.2f} GPa — ⚠ **shipped column is HSE**, "
                     f"이 대조는 산수 검증이지 논문 검증이 아니다")
    except ImportError:
        notes.append("  [SKIP] J2 seafreeze 없음 (시스템 파이썬) — venv 에서만 돈다. "
                     "«안 돌았다» 이고 «통과» 가 아니다")

    # ── J3 ────────────────────────────────────────────────────────────────
    h2o = eos.MATERIALS["h2o"]
    for p_gpa, t_k, want in ((30.0, 1000.0, "ok"), (100.0, 1500.0, "ok"),
                             (400.0, 1500.0, "graded-extrapolation"),
                             (30.0, 2500.0, "graded-extrapolation")):
        ph = h2o.phase_at(p_gpa * GPA)
        got, _dens = ph.thermal_label("H2O-ice", p_gpa * GPA, t_k)
        if got != want:
            fails.append(f"J3 {p_gpa} GPa / {t_k} K: 판정 {got!r}, 등록된 것은 {want!r}")

    # ── J4 ────────────────────────────────────────────────────────────────
    for p_gpa in (5.0, 30.0, 100.0, 300.0):
        for t_k in (400.0, 1000.0, 1800.0):
            cp = h2o.c_p(p_gpa * GPA, t_k)
            gam = F.gruneisen(F.density_at(p_gpa, t_k), t_k)
            kt = F.k_t(F.density_at(p_gpa, t_k), t_k)
            for name, val in (("c_p", cp), ("gamma", gam), ("K_T", kt)):
                if not (val == val and abs(val) != float("inf") and val > 0.0):
                    fails.append(f"J4 {p_gpa} GPa / {t_k} K {name} = {val!r}")

    # ── J5 ────────────────────────────────────────────────────────────────
    # ⚠ 판정하지 않는다 — 예측을 등록하지 않았으므로 크기만 인쇄한다.
    rows = []
    for p_gpa, t_k in ((10.0, 500.0), (30.0, 1000.0), (150.0, 1500.0)):
        ph = h2o.phase_at(p_gpa * GPA)
        const_cv = ph.c_v_ref
        ev = F.thermal_at_hse(p_gpa * GPA, t_k)
        rows.append(f"{p_gpa:5.0f} GPa {t_k:5.0f} K  c_V 상수 {const_cv:7.1f} → 세트 {ev['c_v']:7.1f} "
                    f"J/(kg·K)  ({ev['c_v'] / const_cv - 1.0:+.1%})")
    notes.append("  J5 상수 대 세트 (판정 안 함):\n      " + "\n      ".join(rows))

    # ── J6 ────────────────────────────────────────────────────────────────
    for p_gpa, t_k in ((5.0, 400.0), (60.0, 1200.0), (250.0, 1800.0)):
        rho = F.density_at(p_gpa, t_k)
        back = F.pressure(rho, t_k)
        if abs(back / p_gpa - 1.0) > 1e-6:
            fails.append(f"J6 {p_gpa} GPa / {t_k} K: 되돌린 압력 {back!r}")

    for f in fails:
        print(f"  [FAIL] {f}")
    for n in notes:
        print(n)
    if not fails:
        print("  [PASS] 얼음 VII·X 열 세트 — J1 D(z) 양 끝 · J3 적합 격자 안팎의 등급 · "
              "J7 적분 한 번마다 그 구조의 격자 이탈 수가 남는다 (190 C) · "
              "J4 격자 안에서 유한·양수 · J6 압력 왕복 1e-6 · J2 는 venv 에서만, J5 는 인쇄만")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
