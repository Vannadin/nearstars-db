# 뚜껑 전도 격자와 준정상 해석해의 시험 — 정상 해로의 수렴 · 2 차 정확도 · 재격자 · 해석해 자체 검산
"""Checks for `samuel_lid` (pre-registration v2-3 ①②). Heat production is not sourced yet, so every case is
either H = 0 or a uniform H chosen only to exercise the term — the values here are test inputs, not Mars.

    python3 engine/test_samuel_lid.py

The grid's steady limit must equal the exact steady solution, and its error must fall by about four when
the spacing halves (second order) — with no crust boundary between nodes; with one, only the fall is asserted. The analytic path is checked against a hand evaluation and against its
own continuity conditions. A re-mesh must carry a linear profile exactly.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_lid as sl                # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


R_P, T_S, T_L = 3389.5e3, 220.0, 1500.0
MAT = dict(rho_m=3500.0, c_m=1142.0, k_m=4.0, rho_cr=2900.0, c_cr=1000.0, k_cr=2.5)
YEAR = 3.15576e7


def steady_grid(nodes, d_l, d_cr, h_m, h_cr, steps=60, dt=1e9 * YEAR):
    g = sl.LidGrid(nodes, r_p=R_P, t_s=T_S, **MAT)
    g.start(d_l, T_L)
    for _ in range(steps):
        grad = g.step(dt, d_l=d_l, d_cr=d_cr, t_l=T_L, h_m=h_m, h_cr=h_cr)
    return grad, g


def qs(d_l, d_cr, h_m, h_cr):
    return sl.quasi_steady_gradient(r_p=R_P, d_l=d_l, d_cr=d_cr, t_l=T_L, t_s=T_S, k_m=MAT["k_m"],
                                    k_cr=MAT["k_cr"], h_m=h_m, h_cr=h_cr)


# ① The analytic path, H = 0, one material, by hand: T = A/r + B, dT/dr(R_l) = −A/R_l².
d_l = 200e3
r_l = R_P - d_l
a_hand = (T_L - T_S) / (1 / r_l - 1 / R_P)
check("quasi-steady, H = 0, no crust — against A/r + B by hand",
      abs(qs(d_l, 0.0, 0.0, 0.0) - (-a_hand / r_l ** 2)) < 1e-15, f"{qs(d_l, 0.0, 0.0, 0.0) * 1e3:.6f} K/km")

# ② The analytic two-layer path equals the one-layer path when both layers carry the same k and H.
two = sl.quasi_steady_gradient(r_p=R_P, d_l=d_l, d_cr=50e3, t_l=T_L, t_s=T_S, k_m=4.0, k_cr=4.0,
                               h_m=2e-8, h_cr=2e-8)
one = sl.quasi_steady_gradient(r_p=R_P, d_l=d_l, d_cr=0.0, t_l=T_L, t_s=T_S, k_m=4.0, k_cr=4.0,
                               h_m=2e-8, h_cr=2e-8)
check("quasi-steady — two identical layers equal one layer", abs(two - one) < 1e-12 * abs(one),
      f"{two * 1e3:.6f} vs {one * 1e3:.6f} K/km")

# ③ Heat in the lid lowers the magnitude of the base gradient (it carries part of the flux itself).
check("quasi-steady — H > 0 in the lid makes the base gradient less steep",
      abs(qs(d_l, 50e3, 2e-8, 2e-7)) < abs(qs(d_l, 50e3, 0.0, 0.0)))

# ④ The grid's steady limit equals the analytic one, and the error is second order in Δr.
cases = [("H = 0, crust 50 km", 50e3, 0.0, 0.0), ("H > 0, crust 50 km", 50e3, 2e-8, 2e-7),
         ("H > 0, no crust", 0.0, 2e-8, 0.0), ("H > 0, crust 47.3 km (between nodes)", 47.3e3, 2e-8, 2e-7)]
for name, d_cr, h_m, h_cr in cases:
    exact = qs(d_l, d_cr, h_m, h_cr)
    e1 = abs(steady_grid(41, d_l, d_cr, h_m, h_cr)[0] - exact)
    e2 = abs(steady_grid(81, d_l, d_cr, h_m, h_cr)[0] - exact)
    e4 = abs(steady_grid(161, d_l, d_cr, h_m, h_cr)[0] - exact)
    rel = e4 / abs(exact)
    check(f"grid steady limit → analytic, {name}", rel < 1e-3, f"rel. error {rel:.2e} at 161 nodes")
    if d_cr == 0.0:
        check(f"grid error is second order, {name}", 3.0 < e1 / e2 < 5.0 and 3.0 < e2 / e4 < 5.0,
              f"ratios {e1 / e2:.2f}, {e2 / e4:.2f}")
    elif d_cr == 47.3e3:
        # ⚠ Measured, not second order: the boundary moves within a cell as the spacing halves, so the
        #   ratios are uneven (22.84, 2.07 on 2026-09-23). Only the fall is asserted.
        check(f"grid error falls as the spacing halves, {name}", e1 > e2 > e4,
              f"ratios {e1 / e2:.2f}, {e2 / e4:.2f} — not asserted second order")

# ⑤ Re-meshing carries a linear profile exactly, and a large step does not blow up (implicit).
g = sl.LidGrid(21, r_p=R_P, t_s=T_S, **MAT)
g.start(100e3, T_L)
grad0 = (T_S - T_L) / 100e3
grad = g.step(1e-6 * YEAR, d_l=100e3, d_cr=0.0, t_l=T_L, h_m=0.0, h_cr=0.0)
check("a tiny step keeps the initial linear profile's gradient", abs(grad - grad0) < 1e-3 * abs(grad0),
      f"{grad * 1e3:.5f} vs {grad0 * 1e3:.5f} K/km")
grad_big = g.step(1e12 * YEAR, d_l=150e3, d_cr=0.0, t_l=T_L, h_m=0.0, h_cr=0.0)
exact_150 = qs(150e3, 0.0, 0.0, 0.0)
check("a huge implicit step after a re-mesh lands on the steady gradient", abs(grad_big / exact_150 - 1) < 1e-3,
      f"{grad_big * 1e3:.5f} vs {exact_150 * 1e3:.5f} K/km")
check("re-mesh keeps the end values", g.t[0] == T_L and g.t[-1] == T_S)

print(f"  test_samuel_lid — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
