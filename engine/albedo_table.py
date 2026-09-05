# 표면 유형별 Bond 알베도·위상적분 밴드 — 문서가 인쇄한 양끝을 점으로 접지 않고 그대로 싣는다 (C32)
"""The Bond-albedo table as bands, and the two axes a pick moves in opposite directions.

    python3 engine/albedo_table.py

`docs/reference/surface-color-albedo-methodology.md` prints eight surface types and gives **every one
of them a range**, not a number. The boards downstream carry one number each. This module holds the
printed ends so that the collapse from eight intervals to eight numbers happens somewhere it can be
read, and reports what each end costs.

**The two paths are alternatives, not factors.** The document offers two routes to a Bond albedo and
joins them with *or*, in one sentence:

    …adopt a `q` appropriate to the surface type (analog-grounded), **or** take the Bond albedo
    directly from a solar-system analog.

So `A_analog` (the eight rows) and `q · p` (the phase integral times the geometric albedo) are two
estimates **of the same quantity**. Multiplying the analog table's band by the phase integral's band
is not a wide band, it is a category error — `A = q·p` already has `A` on the left. Where a real
bundle does live is inside the second path: `q` and `p` co-vary by surface type (dark back-scattering
regolith is low in both; bright icy and cloudy bodies are high in both), so crossing the high end of
one against the low end of the other invents a surface nobody described. This module cannot yet
demonstrate that bundle, because no per-surface-type `p` table exists — §5 estimates `p` spectrally,
per body. That gap is named here rather than filled with invented numbers.

**Consequences run on two axes and they disagree.** The albedo is both what the body looks like and a
term in the equilibrium temperature. The bright rows move temperature most and contrast least; the
dark rows do the reverse — the darkest row is a factor of three wide and moves `T_eq` by 1 %. A
one-line summary of "how much does this band matter" would report whichever axis the writer happened
to have in mind, so both are printed for every row.

Anchors for the values below (C33):
  surface-color-albedo-methodology.md@«**Typical Bond albedos by surface type** (analog anchors, pick by composition+state)»
  surface-color-albedo-methodology.md@«The phase integral `q` (≈ 1 for a Lambert surface; ~0.3–0.5 for dark back-scattering regolith like the Moon, ~0.7–1.3 for bright icy/cloud bodies with forward scattering)»
  surface-color-albedo-methodology.md@«A_Bond = q · p_geometric»
  surface-color-albedo-methodology.md@«T_eq = [ S (1 − A) / (4 σ) ]^(1/4)»
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import Band  # noqa: E402

DOC = "surface-color-albedo-methodology.md"

# (표면 유형, 문서가 인쇄한 양끝, 아날로그, 그 행을 겨눈 앵커)
# 값 자리가 비어 있는 것은 누락이 아니다 — 문서가 구간만 인쇄하고 그 안의 점은 고르지 않았다.
_ROWS = (
    ("fresh water ice / snow",        0.6,  0.8,  "Europa, Enceladus, fresh frost",
     "| Fresh water-ice / snow | ~0.6–0.8 |"),
    ("volatile-ice plains (N₂/CH₄/CO₂)", 0.5, 0.85, "Pluto Sputnik, Triton bright terrain",
     "| N₂/CH₄/CO₂ volatile-ice plains | ~0.5–0.85 |"),
    ("bright icy moon (mature)",      0.3,  0.6,  "Europa ~0.6; mixed or old ice lower",
     "| Bright icy moon (mature) | ~0.3–0.6 |"),
    ("oxidized (ferric) dust / rust", 0.2,  0.3,  "Mars ~0.25",
     "| Oxidized (ferric) dust / rust | ~0.2–0.3 |"),
    ("anorthosite / fresh rock",      0.15, 0.25, "lunar highlands, fresh exposures",
     "| Anorthosite / fresh rock | ~0.15–0.25 |"),
    ("tholin / dark-red organic ice", 0.05, 0.15, "Pholus-like weathered icy terrain",
     "| Tholin / dark-red organic ice | ~0.05–0.15 |"),
    ("basalt / mare regolith",        0.06, 0.12, "the Moon ~0.11",
     "| Basalt / mare regolith, space-weathered | ~0.06–0.12 |"),
    ("carbonaceous / C-type regolith", 0.02, 0.06, "darkest common surfaces",
     "| Carbonaceous / C-type regolith | ~0.02–0.06 |"),
)

#: 표면 유형 → Bond 알베도 밴드. 전부 `chosen=False` 다.
BOND_ALBEDO = {
    name: Band(None, lo, hi, f"{DOC}@«{anchor}»", "analog")
    for name, lo, hi, _analog, anchor in _ROWS
}
ANALOG = {name: analog for name, _lo, _hi, analog, _a in _ROWS}

_Q_SENTENCE = ("The phase integral `q` (≈ 1 for a Lambert surface; ~0.3–0.5 for dark back-scattering "
               "regolith like the Moon, ~0.7–1.3 for bright icy/cloud bodies with forward scattering)")

#: 위상적분 q — 문서는 표면 계열 **둘**에만 값을 인쇄한다. 나머지 여섯 행에는 q 가 없다.
#: `bundle="scattering"` 는 두 번째 경로(q·p)의 묶음 이름이다. 짝인 p 표가 아직 없어
#: `corners()` 로 걸을 대상이 지금은 하나뿐이고, 그 사실 자체가 아래에 기록된다.
PHASE_INTEGRAL = {
    "dark back-scattering regolith": Band(None, 0.3, 0.5, f"{DOC}@«{_Q_SENTENCE}»", "analog",
                                          bundle="scattering"),
    "bright icy or cloudy":          Band(None, 0.7, 1.3, f"{DOC}@«{_Q_SENTENCE}»", "analog",
                                          bundle="scattering"),
}

#: q·p 의 짝. §5 는 p 를 표면 유형별이 아니라 천체별로 분광 추정하므로 표가 없다.
GEOMETRIC_ALBEDO_GAP = ("no per-surface-type `p` table exists — §5 estimates the geometric albedo "
                        "spectrally per body, so the `scattering` bundle has one member here and "
                        "cannot be walked until the second one is built")


def t_eq_ratio(band: Band) -> float:
    """양끝이 T_eq 를 몇 배 움직이는가. T_eq ∝ (1 − A)^¼ 이라 항성과 거리에 무관하다."""
    return ((1.0 - band.low) / (1.0 - band.high)) ** 0.25


def contrast_ratio(band: Band) -> float:
    """양끝이 '얼마나 밝게 보이는가'를 몇 배 움직이는가."""
    return band.high / band.low


def main() -> int:
    print("표면 유형별 Bond 알베도 — 문서가 인쇄한 구간과, 양끝이 각각 무엇을 얼마나 움직이는가")
    print(f"{'표면 유형':<34}{'구간':>13}{'T_eq':>9}{'시각 대비':>11}")
    print("-" * 76)
    for name, band in BOND_ALBEDO.items():
        print(f"{name:<34}{f'{band.low}–{band.high}':>13}"
              f"{t_eq_ratio(band):>8.3f}×{contrast_ratio(band):>10.2f}×")
    print()
    print("두 축은 공통 단위가 없다 — 몇 켈빈이 대비 몇 배와 맞먹는지는 인쇄된 데가 없으므로 엔진은")
    print("둘 다 내고 순위를 매기지 않는다. 순위가 필요한 자리가 곧 오너 선택지다.")
    print()
    print("위상적분 q — 문서가 값을 인쇄한 표면 계열은 둘뿐이다")
    for name, band in PHASE_INTEGRAL.items():
        print(f"  {name:<32}{band.low}–{band.high}   (폭 {contrast_ratio(band):.2f}×)")
    print(f"  ⚠ {GEOMETRIC_ALBEDO_GAP}")
    print()
    print("여덟 행 모두 값이 비어 있다 — 문서는 구간만 인쇄했고, 그 안의 점을 고르는 것은 Collapse 다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
