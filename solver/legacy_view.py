# 옛 핵 노드 연결부 — 새 Answer 를 옛 interior_layers 결과 모양(옛 단위)으로 넣고, 옛 사슬을 그대로 돌려 읽은 키를 기록 (등록 S8)
"""legacy_view: run the old engine's chain on the new structure, for the oracle's core-node rows.

Registration rewrite/phase1-a1-impl.frozen.md §3 and S8 (with notes 1–3). Removed after A5.

The old chain (engine/run.py at 097a8aa3) runs unchanged, except that the `interior_layers` recipe is replaced by one
that returns the rewrite's Answer as an old `payload.Result`, in the old units (R⊕, GPa, K). Every other node,
the core nodes included, runs the old code; `core_thermal_history` reads the committed structure table, which is
the frozen-table mode of t2 note 2.

The old BodyState records every lookup as (reader node, key, kind). `reads()` splits them by side: a key answered
by the injected interior_layers Result is an **output** read; a key answered by the body's declared inputs is a
**declared** read (registration §3: outputs vs declared, each logged).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from solver import legacy_materials as lm          # noqa: F401  (puts engine/ on sys.path)

import payload    # noqa: E402
import registry   # noqa: E402
import run        # noqa: E402

#: The old interior_layers keys the in-scope readers use (registration §3), and how each comes from the Answer.
OUTPUT_KEYS = ("core_radius", "cmb_pressure", "cmb_temperature", "core_pressure", "core_temperature", "radius",
               "converged", "core_mass_fraction", "ice_mass_fraction")
IN_SCOPE_READERS = ("core_state", "cmb_heat_flux", "core_energy_balance", "core_entropy_production",
                    "core_thermal_history", "internal_heat_nontidal")
EARTH_RADIUS_M = 6.371e6           # interior.EARTH_RADIUS_M at 097a8aa3


def _q(answer, key):
    for q in answer.quantities:
        if q.key == key:
            return q.point
    return None


def old_values(answer, declared_imf: float | None = None) -> tuple[dict, dict]:
    """(values, units) of the injected interior_layers Result, in the old units (interior.py:5002–5073)."""
    r = _q(answer, "radius")
    rc = _q(answer, "core_radius")
    t_cmb = _q(answer, "cmb_temperature")
    vals = {"nmoi": _q(answer, "nmoi"), "core_temperature": _q(answer, "core_temperature"),
            "cmb_temperature": t_cmb, "cmb_temperature_core": t_cmb, "cmb_temperature_mantle": t_cmb,
            "cmb_pressure": _q(answer, "cmb_pressure") / 1e9, "core_radius": rc / EARTH_RADIUS_M,
            "core_radius_fraction": rc / r, "radius": r / EARTH_RADIUS_M,
            "core_pressure": _q(answer, "core_pressure") / 1e9, "converged": True,
            "core_mass_fraction": _q(answer, "core_mass_fraction"),
            "ice_mass_fraction": 0.0 if declared_imf is None else declared_imf}
    units = {"nmoi": "dimensionless", "core_temperature": "K", "cmb_temperature": "K",
             "cmb_temperature_core": "K", "cmb_temperature_mantle": "K", "cmb_pressure": "GPa",
             "core_radius": "R_earth", "core_radius_fraction": "dimensionless", "radius": "R_earth",
             "core_pressure": "GPa", "converged": "", "core_mass_fraction": "dimensionless",
             "ice_mass_fraction": "dimensionless"}
    return vals, units


@dataclass
class ChainRun:
    body: object            # the old BodyState after the chain ran
    injected: object        # the injected interior_layers Result


def run_chain(v1_yaml: str | os.PathLike, answer, serve_cmf_from_declared: bool = False,
              t_pot: float | None = None) -> ChainRun:
    """Run the old chain on the new structure. `t_pot` overrides the old body's potential temperature in memory (an
    O9 state; the solve used the same value). `serve_cmf_from_declared` is a negative control only (S8): it puts the
    rewrite's CMF into the declared inputs instead of the interior_layers output."""
    registry.load_all()                              # import every recipe module (as run.py / dump.py do)
    body, _expected = run.load_body(Path(v1_yaml))
    if t_pot is not None:
        cur = body.inputs.get("potential_temperature")
        body.inputs["potential_temperature"] = ({**cur, "value": t_pot} if isinstance(cur, dict) else t_pot)
    imf = body.inputs.get("ice_mass_fraction")
    imf = getattr(imf, "get", lambda k, d=None: None)("value") if isinstance(imf, dict) else imf
    vals, units = old_values(answer, imf)
    if serve_cmf_from_declared:
        body.inputs["core_mass_fraction"] = vals.pop("core_mass_fraction")
        units.pop("core_mass_fraction")
    injected = payload.Result(recipe="interior-structure-methodology", version="rewrite-phase1", regime="rewrite",
                              reason="rewrite solver Answer (solver.legacy_view)", grade="judgment", inputs={},
                              values=vals, units=units, converged=True)
    orig_get = registry.get
    registry.get = lambda node: (lambda b: injected) if node == "interior_layers" else orig_get(node)
    try:
        run.solve(body, run.load_chain())
    finally:
        registry.get = orig_get
    return ChainRun(body, injected)


def reads(chain: ChainRun) -> dict:
    """{reader: {"outputs": set, "declared": set, "other": set}} for the in-scope readers, from the old lookup log.
    «outputs»: answered by the injected interior_layers Result; «declared»: answered by the body's inputs;
    «other»: answered by another node."""
    body = chain.body
    out = {}
    for reader, key, kind in body.lookups:
        if reader not in IN_SCOPE_READERS or not kind.endswith("hit"):
            continue
        prod = body._producer(key)
        side = "declared" if prod is None else ("outputs" if prod == "interior_layers" else "other")
        out.setdefault(reader, {"outputs": set(), "declared": set(), "other": set()})[side].add(key)
    return out
