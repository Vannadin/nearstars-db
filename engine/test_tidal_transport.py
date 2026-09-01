# 조석 수송 축을 이오 검증 사건에 고정한다 — 재현 실패의 측정과 역산 상수의 폐합이 앵커
"""Anchor the tidal transport axis on what the Io validation actually measured.

    python3 engine/test_tidal_transport.py

앵커는 우리가 바란 출력이 아니라 **측정된 사건**이다 (Brief 35, 분기 ③+④).
1. 전사 폐합 — 솔버는 인쇄된 (36)+(38)을 기계 잔차까지 푼다 (F_m+F_c=HD 항등 포함).
2. 재현 실패의 측정 불변량 — 자연 독법(Karato&Wu A, Schubert α, Table 5 H)에서
   이오는 사전등록 허용오차(±21 K, ±1.9 km; 커밋 e719b5d7이 실행보다 먼저) 밖에
   앉는다. 이 값들이 움직이면 이야기가 바뀐 것이니 크게 울려야 한다.
3. 역산 폐합 — (1471 K, 12.6 km)이 근이 되는 유일한 상수쌍(비물리)은 실제로
   그 점에 착지한다. 분석 전체의 비트 앵커.
4. 라벨 규율 — 도출/선언 라벨, 안정성 라벨, 검증-실패 라벨이 항상 실려 나온다.
"""
from __future__ import annotations

import sys

import tidal_transport as tt


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. 전사 폐합: 근에서 잔차와 에너지 폐합이 기계 수준 ─────────────────
    p = dict(tt.IO_TABLE5)
    roots = tt.all_roots(p, tt.A_KARATO_WET)
    ok(len(roots) == 1, f"1: 자연 독법(습윤)에서 근이 {len(roots)}개 — 1개였다")
    if roots:
        T_i, d = roots[0]
        rA, rB, aux = tt.residuals(p, tt.A_KARATO_WET, T_i, d)
        HD = p['H'] * p['D']
        ok(abs(rA) < 1e-9 * HD and abs(rB) < 1e-7,
           f"1: 근의 잔차가 기계 수준이 아니다 (rA={rA:.2e}, rB={rB:.2e})")
        ok(abs(aux['F_m'] + aux['F_c'] - HD) < 1e-9 * HD,
           "1: F_m + F_c = HD 폐합 위반 — eq. 22·23·28이 깨졌다")

    # ── 2. 재현 실패의 측정 불변량 (사전등록 허용오차 밖) ────────────────────
    # 측정값 2026-09-01: (A_wet, H=3e-6) → (1586.7 K, 495.7 km); (A_dry) → (1592.4, 519.4).
    for A, expT, expD, name in [(tt.A_KARATO_WET, 1586.7, 495.7e3, "습윤"),
                                (tt.A_KARATO_DRY, 1592.4, 519.4e3, "건조")]:
        r = tt.all_roots(p, A)
        ok(len(r) == 1, f"2: {name} A에서 근 {len(r)}개")
        if not r:
            continue
        T_i, d = r[0]
        ok(abs(T_i - expT) < 0.5 and abs(d - expD) < 0.5e3,
           f"2: {name} 측정값 이동 — ({T_i:.1f} K, {d/1e3:.1f} km), "
           f"기록값 ({expT}, {expD/1e3}). 솔버나 상수가 움직였다 — 추적할 것")
        ok(abs(T_i - tt.IO_PRINTED_T) > tt.IO_TOL_T,
           f"2: {name} T_i가 허용오차 안으로 들어왔다 — 재현 실패 서사가 뒤집혔다. 멈추고 보고")
        ok(abs(d - tt.IO_PRINTED_DELTA) > tt.IO_TOL_DELTA,
           f"2: {name} δ가 허용오차 안으로 들어왔다 — 재현 실패 서사가 뒤집혔다. 멈추고 보고")

    # ── 3. 역산 폐합: 비물리 상수쌍에서 인쇄값에 정확히 착지 ─────────────────
    p2 = dict(tt.IO_TABLE5, alpha=tt.RECOVERED_ALPHA, H=tt.RECOVERED_H)
    r = tt.all_roots(p2, tt.RECOVERED_A)
    ok(len(r) >= 1, "3: 역산 상수에서 근이 없다")
    if r:
        T_i, d = min(r, key=lambda x: abs(x[1] - tt.IO_PRINTED_DELTA))
        ok(abs(T_i - tt.IO_PRINTED_T) < 0.05 and abs(d - tt.IO_PRINTED_DELTA) < 5.0,
           f"3: 역산 폐합 실패 — ({T_i:.2f} K, {d/1e3:.3f} km) ≠ (1471, 12.6)")
    ok(tt.RECOVERED_ALPHA < 3.0e-5 / 10.0,
       "3: 역산 α가 암석값의 1/10 안으로 들어왔다 — '비물리' 판정 재검토 필요")

    # ── 4. 라벨 규율 ─────────────────────────────────────────────────────────
    res = tt.transport_result(3.0, 1.8216e6)  # 이오급 입력
    ok(res['validation']['status'] == "failed-io-reproduction",
       "4: 검증-실패 라벨이 빠졌다")
    ok(res['mode']['provenance'] == "declared", "4: 수송 모드가 선언으로 라벨되지 않았다")
    if res['internal_temperature'] is not None:
        ok(res['internal_temperature']['provenance'] == "derived-from-Edot",
           "4: 내부 온도가 도출값으로 라벨되지 않았다")
    ok(tt.stability_label("andrade")['label'] == "stable",
       "4: Andrade 안정성 라벨이 stable이 아니다")
    ok(tt.stability_label("maxwell+convection")['label'] == "conditionally-stable",
       "4: Maxwell+대류 라벨이 conditionally-stable이 아니다")
    try:
        tt.stability_label("burgers")
        fails.append("4: 미등록 유변 조합이 조용히 통과했다")
    except ValueError:
        pass
    dpt = tt.derive_potential_temperature(3.0, 1.8216e6)
    ok("derived-from-Edot" in dpt['provenance'],
       "4: derive_potential_temperature가 도출/선언 구별을 말하지 않는다")
    ok(dpt['validation']['status'] == "failed-io-reproduction",
       "4: 도출 potential_temperature에 검증-실패 라벨이 안 실렸다")

    if fails:
        print(f"test_tidal_transport: FAIL {len(fails)}")
        for f in fails:
            print("  -", f)
        return 1
    print("test_tidal_transport: OK (전사 폐합·재현 실패 불변량·역산 폐합·라벨 규율)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
