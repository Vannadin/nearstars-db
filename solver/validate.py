# 천체 파일 검사 — yaml 을 읽어 Body 또는 이름 붙은 거절 하나를 낸다; 몸 파일을 읽는 유일한 곳 (phase1-design D-A7-1..5).
"""The input boundary of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A7-1..5, §X1).

`load(path)` parses a v2 body file with the project loader and calls `validate(raw)`. Both return a `Body` or a
`Refusal`; neither raises on bad input. The schema (`data/schema.yaml`) is the closed key vocabulary, and the
role registry (`data/roles.yaml`) decides layer order and named interfaces.
"""
from __future__ import annotations

import difflib
import math
import re
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Protocol

import yaml

from solver import body as bd
from solver import refusals as rf
from solver.result import Refusal

SCHEMA_PATH = Path(__file__).resolve().parent / "data" / "schema.yaml"
SCHEMA = MappingProxyType(yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8")))

#: Unit factors to SI. Earth mass and radius are the old engine's (engine/interior.py:80–81 at 097a8aa3), so a
#: converted body solves the oracle's mass and radius bit for bit.
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6
KM = 1.0e3
BLOCK_FIELDS = ("value", "unit", "grade", "source", "counter_evidence_searched", "note", "band", "uncertainty",
                "uncertainty_basis")
TRIO = ("grade", "source", "counter_evidence_searched")


# ── the loader (D-A7-2) ───────────────────────────────────────────────────────────────────────────────────────
class DuplicateKey(Exception):
    def __init__(self, key, line):
        super().__init__(key, line)
        self.key, self.line = key, line


class Loader(yaml.SafeLoader):
    """PyYAML's SafeLoader with YAML 1.2 core-schema floats and booleans, and duplicate keys refused.

    PyYAML is YAML 1.1: it reads `6.0e21` as a string (R-A1-14) and `no`/`on` as booleans. Here a float is the
    1.2 core form and a boolean is `true`/`false` only. Finiteness is checked after conversion (`1e400` → inf)."""


Loader.yaml_implicit_resolvers = {
    ch: [(tag, rx) for tag, rx in rs if tag not in ("tag:yaml.org,2002:float", "tag:yaml.org,2002:bool")]
    for ch, rs in yaml.SafeLoader.yaml_implicit_resolvers.items()}
Loader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"),
    list("-+0123456789."))
Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
                             list("tTfF"))


def _construct_mapping(loader, node, deep=False):
    seen = {}
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise DuplicateKey(key, key_node.start_mark.line + 1)
        seen[key] = True
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


Loader.add_constructor("tag:yaml.org,2002:map",
                       lambda loader, node: _construct_mapping(loader, node, deep=True))


def parse(text: str):
    return yaml.load(text, Loader=Loader)


# ── materials (asked, not copied: D-A7-4) ─────────────────────────────────────────────────────────────────────
class Materials(Protocol):
    def known(self, material_id: str) -> bool: ...

    def composition_window(self, material_id: str, system: str) -> Mapping | None:
        """component → (lo, hi, source), or None when the material declares no window."""


# ── checks ────────────────────────────────────────────────────────────────────────────────────────────────────
class _Refuse(Exception):
    def __init__(self, refusal: Refusal):
        super().__init__(refusal.id)
        self.refusal = refusal


def _no(id_, where, **ev):
    raise _Refuse(rf.make(id_, where, **ev))


def _nearest(key, known):
    hit = difflib.get_close_matches(str(key), list(known), n=1, cutoff=0.0)
    return hit[0] if hit else ""


def _keys(m: Mapping, allowed, where):
    for k in m:
        if k not in allowed:
            _no("input.unknown_key", where, key=str(k), nearest=_nearest(k, allowed))


def _number(v, key, where, domain=None):
    if v is None:
        _no("input.null_value", where, key=key)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        _no("input.not_number", where, key=key, got=repr(v))
    if not math.isfinite(v):
        _no("input.non_finite", where, key=key, got=repr(v))
    for op, bound in (domain or {}).items():
        ok = {"gt": v > bound, "ge": v >= bound, "lt": v < bound, "le": v <= bound}[op]
        if not ok:
            _no("input.out_of_domain", where, key=key, value=repr(v), domain=dict(domain))
    return float(v)


def _text(v, key, where):
    if v is None:
        _no("input.null_value", where, key=key)
    if not isinstance(v, str) or not v:
        _no("input.not_text", where, key=key, got=repr(v))
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
        _no("input.not_boolean", where, key=key, got=repr(v))
    return v


def _grade(g, key, where):
    grades = SCHEMA["grades"]
    if g in grades["forbidden"] or g not in grades["input"]:
        _no("input.bad_grade", where, key=key, grade=str(g), allowed=list(grades["input"]))


def _trio(blk: Mapping, key, where):
    empty = [f for f in TRIO if not blk.get(f)]
    if empty:
        _no("input.provenance_missing", where, key=key, fields=empty)


def _block(v, key, where, spec, value_check) -> bd.Declared:
    """A scalar-with-provenance block (D-A7-3)."""
    if not isinstance(v, Mapping):
        _no("input.cross_field", where, rule="this key is a block {value, grade, source, …}", detail=f"{key}: {v!r}"[:120])
    _keys(v, BLOCK_FIELDS + tuple(spec.get("extra_fields", ())), f"{where}.{key}")
    if "value" not in v:
        _no("input.value_missing", where, key=key)
    value = value_check(v["value"])
    for f in ("grade", "source", "counter_evidence_searched", "note"):
        if f in v and v[f] is None:
            _no("input.null_value", where, key=f"{key}.{f}")
    if "grade" in v:
        _grade(v["grade"], key, where)
    if spec.get("provenance"):
        _trio(v, key, where)
    unit = v.get("unit")
    if unit is not None and unit != spec.get("unit"):
        _no("input.unit_mismatch", where, key=key, got=str(unit), expected=str(spec.get("unit")))
    band = None
    if "band" in v:
        b = v["band"]
        if not isinstance(b, Mapping) or set(b) != {"lo", "hi"}:
            _no("input.cross_field", where, rule="band is {lo, hi}", detail=f"{key}: {b!r}")
        band = (_number(b["lo"], f"{key}.band.lo", where), _number(b["hi"], f"{key}.band.hi", where))
        if band[0] > band[1]:
            _no("input.cross_field", where, rule="band lo ≤ hi", detail=f"{key}: {band}")
    unc = basis = None
    if "uncertainty" in v or "uncertainty_basis" in v:
        unc = _number(v.get("uncertainty"), f"{key}.uncertainty", where, {"ge": 0})
        basis = _enum(v.get("uncertainty_basis"), f"{key}.uncertainty_basis", where, bd.UNCERTAINTY_BASES)
    return bd.Declared(value=value, unit=spec.get("unit"), grade=v.get("grade"), source=v.get("source"),
                       counter_evidence_searched=v.get("counter_evidence_searched"), note=v.get("note"),
                       band=band, uncertainty=unc, uncertainty_basis=basis)


def _leaf_trio(v, key, where):
    """R-A1-1: inside a record with leaf provenance, every block with a `value` carries the trio."""
    if isinstance(v, Mapping):
        if "value" in v:
            if v["value"] is None:
                _no("input.null_value", where, key=f"{key}.value")
            _trio(v, key, where)
            if "grade" in v:
                _grade(v["grade"], key, where)
        else:
            for k, sub in v.items():
                _leaf_trio(sub, f"{key}.{k}", where)
    elif v is None:
        _no("input.null_value", where, key=key)
    elif isinstance(v, float) and not math.isfinite(v):
        _no("input.non_finite", where, key=key, got=repr(v))


def _input(key, v, spec, where):
    shape = spec["shape"]
    dom = spec.get("domain")
    if v is None:
        _no("input.null_value", where, key=key)
    if shape == "bool":
        return _bool(v, key, where)
    if shape == "enum":
        return _enum(v, key, where, spec["values"])
    if shape == "number":
        return _number(v, key, where, dom)
    if shape == "number_or_block":
        if isinstance(v, Mapping):
            return _block(v, key, where, spec, lambda x: _number(x, f"{key}.value", where, dom))
        return _number(v, key, where, dom)
    if shape == "block":
        if spec.get("value_shape") == "enum":
            check = lambda x: _enum(x, f"{key}.value", where, spec["values"])        # noqa: E731
        elif spec.get("value_shape") == "mapping":
            def check(x):
                if not isinstance(x, Mapping):
                    _no("input.cross_field", where, rule="value is a mapping", detail=f"{key}: {x!r}")
                return x
        else:
            check = lambda x: _number(x, f"{key}.value", where, dom)                 # noqa: E731
        return _block(v, key, where, spec, check)
    if shape == "record":
        if not isinstance(v, Mapping):
            _no("input.cross_field", where, rule="a record is a mapping", detail=f"{key}: {v!r}")
        fields = spec.get("fields", {})
        _keys(v, tuple(fields) + tuple(spec.get("meta", ())), f"{where}.{key}")
        for f, fs in fields.items():
            if f in v and fs.get("shape") == "number":
                _number(v[f], f"{key}.{f}", where, fs.get("domain"))
        if "grade" in v:
            _grade(v["grade"], key, where)
        if spec.get("leaf_provenance"):
            _leaf_trio(v, key, where)
        return bd.Declared(value=v)
    raise AssertionError(f"schema shape {shape!r} for {key}")


def _value(x):
    return x.value if isinstance(x, bd.Declared) else x


def _extent(raw, lid, where, ids_below, roles_below):
    if not isinstance(raw, Mapping) or len(raw) != 1:
        _no("input.extent_invalid", where, layer_id=lid, why=f"extent is one form of {list(SCHEMA['extent'])}")
    (kind, v), = raw.items()
    spec = SCHEMA["extent"].get(kind)
    if spec is None:
        _no("input.extent_invalid", where, layer_id=lid, why=f"unknown form {kind!r}")
    if kind == "phase":
        return bd.Extent("phase", ref=_text(v, f"{lid}.extent.phase", where))
    if kind == "thickness_above":
        if not isinstance(v, Mapping) or set(v) != {"layer", "km"}:
            _no("input.extent_invalid", where, layer_id=lid, why="thickness_above is {layer, km}")
        ref = _text(v["layer"], f"{lid}.extent.thickness_above.layer", where)
        if not ids_below or ref != ids_below[-1] or bd.family(roles_below[-1]) != "core":
            _no("input.thickness_above_pattern", where, layer_id=lid, ref=ref)
        km = _number(v["km"], f"{lid}.extent.thickness_above.km", where, spec["domain"])
        return bd.Extent("thickness_above", km * KM, ref)
    x = _number(v, f"{lid}.extent.{kind}", where, spec["domain"])
    return bd.Extent(kind, x * KM if spec["unit"] == "km" else x)


def _layers(raw, where, materials: Materials | None) -> tuple:
    if not isinstance(raw, list) or not raw:
        _no("input.cross_field", where, rule="layers is a non-empty list", detail=repr(raw)[:80])
    spec = SCHEMA["layer"]
    out, ids, roles = [], [], []
    for i, l in enumerate(raw):
        w = f"{where}.layers[{i}]"
        if not isinstance(l, Mapping):
            _no("input.cross_field", w, rule="a layer is a mapping", detail=repr(l)[:80])
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
        t_decl = _number(l["t_declared"], f"{lid}.t_declared", w, spec["t_declared"]["domain"]) \
            if "t_declared" in l else None
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
                if isinstance(x, (int, float)) and not isinstance(x, bool):
                    _number(x, f"{lid}.composition.{c}", w)
                    if window and c in window and not window[c][0] <= x <= window[c][1]:
                        _no("input.composition_window", w, layer_id=lid, component=str(c), value=x,
                            window=[window[c][0], window[c][1]], source=window[c][2])
                elif x != "fit":
                    _no("input.not_number", w, key=f"{lid}.composition.{c}", got=repr(x))
        params = {}
        for pk, pv in (l.get("params") or {}).items():
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
    return [(l.id, c) for l in layers if l.composition is not None
            for c, x in l.composition.value.items() if x == "fit"]


def _closure(raw, layers, has_radius, where) -> bd.Closure:
    if not isinstance(raw, Mapping):
        _no("input.cross_field", where, rule="closure is a mapping", detail=repr(raw)[:80])
    _keys(raw, ("kind", "layer", "name", "lo", "hi"), f"{where}.closure")
    kinds = SCHEMA["closure"]["kinds"]
    kind = _enum(raw.get("kind"), "closure.kind", where, tuple(kinds))
    layer = _text(raw["layer"], "closure.layer", where) if "layer" in raw else None
    name = _text(raw["name"], "closure.name", where) if "name" in raw else None
    ids = [l.id for l in layers]
    if layer is not None and layer not in ids:
        _no("input.cross_field", where, rule="closure names a layer of the list", detail=layer)
    fits = _fits(layers)
    free = [f"closure {kind}" + (f"({layer}.{name})" if name else f"({layer})" if layer else "")]
    free += [f"{lid}.composition.{c} = fit" for lid, c in fits if not (kind == "composition" and (lid, c) == (layer, name))]
    if kind == "composition" and (layer, name) not in fits:
        free = free[1:]          # the closure's axis is not declared «fit»: the closure has nothing to solve
    if len(free) != 1:
        _no("input.closure_count", where, count=len(free), free=free)
    if kind in ("boundary_mass", "composition") and not has_radius:
        _no("input.cross_field", where, rule="an inverse closure needs radius_earth", detail=kind)
    if kind == "boundary_mass":
        lay = layers[ids.index(layer)] if layer in ids else None
        if lay is None or lay.extent is not None:
            _no("input.cross_field", where, rule="boundary_mass solves a layer declared without extent", detail=str(layer))
    spec = kinds[kind]
    default = spec.get("defaults", {}).get(name) if kind == "composition" else spec.get("default")
    lo = _number(raw["lo"], "closure.lo", where) if "lo" in raw else (default[0] if default else None)
    hi = _number(raw["hi"], "closure.hi", where) if "hi" in raw else (default[1] if default else None)
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


def validate(raw, where: str = "<body>", materials: Materials | None = None) -> bd.Body | Refusal:
    """§X1: a raw mapping → a frozen `Body`, or the first named refusal in a fixed check order."""
    try:
        return _validate(raw, where, materials)
    except _Refuse as r:
        return r.refusal


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
    inputs = raw["inputs"]
    if not isinstance(inputs, Mapping):
        _no("input.cross_field", where, rule="inputs is a mapping", detail=repr(inputs)[:80])
    ispec = SCHEMA["inputs"]
    _keys(inputs, tuple(ispec), f"{where}.inputs")
    for k, s in ispec.items():
        if s.get("required") and k not in inputs:
            _no("input.missing_key", f"{where}.inputs", key=k)
    got = {k: _input(k, v, ispec[k], f"{where}.inputs") for k, v in inputs.items()}
    layers = _layers(raw["layers"], where, materials)
    closure = _closure(raw["closure"], layers, "radius_earth" in got, where)
    _remainders(layers, closure, where)
    jumps = {}
    jspec = SCHEMA["jump"]
    names = {b.name for b in bd.derive_boundaries(layers)} | {b.interface for b in bd.derive_boundaries(layers)
                                                             if b.interface}
    for j, v in (raw.get("jumps") or {}).items():
        if j not in names:
            _no("input.jump_boundary", where, boundary=str(j), known=sorted(names))
        got_j = _input(f"jumps.{j}", v, {"shape": "number_or_block", **jspec}, where)
        jumps[j] = got_j if isinstance(got_j, bd.Declared) else bd.Declared(value=got_j, unit="K")
    radius = got.get("radius_earth")
    if radius is not None:
        r = _value(radius) * EARTH_RADIUS_M
        radius = bd.Declared(value=r, unit="m") if not isinstance(radius, bd.Declared) else \
            bd.Declared(value=r, unit="m", grade=radius.grade, source=radius.source,
                        counter_evidence_searched=radius.counter_evidence_searched, note=radius.note,
                        band=tuple(x * EARTH_RADIUS_M for x in radius.band) if radius.band else None,
                        uncertainty=radius.uncertainty * EARTH_RADIUS_M if radius.uncertainty is not None else None,
                        uncertainty_basis=radius.uncertainty_basis)
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
                   solver_flags={k: v for k, v in by["solver"].items() if isinstance(v, bool)},
                   later_tools=by["later-tools"])


def load(path, materials: Materials | None = None) -> bd.Body | Refusal:
    """D-A7-1: the only reader of body files. Parses with `Loader`, then `validate`."""
    where = Path(path).name
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        return rf.make("input.unreadable", where, path=str(path), error=type(e).__name__)
    try:
        raw = parse(text)
    except DuplicateKey as e:
        return rf.make("input.duplicate_key", where, key=str(e.key), line=e.line)
    except yaml.YAMLError as e:
        return rf.make("input.unreadable", where, path=str(path), error=str(e).splitlines()[0][:160])
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
