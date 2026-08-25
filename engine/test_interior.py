# 내부 구조 앵커 — 조성과 질량만으로 실측 관성모멘트를 재현하는가, 그리고 문서 표를 다시 만든다
"""Anchor the interior solver on measured radii and moments of inertia.

    python3 engine/test_interior.py
    python3 engine/test_interior.py --table     문서 §Validation 표를 다시 낸다
    python3 engine/test_interior.py --roster    로스터 위성 여섯을 훑는다

앵커는 전부 **측정된** 값이다 — 반지름은 측지, C/MR² 는 중력장이나 세차에서 나온
값이지 모형에서 나온 값이 아니다. 우리 출력으로 우리를 시험하면 아무것도 검증되지
않는다.

**층 밀도를 넘기지 않는다.** 예전 2층 모형은 네 앵커 전부에 핵·맨틀 밀도를 손으로
넣어줘야 했고, 그래서 그 시험은 기하만 검증하고 밀도표는 검증하지 못했다. 이제는
질량과 핵질량분율만 준다 — 층 밀도가 적분의 결과이므로, 이 표가 맞으면 상태방정식과
기하가 함께 맞는 것이다.
"""
from __future__ import annotations

import sys

import interior
from interior import EARTH_MASS_KG, EARTH_RADIUS_M, infer_composition, solve

# (이름, 질량 M⊕, 발표 반지름 R⊕, CMF, 발표 C/MR², 발표 f, 출처)
#
# CMF 는 조성 선언이지 적합 매개변수가 아니다. 넷 다 지구화학·중력장 문헌의 표준값을
# 그대로 쓴다 — 우리 답이 맞도록 돌려 맞춘 값이 아니다.
ANCHORS = [
    ("Earth",   1.0000, 1.0000, 0.325, 0.3307, 3480 / 6371,
     "PREM (Dziewonski & Anderson 1981)"),
    ("Mars",    0.1074, 0.5320, 0.24,  0.3644, 1830 / 3390,
     "Konopliv+ 2011 · InSight"),
    ("Mercury", 0.0553, 0.3829, 0.70,  0.3460, 2020 / 2440,
     "Margot+ 2012 (MESSENGER)"),
    ("Moon",    0.0123, 0.2727, 0.019, 0.3931, 350 / 1737,
     "Williams+ 2014 (LLR)"),
]

# 거절해야 하는 것들. 거절이 답이고, **어느 기작 때문인지 이름을 대야** 답이다.
DECLINES = [
    ("미분화", dict(mass_earth=1.0, core_mass_fraction=0.3, differentiated=False),
     "혼합상", "금속이 맨틀에 섞여 있다 — 혼합물 상태방정식이 필요하다"),
    ("분율 합 초과", dict(mass_earth=1.0, core_mass_fraction=0.7, ice_mass_fraction=0.5),
     "질량분율", "핵과 얼음의 합이 1 을 넘는다"),
    ("모르는 조성", dict(mass_earth=1.0, composition="cheese"),
     "조성", "재료가 배정되지 않았다"),
    ("얼음 많은 큰 천체", dict(mass_earth=1.0, composition="water"),
     "얼음 X", "물 기둥이 얼음 X·초이온상까지 내려간다"),
    ("거대행성", dict(mass_earth=120.0, body_class="giant"),
     "폴리트로프", "고체 표면이 없다 — 응축상 EOS 를 H/He 에 쓸 수 없다"),
]

# 로스터. 판정이 아니라 **무엇이 풀리고 무엇이 왜 안 풀리는가** 를 보여주는 표다.
#
# 네 번째 칸은 **보드가 얼음을 허용하는가** 다. 이건 물리가 아니라 선언이고, 넘기지
# 않으면 역산이 밀도만 보고 축을 고른다 — 그러면 보드가 규산염 화산체로 정해둔
# 천체에 얼음을 붙이고 "얼음 상이 필요하다" 는 틀린 진술이 나온다. 저밀도의 원인을
# 가려내는 게 이 레시피의 일이므로, 그 선언은 입력이어야 한다.
#
# (이름, 질량 kg, 반지름 km, 얼음 허용, 보드 근거)
ROSTER = [
    ("Pandora (A b III)",     3.85e24, 5724, True,
     "surface: 대륙과 바다, 극관"),
    ("Cassandra (A b IV)",    9.00e23, 3400, True,
     "surface: 물바다 + 극관"),
    ("Hades (A b II)",        5.00e21,  750, False,
     "identity: rocky moon, 'silicate and ice-free'"),
    ("Dante (A b I)",         1.552e21, 521, False,
     "identity/surface: silicate volcanic (Io-type), SO2 탈가스 대기"),
    ("Chaos (A b V)",         5.40e20,  400, True,
     "identity: Small icy moon, 'water ice with rock'"),
    ("Proxima Cen c I",       2.32e20,  326, True,
     "포획 KBO 위성 — 보드가 얼음을 배제하지 않는다"),
]

TOL = 0.03          # 3 %. 균질 2층 시절의 허용치가 5 % 였고 지구가 그 4.8 % 였다.
EARTH_TOL = 0.01    # 지구는 1 % 안. 자기압축이 실제로 들어갔는지의 판정선이다.
RADIUS_TOL = 0.01   # 반지름 1 %


def rows():
    for name, m, r_pub, cmf, nmoi_pub, f_pub, src in ANCHORS:
        yield name, solve(m, core_mass_fraction=cmf), m, r_pub, nmoi_pub, f_pub, src


def table() -> None:
    """문서 §Validation 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | R derived | R published | ΔR | C/MR² derived | published | error "
          "| f derived | f published | P_c (GPa) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, res, _m, r_pub, nmoi_pub, f_pub, _src in rows():
        v = res.values
        print(f"| {name} | {v['radius']:.4f} | {r_pub:.4f} | "
              f"{(v['radius'] - r_pub) / r_pub * 100:+.1f} % | "
              f"{v['nmoi']:.4f} | {nmoi_pub:.4f} | "
              f"{abs(v['nmoi'] - nmoi_pub) / nmoi_pub * 100:.1f} % | "
              f"{v['core_radius_fraction']:.3f} | {f_pub:.3f} | "
              f"{v['core_pressure']:.1f} |")


def _mechanism(res) -> str:
    """거절 결과에서 **기작 이름** 한 줄을 뽑는다. 증상이 아니라 기작이어야 한다."""
    if "빈 공간" in res.reason:
        return ("porosity: ice is excluded by declaration, so void space is what is "
                "left. Needs a compaction curve")
    if "III·V·VI" in res.reason:
        return "high-pressure ice phases III/V/VI (or a liquid ocean if warm)"
    if "얼음 X" in res.reason:
        return "ice X / superionic phase"
    if "다공도" in res.reason:
        return "porosity or an H/He envelope"
    return "see reason"


def roster_table() -> None:
    """로스터 표. 푼 것은 조성을, 못 푼 것은 기작을 적는다."""
    print("| body | ρ̄ (kg/m³) | ice declared | outcome | what it took, or what is missing |")
    print("|---|---|---|---|---|")
    for name, mkg, r_km, ice_ok, _why in ROSTER:
        rho = mkg / (4.0 / 3.0 * 3.141592653589793 * (r_km * 1e3) ** 3)
        res = infer_composition(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M,
                                ice_allowed=ice_ok)
        ice_col = "allowed" if ice_ok else "**excluded**"
        if res.applicable:
            axis = res.regime.replace("inferred_", "")
            val = res.inputs[axis]
            what = (f"solved — {axis} {val:.3f}, C/MR² {res.values['nmoi']:.4f}, "
                    f"P_c {res.values['core_pressure'] * 1e3:.0f} MPa")
            print(f"| {name} | {rho:.0f} | {ice_col} | solved | {what} |")
        else:
            print(f"| {name} | {rho:.0f} | {ice_col} | declined | {_mechanism(res)} |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0
    if "--roster" in sys.argv:
        roster_table()
        return 0

    fails: list[str] = []

    print("앵커 — 조성과 질량만으로 실측 반지름과 관성모멘트를 재현하는가")
    worst_n = worst_r = 0.0
    for name, res, _m, r_pub, nmoi_pub, f_pub, src in rows():
        if not res.applicable:
            fails.append(f"{name}: 값이 나와야 하는데 거절했다 — {res.reason[:70]}")
            print(f"  [FAIL] {name:9} 거절됨")
            continue
        v = res.values
        off_n = abs(v["nmoi"] - nmoi_pub) / nmoi_pub
        off_r = abs(v["radius"] - r_pub) / r_pub
        worst_n, worst_r = max(worst_n, off_n), max(worst_r, off_r)
        ok = off_n <= TOL and off_r <= RADIUS_TOL
        if not ok:
            fails.append(f"{name}: C/MR² {v['nmoi']:.4f} vs {nmoi_pub} "
                         f"({off_n * 100:.1f}%), R {v['radius']:.4f} vs {r_pub} "
                         f"({off_r * 100:.1f}%)")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:9} "
              f"R {v['radius']:.4f} vs {r_pub:.4f} ({off_r * 100:4.1f}%)  "
              f"C/MR² {v['nmoi']:.4f} vs {nmoi_pub:.4f} ({off_n * 100:4.1f}%)  "
              f"f {v['core_radius_fraction']:.3f} vs {f_pub:.3f}  {src}")

    print("\n자기압축이 실제로 들어갔는가 — 이 한 줄이 이 레시피의 판정선이다")
    earth = solve(1.0, core_mass_fraction=0.325)
    off = abs(earth.values["nmoi"] - 0.3307) / 0.3307
    ok = off <= EARTH_TOL
    if not ok:
        fails.append(f"지구 C/MR² 오차 {off * 100:.2f}% 가 {EARTH_TOL * 100:.0f}% 위다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구 C/MR² 오차 {off * 100:.2f} % "
          f"(균질 2층 모형은 4.8 % 였다, 허용 {EARTH_TOL * 100:.0f} %)")

    print("\n핵-맨틀 경계 압력 — 적분이 깊이까지 맞는가")
    # PREM 의 핵-맨틀 경계는 반지름 3480 km, 압력 135.8 GPa 다. C/MR² 는 적분값이라
    # 프로파일이 어긋나도 상쇄될 수 있지만, 경계 하나의 압력은 상쇄되지 않는다.
    from interior import EARTH_MASS_KG as _ME, shoot
    st, _ = shoot(_ME, 0.325, 0.0, "fe_prem")
    got = st.p_cmb / 1e9
    d = abs(got - 135.8) / 135.8
    ok = d <= 0.02
    if not ok:
        fails.append(f"지구 핵-맨틀 경계 압력 {got:.1f} GPa, PREM 135.8 ({d * 100:.1f}%)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구 CMB {got:.1f} GPa · PREM 135.8 GPa "
          f"({d * 100:.1f} %)")

    print("\n발표된 M-R 관계와 맞는가 — 우리 곡선을 남의 곡선에 대본다")
    # Zeng+ 2016 eq. 2 (arXiv:1512.08827): R/R⊕ = (1.07 − 0.21·CMF)·(M/M⊕)^(1/3.7).
    # 유효 구간은 1-8 M⊕, CMF 0-0.4 이고 곡선과 ~0.01 R⊕ 안에서 맞는다고 논문이 적는다.
    for m, cmf in ((1.0, 0.325), (1.0, 0.0), (2.0, 0.3), (4.0, 0.2)):
        got = solve(m, core_mass_fraction=cmf).values["radius"]
        want = (1.07 - 0.21 * cmf) * m ** (1.0 / 3.7)
        d = abs(got - want)
        ok = d <= 0.02
        if not ok:
            fails.append(f"Zeng+ 2016 곡선 대비 M={m} CMF={cmf}: {got:.4f} vs {want:.4f}")
        print(f"  [{'PASS' if ok else 'FAIL'}] M={m:.1f} CMF={cmf:.3f}  "
              f"우리 {got:.4f} · Zeng+ 2016 {want:.4f} R⊕  (차이 {d:.4f})")

    print("\n거절 — 도메인 밖은 값이 아니라 **기작 이름** 을 돌려주는가")
    for label, kwargs, keyword, why in DECLINES:
        res = solve(**kwargs)
        ok = not res.applicable and keyword in res.reason
        if not ok:
            fails.append(f"{label}: 거절하거나 '{keyword}' 를 이름 대야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:14} {why}")

    print("\n격자 수렴 — 적분 격자가 오차원이 아님을 보인다")
    base = interior.STEPS
    try:
        interior.STEPS = base * 4
        fine = solve(1.0, core_mass_fraction=0.325).values["nmoi"]
    finally:
        interior.STEPS = base
    drift = abs(fine - earth.values["nmoi"]) / fine
    ok = drift < 1e-3
    if not ok:
        fails.append(f"격자 수렴: {base} → {base * 4} 에서 C/MR² 가 {drift:.1e} 움직인다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 격자 {base} → {base * 4} 에서 "
          f"C/MR² 상대변화 {drift:.1e} (앵커 오차 {off * 100:.2f} % 의 "
          f"{off / max(drift, 1e-12):.0f} 분의 1)")

    print("\n얼음 Ih 의 K₀′ 감도 — 표에 없는 상수를 4 로 둔 것이 무해한가")
    from eos import ICE_IH_KT, ICE_IH_RHO0, ICE_IH_TO_III, Phase
    ref = Phase("ih4", "bm2", ICE_IH_RHO0, ICE_IH_KT, 4.0, ICE_IH_TO_III, "")
    alt = Phase("ih6", "bme3", ICE_IH_RHO0, ICE_IH_KT, 6.0, ICE_IH_TO_III, "")
    d = abs(alt.density(ICE_IH_TO_III) - ref.density(ICE_IH_TO_III)) \
        / ref.density(ICE_IH_TO_III)
    ok = d < 0.005
    if not ok:
        fails.append(f"얼음 Ih K₀′ 감도가 {d * 100:.2f}% 로 크다")
    print(f"  [{'PASS' if ok else 'FAIL'}] Ih 상한(209.5 MPa)에서 K₀′ 4 ↔ 6 의 "
          f"밀도 차 {d * 100:.2f} % — 압축 자체가 "
          f"{(ref.density(ICE_IH_TO_III) / ICE_IH_RHO0 - 1) * 100:.1f} % 뿐이다")

    print("\n로스터 — 저밀도 위성 넷 중 몇을 푸는가")
    solved = declined = 0
    for name, mkg, r_km, ice_ok, _why in ROSTER:
        res = infer_composition(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M,
                                ice_allowed=ice_ok)
        if res.applicable:
            solved += 1
            axis = res.regime.replace("inferred_", "")
            print(f"  [풀림] {name:20} {axis} {res.inputs[axis]:.3f} · "
                  f"C/MR² {res.values['nmoi']:.4f} · "
                  f"P_c {res.values['core_pressure'] * 1e3:.0f} MPa")
        else:
            declined += 1
            named = any(k in res.reason for k in ("III·V·VI", "다공도", "얼음 X"))
            if not named:
                fails.append(f"{name}: 거절 이유가 기작 이름이 아니다 — {res.reason[:60]}")
            print(f"  [거절] {name:20} {res.reason[:96]}")
    print(f"         풀림 {solved} · 거절 {declined}")

    print("\n계약 — 페이로드가 제 몫을 하는가")
    r = solve(1.0, core_mass_fraction=0.325)
    for label, cond in (
            ("inputs 기록", set(r.inputs) >= {"mass_earth", "core_mass_fraction"}),
            ("모든 값에 단위", set(r.values) <= set(r.units)),
            ("반지름이 출력", "radius" in r.values),
            ("중심압이 출력", "core_pressure" in r.values),
            ("근거 동반", bool(r.refs)),
            ("한계를 note 에 적음", bool(r.notes)),
            ("grade 가 calibrated", r.grade == "calibrated")):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    print(f"\n  최악 C/MR² 오차 {worst_n * 100:.1f}% · 최악 반지름 오차 "
          f"{worst_r * 100:.1f}% (허용 {TOL * 100:.0f}% / {RADIUS_TOL * 100:.0f}%)")
    print(f"  {r.evidence()[:150]}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
