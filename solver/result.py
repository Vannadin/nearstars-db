# 결과 묶음 — 값 하나(Quantity: 점·띠·출처)와 결과 셋(Answer · Refusal · NoAnswer)의 꼴 (phase1-design D-A3-1..5).
"""Result types of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A3-1..5, post-freeze note 1).

Every type is a frozen dataclass. Sequence fields are coerced to tuples and mapping fields deep-frozen at
construction, so a value cannot change after it is built (§A6). Numeric fields are coerced to float (`-0.0` to
`0.0`), so equal values give equal canonical bytes. Construction checks raise `ValueError`: a bad value here comes
from code, not from input (input is refused by `validate`), so it is a bug and never a refusal.

Types holding mappings are not hashable (`MappingProxyType`); do not put them in sets or use them as dict keys.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, fields, is_dataclass
from types import MappingProxyType
from typing import Any, Mapping

#: Result grades, best first (engine/payload.py:31 `GRADES` at 097a8aa3; R-GV-1). The order is the ranking
#: used for a derived result-level grade (D-A3-3).
GRADES = ("measured", "calibrated", "analog", "judgment", "authored")
#: Every grade word (engine/payload.py:34–35 `GRADE_WORDS` at 097a8aa3).
GRADE_WORDS = ("measured", "literature", "analog", "derived", "judgment", "declared", "inherited", "authored",
               "calibrated")
#: Input grade words: GRADE_WORDS minus «calibrated» (engine/payload.py:36; R-GV-1).
INPUT_GRADES = tuple(g for g in GRADE_WORDS if g != "calibrated")

KINDS = ("exact", "lower", "upper", "interval")                 # D-A3-1, R-C154-1..3
METHODS = ("direct", "interpolated", "bridged", "derived")      # D-A3-1; «bridged» = not directly solved (R-OWN-6)
WHERE_KINDS = ("layer", "boundary", "body")
SIDES = ("lower", "upper", "equal_by_convention")               # R-C153-1/2
LABEL_KINDS = ("known_wrong", "oracle_bias", "expected_verdict_change", "board_choice")   # D-A3-4
LABEL_SCOPES = ("validation sample", "shipped")
SPAN_KINDS = ("refusal", "no_answer", "bridged", "break")       # D-A3-5
NO_ANSWER_REASONS = ("unconverged", "span_too_long")            # D-A3-2, §X3
#: Post-freeze note 1 (owner Q4 ②): a direct solve outside a table carries the numerical band only where a sample
#: check or an on-demand re-solve measured it. Otherwise `Sources.solver_not_measured` is True (a typed flag; readers
#: branch on the flag, never on this text, X3) and `solver_reason` is this registry string.
BAND_NOT_MEASURED = "numerical band not measured"


def freeze(x):
    """Deep-freeze: dicts → read-only mappings, lists/tuples → tuples, sets → sorted tuples."""
    if isinstance(x, Mapping):
        return MappingProxyType({k: freeze(v) for k, v in x.items()})
    if isinstance(x, (list, tuple)):
        return tuple(freeze(v) for v in x)
    if isinstance(x, (set, frozenset)):
        return tuple(sorted((freeze(v) for v in x), key=repr))
    return x


def check_finite(name: str, x) -> float:
    """A number that crosses a type boundary is finite (W-L10-01); returns it as a float. Module-level so a negative
    control can disable it."""
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise ValueError(f"{name} must be a finite number, got {x!r}")
    try:
        f = float(x)
    except OverflowError:
        raise ValueError(f"{name} must be a finite number, got an int of {len(str(x))} digits") from None
    if not math.isfinite(f):
        raise ValueError(f"{name} must be a finite number, got {x!r}")
    return 0.0 if f == 0.0 else f


def check_in(name: str, x: Any, allowed: tuple) -> None:
    if x not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {x!r}")


def _num(obj, *names):
    for n in names:
        object.__setattr__(obj, n, check_finite(f"{type(obj).__name__}.{n}", getattr(obj, n)))


@dataclass(frozen=True)
class SourceBand:
    """One side-source of a band: the offsets it alone produces (R-STEP0-11 `{lo, hi, contrib}`)."""
    lo: float
    hi: float
    contrib: str

    def __post_init__(self):
        _num(self, "lo", "hi")
        if self.lo > self.hi:
            raise ValueError(f"SourceBand lo {self.lo!r} > hi {self.hi!r}")
        if not self.contrib:
            raise ValueError("SourceBand.contrib must name what the source is")


@dataclass(frozen=True)
class Sources:
    """The three sources of a band (R-STEP0-11). Each is a `SourceBand` or None with a reason.

    §A1.7 maps here: the numerical band is `solver`, the declared-input band is `input`; `model` stays null with a
    reason until phase 2's material bands. `solver_not_measured` is Q4 ②'s typed flag: True exactly when the
    numerical band was not measured, and then `solver_reason` is `BAND_NOT_MEASURED`.
    """
    input: SourceBand | None
    model: SourceBand | None
    solver: SourceBand | None
    input_reason: str | None = None
    model_reason: str | None = None
    solver_reason: str | None = None
    solver_not_measured: bool = False

    def __post_init__(self):
        if self.solver_not_measured:
            if self.solver is not None:
                raise ValueError("Sources.solver_not_measured with a solver band")
            object.__setattr__(self, "solver_reason", BAND_NOT_MEASURED)
        elif self.solver is None and self.solver_reason == BAND_NOT_MEASURED:  # x3-ok: refuses the flag's text as a free reason
            raise ValueError("«numerical band not measured» is the flag solver_not_measured, not a free reason")
        for name in ("input", "model", "solver"):
            if getattr(self, name) is None and not getattr(self, name + "_reason"):
                raise ValueError(f"Sources.{name} is null without a reason")


@dataclass(frozen=True)
class Band:
    """An envelope «the range we cannot rule out» (R-STEP0-11): never a probability, never called σ. At least one
    source computes it (D-A3-1: no band without a computing method)."""
    lo: float
    hi: float
    method: str
    sources: Sources
    basis: str = "envelope"

    def __post_init__(self):
        _num(self, "lo", "hi")
        if self.lo > self.hi:
            raise ValueError(f"Band lo {self.lo!r} > hi {self.hi!r}")
        if self.basis != "envelope":
            raise ValueError(f"Band.basis must be 'envelope', got {self.basis!r}")
        if not self.method:
            raise ValueError("Band.method must name how the band was computed")
        if self.sources.input is None and self.sources.model is None and self.sources.solver is None:
            raise ValueError("a Band whose three sources are all null has no computing source")


@dataclass(frozen=True)
class Where:
    """Where a quantity or refusal sits: a layer, a boundary with its side (C153), or the whole body."""
    kind: str
    id: str | None = None
    side: str | None = None

    def __post_init__(self):
        check_in("Where.kind", self.kind, WHERE_KINDS)
        if self.kind == "body":
            if self.id is not None or self.side is not None:
                raise ValueError("Where(body) takes no id and no side")
            return
        if not self.id:
            raise ValueError(f"Where({self.kind}) needs an id")
        if self.kind == "boundary":
            check_in("Where.side", self.side, SIDES)
        elif self.side is not None:
            raise ValueError("only a boundary has a side")


@dataclass(frozen=True)
class MaterialRef:
    id: str
    source: str
    window: Mapping = field(default_factory=dict)     # the source's declared validity window (R-RUL-10a)

    def __post_init__(self):
        object.__setattr__(self, "window", freeze(self.window))


@dataclass(frozen=True)
class SolverInfo:
    """Solver provenance. `solve_id` is §A6's one definition (sha256 of canonical Body, material bytes, options,
    solver version string; no clock); it is computed by the solve context, never here."""
    solve_id: str
    fallbacks: tuple = ()          # class F sites (R-C138-2)
    substitutions: tuple = ()
    counters: tuple = ()           # ((name, int), …), from the solve trace (§A6)

    def __post_init__(self):
        for n in ("fallbacks", "substitutions", "counters"):
            object.__setattr__(self, n, freeze(tuple(getattr(self, n))))


@dataclass(frozen=True)
class Provenance:
    """Per-quantity provenance (D-A3-3, W-L12-02)."""
    grade: str
    solver: SolverInfo
    inputs_read: tuple = ()             # ((field, input grade), …)
    consumed_observations: tuple = ()   # declared observations a closure consumed, e.g. ("R", "core+layer radius 1845 km")
    materials: tuple = ()               # (MaterialRef, …)
    extrapolation: tuple = ()           # ((material id, window text, band text or counter), …) (R-RUL-10/10a)

    def __post_init__(self):
        check_in("Provenance.grade", self.grade, GRADES)
        for n in ("inputs_read", "consumed_observations", "materials", "extrapolation"):
            object.__setattr__(self, n, freeze(tuple(getattr(self, n))))
        for f, g in self.inputs_read:
            if g is not None:
                check_in(f"Provenance.inputs_read[{f}] grade", g, INPUT_GRADES)
        for m in self.materials:
            if not isinstance(m, MaterialRef):
                raise ValueError(f"Provenance.materials holds {m!r}, not a MaterialRef")


@dataclass(frozen=True)
class Label:
    """An oracle label, added by the label pass outside the solver (D-A3-4). Key: (body, node, key, state); body and
    node are the carrier's. `state` is «declared», a T_pot (float) or a point id (str)."""
    kind: str
    scope: str
    rid: str
    reason: str
    state: str | float = "declared"

    def __post_init__(self):
        check_in("Label.kind", self.kind, LABEL_KINDS)
        check_in("Label.scope", self.scope, LABEL_SCOPES)
        if not isinstance(self.state, str):
            object.__setattr__(self, "state", check_finite("Label.state", self.state))


def check_direct_band(q: "Quantity") -> None:
    """Note 1 (Q4 ②): a direct solve's band either carries a measured solver source or says it was not measured."""
    if q.method == "direct" and q.band is not None and q.band.sources.solver is None \
            and not q.band.sources.solver_not_measured:
        raise ValueError(f"Quantity({q.key}): a direct solve's band without a solver source must set "
                         "solver_not_measured (Q4 ②)")


@dataclass(frozen=True)
class Quantity:
    """Every emitted number (D-A3-1). The point is the directly solved value; a curve never overwrites it (R-RUL-21)."""
    key: str
    unit: str
    point: float
    kind: str
    method: str
    where: Where
    provenance: Provenance
    band: Band | None = None
    band_reason: str | None = None
    sensitivity: float | None = None    # dT_c/dT_pot-type factor (§A1.7); not a band source
    labels: tuple = ()

    def __post_init__(self):
        if not self.key:
            raise ValueError("Quantity.key is empty")
        object.__setattr__(self, "point", check_finite(f"Quantity({self.key}).point", self.point))
        check_in(f"Quantity({self.key}).kind", self.kind, KINDS)
        check_in(f"Quantity({self.key}).method", self.method, METHODS)
        if not isinstance(self.where, Where):
            raise ValueError(f"Quantity({self.key}).where is not a Where")
        if self.band is None:
            if not self.band_reason:
                raise ValueError(f"Quantity({self.key}) has no band and no band_reason")
        elif not self.band.lo <= self.point <= self.band.hi:
            raise ValueError(f"Quantity({self.key}) point {self.point!r} outside its band "
                             f"[{self.band.lo!r}, {self.band.hi!r}]")
        check_direct_band(self)
        if self.sensitivity is not None:
            object.__setattr__(self, "sensitivity", check_finite(f"Quantity({self.key}).sensitivity", self.sensitivity))
        object.__setattr__(self, "labels", tuple(self.labels))
        for lab in self.labels:
            if not isinstance(lab, Label):
                raise ValueError(f"Quantity({self.key}) label {lab!r} is not a Label")


@dataclass(frozen=True)
class Note:
    """A typed note, rendered at the boundary (D-A3-2). `kind` names the class; `fields` carry the facts."""
    kind: str
    text: str
    fields: Mapping = field(default_factory=dict)

    def __post_init__(self):
        if not self.kind:
            raise ValueError("Note.kind is empty")
        object.__setattr__(self, "fields", freeze(self.fields))


@dataclass(frozen=True)
class Refusal:
    """A named refusal (D-A3-2). Build it with `refusals.make`, which checks the id and its evidence fields. `where`
    is a locator text (file:key, «solve»); `at` places it typed when it sits on a layer or boundary."""
    id: str
    where: str
    evidence: Mapping
    text: str
    at: Where | None = None

    def __post_init__(self):
        object.__setattr__(self, "evidence", freeze(self.evidence))


@dataclass(frozen=True)
class NoAnswer:
    """No value was reached (D-A3-2). Unconverged values are not values (R-RUL-22). Build it with `refusals.no_answer`."""
    reason: str
    where: str
    evidence: Mapping
    text: str
    at: Where | None = None

    def __post_init__(self):
        check_in("NoAnswer.reason", self.reason, NO_ANSWER_REASONS)
        object.__setattr__(self, "evidence", freeze(self.evidence))


@dataclass(frozen=True)
class LocatedBoundary:
    """A boundary the solve located (§A1.3): its name, kind, and state there."""
    name: str
    kind: str
    m: float
    r: float
    p: float
    t: float

    def __post_init__(self):
        _num(self, "m", "r", "p", "t")


@dataclass(frozen=True)
class Answer:
    """An answer (D-A3-2): quantities by where, located boundaries, profiles, and what could not be made."""
    quantities: tuple
    boundaries: tuple = ()
    profiles: Mapping = field(default_factory=dict)   # layer id → {column name → tuple of floats}
    missing: tuple = ()                               # ((key, Refusal | NoAnswer), …)
    notes: tuple = ()

    def __post_init__(self):
        for n in ("quantities", "boundaries", "missing", "notes"):
            object.__setattr__(self, n, tuple(getattr(self, n)))
        prof = {}
        for lid, cols in dict(self.profiles).items():
            prof[lid] = MappingProxyType({c: tuple(check_finite(f"profile {lid}.{c}", v) for v in vals)
                                          for c, vals in dict(cols).items()})
        object.__setattr__(self, "profiles", MappingProxyType(prof))
        seen = set()
        for q in self.quantities:
            if not isinstance(q, Quantity):
                raise ValueError(f"Answer holds a non-Quantity {q!r}")
            ident = (q.key, q.where)
            if ident in seen:
                raise ValueError(f"Answer holds {q.key} at {q.where} twice")
            seen.add(ident)
        for b in self.boundaries:
            if not isinstance(b, LocatedBoundary):
                raise ValueError(f"Answer.boundaries holds {b!r}, not a LocatedBoundary")
        for key, why in self.missing:
            if not isinstance(why, (Refusal, NoAnswer)):
                raise ValueError(f"missing {key} must carry a Refusal or NoAnswer, got {why!r}")
        for n in self.notes:
            if not isinstance(n, Note):
                raise ValueError(f"Answer.notes holds {n!r}, not a Note")

    @property
    def grade(self) -> str:
        """The result-level grade: the worst over its quantities, never set by hand (D-A3-3)."""
        if not self.quantities:
            raise ValueError("an Answer with no quantities has no grade")
        return GRADES[max(GRADES.index(q.provenance.grade) for q in self.quantities)]


# The outcome tag a verdict reader reads without inspecting content (R-RUL-1).
def outcome_kind(o: Answer | Refusal | NoAnswer) -> str:
    if isinstance(o, Answer):
        return "answer"
    if isinstance(o, Refusal):
        return "refusal"
    if isinstance(o, NoAnswer):
        return "no_answer"
    raise TypeError(f"not an outcome: {o!r}")


@dataclass(frozen=True)
class Span:
    """A typed table span (D-A3-5), replacing the positional list of R-C162-2."""
    t_lo: float
    t_hi: float
    kind: str
    reasons: tuple = ()               # (Refusal | NoAnswer, …)
    tag: str | None = None
    info: Mapping = field(default_factory=dict)

    def __post_init__(self):
        _num(self, "t_lo", "t_hi")
        if self.t_lo > self.t_hi:
            raise ValueError(f"Span t_lo {self.t_lo!r} > t_hi {self.t_hi!r}")
        check_in("Span.kind", self.kind, SPAN_KINDS)
        object.__setattr__(self, "reasons", tuple(self.reasons))
        for r in self.reasons:
            if not isinstance(r, (Refusal, NoAnswer)):
                raise ValueError(f"Span.reasons holds {r!r}, not a Refusal or NoAnswer")
        object.__setattr__(self, "info", freeze(self.info))


def plain(x: Any) -> Any:
    """A JSON-ready form: dataclasses become dicts with a «type» field, mappings dicts, tuples lists. A non-finite
    float becomes {"__float__": "nan" | "inf" | "-inf"} (evidence may carry F = inf at a wall), and -0.0 becomes 0.0."""
    if is_dataclass(x) and not isinstance(x, type):
        d = {"type": type(x).__name__}
        d.update({f.name: plain(getattr(x, f.name)) for f in fields(x)})
        return d
    if isinstance(x, Mapping):
        keys = [str(k) for k in x]
        if len(set(keys)) != len(keys):
            raise ValueError(f"mapping keys collide as text: {keys}")
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [plain(v) for v in x]
    if isinstance(x, (set, frozenset)):
        return [plain(v) for v in sorted(x, key=repr)]
    if isinstance(x, float):
        if not math.isfinite(x):
            return {"__float__": repr(x)}
        return 0.0 if x == 0.0 else x
    return x


def canonical(x: Any) -> str:
    """Canonical JSON: sorted keys, floats by repr, no bare NaN (two identical bundles give identical bytes, §A6)."""
    return json.dumps(plain(x), sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
