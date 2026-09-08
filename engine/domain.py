# 선언된 정의역(Domain)과 한계(Limit)를 필드로 들고, 비교 부호를 선언에서 만들어 밖을 반환값으로 거절하는 공용 기계
"""Declared bounds as records, so a consumer cannot bypass them and a reader cannot invert them.

    from domain import Domain, Limit, DOMAIN_REFUSED
    python3 engine/test_domain.py

Why this exists (Brief 154/155, 2026-09-08). Two families of error in one day, neither caught by a gate:

* **Direction.** A 10–30 mW/m² stagnant-lid *ceiling* was read as a floor; *"up to a factor of 5–10"*
  was read as a two-sided interval. The words ceiling / floor / up-to were in comments and docstrings,
  never in a field, so nothing could compare a declaration with the operator that consumed it.
* **Domain.** `mantle_flux.invert_for_flow` refused outside its bisection bracket by name, and
  `core_history.rates` called the *same law* (`implied_flux`) directly at 3040 K and 4021 K with no check
  at all. A domain that one function keeps and its consumers do not is not a domain (derivation-
  discipline §7: a vocabulary is only real if something rejects what is not in it).

`Material.in_domain(p, t)` (eos.py) is the model this copies: one record per law, the callee asks it,
and outside is a **return value** (§2), never an exception and never a silently extrapolated number.

Two records:

* `Domain(quantity, lo, hi, anchor, caveat)` — where a law was shown to hold. `lo`/`hi` may be `None`
  (open on that side: the source prints no bound there, and saying so is the honest record). `anchor`
  is a `file@«phrase»` citation into the source; `caveat` is the source's own sentence about the edge.
  `in_domain(x)` answers; `refusal(x)` writes the named refusal a callee returns.
* `Limit(value, direction, anchor, low=None, high=None)` — a threshold with the way it cuts as a field:
  `floor` (label holds at/above), `ceiling` (label holds at/below), `lower`/`upper` (a domain edge: outside
  is cannot-say, not the opposite label). `holds(x)` generates the comparison from `direction`, so the
  operator can no longer disagree with the word. `low`/`high` carry a printed width when the threshold is
  itself a band (Reese+ 1998's per-body ceilings); `value` is then the end that is stood on.

No runtime dependency: dataclasses only.
"""
from __future__ import annotations

from dataclasses import dataclass

DIRECTIONS = ("floor", "ceiling", "lower", "upper")
DOMAIN_REFUSED = "outside-declared-domain"


@dataclass(frozen=True)
class Domain:
    quantity: str                 # what the bound is on, with its unit: "T_m [K]"
    lo: float | None              # None = the source prints no lower bound
    hi: float | None              # None = the source prints no upper bound
    anchor: str                   # file@«phrase» — where the edge is printed
    caveat: str = ""              # the source's own sentence about behaviour near the edge
    expansion: float | None = None   # the law's expansion point, when it is one (eq. 35's T_0, eq. 39's T_1):
                                     # below it a call is NOT refused — it is noted as declared extrapolation

    def __post_init__(self) -> None:
        if self.lo is None and self.hi is None:
            raise ValueError(f"{self.quantity}: a domain with no edge on either side declares nothing")
        if self.lo is not None and self.hi is not None and not (self.lo < self.hi):
            raise ValueError(f"{self.quantity}: lo {self.lo} must be below hi {self.hi}")
        if "@«" not in self.anchor:
            raise ValueError(f"{self.quantity}: anchor must be a file@«phrase» citation, got {self.anchor!r}")

    def in_domain(self, x: float) -> bool:
        if self.lo is not None and x < self.lo:
            return False
        if self.hi is not None and x > self.hi:
            return False
        return True

    def edges(self) -> str:
        lo = "open" if self.lo is None else f"{self.lo:g}"
        hi = "open" if self.hi is None else f"{self.hi:g}"
        return f"[{lo}, {hi}]"

    def refusal(self, x: float) -> str | None:
        """The named refusal a callee returns for x, or None inside."""
        if self.in_domain(x):
            return None
        side = "below" if (self.lo is not None and x < self.lo) else "above"
        return (f"{DOMAIN_REFUSED}: {self.quantity} = {x:g} is {side} the declared domain {self.edges()} "
                f"({self.anchor}){'; ' + self.caveat if self.caveat else ''}")

    def extrapolation_note(self, x: float) -> str | None:
        """Inside the domain but below the expansion point: a note, not a refusal (the D6/D11 shape).
        The source prints no lower usage limit, so the call is allowed and the distance is written down."""
        if self.expansion is None or not self.in_domain(x) or x >= self.expansion:
            return None
        return (f"{self.quantity} = {x:g} is {self.expansion - x:g} K below the law's expansion point "
                f"{self.expansion:g} K — declared extrapolation ({self.anchor})")


class DomainRefusal(ValueError):
    """Carried by a helper that cannot return a dict; a recipe's solve() turns it into out_of_domain."""


@dataclass(frozen=True)
class Limit:
    value: float
    direction: str                # floor | ceiling | lower | upper
    anchor: str                   # where the number and its direction are printed
    low: float | None = None      # printed width, if the threshold is a band
    high: float | None = None

    def __post_init__(self) -> None:
        if self.direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {self.direction!r}; one of {DIRECTIONS}")
        if (self.low is None) != (self.high is None):
            raise ValueError("a limit's width needs both ends or neither")
        if self.low is not None and not (self.low <= self.value <= self.high):
            raise ValueError(f"value {self.value} outside its own width [{self.low}, {self.high}]")
        if not self.anchor:
            raise ValueError("a limit without an anchor is a number somebody remembered")

    def holds(self, x: float) -> bool:
        """Whether the label (floor/ceiling) or the domain (lower/upper) holds at x — the operator is
        generated here, from the word, and nowhere else."""
        if self.direction in ("floor", "lower"):
            return x >= self.value
        return x <= self.value

    @property
    def kind(self) -> str:
        return "label" if self.direction in ("floor", "ceiling") else "domain-edge"
