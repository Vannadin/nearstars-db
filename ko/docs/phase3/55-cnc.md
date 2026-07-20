<!-- 55 Cnc A Phase 3 합성. cfg-ready 결정과 근거 -->
# 55 Cancri A — Phase 3 합성

55 Cancri A(ρ¹ Cnc, HD 75732, HIP 43587, HR 3522, Gaia DR3
704967037090946688)는 밝고 가까운 K0 IV-V 왜성으로 G–K 경계에 자리하며,
Gaia DR3 시차 79.448 ± 0.043 mas 기준 태양에서 12.59 ± 0.01 pc(41.0 광년)
떨어져 있습니다. V = 5.95 로 게자리에서 막 육안 한계에 걸리는 밝기이며,
통과(transit)하는 외계행성을 거느린 것으로 알려진 가장 밝은 별 셋 중
하나입니다. 기본 항성 파라미터는 von Braun 외 2011 의 전용 항성-파라미터
논문에 정박해 있으며, 이 연구는 CHARA 간섭계로 별을 직접 분해했습니다.
θ_LD = 0.711 ± 0.004 mas → R = 0.943 ± 0.010 R☉, 직접 측정한
Teff = 5196 ± 24 K, 볼로메트릭 광도 L = 0.582 ± 0.014 L☉ 입니다. 이 별은
영년 주계열에서 약간 진화한 상태라 IV-V 광도 등급을 받지만, 그 외에는
약간 더 차갑고 약간 덜 밝은 준-태양형 항성입니다. 또한 극단적으로
금속이 풍부한 별([Fe/H] ≈ +0.31 ~ +0.42)로 유명한데, 이 값은 프로젝트
정책상 여기서 큐레이션하지 않습니다.

이 별은 늙고 매우 조용합니다. Bourrier 외 2018 은 자전 주기 38.8 ± 0.05 d
(자기 주기를 제거한 뒤 Hα 활동 지수 잔차에 사인 곡선을 맞춰 도출, Season-9
APT 측광의 40.4 d 와 Henry 2000 의 ~39 d Ca II 주기가 보강), 채층 지수
log R'HK = −5.03, 그리고 ≈ 10.5 ± 0.3 yr 의 태양형 자기 활동 주기(KECK
HIRES S-지수, Hα 에서는 ~11.8 yr)를 측정하여, 55 Cnc A 가 늙은(~10 Gyr)
비활동성 항성임을 확인했습니다. Moutou 외 2025 는 P_rot = 38.7 ± 0.8 d
(준주기 GPR)를 독립적으로 재확인하고, 활동 극소기에 ~0.3 G, 극대기에
~3 G 에 불과한 대규모 자기장—태양 자기장의 약 10 분의 1—을 측정했습니다.
이 계는 행성 다섯 개(주기 순으로 e, b, c, f, d)를 거느리며, USP 용암
초지구부터 차가운 ~3.8 M_Jup 거대 행성까지 걸쳐 있고, 자기 주기와 얽힌
장주기 후보 행성(여섯 번째 가능성)도 있습니다(Moutou 2025).

두 번째 태양이 이 계를 공유합니다. 55 Cnc B 는 중간 M형 적색왜성(M4.5V,
Teff ≈ 3200 K, M ≈ 0.26 M☉)으로, 투영 이격 ~1065 AU(육안 84″,
Eggenberger 2004 / Mugrauer 2006), 추정 공전 주기 ~30,000 yr(Moutou
2025)에 자리합니다. 이미 NearStars DB 에 별도 천체(`55_cnc_b`, 자체 행성
두 개 보유)로 등록되어 있으며 **공표된 케플러 궤도가 없어**, A–B 쌍은
모델링하지 않습니다(주석만). 따라서 여기서 이성 궤도는 합성하지 않습니다.
A 의 행성에서 보면 B 는 멀리 떨어진 희미한 주황-적색의 두 번째 태양처럼
보일 것입니다.

**NearStars 시나리오 선택: 조용하고 약간 진화한 노란-주황색 K0 IV-V
준-태양형 항성—태양보다 약간 차갑고 어두우며 극단적으로 금속이 풍부하고
태양형 ~10.5 yr 활동 주기를 가짐—을 von Braun 2011 CHARA 간섭계에
정박시키고, 다섯 행성 무리와 ~1065 AU 의 먼 M4.5V 적색왜성 동반성(55 Cnc B)을
희미한 두 번째 태양으로 함께 묘사합니다.** 모든 물리/활동 행은 고증 파라미터
집합을 따르며, 시각 hex 색조와 동반성 이벤트 기하만 tie-break 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K0 IV-V | high | DB(Gaia / SIMBAD). G–K 경계의 약간 진화한 준거성-왜성, G8 V 로도 자주 인용됨(Bourrier 2018) |
| `mass_msun` | 0.905 ± 0.015 | high | von Braun 2011 — 진화 모델(Phase 2 추천. Crida 2018 통과-밀도 1.015 ± 0.051 은 기록된 대안) |
| `radius_rsun` | 0.943 ± 0.010 | high | von Braun 2011 — CHARA 간섭계, θ_LD 0.711 ± 0.004 mas(Phase 2 추천. 이전에 Bourrier 2018 로 오귀속됐던 DB 반지름을 재정박) |
| `teff_k` | 5196 ± 24 | high | von Braun 2011 — 간섭계 θ_LD + 볼로메트릭 플럭스(Phase 2 추천. Yee 2017 분광 5172 ± 18, Moutou 2025 SPIRou 5198 ± 31 이 오차 내 일치) |
| `luminosity_lsun` | 0.582 ± 0.014 | high | von Braun 2011 — 볼로메트릭 플럭스(Phase 2 추천) |
| `metallicity_fe_h_dex` | null(문헌 ~+0.31 ~ +0.42) | low | [[feedback-skip-metallicity]] 정책상 스킵. 극단적 금속 풍부(Soubiran 2024 +0.32 ± 0.02, Houdebine 2016 +0.42). 색 효과는 지각 한계 이하라 큐레이션 안 함 |
| `age_gyr` | ~10(늙음) | medium | Bourrier 2018 — log R'HK + 느린 자전으로 추론한 늙고 조용한 별. Moutou 2025 는 Ligi 2016 의 31 Myr 간섭계-반지름 대안 대신 >10 Gyr 가지를 채택 |
| `rotation_period_days` | 38.8 ± 0.05 | high | Bourrier 2018 — Hα 활동 지수 잔차 사인 피팅(Phase 2 추천). Moutou 2025 GPR 38.7 ± 0.8, Folsom 2020 ZDI 39 d, Henry 2000 Ca II ~39 d 가 보강 |
| `activity_log_rhk` | −5.03 | high | Bourrier 2018(Phase 2 추천). Moutou 2025 의 21년 평균 −5.01(Isaacson 2024 데이터)이 보강 — 매우 비활동성 |
| `activity_cycle_years` | 10.5 ± 0.3 | high | Bourrier 2018 — KECK HIRES S-지수 태양형 주기(Hα 에서는 ~11.8 yr, Baluev 2015 RV 12.6 yr 과 일치) |
| `large_scale_field_g_min` | 0.3 | medium | Moutou 2025 — SPIRou ZDI 활동 극소기 비부호 자기장(subset #1/#2) |
| `large_scale_field_g_max` | 3.0 | medium | Moutou 2025 — 극대기 근처 자기장(Folsom 2020 이 2017년에 ~3 G 측정). 태양의 7–15 G 보다 ~10 배 약함 |
| `x_ray_log_lx_cgs_min` | 26.8 | low | Tie-break: 공표된 장기 X선 주기 없음. log R'HK = −5.0 의 조용한 K0 V 유사체(HD 69830 / α Cen B 영역)에서 스케일링 |
| `x_ray_log_lx_cgs_max` | 27.3 | low | Tie-break: 10.5 yr 주기에 걸쳐 태양형 진폭 배수 ~3 가정 |
| `limb_darkening_alpha_h` | 0.16 | medium | 5196 K 1D 모델 대기의 H 밴드 멱법칙 추정(Claret–Bloemen 2011 스케일링). 55 Cnc A 에 대해 직접 측정된 값 아님 |
| `visual_surface_tint_hex_primary` | `#ffeccf`(따뜻한 노랑-주황, 태양의 `#fff8f0` 과 HD 69830 의 `#ffe8c8` 사이) | medium | Tie-break: 5196 K K0 IV-V 흑체. HD 69830 의 5394 K 보다 ~200 K 차가워 약간 더 따뜻하고 주황. 초태양 [Fe/H] 의 약한 line-blanketing 적색화는 지각 한계 이하 |
| `stellar_color_temp_k` | 5196 | high | Teff 에서 유도(von Braun 2011) |
| `visual_spot_coverage_max` | 0.005 | low | 합성: 매우 비활동성(log R'HK −5.03), 주기 극대기에 디스크의 ~0.5% 흑점 면적(Bourrier 2018 측광 진폭 ~2 mmag) |
| `visual_corona_extent_radii` | 3.0 | low | 합성: 늙고 비활동성인 K0 왜성에 대한 조용한 태양형 코로나 |
| `companion_present` | true(55 Cnc B, M4.5V, 투영 ~1065 AU) | high | Eggenberger 2004 / Mugrauer 2006 — 육안 84″. Moutou 2025 P ≈ 30,000 yr. 이미 DB 에 `55_cnc_b` 로 등록. A–B 는 공표된 케플러 궤도 없음(모델링 안 함) |
| `visual_companion_event_distant_red_second_sun` | true | low | Tie-break: A 의 어느 행성에서든 B 는 희미한 주황-적색 광점(M4.5V) — 이성 디스크가 아니라 먼 두 번째 태양 |

## Surface synthesis

55 Cnc A 의 광구는 G–K 경계에 자리하며 태양보다 ~580 K 차갑습니다. von
Braun 2011 은 CHARA 배열로 별을 직접 분해(θ_LD = 0.711 ± 0.004 mas)하여
R = 0.943 ± 0.010 R☉ 와 볼로메트릭 Teff = 5196 ± 24 K 를 얻었으며, 이는
Yee 2017 고분해능 분광 5172 ± 18 K 및 Moutou 2025 SPIRou Zeeturbo
5198 ± 31 K 와 오차 내에서 일치합니다. IV-V 광도 등급은 별이 영년
주계열에서 진화하기 시작했음을 알려주며, 0.943 R☉ 외피와 결합하면 적당한
0.582 L☉ 볼로메트릭 광도가 나옵니다. cfg `limb_darkening_alpha_h` 는 1D
대기 멱법칙 추정값 α(H) ≈ 0.16 으로, 더 차가운 광구에서 태양의 0.14 보다
약간 강하며, Claret–Bloemen 2011 격자(log g ≈ 4.4, Teff ≈ 5200 K)와
일치합니다. 이 별에 대해 공표된 직접 간섭계 주연감광 프로파일은 없습니다.

가장 두드러진 화학적 특징은 극단적 금속 풍부도입니다. 55 Cnc A 는 태양
근방에서 가장 금속이 풍부한 별 중 하나로, [Fe/H] ≈ +0.31 ~ +0.42
(Soubiran 2024 +0.32 ± 0.02, Houdebine 2016 +0.42, 문헌 분포 +0.25 ~
+0.45)입니다. 프로젝트 정책상 Phase 2 측정값으로 큐레이션하지 않지만—여기서
생기는 line-blanketing 적색화는 렌더링 지각 한계 이하라서—55 Cnc A 가
이토록 풍부하고 무거운 행성 무리를 형성한 물리적 이유로서 주목할 만합니다.
입상 무늬는 태양형일 것으로 예상되나 더 차가운 대류 전환에서 선형 스케일이
~10% 작습니다.

흑점 면적은 매우 낮습니다. log R'HK = −5.03(Bourrier 2018)은 55 Cnc A 를
국부 G/K 활동 분포의 하위 10분위에 두며, 현대 태양보다 조용하고, 활동
주기에 걸친 최대-최소 측광 변동은 ~2 mmag 에 불과합니다. cfg 는 조용한
태양형 흑점 외피(주기 극대기에 디스크의 ~0.5%)를 채택하고 두드러진
활동 영역 구조는 렌더링하지 않습니다. Moutou 2025 의 SPIRou ZDI 지도는
극소기에 0.3 G 에 불과한 폴로이달, 주로 비대칭의 대규모 자기장을
보여주는데—태양 평균 자기장의 약 10 분의 1입니다.

시각 크림-주황 색조 `#ffeccf` 는 5196 K K0 IV-V 흑체에서 보간한 값으로,
HD 69830(5394 K, `#ffe8c8`)보다 ~200 K 차가워 반 단계 더 따뜻하고
주황이지만, α Cen B(K1V)의 짙은 주황에는 한참 못 미칩니다. 초태양 금속
풍부도가 SED 를 미세하게 적색으로 밀지만 렌더링 분해능에서는 지각되지
않습니다.

## Atmosphere synthesis

55 Cnc A 는 늙고 비활동성인 후기-G/초기-K 왜성에 전형적인 조용한 K0
채층–전이영역–코로나 구조를 가집니다. Ca II H&K 채층 지수 log R'HK =
−5.03(Bourrier 2018)은 Moutou 2025 의 21년 평균 −5.01 로 확인되며,
비활동성 바닥에 자리합니다. 대다수 조용한 항성과 달리 55 Cnc A 는
**잘 특징화된 활동 주기**를 가집니다. Bourrier 2018 은 KECK HIRES S-지수에서
태양형 ≈ 10.5 ± 0.3 yr 주기(진폭 0.024, 태양의 거의 두 배)를 검출했고,
Hα 에서 ~11.8 yr, 아카이브 RV 에서 ~12.6 yr(Baluev 2015)로 일관됩니다.
이 주기에서 Hα 와 S-지수의 반상관 관계는 몇몇 느린 자전 항성에서 관측되는
거동을 닮았습니다.

대규모 자기장은 유난히 약합니다. Moutou 2025 의 SPIRou 분광편광 캠페인은
별을 활동 극소기에 포착해 비부호 자기장을 0.3 G 로만 측정했고, 극소기를
벗어나며 ~0.9 G 로, 2017 극대기 근처에서는 ~3 G(Folsom 2020)로
상승했습니다—태양의 7–15 G 범위보다 약 10 배 약합니다. 이는 매우 낮은
log R'HK 및 늙은 나이와 일관됩니다.

55 Cnc A 에 대해 공표된 장기 X선 주기는 없습니다. cfg 는 log L_X 범위
26.8–27.3 cgs 를 채택하여 태양-조용기부터 태양-주기-극대기 유사 수준까지
포괄합니다—측정된 X선 주기 진폭이 없는 상황에서의 tie-break 로, 조용한
K0 V 영역에서 스케일링했습니다. 통합 XUV 광도는 10⁻⁴ L_bol 보다 한참
아래라, 별의 거주 가능 영역(~0.67–1.32 AU, von Braun 2011)에서 Gyr
시간 척도에 걸쳐 지구형 대기를 의미 있게 침식하기엔 너무 약합니다—다만
이심 궤도의 일부를 그 영역에서 보내는 행성 f 자체가 거대 가스 행성입니다.

코로나/채층 시각 범위는 조용한 태양 기준—얇은 채층과 ~3 R★ 까지의
희미한 코로나—으로 렌더링하며, 10.5 yr 주기에 걸쳐 ~20% 밝아집니다.

## Rotation & spin synthesis

55 Cnc A 는 견고하게 측정된 자전 주기 P_rot = 38.8 ± 0.05 d(Bourrier
2018)를 가지며, 자기 주기를 제거한 뒤 Hα 활동 지수 잔차에 사인 곡선을
맞춰 도출했습니다. 여러 독립 채널이 이를 보강합니다. Season-9 APT 측광은
40.4 ± 0.8 d(모든 측광 시즌 가중 평균 40.04 ± 0.39 d), Henry 2000 의
Ca II 방출 모니터링은 ~39 d, Fischer 2008 의 초기 APT 측광은 42.7 ± 2.5 d
를 줍니다. Moutou 2025 는 준주기 GPR 피팅에서 38.7 ± 0.8 d 를 독립
재확인하고 Folsom 2020 의 39 d ZDI 값을 채택합니다. 방법별 34–43 d 분포는
적당한 차등 자전과 일관됩니다(Folsom 2020 은 0.065 rad/day 상한 설정).

느린 ~39 d 자전 자체가 늙은 나이의 가장 깔끔한 근거입니다. Moutou 2025 는
30 d 를 넘는 자전 주기가 30 Myr 태양형 항성에서는 예상되지 않는다고
지적하며, 이는 Ligi 2016 항성-진화 해의 젊은(31 Myr) 간섭계-반지름 가지를
배제하고 여기서 채택한 >10 Gyr 가지를 지지합니다. 느린 자전은 Skumanich
법칙을 통한 ~10 Gyr 의 자기 제동의 산물입니다.

cfg 를 좌우하는 별진동 모드 검출은 없습니다. 예측 ν_max 가 지금까지 배치된
서베이 케이던스에 비해 너무 높고, 매우 낮은 활동 바닥도 도움이 되지
않습니다. cfg 는 진동 기반 밝기 변조를 인코딩하지 않습니다. 차등 자전은
태양형으로 예상되나 직접 분해되지 않았고, 자전축 경사는 잘 제약되지
않습니다(ZDI 는 i ≈ 70–90° 가정). 시각 렌더링을 위해 NearStars 는 다섯
행성계의 평균 궤도면에 대해 적당히 기울어진 자전축을 채택합니다.

KSP 단위로 cfg 는 별의 `rotationPeriod` 를 측정된 38.8 d(Bourrier 2018)로
설정합니다—정보용입니다. Kopernicus 는 별 자전을 직접 애니메이션하지
않지만, Principia 가 자전축 부기를 위해 `rotationPeriod` 를 읽습니다.

## Visual styling

- **궤도 뷰(계 전체 렌더).** 빽빽한 안쪽 삼중주(0.015 AU 의 e, 빛에 묻힘.
  0.118 AU 의 b. 0.247 AU 의 c)와, 거주 가능 영역 안쪽 가장자리를 쓰는
  0.80 AU 의 이심 궤도 f, 그리고 5.6 AU 멀리의 차가운 거대 행성 d 를 거느린
  따뜻한 노랑-주황 K0 광점. f 와 d 사이의 ~4 AU 간극이 이 계의 정의적
  구조 특징입니다.
- **항성 디스크(클로즈업).** 교과서적 H 밴드 멱법칙 주연감광을 가진 조용한
  K0 IV-V. 입상 셀은 태양보다 약간 작으며, cfg 주기 극대기에 ~0.5%
  최대-최소의 희미한 주기 평균 흑점 밝기 변조 외에는 두드러진 활동 영역이
  없습니다.
- **항성 색.** 따뜻한 노랑-주황 `#ffeccf` — 태양의 `#fff8f0` 과 HD 69830 의
  `#ffe8c8` 사이로, ~200 K 차가운 Teff 에서 후자보다 한 단계 더 따뜻합니다.
  55 Cnc A 는 NS 카탈로그의 "약간 더 붉고 약간 진화한 준-태양형" 항목입니다.
- **활동 주기 애니메이션.** 10.5 yr 주기(Bourrier 2018)에 걸쳐 코로나가
  ~20% 밝아지고 흑점 면적이 ~0.5% 에서 정점을 찍으며, 대규모 자기장이
  0.3 G(극소기)에서 ~3 G(극대기, Moutou 2025)로 진동합니다. M형 왜성
  기준으로는 희미하고 느립니다.
- **먼 적색의 두 번째 태양(55 Cnc B).** A 의 어느 행성에서든 ~1065 AU 의
  M4.5V 동반성은 분해되지 않는 주황-적색 광점입니다—디스크를 보이기엔 너무
  멀지만(각지름 ≪ 1″), 배경 항성보다 여러 등급 밝은 알아볼 수 있는 따뜻한
  두 번째 별입니다. cfg `visual_companion_event_distant_red_second_sun` 에
  플래그됩니다. A–B 궤도는 모델링하지 않으므로(~30,000 yr 주기, 케플러 궤도
  미공표) B 의 위치는 게임플레이 시간 척도에서 고정으로 취급합니다.
- **지구에서 본 별.** V = 5.95 는 55 Cnc A 를 게자리에서 육안 한계에 둡니다.
  어두운 하늘에서는 막 보이고, 그렇지 않으면 수많은 6등급 배경 항성 중
  하나로—다섯 행성계를 분해하는 인게임 망원경 뷰로만 구별됩니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **von Braun K. et al. 2011** — *The 55 Cancri System: Fundamental
  Stellar Parameters, Habitable Zone Planet, and Super-Earth
  Diameter*, ApJ 740, 49 (`2011ApJ...740...49V`, [arXiv:1107.1936](https://arxiv.org/abs/1107.1936)).
  CHARA 간섭계: θ_LD = 0.711 ± 0.004 mas → R = 0.943 ± 0.010 R☉,
  직접 Teff = 5196 ± 24 K, 볼로메트릭 L = 0.582 ± 0.014 L☉, 진화 질량
  0.905 ± 0.015 M☉, HZ 0.67–1.32 AU. **전체 항성층의 Phase 2 정박
  (R, Teff, L, M).**
- **Bourrier V. et al. 2018** — *The 55 Cnc system reassessed*, A&A
  619, A1 (`2018A&A...619A...1B`, [arXiv:1807.04301](https://arxiv.org/abs/1807.04301)). 20년의 측광 +
  분광: P_rot = 38.8 ± 0.05 d, log R'HK = −5.03, 태양형 자기 주기
  P_mag ≈ 10.5 ± 0.3 yr(S-지수. Hα ~11.8 yr)로 늙고(~10 Gyr) 조용한
  별 확인. 자기-주기 케플러를 포함한 균질 계 재피팅. **Phase 2 추천
  질량 / 자전 / 활동 / 행성 e 정박.**
- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou: questions about the magnetic cycle of 55 Cnc A and two
  new planets around B*, A&A 705, A190 (`2026A&A...705A.190M`,
  [arXiv:2510.11523](https://arxiv.org/abs/2510.11523)). A 와 B 양쪽의 SPIRou 분광편광. P_rot = 38.7 ± 0.8 d
  (GPR), ZDI 자기장 0.3 G(극소) – 3 G(극대), 태양보다 ~10× 약함. 나이
  > 10 Gyr 채택. 외행성 d 개정(P 4799 d)과 가능한 6번째 후보 / 13.15 yr
  3.8 M_Jup 신호. 55 Cnc B 주위 행성 두 개 발견. **모델 지식 컷오프
  이후 출판 — 모든 값을 캐시 텍스트에 대조 확인.**

### Read (context / methodology, not directly decision-driving)

- **Demory B.-O. et al. 2016** — *Variability in the super-Earth
  55 Cnc e*, Nature 532, 207 (`2016Natur.532..207D`,
  [arXiv:1505.00269](https://arxiv.org/abs/1505.00269)). Spitzer 4.5 μm 주간면 열복사 변동성. 항성층이 아니라
  행성 e 의 표면/대기 합성에 정보를 줍니다.
- **Soubiran C. et al. 2024** — 55 Cnc A 의 Gaia FGK 벤치마크-별 [Fe/H]
  개정 +0.32 ± 0.02. 금속도 맥락(큐레이션 안 함).
- **Folsom C. P. et al. 2020** — 55 Cnc A 의 ZDI. P_rot = 39 d, 2017
  극대기 근처 대규모 자기장 ~3 G, 차등 자전 상한. 자전 주기 보강.
- **Henry G. W. et al. 2000** — ~39 d 자전 주기를 주는 Ca II 방출
  모니터링. 장기 활동 맥락.

### Read (instrument-only, not visual-informative)

- **Ligi R. et al. 2016** — 두 해(31 Myr 젊음 / 13.2 Gyr 늙음) 나이
  축퇴를 주는 간섭계 항성-진화 피팅. 자전 근거로 늙은 가지를 채택.
- **Crida A. et al. 2018** — 통과-밀도 + 간섭계 질량 1.015 ± 0.051 M☉ /
  R 0.98 R☉(Moutou 2025 Table 1 경유). von Braun 2011 질량/반지름의
  기록된 대안.

### Not read — no arXiv preprint or low-priority (~30 papers)

55 Cnc 동역학 안정성 학회 자료, 역사적 RV 발견 논문(Butler 1997, Marcy
2002, McArthur 2004, Fischer 2008 — 파라미터는 Bourrier 2018 / Moutou
2025 로 대체됨), 그리고 55 Cnc 를 한 추적자로만 쓰는 항성-종족 금속도
카탈로그. 완전한 필터링 bib 는 `docs/phase3/_bib/55-cnc.yaml` 에 `status`
주석과 함께 보존됩니다.

## Open items for follow-up

- **여섯 번째 행성 후보.** Moutou 2025 는 자기 주기와 얽힌 장주기(~13 yr
  또는 그 절반) 후보와, 별도의 13.15 yr / 3.8 M_Jup 외행성 신호(다른
  분해 하에서 행성 d 와 같은 천체일 수도, 별개 외행성일 수도)를 제안합니다.
  미래의 균질 nIR+광학 RV 캠페인이 주기를 행성과 분리한다면 여섯 번째
  행성 Decisions 행이 필요할 수 있습니다.
- **A–B 이성 궤도.** 공표된 케플러 궤도 없음(투영 이격 ~1065 AU, 추정
  주기 ~30,000 yr 만). Gaia DR4 의 천체측정 가속도가 궤도를 제약한다면,
  A–B 쌍을 "주석만"에서 모델링된 넓은 이성으로 격상할 수 있습니다.
- **X선 주기 검출.** 장기 X선 모니터링 없음. cfg `x_ray_log_lx_cgs_min/max`
  는 tie-break 스케일링입니다. Chandra / XMM 캠페인이 주기 진폭을 고정할 수
  있습니다.
- **금속도 격상.** [Fe/H] 는 정책상 스킵. 미래 렌더러가 line-blanketing
  적색화를 보일 만큼 민감해지면 +0.32 ~ +0.42 dex 풍부도를 큐레이션하고
  시각 색조를 재유도해야 합니다.

## Related

- [hd-69830](hd-69830.md) — 비교용 K0 V 조용한 별. 55 Cnc A 는 ~200 K 더 차가운 "더 붉은 준-태양형"
- [alpha-centauri-b](alpha-centauri-b.md) — 비교용 K1V 조용한 별(55 Cnc A 는 색 계열에서 B 보다 따뜻함)
- [55-cnc-e](55-cnc-e.md) — 헤드라인 USP 용암 초지구. 이 별의 L = 0.582 를 T_eq 유도에 사용
- [methodology](../reference/methodology.md) — 항성 필드용 Decisions 스키마 출처
- [data-sources](../reference/data-sources.md) — 이 합성이 상속하는 논문 인용 정책
