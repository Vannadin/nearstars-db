# 바다 층 앵커 — 물 기둥이 밀도를 움직이는가, 경계가 격자에 매이는가, 3층을 역산하는가
"""The ocean block, moved out of `test_interior.py` so the gate has two steps instead of one.

    python3 engine/test_interior_ocean.py

⚠ **Nothing here is new.** The three checks below are the block that `test_interior.py` printed
under the heading «바다 — …» until `4e4b08af`, moved verbatim. It was **845 s of that file's
1 425 s** (59.3 %, measured solo on 2026-09-18), and while it sat in the same step no pool size
could take the gate under it.

⚠ **This file does not own its constants.** `ICY_T_POT` and `ICY_ANCHORS` still live in
`test_interior.py` and are imported here, because a second definition would drift silently —
the tests would stay green while the two files disagreed.
"""
from __future__ import annotations

import sys

import interior
from interior import EARTH_MASS_KG, EARTH_RADIUS_M, infer_three_layer, solve
from test_interior import ICY_ANCHORS, ICY_T_POT


def main() -> int:
    fails: list[str] = []

    print("\n바다 — 밀도를 실제로 움직이는가, 경계가 격자에 매이지 않는가, 3층을 역산하는가")
    # 유로파형 천체: 금속 핵 + 암석 + 물 기둥. 2026-08-29 전에는 표현할 수 없던 구조다.
    eur = dict(core_mass_fraction=0.12, ice_mass_fraction=0.10, potential_temperature=ICY_T_POT)
    m_eur = 4.7998e22 / EARTH_MASS_KG
    with_ocean = solve(m_eur, **eur)
    try:
        interior.OCEAN_LAYER = False
        solid = solve(m_eur, **eur)
    finally:
        interior.OCEAN_LAYER = True
    moved = abs(with_ocean.values["radius"] / solid.values["radius"] - 1.0)
    ok = with_ocean.values["ocean_thickness"] > 0.0 and moved > 1e-3
    if not ok:
        fails.append(f"바다가 밀도를 안 움직인다 — 반지름 변화 {moved:.1e}, "
                     f"바다 {with_ocean.values['ocean_thickness']:.0f} km. 배선이 끊겼다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 유로파형 (핵 0.12 · 얼음 0.10 · {ICY_T_POT:.0f} K): "
          f"바다 {with_ocean.values['ocean_thickness']:.0f} km · 껍질 "
          f"{with_ocean.values['ice_shell_thickness']:.0f} km · 반지름이 고체상 대비 "
          f"{(with_ocean.values['radius'] / solid.values['radius'] - 1) * 100:+.2f} % · "
          f"C/MR² {solid.values['nmoi']:.4f} → {with_ocean.values['nmoi']:.4f}")
    # 격자 위상. 상 경계를 걸음 안에서 보간하지 않으면 여기서 2e-3 이 나온다 (2026-08-29 측정).
    st, _ = interior.shoot(4.7998e22, 0.12, 0.10, "fe_prem", potential_temperature=ICY_T_POT)
    base = interior.STEPS
    got = []
    try:
        for n in (base - 1, base, base + 1):
            interior.STEPS = n
            g = interior.integrate(st.p_center, 4.7998e22, 0.12, 0.10, "fe_prem",
                                   t_center=st.t_center, t_pot=ICY_T_POT)
            got.append((g.mass_kg / 4.7998e22, g.radius_m / EARTH_RADIUS_M))
    finally:
        interior.STEPS = base
    span_m = max(x[0] for x in got) - min(x[0] for x in got)
    span_r = (max(x[1] for x in got) - min(x[1] for x in got)) / got[1][1]
    ok = span_m < 1e-5 and span_r < 1e-5
    if not ok:
        fails.append(f"바다 경계의 격자 위상: {base - 1}↔{base + 1} 걸음에서 겉질량 {span_m:.1e}, "
                     f"반지름 {span_r:.1e} — 상 경계가 걸음에 양자화됐다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 격자 위상 {base - 1} · {base} · {base + 1}: 겉질량 "
          f"{span_m:.1e} · 반지름 {span_r:.1e} (허용 1e-5)")
    # 3층 역산. 유로파의 발표 C/MR² 가 (핵, 얼음) 띠 안에 있고, 그것으로 좁히면 한 점이 나온다.
    # 기본 실행은 격자 두 점만 훑는다 — 넉 점은 `--icy` 가 낸다.
    eu = [a for a in ICY_ANCHORS if a[0] == "Europa"][0]
    band = infer_three_layer(eu[1] / EARTH_MASS_KG, eu[2] * 1e3 / EARTH_RADIUS_M, ICY_T_POT,
                             nmoi=eu[3], core_grid=(0.0, 0.30))
    if not band.applicable:
        fails.append(f"Europa 3층 역산이 거절했다 — {band.reason[:80]}")
        print(f"  [FAIL] Europa 3층 역산 거절: {band.reason[:80]}")
    else:
        inside = band.values["nmoi_low"] <= eu[3] <= band.values["nmoi_high"]
        narrowed = band.regime == "inferred_three_layer_by_nmoi"
        off = abs(band.values["nmoi"] - eu[3]) / eu[3] if narrowed else 1.0
        ok = inside and narrowed and off < 2e-3 and band.converged
        if not ok:
            fails.append(f"Europa 3층: 띠 {band.values['nmoi_low']:.4f}–{band.values['nmoi_high']:.4f}, "
                         f"발표 {eu[3]}, 좁힘 {narrowed}, 오차 {off:.1e}, converged {band.converged}")
        print(f"  [{'PASS' if ok else 'FAIL'}] Europa: 띠 C/MR² {band.values['nmoi_low']:.4f}–"
              f"{band.values['nmoi_high']:.4f} 가 발표값 {eu[3]} 을 담고, 그것으로 좁히면 핵 "
              f"{band.inputs.get('core_mass_fraction', float('nan')):.3f} · 얼음 "
              f"{band.inputs.get('ice_mass_fraction', float('nan')):.3f} · 바다 "
              f"{band.values.get('ocean_thickness', 0):.0f} km / 껍질 "
              f"{band.values.get('ice_shell_thickness', 0):.0f} km · converged {band.converged}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
