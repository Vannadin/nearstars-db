# C47 4단계 방향 시험 러너 — 09-07 복구 실행(앵커)과 현재 커밋의 기대표(회귀)를 둘 다 대조한다
"""C47 step 4 — the Earth/Mars direction test, six runs per potential temperature.

    python3 engine/tools/c47_step4.py            # 표 + **현재 기대표** 대조 (어긋나면 rc=1) — 게이트가 이것을 돈다
    python3 engine/tools/c47_step4.py --anchors  # 09-07 복구 실행의 재현을 요구한다 (어긋나면 rc=1)
    python3 engine/tools/c47_step4.py --quiet    # 표 없이 판정만

⚠ **두 기준을 구분한다.** `ANCHORS` 는 09-07 작업석 실행의 인쇄값이고 **영구 고정**이다 — 브리프 162
커밋 1(`aea75984`)에서만 통과하고, 이후 커밋들은 결함을 하나씩 고치므로 **어긋나는 것이 정상**이다.
`EXPECTED` 는 **현재 커밋의 값**이고 커밋마다 갱신된다 — 게이트가 기본 모드를 돌려 회귀를 막는다.
앵커를 커밋마다 갱신하면 그것은 앵커가 아니고, 기대표를 갱신하지 않으면 그것은 회귀 감지가 아니다.

⚠ **판정은 여기서 하지 않는다.** 사전등록은 `engine/interior-core.md` C47 (g) — 네 판정 칸, 고정값
여덟, 목표 `q_Earth/q_Mars` = 3.68 / 4.78, 무용융 기준선 1.372, (a)(b)(c) 분해. 4단계의 판정은
C47 (k) 커밋 6 에 적혀 있다: 최선 칸 1.5114 로 **어느 α 도 목표에 닿지 않는다.**

복구 경로는 `/Users/vana/Desktop/NearStars-artifacts/2026-09-08-c47-step4/c47_step4_recovered.md`
(C47 (j)). 실행 시간은 ~90 s — eq. 56 의 고정점이 1500 °C 행에서 120여 회 반복한다.
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
BODY_FILES = {"Earth": "earth.yaml", "Mars": "mars.yaml"}

#: 09-07 실행 출력. `(q_E, q_M, ratio)`, 인쇄된 자리수 그대로. **고정 — 갱신하지 않는다.**
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
ANCHOR_B = 4.1921e10
DEPLETED_ANCHORS = {(1350.0, "Earth"): (61.8, 0.9787), (1350.0, "Mars"): (163.8, 0.9090),
                    (1500.0, "Earth"): (108.2, 0.9627), (1500.0, "Mars"): (286.7, 0.8407)}

#: 현재 커밋의 값 — 브리프 162 커밋 6(`e34f2425`) 이후. 결함 수정마다 여기를 갱신한다.
EXPECTED = {
    (1350.0, "§3.2 3.7e-5", "(a) dehydr only"): (51.98, 29.16, 1.7823),
    (1350.0, "§3.2 3.7e-5", "(b) buoyancy only"): (51.98, 36.41, 1.4276),
    (1350.0, "§3.2 3.7e-5", "(c) both"): (51.98, 29.16, 1.7823),
    (1350.0, "§4   2.0e-3", "(a) dehydr only"): (51.98, 29.16, 1.7823),
    (1350.0, "§4   2.0e-3", "(b) buoyancy only"): (51.99, 39.03, 1.3319),
    (1350.0, "§4   2.0e-3", "(c) both"): (51.98, 29.16, 1.7823),
    (1500.0, "§3.2 3.7e-5", "(a) dehydr only"): (51.03, 32.22, 1.5838),
    (1500.0, "§3.2 3.7e-5", "(b) buoyancy only"): (105.78, 78.55, 1.3467),
    (1500.0, "§3.2 3.7e-5", "(c) both"): (51.03, 32.22, 1.5838),
    (1500.0, "§4   2.0e-3", "(a) dehydr only"): (51.03, 32.22, 1.5838),
    (1500.0, "§4   2.0e-3", "(b) buoyancy only"): (120.82, 88.94, 1.3584),
    (1500.0, "§4   2.0e-3", "(c) both"): (51.03, 32.22, 1.5838),
    # 천체별 선언 T_p (지구·화성 모두 1600 K = 1326.85 °C) — 커밋 6 의 판정 벌
    ("declared", "§3.2 3.7e-5", "(a) dehydr only"): (45.15, 29.87, 1.5114),
    ("declared", "§3.2 3.7e-5", "(b) buoyancy only"): (45.15, 32.67, 1.3818),
    ("declared", "§3.2 3.7e-5", "(c) both"): (45.15, 29.87, 1.5114),
    ("declared", "§4   2.0e-3", "(a) dehydr only"): (45.15, 29.87, 1.5114),
    ("declared", "§4   2.0e-3", "(b) buoyancy only"): (45.15, 34.09, 1.3243),
    ("declared", "§4   2.0e-3", "(c) both"): (45.15, 29.87, 1.5114),
}
EXPECTED_B = {"§3.2 3.7e-5": 7.777002e08, "§4   2.0e-3": 4.203785e10}
TARGETS = (3.68, 4.78)
NO_MELTING = 1.372


def declared_t_p_k(body: str) -> float:
    """바디 파일의 `potential_temperature` [K] — `engine/bodies/<body>.yaml` 이 유일한 출처."""
    import yaml
    path = Path(__file__).resolve().parent.parent / "bodies" / BODY_FILES[body]
    return float(yaml.safe_load(path.read_text(encoding="utf-8"))["inputs"]["potential_temperature"])


def urey(body: str, q_w_m2: float) -> float:
    b = sl.STEP4_BODIES[body]
    area = 4.0 * math.pi * b["r_p"] ** 2
    heat = rg.budget(b["mass"] * (1.0 - b["cmf"]))["total_w"]
    return heat / (q_w_m2 * area)


def one_set(key, t_p_earth: float, t_p_mars: float, b_by_alpha: dict, quiet: bool) -> dict:
    """한 벌(여섯 런). `key` 는 공통 T_p 값이거나 `"declared"`."""
    got = {}
    for a_label, alpha in ALPHAS:
        for r_label, d_eta, buoy in RUNS:
            b_a = b_by_alpha[a_label]
            e = sl.step4_run("Earth", t_p_earth, alpha, d_eta, buoy, b_a)
            m = sl.step4_run("Mars", t_p_mars, alpha, d_eta, buoy, b_a)
            q_e, q_m = e["q_w_m2"] * 1e3, m["q_w_m2"] * 1e3
            ratio = e["q_w_m2"] / m["q_w_m2"]
            got[(key, a_label, r_label)] = (round(q_e, 2), round(q_m, 2), round(ratio, 4),
                                            e["eq56_converged"] and m["eq56_converged"])
            if not quiet:
                ur_e, ur_m = urey("Earth", e["q_w_m2"]), urey("Mars", m["q_w_m2"])
                print(f"    α {a_label} {r_label:18s} q_E {q_e:7.2f} q_M {q_m:7.2f} mW/m² · "
                      f"q_E/q_M {ratio:7.4f} · Ur_E {ur_e:6.3f} Ur_M {ur_m:6.3f} "
                      f"Ur_M/Ur_E {ur_m / ur_e:6.3f} · 목표의 {ratio / TARGETS[0] * 100:4.1f} % / "
                      f"{ratio / TARGETS[1] * 100:4.1f} %")
    return got


def main() -> int:
    quiet = "--quiet" in sys.argv
    strict = "--anchors" in sys.argv
    b_by_alpha = {label: sl.fit_b_eq30(alpha) for label, alpha in ALPHAS}
    got, fails = {}, []

    if not quiet:
        for label, _ in ALPHAS:
            print(f"b (α {label} 로 적합, 하나의 전역 선언) = {b_by_alpha[label]:.6e}")
        r_b = b_by_alpha[ALPHAS[0][0]] / b_by_alpha[ALPHAS[1][0]]
        r_a = ALPHAS[0][1] / ALPHAS[1][1]
        print(f"    b 비 {r_b:.6e} 대 α 비 {r_a:.6e} → "
              f"{'α 가 b 에 흡수된다 (Ra_i 동일)' if abs(r_b / r_a - 1) < 1e-6 else '⚠ 흡수되지 않는다'}")
        print(f"목표 q_E/q_M : {TARGETS[0]} (우리 0.454) / {TARGETS[1]} (Korenaga 0.35) · "
              f"무용융 기준선 {NO_MELTING} — C47 (g). 판정은 C47 (k) 커밋 6")
        for body in ("Earth", "Mars"):
            bb = sl.STEP4_BODIES[body]
            print(f"    H_{body} = {rg.budget(bb['mass'] * (1.0 - bb['cmf']))['total_w']:.6e} W · "
                  f"A = {4.0 * math.pi * bb['r_p'] ** 2:.6e} m²")

    for t_p in T_P_CELSIUS:
        if not quiet:
            print(f"\n=== 공통 T_p = {t_p:.0f} °C = {t_p + 273.15:.2f} K, 천체별 조정 없음 ===")
            for body in ("Earth", "Mars"):
                z_d, depth = sl.z_d_from_solidus(sl.STEP4_BODIES[body]["g"],
                                                 sl.STEP4_BODIES[body]["D"], t_p)
                a_km, a_z = DEPLETED_ANCHORS[(t_p, body)]
                ok = round(depth / 1e3, 1) == a_km and round(z_d, 4) == a_z
                if not ok:
                    fails.append(f"{body} {t_p:.0f} 고갈층 {depth / 1e3:.1f}/{z_d:.4f} ≠ {a_km}/{a_z}")
                print(f"    {body:6s} 고갈층 {depth / 1e3:6.1f} km = 맨틀의 "
                      f"{(1 - z_d) * 100:5.2f} %   z*_D(초기) {z_d:.4f}  {'✓' if ok else '✗'}")
        got.update(one_set(t_p, t_p, t_p, b_by_alpha, quiet))

    t_k = {b: declared_t_p_k(b) for b in ("Earth", "Mars")}
    if not quiet:
        print(f"\n=== 천체별 선언 T_p — 지구 {t_k['Earth']:.1f} K · 화성 {t_k['Mars']:.1f} K "
              f"(= {t_k['Earth'] - 273.15:.2f} · {t_k['Mars'] - 273.15:.2f} °C) ===")
        if abs(t_k["Earth"] - t_k["Mars"]) < 1e-9:
            print("    ⚠ 두 선언이 같은 값이라 이 벌은 공통 T_p 케이스와 같다 — 화성이 지구값을 "
                  "이전받았기 때문이고(0단계 통과, 오너 2026-09-08 17:52), 물리적 우연이 아니다.")
    got.update(one_set("declared", t_k["Earth"] - 273.15, t_k["Mars"] - 273.15, b_by_alpha, quiet))

    for key, (q_e, q_m, ratio, converged) in got.items():
        if not converged:
            fails.append(f"{key}: eq. 56 미수렴")
    ref, ref_b, name = ((ANCHORS, {ALPHAS[1][0]: ANCHOR_B}, "09-07 앵커") if strict
                        else (EXPECTED, EXPECTED_B, "현재 기대표"))
    for key, expect in ref.items():
        if key not in got:
            fails.append(f"{key}: {name} 에 있는 칸이 실행되지 않았다")
            continue
        q_e, q_m, ratio, _ = got[key]
        if (q_e, q_m, ratio) != tuple(expect):
            fails.append(f"{key}: {q_e}/{q_m}/{ratio} ≠ {name} {expect[0]}/{expect[1]}/{expect[2]}")
    for label, expect_b in ref_b.items():
        if f"{b_by_alpha[label]:.6e}" != f"{expect_b:.6e}":
            fails.append(f"b(α {label}) {b_by_alpha[label]:.6e} ≠ {name} {expect_b:.6e}")
    n = len(ref) + len(ref_b) + (len(DEPLETED_ANCHORS) if not quiet else 0)

    if fails:
        print(f"\n[FAIL] C47 4단계 — {name} 와 {len(fails)} 칸 어긋남 (기준 {n} 칸)")
        for f in fails:
            print(f"    {f}")
        return 1
    print(f"\n[PASS] C47 4단계 — {name} {n} 칸 일치 "
          f"({'승격된 산수가 복구된 실행을 재현한다' if strict else '회귀 없음'}) · 판정은 C47 (k)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
