<!-- Teegarden's Star c Phase 3 합성: cfg-ready 결정과 근거 -->
# Teegarden's Star c — Phase 3 Synthesis

Teegarden's Star c 는 M7.0 V 모성을 11.416 일 주기로 도는 최소질량
1.05 M⊕ 의 암석 행성으로, 궤도 장반경은 0.0455 AU, 입사 플럭스는
0.35 ± 0.02 S⊕ 입니다 (Dreizler 2024). Bond 알베도 0.3 기준 평형
온도는 209 ± 4 K 로, 물의 어는점보다 64 K 낮습니다. 단순한 벌크
매개변수 가중을 쓰는 Earth Similarity Index 는 높게 나오지만 (ESI =
0.88, Dreizler 2024 의 표현으로 "프록시마 b 와 매우 닮음"), 이 수치는
오해를 부릅니다. c 는 보수적 거주가능 영역의 바깥 가장자리에 있거나 그
너머에 있고, 가장 최근의 전용 3D GCM 연구는 시뮬레이션된 모든 대기
조성에서 c 가 전 지구 눈덩이 상태에 갇혀 있다고 봅니다. 그래서 cfg 는
c 를 **춥고 전 지구적으로 얼음에 덮인 세계** 로 렌더링하며, 온대 지구-
아날로그로 두지 않습니다.

c 의 cfg 결정적 결과는 Hammond 2025 ([arXiv:2504.00978](https://arxiv.org/abs/2504.00978)) 에서 나옵니다.
이 논문은 ExoCAM GCM 모음을 일곱 개의 가까운 HZ 표적에 (티가든 c 포함)
pCO₂ 를 100 μbar 부터 2 bar 까지 바꾸며 돌립니다. 일곱 표적 가운데 최대
2-bar CO₂ 온실 가열에서도 표면 어디서든 액체 물을 지지하지 못한 **유일한**
행성이 c 입니다. 논문은 c 가 "CO₂ 분압 2 bar 에서도 표면이 완전히 얼음에
덮인다" 고 명시합니다. 낮은 입사 플럭스 (Hammond 의 매개변수 세트에서 S
= 0.37), 높은 얼음 알베도 피드백, 그리고 M-왜성 SED 의 제한된 단파장
가열 효율이 결합되어, 얼마만큼의 온실 가스를 실어도 c 를 단단히 눈덩이로
밀어 넣습니다.

Wandel 2019 의 오래된 1D 분석 모델은 더 낙관적인 거주가능성 범위를
줬습니다 (f = 0.5 에서 H_atm = 1–12, H_atm = 1 일 때 substellar 점에
좁은 거주가능 구역). 하지만 그 모델은 대기 가열을 매개변수로 다루며 얼음
알베도 피드백과 3D 열 재분배 물리학을 결여합니다. Hammond 2025 의 3D GCM
이 더 최근이고 행성별이며 더 무거운 독해이므로, cfg 는 이를 따릅니다. cfg
의 눈덩이 선택은 정전적 독해와 *일치하므로* (발산이 아니므로) Canonical-
alternatives 발산 항목이 필요 없으며, 낙관적 Wandel 독해는 Open items 의
cfg 변형으로 보존합니다.

**NearStars 시나리오 선택은 ~1 bar N₂ + 0.1 bar CO₂ 대기를 가진 전
지구적 얼음 피복 "눈덩이" 행성입니다. 조석 고정되어 있고, 표면 온도가
어디서든 273 K 아래이며, 액체 물이 없고, 대기 순환은 적도 초회전 제트가
지배합니다.** cfg 는 구조적으로 b 의 안구 aquaplanet 과 d 의 황량한
암석과 구별됩니다 — c 는 시스템의 전형적 눈덩이입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019; Hammond 2025 GCM 도 1:1 가정 |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.04 | high | Dreizler 2024 Table 4 (0.04 +0.07/−0.03) |
| `argument_of_periastron_deg` | 301 | low | Dreizler 2024 Table 4 (낮은 e 에서 약한 제약: +165/−74) |
| `sidereal_period_days` | 11.416 | high | Dreizler 2024 Table 4 |
| `semi_major_axis_au` | 0.0455 | high | Dreizler 2024 Table 4 |
| `mass_mearth` | 1.05 (msini) | high | Dreizler 2024 Table 4 |
| `radius_rearth` | 1.02 | medium | DB (지구형 MR); Hammond 2025 Table 1 은 1.05 (Zeng 계열) 사용 |
| `surface_gravity_g_earth` | 1.01 | medium | 유도 = 1.05 / 1.02² = 1.01 |
| `density_g_cc` | 5.45 | low | 유도 = 5.513 × 1.05 / 1.02³ = 5.45 (지구형 가정; 통과 없음) |
| `insolation_s_earth` | 0.35 | high | Dreizler 2024 Table 4 (Hammond 2025 는 약간 다른 별 매개변수로 0.37 사용) |
| `equilibrium_temp_k` (A=0.3) | 209 | high | Dreizler 2024 Table 4 (load-bearing; 단순 공식 재계산 아님) |
| `bond_albedo` | 0.55 | medium | Hammond 2025 — 높은 얼음 알베도가 눈덩이 체제를 지배 (얼음 피복 상태에서 추정한 값, 인용 수치 아님) |
| `surface_temp_substellar_k` | 230 | medium | Hammond 2025 Fig. 1 — 가장 따뜻한 주간측 지점도 2 bar CO₂ 에서 여전히 빙점 아래 (지도에서 읽음, 인용 수치 아님) |
| `surface_temp_nightside_k` | 170 | medium | Hammond 2025 Fig. 1 — 야간측 차가운 트랩 (지도에서 읽음, 인용 수치 아님) |
| `surface_temp_global_mean_k` | 200 | medium | Hammond 2025 — 모든 pCO₂ 에서 어디든 빙점 아래 (본문 명시; 구체 평균은 지도에서 읽음) |
| `atmosphere_present` | true | high | Wandel 2019; Hammond 2025 — 0.1–2 bar CO₂ 사례 모두 안정적 기후 유지 |
| `atmosphere_surface_pressure_pa` | 110 000 | medium | Tie-break: Hammond 2025 의 0.1 bar CO₂ + 1 bar N₂ 사례 (따뜻한 가장자리 눈덩이); 2 bar CO₂ 사례조차 얼음 피복 유지 |
| `atmosphere_composition` | N₂ ~91%, CO₂ ~9% (1 bar N₂ 위 0.1 bar CO₂), H₂O 미량, Ar | medium | Tie-break: Hammond 2025 의 0.1 bar CO₂ / 1 bar N₂ 시나리오 채택 (2 bar 사례는 순수 CO₂, N₂ 0) |
| `atmosphere_scale_height_km` | 5.8 | medium | 유도: kT/μg 에서 T=200 K, μ=29, g=9.86 m/s² |
| `atmosphere_tint_rgb_hex` | `#4a3a50` (얇은 Rayleigh + 차가운 하늘의 어둑한 보라) | low | Tie-break: 2904 K 의 낮은 압력에서 Rayleigh — b 의 예상 톤보다 더 어둑 |
| `cloud_cover_fraction` | 0.35 | medium | Hammond 2025 — c 가 cloud-water-path 이상치 (일곱 표적 중 구름 가장 적음; 표면이 얼음 피복이라 대기 수증기 최소) |
| `cloud_morphology` | 초회전 제트가 substellar 점 동쪽으로 실어나르는 희박한 구름; 야간측 차가운 트랩의 CO₂-얼음 구름 가능 | medium | Hammond 2025 — 구름 최대치가 substellar 동쪽에 위치; c 의 총 cloud water path 는 다른 여섯 표적보다 훨씬 작음 |
| `cloud_tint_rgb_hex` | `#a09080` (어둑한 따뜻한 크림 — 습기 매우 적음) | low | Tie-break: 얼음 구름 + M7 V 조명 |
| `ocean_present` | false | high | Hammond 2025 — 2 bar CO₂ 에서도 어디든 얼음 |
| `surface_morphology` | 얼어붙은 바다 기질 위 50–300 m 두께의 전 지구 빙판; 수렴 영역의 험준한 지형; 저위도 충돌 분화구 / 화산 분출구의 드문 노출 어두운 암반 | medium | 눈덩이 지구 아날로그 물리; 티가든-c-specific 한 GCM 표면 topology 논문 없음 |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-왜성 조명 하 얼음 표면) | low | Tie-break: 물 얼음 알베도 0.6–0.8 + 2904 K 조명 |
| `surface_tint_rgb_hex_accent` | `#4a3030` (충돌 분화구와 화산 특징의 노출 마픽 암반) | low | Tie-break: 더 어두운 얼음 아래 지형의 드문 노출 |
| `magnetic_field_present` | true (적당) | low | Tie-break: 지구 질량의 활성 내부; 측정 없음 |
| `magnetic_field_strength_microtesla_equator` | 20 | low | Tie-break: 낮은 지구형 장으로 스케일링; 측정 없음 |
| `aurora_present` | true (약) | low | 대기 + B-장 모두 적당; M-왜성 SEP 환경 |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm — 그러나 매우 약함; CO₂-rich 대기에서는 CO₂⁺ 액센트 `#FF4D4D` 가 지배 가능 |
| `aurora_intensity_kR_typical` | 15 | low | Tie-break: 약함 — 조용한 M7 V 플럭스 측 + 얇은 대기는 SEP 에너지를 거의 결합하지 못함 |
| `surface_radiation_dose_msv_yr` | 50 | low | Tie-break: 낮은 M7 V 플레어 빈도 + 지구형 B-장 + ~1 bar 대기 |
| `star_apparent_angular_diameter_deg` | 1.25 | high | 유도: 2 × 0.107 × 0.00465 / 0.0455 × 57.3 = 1.25° |
| `stellar_illumination_color_temp_k` | 2904 | high | Schweitzer 2019 (모성 Teff 2904 K; 고분산 분광) |

## Surface synthesis

티가든 c 는 S = 0.35 S⊕ 에 있습니다 — 지구 입사 플럭스의 약 1/3 로,
보수적 바깥-HZ 한계에 있거나 그 아래입니다 (Kopparapu 2013, 완전 대기
순환 가정 시 M 왜성 S_outer ≈ 0.36). cfg 의 눈덩이 선택은 c 에 대한 가장
최근의 전용 3D GCM 연구인 Hammond 2025 ([arXiv:2504.00978](https://arxiv.org/abs/2504.00978)) 에 기반합니다.

Hammond 의 ExoCAM 격자는 c 를 세 가지 CO₂ 시나리오로 돌립니다 — 1 bar N₂
위 100 μbar CO₂, 1 bar N₂ 위 0.1 bar CO₂, 그리고 N₂ 배경 없는 2 bar CO₂
— 그리고 세 경우 모두 c 가 얼음에 덮인다고 봅니다. 논문은 "티가든 c 를
제외한 모든 행성 사례는 물의 어는점 위 온도를 가진 거주가능 표면 영역이
일부 있지만, 티가든 c 는 고려한 모든 pCO₂ 값에서 얼음에 덮인다" 고, 또 c
가 "CO₂ 분압 2 bar 에서도 표면이 완전히 얼음에 덮인다" 고 명시합니다. 세
경우에 걸친 정성적 그림은 (pCO₂ 가 커질수록 따뜻해지지만 결코 빙점을 넘지
못함) 다음과 같습니다.

- **100 μbar CO₂**: 가장 차가운 경우. 표면 온도가 야간측 차가운 트랩
  최저값까지 떨어지고, 얇은 CO₂ 저장소가 동결-증발에 가장 취약합니다.
- **0.1 bar CO₂**: 안정적이고 더 따뜻하지만 여전히 얼음 피복 — cfg 의
  "따뜻한 가장자리 눈덩이" 로 채택.
- **2 bar CO₂**: 가장 따뜻한 경우. 주간측이 따뜻해지지만 빙점 아래 유지
  — 시뮬레이션의 최대 온실 가열도 어디서도 표면을 빙점 위로 올리지
  못합니다.

(위의 셀별 온도는 논문 Figure 1 의 표면 온도 지도에서 읽은 것으로,
인용 수치가 아닙니다. 캐시된 본문이 Appendix A 의 global-mean 표를
재현하지 않으므로, Decisions 표의 substellar/야간측 구체값은 medium
confidence 의 figure-level 추정입니다.)

c 가 극단적 온실 부하에서도 얼어붙은 채로 있는 이유는 낮은 입사 플럭스
(0.35 S⊕ 에 불과) 와 M-왜성 SED 가 깨기 어려운 높은 얼음 알베도의 조합
때문입니다. 후기-M 조명은 근적외선에서 피크를 이루는데, 그곳에서 물
얼음은 놀랍게도 흡수성이 높지만 (가시 파장에서 얼음 알베도가 0.7–0.9 인
것과 달리), substellar 주간측은 여전히 얼음-알베도 피드백 루프를 깨기
위해 입사 플럭스의 대부분이 더 짧은 파장에 있어야 합니다 — 정확히 M7 V
모성이 제공하지 못하는 것입니다.

따라서 cfg 는 c 를 **균일한 얼음 피복 표면** 으로 렌더링합니다.

- **substellar 주간측**: 가장 따뜻한 얼음 (높은 pCO₂ 에서 ~230 K). 드물게
  광학적으로 투명할 만큼 얇을 수 있지만 녹은 웅덩이는 형성되지 않습니다.
  표면 형태론은 험준하고, 대기 순환이 얼음 수렴을 일으키는 곳에 압력
  능선이 있습니다.
- **중위도 / 중경도**: 얼어붙은 바다 기질 위 (원시 액체 물이 있다면)
  ~50–300 m 두께의 빙판.
- **야간측**: 영구 CO₂-서리 차가운 트랩 (~170 K). CO₂ 가 얼음으로 침전되며
  국소적으로 대기 압력이 떨어질 가능성 — 화성식 극지 CO₂-서리 아날로그
  지만 야간측 전체 반구에서 일어납니다.

**색조 선택.** 표면은 압도적으로 물 얼음이며, M-왜성 조명에 치우친 따뜻한
크림 `#d8d0c4` 입니다. 액센트 `#4a3030` (어두운 마픽 암반) 은 ejecta 가
일시적으로 얼음 아래 물질을 노출시킨 드문 충돌 분화구에 나타납니다 —
표면 위를 비행하는 플레이어에게 가장 시각적으로 두드러진 특징이 될
것입니다.

## Atmosphere synthesis

cfg 는 Hammond 2025 의 **1 bar N₂ 위 0.1 bar CO₂** 시나리오 (총 ~1.1 bar,
분압 기준 ~9% CO₂) 를 채택합니다 — 눈덩이 체제 중 따뜻한 가장자리에 해당
합니다. Hammond 의 두 N₂-배경 사례 중 더 따뜻하지만, 명시적으로 표면을
빙점 위로 올리지는 않습니다. 조성은 다음과 같습니다.

- **압력** ~1.1 bar (110 kPa) — Hammond 2025 의 중간 사례에 따라 1 bar
  N₂ 배경 위 0.1 bar CO₂.
- **조성** N₂ ~91%, CO₂ ~9% (0.1 bar), H₂O 미량 (200 K 에서 ~6×10⁻⁵
  포화), 소량의 Ar. Hammond 의 가장 두꺼운 사례는 N₂ 없는 순수 2 bar
  CO₂ 라는 점에 유의하며, cfg 는 순수-CO₂ 끝값이 아니라 N₂-배경 중간
  사례를 의도적으로 택합니다.
- **구름.** Hammond 2025 는 c 를 일곱 표적 중 cloud-water-path 이상치로
  봅니다 — 얼음 피복 표면이 총 대기 수증기를 다른 여섯보다 훨씬 낮게
  유지합니다. 형성되는 적은 구름은 종단경계에 모이는 것이 아니라 초회전
  제트에 의해 substellar 점 동쪽으로 실려갑니다 (Hammond 이 저-pCO₂
  사례에서 보고하는 일반적 패턴). 따라서 총 구름 피복은 낮습니다 (~35%).
  야간측 표면 온도가 CO₂ 서리점 아래로 떨어지면 CO₂-얼음 구름이 형성될
  수 있습니다.

**하늘 모습.** 대기는 단파장에서 Rayleigh 산란을 하지만, 2904 K 모성 SED
에서는 단파장 플럭스가 매우 적습니다 — 산란 하늘은 어둑하고 빨강으로
치우칩니다. 천정 하늘 `#3a2a35`, 지평선 `#7a5040`.

모성의 시지름은 1.25° (지구에서 본 태양 시지름의 약 2.3 배) 입니다.
substellar 의 표면 조명은 0.35 × 지구의 볼로메트릭 플럭스 — 지구에서의
황혼에 비유할 만하며, 스펙트럼 피크는 단단히 근적외선에 있습니다. 입사
에너지의 대부분은 근적외선 흡수성이 높은 물-얼음에 흡수되지만, 상향 열
방출의 대부분은 대기가 8–13 μm 창에서 광학적으로 얇기 때문에 우주로
다시 복사됩니다.

**대기 손실과 안정성.** 7–8 Gyr 의 늙고 조용한 모성은, 행성이 외기 방출로
2차 CO₂/N₂ 대기를 만들고 유지하는 한 대기 보존에 유리합니다. Hammond 2025
는 탈출을 포함하지 않습니다. Wandel 2019 는 보존을 리뷰하고 늙고 조용한 M
왜성이 더 젊고 활동적인 별보다 덜 적대적이라고 봅니다. CO₂–N₂ 대기는 전-MS
탈출에 전형적인 원시 H/He 대기보다 무거워 열 탈출에 덜 취약합니다.

**오로라.** 약함 (전형 15 kR — 두꺼운 대기의 HZ 세계보다 훨씬 희미함).
티가든의 낮은 플레어 빈도와 적당한 대기가 결합해 희박한 오로라 디스플레이
를 만듭니다. 가시 방출은 [OI] 557.7 nm 녹색 (`#4DFF4D`) 이 지배하는데,
여기서 O 는 미세한 CO₂ 광분해에서 나옵니다. CO₂ 분율이 높으면 580–700 nm
Fox-Duffendack-Barker 띠의 CO₂⁺ 빨강-주황 액센트 (`#FF4D4D`) 가 유의해
집니다.

## Rotation & spin synthesis

c 의 P_orb = 11.4 d 는 7–8 Gyr 에 걸쳐 Griessmeier 2009 의 조석 고정
시간 척도 안에 단단히 있습니다. cfg 는 동기 자전을 가정하며, 이는 Hammond
2025 가 GCM 에 쓴 1:1 스핀-궤도 상태 및 Wandel 2019 의 조석 고정 행성
처리와 일치합니다. 자전축 기울기는 0 으로 감쇠합니다. 이심률은 0.04
(Dreizler 2024, +0.07/−0.03) 로 낮고 거의 원형에 일관되므로, cfg 는 스핀을
포획된 3:2 공명이 아니라 near-1:1 / pseudo-synchronous 로 렌더링합니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 11.416 일 (986 342 s).

**대기 순환.** Hammond 2025 는 일곱 개의 조석 고정 사례 (c 포함) 모두가
적도 초회전 제트를 발달시킨다고 봅니다 (Fig. 3, zonal-mean zonal wind).
표면 흐름은 더 약합니다. 이는 느리게 자전하는 조석 고정 행성에 대해
정전적이며, Hammond 이 인용하는 "열 초회전" 체제 (Pierrehumbert & Hammond
2019) 와 일치합니다. c 는 Hammond 의 분류에서 Rhines-rotator 동역학 체제에
있습니다.

**계절 없음.** 자전축 기울기 = 0; libration 진폭 작음.

**자기 다이나모.** 지구 질량 c 는 핵 대류에서 적당한 다이나모를 지지할
가능성이 있습니다. cfg 는 낮은 지구형 장 (20 μT) 을 tie-break 으로
선택합니다. 측정 없음.

## Visual styling

표면과 대기 결정을 결합하면, c 는 균일한 흰-크림 눈덩이 세계로 렌더링
됩니다.

- **궤도에서 본 전체 모습.** 거의 특징 없는 얼음 구체로, 표면 거칠기에
  미묘한 변화가 있습니다. 종단경계 특징 (압력 능선, 빙하 흐름 선) 은
  비스듬한 조명에서만 보입니다. 얇은 대기는 거의 림 안개를 만들지
  않습니다.
- **substellar 영역**: 약간 더 따뜻한 얼음 (~230 K), 가능한 드문 얇은
  투명 얼음 패치. 표면 형태론은 초회전 제트가 얼음 수렴을 일으키는 곳에
  수렴-구동 압력 능선을 보여줍니다.
- **중위도**: 균일한 빙판, 큰 규모에서 매끄럽고, 충돌 중심에 어두운
  `#4a3030` 암반이 노출된 가끔의 충돌 분화구.
- **야간측**: 어두움. 표면 온도가 CO₂ 서리점 아래로 떨어지는 곳의 CO₂-서리
  침전이 밝은 패치를 만들 수 있습니다. 차가운 트랩은 균일하게 어둑한
  영역으로 보입니다.
- **대기 안개.** ~8–12 km 두께의 매우 얇은 옅은 보라 림 빛 (`#4a3a50`).
- **하늘의 별.** 티가든의 별은 c 의 하늘에서 1.25° 시지름 (지구에서 본
  태양의 2.3 배) 으로 보입니다. 짙은 빨강-주황 원반으로 나타나며, 조명은
  깊은 황혼처럼 느껴지고 결코 한낮이 되지 않습니다.
- **하늘의 자매 행성.** b (안쪽, ~4.91 d) 와 d (바깥, ~26 d) 가 합을
  지나갑니다. 둘 중 b 가 내합에서 더 밝고 더 가깝습니다.

전체적 시각 인상은 호스(Hoth) 같은 얼음 세계지만 극저온 왜성의 영구
빨강-주황 조명을 가진 모습이어야 합니다. c 는 시각적으로 b 보다 덜
강렬하지만 (바다-동공 대비 없음) 시스템 뷰에서 뚜렷한 "얼어붙은 자매"
동반자를 이룹니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **[2402.00923](https://arxiv.org/abs/2402.00923)** Dreizler S. et al. 2024 — *Teegarden's Star revisited*
  (`2024A&A...684A.117D`). Table 4 에서 c 궤도 정밀화
  (P = 11.416 d, e = 0.04, msini = 1.05 M⊕, T_eq = 209 K @ A=0.3,
  S = 0.35 S⊕, ESI = 0.88 "프록시마 b 와 매우 닮음").
- **[2504.00978](https://arxiv.org/abs/2504.00978)** Hammond T. et al. 2025 — *The climates and thermal
  emission spectra of prime nearby temperate rocky exoplanet targets*
  (`2025ApJ...984..181H`). 100 μbar / 0.1 bar / 2 bar CO₂ 의 c 3D
  ExoCAM GCM — c 는 모든 pCO₂ 에서 어디든 얼음 피복으로, 일곱 표적 중
  결코 액체 물에 도달하지 못하는 유일한 행성. cfg 의 눈덩이 선택을
  결정.
- **[1906.07704](https://arxiv.org/abs/1906.07704)** Wandel A. & Tal-Or L. 2019 — *On the Habitability of
  Teegarden's Star planets* (`2019ApJ...880L..21W`). c 에 대한 1D
  분석적 거주가능성 범위 H_atm = 1–12 (f=0.5, T_max=340 K) — cfg 에서는
  Hammond 2025 가 대체한 더 오래되고 낙관적인 독해.
- **[1906.07196](https://arxiv.org/abs/1906.07196)** Zechmeister M. et al. 2019 — b 와 c 의 발견 논문
  (`2019A&A...627A..49Z`). 원래 궤도 매개변수와 모성 특성화.

### Read (context / methodology, not decision-driving)

- **[2007.15077](https://arxiv.org/abs/2007.15077)** Cifuentes C. et al. 2020 — CARMENES input catalogue
  of M dwarfs (`2020A&A...642A.115C`). M-왜성 Teff/분광형 보정 맥락
  (M7.0 V 빈). 채택된 모성 Teff 2904 K 는 이 카탈로그의 빈 중앙값이
  아니라 Schweitzer 2019 에서 옴.
- **2512.16575** Fujii et al. — M-왜성 HZ 행성의 기후 / 거주가능성
  방법론 맥락.
- **Schweitzer A. et al. 2019** — 모성 별 매개변수 (Teff 2904 K, L, M,
  R); 모성 합성을 통해 사용.

### Read (instrument / non-cfg-decisive)

- 일반 LIFE / MIRECLE 미션 개념 논문 (Hammond 2025 의 PIE 검출 가능성
  틀).

### Not read — no arXiv preprint or low-priority (~2 papers)

- Hill 2023 카탈로그 (skipped — 카탈로그, cfg 비결정적).
- 참고문헌은 `docs/phase3/_bib/teegarden-s-star-c.yaml` 에 보존됨.

## Open items for follow-up

- **Hammond 2025 대 Wandel 2019 (cfg 변형)**: cfg 의 눈덩이 선택은 Hammond
  2025 의 3D ExoCAM 결과를 따릅니다. Wandel 2019 의 오래된 1D 분석 모델은
  c 에 대해 더 낙관적인 H_atm = 1–12 거주가능성 범위를, substellar 점에
  좁은 거주가능 패치와 함께 줍니다. cfg 작성자가 대신 만들 수 있는
  보수적이지만 흥미로운 **변형** 은 "얇은 substellar 따뜻한 점이 있는
  안구" 입니다. 미래의 독립적 3D GCM (THAI-style intercomparison, 또는 c
  에 대한 ROCKE-3D 연구 specific) 이 높은 pCO₂ 에서 substellar 액체 물을
  찾으면 cfg 는 그 변형으로 이동해야 합니다. 지금은 눈덩이가 정전적이고
  cfg 가 이에 일치합니다.
- **표면 온도는 figure 에서 읽은 값이지 인용 수치가 아님**: 캐시된 Hammond
  2025 본문은 Appendix A 의 global-mean 표를 재현하지 않으므로, Decisions
  표의 substellar/야간측/global-mean K 값은 Figure 1 지도에서 읽은
  추정값입니다. 수치 표가 확보되면 조여야 합니다.
- **2-bar CO₂ 끝값**: Hammond 2025 는 표면 녹음 없이 2 bar CO₂ (순수, N₂
  없음) 까지 테스트했습니다. 더 높은 CO₂ 대기 (예: 10 bar Venus-like) 는
  테스트되지 않았고 원칙적으로 표면을 빙점 위로 데울 수 있지만, 그
  압력에서는 다른 효과 (CO₂ 야간측 응결, 대기 붕괴) 가 중요해집니다.
- **통과 확인 없음**: 모든 매개변수가 RV 유도. 시스템은 비-통과 (TESS +
  SPECULOOS).
- **표면 아래 바다**: Hammond 2025 는 내부 구조를 모델링하지 않습니다. c
  가 원시 물 저장소를 가지고 있다면 전 지구 빙판 아래 액체 표면-아래
  바다가 존재할 수 있습니다 (유로파와 유사). cfg 는 이를 궤도에서 가시로
  렌더링하지 않지만 Kerbalism 표면-아래-물 플래그로 추가할 수 있습니다.
- **7–8 Gyr 에 걸친 대기 탈출**: 모델링되지 않음. cfg 는 조용한 현재 별과
  오래된 나이를 기반으로 보존을 가정합니다. c 에 대해 specific 한
  Lammer-style 탈출 계산이 대기 컬럼을 조여줄 것입니다.

## Related

- [teegardens-star](teegardens-star.md) — M7 V 모성
- teegardens-star-b — 안쪽 자매, 온대 aquaplanet (아직 미승격)
- teegardens-star-d — 바깥 자매, 차가운 황량한 암석 (아직 미승격)
- [trappist-1-f](trappist-1-f.md) — HZ 바깥 가장자리의 자매 시스템 아날로그 (TRAPPIST-1 f 는 눈덩이/안구 경계에 더 가까움; c 는 완전 눈덩이)
- [proxima-cen-b](proxima-cen-b.md) — Dreizler 2024 는 c 의 ESI (0.88) 가 비교 가능하다고 인용
- [methodology](../reference/methodology.md) — Decisions 스키마
