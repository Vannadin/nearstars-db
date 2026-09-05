# 세기류 도출값의 폭을 어떻게 싣고 어디서 무너뜨리는가 — 밴드·묶음·선택지 기록 (C32)
"""How a derived strength carries its width, and what happens where the width cannot go on.

    from bands import Band, corners, Choice

The owner asked for two things (2026-09-04): *"자기장 세기는 밴드로 출력하면 좋겠다. 하나의 묶음에서
다른 묶음으로 값이 오갈 때는 사용자한테 선택지가 있음 좋겠어."* This module is the shape both take, so
that the next recipe does not invent a third one.

**A band needs both of its ends printed.** Measured before this was written: only two places in the
engine qualify — the multipolar grid {0.05, 0.10}, both printed by OC06, and the brown-dwarf
radius-driven width, where the range itself is declared. Everything else would be two numbers nobody
published. So a value has three possible shapes, and `Band.kind` says which:

- **interval** — both ends printed. `low` and `high` both real.
- **floored point** — one end printed, the other not. The heat-pipe row is this: the document prints
  2.5 W/m² and "no firm upper bound". A floor is real information (above it, certainly this label;
  below it, unknown), so it is kept as a floor rather than flattened into a bare point — and the
  floor's own grade is recorded separately, because *that* 2.5 is one body's computed flux.
- **point** — nothing printed to widen it. Carries `grade="authored"` if the value itself was chosen
  rather than measured.

**Where a band stops.** The width does not travel forever, and where it ends depends on the consumer:

1. **A formula consumer** — the band passes through. Walk the corners and carry the spread out the
   other side. Two modules already did this by hand before this module existed (`cmb_flux` walks
   ζ × κ_B, `core_history` names its `K_CORNERS`); `corners()` is that pattern with a name.
2. **A classifier consumer** — the band does *not* collapse to a point, it splits into branches. Feed
   a width to a label table and the output is two different labels with nothing in between. The
   engine must not pick one silently, so this is where `Choice` is mandatory.
3. **The emit boundary** — always one number. Every band collapses eventually; (1) collapses as late
   as possible and (2) collapses at the classifier.

**Bundled widths are chosen whole.** `A_Bond = q · p` ties the Bond-albedo width to the phase-integral
width; multiplying them as if independent invents a spread neither source supports. The greenhouse
forcing is worse — CO₂ 1.3–4 bar, H₂ 5–20 %, N₂ 2–3× are a published *combination grid*, and splitting
them produces combinations nobody published. A band therefore carries a `bundle` name, and `corners()`
walks bundle members in step instead of crossing them.

**A collapse is recorded, not just performed**: what was chosen, which end of the band it came from,
and why. The hand-written version of that record already exists on the α Cen board, where a narrative
reads "Teq 225K assumes A_B=0.3: with Class II albedo 0.5–0.8 it could be…" beside a point-valued
field. This turns that sentence into fields.

**Consequences are plural.** A choice can improve one thing and cost another — the bright end of an
albedo band moves surface temperature most, the dark end moves visual contrast most, in opposite
directions. `Choice.consequences` is a mapping precisely so that a one-axis summary cannot hide the
other axis.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

GRADES = ("measured", "calibrated", "analog", "declared", "authored")


@dataclass(frozen=True)
class Band:
    """A value that may carry a width, and always carries where the width came from."""

    value: float
    low: float | None = None
    high: float | None = None
    width_source: str = ""          # in words: which document prints the ends, or why there are none
    grade: str = "authored"
    bundle: str | None = None       # None = independent; a name = chosen whole with its siblings
    floor_grade: str | None = None  # a floor can be weaker than the value it bounds

    def __post_init__(self) -> None:
        if self.grade not in GRADES:
            raise ValueError(f"unknown grade {self.grade!r}; one of {GRADES}")
        for end in (self.low, self.high):
            if end is not None and not (end == end):        # NaN
                raise ValueError("a band end may not be NaN")
        if self.low is not None and self.high is not None and not (self.low <= self.value <= self.high):
            raise ValueError(f"value {self.value} outside its own band [{self.low}, {self.high}]")
        if (self.low is not None or self.high is not None) and not self.width_source:
            raise ValueError("a width without a source is not a band — say where the ends are printed")

    @property
    def kind(self) -> str:
        if self.low is not None and self.high is not None:
            return "interval"
        if self.low is not None or self.high is not None:
            return "floored point"
        return "point"

    def ends(self) -> tuple[float, ...]:
        """The points a formula consumer should walk: both ends and the value, without duplicates."""
        seen = [self.value] + [e for e in (self.low, self.high) if e is not None]
        return tuple(sorted(set(seen)))

    def emit(self, name: str) -> dict:
        """The `*_min` / `*_max` shape the recipes already use (dynamo.py's brown-dwarf branch)."""
        out = {name: self.value}
        if self.low is not None:
            out[f"{name}_min"] = self.low
        if self.high is not None:
            out[f"{name}_max"] = self.high
        return out


def point(value: float, grade: str, why: str = "") -> Band:
    """A value with no printed width. `why` says what would be needed to widen it."""
    return Band(value=value, width_source="", grade=grade)


def floored(value: float, floor: float, width_source: str, grade: str, floor_grade: str) -> Band:
    """One end printed. Kept as a floor because a floor is real information."""
    return Band(value=value, low=floor, width_source=width_source, grade=grade, floor_grade=floor_grade)


def corners(bands: dict[str, Band]) -> list[dict[str, float]]:
    """Every combination a formula consumer should evaluate, with bundles kept whole.

    Independent bands cross with everything. Bands sharing a `bundle` name move together: member i of
    one is taken with member i of its siblings, never with member j, because the combination is what
    the source published."""
    independent = {k: v for k, v in bands.items() if v.bundle is None}
    bundles: dict[str, dict[str, Band]] = {}
    for k, v in bands.items():
        if v.bundle is not None:
            bundles.setdefault(v.bundle, {})[k] = v
    for name, members in bundles.items():
        widths = {len(b.ends()) for b in members.values()}
        if len(widths) != 1:
            raise ValueError(f"bundle {name!r} members must have the same number of ends to move in "
                             f"step; got {widths}")
    axes: list[list[dict[str, float]]] = []
    for k, b in independent.items():
        axes.append([{k: e} for e in b.ends()])
    for members in bundles.values():
        n = len(next(iter(members.values())).ends())
        axes.append([{k: b.ends()[i] for k, b in members.items()} for i in range(n)])
    out = []
    for combo in itertools.product(*axes) if axes else [()]:
        merged: dict[str, float] = {}
        for part in combo:
            merged.update(part)
        out.append(merged)
    return out


@dataclass(frozen=True)
class Choice:
    """What the engine refuses to decide, handed to the owner with everything needed to decide it."""

    at: str                                  # the node or boundary where the width could not go on
    quantity: str
    candidates: tuple[dict, ...]             # each: {value, end, source, grade}
    consequences: dict[str, str] = field(default_factory=dict)   # axis → what changes, in words
    default: float | None = None             # what runs until someone chooses; None = nothing runs
    note: str = ""

    def __post_init__(self) -> None:
        if len(self.candidates) < 2:
            raise ValueError("a choice needs at least two candidates, or it is not a choice")
        for c in self.candidates:
            missing = {"value", "end", "source", "grade"} - set(c)
            if missing:
                raise ValueError(f"candidate {c} is missing {sorted(missing)}")
        if not self.consequences:
            raise ValueError("a choice without a measured consequence is a question, not a choice")


@dataclass(frozen=True)
class Collapse:
    """The record left where a width became one number: what, which end, why."""

    quantity: str
    chosen: float
    end: str            # "low" | "value" | "high"
    why: str
    by: str             # "owner" | "engine (formula consumer)" | "emit"

    def line(self) -> str:
        return f"{self.quantity} = {self.chosen:g} ({self.end} end, {self.by}): {self.why}"
