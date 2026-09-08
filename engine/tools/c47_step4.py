# C47 4단계 방향 시험 러너 — 09-07 복구 실행을 앵커로 재현하고 여섯 런을 인쇄한다
"""C47 step 4 — the Earth/Mars direction test, six runs per potential temperature.

    python3 engine/tools/c47_step4.py            # 여섯 런 × 두 T_p, 09-07 기준값과의 차까지
    python3 engine/tools/c47_step4.py --anchors   # 09-07 재현을 **요구**한다 (어긋나면 rc=1)
    python3 engine/tools/c47_step4.py --quiet     # 표 없이 판정만

⚠ **`--anchors` 는 `aea75984` 에서만 통과한다.** 그 커밋이 09-07 산수를 결함까지 그대로 승격한
지점이고, 이후 커밋들은 결함을 하나씩 고치므로 숫자가 **움직여야 한다.** 그래서 기본 모드는
09-07 값과의 차를 인쇄하고 `rc=0` 으로 끝난다 — 앵커를 커밋마다 갱신하면 그것은 앵커가 아니다.

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


#: 커밋 6 — 천체별 선언 `T_p`. 값은 바디 파일에서 읽는다(타이핑하지 않는다), 단위는 K.
BODY_FILES = {"Earth": "earth.yaml", "Mars": "mars.yaml"}


def declared_t_p_k(body: str) -> float:
    """바디 파일의 `potential_temperature` [K]. `engine/bodies/<body>.yaml` 이 유일한 출처."""
    import yaml
    path = Path(__file__).resolve().parent.parent / "bodies" / BODY_FILES[body]
    return float(yaml.safe_load(path.read_text(encoding="utf-8"))["inputs"]["potential_temperature"])


def urey(body: str, q_w_m2: float) -> float:
    b = sl.STEP4_BODIES[body]
    area = 4.0 * math.pi * b["r_p"] ** 2
    heat = rg.budget(b["mass"] * (1.0 - b["cmf"]))["total_w"]
    return heat / (q_w_m2 * area)


def main() -> int:
    quiet = "--quiet" in sys.argv
    strict = "--anchors" in sys.argv
    # 커밋 4: α 는 Ra_i 에도 들어가고, b 는 **같은 α 로** 적합된다 (자기일관). 그래서 α 는 b 에
    # 흡수되고 두 α 의 결과가 소수 전부까지 같다 — 그 사실이 아래 표에서 확인된다.
    b_by_alpha = {label: sl.fit_b_eq30(alpha) for label, alpha in ALPHAS}
    b_grain = b_by_alpha[ALPHAS[1][0]]      # §4 = 논문 인쇄값 α 로 적합한 b, 앵커 대조용
    fails = []
    if f"{b_grain:.4e}" != f"{B_ANCHOR:.4e}":
        fails.append(f"b {b_grain:.4e} ≠ 앵커 {B_ANCHOR:.4e}")
    if not quiet:
        for label, alpha in ALPHAS:
            print(f"b (α {label} 로 적합, 하나의 전역 선언) = {b_by_alpha[label]:.6e}")
        r_b = b_by_alpha[ALPHAS[0][0]] / b_by_alpha[ALPHAS[1][0]]
        r_a = ALPHAS[0][1] / ALPHAS[1][1]
        print(f"    b 비 {r_b:.6e} 대 α 비 {r_a:.6e} → "
              f"{'α 가 b 에 흡수된다 (Ra_i 동일)' if abs(r_b / r_a - 1) < 1e-6 else '⚠ 흡수되지 않는다'}")
        print(f"    앵커 대조는 §4 쪽 b: {b_grain:.4e} · 앵커 {B_ANCHOR:.4e} {'✓' if not fails else '✗'}")
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
                b_a = b_by_alpha[a_label]
                e = sl.step4_run("Earth", t_p, alpha, d_eta, buoy, b_a)
                m = sl.step4_run("Mars", t_p, alpha, d_eta, buoy, b_a)
                q_e, q_m = e["q_w_m2"] * 1e3, m["q_w_m2"] * 1e3
                ratio = e["q_w_m2"] / m["q_w_m2"]
                ur_e, ur_m = urey("Earth", e["q_w_m2"]), urey("Mars", m["q_w_m2"])
                a_qe, a_qm, a_r = ANCHORS[(t_p, a_label, r_label)]
                ok = (round(q_e, 2) == a_qe and round(q_m, 2) == a_qm and round(ratio, 4) == a_r)
                if not ok:
                    fails.append(f"{t_p:.0f} α {a_label} {r_label}: "
                                 f"{q_e:.2f}/{q_m:.2f}/{ratio:.4f} ≠ {a_qe}/{a_qm}/{a_r}")
                if not quiet:
                    mark = ("✓" if ok else
                            f"Δ q_E {q_e - a_qe:+.2f} · q_M {q_m - a_qm:+.2f} · 비 {ratio - a_r:+.4f}")
                    print(f"    α {a_label} {r_label:18s} q_E {q_e:7.2f} q_M {q_m:7.2f} mW/m² · "
                          f"q_E/q_M {ratio:7.4f} · Ur_E {ur_e:6.3f} Ur_M {ur_m:6.3f} "
                          f"Ur_M/Ur_E {ur_m / ur_e:6.3f}  {mark}")

    # ── 커밋 6 — 천체별 선언 T_p 로 한 벌 더. ⚠ 러너는 T_p 를 °C 로 받고 선언은 K 이다.
    if not quiet:
        tp_k = {b: declared_t_p_k(b) for b in ("Earth", "Mars")}
        print(f"\n=== 천체별 선언 T_p — 지구 {tp_k['Earth']:.1f} K · 화성 {tp_k['Mars']:.1f} K "
              f"(= {tp_k['Earth'] - 273.15:.2f} · {tp_k['Mars'] - 273.15:.2f} °C) ===")
        if abs(tp_k["Earth"] - tp_k["Mars"]) < 1e-9:
            print("    ⚠ 지금 두 선언이 같은 값이라 이 벌은 공통 T_p 케이스와 같다 — 화성이 지구값을"
                  " 이전받았기 때문이고(0단계 통과, 오너 2026-09-08 17:52), 물리적 우연이 아니다.")
        for body in ("Earth", "Mars"):
            z_d, depth = sl.z_d_from_solidus(sl.STEP4_BODIES[body]["g"], sl.STEP4_BODIES[body]["D"],
                                             tp_k[body] - 273.15)
            print(f"    {body:6s} 고갈층 {depth / 1e3:6.1f} km = 맨틀의 {(1 - z_d) * 100:5.2f} %   "
                  f"z*_D {z_d:.4f}")
        for a_label, alpha in ALPHAS:
            for r_label, d_eta, buoy in RUNS:
                b_a = b_by_alpha[a_label]
                e = sl.step4_run("Earth", tp_k["Earth"] - 273.15, alpha, d_eta, buoy, b_a)
                m = sl.step4_run("Mars", tp_k["Mars"] - 273.15, alpha, d_eta, buoy, b_a)
                if not (e["eq56_converged"] and m["eq56_converged"]):
                    fails.append(f"천체별 α {a_label} {r_label}: eq. 56 미수렴")
                ratio = e["q_w_m2"] / m["q_w_m2"]
                ur_e, ur_m = urey("Earth", e["q_w_m2"]), urey("Mars", m["q_w_m2"])
                print(f"    α {a_label} {r_label:18s} q_E {e['q_w_m2'] * 1e3:7.2f} "
                      f"q_M {m['q_w_m2'] * 1e3:7.2f} mW/m² · q_E/q_M {ratio:7.4f} · "
                      f"Ur_E {ur_e:6.3f} Ur_M {ur_m:6.3f} Ur_M/Ur_E {ur_m / ur_e:6.3f} · "
                      f"목표 3.68 의 {ratio / 3.68 * 100:4.1f} % · 4.78 의 {ratio / 4.78 * 100:4.1f} %")

    n = len(ANCHORS) + len(DEPLETED_ANCHORS) + 1
    if fails:
        head = "✗ 09-07 앵커" if strict else "· 09-07 기준값과 다른 칸"
        print(f"\n{head} {len(fails)}/{n}" + (" — 재현 실패, 진행 금지" if strict else " (결함 수정의 효과)"))
        for f in fails:
            print(f"    {f}")
        return 1 if strict else 0
    print(f"\n✅ 09-07 앵커 {n}/{n} 일치 — 승격된 산수가 복구된 실행을 재현한다 (판정은 C47 (g) 의 칸)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
