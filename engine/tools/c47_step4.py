# C47 4단계 방향 시험 러너 — 09-07 복구 실행을 앵커로 재현하고 여섯 런을 인쇄한다
"""C47 step 4 — the Earth/Mars direction test, six runs per potential temperature.

    python3 engine/tools/c47_step4.py            # 여섯 런 × 두 T_p, 09-07 앵커 대조까지
    python3 engine/tools/c47_step4.py --quiet     # 앵커 대조 판정만

⚠ **This reproduces, it does not decide.** The pre-registration is `engine/interior-core.md` C47 (g) —
four verdict cells, eight fixed values, the target `q_Earth/q_Mars` = 3.68 / 4.78 from the no-melting
1.372, and the (a)(b)(c) decomposition. Nothing here elects a cell.

⚠ **The anchors below are the 09-07 work seat's own output**, recovered from that seat's transcript
(C47 (j)); the runner it came from was two inline `python3 -c` blocks and was never committed. Brief 162
commit 1 promotes that arithmetic **unchanged** — three known defects included — so that the numbers can
be reproduced before any of them is repaired. `engine/stagnant_lid.py@«이 절의 산수는 09-07 작업석의 두 번째 인라인 블록»`
carries the same warning beside the code.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import radiogenic as rg                # noqa: E402
import stagnant_lid as sl              # noqa: E402

T_P_CELSIUS = (1350.0, 1500.0)
ALPHAS = (("§3.2 3.7e-5", sl.ALPHA_SECTION_3_2), ("§4   2.0e-3", sl.ALPHA_SECTION_4_PRINTED))
RUNS = (("(a) dehydr only", 100.0, False), ("(b) buoyancy only", 1.0, True), ("(c) both", 100.0, True))

#: 09-07 실행 출력. `(q_E, q_M, ratio)` — 인쇄된 자리수 그대로 (q 는 mW/m², 소수 2자리; 비 4자리).
ANCHORS = {
    (1350.0, "§3.2 3.7e-5", "(a) dehydr only"): (52.02, 29.17, 1.7832),
    (1350.0, "§3.2 3.7e-5", "(b) buoyancy only"): (52.02, 35.90, 1.4492),
    (1350.0, "§3.2 3.7e-5", "(c) both"): (52.02, 29.17, 1.7832),
    (1350.0, "§4   2.0e-3", "(a) dehydr only"): (52.02, 29.17, 1.7832),
    (1350.0, "§4   2.0e-3", "(b) buoyancy only"): (52.04, 39.06, 1.3323),
    (1350.0, "§4   2.0e-3", "(c) both"): (52.02, 29.17, 1.7832),
    (1500.0, "§3.2 3.7e-5", "(a) dehydr only"): (51.04, 23.42, 2.1791),
    (1500.0, "§3.2 3.7e-5", "(b) buoyancy only"): (105.33, 77.74, 1.3549),
    (1500.0, "§3.2 3.7e-5", "(c) both"): (51.04, 22.79, 2.2396),
    (1500.0, "§4   2.0e-3", "(a) dehydr only"): (51.04, 23.42, 2.1791),
    (1500.0, "§4   2.0e-3", "(b) buoyancy only"): (120.93, 89.01, 1.3586),
    (1500.0, "§4   2.0e-3", "(c) both"): (51.04, 23.41, 2.1800),
}
#: 고갈층 두께 [km] 와 `z*_D` — 같은 실행의 인쇄값.
DEPLETED_ANCHORS = {(1350.0, "Earth"): (61.8, 0.9787), (1350.0, "Mars"): (163.8, 0.9090),
                    (1500.0, "Earth"): (108.2, 0.9627), (1500.0, "Mars"): (286.7, 0.8407)}
B_ANCHOR = 4.1921e10


def urey(body: str, q_w_m2: float) -> float:
    b = sl.STEP4_BODIES[body]
    area = 4.0 * math.pi * b["r_p"] ** 2
    heat = rg.budget(b["mass"] * (1.0 - b["cmf"]))["total_w"]
    return heat / (q_w_m2 * area)


def main() -> int:
    quiet = "--quiet" in sys.argv
    b_grain = sl.fit_b_eq30()
    fails = []
    if f"{b_grain:.4e}" != f"{B_ANCHOR:.4e}":
        fails.append(f"b {b_grain:.4e} ≠ 앵커 {B_ANCHOR:.4e}")
    if not quiet:
        print(f"b (하나의 전역 선언, 논문 자기 지구 조건 재적합) = {b_grain:.4e} · 앵커 {B_ANCHOR:.4e} "
              f"{'✓' if not fails else '✗'}")
        print("목표 q_E/q_M : 3.68 (우리 0.454) / 4.78 (Korenaga 0.35) · 무용융 기준선 1.372 — C47 (g)")
        # Ur 열의 분자는 앵커 표에 없다 — 추적 가능하게 함께 인쇄한다 (radiogenic.budget total_w).
        for body in ("Earth", "Mars"):
            bb = sl.STEP4_BODIES[body]
            print(f"    H_{body} = {rg.budget(bb['mass'] * (1.0 - bb['cmf']))['total_w']:.6e} W · "
                  f"A = {4.0 * math.pi * bb['r_p'] ** 2:.6e} m²")

    for t_p in T_P_CELSIUS:
        if not quiet:
            print(f"\n=== 공통 T_p = {t_p:.0f} °C = {t_p + 273.15:.2f} K, 천체별 조정 없음 ===")
        for body in ("Earth", "Mars"):
            z_d, depth = sl.z_d_from_solidus(sl.STEP4_BODIES[body]["g"], sl.STEP4_BODIES[body]["D"], t_p)
            a_km, a_z = DEPLETED_ANCHORS[(t_p, body)]
            ok = round(depth / 1e3, 1) == a_km and round(z_d, 4) == a_z
            if not ok:
                fails.append(f"{body} {t_p:.0f} 고갈층 {depth / 1e3:.1f} km/z {z_d:.4f} ≠ {a_km}/{a_z}")
            if not quiet:
                print(f"    {body:6s} 고갈층 {depth / 1e3:6.1f} km = 맨틀의 "
                      f"{(1 - z_d) * 100:5.2f} %   z*_D {z_d:.4f}  {'✓' if ok else '✗'}")
        for a_label, alpha in ALPHAS:
            for r_label, d_eta, buoy in RUNS:
                e = sl.step4_run("Earth", t_p, alpha, d_eta, buoy, b_grain)
                m = sl.step4_run("Mars", t_p, alpha, d_eta, buoy, b_grain)
                q_e, q_m = e["q_w_m2"] * 1e3, m["q_w_m2"] * 1e3
                ratio = e["q_w_m2"] / m["q_w_m2"]
                ur_e, ur_m = urey("Earth", e["q_w_m2"]), urey("Mars", m["q_w_m2"])
                a_qe, a_qm, a_r = ANCHORS[(t_p, a_label, r_label)]
                ok = (round(q_e, 2) == a_qe and round(q_m, 2) == a_qm and round(ratio, 4) == a_r)
                if not ok:
                    fails.append(f"{t_p:.0f} α {a_label} {r_label}: "
                                 f"{q_e:.2f}/{q_m:.2f}/{ratio:.4f} ≠ {a_qe}/{a_qm}/{a_r}")
                if not quiet:
                    print(f"    α {a_label} {r_label:18s} q_E {q_e:7.2f} q_M {q_m:7.2f} mW/m² · "
                          f"q_E/q_M {ratio:7.4f} · Ur_E {ur_e:6.3f} Ur_M {ur_m:6.3f} "
                          f"Ur_M/Ur_E {ur_m / ur_e:6.3f}  {'✓' if ok else '✗'}")

    n = len(ANCHORS) + len(DEPLETED_ANCHORS) + 1
    if fails:
        print(f"\n✗ 09-07 앵커 {len(fails)}/{n} 불일치 — 재현 실패, 진행 금지")
        for f in fails:
            print(f"    {f}")
        return 1
    print(f"\n✅ 09-07 앵커 {n}/{n} 일치 — 승격된 산수가 복구된 실행을 재현한다 (판정은 C47 (g) 의 칸)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
