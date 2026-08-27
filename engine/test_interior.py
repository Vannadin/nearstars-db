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
    # 미분화는 2026-08-26 에 풀리게 됐다 (test_mixture.py). 얼음·가스와 함께 선언하는
    # 것은 부분 분화의 영역이라 여전히 거절하고, 그 경계를 여기서 지킨다.
    ("미분화 + 얼음", dict(mass_earth=1.0, core_mass_fraction=0.3,
                       ice_mass_fraction=0.3, differentiated=False),
     "부분 분화", "암석+금속만 섞는다 — 얼음이 섞인 것은 다른 문제다"),
    ("분율 합 초과", dict(mass_earth=1.0, core_mass_fraction=0.7, ice_mass_fraction=0.5),
     "질량분율", "핵과 얼음의 합이 1 을 넘는다"),
    ("모르는 조성", dict(mass_earth=1.0, composition="cheese"),
     "조성", "재료가 배정되지 않았다"),
    ("얼음 많은 큰 천체", dict(mass_earth=1.0, composition="water"),
     "얼음 X", "물 기둥이 얼음 X·초이온상까지 내려간다"),
    # 거대행성은 2026-08-26 에 풀리게 됐다 (test_giant.py). 아직 밖인 유체 천체가
    # 이름을 대며 거절하는지는 여기서 계속 지킨다.
    ("갈색왜성", dict(mass_earth=5000.0, body_class="brown_dwarf"),
     "중수소", "13 M_J 위는 광도 이력이 필요하다"),
    ("얼음 자이언트", dict(mass_earth=17.0, body_class="ice_giant"),
     "암모니아", "외피가 H/He 가 아니라 물·암모니아·메탄 혼합물이다"),
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

# ── 3.5 TPa 위의 규산염 ──────────────────────────────────────────────────
#
# 앵커는 **발표된** 수여야 한다는 규율이 이 절에도 걸린다. 이 압력대에는 측정이 없으므로
# 대조 상대는 실험이 아니라 **같은 논문이 따로 발표한 두 번째 표현** 이다.
#
# Seager+ 2007 Table 3 이 Vinet/BME 와 TFD 를 이어 붙인 곡선을 ρ = ρ₀ + cP^n 로 다시
# 적합해 싣는다. MgSiO₃(pv) 행이 아래 셋이고, "valid for the pressure range P < 10¹⁶ Pa"
# 라고 적혀 있다. 우리가 박아둔 BME4 상수는 같은 논문 Table 1 에서 왔으므로, 둘이 서로를
# 재현하면 옮겨 적기가 맞은 것이다 — 54배 오류를 낸 전례가 이 대조를 요구한다.
SEAGER_T3_RHO0 = 4100.0        # kg/m³. Seager+ 2007 Table 3, MgSiO₃ (perovskite)
SEAGER_T3_C = 0.00161          # kg m⁻³ Pa⁻ⁿ. 같은 행
SEAGER_T3_N = 0.541            # 같은 행
SEAGER_T3_TOL = 0.03           # 3 %. 두 표현은 같은 곡선의 두 적합이지 같은 식이 아니다


def seager_table3(p_pa: float) -> float:
    """Seager+ 2007 Table 3 의 병합 EOS 적합. ρ = ρ₀ + c P^n."""
    return SEAGER_T3_RHO0 + SEAGER_T3_C * p_pa ** SEAGER_T3_N


# ── 온도 ────────────────────────────────────────────────────────────────
#
# 앵커는 발표된 값이어야 한다. 온도 프로파일의 앵커는 둘이고, 둘 다 우리 출력이 아니다.
#
# Unterborn+ 2019 (arXiv:1905.06530) 이 자기 모형의 핵-맨틀 경계 온도를 반지름의 닫힌
# 형태로 적합해 실었다 (그들의 eq. 7, 포텐셜 온도 1600 K, 0.75 ≤ R ≤ 1.5 R⊕).
#
#     T_CMB(R) = 4180 R − 2764 R² + 1219 R³
#
# 그리고 그 식이 1 R⊕ 에서 내는 2635 K 를 Lay+ 2008 의 지구 값 2500–2800 K 와 대조하며
# "in good agreement" 라고 적는다. 그 구간이 이 절의 판정선이다 — 우리 계산이 아니라
# 지구에서 측정·추정된 범위다.
#
# eq. 8 은 포텐셜 온도를 옮겼을 때 CMB 온도가 얼마나 따라가는지를 준다.
#
#     ΔT_CMB(R, T_Pot) ≈ (T_Pot − 1600 K) · (0.82 + R^1.81)
UNTERBORN_TCMB = (4180.0, -2764.0, 1219.0)   # eq. 7 계수 (R 의 1·2·3차)
UNTERBORN_TCMB_RANGE = (0.75, 1.5)           # 그 적합이 유효한 반지름 구간 [R⊕]
LAY_2008_EARTH_TCMB = (2500.0, 2800.0)       # K. Unterborn+ 2019 이 인용한 지구 값
UNTERBORN_SENSITIVITY = (0.82, 1.81)         # eq. 8 의 상수와 지수
# 우리 단열선은 지구 근처에서 그 적합과 맞고 위로 갈수록 낮게 흐른다. 그 사실을
# 허용오차로 덮지 않고 **두 개의 검사** 로 나눈다 — 맞는 구간은 좁게 단정하고, 벗어나는
# 몫은 구간에 묶어서 조용히 고쳐지거나 조용히 나빠지는 것을 둘 다 잡는다. 토성의
# +20.7 % 를 test_giant.py 가 다루는 방식과 같다.
TCMB_TOL = 0.05                              # 5 %. R ≤ 1.05 R⊕ 에서
TCMB_DRIFT_BAND = (-0.22, -0.10)             # 4 M⊕ (R 1.46) 에서 기록된 초과분

# eos.py 가 얼음 절 주석에 적어둔 "이 재료의 정직한 오차폭". 기준 등온과 각 상의 구간
# 상단 사이의 밀도 차이고, SeaFreeze 와 대조해서 **잰** 값이다. 열 항이 들어왔으니
# 이제 같은 수가 **계산돼서** 나와야 한다 — 그 일치가 열 항 크기의 독립 검증이다.
ICE_THERMAL_SPREAD = (("ice_iii", 355.0e6, 256.43, 0.0011),
                      ("ice_v", 618.4e6, 272.73, 0.0027),
                      ("ice_vi", 2.216e9, 355.0, 0.013))
ICE_SPREAD_TOL = 0.15    # 상대. 0.11 % 대 0.107 % 같은 자리라 절대가 아니라 상대다


def unterborn_tcmb(radius_earth: float, t_pot: float = 1600.0) -> float:
    """Unterborn+ 2019 eq. 7 과 eq. 8. 포텐셜 온도 t_pot 에서의 CMB 온도 [K].

    eq. 7 은 1600 K 에서의 값이고, eq. 8 이 포텐셜 온도를 옮겼을 때의 이동을 준다.
    둘을 합쳐야 1600 K 아닌 천체와 대볼 수 있다."""
    a, b, c = UNTERBORN_TCMB
    r = radius_earth
    base = a * r + b * r ** 2 + c * r ** 3
    s_a, s_b = UNTERBORN_SENSITIVITY
    return base + (t_pot - 1600.0) * (s_a + r ** s_b)


# 조성별 암석 질량 상한을 재는 축. 값이 아니라 **누가 상한을 정하는가** 가 내용이다.
CEILING_CASES = (
    ("earth_like (CMF 0.325)", dict(core_mass_fraction=0.325)),
    ("pure silicate (CMF 0)", dict(core_mass_fraction=0.0)),
    ("pure iron (fe_eps)", dict(composition="iron")),
)

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


def _seafreeze_gamma() -> list[str]:
    """γ = (∂P/∂T)_V / (ρ c_V) 가 **항등식** 인지 원 표현과 대조한다.

    이 파일은 그뤼나이젠 계수를 새 상수로 들여오지 않고 열압력의 기울기와 비열에서
    닫는다. 그게 맞다는 것은 주장이 아니라 검사 대상이다 — SeaFreeze 가 자기 γ 를
    따로 들고 있으므로, 같은 상태에서 두 값을 대면 된다."""
    out: list[str] = []
    try:
        import numpy as np
        from seafreeze.seafreeze import getProp
    except ImportError:
        print("  [SKIP] SeaFreeze 가 없다 — γ 항등식 대조는 engine/.venv 에서만 돈다")
        return out
    from eos import H2O
    for name, sf_name, t_ref, p_mpa in (("ice_ih", "Ih", 273.152519, 0.101325),
                                        ("ice_iii", "III", 251.15, 1e-3),
                                        ("ice_v", "V", 256.43, 1e-3),
                                        ("ice_vi", "VI", 272.73, 1e-3)):
        ph = [x for x in H2O.phases if x.name == name][0]
        pt = np.empty((1,), dtype="object")
        pt[0] = (p_mpa, t_ref)
        want = float(getProp(pt, sf_name).gamma_Gruneisen[0])
        got = ph.gruneisen(ph.rho0, t_ref + 1.0)   # ΔT 가 0 이면 금속 2차항만 죽는다
        d = abs(got - want) / want
        ok = d < 1e-3
        if not ok:
            out.append(f"{name}: γ 항등식이 {got:.6f}, SeaFreeze 는 {want:.6f}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:8} γ {got:.6f} · SeaFreeze "
              f"{want:.6f} ({d * 100:.4f} %)")
    return out


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


_CEILING_CACHE: dict[str, tuple[float, str]] = {}


def mass_ceiling(**kwargs) -> tuple[float, str]:
    """이 조성이 풀리는 가장 큰 질량을 이분법으로 잰다. (M⊕, 상한을 정한 재료).

    **재는 것이지 적는 것이 아니다.** 상한은 재료의 성질이므로 재료가 바뀌면 움직이고,
    손으로 적어두면 그 순간 두 번째 사본이 된다."""
    key = repr(sorted(kwargs.items()))
    if key in _CEILING_CACHE:
        return _CEILING_CACHE[key]
    lo, hi = 0.5, 400.0
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        if solve(mid, **kwargs).applicable:
            lo = mid
        else:
            hi = mid
    over = solve(hi, **kwargs)
    owner = "?"
    for name in ("fe_eps", "fe_prem", "silicate", "h2o"):
        if name in over.reason:
            owner = name
            break
    _CEILING_CACHE[key] = (lo, owner)
    return lo, owner


def thermal_table() -> None:
    """문서 §Validation 의 온도 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | T_Pot (K) | T_CMB derived | Unterborn+ 2019 eq. 7–8 | Δ | "
          "R | C/MR² | grade |")
    print("|---|---|---|---|---|---|---|---|")
    for label, m, cmf, t_pot in (("Earth (reference)", 1.0, 0.325, 1600.0),
                                 ("Earth, cool mantle", 1.0, 0.325, 1400.0),
                                 ("Earth, hot mantle", 1.0, 0.325, 1900.0),
                                 ("2 M⊕ super-Earth", 2.0, 0.325, 1600.0),
                                 ("4 M⊕ super-Earth", 4.0, 0.325, 1600.0)):
        res = solve(m, core_mass_fraction=cmf, potential_temperature=t_pot)
        v = res.values
        want = unterborn_tcmb(v["radius"], t_pot)
        print(f"| {label} | {t_pot:.0f} | {v['cmb_temperature']:.0f} K | {want:.0f} K | "
              f"{(v['cmb_temperature'] / want - 1) * 100:+.1f} % | {v['radius']:.3f} R⊕ | "
              f"{v['nmoi']:.4f} | {res.grade} |")


def ceiling_table() -> None:
    """문서 §Domain 의 암석 질량 상한 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| composition | mass ceiling | what stops it | its stated ceiling | "
          "R at the ceiling | C/MR² |")
    print("|---|---|---|---|---|---|")
    from eos import MATERIALS
    for label, kwargs in CEILING_CASES:
        m, owner = mass_ceiling(**kwargs)
        res = solve(m, **kwargs)
        cap = MATERIALS[owner].p_max / 1e12 if owner in MATERIALS else float("nan")
        print(f"| {label} | {m:.2f} M⊕ | `{owner}` | {cap:.1f} TPa | "
              f"{res.values['radius']:.3f} R⊕ | {res.values['nmoi']:.4f} |")



def main() -> int:
    if "--thermal" in sys.argv:
        thermal_table()
        return 0
    if "--ceiling" in sys.argv:
        ceiling_table()
        return 0
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

    print("\n그뤼나이젠 — 새 상수가 아니라 항등식인가 (SeaFreeze 있을 때만)")
    fails += _seafreeze_gamma()

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

    print("\n규산염 상 사다리 — 23.83 GPa 부터 13.5 TPa 까지 끊긴 데가 없는가")
    # 2026-08-27 에 mgsio3_pv 가 들어와 사다리가 이어졌다. 얼음과 같은 규율이다 —
    # 전이압 상수 하나를 이웃과 어긋나게 고치면 조용히 구멍이 열리고, 그러면 솔버가
    # 답이 있는 자리에서 거절한다.
    from eos import (SILICATE, SILICATE_PREM_TO_PV, SILICATE_PV_TO_TFD,
                     MATERIALS, Phase)
    for prev, nxt in zip(SILICATE.phases, SILICATE.phases[1:]):
        cond = abs(nxt.p_min - prev.p_max) <= 1e-6 * max(prev.p_max, 1.0)
        if not cond:
            fails.append(f"규산염 사다리가 {prev.name} 상한 {prev.p_max / 1e9:.2f} GPa 와 "
                         f"{nxt.name} 하한 {nxt.p_min / 1e9:.2f} GPa 사이에서 끊겼다")
        print(f"  [{'PASS' if cond else 'FAIL'}] {prev.name:12} → {nxt.name:12} "
              f"{prev.p_max / 1e9:9.2f} GPa 에서 이어진다")

    print("\n이음매 — 지진학 적합과 DFT 적합이 3.5 TPa 에서 겹치는가")
    # 두 적합은 서로를 모른다. PREM 은 지구의 지진파에서, Seager 의 BME4 는 Karki+ 2000
    # 의 DFT 에서 왔다. 그 둘이 이 압력에서 몇 % 안에서 같다는 것이 이 자리에 상을
    # 갈아 끼우면서 밀도 도약을 지어내지 않아도 되는 근거다.
    prem, pv = SILICATE.phases[1], SILICATE.phases[2]
    d_prem, d_pv = prem.density(SILICATE_PREM_TO_PV), pv.density(SILICATE_PREM_TO_PV)
    seam = abs(d_pv - d_prem) / d_prem
    ok = seam < 0.01
    if not ok:
        fails.append(f"3.5 TPa 이음매가 {seam * 100:.2f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] PREM BM2 {d_prem:.0f} · Seager BME4 "
          f"{d_pv:.0f} kg/m³ — 차이 {seam * 100:.2f} %")

    print("\n박아둔 BME4 상수 — 같은 논문의 두 번째 표현을 재현하는가")
    # Seager+ 2007 Table 1 (BME4) 과 Table 3 (병합 곡선의 ρ₀+cPⁿ 적합) 은 같은 논문의
    # 다른 표다. 우리는 Table 1 을 옮겨 적었으므로, Table 3 을 재현하면 옮겨 적기가 맞다.
    worst_t3 = 0.0
    for p_tpa in (0.5, 1.0, 2.0, 3.5, 6.0, 10.0, 13.5):
        got, want = pv.density(p_tpa * 1e12), seager_table3(p_tpa * 1e12)
        worst_t3 = max(worst_t3, abs(got - want) / want)
    ok = worst_t3 <= SEAGER_T3_TOL
    if not ok:
        fails.append(f"BME4 가 Seager Table 3 과 {worst_t3 * 100:.1f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 0.5~13.5 TPa 에서 최악 "
          f"{worst_t3 * 100:.2f} % (허용 {SEAGER_T3_TOL * 100:.0f} %) — Table 3 "
          f"ρ = {SEAGER_T3_RHO0:.0f} + {SEAGER_T3_C} P^{SEAGER_T3_N}")

    print("\n왜 3차가 아니라 4차인가 — K₀″ 를 떼면 얼마나 달라지는가")
    # 반올림 하나가 답을 9 % 움직이는 자리라서, 이 감도는 주장이 아니라 검사 대상이다.
    implied = -(1.0 / pv.k0) * ((3.0 - pv.k0p) * (4.0 - pv.k0p) + 35.0 / 9.0)
    three = Phase("pv3", "bme3", pv.rho0, pv.k0, pv.k0p, pv.p_max, "")
    d3, d4 = three.density(SILICATE_PV_TO_TFD), pv.density(SILICATE_PV_TO_TFD)
    swing = abs(d4 - d3) / d3
    ok = swing > 0.02
    if not ok:
        fails.append(f"BME3 과 BME4 가 {swing * 100:.2f} % 밖에 안 갈린다 — "
                     f"그러면 형태를 늘릴 이유가 없었다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 상한에서 BME3 {d3:.0f} · BME4 {d4:.0f} kg/m³ "
          f"({swing * 100:.1f} %)")
    print(f"         논문이 적은 K₀″ = {pv.k0pp * 1e9:.3f} /GPa 와 3차의 암묵값 "
          f"{implied * 1e9:.5f} /GPa 는 {abs(pv.k0pp / implied - 1) * 100:.2f} % 차이다. "
          f"그 차이가 f² 항을 타고 {swing * 100:.1f} % 로 커진다 — 두 자리 유효숫자로 "
          f"적힌 상수가 하중을 받는 자리이므로, 3차로 근사하지 않는다.")
    # 그리고 적분기가 밟는 구간 전체에서 단조여야 한다. P(ρ) 가 뒤집히면 Newton 이
    # 엉뚱한 뿌리로 간다.
    rho = pv.rho0
    prev_p, mono = -1.0, True
    while rho < pv.density(SILICATE_PV_TO_TFD):
        pr = pv.pressure(rho)
        if pr < prev_p:
            mono = False
            break
        prev_p, rho = pr, rho * 1.002
    if not mono:
        fails.append("BME4 가 유효 구간 안에서 단조가 아니다")
    print(f"  [{'PASS' if mono else 'FAIL'}] 유효 구간 전체에서 P(ρ) 가 단조다")

    print("\n암석 질량 상한 — 조성마다 누가 상한을 정하는가")
    from eos import MATERIALS as _MATS
    for label, kwargs in CEILING_CASES:
        m, owner = mass_ceiling(**kwargs)
        cond = owner in _MATS
        if not cond:
            fails.append(f"질량 상한: {label} 의 거절이 재료를 이름 대지 않는다")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label:24} {m:7.2f} M⊕ 까지 — "
              f"`{owner}` 의 {_MATS[owner].p_max / 1e12:.1f} TPa 가 정한다")

    print("\n외삽 구간 — 밟으면 등급이 내려가고 note 가 이유를 대는가")
    # 3.5 TPa 아래는 측정된 행성의 적합(PREM)이고 위는 제일원리 계산이다. 답이 그 위를
    # 밟았다는 사실이 값을 받는 쪽에 보여야 한다.
    m_top, _ = mass_ceiling(core_mass_fraction=0.325)
    top = solve(m_top, core_mass_fraction=0.325)
    said = any("외삽 구간" in n for n in top.notes)
    ok = top.grade == "analog" and said
    if not ok:
        fails.append(f"외삽 구간: 등급 {top.grade}, note 가 이유를 {'댄다' if said else '안 댄다'}")
    print(f"  [{'PASS' if ok else 'FAIL'}] {m_top:.2f} M⊕ 지구조성 → grade {top.grade}, "
          f"note 가 이유를 이름 댄다")
    # 그리고 아래를 밟은 천체는 움직이면 안 된다.
    low = solve(1.0, core_mass_fraction=0.325)
    ok = low.grade == "calibrated" and not any("외삽 구간" in n for n in low.notes)
    if not ok:
        fails.append("외삽 구간 판정이 3.5 TPa 아래 천체까지 물들였다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구는 grade {low.grade} 그대로다")

    print("\n새 상한 위 — 여전히 이름을 대며 거절하는가")
    m_si, _ = mass_ceiling(core_mass_fraction=0.0)
    over = solve(m_si * 1.2, core_mass_fraction=0.0)
    named = (not over.applicable
             and "silicate" in over.reason
             and "13500" in over.reason)
    if not named:
        fails.append("새 상한 위 거절이 재료와 상한을 이름 대지 않는다")
    print(f"  [{'PASS' if named else 'FAIL'}] {m_si * 1.2:.1f} M⊕ 순규산염 — 거절이 "
          f"`silicate` 와 13500 GPa 를 이름 댄다")
    deg = "Thomas-Fermi" in over.reason or "축퇴" in over.reason
    if not deg:
        fails.append("새 상한 위 거절이 무엇이 그 위인지 말하지 않는다")
    print(f"  [{'PASS' if deg else 'FAIL'}] 그 위가 전자축퇴임을 말한다")

    print("\n온도 — 기준 포텐셜 온도에서 지구가 **비트까지** 안 움직이는가")
    # 이 작업 전체의 판정선이다. PREM 적합은 뜨거운 실제 지구를 관측한 것이라 지구의
    # 지오섬이 그 유효 ρ₀ 안에 이미 있고, 거기에 300 K 기준의 열팽창을 얹으면 지구를
    # 두 번 데운다 — 직전 세션이 목성에 중원소를 두 번 넣어 반지름을 +0.6 % 에서
    # −9.8 % 로 만든 것과 같은 함정이다. 암석-금속 상들의 기준을 1600 K 단열선으로
    # 잡았으므로 그 온도에서는 ΔT 가 항등적으로 0 이고, 그래서 허용오차가 아니라
    # **같음** 을 검사한다.
    from eos import EARTH_POTENTIAL_T
    for name, m, r_pub, cmf, nmoi_pub, f_pub, _src in ANCHORS:
        off = solve(m, core_mass_fraction=cmf)
        on = solve(m, core_mass_fraction=cmf,
                   potential_temperature=EARTH_POTENTIAL_T)
        same = (off.values["nmoi"] == on.values["nmoi"]
                and off.values["radius"] == on.values["radius"])
        if not same:
            fails.append(f"{name}: 기준 온도에서 답이 움직였다 — 이중계상이다 "
                         f"({off.values['nmoi']:.10f} → {on.values['nmoi']:.10f})")
        print(f"  [{'PASS' if same else 'FAIL'}] {name:8} C/MR² {on.values['nmoi']:.6f} · "
              f"R {on.values['radius']:.6f} — 온도를 끈 답과 비트까지 같다")
    ok = solve(1.0, core_mass_fraction=0.325,
               potential_temperature=EARTH_POTENTIAL_T).grade == "calibrated"
    if not ok:
        fails.append("기준 온도를 선언했다고 등급이 내려간다 — 답이 안 움직였는데 내려간다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 기준 온도 선언만으로는 등급이 안 내려간다")

    print("\n온도 — 옮기면 밀도가 움직이고, 방향이 맞는가")
    cool = solve(1.0, core_mass_fraction=0.325, potential_temperature=1400.0)
    hot = solve(1.0, core_mass_fraction=0.325, potential_temperature=1900.0)
    base = solve(1.0, core_mass_fraction=0.325)
    ok = (cool.values["radius"] < base.values["radius"] < hot.values["radius"])
    if not ok:
        fails.append("포텐셜 온도를 올렸는데 반지름이 커지지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 1400 K {cool.values['radius']:.5f} < "
          f"1600 K {base.values['radius']:.5f} < 1900 K {hot.values['radius']:.5f} R⊕ — "
          f"뜨거우면 부풀고 차가우면 줄어든다")
    swing = (hot.values["radius"] - cool.values["radius"]) / base.values["radius"]
    ok = 0.0005 < swing < 0.05
    if not ok:
        fails.append(f"1400~1900 K 에서 반지름이 {swing * 100:.2f} % 움직인다 — "
                     f"배선이 끊겼거나 과하다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 1400~1900 K 폭에서 반지름이 {swing * 100:.2f} % "
          f"움직인다. Seager+ 2007 §IV.2.2 가 평균밀도 3.5 % 오차를 반지름 1.2 % 로 "
          f"환산해 두었고, 같은 자릿수다")
    for label, res in (("1400 K", cool), ("1900 K", hot)):
        ok = res.grade == "analog" and any("선언에 기댄다" in n for n in res.notes)
        if not ok:
            fails.append(f"온도 {label}: 등급이 {res.grade} 이고 이유를 note 가 안 적는다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} → grade {res.grade}, note 가 이유를 댄다")

    print("\n핵 온도 — 발표된 지구 값 안에 떨어지는가 (core_state 가 이걸 먹는다)")
    # 우리 출력으로 우리를 시험하지 않는다. 대는 상대는 Unterborn+ 2019 eq. 7 과
    # 그들이 인용한 Lay+ 2008 의 지구 값이다.
    e = solve(1.0, core_mass_fraction=0.325, potential_temperature=EARTH_POTENTIAL_T)
    t_cmb = e.values["cmb_temperature"]
    lo, hi = LAY_2008_EARTH_TCMB
    ok = lo <= t_cmb <= hi
    if not ok:
        fails.append(f"지구 CMB 온도 {t_cmb:.0f} K 가 Lay+ 2008 의 {lo:.0f}–{hi:.0f} K 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구 CMB {t_cmb:.0f} K · Lay+ 2008 "
          f"{lo:.0f}–{hi:.0f} K · Unterborn+ 2019 eq. 7 {unterborn_tcmb(e.values['radius']):.0f} K")
    from interior import UNTERBORN_TCMB_MAX_R
    near, far = 0.0, None
    for m in (0.5, 1.0, 2.0, 4.0):
        res = solve(m, core_mass_fraction=0.325, potential_temperature=EARTH_POTENTIAL_T)
        r = res.values["radius"]
        if not UNTERBORN_TCMB_RANGE[0] <= r <= UNTERBORN_TCMB_RANGE[1]:
            continue        # 그 적합이 유효한 반지름 구간 밖은 대지 않는다
        d = res.values["cmb_temperature"] / unterborn_tcmb(r) - 1.0
        if r <= UNTERBORN_TCMB_MAX_R:
            near = max(near, abs(d))
        else:
            far = d if far is None else min(far, d)
        print(f"         {m:4.1f} M⊕ (R {r:.3f}) → {res.values['cmb_temperature']:.0f} K · "
              f"eq. 7 {unterborn_tcmb(r):.0f} K ({d * 100:+.1f} %)")
    ok = near <= TCMB_TOL
    if not ok:
        fails.append(f"R ≤ {UNTERBORN_TCMB_MAX_R} R⊕ 에서 CMB 온도가 eq. 7 과 "
                     f"{near * 100:.1f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] R ≤ {UNTERBORN_TCMB_MAX_R:.2f} R⊕ 에서 최악 "
          f"{near * 100:.1f} % (허용 {TCMB_TOL * 100:.0f} %)")
    # 위쪽은 **맞지 않는 것이 답** 이다. 초과분을 구간에 묶어 둔다.
    ok = far is not None and TCMB_DRIFT_BAND[0] <= far <= TCMB_DRIFT_BAND[1]
    if not ok:
        fails.append(f"큰 천체의 CMB 온도 초과분 {far} 가 기록된 구간 "
                     f"{TCMB_DRIFT_BAND} 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 그 위에서는 낮게 흐른다 — 최악 "
          f"{far * 100:+.1f} % (기록된 구간 {TCMB_DRIFT_BAND[0] * 100:.0f}~"
          f"{TCMB_DRIFT_BAND[1] * 100:.0f} %)")
    print(f"         αK_T 를 부피에 무관하다고 둔 Anderson & Goto 근사가 γ 를 1/ρ 로 "
          f"떨어뜨리는데, Debye 모형으로 α(P,T)·C_P(P,T) 를 푸는 Unterborn 쪽은 그렇게 "
          f"빨리 떨어지지 않는다. 그래서 이 갈래가 '대조됐다' 고 말할 수 있는 자리를 "
          f"{UNTERBORN_TCMB_MAX_R:.2f} R⊕ 로 좁게 잡고, 그 위는 note 가 편향을 이름 댄다.")
    # eq. 8 — 포텐셜 온도를 옮겼을 때의 민감도. 같은 논문의 두 번째 표현이다.
    a, b = UNTERBORN_SENSITIVITY
    want = a + e.values["radius"] ** b
    got = (hot.values["cmb_temperature"] - cool.values["cmb_temperature"]) / 500.0
    ok = abs(got / want - 1.0) <= 0.25
    if not ok:
        fails.append(f"CMB 온도 민감도 {got:.2f} 가 eq. 8 의 {want:.2f} 와 25 % 넘게 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] dT_CMB/dT_Pot {got:.2f} · eq. 8 이 주는 "
          f"{want:.2f} ({(got / want - 1) * 100:+.0f} %)")

    print("\n얼음 — 열 항이 이 파일이 이미 적어둔 오차폭을 재현하는가")
    # eos.py 의 얼음 절이 기준 등온 대비 구간 상단의 밀도 차를 III 0.11 % · V 0.27 % ·
    # VI 1.3 % 로 적어 두었다. 그 수는 SeaFreeze 와 대조해 **잰** 것이고, 열 항은
    # 전혀 다른 상수(αK_T)에서 온다. 둘이 맞으면 열 항의 크기가 독립 검증된 것이다.
    from eos import H2O
    for name, p_top, t_top, want_frac in ICE_THERMAL_SPREAD:
        ph = [x for x in H2O.phases if x.name == name][0]
        got = ph.density(p_top) / ph.density(p_top, t=t_top) - 1.0
        d = abs(got / want_frac - 1.0)
        ok = d <= ICE_SPREAD_TOL
        if not ok:
            fails.append(f"{name}: 열 항이 {got * 100:.3f} %, 파일이 적어둔 값은 "
                         f"{want_frac * 100:.2f} %")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:8} 구간 상단 {t_top:.2f} K 에서 "
              f"{got * 100:.3f} % · 주석에 적힌 {want_frac * 100:.2f} % "
              f"({d * 100:.0f} % 차)")

    print("\n열 상수가 없는 상 — 있는 척하지 않고 이름을 대는가")
    from eos import H_HE, MATERIALS as _M
    for mat, want in ((_M["h2o"], "ice_vii"), (H_HE, "hhe_n1")):
        cold = mat.cold_phases()
        ok = want in cold
        if not ok:
            fails.append(f"{mat.name}: 등온으로 남는 상을 {want} 로 이름 대지 않는다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {mat.name:9} 등온으로 남는 상 {cold}")
    for mat in (_M["silicate"], _M["fe_prem"], _M["fe_eps"]):
        ok = mat.has_thermal
        if not ok:
            fails.append(f"{mat.name}: 열 상수가 있어야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {mat.name:9} 전 상에 열 상수가 있다")
    icy = solve(0.0248, core_mass_fraction=0.0, ice_mass_fraction=0.407,
                potential_temperature=250.0)
    said = icy.applicable and any("ice_vii" in n for n in icy.notes)
    if not said:
        fails.append("얼음 천체의 결과가 등온으로 남는 상을 note 에 이름 대지 않는다")
    print(f"  [{'PASS' if said else 'FAIL'}] 얼음 천체 결과의 note 가 그 사실을 싣고 온다")

    print("\n거절 — 온도가 뜻을 잃으면 이름을 대는가")
    zero = solve(1.0, core_mass_fraction=0.325, potential_temperature=0.0)
    base_off = solve(1.0, core_mass_fraction=0.325)
    # 0 은 None 과 같은 '선언 안 함' 이다 — φ₀ · envelope_z 와 같은 규율이다.
    ok = zero.applicable and zero.values["nmoi"] == base_off.values["nmoi"]
    neg = solve(1.0, core_mass_fraction=0.325, potential_temperature=-5.0)
    ok = ok and not neg.applicable and "음수다" in neg.reason
    if not ok:
        fails.append("음수 포텐셜 온도를 이름 대며 거절하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 음수 포텐셜 온도는 거절하고, 0/None 은 "
          f"'판정하지 않는다' 로 읽는다")

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
