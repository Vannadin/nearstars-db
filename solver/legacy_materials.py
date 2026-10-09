# phase-1 물질 어댑터 — 옛 engine/eos 재료와 interior 의 단열 기울기 경로를 MaterialView 규약 뒤에 둔다 (설계 §X4)
"""Phase-1 material adapter: today's engine materials behind the `MaterialView` protocol.

Frozen design: rewrite/phase1-design.frozen.md §X4, §A1.1 (dT/dP from the view), §A6 (adapter debt);
registration rewrite/phase1-a1-impl.frozen.md S4. Phase 2 (A4) replaces this module.

The only module under solver/ that imports engine/ (design §L). It reproduces, for one layer material, what the old
integrator's stage function evaluates at 097a8aa3 (engine/interior.py `deriv` and `_dp.dT`, :1533–1604):
- density: `mat.density(_at_floor(max(P, p_stop)), T, t_pot)`, times (1 − porosity) where the body declares one;
  the column-steam stage below water2's table floor; the hot-surface rule (SURF_RHO) for P ≤ 0;
- (dT/dP)_ad: `interior._adiabatic_dtdp(mat, max(P, p_stop), mat.density(_at_floor(max(P, p_stop)), T, t_pot), T,
  t_pot)`, 0 when T ≤ 0 (no declared temperature), unchanged including the melt-window terms and the 0-with-note
  branch for materials without thermal constants.
An `eos.PhaseGap` (and subclasses) becomes a `stepper.Stop("refused", MaterialRefusal)`; nothing is raised.
"""
from __future__ import annotations

import copy
import importlib
import os
import sys
from dataclasses import dataclass

from solver import stepper as st

_ENGINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
if _ENGINE not in sys.path:
    sys.path.insert(0, _ENGINE)

import eos            # noqa: E402  (engine/, 097a8aa3)
import interior       # noqa: E402
import process_state  # noqa: E402
import steam_if97     # noqa: E402
import water2_table   # noqa: E402


@dataclass(frozen=True)
class MaterialRefusal:
    material_id: str
    p: float
    t: float
    kind: str              # the exception class name, e.g. "PhaseGap", "SpinodalGap"
    message_old: str       # the old engine's reason text (oracle T0 match while the adapter is in use)


#: MEMO entries filled at import (node and placeholder registries). Clearing them would unregister the engine itself,
#: so they are kept; their description in process_state says «registered at import».
IMPORT_REGISTRIES = frozenset({("provisional", "REGISTRY"), ("registry", "_REGISTRY")})


def _registry_entries():
    for (mod, name), (kind, why, initial) in process_state.REGISTRY.items():
        if kind == process_state.FLAG or (mod, name) in IMPORT_REGISTRIES:
            continue
        try:
            m = importlib.import_module(mod)
        except ImportError:
            continue                      # tooling-only modules may be absent from a solver run
        if hasattr(m, name):
            yield (mod, name, kind, m)


#: Each resettable entry's value right after import (deep copies). Resetting restores these, so a counter dict keeps
#: its keys (e.g. eos.DENSITY_BELOW_REF's "lowest_pa"), a memo returns to empty, a start value to its seed.
_PRISTINE = {(mod, name): copy.deepcopy(getattr(m, name)) for mod, name, _k, m in _registry_entries()}


def reset_engine_state() -> list:
    """Reset every resettable entry of engine/process_state.REGISTRY (r2 M11), not a hand-picked list, to its
    value right after import (START seeds, empty MEMOs, zero COUNTERs with their keys). Containers are restored in
    place, so other modules holding a reference see the reset. Not touched:
    - FLAG entries: a flag is set and restored in `finally` by its owner (e.g. interior.COMPOSITIONS, a constant
      table swapped inside one call); `flags_snapshot` checks that they are at rest;
    - the two import-time registries (IMPORT_REGISTRIES).
    Returns [(module, name, kind)] of the entries reset."""
    done = []
    for mod, name, kind, m in _registry_entries():
        fresh = copy.deepcopy(_PRISTINE.get((mod, name)))
        cur = getattr(m, name)
        if isinstance(cur, dict) and isinstance(fresh, dict):
            cur.clear()
            cur.update(fresh)
        elif isinstance(cur, list) and isinstance(fresh, list):
            cur[:] = fresh
        elif isinstance(cur, set) and isinstance(fresh, set):
            cur.clear()
            cur.update(fresh)
        else:
            setattr(m, name, fresh)
        done.append((mod, name, kind))
    return done


def flags_snapshot() -> dict:
    """Current values of the FLAG entries (by repr), to check that a solve leaves them as it found them."""
    out = {}
    for (mod, name), (kind, _why, _initial) in process_state.REGISTRY.items():
        if kind != process_state.FLAG:
            continue
        try:
            m = importlib.import_module(mod)
        except ImportError:
            continue
        if hasattr(m, name):
            out[(mod, name)] = repr(getattr(m, name))
    return out


class LegacyView:
    """One layer material as the old integrator sees it. `p_stop` is the outermost material's floor (the oracle's
    surface pressure); `t_pot` the body's potential temperature (today's ΔT-referenced phases need it, W-L11-02);
    `phi0`, `p_cap` the declared porosity law (0 = none); `column_steam` whether the old column-steam stage rule
    applies (no gas envelope and no envelope Z)."""

    def __init__(self, material_id: str, material, t_pot: float, p_stop: float = 0.0,
                 phi0: float = 0.0, p_cap: float | None = None, column_steam: bool = False):
        self.material_id = material_id
        self.mat = material
        self.t_pot = t_pot
        self.p_stop = p_stop
        self.phi0 = phi0
        self.p_cap = p_cap
        self.column_steam = column_steam
        self.lo = getattr(material, "shoot_lo", 0.0)
        self.p_floor = getattr(material, "p_floor", 0.0)
        self._dense = eos.MATERIALS["h2o_liquid_dense"]

    def _at_floor(self, p: float) -> float:
        return self.lo if (self.lo and p < self.lo) else p

    def _refusal(self, exc, p, t):
        return st.Stop("refused", MaterialRefusal(self.material_id, p, t, type(exc).__name__, str(exc)))

    def density(self, p: float, t: float):
        mat = self.mat
        try:
            if (self.column_steam and mat is self._dense and 0.0 < p < water2_table.P_MIN_PA
                    and steam_if97.in_domain(p, t)):
                rho = interior.COLUMN_STEAM.density(p, t)
            elif p > 0.0:
                rho = mat.density(self._at_floor(max(p, self.p_stop)), t, self.t_pot)
            elif interior.SURF_RHO:
                try:
                    rho = mat.density(self._at_floor(max(1.0e5, self.p_stop)), t, self.t_pot)
                except eos.PhaseGap:
                    rho = mat.rho0          # counted by the caller's trace, not a module counter (design §A1.2)
            else:
                rho = mat.rho0
        except eos.PhaseGap as exc:
            return self._refusal(exc, p, t)
        return rho * (1.0 - interior.porosity_at(mat, p, self.phi0, self.p_cap))

    def dtdp(self, p: float, t: float):
        if t <= 0.0:
            return 0.0
        # at the surface start P = 0 the old engine never evaluated dT/dP (its pass ended there); the start is read at
        # the same pressure as the hot-surface density rule (SURF_RHO): max(1 bar, p_stop)
        pe = max(p, self.p_stop) if p > 0.0 else max(1.0e5, self.p_stop)
        try:
            rho = self.mat.density(self._at_floor(pe), t, self.t_pot)
            return interior._adiabatic_dtdp(self.mat, pe, rho, t, self.t_pot)
        except eos.PhaseGap as exc:
            return self._refusal(exc, p, t)

    def state(self, p: float, t: float, guess_rho=None):
        rho = self.density(p, t)
        if isinstance(rho, st.Stop):
            return rho
        g = self.dtdp(p, t)
        if isinstance(g, st.Stop):
            return g
        return (rho, g)


def ammonia_isotherms() -> tuple:
    """The ammonia table's isotherm nodes [K] (Bethkenhagen+ 2013 Table I, engine/ammonia_table.T_K): interpolation
    switches isotherm pair there, so the integrand has a kink in T (located as events, design §A1.3)."""
    import ammonia_table
    return tuple(float(t) for t in ammonia_table.T_K)
