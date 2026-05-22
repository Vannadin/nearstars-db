<!-- TRAPPIST-1 g Phase 3 합성: cfg-ready 결정과 그 근거 -->
# TRAPPIST-1 g — Phase 3 Synthesis

TRAPPIST-1 g 는 M8V ultra-cool dwarf 를 12.35 일 주기로 도는 1.13 R⊕,
1.32 M⊕ 의 암석 행성입니다. 안쪽에서 여섯 번째 행성으로 지구 일사량의
0.26 배를 받으며, 보수적 거주 가능 영역에서는 한참 바깥쪽에 놓여 있습니다.
TRAPPIST-1 행성 중 크기가 가장 크고, 물 함량도 가장 높은 축에 듭니다.
Bourgeois 2024 (2008.09599) 의 magma-ocean 진화 결과는 water mass fraction
을 0.11–0.24 로 산출했는데, 이는 시스템 내 최고치입니다. 2026-05-22 기준
g 에 대한 JWST 관측은 아직 출판된 바 없으며, 관측적 그림은 HST haze
한계 (Moran 2018) 와 이론적 기후 모델링 (Lincowski 2018, Wolf 2017) 이
주도하고 있습니다.

**NearStars 시나리오 선택은 매우 얇은 CO₂ 대기 (~0.05 bar) 를 가진 전역
빙결 ocean world 입니다. substellar 개방 수역은 없고, 빙하 아래에 액체
물 바다가 존재합니다.** 차가운 outer-HZ 행성에 대한 정석적인 snowball
혹은 "ocean world" 시나리오에 해당합니다. CO₂ 온실효과를 강하게 올려도
g 의 일사량으로는 표면 액체 물을 유지할 수 없으며, Wolf 2017 §5 가
~0.3 S⊕ 이하에서 완전 snowball 이 된다는 것을 보였습니다. 두꺼운 전역
얼음 피복 아래에는 radiogenic heat 에 의한 basal melting 으로 유지되는
상당한 규모의 빙하 아래 액체 물 층이 숨어 있습니다.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 12.35 d 궤도와 조석 damping. Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping. Agol 2021 |
| `eccentricity` | 0.00208 | high | Agol 2021 TTV. 시스템 내 최저값 |
| `argument_of_periastron_deg` | 191 | medium | Agol 2021. 매우 낮은 ecc 라 제약이 약함 |
| `sidereal_period_days` | 12.3524 | high | Agol 2021 |
| `semi_major_axis_au` | 0.04683 | high | Agol 2021 |
| `mass_mearth` | 1.321 | high | Agol 2021 TTV |
| `radius_rearth` | 1.129 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.036 | high | derived = 1.321 / 1.129² |
| `density_g_cc` | 5.06 | high | Agol 2021 |
| `water_mass_fraction` | 0.11–0.50 | medium | Bourgeois 2024 (0.11–0.24). Unterborn 2018 의 inward-migration 모델이 상한을 ≥50 wt% 로 올림 — 어느 쪽이든 시스템 최고치 |
| `insolation_s_earth` | 0.26 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 194 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.6, snowball) | 154 | high | derived. 고-알베도 snowball |
| `bond_albedo` | 0.55 | medium | snowball 얼음 + 얇은 대기. Wolf 2017 cold-snowball |
| `surface_temp_substellar_k` | 200 | medium | Wolf 2017 cold-snowball. basal-melt 는 표면과 격리 |
| `surface_temp_nightside_k` | 130 | medium | Wolf 2017 GCM 의 cold-trap nightside |
| `surface_temp_global_mean_k` | 175 | medium | Wolf 2017 cold-snowball 평균 |
| `atmosphere_present` | true (매우 얇은 CO₂) | medium | Moran 2018 이 H₂-rich 를 배제. outgassing 으로 누적된 얇은 CO₂ |
| `atmosphere_surface_pressure_pa` | 5 000 | medium | 0.05 bar — 174 K 에서 순수 CO₂ 의 안정 equilibrium 인 Turbet 2018 (1707.06927) 의 150 mbar 보다 아래. 화산 outgassing 이 계속된다는 가정 아래의 비평형 escape-balanced 상태. 150 mbar 이상이면 대기가 자가 유지되고, 0.01 bar 미만이면 사실상 무대기 행성이 됩니다 |
| `atmosphere_composition` | CO₂ 90%, N₂ 8%, 미량 H₂O 와 Ar | medium | 액체 물 carbonate-silicate cycle 이 없는 상태에서의 화산 outgassing |
| `atmosphere_scale_height_km` | 4.5 | medium | derived. kT/μg, T≈180 K, μ=43, g=10.2 m/s² |
| `atmosphere_tint_rgb_hex` | `#403028` (무시할 만한 Rayleigh + CO₂ 얼음 haze tint) | low | 매우 얇은 대기, 산란 거의 없음 |
| `cloud_cover_fraction` | 0.10 | medium | 매우 제한적. terminator 의 CO₂ 얼음 cirrus 정도 |
| `cloud_tint_rgb_hex` | `#d0c0b0` (CO₂ 얼음 + 먼지, M-dwarf shifted) | medium | 차갑고 얇은 대기에서 구름 생성이 최소 |
| `ocean_present` | true (빙하 아래만, 표면 표현 없음) | medium | Bourgeois 2024 wmf 0.11–0.24 + 지구-analog radiogenic heat → basal melt 가능성 높음 |
| `ocean_extent_substellar_radius_deg` | 0 | high | 완전 snowball. Wolf 2017 §5 |
| `ocean_tint_rgb_hex` | n/a (얼음 아래 숨겨짐) | high | 표면에서 보이지 않음 |
| `surface_ice_caps` | 100% 전역 피복 | high | 완전 snowball. Pierrehumbert 2011 outer-HZ branch |
| `surface_tint_rgb_hex_primary` | `#e8e0d4` (M-dwarf 빛 아래 깨끗한 눈) | medium | 고-알베도 눈 + 2566 K 조명 |
| `surface_tint_rgb_hex_accent` | `#a09080` (terminator 의 CO₂ 서리와 먼지 patch) | low | terminator 근처의 승화-퇴적 사이클 |
| `surface_morphology` | 전역 빙하 얼음. 차등 자전에서 비롯된 tectonic 응력이 pressure ridge 를 만들고, 따뜻한 spot 에서는 cryovolcanism 가능 | medium | Wolf 2017 + Europa-Ganymede analog 추론 |
| `magnetic_field_present` | 불확실 (내부 hydrosphere convection 으로 활성화 가능) | low | 무시할 수 없는 wmf 가 내부 mantle convection 으로 dynamo 를 유지할 수 있음 |
| `induction_heating_w_m2` | 0.002–0.02 | medium | Grayver 2022. 거리에 따라 감소 |
| `tidal_heating_w_m2` | 2×10⁻⁷–0.001 | medium | Hay & Matsuyama 2019. 이심률 강제의 Maxwell rheology 표면 flux 는 ~2×10⁻⁷ W/m², Andrade rheology 는 다소 큼. g 만 유일하게 planet-planet tides (대부분 f) 에서 2–20% 를 받음 |
| `xuv_flux_at_planet_F_earth` | ~120 (현재) | high | Berardo 2025 (2506.12140). 개정된 L_XUV = 1.83×10²⁸ erg/s 로 2017 추정치보다 30배 높음 |
| `stellar_microflare_cadence_min` | 45 | high | Berardo 2025. 10²⁹ erg microflare 가 ~45 분마다, 10³⁰ erg flare 가 6 시간마다 (JWST) |
| `radiogenic_heat_w_m2` | 0.04 | medium | 지구-analog mantle radiogenics |
| `magnetic_field_strength_microtesla_equator` | 10 | low | RM22 (2203.01065) 스케일링. 1.32 M⊕ (시스템 최대 질량) 가 활성 dynamo 를 뒷받침 |
| `magnetic_dipole_moment_normalized_earth` | 0.35 | medium | RM22 + 2208.06523 (지구급 core 가 dynamo 수명을 늘림). 내부 hydrosphere convection 도 기여할 수 있음 |
| `magnetic_dipole_tilt_deg` | 12 | low | tie-break. 12° 오프셋으로 독특한 오로라 cap 을 만듬 |
| `magnetosphere_standoff_planet_radii` | 4 | medium | Garraffo 2017 Fig. 4. 외곽 행성은 b/c 보다 덜 압축되어 g 궤도에서 4–5 R_p 가 그럴듯 |
| `radiation_belt_present` | true | medium | 자기장 충분 + 외곽 행성의 항성풍 압력 완화 |
| `surface_radiation_dose_msv_yr` | 5000 | high | Atri 2019 (1910.09871) Table 6. 0.045 AU 의 g + 50 g/cm² shielding + 자기장 기준 |
| `atmospheric_shielding_g_cm2` | 50 | medium | Phase 3 cfg 압력 0.05 bar → 약 50 g/cm² column |
| `aurora_present` | true | high | 대기 + 자기장 모두 우호적. CO₂ 지배 발광 |
| `aurora_color_primary_hex` | `#FF6B6B` | medium | CO₂⁺ Fox–Duffendack 600 nm 적색 (Mars-analog snowball 대기). tie-break. UV-only 보다 가시 적색 우선 |
| `aurora_color_secondary_hex` | `#87CEEB` | low | 미량 N₂⁺ 발광이 있다면. 없으면 산란 UV 가 옅은 청색으로 지각됨 |
| `aurora_emission_species_primary` | `CO₂⁺ UV doublet 289 nm + CO Cameron bands` | medium | snowball-얇은 CO₂ 대기의 Mars-analog |
| `aurora_oval_magnetic_latitude_deg` | 58 | medium | Vidotto 2013. R_mp ~4 R_p → α ≈ 30°, oval 위도 ~60° |
| `aurora_intensity_kR_typical` | 60 | low | Fraschetti 2019 의 양성자 flux 를 g 거리에 적용. 지구 대비 적당히 강화 |
| `star_apparent_angular_diameter_deg` | 1.36 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 g 는 0.26 S⊕ 에서 보수적 거주 가능 영역을 한참 벗어난 자리에
있습니다. Wolf 2017 §5 는 현실적인 대기 탈출 제약 아래에서는 10 bar CO₂
조차도 g 의 일사량에서 지속적인 개방 수역을 만들지 못한다고 봅니다.
cold trap 이 너무 효율적이기 때문입니다. Lincowski 2018 도 고려한 모든
대기 조성에서 g 를 snowball 로 분류합니다.

g 를 구해 주는 지질학적 특징은 매우 높은 water mass fraction 입니다.
Bourgeois 2024 (2008.09599) 가 g 에 대해 wmf 0.11–0.24 를 산출했고, 이는
TRAPPIST-1 시스템에서 최고치로 지구 바다의 20–50 배에 해당합니다. 이 물의
대부분은 빙하 아래 액체 물 바다로 존재하는데, 얼음-암석 경계에서 지구와
유사한 radiogenic heat (~0.04 W/m²) 가 basal-melt 를 일으키고 그 위를
두꺼운 (~50–100 km) 전역 얼음 피복이 덮고 있습니다. Cryovolcanism (Europa
와 Ganymede analog) 도 그럴듯하지만 아직 제약은 없습니다.

표면 모양에 대해 snowball template 이 다음을 줍니다.

- **Substellar 에서 substellar 기준 ~30° 까지.** 일사량이 약간 더 높아
  얼음이 가장 얇고 (~30 km), 더 차가운 terminator 와 nightside 쪽으로
  흐르는 얼음 흐름에서 tectonic 활동이 가능합니다.
- **중간 구역 (substellar 에서 30–120°).** 두꺼운 얼음 (~60 km), 큰
  스케일에서는 평활합니다.
- **Terminator (~90°).** pressure-ridge 밀도가 가장 높고, 지형 그림자도
  가장 깁니다.
- **Nightside (>120°).** 얼음이 가장 두껍고 (~100 km), 가장 차가운
  영역에는 CO₂ 서리 퇴적이 있을 수 있습니다.

**색 선택.** M-dwarf 조명 아래에서 깨끗한 눈과 빙하 얼음의 알베도를
반영합니다. primary 는 따뜻한 cream-white `#e8e0d4`, terminator 근처에는
누적된 먼지와 CO₂ 서리 사이클로 tan-shaded patch `#a09080` 가 들어갑니다.

**상한 water mass fraction 에서의 거주 가능성 caveat.** Acuña 2021
(2101.08172) 는 WMF ≥ 0.14 에서 high-pressure ice phase (HPP) 가
hydrosphere 의 암석-물 경계를 봉인해 버려, 빙하 아래 바다의 거주 가능성에
일반적으로 필수로 여겨지는 영양분 교환이 차단된다는 사실을 보였습니다.
WMF ≥ 0.10 에서는 내부 구성의 50% 미만만이 거주 가능한 sub-surface ocean
을 허용합니다. g 의 wmf 범위 (0.11–0.50) 가 정확히 이 임계를 가로지르고
있어, 빙하 아래 바다는 존재하지만 상한에서는 거주 가능 잠재력이 떨어집니다.
시각 cfg 입장에서는 렌더링상의 문제가 아니지만, Principia / astrobiology
관점의 플래그로서 Open items 에 적어 둘 가치가 있습니다.

**Cryovolcanism 따뜻한 spot 을 캐노니컬 시각 feature 로.** g 의 높은
water mass fraction (0.11–0.50) 과 radiogenic + 조석 가열이 결합되어,
두꺼운 (50–100 km) 얼음 껍데기 아래에 상당한 빙하 아래 바다가 존재합니다
(~0.04 W/m² 의 basal melt). Europa-Ganymede analog 추론은 얼음 껍데기가
가장 얇은 위치 — 일반적으로 warm-mantle anomaly 위 — 에서 cryovolcanism
가능성을 뒷받침합니다. 그런 자리에서는 basal water 가 표면까지 도달할 수
있습니다. [[feedback-phase3-interesting-first]] 원칙에 따라, cfg 는
cryovolcanic 분출을 "가능"에서 **canonical** 로 격상시킵니다. 2–4 개의
substellar 따뜻한 spot 근처에 가시 분출이 자리하고, 각각 폭 ~50–100 km
규모로 분출구 주변에 신선한 물-얼음 halo 를 만듭니다. 관측에 모순되지
않고 (어느 쪽도 직접 증거는 없음), 균일한 얼음 표면보다 극적으로 더
흥미롭습니다. cfg-variant 대안은 보존됩니다. 특징 없는 매끈한 snowball
입니다.

**Bedrock 과 산화철.** 사실상 보이지 않습니다. 전역 얼음 피복이 너무
두꺼워 bedrock 노출이 일어날 수 없습니다. 압력으로 얇아져 어두운 patch
가 드러날 수 있는 극단적 terminator ridge 꼭대기 정도가 예외일 수 있는데,
확률이 매우 낮고 궤도에서는 보이지 않습니다.

**조석 lock 아래의 모양.** 일사량 기울기가 최소 (substellar 와
antistellar 의 차이 ~70 K) 이라 얼음 순환이 부드럽습니다. tectonic 활동은
표면 승화 / 퇴적이 아니라 얼음 껍데기의 basal-melt-driven convection (cf.
Europa) 이 주도합니다. 결과적으로 따뜻한 spot 에서 cryovolcanic feature
가 생기는 지질학적으로 활성인 얼음 표면이 됩니다. 시각적으로는 미묘하지만,
"죽은 snowball" 과는 구분되는 인상을 줍니다.

## 대기 합성

g 에 대해 출판된 JWST 관측은 없습니다. HST haze 한계 분석 (Moran 2018,
1810.05210) 이 cloud-free 수소-rich 대기를 배제하지만, secondary 대기는
HST 로 제약되지 않습니다.

이론 모델들은 다음으로 수렴합니다.

- **Wolf 2017.** g 의 일사량에서 완전 snowball. ~10 bar CO₂ 도 액체 물에
  불충분합니다.
- **Lincowski 2018.** g 는 초기 water inventory 에 따라 "snowball" 혹은
  "post-runaway O₂-rich" 로 분류됩니다.
- **Bourgeois 2024.** magma-ocean 페이즈에서 초기 ~10 bar O₂ + CO₂ 대기를
  생성하지만, 대부분은 시스템 수명 동안 hydrodynamic escape 와 표면
  산화로 손실됩니다.

NearStars 는 **0.05 bar CO₂-rich 얇은 대기**를 채택합니다.

- **압력** 0.05 bar (5 kPa). g 의 온도에서 구름 형성에 필요한 임계값
  아래이며, 표면이 대부분 파장에서 우주와 복사적으로 직접 소통할 정도로
  얇습니다. 그래도 0 보다 큰 이유는, 얼어붙은 표면 탓에 carbonate-silicate
  weathering 이 작동하지 않아 화산 outgassing 으로 CO₂ 가 어느 정도
  누적되어야 하기 때문입니다.
- **조성** CO₂ 지배 (90%), N₂ (8%), 미량 H₂O 와 Ar. CO₂ 가 풍부한 것은
  outgassing 누적을 반영하고, H₂O 는 cold-trap 때문에 미량입니다.
- **구름.** 최소 (~10% 전역). terminator 와 nightside cold-trap 의 CO₂
  얼음 cirrus 정도입니다.

**Caveat — 대기 retention.** Van Looveren 2024 (2401.16490) 에 따르면
g 의 ~120 F_EUV,⊕ (Berardo 2025 / 2506.12140 이 L_XUV = 1.83×10²⁸ erg/s
로 2017 값보다 30배 높게 개정) 아래에서는 Jeans escape 만으로도 CO₂ 대기가
**1 bar 당 5 Myr** 수준으로 손실됩니다. 100 × 지구 대기조차도 수십 Myr
안에 잃게 됩니다. 따라서 0.05 bar 선택은 **낙관적인** 값이며, 화산 보충이
계속된다는 가정을 깔고 있습니다. 0.01 bar 또는 완전 무대기 변형은 cfg
백업으로 보존해 둡니다. 별의 microflare cadence (~10²⁹ erg 가 45 분마다,
Berardo 2025 의 HST Ly-α 다년 모니터링) 도 retention 을 더 압박하지만,
cfg 압력을 직접 결정하지는 않습니다.

**Turbet 평형 기준.** Turbet 2018 (1707.06927) 은 g 에 대해 CO₂ 대기
equilibrium 을 명시적으로 풀어, 150 ± 1 mbar 표면 압력 및 174 ± 0.1 K
에서 대기가 안정한 승화-응결 평형 상태에 있음을 보였습니다. 이보다 낮으면
CO₂ 얼음이 표면을 "전체 표면 수준까지 덮을 수 있고", 대기는 붕괴를 향해
불안정해집니다. cfg 의 0.05 bar 선택은 이 평형 아래에 있으며, 지속적인
화산 outgassing 으로 유지되는 비평형 상태를 가정합니다. 물리적으로는
타당하지만 자연스러운 끌개는 아닙니다. 다른 cfg 변형으로 Turbet 평형
압력 (0.15 bar) 을 채택하면, 열역학적으로 더 자기일관적인 대기가 됩니다.

**하늘 외관.** 0.05 bar 대기는 궤도에서 거의 보이지 않습니다. 표면에서
하늘은 거의 검고, 호스트 별이 공허를 배경으로 깊은 적-오렌지 디스크로
떠 있습니다. CO₂ 얼음 구름은 terminator 에서 비스듬한 빛을 받아 옅은
cream wisp 로 보입니다.

**GCM 교차 검증.** Fauchez 2019 (1911.08596) 는 g 에 대해 ≤10 bar 의
모든 그럴듯한 CO₂ 압력에서 snowball 상태를 확인했습니다. 10 bar CO₂
에서도 행성은 "substellar 영역 근처 몇몇 spot 을 빼면 거의 완전히 얼음
으로 덮여 있고, 그 spot 에서만 약간의 물이 바다에서 증발해 비교적 얇은
구름 (~0.1 kg/m²) 을 만든다" 고 합니다. cfg 의 완전 snowball 기본값은
잘 뒷받침됩니다.

**얼음 위 오로라 기하.** 적당한 자기장 (~지구의 0.35 배) 과 얇은
CO₂-rich 대기 조합으로, g 는 자기 위도 ~58° 에 Mars-analog 오로라를
띄웁니다. 지배 발광은 CO₂⁺ 적색 밴드 (Fox–Duffendack ~600 nm) 로, 고위도
얼음을 가로지르는 독특한 적색 오로라 띠를 만듭니다. 강도는 ~60 kR
(지구의 약 6배) 로 적당한 수준이지만, 어두운 snowball 표면 위에서는
충분히 보입니다. cfg 는 이를 `#FF6B6B` primary 띠로 렌더링하고, 미량의
질소가 기여하는 자리에는 `#87CEEB` secondary tint 를 선택적으로 얹습니다.
오로라 oval 은 지구보다 넓고, sub-Alfvénic 통과 동안 적도 쪽으로 ~50°
까지 확장됩니다. 적도 부근 플레이어는 북쪽/남쪽 지평선 위로 글로우처럼
번지는 오로라를 볼 수 있습니다.

## 자전과 spin 합성

12.35 일 주기에서 7.6 Gyr 의 조석 damping 을 거쳐 동기 (1:1) 구성에
도달했습니다. 황도 경사각은 0 으로 damping 되었습니다. 이심률은 0.00208
으로 시스템 최저이며, 3:2 안정 경계의 한참 안쪽이라 1:1 만 그럴듯합니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 12.3524 일 (1 067 251 s).

**계절 없음.** 황도 경사각 = 0. libration 으로 인한 일사량 변동은 0.2%
미만으로 시스템 최저이며, substellar 점은 고정됩니다.

**Planet-planet tides.** Hay & Matsuyama 2019 (1903.04501) 는 g 가 이심률
강제 조석 대비 **planet-planet 조석 가열의 비중이 가장 큰** 행성이라고
지적합니다 (전체의 2–20%, 대부분이 이웃 f 의 기여). 시스템의 다른 행성은
모두 planet-planet 기여가 1% 미만입니다. 절대값 자체는 여전히 작지만
(Maxwell rheology 기준 표면 flux ~2×10⁻⁷ W/m²), f 중력 영향의 상대적
지배는 g 만의 특징이며, Principia cfg 에 충실히 표기해 둘 만한 사실입니다.

**자기 dynamo 기대값.** g 는 TRAPPIST-1 행성 중 질량이 가장 크고 (1.32
M⊕), water mass fraction 도 가장 높아서 (Bourgeois 2024 + Unterborn 2018),
금속 core dynamo 와 별도의 hydrosphere convection 기여 둘 다 뒷받침합니다.
RM22 (2203.01065) 스케일링은 g 를 ~지구의 0.35 배 dipole moment 에
놓는데, 12.4 일의 느린 자전에도 불구하고 그렇습니다. Garraffo 2017 은
외곽 행성이 항성풍에 덜 압축됨을 보였고, 이에 따라 g 는 standoff 가 ~4
R_p 인 비교적 잘 정돈된 magnetosphere 를 갖습니다. Kerbalism cfg 는
1.5–4 R_p 의 닫힌 magnetosphere radiation belt 를 가정합니다.

## 비주얼 스타일

- **전역 외관.** terminator 근처에 미묘한 tan tinting (`#a09080`) 이
  도는, 거의 균일한 따뜻한 cream-white snowball (`#e8e0d4`). 뚜렷한
  "eyeball" feature 는 없습니다. 개방 수역 디스크도 없고, 시스템에서
  시각적으로 가장 차분한 행성입니다.
- **Substellar 영역.** 더 차가운 영역으로 흐르는 tectonic ice-flow 때문에
  얼음이 약간 더 텍스처화되고 균열이 보입니다. 밝은 신선-얼음 patch 로
  나타나는 cryovolcanic feature 도 가능합니다.
- **중간 구역과 terminator.** 비스듬한 2566 K 조명 아래의 pressure
  ridge, crevasse, 긴 지형 그림자. terminator 가 가장 사진발이 좋은
  구역입니다.
- **Nightside.** CO₂ 서리 때문에 약간 더 어두운 cream-tan. KSP nightside
  ambient 는 dayside 의 1–3% 수준입니다.
- **Atmosphere haze.** 궤도에서는 거의 인지 불가. limb 에 hairline 굵기의
  따뜻한-회색 glow (`#403028`) 정도만 보입니다.
- **Cryovolcanic 분출.** 2–4 개의 substellar 따뜻한 spot 이 얇은 대기로
  폭 ~50–100 km 규모의 신선한 물-얼음 분출을 쏘아 올립니다. 각 분출은
  vent 주위로 밝은 halo 를 만들며, 궤도에서는 snowball 을 배경으로 작은
  밝은 patch 처럼 보입니다. 분출은 간헐적이지만 (시간-일 단위 변동) KSP
  렌더링은 충실성을 위해 정적 feature 로 다루는 편이 낫습니다.
- **고위도 오로라 띠.** 자기 위도 ~58° 의 `#FF6B6B` 적색 CO₂⁺ 오로라가
  어두운 nightside 얼음 위에 떠 있습니다. 오로라 강도는 항성풍
  sub-Alfvénic 통과 동안 정점에 달합니다 (Garraffo 2017 기준, 매 궤도의
  50–80%).
- **하늘의 별.** TRAPPIST-1 이 g 의 하늘에서 1.36° 를 차지합니다 (지구에서
  본 태양의 2.7 배). 표면 조명은 0.26 S⊕ 로 외곽 화성의 태양 flux 와
  비슷합니다. cream 빛 설경 위로 떠 있는 적-오렌지 별이 영구적인
  어슴푸레-여명 분위기를 만듭니다. 사실적인 하늘 색조를 위해서는 항성
  표면의 비균질성도 중요합니다. Wakeford 2019 (1811.04877) 는 TRAPPIST-1
  에 가장 잘 맞는 모델로 3-온도 spot 모델을 제시했는데, photosphere 64%
  가 2400 K, spot coverage 35% 가 3000 K, facula 1% 가 5825 K 입니다.
  지배적인 디스크 색은 2400 K 의 차가운 photosphere 가 결정하며 (cfg 의
  `stellar_illumination_color_temp_k` 값 2566 K 가 Agol 2021 기반으로
  이미 반영), 35% 의 3000 K 영역이 고해상도에서 디스크에 옅은 노랑-오렌지
  overtone 을 더합니다.
- **하늘의 자매 행성.** f (안쪽 다음) 가 conjunction 시 각 크기 ~0.3°,
  h (바깥쪽 다음) 가 outer conjunction 시 ~0.2°. 공명 체인 덕에 다중
  행성 정렬이 자주 일어납니다.

## 참고 문헌

### 읽음 (시각 정보 제공, 위 결정 견인)

- **2008.09599** Bourgeois 2024 — Magma ocean evolution for e/f/g.
  g 를 시스템에서 가장 물이 풍부한 행성으로 확립 (wmf 0.11–0.24).
  빙하 아래 바다 cfg 의 근거입니다.
- **2412.10192** Cherubim 2024 — From CO₂- to H₂O-dominated atmospheres
  in magma ocean phase. g 의 진화된 대기에 대한 조성 프레임워크를
  제공합니다.
- **1809.07498** Lincowski 2018 — Evolved climates of TRAPPIST-1 worlds.
  고려된 모든 시나리오에서 g 를 snowball 로 분류합니다. d/e/f phase 3
  에서 이미 읽었습니다.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  경험적 M-dwarf 대기 retention 선에 대한 g 의 위치를 다룹니다. 얇은
  대기는 유지하지만 두꺼운 대기는 어렵다는 결론입니다.
- **1810.05210** Moran 2018 — HST haze limits. 안쪽 5 개 행성 (간접적으로
  g 포함) 에 대해 cloud-free H₂-rich 를 배제합니다. d Phase 3 에서 이미
  읽었습니다.
- **1706.02689** Unterborn 2018 — Inward-migration interpretation of
  TRAPPIST-1 densities. g 와 f 가 ≥50 wt% 물 / 얼음을 가진다고 주장하며,
  Bourgeois 2024 의 0.24 보다 훨씬 높은 상한을 제시합니다.
  `water_mass_fraction` 상한을 0.11–0.50 으로 끌어올린 근거입니다.
- **1903.04501** Hay & Matsuyama 2019 — Tides between TRAPPIST-1 planets.
  g 만 유일하게 조석 가열의 2–20% 를 행성 간 상호작용 (대부분 f) 에서
  받고, 다른 행성은 모두 1% 미만입니다. 자전 섹션의 새 문단을 견인합니다.
- **2401.16490** Van Looveren 2024 — Airy worlds or barren rocks?
  Jeans escape 기반의 정량적 대기 탈출. g 의 ~120 F_EUV,⊕ 에서 CO₂
  대기가 1 bar 당 5 Myr 로 손실됩니다. 새로 추가된 "대기 retention
  caveat" 문단과 대안 cfg 변형의 근거입니다.
- **2506.12140** Berardo 2025 — HST multi-year Ly-α monitoring of
  TRAPPIST-1. L_XUV = 1.83×10²⁸ erg/s 로 개정 (2017 추정치보다 30배 높음).
  microflare cadence 가 ~10²⁹ erg 당 45 분. 결정 표의 새 XUV / microflare
  항목을 견인합니다.
- **1912.05749** Hori & Ogihara 2020 — Hydrogen-rich atmosphere origin.
  g 의 최대 원시 H 대기는 2 wt% 이하이며 수백 Myr 내에 손실됩니다.
  현재 대기가 secondary 임을 뒷받침합니다.
- **1707.06927** Turbet 2018 — TRAPPIST-1 행성에 대한 climate diversity
  모델링. g 의 대기 평형 기준 (순수 CO₂ 에 대해 174 K 에서 150 mbar) 을
  견인하며, 그럴듯한 모든 압력에서 snowball 상태임을 확인합니다.
- **2101.08172** Acuña 2021 — Hydrosphere 특성화. g 의 빙하 아래 바다
  구조 (ice Ih 위에 high-pressure ice, 그 아래 암석 mantle) 를 검증합니다.
  WMF ≥ 0.14 의 거주 가능성 임계 (HPP 가 암석-물 경계를 봉인) 를 식별합니다.
- **1911.08596** Fauchez 2019 — Clouds and hazes 모델링. g 가 10 bar CO₂
  에서조차 snowball 상태임을 확인하고, substellar 부근에만 최소한의 구름이
  형성된다고 밝힙니다.
- **1811.04877** Wakeford 2019 — g 의 HST transmission 과 3-온도 항성
  모델. 정석적인 spot-coverage 값 (2400/3000/5825 K 에서 64:35:1) 을
  제공합니다. 별 하늘 색 예측을 정교화합니다.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. 외곽 행성의 magnetopause 기하를 제공합니다.
- **2203.01065** RM22 — 조석 고정된 암석 행성의 dynamo 스케일링.
- **1910.09871** Atri 2019 — g 의 표면 방사선 dose 표.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2508.12865** Empirical determination of the Cosmic Shoreline.
  g 의 retention 상태에 대한 맥락입니다.
- **2504.01182** Receding Cosmic Shoreline for mid-to-late M dwarfs.
  TRAPPIST-1 시스템 수준 맥락입니다.
- **2210.02484** HZ catalog. g 를 더 넓은 HZ 후보 중 하나로 등재합니다.
  d 에서 이미 읽었습니다.
- **2006.11349** Wunderlich 2020 — Wet/dry e and f. g 는 맥락만. f 에서
  이미 읽었습니다.
- **2506.16063** Mass-radius plane classification. 카탈로그 맥락만
  제공합니다.

### 읽음 (instrument-only, 시각 정보 아님)

(g 에 특화된 것 없음.)

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~14 편)

g 의 참고 문헌은 큰 편입니다 (66 편, 그중 52 편이 arXiv). 다만 대부분이
SETI / technosignature 서베이, mass-radius 카탈로그, 또는 g 를 지나가듯
언급하는 논문입니다.

- **2509.06310** Deep SETI search with FAST. 시각 정보 아님.
- **2208.02511** SETI drift rate context. 시각 정보 아님.
- **여러 cosmic-shoreline 논문** — retention 질문에 대해 집합적으로
  읽었으며, 개별 항목은 시각 정보 제공이 아닙니다.
- **TESS / non-TRAPPIST-1 카탈로그 논문** — 무관합니다.

---

## 후속 follow-up 항목

- g 에 대한 직접 JWST 관측은 아직 없습니다. 향후 transmission 또는
  emission 스펙트럼이 출판되면 대기 압력 / 조성 표를 재검토할 필요가
  있습니다. 특히 g 가 transmission 에서 CO₂ feature 를 보이면 0.05 bar
  선택을 더 정교화할 수 있습니다.
- Cryovolcanism 은 g 에 대해 그럴듯하지만 제약되지 않습니다. 향후 cfg
  변형이 Europa-analog 측면 (resurfaced 얼음 patch 가 보이거나, 따뜻한
  spot 에서 plume feature 가능) 을 강조하고 싶다면 Phase 3.5 로 구현할
  수 있습니다.
- 0.05 bar CO₂ 선택은 "대기 존재" 의 하한 경계입니다. ~0.01 bar 로
  내리거나, 완전 무대기 cold-snowball 변형을 위해 0 으로 둘 수도 있습니다.
- wmf 범위 (0.11–0.24) 는 g 가 해저 hydrothermal 활동을 갖춘 거주 가능
  빙하 아래 층을 호스트할 수 있을 만큼 충분히 높습니다 (Europa-Enceladus
  astrobiology analog). 시각적으로는 관련이 없더라도 Principia 노트에
  남길 가치가 있습니다.
- 0.05 bar 대기는 Turbet 평형 150 mbar 아래에 있습니다. 0.15 bar 의 cfg
  변형이 열역학적으로 더 자연스럽습니다. NearStars 가 "활성 outgassing
  평형" (Turbet) 을 선호할지, "탈출에 간신히 버티는 대기" (현재) 를
  선호할지에 따라 선택이 달라집니다.
- WMF 상한에서의 거주 가능성 제약. 0.14 이상에서는 HPP 가 mantle-바다
  교환을 봉인합니다. Principia 쪽 astrobiology 패스가 거주 가능성을
  중시한다면, g 를 상한에서 marginal 로 플래그해 두기 바랍니다.
- JWST GO 2589 가 flare 특성화 목적으로 g 를 관측했지만 (Burdanov 2025
  / 2512.04265 기준), 아직 출판된 대기 retrieval 은 없습니다. arXiv 를
  주기적으로 다시 확인할 가치가 있습니다.
- **cfg variant. 균일한 매끈한 snowball.** 대안으로 보존합니다. 활성
  feature 없는 해석을 선호하는 사용자를 위해서입니다.
  Cryovolcanism-plumes canonical 버전은 interesting-first 원칙에 따라
  선택되었습니다.
- 표면 방사선 dose ~5 Sv/yr 는 g 를 Kerbalism 의 "moderate-to-high"
  방사선 구간에 놓습니다. 50 g/cm² 의 대기 + ~30 m 의 얼음 차폐가
  있으므로, 얼음 아래 내부 거주지는 시스템에서 가장 안전한 축에
  들어갑니다.
