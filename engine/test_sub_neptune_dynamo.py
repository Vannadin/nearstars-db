# 서브넵튠 다이나모 두 게이트 자기검증 — 단위 환산 · 조건부 선택지 · 중점을 안 고른다는 사실
"""Hold the sub-Neptune dynamo decision to Tang's printed numbers and to C32's rules.

    python3 engine/test_sub_neptune_dynamo.py

1. **The unit conversion is checked, not assumed.** Tang prints erg s⁻¹ cm⁻¹ K⁻¹; the board and the
   engine speak W m⁻¹ K⁻¹. The factor is written out here so a silent conversion cannot drift.
2. **The choice is conditional and says so.** Outside its condition both candidates give a dynamo, so
   it is not the same object as a choice with no consequence, which C32 refuses as a question.
3. **No point is chosen inside the band, and the midpoint is not a candidate.** 70 W/m/K is a number
   neither paper reports; it exists only as arithmetic between two other papers' results.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sub_neptune_dynamo import (CORE_CONDUCTIVITY, CORE_CONDUCTIVITY_CHOICE,  # noqa: E402
                                K_C_HIGH_W_M_K, K_C_LOW_W_M_K, dynamo_verdict,
                                mantle_surface_molten)


def main() -> int:
    fails: list[str] = []

    # 1. erg s⁻¹ cm⁻¹ K⁻¹ → W m⁻¹ K⁻¹  is  ×1e-7 J / 1e-2 m  =  ×1e-5
    for printed_erg, expected_w, who in ((4e6, 40.0, "Konôpková+ 2016"), (1e7, 100.0, "Pozzo+ 2012")):
        got = round(printed_erg * 1e-5, 9)
        if got != expected_w:
            fails.append(f"1: {who}: {printed_erg:g} erg s⁻¹ cm⁻¹ K⁻¹ is {expected_w} W/m/K, got {got}")
    if (K_C_LOW_W_M_K, K_C_HIGH_W_M_K) != (40.0, 100.0):
        fails.append(f"1: the module carries {(K_C_LOW_W_M_K, K_C_HIGH_W_M_K)}, not the printed pair")

    # 2. conditional, with the condition stated in words
    c = CORE_CONDUCTIVITY_CHOICE
    if not c.conditional:
        fails.append("2: this choice is inert while the mantle surface is molten and must say so")
    if "solidif" not in c.only_when:
        fails.append(f"2: the condition must name mantle-surface solidification, got {c.only_when!r}")
    if c.default is not None:
        fails.append("2: no default belongs here — outside the condition a default is a pick nobody "
                     "needs, and inside it the pick is the owner's")

    # 3. nobody has chosen, and the midpoint is not one of the candidates
    if CORE_CONDUCTIVITY.chosen:
        fails.append("3: a point was chosen inside the band that no paper reports")
    mid = CORE_CONDUCTIVITY.middle()
    if any(abs(cand["value"] - mid) < 1e-9 for cand in c.candidates):
        fails.append(f"3: the midpoint {mid} is being offered as if a paper printed it")
    if {cand["value"] for cand in c.candidates} != {40.0, 100.0}:
        fails.append("3: the candidates are the two printed ends, nothing between them")

    # 4. the two gates are read in Tang's order, and gate 1 does not consult k_c
    molten, _ = mantle_surface_molten(25e9, 3000.0)
    solid, _ = mantle_surface_molten(25e9, 1200.0)
    if not (molten is True and solid is False):
        fails.append(f"4: gate 1 is the silicate solidus; got molten={molten}, solid={solid}")
    if dynamo_verdict(25e9, 3000.0)[0] != "dynamo":
        fails.append("4: while the mantle surface is molten the dynamo runs with no k_c at all")
    if dynamo_verdict(25e9, 3000.0, 40.0)[0] != dynamo_verdict(25e9, 3000.0, 100.0)[0]:
        fails.append("4: on the molten branch the two candidates must give the same answer, or the "
                     "choice is not conditional after all")
    if dynamo_verdict(25e9, 1200.0)[0] != "choice required":
        fails.append("4: once gate 1 closes and nobody has picked k_c, the engine must stop and say so")

    # 5. no curve is not the same answer as solid — a consumer has to be able to tell them apart
    off_curve, why = mantle_surface_molten(900e9, 3000.0)
    if off_curve is not None or "판정 없음" not in why:
        fails.append(f"5: above the solidus curve's range the verdict is absent, not 'solid': {why}")
    if dynamo_verdict(900e9, 3000.0)[0] != "undetermined":
        fails.append("5: an absent curve must not be reported as a dynamo verdict")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 서브넵튠 다이나모 — 단위 환산 확인(4e6·1e7 erg → {K_C_LOW_W_M_K:.0f}·"
          f"{K_C_HIGH_W_M_K:.0f} W/m/K) · 조건부 선택지(맨틀 고화 후에만) · 기본값 없음 · "
          f"고른 점 없음(중점 {mid:.0f} 은 후보 아님) · 게이트 순서(융해→k_c) · 곡선 없음≠고체")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
