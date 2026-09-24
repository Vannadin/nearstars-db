# 기저층 전도 격자(판 3-0)의 시험 — 해석해 대조 P3-a · 경계 열류와 에너지 P3-b · B1 · J · k_d 인쇄 · (S14) 검산
"""Checks for `samuel_layer` (pre-registration v2-20 §5, variant 3-0). Every value here is a test input, not
Mars — `H_d` and `T_i` are plate 4's.

    python3 engine/test_samuel_layer.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_layer as lay             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


R_C, D_D, T_C, T_I = 1650e3, 300e3, 2100.0, 1950.0
C_P, K_D, FE_MEAN = 1142.0, 4.0, 96.97
H = 1e-7                                # W/m³ — a test input large enough to bend the profile by ~275 K
YEAR = 3.15576e7


def steady(nodes, fe_top=None, h=H, steps=80, dt=1e9 * YEAR):
    g = lay.LayerGrid(nodes, r_c=R_C, d_d=D_D, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=fe_top)
    g.start(T_C, T_I)
    for _ in range(steps):
        q = g.step(dt, t_c=T_C, t_i=T_I, h_d=h)
    return g, q


def exact(r):
    return lay.steady_shell(r, r_c=R_C, d_d=D_D, t_c=T_C, t_i=T_I, k=K_D, h=H)


# P3-a — the uniform-H steady state against the shell solution, and second order under halving.
err = {}
for n in (21, 41, 81):
    g, _ = steady(n)
    err[n] = max(abs(t - exact(r)[0]) for r, t in zip(g.r, g.t))
bend = max(abs(exact(R_C + x * D_D / 100)[0] - (T_C + (T_I - T_C) * x / 100)) for x in range(101))
scale = max(abs(exact(R_C + x * D_D / 100)[0]) for x in range(101))
check("P3-a — steady T against −H r²/(6k) + A/r + B, relative 1e-3", err[81] / scale < 1e-3,
      f"max |ΔT| {err[81]:.3e} K at 81 nodes · relative {err[81] / scale:.2e} · the H term bends the profile {bend:.1f} K")
r1, r2 = err[21] / err[41], err[41] / err[81]
check("P3-a — error falls ≈ 4× per halving (second order)", 3.5 < r1 < 4.5 and 3.5 < r2 < 4.5,
      f"21→41 {r1:.3f} · 41→81 {r2:.3f}")

# P3-b — boundary fluxes against the exact ones, second order, and the steady energy balance.
qerr = {}
for n in (21, 41, 81):
    g, (q_c, q_d) = steady(n)
    qerr[n] = (abs(q_c - exact(R_C)[1]), abs(q_d - exact(R_C + D_D)[1]))
    if n == 81:
        a_c, a_d = R_C ** 2, (R_C + D_D) ** 2
        vol = ((R_C + D_D) ** 3 - R_C ** 3) / 3               # all ÷ 4π
        bal = (q_d * a_d - q_c * a_c) / (H * vol)
        qs = (q_c, q_d)
check("P3-b — q_c, q_d against the exact fluxes", max(qerr[81]) / abs(exact(R_C + D_D)[1]) < 1e-3,
      f"q_c {qs[0] * 1e3:.4f} (exact {exact(R_C)[1] * 1e3:.4f}) · q_d {qs[1] * 1e3:.4f} (exact {exact(R_C + D_D)[1] * 1e3:.4f}) mW/m²")
fr = [qerr[a][j] / qerr[b][j] for a, b in ((21, 41), (41, 81)) for j in (0, 1)]
check("P3-b — flux error falls ≈ 4× per halving", all(3.5 < x < 4.5 for x in fr),
      " · ".join(f"{x:.3f}" for x in fr))
check("P3-b — energy: q_d A_d − q_c A_c = ∫ H dV (steady, 1e-3)", abs(bal - 1) < 1e-3, f"ratio {bal:.6f}")

# (S14) — the slope makes the volume mean equal ‾Fe#_d, checked by quadrature, not by the formula itself.
FE_TOP = 94.13
m = 20000
num = den = 0.0
for i in range(m):
    r = R_C + (i + 0.5) * D_D / m
    num += lay.enrichment(r, r_c=R_C, d_d=D_D, fe_top=FE_TOP, fe_mean=FE_MEAN) * r * r
    den += r * r
bottom = lay.enrichment(R_C, r_c=R_C, d_d=D_D, fe_top=FE_TOP, fe_mean=FE_MEAN) * FE_MEAN
check("(S14) — volume mean of f_e is 1", abs(num / den - 1) < 1e-8,
      f"{num / den:.10f} · Fe#_di {FE_TOP} → bottom Fe# {bottom:.3f}")
check("(S3) — ρ_d at ‾Fe#_d 96.97 and the 3500 check at 25", abs(lay.layer_density(96.97) - 4166.70) < 0.01
      and abs(lay.layer_density(25.0) - 3500.11) < 0.01,
      f"{lay.layer_density(96.97):.2f} · {lay.layer_density(25.0):.2f} kg/m³")

# Stratified layer, steady: energy still closes with ∫ H_d f_e dV = H_d V (volume mean 1).
g, (q_c, q_d) = steady(81, fe_top=FE_TOP)
bal_s = (q_d * (R_C + D_D) ** 2 - q_c * R_C ** 2) / (H * ((R_C + D_D) ** 3 - R_C ** 3) / 3)
check("stratified (Fe#_di 94.13) — steady energy closes", abs(bal_s - 1) < 1e-3, f"ratio {bal_s:.6f}")

# B1 — D_d = 0 builds nothing and calls nothing; the grid itself refuses it by name.
check("B1 — D_d = 0 → no layer", lay.basal_layer(0.0, nodes=21, r_c=R_C, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN,
                                                 fe_top=None) is None)
try:
    lay.LayerGrid(21, r_c=R_C, d_d=0.0, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=None)
    check("B1 — LayerGrid refuses D_d = 0", False)
except ValueError as e:
    check("B1 — LayerGrid refuses D_d = 0", "D_d" in str(e), str(e))

# J · k_d — printed on every run.
line = g.describe()
print(f"  [J] {line}")
check("J · k_d line carries Fe#_di, its weight and the k_d interpretation",
      "Fe#_di 94.13" in line and "volume" in line and "our interpretation" in line)

# ── Variant 3-1 (melting on, option A) ─────────────────────────────────────────────────────────────
L_M = 6e5                               # J/kg — plate 2's value (v2 §3)


def p_gpa(r):                           # test input: 19 GPa at R_c falling linearly to 16 GPa at R_d
    return 16.0 + 3.0 * (R_C + D_D - r) / D_D


def grid(latent, t_c, t_i, fe_top=FE_TOP, nodes=41):
    g = lay.LayerGrid(nodes, r_c=R_C, d_d=D_D, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=fe_top,
                      latent=latent, pressure_gpa=None if latent is None else p_gpa)
    g.start(t_c, t_i)
    return g


# 3-1 far below the solidus is 3-0, bit for bit (the linearised term adds exact zeros).
cold = [grid(None, 1500.0, 1400.0), grid(L_M, 1500.0, 1400.0)]
for _ in range(20):
    for g in cold:
        g.step(1e7 * YEAR, t_c=1500.0, t_i=1400.0, h_d=H, t_now=0.0)
check("3-1 below the solidus ≡ 3-0 (bit identical)", cold[0].t == cold[1].t and max(cold[1].phi) == 0.0,
      f"D: min T_sol − T {cold[1].margin[0]:.1f} K at r {cold[1].margin[1] / 1e3:.1f} km · P {cold[1].margin[2]:.2f} GPa")

# 3-1 through melting: heat the layer from below, compare with 3-0 on the way and at steady state.
hot = [grid(None, 2100.0, 1900.0), grid(L_M, 2100.0, 1900.0)]
lag = 0.0
for k in range(400):
    for g in hot:
        g.step(1e7 * YEAR, t_c=2500.0, t_i=1900.0, h_d=H, t_now=k * 1e7 * YEAR)
    if k == 20:
        lag = max(a - b for a, b in zip(hot[0].t, hot[1].t))
phi = hot[1].phi
check("3-1 melts, iterations converge, 0 ≤ φ ≤ 1", 0.0 < max(phi) <= 1.0 and min(phi) >= 0.0,
      f"max φ {max(phi):.3f} · most iterations in a step {hot[1].iterations_max} · "
      f"iron shift at the base {lay.FE_SHIFT_K * (FE_MEAN * hot[1].f[0] - lay.FE_M):.1f} K")
check("3-1 latent heat slows the heating (3-0 hotter at 0.2 Gyr)", lag > 0.1, f"largest lead {lag:.2f} K")
for _ in range(60):                     # the layer's diffusion time D²/κ is ≈ 3.4 Gyr — go well past it
    for g in hot:
        g.step(1e9 * YEAR, t_c=2500.0, t_i=1900.0, h_d=H)
steady_gap = max(abs(a - b) for a, b in zip(hot[0].t, hot[1].t))
check("3-1 steady state = 3-0 steady state (∂φ/∂t → 0)", steady_gap < 1e-6, f"{steady_gap:.2e} K after 64 Gyr")
print(f"  [J] {hot[1].describe()}")

try:
    lay.LayerGrid(21, r_c=R_C, d_d=D_D, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=None, latent=L_M)
    check("3-1 without pressure_gpa is refused", False)
except ValueError as e:
    check("3-1 without pressure_gpa is refused", "pressure_gpa" in str(e))

# D's record (v2-29): recording reads the profile and changes nothing — bit identical with it off.
pair = []
for rec in (False, True):
    g = lay.LayerGrid(41, r_c=R_C, d_d=D_D, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=FE_TOP, latent=L_M,
                      pressure_gpa=p_gpa, record=rec)
    g.start(2100.0, 1900.0)
    for k in range(60):
        g.step(1e7 * YEAR, t_c=2500.0, t_i=1900.0, h_d=H, t_now=k * 0.01)
    pair.append(g)
check("D record on ≡ off (bit identical)", pair[0].t == pair[1].t and pair[0].phi == pair[1].phi
      and pair[0].margin == pair[1].margin and len(pair[1].history) == 60 and pair[0].history == [],
      f"last record t {pair[1].history[-1][0]:.2f} · max φ {pair[1].history[-1][1]:.3f} · molten {pair[1].history[-1][2]:.3f}")

# Option B (a one-point comparison, v2-20 §4): no Fe# shift — the curves are plate 2's unshifted.
gb = lay.LayerGrid(21, r_c=R_C, d_d=D_D, c_p=C_P, k_d=K_D, fe_mean=FE_MEAN, fe_top=FE_TOP, latent=L_M,
                   pressure_gpa=p_gpa, iron_shift=False)
check("option B — solidus unshifted, base pressure printed",
      all(t == lay.sm.solidus(p) for t, p in zip(gb.t_sol, gb.p_gpa)) and "option B" in gb.describe()
      and max(gb.p_gpa) < 23.0, gb.describe().split(" · ")[-1])

print(f"  test_samuel_layer — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
