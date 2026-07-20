<!-- TRAPPIST-1 c Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 c — Phase 3 Synthesis

TRAPPIST-1 c 는 M8V ultra-cool dwarf 를 2.42 일 주기로 도는 1.10 R⊕,
1.31 M⊕ 의 암석 행성. 바깥쪽으로 두 번째 행성이며 지구의 2.27 배에
달하는 insolation 을 받음. JWST MIRI 15 μm 의 secondary-eclipse
(Zieba 2023) 와 phase-curve (Ducrot 2025) 측정에서 도출된 dayside
brightness 온도는 369–380 K — 맨 암석이든 얇은 O₂ 지배 대기든 어느
쪽 시나리오와도 양립함. 10 bar (CO₂ 10 ppm) 부터 0.1 bar (순수
CO₂) 까지의 cloud-free O₂/CO₂ 혼합 대기는 배제되며, 황산 구름을 가진
Venus-analog 도 2.6σ 수준에서 disfavored.

**NearStars 시나리오 선택. 어두운 basalt 표면 위에 미량의 H₂O 수증기를
포함하고 유의한 CO₂ 가 없는 얇은 O₂ 지배 대기 (~0.1 bar).** 이는
Luger & Barnes 2015 / Lincowski 2018 / Lincowski 2023 의 "fossil
oxygen" 시나리오를 채택한 것. 초기에는 H₂O 가 풍부한 증기 대기였으나
어린 M-dwarf 의 pre-main-sequence 고광도 시기에 hydrodynamic H escape
가 일어나 수소는 우주로 빠져나가고 광분해로 만들어진 O₂ 만 남게 됨.
남은 표면은 풍화된 상태 (b 의 신선한 ultramafic 과 대비) 로, 성숙한
regolith 가 깔려 있음. b (대기 없음, 신선함), d (terminator 부근에
H₂O 얼음 구름이 있는 얇은 대기) 와 구분되면서도 관측과는 모순되지 않는
설정.

## Decisions

Kopernicus / atmosphere cfg-ready 값. `Confidence`. high = 직접 측정
되었거나 강하게 제약된 값, medium = 강한 근거를 가진 이론값, low =
허용 윈도우 안에서의 미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 2.42 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00654 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 282 | medium | Agol 2021 (낮은 eccentricity → 제약 약함) |
| `sidereal_period_days` | 2.4219 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01580 | high | Agol 2021 |
| `mass_mearth` | 1.308 | high | Agol 2021 TTV |
| `radius_rearth` | 1.097 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.087 | high | derived = 1.308 / 1.097² |
| `density_g_cc` | 5.45 | high | Agol 2021 이 5.447 g/cc (≈ 0.991 ρ⊕) 보고 |
| `insolation_s_earth` | 2.27 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 339 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 380 | high | Zieba 2023 MIRI F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 369 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.05 | medium | Ducrot 2025 가 0 (맨 암석) 과 ~0.3 (반사적) 사이로 제약 |
| `atmosphere_present` | true (thin) | low | O₂ 지배 시나리오를 채택; 대기 없는 (A) 안도 방어 가능 |
| `atmosphere_surface_pressure_pa` | 10 000 | medium | Lincowski 2023 의 1σ-consistent envelope 의 상단인 0.1 bar O₂ |
| `atmosphere_composition` | O₂ 98%, 미량 H₂O / O₃ / CO₂ ≲100 ppm | medium | Lincowski 2018 의 광분해 산소 예측; Lincowski 2023 fit |
| `atmosphere_scale_height_km` | 10 | medium | derived. kT/μg, T≈370 K, μ=32 (O₂), g=10.7 m/s² |
| `atmosphere_tint_rgb_hex` | `#3a3a40` (매우 옅은 O₂ Rayleigh + 얇은 O₃ Chappuis 흡수) | low | 0.1 bar 에서는 scattering 이 미미; O₃ 가 M-dwarf 조명 아래 살짝 gray-blue tint 부여 |
| `dayside_surface_temp_k` | 369 | high | phase-curve 로 측정된 brightness 와 일치 |
| `substellar_peak_temp_k` | 430 | medium | derived bare-surface subsolar (A=0.05, ε=1, 약한 advection) |
| `nightside_surface_temp_k` | 140 | medium | 얇은 O₂ 대기에서의 약한 advection; Ducrot 2025 의 nightside < ~150 K |
| `surface_tint_rgb_hex_primary` | `#2c2218` (풍화된 basalt) | medium | 노화된 basaltic 표면, 최근 화산 활동 없음; Mercury-mature regolith analog |
| `surface_tint_rgb_hex_accent` | `#604030` (광분해 기원의 산화철 patch) | low | 장기간 조석 고정된 표면 위의 UV 광분해; Turbet 2018 메커니즘 |
| `surface_morphology` | 풍화된 basalt 평원; 노화된 충돌 분화구; 잔잔한 기복 | medium | 최근 resurfacing 의 증거 없음 (b 와 대비); 누적 ~8 Gyr 충돌 |
| `surface_ice_caps` | substellar 점에서 ≳60° 떨어진 좁은 띠의 nightside CO₂ / H₂O frost | medium | 얇은 대기로도 미량 H₂O 운반 가능; nightside T 가 CO₂ frost point 보다 낮음 |
| `induction_heating_w_m2` | 0.05–0.5 | medium | Grayver 2022 — 거리 차이로 b 보다 낮음; 활발한 화산을 일으키기에는 부족 |
| `tidal_heating_w_m2` | 0.62 (+0.42/-0.53) (Dobos 2019) 또는 1.32 (+0.30/-0.47) (Barr 2018) | medium | Barr 2018 ([1712.05641](https://arxiv.org/abs/1712.05641)) 과 Dobos 2019 ([1902.03867](https://arxiv.org/abs/1902.03867)) — Grimm 2018 + Agol 2021 질량을 적용한 Maxwell viscoelastic 모델. Io 급 flux 수준이며, 맨틀의 T_eq 는 1659–1666 K (암석 solidus 위 → 부분 용융). |
| `core_mass_fraction` | 0.24 ± 0.08 | medium | Acuña 2021 ([2101.08172](https://arxiv.org/abs/2101.08172)) — Fe/Si 항성 제약 시나리오 |
| `iron_mass_fraction_pct` | ~50 | medium | Barr 2018 — 7 개 행성 중 가장 높은 밀도 (평균 7642 kg/m³), iron 가장 풍부 |
| `water_mass_fraction` | ≤4 × 10⁻⁶ | medium | Acuña 2021 — scenario 1 의 최적 추정치는 사실상 0 |
| `tidal_k2_over_Q` | (0.4–2) × 10⁻⁴ | medium | Brasser 2019 ([1905.00512](https://arxiv.org/abs/1905.00512)) 내부 모델; 동역학적 하한은 k₂/Q ≳ 1×10⁻³ |
| `moment_of_inertia_C` | 0.286 (범위 0.235–0.4) | low | Brasser 2019 의 대표 케이스 |
| `magnetic_field_strength_microtesla_equator` | 3 | low | RM22 스케일링. iron 함량이 가장 높지만 자전이 느려서 (2.4 d) → multipolar regime, 약한 dipole |
| `magnetic_dipole_moment_normalized_earth` | 0.08 | low | RM22 ([2203.01065](https://arxiv.org/abs/2203.01065)) — TESS 의 조석 고정 암석 행성은 0.01–0.1 M_Earth 영역에 몰림 |
| `magnetic_dipole_tilt_deg` | 12 | low | tie-break (interesting-first, interesting-first 룰 적용) — 비대칭 polar cap. 5–15° 의 미적 윈도우 |
| `magnetosphere_standoff_planet_radii` | 1.8 | medium | Garraffo 2017 ([1706.04617](https://arxiv.org/abs/1706.04617)) Fig. 4 — 거리 차이로 b 보다 약간 큼 |
| `radiation_belt_present` | false | medium | 자기장이 너무 약함 (지구의 <0.1 배) 이라 안정적인 입자 포획대를 유지할 수 없음 |
| `surface_radiation_dose_msv_yr` | 50000 | low | Atri 2019 ([1910.09871](https://arxiv.org/abs/1910.09871)) Table 6 을 c 의 0.0158 AU + 100 g/cm² 대기 차폐 조건으로 스케일링. 1 bar O₂ + 자기장이 치명적 flare spike 를 완화 |
| `atmospheric_shielding_g_cm2` | 100 | medium | Phase 3 cfg 압력 0.1 bar O₂ → 약 100 g/cm² column |
| `aurora_present` | true | medium | 얇은 O₂ 대기 + 약한 자기장의 조합이 가시광 오로라 emission 을 만들어냄 |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | O 원자 재결합에 의한 [OI] 557.7 nm 녹색 (O 가 풍부한 얇은 대기에서의 지구 오로라 analog). tie-break. interesting-first 가 UV 지배 대안 대신 녹색을 선택 |
| `aurora_color_secondary_hex` | `#A050B0` | low | O₂⁺ Second Negative bands ~330–400 nm 의 보라색. tie-break. interesting-first 가 UV-블루 연속체 대신 가시광 쪽 끝을 선택 |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + O₂⁺ Second Negative` | medium | 대기 조성 + 표준 오로라 화학 (O 가 풍부한 얇은 대기) |
| `aurora_oval_magnetic_latitude_deg` | 35 | medium | Vidotto 2013 Eq. 7 과 magnetopause ~2 R_p → α ≈ 45°. 약한 자기장이 oval 을 적도 방향으로 확장 |
| `aurora_intensity_kR_typical` | 100 | medium | Kislyakova 2018 의 c 에서의 항성 자기장 1100 nT (지구의 5 nT 대비) → 지구 오로라 driver 의 10–500 배 |
| `induction_heating_magma_ocean_fraction` | 0.68 | medium | Kislyakova 2018 ([1710.08761](https://arxiv.org/abs/1710.08761)) — c 가 시스템 내에서 **induction heating 분율이 가장 높음** (방사성 flux 의 68%). cfg 에 이미 들어가 있는 Io 급 조석 가열을 뒷받침 |
| `star_apparent_angular_diameter_deg` | 4.02 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

c 의 eclipse + phase-curve 데이터는 어둡고 albedo 가 낮은 맨 표면이든,
CO₂ 가 거의 없는 얇은 O₂ 지배 대기든 모두와 양립함 (Zieba 2023,
Lincowski 2023, Ducrot 2025). b 의 경우에는 Ducrot 2024 가 신선한
ultramafic 표면을 뒷받침하는 모델 일관성 논거를 제시했지만, c 의 eclipse
데이터는 풍화되지 않은 표면을 요구하지 않음. 오히려 반대 해석도 가능함.
c 는 tidal heating 과 induction heating 이 모두 b 보다 작기 때문에
표면이 b 보다 훨씬 더 오래되었을 가능성이 있음 (Bolmont 2020 의 추정상
c 의 tidal heating 은 ~10× 낮고, Grayver 2022 의 induction heating 도
같은 이유로 ~10× 낮음).

다만 최근 갱신된 조석 가열 추정치 (Barr 2018 / [1712.05641](https://arxiv.org/abs/1712.05641), Dobos 2019
/ [1902.03867](https://arxiv.org/abs/1902.03867)) 는 c 의 내부 heat flux 를 **Io 급 수준** 인 0.6–1.3
W/m² 로 끌어올림. 기존의 "b 에서 스케일링한" 추정보다 약 한 자리수
높은 값. 이로부터 c 가 **활발하거나 최근까지의 화산 활동** 을 가질
가능성, 심지어 규산염 마그마의 표면 분출까지도 시나리오 안에 들어옴.
따라서 cfg 는 표면 해석의 폭을 넓힘. 풍화된 basalt 가 여전히 가장 흔한
표면으로 남되 (~8 Gyr 의 충돌 누적), **국소적인 "hot spot" 에서의
신선한 basaltic resurfacing** 도 동등하게 그럴 듯한 후보로 다룸. 시각
적으로는 두 성격이 섞인 모습을 보여야 함. 전역적으로는 성숙한 regolith
가 지배적이되, 최근 화산 활동이 있었던 지역 부근에 더 밝고 덜 풍화된
patch 가 나타나는 식.

내부 조성도 7 개 행성 가운데 가장 두드러짐. Acuña 2021 ([2101.08172](https://arxiv.org/abs/2101.08172))
은 c 의 water mass fraction 이 사실상 0 (≤4×10⁻⁶) 이고, core-mass
fraction 은 0.24 ± 0.08 이라고 보고. Barr 2018 은 c 가 **TRAPPIST-1
7 행성 가운데 가장 높은 평균 밀도** (7642 kg/m³ — 질량의 약 50% 가
철) 를 가진다고 보고. 이 iron-richness 는 특정 조성 모델에 의존하지
않는 결과이며, c 는 바깥쪽 행성들의 water-rich 범위와는 명확히 동떨어진
위치에 있음.

**자기 유도 가열이 Io 해석을 뒷받침함.** Kislyakova 2018 ([1710.08761](https://arxiv.org/abs/1710.08761))
은 7 개 TRAPPIST-1 행성 전부에 대해 항성 자기장에 의한 induction
heating 을 계산했는데, c 가 받는 분율이 **가장 큼** — 방사성 flux 의
68% (b 는 ~17%, d 는 ~56%, 바깥쪽은 더 낮음). 여기에 Barr 2018 의
Io 급 조석 flux (1.32 W/m²) 까지 더해지면, c 의 내부 총 열 예산은
부분 용융 임계치를 한참 넘어섬. 표면 근처 마그마 저장소, 그리고
어쩌면 활발한 표면 화산 활동까지가 변두리 대안이 아니라 강한 기본
시나리오가 됨 — 이미 갱신한 Surface tint accent 의 신선한 basalt 와
활발한 resurfacing 쪽 방향과도 일관됨.

내부 조성은 상당량의 물과 양립 가능하지만 반드시 필요한 것은 아님.
Unterborn 2018 ([1806.10084](https://arxiv.org/abs/1806.10084)) 은 c 를 휘발성 외피가 없는 작은 핵 (Fe
≤23 wt%) 의 암석 내부로도, 8–34 wt% 의 물이 필요한 더 큰 핵 조성
으로도 맞출 수 있다고 보고함. 질량과 반지름만으로는 이 이체 축퇴를
해소할 수 없음. Grimm 2018 ([1802.01377](https://arxiv.org/abs/1802.01377)) 은 Agol 2021 (1.308 ± 0.056
M⊕) 보다 약간 낮은 질량 (1.156 +0.142/−0.131 M⊕) 을 제시하며, 휘발성
확률 ≥0.24 — 즉 c 가 확장된 휘발성 외피를 갖지 않는 시나리오와도 일관.
이 제약 조건 아래에서는 "풍화된 basalt" 표면이 가장 단순한 해석.

**색 선택.** M8V 조명 아래의 풍화된 basalt. 어두운 basaltic primary
`#2c2218` 는 풍화된 regolith 의 성숙도를 반영하기 위해 b 의 신선한
ultramafic `#1a1612` 보다 살짝 밝게 잡음. 산화철 accent `#604030` 은
b 보다 더 두드러지게 두는데, 이유는 두 가지. (1) 표면이 더 오래되어
산화가 진행될 시간이 충분했고, (2) 얇은 O₂ 대기가 지속적으로 저수준의
산화제를 공급하기 때문.

**Morphology.** 활발한 resurfacing 이 없다는 것은 충돌 기록이 그대로
보존된다는 뜻. 전 크기 영역에서 윤곽이 뚜렷한 분화구가 분포하며, 그
포화 밀도는 lunar highlands 에 근접함. 초기 100–500 Myr 의 마그마
바다 잔존 feature (Krissansen-Totton 2022, TRAPPIST-1 시스템에 대한
Magma Ocean Evolution 논문) 는 후기 충돌 분지와는 구분되는 넓은
highland 영역으로 일부 보일 것으로 예상.

## Atmosphere synthesis

Zieba 2023 (MIRI F1500W secondary eclipse, 4 visits) 은 15 μm 에서
Fp/F★ = 421 ± 94 ppm 을 측정. 이는 dayside brightness 온도 380 ± 31 K
에 해당하며, low albedo 의 맨 암석 또는 greenhouse 효과가 약한 얇은
대기와 일관됨. 데이터가 배제하는 시나리오.

- ≥10 ppm CO₂ 를 포함한 10 bar cloud-free 대기
- 유의한 CO₂ 를 포함한 1 bar cloud-free 대기
- 0.1 bar 의 순수 CO₂ 대기
- 황산 구름을 가진 Venus-analog 대기 (2.6σ)

Lincowski 2023 은 two-column climate-photochemistry coupled 모델을
사용해 더 폭넓은 대기 유형까지 탐색. 2σ 안에서 다음과 같은 결과.

- 낮은 CO₂ (≲100 ppm) 의 0.1 bar **얇은 O₂ 대기** 가 데이터와
  일관됨
- 1–10 bar O₂ + 100 ppm CO₂ 는 2.0–2.2σ
- 1–10 bar O₂ + 0.5% 이하 CO₂ 는 2.9σ
- 최대 10% 의 H₂O 수증기를 포함한 얇은 O₂ (1σ 이내)

Ducrot 2025 의 phase curve 가 결정타. c 의 dayside 는 369 ± 23 K, nightside
는 검출되지 않으며 (15 μm 에서 ≲ 110 ppm), 유의한 phase offset 도 없음.
결국 맨 암석 또는 얇은 O₂ 시나리오 둘 다 살아남음.

NearStars 에서는 **0.1 bar O₂ 지배 얇은 대기** 를 채택.

- **압력** 은 0.1 bar (10 kPa). 낮은 CO₂ 의 O₂ 지배 조성에 대한
  Lincowski 2023 의 1σ 일관성 envelope 안에 위치.
- **조성** 은 O₂ 가 지배적 (~98%) 이고, 미량의 H₂O 수증기 (~1%) 와
  광분해로 만들어진 O₃ (~100 ppm) 가 포함. CO₂ 는 Zieba 2023 /
  Lincowski 2023 제약을 충족하도록 매우 낮게 (~100 ppm) 유지. O₂
  의 기원은 hydrodynamic-escape 후의 fossil 산소. Luger & Barnes
  2015 에 따르면 초기 TRAPPIST-1 행성들의 H₂O 증기 대기는 H 를
  우주로 잃고 ~10 bar 정도의 O₂ 를 남겼을 것으로 예상되며, 이후
  광분해와 표면 산화가 진행되어 현재의 얇은 O₂ 잔재 수준까지 줄어듦.
- **구름 없음** 을 canonical 상태로 둠. 얇은 O₂ 대기는 정상 상태
  에서 구름이 형성될 만큼 물이 충분하지 않으며, CO₂ 도 CO₂-얼음
  구름을 만들기에는 너무 부족함.

**Population statistics 측면 지원.** Gialluca 2024 ([2405.02401](https://arxiv.org/abs/2405.02401)) 는
"b 는 대기 없음 + c 는 얇은 O₂" 라는 공동 제약 아래에서 안쪽 TRAPPIST-1
행성들에 대해 runaway escape 이후 시기를 MCMC 로 시뮬레이션. 결과는
다음과 같음. 초기 water 가 ≥1 TO 일 때 **c 시뮬레이션의 98% 이상이
O₂ 지배 대기를 유지** 하며, b/c 공동 역추론으로는 초기 water 가 8.2
+1.5/-1.0 Earth oceans 로 나옴. 즉 0.1 bar O₂ 선택은 관측과만 일관한
것이 아니라, runaway-greenhouse 이후 진화의 지배적인 결과이기도 함.

**오로라 시그니처.** 얇은 O₂ 지배 대기에서 입자 충돌이 만들어내는
지배적인 emission 은 [OI] 557.7 nm 의 녹색 (지구의 전형적인 녹색
오로라와 같은 선). 항성풍 압축이 magnetopause 를 ~2 R_p 까지 밀어
넣기 때문에 (Garraffo 2017), 지구에서는 고위도 좁은 띠에 머무는
오로라 oval 이 c 에서는 자기 위도 ~35° 까지 적도 쪽으로 확장됨.
그 결과로 오로라 띠가 극지방에 국한되지 않고 c 의 nightside 상당
부분에서 보이게 됨. 강도는 ~100 kR (지구의 평균 10 kR 대비 약 10
배) 에 이르는데, 항성풍이 상시적으로 강하기 때문. 보조적으로
330–400 nm 부근의 O₂⁺ Second Negative emission 이 보라색 가장자리를
보태며, cfg 렌더링에서는 primary `#4DFF4D` 녹색에 `#A050B0` 보라색을
accent 로 둠. interesting-first tie-break 는 가시광 영역의 이 팔레트를,
플레이어 눈에는 보이지 않을 UV 지배 emission 대안보다 우선 선택함.

**Sky appearance.** 0.1 bar O₂ 대기의 Rayleigh scattering 은 약함
(지구의 1 bar N₂+O₂ 대비 0.5 μm 에서 약 5%). substellar 점 근처의
하늘은 천정에서는 옅은 dark-violet 으로 보이다가 stellar disk 가
밝은 limb 쪽으로 갈수록 옅은 gray-orange 톤으로 바뀜. nightside
방향의 하늘은 사실상 검음. O₃ Chappuis 흡수 (0.6 μm 부근에서 peak)
가 dayside 산란광에 미묘한 회색 overtone 을 더함. 호스트 별은
각지름 4.02° (지구에서 본 태양의 약 8 배) 로 dayside 하늘을 압도.

## Rotation & spin synthesis

7.6 Gyr 동안 2.42 일 주기에 작용한 조석 damping 은 c 를 명확하게 동기
(1:1) 회전 상태로 고정시킴. 황도 경사각도 0 으로 damping. eccentricity
는 0.00654 (Agol 2021) 로, 3:2 공명을 유지하기엔 너무 낮음 (Vinson
2017 의 결론. 3:2 는 e ≳ 0.01 에서만 안정).

**마그마 바다 가능성의 시그니처.** Bolmont 2020 ([2002.02015](https://arxiv.org/abs/2002.02015)) 은
TRAPPIST-1 b/c 의 TTV 가 높은 행성 Love number (k₂ ≳ 1.5) 를 시사할
가능성을 보였는데, 이는 동역학적으로 액체 마그마 층의 존재를 의미하는
신호. Barr 2018 의 Io 급 조석 flux 와 합치면, c 가 부분 용융 상태를
가진다는 사전확률이 올라감. 다만 현재 TTV fit 은 noise-floor 에 묶여
있는 단계이므로 이 추론은 잠정적인 수준.

**자기 다이나모 기대치.** c 의 iron-rich 내부 (Barr 2018. 질량의 50%
가 Fe, 시스템 최고 밀도) 는 안쪽 행성 가운데 다이나모 측면에서 가장
유리한 케이스. 그러나 2.4 일짜리 조석 고정 자전이 Rossby number regime
전환 (Reiners & Christensen 2010) 을 통해 dipolar 자기장 강도를 크게
제한함. RM22 ([2203.01065](https://arxiv.org/abs/2203.01065)) 스케일링은 multipolar/weak 자기장 영역,
즉 지구 dipole moment 의 0.08 배 수준을 예측하며, 적도 표면 자기장
은 ~3 μT 정도. 이는 항성풍 플라즈마의 일부를 휘게 해서 오로라 oval
로 채널링하기에는 충분하지만, Van-Allen 같은 안정 입자 포획대를
유지하기에는 부족한 수준.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 2.4219 일 (209 254 s).
Kopernicus 의 `rotationPeriod` 는 초 단위 궤도 `period` 와 일치시켜야 함.

**계절 없음.** 황도 경사각이 0 이며, libration 으로 인한 insolation
변동도 < 0.5% 에 불과. substellar 점은 지질학적 시간 척도에서 표면
좌표계상 고정된 위치를 유지 (b 에서 언급한 느린 세차 운동은 별개).

**Eccentricity 가 유도하는 조석 굴곡.** e = 0.00654 와 ultra-cool
dwarf 호스트라는 조건에서 강제 libration 으로 인한 조석 가열률은 비교적
적당함. Brasser 2019 ([1905.00512](https://arxiv.org/abs/1905.00512)) 는 내부 모델로부터 k₂/Q 를 (0.4–2)
× 10⁻⁴ 로 제시하며, 동역학적 하한은 k₂/Q ≳ 1×10⁻³, 대표 관성 모멘트
는 C ≈ 0.286 (범위 0.235–0.4). 이로부터 도출되는 표면 tidal flux 는
b 보다 ~10× 낮음 (c 의 더 큰 궤도 반장축과 일관) — 활발한 화산을
일으키기에는 부족한 영역에 머묾. "풍화된 표면" 추론과도 부합함.

## Visual styling

표면과 대기 결정을 종합.

- **전역 색 팔레트.** 어두운 풍화 basalt 본체 (`#2c2218` primary,
  `#604030` accent) 가 강렬한 적색-주황 별빛을 받으면, substellar
  반구 쪽으로 치우친 미묘한 산화철 banding 을 가진 깊은 갈색-차콜
  세계로 보임. 얇은 O₂ 대기는 옅은 limb haze 외에는 궤도에서
  사실상 보이지 않음.
- **Dayside.** substellar 영역 (subsolar peak ~430 K, 일반 dayside
  ~370 K) 의 산화철 patch 는 substellar 점에서 30° 이내가 가장 강함.
  지형 기복은 잔잔함 — 성숙한 충돌 cratering 만 있고 활발한 화산
  활동은 없음. nightside 로의 열 재분배는 약하지만 0 이 아니며 (얇은
  O₂ 대기의 효과), nightside floor 가 ~140 K 로 유지됨.
- **Terminator band.** 2566 K 비스듬한 광선 아래에서 적당한 수준의
  지형 그림자 대비. 낮은 태양 천정각에서는 high-altitude 의 옅은
  gray Rayleigh-산란 haze 가 얇은 limb glow 로 보일 가능성.
- **Nightside.** 차갑고 (~140 K) 어두움. substellar 점에서 ≳60°
  떨어진 좁은 띠에 CO₂/H₂O frost 가 형성될 수 있으며, 자매 행성
  에서 반사된 빛 아래에서는 살짝 밝은 patch 로 비침. 가시광에서는
  열적외 emission 외에는 보이는 게 없음. KSP 의 nightside ambient
  는 dayside 의 약 5–10% 수준.
- **Atmosphere haze.** 두께 3–8 km 의 옅은 gray-violet limb haze
  (`#3a3a40`). 우주를 배경으로 행성 limb 에서만 식별 가능.
- **Star in sky.** c 의 하늘에서 TRAPPIST-1 의 각지름은 4.02° (지구
  에서 본 태양의 8 배). 색은 `#ff7a1a` (2566 K). 표면 밝기는
  ~2.27 S⊕ (지구 궤도에서의 금성 insolation 수준). flare 활동은
  b 와 동일 — 가끔씩 두드러진 IR flare 가 나타남.
- **Sister planets in sky.** b (안쪽 이웃) 가 inferior conjunction
  때 ~0.6°, d (바깥쪽 이웃) 가 4–6 일마다 일어나는 conjunction 때
  ~0.5° 로 보임. Agol 2021 에 따르면 거의 동일 평면 geometry.

## Bibliography

### Read (visual-informative, drove decisions above)

- **[2306.10150](https://arxiv.org/abs/2306.10150)** Zieba 2023 — c 의 JWST/MIRI F1500W secondary eclipse.
  Fp/F★ = 421 ± 94 ppm, dayside T ≈ 380 K. Venus-analog 와 대부분의
  CO₂-rich 대기 시나리오를 배제함. c 의 대기 상한에 대한 발견 논문.
- **[2308.05899](https://arxiv.org/abs/2308.05899)** Lincowski 2023 — two-column climate+photochemistry
  로 진행한 c 의 보다 넓은 대기 탐색. 낮은 CO₂ 의 얇은 O₂ 대기가
  1σ 안에서 데이터와 일관함을 발견. 채택된 O₂ 지배 시나리오의 근거.
- **[2509.02128](https://arxiv.org/abs/2509.02128)** Ducrot 2025 — b 와 c 의 MIRI 15 μm phase curve.
  c 의 dayside 369 ± 23 K, nightside 미검출. 대기 시나리오 공간을
  맨 암석 / 얇은 O₂ 쪽으로 좁힘.
- **[2305.01250](https://arxiv.org/abs/2305.01250)** Acuña 2023 — 내부-대기 결합 모델링. c 가 맨 표면
  일 가능성이 가장 높지만 얇은 대기도 배제할 수 없음을 보임.
  Lincowski 2023 가 해소한 표면-대기 축퇴를 뒷받침.
- **[2412.11987](https://arxiv.org/abs/2412.11987)** Nicholls 2024 — 용암 행성 대기에서의 대류 정지
  현상. c 를 사례 연구로 다루며, 비대류 대기 아래에서 마그마 바다가
  얼마나 지속될 수 있는지 탐색. "풍화된 표면" vs. "신선한
  ultramafic" 선택의 판단 자료가 됨 (c 는 풍화 쪽).
- **[1712.05641](https://arxiv.org/abs/1712.05641)** Barr 2018 — TRAPPIST-1 행성들의 내부 구조와 조석
  가열. c 의 조석 heat flux 를 Io 급 (1.32 W/m²) 으로 상향 조정
  하는 근거. c 가 가장 iron-rich 한 행성 (가장 높은 밀도, ~50% Fe)
  임을 식별.
- **[1902.03867](https://arxiv.org/abs/1902.03867)** Dobos 2019 — TRAPPIST-1 외계 행성의 조석 가열과
  거주 가능성. Grimm 2018 의 질량을 사용한 정제된 Maxwell
  viscoelastic 모델. F_int(c) = 0.62 W/m². 부분 용융 내부를 확정.
- **[2101.08172](https://arxiv.org/abs/2101.08172)** Acuña 2021 — 수권 (hydrosphere) 특성화. c 의 WMF
  ≤ 4×10⁻⁶, CMF 0.24 ± 0.08. "건조한 암석" 내부 선택의 근거.
- **[2405.02401](https://arxiv.org/abs/2405.02401)** Gialluca 2024 — MCMC escape 시뮬레이션. c 결과의
  98% 이상이 O₂ 대기를 유지. 0.1 bar O₂ 시나리오를 강하게 지지.
- **[2002.02015](https://arxiv.org/abs/2002.02015)** Bolmont 2020 — TTV 기반 Love number 제약이 마그마
  층 가능성을 시사.
- **[1706.04617](https://arxiv.org/abs/1706.04617)** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. 안쪽 행성들의 magnetopause 를 1.5–2
  R_p 영역에 두는 MHD 시뮬레이션.
- **[2203.01065](https://arxiv.org/abs/2203.01065)** RM22 — Internal Structures and Magnetic Moments.
  조석 고정 암석 행성의 다이나모 스케일링.
- **[1910.09871](https://arxiv.org/abs/1910.09871)** Atri 2019 — Stellar Proton Event 의 표면 흡수
  선량 테이블. 방사선 cfg 의 기준 문서.

### Read (context / methodology, not decision-driving)

- **[2412.16541](https://arxiv.org/abs/2412.16541)** 연속된 b/c transit 을 이용한 stellar contamination
  보정. 모든 TRAPPIST-1 transmission 관측에 적용되는 방법론으로,
  시각 정보에 직결되진 않음.
- **[2412.11627](https://arxiv.org/abs/2412.11627)** Ducrot 2024 — b 의 12.8 + 15 μm 결합 eclipse 분석.
  맨 암석 vs. CO₂-haze 해석 구도가 c 의 옵션과 평행하기에 함께 언급.
- **[2507.02052](https://arxiv.org/abs/2507.02052)** JWST MIRI 15 μm eclipse 데이터의 균일 재분석
  (frame-normalized PCA). cross-check 용이며, 결과는 일관됨.
- **[2505.03672](https://arxiv.org/abs/2505.03672)** TRAPPIST-1 행성의 secondary-atmosphere 공급원으로
  서의 water outgassing 에 대한 통계 지구화학 제약. "fossil O₂"
  추론의 배경 맥락 제공.
- **[1802.01377](https://arxiv.org/abs/1802.01377)** Grimm 2018 — TTV 기반 질량 + Bayesian 내부 fit.
  c 의 휘발성 확률 ≥0.24 (확장된 물 외피가 필수가 아님). 질량은
  Agol 2021 보다 약간 낮지만 불확실성 범위 안.
- **[1806.10084](https://arxiv.org/abs/1806.10084)** Unterborn 2018 — 갱신된 조성 모델. c 의 내부는
  작은 핵의 무수(無水) 암석 조성과 더 큰 핵의 습윤 (8–34 wt%
  water) 조성 사이에서 축퇴됨. 두 선택지 모두 현재 cfg 와 일관.
- **[1905.00512](https://arxiv.org/abs/1905.00512)** Brasser, Barr & Dobos 2019 — b 와 c 의 조석 파라
  미터. decisions 표의 새 항목인 `tidal_k2_over_Q` 와
  `moment_of_inertia_C` 의 근거. 참고. 이전 synthesis 에서 이 논문
  을 "Bolmont 2020" 으로 잘못 인용했던 것을 수정함.

### Read (instrument-only, not visual-informative)

- **[2409.19333](https://arxiv.org/abs/2409.19333)** stellar contamination 보정 방법론 논문. 완전성을
  위해 인용했으나 c 의 시각 콘텐츠에는 직접 기여하지 않음.

### Not read — no arXiv preprint or low-priority (~20 papers)

c 의 참고문헌은 b 의 것보다 작음 (32 vs 66). arXiv 가 없는 논문은
대부분 학회 요약이거나 자매 행성의 biosignature 연구. 건너뛴 주목할
만한 항목.

- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — Ducrot 2025 의 Nature
  Astronomy 정식 출판본일 가능성이 높음 (arXiv [2509.02128](https://arxiv.org/abs/2509.02128) 으로 이미
  다룸). Skip.
- **2025arXiv...** 다양한 retraction / re-fit 학회 요약. c 의
  eclipse depth 를 갱신하는 경우가 아니면 skip.

---

## Open items for follow-up

- 더 짧은 파장의 MIRI 필터 (예. c 의 F1280W) 로 진행될 향후 c
  emission 분광 결과에 대해 0.1 bar O₂ 대기 선택을 재검증할 것.
  대기 없음 시나리오도 통계적으로 동등하게 양립하며, 추후 렌더러가
  "맨 암석 형제" b+c 페어링이 필요하다면 그쪽이 선호될 수도 있음.
- 산화철 accent 의 두드러짐을 Way 2024 / Cohen 2024 (TRAPPIST-1
  표면 산화 모델링) 의 c 전용 예측과 대조 확인. 공개되는 시점에
  진행.
- "대기 없는 맨 암석" 해석에 대응하는 cfg 변형도 준비. b 의 대기
  없는 cfg 와 팔레트를 맞춰 페어링하는 방식.
- `density_g_cc` 항목 (5.45) 이 이제 Agol 2021 이 보고한 5.447 g/cc
  (≈ 0.991 ρ⊕) 와 정확히 일치하므로, 이전의 derived 값과 보고값
  사이의 불일치는 해소됨.
- 자기장 강도는 스케일링 기반의 low-confidence 값. Vedantham 2020
  같은 직접적인 radio emission 상한을 사용하면 dipole moment 범위를
  더 좁힐 수 있음.
- interesting-first tie-break 결과. 오로라 색은 UV 지배 대신 가시광
  녹색/보라색으로 설정. 더 넓은 렌더링 팔레트를 지원하는 경우라면,
  cfg variant 로 UV 지배 emission 을 옅은 glow 로 표현하는 것도 가능.

## Related

- [trappist-1-b](trappist-1-b.md) — 내측 형제. "유의한 대기 없음" JWST 코호트의 두 후보 중 하나.
- [trappist-1-d](trappist-1-d.md) — 인접한 외측 형제. 얇은 대기 시나리오가 cosmic shoreline 논리를 공유합니다.
- [trappist-1-e](trappist-1-e.md) — 계 전체의 거주가능역 기준점.
- [methodology](../reference/methodology.md) — Decisions 표 컨벤션과 신뢰도 라벨의 스키마.
- [mod-reference](../reference/mod-reference.md) — 다운스트림 KSP 모드.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 이 REX 기준 TRAPPIST-1 질량/반지름 재 fit 을 다룹니다.
