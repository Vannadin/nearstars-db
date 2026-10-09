# 결과 묶음 — 값 하나(Quantity: 점·띠·출처)와 결과 셋(Answer · Refusal · NoAnswer)의 꼴 (phase1-design D-A3-1..5).
"""Result types of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A3-1..5, post-freeze note 1).

Every type is a frozen dataclass whose collections are tuples or read-only mappings, so a value cannot change
after it is built. Construction checks raise `ValueError`: a bad value here comes from code, not from input
(input is refused by `validate`), so it is a bug and never a refusal.
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
#: Input grade words (engine/payload.py:34–36 `GRADE_WORDS` minus «calibrated»; R-GV-1).
GRADE_WORDS = ("measured", "literature", "analog", "derived", "judgment", "declared", "inherited", "authored",
               "calibrated")
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
#: check or an on-demand re-solve measured it; otherwise `sources.solver` is null with this reason.
BAND_NOT_MEASURED = "numerical band not measured"


def _ro(m: Mapping | None) -> Mapping:
    return MappingProxyType(dict(m or {}))


def check_finite(name: str, x: float) -> None:
    """A number that crosses a type boundary is finite (W-L10-01). Module-level so a negative control can disable it."""
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
        raise ValueError(f"{name} must be a finite number, got {x!r}")


def check_in(name: str, x: Any, allowed: tuple) -> None:
    if x not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {x!r}")


@dataclass(frozen=True)
class SourceBand:
    """One side-source of a band: the offsets it alone produces (R-STEP0-11 `{lo, hi, contrib}`)."""
    lo: float
    hi: float
    contrib: str

    def __post_init__(self):
        check_finite("SourceBand.lo", self.lo)
        check_finite("SourceBand.hi", self.hi)
        if self.lo > self.hi:
            raise ValueError(f"SourceBand lo {self.lo!r} > hi {self.hi!r}")
        if not self.contrib:
            raise ValueError("SourceBand.contrib must name what the source is")


@dataclass(frozen=True)
class Sources:
    """The three sources of a band (R-STEP0-11). Each is a `SourceBand` or None with a reason.

    §A1.7 maps here: the numerical band is `solver`, the declared-input band is `input`; `model` stays null with a
    reason until phase 2's material bands.
    """
    input: SourceBand | None
    model: SourceBand | None
    solver: SourceBand | None
    input_reason: str | None = None
    model_reason: str | None = None
    solver_reason: str | None = None

    def __post_init__(self):
        for name in ("input", "model", "solver"):
            if getattr(self, name) is None and not getattr(self, name + "_reason"):
                raise ValueError(f"Sources.{name} is null without a reason")


@dataclass(frozen=True)
class Band:
    """An envelope «the range we cannot rule out» (R-STEP0-11): never a probability, never called σ."""
    lo: float
    hi: float
    method: str
    sources: Sources
    basis: str = "envelope"

    def __post_init__(self):
        check_finite("Band.lo", self.lo)
        check_finite("Band.hi", self.hi)
        if self.lo > self.hi:
            raise ValueError(f"Band lo {self.lo!r} > hi {self.hi!r}")
        if self.basis != "envelope":
            raise ValueError(f"Band.basis must be 'envelope', got {self.basis!r}")
        if not self.method:
            raise ValueError("Band.method must name how the band was computed")


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
        object.__setattr__(self, "window", _ro(self.window))


@dataclass(frozen=True)
class SolverInfo:
    """Solver provenance. `solve_id` is §A6's one definition (sha256 of canonical Body, material bytes, options,
    solver version string; no clock); it is computed by the solve context, never here."""
    solve_id: str
    fallbacks: tuple = ()          # class F sites (R-C138-2)
    substitutions: tuple = ()
    counters: tuple = ()           # ((name, int), …), from the solve trace (§A6)


@dataclass(frozen=True)
class Provenance:
    """Per-quantity provenance (D-A3-3, W-L12-02)."""
    grade: str
    solver: SolverInfo
    inputs_read: tuple = ()             # ((field, grade), …)
    consumed_observations: tuple = ()   # declared observations a closure consumed, e.g. ("R", "core+layer radius 1845 km")
    materials: tuple = ()               # (MaterialRef, …)
    extrapolation: tuple = ()           # ((material id, window text, band text or counter), …) (R-RUL-10/10a)

    def __post_init__(self):
        check_in("Provenance.grade", self.grade, GRADES)


@dataclass(frozen=True)
class Label:
    """An oracle label, added by the label pass outside the solver (D-A3-4). Key: (body, node, key, state)."""
    kind: str
    scope: str
    rid: str
    reason: str
    state: str = "declared"             # «declared», a T_pot, or a point id

    def __post_init__(self):
        check_in("Label.kind", self.kind, LABEL_KINDS)
        check_in("Label.scope", self.scope, LABEL_SCOPES)


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
        check_finite(f"Quantity({self.key}).point", self.point)
        check_in(f"Quantity({self.key}).kind", self.kind, KINDS)
        check_in(f"Quantity({self.key}).method", self.method, METHODS)
        if self.band is None:
            if not self.band_reason:
                raise ValueError(f"Quantity({self.key}) has no band and no band_reason")
        elif not self.band.lo <= self.point <= self.band.hi:
            raise ValueError(f"Quantity({self.key}) point {self.point!r} outside its band "
                             f"[{self.band.lo!r}, {self.band.hi!r}]")
        if self.sensitivity is not None:
            check_finite(f"Quantity({self.key}).sensitivity", self.sensitivity)
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
        object.__setattr__(self, "fields", _ro(self.fields))


@dataclass(frozen=True)
class Refusal:
    """A named refusal (D-A3-2). Build it with `refusals.make`, which checks the id and its evidence fields."""
    id: str
    where: str
    evidence: Mapping
    text: str

    def __post_init__(self):
        object.__setattr__(self, "evidence", _ro(self.evidence))


@dataclass(frozen=True)
class NoAnswer:
    """No value was reached (D-A3-2). Unconverged values are not values (R-RUL-22). Build it with `refusals.no_answer`."""
    reason: str
    where: str
    evidence: Mapping
    text: str

    def __post_init__(self):
        check_in("NoAnswer.reason", self.reason, NO_ANSWER_REASONS)
        object.__setattr__(self, "evidence", _ro(self.evidence))


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
        for k in ("m", "r", "p", "t"):
            check_finite(f"LocatedBoundary({self.name}).{k}", getattr(self, k))


@dataclass(frozen=True)
class Answer:
    """An answer (D-A3-2): quantities by where, located boundaries, profiles, and what could not be made."""
    quantities: tuple
    boundaries: tuple = ()
    profiles: Mapping = field(default_factory=dict)   # layer id → {column name → tuple of floats}
    missing: tuple = ()                               # ((key, Refusal | NoAnswer), …)
    notes: tuple = ()

    def __post_init__(self):
        object.__setattr__(self, "profiles", _ro({k: _ro(v) for k, v in dict(self.profiles).items()}))
        seen = set()
        for q in self.quantities:
            if not isinstance(q, Quantity):
                raise ValueError(f"Answer holds a non-Quantity {q!r}")
            ident = (q.key, q.where)
            if ident in seen:
                raise ValueError(f"Answer holds {q.key} at {q.where} twice")
            seen.add(ident)
        for key, why in self.missing:
            if not isinstance(why, (Refusal, NoAnswer)):
                raise ValueError(f"missing {key} must carry a Refusal or NoAnswer, got {why!r}")

    @property
    def grade(self) -> str:
        """The result-level grade: the worst over its quantities, never set by hand (D-A3-3)."""
        if not self.quantities:
            raise ValueError("an Answer with no quantities has no grade")
        return GRADES[max(GRADES.index(q.provenance.grade) for q in self.quantities)]

    @property
    def kind(self) -> str:
        return "answer"


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
    reasons: tuple = ()
    tag: str | None = None
    info: Mapping = field(default_factory=dict)

    def __post_init__(self):
        check_finite("Span.t_lo", self.t_lo)
        check_finite("Span.t_hi", self.t_hi)
        if self.t_lo > self.t_hi:
            raise ValueError(f"Span t_lo {self.t_lo!r} > t_hi {self.t_hi!r}")
        check_in("Span.kind", self.kind, SPAN_KINDS)
        object.__setattr__(self, "info", _ro(self.info))


def plain(x: Any) -> Any:
    """A JSON-ready form: dataclasses become dicts with a «type» field, mappings dicts, tuples lists."""
    if is_dataclass(x) and not isinstance(x, type):
        d = {"type": type(x).__name__}
        d.update({f.name: plain(getattr(x, f.name)) for f in fields(x)})
        return d
    if isinstance(x, Mapping):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [plain(v) for v in x]
    return x


def canonical(x: Any) -> str:
    """Canonical JSON: sorted keys, floats by repr, no NaN (two identical bundles give identical bytes, §A6)."""
    return json.dumps(plain(x), sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
