# C55 1단계 테스트 — Xu+ 2021 이 인쇄한 Fe–S 부피 규칙 전사와, ρ₀ 가 없어 거절하는 자리 (브리프 178 B)
"""Anchors for the printed liquid Fe–S rules, and for the refusal that stands in for the density.

    python3 engine/test_fe_s.py        # the gate; ~0 s, this is arithmetic on two printed formulas

⚠ **This file's most important row is a refusal.** The owner decided to build a binary Fe–S material
first (C55, 2026-09-10), and Xu+ 2021 prints two of the three things a `Phase` needs — `K₀(X_S)` and
`K′(X_S)` — but **not `ρ₀(X_S)`** anywhere. Recovering it from Table 1's 7 GPa values by inverting their
eq. (3) would be *our* arithmetic, and this repository's rule is that a paper's printed derivation wins
over ours. So the material is **not built**, the attempt
refuses by name, and the reproduction anchors R4–R6 (the paper's own Fe–S density points) are registered
as **refusals** rather than as numbers.

⚠ **The first version of this file said the refusal would be filled when Table S1 arrived. The SI
arrived and that table does not exist**: what it holds is an end-member EOS and Margules coefficients,
because the paper's composition dependence is a non-ideal solution model rather than a
(ρ₀, K₀, K′) triple. So candidate B is not waiting on a document — it does not fit the `Phase` slot at
all, and the material that gets built is candidate A (Huang 2023, whose SI *does* print composition
derivatives at two Mars-core anchors).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos                                # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


print("① 인쇄된 두 규칙의 끝점 — 논문의 상수가 그대로 나오는가 (Xu+ 2021 §2.4)")
row(eos.xu_fes_k0_pa(0.0) == 76.0 * eos.GPA,
    f"X_S = 0 → K₀ = {eos.xu_fes_k0_pa(0.0) / eos.GPA:.1f} GPa · 인쇄 «K_Fe = 76 GPa»")
row(eos.xu_fes_k0_pa(1.0) == 1.6 * eos.GPA,
    f"X_S = 1 → K₀ = {eos.xu_fes_k0_pa(1.0) / eos.GPA:.1f} GPa · 인쇄 «K_S = 1.6 GPa»")
row(eos.xu_fes_k0p(0.0) == 6.5 and eos.xu_fes_k0p(1.0) == 9.5,
    f"K′ = 6.5 + 3·X_S → 끝점 {eos.xu_fes_k0p(0.0)} · {eos.xu_fes_k0p(1.0)} (인쇄 «K′_Fe = 6.5», 계수 3)")

mid = eos.xu_fes_k0_pa(0.30)
row(abs(mid - (76.0 ** 0.70) * (1.6 ** 0.30) * eos.GPA) < 1.0,
    f"X_S = 0.30 → K₀ = {mid / eos.GPA:.4f} GPa — 지수 혼합을 여기서 다시 계산한 값과 같다 "
    "(전사가 규칙이지 표가 아니라는 뜻)")

print("\n② 어휘가 실재한다 — 원자분율 밖은 거절한다")
for bad in (-0.01, 1.01):
    try:
        eos.xu_fes_k0_pa(bad)
        row(False, f"X_S = {bad} 가 통과했다")
    except ValueError as e:
        row("원자분율" in str(e), f"X_S = {bad} → 거절 «{str(e)[:44]}…»")

print("\n③ ⚠ 등록된 거절 — ρ₀ 가 인쇄되지 않아 재질을 짓지 않는다 (이것이 오늘의 기대 결과다)")
try:
    eos.iron_fes_phase(0.30)
    row(False, "상이 만들어졌다 — ρ₀ 없이 만들어졌다면 어딘가에서 수를 지어낸 것이다")
except eos.PhaseGap as e:
    msg = str(e)
    row("Table S1" in msg and "우리 산수" in msg,
        f"거절이 **무엇이 없는지** 이름을 댄다: Table S1 · 역산 금지 사유 — «{msg[:60]}…»")
    row("형식 불일치" in msg or "슬롯에 애초에 들어가지 않는다" in msg,
        "그리고 **기다림이 아니라 형식 불일치**라고 말한다 — SI 는 도착했고 그 표는 없었다")

print("\n④ 융해 바운드는 이미 있고, 19 GPa 는 등록된 공백이다 (Mori+ 2017)")
row(eos.iron_fes_eutectic_t_melt(19.0e9) is None,
    "19 GPa → None. 화성 CMB 압력대의 아래쪽이 Mori 의 기준점(21 GPa) 밖이라 **공백이 답이다**")
row(abs(eos.iron_fes_eutectic_t_melt(21.0e9) - 1348.0) < 1e-9,
    f"21 GPa → {eos.iron_fes_eutectic_t_melt(21.0e9):.1f} K (식 (1) 의 기준점 그대로)")
row("10–21 GPa" in eos.IRON_FES_GAP_REASON,
    "그 공백은 이름과 이유를 이미 갖고 있다 (`IRON_FES_GAP_REASON`) — 이 브리프가 만든 것이 아니다")

print("\n⑤ 기존 두 철은 손대지 않았다")
fp = eos.MATERIALS["fe_prem"].phases[0]
fe = eos.MATERIALS["fe_eps"].phases[0]
row(fp.rho0 == 7050.0 and fp.k0 == 201.0 * eos.GPA and fp.fit_state == "liquid",
    f"fe_prem ρ₀ {fp.rho0:.0f} · K₀ {fp.k0 / eos.GPA:.0f} GPa · {fp.fit_state} — 그대로")
row(fe.fit_state == "solid" and "fe_s" not in eos.MATERIALS,
    "fe_eps 도 그대로이고, **`fe_s` 는 아직 MATERIALS 에 없다** — 지어지지 않았다는 사실이 "
    "레지스트리에서도 참이다")

print("\n기록 — 재현 앵커 R4–R6 은 오늘 **거절**이 기대 결과다 (판정 아님)")
print("      Xu+ 2021 의 Fe–S 밀도점들과 대조하려면 ρ₀(X_S) 가 있어야 하는데, 그 논문은 그것을 표로")
print("      인쇄하지 않고 비이상 용액 모델의 출력으로 낸다 — 슬롯이 아니라 형식이 다르다.")
print("      순수 Fe 쪽 앵커(Huang+ 2023 의 19 GPa/2100 K ρ 8083 · K_T 156)는 **다른 기준점**에")
print("      놓여 있어 이 두 규칙(1 bar · 1900 K)과 직접 비교되지 않는다 — 비교하려면 둘 중 하나를")
print("      옮겨야 하고 그 옮김이 곧 우리 산수다. 그래서 여기서도 수로 만들지 않는다.")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
