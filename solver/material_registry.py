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
from dataclasses import dataclass
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

    def declared(self) -> tuple:
        """Ids of records carrying a user-declared source anywhere (impl note 3 B2): counted on boards and gates."""
        return tuple(sorted(i for i, r in self.records.items() if _has_user_declared(r)))

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


def _gamma(ph: Mapping, file):
    gw = ph["thermal"]["gamma_window"]
    for i, ts in enumerate(ph["thermal"].get("sets", ())):
        w = ts["window"]
        if w["p_min"] < gw["p_min"] or w["p_max"] > gw["p_max"]:
            raise _Stop("material.gamma_window", file=file, phase=ph["id"], set=i,
                        why=f"set [{w['p_min']}, {w['p_max']}] Pa outside γ window [{gw['p_min']}, {gw['p_max']}]")


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


def _kind(rec: Mapping, file):
    ids = [p["id"] for p in rec["phases"]]
    if len(set(ids)) != len(ids):
        raise _Stop("material.kind_rule", file=file, why=f"phase ids repeat: {ids}")
    kind = rec["kind"]
    if kind == "single" and len(ids) != 1:
        raise _Stop("material.kind_rule", file=file, why="a single record has one phase")
    if kind == "branched":
        pairs = [tuple(b["between"]) for b in rec.get("boundaries", ())]
        want = list(zip(ids, ids[1:]))
        if sorted(pairs) != sorted(want):
            raise _Stop("material.kind_rule", file=file, why=f"boundaries {pairs} vs adjacent pairs {want}")
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
        doc = parse(Path(path).read_text(encoding="utf-8"))
    except (LoadError, OSError) as e:
        return LoadStop("material.unreadable", MappingProxyType({"file": Path(path).name, "detail": str(e)[:200]}))
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
        for ph in raw["phases"]:
            _edges(ph, file)
            _gamma(ph, file)
            _sources_and_joins(ph, file)
            _table(ph, file)
    except _Stop as s:
        return s.stop
    return freeze(raw)


def load(directory: Path = MATERIALS_DIR, manifest: Path | None = None) -> Registry | LoadStop:
    """Every record in `directory` (schema and manifest excepted), checked; the registry or the first STOP."""
    registered = read_manifest(Path(directory) / "sources.yaml" if manifest is None else manifest)
    if isinstance(registered, LoadStop):
        return registered
    out = {}
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
        if rec["id"] in out:
            return LoadStop("material.duplicate_id", MappingProxyType({"file": f.name, "id": rec["id"]}))
        out[rec["id"]] = rec
    return Registry(MappingProxyType(out))
