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

#: «Material data bytes» of solve_id (design §A6; r2 S7 note-4 HOLDs): the engine tree as git tracks it — the blob ids
#: of every tracked engine file outside bodies/, test fixtures, tests, tools, requirements and prose (r2: untracked and
#: generated files must not count). A tracked file modified in the working tree adds its path and content hash, so a
#: dirty tree gets its own id. A fixed function of the tree: no process history, no machine paths, no file reads beyond
#: git's own (r2: no per-solve re-read of every table).
_DATA_SUFFIXES = (".py", ".json", ".yaml", ".yml", ".csv", ".txt", ".npz", ".npy", ".dat", ".h5")
_NOT_DATA_PARTS = ("engine/bodies/", "engine/test_fixtures/", "engine/tools/", "/__pycache__/")


def _counts(path: str) -> bool:
    base = path.rsplit("/", 1)[-1]
    return (path.endswith(_DATA_SUFFIXES) and not base.startswith(("test_", "requirements"))
            and not any(x in path for x in _NOT_DATA_PARTS))


def material_bytes() -> bytes:
    """sha256 over the tracked engine files' (path, blob id) lines of `git ls-files -s`, plus (path, content sha256) of
    every such file modified in the working tree."""
    import hashlib
    import subprocess
    repo = os.path.dirname(_ENGINE)
    ls = subprocess.run(["git", "-C", repo, "ls-files", "-s", "--", "engine"], capture_output=True, text=True,
                        check=True).stdout.splitlines()
    h = hashlib.sha256()
    for line in sorted(ls):
        meta, path = line.split("\t", 1)
        if _counts(path):
            h.update(f"{path} {meta.split()[1]}\n".encode())
    dirty = subprocess.run(["git", "-C", repo, "diff", "--name-only", "--", "engine"], capture_output=True, text=True,
                           check=True).stdout.split()
    for path in sorted(p for p in dirty if _counts(p)):
        full = os.path.join(repo, path)
        content = open(full, "rb").read() if os.path.isfile(full) else b"<deleted>"
        h.update(f"dirty {path} ".encode() + hashlib.sha256(content).digest())
    return h.digest()


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


#: MEMOs that are functions of constants or static data by their own REGISTRY text («lazily built table, a function
#: of the constants only», «keyed by the phase constants», «… same arithmetic, same values», «lazily loaded …»), plus
#: the tooling-only checker memos. They cannot carry one solve's state into the next, so they are neither checked
#: nor reset (clearing them would only cost a rebuild).
CONSTANT_MEMOS = frozenset({
    ("rtpress", "_VMIN_TAB"), ("ice_fr2015", "_GL_NODES"), ("mantle_composition", "_TABLE_PHASE"),
    ("mantle_composition", "_TABLES"), ("rocky_roster", "_ROWS"), ("eos", "_SPINODAL"), ("eos", "_PRESSURE_FAST"),
    ("water_table", "_CACHE"), ("water2_table", "_CACHE"), ("paleos", "_FACTS"),
    ("check_refs", "BASENAMES"), ("check_refs", "CACHE")})

#: Record-shaped MEMOs: a dict with fixed fields, at rest when every field is empty, None or 0.
RECORD_MEMOS = frozenset({("interior", "_FAMILY_TRAIL")})


def _empty(v) -> bool:
    return v is None or v == 0 or (isinstance(v, (list, set, dict, tuple)) and len(v) == 0)


def _at_rest(key, v) -> bool:
    """A per-solve memo's empty form: None, an empty container (keyed caches must be **empty**, r2 N4), a tuple of
    Nones (rtpress._LAST_LIQUID = (None, None, None)), or a RECORD_MEMOS dict whose fields are all empty."""
    if key in RECORD_MEMOS and isinstance(v, dict):
        return all(_empty(x) for x in v.values())
    if v is None or (isinstance(v, (list, set, dict)) and len(v) == 0):
        return True
    return isinstance(v, tuple) and all(x is None for x in v)


def _counter_at_rest(v) -> bool:
    """A counter's zero form as written in its source: 0, None, an empty container, a list of zeros, or a dict whose
    values are all at rest (eos.DENSITY_BELOW_REF = {"lowest_pa": None, …}, rtpress.OUTSIDE = {"calls": 0, …})."""
    if v is None or (isinstance(v, (int, float)) and v == 0):
        return True
    if isinstance(v, (list, set, tuple)):
        return all(_counter_at_rest(x) for x in v)
    if isinstance(v, dict):
        return all(_counter_at_rest(x) for x in v.values())
    return False


#: Snapshot at the adapter's import (deep copies) of the per-solve MEMOs and the COUNTERs. Restoring a COUNTER keeps
#: its keys (e.g. eos.DENSITY_BELOW_REF["lowest_pa"]); restoring a MEMO gives its empty form, checked here: a memo
#: filled before this import makes the import fail by name (r2). START entries are not snapshotted: they go back to
#: their REGISTRY initial, which equals the source value for both (r2 S4 B1).
_PRISTINE = {(mod, name): copy.deepcopy(getattr(m, name)) for mod, name, k, m in _registry_entries()
             if k != process_state.START and (mod, name) not in CONSTANT_MEMOS}
_NOT_AT_REST = sorted(f"{mod}.{name}" for mod, name, k, m in _registry_entries()
                      if k == process_state.MEMO and (mod, name) not in CONSTANT_MEMOS
                      and not _at_rest((mod, name), getattr(m, name)))
_NOT_AT_REST += sorted(f"{mod}.{name}" for mod, name, k, m in _registry_entries()
                      if k == process_state.COUNTER and not _counter_at_rest(getattr(m, name)))
if _NOT_AT_REST:
    raise ImportError("solver.legacy_materials imported after engine memos or counters were filled: " + ", ".join(_NOT_AT_REST))


def reset_engine_state() -> list:
    """Reset the per-solve entries of engine/process_state.REGISTRY (r2 M11):
    - START → its REGISTRY initial value (equal to the source value);
    - per-solve MEMO → its empty form (snapshotted at rest at import), in place;
    - COUNTER → its value at import, in place (keys kept).
    Not touched: FLAG entries (set and restored in `finally` by their owner, e.g. interior.COMPOSITIONS), the two
    import-time registries (IMPORT_REGISTRIES) and the CONSTANT_MEMOS. Returns [(module, name, kind)] reset."""
    done = []
    initial = {(mod, name): init for (mod, name), (_k, _w, init) in process_state.REGISTRY.items()}
    for mod, name, kind, m in _registry_entries():
        if (mod, name) in CONSTANT_MEMOS:
            continue
        fresh = copy.deepcopy(initial[(mod, name)] if kind == process_state.START else _PRISTINE.get((mod, name)))
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
        self.surface_fallbacks = 0      # SURF_RHO falls back to rho0 (§A1.2): counted here, read into the trace
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
                    rho = mat.rho0          # counted on this view (owned by the solve's context), not a module dict
                    self.surface_fallbacks += 1
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
        """(ρ, (dT/dP)_ad, notes) or a Stop. `guess_rho` is accepted for the X4 signature and unused: the old
        materials keep their own inversion start. Notes: «surface_rho0_fallback» when the hot-surface rule fell back
        to ρ₀ (then (dT/dP)_ad is 0 there: the material refuses the surface state, so it has no gradient);
        «no_thermal_constants» when the material carries none (the old engine's 0-with-note branch)."""
        before = self.surface_fallbacks
        rho = self.density(p, t)
        if isinstance(rho, st.Stop):
            return rho
        if self.surface_fallbacks != before:
            return (rho, 0.0, ("surface_rho0_fallback",))
        g = self.dtdp(p, t)
        if isinstance(g, st.Stop):
            return g
        has = getattr(self.mat, "has_thermal", None)          # a property on eos.Material
        has = has() if callable(has) else has
        notes = ("no_thermal_constants",) if (t > 0.0 and has is False) else ()
        return (rho, g, notes)


def ammonia_isotherms() -> tuple:
    """The ammonia table's isotherm nodes [K] (Bethkenhagen+ 2013 Table I, engine/ammonia_table.T_K): interpolation
    switches isotherm pair there, so the integrand has a kink in T (located as events, design §A1.3)."""
    import ammonia_table
    return tuple(float(t) for t in ammonia_table.T_K)


BASAL_CONST = "silicate_basal_const"


#: Water-family materials (interior.VOLATILE_NAMES at 097a8aa3). The old integrator chooses among them per step
#: (liquid_material, with_rock / with_ices, the liquid-crust refusal); that dispatch is not in the phase-1 adapter
#: (registration note 2), so a layer of one of them is a named refusal until it is ported.
NOT_PORTED = frozenset(interior.VOLATILE_NAMES)


def _has_water(mat) -> bool:
    """A water-family material, or a mixture holding one (with_rock / with_ices / envelope water)."""
    if getattr(mat, "name", "") in NOT_PORTED or interior._volatile(mat):
        return True
    return any(w > 0.0 and _has_water(m) for m, w in (getattr(mat, "parts", None) or ()))


def resolve(layer, t_pot: float, p_stop: float, column_steam: bool = False):
    """The view of one layer (S7). Plain ids are engine MATERIALS keys (eos.py:4431 + CORE_BOX_MATERIALS); the basal
    constant-density layer is `silicate_basal_const` with params.density. Composition-built materials (declared or
    fitted cores, declared mantles) are built inside their old contexts by the caller per trial (not here).
    Returns a LegacyView, or None for an id this adapter cannot build (the caller refuses input.unknown_material)."""
    params = layer.params or {}
    if layer.material == BASAL_CONST:
        rho = params.get("density")
        rho = getattr(rho, "value", rho)
        if rho is None:
            return None
        return LegacyView(BASAL_CONST, interior.BasalConstDensity(float(rho)), t_pot, p_stop)
    if layer.material in NOT_PORTED or layer.material.startswith(("h2o", "steam")):
        return None
    mat = interior.MATERIALS.get(layer.material)
    if mat is None or _has_water(mat):
        return None
    phi0 = params.get("porosity_phi0")
    p_cap = params.get("porosity_p_cap")
    return LegacyView(layer.material, mat, t_pot, p_stop,
                      phi0=float(getattr(phi0, "value", phi0) or 0.0),
                      p_cap=None if p_cap is None else float(getattr(p_cap, "value", p_cap)),
                      column_steam=column_steam)


# ── S10 builders (registration note 5 item 3b/3c): composition-built materials, made as the old context managers make
#    them, but never registered in MATERIALS and never swapping COMPOSITIONS (FLAG state) ──────────────────────────────

def _pin_of(o: float, c: float) -> str:
    for pin, v in interior.LIGHT_ELEMENT_PINS.items():
        if v["O"] == o and v["C"] == c:
            return pin
    return f"o{o}_c{c}"


def build_fe_core_light(s: float, o: float, c: float):
    """The liquid Fe–S–O–C core material at S = s, O = o, C = c (mass fractions), as `interior._sulphur_core` builds it
    at 097a8aa3 (interior.py:5859 ff.: core_mole_fractions → huang_core_phase(x, "19GPa") in a Material with the fit-floor
    reasons)."""
    x = eos.core_mole_fractions({"S": s, "O": o, "C": c})
    name = f"fe_core_fit_s{s * 100:.4f}_{_pin_of(o, c)}"
    return eos.Material(
        name, f"액체 Fe–S–O–C · S {s * 100:.4f} wt% ({_pin_of(o, c)})",
        (eos.huang_core_phase(x, "19GPa"),), fit_composition="Fe-S-O-C", role="core",
        gap_reason="이 재질은 상이 하나라 상 **사이** 빈 구간이 없다",
        under_reason=eos.FE_S_FIT_FLOOR_REASON, floor_source=eos.FE_S_FIT_FLOOR_SOURCE)


def build_silicate_decl(wt: dict):
    """The declared-mantle silicate for oxide wt% `wt`: the object `mantle_composition.declared(wt)` installs as
    MATERIALS["silicate"] (table_material over the base silicate), built without the swap. Returns None with the old
    refusal text when the table is missing."""
    import mantle_composition
    tab, why = mantle_composition.load(dict(wt))
    if why:
        return None, why
    return mantle_composition.table_material(interior.MATERIALS["silicate"], tab.key), None
