# 정체 뚜껑 안의 전도 — 2019 SI 식 (21) 음해 유한차분(본판)과 준정상 해석해(비교판), 뚜껑 바닥 기울기를 낸다
"""Conduction inside the stagnant lid, for the last term of 2019 SI eq. (20).

Pre-registration v2-3 (blob `1b6bb86c`), owner decision 2026-09-23 «ⓐ로 가고 ⓑ는 비교용으로 같이»:

* **`LidGrid` — the main path, as printed.** 2019 SI eq. (21), PDF p7:
  `ρ(r) C(r) ∂T/∂t = (1/r²) ∂/∂r (r² k(r) ∂T/∂r) + H(r)`, crust properties for `r > R_p − D_cr` and mantle
  properties elsewhere; *"discretized with an implicit finite-difference scheme … a regular grid … re-meshed
  at each time step … the previous time step is … linearly interpolated onto the new grid"*.
  Backward Euler in time, a conservative second-order stencil in radius, `T(R_p) = T_s` and `T(R_l) = T_l`.
* **`quasi_steady_gradient` — the comparison path, reported only.** The same equation with `∂T/∂t = 0`,
  solved exactly in one or two layers with a uniform `H` in each. It never enters the A0 verdict (v2-3 ②).

Both return `∂T/∂r` at `r = R_l` (negative when the lid is hotter at its base). The heat production is an
argument: `samuel_model.heat_production` still refuses, so nothing here chooses a value for it.

What the paper does not print, and is chosen here (named so a reader can contest it):

* the number of grid nodes — a constructor argument with no default;
* the base gradient is a second-order one-sided difference, `(−3T₀ + 4T₁ − T₂)/(2Δr)`;
* where the crust–mantle boundary falls between two nodes, the conductivity linking them is the series
  (length-weighted harmonic) mean over that interval, and a node's `ρC` and `H` are its cell's
  length-weighted mean;
* on re-meshing, a new node outside the old lid takes the nearer end value of the old profile.
"""
from __future__ import annotations


def _solve_tridiagonal(a: list, b: list, c: list, d: list) -> list:
    """Thomas algorithm: a[i] x[i-1] + b[i] x[i] + c[i] x[i+1] = d[i]."""
    n = len(d)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0], dp[0] = c[0] / b[0], d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def _interp(x_new: float, xs: list, ys: list) -> float:
    """Linear interpolation on an increasing grid; outside it, the nearer end value."""
    if x_new <= xs[0]:
        return ys[0]
    if x_new >= xs[-1]:
        return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x_new:
            lo = mid
        else:
            hi = mid
    w = (x_new - xs[lo]) / (xs[hi] - xs[lo])
    return ys[lo] + w * (ys[hi] - ys[lo])


class LidGrid:
    """The temperature profile in the lid, carried from step to step (2019 SI eq. (21))."""

    def __init__(self, nodes: int, *, r_p: float, t_s: float, rho_m: float, c_m: float, k_m: float,
                 rho_cr: float, c_cr: float, k_cr: float):
        if nodes < 3:
            raise ValueError(f"LidGrid needs at least 3 nodes for a second-order base gradient, got {nodes}")
        self.n = nodes
        self.r_p, self.t_s = r_p, t_s
        self.mantle = (rho_m * c_m, k_m)
        self.crust = (rho_cr * c_cr, k_cr)
        self.r: list | None = None
        self.t: list | None = None

    def start(self, d_l: float, t_l: float) -> None:
        """The initial profile: linear between T_l at the base and T_s at the surface."""
        self.r = [self.r_p - d_l + i * d_l / (self.n - 1) for i in range(self.n)]
        self.t = [t_l + (self.t_s - t_l) * i / (self.n - 1) for i in range(self.n)]

    def step(self, dt: float, *, d_l: float, d_cr: float, t_l: float, h_m: float, h_cr: float) -> float:
        """Re-mesh onto the lid of thickness `d_l`, advance one implicit step of `dt`, return ∂T/∂r at R_l."""
        if self.r is None:
            raise RuntimeError("LidGrid.step before LidGrid.start")
        r_new = [self.r_p - d_l + i * d_l / (self.n - 1) for i in range(self.n)]
        t_old = [_interp(x, self.r, self.t) for x in r_new]
        dr = d_l / (self.n - 1)
        r_crust = self.r_p - d_cr
        n = self.n
        a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
        b[0], d[0] = 1.0, t_l                      # T(R_l) = T_l
        b[-1], d[-1] = 1.0, self.t_s               # T(R_p) = T_s
        (rc_m, k_m), (rc_cr, k_cr) = self.mantle, self.crust

        def crust_len(lo: float, hi: float) -> float:
            return max(0.0, hi - max(lo, r_crust))

        for i in range(1, n - 1):
            ri = r_new[i]
            rm, rp = ri - dr / 2, ri + dr / 2
            f_cr = crust_len(rm, rp) / dr                      # crust share of this node's cell
            rho_c = f_cr * rc_cr + (1 - f_cr) * rc_m
            h = f_cr * h_cr + (1 - f_cr) * h_m
            # between two nodes, the conductivity that carries a 1-D flux exactly: dr / Σ (length / k)
            l_lo = crust_len(r_new[i - 1], ri)
            l_hi = crust_len(ri, r_new[i + 1])
            k_lo = dr / (l_lo / k_cr + (dr - l_lo) / k_m)
            k_hi = dr / (l_hi / k_cr + (dr - l_hi) / k_m)
            w_lo = rm * rm * k_lo / (ri * ri * dr * dr)
            w_hi = rp * rp * k_hi / (ri * ri * dr * dr)
            cap = rho_c / dt
            a[i], b[i], c[i] = -w_lo, cap + w_lo + w_hi, -w_hi
            d[i] = cap * t_old[i] + h
        self.r, self.t = r_new, _solve_tridiagonal(a, b, c, d)
        return (-3.0 * self.t[0] + 4.0 * self.t[1] - self.t[2]) / (2.0 * dr)


def quasi_steady_gradient(*, r_p: float, d_l: float, d_cr: float, t_l: float, t_s: float, k_m: float,
                          k_cr: float, h_m: float, h_cr: float) -> float:
    """∂T/∂r at R_l for the steady lid: each layer is T = −H r²/(6k) + A/r + B, with T(R_l) = T_l,
    T(R_p) = T_s, and T and k ∂T/∂r continuous at R_p − D_cr. A crust at least as thick as the lid
    makes the lid one crustal layer."""
    r_l = r_p - d_l
    if d_cr >= d_l or d_cr <= 0.0:
        k, h = (k_cr, h_cr) if d_cr >= d_l else (k_m, h_m)
        # T(r_l) = t_l, T(r_p) = t_s  →  A (1/r_l − 1/r_p) = t_l − t_s + h (r_l² − r_p²)/(6k)
        a = (t_l - t_s + h * (r_l ** 2 - r_p ** 2) / (6 * k)) / (1 / r_l - 1 / r_p)
        return -h * r_l / (3 * k) - a / r_l ** 2
    r_i = r_p - d_cr
    # unknowns A1, B1 (mantle part), A2, B2 (crust)
    m = [[1 / r_l, 1, 0, 0],
         [0, 0, 1 / r_p, 1],
         [1 / r_i, 1, -1 / r_i, -1],
         [-k_m / r_i ** 2, 0, k_cr / r_i ** 2, 0]]
    rhs = [t_l + h_m * r_l ** 2 / (6 * k_m),
           t_s + h_cr * r_p ** 2 / (6 * k_cr),
           h_m * r_i ** 2 / (6 * k_m) - h_cr * r_i ** 2 / (6 * k_cr),
           h_m * r_i / 3 - h_cr * r_i / 3]
    a1 = _solve4(m, rhs)[0]
    return -h_m * r_l / (3 * k_m) - a1 / r_l ** 2


def _solve4(m: list, v: list) -> list:
    """Gaussian elimination with partial pivoting, for the 4 × 4 continuity system."""
    n = len(v)
    aug = [row[:] + [v[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(col + 1, n):
            f = aug[r][col] / aug[col][col]
            for cc in range(col, n + 1):
                aug[r][cc] -= f * aug[col][cc]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (aug[r][n] - sum(aug[r][cc] * x[cc] for cc in range(r + 1, n))) / aug[r][r]
    return x
