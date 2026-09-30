# 풀이 사이에 남는 모듈 수준 상태를 한 곳에 등록하고 반복 출발점만 초기화하는 레지스트리 (structure-grid 덧붙임 44)
"""One registry for module-level state that survives from one solve to the next.

Each entry is (module, name, kind, reason). Kinds:
- ``start``   — the previous solve's answer, used only as an iteration's starting point. It can move the
  last digits of the next solve, so `reset()` puts it back to the module's initial value.
- ``memo``    — returns a stored value only for the same key, or a lazily loaded table: harmless.
- ``counter`` — counts events; outside the value path.
- ``flag``    — a build switch.

`test_process_state.py` counts the module-level names that functions rebind with ``global`` or whose
contents functions mutate, and fails on any that is not listed here — a new cache has to be registered.
`reset()` is called per point by `parallel_points` (table building only); node solves elsewhere do not
call it, so shipped values do not move through this module.
"""
from __future__ import annotations

import importlib

START, MEMO, COUNTER, FLAG = "start", "memo", "counter", "flag"

#: (module, name) → (kind, reason, initial value for ``start`` entries)
REGISTRY: dict[tuple[str, str], tuple[str, str, object]] = {
    ("water_hot", "_LAST_DENSITY"): (START, "previous (P, T, rho): secant starting point (C122)", (0.0, 0.0, 0.0)),
    ("fermi", "_LAST_INVERSE"): (START, "previous (value, eta): Newton starting point", (0.0, 0.0)),
    ("rtpress", "_LAST_LIQUID"): (MEMO, "returned only for the same (P, T)", None),
    ("rtpress", "_VMIN_TAB"): (MEMO, "lazily built table, a function of the constants only", None),
    ("ice_fr2015", "_GL_NODES"): (MEMO, "lazily built quadrature nodes", None),
    ("ice_fr2015", "_CACHE"): (MEMO, "keyed by (name, P, T)", None),
    ("fe_liquid", "_CACHE"): (MEMO, "keyed by (name, P, T)", None),
    ("mantle_composition", "_TABLE_PHASE"): (MEMO, "lazily loaded phase table", None),
    ("rocky_roster", "_ROWS"): (MEMO, "lazily loaded roster rows", None),
    ("rocky_roster", "_CACHE"): (MEMO, "keyed by name", None),
    ("eos", "_SPINODAL"): (MEMO, "keyed by the phase constants", None),
    ("eos", "_PRESSURE_FAST"): (MEMO, "pressure closure keyed by the phase constants (C137)", None),
    ("interior", "ADAPTIVE_STATS"): (COUNTER, "step counts", None),
    ("mantle_composition", "TABLE_ASKS"): (COUNTER, "table lookups", None),
    ("rtpress", "OUTSIDE"): (COUNTER, "calls outside the calibration window", None),
    ("rtpress", "CALLS"): (COUNTER, "call count", None),
    ("eos", "P_EDGE_CALLS"): (COUNTER, "edge-evaluator calls", None),
    ("eos", "DENSITY_REACH"): (COUNTER, "density-fit reach", None),
    ("eos", "DENSITY_BELOW_REF"): (COUNTER, "calls below the reference pressure", None),
    ("eos", "FE_S_MODEL_ASKS"): (COUNTER, "Fe-S model asks", None),
    ("ice_fr2015", "STATS"): (COUNTER, "inversion counts", None),
    ("paleos", "PALEOS_COST"): (COUNTER, "lookup cost", None),
    ("check_refs", "BASENAMES"): (MEMO, "file index of the reference checker (tooling)", None),
    ("check_refs", "CACHE"): (MEMO, "file text read once (tooling)", None),
    ("interior", "_BASAL_INFO"): (MEMO, "side facts keyed by id(structure), cleared at each solve", None),
    ("interior", "_ICE_GRID_DELTA"): (MEMO, "side facts keyed by id(structure), cleared at each solve", None),
    ("interior", "_LITHO_INFO"): (MEMO, "side facts keyed by id(structure), cleared at each solve", None),
    ("interior", "_FAMILY_INFO"): (MEMO, "family-oscillation facts keyed by id(structure), cleared at each solve", None),
    ("mantle_composition", "_TABLES"): (MEMO, "lazily loaded mantle tables, keyed", None),
    ("paleos", "_FACTS"): (MEMO, "lazily read table facts, keyed", None),
    ("provisional", "REGISTRY"): (MEMO, "placeholders registered at import", None),
    ("registry", "_REGISTRY"): (MEMO, "node functions registered at import", None),
    ("eos", "VERDICT_ASKINGS"): (COUNTER, "thermal-set verdict asks", None),
    ("ice_fr2015", "CLAMPED_STATES"): (COUNTER, "record of clamped states", None),
    ("rocky_roster", "_FUNNEL"): (COUNTER, "roster funnel counts", None),
    ("samuel_model", "DEFAULT_USES"): (COUNTER, "default-parameter uses", None),
    ("interior", "COMPOSITIONS"): (FLAG, "constant table swapped inside one call and restored in finally", None),
    ("parallel_points", "_FN"): (FLAG, "the function the helper is solving now", None),
    ("interior", "_REOPEN"): (FLAG, "re-entry guard while re-closing melt families inside one solve, reset in finally", None),
    ("interior", "_FAMILY_TRAIL"): (MEMO, "one solve's outer-loop family record (addendum 57), cleared at each solve", None),
    ("interior", "_ENTRY"): (FLAG, "re-close entry for one table solve (addendum 57 rule 3c), set and cleared in finally by the caller", None),
    ("structure_grid", "BUILDING"): (FLAG, "table build in progress", None),
    ("structure_grid", "GRID_DIR"): (FLAG, "table directory override", None),
}


def reset() -> None:
    """Put every ``start`` entry back to its initial value (per point, table building)."""
    for (mod, name), (kind, _why, initial) in REGISTRY.items():
        if kind == START:
            setattr(importlib.import_module(mod), name, initial)
