# 항성풍 세 값과 그것이 정하는 유도 자기권 경계 — 화성 적합을 그대로, 빌려 쓰는 자리에 이름을 붙여 (C-induced)
"""The stellar wind at a body, and the induced magnetosphere boundary it sets.

    python3 engine/stellar_wind.py

**Nothing here is a placeholder.** The three wind outputs reach real values by three different routes,
and the route is what their grade records:

- **`v_sw` is declared.** 400 km/s, the repository's single value for it
  (`phase3/stellar_wind_synthesis/context-notes.md`: *"stellar_wind_speed_kms = 400 (assumed, Wood)
  unless measured"*). An assumption, and saying so is more honest than calling it provisional.
- **`n_sw` is derived**, from spherical steady-state mass conservation `n = Ṁ / (4π r² v m̄)` — a
  textbook identity, and `Ṁ` is already carried per host. At the Sun's own values this returns
  **6.70 cm⁻³ at 1 AU**, inside the observed 5–7.
- **`p_ram` is wired**, not invented: `scripts/refs/magnetopause_geometry.py` already computes it as
  `2.0 nPa · Ṁ / a²` and two Proxima boards use it. ⚠ Deriving it instead from `n m_p v²` gives
  **1.79 nPa** at 1 AU against that 2.0 anchor — a 10 % gap between a board convention and the
  identity above. Recorded, not silently resolved; the boards are not touched here.

**The boundary is Ramstad+ 2017a's fit, carried whole.** Its IMB is a double conic in which only
`L_n` depends on the wind, and the subsolar point is four equations away from the printed table:

    L_n  = a·n^b·(v/100)^c + d          Table 2: 0.59, −0.30, −0.81, 0.49
    r_TD = √(L_n² + (ε_n²−1)x_Fn² + 2 ε_n L_n x_Fn)                       eq (7)
    ξ    = (1−ε_n²) x_Fn − ε_n L_n                                        eq (8)
    L_d  = √((1−ε_d²) r_TD² + ξ²)                                         eq (5)
    x_Fd = (ε_d L_d + ξ)/(1−ε_d²)                                         eq (6)
    r_SD = x_Fd + L_d/(1+ε_d)                                             eq (9)

⚠ **The velocity is in units of 100 km/s, not the km/s the paper prints** (`paper-defects.md` #20);
the conversion is written out in `_v100()` and checked in the test rather than done in passing. ⚠ Eq
(6) can be read two ways from the text and the other reading puts the boundary at 0.887 R_p, inside
the planet — recorded so the next reader does not have to rule it out again.

⚠ **`p_dyn` never enters.** The paper's short form takes a pressure, but the model that matters takes
`n` and `v` directly, so the question of whether our `p_ram` convention matches theirs does not arise
for this boundary. (It could not be settled from the paper anyway: proton-only and 5 %-helium
readings both reproduce the short form to within 1–3 %, proton-only slightly better.)

⚠ **This fit is Martian by construction.** `n_sw` and `v_sw` are its only variables; the neutral
atmosphere is absorbed into the fitted constants, which the paper states — those effects are
*"assumed to average out"*. Using it on any other body borrows Mars's atmosphere, and the paper gives
**no rule for carrying it elsewhere**, unlike Egan's `B_max ∝ P_sw^(1/2)` for the intrinsic side.

**Not yet a chain recipe.** `chain.yaml`'s `stellar_wind` node carries no `recipe:` document, so a
`## Contract` block has nowhere to live and `check_contracts` would fail the moment this registered.
Assigning that node a methodology document is a modelling decision, not a wiring one, and is left to
the owner rather than taken here.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

M_PROTON_KG = 1.6726219e-27
AU_M = 1.495978707e11
M_SUN_KG = 1.98892e30
YEAR_S = 3.155815e7
#: 태양 질량손실률 2e-14 M☉/yr — 교과서 값. 호스트별 Ṁ 은 이 배수로 들어온다.
MDOT_SUN_KG_S = 2e-14 * M_SUN_KG / YEAR_S
#: 레포 유일값. 측정치가 없으면 이 가정을 쓴다 (phase3/stellar_wind_synthesis/context-notes.md).
V_SW_ASSUMED_KMS = 400.0
#: 보드 관행의 1 AU 램압 앵커. 아래 항등식은 1.79 를 낸다 — 10 % 차이를 여기 적어 둔다.
P_RAM_BOARD_ANCHOR_1AU_NPA = 2.0

# ── Ramstad+ 2017a, Table 2 (IMB) ─────────────────────────────────────────
LN_A, LN_B, LN_C, LN_D = 0.59, -0.30, -0.81, 0.49
EPS_N, X_FN, EPS_D = 0.95, 1.64, 0.57
R_MARS_KM = 3390.0          # 논문의 공간 단위. 다른 천체에 쓰면 R_p 로 재해석하는 것이고, 그것이 "빌린다"는 그 단계다.
#: 이온권계면 고도 범위. **이 부등식에 넣지 않는다** — 다른 면이다. 금성 셋 + 화성 하나가 이 안에 든다.
IONOPAUSE_RANGE_R_P = (1.05, 1.2)


def _v100(v_kms: float) -> float:
    """논문이 km/s 라 인쇄하지만 적합 지수는 100 km/s 단위라야 맞는다 (paper-defects #20)."""
    return v_kms / 100.0


def number_density_cm3(mdot_rel_sun: float, a_au: float, v_kms: float = V_SW_ASSUMED_KMS) -> float:
    """n = Ṁ / (4π r² v m_p) — 구면 정상류 질량보존. 교과서 항등식이라 근거 문서가 따로 없다."""
    r = a_au * AU_M
    v = v_kms * 1e3
    n_si = mdot_rel_sun * MDOT_SUN_KG_S / (4.0 * math.pi * r * r * v * M_PROTON_KG)
    return n_si * 1e-6


def ram_pressure_npa(n_cm3: float, v_kms: float = V_SW_ASSUMED_KMS) -> float:
    """p = n m_p v². 양성자만 — 논문이 정의를 인쇄하지 않고, 축약형 대조로도 헬륨 포함 여부를 못 가른다."""
    return n_cm3 * 1e6 * M_PROTON_KG * (v_kms * 1e3) ** 2 * 1e9


def imb_subsolar_r_p(n_cm3: float, v_kms: float = V_SW_ASSUMED_KMS) -> float:
    """Ramstad+ 2017a 의 IMB 지하점 [R_p]. 식 (11)→(7)→(8)→(5)→(6)→(9)."""
    ln = LN_A * n_cm3 ** LN_B * _v100(v_kms) ** LN_C + LN_D
    r_td = math.sqrt(ln * ln + (EPS_N ** 2 - 1) * X_FN ** 2 + 2 * EPS_N * ln * X_FN)
    xi = (1 - EPS_N ** 2) * X_FN - EPS_N * ln
    l_d = math.sqrt((1 - EPS_D ** 2) * r_td * r_td + xi * xi)
    x_fd = (EPS_D * l_d + xi) / (1 - EPS_D ** 2)
    return x_fd + l_d / (1 + EPS_D)


def imb_subsolar_altitude_km(n_cm3: float, v_kms: float = V_SW_ASSUMED_KMS,
                             radius_km: float = R_MARS_KM) -> float:
    """고도 [km]. 두 논문이 인쇄하는 형태가 고도라서 인용은 이쪽으로 한다 —
    다만 판정 오차는 반지름 기준으로 읽어야 한다 (고도 3.3 % = 반지름 0.66 %)."""
    return (imb_subsolar_r_p(n_cm3, v_kms) - 1.0) * radius_km


def main() -> int:
    n1 = number_density_cm3(1.0, 1.0)
    print("태양 공칭 (Ṁ = 1 M☉ 단위, 1 AU, 400 km/s)")
    print(f"  n_sw    {n1:.2f} cm⁻³   (관측 5–7 안)")
    print(f"  p_ram   {ram_pressure_npa(n1):.2f} nPa   ⚠ 보드 관행 앵커 "
          f"{P_RAM_BOARD_ANCHOR_1AU_NPA} nPa 와 {abs(ram_pressure_npa(n1)/2.0-1)*100:.0f} % 차이")
    print("\n화성 궤도에서의 IMB (Ramstad 적합)")
    for n, v, label in ((2.0, 400.0, "공칭"), (0.3, 250.0, "극저압"), (12.0, 700.0, "극고압")):
        r = imb_subsolar_r_p(n, v)
        print(f"  {label:<6} n {n:>5} v {v:>5} → {r:.4f} R_p = {(r-1)*R_MARS_KM:>4.0f} km")
    r_nom = imb_subsolar_r_p(2.0, 400.0)
    print(f"\n  Egan/Trotignon 상수 847 km (1.2499 R_p) 와 비교 — 고도 "
          f"{abs((r_nom-1)*R_MARS_KM/847-1)*100:.1f} % · 반지름 {abs(r_nom/1.2499-1)*100:.2f} %")
    print(f"  이온권계면 범위 {IONOPAUSE_RANGE_R_P} 는 다른 면이라 이 부등식에 넣지 않는다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
