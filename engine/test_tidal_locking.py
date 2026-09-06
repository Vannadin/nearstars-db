# 조석 잠김 자기검증 — 문서 §2 표를 재현하려 시도하고, **재현되지 않는 자리를 고정한다**
"""Hold the despin recipe to the document, including where the document fails its own formula.

    python3 engine/test_tidal_locking.py

§2 prints τ_lock only as orders of magnitude, so item-by-item matching is impossible; the strongest
available test is **order of magnitude plus the yes/no**, and that is what runs here.

⚠ **The yes/no is nearly free.** For the Moon, Mercury and Io every `Q/k₂` in the printed class gives
the same verdict, so a green light there proves little. **Venus is where the test has any weight**, and
Venus is where the document and its own formula part company. That row is pinned, not smoothed.

The claim being pinned is stronger than "one row disagrees": **no single choice of `Q/k₂` and `ω₀`
reproduces the table**, because those constants are shared and therefore cancel out of the ratio
between two bodies. `τ(Venus)/τ(Moon)` is fixed by geometry and mass alone. Any order-unity factor
missing from the printed formula cancels the same way, so fetching the unheld sources cannot move it.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tidal_locking import (E_MERCURY_RESONANT, E_MOON_ONE_TO_ONE, STATE_RESONANCE,  # noqa: E402
                           STATE_SYNCHRONOUS, STATE_UNCLASSIFIED, despin_timescale_yr,
                           equilibrium_spin_ratio, rotation_state, solve)

M_EARTH = 5.9722e24
R_EARTH = 6.371e6
M_SUN_IN_EARTHS = 333030.0

# (라벨, mass_earth, radius_earth, a_km, perturber_M⊕, age_Gyr, e, 영구사중극, 관측 상태)
ANCHORS = (
    ("Moon",    0.0123, 0.2727, 3.844e5,  1.0,             4.5, 0.055,  False, STATE_SYNCHRONOUS),
    ("Mercury", 0.0553, 0.3829, 5.791e7,  M_SUN_IN_EARTHS, 4.5, 0.206,  True,  STATE_RESONANCE),
    ("Io",      0.0150, 0.2860, 4.217e5,  317.8,           4.5, 0.0041, False, STATE_SYNCHRONOUS),
)


def main() -> int:
    fails: list[str] = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    # 1. the three bodies the formula does get right, state and all
    for label, m, r, a_km, mp, age, e, quad, want_state in ANCHORS:
        res = solve(m, r, a_km, mp, age, e, permanent_quadrupole=quad)
        ok(res.values["locked"] is True, f"1: {label} is observed despun; got locked={res.values['locked']}")
        ok(res.values["rotation_state"] == want_state,
           f"1: {label} is observed in {want_state[:20]}…; got {res.values['rotation_state'][:40]}")

    # 2. ⚠ Venus: the printed formula and the printed class cannot despin it, while the literature
    # says the solid tide would. The defect is in the table's constants, not in the physics claim.
    venus = solve(0.815, 0.9499, 1.082e8, M_SUN_IN_EARTHS, 4.5, 0.007)
    ok(venus.values["locked"] is False,
       f"2: with the printed rocky class Venus does not despin — pinned because Leconte 2015 says "
       f"the solid tide would synchronise it, so this gap is the document's to close, not physics'. "
       f"got locked={venus.values['locked']}")
    ok(venus.values["t_lock_yr_min"] > 4.5e9,
       f"2: even the fast end must exceed the age; got {venus.values['t_lock_yr_min']:.3g} yr")

    # 3. ⚠ and no shared constant can fix it: the ratio is fixed by geometry and mass alone
    def tau(m, r, a_km, mp, qk):
        return despin_timescale_yr(m * M_EARTH, r * R_EARTH, 0.33, a_km * 1e3, mp * M_EARTH, qk)
    ratios = {qk: tau(0.815, 0.9499, 1.082e8, M_SUN_IN_EARTHS, qk) / tau(0.0123, 0.2727, 3.844e5, 1.0, qk)
              for qk in (1e1, 1e2, 1e3, 1e4)}
    spread = max(ratios.values()) / min(ratios.values())
    ok(abs(spread - 1.0) < 1e-9,
       f"3: τ(Venus)/τ(Moon) must not depend on Q/k₂ at all — that is why no constant fixes the "
       f"table; got a spread of {spread}")
    ratio = ratios[1e2]
    ok(6.0e3 < ratio < 7.5e3, f"3: the ratio is ~6.1e3; got {ratio:.3g}")
    for moon_tau in (1e7, 1e8):
        ok(moon_tau * ratio / 4.5e9 > 10.0,
           f"3: with the Moon at the document's {moon_tau:.0e} yr, Venus lands at "
           f"{moon_tau * ratio / 4.5e9:.0f}× the system age. Since the ratio is constant, the repair "
           f"cannot be a shared coefficient — it has to be a per-body Q/k₂, and §2's Venus cell is "
           f"the one that names no number")

    # 4. §4's boundary is not printed, so the anchors set it and the gap between them refuses
    ok(rotation_state(E_MOON_ONE_TO_ONE, False) == STATE_SYNCHRONOUS,
       "4: the Moon's own eccentricity must still read 1:1 — an earlier 0.01 threshold called the "
       "document's canonical 1:1 anchor pseudo-synchronous")
    ok(rotation_state(0.12, False) == STATE_UNCLASSIFIED,
       "4: between the two anchors the document prints nothing, so neither does this")
    ok(rotation_state(E_MERCURY_RESONANT, True) == STATE_RESONANCE,
       "4: at Mercury's eccentricity with a permanent quadrupole, the p:q class")

    # 5. Hut 1981's small-e limit, as the document states it
    ok(abs(equilibrium_spin_ratio(0.0) - 1.0) < 1e-12, "5: a circular orbit gives ω_eq = n")
    ok(abs(equilibrium_spin_ratio(0.05) - (1 + 6 * 0.05 ** 2)) < 1e-3,
       f"5: the document says ω_eq/n ≈ 1 + 6e² for small e; got {equilibrium_spin_ratio(0.05)}")

    # 6. a roster body, against a number the board already carries independently
    pandora = solve(0.6447, 0.8984, 252393.0, 120.0, 5.3, 0.0)
    ok(pandora.values["locked"] is True and pandora.values["rotation_state"] == STATE_SYNCHRONOUS,
       "6: Pandora sits deep inside the a⁶ gate")
    ok(abs(pandora.values["rotation_period_h"] - 32.0) < 0.5,
       f"6: synchronous rotation from the orbit gives 32 h, which is what the α Cen board already "
       f"declares for it; got {pandora.values['rotation_period_h']:.2f} h")

    # 7. the band decides, or nothing does
    straddle = solve(0.815, 0.9499, 1.082e8, M_SUN_IN_EARTHS, 50.0, 0.007)
    ok(straddle.values["locked"] is None and "cannot say" in straddle.reason,
       f"7: when the Q/k₂ band straddles the age the recipe must decline; got "
       f"{straddle.values['locked']}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 조석 잠김 — 앵커 셋 상태까지 일치(달 1:1 · 수성 p:q · 이오 1:1) · "
          f"⚠ 금성은 표와 어긋남을 고정(Leconte 는 고체조석이 동기화한다고 말한다 → 결함은 표의 상수 쪽) · 비 {ratio:.2g}× 가 Q/k₂ 에 불변 "
          f"→ 어떤 상수로도 §2 표 재현 불가 · §4 경계 미인쇄 구간 거절 · Hut 소극한 · "
          f"판도라 32 h(보드 선언과 독립 일치) · 밴드가 나이를 걸치면 판정 보류")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
