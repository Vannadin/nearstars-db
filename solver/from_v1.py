# 옛 천체 파일(v1) 변환기 — 오늘의 bodies/*.yaml 을 층 목록(v2)으로 옮기고, 옮기며 고친 것을 이름 붙은 메모로 남긴다 (D-A2-6/7, c8 메모 1).
"""v1 → v2 body conversion (`rewrite/phase1-design.frozen.md` D-A2-6, D-A2-7; `rewrite/phase1-impl-c8.frozen.md`
post-freeze note 1).

`load_v1(path)` reads a v1 body file the way the old engine does (PyYAML `safe_load`, YAML 1.1: that is v1's own
grammar), maps it to a v2 raw document with `from_v1`, and validates that with `validate.validate`. It returns
`(Body | Refusal, aside)`. `aside` holds what is not body input: the v1 `expected:`, `transfers:` and `units:`
sections, for the comparator and run.py-style checks.

Every change the conversion makes to a v1 value or shape is a typed `Note` on the Body; nothing is changed silently.
A v1 body whose layer list would need a solve (the old inversion axis) and is not in the fixed table is refused.
"""
from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml

from solver import refusals as rf
from solver import validate as vd
from solver.body import Body
from solver.result import Note, Refusal, freeze
from solver.yamlio import load_data

PRESETS = load_data(Path(__file__).resolve().parent / "data" / "presets.yaml")


def thaw(x):
    """A frozen data value as plain dicts and lists (the v2 raw document is plain data)."""
    if isinstance(x, Mapping):
        return {k: thaw(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return [thaw(v) for v in x]
    return x

#: interior.LIGHT_ELEMENT_PINS at 097a8aa3 (interior.py:5838–5839): the owner box's fixed O · C ends (R-CLE-6).
LIGHT_ELEMENT_PINS = freeze({"box_floor": {"O": 0.01, "C": 0.005}, "box_ceiling": {"O": 0.04, "C": 0.014}})
#: porosity.P_LAB_MAX at 097a8aa3 (porosity.py:84): the compaction experiments' highest pressure (Durham+ 2005). The
#: old porous-rock inversion reads the porosity law only below it (interior.py:5180–5236; c8 note 1 §2 (a)).
P_LAB_MAX_PA = 150.0e6
#: Classes the old engine refuses before any solve (FLUID_CLASSES, interior.py:4033, checked :4149) and classes it can
#: invert (INFERABLE_CLASSES, :5826, checked :6181).
FLUID_CLASSES = ("brown_dwarf", "star")
INFERABLE_CLASSES = ("rocky", "moon", None)

#: Mantle and declared-core material ids the adapter builds from (system, composition) (c8 note 1 §3a; b9 S7).
CORE_LIGHT_MATERIAL = "fe_core_light"
MANTLE_DECL_MATERIAL = "silicate_decl"
BASAL_MATERIAL = "silicate_basal_const"

#: v1 keys the conversion turns into layers or the closure; every other v1 input key is carried as a v2 input.
LAYER_KEYS = ("composition_intent", "core_mass_fraction", "core_material", "ice_mass_fraction",
              "lithosphere_thickness_km", "mantle_composition", "core_light_elements", "light_element_fixing",
              "core_plus_layer_radius_km", "basal_layer_thickness_km", "basal_layer_density")
#: Units of the layer-forming v1 keys (their v2 home is a layer, not the schema's inputs table).
LAYER_UNITS = freeze({"core_mass_fraction": "1", "ice_mass_fraction": "1", "lithosphere_thickness_km": "km",
                      "core_plus_layer_radius_km": "km", "basal_layer_thickness_km": "km", "basal_layer_density": "kg/m3"})
#: v1 unit spellings mapped to the schema's (D-A2-7). The prose unit is matched exactly, never by pattern.
UNIT_ALIASES = freeze({"dimensionless": "1",
                       "Fe#(=100·Fe/(Fe+Mg), 몰비) — 0–100 이지 0–1 이 아니다": "Fe#, molar, 0–100"})


class _Refuse(Exception):
    def __init__(self, r: Refusal):
        super().__init__(r.id)
        self.refusal = r


def _no(id_, where, **ev):
    raise _Refuse(rf.make(id_, where, **ev))


def _val(x):
    return x.get("value") if isinstance(x, Mapping) else x


def _schema_unit(key):
    spec = vd.SCHEMA["inputs"].get(key)
    if spec is not None:
        return spec.get("unit")
    return LAYER_UNITS.get(key)


def _units(doc, inputs, where, notes):
    units = doc.get("units") or {}
    for key, u in units.items():
        want = _schema_unit(key)
        got = UNIT_ALIASES.get(u, u)
        if got != u:
            notes.append(Note("v1_unit_alias", f"v1 unit «{u}» of {key} read as the schema unit «{got}»",
                              {"key": key, "v1": u, "schema": got}))
        if want is not None and got != want:
            _no("input.unit_mismatch", where, key=key, got=str(u), expected=str(want))
    for key, v in inputs.items():
        want = _schema_unit(key)
        if key not in units and want not in (None, "1") and isinstance(_val(v), (int, float)) \
                and not isinstance(_val(v), bool):
            notes.append(Note("v1_unit_assumed", f"{key} has no v1 unit; the schema unit «{want}» is assumed",
                              {"key": key, "schema": want}))


def _block(v1: Mapping, key, notes, drop=()) -> dict:
    """A v1 block as a v2 block: `uncertainty_km` → `uncertainty` (basis «±»), listed v1-only fields dropped."""
    out = {k: thaw(copy.deepcopy(x)) for k, x in v1.items() if k not in drop and k != "uncertainty_km"}
    for k in drop:
        if k in v1:
            notes.append(Note("v1_field_dropped", f"{key}.{k} dropped: v1-only, carried by the v2 shape",
                              {"key": key, "field": k}))
    if "uncertainty_km" in v1:
        out["uncertainty"], out["uncertainty_basis"] = v1["uncertainty_km"], "±"
        notes.append(Note("v1_uncertainty", f"{key}.uncertainty_km read as uncertainty ± in km",
                          {"key": key, "value": v1["uncertainty_km"]}))
    return out


def _preset_layers(inp, where, notes):
    """Declared branch (old `_solve_declared`): the preset's layers, with declared fields winning (R-PO-1..3)."""
    intent = inp.get("composition_intent")
    if intent is None:
        _no("input.v1_unmapped", where, key="core_mass_fraction",
            detail="core_mass_fraction without composition_intent (the old solve refuses composition None)")
    if intent not in PRESETS or intent == "not_expanded" or "layers" not in PRESETS[intent]:
        _no("input.v1_unmapped", where, key="composition_intent",
            detail=f"preset {intent!r} has no registered layer list")
    layers = thaw(PRESETS[intent]["layers"])
    core = layers[0]
    for key, field, now in (("core_mass_fraction", "extent", core["extent"]["mass_fraction"]),
                            ("core_material", "material", core["material"])):
        if key in inp:
            got = _val(inp[key])
            if got != now:
                notes.append(Note("preset_override", f"`composition_intent` '{intent}' 의 `{key}` {now} 을 선언 {got} 이 "
                                  "덮음 — 선언이 이긴다(규칙)", {"intent": intent, "key": key, "preset": now,
                                                               "declared": got}))
            if field == "extent":
                core["extent"] = {"mass_fraction": got}
            else:
                core["material"] = got
    if _val(inp.get("ice_mass_fraction")):
        _no("input.v1_unmapped", where, key="ice_mass_fraction", detail="an ice layer on the declared branch")
    for key in ("mantle_composition", "core_light_elements", "core_plus_layer_radius_km"):
        if key in inp:
            _no("input.v1_unmapped", where, key=key, detail="not on the declared branch at 097a8aa3")
    return layers


def _lid(inp, layers, notes):
    """`lithosphere_thickness_km` → a conductive lid layer below the surface (R-LITHO-2/3, c8 note 1 §3)."""
    blk = inp["lithosphere_thickness_km"]
    mantle_material = layers[-1]["material"]
    layers.append({"id": "lithosphere", "role": "lid", "material": mantle_material, "thermal": "conductive",
                   "extent": {"depth_from_surface": _block(blk, "lithosphere_thickness_km", notes)
                              if isinstance(blk, Mapping) else blk}})
    notes.append(Note("v1_lid_layer", "lithosphere_thickness_km becomes a conductive lid layer of the mantle material",
                      {"material": mantle_material}))


def _venus(inp, where, notes):
    return ([{"id": "core", "role": "core", "material": "fe_prem"},
             {"id": "mantle", "role": "mantle", "material": "silicate"}],
            {"kind": "boundary_mass", "layer": "core"})


def _dante(inp, where, notes):
    if _val(inp.get("ice_mass_fraction")) != 0.0:
        _no("input.v1_unmapped", where, key="ice_mass_fraction", detail="the fixed table's Dante row assumes ice 0")
    notes.append(Note("v1_ice_excluded", "ice_mass_fraction 0.0: no ice layer (it selects the porosity axis in the "
                      "old rule)", {"key": "ice_mass_fraction"}))
    cap = {"value": P_LAB_MAX_PA, "grade": "literature", "source": "porosity.P_LAB_MAX at 097a8aa3 (porosity.py:84), "
           "the compaction experiments' highest pressure, Durham+ 2005",
           "counter_evidence_searched": "the old inversion also built the uncapped envelope (interior.py:5130 ff.) and "
           "judged on the conservative side; v2 carries the capped law only (c8 note 1 §2, r2 non-blocking)"}
    return ([{"id": "rock", "role": "mantle", "material": "silicate",
              "params": {"initial_porosity": "fit", "porosity_p_cap": cap}}],
            {"kind": "composition", "layer": "rock", "name": "initial_porosity"})


def _mars(inp, where, notes):
    cle = inp.get("core_light_elements")
    cplr = inp.get("core_plus_layer_radius_km")
    thick = inp.get("basal_layer_thickness_km")
    dens = inp.get("basal_layer_density")
    mc = inp.get("mantle_composition")
    if not all(isinstance(x, Mapping) for x in (cle, cplr, thick, dens, mc)):
        _no("input.v1_unmapped", where, key="core_plus_layer_radius_km",
            detail="the fixed table's Mars row needs core_light_elements, the basal layer and mantle_composition")
    comp = _val(cle)
    pin = next((n for n, oc in LIGHT_ELEMENT_PINS.items() if comp.get("O") == oc["O"] and comp.get("C") == oc["C"]), None)
    fix = _val(inp.get("light_element_fixing"))
    if fix is not None and fix != pin:
        _no("input.cross_field", where, rule="light_element_fixing agrees with core_light_elements (R-CLE-4)",
            detail=f"fixing {fix!r}, O·C point to {pin!r}")
    if fix is not None:
        notes.append(Note("v1_fixing_checked", f"light_element_fixing «{fix}» agrees with core_light_elements; dropped",
                          {"pin": pin}))
    r_top = _val(cplr)
    r_core = r_top - _val(thick)
    notes.append(Note("v1_core_radius_derived", f"core boundary r = {r_top} − {_val(thick)} = {r_core} km "
                      "(core_plus_layer_radius_km − basal_layer_thickness_km; b9's shared sentence, D-A2-8)",
                      {"r_top_km": r_top, "thickness_km": _val(thick), "r_core_km": r_core}))
    layers = [{"id": "core", "role": "core", "material": CORE_LIGHT_MATERIAL, "system": "iron_alloy",
               "composition": _block(cle, "core_light_elements", notes, drop=("fit",)),
               "extent": {"radius_from_centre": r_core}},
              {"id": "basal", "role": "basal_layer", "material": BASAL_MATERIAL,
               "extent": {"radius_from_centre": _block(cplr, "core_plus_layer_radius_km", notes)},
               "params": {"density": _block(dens, "basal_layer_density", notes),
                          "thickness_km": _block(thick, "basal_layer_thickness_km", notes)}},
              {"id": "mantle", "role": "mantle", "material": MANTLE_DECL_MATERIAL, "system": "silicate",
               # the v1 grade and source are carried verbatim: «measured» = a paper's value for this body, and the
               # grade is never upgraded (phase-2 impl note 2 item 5)
               "composition": {**_block(mc, "mantle_composition", notes), "source_kind": "measured"}}]
    return layers, {"kind": "composition", "layer": "core", "name": "S"}


#: The layer-forming keys each branch consumes; any other layer-forming key present is refused.
BRANCH_KEYS = freeze({
    "declared": ("composition_intent", "core_mass_fraction", "core_material", "ice_mass_fraction",
                 "lithosphere_thickness_km"),
    "Venus": ("lithosphere_thickness_km",),
    "Dante (fixture)": ("ice_mass_fraction", "lithosphere_thickness_km"),
    "Mars": ("mantle_composition", "core_light_elements", "light_element_fixing", "core_plus_layer_radius_km",
             "basal_layer_thickness_km", "basal_layer_density", "lithosphere_thickness_km"),
})

#: The old engine's inversion axis per v1 body, from the Mac run at 097a8aa3 (c8 note 1 §2). Re-checked against
#: O1 when the PC capture lands; a mismatch is a STOP.
INVERSION_TABLE = MappingProxyType({"Venus": _venus, "Dante (fixture)": _dante, "Mars": _mars})


def from_v1(doc, where: str = "<v1>"):
    """A v1 document → (v2 raw document, notes, aside), or a Refusal. Never raises on input."""
    try:
        return _from_v1(doc, where)
    except _Refuse as r:
        return r.refusal
    except (TypeError, AttributeError, KeyError, ValueError) as e:     # a malformed v1 shape (r2 fix-s3 non-blocking)
        return rf.make("input.v1_unmapped", where, key="<document>", detail=f"{type(e).__name__}: {str(e)[:120]}")


def _from_v1(doc, where):
    if doc is None:
        _no("input.empty", where, path=where)
    if not isinstance(doc, Mapping):
        _no("input.not_mapping", where, path=where, got_type=type(doc).__name__)
    notes: list = []
    aside = {k: doc[k] for k in ("expected", "transfers", "units") if k in doc}
    for k in ("expected", "transfers"):
        if k in doc:
            notes.append(Note("v1_aside", f"v1 `{k}:` is not body input; returned beside the Body", {"section": k}))
    _keys = set(doc) - {"name", "kind", "parent", "inputs", "units", "expected", "transfers"}
    if _keys:
        _no("input.v1_unmapped", where, key=sorted(_keys)[0], detail="unknown v1 top-level section")
    if not isinstance(doc.get("inputs"), Mapping):
        _no("input.v1_unmapped", where, key="inputs", detail="v1 inputs is not a mapping")
    if not isinstance(doc.get("units") or {}, Mapping):
        _no("input.v1_unmapped", where, key="units", detail="v1 units is not a mapping")
    inp = dict(doc["inputs"])
    _units(doc, inp, where, notes)
    cls = inp.get("body_class")
    if cls in FLUID_CLASSES:
        _no("input.class_out_of_scope", where, body_class=cls,
            why=vd.SCHEMA["inputs"]["body_class"]["out_of_scope"][cls])
    declared = inp.get("composition_intent") is not None or inp.get("core_mass_fraction") is not None
    if not declared and cls not in INFERABLE_CLASSES:
        _no("input.composition_undeclared", where, body_class=str(cls),
            looked_for="`composition_intent` · `core_mass_fraction`")
    if declared:
        layers = _preset_layers(inp, where, notes)
        closure = {"kind": "R"}
    else:
        row = INVERSION_TABLE.get(doc.get("name"))
        if row is None:
            _no("input.v1_unmapped", where, key="composition",
                detail="the inversion axis needs a solve (core, ice or porosity); declare the closure")
        layers, closure = row(inp, where, notes)
    used = BRANCH_KEYS["declared" if declared else doc.get("name")]
    unused = sorted(k for k in LAYER_KEYS if k in inp and k not in used)
    if unused:                 # a layer-forming key this branch would not consume is refused, never dropped (r2)
        _no("input.v1_unmapped", where, key=unused[0], detail="a layer-forming v1 key this branch does not consume")
    if "lithosphere_thickness_km" in inp:
        if not declared:
            _no("input.v1_unmapped", where, key="lithosphere_thickness_km",
                detail="a lid on an inversion body is refused through phase 1 (R-LITHO-6, owner Q3)")
        _lid(inp, layers, notes)
    raw = {"name": doc.get("name"), "kind": doc.get("kind"),
           "inputs": {k: v for k, v in inp.items() if k not in LAYER_KEYS},
           "layers": layers, "closure": closure}
    if "parent" in doc:
        if doc["parent"] is None:
            notes.append(Note("v1_null_parent", "parent: null read as absent (a free-floating body)", {}))
        else:
            raw["parent"] = doc["parent"]
    return raw, notes, aside


def load_v1(path, materials=None):
    """Read a v1 body file, convert it and validate it: `(Body | Refusal, aside)`."""
    where = Path(path).name
    try:
        doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except OSError as e:
        return rf.make("input.unreadable", where, path=str(path), error=type(e).__name__), {}
    except UnicodeDecodeError as e:
        return rf.make("input.unreadable", where, path=str(path), error=f"not UTF-8 at byte {e.start}"), {}
    except yaml.YAMLError as e:
        return rf.make("input.unreadable", where, path=str(path), error=str(e).splitlines()[0][:160]), {}
    except (RecursionError, ValueError, TypeError) as e:
        return rf.make("input.unreadable", where, path=str(path), error=f"{type(e).__name__}: {str(e)[:120]}"), {}
    try:
        out = from_v1(doc, where)
    except RecursionError:
        return rf.make("input.unreadable", where, path=str(path), error="nesting too deep"), {}
    if isinstance(out, Refusal):
        return out, {}
    raw, notes, aside = out
    body = vd.validate(raw, where, materials)
    if isinstance(body, Body):
        body = replace(body, notes=tuple(notes))
    return body, aside
