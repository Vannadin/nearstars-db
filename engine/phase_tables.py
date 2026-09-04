# 상(phase) 조인 키 + 물성 곁표 — 전기전도도 σ · 조석 k₂/Q. 빈 칸이 기본이고, 채운 칸은 등급·출처를 단다
"""Phase join key and property side tables.

Grounding and pre-registration: `engine/phase-tables-context-notes.md` (owner-adopted pattern, 2026-09-04).

    key    = a phase name the materials actually emit (`eos.Phase.name`, or a single-phase material's name)
    axis   = one property with a waiting consumer: `conductivity` (σ, S/m — C23's Rm criterion),
             `tidal_kq` (k₂/Q band — `tidal_heating`, not yet written)
    cell   = value or band + unit + grade + source + note, OR None

Rules (pre-registered ⑥–⑨):
- An EMPTY cell is legal and the default: it means the consumer refuses for that phase. Nothing is filled
  as `authored` merely to complete the table; an `authored` cell needs the two markers of
  `AUTHORED-VALUES-POLICY.md` in its note and is refused otherwise.
- Only axes with a waiting consumer exist. Colour and latent heat are not opened.
- `summary()` prints filled / total per axis and the number of `authored` cells — the gate shows how empty
  the table is; that list is the research queue.
- Item ② (class defaults) attaches to the body-class axis only; a phase is not a class, so ② never fills
  these cells.
- No value comes from the predecessor tool.

Key discipline: `PHASE_KEYS` is READ from `eos` at import, and the test fails when a table's key set differs
from it — a phase added to `eos` without a row fails the gate; a row for a phase the engine does not emit is
a promise the engine cannot keep and fails too.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eos import MATERIALS            # noqa: E402
from payload import AUTHORED_MARKERS, GRADES  # noqa: E402

MU_0 = 4.0e-7 * 3.141592653589793


def emitted_phase_keys() -> tuple[str, ...]:
    """Every phase name a material can emit, in `eos` order. Read, not typed."""
    keys: list[str] = []
    for name, mat in MATERIALS.items():
        phases = getattr(mat, "phases", None)
        if phases:
            for ph in phases:
                if ph.name not in keys:
                    keys.append(ph.name)
        else:
            k = getattr(mat, "name", name)
            if k not in keys:
                keys.append(k)
    return tuple(keys)


PHASE_KEYS = emitted_phase_keys()


@dataclass(frozen=True)
class Cell:
    value: float | tuple[float, float]     # a number, or a (lo, hi) band
    unit: str
    grade: str                             # measured | calibrated | analog | judgment | authored
    source: str                            # bibcode / document, with the place in it
    note: str = ""

    def __post_init__(self) -> None:
        if self.grade not in GRADES:
            raise ValueError(f"grade '{self.grade}' 는 {GRADES} 밖")
        if self.grade == "authored":
            missing = [m for m in AUTHORED_MARKERS if m not in self.note]
            if missing:
                raise ValueError(f"authored 셀에는 note 에 {AUTHORED_MARKERS} 가 다 있어야 한다 — 없는 것 {missing}")
        if not self.source:
            raise ValueError("셀에 출처가 없다")


# ── axis 1: electrical conductivity σ [S/m] — consumer: C23's magnetic Reynolds number (not built) ──
# Filled: the liquid iron alloy core (the only phase a held paper prints a σ for).
# Empty on purpose: fe_eps (laboratory pure ε-iron — a different material from the alloy core; no held value),
# silicates (Kislyakova+ 2017 `1710.08761` uses an "Earth-like conductivity profile for a dry and iron-poor
# silicate mantle" but the numbers are in its figure, not its text — no printed value to cite), antigorite,
# the ices, liquid/hot water (Nettelmann+ 2014 `1402.7299` prints only the ionic→plasma threshold "> 100 Ω⁻¹ cm⁻¹"
# — a transition marker, not a phase value), H–He, ammonia.
CONDUCTIVITY: dict[str, Cell | None] = {k: None for k in PHASE_KEYS}
CONDUCTIVITY["fe_prem"] = Cell(
    value=1.36e6, unit="S/m", grade="analog",
    source="2203.01065 (RM22) Table, core row 'Electric conductivity (σ) 1.36·10⁶ S m⁻¹', source mark D",
    note=("Earth's liquid-alloy core value applied to any fe_prem layer (analog, not this body's). Cross-checks: "
          "Tang+ 2025 (2025ApJ...989...28T) Table, 'σ 1×10⁶ S m⁻¹, electrical conductivity of core' (their ref. 46) — "
          "the same order. ⚠ SELF-CONTRADICTORY WITHIN RM22: the printed λ_m = 1.32 m²/s implies σ = 6.03e5 S/m, "
          "a factor 2.26 below this cell (paper-defects row 14). C23's Rm = μ₀σUD against a threshold of 50 carries "
          "that factor whole; C23 must compute Rm with BOTH values and report first whether the on/off verdict "
          "flips. Tang+ 2025's ~1e6 supports the order of magnitude only and does not split the 2.26."),
)

# ── axis 2: tidal k₂/Q band [—] — consumer: tidal_heating (not written) ──
# Bands are the class bands of docs/reference/tidal-heating-methodology.md §5 (Io / Enceladus / giant anchors),
# attached to the phases those classes are made of. ⚠ These ten cells are a CLASS band copied onto each phase,
# not a per-phase measurement: the difference between phases of one class is 0 here, and that 0 means "not
# distinguished", not "equal". A per-phase value replaces the cell when one arrives. Empty on purpose: iron (the core is not the dissipating
# layer in the fixed-Q recipe; no band printed), antigorite (hydrated silicate, no band), liquid / hot water
# (k₂/Q is a solid-body quantity; the doc's icy band is for a SHELL + ocean body, not a liquid layer), ammonia.
_TIDAL_DOC = "docs/reference/tidal-heating-methodology.md §5 (class table)"
TIDAL_KQ: dict[str, Cell | None] = {k: None for k in PHASE_KEYS}
for _k in ("mgsio3_en", "mgsio3_prem", "mgsio3_pv"):
    TIDAL_KQ[_k] = Cell(value=(1.0e-3, 1.0e-2), unit="—", grade="analog", source=_TIDAL_DOC,
                        note="rocky / silicate class band (k₂ ~0.1–0.3, Q ~10–100; Io-calibrated). Strongly T-dependent; "
                             "a partially molten layer raises k₂ and lowers Q. A class band on a phase, not a phase measurement.")
for _k in ("ice_ih", "ice_iii", "ice_v", "ice_vi", "ice_vii", "ice_x"):
    TIDAL_KQ[_k] = Cell(value=(1.0e-4, 1.0e-2), unit="—", grade="analog", source=_TIDAL_DOC,
                        note="icy + subsurface-ocean class band (k₂ ~0.01–0.1, Q ~1–100; Enceladus / Europa). The doc marks it "
                             "'very model-dependent' and a floor when an ocean decouples the shell. A class band on a phase.")
TIDAL_KQ["h_he"] = Cell(value=(1.0e-5, 1.0e-3), unit="—", grade="analog", source=_TIDAL_DOC,
                        note="gas / ice giant class band (k₂ ~0.1–0.6, Q ~10³–10⁵). Relevant when the giant itself is the heated body.")

AXES: dict[str, dict[str, Cell | None]] = {"conductivity": CONDUCTIVITY, "tidal_kq": TIDAL_KQ}


def lookup(axis: str, phase: str) -> Cell | None:
    """The cell, or None — None means 'the consumer refuses for this phase' (the normal path)."""
    table = AXES[axis]
    if phase not in table:
        raise KeyError(f"'{phase}' 는 엔진이 내는 상이 아니다 — 키 {PHASE_KEYS}")
    return table[phase]


def summary() -> dict[str, dict[str, int]]:
    """filled / total / authored per axis — what the gate prints."""
    out = {}
    for axis, table in AXES.items():
        cells = [c for c in table.values() if c is not None]
        out[axis] = {"filled": len(cells), "total": len(table),
                     "authored": sum(1 for c in cells if c.grade == "authored")}
    return out


def magnetic_diffusivity(phase: str) -> float | None:
    """λ_m = 1/(μ₀ σ) [m²/s] from the conductivity cell; None when the cell is empty."""
    c = lookup("conductivity", phase)
    return None if c is None else 1.0 / (MU_0 * float(c.value))
