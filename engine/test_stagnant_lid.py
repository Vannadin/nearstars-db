# 정체뚜껑 스케일링 앵커 — Korenaga 2009 Table 2 행별 대조·eq. 44 임계값·eq. 30 이 eq. 29 의 극한임 (C47 (f))
"""Anchor the Korenaga 2009 stagnant-lid transcription on the rows the paper prints.

    python3 engine/test_stagnant_lid.py

1. **Table 2 의 Δη=1 블록 10행** — eq. 29 가 인쇄된 `Nu` 를 rms 3 % 안에서 재현할 것. 논문이
   자기 적합 rms 를 ~1.2 % 라 적지만 그건 **Table 1** 에 대한 것이고, Table 2 는 적합에 안
   쓰인 집합이다. 편향이 0 근처일 것도 함께 지킨다.
2. ⚠ **`a_rh` 를 다시 맞춰도 안 나아진다** — 2.5 → 2.256 으로 재적합해 얻는 것이 0.1 %p 뿐이니
   잔차는 조정할 자리가 아니다. 이 시험이 그 사실을 박는다(맞추려는 유혹을 막는 자리).
3. **eq. 30 은 eq. 29 의 `Nu ≫ 1` 극한** — Ra_i 를 올리면 둘이 수렴할 것. C47 (c) 가 eq. 30 으로
   방향 시험을 돌렸고, Table 2 의 Nu 3–7 은 그 극한이 아니다.
4. **eq. 44** 가 본문의 ~450 (n=1) · ~104 (n=3) 을 주고, ⚠ **n=2 는 7 % 어긋난다**(143 대 ~134).
5. **공짜 교차검사** — Nimmo+ 2004 의 `ζ = 10⁻²` 가 `ΔT = 1350 K` 에서 주는 `θ = 13.5` 가
   Table 2 의 `θ` 범위 7.93–16.05 안에 들 것. 독립 전사된 두 모듈이 같은 뜻의 수에서 일치한다.
"""
from __future__ import annotations

import math
import sys

import mantle_flux as mf
import stagnant_lid as sl

fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def main() -> int:
    # ── 1. Table 2 행별 ────────────────────────────────────────────────────────
    rms = sl.table2_rms()
    errs = [r[3] for r in sl.table2_residuals()]
    bias = sum(errs) / len(errs)
    ok(len(sl.TABLE2_DETA1) == 10, f"1: Table 2 Δη=1 블록은 10행이다; {len(sl.TABLE2_DETA1)}행")
    ok(rms < 3.0, f"1: eq. 29 가 Table 2 를 rms 3 % 안에서 재현해야 한다 — {rms:.2f} %")
    ok(abs(bias) < 1.0, f"1: 편향이 ±1 %p 안이어야 한다 (계통 오차가 아니라 흩어짐) — {bias:+.2f} %p")
    ok(max(abs(e) for e in errs) < 5.0,
       f"1: 최악 행이 5 % 안이어야 한다 — {max(abs(e) for e in errs):.2f} %")

    # ── 2. a_rh 재적합은 얻는 게 없다 ─────────────────────────────────────────
    best = min((sl.table2_rms(x / 1000.0), x / 1000.0) for x in range(1500, 3501, 5))
    ok(rms - best[0] < 0.5,
       f"2: ⚠ `a_rh` 재적합이 rms 를 0.5 %p 넘게 개선하면 잔차가 조정 가능하다는 뜻이고, 그러면 "
       f"본문의 단일값을 쓸 근거가 흔들린다 — 2.5 에서 {rms:.2f} %, 최적 {best[1]:.3f} 에서 "
       f"{best[0]:.2f} %")

    # ── 3. eq. 30 은 eq. 29 의 극한 ───────────────────────────────────────────
    near = sl.nu_preasymptotic(12.0, 4.4e6) / sl.nu_asymptotic(12.0, 4.4e6)
    far = sl.nu_preasymptotic(12.0, 4.4e14) / sl.nu_asymptotic(12.0, 4.4e14)
    ok(abs(far - 1.0) < abs(near - 1.0) and abs(far - 1.0) < 0.05,
       f"3: Ra_i 를 올리면 eq. 29 가 eq. 30 으로 수렴해야 한다 — Table 2 규모에서 {near:.3f}, "
       f"10⁸배에서 {far:.3f}. ⚠ Table 2 의 Nu 3–7 은 점근이 아니고, C47 (c) 는 그 점근형으로 "
       f"방향 시험을 돌렸다")
    ok(near > 1.20,
       f"3: Table 2 규모에서 두 식이 20 % 넘게 갈려야 한다 (그래서 eq. 30 으로는 못 잰다) — {near:.3f}")

    # ── 4. eq. 44 ─────────────────────────────────────────────────────────────
    ok(abs(sl.ra_crit(1) / 450.0 - 1) < 0.05, f"4: Ra_crit(1) ~450; {sl.ra_crit(1):.0f}")
    ok(abs(sl.ra_crit(3) / 104.0 - 1) < 0.07, f"4: Ra_crit(3) ~104; {sl.ra_crit(3):.0f}")
    ok(abs(sl.ra_crit(2) / 134.0 - 1) > 0.05,
       f"4: ⚠ n=2 의 7 % 불일치는 **기록된 사실**이다 — 이 시험은 그것이 사라지면 알려 준다 "
       f"(식 143 대 본문 ~134); 지금 {sl.ra_crit(2):.0f}")

    # ── 5. 두 논문의 θ 가 만난다 ───────────────────────────────────────────────
    theta_nimmo = mf.ZETA * 1350.0
    thetas = [t for t, _r, _n in sl.TABLE2_DETA1]
    ok(min(thetas) <= theta_nimmo <= max(thetas),
       f"5: Nimmo ζ={mf.ZETA:g} 가 ΔT=1350 에서 주는 θ={theta_nimmo:.2f} 가 Korenaga Table 2 의 "
       f"θ 범위 {min(thetas):.2f}–{max(thetas):.2f} 안에 들어야 한다 — 독립 전사된 두 모듈의 "
       f"무료 정합 검사")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 정체뚜껑 스케일링 — Korenaga 2009 Table 2 Δη=1 10행 eq. 29 대조 rms "
              f"{rms:.2f} % (편향 {bias:+.2f} %p, 최악 {max(abs(e) for e in errs):.2f} %) · "
              f"a_rh 재적합 이득 {rms - best[0]:.2f} %p 뿐 · eq. 30 은 극한(Table 2 규모 {near:.3f} → "
              f"10⁸배 {far:.3f}) · Ra_crit 441/143/98 (n=2 ⚠ 7 % 차 기록) · Nimmo θ "
              f"{theta_nimmo:.2f} 가 Table 2 범위 안")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
