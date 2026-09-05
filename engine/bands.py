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
  rather than measured. A pick between two *published* ends is not `authored` but `judgment`, which is
  the grade a `Collapse` leaves behind.

A band's working `value` may be `None`, which says *the document prints the ends and no point inside
them*. That is the state the eight rows of the Bond-albedo table are in, and it is not the same as a
midpoint: a midpoint is a pick, and a pick is a `Collapse`.

Such a band **is** emitted, because the game cannot start without a number (owner, 2026-09-05). What
the refusal used to protect is protected by a label instead: the emitted point carries
`<name>_pick`, and for a band nobody has chosen it reads **unchosen**. Read a bare number a year from
now and there is no way to tell a reviewed decision from a gap someone never filled; that
misreading is the defect this whole day was spent removing, so the number never travels alone. Every
emit carries the ends and their source alongside.

The one band this does not reach is a member of a co-selected group whose pairing nobody published. It has no
middle *of its own*: filling one here and one in each sibling rebuilds exactly the combination
`corners()` refuses, so `emit()` sends the caller to the case's `Choice` instead. Nothing stalls,
because choosing the case supplies every member at once.

Three ways a point can come to exist, and they must never share a label:

- **printed** — the document prints a centre with its band, `660 µT (540–810)`. That centre is the
  default. **Never compute a midpoint over a printed one**; 675 would be our arithmetic overwriting
  a published number.
- **chosen** — someone picked a point, and a `Collapse` says which end and why.
- **unchosen** — nobody picked, so the engine fills the middle to keep the pipeline moving. Not a
  judgment: no judgment happened. The grade stays whatever the *ends* are graded, because inventing a
  grade for "we filled it in" would put that fiction into the same vocabulary as measurement.

The middle is arithmetic unless the band says `mean="geometric"`. A quantity that spreads by factors
(the multipolar grid 0.05–0.10: arithmetic 0.075, geometric 0.0707) is more natural in the geometric
mean, but choosing one for every band would be an exchange rate the engine invented, so each band
declares its own and silence means arithmetic. On a narrow band the two agree and it does not matter.

**Where a band stops.** The width does not travel forever, and where it ends depends on the consumer:

1. **A formula consumer** — the band passes through. Walk the corners and carry the spread out the
   other side. Two modules already did this by hand before this module existed (`cmb_flux` walks
   ζ × κ_B, `core_history` names its `K_CORNERS`); `corners()` is that pattern with a name.
2. **A classifier consumer** — the band does *not* collapse to a point, it splits into branches. Feed
   a width to a label table and the output is two different labels with nothing in between. The
   engine must not pick one silently, so this is where `Choice` is mandatory.
3. **The emit boundary** — always one number. Every band collapses eventually; (1) collapses as late
   as possible and (2) collapses at the classifier.

**A co-selected group whose pairing nobody published cannot be walked at all.** Moving members in step is not
the neutral option — it is a second assumption, and the greenhouse cases are where it shows: raising
CO₂ lets a run reach the same temperature on less H₂, so pairing both low ends is a combination the
paper no more published than the crossed corners are. Such a band declares `pairing="unknown"` and
`corners()` refuses it by name, rather than quietly walking the diagonal.

⚠ **This field is called `co_selected` and not `bundle` on purpose.** `bindings.yaml` already has a
`bundled`, rendered by `build_graph_page` and read by `backflow` as "벌크라 재도출 불가": a field that is
a bulk figure and cannot be re-derived per component. Unrelated meaning, and the two would never have
collided anywhere — which is exactly the danger, because nothing would have failed on the day one
slid into the other's place. A comment stops the people who read; a different name stops the rest.

**Alternatives are not seats.** `co_selected` says *chosen together*; `estimates` says *chosen instead of
each other*. The eight rows of the Bond-albedo table and the two phase-integral families all estimate
`A_Bond` — the document reaches it by an analog table **or** by `q·p` — so they are ten options on one
seat, not ten seats. Counting them as ten would show the owner the same quantity to decide twice.

**Bundled widths are chosen whole.** `A_Bond = q · p` ties the Bond-albedo width to the phase-integral
width; multiplying them as if independent invents a spread neither source supports. The greenhouse
forcing is worse — CO₂ 1.3–4 bar, H₂ 5–20 %, N₂ 2–3× are a published *combination grid*, and splitting
them produces combinations nobody published. A band therefore carries a `co_selected` group name, and
`corners()` walks that group's members in step instead of crossing them.

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

# 등급 어휘는 payload 가 하나만 가진다 — 여기서 다시 적으면 그 순간 두 번째 사본이고,
# 실제로 그렇게 됐었다: 이 파일은 payload 에 없는 `declared` 를 지어내고, 발표된 선택지
# 사이의 판단을 뜻하는 `judgment` 를 빠뜨렸다. 하필 C32 의 붕괴가 바로 그 등급이다.
from payload import GRADES  # noqa: F401


@dataclass(frozen=True)
class Band:
    """A value that may carry a width, and always carries where the width came from."""

    value: float | None
    low: float | None = None
    high: float | None = None
    width_source: str = ""          # in words: which document prints the ends, or why there are none
    grade: str = "authored"
    co_selected: str | None = None       # None = independent; a name = chosen whole with its siblings
    floor_grade: str | None = None  # a floor can be weaker than the value it bounds
    pairing: str = "in step"        # "in step" | "unknown" — is it published which end goes with which
    estimates: str | None = None    # the quantity this band is ONE estimate of; siblings naming the
                                    # same quantity are alternatives, and picking two double-counts
    value_origin: str = "chosen"    # "printed" (the document prints the centre) | "chosen" (someone picked)
    mean: str = "arithmetic"        # "arithmetic" | "geometric" — how an unchosen middle is filled

    def __post_init__(self) -> None:
        if self.value is None and self.low is None and self.high is None:
            raise ValueError("a band with neither a value nor an end says nothing")
        if self.grade not in GRADES:
            raise ValueError(f"unknown grade {self.grade!r}; one of {GRADES}")
        if self.pairing not in ("in step", "unknown"):
            raise ValueError(f"unknown pairing {self.pairing!r}; 'in step' or 'unknown'")
        if self.value_origin not in ("printed", "chosen"):
            raise ValueError(f"unknown value_origin {self.value_origin!r}; 'printed' or 'chosen'")
        if self.mean not in ("arithmetic", "geometric"):
            raise ValueError(f"unknown mean {self.mean!r}; 'arithmetic' or 'geometric'")
        if self.mean == "geometric" and any(e is not None and e <= 0 for e in (self.low, self.high)):
            raise ValueError("a geometric mean needs both ends positive")
        if self.pairing == "unknown" and self.co_selected is None:
            raise ValueError("pairing describes how a band moves with its co-selected siblings; "
                             "an independent band has nothing to pair with")
        for end in (self.low, self.high):
            if end is not None and not (end == end):        # NaN
                raise ValueError("a band end may not be NaN")
        if (self.low is not None and self.high is not None and self.value is not None
                and not (self.low <= self.value <= self.high)):
            raise ValueError(f"value {self.value} outside its own band [{self.low}, {self.high}]")
        if (self.low is not None or self.high is not None) and not self.width_source:
            raise ValueError("a width without a source is not a band — say where the ends are printed")

    @property
    def chosen(self) -> bool:
        """Whether a working point inside the band has been picked yet."""
        return self.value is not None

    @property
    def kind(self) -> str:
        if self.low is not None and self.high is not None:
            return "interval"
        if self.low is not None or self.high is not None:
            return "floored point"
        return "point"

    @property
    def pick(self) -> str:
        """How the emitted point came to exist. Never the same word for two different origins."""
        if self.value is None:
            return "unchosen"
        return self.value_origin

    def middle(self) -> float | None:
        """The point the engine fills when nobody has chosen one, by the band's own declared mean."""
        if self.low is None or self.high is None:
            return None
        if self.mean == "geometric":
            return (self.low * self.high) ** 0.5
        return (self.low + self.high) / 2.0

    def ends(self) -> tuple[float, ...]:
        """The points a formula consumer should walk: both ends and the value, without duplicates."""
        seen = [e for e in (self.value, self.low, self.high) if e is not None]
        return tuple(sorted(set(seen)))

    def emit(self, name: str) -> dict:
        """The `*_min` / `*_max` shape the recipes already use (dynamo.py's brown-dwarf branch), plus
        the label that says how the point came to exist and where its ends are printed."""
        if self.value is None and self.pairing == "unknown":
            raise ValueError(
                f"{name}: this band belongs to the co-selected group {self.co_selected!r}, whose pairing nobody "
                "published, so it has no middle of its own — filling one here and one in each "
                "sibling rebuilds the very combination corners() refuses. Choose the case whole "
                "(its Choice), then emit the case's own numbers.")
        value = self.value if self.value is not None else self.middle()
        if value is None:
            raise ValueError(f"{name}: no point and no pair of ends to take a middle between")
        out = {name: value, f"{name}_pick": self.pick}
        if self.value is None:
            out[f"{name}_pick"] = (f"unchosen — nobody has picked a point in this band, so the engine "
                                   f"filled the {self.mean} middle")
        if self.low is not None:
            out[f"{name}_min"] = self.low
        if self.high is not None:
            out[f"{name}_max"] = self.high
        if self.width_source:
            out[f"{name}_width_source"] = self.width_source
        return out


def point(value: float, grade: str, why: str = "") -> Band:
    """A value with no printed width. `why` says what would be needed to widen it."""
    return Band(value=value, width_source="", grade=grade)


def floored(value: float, floor: float, width_source: str, grade: str, floor_grade: str) -> Band:
    """One end printed. Kept as a floor because a floor is real information."""
    return Band(value=value, low=floor, width_source=width_source, grade=grade, floor_grade=floor_grade)


def corners(bands: dict[str, Band]) -> list[dict[str, float]]:
    """Every combination a formula consumer should evaluate, with co_groups kept whole.

    Independent bands cross with everything. Bands sharing a `co_selected` name move together: member i of
    one is taken with member i of its siblings, never with member j, because the combination is what
    the source published."""
    independent = {k: v for k, v in bands.items() if v.co_selected is None}
    co_groups: dict[str, dict[str, Band]] = {}
    for k, v in bands.items():
        if v.co_selected is not None:
            co_groups.setdefault(v.co_selected, {})[k] = v
    for name, members in co_groups.items():
        unknown = sorted(k for k, b in members.items() if b.pairing == "unknown")
        if unknown:
            raise ValueError(
                f"co-selected group {name!r} cannot be walked: {unknown} declare their pairing unknown. "
                "Crossing the members invents combinations nobody published, and walking them in "
                "step invents a different one — the diagonal is a claim too. Choose a published "
                "case instead.")
        widths = {len(b.ends()) for b in members.values()}
        if len(widths) != 1:
            raise ValueError(f"co-selected group {name!r} members must have the same number of ends to move in "
                             f"step; got {widths}")
    axes: list[list[dict[str, float]]] = []
    for k, b in independent.items():
        axes.append([{k: e} for e in b.ends()])
    for members in co_groups.values():
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
    """The record left where a width became one number: what, which end, why.

    `end="outside"` is not a pick from the band at all — it is an adopted value that disagrees with
    the band its own source prints, and the α Cen board holds one (`A_B = 0.3` beside a printed Class
    II albedo of 0.5–0.8). It gets its own word so that filling an unchosen middle can never quietly
    stand in for it: replace that 0.3 with 0.65 and the disagreement is gone from the record."""

    quantity: str
    chosen: float
    end: str            # "low" | "value" | "high" | "outside"
    why: str
    by: str             # "owner" | "engine (formula consumer)" | "emit"

    def __post_init__(self) -> None:
        if self.end not in ("low", "value", "high", "outside"):
            raise ValueError(f"unknown end {self.end!r}; 'low', 'value', 'high' or 'outside'")

    def line(self) -> str:
        return f"{self.quantity} = {self.chosen:g} ({self.end} end, {self.by}): {self.why}"
