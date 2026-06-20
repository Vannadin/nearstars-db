<!-- TRAPPIST-1 f Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 f — Phase 3 Synthesis

TRAPPIST-1 f 는 M8V ultra-cool dwarf 를 9.21 일 주기로 도는 1.04 R⊕,
1.04 M⊕ 의 암석 행성입니다. 안쪽에서 다섯 번째 행성이며 지구 일조량의
0.38배를 받습니다. 보수적 거주 가능 영역의 바깥, maximum-greenhouse
한계 근처에 자리합니다 (Kopparapu 2013). 질량과 반경이 시스템 전체에서
지구와 가장 비슷하지만, Agol 2021 의 bulk density 가 4.92 g/cc 로 충분히
낮아 f 는 상당량의 물을 품은 워터 월드일 가능성이 높습니다. Acuña 2025
(2504.16201) 는 water mass fraction 을 16.2% ± 9.9% 로 추정합니다.
f 에 대한 첫 NIRISS 대기 정찰 (Lim 2024, ADS bibcode 2024ESS.....510106L;
arXiv preprint 없음) 은 구름 없는 수소 풍부 대기를 배제했지만 2차 대기에는
강한 제약을 걸지 못했습니다.

**NearStars 시나리오 선택. 표면 전체가 얼음으로 덮인 전역 snowball 이지만,
그 얼음 아래에는 Europa 형 sub-glacial ocean — basal/지열 용융과 행성의
높은 물 함량으로 유지되는 전역 얼음 아래의 액체 층 — 이 있습니다.**
interesting-first 룰 원칙에 따라, 관측과 모순되지 않는 시나리오들 중에서
더 인상적인 해석을 cfg 의 canonical 로 채택합니다. f 는 여전히 진정한
ocean world 이며, 다만 얼음으로 덮여 해양이 지각 아래에 숨어 있을 뿐입니다.
Wolf 2017, Turbet 2018, Fauchez 2019 는 모두 f 가 모델링된 모든 CO₂ 압력에서
완전한 snowball 이라는 데로 수렴합니다. f 는 HZ 의 maximum-CO₂-greenhouse
바깥 가장자리 너머에 있어, 30 bar CO₂ 에서도 표면의 물이 열리지 않습니다
(표면 open-water "eyeball" 은 f 가 아니라 e 의 것입니다). 보수적인 canonical
대안은 액체 층이 전혀 없는 완전히 얼어붙은 f 이며, 고증 cfg variant 로
보존합니다.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 9.21 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.01007 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 8.81 | medium | Agol 2021 |
| `sidereal_period_days` | 9.2075 | high | Agol 2021 |
| `semi_major_axis_au` | 0.03849 | high | Agol 2021 |
| `mass_mearth` | 1.039 | high | Agol 2021 TTV |
| `radius_rearth` | 1.045 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.952 | high | derived = 1.039 / 1.045² |
| `density_g_cc` | 4.92 | high | Agol 2021 |
| `water_mass_fraction` | 0.04–0.16 | high | Acuña 2025 (2504.16201) 가 MAGRATHEA 로 7-16% 보고, Acuña 2021 (2101.08172) 의 Fe/Si 제약 시나리오 2 는 3.7 ± 2.6%. 최근 추정치들의 합집합이 하한을 넓힘 |
| `insolation_s_earth` | 0.38 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 215 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, snowball) | 188 | high | derived. high-albedo snowball 케이스 |
| `bond_albedo` | 0.50 | medium | 전역 눈/얼음 cover (snowball). 높은 albedo, A=0.5 평형 온도 행과 일관 |
| `surface_temp_substellar_k` | 260 | medium | Wolf 2017 / Turbet 2018 snowball — substellar 최고점 ~260 K, 273 K 빙점 미만 (표면 open water 없음) |
| `surface_temp_nightside_k` | 165 | medium | Wolf 2017 GCM. 얼음으로 덮인 차가운 nightside |
| `surface_temp_global_mean_k` | 220 | medium | Wolf 2017 GCM cold-snowball 범위 |
| `atmosphere_present` | true (얇은 CO₂-rich) | medium | Lim 2024 가 H₂-rich 배제, 얇은 CO₂ 는 허용. Wolf 2017 outer-HZ snowball 케이스 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | 1 bar CO₂-rich (활성 규산염 풍화가 없는 얼음 덮인 세계에서 CO₂ 가 축적). Lim 2024 NIRISS 는 2차 대기를 제약하지 못함. f 는 모델링된 모든 CO₂ 압력에서 snowball 이므로 (Wolf 2017, Turbet 2018, Fauchez 2019), 압력은 온/냉 divergence 가 아님. |
| `atmosphere_composition` | CO₂ 95%, N₂ 4%, 미량 H₂O | medium | outgassing 주도. Wolf 2017 1 bar branch, substellar 표면 근처에서 H₂O 포화 |
| `atmosphere_scale_height_km` | 5 | medium | derived. kT/μg, T≈230 K, μ=43 (CO₂-rich), g=9.3 m/s² |
| `atmosphere_tint_rgb_hex` | `#604040` (매우 얇은 CO₂ Rayleigh + 먼지 haze) | low | 1 bar 에서 적당한 CO₂ Rayleigh + CO₂-ice/먼지 haze 가능 |
| `cloud_cover_fraction` | 0.25 | medium | Wolf 2017 — 차갑고 얇은 대기에서는 구름 형성이 제한됨 |
| `cloud_tint_rgb_hex` | `#d8c8b8` (CO₂ 얼음 + 물 얼음 혼합, M-dwarf 적색 이동) | medium | terminator + substellar cirrus |
| `ocean_present` | true (전역 얼음 아래의 sub-glacial basal-melt ocean — Europa-analog. 표면 open water 없음) | medium | Acuña 2025 wmf 16%. basal melting + 지열 flux 로 얼음 아래에 액체 층 |
| `ocean_extent_substellar_radius_deg` | 0 | medium | 표면 open water 없음 (snowball). 해양은 sub-glacial (Europa-analog). 이전의 40° 는 잘못 귀속된 표면 eyeball 해석에서 나온 값. Wolf 2017 은 실제로 f 를 snowball 로 만듦 |
| `ocean_tint_rgb_hex` | `#1a1c30` (깊고 어두운 navy, 대부분 얼음 아래) | low | sub-glacial ocean, 전역 얼음 아래라 궤도에서 보이지 않음 |
| `surface_ice_caps` | 전역 얼음 cover (snowball) — sub-glacial ocean 위 표면의 ~100%. pressure-ridge / sea-ice 텍스처 | medium | Wolf 2017 / Turbet 2018 snowball. 얼음이 표면 전체를 덮음 |
| `surface_tint_rgb_hex_primary` | `#e0d8d0` (깨끗한 눈 / 빙하 얼음) | medium | 눈 albedo + M-dwarf 조명 |
| `surface_tint_rgb_hex_accent` | `#888070` (먼지로 얼룩진 CO₂ frost + 능선 정상의 노출된 기반암) | low | nightside CO₂ frost over ice. 얇은 sublimation lag |
| `surface_morphology` | 얼어붙은 해양 위의 전역 빙하 얼음. pressure-ridge 지형. terminator 능선에 기반암 노출 | medium | tidally-locked snowball. Wolf 2017 |
| `magnetic_field_present` | true (약함, ~0.05× 지구) | low | 작은 질량 + 차가운 내부 + 느린 자전 |
| `induction_heating_w_m2` | 0.001–0.005 | medium | Kislyakova 2017 (1710.08761) — 총 induction heating 1.1×10¹⁸ W ≈ f 표면 기준 0.0012 W/m². molten-mantle 임계값 미만 |
| `tidal_heating_w_m2` | 0.0–0.19 | medium | Barr 2018 (1712.05641) — Maxwell viscoelastic. F_tidal,f = 0.14 +0.05/-0.14 W/m², mantle T_eq 1621 K. 하한은 0 (불확실성이 0 까지 걸침). 이전 Bolmont 2020 scaled 추정 대비 30배 높음 |
| `radiogenic_heat_w_m2` | 0.04 | low | 지구형 BSE(bulk-silicate-Earth) 방사성 열류속(현재값 ~0.04 W/m²)을 질량으로 스케일. 방법은 Wang et al. 2020 (`2020A&A...644A..19W`)의 외계행성 방사성 열 프레임워크를 따름. 다만 Eu→Th/U 호스트 원소비 보정은 호스트별 원소비를 큐레이션하지 않아 적용하지 않았고, 대신 지구형 원소비를 가정함 |
| `magnetic_field_strength_microtesla_equator` | 9 | low | RM22 (2203.01065) scaling. 1.04 M⊕ 는 활성 dynamo 를 지지하나 느린 자전 (9.2 d) 으로 multipolar 영역, ~0.3× 지구 |
| `magnetic_dipole_moment_normalized_earth` | 0.3 | medium | Garraffo 2017 (1706.04617) f 의 0.3 G 테스트 케이스. 활성 dynamo 를 지지 |
| `magnetic_dipole_tilt_deg` | 12 | low | 동률 처리. 12° 오프셋이 두드러진 auroral cap 를 만듦 |
| `magnetosphere_standoff_planet_radii` | 3.5 | high | Garraffo 2017 Fig. 4 하단 패널 — super-Alfvénic 조건의 f 에서 3–4 R_p |
| `radiation_belt_present` | true | medium | B-field 가 marginal 하게 충분. 외곽 행성이라 stellar wind 압축이 b/c 보다 덜 가혹 |
| `surface_radiation_dose_msv_yr` | ~70 (10²–10³ 차수. SPE 빈도 의존) | low | Atri 2019 (1910.09871). 강한 스펙트럼 SPE 1회가 1 bar + 지구형 B-field 에서 표면에 ~2.25 mGy (Table 4, 1000 g/cm². GCR 배경의 ≈1260배). 연간 = 이벤트당 × 플레어 빈도이며, 이 빈도는 이제 Vasilyev et al. 2026 (`2605.05468`, JWST+K2 플레어 빈도 분포) 이 정량화함. β = 0.753, E_TESS > 10³² erg 플레어가 ~25 일마다 (이전 추정 대비 ~10배). 이 빈도에서 ~70 mSv/yr, 정직한 범위는 여전히 10²–10³ 차수. 기존 7000 은 Table 6 의 30 g/cm² enhancement factor 를 mSv/yr 로 오표기 |
| `atmospheric_shielding_g_cm2` | 1000 | medium | Phase 3 cfg 압력 1 bar CO₂ → ~1000 g/cm² 기둥 |
| `aurora_present` | true | high | 대기 + B-field 모두 존재. 지구보다 얇은 CO₂-rich 대기는 Mars-analog 오로라를 만듦 |
| `aurora_color_primary_hex` | `#FF6B6B` | medium | CO₂⁺ Fox–Duffendack–Barker 밴드 적색 ~580–620 nm (Mars-analog). 동률 처리: 가시 영역의 적색을 UV 일변도보다 우선 |
| `aurora_color_secondary_hex` | `#B19CD9` | medium | CO Cameron 밴드 + CO₂⁺ ultraviolet doublet ~289 nm 의 가시 보라 산란 |
| `aurora_emission_species_primary` | `CO₂⁺ UV doublet 289 nm + CO Cameron bands + O 297.2 nm` | medium | MAVEN Mars 오로라 analog |
| `aurora_oval_magnetic_latitude_deg` | 55 | medium | Vidotto 2013, R_mp ~3.5 R_p → α ≈ 32°, 오로라 위도 ~58° |
| `aurora_intensity_kR_typical` | 80 | low | Fraschetti 2019 f 거리의 양성자 flux |
| `star_apparent_angular_diameter_deg` | 1.65 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 f 는 보수적 거주 가능 영역 (Kopparapu 2014) 의 바깥 가장자리에
자리하며 지구 일조량의 38% 를 받습니다. f 는 maximum-CO₂-greenhouse 바깥
가장자리 너머에 있어, CO₂ 적재량과 무관하게 표면이 전역적으로 얼어붙습니다
(Wolf 2017 §5 는 30 bar CO₂ 에서도 f 를 snowball 로 만들고, Turbet 2018 과
Fauchez 2019 도 CO₂ ≤10 bar 의 모든 범위에서 일치). GCM 이 이 일조량에서
실제로 만들어내는 표면 open-water eyeball 은 f 가 아니라 한 칸 안쪽 행성인
e 의 것입니다.

Acuña 2025 (2504.16201) 가 현재 최선의 내부 fit 을 제공합니다. 모든 내부
파라미터의 변화를 허용하면 water mass fraction 이 16.2% ± 9.9%, 또는
mantle-to-core 비율을 지구형으로 고정하면 6.9% ± 2.0% 입니다. 어느 쪽이든
f 는 지구보다 상당히 더 hydrated 된 행성이며, 전역 얼음 cover 아래에
전역 액체 물 층을 가진 진정한 "ocean world" 일 가능성이 큽니다.

Bourgeois 2024 (2008.09599) 의 magma-ocean 진화 작업은 f 가 100 Myr
이상 지속된 magma ocean 단계를 거치며 상당량의 대기 물과 산소를 만들어냈음을
시사합니다. 그 후 대부분의 물은 mantle 로 재평형되거나, 광분해 탈출로
우주로 손실되거나, 행성이 식으면서 표면에 응결되었습니다. 지금 남아 있는
sub-glacial ocean 과 얇은 CO₂ 대기가 장기적 endpoint 에 해당합니다.

표면 morphology 의 경우 tidally-locked snowball 템플릿은 다음의 구조를
줍니다.

- **Substellar disk** (substellar 점에서 ≲8°). ~260 K 의 얇은 얼음,
  open water 없음. substellar 최고점이 273 K 빙점 아래에 머물기 때문에,
  표면은 용융 lens 가 아니라 국지적 균열을 동반한 얼음입니다.
- **빙하 얼음 영역** (substellar 에서 8–180°). sub-glacial 액체 물 ocean
  위의 두꺼운 (>1 km) 빙하 얼음. 표면 T 는 ice line 의 ~250 K 에서
  antistellar 점의 ~170 K 까지 단조 감소.
- **Terminator** (substellar 에서 ~90°). 차갑고 (~190 K) 어두움. 가장
  사진발이 좋은 영역으로, 2566 K 빛이 비스듬히 비추는 가운데 pressure
  ridge 가 긴 그림자를 드리움. 빙하 흐름이 지각 highs 위에서 얼음을 얇게
  만든 곳에서는 기반암 노출도 가능.

**색 선택.** 눈과 빙하 얼음의 albedo 는 깨끗하고 신선한 경우 0.6–0.8,
먼지로 얼룩져 노화된 경우 0.4–0.6 입니다. M-dwarf 조명 아래에서는 청-백색이
아닌 따뜻한 크림색 (`#e0d8d0`) 으로 보입니다. nightside 의 CO₂ frost 가
어두운 패치에 약간의 황갈색 tint 를 더합니다 (`#888070`).

**interesting-first 에 따른 sub-glacial ocean.** Wolf 2017, Turbet 2018,
Fauchez 2019 가 모두 수렴합니다. f 는 모델링된 모든 CO₂ 압력에서 완전한
snowball 입니다 (Wolf 2017 에서는 30 bar CO₂ 에서도 snowball 인데, f 가
HZ 의 maximum-CO₂-greenhouse 바깥 가장자리 너머에 있기 때문입니다).
표면 open-water disk 는 없습니다 — substellar "eyeball" 기하는 f 가
아니라 e 의 것입니다. 따라서 interesting-first 해석은 sub-glacial
ocean-world 프레이밍을 택합니다. f 의 높은 물 함량 (Acuña 2025 wmf 16%)
과 basal/지열 용융이 전역 얼음 아래의 액체 층을 만들며, 궤도에서는 보이지
않더라도 이것이 f 를 정의하는 "ocean world" 특징입니다. 이렇게 하면 GCM 이
뒷받침하지 않는 표면 물을 지어내지 않고도 f 를 진정한 ocean world — 인상적인
Europa-analog — 로 유지할 수 있습니다. 액체 층이 전혀 없는 보수적인 완전
동결 해석은 고증 canonical 대안으로 Open items 에 보존합니다.

**Sub-glacial ocean 구조.** Acuña 2021 (2101.08172) 은 hydrosphere
층 구조를 상세히 다룹니다. 표면의 ice Ih, 깊이가 늘면서 등장하는 high-pressure
ice phase (II/III/V/VI), 바닥 (~100 GPa) 의 ice VII 로의 전이입니다.
지열 flux 에 따라 ice Ih 와 high-pressure ice 사이에 얇은 액체 물 lens 가
존재할 수 있는데, 이것이 cfg 가 이미 채택한 sub-glacial ocean 입니다.
태양계에서 가장 가까운 analog 는 Europa 형 층상 hydrosphere 입니다.

**광화학 haze / tholin 층.** Turbet 2018 §6 은 f 가 자신의 고도에서
광화학 haze 형성을 유지한다고 봅니다. 지질학적 시간 척도에서 이 haze 들은
UV 노출 지역으로 편향된 희미한 황갈색 표면 overlay 로 침적됩니다. cfg 의
산화철 accent 가 이미 비슷한 효과를 일부 잡아내지만, 메커니즘 (UV 광화학
→ tholin 침적) 은 산화 형성과는 별개입니다. 두 메커니즘이 모두 표면 색에
기여할 수 있습니다.

**산화철 / 기반암.** 노출은 제한적입니다. terminator 근처 능선 정상에서
빙하 흐름이 얼음을 얇게 만든 곳에서만 드러납니다. f 의 거리에서는 별의 UV
가 약하고 지속적인 얼음 cover 가 대부분의 기반암을 광분해 산화로부터
보호하기 때문에, 산화철 tint 는 안쪽 행성 (b, c) 에 비해 훨씬 희미합니다.

**조석 고정 하의 morphology.** 얼음 순환이 핵심입니다. substellar 점의
표면 가열이 얼음을 sublimate 시키며 (얇은 대기 탓에 속도는 낮음), CO₂ 와
미량 H₂O 는 대기 순환을 통해 더 차가운 terminator 와 nightside 로 운반되어
응결합니다. 그 후 빙하 흐름이 얼음을 다시 substellar disk 쪽으로 되돌리며,
결과적으로 표면 전체가 얼음으로 덮인 위에서 안정한 얼음 순환이 성립합니다 —
substellar 점에 open water 는 결코 형성되지 않습니다.

## 대기 합성

f 에 대한 Lim 2024 NIRISS 정찰 (arXiv preprint 없음, conference abstract
ADS bibcode 2024ESS.....510106L) 은 f 의 첫 JWST transmission 관측을
보고합니다. 결과는 다음과 같습니다. H₂-rich 대기는 배제되며 Moran 2018
(1810.05210) 의 HST 한계와 일관되지만, 2차 대기 (CO₂, N₂, H₂O-rich) 는
현재 가용한 transit baseline 으로는 제약되지 않습니다. 즉 f 의 관측적 그림은
b, c, d, e 보다 훨씬 더 열려 있습니다.

이론적 모델링 (Wolf 2017 §5, Turbet 2018, Fauchez 2019) 은 f 가 완전한
snowball 이라는 데로 수렴합니다. f 는 HZ 의 maximum-CO₂-greenhouse 바깥
가장자리 너머에 있어, 수십 bar 의 CO₂ 로도 표면의 물이 열리지 않습니다
(Wolf 2017 은 30 bar CO₂ 에서도 f 를 snowball 로 만들고, Turbet 2018 과
Fauchez 2019 도 CO₂ ≤10 bar 의 모든 범위에서 일치). 그럼에도 CO₂ 가 표면에
축적되는 것은, 전역적으로 얼음에 덮인 세계에서는 carbonate-silicate 풍화
sink 가 대부분 막혀 있기 때문입니다.

NearStars 는 **snowball 표면 위의 1 bar CO₂-rich 대기** 를 채택합니다.

- **압력** 1 bar (100 kPa). 얼음으로 덮인 표면에서는 활성 규산염 풍화가
  없어 CO₂ 가 축적됩니다. 이것은 두께 추정치일 뿐 온/냉 스위치가 아닙니다
  — f 는 모델링된 모든 CO₂ 압력에서 snowball 이므로, 여기서 압력은
  divergence 축이 아닙니다.
- **조성** CO₂ 지배 (95%), N₂ (4%), 미량 H₂O (얼음으로 cold-trap 됨).
  outgassing 주도이며, 표면이 전역적으로 얼음으로 덮여 있어
  carbonate-silicate 풍화는 제한적입니다.
- **구름.** 중간 정도 (~30% 전역). 얇은 물-얼음 및 CO₂-얼음 구름과
  terminator, 고위도의 간헐적 cirrus.

**Mars-analog 오로라.** 1 bar CO₂ 대기와 무시할 수 없는 자기장 (~0.3 ×
지구, Garraffo 2017 테스트 케이스) 을 모두 갖춘 f 는 stellar-wind 강하
입자로 인한 Mars-analog 오로라를 보유합니다. 지배적인 방출은 CO₂⁺
Fox–Duffendack–Barker 밴드의 580–620 nm 적-오렌지로, MAVEN 이 Mars 의
이산 UV+가시 오로라에서 본 것과 동일한 화학입니다. 부차적으로 CO₂⁺ UV
doublet 과 CO Cameron 밴드가 가시 보라색으로 산란합니다. 평균 stellar
wind 조건에서 오로라 oval 은 자기 위도 ~55° 에 자리하며, 강도는 ~80 kR
(지구 평균의 ~8배) 입니다. cfg 렌더링용으로는 오로라 oval 을 따라 주색
`#FF6B6B` 적색과 `#B19CD9` 보라 accent 를 둡니다. interesting-first
동률 처리: UV 일변도 렌더링 (플레이어 시점에서 보이지 않음) 대신 적+보라의
가시 팔레트를 선택했습니다.

**CO₂ cold-trap 기하.** Turbet 2018 은 f 의 CO₂ 얼음 침적이 경도 -120°,
위도 ±80°, 고도 30–50 km 의 두 개의 대칭적 cold trap 에 우선적으로 형성된다고
봅니다. 이는 cfg 의 시각적 annotation 으로 의미가 있습니다. nightside CO₂
얼음 구름은 균일하게 분포하지 않고 이 극지 cold-trap 영역에 집중됩니다.

**하늘 외관.** 1 bar CO₂ 대기는 적당한 Rayleigh scattering 을 주고,
M-dwarf SED 가 단파장 기여를 추가로 깎아 내립니다. substellar 근처 하늘은
별이 압도적으로 지배하는 가운데 희미한 dark-rust (`#604040`) 톤을 띠며,
terminator 근처에서는 CO₂ 얼음 구름의 forward-scattering 으로 limb 에
희미한 cyan-white 가 비치는 것을 제외하면 하늘이 어둡습니다.

## 자전 & spin 합성

7.6 Gyr 에 걸친 9.21 일 주기의 조석 damping 이 f 의 동기 (1:1) 구성을
확립합니다. 황도 경사각은 0 으로 damping 됩니다. 이심률은 0.01007 로,
3:2 spin-orbit 가 marginally 안정해지는 상단 가장자리에 해당하지만
(Vinson 2017), 1:1 이 여전히 압도적 확률의 상태로 남습니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 9.2075 일 (795 528 s).

**계절 없음.** 황도 경사각 = 0. libration 유도 일조량 변동은 ~ 1%
입니다 (e 보다 이심률이 높아 안쪽 행성보다 약간 큼). substellar 점은
본질적으로 고정되어 있습니다.

**자기 dynamo 기대.** f 의 지구 질량급 핵은 활성 dynamo 를 지지합니다
(Driscoll & Olson 의 2208.06523 스케일링은 지구 질량 dynamo 가 핵
고화 타이밍을 통해 수명이 연장됨을 보임). 9.2 일의 조석 고정 자전은
slow-rotation Reiners 스케일링으로 dipole 강도를 낮추지만 (~0.3 ×
지구 dipole), 일관된 dipole 자체는 유지 가능합니다. Garraffo 2017 은
f 를 거주 가능 영역의 대표 케이스로 명시하며 표면 자장 0.3 G 를 채택했고,
cfg 도 이 가정에 맞춥니다.

## 비주얼 스타일

- **전역 외관.** 궤도에서 본 f 는 균일한 빙하 얼음 snowball 세계
  (`#e0d8d0`) 입니다 — 얼음이 표면 전체를 덮으며 open-water 동공은
  없습니다. sub-glacial ocean 은 지각 아래에 숨어 궤도에서 보이지 않습니다.
  오로라 oval 의 `#FF6B6B` 적색 띠가 자기 위도 ~55° 근처의 nightside 를
  가로지르며, 어두운 얼음을 배경으로 그림자 속에서 보입니다.
- **Substellar 영역.** open water 는 없습니다. 희미한 얇은 얼음 텍스처와
  국지적 균열이 표면에서 가장 따뜻한 (~260 K) 부분을 표시하지만, 나머지
  전구와 같은 따뜻한 크림색 얼음으로 보입니다.
- **빙하 얼음.** 보이는 표면의 대부분을 차지합니다. 큰 스케일에서는
  매끄럽지만 terminator 의 비스듬한 빛 아래에서는 pressure ridge 와
  crevasse 가 드러납니다. 신선한 눈 (`#e0d8d0`) 과 먼지로 얼룩지거나 다시
  얼어붙은 얼음 (`#c8c0b0`) 사이에 미묘한 색 변화가 있습니다.
- **Terminator band.** 비스듬한 빛 아래 지형 대비가 큽니다. 능선 정상에
  기반암 노출이 있을 수 있습니다 (`#888070` accent).
- **Nightside.** CO₂ frost 가 만든 어둑한 크림-황갈색 톤. KSP nightside
  ambient 는 dayside 의 2–5% 수준.
- **Atmosphere haze.** 매우 얇은 따뜻한 회-적색 limb glow (`#604040`),
  두께는 5–10 km, 행성 limb 의 공간 배경에 대해서만 보입니다.
- **하늘의 별.** TRAPPIST-1 은 f 의 하늘에서 1.65° 를 차지합니다 (지구에서
  본 태양의 3배). 깊은 적-오렌지 disk 로 나타납니다. 표면 조명은
  0.38 S⊕ 로 지구의 깊은 황혼과 비슷하며, 별의 어둑한 적색 빛이 설경에
  영구적인 새벽빛 tint 를 부여합니다.
- **하늘의 자매 행성.** e (다음 안쪽) 가 inferior conjunction 시 각 크기
  ~0.3°; g (다음 바깥쪽) 가 outer conjunction 시 ~0.3°. 합은 약 25 일
  마다 일어납니다 (f-g synodic 주기).

## 고증 대안

### 고증과 어긋난 cfg 픽

| 항목 | 게임 (cfg) | 고증 대안 | 어긋난 이유 |
|---|---|---|---|
| `ocean_present` | true — sub-glacial Europa-analog ocean | 완전 동결, 액체 층 없음 (지열+조석+radiogenic flux 가 basal melt 에 부족할 경우) | 높은 물 함량 (Acuña 2025 wmf 16%) 과 basal melt 가 sub-glacial ocean 을 그럴듯하게 만들며, 이것이 f 를 정의하는 "ocean world" 특징입니다. 보수적인 완전 동결 해석은 cfg variant 로 보존합니다. snowball 표면 자체는 이제 canonical 과 일치하며 (Wolf 2017 / Turbet 2018 / Fauchez 2019) divergence 가 아닙니다. |

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2504.16201** Acuña 2025 — MAGRATHEA 를 이용한 f 의 내부 구조 분석.
  wmf 16.2% ± 9.9% (free CMF) 또는 6.9% ± 2.0% (지구형 mantle-to-core).
  f 를 ocean world 로 확립하며, sub-glacial ocean cfg 를 견인.
- **2008.09599** Bourgeois 2024 — e/f/g 의 magma ocean 진화. f 가 진화를
  거치며 상당량의 물을 보유했다고 예측.
- **2006.11349** Wunderlich 2020 — e 와 f 의 wet vs. dry 대기. f 의 대기를
  CO₂-rich (snowball branch) 또는 dry desiccated post-runaway 상태로 제약.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계들의 진화한 기후. f 는
  Lincowski 의 모델링이 차갑고 CO₂-rich 한 대기를 평형으로 보여주는 행성
  중 하나. d Phase 3 / e Phase 3 에서 이미 읽음.
- **1712.05641** Barr 2018 — TRAPPIST-1 행성들의 내부 구조와 조석 가열.
  f 의 조석 heat flux 를 0.14 W/m² (이전 추정 대비 30배) 로 상향 수정하는
  근거. Maxwell viscoelastic. mantle T_eq 1621 K.
- **2101.08172** Acuña 2021 — Hydrosphere 특성화. f 의 sub-glacial ocean
  구조 (ice Ih / high-pressure ice / ice VII) 를 상세히 다룸. WMF
  3.7 ± 2.6% scenario 2 로 water 함량의 하한을 넓힘.
- **1707.06927** Turbet 2018 — TRAPPIST-1 의 기후 다양성 모델링.
  **snowball 기본값을 견인.** 0.1 bar CO₂ 에서 f 는 완전히 얼음으로 덮임
  (substellar lens 없음). open ocean 은 ≥1 bar CO₂ 에서만 나타남. 극지
  CO₂ cold-trap 기하도 식별.
- **1710.08761** Kislyakova 2017 — Induction heating 추정. f 의 총량
  ~1.1×10¹⁸ W. cfg 의 induction heating 을 하향 수정.
- **1911.08596** Fauchez 2019 — HZ TRAPPIST-1 행성들의 구름 및 haze
  모델링. CO₂ 압력 ≤10 bar 의 모든 그럴듯한 범위에서 f 의 snowball
  상태를 확인.
- **1706.04617** Garraffo 2017 — TRAPPIST-1 의 위협적인 자기 및 플라즈마
  환경. f 를 거주 가능 영역의 대표 케이스로 채택. 0.3 G 테스트 케이스가
  cfg dipole moment 를 견인.
- **2203.01065** RM22 — 암석 행성 magnetic moment 스케일링.
- **1910.09871** Atri 2019 — f 의 표면 선량 테이블.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2605.06964** TRAPPIST-1 기후의 에너지 균형 모델. 방법론 논문이며 f 의
  snowball 상태를 지지.
- **2506.21351** SEPHI 2.0 거주 가능성 지수. 카탈로그 맥락만.
- **2502.00132** Way 2025 — d 중심 논문이지만 f 에도 적용되는 tidally-locked
  GCM 의 유용한 방법론 reference.
- **1810.05210** Moran 2018 — HST haze 한계. d Phase 3 에서 이미 읽음.

### 읽음 (instrument-only, 시각 정보 아님)

(이 깊이에서 f 에 특화된 항목 없음.)

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~9 편)

f 의 참고 문헌은 매우 작습니다 (15 편, arXiv 6 편).

- **2024ESS.....510106L** Lim 2024 — TRAPPIST-1 f NIRISS 대기 정찰.
  **f 의 핵심 관측 논문이지만 arXiv preprint 가 없음.** ADS 초록만 가용.
  대기 추론 (H₂-rich 배제, 2차 대기 미제약) 은 초록에서 가져왔음. **arXiv
  preprint 가 등장하면 fetch 하도록 flag.**
- **2025arXiv...** biosignature feasibility 와 ELT 특성화에 관한 다양한
  conference 요약. Skip.

---

## 후속 follow-up 항목

- arXiv preprint 가 가용해지면 Lim 2024 NIRISS f 논문을 재fetch. 공식
  출판 버전이 2차 대기 제약을 강화할 가능성이 있음.
- 1 bar CO₂ 두께는 outgassing 추정치이며 (얼음으로 덮인 표면에 CO₂ 가
  축적), f 특화 관측으로 제약되는 값은 아님. f 는 모델링된 모든 CO₂ 압력에서
  snowball 이므로 압력은 온/냉 스위치가 아니라 두께/haze 파라미터임. 미래의
  JWST emission 분광이 f 의 기둥값을 좁히면 그에 맞춰 정밀화.
- snowball 표면은 이제 변형이 아니라 **기본값** 임 (Wolf 2017 / Turbet 2018
  / Fauchez 2019 수렴). 균일한 빙하 얼음 구체가 canonical 렌더이며, 꺼 둘
  표면 open water 자체가 없음.
- **거부/공격적 변형: 1 bar CO₂ + substellar open-water "eyeball".** 이것은
  f 에 대해 Wolf 2017 이 뒷받침하지 않음 — f 는 30 bar CO₂ 에서도 snowball
  임 (open-water eyeball 은 e 의 것). 잘못 귀속된 해석을 명시적으로 거부로
  표시하기 위해서만 여기 기록함. f 에는 렌더하지 말 것.
- water mass fraction (7–16%) 이 충분히 높아서 f 는 Europa 와 비교 가능한
  sub-glacial 액체 물 층을 가질 가능성이 있음. 조석이나 radiogenic 가열이
  해저까지 닿는다면 hydrothermal 활동까지 동반할 수도 있음. 직접적인 시각
  요소는 아니지만 Principia annotation 으로 남길 만한 가치가 있음.
- f 에 남은 gameplay 대 fidelity 트레이드오프는 표면 상태가 아니라
  (어느 쪽이든 snowball 임) sub-glacial ocean 의 존재 여부임.
  interesting-first 픽은 Europa-analog sub-glacial ocean 을 유지하고,
  보수적 해석은 그것을 제거함.
- **고증 canonical 대안: 완전히 얼어붙은 f, 액체 층 없음.** 지열 + 조석 +
  radiogenic flux 가 basal melt 에 부족하면, f 는 sub-glacial ocean 없이
  바닥까지 고체 얼음임. 궤도에서의 렌더는 동일하고 (균일한 빙하 얼음),
  바뀌는 것은 `ocean_present` → false 뿐임. 보수적 cfg variant 로 보존함.
- 자기장 강도는 스케일링 기반임. TRAPPIST-1 특화 dynamo 모델이 가용해지면
  정밀화 가능.

## Related

- [trappist-1-e](trappist-1-e.md) — 내측 형제. 계의 거주가능역 기준점.
- [trappist-1-g](trappist-1-g.md) — 외측 형제. 둘 다 snowball 표면이지만, f 의 높은 물 함량이 sub-glacial ocean 을 더 그럴듯하게 만듭니다.
- [trappist-1-h](trappist-1-h.md) — 가장 바깥 형제. 둘 다 저일사 환경이지만 휘발성 예산이 다릅니다.
- [methodology](../reference/methodology.md) — Decisions 스키마.
- [mod-reference](../reference/mod-reference.md) — 다운스트림 모드.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10. Agol 2021 이후 f 의 질량이 +53% 이동 (계 내 최대 변화).
