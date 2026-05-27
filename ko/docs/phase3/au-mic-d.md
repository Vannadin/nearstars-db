<!-- AU Mic d Phase 3 합성. cfg-ready 결정과 근거 -->
# AU Mic d — Phase 3 Synthesis

AU Microscopii d 는 22 Myr 의 M1Ve flare star AU Mic 주위 12.74-d
궤도를 도는 1.053 ± 0.511 M⊕ 지구질량 행성 후보입니다. Wittrock et
al. 2023 (AJ 166, 232. `2023AJ....166..232W`, arXiv:2310.10719) 이
이미 알려진 행성 b 와 c 의 통과 타이밍 분석을 통해 TESS + 지상 결합
통과 데이터셋에서 발견했습니다. d 자체는 통과하지 않으며 (직접
반지름 측정 없음) 궤도 주기와 질량은 b 와 c 의 통과 시각에 새기는
중력 섭동에서 옵니다. Mallorquin et al. 2024 (`2024A&A...689A.132M`)
의 독립적 ESPRESSO RV 재분석은 d 신호를 marginal RV 유의성에서
찾으며 TTV 유도 질량과 일관됩니다. NASA Exoplanet Archive 에 등재된
반지름 (1.02 R⊕) 은 측정값이 아니라 질량-반지름 관계의 placeholder
입니다.

d 가 통과하지 않으므로 bulk 밀도, 대기, 표면 속성은 측정이 아니라
추론됩니다. 질량 불확실도 (± 0.511 M⊕. 거의 50%) 가 큽니다. 0.105
AU 의 약 0.092 L☉ 일사량은 지구의 ~8.4 배 — 어떤 합리적 거주가능
영역 경계 안쪽으로도 깊이 들어가며, 지구 analog albedo 가정에서 평형
온도가 ~440 K 입니다. d 는 snow line 안쪽이자 분해된 잔해 원반
(35–210 AU) 안쪽을 돕니다. AU Mic 의 super-flare 폭격에 노출된 세
안쪽 작은 행성 (b 와 c 와 함께) 중 하나입니다.

**NearStars 시나리오 선택. 조석 lock 된 지구질량 암석 행성. 활발한
화산에서 outgassing 된 얇은 secondary 대기 (~10⁴ Pa, CO₂ 우세), 주간
측면에 철 산화물 reddening 이 있는 현무암 표면, substellar 부근에
부분 냉각 lava 피처, 그리고 전반적으로 뜨거운 terminator-to-야간
열 분포. 이 시나리오는 documented divergence 로 선택. AU Mic 의 XUV
폭격 하 canonical 해석은 airless (22 Myr 에 걸친 빠른 대기 스트립)
이지만 cfg 는 화산 보충 thin-atmosphere 해석을 택합니다 — 어리고
조석 가열되고 가능하면 magma-ocean-residual 인 행성에서의 outgassing
이 그럴듯한 보충원이며, 대기의 시각적 존재가 cfg 의 가장 구별되는
피처이기 때문.** 27 개 cfg 픽. 22 개 canonical-aligned, 3 개 tie-break,
2 개 documented divergence (atmosphere_present, ocean_present).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 12.74 d 궤도. 0.51 M☉ 주위 0.105 AU 의 지구질량 행성에 대해 조석 감쇠 ≪ 22 Myr 나이 |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.00305 | high | Wittrock 2023 TTV fit |
| `argument_of_periastron_deg` | 160.79 | medium | Wittrock 2023 TTV fit (낮은 e → 약한 제약) |
| `sidereal_period_days` | 12.73596 | high | Wittrock 2023 TTV fit. Mallorquin 2024 RV 와 일관 |
| `semi_major_axis_au` | 0.105 | medium | 케플러 제3 통해 주기 + M☉ 에서 유도. Wittrock 2023 §4 |
| `inclination_deg` | 89.32 | medium | Wittrock 2023 TTV fit (edge-on 과 일관이지만 통과 관측 없음) |
| `mass_mearth` | 1.053 ± 0.511 | medium | Wittrock 2023 N-body + TTV 동역학 fit |
| `radius_rearth` | 1.02 | low | Tie-break. 통과 검출 없음. NEA placeholder 가 질량-반지름 관계에서 (Chen & Kipping 2017 확률 관계). cfg 는 지구-analog 암석 행성 시각 인식을 위해 1.02 선택 |
| `surface_gravity_g_earth` | 1.01 | low | 유도 = 1.053 / 1.02². 반지름 가정의 downstream |
| `density_g_cc` | 5.45 | low | 유도. 지구-analog 암석 조성과 일관 |
| `insolation_s_earth` | 8.4 | high | L = 0.092 L☉ 과 a = 0.105 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 478 | high | 유도 |
| `equilibrium_temp_k` (A=0.1) | 466 | high | 유도. 적당한 어두운 현무암 albedo |
| `bond_albedo` | 0.10 | medium | 부분 먼지 덮인 어두운 현무암 표면. M-왜성 SED 가 유효 albedo 감소 |
| `dayside_surface_temp_k` | 530 | medium | 얇은 대기 → 제한된 주야 재분배. 주간이 T_eq 보다 살짝 높음 |
| `nightside_surface_temp_k` | 250 | medium | 약한 대기 운반. 현무암 표면의 열 관성 |
| `atmosphere_present` | true (얇은 secondary CO₂) | medium | Documented divergence. Canonical alternatives 참조. 활동적 내부의 outgassing (Driscoll & Barnes 2015 어린 암석 행성에 대한 조석 가열 구동 화산 스케일링) 이 AU Mic XUV 폭격에도 불구하고 얇은 secondary 대기 보충 |
| `atmosphere_surface_pressure_pa` | 10000 | medium | Documented divergence. Canonical alternatives 참조. outgassing 균형 대 탈출에서 ~0.1 bar CO₂. 보수 variant 는 0 (airless) |
| `atmosphere_composition` | CO₂ ~85%, N₂ ~10%, SO₂ ~3%, H₂O 미량. outgassing 보충 | medium | 환원에서 산화 전이 하의 화산 outgassing 조성. 화산 plume 에서의 활동 마커로서의 미량 SO₂ |
| `atmosphere_scale_height_km` | 13 | medium | 유도. T = 450 K, μ = 43 (CO₂), g = 9.9 m/s² 의 kT/μg |
| `atmosphere_tint_rgb_hex` | `#704030` | low | Tie-break. interesting-first. M1V 의 붉은 조명 하 얇은 CO₂ + 화산 먼지 → muted red-brown haze. b/c 의 H/He 띠와 구별됨 |
| `cloud_cover_fraction` | 0.20 | medium | 얇은 대기 → 제한된 구름 형성. 화산 지역 근처의 옅은 SO₂ 에어로졸 haze 패치 |
| `cloud_morphology` | 활동 화산 지역 근처의 옅은 적운 / SO₂ haze 패치. 나머지는 대부분 맑음 | low | Tie-break. generic 보다 distinctive. SO₂ plume 이 활동 화산 province 에 국한 |
| `cloud_tint_rgb_hex` | `#a08070` | low | Tie-break. M-왜성 SED 하 SO₂ haze 의 따뜻한 크림 |
| `ocean_present` | false (차가운 야간에서 sub-glacial 가능. 가시 표면은 건조) | medium | Documented divergence. Canonical alternatives 참조. 표면 온도 영역 (주간 530 K, 야간 250 K) + 얇은 대기가 안정한 표면 액체 물을 배제. 원거리 hemisphere 에 cold-trap 얼음 가능 |
| `surface_tint_rgb_hex_primary` | `#5a4030` | medium | M1V 조명 하의 어두운 현무암 표면. 광화학 변경에서의 철 산화물 reddening |
| `surface_tint_rgb_hex_accent` | `#a04020` | low | Tie-break. interesting-first. 활동 화산 지역의 냉각 lava red 또는 광분해 산화 patch 모두 어울림. cfg 는 시각적 distinctiveness 를 위해 lava 선택 |
| `surface_morphology` | 철 산화물 reddening 을 가진 어두운 현무암 평원. substellar 의 국지적 냉각 lava patch. 표면 얼음 + 서리 lag 를 가진 야간 cold trap | medium | 조석 가열된 어린 암석 행성 (Driscoll & Barnes 2015 프레임워크). Myr 시간 척도의 화산 resurfacing |
| `surface_ice_caps` | 반-substellar 위치의 hemispheric 야간 서리 cap. 승화 구동 volatile 사이클 | medium | 조석 lock terminator 응결. 얇은 대기가 volatile 운반을 주간에서 야간으로 허용 |
| `magnetic_field_present` | true (약한) | low | 활동 내부를 가진 지구질량 암석 행성. 느린 자전에도 불구하고 dynamo 가능 |
| `magnetic_field_strength_microtesla_equator` | 5 | low | 느린 자전 (12.74 d lock) 에서의 약한 dynamo 이지만 활동적 코어. Reiners & Christensen 2010 스케일링 |
| `surface_radiation_dose_msv_yr` | 5000 | medium | 얇은 대기 column (~100 g/cm²) + 약한 자기장 → AU Mic super-flare 하 높은 표면 dose. Atri 2019 프레임워크 |
| `aurora_present` | true | medium | 얇은 대기 + 약한 B 필드 + 강한 항성풍 → 가시 오로라. Mars-analog CO₂⁺ 방출 |
| `aurora_color_primary_hex` | `#ff6b6b` | medium | CO₂⁺ Fox–Duffendack–Barker 밴드 빨강 ~580–620 nm. Mars-analog 가시 오로라 |
| `aurora_emission_species_primary` | CO₂⁺ doublet + CO Cameron 밴드 + O 297.2 nm | medium | 얇은 CO₂ 대기 화학. MAVEN Mars 오로라 analog |
| `star_apparent_angular_diameter_deg` | 4.2 | high | 유도. 2 × 0.82 R☉ / 0.105 AU × (180/π) ≈ 4.2° |
| `stellar_illumination_color_temp_k` | 3518 | high | host 별 Teff 에서 |

## Surface synthesis

AU Mic d 는 AU Mic 시스템의 네 행성 중 관측적으로 가장 불확실
합니다. 통과 없이 반지름은 측정되지 않습니다. NASA Exoplanet Archive
에 등재된 1.02 R⊕ 는 질량-반지름 관계 (Chen & Kipping 2017 확률
스케일링) 의 placeholder 이지 독립 측정이 아닙니다. cfg 가 이
placeholder 를 채택하는 이유는 (a) 지구-analog 밀도 가정 하 Wittrock
2023 N-body 유도 질량과 일관되고, (b) 대안 (더 작은 암석 행성을
더 높은 밀도로, 또는 더 큰 sub-Neptune 을 더 낮은 밀도로) 이 더
잘 제약되지 않기 때문입니다.

NearStars 의 목적에서 d 는 따라서 밀도 5.45 g/cc, 표면 중력 1.01
g_Earth 의 지구-analog 암석 행성으로 모델링됩니다 — 관측 윈도우
안의 그럴듯한 reading. 표면은 철 산화물 reddening 을 가진 현무암
입니다. 어두운 주조 (`#5a4030`) 는 환원성 대기 화학 하 풍화된
현무암에 흔한 M1V 조명 + 철광물 reddening 을 반영합니다. accent
조 (`#a04020`) 는 substellar 부근의 활동적 냉각 lava patch 를 표현
합니다 — 균일하게 풍화된 표면보다 시각적 흥미를 선호하는 tie-break
선택.

**조석 lock 하의 표면 형태.** 1:1 spin-orbit 동기화에서 substellar
hemisphere 는 영구 조명을 받고 (530 K 평형) 반-substellar hemisphere
는 영구 어둡습니다 (250 K). 대기 열 운반이 약해 (얇은 대기)
terminator 를 가로지르는 온도 구배가 가파릅니다 — ~1000 km 에 걸쳐
50–80 K 일 수 있음. 이는 다음을 구동합니다.

- **substellar lava province.** 조석 가열 + 방사성 가열 + 지속적
  항성 조명이 substellar hemisphere 를 지속적 화산 활동을 유지하기
  에 충분히 따뜻하게 유지합니다. 냉각 lava patch 가 활동 province
  안에서 1000–1500 K (붉은-노란 glow) 로 보입니다. 주변 현무암 평원
  은 530 K (어두움).
- **중위도 풍화 현무암.** terminator zone (substellar lava province
  과 야간 cold trap 사이) 이 광화학 철 산화물 reddening 의 풍화된
  현무암 평원을 호스트합니다 — 주 표면 색조 `#5a4030`.
- **야간 cold trap.** 반-substellar hemisphere 가 대기 운반에서
  서리 축적 — CO₂, SO₂, 미량 H₂O 가 응결. 표면 얼음 cap 이
  반-substellar 점에 국한. 얇은 서리가 ~30° 바깥으로 뻗음.

**광물학.** AU Mic 의 강한 XUV 플럭스에 의해 구동된 표면의 상부
mm 가 광화학 변경을 겪습니다. Fe²⁺ 함유 규산염이 Gyr 시간 척도에서
Fe³⁺ 로 산화되지만, 22 Myr 에서는 과정이 부분 완료에 그칩니다. 결과
는 fresh 어두운 현무암 + 부분 풍화 철 산화물 reddening 의 표면 —
정확히 cfg 가 채택하는 regolith reading.

시스템의 어린 나이는 **활동적 resurfacing 이 그럴듯함** 을 의미합니다.
어린 암석 행성에 대한 조석 가열 구동 화산 활동의 Driscoll & Barnes
2015 프레임워크는 e = 0.003 에서 d 에 대해 ~0.1–1 W/m² 의 조석 열
플럭스를 줍니다 — Io 의 2 W/m² 플럭스와 대략 같거나 약간 위. 이는
Myr 시간 척도에서 행성의 상당 부분을 resurface 하는 일시적 화산
활동을 구동하기에 충분합니다. cfg 의 substellar lava province + 대기
SO₂ haze 가 가시적 결과입니다.

## Atmosphere synthesis

d 의 대기는 cfg 의 가장 결과가 큰 픽이며 — 가장 수정에 노출된 픽
입니다. 지배적인 질문은 22 Myr 에 걸친 AU Mic 의 super-flare 폭격
이 어떤 primary H/He envelope 도 스트립했는지 (d 의 작은 질량과
AU Mic 의 포화 XUV 영역을 고려하면 매우 가능) 와, outgassing 으로
유지되는 얇은 secondary 대기가 현재 존재하는지입니다.

**Documented divergence.** XUV 탈출 논증의 canonical reading (Owen
& Wu 2017. Cohen 2024 시스템 수준 MHD. Tristan 2023 super-flare
센서스. Atri 2019 표면 dose 계산) 은 d 가 airless 여야 한다는 것
입니다. AU Mic 의 XUV 하 d 의 일사량에서의 대기 스트립 속도가
화산 활동이 잠잠한 지구질량 행성에 대한 outgassing 보충 속도를
초과합니다. cfg 는 다르게 선택 — ~10⁴ Pa (0.1 bar) 의 얇은 secondary
대기 채택 — 그 이유는 (a) AU Mic 의 어린 나이가 d 의 내부를 열적
으로 활동적으로 만들고 (조석 + 방사성 + 잔여 accretion 열), (b)
Driscoll & Barnes 2015 프레임워크가 Myr 시간 척도에서 활동 outgassing
을 뒷받침하며, (c) atmosphere-present cfg 가 bare-rock airless analog
보다 더 시각적으로 distinctive 한 표현을 제공하기 때문. canonical
airless reading 은 Open items 의 cfg variant 로 보존되고
`## Canonical alternatives` 에 등재.

**압력.** cfg 는 ~10⁴ Pa (0.1 bar) 채택. 이 압력에서 시각적 대기
효과 (가장자리 근처의 Rayleigh 산란, 일몰 색, 옅은 구름 덮개) 는
존재하지만 미묘합니다 — 지구 대기보다는 Mars 대기에 가깝습니다.
이 압력에서의 탈출 속도가 Gyr 시간 척도에서 outgassing 과 균형을
이룹니다.

**조성.** 비교적 어린 암석 행성의 화산 outgassing 은 CO₂ 우세 대기
를 만듭니다 (analog. 초기 지구, 초기 Mars). cfg 조성 (CO₂ ~85%,
N₂ ~10%, SO₂ ~3%) 이 이 canonical 화산 outgassing 템플릿을 반영
하며, SO₂ 는 활동 plume 활동의 마커입니다. H₂O 는 미량 수준 — 대부분
의 물은 내부 reservoir 에 갇혀 있거나 광분해 + 손실 (H 는 탈출, O 는
잔류하거나 표면 광물을 산화).

**하늘 외관.** d 의 얇은 CO₂ 대기 아래 주간 하늘은 흐릿한 적-주황
입니다 — Rayleigh 산란이 0.1 bar 에서 최소이므로 하늘은 주간에도
대부분 어둡고, 별의 직접 glare 와 옅은 먼지-reddening haze 만 있습니다.
대기를 수평으로 통과해 보면 더 깊은 red-brown 띠가 나옵니다 — 일몰
기하가 주간 전체에 걸쳐 지속됩니다. 화산 plume 의 SO₂ 에어로졸이
따뜻한 크림 색조 (`#a08070`) 의 국지적 대기 haze patch 를 만듭니다.
야간 하늘은 자매 행성 conjunction 과 별빛 외에는 조명 없이 어둡습니다.

**대기 보전.** 항성 양성자 이벤트 하 표면 dose 의 Atri 2019 프레임
워크는 d 의 대기가 — 0.1 bar 에서도 — 제한된 복사 차폐를 제공함을
시사합니다 (~100 g/cm² column, 지구의 1030 g/cm² 대비). Super-flare
이벤트 (Tristan 2023. Cully 1993) 가 주기적으로 상층 대기를 스트립
합니다. outgassing 이 수년에서 수십 년 시간 척도에서 보충합니다. cfg
는 이를 super-flare 이벤트 동안의 옅은 상층 대기 glow 로 렌더링합니다
— 가장자리 haze 의 잠시 향상으로 보입니다.

## Rotation & spin synthesis

0.51 M☉ 주위 0.105 AU 의 지구질량 행성에 대한 조석 감쇠는 암석
행성 Q ≈ 100 (Goldreich & Soter 1966) 에서 ~10⁵ 년 시간 척도로
진행됩니다 — 22-Myr 시스템 나이보다 훨씬 짧습니다. d 는 1:1
spin-orbit 동기화에 완전히 잠겨 있습니다. 이심률 0.003 (Wittrock
2023) 은 3:2 spin-orbit (Vinson 2017 임계점 ~0.01) 을 지지하기에
너무 낮습니다. 1:1 이 분명합니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 12.73596 일 (1 100 234
초). Kopernicus `rotationPeriod` 는 궤도 `period` 와 일치해야 함.

**계절 없음.** Obliquity 가 0 으로 감쇠. 이심률 유도 일사 변동이
≲ 1% — 무시 가능. substellar 와 반-substellar hemisphere 가 지질학적
시간 척도에서 안정.

**주야 열 대비.** 얇은 대기 (10⁴ Pa CO₂) 에서 주야 재분배가 약함.
예상 대비. 280 K (주간 530 K, 야간 250 K). substellar 점이 영구
~530 K, terminator 가 ~390 K, 반-substellar 점이 ~250 K. 이 온도들이
cfg 의 표면 형태를 뒷받침합니다. substellar lava province, 풍화된
terminator 현무암, 야간 서리 cap.

**느린 자전 효과.** 12.74-일 자전 주기에서 Coriolis 효과는 지구의
한 자릿수 약합니다. 대기 순환은 zonal jet 보다는 직접적인 주야 열
forcing 에 지배됩니다 (Sergeev 2020 substellar 대류 프레임워크).
substellar 대류 cluster + 야간 서리 응결이 지배적인 대기 패턴을
형성합니다.

## Visual styling

AU Mic d 의 시각 표현은 얇은 대기를 가진 조석 lock 암석 세계입니다
— b/c 의 가스 자이언트 디스크와 구별됨.

- **전반 외관.** 철 산화물 reddening 과 밝은 substellar lava province
  를 가진 어두운 현무암 디스크. 4.2° 각지름 (지구에서 본 태양의
  8 배) 의 AU Mic 이 비춥니다. 주간 hemisphere 는 활동적 substellar
  zone 을 가진 조석 lock 암석 행성의 특징적 "안구" 기하를 보입니다.
  substellar lava province 가 가장 밝은 피처로 1000–1500 K 에서
  red-yellow glow — 궤도에서 ~30° 지름의 밝은 patch 로 보임.
- **substellar lava province.** ~30° 반지름의 대략 원형 substellar
  영역 안에서 1000–1500 K (red-yellow glow) 의 활동적 냉각 lava
  patch. 주변 현무암 평원 (530 K) 은 어두움 (`#5a4030` 주 색조). 빛
  나는 lava 와 어두운 현무암 간의 대비가 cfg 의 가장 시각적으로
  돋보이는 표면 피처입니다.
- **terminator 풍화 현무암.** substellar lava 와 야간 서리 사이에서
  terminator zone 이 철 산화물 reddening 의 풍화된 현무암 평원을
  보입니다. 표면 색조 `#5a4030` 주, 활동 화산 patch 에서 `#a04020`
  accent. 비스듬한 조명에서의 긴 그림자가 미묘한 지형 기복을 드러
  냅니다.
- **야간 서리 cap.** 반-substellar hemisphere 가 서리 (CO₂, SO₂,
  미량 H₂O) 를 축적하면서 대기가 cold trap 으로 volatile 을 운반
  합니다. 반-substellar 점 중심의 국지적 밝은 patch (~30° 지름) 로
  보이고, 얇은 서리가 ~30° 바깥으로 뻗습니다. 서리가 별빛을 반사
  하여 야간 cold trap 이 흐릿하게 보입니다.
- **대기 haze.** 옅은 red-brown 가장자리 glow (`#704030`) 약 10–15
  km 두께 — Rayleigh 산란된 M-왜성 빛 + 화산 먼지 + SO₂ 에어로졸.
  활동 화산 지역 근처의 국지적 SO₂ plume 이 느린 zonal wind 에 표류
  하는 따뜻한 크림 patch (`#a08070`) 로 보입니다.
- **super-flare 동안의 오로라.** Mars-analog 가시 오로라 (`#ff6b6b`
  주, CO₂⁺ Fox–Duffendack–Barker 밴드 580–620 nm) 가 AU Mic super-flare
  이벤트 동안 나타납니다. 약한 자기장 극에 국한. 약한 필드 때문에
  오로라 oval 이 낮은 자기 위도 (~40°) 에 있습니다. flare 이벤트
  동안 야간 hemisphere 의 많은 곳에서 보임. 정적 동안에는 높은
  자기 위도에서만.
- **하늘의 별.** AU Mic 이 d 의 하늘에서 4.2° 를 차지 (지구에서 본
  태양의 8 배) — 주간 하늘을 지배하는 광활한 깊은 붉은 디스크.
  substellar 에서 표면 조명 지구의 8.4 배이지만 근적외선 쪽으로
  red-shift. 가시광 밝기는 지구의 정오 태양에 견줄 만함. Super-flare
  가 10–60 분간 1–3 등급 밝힘 — substellar lava province 의 일시적
  밝아짐으로 보임.
- **자매 행성.** b (가장 안쪽, puffy Neptune) 가 conjunction 에서
  ~0.3° 지름의 적당한 점으로 보임. c (중간, sub-Neptune) 가 더 작지만
  여전히 보임. e (가장 바깥, 확인된다면) 가 옅음. 35–210 AU 의
  가장자리 정면 잔해 원반이 AU Mic 양옆으로 가늘고 밝은 줄로 보임.

## Canonical alternatives

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `atmosphere_present` | true (얇은 CO₂ ~0.1 bar. outgassing 보충) | false (AU Mic XUV 폭격 하 airless) | Owen & Wu 2017 광증발 + Cohen 2024 시스템 수준 MHD + Tristan 2023 super-flare 센서스 하의 canonical 해석은 0.105 AU 의 AU Mic XUV 플럭스에 대해 지구질량 d 가 primary H/He envelope 도 vapor 두께의 secondary 대기도 보전할 수 없다는 것. cfg 는 화산 보충 thin-atmosphere reading 을 택함. 이유. (a) d 의 어린 나이 + 조석 가열이 활동 outgassing 을 뒷받침 (Driscoll & Barnes 2015), (b) atmosphere-present 시각화가 bare-rock airless analog 보다 의미 있게 더 흥미. canonical airless variant 는 cfg fallback 으로 Open items 에 보존. |
| `atmosphere_surface_pressure_pa` | 10000 (0.1 bar CO₂) | 0 (진공) | atmosphere_present 선택의 downstream. 보수 variant 는 모든 대기 시각 레이어 비활성화로 pressure = 0 배포. |
| `ocean_present` | false (가시 표면 건조. 야간 cold trap 이 얼음/서리 축적) | false (airless variant 도 표면 volatile 없음) | 두 variant 가 "표면 액체 물 없음" 으로 수렴하지만 야간 얼음 존재 여부에서 다름. cfg 는 atmosphere-present 시나리오에서 야간 얼음 유지. airless variant 는 야간 얼음 없음 (volatile 운반할 대기 없음). |

## Bibliography

### Read (visual-informative, drove decisions above)

- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719). N-body + TTV 동역학 질량. 12.74 d, 질량 1.053 ± 0.511 M⊕ 의 TTV 전용 후보로 d 도입. **cornerstone 발견 논문.**
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO RV 재분석이 d 신호를 marginal 유의성에서 회수. 불확실도 안에서 TTV 유도 파라미터 확인.
- **Driscoll P. E. & Barnes R. 2015** — *Tidal Heating of Earth-like Exoplanets around M Stars*, Astrobiology 15, 739 (`2015AsBio..15..739D`, arXiv:1506.08077). M-왜성 거주가능 영역의 어린 암석 행성에 대한 조석 가열 구동 화산 활동 프레임워크. d 의 표면 화산 + 대기 보충 논증에 채택.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810). 광증발 프레임워크. M-왜성 XUV 하 d 의 일사량에서 작은 행성이 Myr 시간 척도에서 대기를 스트립한다는 canonical 논증. cfg 의 documented divergence 가 이 reading 에 반함.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare 센서스. 10³¹ erg 위 비율 5.6/일. canonical alternative 에 대한 대기 스트립 논증 구동.
- **Atri D. 2019** — *Modelling stellar proton event-induced particle radiation dose on close-in exoplanets*, MNRAS 492, L28 (`2020MNRAS.492L..28A`, arXiv:1910.09871). 항성 양성자 이벤트 하 M-왜성 외계행성에 대한 표면 dose 계산. 복사 환경과 오로라 강도에 정보 제공.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a Key Role in the Climate of Tidally Locked Terrestrial Exoplanets: Insights from High-Resolution Simulations*, ApJ 894, 84 (`2020ApJ...894...84S`, arXiv:2004.03007). 조석 lock thin-atmosphere 행성에 대한 substellar 대류 프레임워크.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13428). TESS 의 b 발견. d 의 대기 보전 논의에 정보를 주는 항성 활동 맥락 제공.
- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, arXiv:2102.05288). c 의 발견. d 의 TTV 검출을 가능하게 한 안쪽 행성 구조 정의.
- **Chen J. & Kipping D. 2017** — *Probabilistic Forecasting of the Masses and Radii of Other Worlds*, ApJ 834, 17 (`2017ApJ...834...17C`, arXiv:1603.08614). d 의 placeholder 반지름 (1.02 R⊕) 에 NASA Exoplanet Archive 가 사용한 질량-반지름 관계.
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*, Icarus 5, 375 (`1966Icar....5..375G`). 1:1 spin-orbit 결론에 사용한 조석 감쇠 시간 척도 프레임워크.
- **Vinson A. M. & Hansen B. M. S. 2017** — *On the spin states of habitable zone exoplanets around M dwarfs: the effect of a near-resonant companion*, MNRAS 472, 3217 (`2017MNRAS.472.3217V`, arXiv:1709.00007). spin-orbit 공명 임계점. e = 0.003 이 3:2 에 너무 낮음.

### Read (instrument / non-decisive)

- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 455 (`2023MNRAS.525..455D`). host 별 ZDI. 행성 복사 환경에 대한 항성 자기장 맥락 제공.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). Mallorquin 2024 의 d 회수에 (간접적으로) 적용된 AU Mic RV detrending 방법론.

### Not read — no arXiv preprint or low-priority (~20 papers)

여러 최근 시스템 수준 동역학 연구 (3-행성 vs 4-행성 안정성 검사,
후기 TESS sector 의 TTV 재분석) 가 ADS 기록에 있지만, Wittrock 2023
의 headline 질량/주기 파라미터를 바꾸지 않아 이 합성을 위해 깊이
읽지 않았습니다. d-특정 특성화 계획에 대한 제안 초록과 학회 요약
(DPS, EPSC) 은 cfg-결정적 내용을 기여하지 않습니다.

## Open items for follow-up

- **d 의 통과 탐색.** d 의 궤도 경사각이 호의적이라면 (Wittrock
  2023 TTV fit 이 i ≈ 89.3° 를 주지만 상당한 불확실도) 미래의 TESS
  sector 나 PLATO 관측이 d 의 통과를 잡고 반지름을 직접 측정할 수
  있습니다. 이는 반지름 불확실도 + 밀도 불확실도를 low 에서 high
  confidence 로 collapse 시킬 것입니다.
- **독립 확인.** d 는 현재 marginal RV 회수의 TTV 전용입니다. 두
  번째 TTV epoch 나 더 높은 정밀도 RV 환원이 행성 확인을 강화할
  것입니다. d 가 철회된다면 (Mallorquin 2024 회수를 고려하면
  가능성은 낮지만 가능함) cfg 는 AU Mic 시스템을 b/c/e 만 배포해야
  합니다.
- **대기 검출 / 비검출.** d 의 어떤 미래 투과 스펙트럼 (통과가
  검출된다면) 도 atmosphere-present cfg 픽을 직접 제약할 것입니다.
  높은 SNR 의 비검출은 canonical airless variant 를 선호하고,
  CO₂/SO₂ 검출은 cfg 의 outgassing 시나리오를 뒷받침할 것입니다.
- **cfg variant. airless 암석 d.** canonical 해석 (canonical
  alternatives 행) — AU Mic 의 super-flare XUV 폭격에 의해 스트립된
  airless 암석 행성으로서의 d — 가 cfg variant 로 보존됩니다. 표면
  색조는 비슷하게 유지되지만 (현무암 + 철 산화물), atmosphere_present
  = false, ocean_present = false, 오로라 없음, 대기 haze 없음. lava
  province substellar 피처는 두 variant 모두에서 지속 (조석 + 방사성
  가열).
- **cfg variant. 무거운 d.** Wittrock 2023 의 질량 불확실도가 0.5–1.5
  M⊕ (1σ) 에 걸칩니다. 고질량 끝 (1.5 M⊕) 이 placeholder 반지름
  (1.02 R⊕) 에서 밀도 7.9 g/cc 를 함의 — Mercury 처럼 금속 풍부 조성.
  이 variant 는 canonical reading 과 시각적으로 구별되지 않을
  가능성이 크지만 내부 모델링 일관성을 위해 노트로 남겨야 합니다.
- **cfg variant. 조석 가열 극단.** Driscoll & Barnes 2015 프레임워크
  가 고-e + 고-Q 범위에서 ~10 W/m² 까지의 조석 가열을 허용. 광범위한
  화산 활동의 Io 급 전반 활동 d 를 만들기에 충분. cfg 는 적당한
  0.1–1 W/m² reading 채택. Io 급 variant 는 substellar lava province
  를 전 지구적 범위로 확장하고 대기 SO₂ 를 증가시킬 것입니다.

## Related

- [au-mic](au-mic.md) — disk 기하를 포함한 host 별 합성
- [au-mic-b](au-mic-b.md) — 자매 행성. 8.5 d 의 puffy hot Neptune
- [au-mic-c](au-mic-c.md) — 자매 행성. 18.9 d 의 sub-Neptune
- [au-mic-e](au-mic-e.md) — 자매 행성. 33.1 d 의 ESPRESSO RV 후보
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — downstream cfg 작성기
