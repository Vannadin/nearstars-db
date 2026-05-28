# 티가든의 별 c — Phase 3 합성

티가든의 별 c 는 M7.0 V 모성 둘레를 11.416 일 주기로 도는 최소질량
1.05 M⊕ 의 암석 행성으로, 궤도 장반경 0.0455 AU 와 입사 플럭스 0.35 ±
0.02 S⊕ (Dreizler 2024) 를 가집니다. Bond 알베도 0.3 의 평형 온도는
209 ± 4 K — 물의 어는점보다 70 K 낮습니다. 단순한 벌크 매개변수 가중을
쓰는 Earth Similarity Index 는 높게 나옵니다 (ESI = 0.88, Dreizler
2024 에 따르면 프록시마 b 와 비슷). 하지만 이는 오해를 부르는 수치입니다.
c 는 보수적 거주가능 영역의 바깥 가장자리에 있거나 그 너머에 있으며,
최근의 3D GCM 모델링은 시뮬레이션된 모든 대기 조성에서 c 가 전 지구
눈덩이 상태에 갇혀 있다는 결과를 줍니다. cfg 는 따라서 c 를 **춥고, 전
지구적으로 얼음에 덮인 세계** 로 렌더링합니다 — 온대 지구-아날로그가
아닙니다.

c 에 관한 cfg 결정적 결과는 Hammond 2025 (arXiv:2504.00978) 에서
나옵니다. 그들은 ExoCAM GCM 모음을 일곱 개의 가까운 HZ 표적에 (티가든
c 포함) pCO₂ 를 100 μbar 부터 2 bar 까지 변화시키며 돌립니다. 일곱
표적 중 2-bar CO₂ 의 최대 온실 가열에서도 표면 어디서든 액체 물을
지지하지 못한 **유일한** 행성이 c 입니다. 낮은 입사 플럭스 (Hammond 의
매개변수 세트에서 S = 0.37), 높은 얼음 알베도 피드백, 그리고 M-왜성
SED 의 제한된 단파장 가열 효율이 결합되어, 얼마만큼의 온실 가스를
실어도 c 를 단단히 눈덩이로 밀어 넣습니다.

Wandel 2019 의 오래된 1D 분석 모델은 더 낙관적인 거주가능성 범위 (f =
0.5 에서 H_atm = 1-12) 를 줬지만, 그 모델은 얼음 알베도 피드백과 3D 열
재분배 물리학을 결여하고 있습니다. Hammond 2025 의 3D GCM 이 정전적
독해이며, cfg 는 이를 따릅니다.

**NearStars 시나리오 선택: 얇은 CO₂-증강 N₂ 대기를 가진 전 지구적
얼음 피복 "눈덩이" 행성으로, 조석 고정되어 있고, 표면 온도가 어디서든
273 K 아래이며, 액체 물이 없고, 대기 순환은 적도 초회전 제트가 지배.**
cfg 는 구조적으로 b 의 안구 aquaplanet 과 d 의 황량한 암석과 구별됩니다
— c 는 시스템의 전형적 눈덩이입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019; Hammond 2025 GCM 도 1:1 가정 |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.06 | high | Dreizler 2024 |
| `argument_of_periastron_deg` | 301 | low | Dreizler 2024 (낮은 e 에서 약한 제약: +165/−74) |
| `sidereal_period_days` | 11.416 | high | Dreizler 2024 |
| `semi_major_axis_au` | 0.0455 | high | Dreizler 2024 |
| `mass_mearth` | 1.05 (msini) | high | Dreizler 2024 표 4 |
| `radius_rearth` | 1.02 | medium | Hammond 2025 (Zeng 2016 지구형 MR) |
| `surface_gravity_g_earth` | 1.01 | medium | 유도 = 1.05 / 1.02² |
| `density_g_cc` | 5.4 (지구형 가정) | low | 통과 없음 |
| `insolation_s_earth` | 0.35 | high | Dreizler 2024 (Hammond 2025 는 약간 다른 별 매개변수로 0.37 사용) |
| `equilibrium_temp_k` (A=0.3) | 209 | high | Dreizler 2024 |
| `bond_albedo` | 0.55 | medium | Hammond 2025 — 높은 얼음 알베도가 눈덩이 체제를 지배 |
| `surface_temp_substellar_k` | 230 | medium | Hammond 2025 ExoCAM Fig. 2 — 가장 따뜻한 주간측 지점도 여전히 빙점 아래 |
| `surface_temp_nightside_k` | 170 | medium | Hammond 2025 야간측 차가운 트랩, CO₂ 서리 체제이기도 함 |
| `surface_temp_global_mean_k` | 200 | medium | Hammond 2025 — 모든 pCO₂ 에서 어디든 빙점 아래 |
| `atmosphere_present` | true | high | Wandel 2019; Hammond 2025 의 0.1-2 bar CO₂ 기본값 모두 지속 가능 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | Tie-break: Hammond 2025 1-bar 지구형 기본; 2 bar CO₂ 도 얼음을 녹이지 못함 |
| `atmosphere_composition` | N₂ 99%, CO₂ 1%, H₂O 미량, Ar 0.5% | medium | Tie-break: Hammond pCO₂=0.1 bar 사례를 "따뜻한 가장자리" 눈덩이로 묶음 |
| `atmosphere_scale_height_km` | 5.5 | medium | 유도: kT/μg 에서 T=200 K, μ=29, g=9.9 m/s² |
| `atmosphere_tint_rgb_hex` | `#4a3a50` (얇은 Rayleigh + 차가운 하늘 어둑한 보라) | low | Tie-break: 2904 K 의 낮은 압력에서 Rayleigh — b 의 `#5a3a40` 보다 더 어둑 |
| `cloud_cover_fraction` | 0.35 | medium | Hammond 2025 — 종단경계 차가운 트랩에서 부분 구름; 지구형보다 적음 |
| `cloud_morphology` | 종단경계 차가운 트랩의 부분적 물-얼음 / CO₂-얼음 구름; substellar 상공의 드문 높은 권운 | medium | Hammond 2025 — 바람 quivers 가 종단경계 수렴을 보임; 눈덩이 대기는 습기가 제한적 |
| `cloud_tint_rgb_hex` | `#a09080` (어둑한 따뜻한 크림 — b 보다도 습기가 적음) | low | Tie-break: 얼음 구름 + M7 V 조명 |
| `ocean_present` | false | high | Hammond 2025 — 2 bar CO₂ 에서도 어디든 얼음 |
| `surface_morphology` | 얼어붙은 바다 기질 위 50-300 m 두께의 전 지구 빙판; 수렴 영역의 험준한 지형; 저위도 충돌 분화구 / 화산 분출구에서 드문 노출 어두운 암반 | medium | 눈덩이 지구 아날로그 물리; 티가든-c-specific 한 GCM topology 논문 없음 |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-왜성 조명 하 얼음 표면) | medium | Tie-break: 물 얼음 알베도 0.6-0.8 + 2904 K 조명; 시스템 일관성을 위해 b 의 얼음 톤과 일치 |
| `surface_tint_rgb_hex_accent` | `#4a3030` (충돌 분화구와 화산 특징의 노출 마픽 암반) | low | Tie-break: 드문 노출이 b 보다 어두운 지형을 시사 |
| `magnetic_field_present` | true (적당) | low | Tie-break: 지구 질량의 활성 내부; 측정 없음 |
| `magnetic_field_strength_microtesla_equator` | 20 | low | Tie-break: c 가 더 차갑기 때문에 (느린 핵 대류) b 보다 약간 낮게 스케일링; 측정 없음 |
| `aurora_present` | true (약) | low | 대기 + B-장 모두 적당; M-왜성 SEP 환경 |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm — 그러나 매우 약함; CO₂-rich 대기에서는 CO₂⁺ 액센트 `#FF4D4D` 가 지배 가능 |
| `aurora_intensity_kR_typical` | 15 | low | Tie-break: b 의 30 kR 의 절반 — c 가 더 어둑한 플럭스 측이고 더 얇은 대기는 SEP 에너지를 덜 결합 |
| `surface_radiation_dose_msv_yr` | 50 | low | Tie-break: 낮은 M7 V 플레어 빈도 + 지구형 B-장 + 1 bar 대기 |
| `star_apparent_angular_diameter_deg` | 1.25 | high | 유도: 2 × 0.107×0.00465 / 0.0455 × 57.3 = 1.25° |
| `stellar_illumination_color_temp_k` | 2904 | high | Cifuentes 2020 |

## Surface synthesis

티가든 c 는 S = 0.35 S⊕ 에 있습니다 — 지구 입사 플럭스의 약 1/3, 보수적
바깥-HZ 한계 아래 (Kopparapu 2013 M 왜성에 대한 S_outer ≈ 0.36 with 완전
대기 순환). cfg 의 눈덩이 선택은 c 에 대한 가장 최근의 헌신적 3D GCM
연구인 Hammond 2025 (arXiv:2504.00978) 에 기반합니다.

Hammond 의 ExoCAM 격자는 c 를 세 가지 pCO₂ 값 (100 μbar, 0.1 bar, 2
bar) 모두 1 bar N₂ 배경으로 돌리고 다음을 찾습니다.

- **100 μbar CO₂**: 표면 온도가 야간측 차가운 트랩에서 ~140 K, substellar
  에서 ~190 K 로 떨어짐. CO₂ 대기 저장소 전체가 얼어붙을 것 — 대기 붕괴
  임박.
- **0.1 bar CO₂**: 표면 170-220 K, 야간측 ~170 K, substellar ~220 K.
  안정적 대기지만 여전히 얼음 피복.
- **2 bar CO₂**: substellar 가 ~230 K 로 따뜻해지고, 야간측 ~190 K.
  여전히 어디든 얼음 피복 — 시뮬레이션에서 달성 가능한 최대 온실 가열도
  주간측을 빙점 위로 올리지 못함.

c 가 극단적 온실 부하에서도 얼어붙은 채로 있는 이유는 낮은 입사 플럭스
(0.35 S⊕ 에 불과) 와, M-왜성 SED 가 깨기 어려운 높은 얼음 알베도의
조합 때문입니다. 후기-M 조명은 근적외선에서 피크를 이루는데, 그곳에서
물 얼음은 놀랍게도 흡수성이 높지만 (가시 파장에서 얼음 알베도가 0.7-0.9
인 것과 달리), substellar 주간측은 여전히 얼음-알베도 피드백 루프를
깨기 위해 입사 플럭스의 대부분이 더 짧은 파장에 있어야 합니다 — 정확히
M7 V 모성이 제공하지 못하는 것입니다.

따라서 cfg 는 c 를 **균일한 얼음 피복 표면** 으로 렌더링합니다.

- **substellar 주간측**: 표면 온도 ~220-230 K. 드물게 얇아 (최대 수 미터)
  광학적으로 투명한 얼음일 수 있지만, 녹은 웅덩이는 형성되지 않습니다.
  표면 형태론은 험준하고, 대기 순환이 얼음 수렴을 일으키는 곳에 압력
  능선이 있습니다.
- **중위도 / 중경도**: 얼어붙은 바다 기질 위 (원시 액체 물이 있다면)
  ~50-300 m 두께의 빙판. 표면 온도 180-210 K.
- **야간측**: 영구 CO₂-서리 차가운 트랩. 표면 온도 ~170 K, CO₂ 가 얼음
  으로 침전되면서 국소적으로 대기 압력이 떨어질 가능성 — 화성식 극지
  CO₂-서리 아날로그지만 야간측 전체 반구에서.

**색조 선택.** 표면은 압도적으로 물 얼음이고, b 와 같은 M-왜성-조명-치우친
따뜻한 크림 `#d8d0c4` 입니다. 액센트 `#4a3030` (어두운 마픽 암반) 은
ejecta 가 일시적으로 표면 아래 물질을 노출시킨 드문 충돌 분화구에 나타
납니다 — 표면 위를 비행하는 플레이어에게 가장 시각적으로 두드러진 특징이
될 것입니다.

## Atmosphere synthesis

cfg 는 **1 bar N₂ + 1% CO₂** 조성을 채택합니다 — Hammond 2025 의 0.1
bar 와 2 bar CO₂ 시나리오 사이의 타협입니다. 눈덩이 체제의 따뜻한 가장
자리에 해당 (substellar 약 220-230 K) 하지만, 명시적으로 표면을 빙점
위로 올리지는 않습니다. 조성은 다음과 같습니다.

- **압력** 1 bar (100 kPa) — Hammond 2025 N₂ 배경 기본.
- **조성** N₂ 99%, CO₂ 1% (10 mbar — 지구의 400 ppm 과 Hammond 의 0.1
  bar 사이), H₂O 미량 (200 K 에서 ~6×10⁻⁵ 포화), Ar 0.5%.
- **구름.** Hammond 2025 바람 벡터 맵 (Fig. 2) 은 종단경계 수렴 흐름
  영역을 보여주는데, 그곳에서 (이미 극히 희박한) 대기 수증기가 얇은
  구름으로 응결됩니다. 전체 구름 피복 ~35% — 액체-상 물 순환이 최소이기
  때문에 b 의 55% 보다 훨씬 적습니다. 야간측 표면 온도가 CO₂ 서리점
  (~165 K at 1 bar) 아래로 떨어지면 CO₂-얼음 구름이 형성될 수 있어,
  야간측에서 가끔 밝은 구름 특징이 생길 수 있습니다.

**하늘 모습.** 1 bar 대기는 단파장에서 Rayleigh 산란을 하지만, 2904 K
모성 SED 에서는 b 보다도 단파장 플럭스가 더 적습니다 — 산란 하늘은
어둑하고 빨강으로 치우칩니다. 천정 하늘 `#3a2a35`, 지평선 `#7a5040`.

모성의 시지름은 1.25° (지구에서 본 태양 시지름의 약 2.3 배). substellar
의 표면 조명은 0.35 × 지구의 볼로메트릭 플럭스 — 지구에서의 황혼에 비유
할 만하며, 스펙트럼 피크는 단단히 근적외선에 있습니다. 입사 에너지의
대부분은 근적외선 흡수성이 높은 물-얼음에 흡수되지만, 상향 열 방출의
대부분은 얇은 대기가 8-13 μm 창에서 광학적으로 얇기 때문에 우주로 다시
복사됩니다.

**대기 손실과 안정성.** 8 Gyr 의 늙고 조용한 모성은 행성이 외기 방출로
2차 CO₂/N₂ 대기를 만들고 유지하는 한 대기 보존을 유리하게 합니다.
Hammond 2025 는 탈출을 포함하지 않습니다. Wandel 2019 §3.1 은 보존을
리뷰하고 늙고 조용한 M 왜성이 더 젊고 활동적인 별보다 덜 적대적이라고
찾습니다. CO₂-N₂ 대기는 전-MS 탈출에 전형적인 원시 H/He 대기보다 무거워
열 탈출에 덜 취약합니다.

**오로라.** 약함 (전형 15 kR, b 는 30 kR, TRAPPIST-1 e 는 150 kR). 티가든
거리에서의 더 낮은 플레어 빈도와 더 얇은 대기가 결합해 희박한 오로라
디스플레이를 만듭니다. 가시 방출은 [OI] 557.7 nm 녹색 (`#4DFF4D`) 이
지배하는데, 여기서 O 는 미세한 CO₂ 광분해에서 나옵니다. CO₂ 분율이 수
% 를 넘으면 580-700 nm Fox-Duffendack-Barker 띠의 CO₂⁺ 빨강-주황 액센트
(`#FF4D4D`) 가 유의해집니다.

## Rotation & spin synthesis

c 의 P_orb = 11.4 d 는 8 Gyr 에 걸쳐 Griessmeier 2009 조석 고정 시간
척도 안에 단단히 있습니다. cfg 는 동기 자전을 가정합니다. 자전축 기울기
는 0 으로 감쇠. 이심률 0.06 (Dreizler 2024) — 3:2 스핀-궤도 공명이 불안
정할 만큼 원형에 가깝습니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 11.416 일 (986 342 s).

**대기 순환.** Hammond 2025 ExoCAM 은 c 에 적도 초회전 제트를 줍니다
(그들의 Fig. 3 zonal-mean zonal wind 는 낮은 압력의 적도에서 ~20 m/s 의
양의 흐름을 보임). 표면 흐름은 더 약합니다. 이는 느리게 자전하는 조석
고정 행성에 대해 정전적이며 "열 초회전" 체제 (Pierrehumbert & Hammond
2019) 와 일치합니다.

**계절 없음.** 자전축 기울기 = 0; libration 진폭 작음.

**자기 다이나모.** 지구 질량 c 는 핵 대류에서 적당한 다이나모를 지지할
가능성이 있습니다. cfg 는 낮은 지구형 장 (b 의 25 μT 보다 약간 적은 20
μT) 을 tie-break 으로 선택 — 더 차가운 내부는 핵 대류가 약간 덜 활발할
수 있습니다. 측정 없음.

## Visual styling

표면과 대기 결정을 결합하면, c 는 균일한 흰-크림 눈덩이 세계로 렌더링
됩니다.

- **궤도에서 본 전체 모습.** 거의 특징 없는 얼음 구체로, 표면 거칠기에
  미묘한 변화. 종단경계 특징 (압력 능선, 빙하 흐름 선) 은 비스듬한 조명
  에서만 보입니다. 얇은 대기는 거의 림 안개를 만들지 않습니다.
- **substellar 영역**: 약간 더 따뜻한 얼음 (~230 K), 가능한 드문 녹은
  웅덩이 등가물 얇은 투명 얼음 패치. 표면 형태론은 대기 초회전 제트가
  얼음 수렴을 일으키는 곳에 수렴-구동 압력 능선을 보여줍니다.
- **중위도**: 균일한 빙판, 큰 규모에서 매끄럽고, 충돌 중심에 어두운
  `#4a3030` 암반이 노출된 가끔의 충돌 분화구.
- **야간측**: 어두움, 표면 온도가 165 K 아래로 떨어지는 곳의 CO₂-서리
  침전이 밝은 패치를 만들 수 있음. 차가운 트랩이 균일하게 어둑한 영역
  으로 보임.
- **대기 안개.** ~8-12 km 두께의 매우 얇은 옅은 보라 림 빛 (`#4a3a50`).
- **하늘의 별.** 티가든의 별은 c 의 하늘에서 1.25° 시지름 (지구에서 본
  태양의 2.3 배). b 에서보다 훨씬 작은 짙은 빨강-주황 원반으로 보임 —
  조명은 깊은 황혼처럼 느껴지며 결코 한낮이 되지 않음.
- **하늘의 자매 행성.** b 가 내합에서 (~0.3° 시지름, m_v ≈ −6); d 가
  외합에서 (~0.2°, m_v ≈ −4). b 와는 박자 주기에서 ~8 일마다 내합.

전체적 시각 인상은 호스(Hoth) 같은 얼음 세계지만 극저온 왜성의 영구
빨강-주황 조명을 가진 모습이어야 합니다. c 는 시각적으로 b 보다 덜
강렬하지만 (바다-동공 대비 없음) 시스템 뷰에서 뚜렷한 "얼어붙은 자매"
동반자를 이룹니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Dreizler S. et al. 2024** — *Teegarden's Star revisited*
  (`2024A&A...684A.117D`, arXiv:2402.00923). 정밀화된 c 궤도
  (P = 11.416 d, e = 0.06, msini = 1.05 M⊕, T_eq = 209 K, S = 0.35 S⊕).
- **Hammond T. et al. 2025** — *The climates and thermal emission
  spectra of prime nearby temperate rocky exoplanet targets* (`2025ApJ...
  984..181H`, arXiv:2504.00978). 100 μbar / 0.1 bar / 2 bar CO₂ 의 c
  의 3D ExoCAM GCM — c 는 모든 pCO₂ 에서 어디든 얼음 피복. cfg 의
  눈덩이 선택을 결정.
- **Wandel A. & Tal-Or L. 2019** — *On the Habitability of Teegarden's
  Star planets* (`2019ApJ...880L..21W`, arXiv:1906.07704). c 에 대한
  1D 분석적 거주가능성 범위 H_atm = 1-12 — Hammond 2025 가 대체한 더
  오래되고 낙관적인 독해.
- **Zechmeister M. et al. 2019** — b 와 c 의 발견 논문 (arXiv:1906.
  07196). 원래 궤도 매개변수.

### Read (context / methodology, not decision-driving)

- **Kossakowski D. et al. 2023** — *The CARMENES search for exoplanets
  around M dwarfs. Wolf 1069 b: Earth-mass planet in the habitable
  zone of a nearby, very low-mass star* (`2023A&A...670A..84K`,
  arXiv:2301.02477). 더 따뜻한 M5 V 둘레의 S = 0.65 S⊕ 의 비교 암석
  행성. c (S = 0.35) 가 왜 더 차가운 가장자리인지의 틀을 잡는 데
  도움이 됨.
- **Schweitzer A. et al. 2019** — 별 매개변수; 모성 통해 사용.
- **Boukrouche R. et al. 2024** — 물 구름 방출 스펙트럼
  (arXiv:2411.07922). b 용이지만 c 의 방법론 맥락.

### Read (instrument / non-cfg-decisive)

- 일반 LIFE / MIRECLE 미션 개념 논문 (Hammond 맥락).

### Not read — no arXiv preprint or low-priority

c 의 참고문헌은 작습니다 (7 개 논문, 5 개 arXiv). 단 하나만 `skipped`
으로 표시 — Hill 2023 카탈로그. 다른 모두는 deep-read 또는 skim. `docs/
phase3/_bib/teegarden-s-star-c.yaml` 에 보존됨.

## Open items for follow-up

- **Hammond 2025 대 Wandel 2019**: cfg 의 눈덩이 선택은 Hammond 2025
  의 3D ExoCAM 결과에 의존합니다. Wandel 2019 의 오래된 1D 분석 모델은
  c 에 대해 H_atm = 1-12 의 더 낙관적인 거주가능성 범위를 줍니다.
  미래의 독립적인 3D GCM (THAI-style intercomparison, 또는 c 에 대한
  ROCKE-3D 연구 specific) 이 높은 pCO₂ 에서 substellar 의 액체 물을
  찾으면, cfg 는 한계적 "얇은 substellar 따뜻한 점이 있는 안구" 변형
  으로 이동할 것입니다. 지금은 눈덩이가 정전적.
- **2-bar CO₂ 시나리오**: Hammond 2025 는 2 bar CO₂ 까지 테스트했고
  표면 녹음 없음. 더 높은 CO₂ 대기 (예: 10 bar Venus-like) 는 테스트
  되지 않았고 원칙적으로 빙점 위 표면 온도를 만들 수 있지만, 그 압력
  에서는 다른 효과 (CO₂ 야간측 응결, 대기 붕괴) 가 중요해집니다.
- **통과 확인 없음**: 모든 매개변수가 RV 유도. 비-통과 기하학에서 통과
  검출은 극도로 가능성이 낮음.
- **표면 아래 바다**: Hammond 2025 는 내부 구조를 모델링하지 않습니다.
  c 가 원시 물 저장소를 가지고 있다면 액체 표면-아래 바다가 전 지구
  빙판 아래 존재할 수 있습니다 — 유로파와 유사. cfg 는 현재 표면-아래
  바다를 궤도에서 가시로 렌더링하지 않지만 Kerbalism 표면-아래-물 플래
  그로 추가할 수 있습니다.
- **CO₂ 서리 순환**: 야간측 차가운 트랩은 계절-스케일 (궤도-주기) CO₂
  서리 침전 순환을 가질 수 있습니다. P_orb = 11 d 에서 순환은 빠릅니다.
  c 에 대해 명시적으로 모델링한 발표 연구 없음.
- **8 Gyr 에 걸친 대기 탈출**: 모델링되지 않음. cfg 는 조용한 현재 별
  과 오래된 나이를 기반으로 보존을 가정합니다. c 에 대해 specific 한
  Lammer-style 탈출 계산이 대기 컬럼을 조여줄 것입니다.

## Related

- [teegardens-star](teegardens-star.md) — M7 V 모성
- [teegardens-star-b](teegardens-star-b.md) — 안쪽 자매, 온대 aquaplanet
- [teegardens-star-d](teegardens-star-d.md) — 바깥 자매, 차가운 황량한 암석
- [trappist-1-f](trappist-1-f.md) — HZ 바깥 가장자리의 자매 시스템 아날로그 (TRAPPIST-1 f 는 눈덩이/안구 경계에 더 가까움; c 는 완전 눈덩이)
- [proxima-cen-b](proxima-cen-b.md) — Dreizler 2024 는 c 의 ESI (0.88) 가 비교 가능하다고 인용
- [methodology](../reference/methodology.md) — Decisions 스키마
