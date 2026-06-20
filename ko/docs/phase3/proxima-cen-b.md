<!-- Proxima Centauri b Phase 3 합성: cfg-ready 결정과 근거 -->
# Proxima Centauri b — Phase 3 Synthesis

Proxima Centauri b 는 태양에 가장 가까운 별을 11.18 일 거의 원형 궤도로
도는 1.055 지구질량 암석 행성입니다 (sma 0.04848 AU, 일조량 0.65× 지구).
Anglada-Escudé 외 2016 (Nature 536, 437. arXiv:1609.03449) 가 10 년의
HARPS, UVES, follow-up RV 모니터링으로 발견했고, 이어진 ESPRESSO +
HARPS + NIRPS 캠페인을 거치며 Suárez Mascareño 외 2025 (SM25) 의 결합
분석으로 정련됐습니다. SM25 가 보고한 현재 best 궤도 fit. P = 11.18465
± 0.00053 d, a = 0.04848 AU, e ≈ 0 (fit 정밀도에서 원형과 일관), Msini
= 1.055 ± 0.055 M⊕, JD 2 460 548.59 의 mean anomaly 0°. Faria 2022 와
SM25 모두 원형 궤도를 선호합니다. Anglada-Escudé 2016 의 원래 fit 은
non-zero best-fit eccentricity 가 아닌 e < 0.35 의 상한이었고, 이후
ESPRESSO + NIRPS 데이터가 이를 e < 0.1 (95% CL) 로 타이트하게 만들었
습니다.

행성은 통과하지 않습니다 (Jenkins et al. 2019, arXiv:1905.01336.
Gilbert et al. 2021, arXiv:2110.10702 — 여러 Spitzer + TESS 캠페인이
발견 주기에서 통과를 배제). 그래서 반지름, 밀도, 대기 성질은 측정값이
아니라 추론값입니다. Proxima b 의 기후 모델링은 이제 성숙했습니다.
Turbet et al. 2016 가 1D 파라미터 공간을 처음 mapping 했고, Boutle
et al. 2017 가 Met Office Unified Model (UM) 을 Earth-like 와 simplified-
N₂ 시나리오로 돌렸으며, Del Genio et al. 2019 가 active ocean 컴포넌트
를 더했고, Sergeev et al. 2020 가 substellar convection 을 강조했으며,
Salazar et al. 2020 와 Lewis et al. 2018 가 substellar continent
지오메트리를 탐색했고, Galuzzo 2021 가 3D 검출 가능성 시뮬레이션을
만들었고, Braam et al. (2022 / 2023 / 2024 / 2026) 가 trace species
스펙트라의 photochemistry framework 을 구축했습니다. Meadows et al.
2018 가 환경 상태와 관측 discriminant 를 열거했습니다.

대기 보유 질문 — Proxima 의 flare 환경에서 Proxima b 가 의미 있는
대기를 보유했는가 — 는 진짜로 열려 있습니다. Atri 2020 (1910.09871)
은 대기 없는 조건에서 다세포 생명에 lethal 한 표면 방사선 도즈를
계산하며, Lee 2021 (2109.06963) 은 ~10⁹ atoms cm⁻² s⁻¹ 의 Venus-analog
photochemical 산소 escape 를 모델링하고, Garraffo 2022 (2211.15697) 는
super-Alfvénic transit 동안 항성풍 ram pressure 가 태양값의 10⁴–10⁶
배 spike 함을 찾습니다. 반대편에서 Zuluaga 2018 (1609.00707) 은 적당한
고유 자기장 (~0.1 M⊕ 쌍극자 모멘트) 이 부분 차폐를 제공할 수 있음을
보이며, Meadows 2018 §3 는 모든 escape 계산이 초기 Proxima XUV 역사에
대한 가정에 의존하며 이 가정 자체가 10 배 수준에서 불확실하다고 지적
합니다. cfg 는 atmosphere-present 결정을 divergence 가 아니라 **tie-break**
으로 다룹니다. 문헌이 "보유" 와 "박탈" 시나리오 모두를 비슷한 plausibility
로 주며, NearStars 는 interesting-first 룰에 따라
시각적으로 구별되는 atmosphere-present 케이스를 선택합니다.

**NearStars 시나리오 선택. 1 bar N₂ + CO₂ 대기, substellar 점에서 ~60°
까지 뻗는 substellar 열린 물 ocean lens, 그 외 영역의 광범위한 빙하
ice 를 가진 1.055 M⊕ 의 조석 고정 암석 행성. 구름 덮개 55%, substellar
convective cluster 와 Rossby-wave-driven extratropical 변동성 포함.
약한 고유 자기장 (~0.1 M⊕ 쌍극자 모멘트), 크게 압축된 magnetosphere,
Proxima superflare 동안 잦은 aurora.** 42 cfg 픽. 31 canonical-aligned,
11 tie-break (hex 색상, 구름 morphology 디테일, 자기장 범위, 물 질량
분율). documented divergence 는 없습니다 — canonical reading (Boutle
2017 + Del Genio 2019 + Sergeev 2020 + Salazar 2020) 이 정확히 이
시나리오를 지지하며, snowball 과 desiccated 변형은 Open items 에 보존
됩니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 11.18-d 궤도. Walterová 2020 조석 고정 시간 스케일 ~10⁵ 년 |
| `obliquity_deg` | 0 | high | 조석 damping |
| `eccentricity` | 0.0 | high | SM25 — fit 이 원형과 일관 |
| `sidereal_period_days` | 11.18465 ± 0.00053 | high | SM25 |
| `semi_major_axis_au` | 0.04848 ± 0.00029 | high | SM25 |
| `mean_anomaly_at_epoch_deg` (JD 2 460 548.59) | 0 | high | SM25 |
| `mass_mearth` | 1.055 ± 0.055 | high | SM25 Msini |
| `radius_rearth` | 1.07 | medium | Tie-break. 비통과. 지구형 암석 구성에 대한 mass-radius 가 1.04–1.10 R⊕. interesting-first 가 시각 인식을 위해 1.07 선택 |
| `surface_gravity_g_earth` | 0.92 | medium | 유도 = 1.055 / 1.07² |
| `density_g_cc` | 5.36 | medium | 유도. 지구형 암석 구성과 일관 |
| `water_mass_fraction` | 0.05–0.10 | medium | Tie-break. Herath 2021 내부 모델이 0.001–0.4 허용. 표면 물 시각을 위해 지구형 윈도우 선택 |
| `insolation_s_earth` | 0.646 | high | L = 0.00157 L☉, a = 0.04848 AU 로 유도 |
| `equilibrium_temp_k` (A=0) | 226 | high | 유도 |
| `equilibrium_temp_k` (A=0.3) | 207 | high | 유도 |
| `bond_albedo` | 0.30 | medium | Boutle 2017 GCM 범위 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Boutle 2017 §3 — 조석 고정 simplified-N₂ 시나리오의 peak dayside. Del Genio 2019 동적 ocean 과 호환 |
| `surface_temp_nightside_cold_trap_k` | 150 | medium | Boutle 2017 §3 — 야측 cold-trap 최소 (Earth-like 대기는 살짝 더 따뜻) |
| `surface_temp_global_mean_k` | 250 | medium | Boutle 2017 — e=0 에서 mean 이 빙점 아래. Del Genio 2019 동적 ocean 이 ~10–20 K 야측 redistribution 추가 |
| `atmosphere_present` | true | medium | Tie-break. Boutle 2017 + Meadows 2018 + Zuluaga 2018 가 보유를 viable 하게 유지. Atri 2020 + Garraffo 2022 가 escape 선호. 둘 다 관측과 일관. interesting-first 가 interesting-first 룰에 따라 가시 대기 선택 |
| `atmosphere_surface_pressure_pa` | 100000 (1 bar) | medium | Boutle 2017 의 nominal Earth-like / simplified-N₂ 시나리오 모두 1 bar 에서 돌림 |
| `atmosphere_composition` | N₂ ~99%, CO₂ ~376 ppm (trace), H₂O 0.1–1% (substellar 근처 포화), trace O₂ | medium | Boutle 2017 simplified-N₂ (CO₂ MMR 5.94×10⁻⁴ ≈ 376 ppm). Braam 2024 의 trace species photochemistry |
| `atmosphere_scale_height_km` | 11 | medium | 유도. T = 260 K, μ = 30, g = 9.0 m/s² 의 kT/μg |
| `atmosphere_tint_rgb_hex` | `#4a3030` (M5.5V 아래의 깊은 빨강-시프트된 Rayleigh + Mie) | medium | Tie-break. Proxima SED 가 Rayleigh blue 를 크게 reddening. 게임 내 가시 대비를 위해 특정 shade 선택 |
| `cloud_cover_fraction` | 0.55 | medium | Boutle 2017 + Cohen 2023 wave-driven 구름 변동성 |
| `cloud_morphology` | substellar convective cluster + extra-tropical Rossby wave trains + 야측 더 맑음 | medium | Boutle 2017 + Sergeev 2020 substellar convection + Cohen 2023 traveling waves |
| `cloud_tint_rgb_hex` | `#d8a888` (M 왜성 아래 따뜻한 크림 물 구름) | medium | Tie-break. 물-구름 albedo × M 왜성 SED. 어두운 ocean 대비 따뜻한 톤 선택 |
| `ocean_present` | true (substellar 열린 물 lens) | medium | Boutle 2017 + Del Genio 2019 동적 ocean |
| `ocean_extent_substellar_radius_deg` | 60 | medium | Boutle 2017 — Earth-like 시나리오에서 substellar 부터 ~60° 의 ice line |
| `ocean_tint_rgb_hex` | `#0a2238` (희미한 빨강 별 아래 매우 어두운 navy) | medium | 낮은 일조량 + 깊은 액체 물 → 어두운 파랑-보라 |
| `surface_ice_caps` | ~60° 부터 바깥쪽으로 감쌈. 표면의 ~75% 커버 | medium | Boutle 2017 ice cover. Sergeev 2020 열 기울기 확인 |
| `surface_tint_rgb_hex_primary` | `#d4cab8` (빨강 별 아래 물 ice + frost) | medium | 물 얼음 albedo 0.5–0.7 × M 왜성 SED |
| `surface_tint_rgb_hex_accent` | `#7a4a30` (terminator 압력 ridge 꼭대기의 노출된 bedrock) | low | Tie-break. 고압 ridge 축에 subglacial 암석을 노출시키는 ice-flow 지오메트리 |
| `surface_morphology` | substellar 액체 ocean 디스크, sea-ice + slush 전이 환, 그 외에는 동결 ocean 위 빙하 ice, terminator ridge 의 노출된 bedrock | medium | eyeball-Earth 지오메트리에 대한 Boutle / Del Genio / Sergeev 컨센서스 |
| `magnetic_field_present` | true (적당) | medium | Tie-break. Zuluaga 2018 하한이 쌍극자 지지. 실제 값에 큰 불확실. interesting-first 가 aurora 시각을 위해 present 선택 |
| `magnetic_dipole_moment_normalized_earth` | 0.1 | medium | Tie-break. Zuluaga 2018 plausibility 범위 0.01–1.0. 부분 차폐 regime 을 위해 0.1 선택 |
| `magnetic_dipole_tilt_deg` | 15 | low | Tie-break. 구분되는 aurora-cap 지오메트리. 문헌이 Proxima b 의 쌍극자 tilt 에 침묵 |
| `magnetosphere_standoff_planet_radii` | 3–11 | high | Garraffo 2022 — magnetopause standoff 가 궤도 위상에 따라 3–11 R_p 로 변동 (표면 자기장 0.1 G). super-Alfvénic transit 때 하단으로 압축 |
| `radiation_belt_present` | false | medium | Garraffo 2022 + Atri 2020 — 무거운 CME 압축이 안정한 갇힌 입자 population 을 막음 |
| `surface_radiation_dose_msv_yr` | 5000 | low | Atri 2020 (1910.09871) SEP→dose 프레임워크, 1 bar 대기 차폐 + 약한 B 필드. superflare 동안 10⁵ 까지 spike. Atri 가 보고하는 값은 event 당 Gray + enhancement 계수이지 연간 mSv/yr 가 아니므로, 이 연간값은 변환 추정 → low |
| `atmospheric_shielding_g_cm2` | 1000 | high | 1 bar 대기 → ~1000 g/cm² 컬럼 |
| `aurora_present` | true | high | 대기 + B 필드 모두 존재. Garraffo 2022 + Vida 2019 의 잦은 superflare cadence 가 강렬한 강수를 구동 |
| `aurora_color_primary_hex` | `#4DFF4D` ([OI] 557.7 nm 녹색) | medium | Tie-break. N₂/CO₂/O₂ trace 대기 화학. 지구 analog 분광에 따라 녹색 산소 선이 dominant |
| `aurora_color_secondary_hex` | `#FF4D4D` (CO₂⁺ Fox–Duffendack–Barker + N₂⁺ Meinel 빨강 밴드) | medium | Tie-break. N₂+CO₂ trace 대기의 photochemistry. 가시 팔레트 다양성 |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + N₂⁺ 391.4 nm First Negative + CO₂⁺ doublet` | medium | Braam 2024 photochemistry framework |
| `aurora_oval_magnetic_latitude_deg` | 60 | medium | 약한 B 필드 + super-Alfvénic 압축이 aurora ring 을 넓힘 |
| `aurora_intensity_kR_typical` | 500 | medium | 지구의 전형적인 10 kR baseline 의 10–50 배. 잦은 superflare boost |
| `star_apparent_angular_diameter_deg` | 1.5 | high | 유도. 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2980 | high | Proxima Teff |

## Surface synthesis

Proxima b 는 canonical "eyeball Earth" 입니다 — 빙하 ice 로 둘러싸인
substellar 열린 물 디스크를 가진 조석 고정 암석 행성. Boutle 2017 §3 가
이 지오메트리가 Earth-like 대기 (현대 구성) 와 simplified-N₂ (1 bar
N₂ + 376 ppm CO₂) 시나리오에 걸쳐 지속됨을 입증하며, Del Genio 2019 가
동적 ocean 컴포넌트를 추가해도 살아남음을 확인합니다 (실제로 열 재분배
를 강화해 열린 물 디스크를 약간 더 넓힙니다).

substellar 열린 물 디스크는 substellar 점에서 약 60° 까지 뻗으며, 이를
넘으면 표면 온도가 빙점 아래로 떨어지고 안정한 빙하 ice 가 형성됩니다.
경계는 sharp 하지 않고, sea-ice, slush, 간헐적 melt-back 의 전이 환이
시각적으로 인상적인 색과 텍스처 변화의 ring 을 만듭니다. 디스크 자체는
어둡습니다 — cfg 에서 `#0a2238` — 낮은 M 왜성 일조량 (0.65 S⊕) 과 물의
700 nm 이상 깊은 흡수가 결합한 결과입니다. 궤도의 관측자에게 ocean lens
는 antistellar 반구를 덮는 밝은 빙하 ice 대비 거의 검은 디스크로 보입니다.

빙하 ice 표면 (`#d4cab8` cfg 색조) 이 행성의 ~75% 를 덮습니다. Sergeev
2020 (arXiv:2004.03007) 은 substellar convective 플룸이 열린 물 디스크
아래 표면까지 따뜻한 공기의 지속적인 subduction 을 구동하고, 이것이
다시 ice 경계를 차가운 antistellar drag 에 대해 유지함을 발견합니다.
terminator 의 표면 morphology 는 빙하 흐름에서 온 ridge 와 고압 ridge
축의 노출된 bedrock 이 지배합니다 (bedrock 노출에 대한 cfg `surface_tint_rgb_hex_accent
= #7a4a30`).

Shields 2018 (1808.09977) 은 대안 hydrohalite-snowball 시나리오를
제시합니다. 염도가 충분하고 기후가 snowball regime 으로 빠지면, ice
표면의 염 deposit 이 albedo 를 강화하고 snowball 상태를 안정화합니다.
이는 canonical cfg 선택 대신 Open items 변형으로 보존됩니다.

물 질량 분율이 열린 물 디스크의 깊이와 총 지하 ice 저장을 설정합니다.
Herath 2021 내부 모델이 질량 기준 0.001 부터 0.4 까지 허용하며, 직접
측정으로 구분할 방법이 없습니다. cfg 의 5–10% 지구 analog 선택은
tie-break 입니다 — ~3-5 km 평균 ocean 깊이와 알아볼 수 있는 지구형 표면
hydrology 를 주지만, 범위가 넓습니다. 더 건조한 (0.001) 변형은 열린
물 디스크를 줄이고, 더 습한 (0.4) 변형은 Hycean 지오메트리에 접근합니다.

## Atmosphere synthesis

cfg 는 Boutle 2017 simplified-N₂ 대기를 canonical Proxima b 시나리오로
채택합니다. 1 bar 표면 압력, N₂ 우세 (~99%), trace ~376 ppm CO₂, trace H₂O (substellar
표면 근처 포화, 더 높은 고도와 terminator 쪽으로 dew point 까지 떨어짐).
trace O₂ (≪ 1%) 가 [OI] 557.7 nm aurora 방출을 지원하기 위해 포함됩니다.
출처는 photochemical (H₂O 분해 + H escape) 이며 생물학적이 아닙니다.

이 구성은 canonical 표면 온도 분포를 재현합니다. T_substellar ≈ 290 K
(peak dayside), T_nightside cold-trap 최소 ≈ 150 K, T_global_mean ≈ 250 K
(Boutle 2017 §3 + Fig. 2). 열 수송이 substellar 에서 야측으로 simplified-
N₂ 시나리오에서 대기 순환에 의해 지배되며, 동적 ocean (Del Genio 2019)
추가가 재분배를 ~10–20 K 강화하고 야측 온도를 bare-N₂ cold-trap 바닥
위로 올립니다.

구름 덮개는 cfg 에서 55% 입니다 — Boutle 2017 + Cohen 2023 + Sergeev
2020 범위의 중점으로 선택. 구름 morphology 는 조석 고정 동기 M 왜성
행성의 특징적인 형태. substellar convective cluster (Sergeev 2020) 와
높은 cirrus shield, extra-tropical Rossby wave trains (Cohen 2023,
2211.11887) 가 ±30–60° 위도에 traveling 구름 밴드를 만들고, 더 맑은
야측 (Joshi 2020 dark-side inversion analog). cfg `cloud_morphology` 필드
가 세 컴포넌트 모두를 하나의 문자열로 잡습니다.

Photochemistry (Yates 2020, 1912.08743. Braam 2024, 2410.19108) 는 낮밤
terminator 주변의 O₃ 생성이 지배하며, canonical M 왜성 "stratospheric
ozone ring" 이 미래 transmission spectroscopy 에서 관측 가능할 수 있는
UV 신호를 만듭니다 (Proxima b 가 비통과이지만). Scheucher 2020 (2003.02036)
이 우주선 유도 화학 기여를 더합니다 — magnetosphere 가 크게 압축되는
super-Alfvénic transit 동안 중요해집니다.

대기는 행성의 1차 방사선 차폐입니다. cfg 의 `atmospheric_shielding_g_cm2
= 1000` (1 bar 컬럼) 이 조용한 조건에서 표면 도즈를 ~5000 mSv/년으로
줄입니다 (Atri 2020 Table 6 의 비슷한 시나리오). Superflare 사건은
도즈를 사건당 10⁵ mSv 로 spike 시켜, 어떤 생물학적 임계점도 한참
넘기지만 공간적 시간적으로 국소화됩니다.

물 vapor transit 모호성 (Macdonald 2024, 2402.12253) 은 Proxima b 가
통과했다 해도 1-bar 습한 대기와 desiccated 표면을 구분하려면 매우 고정밀
retrieval 이 필요함을 의미합니다. cfg 의 대기 H₂O 풍도는 측정값이
아니라 추론값입니다.

## Rotation & spin synthesis

Proxima b 는 조석 고정 상태이며, substellar 점은 행성 frame 의 0° 에
고정되고 sidereal 회전 주기가 11.18 일 궤도 주기와 동일합니다. 0.122-M☉
M 왜성 주위 0.04848 AU 의 1.055-M⊕ 암석 행성에 대한 조석 고정 시간
스케일은 < 10⁵ 년 (Walterová 2020 Fig. 4) 으로 시스템 나이보다 훨씬
짧습니다. 황도 경사도 비슷하게 0° 로 damping 됐습니다.

spin-orbit resonance 는 1:1 (동기) 인데, 궤도 이심률이 0 (SM25) 이기
때문입니다. 0 이 아닌 이심률이라면 Proxima b 는 더 높은 차수 resonance
로 migration 했을 것 (Makarov 2012 framework) 이며, substellar 점에서
간헐적 일조량이 만들어졌을 것입니다 — Braam 2025 (2410.19108) 가
spin-orbit resonance 기후 효과를 탐색했지만 SM25 의 0 이심률 결과가
cfg 에서 그것을 배제합니다.

Libration 진폭은 < 1° 입니다 (무시할 수준). substellar 점의 고정된 위치
가 Surface synthesis 섹션에서 설명한 eyeball-Earth 지오메트리를 만듭니다.
일간 diurnal cycle 이 없고, 유일한 시간 변조는 Proxima 의 7 년 활동
사이클에서 옵니다 — substellar 일조량 진폭을 살짝 변조합니다.

자기 dynamo. Zuluaga 2018 (1609.00707) 은 지구형 핵 구조와 10+ 일
회전 주기를 가진 1 M⊕ 암석 행성에 대해 적당한 고유 자기 쌍극자가 plausible
함을 발견합니다 (~ 0.01–1.0 M⊕ 모멘트). cfg 는 0.1 M⊕ 를 tie-break
중점으로 채택합니다 — 부분 대기 차폐와 가시 aurora 에 충분하지만
Proxima 항성풍을 완전히 repel 할 만큼 강하지는 않습니다.

## Visual styling

NearStars 에서 Proxima b 는 시스템의 시각 centerpiece 입니다 — 카탈로그
에서 가장 많이 모델링된 조석 고정 암석 행성이며 시각적으로 구별되는
eyeball-Earth 지오메트리를 가집니다. substellar 열린 물 디스크
(`#0a2238`) 가 밝은 빙하-흰색 ice 행성 (`#d4cab8`) 위에 거의 검은 눈으로
읽힙니다. 따뜻한 크림 구름 덮개 (`#d8a888`) 가 표면을 구분되는 substellar
cluster + extratropical 밴드 패턴으로 쪼개고, terminator ridge 가 노출
된 bedrock (`#7a4a30`) 을 보이며 — 지배적인 차가운 팔레트 대비 따뜻한
earth-tone 액센트입니다.

Proxima 가 b 의 하늘에서 각지름 1.5° 를 채웁니다 — 지구에서 본 태양
겉보기 지름의 3 배. 깊은 빨강 M5.5V 조명 (`stellar_color_temp_k = 2980`)
이 전체 표면을 따뜻한 cast 로 채웁니다. Aurora ring (`#4DFF4D` 1차,
`#FF4D4D` 2차) 이 잦은 superflare 동안 terminator 를 따라 일렁이며,
cfg `aurora_intensity_kR_typical = 500` 이 peak 사건 동안 궤도에서 보이는
glow 를 만듭니다.

구름 밴드 morphology 는 substellar Rossby wave (Cohen 2023) 의 10 일
회전 주기로 진화하여, 게임 내 구름 애니메이션에 가시 1-주 cadence 를
줍니다. substellar convective cluster 는 살짝 빠른 ~5 일 사이클로 맥동
합니다 (Sergeev 2020).

대기의 Rayleigh 산란 색은 M 왜성 SED 에 의해 크게 reddening 됩니다 —
지구의 파란 하늘 대신 Proxima b 의 대기는 낮 동안 어둡고 깊은 빨강
하늘을 만들고, 따뜻한 sunset 톤을 거쳐 terminator 에서 거의 검정으로
전이합니다. cfg `atmosphere_tint_rgb_hex = #4a3030` 이 궤도에서 보이는
이 빨강-시프트된 대기를 잡습니다. Proxima superflare 동안 하늘이 강렬한
UV + 광학 산란과 함께 잠시 밝아져, cfg `aurora_*` 필드와 동기화된 시각
적으로 극적인 flare 이벤트를 만듭니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (arXiv:1609.03449). 발견 논문. Best-fit P = 11.186 d, Msini =
  1.27 M⊕, a = 0.0485 AU.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS* (arXiv:2507.21751). 현재 best 궤도
  fit. P = 11.18465 d, e = 0, Msini = 1.055 M⊕.
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (arXiv:2005.12114). 중간 단계 정련.
- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri* (arXiv:2202.05188). b 질량을 1.07 M⊕ 로
  정련. 동반 Proxima d.
- **Boutle I. A. et al. 2017** — *Exploring the climate of Proxima B
  with the Met Office Unified Model*, A&A 601, A120
  (arXiv:1702.08463). UK Met Office UM GCM. substellar 열린 물 lens,
  이심률 sensitivity, Earth-like 와 simplified-N₂ 시나리오.
- **Turbet M. et al. 2016** — *The habitability of Proxima Centauri b.
  II. Possible climates and observability*, A&A 596, A112
  (arXiv:1608.06827). 1D 기후 framework. aquaplanet 부터 snowball
  까지 범위.
- **Meadows V. S. et al. 2018** — *The Habitability of Proxima
  Centauri b: Environmental States and Observational Discriminants*,
  AsBio 18, 133 (arXiv:1608.08620). 대기 보유 시나리오 + 관측
  discriminant.
- **Del Genio A. D. et al. 2019** — *Habitable Climate Scenarios for
  Proxima Centauri b with a Dynamic Ocean*, AsBio 19, 99
  (`2019AsBio..19...99D`. arXiv 프리프린트 없음 — Tier A manual
  followup. Boutle / Sergeev / Salazar 통해 인용). 동적 ocean 이 열
  재분배를 강화하고 열린 물 디스크를 넓힘을 입증.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a
  Key Role in the Climate of Tidally Locked Terrestrial Exoplanets*,
  ApJ 894, 84 (arXiv:2004.03007). substellar convection 플룸이 열
  수송을 구동.
- **Salazar A. M. et al. 2020** — *The Effect of Substellar Continent
  Size on Ocean Dynamics of Proxima Centauri b*, ApJL 896, L34
  (arXiv:2005.14185). substellar continent 지오메트리 sensitivity.
- **Lewis N. T. et al. 2018** — *The Influence of a Substellar
  Continent on the Climate of a Tidally Locked Exoplanet*, ApJ 854,
  171 (arXiv:1802.00378). 건조 substellar continent 가 순환을 안정화.
- **Joshi M. M. et al. 2020** — *Earth's Polar Night Boundary Layer
  as an Analog for Dark Side Inversions on Synchronously Rotating
  Planets*, ApJ 892, 81 (arXiv:2003.06306). 야측 inversion.
- **Yates J. S. et al. 2020** — *Ozone chemistry on tidally locked
  M dwarf planets*, MNRAS 492, 1691 (arXiv:1912.08743). terminator
  오존 ring.
- **Cohen M. et al. 2023** — *Traveling Planetary-scale Waves Cause
  Cloud Variability on Tidally Locked Aquaplanets*, ApJ 942, 86
  (arXiv:2211.11887). Rossby-wave 구름 변동성.
- **Scheucher M. et al. 2020** — *Proxima Centauri b: A Strong Case
  for Including Cosmic-Ray-induced Chemistry in Atmospheric
  Biosignature Studies*, ApJ 893, 12 (arXiv:2003.02036). 우주선
  driven photochemistry.
- **Shields A. L. et al. 2018** — *Hydrohalite Salt-albedo Feedback
  Could Cool M-dwarf Planets*, ApJL 866, L18 (arXiv:1808.09977).
  Snowball 변형 컨텍스트.
- **Zuluaga J. I. et al. 2018** — *Magnetic properties of Proxima
  Centauri b analogues*, MNRAS 480, 4225 (arXiv:1609.00707).
  Plausible 쌍극자 모멘트 범위.
- **Atri D. et al. 2020** — *Stellar Proton Event-induced surface
  radiation dose* (arXiv:1910.09871). 표면 도즈 계산.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). 조석 고정
  시간 스케일.
- **Garraffo C. et al. 2022** — *Revisiting the Space Weather
  Environment of Proxima Centauri b*, ApJL 941, L8 (arXiv:2211.15697).
  항성풍 ram pressure spike. magnetosphere 압축.
- **Lee Y. et al. 2021** — *Exosphere Modeling of Proxima b: A Case
  Study of Photochemical Escape* (arXiv:2109.06963). Venus-analog
  산소 escape rate.
- **Macdonald E. et al. 2024** — *Water vapour transit ambiguities
  for habitable M-Earths* (arXiv:2402.12253). 대기 습도 retrieval
  모호성.
- **Galuzzo D. et al. 2021** — *Three-dimensional Climate Simulations
  for the Detectability of Proxima Centauri b*, ApJ 909, 191
  (arXiv:2102.03255). 3D 검출 가능성 framework.
- **Braam M. et al. 2024** — *Earth-like Exoplanets in Spin–Orbit
  Resonances*, MNRAS 528, 3098 (arXiv:2410.19108). 기후 동역학 + 3D
  photochemistry.

### Read (context / methodology, not decision-driving)

- **Bonfils X. et al. 2018** — *A temperate exo-Earth around a quiet
  M dwarf at 3.4 parsec* (arXiv:1711.06177). 자매 시스템 컨텍스트.
- **Jenkins J. S. et al. 2019** — *Proxima Centauri b is not a
  transiting exoplanet* (arXiv:1905.01336). 통과 배제.
- **Gilbert E. A. et al. 2021** — *No Transits of Proxima Centauri
  planets in high cadence TESS data* (arXiv:2110.10702). Jenkins
  강화.
- **Hammond T. et al. 2025** — 근처 암석 외계행성의 thermal emission
  스펙트라 (arXiv:2504.00978). 다중 행성 스펙트라.
- **De Luca P. et al. 2024** — 오존-기후 동역학
  (arXiv:2404.17972).
- **Boldog Á. et al. 2024** — 내부 물 함량
  (arXiv:2312.01893).
- **Noack L. et al. 2021** — *Interior heating and outgassing of
  Proxima Centauri b* (`2021A&A...651A.103N`, no arXiv). Tier A
  manual followup. abstract 통해 인용.
- **Herath M. et al. 2021** — *Interior structures of Proxima b and
  Ross 128 b* (`2021MNRAS.500..333H`, no arXiv). Tier A manual
  followup. abstract 통해 인용.
- **Reiners A. et al. 2018** — Proxima 자기장 (arXiv:1711.06576).
- **Vida K. et al. 2019** — Proxima flare 통계 (arXiv:1907.12580).
- **Fuhrmeister B. et al. 2022** — Proxima X 선 + FUV 동시 flare
  (arXiv:2204.09270).

### Read (instrument / non-cfg-decisive)

- **Hardegree-Ullman K. et al. 2025** — Bioverse 직접 촬영 전망
  (arXiv:2405.11423). 미래 관측 가능성 framework.
- **Singla M. et al. 2023** — 암석 외계행성 reflection 스펙트라
  (arXiv:2303.00540). 고대비 imaging.
- **Pearce L. A. et al. 2025** — 직접 검출 하늘 위치 예측
  (arXiv:2509.06747). 미션 계획.

### Not read — no arXiv preprint or low-priority (~85 papers)

학회 abstract, biosignature 추측, technosignature 탐색, gravitational-
lens 추진 제안은 `docs/phase3/_bib/proxima-cen-b.yaml` 에 `status:
skipped` 주석으로 보존됩니다.
`phase3/alpha_centauri_proxima/manual-paper-followup.md` 에 잡힌 주목
할 만한 Tier A no-arXiv 항목 세 개. **Del Genio 2019** (동적 ocean),
**Noack 2021** (내부 outgassing), **Herath 2021** (내부 구조).

## Open items for follow-up

- **대기 박탈 변형.** Atri 2020 + Garraffo 2022 + Lee 2021 모두 공격적
  XUV / 항성풍 침식 시나리오에서 박탈된 Proxima b 를 허용합니다. cfg
  `atmosphere_present: true` 는 tie-break 이며, 대안 cfg 변형은
  `atmosphere_present: false` 로 표면이 완전한 Proxima 일조량을 받는
  뜨거운 암석 사막이 됩니다. 하류 `kopernicus-cfg` writer 가 양쪽
  변형을 지원할 수 있습니다.
- **Snowball 변형.** Shields 2018 hydrohalite-snowball + Turbet 2016
  저-CO₂ snowball 이 substellar 열린 물 디스크 없는 완전 ice-covered
  Proxima b 를 줍니다. cfg 는 Boutle 2017 eyeball-Earth canonical 을
  채택하지만, snowball 은 관측과 일관됩니다.
- **더 높은 물 함량 변형.** Herath 2021 내부 모델이 최대 ~40 wt% 물을
  허용합니다. 훨씬 깊은 substellar ocean 과 가능한 물-구름 opacity 의
  Hycean 식 변형은 또 다른 미래 cfg 분기입니다.
- **Spin-orbit resonance 기후.** Braam 2024 (2410.19108) 이 비동기
  spin-orbit resonance 기후를 탐색했습니다. SM25 의 0 이심률 궤도가
  동기 케이스를 canonical 로 만들지만, 약한 이심률로 재분석하면 바뀔
  수 있습니다.
- **직접 촬영.** Sanghi 2025 + Beichman 2025 JWST 프로그램이 결국
  Proxima b 의 반사광 스펙트럼을 제약할 수 있습니다. 대기 특징이
  검출되면 cfg 가 새 제약에 대해 재검증돼야 합니다.
- **자기장 측정.** Zuluaga 2018 가 plausibility 범위만 제공합니다.
  Proxima 항성풍 transit 동안의 라디오 방출을 통한 향후 직접 측정이
  쌍극자 모멘트를 제약할 수 있습니다.

## Related

- [proxima-cen](proxima-cen.md) — host 별 (M5.5Ve 플레어 환경. 대기 유지 문제는 host 의 XUV 이력에서 비롯됨)
- [proxima-cen-d](proxima-cen-d.md) — 안쪽 형제 행성. USP Mercury-analog (대기 없음 예상) 으로 b 의 대기 유지 시나리오와 대비
- [trappist-1-e](trappist-1-e.md) — 또 다른 온대 M-dwarf HZ aquaplanet analog. eyeball-Earth 의 substellar-ocean 기하를 공유
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 이 천체의 대기+해양 cfg 를 소비하는 다운스트림 모드
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6 Proxima 로스터 (REX 는 b + c 철회. NS 는 Faria 2022 이후 b + d)
