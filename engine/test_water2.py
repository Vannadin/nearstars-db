# 조밀한 액체 물 표(water2) 검사 — 유효 천장이 지켜지는가, 두 이음매가 얼마인가, 거절이 이름을 대는가
"""Checks for `water2_table.py` and the `h2o_liquid_dense` material.

    python3 engine/test_water2.py

SeaFreeze is not available on system Python, so the transcription itself is checked by the
generator (`tools/make_water2_table.py`, which records its interpolation errors in the
module). What this file checks with what the engine has:

1. **The ragged ceiling** — every isotherm's baked cells are physical (ρ rising with P,
   c_P in the liquid range, dT/dP|_S positive), and the material refuses above the ceiling
   naming Brown 2018 / water2, and below 0.1 GPa, and outside 360–1100 K.
2. **Seam water1 ↔ water2**, from the two baked tables over the overlap they share
   (0.1–2.3 GPa × 360–500 K), compared with what the generator measured on the splines.
3. **Seam water2 ↔ Mazevet+ 2019** along the hot-water fit's floor, 1000 K, over the
   pressures the table reaches there — measured and printed; the number goes into the C3
   revisited line. No tolerance is asserted on it: it is a finding, not a gate.
4. The material's c_P and ∇_ad are finite and positive across the band the ice-shell moons
   walk (2.3–10 GPa × 500–1000 K).
"""
from __future__ import annotations

import math
import sys

import water2_table as w2
import water_table as w1
import water_hot as wh
from eos import MATERIALS, PhaseGap


def main() -> int:
    fails: list[str] = []

    def check(ok: bool, label: str) -> None:
        if not ok:
            fails.append(label)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("들쭉날쭉한 천장 — 굳힌 칸이 전부 물리적인가")
    bad = 0
    for i, (row_r, row_d, row_c) in enumerate(zip(w2.RHO, w2.DTDP_S, w2.C_P)):
        n = w2.KEEP[i]
        if len(row_r) != n or len(row_d) != n or len(row_c) != n:
            bad += 1
            continue
        if any(b <= a for a, b in zip(row_r, row_r[1:])):
            bad += 1
        if any(not (1000.0 < c < 15000.0) for c in row_c) or any(d <= 0.0 for d in row_d):
            bad += 1
    check(bad == 0, f"{w2.NT} 등온선 × KEEP 칸: ρ 단조증가, 1000 < c_P < 15000 J/kg/K, dT/dP|_S > 0 (어긋난 등온선 {bad})")
    ceil = {t: w2.p_ceiling(float(t)) / 1e9 for t in (360, 400, 500, 600, 700, 800, 900, 1000, 1100)}
    check(all(ceil[a] <= ceil[b] for a, b in zip(sorted(ceil), sorted(ceil)[1:])),
          "천장이 온도에 단조: " + " · ".join(f"{t} K {c:.1f} GPa" for t, c in ceil.items()))
    check(abs(w2.P_MIN_PA - 0.1e9) < 1.0 and w2.T_LO_K == 360.0 and w2.T_MAX_K == 1100.0,
          f"창 0.1 GPa–천장 × {w2.T_LO_K:.0f}–{w2.T_MAX_K:.0f} K, 가장 뜨거운 천장 {w2.P_MAX_PA / 1e9:.1f} GPa")
    check(w2.INTERP_BAND_RHO < 1e-4 and w2.INTERP_BAND_DTDP < 1e-3 and w2.INTERP_WINDOW_RHO < 1e-3,
          f"생성기가 잰 보간 오차: 띠(2.3–10 GPa × 500–1000 K) ρ {w2.INTERP_BAND_RHO:.1e} · dT/dP {w2.INTERP_BAND_DTDP:.1e}; "
          f"창 전체 ρ {w2.INTERP_WINDOW_RHO:.1e}")

    print("\n거절 — 이름을 대는가")
    d = MATERIALS["h2o_liquid_dense"]
    for p_gpa, t, why, cold in ((15.0, 700.0, "700 K 천장(13 GPa) 위", True), (0.05, 600.0, "0.1 GPa 아래 (too_cold: 더 뜨거우면 Mazevet)", True),
                                (3.0, 300.0, "360 K 아래", True), (3.0, 1200.0, "1100 K 위", False)):
        try:
            d.density(p_gpa * 1e9, t)
            check(False, f"{why}: 거절해야 한다")
        except PhaseGap as e:
            named = ("water2" in e.reason or "Brown 2018" in e.reason) or "표" in e.reason
            check(named and (cold is None or e.too_cold == cold), f"{why}: too_cold={e.too_cold} — '{e.reason[:70]}…'")
    check(d.in_domain(3e9, 700.0) and not d.in_domain(15e9, 700.0) and MATERIALS["h2o_liquid_dense"] is d,
          "in_domain 이 천장을 알고, MATERIALS 에 등록")

    print("\n이음매 1 — water1 ↔ water2, 두 굳힌 표에서 (0.1–2.3 GPa × 360–500 K)")
    worst_r, worst_d, where = 0.0, 0.0, ("", "")
    lp = -1.0
    while lp <= math.log10(2.29):
        p = 10.0 ** lp * 1e9
        for t in range(360, 501, 10):
            if not (w1.in_domain(p, float(t)) and w2.in_domain(p, float(t))):
                continue
            er = abs(w2.density(p, float(t)) / w1.density(p, float(t)) - 1.0)
            ed = abs(w2.dtdp_adiabat(p, float(t)) / w1.dtdp_adiabat(p, float(t)) - 1.0)
            if er > worst_r:
                worst_r, where = er, (f"{p / 1e9:.2f} GPa · {t} K", where[1])
            if ed > worst_d:
                worst_d, where = ed, (where[0], f"{p / 1e9:.2f} GPa · {t} K")
        lp += 0.04
    check(worst_r < 2.0e-3 and abs(worst_r - w2.SEAM_W1_RHO_BAKED) < 1.0e-3,
          f"ρ 최악 {worst_r * 100:.2f} % at {where[0]} (생성기가 스플라인에서 잰 {w2.SEAM_W1_RHO_BAKED * 100:.2f} %)")
    check(worst_d < 0.15,
          f"dT/dP|_S 최악 {worst_d * 100:.1f} % at {where[1]} (생성기 {w2.SEAM_W1_DTDP_BAKED * 100:.1f} %) — 밀도보다 훨씬 크다, 두 표현의 α/(ρc_P) 가 갈린다")
    print(f"  (바다 자리 252–360 K 는 이 표 밖이고 생성기가 스플라인에서 직접 쟀다: water2 가 water1 과 1 % 안에 드는 것은 "
          f"240 K 에서 0.63 GPa 까지, 330 K 에서 2.0 GPa 까지뿐 — 그 위는 스플라인이 비물리적, 최악 ρ {w2.SEAM_W1_RHO_OCEAN * 100:.0f} %)")

    print("\n이음매 2 — water2 ↔ Mazevet+ 2019, 1000 K (뜨거운 물의 바닥)에서")
    t = 1000.0
    p = 2.3e9
    rows = []
    while p <= w2.p_ceiling(t):
        r2, rh = w2.density(p, t), wh.density(p, t)
        rows.append((p / 1e9, r2, rh, rh / r2 - 1.0))
        p *= 1.5
    seam_worst = max(abs(x[3]) for x in rows)
    for p_gpa, r2, rh, dv in rows:
        print(f"    {p_gpa:6.2f} GPa: water2 {r2:6.0f} · Mazevet {rh:6.0f} · Mazevet/water2 − 1 = {dv * 100:+.2f} %")
    check(all(math.isfinite(x[3]) for x in rows),
          f"1000 K 이음매: Mazevet 이 water2 보다 {min(x[3] for x in rows) * 100:+.1f} … {max(x[3] for x in rows) * 100:+.1f} % "
          f"(2.3 GPa 부터 {rows[-1][0]:.1f} GPa 까지, 최악 {seam_worst * 100:.1f} %) — 기록, 판정 없음")

    print("\n재료 — 띠 안에서 c_P 와 ∇_ad")
    ok = True
    for p_gpa in (2.5, 4.0, 6.0, 8.0, 10.0):
        for t in (520.0, 700.0, 900.0):
            if not w2.in_domain(p_gpa * 1e9, t):
                continue
            c, g = d.c_p(p_gpa * 1e9, t), d.grad_ad(p_gpa * 1e9, t)
            ok = ok and math.isfinite(c) and c > 0.0 and 0.0 < g < 1.0
    check(ok, "2.5–10 GPa × 520–900 K 에서 c_P > 0, 0 < ∇_ad < 1")

    print()
    if fails:
        print(f"FAIL: {len(fails)}")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
