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
import math
from eos import EARTH_POTENTIAL_T as _NL_EARTH_T
from interior import (EARTH_MASS_KG, EARTH_RADIUS_M, infer_composition,
                      infer_three_layer, solve)
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
    # 2026-08-27 까지 이 자리는 1 M⊕ 였다. 얼음 X 가 들어와 그 천체가 풀리므로,
    # 같은 거절을 **새 울타리** 에서 다시 건다 — 천장을 없앤 게 아니라 옮긴 것이다.
    # 30 M⊕ 다. 8.0 이었는데 그 천체는 **풀린다** — 8.0 의 거절은 물리가 아니라
    # 괄호잡기가 버릴 시험압에서 얼음을 깬 것이었고, 그 결함을 이 검사가 못 박고
    # 있었다 (2026-08-27 에 고침). 지금 값은 수렴해의 얼음 기둥이 실제로 1 TPa 를
    # 넘는 자리이고, 프리셋의 실제 상한은 21.68 M⊕ 다.
    ("물이 아주 많은 큰 천체", dict(mass_earth=30.0, composition="water"),
     "근거 구간을 벗어난다", "얼음 기둥이 French & Redmer 표현의 1 TPa 상한을 넘는다"),
    # 거대행성은 2026-08-26 에 풀리게 됐다 (test_giant.py). 아직 밖인 유체 천체가
    # 이름을 대며 거절하는지는 여기서 계속 지킨다.
    ("갈색왜성", dict(mass_earth=5000.0, body_class="brown_dwarf"),
     "중수소", "13 M_J 위는 광도 이력이 필요하다"),
    # 얼음거대행성은 2026-08-27 에 열렸다. 남은 거절은 **온도를 선언하지 않은 경우** 이고,
    # 그건 이 갈래의 성질이다 — 유체 물의 적합은 P(ρ,T) 가 통째로 하나라 온도가 인자다.
    ("온도 없는 얼음 자이언트", dict(mass_earth=17.0, body_class="ice_giant",
                            core_mass_fraction=0.0, ice_mass_fraction=0.8,
                            gas_mass_fraction=0.13),
     "등온으로 풀 수 없다", "유체 물은 온도가 인자라 등온 경로가 없다"),
    ("얼음 없는 얼음 자이언트", dict(mass_earth=17.0, body_class="ice_giant",
                            core_mass_fraction=0.0, ice_mass_fraction=0.0,
                            gas_mass_fraction=0.13, potential_temperature=2500.0),
     "얼음거대행성이 아니다", "이 클래스를 이름 그대로 만드는 층이 없다"),
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
# 2026-08-29 까지 다섯 중 Ganymede 만 판정선이었고, 나머지 넷은 "자유 분율 하나만 푸는 2층
# 구조라서 못 맞히는 천체" 라고 적혀 있었다. 바다와 3층 역산이 들어온 뒤 그 문장은 시험됐다 —
# `--icy` 가 다섯 천체의 (핵, 얼음) 띠를 내고 발표 C/MR² 가 그 띠 안인지 말한다. 안이면
# 층이 모자랐던 것이고, 밖이면 이유가 다른 이름을 얻는다 (암석의 밀도, 부분 분화). 기본
# 실행은 Ganymede(2층, 예전 그대로)와 Europa(3층, 좁히기까지)를 판정선으로 든다. C/MR² 값은
# 전부 ADS 전문에서 확인했다.
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


# ── 녹는곡선 ────────────────────────────────────────────────────────────
#
# 앵커는 발표된 값이어야 한다. 녹는곡선의 앵커는 셋이고 셋 다 우리 출력이 아니다.
#
# IAPWS R14-08(2011) §7 은 "프로그램 검증용" 이라고 이름 붙여 각 식마다 계산값을 하나씩
# 싣는다. 그 표를 그대로 다시 낸다 — 이 파일이 그 식을 옮겨 적었는지를 재는 자리다.
IAPWS_TABLE3 = (("ice_ih", 260.0, 138.268),
                ("ice_iii", 254.0, 268.685),
                ("ice_v", 265.0, 479.640),
                ("ice_vi", 320.0, 1356.76),
                ("ice_vii", 550.0, 6308.71))     # (상, T [K], p [MPa])
IAPWS_TABLE3_TOL = 5e-6      # 표가 실은 자릿수만큼

# 철의 융해온도. 발표된 두 실험과 두 계산이 내핵 경계(330 GPa)에서 무엇을 말하는가.
FE_ICB_GPA = 330.0
FE_ICB_ANCHORS = (("Anzellini+ 2013 (2013Sci...340..464A)", 6230.0, 500.0),
                  ("Sinmyo+ 2019 (2019E&PSL.510...45S)", 5500.0, 220.0))
FE_ZERO_P_MELT = 1811.0      # K. 상압 철의 녹는점. 곡선의 T₀ 가 이 근처여야 한다
FE_ZERO_P_TOL = 0.02


# ── 얼음 X ──────────────────────────────────────────────────────────────
#
# 이 상은 이 사다리에서 **읽은 게 아니라 적합한** 유일한 얼음이다. 그래서 재는 것이
# 두 가지다 — 적합이 자기 출처를 얼마나 재현하는가, 그리고 이음매가 얼마나 벌어지는가.
# 둘 다 eos.py 주석에 수로 적혀 있으므로, 여기서 다시 재서 그 수가 맞는지를 본다.
ICE_X_FIT_WORST = 0.01475      # 상대. 37.4 GPa–1 TPa 의 300 K 등온선에서
ICE_X_FIT_TOL = 0.10           # 그 수 자체의 허용 표류 (상대)
ICE_X_SEAM = -0.0226           # 37.4 GPa 에서 ice_vii BME 대비 ice_x Vinet
ICE_X_SEAM_TOL = 0.10
# 초이온상. Millot+ 2019 (2019Natur.569..251M) 초록이 적는 하한이고, 우리 온도 천장이
# 그 **아래** 에 서 있다는 것이 검사 대상이다 — 위에 서 있으면 초이온상을 얼음 X 라고
# 부르게 된다.
MILLOT_SUPERIONIC = (100.0e9, 2000.0)


def unterborn_tcmb(radius_earth: float, t_pot: float = 1600.0) -> float:
    """Unterborn+ 2019 eq. 7 과 eq. 8. 포텐셜 온도 t_pot 에서의 CMB 온도 [K].

    eq. 7 은 1600 K 에서의 값이고, eq. 8 이 포텐셜 온도를 옮겼을 때의 이동을 준다.
    둘을 합쳐야 1600 K 아닌 천체와 대볼 수 있다."""
    a, b, c = UNTERBORN_TCMB
    r = radius_earth
    base = a * r + b * r ** 2 + c * r ** 3
    s_a, s_b = UNTERBORN_SENSITIVITY
    return base + (t_pot - 1600.0) * (s_a + r ** s_b)


# ── 두 번째 앵커: Noack & Lasbleis 2020 ─────────────────────────────────
#
# Noack & Lasbleis 2020, A&A 638, A129 (2020A&A...638A.129N, 오픈 액세스, PDF 가 캐시에 있다) 가
# 자기 내부구조 모형의 맨틀 단열선을 핵-맨틀 경계까지 끌고 간 매개변수화를 싣는다. 0.8 ~ 2 M⊕,
# 지구형 조성(Fe·Mg·Si·O), 그들의 §7 이 "We limited our mass range to two Earth masses" 라고
# 적는다. 상수는 전부 PDF 에서 직접 읽었다 (2026-08-30).
#
#   (5)  R_p [km]     = (7030 − 1840 X_Fe) (M/M⊕)^0.282          X_Fe = 행성 전체의 철 질량분율
#   (9)  R_c,hot [km] = 4850 X_CMF^0.328 (M/M⊕)^0.266
#   (13) g_0 = G M / (R_p·1000)²        (14) g_CMB = G X_CMF M / (R_c·1000)²
#   (15) g_m,av = (g_0 + g_CMB) / 2
#   (18) α_m,av [1/K] = (13 + 0.738 X_CMF − 11 (M/M⊕)^0.04) × 10⁻⁵
#   (19) C_p,m,av [J/kg/K] = 1275 − 585 #FeM^1.06
#   (22) T_CMB,cold = T_um · exp( dT · g_m,av α_m,av / C_p,m,av · (R_p − R_c,hot − D_l)·1000 )
#        T_um = 2000 K ("for simplicity") at the bottom of the lithosphere, D_l = 250 km, dT ≈ 0.5
#
# **식 (20)(21) 은 쓰지 않는다.** T_CMB,hot · T_CMB,warm 은 마그마 오션 직후의 **초기** 온도이고
# (Stixrude 2014 융해곡선 위, 지구에서 4800 / 4300 K 쯤), 논문이 일부러 "문헌값을 수천 K 초과한다"
# 고 주장하는 값이다. 현재 단열선과 댈 수 있는 것은 (22) 하나다.
#
# **앵커가 다르다는 것을 적어 둔다.** (22) 는 250 km 깊이에서 2000 K 를 출발점으로 쓰고, 이 레시피는
# 표면 포텐셜 온도 1600 K 에서 출발한다 (Unterborn 의 eq. 7 도 그렇다). 그래서 두 가지를 잰다 —
# (A) 식 (22) 를 인쇄된 그대로(T_um = 2000 K) 와 엔진의 CMB 온도, (B) 식의 지수 인자
# exp(…) 와 엔진의 T_CMB / T(250 km) 비. (B) 가 단열선 **기울기** 의 비교이고 (A) 는 출발점 선택까지
# 섞인 비교다.
NL2020_RP = (7030.0, 1840.0, 0.282)          # Noack & Lasbleis eq. 5 (not Unterborn's eq. 8 above)
NL2020_RC_HOT = (4850.0, 0.328, 0.266)       # Noack & Lasbleis eq. 9
NL2020_ALPHA = (13.0, 0.738, 11.0, 0.04)     # Noack & Lasbleis eq. 18, × 1e-5
NL2020_CP = (1275.0, 585.0, 1.06)            # Noack & Lasbleis eq. 19
NL2020_T_UM = 2000.0                         # K, Noack & Lasbleis eq. 22
NL2020_D_L_KM = 250.0                        # km, Noack & Lasbleis eq. 22
NL2020_DT = 0.5                              # Noack & Lasbleis eq. 22 의 경험 인자
NL2020_FE_M = 0.1                            # 지구형 맨틀 철 수 (§2.2, "best resembles Earth")
NL2020_MASS_RANGE = (0.8, 2.0)               # M⊕
NL2020_G = 6.67384e-11                       # 논문이 적은 G
NL2020_M_EARTH = 5.972e24                    # 논문이 적은 M⊕ [kg]
# 재는 값. 엔진 기하(R_p · R_c 는 엔진 출력)에서 식 (22) 가 내는 T_CMB 와 엔진 T_CMB 의 비 − 1 의
# 구간, 0.8 ~ 2 M⊕. 2026-08-30 에 잰 구간이고, 여기서 나가면 무엇이 움직였는지 봐야 한다.
NL2020_BAND = (-0.03, 0.0)                   # (A), 엔진 / 식 (22) − 1: 잰 값 −2.2 % (0.8 M⊕) → −0.8 % (2 M⊕)
NL2020_SLOPE_BAND = (0.10, 0.16)             # (B), 엔진 상승비 / 식의 지수 인자 − 1: 잰 값 +11.6 ~ +13.5 %
NL2020_EARTH_TCMB = 2563.0                   # K. 식 (22) 를 엔진의 지구 기하에 넣은 값 — 조사가 보고한 2562 K 의 독립 재현
ANCHOR_SPREAD_BAND = (0.04, 0.10)            # 두 앵커가 서로 어긋나는 폭 (Unterborn / N&L − 1), 1 → 2 M⊕


def nl2020_exponent(mass_earth: float, radius_km: float, core_radius_km: float,
                    x_cmf: float, fe_m: float = NL2020_FE_M) -> float:
    """식 (22) 의 지수 인자 exp(dT · g α / C_p · (R_p − R_c − D_l)·1000)."""
    m_kg = mass_earth * NL2020_M_EARTH
    g0 = NL2020_G * m_kg / (radius_km * 1000.0) ** 2
    g_cmb = NL2020_G * x_cmf * m_kg / (core_radius_km * 1000.0) ** 2
    g_av = 0.5 * (g0 + g_cmb)
    a0, a1, a2, a3 = NL2020_ALPHA
    alpha = (a0 + a1 * x_cmf - a2 * mass_earth ** a3) * 1e-5
    c0, c1, c2 = NL2020_CP
    c_p = c0 - c1 * fe_m ** c2
    depth_m = (radius_km - core_radius_km - NL2020_D_L_KM) * 1000.0
    return math.exp(NL2020_DT * g_av * alpha / c_p * depth_m)


def nl2020_tcmb(mass_earth: float, radius_km: float, core_radius_km: float,
                x_cmf: float, fe_m: float = NL2020_FE_M) -> float:
    """식 (22) 그대로 — T_um = 2000 K 에서 출발한 CMB 온도 [K]."""
    return NL2020_T_UM * nl2020_exponent(mass_earth, radius_km, core_radius_km, x_cmf, fe_m)


def nl2020_geometry(mass_earth: float, x_cmf: float, x_fe: float) -> tuple[float, float]:
    """논문 자신의 기하 — 식 (5) 의 R_p 와 식 (9) 의 R_c,hot [km]."""
    r0, r1, re = NL2020_RP
    c0, ce1, ce2 = NL2020_RC_HOT
    return ((r0 - r1 * x_fe) * mass_earth ** re, c0 * x_cmf ** ce1 * mass_earth ** ce2)


def _mantle_t_at_depth(res, depth_km: float = NL2020_D_L_KM) -> float:
    """엔진의 맨틀 온도를 깊이 depth_km 에서 읽는다 — 풀린 중심에서 한 번 더 적분하며
    규산염 밀도 호출의 (P, T) 를 모아, 그 깊이의 정수압(ρ g h, 표면 g 와 상부 맨틀 밀도)에서 보간."""
    import eos as _eos
    v = res.values
    m_kg = v["mass_earth"] * EARTH_MASS_KG if "mass_earth" in v else res.inputs["mass_earth"] * EARTH_MASS_KG
    samples: list[tuple[float, float]] = []
    orig = _eos.Material.density

    def rec(self, p, t=0.0, t_pot=0.0, _o=orig):
        if self.name == "silicate" and t > 0.0:
            samples.append((p, t))
        return _o(self, p, t, t_pot)
    _eos.Material.density = rec
    try:
        st = interior.integrate(v["core_pressure"] * 1e9, m_kg, res.inputs["core_mass_fraction"], 0.0,
                                "fe_prem", t_center=v["core_temperature"], t_pot=_NL_EARTH_T)
    finally:
        _eos.Material.density = orig
    g = interior.G * m_kg / st.radius_m ** 2
    rho_um = _eos.MATERIALS["silicate"].density(1e9, _NL_EARTH_T, _NL_EARTH_T)
    p_depth = rho_um * g * depth_km * 1000.0
    samples.sort()
    for (p0, t0), (p1, t1) in zip(samples, samples[1:]):
        if p0 <= p_depth <= p1:
            return t0 + (t1 - t0) * (p_depth - p0) / (p1 - p0)
    return samples[0][1] if samples else 0.0


def adiabat_window_table() -> list[dict]:
    """0.8 ~ 2 M⊕ 지구형에서 엔진 · Unterborn eq. 7 · Noack & Lasbleis eq. (22) 를 나란히."""
    out = []
    for m in (0.8, 1.0, 1.2, 1.5, 2.0):
        res = solve(m, core_mass_fraction=0.325, potential_temperature=_NL_EARTH_T)
        v = res.values
        r_km = v["radius"] * EARTH_RADIUS_M / 1e3
        rc_km = v["core_radius"] * EARTH_RADIUS_M / 1e3
        t_engine = v["cmb_temperature"]
        t_nl = nl2020_tcmb(m, r_km, rc_km, 0.325)
        rp_paper, rc_paper = nl2020_geometry(m, 0.325, 0.35)
        t_nl_paper = nl2020_tcmb(m, rp_paper, rc_paper, 0.325)
        t_unt = unterborn_tcmb(v["radius"]) if UNTERBORN_TCMB_RANGE[0] <= v["radius"] <= UNTERBORN_TCMB_RANGE[1] else None
        t_depth = _mantle_t_at_depth(res)
        out.append(dict(mass=m, radius=v["radius"], r_km=r_km, rc_km=rc_km, t_engine=t_engine,
                        t_nl=t_nl, t_nl_paper=t_nl_paper, rp_paper=rp_paper, rc_paper=rc_paper,
                        t_unt=t_unt, t_depth=t_depth,
                        rise_engine=t_engine / t_depth if t_depth else float("nan"),
                        rise_nl=nl2020_exponent(m, r_km, rc_km, 0.325), grade=res.grade))
    return out


def print_adiabat_window() -> None:
    print("| M (M⊕) | R (R⊕) | engine T_CMB | N&L eq. 22 (engine R_p, R_c) | Δ | N&L eq. 22 (paper R_p, R_c) | Δ | Unterborn eq. 7 | Δ | engine T(250 km) | rise engine | rise eq. 22 | Δ |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in adiabat_window_table():
        du = "–" if r["t_unt"] is None else f"{r['t_unt']:.0f} K | {(r['t_engine'] / r['t_unt'] - 1) * 100:+.1f} %"
        print(f"| {r['mass']:.1f} | {r['radius']:.3f} | {r['t_engine']:.0f} K | {r['t_nl']:.0f} K | "
              f"{(r['t_engine'] / r['t_nl'] - 1) * 100:+.1f} % | {r['t_nl_paper']:.0f} K | "
              f"{(r['t_engine'] / r['t_nl_paper'] - 1) * 100:+.1f} % | {du} | {r['t_depth']:.0f} K | "
              f"{r['rise_engine']:.3f} | {r['rise_nl']:.3f} | {(r['rise_engine'] / r['rise_nl'] - 1) * 100:+.1f} % |")


# ── Kimura & Murakami 2023 — Reinhardt 액체선의 측정 검사 (F1) ─────────────────
#
# 2023JChPh.158m4504K, PDF 가 캐시에 있다. Table I 에서 옮겼다 (열: P + P_th [GPa], T [K], 괄호 불확도).
# 같은 압력 묶음에서 **가장 낮은** 액체 관측 온도가 융해온도다 — 융해는 "appearance of the Brillouin
# peaks derived from the liquid phase" 로 판정하고, 더 뜨거운 행은 융해점 위의 액체다 (그들의 eq. (2)
# 가 31 GPa 에서 1316 K 를 내어 1300 K 행 옆에 선다). 별표 행(7.8 ~ 21.3 GPa)은 Queyroux 곡선에서
# **추정한** 온도라 측정이 아니고, 여기 넣지 않는다. 기준: |Reinhardt − Kimura| ≤ Kimura 의 불확도.
KIMURA_TABLE_I = ((25.9, 1300.0, 140.0), (30.7, 1300.0, 140.0), (37.2, 1530.0, 140.0),
                  (41.1, 1570.0, 140.0), (47.3, 1730.0, 140.0), (49.6, 1770.0, 140.0),
                  (51.5, 1860.0, 140.0), (53.5, 1910.0, 140.0))
KIMURA_INSIDE_MIN = 6            # 2026-08-30 에 잰 값: Reinhardt 구간 안 7 점 중 6 점이 불확도 안
# Kimura & Murakami eq. (2): Simon–Glatzel, Queyroux+ 2020 의 삼중점(14.6 GPa · 850 K)에 앵커
KIMURA_SIMON = (14.6, 850.0, 21.0, 1.32)     # P_ref [GPa], T_ref [K], A, C
KIMURA_SEAM_BAND = (0.10, 0.20)              # eq. (2) / Reinhardt − 1 at 20.6 GPa, 잰 값 +13.9 %


# ── antigorite (C10) — 옮겨 적기 검산 ────────────────────────────────────
#
# Hilairet+ 2006 (2006GeoRL..33.2302H) 는 ρ₀ 를 인쇄하지 않는다. eos.py 가 구조식과 m = 1 부피에서
# 도출했으므로 여기서 **다시** 도출해 같은 수가 나오는지, 그리고 논문의 인쇄값 셋에 대는지를 본다.
HILAIRET_FORMULA = (("Mg", 2.62), ("Fe", 0.16), ("Al", 0.15 + 0.04), ("Si", 1.96), ("O", 5.0),
                    ("OH", 3.57))                 # §2 [6] (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)(Si₁.₉₆Al₀.₀₄)O₅(OH)₃.₅₇
HILAIRET_V_M1_A3 = 172.0                          # Å³, §4 [15] "V₀ corresponding to m = 1 … 172 Å³"
HILAIRET_V0_A3 = 2926.23                          # Å³, §3 [13] BM2 cell volume
HILAIRET_POLYSOME_M = 17                          # Capitani & Mellini 2004, the structure used to index
HILAIRET_PRINTED_DENSITY = (5.7e9, 470.0 + 273.15, 2765.0)   # §4: "at 5.7 GPa and 470°C … 2765 kg·m⁻³"
ATOMIC_MASS_U = {"Mg": 24.305, "Fe": 55.845, "Al": 26.982, "Si": 28.086, "O": 15.999, "OH": 17.007}
AMU_KG = 1.66053907e-27


SERPENTINE_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)


def print_serpentine_bands() -> None:
    """C10 — 세 위성의 3층 띠를 사문석화 분율마다 다시 돌린다 (한 위성에 몇 분). 문서 §Validation 의
    표가 이것으로 만들어졌고, 게이트에는 넣지 않는다."""
    print("| moon | published | " + " | ".join(f"band top f = {f}" for f in SERPENTINE_GRID) + " |")
    print("|---|---|" + "---|" * len(SERPENTINE_GRID))
    for name, mkg, r_km, nmoi_pub, _src, _gate in ICY_ANCHORS:
        if name not in ("Callisto", "Titan", "Enceladus"):
            continue
        tops = []
        for f in SERPENTINE_GRID:
            res = infer_three_layer(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M, ICY_T_POT,
                                    nmoi=nmoi_pub, serpentinisation=f)
            tops.append(f"{res.values['nmoi_high']:.4f}" if res.applicable else "declined")
        print(f"| {name} | {nmoi_pub:.4f} | " + " | ".join(tops) + " |")


MIDDLE_RUNG_T_POT = 200.0                      # 지각이 녹는곡선 아래에 서는 선언 온도 (270 K 는 거절된다)
MIDDLE_RUNG_FRONTS = (1.0, 0.9, 0.8, 0.7, 0.6)
MIDDLE_RUNG_ROCK = (0.3, 0.6)


def print_middle_rung_bands() -> None:
    """C11 — Callisto·Titan 의 3층 띠를 분화 전선 × 지각 암석분율 격자로 다시 돌린다 (한 점에 1–6 분).
    선언 격자는 위 상수이고 맞추지 않는다. 문서 §Validation 의 표가 이것으로 만들어졌고 게이트에는 안 넣는다.
    270 K 에서는 지각이 녹는곡선 위라 거절되므로 200 K 에서 돌리고, 지각 없는 기준(전선 1.0)도 같은 온도로 낸다."""
    print(f"T_pot = {MIDDLE_RUNG_T_POT:.0f} K · 전선 {MIDDLE_RUNG_FRONTS} · 지각 암석 {MIDDLE_RUNG_ROCK}")
    print("| moon | published | front | X_d | band (low–high) | members |")
    print("|---|---|---|---|---|---|")
    for name, mkg, r_km, nmoi_pub, _src, _gate in ICY_ANCHORS:
        if name not in ("Callisto", "Titan"):
            continue
        for f in MIDDLE_RUNG_FRONTS:
            for xd in (MIDDLE_RUNG_ROCK if f < 1.0 else (0.0,)):
                res = infer_three_layer(mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M, MIDDLE_RUNG_T_POT,
                                        nmoi=nmoi_pub, differentiation_front=f, crust_rock_fraction=xd)
                if res.applicable:
                    band = f"{res.values['nmoi_low']:.4f}–{res.values['nmoi_high']:.4f}"
                    mem = " · ".join(f"핵 {m['core_mass_fraction']:.2f}/얼음 {m['ice_mass_fraction']:.3f}/{m['nmoi']:.4f}"
                                     for m in res.values["members"])
                else:
                    band, mem = "declined", (res.reason or "")[:80]
                print(f"| {name} | {nmoi_pub:.4f} | {f} | {xd} | {band} | {mem} |")


# 조성별 암석 질량 상한을 재는 축. 값이 아니라 **누가 상한을 정하는가** 가 내용이다.
CEILING_CASES = (
    ("earth_like (CMF 0.325)", dict(core_mass_fraction=0.325)),
    ("pure silicate (CMF 0)", dict(core_mass_fraction=0.0)),
    ("pure iron (fe_eps)", dict(composition="iron")),
    # 앞의 셋은 **안쪽** 재료가 상한을 정한다 — 중심이 그 재료 안에 있으므로 그
    # 검사는 맞고, 괄호잡기 수정에도 한 자리도 안 움직였다. water 만 다르다: 얼음이
    # 바깥층이라 상한을 정하는 것이 중심에 있지 않은 재료이고, 그래서 이 프리셋만
    # 시험압이 버려질 자리에서 깨지는 결함에 걸렸다. 그 대비가 이 행의 내용이다.
    ("water (ice 0.50, 얼음이 바깥층)", dict(composition="water")),
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


ICE_CEILING_CASES = (
    ("water 프리셋 (얼음 0.50 · 핵 0.163)", dict(composition="water")),
    ("얼음질량분율 0.25", dict(core_mass_fraction=0.163, ice_mass_fraction=0.25)),
    ("얼음질량분율 0.75", dict(core_mass_fraction=0.0, ice_mass_fraction=0.75)),
    ("순수 얼음", dict(core_mass_fraction=0.0, ice_mass_fraction=1.0)),
)


def ice_mass_ceiling(**kwargs) -> float:
    """얼음이 있는 조성이 풀리는 가장 큰 질량 [M⊕].

    `mass_ceiling` 과 달리 아래로 0.5 M⊕ 밑까지 내려간다. 2026-08-27 의 water 프리셋
    상한이 0.0398 M⊕ 였고, 그 자리를 못 재면 이 작업이 무엇을 열었는지도 못 잰다."""
    lo, hi = 1e-4, 400.0
    if solve(hi, **kwargs).applicable:
        return hi
    for _ in range(45):
        mid = (lo * hi) ** 0.5
        if solve(mid, **kwargs).applicable:
            lo = mid
        else:
            hi = mid
    return lo


def _ice_x_crosscheck() -> list[str]:
    """얼음 X 의 Vinet 이 자기 출처(French & Redmer 2015) 를 재현하는가.

    **이 상은 읽은 게 아니라 적합한 것이다.** 그래서 III·V·VI 처럼 '상수가 표류했는가'
    를 묻는 것으로는 부족하고, 곡선 전체가 원 표현에서 얼마나 벗어나는지를 재야 한다.
    그 수(1.475 %)가 eos.py 주석에 적혀 있으므로 여기서 다시 잰다. SeaFreeze 가 없으면
    건너뛴다 — check.sh 는 무거운 의존성 없이 돌아야 한다."""
    try:
        import numpy as np
        from seafreeze.seafreeze import defpath, getProp
    except ImportError:
        print("  [SKIP] SeaFreeze 가 없다 — 얼음 X 적합 대조는 engine/.venv 에서만 돈다")
        return []
    from eos import H2O, ICE_VII_TO_X, ICE_VII_X_REF_T, ICE_X_P_MAX
    icex = [x for x in H2O.phases if x.name == "ice_x"][0]
    ps = [ICE_VII_TO_X * (ICE_X_P_MAX / ICE_VII_TO_X) ** (i / 40.0)
          for i in range(41)]
    arr = np.array([np.array([q / 1e6 for q in ps]),
                    np.array([ICE_VII_X_REF_T])], dtype=object)
    want = np.asarray(getProp(arr, "VII_X_French", defpath, "rho").rho, float).ravel()
    worst = max(abs(icex.density(q) - w) / w for q, w in zip(ps, want))
    bad: list[str] = []
    ok = abs(worst / ICE_X_FIT_WORST - 1.0) <= ICE_X_FIT_TOL
    if not ok:
        bad.append(f"ice_x 적합이 원 표현에서 {worst * 100:.3f} % 벗어난다, "
                   f"기록된 값은 {ICE_X_FIT_WORST * 100:.3f} %")
    print(f"  [{'PASS' if ok else 'FAIL'}] ice_x  {ICE_VII_TO_X / 1e9:.1f}–"
          f"{ICE_X_P_MAX / 1e9:.0f} GPa 에서 최악 {worst * 100:.3f} % "
          f"(주석에 적힌 {ICE_X_FIT_WORST * 100:.3f} %)")
    return bad


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


# 얼음 위성의 포텐셜 온도 선언. 껍질 아래 바다 꼭대기는 그 압력의 얼음 Ih 녹는점에 있고
# (273.16 K 에서 251.2 K 까지), 그것을 표면까지 감압한 단열선의 온도가 선언값이다. 270 K 는
# 20–30 km 껍질에 해당하고, 값은 열 이력이 정하므로 이 표의 모든 행이 그 선언에 기댄다.
ICY_T_POT = 270.0


def _water_table_crosscheck() -> list[str]:
    """water_table.py 의 밀도가 SeaFreeze water1 을 재현하는가. 생성기가 적은 보간 오차 안이어야 한다."""
    try:
        from seafreeze.seafreeze import getProp
    except ImportError:
        print("  [SKIP] SeaFreeze 가 없다 — 액체 물 표 대조는 engine/.venv 에서만 돈다")
        return []
    import numpy as np
    import water_table
    worst = worst_c = 0.0
    for p_mpa, t_k in ((5.0, 273.15), (150.0, 265.0), (600.0, 290.0), (1200.0, 310.0),
                       (2100.0, 350.0)):
        pt = np.empty((1,), dtype=object)
        pt[0] = (p_mpa, t_k)
        o = getProp(pt, "water1")
        rho_sf = float(o.rho[0])
        worst = max(worst, abs(water_table.density(p_mpa * 1e6, t_k) / rho_sf - 1.0))
        # c_P 는 2026-08-31 (얼음 축) 에 구웠다 — 같은 다섯 점에서 원 표현과 대조한다.
        worst_c = max(worst_c, abs(water_table.c_p(p_mpa * 1e6, t_k) / float(o.Cp[0]) - 1.0))
    ok = worst < 5e-4 and worst_c < 1e-2
    print(f"  [{'PASS' if ok else 'FAIL'}] 다섯 점에서 최악 ρ {worst:.1e} (생성기 2e-4 · 허용 5e-4) "
          f"· c_P {worst_c:.1e} (생성기 4.5e-3 바다 창 · 허용 1e-2)")
    return [] if ok else [f"액체 물 표가 SeaFreeze water1 과 ρ {worst:.1e} · c_P {worst_c:.1e} 어긋난다"]


def icy_table() -> None:
    """문서 §Validation 의 얼음 위성 표를 다시 낸다 — 2층 한 점과 3층 띠를 나란히."""
    print("| moon | ρ̄ (kg/m³) | two-layer C/MR² | three-layer band (core 0 → 0.45) | published | inside? | narrowed by C/MR² | source |")
    print("|---|---|---|---|---|---|---|---|")
    for name, mkg, r_km, nmoi_pub, src, _gate in ICY_ANCHORS:
        rho = mkg / (4.0 / 3.0 * 3.141592653589793 * (r_km * 1e3) ** 3)
        m_e, r_e = mkg / EARTH_MASS_KG, r_km * 1e3 / EARTH_RADIUS_M
        two = infer_composition(m_e, r_e, ice_allowed=True)
        two_s = f"{two.values['nmoi']:.4f}" if two.applicable else "declined"
        res = infer_three_layer(m_e, r_e, ICY_T_POT, nmoi=nmoi_pub)
        if not res.applicable:
            print(f"| {name} | {rho:.0f} | {two_s} | declined | {nmoi_pub:.4f} | – | – | {src} |")
            continue
        lo, hi = res.values["nmoi_low"], res.values["nmoi_high"]
        inside = lo <= nmoi_pub <= hi
        if res.regime == "inferred_three_layer_by_nmoi":
            narrowed = (f"core {res.inputs['core_mass_fraction']:.3f} · ice "
                        f"{res.inputs['ice_mass_fraction']:.3f} · ocean "
                        f"{res.values['ocean_thickness']:.0f} km / shell "
                        f"{res.values['ice_shell_thickness']:.0f} km")
        else:
            narrowed = "outside the band: " + ("rock lighter than this silicate — and than antigorite (C10)" if nmoi_pub > hi
                                               else "core grid too small")
        print(f"| {name} | {rho:.0f} | {two_s} | {lo:.4f} – {hi:.4f} | {nmoi_pub:.4f} | "
              f"{'yes' if inside else 'no'} | {narrowed} | {src} |")


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


# 얼음거대행성의 앵커는 test_ice_giant.py 로 옮겨갔다 (2026-08-28). 여기 있던
# ICE_GIANT_T_POT = 2500 K 는 폴리트로프 시절의 선언(얼음 맨틀 꼭대기 온도)이었고, 수소-헬륨
# 표가 들어와 선언이 1 bar 온도가 된 뒤로는 두 행성 다 거절을 찍고 있었다 — 앵커가 아니라
# 낡은 표였다. 전체 풀이는 그 파일의 --refresh 가, 표는 --table 이 낸다.
def ice_giant_table() -> None:
    """문서의 얼음거대행성 표. test_ice_giant.py 의 굳힌 앵커에서 낸다."""
    from test_ice_giant import table
    table()


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
    if "--icegiant" in sys.argv:
        ice_giant_table()
        return 0
    if "--serpentine" in sys.argv:
        print_serpentine_bands()
        return 0
    if "--middle-rung" in sys.argv:
        print_middle_rung_bands()
        return 0
    if "--adiabat" in sys.argv:
        print_adiabat_window()
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

    # ── 괄호잡기가 버릴 시험압을 물리로 착각하지 않는가 ──────────────────
    #
    # 이 결함은 **두 번** 나왔고 두 번 다 물리로 읽혔다. 2026-08-26 에 지구식 암석이
    # 6.84 M⊕ 에서 막힌다고 보고됐는데 그 수렴해의 중심압은 2741 GPa 로 규산염 천장
    # 3500 근처도 아니었다. 2026-08-27 에 water 프리셋이 5.884 M⊕ 에서 막힌다고
    # 보고됐는데 8.0 M⊕ 가 멀쩡히 수렴한다.
    #
    # 그래서 증상이 아니라 **기작** 을 지킨다. 아래 두 천체는 답에 이르는 길에서
    # 시험압이 바깥 층의 천장을 넘고, 수렴해는 그 천장 한참 아래에 있다. 하나라도
    # 거절로 돌아오면 괄호잡기가 다시 시험값을 내보내고 있는 것이다.
    # ── 괄호가 안 잡힐 때 거절이 기작을 이름 대는가 ────────────────────
    #
    # 이 경로가 두 상황을 한 문구로 내보내고 있었다. 눈금이 실제로 막힌 경우와,
    # 축이 끝까지 풀렸는데 목표가 그 **밖** 인 경우다. 뒤쪽에서는 막힌 눈금이 없어서
    # 이유가 "이유 미상" 으로 나갔다 — 거절은 기작을 이름 대야 한다는 이 엔진의 규칙을
    # 어기는 자리였고, 넓힌 암석 로스터에서 다섯 중 셋이 그 문구를 달고 있었다.
    print("\n괄호 실패 — 사정거리 밖과 막힌 구간을 갈라 말하는가")
    for label, m, r, want in (
            ("순철보다 밀하다", 4.0, 0.880, "순철로 채워도"),
            ("지구 핵보다 순수한 철이 필요하다", 0.633, 0.699, "그보다 순수한 철"),
            ("눈금이 실제로 막혔다", 21.301, 1.610, "막힌 구간")):
        res = infer_composition(m, r, ice_allowed=False)
        ok = (not res.applicable) and want in res.reason
        if not ok:
            fails.append(f"괄호 실패: {label} — {res.reason[:70]}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    # 그리고 어느 경로도 '이유 미상' 을 내보내지 않는다.
    leaked = [m for m, r in ((4.0, 0.880), (0.633, 0.699), (8.9, 1.310))
              if "이유 미상" in infer_composition(m, r, ice_allowed=False).reason]
    if leaked:
        fails.append(f"괄호 실패: '이유 미상' 이 남아 있다 — {leaked}")
    print(f"  [{'PASS' if not leaked else 'FAIL'}] '이유 미상' 을 내보내지 않는다")

    print("\n괄호잡기 — 버릴 시험압에서 바깥 층이 깨져도 거절하지 않는가")
    # 15 M⊕ 는 예전 상한의 2.5 배이고 실제 상한(21.5)에서는 떨어져 있다. 상한 바로
    # 아래를 고르면 좁히기가 많이 돌아 이 검사 하나가 10 초를 먹는데, 여기서 지키는
    # 것은 상한의 위치가 아니라 **버릴 시험압이 새어 나오지 않는다** 는 것이다.
    for label, m in (("water 8 M⊕ (예전 5.884 상한 위)", 8.0),
                     ("water 15 M⊕", 15.0)):
        res = solve(m, composition="water")
        ok = res.applicable
        if not ok:
            fails.append(f"괄호잡기: {label} 가 거절했다 — {res.reason[:70]}")
        else:
            base = res.values["core_pressure"]
            print(f"  [PASS] {label} — 중심압 {base:.0f} GPa · "
                  f"C/MR² {res.values['nmoi']:.4f}")
            continue
        print(f"  [FAIL] {label}")

    # 그리고 진짜 거절은 여전히 살아 있어야 한다. 없애는 게 아니라 옮기는 것이었다.
    over = solve(30.0, composition="water")
    real = (not over.applicable) and "h2o" in over.reason
    if not real:
        fails.append("괄호잡기: 얼음 천장을 진짜로 넘는 천체가 거절하지 않는다")
    print(f"  [{'PASS' if real else 'FAIL'}] water 30 M⊕ 는 여전히 거절하고 "
          "바깥 층을 이름 댄다")

    print("\n격자 수렴 — 적분 격자가 오차원이 아님을 보인다")
    # 지구는 핵/맨틀 밀도 대비가 작아 층 경계의 걸음 양자화가 잘 안 보이는 천체다. 밀도
    # 대비가 큰 얼음/가스 경계에서 같은 질문(격자 위상 1499 ↔ 1501, 격자 4배)을 묻는 것은
    # test_ice_giant.py 가 한다 — 2026-08-28 의 계단 결함은 거기서만 보였다.
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

    print("\n물얼음 상 사다리 — 209.5 MPa 부터 1 TPa 까지 끊긴 데가 없는가")
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

    # ── Kimura & Murakami 2023 — Reinhardt 액체선의 측정 검사 (F1) ──
    print("\n융해곡선 재심 (F1) — Kimura & Murakami 2023 Table I 대 Reinhardt+ 2022 액체선")
    from eos import _interp_line as _il2, REINHARDT_LIQUID as _RL2, IAPWS_VII_END as _IVE2
    inside = n_cmp = 0
    for p_gpa, t_k, sig in KIMURA_TABLE_I:
        t_r = _il2(_RL2, p_gpa * 1e9)
        if t_r is None:
            print(f"         {p_gpa:5.1f} GPa · {t_k:.0f} ± {sig:.0f} K — Reinhardt 의 52.4 GPa 밖")
            continue
        n_cmp += 1
        ok_pt = abs(t_r - t_k) <= sig
        inside += ok_pt
        print(f"         {p_gpa:5.1f} GPa · Kimura {t_k:.0f} ± {sig:.0f} K · Reinhardt {t_r:.0f} K "
              f"({t_r - t_k:+.0f} K, {(t_r - t_k) / sig:+.2f} σ) {'안' if ok_pt else '**밖**'}")
    ok = inside >= KIMURA_INSIDE_MIN
    if not ok:
        fails.append(f"Reinhardt 액체선이 Kimura 의 불확도 안에 드는 점이 {inside}/{n_cmp} — 기록 {KIMURA_INSIDE_MIN} 미만")
    print(f"  [{'PASS' if ok else 'FAIL'}] {n_cmp} 점 중 {inside} 점이 측정 불확도 안 (기록 ≥ {KIMURA_INSIDE_MIN}); "
          "밖의 한 점(25.9 GPa)은 측정이 시뮬레이션보다 뜨겁다 — IAPWS 쪽이 아니다")
    p_ref, t_ref, a_s, c_s = KIMURA_SIMON
    t_simon = t_ref * ((_IVE2 / 1e9 - p_ref) / a_s + 1.0) ** (1.0 / c_s)
    d = t_simon / _il2(_RL2, _IVE2) - 1.0
    ok = KIMURA_SEAM_BAND[0] <= d <= KIMURA_SEAM_BAND[1]
    if not ok:
        fails.append(f"이음매에서 Kimura & Murakami eq. (2) / Reinhardt − 1 = {d * 100:+.1f} % 가 기록 구간 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 이음매 {_IVE2 / 1e9:.1f} GPa: Kimura & Murakami eq. (2) {t_simon:.0f} K — Reinhardt 보다 "
          f"{d * 100:+.1f} %, IAPWS 식 (5) 715 K 보다 {(t_simon / 715.0 - 1) * 100:+.0f} % — 측정이 시뮬레이션 쪽에 선다")

    # ── antigorite (C10) — 옮겨 적기 검산 ──
    print("\nantigorite — Hilairet+ 2006 의 BM2 와, 인쇄되지 않은 ρ₀ 의 재도출")
    from eos import ANTIGORITE, ANTIGORITE_RHO0, ANTIGORITE_K0, ANTIGORITE_P_MAX
    mass_u = sum(ATOMIC_MASS_U[el] * n for el, n in HILAIRET_FORMULA)
    rho0_again = mass_u * AMU_KG / (HILAIRET_V_M1_A3 * 1e-30)
    ok = abs(rho0_again - ANTIGORITE_RHO0) < 0.5
    if not ok:
        fails.append(f"antigorite ρ₀ 재도출 {rho0_again:.1f} 이 eos.py 의 {ANTIGORITE_RHO0} 와 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 구조식 {mass_u:.2f} u / 172 Å³ → ρ₀ {rho0_again:.1f} kg/m³ "
          f"(eos.py {ANTIGORITE_RHO0})")
    m_units = HILAIRET_V0_A3 / HILAIRET_V_M1_A3
    ok = abs(m_units - HILAIRET_POLYSOME_M) < 0.05
    if not ok:
        fails.append(f"V₀ / V(m=1) = {m_units:.3f} 이 m = 17 폴리솜과 안 맞는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] V₀ 2926.23 / 172 = {m_units:.3f} — Capitani & Mellini 2004 의 "
          f"m = {HILAIRET_POLYSOME_M} 폴리솜")
    p_pr, t_pr, rho_pr = HILAIRET_PRINTED_DENSITY
    rho_rt = ANTIGORITE.density(p_pr)
    d = rho_rt / rho_pr - 1.0
    ok = 0.02 < d < 0.035
    if not ok:
        fails.append(f"5.7 GPa 상온 밀도 {rho_rt:.0f} 가 논문의 470 °C 값 2765 보다 {d * 100:+.1f} % — "
                     "450 K 열팽창의 크기(2–3.5 %)가 아니다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 5.7 GPa: 상온 곡선 {rho_rt:.0f} kg/m³ 대 논문의 470 °C 인쇄값 "
          f"{rho_pr:.0f} → {d * 100:+.1f} %, 450 K 열팽창의 크기와 부호")
    from eos import ANTIGORITE_ALPHA_K, HP98_ATG_A0, HP98_ATG_CP_298
    # F2 (2026-08-30): 열항은 Holland & Powell 1998 Table 5 atg 행에서 — a° 4.70e-5 (forsterite 의 6.13 이 같은 열
    # 규약을 확인), α(298) = a°(1 − 10/√298.15), Hilairet 의 K₀ 를 곱함. C_p(298) 은 다항식에서 다시 낸다.
    a0 = HP98_ATG_A0
    alpha_298 = a0 * (1.0 - 10.0 / 298.15 ** 0.5)
    cp_298 = (9.6210e3 - 9.1183e-2 * 298.15 - 35941.6e3 / 298.15 ** 2 - 83.0342e3 / 298.15 ** 0.5) / 4.5359
    ok = (ANTIGORITE.cold_phases() == () and ANTIGORITE_P_MAX == 10e9
          and abs(ANTIGORITE_ALPHA_K / (alpha_298 * ANTIGORITE_K0) - 1.0) < 1e-9
          and abs(HP98_ATG_CP_298 / cp_298 - 1.0) < 1e-3)
    if not ok:
        fails.append(f"antigorite 열항이 Holland & Powell 1998 에서 다시 낸 값과 다르다 — αK {ANTIGORITE_ALPHA_K:.4e} "
                     f"대 {alpha_298 * ANTIGORITE_K0:.4e}, c_p {HP98_ATG_CP_298:.1f} 대 {cp_298:.1f}, cold {ANTIGORITE.cold_phases()}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 열항 (Holland & Powell 1998 Table 5 atg): α(298) {alpha_298:.3e} K⁻¹ × K₀ → "
          f"αK_T {ANTIGORITE_ALPHA_K / 1e6:.3f} MPa/K · c_P(298) {cp_298:.0f} J/kg/K · 상한 {ANTIGORITE_P_MAX / 1e9:.0f} GPa — "
          "빌린 항을 298 K 에서 평탄화, 등급은 그 빌림이 정한다")
    for p_gpa in (0.023, 2.73, 3.28):
        print(f"         {p_gpa:5.3f} GPa → {ANTIGORITE.density(p_gpa * 1e9):.0f} kg/m³")

    # ── 두 번째 앵커 (C8) ──
    # 등급을 올리는 근거는 "앵커가 하나 더 있다" 가 아니라 **"그 앵커와 이만큼 어긋난다"** 다.
    # 그래서 표 전체를 재고 구간에 묶는다. 표는 `--adiabat` 가 낸다.
    print("\n두 번째 앵커 — Noack & Lasbleis 2020 eq. (22), 0.8 ~ 2 M⊕")
    nl_rows = adiabat_window_table()
    earth = [r for r in nl_rows if r["mass"] == 1.0][0]
    ok = abs(earth["t_nl"] - NL2020_EARTH_TCMB) < 1.0
    if not ok:
        fails.append(f"식 (22) 의 지구 값 {earth['t_nl']:.1f} K 가 옮겨 적은 기록 {NL2020_EARTH_TCMB:.0f} K 와 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 식 (22) · 지구 기하 → {earth['t_nl']:.0f} K (기록 {NL2020_EARTH_TCMB:.0f} K, "
          f"조사 보고 2562 K 의 독립 재현) · 엔진 {earth['t_engine']:.0f} K · eq. 7 {earth['t_unt']:.0f} K")
    worst_lo = min(r["t_engine"] / r["t_nl"] - 1.0 for r in nl_rows)
    worst_hi = max(r["t_engine"] / r["t_nl"] - 1.0 for r in nl_rows)
    ok = NL2020_BAND[0] <= worst_lo and worst_hi <= NL2020_BAND[1]
    if not ok:
        fails.append(f"엔진 / 식 (22) 의 폭 {worst_lo * 100:+.1f} ~ {worst_hi * 100:+.1f} % 가 기록 구간 {NL2020_BAND} 밖")
    for r in nl_rows:
        print(f"         {r['mass']:.1f} M⊕ (R {r['radius']:.3f}) → 엔진 {r['t_engine']:.0f} K · eq. (22) {r['t_nl']:.0f} K "
              f"({(r['t_engine'] / r['t_nl'] - 1) * 100:+.1f} %) · eq. 7 "
              + ("–" if r["t_unt"] is None else f"{r['t_unt']:.0f} K ({(r['t_engine'] / r['t_unt'] - 1) * 100:+.1f} %)"))
    print(f"  [{'PASS' if ok else 'FAIL'}] 엔진은 식 (22) 에 {worst_lo * 100:+.1f} ~ {worst_hi * 100:+.1f} % — "
          f"기록 구간 {NL2020_BAND[0] * 100:+.0f} ~ {NL2020_BAND[1] * 100:+.0f} %")
    slopes = [r["rise_engine"] / r["rise_nl"] - 1.0 for r in nl_rows]
    ok = NL2020_SLOPE_BAND[0] <= min(slopes) and max(slopes) <= NL2020_SLOPE_BAND[1]
    if not ok:
        fails.append(f"상승비의 폭 {min(slopes) * 100:+.1f} ~ {max(slopes) * 100:+.1f} % 가 기록 구간 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 250 km 에서 CMB 까지의 상승비: 엔진이 식의 지수 인자보다 "
          f"{min(slopes) * 100:+.1f} ~ {max(slopes) * 100:+.1f} % 가파르다 — 절대 온도가 맞는 것은 출발점이 "
          f"다른 것(식 2000 K, 엔진 {earth['t_depth']:.0f} K)과 상쇄된 결과이고, 그 사실을 적는다")
    spreads = [(r["t_unt"] / r["t_nl"] - 1.0) for r in nl_rows if r["t_unt"] is not None and r["mass"] >= 1.0]
    ok = ANCHOR_SPREAD_BAND[0] <= max(spreads) <= ANCHOR_SPREAD_BAND[1]
    if not ok:
        fails.append(f"두 앵커의 상호 폭 {max(spreads) * 100:.1f} % 가 기록 구간 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 두 앵커끼리는 1 → 2 M⊕ 에서 {min(spreads) * 100:+.1f} ~ {max(spreads) * 100:+.1f} % "
          f"어긋난다 — 엔진은 그 사이에 앉는다")

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
    # **2026-08-28 에 이 목록이 비었다.** 마지막으로 남아 있던 것이 폴리트로프
    # `hhe_n1` 이었고, 그 한 줄 때문에 온도가 외피를 흐르지 않아 선언된 포텐셜 온도가
    # 표면이 아니라 얼음 맨틀 꼭대기에 떨어졌다. Chabrier+ 2019 표가 ∇_ad 를 들고
    # 오면서 사라졌다. 그러니 검사는 "이름을 대는가" 에서 **"비었는가"** 로 바뀐다 —
    # 다시 채워지면 온도 경계조건의 뜻이 조용히 옮겨간다는 뜻이므로.
    cold = {m: _M[m].cold_phases() for m in ("h2o", "h_he", "silicate", "fe_prem")}
    ok = all(v == () for v in cold.values())
    if not ok:
        fails.append(f"등온으로 남는 상이 남아 있다 — {cold}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 등온으로 남는 상이 하나도 없다 — h2o 는 "
          f"2026-08-27 에 ice_vii 이, h_he 는 2026-08-28 에 hhe_n1 이 마지막이었다")
    print(f"         h_he 가 비었다는 것이 곧 **포텐셜 온도가 이 갈래에서도 표면의 "
          f"온도** 라는 뜻이다 (1 bar 준위).")
    for mat in (_M["silicate"], _M["fe_prem"], _M["fe_eps"], _M["h2o"], H_HE):
        ok = mat.has_thermal
        if not ok:
            fails.append(f"{mat.name}: 열 상수가 있어야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {mat.name:9} 전 상에 열 상수가 있다")

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

    print("\n녹는곡선 — IAPWS 가 검증용으로 실은 다섯 점을 다시 내는가")
    # 손으로 옮겨 적은 식이 맞는지를 그 표준 자신의 검증표로 잰다.
    from eos import iapws_p_melt, iron_t_melt, water_t_melt
    from eos import (IRON_LIGHT_ELEMENT_FACTOR, IRON_MELT_SPLICE, IRON_MELT_LOW,
                     IRON_MELT_HIGH, IRON_MELT_MAX)
    for name, t_k, want_mpa in IAPWS_TABLE3:
        got = iapws_p_melt(name, t_k) / 1e6
        d = abs(got - want_mpa) / want_mpa
        ok = d <= IAPWS_TABLE3_TOL
        if not ok:
            fails.append(f"IAPWS {name}: {t_k} K 에서 {got:.5f} MPa, 표는 {want_mpa}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:8} {t_k:6.1f} K → {got:10.4f} MPa "
              f"· 표 {want_mpa:10.4f} (상대차 {d:.1e})")

    print("\n녹는곡선 — 뒤집기가 제자리로 돌아오는가, 그리고 창을 끊김 없이 덮는가")
    worst_inv = 0.0
    for name, t_k, _p in IAPWS_TABLE3:
        p_pa = iapws_p_melt(name, t_k)
        back = water_t_melt(p_pa)
        if back is None:
            fails.append(f"물 녹는곡선이 {p_pa / 1e6:.1f} MPa 에서 None 을 돌려준다")
            continue
        worst_inv = max(worst_inv, abs(back - t_k))
    ok = worst_inv < 1e-6
    if not ok:
        fails.append(f"p_melt(T) 를 뒤집은 T 가 {worst_inv:.3g} K 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] p→T 뒤집기 최악 {worst_inv:.2e} K")
    # 따뜻한 얼음 창 전체. 209.5 MPa ~ 2.216 GPa 안에서 곡선이 끊기지 않고 단조증가한다.
    from eos import ICE_IH_TO_III, ICE_VI_TO_VII
    prev = None
    gap = None
    for i in range(101):
        p_pa = ICE_IH_TO_III + (ICE_VI_TO_VII - ICE_IH_TO_III) * i / 100.0
        t_m = water_t_melt(p_pa)
        if t_m is None:
            gap = p_pa
            break
        if prev is not None and t_m < prev - 1e-9:
            gap = p_pa
            break
        prev = t_m
    ok = gap is None
    if not ok:
        fails.append(f"따뜻한 얼음 창의 녹는곡선이 {gap / 1e6:.1f} MPa 에서 끊긴다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 209.5 MPa–2.216 GPa 에서 끊긴 데 없이 "
          f"{water_t_melt(ICE_IH_TO_III):.2f} K → {prev:.2f} K 로 오른다")

    print("\n녹는곡선 — 철이 발표된 앵커 안에 떨어지는가")
    t0 = iron_t_melt(0.0)
    d = abs(t0 - FE_ZERO_P_MELT) / FE_ZERO_P_MELT
    ok = d <= FE_ZERO_P_TOL
    if not ok:
        fails.append(f"상압 철 녹는점이 {t0:.0f} K, 실측 {FE_ZERO_P_MELT:.0f} K")
    print(f"  [{'PASS' if ok else 'FAIL'}] 상압 {t0:.0f} K · 실측 {FE_ZERO_P_MELT:.0f} K "
          f"({d * 100:.1f} %)")
    t_icb = iron_t_melt(FE_ICB_GPA * 1e9)
    hit = [n for n, v, u in FE_ICB_ANCHORS if abs(t_icb - v) <= u]
    ok = bool(hit)
    if not ok:
        fails.append(f"내핵 경계 순철 녹는점 {t_icb:.0f} K 가 두 실험 어느 오차범위에도 "
                     f"안 들어간다")
    print(f"  [{'PASS' if ok else 'FAIL'}] {FE_ICB_GPA:.0f} GPa 에서 순철 {t_icb:.0f} K")
    for n, v, u in FE_ICB_ANCHORS:
        inside = "안" if abs(t_icb - v) <= u else "밖"
        print(f"         {n}: {v:.0f} ± {u:.0f} K — {inside}")
    print(f"         두 실험이 서로 "
          f"{abs(FE_ICB_ANCHORS[0][1] - FE_ICB_ANCHORS[1][1]) / FE_ICB_ANCHORS[1][1] * 100:.0f} % "
          f"어긋난다. 이 곡선의 정직한 오차폭이 그 폭이다.")

    print("\n녹는곡선 — 두 적합의 이음매를 재본다 (지어낸 수가 아니라)")
    lo_t0, lo_p0, lo_a, lo_c = IRON_MELT_LOW
    hi_t0, hi_p0, hi_a, hi_c = IRON_MELT_HIGH
    worst_splice = 0.0
    for p_gpa in (300.0, 330.0, 365.0):
        a = lo_t0 * (1.0 + (p_gpa * 1e9 - lo_p0) / lo_a) ** lo_c
        b = hi_t0 * (1.0 + (p_gpa * 1e9 - hi_p0) / hi_a) ** hi_c
        worst_splice = max(worst_splice, abs(b - a) / a)
        print(f"         {p_gpa:.0f} GPa — Zhang+ 2015 {a:.0f} K · "
              f"González-Cataldo+ 2023 {b:.0f} K ({(b / a - 1) * 100:+.1f} %)")
    ok = 0.05 < worst_splice < 0.10
    if not ok:
        fails.append(f"두 융해 적합의 겹치는 구간 차이가 {worst_splice * 100:.1f} % 로 "
                     f"기록된 6.8~7.5 % 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 겹치는 구간 최악 {worst_splice * 100:.1f} % — "
          f"두 실험이 어긋나는 13 % 보다 좁다")
    ok = iron_t_melt(IRON_MELT_MAX * 1.01) is None
    if not ok:
        fails.append("5 TPa 위에서도 융해온도를 돌려준다 — 두 적합 다 밖인 자리다")
    print(f"  [{'PASS' if ok else 'FAIL'}] {IRON_MELT_MAX / 1e12:.0f} TPa 위는 값이 아니라 "
          f"None 이다")

    print("\n녹는곡선 — 없는 재료는 없다고 말하는가")
    from eos import MATERIALS as _MM, H_HE
    # h2o 는 2026-08-27 에 전 상이 곡선을 들고 있었다. 얼음 X 가 들어오면서 곡선이
    # **없는 상이 하나 생겼다** — IAPWS 식 (5) 가 715 K(20.6 GPa) 에서 끝나기 때문이고,
    # 그 사실을 지우지 않고 이름으로 들고 있는 것이 여기서 검사하는 것이다.
    for mat, want_free in ((_MM["silicate"], True), (_MM["h2o"], False),
                           (_MM["fe_prem"], False), (_MM["fe_eps"], False),
                           (H_HE, True)):
        free = mat.melt_free_phases()
        ok = bool(free) == want_free
        if not ok:
            fails.append(f"{mat.name}: 녹는곡선 유무를 잘못 말한다 — {free}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {mat.name:9} 곡선 없는 상 {free or '()'}")
    # 2026-08-30 까지 ice_x 가 곡선 없는 상이었다. Reinhardt+ 2022 의 액체선이 52.4 GPa 까지 오므로
    # 이제 곡선은 있고, **어디서 끝나는지** 가 검사 대상이다 — 그 위는 None 이고 판정문이 그 압력을 말한다.
    from eos import REINHARDT_P_MAX as _RPM, IAPWS_VII_END as _IVE, water_t_melt as _wtm
    ok = (_wtm(_RPM) is not None and _wtm(_RPM * 1.0001) is None
          and abs(_wtm(_RPM) - 1953.0) < 1e-9)
    if not ok:
        fails.append(f"물의 녹는곡선이 {_RPM / 1e9:.1f} GPa 에서 1953 K 로 끝나지 않는다 — "
                     f"{_wtm(_RPM)}, {_wtm(_RPM * 1.0001)}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 물의 녹는곡선은 {_RPM / 1e9:.1f} GPa · 1953 K 에서 끝난다 "
          "(Reinhardt+ 2022 의 마지막 점) — 그 위는 None")
    # (a) 이음매. IAPWS 식 (5) 가 끝나는 20.6 GPa 에서 두 곡선의 폭을 **잰다**. 규산염 이음매(0.21 %)와
    # 같은 규칙이고, 이 폭이 크다는 것이 이 곡선을 analog 로 두는 이유 중 하나다.
    from eos import _interp_line as _il, REINHARDT_LIQUID as _RL
    t_iapws = _wtm(_IVE * (1.0 - 1e-12))
    t_rein = _il(_RL, _IVE)
    seam = (t_rein - t_iapws) / t_iapws
    ok = abs(t_iapws - 715.0) < 0.5 and abs(seam - 0.2634) < 0.002
    if not ok:
        fails.append(f"20.6 GPa 이음매가 기록과 다르다 — IAPWS {t_iapws:.1f} K, Reinhardt {t_rein:.1f} K, "
                     f"{seam * 100:+.2f} %")
    print(f"  [{'PASS' if ok else 'FAIL'}] 이음매 {_IVE / 1e9:.2f} GPa: IAPWS {t_iapws:.0f} K → Reinhardt "
          f"{t_rein:.0f} K, 녹는점 {seam * 100:+.1f} % — 잰 값이고 문서가 같은 수를 적는다")
    # (c) 표는 생성된 것이다: 논문이 본문에 적는 삼중점(20 GPa · 875 K)과 직접 공존 점들을 지나는가.
    import ice_melt_table as _imt
    tp_p, tp_t = _imt.TRIPLE_POINT_GPA_K
    worst = max(abs(_il(_RL, p_gpa * 1e9) - t_k) for p_gpa, t_k in _imt.DIRECT_COEXISTENCE)
    # 삼중점 20 GPa 는 IAPWS 의 구간(20.6 GPa 까지) 안이라 water_t_melt 는 거기서 IAPWS 를 답한다
    # (705 K — 이음매의 다툼이 바로 이것이다). 검사하는 것은 **굳힌 선 자체** 가 논문의 점을 지나는가다.
    ok = abs(_il(_RL, tp_p * 1e9) - tp_t) < 1e-9 and worst < 30.0
    if not ok:
        fails.append(f"굳힌 액체선이 논문의 삼중점·직접 공존 점을 지나지 않는다 — "
                     f"삼중점 {_il(_RL, tp_p * 1e9)}, 직접 공존 최악 {worst:.1f} K")
    print(f"  [{'PASS' if ok else 'FAIL'}] 굳힌 액체선이 논문의 삼중점 {tp_p:.0f} GPa · {tp_t:.0f} K 를 지나고 "
          f"직접 공존 {len(_imt.DIRECT_COEXISTENCE)} 점과 최악 {worst:.0f} K 안이다 (데이터 "
          f"{_imt.DATA_COMMIT[:10]})")
    # (d) 적합의 천장과 상 경계는 다른 객체다.
    from eos import water_vii1_vii2_boundary as _wvb, ICE_VII_X_T_MAX as _IXT
    # 47 GPa 에서는 Reinhardt 의 액체선이 정확히 1800.0 K 를 지난다 — 사다리 천장과 같은 **수** 이지만
    # 다른 **객체** 다 (하나는 상 경계, 하나는 매듭의 끝). 그래서 수가 다른 45 GPa 에서 셋을 대본다.
    ok = (_wvb(45e9) is not None and _wvb(45e9) != _IXT and _wtm(45e9) != _IXT
          and abs(_wtm(47e9) - _IXT) < 1e-9)
    if not ok:
        fails.append("적합 천장(1800 K)과 상 경계가 갈라져 있지 않다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 45 GPa 에서 VII′–VII″ 선 {_wvb(45e9):.0f} K · 녹는점 {_wtm(45e9):.0f} K "
          f"· 사다리 천장 {_IXT:.0f} K — 셋이 다른 수이고 다른 종류다 (47 GPa 에서 액체선이 "
          "1800 K 를 지나는 것은 우연이고, 같은 수라도 같은 객체가 아니다)")
    ok = (_MM["fe_eps"].t_melt(FE_ICB_GPA * 1e9)
          > _MM["fe_prem"].t_melt(FE_ICB_GPA * 1e9))
    if not ok:
        fails.append("합금 핵(fe_prem)의 녹는점이 순철(fe_eps)보다 낮지 않다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 합금 핵이 순철보다 "
          f"{(1 - IRON_LIGHT_ELEMENT_FACTOR) * 100:.0f} % 낮게 녹는다 — "
          f"{_MM['fe_prem'].t_melt(FE_ICB_GPA * 1e9):.0f} K 대 "
          f"{_MM['fe_eps'].t_melt(FE_ICB_GPA * 1e9):.0f} K")

    print("\n따뜻한 얼음 창 — 판정이 나오고, 온도를 옮기면 뒤집히는가")
    icy = dict(core_mass_fraction=0.0, ice_mass_fraction=0.407)
    cold = solve(0.0248, potential_temperature=120.0, **icy)
    warm = solve(0.0248, potential_temperature=250.0, **icy)
    none_t = solve(0.0248, **icy)
    got = (cold.values["ice_column_state"], warm.values["ice_column_state"],
           none_t.values["ice_column_state"])
    ok = got == ("solid", "molten", "undecided")
    if not ok:
        fails.append(f"얼음 창 판정이 {got} 다 — (solid, molten, undecided) 여야 한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 120 K → {got[0]} · 250 K → {got[1]} · "
          f"온도 미선언 → {got[2]}")
    ok = solve(1.0, core_mass_fraction=0.325).values["ice_column_state"] == "none"
    if not ok:
        fails.append("얼음이 없는 천체가 'none' 이라고 말하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 얼음 기둥이 없으면 'none' 이다")
    said = any("바다를 담은 값" in n for n in warm.notes)
    if not said:
        fails.append("녹았다고 판정하면서 밀도가 바다를 담았다는 사실을 note 가 안 적는다")
    print(f"  [{'PASS' if said else 'FAIL'}] 녹은 해의 note 가 바다를 담은 값이라고 적는다")
    ok = warm.values["ocean_thickness"] > 0.0 and cold.values["ocean_thickness"] == 0.0
    if not ok:
        fails.append("바다 두께가 판정과 어긋난다 — molten 인데 0 이거나 solid 인데 양수다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 250 K 바다 {warm.values['ocean_thickness']:.0f} km "
          f"· 껍질 {warm.values['ice_shell_thickness']:.0f} km · 120 K 바다 0 km")

    print("\n바다 — 밀도를 실제로 움직이는가, 경계가 격자에 매이지 않는가, 3층을 역산하는가")
    # 유로파형 천체: 금속 핵 + 암석 + 물 기둥. 2026-08-29 전에는 표현할 수 없던 구조다.
    eur = dict(core_mass_fraction=0.12, ice_mass_fraction=0.10, potential_temperature=ICY_T_POT)
    m_eur = 4.7998e22 / EARTH_MASS_KG
    with_ocean = solve(m_eur, **eur)
    try:
        interior.OCEAN_LAYER = False
        solid = solve(m_eur, **eur)
    finally:
        interior.OCEAN_LAYER = True
    moved = abs(with_ocean.values["radius"] / solid.values["radius"] - 1.0)
    ok = with_ocean.values["ocean_thickness"] > 0.0 and moved > 1e-3
    if not ok:
        fails.append(f"바다가 밀도를 안 움직인다 — 반지름 변화 {moved:.1e}, "
                     f"바다 {with_ocean.values['ocean_thickness']:.0f} km. 배선이 끊겼다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 유로파형 (핵 0.12 · 얼음 0.10 · {ICY_T_POT:.0f} K): "
          f"바다 {with_ocean.values['ocean_thickness']:.0f} km · 껍질 "
          f"{with_ocean.values['ice_shell_thickness']:.0f} km · 반지름이 고체상 대비 "
          f"{(with_ocean.values['radius'] / solid.values['radius'] - 1) * 100:+.2f} % · "
          f"C/MR² {solid.values['nmoi']:.4f} → {with_ocean.values['nmoi']:.4f}")
    # 격자 위상. 상 경계를 걸음 안에서 보간하지 않으면 여기서 2e-3 이 나온다 (2026-08-29 측정).
    st, _ = interior.shoot(4.7998e22, 0.12, 0.10, "fe_prem", potential_temperature=ICY_T_POT)
    base = interior.STEPS
    got = []
    try:
        for n in (base - 1, base, base + 1):
            interior.STEPS = n
            g = interior.integrate(st.p_center, 4.7998e22, 0.12, 0.10, "fe_prem",
                                   t_center=st.t_center, t_pot=ICY_T_POT)
            got.append((g.mass_kg / 4.7998e22, g.radius_m / EARTH_RADIUS_M))
    finally:
        interior.STEPS = base
    span_m = max(x[0] for x in got) - min(x[0] for x in got)
    span_r = (max(x[1] for x in got) - min(x[1] for x in got)) / got[1][1]
    ok = span_m < 1e-5 and span_r < 1e-5
    if not ok:
        fails.append(f"바다 경계의 격자 위상: {base - 1}↔{base + 1} 걸음에서 겉질량 {span_m:.1e}, "
                     f"반지름 {span_r:.1e} — 상 경계가 걸음에 양자화됐다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 격자 위상 {base - 1} · {base} · {base + 1}: 겉질량 "
          f"{span_m:.1e} · 반지름 {span_r:.1e} (허용 1e-5)")
    # 3층 역산. 유로파의 발표 C/MR² 가 (핵, 얼음) 띠 안에 있고, 그것으로 좁히면 한 점이 나온다.
    # 기본 실행은 격자 두 점만 훑는다 — 넉 점은 `--icy` 가 낸다.
    eu = [a for a in ICY_ANCHORS if a[0] == "Europa"][0]
    band = infer_three_layer(eu[1] / EARTH_MASS_KG, eu[2] * 1e3 / EARTH_RADIUS_M, ICY_T_POT,
                             nmoi=eu[3], core_grid=(0.0, 0.30))
    if not band.applicable:
        fails.append(f"Europa 3층 역산이 거절했다 — {band.reason[:80]}")
        print(f"  [FAIL] Europa 3층 역산 거절: {band.reason[:80]}")
    else:
        inside = band.values["nmoi_low"] <= eu[3] <= band.values["nmoi_high"]
        narrowed = band.regime == "inferred_three_layer_by_nmoi"
        off = abs(band.values["nmoi"] - eu[3]) / eu[3] if narrowed else 1.0
        ok = inside and narrowed and off < 2e-3 and band.converged
        if not ok:
            fails.append(f"Europa 3층: 띠 {band.values['nmoi_low']:.4f}–{band.values['nmoi_high']:.4f}, "
                         f"발표 {eu[3]}, 좁힘 {narrowed}, 오차 {off:.1e}, converged {band.converged}")
        print(f"  [{'PASS' if ok else 'FAIL'}] Europa: 띠 C/MR² {band.values['nmoi_low']:.4f}–"
              f"{band.values['nmoi_high']:.4f} 가 발표값 {eu[3]} 을 담고, 그것으로 좁히면 핵 "
              f"{band.inputs.get('core_mass_fraction', float('nan')):.3f} · 얼음 "
              f"{band.inputs.get('ice_mass_fraction', float('nan')):.3f} · 바다 "
              f"{band.values.get('ocean_thickness', 0):.0f} km / 껍질 "
              f"{band.values.get('ice_shell_thickness', 0):.0f} km · converged {band.converged}")
    print("\n액체 물 표 — 굳힌 표가 원 표현과 같은가 (SeaFreeze 있을 때만)")
    fails += _water_table_crosscheck()

    print("\n녹는곡선 — Queyroux+ 2020 Table S1 (F4): 대역 안의 측정이 두 곡선 어느 쪽에 앉는가")
    # Queyroux+ 2020 Supplemental Material Table S1, PDF 4쪽에서 읽음: (Tm K, σT K, Pm GPa, σP GPa).
    # 판정 척도는 F1 의 것 — 잔차가 인쇄된 σT 안이면 "앉는다". 삼중점 850(20) K 는 적합의 교점이라 쓰지 않는다.
    QUEYROUX_S1 = ((660, 5, 8.4, 0.2), (677, 5, 8.8, 0.2), (757, 10, 11.3, 0.2), (790, 10, 12.5, 0.65),
                   (853, 10, 14.6, 0.2), (905, 10, 15.1, 0.2), (930, 10, 16.6, 0.5), (944, 10, 16.6, 0.2),
                   (978, 10, 17.3, 1.1), (1172, 100, 27.0, 1.5), (1310, 100, 36.7, 2.0), (1492, 100, 44.7, 1.5))
    _line = sorted((pp, tk) for pp, tk, _f in _imt.LIQUID_LINE)

    def _reinhardt(p_gpa):
        for (p0, t0), (p1, t1) in zip(_line, _line[1:]):
            if p0 <= p_gpa <= p1:
                return t0 + (t1 - t0) * (p_gpa - p0) / (p1 - p0)
        return None
    cold_both = 0
    band = []
    high = []
    for tm, st_, pm, _sp in QUEYROUX_S1:
        ia = water_t_melt(pm * 1e9) if pm <= 20.6 else None
        rh = _reinhardt(pm)
        if pm <= 20.6:
            if ia < tm - st_ and (rh is None or rh < tm - st_):
                cold_both += 1
            if 16.5 <= pm <= 20.6:
                band.append((pm, tm, st_, ia - tm, rh - tm))
        else:
            high.append((pm, tm, st_, rh - tm, abs(rh - tm) <= st_))
    ok = cold_both == 9 and all(d_i < -20 * st_ and d_r < -20 * st_ for _p, _t, st_, d_i, d_r in band)
    if not ok:
        fails.append("Queyroux Table S1: 대역 안 측정이 두 곡선보다 뜨겁다는 기록이 더는 성립하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 20.6 GPa 아래 9 점 전부에서 IAPWS 와 Reinhardt 가 측정보다 차갑다; 대역 안 3 점: "
          + " · ".join(f"{p:.1f} GPa {t}±{s_} K → IAPWS {di:+.0f} / Reinhardt {dr:+.0f} K" for p, t, s_, di, dr in band))
    inside = [x for x in high if x[4]]
    ok = len(inside) == 1 and inside[0][0] == 27.0 and all(x[3] > 0 for x in high if not x[4])
    if not ok:
        fails.append("Queyroux Table S1: 27 GPa 위의 기록(27 에서 안, 36.7·44.7 에서 Reinhardt 가 더 뜨거움)이 성립하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 27 GPa 위(σT 100 K): "
          + " · ".join(f"{p:.1f} GPa Reinhardt {d:+.0f} K ({'안' if i else '밖'})" for p, _t, _s, d, i in high)
          + " — Queyroux 가족이 레이저가열 가족보다 100–150 K 낮다는 그들의 진술과 같은 방향")
    ok = all(s_ / t < 0.05 for t, s_, p, _ in QUEYROUX_S1 if p <= 17.3) and all(s_ / t > 0.05 for t, s_, p, _ in QUEYROUX_S1 if p >= 27.0)
    if not ok:
        fails.append("Queyroux Table S1 의 σT/Tm 이 기록(17.3 GPa 까지 5 % 아래, 27 GPa 위 5 % 위)과 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] σT/Tm: 17.3 GPa 까지 0.7–1.3 % (5 % 문턱 아래) · 27 GPa 위 6.7–8.5 % (위) — 등급은 측정이 아니라 곡선이 막는다")

    print("\n중간 단 (C11) — 선언된 분화 전선 위의 원시 지각")
    # 전선 1.0 은 예전 열 그대로다: 같은 천체를 명시적으로 1.0 으로 풀면 비트까지 같아야 한다.
    same = solve(m_eur, differentiation_front=1.0, **eur)
    ok = (same.values["radius"] == with_ocean.values["radius"]
          and same.values["nmoi"] == with_ocean.values["nmoi"])
    if not ok:
        fails.append("differentiation_front=1.0 이 기본 경로와 비트까지 같지 않다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 전선 1.0 = 지각 없음: 기본 풀이와 비트까지 같다")
    # 270 K 의 지각은 자기모순이다 — 0.02–0.6 GPa 의 얼음 Ih·III·V 녹는점(251–273 K)이 그 아래에 있다.
    warm_crust = solve(m_eur, differentiation_front=0.8, crust_rock_fraction=0.6, **eur)
    ok = (not warm_crust.applicable) and "녹는곡선 위" in (warm_crust.reason or "")
    if not ok:
        fails.append("270 K 의 지각이 거절되지 않았다 — 녹은 적 없는 지각이 녹는곡선 위에 앉았다")
    print(f"  [{'PASS' if ok else 'FAIL'}] {ICY_T_POT:.0f} K 의 지각(전선 0.8 · 암석 0.6)은 자기모순이라 거절: "
          f"'{(warm_crust.reason or '')[:60]}…'")
    # 200 K 에서는 지각이 선다. 방향은 사전 등록대로: 지각 암석은 C/MR² 를 올리고 공극은 내린다.
    cold = dict(eur, potential_temperature=200.0)
    ref = solve(m_eur, **cold)
    crust = solve(m_eur, differentiation_front=0.8, crust_rock_fraction=0.6, **cold)
    porous = solve(m_eur, differentiation_front=0.8, crust_rock_fraction=0.6, crust_porosity=True, **cold)
    ok = (ref.applicable and crust.applicable and porous.applicable)
    if not ok:
        fails.append("200 K 유로파형의 지각 풀이가 거절됐다: " + " / ".join((r.reason or "")[:80] for r in (ref, crust, porous) if not r.applicable))
        print("  [FAIL] 200 K 유로파형 지각 풀이 거절")
    if ok:
        ok = (crust.values["nmoi"] > ref.values["nmoi"] > 0.0
              and porous.values["nmoi"] < crust.values["nmoi"]
              and crust.values["crust_thickness"] > 0.0 and crust.grade == "analog"
              and "crust_primordial" in crust.regime)
        if not ok:
            fails.append("지각의 방향이 사전 등록과 어긋난다 — 암석은 올리고 공극은 내려야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] 200 K 유로파형: 지각 없음 C/MR² {ref.values['nmoi']:.4f} → 전선 0.8 · 암석 0.6 "
              f"{crust.values['nmoi']:.4f} (두께 {crust.values['crust_thickness']:.0f} km) → 공극 얹으면 "
              f"{porous.values['nmoi']:.4f}; analog, 층 이름에 crust_primordial")
    # 거절 셋: 얼음 없는 전선, 암석 0 의 지각, 조성보다 많이 요구하는 지각, 두 공극 법칙.
    bad = [solve(0.5, core_mass_fraction=0.3, differentiation_front=0.8, crust_rock_fraction=0.5, potential_temperature=1600.0),
           solve(m_eur, differentiation_front=0.8, **cold),
           solve(m_eur, differentiation_front=0.5, crust_rock_fraction=0.2, **cold),
           solve(m_eur, differentiation_front=0.8, crust_rock_fraction=0.4, crust_porosity=True, initial_porosity=0.3, **cold)]
    ok = all(not r.applicable for r in bad)
    if not ok:
        fails.append("지각 선언의 자기모순을 거절하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 거절 넷: 얼음 없는 전선 · 암석 0 의 지각 · 조성을 넘는 지각 · 두 공극 법칙")


    print("\n얼음 X — 적합이 자기 출처를 재현하는가 (SeaFreeze 있을 때만)")
    fails += _ice_x_crosscheck()

    print("\n얼음 X — 이음매와 온도 천장")
    from eos import (H2O as _H2O, ICE_VII_TO_X, ICE_VII_X_T_MAX, ICE_X_P_MAX,
                     PhaseGap)
    vii = [x for x in _H2O.phases if x.name == "ice_vii"][0]
    icex = [x for x in _H2O.phases if x.name == "ice_x"][0]
    seam = vii.density(ICE_VII_TO_X) / icex.density(ICE_VII_TO_X) - 1.0
    ok = abs(seam / ICE_X_SEAM - 1.0) <= ICE_X_SEAM_TOL
    if not ok:
        fails.append(f"37.4 GPa 이음매가 {seam * 100:+.2f} %, 기록된 값은 "
                     f"{ICE_X_SEAM * 100:+.2f} %")
    print(f"  [{'PASS' if ok else 'FAIL'}] 37.4 GPa 이음매 {seam * 100:+.2f} % "
          f"(기록 {ICE_X_SEAM * 100:+.2f} %) — ice_vii {vii.density(ICE_VII_TO_X):.1f} 대 "
          f"ice_x {icex.density(ICE_VII_TO_X):.1f} kg/m³")
    print(f"         규산염 이음매의 0.21 % 보다 열 배 넓다. 1987년 실험 적합을 37.4 GPa "
          f"까지 끌고 간 값과 2015년 퍼텐셜의 차이이고, 어느 쪽도 상대에 맞춰 당기지 "
          f"않았다 — 당기면 우리 출력에 적합하는 것이다.")
    p_sup, t_sup = MILLOT_SUPERIONIC
    ok = ICE_VII_X_T_MAX < t_sup
    if not ok:
        fails.append(f"온도 천장 {ICE_VII_X_T_MAX:.0f} K 가 초이온상 하한 {t_sup:.0f} K "
                     f"위다 — 초이온상을 얼음 X 라고 부르게 된다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 온도 천장 {ICE_VII_X_T_MAX:.0f} K 가 "
          f"초이온상 하한 {t_sup:.0f} K (Millot+ 2019, {p_sup / 1e9:.0f} GPa 위) 아래다")
    got = None
    try:
        _H2O.density(200e9, ICE_VII_X_T_MAX + 100.0)
    except PhaseGap as gap:
        got = gap
    ok = got is not None and "초이온상" in got.reason and got.temperature_k > 0
    if not ok:
        fails.append("온도 천장 위에서 초이온상을 이름 대며 거절하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 천장 위는 값이 아니라 거절이고, 그 위가 "
          f"무엇인지를 말한다")
    got = None
    try:
        _H2O.density(ICE_X_P_MAX * 1.01)
    except PhaseGap as gap:
        got = gap
    ok = got is not None and "매듭 구간" in got.reason
    if not ok:
        fails.append("1 TPa 위에서 이름을 대며 거절하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] {ICE_X_P_MAX / 1e9:.0f} GPa 위도 이름을 대며 "
          f"거절한다 — 물리가 없는 게 아니라 읽을 형태가 없다고 말한다")

    shallow = solve(0.5, composition="water")
    deep = solve(1.0, composition="water")
    ok = (shallow.grade == "calibrated" and deep.grade == "analog"
          and any("얼음 X 까지 내려갔다" in n for n in deep.notes))
    if not ok:
        fails.append(f"얼음 X 를 밟아도 등급이 안 내려간다 — 0.5 M⊕ {shallow.grade}, "
                     f"1.0 M⊕ {deep.grade}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 얼음 X 를 밟으면 등급이 내려간다 — "
          f"0.5 M⊕ {shallow.grade} → 1.0 M⊕ {deep.grade}, note 가 이유를 댄다")

    print("\n얼음 조성의 질량 상한 — 닫혀 있던 조성이 열렸는가")
    for label, kw in ICE_CEILING_CASES:
        m = ice_mass_ceiling(**kw)
        print(f"         {label:34} {m:9.4f} M⊕")
    m_water = ice_mass_ceiling(composition="water")
    ok = m_water > 1.0
    if not ok:
        fails.append(f"water 프리셋 상한이 {m_water:.4f} M⊕ 로 아직 지구 아래다")
    print(f"  [{'PASS' if ok else 'FAIL'}] water 프리셋이 {m_water:.3f} M⊕ 까지 풀린다 "
          f"(2026-08-27 에는 0.0398 M⊕ 로 달의 3.2 배였다)")

    print("\n냉측 일반 수정 (브리프 22) — 물 기둥이 가장 안쪽인 천체가 스텁 없이 적분되는가")
    # 2026-08-31 까지 이 구성(C13 끝 B: 규산염층 없음, 암석은 외피 Z)은 **1 ULP 의 유령
    # 규산염 스텁이 있어야만** 풀렸다 — 중심 씨앗이 디스패치 없이 정적 사다리를 불러
    # 매듭 상한(1 TPa; 데이터 천장 ~355 GPa — C6)이나 초이온 온도 상한에서 죽었고, 사격의 괄호도 사다리 상한에
    # 잘렸다. 지금은 씨앗이 걸음과 같은 디스패치를 받는다. 수렴점은 스텁 실험(ε=1e-9,
    # 2026-08-31)의 값이고, 여기서는 그 자리의 적분 한 번이 서고 질량이 닫히는지만 본다.
    for name_, m_, pc_gpa, tc_k in (("Uranus", 14.536, 784.0, 4953.0),
                                    ("Neptune", 17.147, 984.0, 4901.0)):
        gmf_ = (2.0 if name_ == "Uranus" else 2.2) / m_
        rockf_ = (0.79 if name_ == "Uranus" else 1.04) / m_
        try:
            stb = interior.integrate(pc_gpa * 1e9, m_ * EARTH_MASS_KG, 0.0, 1.0 - gmf_ - rockf_,
                            "fe_prem", gmf=gmf_ + rockf_, envelope_z=rockf_ / (gmf_ + rockf_),
                            t_center=tc_k, t_pot=76.0 if name_ == "Uranus" else 72.0)
            ratio = stb.mass_kg / (m_ * EARTH_MASS_KG)
            ok = abs(ratio - 1.0) < 0.05
            if not ok:
                fails.append(f"냉측: {name_} 끝 B 적분의 질량이 목표의 {ratio:.3f} 배다")
            print(f"  [{'PASS' if ok else 'FAIL'}] {name_} 끝 B (암석을 외피 Z 로, 규산염층 0) — "
                  f"수렴점 적분이 서고 질량/목표 {ratio:.4f}")
        except PhaseGap as g_:
            fails.append(f"냉측: {name_} 끝 B 가 다시 죽는다 — {g_.reason[:80]}")
            print(f"  [FAIL] {name_} 끝 B 거절: {g_.reason[:80]}")
    # 근거 천장 자체는 남아 있어야 한다 — 온도가 흐르지 않는 차가운 물 천체는 여전히
    # 이름을 대며 거절한다 (사다리의 1 TPa 는 표현이 끝나는 실재하는 자리다 — 매듭 상자; C6).
    try:
        interior.integrate(1.2e12, 10.0 * EARTH_MASS_KG, 0.0, 1.0, "fe_prem")
        fails.append("냉측: 온도 없는 물 천체가 1.2 TPa 중심을 거절하지 않는다")
        print("  [FAIL] 차가운 근거 천장이 사라졌다")
    except PhaseGap as g_:
        ok = "근거 구간의 상한" in g_.reason and not g_.too_cold
        if not ok:
            fails.append("냉측: 차가운 물 천체의 천장 거절이 이름·방향을 잃었다")
        print(f"  [{'PASS' if ok else 'FAIL'}] 온도 없는 1.2 TPa 물 중심은 여전히 이름 대며 거절 "
              f"(too_cold={g_.too_cold}): '{g_.reason[:50]}…'")

    print("\n스팀 (IAPWS-IF97 r1·2, 브리프 25) — 전사가 표준의 인쇄 검증값을 재현하는가")
    import steam_if97
    worst_if97 = steam_if97.verify()
    ok = worst_if97 < 1e-8
    if not ok:
        fails.append(f"IF97 전사가 표준 검증값과 {worst_if97:.1e} 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] Tables 5·15·35 + B23 점, 최악 상대오차 {worst_if97:.1e} "
          "(표준이 9유효숫자로 인쇄)")
    # region 3 삼각형(623.15–863.15 K × p_B23–100 MPa)도 같은 날 전사됐다(벽의 잔여가
    # 정확히 거기였다). 벽의 실측 표본 두 점이 열려 있고, region 5(1073 K 위)는 이름으로 밖.
    ok = (steam_if97.region(50e6, 700.0) == 3 and steam_if97.in_domain(50e6, 700.0)
          and steam_if97.in_domain(22.1e6, 661.0) and steam_if97.in_domain(97e6, 645.0)
          and steam_if97.in_domain(2e6, 1000.0) and not steam_if97.in_domain(2e6, 1100.0))
    if not ok:
        fails.append("IF97 영역 판정이 어긋난다 — region 1·2·3 창 또는 region 5 경계가 뒤바뀌었다")
    print(f"  [{'PASS' if ok else 'FAIL'}] region 3(50 MPa·700 K)과 벽 표본(22.1 MPa·661 K, "
          "97 MPa·645 K) 열림 · region 5(1100 K)는 밖")

    print("\n서브넵튠 — 가스 외피 아래 철 핵이 풀리고, 사다리가 천장 거절을 지어내지 않는가")
    # 2026-08-29 까지 이 둘은 fe_prem 의 12 TPa 천장 거절을 냈다 — 5 M⊕ 가 닿을 수 없는 압력이다.
    # 원인은 외피 바닥의 표 영역 이탈을 표면으로 오인한 것이었다 (sub-neptune-context-notes.md).
    # 여기서 지키는 것은 수치가 아니라 **기작** 이다: 풀리거나, 이름을 대며 거절하거나.
    gj = solve(8.41, core_mass_fraction=0.325 * 0.98, ice_mass_fraction=0.0,
               gas_mass_fraction=0.02, body_class="sub_neptune", potential_temperature=300.0)
    ok = gj.applicable and gj.converged and gj.grade == "analog"
    if not ok:
        fails.append(f"서브넵튠: 가스 외피 아래 철 핵이 안 풀린다 — "
                     f"{gj.reason[:80] if not gj.applicable else gj.converged}")
    print(f"  [{'PASS' if ok else 'FAIL'}] GJ 1214 b (8.41 M⊕ · H/He 2 % · 1 bar 300 K): "
          + (f"R {gj.values['radius']:.3f} R⊕ (발표 2.733) · converged {gj.converged} · analog"
             if gj.applicable else "거절"))
    # 20 % 는 이제 풀린다 (12.7 R⊕ — 그 선언에 충실한 답이다). 순수 가스 5 M⊕ 가 거절이다: 1 bar
    # 500 K 단열선이 묶이는 가장 뜨거운 치밀한 해가 1 bar 에서 145 K 뿐이라, 그 위는 부푼 가지다.
    hot = solve(5.0, core_mass_fraction=0.0, ice_mass_fraction=0.0, gas_mass_fraction=1.0,
                body_class="giant", potential_temperature=500.0)
    ok = (not hot.applicable and "묶이지 않는다" in hot.reason and "천장" not in hot.reason
          and "12000" not in hot.reason)
    if not ok:
        fails.append("서브넵튠: 5 M⊕ · 순수 가스 · 500 K 가 '묶이지 않는 외피' 로 거절해야 하는데 "
                     f"{'풀렸다' if hot.applicable else hot.reason[:80]}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 5 M⊕ · 순수 가스 · 1 bar 500 K: "
          + ("풀렸다 (거절해야 한다)" if hot.applicable else
             "거절하며 묶이는 가장 뜨거운 해와 벽을 인용한다 — 천장이 아니다"))
    gasless = solve(8.0, core_mass_fraction=0.3, body_class="sub_neptune",
                    potential_temperature=300.0)
    ok = not gasless.applicable and "선언하면 풀린다" in gasless.reason
    if not ok:
        fails.append("서브넵튠: 가스질량분율 없이 선언하면 그것이 선언임을 말하며 거절해야 한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 가스질량분율 없는 서브넵튠은 선언을 요구하며 거절한다")

    print("\n얼음거대행성 — 열렸는가, 그리고 뜨거운 물이 자기 구간을 지키는가")
    # **적분은 여기서 안 돌린다.** 얼음거대행성 하나가 24 ~ 500 초라 check.sh 의 예산에
    # 안 들어간다. 천왕성·해왕성 표는 `--icegiant` 가 낸다. 여기서는 적분하지 않고 되는
    # 것만 짚는다 — 배선과 재료의 울타리다.
    from interior import FLUID_CLASSES, ICE_GIANT_CLASSES
    from eos import H2O_HOT, PhaseGap as _PG
    import water_hot as _wh
    ok = "ice_giant" not in FLUID_CLASSES and "ice_giant" in ICE_GIANT_CLASSES
    if not ok:
        fails.append("ice_giant 가 아직 FLUID_CLASSES 에 있다")
    print(f"  [{'PASS' if ok else 'FAIL'}] ice_giant 가 거절 목록에서 나왔다 — "
          f"남은 유체 거절은 {FLUID_CLASSES}")
    for t, needle, label in ((0.0, "등온 경로로 풀 수 없다", "온도 미선언"),
                             (800.0, "하한", "1000 K 아래 (Mazevet 이 적은 유체의 바닥)"),
                             (60000.0, "상한", "50000 K 위 (적합의 상한)")):
        got = None
        try:
            H2O_HOT.density(100e9, t)
        except _PG as gap:
            got = gap
        ok = got is not None and needle in got.reason
        if not ok:
            fails.append(f"뜨거운 물이 {label} 에서 이름 대며 거절하지 않는다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:28} → 이름 대며 거절한다")
    # 2026-08-30 까지는 두 수가 같아야 했다 ("온도 축에 틈이 없다"). 그 항등식이 바로 적합의 천장을
    # 상 경계로 쓰는 혼동이었다. 지금은 녹는곡선이 어느 쪽인지를 정하고, 두 수는 출처가 다르다 —
    # 1000 K 는 Mazevet+ 2019 §3.1 이 유체에 대해 적은 바닥, 1800 K 는 French & Redmer 2015 매듭의 끝.
    ok = _wh.T_MIN == 1000.0 and ICE_VII_X_T_MAX == 1800.0 and _wh.T_MIN != ICE_VII_X_T_MAX
    if not ok:
        fails.append(f"뜨거운 물의 하한 {_wh.T_MIN} 과 사다리 천장 {ICE_VII_X_T_MAX} 가 "
                     "기록(1000 · 1800)과 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 뜨거운 물의 하한 {_wh.T_MIN:.0f} K (Mazevet §3.1) 과 사다리 "
          f"천장 {ICE_VII_X_T_MAX:.0f} K (French & Redmer 매듭) 는 다른 수다 — 사이는 녹는곡선이 가른다")

    print("\n얼음거대행성 — 거절이 거리를 수로 말하는가")
    from eos import (AVL_ICES_DEVIATION, AVL_ICES_TERNARY_DEVIATION,
                     AVL_VOLUME_DEVIATION, ICE_VII_X_T_MAX,
                     SOLAR_ICE_MASS_FRACTIONS)
    ok = abs(sum(SOLAR_ICE_MASS_FRACTIONS.values()) - 1.0) < 1e-12
    if not ok:
        fails.append("태양 조성 얼음 질량분율의 합이 1 이 아니다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 태양 조성 얼음 분율 "
          f"{SOLAR_ICE_MASS_FRACTIONS} 의 합이 1 이다")
    ok = AVL_ICES_TERNARY_DEVIATION < AVL_ICES_DEVIATION < AVL_VOLUME_DEVIATION
    if not ok:
        fails.append("부피 가법 혼합의 유효 한계 셋이 순서대로가 아니다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 부피 가법 혼합의 한계: 얼음 삼성분 "
          f"{AVL_ICES_TERNARY_DEVIATION * 100:.1f} % < 얼음 이성분 "
          f"{AVL_ICES_DEVIATION * 100:.0f} % < H-He {AVL_VOLUME_DEVIATION * 100:.0f} % — "
          f"행성 얼음이 H-He 보다 얌전하다")

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
