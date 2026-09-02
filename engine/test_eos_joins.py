# 밀도 적합과 녹는곡선이 같은 조성·같은 물질상을 말하는지 — Phase 의 join/fit_state 선언 게이트 (브리프 41)
"""Gate: every phase that carries a melting curve declares what its density fit describes.

    python3 engine/test_eos_joins.py

Two clauses, same shape (engine/eos-join-context-notes.md):
1. **join** — the composition the density fit describes must be declared, and where it differs
   from the composition the melting curve was measured on (`eos.MELT_CURVE_JOIN`), the phase
   must say how it bridges them (`join_note`). Fe–Fe₃S eutectic beside an FeS density is the
   trap; MgSiO₃ densities under a mantle-rock solidus is the bridge that already exists.
2. **fit_state** — which side of the melting curve the fit was measured on, solid or liquid.
   fe_prem (PREM outer core) is the liquid member core_state answers liquid verdicts with;
   fe_eps is the solid. Pinned, so the pair cannot silently swap.

A phase without a melting curve (antigorite) is not asked clause 1; it may still declare.
"""
from __future__ import annotations

import sys

import eos


def main() -> int:
    fails: list[str] = []
    checked = bridged = 0
    for mat in eos.MATERIALS.values():
        for ph in getattr(mat, "phases", ()):
            if not isinstance(ph, eos.Phase):
                continue
            if ph.fit_state and ph.fit_state not in eos.FIT_STATES:
                fails.append(f"{mat.name}/{ph.name}: fit_state {ph.fit_state!r} 는 {eos.FIT_STATES} 밖")
            if not ph.has_melt:
                continue
            checked += 1
            if ph.melt not in eos.MELT_CURVE_JOIN:
                fails.append(f"{mat.name}/{ph.name}: melt {ph.melt!r} 의 조성이 MELT_CURVE_JOIN 에 없다")
                continue
            if not ph.join:
                fails.append(f"{mat.name}/{ph.name}: 녹는곡선({ph.melt})이 있는데 밀도 적합의 join 이 선언되지 않았다")
            if not ph.fit_state:
                fails.append(f"{mat.name}/{ph.name}: 녹는곡선이 있는데 fit_state(solid|liquid)가 선언되지 않았다")
            curve = eos.MELT_CURVE_JOIN[ph.melt]
            if ph.join and ph.join != curve:
                bridged += 1
                if not ph.join_note:
                    fails.append(f"{mat.name}/{ph.name}: 밀도 join {ph.join!r} ≠ 곡선 조성 {curve!r} 인데 "
                                 "join_note 가 없다 — 다른 조인을 말없이 이어 붙였다")
    # clause 2 pinned on the iron pair core_state relies on
    fe_prem, fe_eps = eos.MATERIALS["fe_prem"].phases[0], eos.MATERIALS["fe_eps"].phases[0]
    if fe_prem.fit_state != "liquid":
        fails.append(f"fe_prem 은 PREM 외핵 **액체** 적합인데 fit_state={fe_prem.fit_state!r}")
    if fe_eps.fit_state != "solid":
        fails.append(f"fe_eps 는 순수 ε-철 **고체** 적합인데 fit_state={fe_eps.fit_state!r}")
    if abs(fe_prem.melt_scale - eos.IRON_LIGHT_ELEMENT_FACTOR) > 1e-12 or not fe_prem.join_note:
        fails.append("fe_prem 의 합금 다리(melt_scale + join_note)가 풀렸다")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 조인/물질상 선언 — 녹는곡선 있는 상 {checked}개 전부 join·fit_state 선언, "
              f"곡선과 다른 조인 {bridged}개는 모두 join_note 를 싣는다 (fe_prem 액체 · fe_eps 고체 고정)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
