# 기저층 안의 전도 — 2021 식 (21)–(22) 음해 유한차분, 층만 푸는 판 3(녹음 끔 3-0 · 켬 3-1), 두 경계 열류와 녹음까지 남은 거리를 낸다
"""Conduction inside the enriched basal layer, Samuel+ 2021 eqs. (21)–(22) — plate 3 of the thermal plan.

Pre-registration v2-20 (blob `f86a43d2`), variants **3-0** (melting term off) and **3-1** (on):

* (21), PDF p. 13: `ρ(r) C_pm ∂T/∂t = (k/r²) ∂/∂r (r² ∂T/∂r) + H(t, r) − ρ(r) L_m ∂φ(t, r)/∂t`, for
  `R_c ≤ r ≤ R_c + D_d`. Variant 3-0 drops the last term; 3-1 is built with `latent=` given.
* 3-1's melting curves (option A, «Samuel+ 2021's printed choice», PDF p. 14): the 2023 SI (9) solidus and
  liquidus of plate 2, each minus `6 (Fe_d(r) − Fe_m)`, with `Fe_d(r) = ‾Fe#_d f_e(r)`. ⚠ 2021 cites
  Elkins-Tanton 2008 eq. 2 for it; that equation has no iron-number term (v2-16 ③), so it is not cited here.
  `φ` is plate 2's clamped 2021 eq. (9).
* (22a) `ρ(r) = ρ_d f_e(r)`, (22b) `H(t, r) = H_d(t) f_e(r)`, PDF p. 14.
* `f_e(r)` from 2021 SI S5 (preprint PDF pp. 51–52): (S12) Fe#_d(r) linear in depth below `R_d`, (S14) its
  slope from the top value `Fe#_di` and the volume mean `‾Fe#_d`, (S15) `f_e = Fe#_d(r) / ‾Fe#_d`.
* `q_c = −k ∂T/∂r |_{R_c}`, `q_d = −k ∂T/∂r |_{R_c + D_d}`, second-order one-sided differences (PDF p. 14).
* `ρ_d` from 2021 SI (S3), PDF p. 46: `ρ_0 + ‾Fe#_d (ρ_Fe − ρ_Mg)` with Fe# as a fraction — **our
  arithmetic** (v2-20 §3): the fraction reading is fixed only by the 3500 kg/m³ check at Fe# 25.

The boundary temperatures `T(R_c) = T_c`, `T(R_d) = T_i` and the heating `H_d(t)` are **arguments** —
coupling the layer to the mantle budget ((18)–(20), T_i) is plate 4. `D_d` is fixed in time (2021 PDF p. 13
neglects erosion by plumes), so the grid never re-meshes.

`k` is `k_d` — ⚠ **our interpretation** (v2-20 §3): 2021 prints `k_m` in (21), `q_c` and `q_d`; 2023 SI §3
(PDF p. 11) introduces a layer conductivity `k_d`, read here as the layer's conductivity everywhere in it.

What is chosen here and not printed (named so a reader can contest it):

* the number of grid nodes — a constructor argument with no default;
* a node's `ρ` and `H` take `f_e` at the node (the layer is smooth, no interface falls between nodes);
* the starting profile is linear between `T_c` and `T_i` (plate 4 decides what the coupled run starts from);
* 3-1's implicit step linearises `φ(T)` about the last iterate and repeats (Newton on the piecewise-linear
  `φ`) until the largest change is below `MELT_TOL_K`, at most `MELT_MAX_ITER` times — a step that does not
  converge is refused, not returned.
"""
from __future__ import annotations

import samuel_model as sm
from samuel_lid import _solve_tridiagonal

#: 2021 SI S1 (preprint PDF p. 46), eq. (S3): ρ_d = ρ_0 + Fe# (ρ_Fe − ρ_Mg); ρ_0 is the Fe#_UL 25 plate's value.
RHO_0, RHO_FE, RHO_MG = 3268.56, 4192.2, 3266.0
#: 2021 SI S1 (preprint PDF p. 46): «Fe#_UL = 25 (precisely 24.9884 (Bertka & Fei, 1997))» — 2021's Fe_m.
FE_M = 24.9884
#: 2021 PDF p. 14 — the iron term's coefficient, K per Fe-number unit.
FE_SHIFT_K = 6.0
MELT_TOL_K, MELT_MAX_ITER = 1e-6, 50


def layer_density(fe_mean: float) -> float:
    """(S3) with the volume-mean Fe# as a fraction — our arithmetic, not a printed value (v2-20 §3)."""
    return RHO_0 + fe_mean / 100.0 * (RHO_FE - RHO_MG)


def fe_slope(r_c: float, d_d: float, fe_top: float, fe_mean: float) -> float:
    """(S14): dFe#_d/dh_d = 4 (R_d³ − R_c³)(‾Fe#_d − Fe#_di) / (R_d⁴ − R_c³ (4 R_d − 3 R_c))."""
    r_d = r_c + d_d
    return 4 * (r_d ** 3 - r_c ** 3) * (fe_mean - fe_top) / (r_d ** 4 - r_c ** 3 * (4 * r_d - 3 * r_c))


def enrichment(r: float, *, r_c: float, d_d: float, fe_top: float | None, fe_mean: float) -> float:
    """(S12) + (S15) inside the layer. `fe_top=None` is the uniform layer, f_e ≡ 1."""
    if fe_top is None:
        return 1.0
    r_d = r_c + d_d
    return (fe_top + (r_d - r) * fe_slope(r_c, d_d, fe_top, fe_mean)) / fe_mean


def basal_layer(d_d: float, **kw) -> "LayerGrid | None":
    """B1 (plate 3's share): `D_d = 0` means no layer — nothing is built and nothing is called."""
    return None if d_d == 0.0 else LayerGrid(d_d=d_d, **kw)


class LayerGrid:
    """The temperature profile in the basal layer, carried from step to step (2021 eq. (21), variants 3-0 / 3-1)."""

    def __init__(self, nodes: int, *, r_c: float, d_d: float, c_p: float, k_d: float, fe_mean: float,
                 fe_top: float | None, rho_d: float | None = None, latent: float | None = None,
                 pressure_gpa=None, fe_m: float = FE_M, iron_shift: bool = True, record: bool = False,
                 shift_k: float | None = None, curves: dict | None = None):
        if nodes < 3:
            raise ValueError(f"LayerGrid needs at least 3 nodes for second-order boundary fluxes, got {nodes}")
        if d_d <= 0.0:
            raise ValueError(f"LayerGrid needs D_d > 0, got {d_d} — D_d = 0 is `basal_layer` returning None (B1)")
        self.n, self.r_c, self.d_d, self.k = nodes, r_c, d_d, k_d
        self.fe_mean, self.fe_top = fe_mean, fe_top
        self.rho_d = layer_density(fe_mean) if rho_d is None else rho_d
        self.dr = d_d / (nodes - 1)
        self.r = [r_c + i * self.dr for i in range(nodes)]
        self.f = [enrichment(x, r_c=r_c, d_d=d_d, fe_top=fe_top, fe_mean=fe_mean) for x in self.r]
        self.rho_c = [self.rho_d * f * c_p for f in self.f]
        self.t: list | None = None
        self.latent = latent
        if latent is not None:
            if pressure_gpa is None:
                raise ValueError("variant 3-1 (latent given) needs pressure_gpa(r) for the melting curves")
            # option A shifts both curves by 6 (Fe_d − Fe_m); option B (v2-20 §4, a one-point comparison)
            # keeps Duncan's curve unshifted — Duncan+ 2018 measured one composition, Fe# ≈ 25
            k6 = shift_k if shift_k is not None else sm._default("fe_shift_k", FE_SHIFT_K)
            shift = [k6 * (fe_mean * f - fe_m) if iron_shift else 0.0 for f in self.f]
            p = [pressure_gpa(x) for x in self.r]
            self.p_gpa = p
            self.t_sol = [sm.solidus(pi, curves) - s for pi, s in zip(p, shift)]
            self.t_liq = [sm.liquidus(pi, curves) - s for pi, s in zip(p, shift)]
            self.phi: list | None = None
        self.iron_shift = iron_shift
        self.fe_m = fe_m
        self.margin: tuple | None = None           # D: (min T_sol − T, r, P, T, t)
        # D's record (v2-29): per step (t, max φ, molten volume fraction, min T_sol − T). Reads only.
        self.record = record
        self.history: list = []
        self.iterations_max = 0

    def describe(self) -> str:
        """J and the k_d line — printed on every run (v2-20 §5)."""
        top = "uniform (f_e ≡ 1)" if self.fe_top is None else f"Fe#_di {self.fe_top:g}"
        return (f"layer: D_d {self.d_d / 1e3:g} km · ‾Fe#_d {self.fe_mean:g} · {top} · mean weight: volume "
                f"(2021 SI S5 (S13)) · ρ_d {self.rho_d:.1f} kg/m³ (S3, our arithmetic) · "
                f"k_d {self.k:g} W/m/K — our interpretation (2023 SI §3 k_d) · "
                + ("variant 3-0 (melting off)" if self.latent is None else
                   (f"variant 3-1 (L_m {self.latent:g} J/kg, option A: 6 (Fe_d − Fe_m), Fe_m {self.fe_m}, "
                    f"«Samuel+ 2021's printed choice»)" if self.iron_shift else
                    f"variant 3-1 (L_m {self.latent:g} J/kg, option B: no Fe# shift — Duncan+ 2018 one point, "
                    f"a comparison; layer base P {max(self.p_gpa):.2f} GPa)")))

    def start(self, t_c: float, t_i: float) -> None:
        """The starting profile: linear between T_c at R_c and T_i at R_d (our choice)."""
        self.t = [t_c + (t_i - t_c) * i / (self.n - 1) for i in range(self.n)]
        if self.latent is not None:
            self.phi = [sm.melt_fraction(t, a, b) for t, a, b in zip(self.t, self.t_sol, self.t_liq)]

    def step(self, dt: float, *, t_c: float, t_i: float, h_d: float, t_now: float | None = None) -> tuple:
        """Advance one backward-Euler step of `dt`; return (q_c, q_d) in W/m², positive outward."""
        if self.t is None:
            raise RuntimeError("LayerGrid.step before LayerGrid.start")
        if self.latent is None:
            self.t = self._solve(dt, t_c, t_i, h_d, None)
        else:
            self._melt_step(dt, t_c, t_i, h_d)
            self._track_margin(t_now)
        return self.fluxes()

    def _melt_step(self, dt: float, t_c: float, t_i: float, h_d: float) -> None:
        """ρC (T − T⁰)/dt + ρL (φ(T) − φ⁰)/dt = diffusion + H, φ linearised about the last iterate."""
        t_k, phi_old = self.t[:], self.phi
        for it in range(1, MELT_MAX_ITER + 1):
            lin = []
            for i in range(self.n):
                a, b = self.t_sol[i], self.t_liq[i]
                slope = 1.0 / (b - a) if a < t_k[i] < b else 0.0
                phi_k = sm.melt_fraction(t_k[i], a, b)
                lin.append((slope, phi_k - slope * t_k[i] - phi_old[i]))
            t_new = self._solve(dt, t_c, t_i, h_d, lin)
            change = max(abs(x - y) for x, y in zip(t_new, t_k))
            t_k = t_new
            if change < MELT_TOL_K:
                self.iterations_max = max(self.iterations_max, it)
                self.t = t_k
                self.phi = [sm.melt_fraction(t, a, b) for t, a, b in zip(t_k, self.t_sol, self.t_liq)]
                return
        raise sm.Refused(f"layer melting step did not converge in {MELT_MAX_ITER} iterations "
                         f"(last change {change:.3e} K)")

    def _track_margin(self, t_now: float | None) -> None:
        """D — the smallest distance to the (iron-shifted) solidus, with where and when it fell."""
        i = min(range(self.n), key=lambda j: self.t_sol[j] - self.t[j])
        m = (self.t_sol[i] - self.t[i], self.r[i], self.p_gpa[i], self.t[i], t_now)
        if self.margin is None or m[0] < self.margin[0]:
            self.margin = m
        if self.record:
            w = [x * x for x in self.r]                     # volume weights ∝ r² on the uniform grid
            molten = sum(wi * p for wi, p in zip(w, self.phi)) / sum(w)
            self.history.append((t_now, max(self.phi), molten, m[0]))

    def _solve(self, dt: float, t_c: float, t_i: float, h_d: float, lin) -> list:
        n, dr, k = self.n, self.dr, self.k
        a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
        b[0], d[0] = 1.0, t_c                      # T(R_c) = T_c
        b[-1], d[-1] = 1.0, t_i                    # T(R_d) = T_i
        for i in range(1, n - 1):
            ri = self.r[i]
            rm, rp = ri - dr / 2, ri + dr / 2
            w_lo = rm * rm * k / (ri * ri * dr * dr)
            w_hi = rp * rp * k / (ri * ri * dr * dr)
            cap = self.rho_c[i] / dt
            a[i], b[i], c[i] = -w_lo, cap + w_lo + w_hi, -w_hi
            d[i] = cap * self.t[i] + h_d * self.f[i]
            if lin is not None:
                rho_l = self.rho_d * self.f[i] * self.latent / dt
                b[i] += rho_l * lin[i][0]
                d[i] -= rho_l * lin[i][1]
        return _solve_tridiagonal(a, b, c, d)

    def fluxes(self) -> tuple:
        """q_c and q_d from second-order one-sided differences of the current profile."""
        t, dr, k = self.t, self.dr, self.k
        g_c = (-3.0 * t[0] + 4.0 * t[1] - t[2]) / (2.0 * dr)
        g_d = (3.0 * t[-1] - 4.0 * t[-2] + t[-3]) / (2.0 * dr)
        return -k * g_c, -k * g_d


def steady_shell(r: float, *, r_c: float, d_d: float, t_c: float, t_i: float, k: float, h: float) -> tuple:
    """The exact steady solution for uniform H: T = −H r²/(6k) + A/r + B with T(R_c) = T_c, T(R_d) = T_i.
    Returns (T(r), −k dT/dr at r)."""
    r_d = r_c + d_d
    a = (t_c - t_i + h * (r_c ** 2 - r_d ** 2) / (6 * k)) / (1 / r_c - 1 / r_d)
    b = t_c + h * r_c ** 2 / (6 * k) - a / r_c
    return -h * r * r / (6 * k) + a / r + b, -k * (-h * r / (3 * k) - a / r ** 2)
