# 항성풍·IMB 자기검증 — "배선이 흐른다"와 "답이 맞다"를 이름으로 갈라 둔다
"""Two different claims, kept apart on purpose.

    python3 engine/test_stellar_wind.py

**wiring** — the pipe carries a number from Ṁ and a distance through to a boundary altitude, and the
number is not absurd. Passing says the plumbing is connected. It does **not** say the answer is right
for that body.

**answer** — the result agrees with an independently published value. Only Mars has one here: Egan
cites Trotignon's 847 km and Ramstad's fit gives 819 km. Venus gets a wiring check only, because
nothing we hold prints a Venus IMB subsolar altitude — Edberg publishes tail parameters and not the
dayside radius. If the two checks shared a name, a Venus pass would read as evidence that the Martian
fit transfers, which is exactly the claim nobody has tested.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stellar_wind import (IONOPAUSE_RANGE_R_P, P_RAM_BOARD_ANCHOR_1AU_NPA, R_MARS_KM,  # noqa: E402
                          imb_subsolar_altitude_km, imb_subsolar_r_p, number_density_cm3,
                          ram_pressure_npa, _v100)


def main() -> int:
    fails: list[str] = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    # ── unit conversion, written out rather than trusted (paper-defects #20)
    ok(_v100(400.0) == 4.0, "unit: the fit takes 100 km/s units; 400 km/s is 4.0")
    printed_kms = 0.59 * 2.0 ** -0.30 * 400.0 ** -0.81 + 0.49
    correct = 0.59 * 2.0 ** -0.30 * 4.0 ** -0.81 + 0.49
    ok(abs(correct - 0.6459) < 1e-4 and abs(printed_kms - 0.4937) < 1e-4,
       f"unit: L_n is 0.6459 in 100 km/s units and 0.4937 if the printed km/s is taken ({correct}, {printed_kms})")
    short_form = 0.13 * 0.535 ** -0.30 + 0.49          # the paper's own eq (13) check
    ok(abs(correct / short_form - 1) < 0.01,
       f"unit: the 100 km/s reading must agree with the paper's short form, got {correct} vs {short_form}")

    # ── answer: Mars, against a value published by someone else
    r = imb_subsolar_r_p(2.0, 400.0)
    ok(abs(r - 1.2417) < 5e-4, f"answer(Mars): the printed equations give 1.2417 R_p, got {r:.4f}")
    alt = imb_subsolar_altitude_km(2.0, 400.0)
    ok(abs(alt - 819) < 2, f"answer(Mars): 819 km subsolar altitude, got {alt:.0f}")
    ok(abs(alt / 847.0 - 1) < 0.04 and abs(r / 1.2499 - 1) < 0.01,
       "answer(Mars): must meet Egan/Trotignon's 847 km within 3.3 % in altitude and 0.66 % in radius")

    # the rejected reading of eq (6) puts the boundary inside the planet — kept as a guard
    ln = 0.59 * 2.0 ** -0.30 * 4.0 ** -0.81 + 0.49
    r_td = math.sqrt(ln * ln + (0.95 ** 2 - 1) * 1.64 ** 2 + 2 * 0.95 * ln * 1.64)
    xi = (1 - 0.95 ** 2) * 1.64 - 0.95 * ln
    l_d = math.sqrt((1 - 0.57 ** 2) * r_td * r_td + xi * xi)
    rejected = (0.57 * l_d + xi / (1 - 0.57 ** 2)) + l_d / 1.57
    ok(rejected < 1.0, f"eq(6): the other reading must land inside the planet and be excluded, got {rejected:.3f}")

    # ── wiring: the pipe carries Ṁ and a distance through to a boundary
    n_sun = number_density_cm3(1.0, 1.0)
    ok(5.0 <= n_sun <= 7.0, f"wiring(Sun): 1 AU density should land in the observed 5–7 cm⁻³, got {n_sun:.2f}")
    p_sun = ram_pressure_npa(n_sun)
    ok(abs(p_sun / P_RAM_BOARD_ANCHOR_1AU_NPA - 1) < 0.15,
       f"wiring(Sun): the identity should reproduce the board's 2.0 nPa anchor to ~10 %, got {p_sun:.2f}")

    n_mars = number_density_cm3(1.0, 1.524)
    ok(2.0 <= n_mars <= 4.0, f"wiring(Mars): 1.52 AU density, got {n_mars:.2f} cm⁻³")
    alt_mars = imb_subsolar_altitude_km(n_mars, 400.0)
    ok(400.0 <= alt_mars <= 1200.0,
       f"wiring(Mars): the derived density must carry through to a plausible altitude, got {alt_mars:.0f} km")

    n_venus = number_density_cm3(1.0, 0.723)
    r_venus = imb_subsolar_r_p(n_venus, 400.0)
    ok(1.0 < r_venus < 1.5,
       f"wiring(Venus): the pipe carries a boundary for Venus's wind too, got {r_venus:.3f} R_p")
    # ⚠ and no answer check for Venus: nothing we hold prints its subsolar IMB altitude.

    # ── the ionopause range is a different quantity and stays out of this inequality
    ok(IONOPAUSE_RANGE_R_P[1] < 1.2417,
       "surface: the ionopause range must sit below the IMB, or the two have been confused again")
    for measured in (1.0545, 1.1157, 1.1652, 1.089):     # Venus ×3 (Brace), Mars (Vignes)
        ok(IONOPAUSE_RANGE_R_P[0] <= measured <= IONOPAUSE_RANGE_R_P[1],
           f"surface: {measured} is an ionopause measurement and must fall inside {IONOPAUSE_RANGE_R_P}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 항성풍·IMB — 단위 환산 드러냄(400 km/s → 4.0, 인쇄대로면 0.4937) · "
          f"answer(화성) {alt:.0f} km 대 Egan 847(고도 3.3 % · 반지름 0.66 %) · 식(6) 다른 읽기 배제 · "
          f"wiring(태양 {n_sun:.2f} cm⁻³ · {p_sun:.2f} nPa · 화성 · 금성) · 이온권계면 넷 전부 범위 안")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
