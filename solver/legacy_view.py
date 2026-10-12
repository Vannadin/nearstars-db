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

import dataclasses
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from solver import legacy_materials as lm          # noqa: F401  (puts engine/ on sys.path)

import payload    # noqa: E402
import registry   # noqa: E402
import run        # noqa: E402
from state import BodyState   # noqa: E402

#: The old interior_layers keys the in-scope readers use (registration §3), and how each comes from the Answer.
OUTPUT_KEYS = ("core_radius", "cmb_pressure", "cmb_temperature", "core_pressure", "core_temperature", "radius",
               "converged", "core_mass_fraction", "ice_mass_fraction")
IN_SCOPE_READERS = ("core_state", "cmb_heat_flux", "core_energy_balance", "core_entropy_production",
                    "core_thermal_history", "internal_heat_nontidal")
EARTH_RADIUS_M = 6.371e6           # interior.EARTH_RADIUS_M at 097a8aa3
#: Switch-over note 7 (directing, r2): core_energy.find_root bisects on the sign of f with no residual check, so where
#: f jumps (inner-core nucleation) it returns the jump as a «root». A root must meet this |f / Q_CMB| (route B's own
#: bound in engine/test_core_energy.py; true roots sit near 1e-12), fixed before any comparison.
BALANCE_TOL = 1e-9


def _q(answer, key):
    for q in answer.quantities:
        if q.key == key:
            return q.point
    return None


def old_values(answer, declared_imf: float | None = None) -> tuple[dict, dict]:
    """(values, units) of the injected interior_layers Result, in the old units (interior.py:5002–5073). Where the
    Answer has no such quantity (a coreless body; no temperature path), the old engine wrote 0 into the slot, and so
    does this (comparator post-freeze note 1, «zero means absent»; r2 run_oracle B2)."""
    z = lambda v: 0.0 if v is None else v
    r = _q(answer, "radius")
    rc = z(_q(answer, "core_radius"))
    t_cmb = z(_q(answer, "cmb_temperature"))
    vals = {"nmoi": _q(answer, "nmoi"), "core_temperature": z(_q(answer, "core_temperature")),
            "cmb_temperature": t_cmb, "cmb_temperature_core": t_cmb, "cmb_temperature_mantle": t_cmb,
            "cmb_pressure": z(_q(answer, "cmb_pressure")) / 1e9, "core_radius": rc / EARTH_RADIUS_M,
            "core_radius_fraction": rc / r, "radius": r / EARTH_RADIUS_M,
            "core_pressure": _q(answer, "core_pressure") / 1e9, "converged": True,
            "core_mass_fraction": z(_q(answer, "core_mass_fraction")),
            "ice_mass_fraction": 0.0 if declared_imf is None else declared_imf}
    units = {"nmoi": "dimensionless", "core_temperature": "K", "cmb_temperature": "K",
             "cmb_temperature_core": "K", "cmb_temperature_mantle": "K", "cmb_pressure": "GPa",
             "core_radius": "R_earth", "core_radius_fraction": "dimensionless", "radius": "R_earth",
             "core_pressure": "GPa", "converged": "", "core_mass_fraction": "dimensionless",
             "ice_mass_fraction": "dimensionless"}
    if _q(answer, "core_mass_fraction") is None:
        # the old interior_layers wrote no core_mass_fraction for a body without one (O1 dante_fixture at 097a8aa3:
        # the key is absent), so internal_heat_nontidal read None and declined («core_mass_fraction 이 선언되지 않아
        # …»). A 0 here made it answer (T0 flip, c8). Verdict parity: directing 2026-10-10 ~00:00 «Dante
        # internal_heat_nontidal verdict». A body whose CMF is inferred (Venus, Mars) still carries it, as the old did.
        del vals["core_mass_fraction"], units["core_mass_fraction"]
    return vals, units


@dataclass
class ChainRun:
    body: object            # the old BodyState after the chain ran
    injected: object        # the injected interior_layers Result
    declared_keys: frozenset = frozenset()   # the v1 body's own declared input keys, before any control edits
    table_reads: tuple = ()                   # (path, blob, grid returned?) of every structure_grid.load_for call
    notes: tuple = ()                         # Note dicts the chain adds to the record (core_balance_not_solved)


def balance_guard(r, roots=()):
    """(Result, note dict or None) for core_energy_balance. `roots`: (dtc_dt, h, T, residual) of every find_root call the
    node made, in order — the central root first, then the four dTc/dt × H band corners (core_energy.solve). A root
    must meet BALANCE_TOL (68 H1, directing: no root, no value):
    - the central root (balance_residual) fails → an out-of-domain Result (no values, so no later node reads them);
    - a band corner fails → core_cmb_temperature_solved_min/_max become None, the centre's values stand;
    either way the Note core_balance_not_solved names the failing roots. The structure answer is untouched (note 13
    §2's precedent for sensitivity)."""
    if not r.applicable:
        return r, None
    res = (r.values or {}).get("balance_residual")
    corners = [{"dtc_dt": d, "h": h, "t": t, "residual": x} for d, h, t, x in roots[1:]
               if t is not None and x is not None and abs(x) > BALANCE_TOL]
    centre_bad = res is not None and abs(res) > BALANCE_TOL
    if not centre_bad and not corners:
        return r, None
    reason = "root on a discontinuity"
    fields = {"residual": res, "tolerance": BALANCE_TOL, "reason": reason, "failed": "centre" if centre_bad else "corners",
              "corners": corners}
    if centre_bad:
        text = (f"core_energy_balance: |balance_residual| {abs(res):.3g} > {BALANCE_TOL:g}; the bisection's sign change "
                f"is not a root ({reason}), so the node gives no values")
        out = payload.out_of_domain(r.recipe, r.version, text, inputs=dict(r.inputs), refs=tuple(r.refs or ()),
                                    notes=tuple(r.notes or ()))
    else:
        text = (f"core_energy_balance: {len(corners)} band corner root(s) past {BALANCE_TOL:g} ({reason}); "
                f"core_cmb_temperature_solved_min/_max give no value, the central root stands")
        vals = {**r.values, "core_cmb_temperature_solved_min": None, "core_cmb_temperature_solved_max": None}
        out = dataclasses.replace(r, values=vals)
    return out, {"type": "Note", "kind": "core_balance_not_solved", "text": text, "fields": fields}


def run_chain(v1_yaml: str | os.PathLike, answer, serve_cmf_from_declared: bool = False,
              t_pot: float | None = None, serve_from_declared: tuple = (), refusal_text: str | None = None
              ) -> ChainRun:
    """Run the old chain on the new structure. `t_pot` overrides the old body's potential temperature in memory (an
    O9 state; the solve used the same value). `serve_cmf_from_declared` is a negative control only (S8): it puts the
    rewrite's CMF into the declared inputs instead of the interior_layers output."""
    registry.load_all()                              # import every recipe module (as run.py / dump.py do)
    body, _expected = run.load_body(Path(v1_yaml))
    declared_keys = frozenset(body.inputs)
    if t_pot is not None:
        cur = body.inputs.get("potential_temperature")
        body.inputs["potential_temperature"] = ({**cur, "value": t_pot} if isinstance(cur, dict) else t_pot)
    imf = body.inputs.get("ice_mass_fraction")
    imf = getattr(imf, "get", lambda k, d=None: None)("value") if isinstance(imf, dict) else imf
    if refusal_text is not None:
        injected = payload.out_of_domain("interior-structure-methodology", "rewrite-phase1", refusal_text, inputs={})
        return _run(body, injected, declared_keys)
    vals, units = old_values(answer, imf)
    for k in (("core_mass_fraction",) if serve_cmf_from_declared else ()) + tuple(serve_from_declared):
        body.inputs[k] = vals.pop(k)                 # negative controls only: a structure key moved to the inputs
        units.pop(k)
    injected = payload.Result(recipe="interior-structure-methodology", version="rewrite-phase1", regime="rewrite",
                              reason="rewrite solver Answer (solver.legacy_view)", grade="judgment", inputs={},
                              values=vals, units=units, converged=True)
    return _run(body, injected, declared_keys)


def _run(body, injected, declared_keys) -> ChainRun:
    """The old chain with interior_layers replaced by `injected` (an Answer as an old Result, or the rewrite's refusal
    as an out-of-domain Result, so the old nodes decline as they did; r2 run_oracle B3). Every structure_grid.load_for
    call is recorded with the table file's git blob, so «table read» is what was actually read (r2 B1)."""
    import hashlib
    import structure_grid
    reads = []
    orig_load = structure_grid.load_for

    def load_for(state):
        path = structure_grid._path_for(state.name)
        blob = None
        if path.exists():
            data = path.read_bytes()
            blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        got = orig_load(state)
        reads.append((str(path.relative_to(Path(lm._ENGINE).parent)), blob, got[0] is not None))
        return got
    orig_get = registry.get
    notes = []

    def guarded(fn):
        if fn is None:
            return None

        def run_balance(b):
            import core_energy as ce
            real, roots = ce.find_root, []

            def find_root(t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt=ce.DTC_DT, h=ce.H_CORE, t_hi=None):
                t = real(t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h, t_hi)
                x = None
                if t is not None:
                    f, bl, _terms = ce.balance(t, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h)
                    x = f / max(bl["q_c_w"], 1.0)                  # as core_energy.solve's balance_residual
                roots.append((dtc_dt, h, t, x))
                return t
            ce.find_root = find_root
            try:
                got = fn(b)
            finally:
                ce.find_root = real
            r, note = balance_guard(got, tuple(roots))
            note is not None and notes.append(note)
            return r
        return run_balance

    registry.get = lambda node: ((lambda b: injected) if node == "interior_layers" else
                                 guarded(orig_get(node)) if node == "core_energy_balance" else orig_get(node))
    structure_grid.load_for = load_for
    try:
        run.solve(body, run.load_chain())
    finally:
        registry.get = orig_get
        structure_grid.load_for = orig_load
    return ChainRun(body, injected, declared_keys, tuple(reads), tuple(notes))


class LookupLogOff(RuntimeError):
    """The old lookup log is off (NEARSTARS_LOOKUP_LOG=0) or recorded nothing, so the read checks have nothing to
    judge; an empty log looks exactly like a clean one (engine state.py `log_enabled`), so this is a STOP, never a
    pass (P1R-G3-C-03)."""


def _log_on(chain: ChainRun):
    if not BodyState.log_enabled() or not chain.body.lookups:
        raise LookupLogOff(f"{chain.body.name}: the old lookup log is {'off' if not BodyState.log_enabled() else 'empty'}"
                           "; the registration §3 read checks cannot run (unset NEARSTARS_LOOKUP_LOG)")


def reads(chain: ChainRun) -> dict:
    """{reader: {"outputs": set, "declared": set, "other": set}} for the in-scope readers, from the old lookup log.
    «outputs»: answered by the injected interior_layers Result; «declared»: answered by the body's inputs;
    «other»: answered by another node. LookupLogOff when the log is off or empty (G3-C-03)."""
    _log_on(chain)
    body = chain.body
    out = {}
    for reader, key, kind in body.lookups:
        if reader not in IN_SCOPE_READERS or not kind.endswith("hit"):
            continue
        prod = body._producer(key)
        side = "declared" if prod is None else ("outputs" if prod == "interior_layers" else "other")
        out.setdefault(reader, {"outputs": set(), "declared": set(), "other": set()})[side].add(key)
    return out


#: The «other» bucket (registration note 5): keys an in-scope reader takes from another old node (e.g. core_state's
#: core_cmb_temperature_used). They belong to the old chain, not to the structure contract, and are not judged here.
STRUCTURE_KEYS = frozenset(OUTPUT_KEYS) | {"nmoi", "cmb_temperature_core", "cmb_temperature_mantle",
                                          "core_radius_fraction"}


def check_reads(chain: ChainRun) -> list:
    """Violations of registration §3 as amended by note 5, empty when the chain reads as registered:
    - an output read (answered by the injected interior_layers) outside OUTPUT_KEYS;
    - a structure key read from the declared side, unless the v1 body itself declares it (Earth's CMF);
    - a registered output key an in-scope reader asked for and missed (no producer answered it)."""
    bad = []
    body = chain.body
    for reader, sides in reads(chain).items():          # LookupLogOff when the log is off (G3-C-03)
        for k in sorted(sides["outputs"] - set(OUTPUT_KEYS)):
            bad.append((reader, k, "output read outside the registered set"))
        for k in sorted(sides["declared"] & STRUCTURE_KEYS):
            if k not in chain.declared_keys:
                bad.append((reader, k, "structure key served from the declared side"))
    for reader, key, kind in body.lookups:
        if reader in IN_SCOPE_READERS and kind.endswith("miss") and key in OUTPUT_KEYS:
            bad.append((reader, key, "registered output missed"))
    return bad
