# 액체 MgSiO₃ 의 RTpress 상태방정식 — Wolf & Bower 2018 식을 원자당(N = 1)으로 직접 옮기고 Luo & Deng 2025 Table 1 을 꽂는 모듈 (C120)
"""RTpress liquid MgSiO₃ (pre-registration `prereg-c120-melt.md`, frozen 4d574381).

Equations are Wolf & Bower 2018, PEPI 278, 59–74, written per atom (N = 1): V in Å³/atom, energies and the
thermal coefficients bₙ in eV/atom («all bn parameters retain units of energy», after their eq. (10)), k_B in eV/K,
pressure in GPa. The one unit conversion is eV/Å³ → GPa (×160.2177), applied alike to every energy term.
Nothing is copied from the RTpress package or from PALEOS — each quantity is written from the equation named
beside it. No electronic term (their App. C): Luo & Deng's Table 1 carries none, their AIMD already uses the
Mermin functional.

Parameters: Luo & Deng 2025, JGR Planets 130, e2024JE008678, Table 1 «This study» — fitted to AIMD at
0–1200 GPa · 2200–14 000 K. Calls outside that window return values and are counted (`OUTSIDE`).

Convention: S₀ = 0, so E(V₀, T₀) = E₀ (Wolf & Bower eq. (5) with the entropy constant dropped; it cancels
in P, C_V, γ and every other derivative).
"""
from __future__ import annotations

import math

K_B = 8.617333262e-5          # eV/K
PV = 160.2176634              # GPa·Å³ per eV
AMU = 1.66053906660e-27       # kg
M_ATOM = 100.3887 / 5.0       # g/mol per atom of MgSiO₃ (Mg 24.305 + Si 28.085 + 3 × O 15.999)

# Luo & Deng 2025 Table 1, «This study»
T0, M, V0, K0, KP0, E0 = 3000.0, 0.6, 14.352, 13.53, 6.767, -6.399
GAMMA0, GAMMAP0 = 0.158, -1.710
B = (1.763, 0.982, 2.11, 0.37, 1.9)
WINDOW_P, WINDOW_T = (0.0, 1200.0), (2200.0, 14000.0)
CV_KIN = 1.5 * K_B            # (B.3), N = 1
A1 = 6.0 * GAMMA0                                      # (7)
A2 = -12.0 * GAMMA0 + 36.0 * GAMMA0 ** 2 - 18.0 * GAMMAP0

OUTSIDE = {"calls": 0, "outside": 0, "loop": 0}


# ── reference isotherm, Vinet (6) ─────────────────────────────────────────
def _eta():
    return 1.5 * (KP0 - 1.0)


def p0t(v: float) -> float:
    """P₀T(V) = 3K₀ x⁻² (1 − x) e^{η(1−x)} [GPa], x = (V/V₀)^{1/3} — eq. (6)."""
    x = (v / V0) ** (1.0 / 3.0)
    return 3.0 * K0 * x ** -2 * (1.0 - x) * math.exp(_eta() * (1.0 - x))


def f0t(v: float) -> float:
    """F₀T(V) = 9K₀V₀/η² (1 + [η(1−x) − 1] e^{η(1−x)}) + E₀ [eV/atom] — eq. (6), K₀V₀ converted by PV."""
    x = (v / V0) ** (1.0 / 3.0)
    eta = _eta()
    return 9.0 * K0 * V0 / eta ** 2 * (1.0 + (eta * (1.0 - x) - 1.0) * math.exp(eta * (1.0 - x))) / PV + E0


# ── reference adiabat (7) and its Grüneisen parameter ─────────────────────
def _strain(v: float) -> float:
    return 0.5 * ((V0 / v) ** (2.0 / 3.0) - 1.0)


def t0s(v: float) -> float:
    """T₀S(V) = T₀ √(1 + a₁f + ½a₂f²) — eq. (7)."""
    f = _strain(v)
    return T0 * math.sqrt(1.0 + A1 * f + 0.5 * A2 * f * f)


def gamma0s(v: float) -> float:
    """γ₀S = −d ln T₀S / d ln V along the reference adiabat, from eq. (7): df/d ln V = −(2f + 1)/3."""
    f = _strain(v)
    return (2.0 * f + 1.0) * (A1 + A2 * f) / (6.0 * (1.0 + A1 * f + 0.5 * A2 * f * f))


# ── Rosenfeld–Tarazona thermal terms (8)–(12), App. B ─────────────────────
def b_of(v: float) -> float:
    """b(V) = Σ bₙ (V/V₀ − 1)ⁿ [eV/atom] — eq. (10)."""
    u = v / V0 - 1.0
    return sum(bn * u ** n for n, bn in enumerate(B))


def db_of(v: float) -> float:
    """b′(V) = Σ n bₙ (V/V₀ − 1)^{n−1} / V₀ [eV/atom/Å³] — eq. (B.2)."""
    u = v / V0 - 1.0
    return sum(n * bn * u ** (n - 1) for n, bn in enumerate(B) if n) / V0


def f_t(t: float) -> float:
    """f_T = (T/T₀)^m − 1 — eq. (9)."""
    return (t / T0) ** M - 1.0


def f_t1(t: float) -> float:
    """f_T⁽¹⁾ = (m/T₀)(T/T₀)^{m−1} — eq. (B.1)."""
    return (M / T0) * (t / T0) ** (M - 1.0)


def c_v(v: float, t: float) -> float:
    """C_V = b(V)·f_T⁽¹⁾ + 3/2·k_B [eV/K/atom] — eq. (B.4), N = 1."""
    return b_of(v) * f_t1(t) + CV_KIN


def entropy(v: float, t: float) -> float:
    """S(V, T) = S₀ + ΔS(V, T₀S → T), S₀ = 0 — eqs. (5), (12)."""
    ts = t0s(v)
    return b_of(v) / (M - 1.0) * (f_t1(t) - f_t1(ts)) + CV_KIN * math.log(t / ts)


def energy(v: float, t: float) -> float:
    """E(V, T) = F₀T(V) + T₀·S(V, T₀) + ΔE(V, T₀ → T) [eV/atom] — eqs. (5), (11)."""
    return f0t(v) + T0 * entropy(v, T0) + b_of(v) * (f_t(t) - f_t(T0)) + CV_KIN * (t - T0)


def free_energy(v: float, t: float) -> float:
    """F = E − T·S — eq. (4)."""
    return energy(v, t) - t * entropy(v, t)


def _ds_dv(v: float, t: float) -> float:
    """(∂S/∂V)_T = b′/(m−1)·[f_T⁽¹⁾(T) − f_T⁽¹⁾(T₀S)] + γ₀S·C_V(V, T₀S)/V [eV/K/Å³] — derivative of eq. (12)
    with dT₀S/dV = −γ₀S T₀S/V; this is also (∂P/∂T)_V (Maxwell)."""
    ts = t0s(v)
    return db_of(v) / (M - 1.0) * (f_t1(t) - f_t1(ts)) + gamma0s(v) * c_v(v, ts) / v


def pressure(v: float, t: float) -> float:
    """P = P₀T(V) + ΔP_E + ΔP_S [GPa] — eqs. (13)–(14):
    ΔP_E = −b′(V)·Δf_T(T₀ → T); ΔP_S = T·(∂S/∂V)_T − T₀·(∂S/∂V)_{T₀}."""
    dpe = -db_of(v) * (f_t(t) - f_t(T0))
    dps = t * _ds_dv(v, t) - T0 * _ds_dv(v, T0)
    return p0t(v) + (dpe + dps) * PV


def dpdt_v(v: float, t: float) -> float:
    """(∂P/∂T)_V [GPa/K] = (∂S/∂V)_T (Maxwell)."""
    return _ds_dv(v, t) * PV


def gruneisen(v: float, t: float) -> float:
    """γ = V (∂P/∂T)_V / C_V — thermodynamic definition (their eq. (1))."""
    return v * _ds_dv(v, t) / c_v(v, t)


def k_t(v: float, t: float, h: float = 1e-5) -> float:
    """K_T = −V (∂P/∂V)_T [GPa]. ⚠ Central difference of the analytic P (step h·V) — the paper prints no K_T
    expression; the one numerical derivative in the module."""
    dv = h * v
    return -v * (pressure(v + dv, t) - pressure(v - dv, t)) / (2.0 * dv)


def derived(v: float, t: float) -> dict:
    """ρ [kg/m³] · P · K_T · K_S [GPa] · α [1/K] · γ · c_V · c_P [J/kg/K] · ∇_ad."""
    p, kt, g = pressure(v, t), k_t(v, t), gruneisen(v, t)
    alpha = dpdt_v(v, t) / kt
    cv = c_v(v, t)
    cp = cv + t * v * alpha * alpha * kt / PV          # eV/K/atom
    ks = kt * (1.0 + alpha * g * t)
    per_kg = 1.602176634e-19 / (M_ATOM * 1e-3 / 6.02214076e23)
    return {"rho": M_ATOM * 1e-3 / 6.02214076e23 / (v * 1e-30), "p": p, "k_t": kt, "k_s": ks, "alpha": alpha,
            "gamma": g, "c_v": cv * per_kg, "c_p": cp * per_kg, "nabla_ad": g * p / ks if ks > 0 else 0.0}


MATERIAL = "rtpress_mgsio3_liquid"
N_GRID = 64                   # 덧붙임 2 B.1 — log-uniform V grid on [0.2, 1.6]·V₀ (neighbour ratio 8^(1/63) = 1.034)


def _v_min(t: float, v_a: float, v_b: float) -> float:
    """덧붙임 2 B.2 — the first minimum of P(V) between two grid points: bisect the sign change of
    g = (∂P/∂V)_T (central difference, step 1e-6·V) to a width below 1e-9·V₀."""
    def g(v):
        dv = 1e-6 * v
        return pressure(v + dv, t) - pressure(v - dv, t)
    lo, hi = v_a, v_b
    while hi - lo >= 1e-9 * V0:
        mid = 0.5 * (lo + hi)
        if g(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ── 덧붙임 3 (frozen 4fc1b0c1): V_min(T) table, checks, false position — cost only ──────
T_TAB = [300.0 * (20000.0 / 300.0) ** (k / 240) for k in range(241)]
_VMIN_TAB: list | None = None        # per T: (V_min, monotone?) — built on the first call


def _dpdv(v: float, t: float) -> float:
    dv = 1e-6 * v
    return (pressure(v + dv, t) - pressure(v - dv, t)) / (2.0 * dv)


def _vmin_full(t: float):
    """덧붙임 2 B.1–B.2 for one T: (V_min, False) at the first minimum from the small-V side, or (1.6·V₀, True)."""
    grid = [0.2 * V0 * 8.0 ** (i / (N_GRID - 1)) for i in range(N_GRID)]
    pg = [pressure(v, t) for v in grid]
    for i in range(1, N_GRID - 1):
        if pg[i] - pg[i - 1] < 0.0 <= pg[i + 1] - pg[i]:
            return _v_min(t, grid[i - 1], grid[i + 1]), False
    return grid[-1], True


def _table():
    global _VMIN_TAB
    if _VMIN_TAB is None:
        _VMIN_TAB = [_vmin_full(tk) for tk in T_TAB]
    return _VMIN_TAB


def _vmin_hat(t: float):
    """ln T linear interpolation of V_min; None when either neighbour is monotone or T is off the table."""
    tab = _table()
    if not (T_TAB[0] <= t <= T_TAB[-1]):
        return None
    x = math.log(t / T_TAB[0]) / math.log(T_TAB[-1] / T_TAB[0]) * 240
    k = min(int(x), 239)
    (va, ma), (vb, mb) = tab[k], tab[k + 1]
    if ma or mb:
        return None
    u = x - k
    return va + u * (vb - va)


def _false_position(p: float, t: float, lo: float, hi: float) -> float:
    """Illinois false position on [lo, hi]; stops on bracket width < 1e-12·V₀ only; bisection after 60 steps."""
    f_lo, f_hi = pressure(lo, t) - p, pressure(hi, t) - p
    side, it = 0, 0
    while hi - lo >= 1e-12 * V0:
        it += 1
        if it > 60:
            mid = 0.5 * (lo + hi)
        else:
            mid = (lo * f_hi - hi * f_lo) / (f_hi - f_lo)
            if not (lo < mid < hi):
                mid = 0.5 * (lo + hi)
        f = pressure(mid, t) - p
        if (f > 0.0) == (f_lo > 0.0):
            lo, f_lo = mid, f
            if side == -1:
                f_hi *= 0.5
            side = -1
        else:
            hi, f_hi = mid, f
            if side == 1:
                f_lo *= 0.5
            side = 1
    return 0.5 * (lo + hi)


def volume(p: float, t: float) -> float:
    """덧붙임 3: bracket [0.2·V₀, V̂_min] from the V_min(T) table, three checks, false position; any check failing
    sends this call back to `volume_full` (덧붙임 2 B entire, counted as `fallback`). Values equal to `volume_full`
    within the frozen check (|ΔV|/V < 1e-10, same refusals)."""
    vh = _vmin_hat(t)
    if vh is None:
        return volume_full(p, t)
    lo = 0.2 * V0
    if not (pressure(vh, t) <= p and _dpdv(vh * (1.0 - 1e-3), t) < 0.0 and pressure(lo, t) >= p):
        OUTSIDE["fallback"] = OUTSIDE.get("fallback", 0) + 1
        return volume_full(p, t)
    OUTSIDE["calls"] += 1
    if not (WINDOW_P[0] <= p <= WINDOW_P[1] and WINDOW_T[0] <= t <= WINDOW_T[1]):
        OUTSIDE["outside"] += 1
    OUTSIDE["loop"] = OUTSIDE.get("loop", 0) + 1
    OUTSIDE.setdefault("loop_first", (p, t))
    v = _false_position(p, t, lo, vh)
    if not _dpdv(v, t) < 0.0:
        OUTSIDE["fallback"] = OUTSIDE.get("fallback", 0) + 1
        OUTSIDE["calls"] -= 1
        return volume_full(p, t)
    return v


def volume_full(p: float, t: float) -> float:
    """V(P, T) on the mechanically stable branch (∂P/∂V)_T < 0 only (덧붙임 2, frozen 0cb19a20).
    If P(V) is monotone on the 64-point grid over [0.2, 1.6]·V₀ the bracket is that interval (as frozen in 1.1);
    otherwise it is [0.2·V₀, V_min] at the first minimum from the small-V side. No root → `eos.PhaseGap`, named.
    Counts calls outside the calibration window (`outside`) and calls that met a non-monotone P(V) (`loop`)."""
    import eos
    OUTSIDE["calls"] += 1
    if not (WINDOW_P[0] <= p <= WINDOW_P[1] and WINDOW_T[0] <= t <= WINDOW_T[1]):
        OUTSIDE["outside"] += 1
    grid = [0.2 * V0 * 8.0 ** (i / (N_GRID - 1)) for i in range(N_GRID)]
    pg = [pressure(v, t) for v in grid]
    lo, hi = grid[0], grid[-1]
    for i in range(1, N_GRID - 1):
        if pg[i] - pg[i - 1] < 0.0 <= pg[i + 1] - pg[i]:
            OUTSIDE["loop"] = OUTSIDE.get("loop", 0) + 1
            OUTSIDE.setdefault("loop_first", (p, t))
            hi = _v_min(t, grid[i - 1], grid[i + 1])
            p_min = pressure(hi, t)
            if p_min > p:
                raise eos.PhaseGap(MATERIAL, p * 1e9, (
                    f"rtpress: 이 (P, T) 에 역학적으로 안정한 액체 없음 — 안정 가지의 최저 압력 "
                    f"P(V_min) = {p_min:.4g} GPa at V/V₀ = {hi / V0:.4f} (T {t:.1f} K, 목표 {p:.4g} GPa)"), t)
            break
    g_lo, g_hi = pressure(lo, t) - p, pressure(hi, t) - p
    if g_lo * g_hi > 0.0:
        raise eos.PhaseGap(MATERIAL, p * 1e9, (
            f"rtpress: P {p:.4g} GPa at T {t:.1f} K has no root in V ∈ [{lo / V0:.3g}, {hi / V0:.4g}]·V₀ "
            f"(P spans {pressure(hi, t):.4g}–{pressure(lo, t):.4g} GPa)"), t)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        g = pressure(mid, t) - p
        if (g > 0.0) == (g_lo > 0.0):
            lo, g_lo = mid, g
        else:
            hi = mid
        if hi - lo < 1e-12 * V0:
            break
    return 0.5 * (lo + hi)


# ── engine hook (prereg-c120-melt 1.2 · 덧붙임 4) ─────────────────────────
_LAST_LIQUID = (None, None, None)
CALLS = 0                     # liquid() 호출 수 — 시험이 풀이 앞에 0 으로 두고 센다(C120 덧붙임 5 C.3)


def liquid(p_pa: float, t: float) -> tuple[float, float, float]:
    """(ρ [kg/m³], ∇_ad, c_P [J/kg/K]) of the liquid at (P [Pa], T) on the stable branch. Refusal is `eos.PhaseGap`.
    Remembers the last (P, T) only — the integrator asks density and slope at the same point in a row."""
    global _LAST_LIQUID, CALLS
    CALLS += 1
    key = (p_pa, t)
    if _LAST_LIQUID[0] == key:
        return _LAST_LIQUID[1]
    v = volume(p_pa / 1e9, t)
    d = derived(v, t)
    out = (d["rho"], d["nabla_ad"], d["c_p"])
    _LAST_LIQUID = (key, out, None)
    return out
