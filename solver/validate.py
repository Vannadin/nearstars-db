# 천체 파일 검사 — yaml 을 읽어 Body 또는 이름 붙은 거절 하나를 낸다; 몸 파일을 읽는 유일한 곳 (phase1-design D-A7-1..5).
"""The input boundary of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A7-1..5, §X1).

`load(path)` parses a v2 body file with the project loader (`yamlio`) and calls `validate(raw)`. Both return a
`Body` or a `Refusal`; neither raises on any input. The schema (`data/schema.yaml`) is the closed key vocabulary,
and the role registry (`data/roles.yaml`) decides layer order and named interfaces.

Check order is fixed: top-level keys, inputs (in file order), layers, closure, remainders, jumps, cross-field rules.
Two files with the same content in a different key order may give a different first refusal.

Deferred, recorded here: R-C74-2-9 (a layer declaration without T_pot where the material needs one) needs the
material resolver (b9 S7); v1-only conflicts (R-CLE-4/8) are `from_v1`'s.
"""
from __future__ import annotations

import difflib
import math
from pathlib import Path
from typing import Mapping, Protocol

from solver import body as bd
from solver import refusals as rf
from solver.result import Refusal
from solver.yamlio import LoadError, load_data, parse

SCHEMA_PATH = Path(__file__).resolve().parent / "data" / "schema.yaml"
SCHEMA = load_data(SCHEMA_PATH)

#: Unit factors to SI. Earth mass and radius are the old engine's (engine/interior.py:80–81 at 097a8aa3), so a
#: converted body solves the oracle's mass and radius bit for bit.
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6
KM = 1.0e3
BLOCK_FIELDS = ("value", "unit", "grade", "source", "counter_evidence_searched", "note", "band", "uncertainty",
                "uncertainty_basis")
TRIO = ("grade", "source", "counter_evidence_searched")
TEXT_FIELDS = ("grade", "source", "counter_evidence_searched", "note")
#: Solver inputs that go into `Body.surface` / `Body.radius`; every other solver input rides in `Body.solver_flags`.
SURFACE_KEYS = ("mass_earth", "radius_earth", "potential_temperature", "surface_temperature_k", "surface_pressure_pa")
MAX_DEPTH = 32                     # nesting allowed inside a record (thermal_evolution is 3 deep)


class Materials(Protocol):
    """The material resolver validate asks (D-A7-4); b9's legacy_materials provides it (S7)."""

    def known(self, material_id: str) -> bool: ...

    def composition_window(self, material_id: str, system: str) -> Mapping | None:
        """component → (lo, hi, source), or None when the material declares no window."""


# ── refusal plumbing ──────────────────────────────────────────────────────────────────────────────────────────
class _Refuse(Exception):
    def __init__(self, refusal: Refusal):
        super().__init__(refusal.id)
        self.refusal = refusal


def _no(id_, where, **ev):
    raise _Refuse(rf.make(id_, where, **ev))


def _nearest(key, known):
    hit = difflib.get_close_matches(str(key), [str(k) for k in known], n=1, cutoff=0.0)
    return hit[0] if hit else ""


def _mapping(v, key, where):
    if v is None:
        _no("input.null_value", where, key=key)
    if not isinstance(v, Mapping):
        _no("input.cross_field", where, rule=f"{key} is a mapping", detail=repr(v)[:80])
    return v


def _keys(m: Mapping, allowed, where):
    for k in m:
        if k not in allowed:
            _no("input.unknown_key", where, key=str(k), nearest=_nearest(k, allowed))


# ── scalar checks ─────────────────────────────────────────────────────────────────────────────────────────────
def _number(v, key, where, domain=None, scale=1.0):
    """A finite number in its domain; `scale` converts to SI and the SI value must be finite too."""
    if v is None:
        _no("input.null_value", where, key=key)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        _no("input.not_number", where, key=key, got=repr(v)[:80])
    try:
        f = float(v)
    except OverflowError:
        _no("input.non_finite", where, key=key, got=f"int of {len(str(v))} digits")
    if not math.isfinite(f):
        _no("input.non_finite", where, key=key, got=repr(v))
    for op, bound in (domain or {}).items():
        ok = {"gt": f > bound, "ge": f >= bound, "lt": f < bound, "le": f <= bound}[op]
        if not ok:
            _no("input.out_of_domain", where, key=key, value=repr(v), domain=dict(domain))
    if not math.isfinite(f * scale):
        _no("input.out_of_domain", where, key=key, value=repr(v), domain={"finite in SI": True})
    return f


def _text(v, key, where):
    if v is None:
        _no("input.null_value", where, key=key)
    if not isinstance(v, str) or not v:
        _no("input.not_text", where, key=key, got=repr(v)[:80])
    return v


def _enum(v, key, where, values):
    _text(v, key, where)
    if v not in values:
        _no("input.not_in_vocabulary", where, key=key, got=repr(v), allowed=list(values))
    return v


def _bool(v, key, where):
    if v is None:
        _no("input.null_value", where, key=key)
    if not isinstance(v, bool):
        _no("input.not_boolean", where, key=key, got=repr(v)[:80])
    return v


def _grade(g, key, where):
    grades = SCHEMA["grades"]
    if not isinstance(g, str) or g in grades["forbidden"] or g not in grades["input"]:
        _no("input.bad_grade", where, key=key, grade=str(g), allowed=list(grades["input"]))


def _provenance(blk: Mapping, key, where, rule):
    """`rule`: «trio» = grade · source · counter_evidence_searched (R-A1-12); «shape» = grade, source, and a
    counter_evidence_searched or a note (the block shape, D-A7-3); None = nothing required."""
    if rule == "trio":
        empty = [f for f in TRIO if not blk.get(f)]
    elif rule == "shape":
        empty = [f for f in ("grade", "source") if not blk.get(f)]
        if not blk.get("counter_evidence_searched") and not blk.get("note"):
            empty.append("counter_evidence_searched|note")
    else:
        empty = []
    if empty:
        _no("input.provenance_missing", where, key=key, fields=empty)


def _block(v, key, where, spec, value_check) -> bd.Declared:
    """A scalar-with-provenance block (D-A7-3)."""
    if not isinstance(v, Mapping):
        _no("input.cross_field", where, rule="this key is a block {value, grade, source, …}", detail=f"{key}: {v!r}"[:120])
    extra = tuple(spec.get("extra_fields", ()))
    _keys(v, BLOCK_FIELDS + extra, f"{where}.{key}")
    if "value" not in v:
        _no("input.value_missing", where, key=key)
    value = value_check(v["value"])
    for f in TEXT_FIELDS:
        if f in v:
            _text(v[f], f"{key}.{f}", where)
    if "grade" in v:
        _grade(v["grade"], key, where)
    _provenance(v, key, where, "trio" if spec.get("provenance") is True else spec.get("provenance"))
    unit = v.get("unit")
    if unit is not None and unit != spec.get("unit"):
        _no("input.unit_mismatch", where, key=key, got=str(unit), expected=str(spec.get("unit")))
    band = None
    if "band" in v:
        b = v["band"]
        if not isinstance(b, Mapping) or set(b) != {"lo", "hi"}:
            _no("input.cross_field", where, rule="band is {lo, hi}", detail=f"{key}: {b!r}"[:120])
        si = spec.get("si", 1.0)
        band = (_number(b["lo"], f"{key}.band.lo", where, None, si), _number(b["hi"], f"{key}.band.hi", where, None, si))
        if band[0] > band[1]:
            _no("input.cross_field", where, rule="band lo ≤ hi", detail=f"{key}: {band}")
    unc = basis = None
    if "uncertainty" in v or "uncertainty_basis" in v:
        unc = _number(v.get("uncertainty"), f"{key}.uncertainty", where, {"ge": 0}, spec.get("si", 1.0))
        basis = _enum(v.get("uncertainty_basis"), f"{key}.uncertainty_basis", where, bd.UNCERTAINTY_BASES)
    ex = {f: v[f] for f in extra if f in v}
    return bd.Declared(value=value, unit=spec.get("unit"), grade=v.get("grade"), source=v.get("source"),
                       counter_evidence_searched=v.get("counter_evidence_searched"), note=v.get("note"),
                       band=band, uncertainty=unc, uncertainty_basis=basis, extra=ex)


def _walk(v, key, where, depth, leaf_trio):
    """Records: finite numbers, no nulls, text keys, bounded depth; with `leaf_trio`, every block with a `value`
    carries the trio (R-A1-1)."""
    if depth > MAX_DEPTH:
        _no("input.cross_field", where, rule=f"nesting deeper than {MAX_DEPTH}", detail=key)
    if v is None:
        _no("input.null_value", where, key=key)
    if isinstance(v, Mapping):
        for k in v:
            if not isinstance(k, str):
                _no("input.not_text", where, key=f"{key} key", got=repr(k)[:80])
        if "value" in v and leaf_trio:
            _provenance(v, key, where, "trio")
            if "grade" in v:
                _grade(v["grade"], key, where)
        for k, sub in v.items():
            _walk(sub, f"{key}.{k}", where, depth + 1, leaf_trio)
    elif isinstance(v, (list, tuple)):
        for i, sub in enumerate(v):
            _walk(sub, f"{key}[{i}]", where, depth + 1, leaf_trio)
    elif isinstance(v, (int, float)) and not isinstance(v, bool):
        _number(v, key, where)
    elif not isinstance(v, (str, bool)):
        _no("input.not_text", where, key=key, got=repr(v)[:80])


def _input(key, v, spec, where):
    shape = spec["shape"]
    dom = spec.get("domain")
    si = spec.get("si", 1.0)
    if v is None:
        _no("input.null_value", where, key=key)
    if shape == "bool":
        return _bool(v, key, where)
    if shape == "enum":
        return _enum(v, key, where, spec["values"])
    if shape == "number":
        return _number(v, key, where, dom, si)
    if shape == "number_or_block":
        if isinstance(v, Mapping):
            return _block(v, key, where, {"provenance": "shape", **spec},
                          lambda x: _number(x, f"{key}.value", where, dom, si))
        return _number(v, key, where, dom, si)
    if shape == "block":
        if spec.get("value_shape") == "enum":
            def check(x):
                return _enum(x, f"{key}.value", where, spec["values"])
        elif spec.get("value_shape") == "mapping":
            def check(x):
                _mapping(x, f"{key}.value", where)
                _walk(x, f"{key}.value", where, 1, False)
                return x
        else:
            def check(x):
                return _number(x, f"{key}.value", where, dom, si)
        return _block(v, key, where, {"provenance": "shape", **spec}, check)
    if shape == "record":
        _mapping(v, key, where)
        fields = spec.get("fields", {})
        _keys(v, tuple(fields) + tuple(spec.get("meta", ())), f"{where}.{key}")
        for f, fs in fields.items():
            if f in v and fs.get("shape") == "number":
                _number(v[f], f"{key}.{f}", where, fs.get("domain"))
        for f in TEXT_FIELDS:
            if f in v:
                _text(v[f], f"{key}.{f}", where)
        if "grade" in v:
            _grade(v["grade"], key, where)
        _walk(v, key, where, 0, bool(spec.get("leaf_provenance")))
        if spec.get("check") == "declared_needs_override" and v.get("grade") == "declared" and "override" not in v:
            _no("input.cross_field", where, rule="a radiogenic «declared» grade has its override block (R-GV-4)",
                detail=key)
        return bd.Declared(value=v)
    raise AssertionError(f"schema shape {shape!r} for {key}")


def _value(x):
    return x.value if isinstance(x, bd.Declared) else x


# ── layers ────────────────────────────────────────────────────────────────────────────────────────────────────
def _extent(raw, lid, where, ids_below, roles_below):
    if not isinstance(raw, Mapping) or len(raw) != 1:
        _no("input.extent_invalid", where, layer_id=lid, why=f"extent is one form of {list(SCHEMA['extent'])}")
    (kind, v), = raw.items()
    spec = SCHEMA["extent"].get(kind)
    if spec is None:
        _no("input.extent_invalid", where, layer_id=lid, why=f"unknown form {kind!r}")
    if kind == "phase":
        return bd.Extent("phase", ref=_text(v, f"{lid}.extent.phase", where))
    scale = KM if spec.get("unit") == "km" else 1.0
    if kind == "thickness_above":
        if not isinstance(v, Mapping) or set(v) != {"layer", "km"}:
            _no("input.extent_invalid", where, layer_id=lid, why="thickness_above is {layer, km}")
        ref = _text(v["layer"], f"{lid}.extent.thickness_above.layer", where)
        if not ids_below or ref != ids_below[-1] or bd.family(roles_below[-1]) != "core":
            _no("input.thickness_above_pattern", where, layer_id=lid, ref=ref)
        v, key = v["km"], f"{lid}.extent.thickness_above.km"
    else:
        key = f"{lid}.extent.{kind}"
    if isinstance(v, Mapping):            # a declared extent keeps its provenance (D-A2-2; R-LITHO-1, R-MLD-2)
        decl = _block(v, key, where, {"unit": spec.get("unit"), "provenance": "shape"},
                      lambda y: _number(y, f"{key}.value", where, spec["domain"], scale))
        x = decl.value
    else:
        decl, x = None, _number(v, key, where, spec["domain"], scale)
    ref = ids_below[-1] if kind == "thickness_above" else None
    return bd.Extent(kind, x * scale, ref=ref, declared=decl)


def _layers(raw, where, materials: Materials | None) -> tuple:
    if raw is None:
        _no("input.null_value", where, key="layers")
    if not isinstance(raw, list) or not raw:
        _no("input.cross_field", where, rule="layers is a non-empty list", detail=repr(raw)[:80])
    spec = SCHEMA["layer"]
    out, ids, roles = [], [], []
    for i, l in enumerate(raw):
        w = f"{where}.layers[{i}]"
        _mapping(l, f"layers[{i}]", w)
        _keys(l, tuple(spec), w)
        for k, s in spec.items():
            if s.get("required") and k not in l:
                _no("input.missing_key", w, key=k)
        lid = _text(l["id"], "id", w)
        if lid in ids:
            _no("input.duplicate_layer_id", w, layer_id=lid)
        role = _text(l["role"], f"{lid}.role", w)
        if role not in bd.ROLES["roles"]:
            _no("input.unknown_role", w, layer_id=lid, role=role)
        mat = _text(l["material"], f"{lid}.material", w)
        if materials is not None and not materials.known(mat):
            _no("input.unknown_material", w, layer_id=lid, material=mat)
        ext = _extent(l["extent"], lid, w, ids, roles) if "extent" in l else None
        thermal = _enum(l.get("thermal", "adiabatic"), f"{lid}.thermal", w, spec["thermal"]["values"])
        t_decl = None
        if "t_declared" in l:
            t_decl = _value(_input(f"{lid}.t_declared", l["t_declared"], spec["t_declared"], w))
        if (thermal == "isothermal") != (t_decl is not None):
            _no("input.cross_field", w, rule="t_declared goes with thermal isothermal", detail=lid)
        system = _text(l["system"], f"{lid}.system", w) if "system" in l else None
        comp = None
        if "composition" in l:
            if system is None:
                _no("input.cross_field", w, rule="composition needs a system (R-LAYERGEN-1)", detail=lid)
            comp = _input(f"{lid}.composition", l["composition"], spec["composition"], w)
            window = materials.composition_window(mat, system) if materials is not None else None
            for c, x in comp.value.items():
                if x == "fit":
                    continue
                _number(x, f"{lid}.composition.{c}", w)
                if window and c in window and not window[c][0] <= x <= window[c][1]:
                    _no("input.composition_window", w, layer_id=lid, component=str(c), value=x,
                        window=[window[c][0], window[c][1]], source=window[c][2])
        params = {}
        for pk, pv in _mapping(l.get("params", {}), f"{lid}.params", w).items():
            _text(pk, f"{lid}.params key", w)
            if pv == "fit":                   # a closure axis marker, not a declared value: no trio (c8 note 1 §3a)
                params[pk] = bd.Declared(value="fit")
                continue
            params[pk] = _input(f"{lid}.params.{pk}", pv, {"shape": "block", "provenance": True}, w)
        out.append(bd.Layer(id=lid, role=role, material=mat, extent=ext, thermal=thermal, t_declared=t_decl,
                            system=system, composition=comp, params=params))
        ids.append(lid)
        roles.append(role)
    bad = bd.order_violations(tuple(out))
    if bad:
        pair, rule = bad[0]
        _no("input.layer_order", where, pair=pair, rule=rule)
    return tuple(out)


def _fits(layers) -> list:
    """Each (layer id, axis) marked «fit», in a composition (core S) or in params (rock initial_porosity)."""
    out = [(l.id, c) for l in layers if l.composition is not None
           for c, x in l.composition.value.items() if x == "fit"]
    return out + [(l.id, k) for l in layers for k, d in l.params.items() if d.value == "fit"]


# ── closure (D-A2-8) ──────────────────────────────────────────────────────────────────────────────────────────
def _closure(raw, layers, has_radius, where) -> bd.Closure:
    _mapping(raw, "closure", where)
    kinds = SCHEMA["closure"]["kinds"]
    kind = _enum(raw.get("kind"), "closure.kind", where, tuple(kinds))
    spec = kinds[kind]
    _keys(raw, ("kind", "lo", "hi") + tuple(spec["fields"]), f"{where}.closure")
    for f in spec["fields"]:
        if f not in raw:
            _no("input.missing_key", where, key=f"closure.{f}")
    layer = _text(raw["layer"], "closure.layer", where) if "layer" in raw else None
    name = _text(raw["name"], "closure.name", where) if "name" in raw else None
    ids = [l.id for l in layers]
    if layer is not None and layer not in ids:
        _no("input.cross_field", where, rule="closure names a layer of the list", detail=layer)
    # The closure record and the «fit» markers must agree: exactly one free scalar (D-A2-8, r2 S2-B3).
    fits = set(_fits(layers))
    want = {(layer, name)} if kind == "composition" else set()
    if fits != want:
        extra = sorted(f"{a}.{b} = fit" for a, b in fits - want)
        own = [] if kind == "composition" and (layer, name) not in fits else \
            [f"closure {kind}" + (f"({layer}.{name})" if name else f"({layer})" if layer else "")]
        _no("input.closure_count", where, count=len(own) + len(extra), free=own + extra)
    if kind in ("boundary_mass", "composition") and not has_radius:
        _no("input.cross_field", where, rule="an inverse closure needs radius_earth", detail=kind)
    if kind == "boundary_mass":
        if layers[ids.index(layer)].extent is not None:
            _no("input.cross_field", where, rule="boundary_mass solves a layer declared without extent", detail=layer)
        others = [l.id for l in layers if l.id != layer and l.extent is None]
        if len(others) != 1:
            # with no other remainder the other layers' extents already fix this layer's mass: nothing is free
            _no("input.closure_count", where, count=0,
                free=[f"boundary_mass({layer}) needs exactly one other layer without extent, has {others}"])
    default = spec.get("defaults", {}).get(name) if kind == "composition" else spec.get("default")
    dom = spec.get("domain")
    scale = EARTH_RADIUS_M if kind == "R" else 1.0       # the SI value must stay finite too (r2 fix-s3 B1)
    lo = _number(raw["lo"], "closure.lo", where, dom, scale) if "lo" in raw else (default[0] if default else None)
    hi = _number(raw["hi"], "closure.hi", where, dom, scale) if "hi" in raw else (default[1] if default else None)
    if lo is None or hi is None:
        _no("input.missing_key", where, key="closure.lo/hi (no schema default for this axis)")
    if not lo < hi:
        _no("input.cross_field", where, rule="closure lo < hi", detail=f"[{lo}, {hi}]")
    if kind == "R":
        lo, hi = lo * EARTH_RADIUS_M, hi * EARTH_RADIUS_M
    return bd.Closure(kind=kind, lo=lo, hi=hi, layer=layer, name=name)


def _remainders(layers, closure, where):
    rest = [l.id for l in layers if l.extent is None
            and not (closure.kind == "boundary_mass" and l.id == closure.layer)]
    if len(rest) > 1:
        _no("input.extent_invalid", where, layer_id=rest[1], why=f"only one layer may take the rest of the mass: {rest}")
    fr = [l.extent.value for l in layers if l.extent is not None and l.extent.kind == "mass_fraction"]
    tol = SCHEMA["tolerances"]["mass_fraction_sum"]
    if len(fr) == len(layers) and abs(sum(fr) - 1.0) > tol:
        _no("input.mass_fraction_sum", where, total=sum(fr), tol=tol)
    if sum(fr) > 1.0 + tol:
        _no("input.mass_fraction_sum", where, total=sum(fr), tol=tol)


def _jumps(raw, layers, where):
    bounds = bd.derive_boundaries(layers)
    alias = {b.interface: b.name for b in bounds if b.interface}
    names = {b.name for b in bounds} | set(alias)
    out, hit = {}, {}
    for j, v in _mapping(raw, "jumps", where).items():
        if j not in names:
            _no("input.jump_boundary", where, boundary=str(j), known=sorted(names))
        canon = alias.get(j, j)
        if canon in hit:                     # one boundary named twice, by alias and by id (R-IJ-3)
            _no("input.cross_field", where, rule="a boundary's jump is declared once (R-IJ-3)",
                detail=f"{hit[canon]} and {j} are both {canon}")
        hit[canon] = j
        got = _input(f"jumps.{j}", v, {"shape": "number_or_block", **SCHEMA["jump"]}, where)
        out[j] = got if isinstance(got, bd.Declared) else bd.Declared(value=got, unit="K")
    return out


def _cross_inputs(got, where):
    reg = got.get("tectonic_regime")
    if isinstance(reg, bd.Declared) and "contested" in reg.extra:
        c = reg.extra["contested"]
        if not isinstance(c, tuple) or not c or not all(isinstance(x, str) and x for x in c):
            _no("input.cross_field", where, rule="contested is a non-empty list of sources (R-GV-5)",
                detail=repr(c)[:80])


# ── entry points ──────────────────────────────────────────────────────────────────────────────────────────────
def validate(raw, where: str = "<body>", materials: Materials | None = None) -> bd.Body | Refusal:
    """§X1: a raw mapping → a frozen `Body`, or the first named refusal in a fixed check order. Never raises on input."""
    try:
        return _validate(raw, where, materials)
    except _Refuse as r:
        return r.refusal
    except RecursionError:
        return rf.make("input.cross_field", where, rule=f"nesting deeper than {MAX_DEPTH}", detail="document")


def _declared_or_value(v):
    return v if isinstance(v, bd.Declared) else bd.Declared(value=v)


def _validate(raw, where, materials):
    if raw is None:
        _no("input.empty", where, path=where)
    if not isinstance(raw, Mapping):
        _no("input.not_mapping", where, path=where, got_type=type(raw).__name__)
    top = SCHEMA["top"]
    _keys(raw, tuple(top), where)
    for k, s in top.items():
        if s.get("required") and k not in raw:
            _no("input.missing_key", where, key=k)
    name = _text(raw["name"], "name", where)
    kind = _enum(raw["kind"], "kind", where, top["kind"]["values"])
    parent = _text(raw["parent"], "parent", where) if "parent" in raw else None
    inputs = _mapping(raw["inputs"], "inputs", where)
    ispec = SCHEMA["inputs"]
    _keys(inputs, tuple(ispec), f"{where}.inputs")
    for k, s in ispec.items():
        if s.get("required") and k not in inputs:
            _no("input.missing_key", f"{where}.inputs", key=k)
    got = {k: _input(k, v, ispec[k], f"{where}.inputs") for k, v in inputs.items()}
    cls = _value(got.get("body_class"))
    if cls in ispec["body_class"]["out_of_scope"]:
        _no("input.class_out_of_scope", where, body_class=cls, why=ispec["body_class"]["out_of_scope"][cls])
    _cross_inputs(got, where)
    layers = _layers(raw["layers"], where, materials)
    closure = _closure(raw["closure"], layers, "radius_earth" in got, where)
    _remainders(layers, closure, where)
    jumps = _jumps(raw.get("jumps", {}), layers, where)
    if any(l.thermal == "conductive" for l in layers) and "surface_temperature_k" not in got:
        _no("input.cross_field", where, rule="a conductive layer needs surface_temperature_k (R-LITHO-6)",
            detail=", ".join(l.id for l in layers if l.thermal == "conductive"))
    radius = got.get("radius_earth")
    if radius is not None:
        r = _declared_or_value(radius)
        radius = bd.Declared(value=r.value * EARTH_RADIUS_M, unit="m", grade=r.grade, source=r.source,
                             counter_evidence_searched=r.counter_evidence_searched, note=r.note,
                             band=tuple(x * EARTH_RADIUS_M for x in r.band) if r.band else None,
                             uncertainty=r.uncertainty * EARTH_RADIUS_M if r.uncertainty is not None else None,
                             uncertainty_basis=r.uncertainty_basis)
    p_s = got.get("surface_pressure_pa")
    surface = bd.SurfaceState(
        m=_value(got["mass_earth"]) * EARTH_MASS_KG,
        p_s=_value(p_s) if p_s is not None else None,
        p_s_source="declared" if p_s is not None else "material_floor",
        t_s=_value(got["surface_temperature_k"]) if "surface_temperature_k" in got else None,
        t_pot=_value(got["potential_temperature"]) if "potential_temperature" in got else None)
    by = {"solver": {}, "history": {}, "later-tools": {}}
    for k, v in got.items():
        by[ispec[k]["consumer"]][k] = v
    return bd.Body(name=name, kind=kind, parent=parent, surface=surface, layers=layers, closure=closure,
                   radius=radius, jumps=jumps, declarations=by["history"],
                   solver_flags={k: v for k, v in by["solver"].items() if k not in SURFACE_KEYS},
                   later_tools=by["later-tools"],
                   surface_declared={k: _declared_or_value(v) for k, v in got.items() if k in SURFACE_KEYS})


def load(path, materials: Materials | None = None) -> bd.Body | Refusal:
    """D-A7-1: the only reader of body files. Parses with the project loader, then `validate`. Never raises."""
    where = Path(path).name
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        return rf.make("input.unreadable", where, path=str(path), error=type(e).__name__)
    except UnicodeDecodeError as e:
        return rf.make("input.unreadable", where, path=str(path), error=f"not UTF-8 at byte {e.start}")
    try:
        raw = parse(text)
    except LoadError as e:
        if e.kind == "duplicate_key":
            return rf.make("input.duplicate_key", where, key=str(e.key), line=e.line)
        if e.kind == "bad_key":
            return rf.make("input.not_text", where, key=f"line {e.line} key", got=str(e.key)[:80])
        if e.kind == "bad_tag":
            return rf.make("input.not_text", where, key=f"line {e.line} tag", got=str(e.key)[:80])
        return rf.make("input.unreadable", where, path=str(path), error=e.detail)
    return validate(raw, where, materials)


def load_all(paths, materials: Materials | None = None) -> dict:
    """Each file on its own (W-L10-04): a bad file refuses by its own name and never breaks another's load.
    Two files with one `name` are both refused (input.duplicate_name)."""
    out = {str(p): load(p, materials) for p in sorted(map(str, paths))}
    names = {}
    for p, b in out.items():
        if isinstance(b, bd.Body):
            names.setdefault(b.name, []).append(p)
    for n, ps in names.items():
        if len(ps) > 1:
            for p in ps:
                out[p] = rf.make("input.duplicate_name", Path(p).name, name=n, paths=[Path(x).name for x in ps])
    return out
