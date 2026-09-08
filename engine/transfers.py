# 한 천체에서 정해진 값이 다른 천체에 들어올 때 붙는 출처 기록(Transfer)과, 그것을 거절하는 규칙
"""A value demonstrated on one body, used on another, carries a record — or the body does not load.

    from transfers import check_body      # run.load_body calls it
    python3 engine/test_transfers.py      # the rules, fired both ways

Why this exists (Brief 153, 2026-09-08). Earth's `mantle_initial_potential_temperature: 3040 K` was
nearly copied into `mars.yaml`. 3040 is not printed anywhere: it is Nimmo's 4800 K divided by
**Earth's** adiabat ratio 1.579, and Mars has its own (1.1937 → 4021 K). The engine held that fact in
a nine-line yaml comment and a `# Earth's, declared for every body` remark, and nothing could say no.
The grade words (`GRADES`, `Band.value_origin`) say where a value came from; none says **which body it
was shown on**. This module adds that word and the three refusals that make it a vocabulary
(derivation-discipline §7: a vocabulary is only real if something rejects what is not in it).

Two axes, two values each — the owner's decision over a single three-valued `form`:

* `form`  — `printed` (the source prints this number) | `derived` (we computed it from the source)
* `kind`  — `parameter` (a model constant; Nimmo's Table 2 set travels as a calibrated whole)
           | `state` (a property of the body itself: a temperature, a mass fraction, an age)

Rules, in the order they fire:

  (i)   A numeric input equal to another body file's input for the same key needs a record on one
        side naming the other as `from_body`. Introduction cost: every existing transfer fails once.
  (ii)  `kind: state` with `form: derived` is refused outright — a body's own state derived with
        another body's state is the 3040 shape. `kind: state` + `printed` needs `grade: analog`;
        `kind: parameter` needs `grade: calibrated`. Vocabulary outside the four words is refused.
  (iii) `anchor` must be a `file@«phrase»` citation; `check_refs.py` (gate 12b) resolves it.

`validated` is a separate axis and is **not** checked here: "may Earth's T_p travel to Mars at all" is
C47's stage-0 question, and folding it into `form` would blur both. It is carried so the record can
say `pending` out loud.

Code defaults that travel (Nimmo's Earth-calibrated constants, Palme & O'Neill's concentrations …)
are listed in `CODE_DEFAULTS` below as `kind: parameter` records; `test_transfers.py` checks each
names an attribute that exists. Consumption of a code default on a body other than its `from_body` is
by construction (they are the recipe's defaults) and is not tracked per call.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from payload import GRADES

FORMS = ("printed", "derived")
KINDS = ("parameter", "state")
GRADE_FOR_KIND = {"state": "analog", "parameter": "calibrated"}
ANCHOR = re.compile(r"^[A-Za-z0-9_./-]+@«[^»]+»$")

BODIES_DIR = Path(__file__).resolve().parent / "bodies"


class TransferError(ValueError):
    """A body file carries a value from another body without a record the rules accept."""


@dataclass(frozen=True)
class Transfer:
    field: str
    from_body: str
    form: str
    kind: str
    grade: str
    anchor: str
    validated: str = "pending"
    module: str | None = None      # CODE_DEFAULTS only: the module whose attribute `field` is

    def __post_init__(self) -> None:
        if self.form not in FORMS:
            raise TransferError(f"{self.field}: form {self.form!r} is not one of {FORMS}")
        if self.kind not in KINDS:
            raise TransferError(f"{self.field}: kind {self.kind!r} is not one of {KINDS}")
        if self.grade not in GRADES:
            raise TransferError(f"{self.field}: grade {self.grade!r} is not one of {GRADES}")
        if self.kind == "state" and self.form == "derived":
            raise TransferError(
                f"{self.field}: a body's own state derived on {self.from_body} does not travel "
                f"(the 3040 K shape — only the printed value travels; derive again with this body's own state)")
        want = GRADE_FOR_KIND[self.kind]
        if self.grade != want:
            raise TransferError(f"{self.field}: kind {self.kind!r} carries grade {want!r}, not {self.grade!r}")
        if not ANCHOR.match(self.anchor):
            raise TransferError(f"{self.field}: anchor {self.anchor!r} is not a file@«phrase» citation")


def parse(doc: dict) -> list[Transfer]:
    """The `transfers:` block of a body file, each entry rule-checked on construction."""
    out = []
    for raw in doc.get("transfers") or []:
        try:
            out.append(Transfer(**raw))
        except TypeError as e:          # unknown or missing key
            raise TransferError(f"{doc.get('name')}: transfer entry {raw!r}: {e}") from None
    return out


def _numeric_inputs(doc: dict) -> dict[str, float]:
    return {k: v for k, v in (doc.get("inputs") or {}).items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)}


def shared_values(doc: dict, others: dict[str, dict]) -> list[tuple[str, str]]:
    """(key, other_body) pairs where this body's numeric input equals another body's for the same key."""
    mine = _numeric_inputs(doc)
    hits = []
    for name, other in others.items():
        if name == doc.get("name"):
            continue
        theirs = _numeric_inputs(other)
        for k, v in mine.items():
            if k in theirs and theirs[k] == v:
                hits.append((k, name))
    return hits


def load_others(bodies_dir: Path = BODIES_DIR) -> dict[str, dict]:
    docs = {}
    for p in sorted(bodies_dir.glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        docs[d["name"]] = d
    return docs


def check_body(doc: dict, others: dict[str, dict] | None = None) -> list[Transfer]:
    """Rules (i)–(iii) for one body file. Raises TransferError; returns the accepted records."""
    others = load_others() if others is None else others
    records = parse(doc)                       # (ii), (iii)
    recorded = {t.field for t in records}
    for key, other in shared_values(doc, others):   # (i)
        # A record for the key on either side satisfies the pair: it names where the value came from,
        # which may be a third body (Mars and Pandora both carry Earth's 1600 K, from Earth, not each other).
        if key in recorded:
            continue
        if key in {t["field"] for t in (others[other].get("transfers") or [])}:
            continue
        raise TransferError(
            f"{doc['name']}: inputs.{key} equals {other}'s value and neither side records the transfer "
            f"(add a transfers: entry — field, from_body, form, kind, grade, anchor)")
    return records


# ── Code defaults that were demonstrated on one body and serve every body ──────────────────────
# One record per module constant (or constant set) the survey of 2026-09-08 found travelling. All are
# `parameter` — a calibrated set moves as a whole under its CONDITION string. K_T and K_B are `derived`
# (by identity from printed constants), which the parameter rule allows; on a `state` it would not.
_E = "Earth"
CODE_DEFAULTS: tuple[Transfer, ...] = (
    Transfer("T_S", _E, "printed", "parameter", "calibrated",
             "mantle_flux.py@«T_S = 293.0»", "at source", module="mantle_flux"),
    Transfer("EARTH_G", _E, "printed", "parameter", "calibrated",
             "mantle_flux.py@«EARTH_G = 9.8»", "at source", module="mantle_flux"),
    Transfer("RA_C", _E, "printed", "parameter", "calibrated",
             "mantle_flux.py@«Nimmo+ 2004 Table 2, top-layer constants»", "at source", module="mantle_flux"),
    Transfer("K_T", _E, "derived", "parameter", "calibrated",
             "mantle_flux.py@«K_T = KAPPA_T * RHO_M * C_PM»", "identity κ = k/(ρ C_p)", module="mantle_flux"),
    Transfer("C_PM", _E, "printed", "parameter", "calibrated",
             "mantle_flux.py@«C_PM = 1200.0»", "at source", module="mantle_flux"),
    Transfer("K_B", _E, "derived", "parameter", "calibrated",
             "cmb_flux.py@«K_B = KAPPA_B * mf.RHO_M * mf.C_PM»", "identity", module="cmb_flux"),
    Transfer("K_CORE", _E, "printed", "parameter", "calibrated",
             "cmb_flux.py@«K_CORE = 50.0»", "at source", module="cmb_flux"),
    Transfer("DTC_DT", _E, "printed", "parameter", "calibrated",
             "core_energy.py@«DTC_DT = -33.0 / GYR_S»", "at source", module="core_energy"),
    Transfer("MANTLE_SHARE", _E, "printed", "parameter", "calibrated",
             "radiogenic.py@«MANTLE_SHARE = 0.70»", "at source", module="radiogenic"),
    Transfer("B_EQ_EARTH_UT", _E, "printed", "parameter", "calibrated",
             "dynamo_rocky.py@«B_EQ_EARTH_UT = 30.0»", "at source", module="dynamo_rocky"),
    Transfer("EARTH_POTENTIAL_T", _E, "printed", "parameter", "calibrated",
             "eos.py@«EARTH_POTENTIAL_T = 1600.0»", "t_ref of every EOS fit", module="eos"),
)


def check_code_defaults() -> list[str]:
    """Each CODE_DEFAULTS record names an attribute that exists in its module. Returns problems."""
    import importlib
    problems = []
    for t in CODE_DEFAULTS:
        mod = importlib.import_module(t.module)
        if not hasattr(mod, t.field):
            problems.append(f"{t.module}.{t.field} does not exist")
    return problems
