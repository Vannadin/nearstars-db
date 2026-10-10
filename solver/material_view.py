# 물질 기록 뷰 — 기록 하나를 솔버 규약(state · dtdp · seams · transitions)으로; 창 밖은 선언된 거절 또는 띠 Note (phase-2 등록 P3)
"""The view of one material record (rewrite/phase2-impl.frozen.md P3; design §I, D-M2; impl notes 1, 4).

`RecordView(record, t_pot)` answers what `LegacyView` answers, from the record's data alone:
- `density(p, t)`, `dtdp(p, t)`, `state(p, t) → (ρ, (dT/dP)_ad, notes) | Stop`, `porosity(p)`;
- `seams()` (phase windows, thermal-set seams, source seams) and `transitions()` (declared boundaries);
- out of a window: the edge's declared refusal as a Stop, or the value with a band Note — never a bare value.

The numerics follow the legacy path the record migrates (engine at 097a8aa3), so that impl P5's stage (a) can hold
within T1: the cold curves are Seager+ 2007 eqs (4)/(5) (2007ApJ...669.1279S p.1281), the density is the same Newton
inversion, K_T the same stencil difference, the reference adiabat the same PCHIP. Each is noted where it is written.

Forms built here: bm2, bme3, vinet. Not yet: table, library (P3 later steps); bme4 is not built (impl P3).
Evaluators: dorogokupets2017_liquid_fe (Sci. Rep. 7, 41863, eqs (1), (2), (9)–(17)), read from the record's params.
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from solver import material_checks as mc
from solver import material_library as ml
from solver import material_registry as mr
from solver import stepper as st
from solver.result import freeze

R_GAS = 8.314462618          # J/(mol·K), the value legacy fe_liquid uses (a formula input, not a read source)


def thaw_plain(x):
    """Plain dicts and lists from a record that may be frozen (mappingproxy / tuple) or plain."""
    if isinstance(x, Mapping):
        return {k: thaw_plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [thaw_plain(v) for v in x]
    return x


def _v(c) -> float:
    return float(c["value"])


@dataclass(frozen=True)
class RecordRefusal:
    """A declared refusal from a record's edge (D-M2): which record, where, and the registry id it declared."""
    material_id: str
    p: float
    t: float
    refusal: str
    why: str


@dataclass(frozen=True)
class BandNote:
    """A declared band surfaced with a value (design §I): it never changes the value."""
    material_id: str
    edge: str
    form: str
    error: float | None
    method: str | None
    grade: str
    origin: str


# ── PCHIP in ln P: the same algorithm as legacy smooth_table at 097a8aa3 (Fritsch–Carlson) ────────────────────────────
def _end_slope(h0, h1, d0, d1):
    s = ((2.0 * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
    if s * d0 <= 0.0:
        return 0.0
    if d0 * d1 < 0.0 and abs(s) > 3.0 * abs(d0):
        return 3.0 * d0
    return s


def _inner_slope(h0, h1, d0, d1):
    if d0 * d1 <= 0.0:
        return 0.0
    w1, w2 = 2.0 * h1 + h0, h1 + 2.0 * h0
    return (w1 + w2) / (w1 / d0 + w2 / d1)


def _pchip(x, xs, ys):
    """Inside the table: monotone cubic Hermite; outside: straight along the end PCHIP slope (C¹)."""
    n = len(xs)
    if x <= xs[0]:
        return ys[0] + _edge_slope(xs, ys, False) * (x - xs[0])
    if x >= xs[-1]:
        return ys[-1] + _edge_slope(xs, ys, True) * (x - xs[-1])
    lo, hi = 0, n - 1
    while hi - lo > 1:                                   # bisect: xs[lo] <= x < xs[hi]
        mid = (lo + hi) // 2
        if xs[mid] <= x:
            lo = mid
        else:
            hi = mid
    i = lo
    x0, x1, y0, y1 = xs[i], xs[i + 1], ys[i], ys[i + 1]
    t = (x - x0) / (x1 - x0)
    if t == 0.0:
        return y0
    h = x1 - x0
    d = (y1 - y0) / h
    if i >= 1:
        hl = x0 - xs[i - 1]
        m0 = _inner_slope(hl, h, (y0 - ys[i - 1]) / hl, d)
    elif i + 2 < n:
        hr = xs[i + 2] - x1
        m0 = _end_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    else:
        m0 = d
    if i + 2 < n:
        hr = xs[i + 2] - x1
        m1 = _inner_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    elif i >= 1:
        hl = x0 - xs[i - 1]
        m1 = _end_slope(h, hl, d, (y0 - ys[i - 1]) / hl)
    else:
        m1 = d
    t2, t3 = t * t, t * t * t
    return ((2.0 * t3 - 3.0 * t2 + 1.0) * y0 + (t3 - 2.0 * t2 + t) * h * m0
            + (-2.0 * t3 + 3.0 * t2) * y1 + (t3 - t2) * h * m1)


def _edge_slope(xs, ys, right):
    if len(xs) < 3:
        return (ys[-1] - ys[-2]) / (xs[-1] - xs[-2]) if right else (ys[1] - ys[0]) / (xs[1] - xs[0])
    if right:
        h0, h1 = xs[-1] - xs[-2], xs[-2] - xs[-3]
        return _end_slope(h0, h1, (ys[-1] - ys[-2]) / h0, (ys[-2] - ys[-3]) / h1)
    h0, h1 = xs[1] - xs[0], xs[2] - xs[1]
    return _end_slope(h0, h1, (ys[1] - ys[0]) / h0, (ys[2] - ys[1]) / h1)


# ── cold curves (Seager+ 2007, 2007ApJ...669.1279S p.1281, eqs (4) and (5)); bm2 is eq. (5) at K0' = 4 ────────────────
def _cold_pressure(form: str, rho0: float, k0: float, k0p: float):
    c = 1.5 * k0
    if form == "bm2":
        return lambda rho: c * ((rho / rho0) ** (7.0 / 3.0) - (rho / rho0) ** (5.0 / 3.0))
    if form == "bme3":
        a = 0.75 * (k0p - 4.0)
        return lambda rho: (c * ((rho / rho0) ** (7.0 / 3.0) - (rho / rho0) ** (5.0 / 3.0))
                            * (1.0 + a * ((rho / rho0) ** (2.0 / 3.0) - 1.0)))
    if form == "vinet":
        def p(rho):
            eta13 = (rho / rho0) ** (-1.0 / 3.0)                  # η^{-1/3}, η = ρ/ρ0
            return 3.0 * k0 * (rho / rho0) ** (2.0 / 3.0) * (1.0 - eta13) * math.exp(1.5 * (k0p - 1.0) * (1.0 - eta13))
        return p
    raise ValueError(f"form {form!r} is not built in this view")


# ── evaluators: printed formulas over the record's params ───────────────────────────────────────────────────────────
class Dorogokupets2017Liquid:
    """Dorogokupets+ 2017 (2017NatSR...741863D) eqs (1), (2), (9)–(17) for one Table 1 column, from the record's params
    (each a constant as read). Supplies (∂P/∂T)_V, c_V and γ at (P, T). Same arithmetic as legacy fe_liquid at 097a8aa3,
    one formula unit per molar mass. The per-view cache is owned by the view (no module state)."""

    NEEDS = mr.EVALUATOR_PARAMS["dorogokupets2017_liquid_fe"]
    CACHE_MAX = 65536

    def __init__(self, params: Mapping):
        missing = [k for k in self.NEEDS if k not in params]
        if missing:
            raise ValueError(f"dorogokupets2017_liquid_fe needs params {missing}")
        g = {k: _v(params[k]) for k in self.NEEDS}
        self.__dict__.update(g)
        self.eta = 1.5 * self.k0p - 1.5
        self.cache: dict = {}

    def _gamma(self, x):
        return self.gamma_inf + (self.gamma0 - self.gamma_inf) * x ** self.beta

    def _theta(self, x):
        return self.theta0 * x ** (-self.gamma_inf) * math.exp((self.gamma0 - self.gamma_inf) / self.beta
                                                               * (1.0 - x ** self.beta))

    def pressure(self, v, t):
        x = v / self.v0
        xb = x ** self.beta
        th = self.theta0 * x ** (-self.gamma_inf) * math.exp((self.gamma0 - self.gamma_inf) / self.beta * (1.0 - xb))
        gam = self.gamma_inf + (self.gamma0 - self.gamma_inf) * xb
        nr = 3.0 * R_GAS
        p_th = nr * gam / v * th * (1.0 / (math.exp(th / t) - 1.0) - 1.0 / (math.exp(th / self.t_ref) - 1.0))
        p_el = self.g_el / v * 1.5 * R_GAS * self.e0 * x ** self.g_el * (t * t - self.t_ref * self.t_ref)
        xx = x ** (1.0 / 3.0)
        p_cold = 3.0 * self.k0 * xx ** -2 * (1.0 - xx) * math.exp(self.eta * (1.0 - xx))
        return p_cold + p_th + p_el

    def volume(self, p, t):
        """The same inversion as legacy: 8 halvings, Newton to 1 Pa inside the window, else 80 halvings."""
        lo, hi = 0.2 * self.v0, 1.5 * self.v0
        for _ in range(8):
            mid = 0.5 * (lo + hi)
            if self.pressure(mid, t) > p:
                lo = mid
            else:
                hi = mid
        v = 0.5 * (lo + hi)
        for _ in range(40):
            f = self.pressure(v, t) - p
            if abs(f) < 1.0:
                return v
            h = v * 1e-6
            dfdv = (self.pressure(v + h, t) - self.pressure(v - h, t)) / (2.0 * h)
            if dfdv == 0.0:
                break
            v_new = v - f / dfdv
            if not (0.2 * self.v0 < v_new < 1.5 * self.v0):
                break
            if abs(f / dfdv) < v * 1e-12:
                return v_new
            v = v_new
        lo, hi = 0.2 * self.v0, 1.5 * self.v0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if self.pressure(mid, t) > p:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def at(self, p, t) -> dict:
        key = (p, t)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        v = self.volume(p, t)
        x = v / self.v0
        u = self._theta(x) / t
        c_th = 3.0 * R_GAS * u * u * math.exp(u) / (math.exp(u) - 1.0) ** 2
        c_el = 3.0 * R_GAS * self.e0 * x ** self.g_el * t
        dpdt = self._gamma(x) * c_th / v + self.g_el * c_el / v
        out = {"dpdt_v": dpdt, "c_v": (c_th + c_el) / self.molar_mass, "gruneisen": dpdt * v / (c_th + c_el)}
        if len(self.cache) >= self.CACHE_MAX:            # 68 N17: bounded; values are pure, so clearing only costs time
            self.cache.clear()
        self.cache[key] = out
        return out


class FrenchRedmer2015:
    """French & Redmer 2015 (2015PhRvB..91a4308F) ices VII/X: f(ρ,T) = u_e(ρ) + u_n(ρ) + f_t(ρ,T), eqs (6), (9), (11),
    (12), (14), (15), Tables I (HSE), II, III. Coefficients are in the fit's own units as printed (ρ g/cm³, f kJ/g);
    this boundary converts: ρ in kg/m³ → g/cm³, p GPa → Pa, c_V kJ/(g·K) → J/(kg·K). The same arithmetic as legacy
    ice_fr2015 at 097a8aa3: 32-node Gauss–Legendre Debye integral, central differences (ΔT 1e-3·max(1, T/1000) K,
    Δρ 1e-6·max(1, ρ) g/cm³), the guarded-secant inversion to 1e-10 relative. The proton entropy s_p (eq. 10) is
    constant in ρ and left out (c8). Per-view state only (nodes, cache)."""

    NEEDS = mr.EVALUATOR_PARAMS["french_redmer2015"]
    CACHE_MAX = 65536

    def __init__(self, params: Mapping):
        missing = [k for k in self.NEEDS if k not in params]
        if missing:
            raise ValueError(f"french_redmer2015 needs params {missing}")
        g = {k: _v(params[k]) for k in self.NEEDS}
        self.ue = tuple(g[f"a{i}"] for i in range(6))
        self.un = tuple(g[f"b{i}"] for i in range(5))
        self.alpha = {(0, -k): g[f"alpha_0_m{k}"] for k in (4, 3, 2)}
        self.gamma = {(j, -k): g[f"gamma_{j}_m{k}"] for j in range(4) for k in (4, 3, 2)}
        self.t_d, self.t_e, self.a_d, self.a_e, self.k0 = g["t_d"], g["t_e"], g["a_d"], g["a_e"], g["k0"]
        self.rho_lo, self.rho_hi = g["rho_search_min"] / 1e3, g["rho_search_max"] / 1e3     # g/cm³
        self.nodes = self._gl_nodes(32)
        self.cache: dict = {}

    @staticmethod
    def _gl_nodes(n):
        out = []
        for k in range(n):
            x = math.cos(math.pi * (k + 0.75) / (n + 0.5))
            for _ in range(60):
                p0, p1 = 1.0, 0.0
                for j in range(n):
                    p0, p1 = ((2 * j + 1) * x * p0 - j * p1) / (j + 1), p0
                dp = n * (x * p0 - p1) / (x * x - 1.0)
                dx = -p0 / dp
                x += dx
                if abs(dx) < 1e-15:
                    break
            out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
        return tuple(out)

    def _debye(self, z):
        if z <= 0.0:
            return 1.0
        total = 0.0
        for x, w in self.nodes:
            t = 0.5 * z * (x + 1.0)
            total += 0.5 * z * w * (t ** 3 / math.expm1(t) if t > 0 else 0.0)
        return 3.0 * total / z ** 3

    def f(self, rho, t):                                   # kJ/g at ρ [g/cm³], T [K]
        a0, a1, a2, a3, a4, a5 = self.ue
        ln = math.log(rho)
        ue = a0 + a1 * rho + a2 * rho ** 2 + a3 * rho ** 3 + a4 * ln + a5 * ln ** 2
        b0, b1, b2, b3, b4 = self.un
        un = b0 + b1 * rho + b2 * rho ** 2 + b3 * math.exp(-b4 * rho ** 10)
        ft = 0.0
        for (i, k), a in self.alpha.items():
            ti = self.t_d * self.a_d ** i
            ft += a * t * (3.0 * math.log(-math.expm1(-ti / t)) - self._debye(ti / t)) * rho ** (k / self.k0)
        for (j, k), gm in self.gamma.items():
            tj = self.t_e * self.a_e ** j
            ft += gm * t * math.log(-math.expm1(-tj / t)) * rho ** (k / self.k0)
        return ue + un + ft

    def _p(self, rho, t):                                  # GPa
        h = 1e-6 * max(1.0, rho)
        return rho ** 2 * (self.f(rho + h, t) - self.f(rho - h, t)) / (2.0 * h)

    def _rho(self, p_gpa, t):
        lo, hi = self.rho_lo, self.rho_hi
        f_lo, f_hi = self._p(lo, t) - p_gpa, self._p(hi, t) - p_gpa
        if f_lo > 0.0 or f_hi < 0.0:
            return None                                    # outside the search bracket: the caller refuses
        a, b, fa = lo, hi, f_lo
        x0, f0, x1, f1 = lo, f_lo, hi, f_hi
        for _ in range(60):
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0) if f1 != f0 else 0.5 * (a + b)
            if not (a < x2 < b):
                x2 = 0.5 * (a + b)
            f2 = self._p(x2, t) - p_gpa
            if (fa < 0.0) != (f2 < 0.0):
                b = x2
            else:
                a, fa = x2, f2
            done = f2 == 0.0 or abs(x2 - x1) <= 1e-10 * abs(x2)
            x0, f0, x1, f1 = x1, f1, x2, f2
            if done:
                break
        return x1

    def at(self, p, t) -> dict:
        key = (p, t)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        rho = self._rho(p / 1e9, t)
        if rho is None:
            raise ValueError(f"french_redmer2015: {p:g} Pa at {t:g} K is outside the ρ search bracket")
        ht = 1e-3 * max(1.0, t * 1e-3)
        f0 = self.f(rho, t)
        cv = -t * (self.f(rho, t + ht) - 2.0 * f0 + self.f(rho, t - ht)) / ht ** 2
        dpdt = (self._p(rho, t + ht) - self._p(rho, t - ht)) / (2.0 * ht)
        hr = 1e-6 * max(1.0, rho)
        kt = rho * (self._p(rho + hr, t) - self._p(rho - hr, t)) / (2.0 * hr)
        out = {"dpdt_v": dpdt * 1e9, "c_v": cv * 1e6, "gruneisen": 0.0 if cv <= 0.0 else dpdt / (rho * cv),
               "k_t": kt * 1e9, "density": rho * 1e3}
        if len(self.cache) >= self.CACHE_MAX:
            self.cache.clear()
        self.cache[key] = out
        return out


EVALUATORS = MappingProxyType({"dorogokupets2017_liquid_fe": Dorogokupets2017Liquid,
                               "french_redmer2015": FrenchRedmer2015})


class _EvaluatorPhase:
    """An evaluator used as a phase's EOS: the same face as the library adapter (ρ, dT/dP), from the evaluator's ρ,
    γ, K_T and (∂P/∂T)_V: (dT/dP)_S = γT/K_S, K_S = K_T + (∂P/∂T)_V·γ·T. A failure is LibraryOutOfRange."""

    def __init__(self, ev):
        self.ev = ev

    def at(self, p, t):
        try:
            x = self.ev.at(p, t)
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            raise ml.LibraryOutOfRange(str(e)) from e
        k_s = x["k_t"] + x["dpdt_v"] * x["gruneisen"] * t
        return {"rho": x["density"], "dtdp": x["gruneisen"] * t / max(k_s, 1.0), "k_t": x["k_t"], "g": math.nan}


# ── the view ────────────────────────────────────────────────────────────────────────────────────────────────────────
@dataclass
class _Set:
    p_min: float
    p_max: float
    edge_limit: float | None
    edge_band: Mapping | None
    edge_refusal: str | None
    alpha_k: float
    alpha_k_dt: float
    c_v: float
    t_ref: float
    t_ref_kind: str
    evaluator: object = None


@dataclass
class _Phase:
    id: str
    p_min: float
    p_max: float
    t_min: float
    t_max: float
    cold: object
    rho0: float
    k0: float
    alpha_k: float
    alpha_k_dt: float
    c_v: float
    ref_kind: str
    t_ref_kind: str
    t_ref: float
    adiabat: tuple | None
    sets: list = field(default_factory=list)
    library: object = None
    gamma_window: tuple = (0.0, math.inf)
    constants_span: tuple | None = None
    edges: Mapping = field(default_factory=dict)


def _num(x) -> float:
    return float(x)


class RecordView:
    """One material record as the integrator sees it (P3). `t_pot` is the body's potential temperature; `p_stop` the
    outermost material's floor, as for LegacyView."""

    def __init__(self, record: Mapping, t_pot: float, p_stop: float = 0.0):
        self.material_id = record["id"]
        self.t_pot = float(t_pot)
        self.p_stop = float(p_stop)
        self.kind = record["kind"]
        # 68 N27: the view reads only its own frozen copy, so a later change by the caller cannot reach it
        self.record = freeze(copy.deepcopy(thaw_plain(record)))
        self.boundaries = tuple(self.record.get("boundaries", ()))
        self.phases = [self._phase(ph) for ph in self.record["phases"]]
        self.notes: list = []
        self._band_errors: dict = {}             # (phase index, set index) → the method's value, evaluated once

    # construction ─────────────────────────────────────────────────────────────────────────────────────────────────
    def _phase(self, ph):
        eos = ph["eos"]
        pr = eos.get("params", {})
        form = eos["form"]
        lib = None
        if form == "library":                       # note 1 §6: the pinned installed library, evaluated at runtime
            lib, cold = ml.SeaFreezePhase(eos["library"]["submodel"]), None
        elif form == "evaluator":                   # a potential gives ρ and its derivatives (c8: French & Redmer)
            lib, cold = _EvaluatorPhase(EVALUATORS[eos["evaluator"]["name"]](eos["evaluator"].get("params", {}))), None
        else:
            k0p = _v(pr["k0p"]) if "k0p" in pr else 4.0
            cold = _cold_pressure(form, _v(pr["rho0"]), _v(pr["k0"]), 4.0 if form == "bm2" else k0p)
        ref = eos["reference"]
        th = ph["thermal"]
        pc = th.get("pressure", {})
        ad = ref.get("adiabat")
        sets = []
        for s in th.get("sets", ()):
            k = s.get("constants") or {}
            ev = s.get("evaluator")
            e = s.get("edge_above")
            sets.append(_Set(p_min=_num(s["window"]["p_min"]), p_max=_num(s["window"]["p_max"]),
                             edge_limit=None if e is None else _num(e["limit"]),
                             edge_band=None if e is None else e["band"],
                             edge_refusal=None if e is None else e.get("refusal"),
                             alpha_k=_v(k["alpha_k"]) if "alpha_k" in k else 0.0,
                             alpha_k_dt=_v(k["alpha_k_dt"]) if "alpha_k_dt" in k else 0.0,
                             c_v=_v(k["c_v"]) if "c_v" in k else 0.0,
                             t_ref=_v(s["t_ref"]) if "t_ref" in s else 0.0,
                             t_ref_kind=s.get("t_ref_kind", "isotherm"),
                             evaluator=None if ev is None else EVALUATORS[ev["name"]](ev.get("params", {}))))
        w = ph["window"]
        gw = th.get("gamma_window") or {"p_min": 0.0, "p_max": math.inf}     # a library phase has none
        return _Phase(id=ph["id"], p_min=_num(w["p_min"]), p_max=_num(w["p_max"]),
                      t_min=_num(w.get("t_min", 0.0)), t_max=_num(w.get("t_max", 0.0)),
                      cold=cold, rho0=_v(pr["rho0"]) if "rho0" in pr else 0.0, k0=_v(pr["k0"]) if "k0" in pr else 0.0,
                      library=lib,
                      alpha_k=_v(pc["alpha_k"]) if "alpha_k" in pc else 0.0,
                      alpha_k_dt=_v(pc["alpha_k_dt"]) if "alpha_k_dt" in pc else 0.0,
                      c_v=_v(pc["c_v"]) if "c_v" in pc else 0.0,
                      ref_kind=ref["kind"], t_ref_kind=ref.get("t_ref_kind", "isotherm"),
                      t_ref=_v(ref["t"]) if "t" in ref else 0.0,
                      adiabat=None if ad is None else (tuple(float(x) for x in ad["lnp"]),
                                                       tuple(float(x) for x in ad["t"])),
                      sets=sets, gamma_window=(_num(gw["p_min"]), _num(gw["p_max"])), edges=ph["edges"],
                      constants_span=None if "phase_constants" not in th else
                      (_num(th["phase_constants"]["p_min"]), _num(th["phase_constants"]["p_max"])))

    # edges (D-M2) ─────────────────────────────────────────────────────────────────────────────────────────────────
    def boundary_pressure(self, curve, t):
        """P_b(T) of a declared boundary curve (D-P1): clapeyron p0 + slope·(T − t0), or a table of printed (T, P) nodes
        read piecewise-linearly in T (no extrapolation: outside the nodes the curve is absent, None). Other forms are
        not built yet (None)."""
        form = curve["form"]
        if form == "ln_sum":                           # IAPWS R14-08 Simon-type melting line, only in its printed range
            if t < _v(curve["t_min"]) or t > _v(curve["t_max"]):
                return None
            th = t / _v(curve["t_star"])
            return _v(curve["p_star"]) * math.exp(sum(_v(x["a"]) * (1.0 - th ** _v(x["b"])) for x in curve["terms"]))
        if form == "clapeyron":                        # 68 N32: only inside its printed T range
            if ("t_min" in curve and t < _v(curve["t_min"])) or ("t_max" in curve and t > _v(curve["t_max"])):
                return None
            return _v(curve["p0"]) + _v(curve["slope"]) * (t - _v(curve["t0"]))
        if form == "table":
            nodes = [(float(a), float(b)) for a, b in curve["nodes"]]
            for (t0, p0), (t1, p1) in zip(nodes, nodes[1:]):
                if t0 <= t <= t1:
                    return p0 + (p1 - p0) * (t - t0) / (t1 - t0)
            return None
        return None

    def _branch_at(self, p, t):
        """Branched record (D-P1): the phase on P's side of each declared boundary at T, in the record's phase order
        (lower-P phase first). A boundary whose curve is absent at T refuses (no phase is guessed)."""
        by_id = {ph.id: ph for ph in self.phases}
        cur = self.phases[0]
        for b in self.boundaries:                       # one per adjacent pair, in phase order (registry kind rule)
            lo, hi = b["between"]
            if lo != cur.id:
                break
            pb = self.boundary_pressure(b["curve"], t)
            if pb is None:
                return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                        f"boundary {tuple(b['between'])} has no curve at {t:g} K"))
            if p < pb:
                break
            cur = by_id[hi]
        return cur

    def refusal_region_at(self, p, t):
        """The declared refusal region holding (P, T), or None. Inside its box; at P ≥ every lower curve and P < every
        upper curve (half-open, as fields). A curve absent at T leaves the region not holding there."""
        for r in self.record.get("refusals", ()):
            b = r["box"]
            if not (b["p_min"] <= p <= b["p_max"] and b.get("t_min", -math.inf) <= t <= b.get("t_max", math.inf)):
                continue
            ok = True
            for c in r.get("lower", ()):
                pb = self.boundary_pressure(c, t)
                ok = ok and pb is not None and p >= pb
            for c in r.get("upper", ()):
                pb = self.boundary_pressure(c, t)
                ok = ok and pb is not None and p < pb
            if ok:
                return r
        return None

    def source_density(self, phase_index, source_id, p, t):
        """ρ(P, T) [kg/m³] from one declared source of a phase (impl note 3 A8): its own eos (a cold curve with its
        thermal_model, a library, or an evaluator), else the phase's own EOS. A Stop where it cannot answer."""
        ph = self.phases[phase_index]
        src = next((s for s in self.record["phases"][phase_index].get("sources", ()) if s["id"] == source_id), None)
        if src is None:
            raise KeyError(f"{ph.id}: no source {source_id!r}")
        eos = src.get("eos")
        if eos is None:
            return self._phase_density(ph, p, t)
        form = eos["form"]
        try:
            if form == "library":
                return ml.SeaFreezePhase(eos["library"]["submodel"]).at(p, t)["rho"]
            if form == "evaluator":
                return _EvaluatorPhase(EVALUATORS[eos["evaluator"]["name"]](eos["evaluator"].get("params", {}))).at(p, t)["rho"]
        except ml.LibraryOutOfRange as e:
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data", str(e)))
        pr = eos["params"]
        cold = _cold_pressure(form, _v(pr["rho0"]), _v(pr["k0"]), 4.0 if form == "bm2" else _v(pr.get("k0p", {"value": 4.0})))
        rho0, k0 = _v(pr["rho0"]), _v(pr["k0"])
        rho = rho0 * (1.0 + p / k0) ** 0.4                       # the same Newton as a phase's cold inversion
        for _ in range(60):
            f = cold(rho) - p
            if abs(f) <= 1e-9 * max(p, 1.0):
                break
            h = rho * 1e-7
            dfd = (cold(rho + h) - cold(rho - h)) / (2.0 * h)
            if dfd <= 0.0:
                return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                        f"source {source_id}: cold curve does not invert"))
            rho = max(rho - f / dfd, 0.5 * rho0)
        tm = src.get("thermal_model")
        if tm is not None and tm["kind"] == "exp_alpha":          # V = V_cold(P)·exp(α0 (T − T0)) → ρ = ρ_cold·exp(−…)
            rho = rho * math.exp(-_v(tm["alpha0"]) * (t - _v(tm["t0"])))
        return rho

    def _sides_hold(self, ph, p, t):
        """Note 6 FB1: ph lies on its own side of every declared boundary naming it; half-open (FB2): a boundary point
        belongs to the high-P phase (the second id). Returns True, False, or a Stop for a curve absent at T. A curve
        absent at T refuses only where the other phase's window also holds (P, T); where the other phase cannot be,
        there is nothing to separate and the absent curve is inert (c8, h2o liquid–VII printed only above 355 K). A
        curve present at T always bounds both phases (FB1)."""
        by_id = {x.id: x for x in self.phases}
        for b in self.boundaries:
            lo, hi = b["between"]
            if ph.id not in (lo, hi):
                continue
            pb = self.boundary_pressure(b["curve"], t)
            if pb is None:
                other = by_id.get(hi if ph.id == lo else lo)
                if other is None or not self._in_window(other, p, t):
                    continue
                return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                        f"boundary {lo}–{hi}: its curve is absent at {t:g} K"))
            if (ph.id == hi and p < pb) or (ph.id == lo and p >= pb):
                return False
        return True

    def _in_window(self, ph, p, t):
        return ph.p_min <= p <= ph.p_max and not (ph.t_max and t > ph.t_max) and not (ph.t_min and t < ph.t_min)

    def _field_at(self, p, t):
        """Impl note 6: the phase whose stability field holds (P, T). A gibbs phase also needs the lowest G among the
        record's gibbs phases whose window holds (one source; G never compared across sources); a tie goes to the
        higher-P phase (later in phase order). None → «no phase here»; two or more → overlap; never a guess."""
        hit = self.refusal_region_at(p, t)
        if hit is not None:                                # a declared refusal region wins over every field
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, hit["id"], hit["reason"]))
        kinds = {ph.id: self.record["phases"][i]["field"]["kind"] for i, ph in enumerate(self.phases)}
        gibbs = [ph for ph in self.phases if kinds[ph.id] == "gibbs" and ph.library is not None
                 and self._in_window(ph, p, t)]
        g_win = None
        if gibbs:
            best = None
            for ph in gibbs:
                try:
                    g = ph.library.at(p, t)["g"]
                except ml.LibraryOutOfRange:
                    continue                                # outside the spline: not a candidate
                if best is None or g <= best[0]:            # ≤: a tie goes to the later (higher-P) phase
                    best = (g, ph)
            g_win = None if best is None else best[1]
        hits = []
        for ph in self.phases:
            if not self._in_window(ph, p, t):
                continue
            if kinds[ph.id] == "gibbs" and ph is not g_win:
                continue
            side = self._sides_hold(ph, p, t)
            if isinstance(side, st.Stop):
                return side
            if side:
                hits.append(ph)
        if not hits:
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                    f"no phase here ({p:g} Pa, {t:g} K)"))
        if len(hits) > 1:
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "material.field_overlap",
                                                    f"fields overlap: {[h.id for h in hits]}"))
        return hits[0]

    def _phase_at(self, p, t):
        """The phase whose window holds p (p_min ≤ p ≤ p_max, as legacy Material.phase_at), or the edge's outcome. A
        branched record picks the phase by its declared boundary curves first, then applies that phase's window."""
        if self.kind == "branched" and self.record.get("choice") == "field":
            ph = self._field_at(p, t)
            if isinstance(ph, st.Stop):
                return ph
            return ph
        if self.kind == "branched" and self.boundaries:
            ph = self._branch_at(p, t)
            if isinstance(ph, st.Stop):
                return ph
            if not ph.p_min <= p <= ph.p_max:
                return self._edge(ph, "p_max" if p > ph.p_max else "p_min", p, t)
            if t > 0.0 and ph.t_max and t > ph.t_max:
                return self._edge(ph, "t_max", p, t)
            if t > 0.0 and ph.t_min and t < ph.t_min:
                return self._edge(ph, "t_min", p, t)
            return ph
        for ph in self.phases:
            if ph.p_min <= p <= ph.p_max:
                if t > 0.0 and ph.t_max and t > ph.t_max:
                    return self._edge(ph, "t_max", p, t)
                if t > 0.0 and ph.t_min and t < ph.t_min:
                    return self._edge(ph, "t_min", p, t)
                return ph
        ph = self.phases[-1] if p > self.phases[-1].p_max else self.phases[0]
        return self._edge(ph, "p_max" if p > ph.p_max else "p_min", p, t)

    def _edge(self, ph, name, p, t):
        e = ph.edges.get(name)
        if e is None or "refusal" in e:
            rid = "input.material_out_of_data" if e is None else e["refusal"]
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, rid, f"{ph.id}: past {name}"))
        # 68 N15: a band edge would give a value with a Note; until bands are evaluated (a later P3 step) it refuses, so no
        # record gets a bare value past its window meanwhile
        return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                f"{ph.id}: band edge {name} (band evaluation not built yet)"))

    # thermal ──────────────────────────────────────────────────────────────────────────────────────────────────────
    def _delta_t(self, ph, t, p):
        """Legacy Phase.delta_t: the phase's own reference (an adiabat table where the record carries one, C148)."""
        if not ph.alpha_k or t is None or t <= 0.0:
            return 0.0
        if ph.t_ref_kind == "adiabat":
            if self.t_pot <= 0.0:
                return 0.0
            if ph.adiabat is not None:
                return t - _pchip(math.log(p), *ph.adiabat)
            return t * (1.0 - ph.t_ref / self.t_pot)
        return t - ph.t_ref

    def _set_delta_t(self, s, t):
        """Legacy _set_delta_t: a set's ΔT runs from its own t_ref; never from the phase's table (68 N4)."""
        if t is None or t <= 0.0:
            return 0.0
        if s.t_ref_kind == "adiabat":
            return 0.0 if self.t_pot <= 0.0 else t * (1.0 - s.t_ref / self.t_pot)
        return t - s.t_ref

    def _thermal_pressure(self, ph, t, p):
        dt = self._delta_t(ph, t, p)
        return ph.alpha_k * dt + 0.5 * ph.alpha_k_dt * dt * dt

    @staticmethod
    def _set_top(s):
        """Where a set's values end: its window, or its declared edge band's limit (G4). The printed-scope edge itself
        is not a seam: the same evaluator continues, with a band Note."""
        return s.p_max if s.edge_limit is None else s.edge_limit

    def _set_at(self, ph, p):
        for s in ph.sets:
            if s.p_min <= p < self._set_top(s):
                return s
        return None

    def _gamma_gap(self, ph, p, t):
        """68 H2: past the γ window with no set covering P, γ is never the phase's constants (P2: no silent fallback).
        The Stop carries the declared edge refusal of the set this P lies past, else input.material_out_of_data."""
        g_lo, g_hi = ph.gamma_window
        # inside the γ window the phase's constants answer only where no sets exist at all, or inside the declared
        # phase_constants span (68 N19); any other uncovered P is a gap and refuses
        if g_lo <= p <= g_hi and (not ph.sets or (ph.constants_span is not None
                                                   and ph.constants_span[0] <= p <= ph.constants_span[1])):
            return None
        rid = "input.material_out_of_data"
        for s in ph.sets:
            if s.edge_limit is not None and p >= s.edge_limit and s.edge_refusal:
                rid = s.edge_refusal
        return st.Stop("refused", RecordRefusal(self.material_id, p, t, rid,
                                                f"{ph.id}: γ asked at {p:g} Pa, outside its window and every set"))

    def _ev(self, s, p, t, key):
        """A set's evaluator at (P, T); a failure is a named Stop, never an exception out of state() (68 N35)."""
        try:
            return s.evaluator.at(p, t)[key]
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                    f"evaluator {type(s.evaluator).__name__}: {e}"))

    def _band_error(self, ph, s):
        """A band's error: as declared, or its method evaluated from the record through the C4 grammar (once per view).
        A method that cannot be evaluated refuses; a band never rides without its number."""
        if s.edge_band.get("error") is not None:
            return float(s.edge_band["error"])
        pi, si = self.phases.index(ph), ph.sets.index(s)
        if (pi, si) not in self._band_errors:
            got = mc.evaluate(s.edge_band["method"], self.record["phases"][pi], {}, mc.view_spread(self, pi))
            if isinstance(got, mc.CheckStop):                # 68 N26: the grammar's own id, not the data-gap id
                got = st.Stop("refused", RecordRefusal(self.material_id, s.p_max, 0.0, got.id,
                                                       f"{ph.id}: band method does not evaluate: {got.why}"))
            self._band_errors[(pi, si)] = got
        return self._band_errors[(pi, si)]

    def _dpdt_v(self, ph, t, p):
        s = self._set_at(ph, p)
        if s is None:
            gap = self._gamma_gap(ph, p, t)
            if gap is not None:
                return gap
            return ph.alpha_k + ph.alpha_k_dt * self._delta_t(ph, t, p)
        if s.evaluator is not None:
            return self._ev(s, p, t, "dpdt_v")
        return s.alpha_k + s.alpha_k_dt * self._set_delta_t(s, t)

    def gruneisen(self, ph, p, rho, t):
        s = self._set_at(ph, p)
        if s is not None:
            if s.edge_limit is not None and p >= s.p_max and s.edge_band is not None:
                err = self._band_error(ph, s)
                if isinstance(err, st.Stop):
                    return err
                self.notes.append(BandNote(self.material_id, f"{ph.id} γ set past {s.p_max:g} Pa", s.edge_band["form"],
                                           err, s.edge_band.get("method"), s.edge_band["grade"], s.edge_band["origin"]))
            if s.evaluator is not None:
                return self._ev(s, p, t, "gruneisen")
            if s.c_v <= 0.0 or rho <= 0.0:
                return 0.0
            return self._dpdt_v(ph, t, p) / (rho * s.c_v)
        gap = self._gamma_gap(ph, p, t)
        if gap is not None:
            return gap
        if not ph.alpha_k or rho <= 0.0:
            return 0.0
        return self._dpdt_v(ph, t, p) / (rho * ph.c_v)

    # density ──────────────────────────────────────────────────────────────────────────────────────────────────────
    def _library(self, ph, p, t, key):
        try:
            return ph.library.at(p, t)[key]
        except ml.LibraryOutOfRange as e:           # 68 N28: a named Stop, never a crash
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data", str(e)))

    def _phase_density(self, ph, p, t):
        """Legacy Phase.density: subtract the thermal pressure, invert the cold curve by the same Newton. A library
        phase reads ρ from the pinned library."""
        if ph.library is not None:
            return self._library(ph, p, t, "rho")
        p_th = self._thermal_pressure(ph, t, p)
        if p_th:
            p = p - p_th
        if p <= 0.0:
            if not p_th:
                return ph.rho0
            return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                    f"{ph.id}: thermal pressure exceeds the total (expansion side "
                                                    "not built in phase 2)"))
        rho = ph.rho0 * (1.0 + p / ph.k0) ** 0.4
        tol = 1e-9 * max(p, 1.0)
        floor = ph.rho0 * 0.5
        for _ in range(60):
            f = ph.cold(rho) - p
            if abs(f) <= tol:
                return rho
            h = rho * 1e-7
            dfd = (ph.cold(rho + h) - ph.cold(rho - h)) / (2.0 * h)
            if dfd <= 0.0:
                break
            nxt = rho - f / dfd
            if nxt <= floor:
                nxt = 0.5 * (rho + floor)
            if abs(nxt - rho) <= 1e-12 * rho:
                return nxt
            rho = nxt
        return st.Stop("refused", RecordRefusal(self.material_id, p, t, "input.material_out_of_data",
                                                f"{ph.id}: density inversion did not converge"))

    def density(self, p: float, t: float):
        ph = self._phase_at(p, t)
        if isinstance(ph, st.Stop):
            return ph
        return self._phase_density(ph, p, t)

    def _stencil_bounds(self, ph, p):
        """Legacy Material.stencil_bounds: the (lo, hi] interval holding p between phase bounds and set seams."""
        lo, hi = 0.0, math.inf
        bs = [ph.p_min, ph.p_max] + [b for s in ph.sets for b in (s.p_min, self._set_top(s))]
        for b in bs:
            if 0.0 < b < math.inf:
                if b < p:
                    lo = max(lo, b)
                else:
                    hi = min(hi, b)
        return lo, hi

    def dtdp(self, p: float, t: float):
        """Legacy interior._adiabatic_dtdp for a phase with thermal constants: γT/K_S, K_S = K_T + (∂P/∂T)_V·γ·T, K_T the
        stencil difference of the density path inside the phase's (lo, hi] interval (C157)."""
        if t <= 0.0:
            return 0.0
        pe = max(p, self.p_stop) if p > 0.0 else max(1.0e5, self.p_stop)
        ph = self._phase_at(pe, t)
        if isinstance(ph, st.Stop):
            return ph
        if ph.library is not None:                 # (dT/dP)_S = αT/(ρc_P) from the library, checked against its Js
            return self._library(ph, pe, t, "dtdp")
        rho = self._phase_density(ph, pe, t)
        if isinstance(rho, st.Stop):
            return rho
        gamma = self.gruneisen(ph, pe, rho, t)
        if isinstance(gamma, st.Stop):
            return gamma
        if gamma <= 0.0:
            return 0.0
        h = pe * 1e-4
        p_lo, p_hi = pe - h, pe + h
        if p_hi > ph.p_max:
            p_hi = ph.p_max
            p_lo = min(p_lo, p_hi - 2.0 * h)
        lo_b, hi_b = self._stencil_bounds(ph, pe)
        lo_b = math.nextafter(lo_b, math.inf) if lo_b > 0.0 else lo_b
        if p_hi > hi_b:
            p_hi = hi_b
            p_lo = max(min(p_lo, p_hi - 2.0 * h), lo_b)
        if p_lo < lo_b:
            p_lo = lo_b
            p_hi = min(max(p_hi, p_lo + 2.0 * h), hi_b)
        d_hi, d_lo = self._phase_density(ph, p_hi, t), self._phase_density(ph, p_lo, t)
        for d in (d_hi, d_lo):
            if isinstance(d, st.Stop):
                return d
        if d_hi <= d_lo:
            return 0.0
        k_t = rho * (p_hi - p_lo) / (d_hi - d_lo)
        dpdt = self._dpdt_v(ph, t, pe)
        if isinstance(dpdt, st.Stop):
            return dpdt
        k_s = k_t + dpdt * gamma * t
        return gamma * t / max(k_s, 1.0)

    def porosity(self, p: float) -> float:
        return 0.0

    def state(self, p: float, t: float, guess_rho=None):
        self.notes.clear()
        rho = self.density(p, t)
        if isinstance(rho, st.Stop):
            return rho
        g = self.dtdp(p, t)
        if isinstance(g, st.Stop):
            return g
        return (rho, g, tuple(self.notes))

    # boundaries ───────────────────────────────────────────────────────────────────────────────────────────────────
    def seams(self) -> tuple:
        """Pressures where the integrand changes piece: phase windows and thermal-set seams (finite, > 0)."""
        out = set()
        for ph in self.phases:
            for b in [ph.p_min, ph.p_max] + [x for s in ph.sets for x in (s.p_min, self._set_top(s))]:
                if 0.0 < b < math.inf:
                    out.add(b)
        return tuple(sorted(out))

    def transitions(self) -> tuple:
        """Declared univariant boundaries (design §I): (between, kind, curve). Source seams are never listed here."""
        return tuple((tuple(b["between"]), b["kind"], b["curve"]) for b in self.boundaries)
