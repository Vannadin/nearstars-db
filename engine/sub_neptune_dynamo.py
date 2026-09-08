# 서브넵튠 철핵 다이나모의 두 게이트 — 맨틀 표면이 먼저고, 핵 전도도는 그 다음이다 (C23 · C32)
"""The two gates Tang+ 2025 puts on a sub-Neptune's iron-core dynamo, in the order the paper puts them.

    python3 engine/sub_neptune_dynamo.py

This module holds no recipe yet. It holds the **decision the owner has to make** and the evidence for
it, in the shape C32 gives such things, so that the branch which eventually judges a sub-Neptune's
dynamo does not re-derive any of it.

**Rm is not a gate.** The engine's own pre-registration (C23, 2026-09-04) worried about three things:
a 2.26× disagreement in RM22's electrical conductivity, a threshold printed as 40 in our ladder and
50 by Tang, and a velocity scaling from an unheld paper. Tang's own sentence closes all three:

    "as long as a convective layer is present in the liquid iron, Rm can readily exceed the critical
     value. Our numerical results show that Rm typically ranges from 10³ − 10⁵, well surpassing the
     critical threshold before Fconv drops below 10⁻³ erg cm⁻²"

Against 40 or 50 that is a margin of 20× to 2500×. Every one of the three worries lives inside it.

**Gate 1 is the mantle**, from the paper's abstract: *"dynamo action in sub-Neptune iron cores
persists as long as the mantle surface remains molten, often exceeding 10 Gyr, and becomes sensitive
to core thermal conductivity after solidification."* Figure 19 says it again in its caption. So the
question "does the iron core run a dynamo" is answered by the **silicate melting judgement**, not by
anything about the core.

**Gate 2 is `k_c`, and only after gate 1 has closed.** That makes it the first conditional `Choice`
in the engine: while the mantle surface is molten both candidates give a dynamo, and the pick is
inert. Once it solidifies the same pick turns the dynamo on or off — and on a low-mass, thin-envelope
sub-Neptune that is the difference between a body with aurorae and one without.

Anchors (C33) — the paper, not our summary of it:
  Tang+ 2025 `2025ApJ...989...28T` (cached PDF), abstract · Figure 19 caption · §Rm discussion
  the two conductivities are Konôpková+ 2016 `2016Natur.534...99K` and Pozzo+ 2012 `2012Natur.485..355P`,
  cited by Tang; neither is read here, so both are carried as "Tang attributes it to them"
  ⚠ 2026-09-09 (C49): 이 줄의 Konôpková 비브코드는 `2016ApJ...817..107K` 였고 **ADS 에서 아무것도
  아닙니다**(numFound 0). 실제 논문은 Nature 534, 99 — *"Direct measurement of thermal conductivity in
  solid iron"*, `2016Natur.534...99K`, ADS 인용 253회. 값(40 W/m/K)은 Tang 이 그렇게 돌린 것이므로
  바뀌지 않고, 가리키는 논문만 고쳤다
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import Band, Choice  # noqa: E402
from eos import silicate_melt_fraction, silicate_solidus  # noqa: E402

#: 게이트 1. 이 노드가 아니라 규산염 용융 판정이 답한다 — 그래서 여기엔 값이 아니라 이름만 있다.
MANTLE_GATE = ("the mantle surface is molten — while it is, the dynamo runs and `k_c` changes "
               "nothing; answered by the silicate melting judgement (eos.silicate_solidus), "
               "not by anything in the core")

# erg s⁻¹ cm⁻¹ K⁻¹ → W m⁻¹ K⁻¹ 는 10⁻⁷ J / 10⁻² m = ×10⁻⁵. 4e6 → 40, 1e7 → 100.
_ERG_CM_K_TO_W_M_K = 1e-5
# round: 1e7 × 1e-5 는 이진 부동소수점에서 100.00000000000001 이 된다. 논문이 인쇄한 것은 100 이고,
# 우리 산술의 찌꺼기를 유효숫자인 양 싣지 않는다.
K_C_LOW_W_M_K = round(4e6 * _ERG_CM_K_TO_W_M_K, 9)     # 40, Konôpková+ 2016 (Tang's solid lines)
K_C_HIGH_W_M_K = round(1e7 * _ERG_CM_K_TO_W_M_K, 9)    # 100, Pozzo+ 2012 (Tang's dashed lines)

#: 핵 열전도도. 양끝이 둘 다 인쇄돼 있고 각각 귀속돼 있다 — C32 가 밴드로 받는 조건 그대로다.
#: 값이 비어 있는 것은 아무도 고르지 않았기 때문이고, 중점을 채우는 것은 이 자리에서 특히 나쁘다:
#: 70 W/m/K 는 두 논문 중 어느 쪽도 말하지 않은 수다.
CORE_CONDUCTIVITY = Band(
    None, K_C_LOW_W_M_K, K_C_HIGH_W_M_K,
    "Tang+ 2025 tests both: 4e6 erg s⁻¹ cm⁻¹ K⁻¹ (Konôpková+ 2016, solid) and 1e7 (Pozzo+ 2012, "
    "dashed), i.e. 40 and 100 W m⁻¹ K⁻¹",
    "calibrated", estimates="core thermal conductivity")

CORE_CONDUCTIVITY_CHOICE = Choice(
    at="dynamo_sub_neptune",
    quantity="core thermal conductivity k_c [W m⁻¹ K⁻¹]",
    candidates=({"value": K_C_LOW_W_M_K, "end": "low", "grade": "calibrated",
                 "source": "Konôpková+ 2016, as Tang tests it (solid lines)"},
                {"value": K_C_HIGH_W_M_K, "end": "high", "grade": "calibrated",
                 "source": "Pozzo+ 2012, as Tang tests it (dashed lines); RM22 quotes the same 100"}),
    consequences={
        "does the dynamo run at all": "after the mantle surface solidifies the core's cooling rate "
                                      "drops sharply and convection weakens; the conductivity then "
                                      "decides whether what is left still drives a dynamo. On a "
                                      "low-mass, thin-envelope sub-Neptune this is on or off.",
        "what the body looks like": "a field or no field is aurorae or none, and it is the only "
                                    "visible consequence a reader of the board will ever notice.",
    },
    default=None,
    only_when="the mantle surface has solidified",
    note="no default: while gate 1 is open both candidates give a dynamo, so a default would be a "
         "pick nobody needs; once gate 1 closes the pick is load-bearing and belongs to the owner")


#: 게이트 1 이 "녹아 있다"로 읽는 최소 용융분율. 탱은 "the mantle surface remains molten" 이라고만
#: 적고 분율을 인쇄하지 않는다. 0 초과면 솔리더스 위라는 뜻이고, 그게 이 문장이 지지하는 전부다.
MOLTEN_FRACTION_FLOOR = 0.0


def mantle_surface_molten(pressure_pa: float, temperature_k: float,
                          variant: str = "peridotitic") -> tuple[bool | None, str]:
    """게이트 1. 맨틀 표면이 규산염 솔리더스 위인가.

    (판정, 이유) 를 돌려준다. 판정이 None 이면 이 압력에 곡선이 없다는 뜻이지 "안 녹았다"가 아니다 —
    둘을 같은 값으로 내면 소비처가 구별하지 못한다."""
    sol = silicate_solidus(pressure_pa, variant)
    if sol is None:
        return None, (f"규산염 솔리더스가 {pressure_pa / 1e9:.3g} GPa 에서 곡선을 갖지 않는다 "
                      f"(0–500 GPa 밖). 판정 없음이지 '고체'가 아니다.")
    phi = silicate_melt_fraction(pressure_pa, temperature_k, variant)
    molten = temperature_k > sol
    return molten, (f"맨틀 표면 {temperature_k:.0f} K vs 솔리더스 {sol:.0f} K "
                    f"({pressure_pa / 1e9:.3g} GPa) → 용융분율 "
                    f"{'없음' if phi is None else f'{phi:.2f}'}; "
                    f"{'액체' if molten else '고체'}")


def dynamo_verdict(pressure_pa: float, temperature_k: float,
                   k_c_w_m_k: float | None = None,
                   variant: str = "peridotitic") -> tuple[str, str]:
    """두 게이트를 순서대로 읽는다. Tang 의 문장이 정하는 순서 그대로다.

    `k_c` 는 게이트 1 이 닫힌 뒤에만 읽힌다. 고르지 않았으면 (None) 그 자리에서 판정을 멈추고
    선택지를 가리킨다 — 엔진이 대신 고르지 않는다 (C32)."""
    molten, why = mantle_surface_molten(pressure_pa, temperature_k, variant)
    if molten is None:
        return "undetermined", why
    if molten:
        return "dynamo", (f"{why} — 맨틀 표면이 녹아 있는 한 다이나모는 돈다. "
                          f"핵 전도도는 이 가지에서 아무것도 바꾸지 않는다.")
    if k_c_w_m_k is None:
        return "choice required", (
            f"{why} — 게이트 1 이 닫혔으므로 이제 핵 전도도가 판정을 가른다. "
            f"{CORE_CONDUCTIVITY_CHOICE.quantity} 가 아직 선택되지 않았다 "
            f"(후보 {K_C_LOW_W_M_K:.0f} / {K_C_HIGH_W_M_K:.0f}).")
    return "conductivity-dependent", (
        f"{why} — 고화 후이므로 판정은 선택된 k_c = {k_c_w_m_k:g} W/m/K 위에 선다. "
        f"⚠ Tang 은 이 가지에서 '전도도 선택에 민감해진다'까지만 말하고 켜짐/꺼짐 문턱을 인쇄하지 않는다.")


def main() -> int:
    print("서브넵튠 철핵 다이나모 — 게이트는 둘, 순서가 있다\n")
    print("  게이트 1 (맨틀):", MANTLE_GATE)
    print("    → 열려 있는 동안 다이나모는 돌고, 아래 선택은 아무것도 바꾸지 않는다.\n")
    c = CORE_CONDUCTIVITY_CHOICE
    print(f"  게이트 2 (핵 전도도) — 조건부: {c.only_when}")
    for cand in c.candidates:
        print(f"    {cand['value']:>5.0f} W/m/K  ({cand['end']:<4}) {cand['source']}")
    print(f"    밴드 {CORE_CONDUCTIVITY.low}–{CORE_CONDUCTIVITY.high}, 고른 점 없음 "
          f"(중점 {CORE_CONDUCTIVITY.middle():.0f} 은 두 논문 중 어느 쪽도 말하지 않는 수다)")
    for axis, what in c.consequences.items():
        print(f"    · {axis}: {what}")
    print(f"\n  Rm 은 게이트가 아니다 — 10³–10⁵ 로 문턱(40~50)의 20~2500배다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
