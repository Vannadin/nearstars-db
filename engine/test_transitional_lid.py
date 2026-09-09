# C51 커밋 C 테스트 — F&B 2014 전이 법칙 전사가 인쇄된 상수·지수·폐합과 맞는지 (판정 칸 없음)
"""Anchors for the transitional-regime transcription (`transitional_lid.py`, C51 commit C).

    python3 engine/test_transitional_lid.py      # the gate; ~0 s

⚠ **No verdict cell is read here and no body is evaluated.** The law's inputs are non-dimensional
quantities of Foley & Bercovici 2014's own models and this engine declares none of them. What this
file checks is that the transcription matches what the paper prints, and it measures two things the
paper leaves as prose: how much its own rounding of its own exponents is worth, and how far apart its
three `(m, p)` rows put the same answer.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transitional_lid as tl          # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# Fig. 13's own axis ranges, so nothing here is evaluated outside what the paper plotted.
RA_GRID = (1e5, 1e6, 1e7, 1e8)                 # panel A: Ra' T'_i spans 10⁵–10⁸
MU_GRID = (1e3, 1e5, 1e7, 1e9)                 # panel C: μ'_l spans 10³–10⁹
DAMAGE_GRID = (1e-4, 1e-2, 1e0, 1e2, 1e4)      # panel B: D/(H h'_l) spans 10⁻⁴–10⁴
L_PRIME = 2.0                                  # inside the printed ≈1.5–4


def physical_grid(m=2, p=4):
    """Closed solutions inside the plotted ranges, keeping only physically usable ones."""
    out = []
    for ra in RA_GRID:
        for mu in MU_GRID:
            for dmg in DAMAGE_GRID:
                r = tl.close_t_i(L_PRIME, mu, 1.0, dmg, dmg, ra, m=m, p=p)
                if "refused" in r or not (0.05 < r["t_i"] < 0.99) or r["delta_l"] >= 0.5:
                    continue
                out.append((ra, mu, dmg, r))
    return out


print("① Table 1 세 행 — 인쇄된 자릿수 그대로")
row(tl.TABLE1[(2, 4)] == {"c5": 20.0, "beta_ra": -0.6603, "beta_d": -0.3151, "beta_mu": 0.2484, "beta_l": 0.1071}
    and tl.TABLE1[(3, 4)]["c5"] == 86.0 and tl.TABLE1[(3, 5)]["c5"] == 11.0,
    "(2,4) C₅ 20 · (3,4) 86 · (3,5) 11 — 지수 넷도 인쇄 자릿수대로")
betas_l = [tl.TABLE1[k]["beta_l"] for k in ((2, 4), (3, 4), (3, 5))]
c5s = [tl.TABLE1[k]["c5"] for k in ((2, 4), (3, 4), (3, 5))]
row(min(betas_l) < 0.0 < max(betas_l) and max(c5s) / min(c5s) > 7.0,
    f"⚠ β_L 이 세 행에서 부호를 바꾼다 ({betas_l[0]:+.4f} · {betas_l[1]:+.4f} · {betas_l[2]:+.4f}) 고 "
    f"C₅ 는 {min(c5s):.0f}–{max(c5s):.0f} 로 {max(c5s)/min(c5s):.1f}배 벌어진다 — «판 길이가 어떻게 "
    "들어가는가» 에 원전이 단일한 답을 주지 않는다")

print("\n② 식 (60) 은 식 (54) 의 지수를 반올림한 것이다 — 둘을 나란히 두고 차이를 잰다")
same = tl.nu_eq60(L_PRIME, 1e5, 1e2, 1e6, 0.9)
via54 = 0.9 / tl.delta_l(L_PRIME, 1e5, 1e2, 1e6, 0.9, constants=dict(tl.EQ60_ROUNDED, c5=20.0))
row(abs(same - via54) / same < 1e-12,
    f"반올림 지수를 식 (54) 에 넣으면 식 (60) 이 정확히 나온다 ({same:.6f} = {via54:.6f}) — 같은 식이 맞다")
grid = physical_grid()
ratios = [tl.rounded_vs_fitted(L_PRIME, mu, dmg, ra, r["t_i"])["ratio"] for ra, mu, dmg, r in grid]
row(len(grid) >= 30 and min(ratios) > 0.0,
    f"인쇄된 축 범위 안 물리적 조합 {len(grid)}개에서 반올림/적합 Nu 비 "
    f"**{min(ratios):.3f}–{max(ratios):.3f}** (최대 {max(abs(min(ratios)-1), abs(max(ratios)-1))*100:.1f} % 차) "
    "— 논문이 자기 지수를 반올림한 값어치다")

print("\n③ 폐합 식 (59) — 위·아래 경계층 열류가 실제로 맞는가")
ok_all = True
for ra, mu, dmg, r in grid[:8]:
    lhs = r["t_i"] / r["delta_l"]
    rhs = (1.0 - r["t_i"]) / r["delta_m"]
    ok_all = ok_all and abs(lhs - rhs) / lhs < 1.0e-9
row(ok_all, f"T'_i/δ'_l = (1−T'_i)/δ'_m 이 {min(8, len(grid))}개 표본에서 상대 10⁻⁹ 안 (이분 40회 안팎)")
t_is = [r["t_i"] for _, _, _, r in grid]
print(f"      기록: 이 격자에서 T'_i {min(t_is):.3f}–{max(t_is):.3f}, δ'_l {min(r['delta_l'] for _,_,_,r in grid):.4f}–"
      f"{max(r['delta_l'] for _,_,_,r in grid):.4f}, Nu {min(r['nu'] for _,_,_,r in grid):.2f}–{max(r['nu'] for _,_,_,r in grid):.1f}.")

print("\n④ (m, p) 를 바꾸면 같은 입력이 얼마나 다른 답을 내는가 — 오너 선택지 (b) 의 크기")
base = physical_grid(2, 4)
pick = base[len(base) // 2]
ra, mu, dmg, _ = pick
per_mp = {}
for m, p in ((2, 4), (3, 4), (3, 5)):
    r = tl.close_t_i(L_PRIME, mu, 1.0, dmg, dmg, ra, m=m, p=p)
    per_mp[(m, p)] = r
    if "refused" not in r:
        print(f"      (m,p) {(m, p)}: T'_i {r['t_i']:.4f} · δ'_l {r['delta_l']:.4f} · Nu {r['nu']:.2f}")
nus = [r["nu"] for r in per_mp.values() if "refused" not in r]
row(len(nus) == 3,
    f"Ra' {ra:.0e} · μ'_l {mu:.0e} · D/(H h'_l) {dmg:.0e} 한 점에서 세 행이 Nu "
    f"**{min(nus):.2f}–{max(nus):.1f}** ({max(nus)/min(nus):.1f}배) — 밴드로 나르는 이유")

print("\n⑤ 바디 경로는 없다 — 이름을 대며 거절한다")
r = tl.solve_on_body()
row("refused" in r and len(r["missing"]) == 7 and "L'" in r["missing"][0],
    f"거절: 비차원 입력 {len(r['missing'])}개 전부 이 엔진에 값이 없다 — «{r['refused'][:64]}…»")

print("\n기록 — 원전이 자기에 대해 말하는 것 (판정 아님)")
print(f"      · C₆ = {tl.C6} (식 (16) 과의 극한 일치로 정함) · Ra_c ≈ {tl.RA_CRIT:.0f} (free-slip) · "
      f"L′ ≈ {tl.L_PRIME_RANGE[0]}–{tl.L_PRIME_RANGE[1]} (종횡비 4×1 → 16×1)")
print(f"      · §8.1 의 지구 맨틀 퍼텐셜 온도 **{tl.T_M0_EARTH_K:.0f} K** — 우리 선언 1600, Foley/Korenaga 1623 에 이어 셋째 값이다")
print(f"      · E_h = {tl.E_H_J_MOL/1e3:.0f} kJ/mol (§8.1, 결정성장 실험)")
print("      · ⚠ 원전의 주장: 전이는 **점진적**이고 «plate-tectonics lying within the transitional regime», "
      "금성도 «transitional regime, close to the fully-stagnant lid» 다.")
print("        우리 바디는 `stagnant_lid: true/false` 로 선언한다 — 이 원전이 지구도 금성도 그렇게 "
      "기술되지 않는다고 말하는 이분값이다. 이름만 붙이고 고치지 않는다.")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
