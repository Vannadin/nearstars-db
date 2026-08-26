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
from porosity import MASS_COMPACT_KG, P_GRAIN_FRACTURE, voids_expected

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
# 다섯 번째 칸은 **보드가 조석가열을 선언하는가** 다. 이것도 물리가 아니라 선언이다 —
# 조석가열은 다른 노드의 출력이고, 여기서 질량이나 궤도로 추정하면 그 노드의 두 번째
# 사본이 생긴다. 공극이 남을 레짐인가를 판정하는 세 지표 중 하나로만 쓰인다
# (Bierson+ 2019 §2.2 의 제외 목록).
#
# 지금 True 인 둘은 보드에 `tidal_heating` 행을 실제로 가진 둘이다
# (phase4/alpha_centauri.yaml:1553 Dante ~1200× Io · :1888 Hades ~15× Io). 나머지
# 넷에는 그 행이 없다.
#
# (이름, 질량 kg, 반지름 km, 얼음 허용, 조석가열 선언, 보드 근거)
ROSTER = [
    ("Pandora (A b III)",     3.85e24, 5724, True,  False,
     "surface: 대륙과 바다, 극관"),
    ("Cassandra (A b IV)",    9.00e23, 3400, True,  False,
     "surface: 물바다 + 극관"),
    ("Hades (A b II)",        5.00e21,  750, False, True,
     "identity: rocky moon, 'silicate and ice-free'"),
    ("Dante (A b I)",         1.552e21, 521, False, True,
     "identity/surface: silicate volcanic (Io-type), SO2 탈가스 대기"),
    ("Chaos (A b V)",         5.40e20,  400, True,  False,
     "identity: Small icy moon, 'water ice with rock'"),
    ("Proxima Cen c I",       2.32e20,  326, True,  False,
     "포획 KBO 위성 — 보드가 얼음을 배제하지 않는다"),
]

# 태양계 얼음 위성. **발표된** C/MR² 를 재현하는지 보는 자리이고, 새로 들어온
# III·V·VI 이 수렴한 해 안에서 실제로 쓰이는지 확인하는 자리다 — Ganymede 의 얼음 기둥
# 바닥은 1.5 GPa 로 얼음 VI 구간 한가운데다.
#
# 다섯 중 **Ganymede 만 판정선** 이다. 나머지 넷은 이 레시피가 자유 분율 하나만 푸는
# 2층 구조라서 못 맞히는 천체들이고, 그 사실 자체가 이 표의 내용이다. C/MR² 값은 전부
# ADS 전문에서 확인했다.
#
# (이름, 질량 kg, 반지름 km, 발표 C/MR², 출처, 판정선인가)
ICY_ANCHORS = [
    ("Ganymede",  1.4819e23, 2634.1, 0.3115,
     "Schubert+ 2004 (Anderson+ 1996)", True),
    ("Callisto",  1.0759e23, 2410.3, 0.3549, "Anderson+ 2001", False),
    ("Titan",     1.3452728e23, 2575.5, 0.3414, "Iess+ 2010 (Cassini)", False),
    ("Europa",    4.7998e22, 1560.8, 0.346,  "Anderson+ 1998", False),
    ("Enceladus", 1.0802e20,  252.1, 0.335,  "Iess+ 2014 (Cassini)", False),
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
    if "얼음 X" in res.reason:
        return "ice X / superionic phase"
    if "다공도" in res.reason:
        return "porosity or an H/He envelope"
    return "see reason"


def roster_table() -> None:
    """로스터 표. 푼 것은 조성을, 못 푼 것은 기작을 적는다.

    `voids?` 칸이 있는 이유. 공극 축으로 풀린 천체는 `solved` 로 나오지만, 그 해가
    **믿을 만한 레짐에서 나왔는가** 는 별개의 질문이고 답이 다를 수 있다. 그 판정이
    출력에 없던 동안에는 방법론 문서의 산문만이 그 사실을 들고 있었다 — 표가 스스로
    말하지 못하면 산문이 대신 말하게 되고, 산문은 어긋난다."""
    print("| body | ρ̄ (kg/m³) | ice declared | tidal | outcome | voids? "
          "| what it took, or what is missing |")
    print("|---|---|---|---|---|---|---|")
    for name, mkg, r_km, ice_ok, tidal, _why in ROSTER:
        rho = mkg / (4.0 / 3.0 * 3.141592653589793 * (r_km * 1e3) ** 3)
        res = infer_composition(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M,
                                ice_allowed=ice_ok, tidal_heating=tidal)
        ice_col = "allowed" if ice_ok else "**excluded**"
        tidal_col = "declared" if tidal else "—"
        if res.applicable:
            axis = res.regime.replace("inferred_", "")
            val = res.inputs[axis]
            # 공극 축으로 풀린 것만 판정이 결론을 바꾼다. 다른 축은 빈 공간을
            # 주장하지 않으므로 판정이 걸려도 그 해에 대한 진술이 아니다.
            porous = axis == "initial_porosity"
            ok = res.values["voids_expected"]
            verdict = ("**no**" if porous and not ok else
                       "yes" if porous else "n/a")
            what = (f"solved — {axis} {val:.3f}, C/MR² {res.values['nmoi']:.4f}, "
                    f"P_c {res.values['core_pressure'] * 1e3:.0f} MPa")
            if porous and not ok:
                what += " — **공극 해이나 공극이 남을 레짐이 아니다**"
            print(f"| {name} | {rho:.0f} | {ice_col} | {tidal_col} | solved "
                  f"| {verdict} | {what} |")
        else:
            print(f"| {name} | {rho:.0f} | {ice_col} | {tidal_col} | declined "
                  f"| — | {_mechanism(res)} |")


# 각 상의 기준 등온. eos.py 가 이 온도에서 P = 0 의 ρ·K_T·K′ 를 읽어 BME3 상수로 쓴다.
SEAFREEZE_REF = (("ice_iii", "III", 251.15, 209.5, 355.0),
                 ("ice_v", "V", 256.43, 355.0, 618.4),
                 ("ice_vi", "VI", 272.73, 618.4, 2216.0))

# SeaFreeze README 가 검증용으로 싣는 단일점 출력. 얼음 VI, 900 MPa / 255 K.
# 이건 **발표된 값** 이라 우리 출력으로 우리를 시험하는 게 아니다.
SEAFREEZE_PUBLISHED_ICE_VI = (900.0, 255.0, 1356.1)


def _seafreeze_crosscheck() -> list[str]:
    """박아둔 III·V·VI 상수를 원 Gibbs 표현과 대조한다. 없으면 건너뛴다."""
    try:
        import numpy as np
        from seafreeze.seafreeze import defpath, getProp
    except ImportError:
        print("  [SKIP] SeaFreeze 가 없다. engine/.venv 로 돌리면 이 절이 뛴다 "
              "(engine/requirements.txt)")
        return []

    def sf(p_mpa, t_k, phase, *props):
        arr = np.array([np.atleast_1d(np.asarray(p_mpa, float)),
                        np.atleast_1d(np.asarray(t_k, float))], dtype=object)
        out = getProp(arr, phase, defpath, *props)
        return [np.asarray(getattr(out, k), float).ravel() for k in props]

    from eos import MATERIALS
    bad: list[str] = []
    phases = {ph.name: ph for ph in MATERIALS["h2o"].phases}

    # 1) 얼음 Ih 이 두 출처에서 같은가. 이 일치가 III·V·VI 을 같은 표현에서 읽어올 근거다.
    rho_ih = sf(0.101325, 273.152519, "Ih", "rho")[0][0]
    d = abs(rho_ih - 916.721463419) / 916.721463419
    ok = d < 1e-9
    if not ok:
        bad.append(f"SeaFreeze 의 얼음 Ih 이 IAPWS-06 검증값과 {d:.1e} 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 얼음 Ih  SeaFreeze {rho_ih:.9f} · "
          f"IAPWS-06 916.721463419 kg/m³ (상대차 {d:.1e})")

    # 2) 세 상의 상수가 그 자리에서 다시 나오는가, 그리고 그 상수로 세운 BME3 가
    #    구간 전체에서 원 표현의 ρ(P) 를 재현하는가.
    for name, code, t_ref, p_lo, p_hi in SEAFREEZE_REF:
        ph = phases[name]
        rho0, k0, k0p = (v[0] for v in sf(0.0, t_ref, code, "rho", "Kt", "Kp"))
        drifts = [abs(ph.rho0 - rho0) / rho0,
                  abs(ph.k0 - k0 * 1e6) / (k0 * 1e6),
                  abs(ph.k0p - k0p) / k0p]
        ps = [p_lo + (p_hi - p_lo) * i / 24 for i in range(25)]
        got = sf(ps, t_ref, code, "rho")[0]
        worst = max(abs(ph.density(p * 1e6) - g) / g for p, g in zip(ps, got))
        ok = max(drifts) < 1e-6 and worst < 0.002
        if not ok:
            bad.append(f"{name}: 상수 표류 {max(drifts):.1e}, 구간 재현 오차 {worst * 100:.3f} %")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:8} T_ref {t_ref:6.2f} K  "
              f"ρ₀ {ph.rho0:9.4f} · K₀ {ph.k0 / 1e9:7.4f} GPa · K₀′ {ph.k0p:.4f}  "
              f"(상수 표류 {max(drifts):.0e}, {p_lo:.0f}-{p_hi:.0f} MPa 재현 "
              f"{worst * 100:.3f} %)")

    # 3) 발표된 단일점. 우리 얼음 VI 는 272.73 K 등온이고 그 점은 255 K 라, 차이는
    #    온도 그 자체다 — 그래서 이 줄은 사다리가 아니라 **온도폭** 을 재는 자리다.
    p_mpa, t_k, rho_pub = SEAFREEZE_PUBLISHED_ICE_VI
    rho_sf = sf(p_mpa, t_k, "VI", "rho")[0][0]
    rho_ours = phases["ice_vi"].density(p_mpa * 1e6)
    d_pub = abs(rho_sf - rho_pub) / rho_pub
    d_ours = (rho_ours - rho_pub) / rho_pub
    ok = d_pub < 1e-4 and abs(d_ours) < 0.02
    if not ok:
        bad.append(f"발표 체크값: SeaFreeze {d_pub:.1e}, 우리 등온 {d_ours * 100:+.2f} %")
    print(f"  [{'PASS' if ok else 'FAIL'}] 발표 체크값 얼음 VI {p_mpa:.0f} MPa / {t_k:.0f} K "
          f"= {rho_pub} kg/m³ · SeaFreeze {rho_sf:.2f} (상대차 {d_pub:.0e}) · "
          f"우리 272.73 K 등온 {rho_ours:.2f} ({d_ours * 100:+.2f} %, 이게 온도폭이다)")
    return bad


def icy_table() -> None:
    """문서 §Validation 의 얼음 위성 표를 다시 낸다."""
    print("| moon | ρ̄ (kg/m³) | ice fraction | ice-column base | C/MR² derived | published | error | source |")
    print("|---|---|---|---|---|---|---|---|")
    for name, mkg, r_km, nmoi_pub, src, _gate in ICY_ANCHORS:
        rho = mkg / (4.0 / 3.0 * 3.141592653589793 * (r_km * 1e3) ** 3)
        res = infer_composition(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M,
                                ice_allowed=True)
        if not res.applicable:
            print(f"| {name} | {rho:.0f} | – | – | declined | {nmoi_pub:.4f} | – | {src} |")
            continue
        imf = res.inputs["ice_mass_fraction"]
        base = _ice_base_gpa(res)
        print(f"| {name} | {rho:.0f} | {imf:.3f} | {base} | "
              f"{res.values['nmoi']:.4f} | {nmoi_pub:.4f} | "
              f"{abs(res.values['nmoi'] - nmoi_pub) / nmoi_pub * 100:.1f} % | {src} |")


def _ice_base_gpa(res) -> str:
    """note 에 기록된 얼음 기둥 바닥 압력을 상 이름과 함께 뽑는다."""
    for note in res.notes:
        if "얼음 기둥 바닥" in note:
            frag = note.split("얼음 기둥 바닥")[1].split(",")[0].strip()
            gpa = float(frag.split()[0])
            phase = ("ice Ih" if gpa < 0.2095 else "ice III" if gpa < 0.355
                     else "ice V" if gpa < 0.6184 else "ice VI" if gpa < 2.216
                     else "ice VII")
            return f"{frag} ({phase})"
    return "–"


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0
    if "--roster" in sys.argv:
        roster_table()
        return 0
    if "--icy" in sys.argv:
        icy_table()
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

    print("\n발표된 얼음 위성 — 새 상들이 수렴한 해 안에서 실제로 쓰이는가")
    # Ganymede 만 판정선이다. 얼음 기둥 바닥이 1.5 GPa 로 얼음 VI 구간 한가운데라,
    # 이 한 줄이 III·V·VI 이 사격 경로가 아니라 **답** 안에서 쓰인다는 증거다.
    # 나머지 넷은 `--icy` 가 표로 낸다 — 2층 구조로는 못 맞히는 천체들이고, 넣으면
    # 기본 실행이 1분을 넘긴다.
    gan = [a for a in ICY_ANCHORS if a[5]][0]
    res = infer_composition(gan[1] / EARTH_MASS_KG, gan[2] * 1e3 / EARTH_RADIUS_M,
                            ice_allowed=True)
    if not res.applicable:
        fails.append(f"{gan[0]}: 풀려야 하는데 거절했다 — {res.reason[:70]}")
        print(f"  [FAIL] {gan[0]} 거절됨")
    else:
        base = _ice_base_gpa(res)
        off = abs(res.values["nmoi"] - gan[3]) / gan[3]
        ok = off <= TOL and "ice VI" in base
        if not ok:
            fails.append(f"{gan[0]}: C/MR² {res.values['nmoi']:.4f} vs {gan[3]} "
                         f"({off * 100:.1f}%), 얼음 기둥 바닥 {base}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {gan[0]} C/MR² {res.values['nmoi']:.4f} vs "
              f"{gan[3]:.4f} ({off * 100:.1f} %) · 얼음질량분율 "
              f"{res.inputs['ice_mass_fraction']:.3f} · 얼음 기둥 바닥 {base} · {gan[4]}")

    print("\n물얼음 상 사다리 — 209.5 MPa 부터 37.4 GPa 까지 끊긴 데가 없는가")
    # 2026-08-25 에 III·V·VI 이 들어와 사다리가 이어졌다. 이어져 있다는 것은 주장이
    # 아니라 검사 대상이다 — 전이압 상수 하나를 이웃과 어긋나게 고치면 조용히 구멍이
    # 다시 열리고, 그러면 솔버가 답이 있는 자리에서 거절한다.
    from eos import H2O
    for prev, nxt in zip(H2O.phases, H2O.phases[1:]):
        cond = abs(nxt.p_min - prev.p_max) <= 1e-6 * max(prev.p_max, 1.0)
        if not cond:
            fails.append(f"얼음 사다리가 {prev.name} 상한 {prev.p_max / 1e6:.1f} MPa 와 "
                         f"{nxt.name} 하한 {nxt.p_min / 1e6:.1f} MPa 사이에서 끊겼다")
        print(f"  [{'PASS' if cond else 'FAIL'}] {prev.name:8} → {nxt.name:8} "
              f"{prev.p_max / 1e6:8.1f} MPa 에서 이어진다")

    print("\nIII·V·VI 의 세 상수 — 박아둔 값이 원 표현과 같은가 (SeaFreeze 있을 때만)")
    # 계수를 손으로 옮겨 적은 것이므로 대조가 필요하다. 이 리포지토리는 손으로 친 표에서
    # 54배가 어긋난 전례가 있다. SeaFreeze 는 **런타임 의존성이 아니다** — check.sh 는
    # 시스템 파이썬으로 돌고 이 절만 건너뛴다. 대조는 engine/.venv 로 돌릴 때 실제로 뛴다.
    #
    #   engine/.venv/bin/python engine/test_interior.py
    fails += _seafreeze_crosscheck()

    print("\n로스터 — 저밀도 위성 넷 중 몇을 푸는가")
    solved = declined = 0
    for name, mkg, r_km, ice_ok, tidal, _why in ROSTER:
        res = infer_composition(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M,
                                ice_allowed=ice_ok, tidal_heating=tidal)
        if res.applicable:
            solved += 1
            axis = res.regime.replace("inferred_", "")
            voids = "" if axis != "initial_porosity" else (
                " · 공극 레짐 " + ("O" if res.values["voids_expected"] else "X"))
            print(f"  [풀림] {name:20} {axis} {res.inputs[axis]:.3f} · "
                  f"C/MR² {res.values['nmoi']:.4f} · "
                  f"P_c {res.values['core_pressure'] * 1e3:.0f} MPa{voids}")
        else:
            declined += 1
            named = any(k in res.reason for k in ("다공도", "얼음 X"))
            if not named:
                fails.append(f"{name}: 거절 이유가 기작 이름이 아니다 — {res.reason[:60]}")
            print(f"  [거절] {name:20} {res.reason[:96]}")
    print(f"         풀림 {solved} · 거절 {declined}")

    # ── 공극 레짐 판정 ──────────────────────────────────────────────────
    #
    # 지표 셋을 하나씩 켜고 끈다. 판정이 산문이 아니라 값이 된 뒤로 이렇게 시험할 수
    # 있고, 그게 승격의 이유다. 각 지표마다 **양쪽** 을 본다 — 문턱 위에서 발화하고
    # 아래에서 침묵해야 지표이지, 늘 발화하면 상수다.
    print("\n공극 레짐 판정 — 지표 셋이 각자 문턱의 양쪽에서 다르게 답하는가")
    below = MASS_COMPACT_KG * 0.5      # 관측된 전이질량 아래
    above = MASS_COMPACT_KG * 5.0      # 위
    p_lo = P_GRAIN_FRACTURE * 0.5      # 파쇄 문턱 아래
    p_hi = P_GRAIN_FRACTURE * 5.0      # 위
    for label, args, want in (
            ("셋 다 안 걸리면 공극이 기대된다", (below, p_lo, False), True),
            ("질량이 전이질량을 넘으면 아니다", (above, p_lo, False), False),
            ("중심압이 파쇄 문턱을 넘으면 아니다", (below, p_hi, False), False),
            ("조석가열이 선언되면 아니다", (below, p_lo, True), False)):
        got, why = voids_expected(*args)
        ok = got is want
        if not ok:
            fails.append(f"공극 레짐 판정: {label} — {got}, {why[:60]}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    # 판정은 **이유를 이름 대야** 한다. 불리언만 돌려주면 표가 다시 산문을 부른다.
    _, why_off = voids_expected(above, p_hi, True)
    named = all(k in why_off for k in ("전이질량", "파쇄 문턱", "조석가열"))
    if not named:
        fails.append(f"공극 레짐 판정: 걸린 지표를 전부 이름 대지 않는다 — {why_off}")
    print(f"  [{'PASS' if named else 'FAIL'}] 걸린 지표를 이름 댄다")

    # 그리고 솔버를 통해서도 나와야 한다. 판정 함수만 맞고 배선이 끊기면 표는 여전히
    # 아무 말도 못 한다.
    r_dante = infer_composition(1.552e21 / EARTH_MASS_KG, 521e3 / EARTH_RADIUS_M,
                                ice_allowed=False, tidal_heating=True)
    wired = (r_dante.applicable
             and r_dante.regime == "inferred_initial_porosity"
             and r_dante.values.get("voids_expected") is False)
    if not wired:
        fails.append("공극 레짐 판정: 역산 결과에 판정이 실려 오지 않는다")
    print(f"  [{'PASS' if wired else 'FAIL'}] 공극 축으로 풀린 결과가 판정을 싣고 온다")

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
