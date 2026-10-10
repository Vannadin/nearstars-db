# 물질 등록부 — solver/materials/*.yaml 을 읽어 스키마와 적재 규칙으로 검사하고 등록부를 짓는다; 어긋나면 이름 붙은 적재 멈춤 (phase-2 등록 P2)
"""The material registry (rewrite/phase2-impl.frozen.md P2; design D-M1, D-M2, D-P1, note 1 item 3).

`load()` reads every record under `solver/materials/` (the schema file excepted), checks it against the P1 schema and
the load rules, and returns a `Registry`, or a `LoadStop` naming the first rule a record breaks. Nothing is
hand-listed and nothing raises on a bad record: a STOP is a value with an id and evidence, as a refusal is.

Load rules:
- the schema's closed key lists, required keys and shapes (`material.unknown_key`, `material.missing_key`,
  `material.bad_shape`); the record id equals its file stem;
- D-M2: every phase has a field and a window; where the field passes a finite window edge, that edge declares a band
  or a refusal (`material.edge_undeclared`). Both are allowed; declaring neither is the STOP. A field given only by
  curves is taken as unbounded, so each finite edge must be declared;
- every band states its error's origin (the schema requires `origin`);
- γ has its own window: each thermal set lies inside `gamma_window` (`material.gamma_window`). There is no fallback
  field, so a record carrying one stops as an unknown key;
- the citation form (note 1 item 3): exactly one of cache (with page, where and a 64-hex sha256), `name@version`, or
  `doi:10.…` (`material.bad_cite`). A cache cite's sha256 must match a row of the tracked source manifest
  `solver/materials/sources.yaml` (impl note 3 C3, `material.unregistered_source`). Load never opens the paper cache:
  it is git-ignored, and a host without it must still load. Existence and hash against the file are a P4 test;
- kinds (D-P1): a branched record declares one boundary per adjacent phase pair, naming its phases; a hand-over record
  declares its joins (`material.kind_rule`).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from solver.yamlio import LoadError, load_data, parse
from solver.result import freeze

MATERIALS_DIR = Path(__file__).resolve().parent / "materials"
SCHEMA = load_data(MATERIALS_DIR / "schema.yaml")
#: The tracked source manifest (impl note 3 C3): one row per registered PDF, keyed by sha256.
MANIFEST = MATERIALS_DIR / "sources.yaml"
NOT_RECORDS = ("schema.yaml", "sources.yaml")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_LIB = re.compile(r"^[A-Za-z][\w.-]*@[0-9][\w.+-]*$")
_DOI = re.compile(r"^doi:10\.\d{4,9}/\S+$")
_EDGES = (("p_min", "p_min", "lower"), ("p_max", "p_max", "upper"), ("t_min", "t_min", "lower"),
          ("t_max", "t_max", "upper"))

#: The load STOP ids: (evidence fields, how to fix). A STOP is data, never an exception; the fix text is what the
#: checker prints after «what is wrong» (impl note 3 C2: field / what is wrong / how to fix).
STOPS = MappingProxyType({
    "material.placeholder": (("file", "path", "text"),
                             "Replace the scaffold's FILL placeholder with the value from your source."),
    "material.unreadable": (("file", "detail"),
                            "Fix the YAML syntax at the line named; duplicate keys are not allowed."),
    "material.unknown_key": (("file", "path", "key", "allowed"),
                             "Remove the key or correct its spelling to one of the allowed keys (solver/materials/schema.yaml)."),
    "material.missing_key": (("file", "path", "key"),
                             "Add the key; the scaffold (`python -m solver.materials new`) lists every required key."),
    "material.bad_shape": (("file", "path", "expected", "got"),
                           "Give the value in the expected form (number in SI, text, one of the listed values, or a list)."),
    "material.id_mismatch": (("file", "id"),
                             "Make `id` equal to the file name without .yaml, or rename the file."),
    "material.duplicate_id": (("file", "id"),
                              "Two files declare the same id; rename one."),
    "material.edge_undeclared": (("file", "phase", "edge"),
                                 "The stability field reaches past this window edge: declare `edges.<edge>` as "
                                 "{refusal: input.material_out_of_data} or as a band with form, error, grade and origin."),
    "material.edge_both": (("file", "phase", "edge"),
                           "An edge is either a refusal or a band; keep one."),
    "material.gamma_window": (("file", "phase", "set", "why"),
                              "Move the thermal set's window inside `thermal.gamma_window`, or widen the γ window "
                              "only if a source supports γ there. There is no γ fallback value."),
    "material.bad_cite": (("file", "path", "why"),
                          "Cite where the value was read: {cache, page, where, sha256} for a registered PDF, "
                          "{library: name@version}, {doi: doi:10.…}, {formula: <formula and inputs>}, or "
                          "{user_declared: <reason>} for a value with no source; exactly one."),
    "material.unregistered_source": (("file", "path", "sha256"),
                                     "Register the PDF first: `python -m solver.materials add-source <pdf>` adds its "
                                     "sha256 to solver/materials/sources.yaml."),
    "material.sigma_rule": (("file", "phase", "source", "why"),
                            "Give σ in one of three forms: propagated {from, correlation}, constant {value, "
                            "reduction}, or not_printed {where}; never a stand-in value for an unprinted σ."),
    "material.join_rule": (("file", "phase", "join", "why"),
                           "A join names two of the phase's sources. blend and cross_check need the overlap box; "
                           "blend and taper weigh by P only; a taper needs edge_p and side; k is 2."),
    "material.precedence": (("file", "phase", "why"),
                            "Fix the preferred source before any comparison: measured over computed (rule basis), "
                            "else a declared precedence with its date, or a frozen record as ref. Never swap after a "
                            "gate result."),
    "material.table_check": (("file", "phase", "why"),
                             "Fix the table at the node named: ρ must rise with P on every isotherm, K_T > 0, c_P > 0, "
                             "α inside its declared range, no holes or NaN; a bilinear table needs α and K_T columns."),
    "material.library_pin": (("file", "why"),
                             "Install the pinned library version (pip install --require-hashes from the repo's pin "
                             "file), or update the record's library.version and library.sha256 after a reviewed "
                             "upgrade; the sha256 is material_library.tree_sha256(<name>)."),
    "material.triple_point_miss": (("file", "phases", "why"),
                                   "At a declared mixed triple point the declared curves and the min-G boundary must "
                                   "pass within the tolerance set before measuring; correct the curve or the printed "
                                   "point (impl note 6 item 4), never widen the tolerance after seeing the miss."),
    "material.kind_rule": (("file", "why"),
                           "Match the record kind: single = one phase; branched = one boundary per adjacent phase "
                           "pair; hand_over = joins; a library form names its pinned library."),
})


@dataclass(frozen=True)
class LoadStop:
    id: str
    evidence: Mapping

    def __post_init__(self):
        want = STOPS[self.id][0]
        if set(self.evidence) != set(want):
            raise ValueError(f"{self.id}: evidence {sorted(self.evidence)} vs {sorted(want)}")

    @property
    def fix(self) -> str:
        """How to fix it, in plain words (impl note 3 C2)."""
        return STOPS[self.id][1]


class _Stop(Exception):
    def __init__(self, id_, **ev):
        super().__init__(id_)
        self.stop = LoadStop(id_, MappingProxyType(dict(ev)))


@dataclass(frozen=True)
class Registry:
    records: Mapping            # id → the record, deep-frozen
    unavailable: Mapping = field(default_factory=lambda: MappingProxyType({}))   # id → LoadStop: a library pin
                                                                                   # that does not match (note 1 §6)

    def declared(self) -> tuple:
        """Ids of records carrying a user-declared source anywhere (impl note 3 B2): counted on boards and gates."""
        return tuple(sorted(i for i, r in self.records.items() if _has_user_declared(r)))

    def get(self, material_id: str):
        """The record, or the LoadStop that made it unavailable (with its fix text), or None for an unknown id
        (68 N31: a body asking for an unavailable record gets why, not a missing key)."""
        if material_id in self.records:
            return self.records[material_id]
        return self.unavailable.get(material_id)

    def known(self, material_id: str) -> bool:
        return material_id in self.records

    def __getitem__(self, material_id: str):
        return self.records[material_id]


def _has_user_declared(x) -> bool:
    if isinstance(x, Mapping):
        return "user_declared" in x or any(_has_user_declared(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(_has_user_declared(v) for v in x)
    return False


# ── shape walk over the schema ──────────────────────────────────────────────────────────────────────────────────
def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and not math.isnan(x)


PLACEHOLDER = "FILL"         # what the scaffold writes where a value is owed (impl note 3 C1)


def _check(v, spec, path, file, cites: list):
    if isinstance(v, str) and v.startswith(PLACEHOLDER):
        raise _Stop("material.placeholder", file=file, path=path, text=v[:80])
    shape = spec["shape"]
    if shape == "number":
        if not _is_number(v):
            raise _Stop("material.bad_shape", file=file, path=path, expected="number", got=repr(v)[:60])
    elif shape == "text":
        if not isinstance(v, str) or not v.strip():
            raise _Stop("material.bad_shape", file=file, path=path, expected="text", got=repr(v)[:60])
    elif shape == "bool":
        if not isinstance(v, bool):
            raise _Stop("material.bad_shape", file=file, path=path, expected="bool", got=repr(v)[:60])
    elif shape == "enum":
        if v not in spec["values"]:
            raise _Stop("material.bad_shape", file=file, path=path, expected=f"one of {list(spec['values'])}",
                        got=repr(v)[:60])
    elif shape in ("record", "constant", "source"):
        _section(v, spec.get("of", shape), path, file, cites)
    elif shape == "list":
        if not isinstance(v, (list, tuple)) or len(v) < spec.get("min", 0):
            raise _Stop("material.bad_shape", file=file, path=path, expected=f"a list of ≥ {spec.get('min', 0)}",
                        got=repr(v)[:60])
        if "of" in spec:
            for i, x in enumerate(v):
                _section(x, spec["of"], f"{path}[{i}]", file, cites)
    elif shape == "mapping":
        if not isinstance(v, Mapping):
            raise _Stop("material.bad_shape", file=file, path=path, expected="mapping", got=repr(v)[:60])
        if "of" in spec:
            for k, x in v.items():
                _section(x, spec["of"], f"{path}.{k}", file, cites)
    else:
        raise AssertionError(f"schema shape {shape!r} at {path}")


def _section(v, name, path, file, cites: list):
    """Walk one schema section; cache cites are collected into `cites` as (path, sha256) for the manifest check."""
    spec = SCHEMA[name]
    if not isinstance(v, Mapping):
        raise _Stop("material.bad_shape", file=file, path=path, expected=f"a {name} mapping", got=repr(v)[:60])
    for k in v:
        if k not in spec:
            raise _Stop("material.unknown_key", file=file, path=path, key=str(k), allowed=sorted(spec))
    for k, s in spec.items():
        if s.get("required") and k not in v:
            raise _Stop("material.missing_key", file=file, path=path, key=k)
    for k, x in v.items():
        _check(x, spec[k], f"{path}.{k}", file, cites)
    if name == "source":
        _cite(v, path, file, cites)


# ── load rules beyond shape ─────────────────────────────────────────────────────────────────────────────────────
def _cite(src: Mapping, path, file, cites: list):
    """Note 1 item 3, form only: exactly one of cache / library / doi; a cache cite has page, where and sha256."""
    kinds = [k for k in ("cache", "library", "doi", "user_declared", "formula") if k in src]
    if len(kinds) != 1:
        raise _Stop("material.bad_cite", file=file, path=path,
                    why=f"exactly one of cache/library/doi/user_declared/formula, got {kinds}")
    k = kinds[0]
    if k == "cache":
        cites.append((path, src.get("sha256")))
        gone = [f for f in ("page", "where", "sha256") if f not in src]
        if gone:
            raise _Stop("material.bad_cite", file=file, path=path, why=f"a cache cite needs {gone}")
        if not _SHA.match(src["sha256"]):
            raise _Stop("material.bad_cite", file=file, path=path, why="sha256 is 64 lowercase hex")
        if "/" in src["cache"] or src["cache"].startswith("."):
            raise _Stop("material.bad_cite", file=file, path=path, why="cache is a file name in the paper cache")
    elif k == "library" and not _LIB.match(src["library"]):
        raise _Stop("material.bad_cite", file=file, path=path, why="library is name@version")
    elif k == "doi" and not _DOI.match(src["doi"]):
        raise _Stop("material.bad_cite", file=file, path=path, why="doi is doi:10.…")


def _edges(ph: Mapping, file):
    """D-M2: where the field passes a finite window edge, the edge declares a band or a refusal."""
    win, field, edges = ph["window"], ph["field"], ph["edges"]
    fbox = field.get("box")
    for name, key, side in _EDGES:
        w = win.get(key)
        if w is None or (side == "lower" and w <= 0.0) or (side == "upper" and math.isinf(w)):
            continue                                   # no finite edge on this side
        f = None if fbox is None else fbox.get(key)
        inside = f is not None and ((side == "lower" and f >= w) or (side == "upper" and f <= w))
        e = edges.get(name)
        if e is not None and ("refusal" in e) == ("band" in e):
            raise _Stop("material.edge_both" if "refusal" in e else "material.edge_undeclared",
                        file=file, phase=ph["id"], edge=name)
        if not inside and e is None:
            raise _Stop("material.edge_undeclared", file=file, phase=ph["id"], edge=name)


def _library_thermal(ph: Mapping, file):
    """68 on 6c7bb337: a library-form phase takes γ and dT/dP from the library, so it carries no thermal sets and no
    gamma_window (fields read by nothing would claim a decision lives there); every other phase needs gamma_window."""
    th = ph["thermal"]
    if ph["eos"]["form"] in ("library", "evaluator"):
        extra = [k for k in ("sets", "gamma_window", "phase_constants") if k in th]
        if extra:
            raise _Stop("material.kind_rule", file=file,
                        why=f"phase {ph['id']}: a library phase reads γ and dT/dP from the library; remove {extra}")
    elif "gamma_window" not in th:
        raise _Stop("material.missing_key", file=file, path=f"phase {ph['id']}.thermal", key="gamma_window")


def _gamma(ph: Mapping, file):
    if ph["eos"]["form"] in ("library", "evaluator"):
        return
    gw = ph["thermal"]["gamma_window"]
    for i, ts in enumerate(ph["thermal"].get("sets", ())):
        w = ts["window"]
        if w["p_min"] < gw["p_min"] or w["p_max"] > gw["p_max"]:
            raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                        why=f"set [{w['p_min']}, {w['p_max']}] Pa outside γ window [{gw['p_min']}, {gw['p_max']}]")
        sc = ts.get("printed_scope")
        if sc is not None and w["p_max"] > sc["p_max"]:            # 68 N9: a window is not widened by declaration
            raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                        why=f"set p_max {w['p_max']} Pa past its printed scope {sc['p_max']} Pa; use edge_above")
        if "edge_above" in ts:
            ea, pw = ts["edge_above"], ph["window"]["p_max"]
            if ea["limit"] > pw:                                     # 68 N11
                raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                            why=f"edge_above limit {ea['limit']} Pa past the phase window's p_max {pw} Pa")
            if ea["limit"] < pw and "refusal" not in ea:             # 68 N10: the Stop above the limit has an id
                raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                            why="edge_above below the phase window's p_max declares its refusal id")
        # past the γ window only through a declared edge band to a stated limit (G4): γ never falls back silently
        if "edge_above" in ts and not ts["edge_above"]["limit"] > w["p_max"]:
            raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                        why="edge_above's limit must lie above the set window's p_max")


def _gamma_tiling(ph: Mapping, file):
    """68 N19: inside the γ window, the sets ([p_min, p_max)) and the declared phase_constants span cover every P."""
    th = ph["thermal"]
    sets = th.get("sets", ())
    if not sets or ph["eos"]["form"] in ("library", "evaluator"):
        return                                    # a phase with no sets: its constants are the γ source throughout
    gw = th["gamma_window"]
    spans = sorted([(s["window"]["p_min"], s["window"]["p_max"]) for s in sets]
                   + ([(th["phase_constants"]["p_min"], th["phase_constants"]["p_max"])] if "phase_constants" in th else []))
    at = gw["p_min"]
    for lo, hi in spans:
        if lo > at:
            break
        at = max(at, hi)
    if at < gw["p_max"]:
        raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=-1,
                    why=f"γ window [{gw['p_min']}, {gw['p_max']}] Pa is not covered from {at} Pa: declare the span "
                        "in thermal.phase_constants or add a set")


def _bands(x, path, file):
    """Every band states exactly one of error / method (a method is evaluated by the checker, never hand-written)."""
    if isinstance(x, Mapping):
        if {"origin", "form", "grade"} <= set(x) and (("error" in x) == ("method" in x)):
            raise _Stop("material.bad_shape", file=file, path=path, expected="a band with exactly one of error / method",
                        got=repr(sorted(x))[:60])
        for k, v in x.items():
            _bands(v, f"{path}.{k}", file)
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            _bands(v, f"{path}[{i}]", file)


#: The params each registered evaluator reads (68 H1 on 6c735c86): a value the solver needs comes from the record, so a
#: record lacking one STOPs at load, not at view construction. The view reads its list from here.
EVALUATOR_PARAMS = MappingProxyType({
    "dorogokupets2017_liquid_fe": ("v0", "k0", "k0p", "theta0", "gamma0", "beta", "gamma_inf", "e0", "g_el", "t_ref",
                                   "molar_mass"),
    # French & Redmer 2015 (2015PhRvB..91a4308F) eqs (6), (9), (11), (12), (14), (15); coefficients in the fit's own
    # units (ρ in g/cm³, f in kJ/g), as printed (c8); the evaluator converts at its boundary. rho_search_min/max: the
    # inversion bracket (legacy 1.6 and 5.75 g/cm³), declared in the record.
    "french_redmer2015": ("a0", "a1", "a2", "a3", "a4", "a5", "b0", "b1", "b2", "b3", "b4", "t_d", "t_e", "a_d", "a_e",
                          "k0", "alpha_0_m4", "alpha_0_m3", "alpha_0_m2",
                          "gamma_0_m4", "gamma_0_m3", "gamma_0_m2", "gamma_1_m4", "gamma_1_m3", "gamma_1_m2",
                          "gamma_2_m4", "gamma_2_m3", "gamma_2_m2", "gamma_3_m4", "gamma_3_m3", "gamma_3_m2",
                          "rho_search_min", "rho_search_max"),
})


def _evaluators(ph: Mapping, file):
    eos_ev = ph["eos"].get("evaluator")
    if ph["eos"]["form"] == "evaluator" and eos_ev is None:
        raise _Stop("material.kind_rule", file=file, why=f"phase {ph['id']}: an evaluator form names its evaluator")
    for i, ts in enumerate(list(ph["thermal"].get("sets", ())) + ([{"evaluator": eos_ev}] if eos_ev else [])):
        ev = ts.get("evaluator")
        if ev is None:
            continue
        need = EVALUATOR_PARAMS.get(ev["name"])
        if need is None:
            raise _Stop("material.kind_rule", file=file,
                        why=f"phase {ph['id']} set {i}: evaluator {ev['name']!r} is not registered {sorted(EVALUATOR_PARAMS)}")
        gone = [k for k in need if k not in (ev.get("params") or {})]
        if gone:
            raise _Stop("material.kind_rule", file=file,
                        why=f"phase {ph['id']} set {i}: evaluator {ev['name']} needs params {gone}")


K_GATE = 2.0        # impl note 3 A3: fixed; a different k is a recorded change, never a per-record choice


def _sources_and_joins(ph: Mapping, file):
    """Impl note 3 A3, A4, A8 and note 4 items 1, 3, 4: the per-source σ form, the join shapes, and precedence."""
    srcs = {x["id"]: x for x in ph.get("sources", ())}
    if len(srcs) != len(ph.get("sources", ())):
        raise _Stop("material.join_rule", file=file, phase=ph["id"], join=-1, why="source ids repeat")
    for sid, x in srcs.items():
        sg = x["sigma"]
        need = {"propagated": ("from", "correlation"), "constant": ("value", "reduction"),
                "not_printed": ("where",)}[sg["kind"]]
        gone = [f for f in need if f not in sg]
        if gone:
            raise _Stop("material.sigma_rule", file=file, phase=ph["id"], source=sid,
                        why=f"sigma kind {sg['kind']} needs {gone}")
        if sg["kind"] == "not_printed" and "value" in sg:
            raise _Stop("material.sigma_rule", file=file, phase=ph["id"], source=sid,
                        why="an unprinted σ takes no stand-in value")
        if sg.get("correlation") == "printed" and "matrix" not in sg:
            raise _Stop("material.sigma_rule", file=file, phase=ph["id"], source=sid,
                        why="a printed correlation gives its matrix")
    joins = ph.get("joins_within", ())
    for i, j in enumerate(joins):
        bad = [b for b in j["between"] if b not in srcs]
        if len(j["between"]) != 2 or bad:
            raise _Stop("material.join_rule", file=file, phase=ph["id"], join=i,
                        why=f"between names two of the phase's sources {sorted(srcs)}; unknown {bad}")
        kind = j["kind"]
        need = {"blend": ("overlap", "weight"), "cross_check": ("overlap",), "taper": ("edge_p", "side", "weight"),
                "seam": ()}[kind]
        gone = [f for f in need if f not in j]
        if gone:
            raise _Stop("material.join_rule", file=file, phase=ph["id"], join=i, why=f"{kind} needs {gone}")
        if "k" in j and j["k"] != K_GATE:
            raise _Stop("material.join_rule", file=file, phase=ph["id"], join=i,
                        why=f"k is {K_GATE:g} (impl note 3 A3); a different k is a recorded change")
        if kind == "taper" and "width" in j:
            w, pe = j["width"]["p_end"], j["edge_p"]
            if (j["side"] == "upper" and w <= pe) or (j["side"] == "lower" and w >= pe):
                raise _Stop("material.join_rule", file=file, phase=ph["id"], join=i,
                            why=f"a {j['side']} taper ends on the far side of P_e")
    if joins:
        pr = ph.get("precedence")
        if pr is None:
            raise _Stop("material.precedence", file=file, phase=ph["id"], why="a phase with joins declares precedence")
        if pr["by"] == "declared" and "declared_before_comparison" not in pr:
            raise _Stop("material.precedence", file=file, phase=ph["id"], why="a declared precedence carries its date")
        if pr["by"] == "frozen" and "ref" not in pr:
            raise _Stop("material.precedence", file=file, phase=ph["id"], why="a frozen precedence names its ref")
        for i, j in enumerate(joins):
            a, b = (srcs[x]["basis"] for x in j["between"])
            if pr["by"] == "basis" and a == b:
                raise _Stop("material.precedence", file=file, phase=ph["id"],
                            why=f"join {i}: both sources are {a}; basis cannot decide, so declare or freeze it")
            if a == "computed" and b == "measured":
                raise _Stop("material.precedence", file=file, phase=ph["id"],
                            why=f"join {i}: measured beats computed (note 3 A6.1); the preferred source is listed first")


def _reference_and_sets(ph: Mapping, file):
    """68 on 738358de N3 and b0169870 N5: the reference adiabat's nodes are paired and strictly increasing in ln P; a
    thermal set with an adiabat kind or a T² term names its own t_ref (legacy's trap: without it ΔT runs from 0 K)."""
    ad = ph["eos"]["reference"].get("adiabat")
    if ad is not None:
        if len(ad["lnp"]) != len(ad["t"]) or len(ad["lnp"]) < 2 or not _increasing(ad["lnp"]) \
                or not all(_is_number(x) and x > 0.0 for x in ad["t"]):
            raise _Stop("material.kind_rule", file=file,
                        why=f"phase {ph['id']}: reference adiabat needs paired lnp/t nodes, lnp strictly increasing, T > 0")
    for i, ts in enumerate(ph["thermal"].get("sets", ())):
        k_dt = (ts.get("constants") or {}).get("alpha_k_dt")
        needs = ts.get("t_ref_kind") == "adiabat" or (k_dt is not None and k_dt["value"] != 0.0)
        if needs and "t_ref" not in ts:
            raise _Stop("material.kind_rule", file=file,
                        why=f"phase {ph['id']} set {i}: an adiabat kind or a T² term needs the set's own t_ref")


def _disclosures(rec: Mapping, file):
    """A disclosed fail cites a cached source (page) that prints the disagreement; no other source kind will do."""
    for i, fc in enumerate(rec["formula_checks"]):
        d = fc.get("disclosed_fail")
        if d is not None and "cache" not in d["source"]:
            raise _Stop("material.bad_cite", file=file, path=f"record.formula_checks[{i}].disclosed_fail.source",
                        why="a disclosed fail cites the cached source that prints the disagreement")


def _curves(rec: Mapping, file):
    """68 N32: a clapeyron boundary declares its printed T range (t_min, t_max), as a table's nodes do."""
    for i, b in enumerate(rec.get("boundaries", ())):
        c = b["curve"]
        if c["form"] in ("clapeyron", "ln_sum") and not ("t_min" in c and "t_max" in c):
            raise _Stop("material.kind_rule", file=file,
                        why=f"boundary {i}: a {c['form']} curve declares t_min and t_max")
        if c["form"] == "ln_sum" and not ("p_star" in c and "t_star" in c and c.get("terms")):
            raise _Stop("material.kind_rule", file=file, why=f"boundary {i}: an ln_sum curve needs p_star, t_star, terms")


def _increasing(xs) -> bool:
    return all(_is_number(x) for x in xs) and all(b > a for a, b in zip(xs, xs[1:]))


def _table(ph: Mapping, file):
    """Impl note 3 B1–B3 and note 4 item 5: the direct table's shape and physical checks."""
    if ph["eos"]["form"] != "table":
        return
    if "table" not in ph["eos"]:
        raise _Stop("material.kind_rule", file=file, why=f"phase {ph['id']}: a table form carries its table")
    tb = ph["eos"]["table"]
    pid = ph["id"]

    def no(why):
        raise _Stop("material.table_check", file=file, phase=pid, why=why)

    first, ts, cols = tb["first"], tb["t"], tb["columns"]
    if not _increasing(first) or not _increasing(ts):
        no("the axis nodes are numbers in increasing order")
    for name, rows in cols.items():
        if len(rows) != len(first) or any(len(r) != len(ts) for r in rows):
            no(f"column {name} is {len(first)} rows × {len(ts)} values")
        for i, r in enumerate(rows):
            for k, v in enumerate(r):
                if not _is_number(v) or math.isinf(v):
                    no(f"column {name} has a hole or NaN at node ({first[i]}, {ts[k]})")
    if tb["interpolation"] == "bilinear_lnp_t" and not ({"alpha", "k_t"} <= set(cols) or {"c_p", "k_t"} <= set(cols)):
        no("bilinear interpolation needs α and K_T columns (or c_P and K_T), or a C¹ interpolant (note 4 item 5)")
    dens = "rho" if tb["axes"] == "P_T" else None
    if dens is not None and dens not in cols:
        no("a (P, T) table carries a rho column")
    for k, t in enumerate(ts):
        seq = [cols["rho"][i][k] for i in range(len(first))] if dens else [cols["P"][i][k] for i in range(len(first))] \
            if "P" in cols else None
        if seq is None:
            no("a (ρ, T) table carries a P column")
        for i in range(1, len(seq)):
            if not seq[i] > seq[i - 1]:
                no(f"ρ does not rise with P on the {t} K isotherm between nodes {first[i - 1]} and {first[i]}")
    for name, test, why in (("k_t", lambda v: v > 0.0, "K_T > 0"), ("c_p", lambda v: v > 0.0, "c_P > 0")):
        for i, r in enumerate(cols.get(name, ())):
            for k, v in enumerate(r):
                if not test(v):
                    no(f"{why} fails at node ({first[i]}, {ts[k]}): {v}")
    if "alpha" in cols:
        rng = tb.get("alpha_range")
        if not rng or len(rng) != 2:
            no("an α column needs its declared alpha_range [lo, hi]")
        for i, r in enumerate(cols["alpha"]):
            for k, v in enumerate(r):
                if not rng[0] <= v <= rng[1]:
                    no(f"α {v} outside its declared range {list(rng)} at node ({first[i]}, {ts[k]})")


def _field_record(rec: Mapping, ids: list, pairs: list, file):
    """Impl note 6 item 4: every phase has a gibbs or sourced field; the gibbs phases are library-form phases of one
    pin (one source); each boundary names two of the record's phases and is a declared curve (clapeyron / table),
    never a library-derived line, since G is never compared across sources."""
    gibbs_pins = set()
    for ph in rec["phases"]:
        k = ph["field"]["kind"]
        if k not in ("gibbs", "sourced"):
            raise _Stop("material.kind_rule", file=file, why=f"phase {ph['id']}: a field record's fields are gibbs or sourced")
        if k == "gibbs":
            lib = ph["eos"].get("library")
            if ph["eos"]["form"] != "library" or lib is None:
                raise _Stop("material.kind_rule", file=file, why=f"phase {ph['id']}: a gibbs field needs a library phase")
            gibbs_pins.add((lib["name"], lib["version"], lib["sha256"]))
    if len(gibbs_pins) > 1:
        raise _Stop("material.kind_rule", file=file, why="gibbs phases come from more than one library pin (one source)")
    for a, b in pairs:
        if a not in ids or b not in ids:
            raise _Stop("material.kind_rule", file=file, why=f"boundary {a}–{b} names a phase the record lacks")
    for bnd in rec.get("boundaries", ()):
        if bnd["curve"]["form"] not in ("clapeyron", "table", "ln_sum"):
            raise _Stop("material.kind_rule", file=file,
                        why=f"boundary {tuple(bnd['between'])}: a field record's boundary is a declared curve")


def _kind(rec: Mapping, file):
    ids = [p["id"] for p in rec["phases"]]
    if len(set(ids)) != len(ids):
        raise _Stop("material.kind_rule", file=file, why=f"phase ids repeat: {ids}")
    kind = rec["kind"]
    if kind == "single" and len(ids) != 1:
        raise _Stop("material.kind_rule", file=file, why="a single record has one phase")
    if kind == "branched":
        choice = rec.get("choice")
        if choice is None:                                    # impl note 6 item 1
            raise _Stop("material.kind_rule", file=file, why="a branched record declares choice: chain | field")
        pairs = [tuple(b["between"]) for b in rec.get("boundaries", ())]
        if choice == "chain":
            want = list(zip(ids, ids[1:]))
            if sorted(pairs) != sorted(want):
                raise _Stop("material.kind_rule", file=file, why=f"boundaries {pairs} vs adjacent pairs {want}")
        else:
            _field_record(rec, ids, pairs, file)
    if kind == "hand_over" and not rec.get("joins"):
        raise _Stop("material.kind_rule", file=file, why="a hand-over record declares its joins")
    for ph in rec["phases"]:
        if ph["eos"]["form"] == "library" and "library" not in ph["eos"]:
            raise _Stop("material.kind_rule", file=file, why=f"phase {ph['id']}: a library form names its pin")


def _is_sha(x) -> bool:
    return isinstance(x, str) and _SHA.match(x) is not None


def read_manifest(path: Path = MANIFEST) -> frozenset | LoadStop:
    """The registered sha256 set. An absent manifest registers nothing; a malformed one STOPs."""
    if not Path(path).exists():
        return frozenset()
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as e:
        return LoadStop("material.unreadable", MappingProxyType({"file": Path(path).name, "detail": str(e)[:200]}))
    return manifest_shas(text, Path(path).name)


def manifest_shas(text: str, name: str = "sources.yaml") -> frozenset | LoadStop:
    """The registered sha256 set from manifest text (also used to check a new manifest before it is written)."""
    try:
        doc = parse(text)
    except LoadError as e:
        return LoadStop("material.unreadable", MappingProxyType({"file": name, "detail": str(e)[:200]}))
    path = Path(name)
    rows = (doc or {}).get("sources", []) if isinstance(doc, Mapping) else None
    if not isinstance(rows, list) or not all(isinstance(r, Mapping) and _is_sha(r.get("sha256")) for r in rows):
        return LoadStop("material.unreadable", MappingProxyType(
            {"file": Path(path).name, "detail": "sources is a list of rows, each with a 64-hex sha256"}))
    return frozenset(r["sha256"] for r in rows)


def check_record(raw, file: str, registered: frozenset = frozenset()) -> Mapping | LoadStop:
    """One record's load rules; the record (deep-frozen) or the first STOP."""
    cites: list = []
    try:
        _section(raw, "record", "record", file, cites)
        for path, sha in cites:
            if sha not in registered:
                raise _Stop("material.unregistered_source", file=file, path=path, sha256=str(sha))
        if raw["id"] != Path(file).stem:
            raise _Stop("material.id_mismatch", file=file, id=raw["id"])
        _kind(raw, file)
        _curves(raw, file)
        _disclosures(raw, file)
        _bands(raw, "record", file)
        for ph in raw["phases"]:
            _edges(ph, file)
            _library_thermal(ph, file)
            _gamma(ph, file)
            _gamma_tiling(ph, file)
            _sources_and_joins(ph, file)
            _reference_and_sets(ph, file)
            _evaluators(ph, file)
            _table(ph, file)
    except _Stop as s:
        return s.stop
    return freeze(raw)


def load(directory: Path = MATERIALS_DIR, manifest: Path | None = None) -> Registry | LoadStop:
    """Every record in `directory` (schema and manifest excepted), checked; the registry or the first STOP."""
    registered = read_manifest(Path(directory) / "sources.yaml" if manifest is None else manifest)
    if isinstance(registered, LoadStop):
        return registered
    out, unavailable, shas = {}, {}, {}             # shas: a library's tree sha, computed once per load (68 N30)
    for f in sorted(Path(directory).glob("*.yaml")):
        if f.name in NOT_RECORDS:
            continue
        try:
            raw = parse(f.read_text(encoding="utf-8"))
        except (LoadError, OSError) as e:
            return LoadStop("material.unreadable", MappingProxyType({"file": f.name, "detail": str(e)[:200]}))
        rec = check_record(raw, f.name, registered)
        if isinstance(rec, LoadStop):
            return rec
        if rec["id"] in out or rec["id"] in unavailable:
            return LoadStop("material.duplicate_id", MappingProxyType({"file": f.name, "id": rec["id"]}))
        pin = _library_pin(rec, f.name, shas)
        if pin is not None:                         # that record only: the others still load (impl note 1 §6)
            unavailable[rec["id"]] = pin
            continue
        miss = triple_point_misses(rec, f.name)
        if miss is not None:
            return miss
        out[rec["id"]] = rec
    return Registry(MappingProxyType(out), MappingProxyType(unavailable))


def triple_point_misses(rec: Mapping, file: str) -> LoadStop | None:
    """Impl note 6 item 4 (68 (2)): at each declared mixed triple point, every declared curve between two of its phases
    passes within dp of the printed P at the printed T (the check is at that T, so dt is recorded but the printed T is
    taken as exact; 68 N36), and so does the min-G boundary between two of its gibbs
    phases (located by bisection in P over their G difference within ±2·dp: a crossing farther away is a miss anyway,
    and the narrow bracket keeps the library inside its own range)."""
    tps = rec.get("triple_points") or ()
    if not tps:
        return None
    from solver import material_view as mv
    view = mv.RecordView(rec, 0.0)
    kinds = {ph["id"]: ph["field"]["kind"] for ph in rec["phases"]}
    by_id = {ph.id: ph for ph in view.phases}
    for tp in tps:
        names = list(tp["phases"])
        p0, t0 = float(tp["p"]["value"]), float(tp["t"]["value"])
        dp = float(tp["tolerance"]["dp"])

        def stop(why):
            return LoadStop("material.triple_point_miss", MappingProxyType({"file": file, "phases": names, "why": why}))
        if "unchecked" in tp:                         # listed, not checked: only inside a declared refusal region (c8)
            if view.refusal_region_at(p0, t0) is None:
                return stop("marked unchecked but no declared refusal region holds the point")
            continue
        for b in rec.get("boundaries", ()):
            if set(b["between"]) <= set(names):
                pb = view.boundary_pressure(b["curve"], t0)
                if pb is None or abs(pb - p0) > dp:
                    return stop(f"curve {tuple(b['between'])} at {t0:g} K is {pb!r} Pa, not within {dp:g} of {p0:g}")
        gib = [n for n in names if kinds.get(n) == "gibbs"]
        for i in range(len(gib)):
            for j in range(i + 1, len(gib)):
                a, b = by_id[gib[i]].library, by_id[gib[j]].library

                def dg(p):
                    return a.at(p, t0)["g"] - b.at(p, t0)["g"]
                lo, hi = p0 - 2 * dp, p0 + 2 * dp
                try:
                    flo, fhi = dg(lo), dg(hi)
                    if flo * fhi > 0.0:
                        return stop(f"min-G boundary {gib[i]}–{gib[j]} not found within ±{2 * dp:g} Pa of {p0:g}")
                    for _ in range(60):
                        mid = 0.5 * (lo + hi)
                        fm = dg(mid)
                        if (fm > 0.0) == (flo > 0.0):
                            lo, flo = mid, fm
                        else:
                            hi = mid
                except ImportError:                          # 68 N36: an import failure is not a miss
                    raise
                except Exception as e:                       # a library failure at the point is a miss, by name
                    return stop(f"min-G boundary {gib[i]}–{gib[j]} could not be evaluated: {e}")
                if abs(0.5 * (lo + hi) - p0) > dp:
                    return stop(f"min-G boundary {gib[i]}–{gib[j]} at {t0:g} K is {0.5 * (lo + hi):g} Pa, "
                                f"not within {dp:g} of {p0:g}")
    return None


def _library_pin(rec: Mapping, file: str, shas: dict) -> LoadStop | None:
    from solver import material_library as ml
    for ph in rec["phases"]:
        lib = ph["eos"].get("library")
        if ph["eos"]["form"] == "library" and lib is not None:
            if lib["name"] not in shas:
                shas[lib["name"]] = ml.tree_sha256(lib["name"]) if lib["name"] in ml.PACKAGES else None
            got = ml.check_pin(lib, shas[lib["name"]])
            if got is not None:
                return LoadStop("material.library_pin", MappingProxyType({"file": file, "why": got.why}))
    return None
