<!-- TRAPPIST-1 e Phase 3 합성: cfg-ready 결정과 근거 -->
# TRAPPIST-1 e — Phase 3 Synthesis

TRAPPIST-1 e 는 M8V ultra-cool dwarf 를 6.10 일 주기로 도는 0.92 R⊕, 0.69
M⊕ 의 암석 행성입니다. 안쪽에서 네 번째 행성이며 지구 일조량의 0.66배를
받아 보수적 거주 가능 영역 한가운데에 자리잡고 있고, TRAPPIST-1 시스템
전체를 통틀어 **거주 가능성이 가장 높은 단일 세계**로 꼽힙니다 (Wolf
2017, Turbet 2018, Lincowski 2018, Way 2025). 최근 JWST NIRSpec PRISM
transmission 스펙트럼 (Glidden et al. 2025 DREAMS, 4회 방문) 은 상당한
stellar contamination 에 시달리지만, 그럼에도 H₂-rich 대기를 배제하고
Venus 형 CO₂-rich 대기를 2σ 수준에서 약하게 disfavor 합니다. 미량의
CO₂ 와 CH₄ 를 동반한 N₂-rich 대기는 완전히 허용되며, 맨 암석 해석도
관측과 모순되지 않습니다.

**NearStars 시나리오 선택. 1 bar N₂/CO₂/H₂O 대기를 가진 온대
aquaplanet 으로, 해양을 보유하고 substellar 지점 부근에 열린 물,
terminator 와 nightside 에 얼음을 가진 조석 고정 "안구(eyeball)"
geometry 입니다.** 이것이 canonical "최선의 거주 가능 후보" cfg 변형이며,
(여전히 관측과 양립 가능한) 여러 옵션 가운데 Wolf 2017 / Turbet 2018 /
Way 2025 의 aquaplanet 시나리오를 채택했습니다. 대안인 맨 암석 해석은
백업 cfg 변형으로 남겨둡니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence`. high = 직접
측정되었거나 강하게 제약된 값, medium = 강한 지지를 받는 이론값, low =
허용 윈도우 안에서의 미적 선택입니다.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 6.10 d 궤도와 조석 damping. Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping. Agol 2021 |
| `eccentricity` | 0.00510 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 108 | medium | Agol 2021 (low ecc 라 제약이 약함) |
| `sidereal_period_days` | 6.1010 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02925 | high | Agol 2021 |
| `mass_mearth` | 0.692 | high | Agol 2021 TTV |
| `radius_rearth` | 0.920 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.818 | high | derived = 0.692 / 0.920² |
| `density_g_cc` | 4.92 | high | Agol 2021 (지구보다 낮아 water-rich 내부 시사) |
| `water_mass_fraction` | 0.05–0.10 | medium | Agol 2021 + Acuña 2021 — 낮은 질량과 낮은 밀도가 수 wt% H₂O 와 일관됨 |
| `insolation_s_earth` | 0.66 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 251 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 230 | high | derived; 지구형 albedo 가정 |
| `bond_albedo` | 0.30 | medium | 지구 값 + Hapi 2024 aqua-planet GCM 범위 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Wolf 2017 GCM Aquaplanet, Turbet 2018 §4 |
| `surface_temp_nightside_k` | 230 | medium | Wolf 2017 GCM, 얼음으로 덮인 nightside |
| `surface_temp_global_mean_k` | 270 | medium | Wolf 2017 GCM Aquaplanet |
| `atmosphere_present` | true | high | 채택한 시나리오, Glidden 2025 와 일관 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | 1 bar 의 canonical 지구형. Glidden 2025 가 미량 CO₂ 를 가진 N₂-rich 를 허용 |
| `atmosphere_composition` | N₂ 78%, O₂ ~5% (낮음, abiotic), CO₂ ~1%, H₂O 0.1–1%, Ar 0.5% | medium | Wolf 2017, Lincowski 2018 aquaplanet 평형. outer-HZ 온실 가열을 위해 지구보다 CO₂ 가 높음 |
| `atmosphere_scale_height_km` | 9.5 | medium | derived. kT/μg with T≈270 K, μ=29, g=8.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a7090` (M-dwarf 적색 이동을 동반한 muted blue) | medium | 2566 K 조명 아래의 Rayleigh-blue 가 dim cyan-gray 쪽으로 강하게 적색 이동 |
| `cloud_cover_fraction` | 0.55 | medium | Wolf 2017 GCM Aquaplanet 의 stratocumulus + cirrus (Cohen 2022 UM 은 60%). THAI II 4-GCM intercomparison (Sergeev 2022) 은 LMD-G / ExoCAM / UM / ROCKE-3D 사이에서 10–77% 의 분산을 보이는데 0.55 는 그 중간값. 신뢰도는 high 에서 한 단계 내림 |
| `subsurface_ocean_probability` | 0.876 | medium | Boldog 2023 ([2312.01893](https://arxiv.org/abs/2312.01893)) — HZ 최상위 등급 |
| `cloud_morphology` | 이중 중위도 밴드 + substellar 의 준정상 클러스터 | medium | Cohen 2022 UM 과 Wolf 2017 ROCKE-3D 가 이중 중위도 jet regime 을 도출. THAI II 는 e 가 적도 superrotation (Hab 1 에서 4개 중 3개 GCM) 과 중위도 (ROCKE-3D 그리고 특정 설정의 UM) 사이의 tipping point 에 위치한다고 보여줌. 이중 밴드 cfg 선택은 동등하게 지지되는 두 결과 중 하나 |
| `cloud_tint_rgb_hex` | `#c0a890` (warm cream, 적색 이동된 물 구름) | medium | 물 구름 + 2566 K 조명 → warm cream-orange |
| `ocean_present` | true (substellar 의 열린 물 disk, 그 외에는 얼음) | medium | Turbet 2018 aquaplanet, Pierrehumbert 2011 "eyeball Earth" morphology |
| `ocean_extent_substellar_radius_deg` | 35 | medium | Wolf 2017 Aquaplanet — substellar 지점에서 ~35° 이내가 열린 해양 |
| `ocean_tint_rgb_hex` | `#1a2540` (낮은 M-dwarf 일조량 아래 어두운 navy) | low | 깊은 해양 + 흐릿한 적색 별 → 어두운 blue-violet |
| `surface_ice_caps` | substellar 열린 물 disk 바깥 전 영역, 표면의 약 60% | medium | Wolf 2017 Aquaplanet 의 ice line 이 substellar 에서 ~35° |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-dwarf 빛 아래의 snow / sea ice) | medium | 물 얼음 albedo 0.6–0.8 + 적색 이동 조명 |
| `surface_tint_rgb_hex_accent` | `#7a6a58` (terminator 의 ridge 정상에 노출된 기반암) | low | 얇은 대기 + 얼음 흐름 geometry |
| `surface_morphology` | substellar 의 ~35° 이내 해양, 그 외에는 sea-ice + 빙하 지형, 얼음 경계에 침수 + 노출 지형 | medium | Hu 2014 / Pierrehumbert 2011 조석 고정 aquaplanet 템플릿 |
| `magnetic_field_present` | true (modest, 지구의 ~0.1배) | low | 작은 질량 + 느린 자전 → 약한 고유 자기장. 직접 제약은 없음 |
| `induction_heating_w_m2` | 0.01–0.1 | medium | Grayver 2022 — b/c 보다 e 에서 훨씬 낮음 |
| `tidal_heating_w_m2` | 0.13–0.51 | medium | Bolmont et al. 2026 (`2601.03408`) Table 3 — degree-2 Love number k₂ + 내부 구조 (핵 크기) + Agol 2021 이심률을 이용한 재유도. 보수적 최소값으로 핵 크기 전 범위에서 0.13–0.51 W/m² (불확실성까지 포함하면 ~1.4 까지). e 는 조석 가열이 지배적이며 지구 지열 flux 의 ~1.5–6배 → "화산 활동이나 판 구조 운동과 양립 가능" (그들의 §5). 같은 저자의 Bolmont 2020 "e 에서 최소" (0.001–0.01) 를 대체 |
| `magnetic_field_strength_microtesla_equator` | 30 | medium | Wang 2025 ([2504.16662](https://arxiv.org/abs/2504.16662)) 의 e MHD 시뮬레이션이 0.32 G ≈ 지구 강도를 채택. Garraffo 2017 테스트 케이스도 0.3 G. Documented divergence — 아래 Canonical alternatives 참조. RM22 다이나모 스케일링은 조석 고정 저질량 행성에 약 2 μT 를 도출하나, cfg 는 시각적 자기권을 위해 Wang 의 지구 수준 가정을 채택합니다. |
| `magnetic_dipole_moment_normalized_earth` | 0.3 | medium | Wang 2025 의 지구형 가정. 거주 가능 시나리오 렌더링에서 보수적인 값 |
| `magnetic_dipole_tilt_deg` | 11 | medium | 지구형 11° (Wang 2025 는 23.5° 를 사용하지만 tilt 민감도를 함께 보고). 타이브레이크. 11° 가 플레이어에게 인식 가능한 오로라 geometry 를 제공 |
| `magnetosphere_standoff_planet_radii` | 5 | high | Wang 2025 Fig. 5, 0.32 G 자기장 — 평온기 5–9 R_e, CME 교란 시 ~3 R_e |
| `radiation_belt_present` | true | medium | B-field ≥ 지구의 0.1 + 평온기 폐쇄 자기권 — Van Allen 같은 방사선 벨트가 가능하지만, sub-Alfvénic transit 동안에는 크게 교란됨 |
| `surface_radiation_dose_msv_yr` | ~120 (10²–10³ 차수. SPE 빈도 의존) | low | Atri 2019 ([1910.09871](https://arxiv.org/abs/1910.09871)). 강한 스펙트럼 SPE 1회가 1 bar + 지구형 B-field 에서 표면에 ~3.9 mGy 침착 (Table 4, 1000 g/cm². GCR 배경의 ≈2200배, Table 6). 연간 dose = 이벤트당 × 플레어 빈도이며, 이 빈도는 이제 Vasilyev et al. 2026 (`2605.05468`, JWST+K2 플레어 빈도 분포) 이 정량화함. 단일 거듭제곱 법칙 β = 0.753, E_TESS > 10³² erg 플레어가 ~25 일마다 1회 (이전 추정 대비 ~10배 잦음). 이 빈도에서 ~120 mSv/yr, 정직한 범위는 여전히 10²–10³ 차수. 기존 12000 은 Table 6 의 무차원 GCR-enhancement factor 를 연간 mSv 로 오표기한 값 |
| `atmospheric_shielding_g_cm2` | 1000 | high | Phase 3 cfg 압력 1 bar 지구형 → ~1000 g/cm² column |
| `aurora_present` | true | high | 대기와 자기장이 모두 충분. Fraschetti 2019 ([1902.03732](https://arxiv.org/abs/1902.03732)) 양성자 flux 가 지구의 10⁶배 → 강렬한 precipitation |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | N₂/CO₂/O₂ 대기에서 [OI] 557.7 nm 녹색이 지배 — 지구형 오로라 색. interesting-first 타이브레이크에서 UV-only 대안 대신 녹색 선택 |
| `aurora_color_secondary_hex` | `#FF4D4D` | medium | CO₂⁺ Fox–Duffendack–Barker 밴드 (580–700 nm 적-오렌지) + N₂⁺ Meinel 밴드. 타이브레이크. 가시 팔레트 다양성을 강화 |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + N₂⁺ 391.4 nm First Negative + CO₂⁺ doublet` | medium | 대기 조성 + 표준 오로라 화학 |
| `aurora_oval_magnetic_latitude_deg` | 50 | medium | Wang 2025 standoff 5 R_p, Vidotto 2013 식 7 → α ≈ 27°, 평온기 oval lat ~63°. sub-Alfvénic transit 동안 ~50° 까지 확장 허용 |
| `aurora_intensity_kR_typical` | 150 | medium | Fraschetti 2019 의 양성자 flux 가 지구의 최대 6 자릿수 위 → 오로라가 지구 평균 10 kR 의 15배 (보수적 중간값) |
| `star_apparent_angular_diameter_deg` | 2.17 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 e 는 시스템에서 거주 가능성이 가장 높은 세계입니다. 세
가지 증거선이 한 점으로 수렴합니다.

1. **일조량** (0.66 S⊕) 은 온실 가열을 동반한 어떤 합리적 대기에
   대해서도 보수적 거주 가능 영역 (Kopparapu 2013 / 2014) 안에
   위치합니다. 대기가 없으면 e 는 얼어붙고, 1 bar N₂/CO₂ 면 표면
   액체 물을 유지합니다 (Wolf 2017, Turbet 2018 §4).

2. **밀도** (Agol 2021 의 4.92 g/cc) 는 지구의 5.51 g/cc 보다 낮아
   non-trivial 한 물 질량 분율과 양립합니다. 마그마 바다 모델링
   (Bourgeois et al. 2024 — [2008.09599](https://arxiv.org/abs/2008.09599)) 은 e 의 물 질량 분율을
   0–0.23 범위로 제시하며 중심 추정값은 0.05–0.10 수준입니다 (질량
   기준 수 퍼센트는 지구 해양 분량의 수 배에 해당).

3. **관측 일관성.** Glidden 2025 (DREAMS) 는 H₂-rich 를 배제하고
   Venus 형 대기를 약하게 disfavor 하지만, 미량 CO₂ 와 CH₄ 를 가진
   N₂-rich 대기는 명시적으로 허용합니다 — 정확히 canonical 한
   지구형 2차 대기입니다.

표면 morphology 의 경우, 조석 고정 aquaplanet 템플릿 (Pierrehumbert
2011, Hu & Yang 2014, Wolf 2017) 이 독특한 "eyeball Earth" 패턴을
제시합니다.

- **Substellar disk** (substellar 지점에서 ≲35°). 열린 해양이며
  액체 물을 유지할 만큼 따뜻합니다 (Wolf 2017 Aquaplanet 시나리오의
  substellar 표면 온도 ~290 K). cirrus 구름이 동반될 수 있습니다.
- **중위도 / 중경도** (substellar 에서 35–90°). sea ice 가 자리잡고,
  두께는 ice line 의 수 m 에서 terminator 부근의 수백 m 까지
  변합니다.
- **Terminator 와 nightside** (substellar 에서 >90°). 얼어붙은 해양
  위 두꺼운 빙하 얼음 (>1 km) 이 덮고 있으며, 얼음이 tectonic
  feature 주변에서 갈라진 ridge 정상에는 노출 지형이 가능합니다.

**색 선택.** 두 가지 효과가 맞붙습니다. (a) 본래 얼음/눈 albedo 는
높고 (0.6–0.8) 푸르스름한 흰색이지만, (b) 2566 K M-dwarf 조명이 인지
hue 를 적-오렌지 쪽으로 강하게 끌어당깁니다. 결과적으로 얼음 표면은
warm cream-white (`#d8d0c4`), 깊은 해양은 어두운 navy-violet (`#1a2540`)
로 잡힙니다. Hu 2014 도 명시적으로 지적했듯, M-dwarf 주위 aquaplanet
은 stellar SED 가 Rayleigh-scatter 할 단파장 flux 를 거의 갖지 않기
때문에 지구보다 "덜 푸르게" 보입니다.

**산화철 / 기반암.** 노출은 제한적입니다 — 표면 대부분이 얼음으로
덮여 있기 때문입니다. 기반암 외관은 빙하 흐름이 얼음을 얇게 만든
terminator 부근 ridge 정상에 국한됩니다. accent `#7a6a58` 은 M-dwarf
빛 아래의 muted weathered-basalt 톤입니다.

**조석 고정 하의 morphology.** Substellar disk 가 활발한 수문학적
순환의 무대가 됩니다 — 표면 가열이 증발을 일으키고, polar / nightside
cold-trap 에서 응결이 영구 빙하를 형성하며, 빙하 흐름이 다시 물을
substellar disk 쪽으로 되돌립니다. 이 패턴은 지질학적 시간 척도에서
안정적이어서 (Wolf 2017 §6) 계절 사이클 대신 영구적인 기후 영역을
가진 행성을 만들어냅니다.

## Atmosphere synthesis

Glidden 2025 (DREAMS NIRSpec PRISM, 4 transit) 는 e 의 첫 JWST
transmission 스펙트럼을 제시합니다. 0.6–5 μm 전반에 걸친 상당한
stellar contamination 이 추론을 복잡하게 만들지만, Gaussian process 로
stellar feature 를 marginalize 한 결과 다음을 확인했습니다.

- H₂-rich (부피로 ≳80%) 구름 동반 대기는 >3σ 에서 배제
- Venus 형 CO₂-rich 대기는 2σ 에서 약하게 disfavor
- 미량 CO₂ 와 CH₄ 를 가진 N₂-rich 대기는 **완전히 허용**
- 맨 암석 해석도 적합하지만 설명되지 않은 feature 가 남음

이는 Wolf 2017 / Lincowski 2018 / Way 2025 모델링이 기대하는 지구형
2차 대기와 부합하며 — 오히려 그것을 뒷받침합니다.

NearStars 에서는 **1 bar N₂-rich aquaplanet 대기**를 채택합니다.

- **압력** 1 bar (100 kPa) — 지구형 값으로, Glidden 2025 N₂-rich 일관성 윈도우 안에 여유 있게 들어갑니다.
- **조성** N₂ 78%, Ar 0.5%, CO₂ 1% (outer-HZ 온실 가열을 위해 지구의 0.04% 보다 올림 — Wolf 2017 은 거주 가능 표면 유지에 1–10× CO₂ 증대가 필요하다고 보고. THAI II Hab 1 은 CO₂ 400 ppm 만으로 전역 평균 232–246 K 를 보이는데, 이는 더 따뜻한 Hab 2 의 1 bar CO₂ 시나리오보다 약 25 K 차가운 값. cfg 의 1% CO₂ 선택은 Hab 1 과 Hab 2 사이에 위치), H₂O 0.1–1% (substellar 표면 부근은 포화), O₂ ~5% (abiotic 광분해).
- **구름.** THAI II 4-GCM intercomparison 은 Hab 1 에 대해 10–77% 의 구름 커버를 제시하고, cfg 의 0.55 분율은 그 중간값입니다. ROCKE-3D 의 high-cloud 끝단은 따뜻한 온대 시나리오에 더 잘 맞을 수 있고, LMD-G 의 low-cloud 끝단은 더 차갑고 건조한 변형과 일관됩니다.

**하늘 외관.** 1 bar N₂ 대기는 단파장에서 지구형 Rayleigh scattering
을 보이지만, 2566 K stellar SED 는 0.5 μm 아래에서 flux 가 거의
없습니다 — 따라서 산란된 하늘 색은 지구의 푸름에 비해 훨씬 어둡고
오렌지 쪽으로 이동합니다. 천정 하늘은 dim 한 red-blue 혼합
(~`#3a4060`) 이고 horizon 으로 갈수록 warm orange (`#a07050`) 로
전환됩니다. 물 구름 feature 는 적색 stellar light 를 받는 warm cream
패치 (`#c0a890`) 로 나타납니다.

호스트 별이 각 크기 2.17° 로 낮 하늘을 지배합니다 (지구에서 본 태양
각 크기의 약 4배). substellar 지점의 표면 조명은 지구의 약 0.66배로
짙게 흐린 지구의 하루와 비슷하지만, spectral peak 이 적색 / 근적외선
쪽으로 확실히 밀려 있습니다.

**Nightside.** 직접적인 stellar 조명은 없습니다. 광원은 (a) 대기 순환
을 통해 dayside 에서 운반된 산란광 (무시 가능), (b) 자매 행성에서
반사된 빛 (합 시 f 와 d 가 각 크기 ~0.4–0.5°, mv ≈ −10 ~ −13), (c)
멀리 있는 별빛 (부재한 태양 때문에 대기 산란이 없어 잘 보임) 정도가
전부입니다. nightside 하늘은 극적으로 어두워서 — KSP 의 nightside
ambient 는 dayside 의 약 1% 수준으로 두어야 합니다.

**행성을 정의하는 비주얼로서의 오로라.** 1 bar 대기와 여기서 채택한 지구형 자기장 (Wang 2025) 이 동시에 있기에, e 는 이 시스템에서 가장 강력한 오로라 후보입니다. e 궤도의 양성자 flux 는 지구의 약 10⁶배 (Fraschetti 2019, [1902.03732](https://arxiv.org/abs/1902.03732)) 로, 오로라 강도가 ~150 kR (지구 평균 10 kR 의 15배) 에 이릅니다. 지배적인 발광은 [OI] 557.7 nm 녹색 (지구 오로라 analog) 이고, 부차적으로 CO₂⁺ Fox–Duffendack–Barker 밴드가 적-오렌지 액센트를 더합니다. 결정적으로, 각 궤도의 50–80% 를 차지하는 sub-Alfvénic transit (Garraffo 2017) 동안에는 오로라 oval 이 평온기의 자기 위도 ~60° 에서 ~50° 까지 확장되어 — 극지뿐 아니라 nightside 반구의 상당 부분에서도 보이게 됩니다. cfg 렌더링 측면에서는 1차 `#4DFF4D` 녹색 오로라 밴드에 2차 `#FF4D4D` 적-오렌지 오버레이를 얹고, 플레어 이벤트 동안에는 강도를 끌어올리면 됩니다. interesting-first 타이브레이크에서 더 약한 자기장 대안 대신 지구형 자기장 (Wang 2025) 을 골라, 무질서한 극지 precipitation 대신 인식 가능한 오로라 구조를 얻었습니다.

## Rotation & spin synthesis

7.6 Gyr 동안 6.10 일 주기에서 작용한 조석 damping 은 동기 (1:1) 구성을
모호함 없이 확립시켰습니다. 황도 경사각은 0 으로 damping 되었고 (Agol
2021 §6.2), eccentricity 0.00510 (Agol 2021) 은 3:2 spin-orbit 에 들어
가기에는 지나치게 낮습니다 (Vinson 2017).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 6.1010 일 (527 127 s).
Kopernicus 의 `rotationPeriod` 는 궤도 `period` 와 초 단위로 일치해야
합니다.

**느린 자전 효과.** 6.1 일 자전 주기에서는 Coriolis 효과가 지구보다 약합니다. THAI II 4-GCM intercomparison (Sergeev 2022, [2109.11459](https://arxiv.org/abs/2109.11459)) 은 e 가 두 가지 대기 순환 regime 사이의 **tipping point** 에 위치한다고 보여줍니다. 적도 jet ("Gill–Matsuno" superrotation, ExoCAM / LMD-G / UM Hab 1 에서 관찰) 과 중위도 jet ("fast rotator", ROCKE-3D 그리고 Cohen 2022 설정의 UM 에서 관찰). 두 regime 은 서로 다른 구름 morphology 를 만들어내며 — NearStars 에서는 이중 밴드의 중위도 jet 비주얼 (평균 zonal wind ~18 m/s, 60–70°N/S 의 Rossby gyre, 위도 ±30° 까지 도달하는 substellar 구름 disk) 을 채택합니다. 다만 대안인 적도 jet morphology (저위도의 zonal 구름 벨트와 중위도의 더 맑은 zone) 도 물리적으로 동등하게 타당합니다. 구름 가변성의 20일 준정상 cycle (Cohen 2022) 은 KSP 게임플레이 속도에서는 너무 느려 의미가 없습니다.

**계절 없음.** 황도 경사각 = 0. libration 유도 일조량 변동은 0.4%
미만입니다. substellar 지점과 그 열린 물 disk 는 표면 frame 에서
고정되어 있습니다.

**자기 다이나모에 대한 기대.** e 의 질량 (0.69 M⊕) 과 활발한 내부 (Bourgeois 2024 의 마그마 바다 진화, 상당한 물 질량 분율) 는 6.1 일의 조석 고정 자전에도 불구하고 지속적인 다이나모를 뒷받침합니다. Wang 2025 ([2504.16662](https://arxiv.org/abs/2504.16662)) 의 MHD 시뮬레이션은 e 의 거주 가능 시나리오에 대해 0.32 G 의 지구형 표면 자기장을 명시적으로 채택하고, 평온기 magnetopause standoff 가 5–9 R_p (CME 동안에는 ~3 R_p 로 압축) 라고 보고합니다. interesting-first 타이브레이크는 약한 자기장 대안 (시스템에서 빈번한 sub-Alfvénic 에피소드 동안 e 가 사실상 자기권 보호 없이 노출되는 시나리오) 대신 이 지구형 자기장을 선호합니다. Kerbalism 의 방사선 모델링에서는 폐쇄 자기권을 가정합니다. cfg 는 평온기에 1.5–4 R_p 에 trapped-particle 벨트를 두며, stellar wind 상태에 따라 큰 변동성을 갖습니다.

## Visual styling

표면과 대기 결정 사항을 결합한 결과입니다.

- **전역 외관.** 궤도에서 보면 e 는 substellar 지점 부근에 warm-cream
  열린 물 "동공"을 가진 눈공처럼 보이고, 그 주위는 fractal 한 sea-ice
  전이대, 그 너머는 완전한 흰색-크림 빙하 얼음으로 덮여 있습니다.
  영구적 구름 커버 (전역 ~55%) 가 외관을 부드럽게 만들고, substellar
  해양 위에는 stratocumulus, 얼음 영역 위에는 high cirrus 가 자리잡
  습니다.
- **Substellar disk (열린 물).** 강렬한 적-오렌지 조명 아래의 어두운
  navy 해양 (`#1a2540`) 에 warm cream 구름 (`#c0a890`) 이 점점이
  박힌 모습. 행성에서 시각적으로 가장 인상적인 feature 입니다.
- **얼음 전이 밴드.** warm cream (`#d8d0c4`) 얼음과 어두운 해양
  (`#1a2540`) 의 fractal 패턴 — 열린 lead 가 보이는 깨진 sea ice
  입니다. 전이 반경은 substellar 에서 약 35° (Wolf 2017) 이며, KSP
  지형은 이를 거의 원형의 ice line 으로 표현해야 합니다.
- **빙하 얼음 영역.** 빙하 흐름이 기반암과 만나는 곳에 미세한 지형
  기복을 가진 매끄러운 warm cream (`#d8d0c4`). terminator 는 비스듬한
  조명에서 가장 밝은 영역으로, 긴 그림자가 압력 ridge 와 crevasse 를
  드러냅니다.
- **Nightside.** starlight 를 반사하는 얼음의 옅은 cyan-white sheen 만
  남는 어두움. 보이는 feature 는 압력 ridge, 균열, 가끔의 refrozen
  lead 정도입니다. KSP nightside ambient ≈ dayside 의 1%, 렌더링은
  얼음 feature 만 드러내야 합니다.
- **Atmosphere haze.** 약 15–25 km 두께의 옅은 gray-blue limb glow
  (`#5a7090`) — Rayleigh 산란된 M-dwarf 빛입니다. M-dwarf SED 때문에
  지구의 푸른 limb 보다 훨씬 흐릿합니다.
- **하늘의 별.** TRAPPIST-1 이 e 의 하늘에서 2.17° 를 차지합니다
  (지구에서 본 태양의 4배). 팔 길이로 든 큰 식기 접시 정도 크기의
  깊은 적-오렌지 disk (`#ff7a1a`) 로 보이며, substellar 지점의 표면
  조명은 "영원한 일몰" 같은 느낌이고, 멀어질수록 황혼에서 완전한
  밤으로 흐려집니다.
- **하늘의 자매 행성.** d (안쪽 이웃) 는 합에서 각 크기 ~0.3°, f
  (바깥쪽 이웃) 는 ~0.4°. 공명 체인 덕분에 며칠마다 합이 발생하며,
  전체 시스템은 거의 동일 평면입니다.

## Canonical alternatives

### Diverged cfg picks

| 항목 | 게임 (cfg) | 고증 대안 | 어긋난 이유 |
|---|---|---|---|
| `magnetic_field_strength_microtesla_equator` | 30 μT (지구 수준, Wang 2025 0.32 G MHD 시나리오) | 약 2 μT (RM22 다이나모 스케일링 — 조석 고정 저질량 행성 대상, Reiners & Christensen 2010) | Wang 2025 는 거주 가능성 시나리오를 위해 지구 수준 자기장을 *가정*한 것이고, RM22 는 자전 주기와 핵 크기 의존성으로부터 더 약한 값을 *유도*합니다. cfg 는 Wang 의 가정을 채택했습니다 — 강한 자기권과 지구식 오로라 오벌이 플레이어가 즉시 인지할 수 있는 시각 신호이기 때문입니다. 약한 자기장 시나리오에서는 e 의 자기권 보호가 어수선한 극 영역 강수로만 나타나 시각적 hook 이 약합니다. 약한 자기장 시나리오는 Open items 에 cfg variant 로 보존합니다. |
| `magnetic_dipole_moment_normalized_earth` | 지구의 0.3 배 (자기장 강도 선택에서 파생) | 지구의 0.1 배 미만 (RM22 에서 파생) | 자기장 강도 선택에서 파생되는 값입니다. 독립 결정이 아닙니다. |

## Bibliography

### Read (visual-informative, drove decisions above)

- **[2509.05414](https://arxiv.org/abs/2509.05414)** Glidden 2025 (DREAMS NIRSpec PRISM) — e 의 첫 JWST
  transmission 스펙트럼 (4 visit). 구름 동반 H₂-rich 대기를 >3σ 에서
  배제하고 stellar contamination 처리 방법을 제약합니다. 초석이 되는
  관측 논문입니다.
- **[2509.05407](https://arxiv.org/abs/2509.05407)** Glidden 2025 (DREAMS Secondary Atmospheres) — 동반
  논문입니다. **미량 CO₂ 와 CH₄ 를 가진 N₂-rich 대기 완전히 허용,
  Venus 형은 2σ 에서 약하게 disfavor.** 시나리오 선택의 결정적
  근거입니다.
- **[2510.18704](https://arxiv.org/abs/2510.18704)** Bourgeois 2025 — e 에 대한 다중모델 앙상블 (광화학
  + 3D 기후 + transmission 스펙트럼). N₂/CO₂/CH₄/H₂O 조성 공간, 물
  구름, 광화학 haze 를 탐구하며 구름 커버 분율과 대기 조성 혼합에
  정보를 제공합니다.
- **[2502.00132](https://arxiv.org/abs/2502.00132)** Way 2025 — TRAPPIST-1 d 를 위한 ROCKE-3D GCM 스위트
  지만 e 와의 광범위한 비교를 동반합니다. e 를 거주 가능 파라미터
  공간 안에 위치시키고 Earth/Venus/Dead 삼분법을 논의합니다. d Phase
  3 에서 이미 검토되었습니다.
- **[1809.07498](https://arxiv.org/abs/1809.07498)** Lincowski 2018 — 모든 TRAPPIST-1 행성의 진화한 기후.
  "Aqua planet e 는 지구형 지질 outgassing 과 CO₂ 가 주어지면 온대
  표면을 유지할 수 있다." aquaplanet cfg 선택의 직접적 동기입니다.
- **[2006.11349](https://arxiv.org/abs/2006.11349)** Wunderlich 2020 — e 와 f 의 wet vs. dry 대기. e 가
  지구형 geology + CO₂ 조건에서 온대일 수 있음을 확인하며 cfg 조성
  결정을 뒷받침합니다.
- **[2008.09599](https://arxiv.org/abs/2008.09599)** Bourgeois 2024 — e/f/g 의 마그마 바다 진화. e 의 물
  질량 분율 범위 0–0.23 을 제시해 기반암 물 예산을 설정합니다. 표면
  합성에서 사용했습니다.
- **[2109.11457](https://arxiv.org/abs/2109.11457)** Sergeev 2022 (THAI I) — TRAPPIST-1 e 에 대한 dry-case 4-GCM intercomparison. wet/dry 비교의 베이스라인 레퍼런스입니다.
- **[2109.11459](https://arxiv.org/abs/2109.11459)** Sergeev 2022 (THAI II) — moist-case 4-GCM intercomparison. 10–77% 구름 커버 분산과 적도-vs-중위도 jet regime 의 tipping-point 분석을 제공합니다. **cfg 의 구름 morphology 신뢰도에 대한 주요 refinement.**
- **[2109.11460](https://arxiv.org/abs/2109.11460)** Fauchez 2022 (THAI III) — THAI 스위트에서 e 에 대한 시뮬레이션된 transmission 스펙트럼. JWST 검출에 필요한 조건을 제약합니다 (Hab 1. 23–38 transit, Hab 2. 7–12 transit).
- **[1902.03732](https://arxiv.org/abs/1902.03732)** Fraschetti 2019 — TRAPPIST-1 HZ 의 Stellar Energetic Particle flux. e 에서 양성자 flux 가 지구의 약 10⁶배일 것으로 예측하지만 두 가지 완화 메커니즘 (stellar B-field 에 의한 containment, CME 억제) 을 동반합니다. 특정 값을 강제하지 않으면서도 cfg 에 자기장을 유지할 근거를 줍니다. 오로라 강도 추정 (지구 양성자 flux 의 10⁶배 → ~150 kR) 도 함께 뒷받침합니다.
- **[1706.04617](https://arxiv.org/abs/1706.04617)** Garraffo 2017 — TRAPPIST-1 의 위협적인 자기 및 플라스마 환경. 각 궤도의 50–80% 를 차지하는 sub-Alfvénic transit 과 오로라 oval geometry 함의를 제공합니다.
- **[2504.16662](https://arxiv.org/abs/2504.16662)** Wang 2025 — 지구형 자기장을 가진 TRAPPIST-1 e 거주 가능성의 MHD 시뮬레이션. cfg 의 `magnetic_field_strength` 값의 근거입니다.
- **[1910.09871](https://arxiv.org/abs/1910.09871)** Atri 2019 — 별 양성자 이벤트의 표면 dose. e 의 12 Sv/yr 베이스라인 + 플레어 시 지구의 10⁶배 스파이크를 제공합니다.

### Read (context / methodology, not decision-driving)

- **[2403.03403](https://arxiv.org/abs/2403.03403)** M dwarf 외계행성은 얼마나 거주 가능한가? 표면 조건
  모델링. 일반 M-dwarf HZ 맥락이며 e 특화는 아닙니다.
- **[2412.10192](https://arxiv.org/abs/2412.10192)** CO₂ 지배에서 H₂O 지배 대기로. 거주 가능 영역 행성의
  휘발성 cycling 배경이며, CO₂ 분율 선택 (outer-HZ 가열을 위해 0.04%
  대신 1%) 에 정보를 제공합니다.
- **[2206.00028](https://arxiv.org/abs/2206.00028)** Felton 2022 — 대기 교환 biosignature false-positive
  (d 의 O₂ 가 e 로 운반). d Phase 3 에서 이미 검토. abiotic O₂
  배경을 제약하지만 비주얼 cfg 는 바꾸지 않습니다.
- **[2310.15992](https://arxiv.org/abs/2310.15992)** 느리게 자전하는 조석 고정 행성을 위한 새로운 2D
  Energy Balance Model. substellar disk 모델링의 방법론적 맥락
  입니다.
- **[2211.11887](https://arxiv.org/abs/2211.11887)** Cohen 2022 — 조석 고정 aquaplanet 의 traveling
  planetary-scale wave, Met Office UM GCM. **cloud morphology** 결정을
  주도합니다. e 는 이중 중위도 jet regime (평균 zonal wind ~18 m/s)
  에 자리잡고, substellar 구름 disk 는 위도 ±30° 까지만 도달합니다.
  두 개의 정상 Rossby gyre 가 60–70°N/S 에 있고, 동쪽 gyre 는 약 20일
  주기로 진동합니다. 평균 구름 분율 60% 로 Wolf 2017 을 확인해줍니다.
- **[2312.01893](https://arxiv.org/abs/2312.01893)** Boldog 2023 — HZ 암석 행성의 물 함량. e 의 subsurface
  ocean probability 가 87.56% (그들의 카탈로그 최상위 등급). 암석-얼음
  경계의 조석 가열은 0.21 W/m² (범위 0.18–0.24) 로 표면 flux 보다
  훨씬 큽니다. water-rich aquaplanet cfg 선택을 뒷받침합니다.
- **[1906.06797](https://arxiv.org/abs/1906.06797)** Yamashiki 2019 — 별의 superflare 가 거주 가능성에
  미치는 영향. TRAPPIST-1 의 Spot Maximum Flare = 9.09×10³² erg.
  1 bar N₂/O₂ 대기 + 지구 수준 자기장이 있으면 Spot Maximum 하에서도
  지표 dose 가 비치사 수준으로 유지됩니다 (대기 상층 ≤1.18×10⁴ Sv →
  지표에서는 관리 가능). 복잡한 생명에 필요한 임계 대기 column 은
  ~2.04×10² g/cm² (지구의 20%) 입니다. 1 bar 대기 cfg 를 유지할 근거
  를 제공합니다.
- **[2309.15239](https://arxiv.org/abs/2309.15239)** + **[2405.20167](https://arxiv.org/abs/2405.20167)** Cooke 2023 / 2024 — e 에 대한
  WACCM6 지구형 대륙 시뮬레이션. 현실적 육해 분포 때문에 전역 평균
  표면 T 가 219–231 K 로 Wolf 2017 aquaplanet 의 270 K 보다 차갑게
  나옵니다. O₃ column 은 stellar UV 시나리오에 따라 50–1310 DU.
  aquaplanet cfg 는 더 따뜻한 Wolf 2017 베이스라인을 택하고, WACCM6
  은 "덜 거주 가능한" cfg 변형용 차가운 대안으로 둡니다.
- **[2601.18324](https://arxiv.org/abs/2601.18324)** Bourgeois 2026 — TRAPPIST-1 e 의 이른 Great Oxidation
  Event (지구보다 약 700 Myr 빠름, K_oxy ~0.83 vs 1.0). M-dwarf UV
  분포가 O₂ 광분해보다 O₃ 형성에 유리해, 낮은 대기 O₂ 에서도 두꺼운
  O₃ 층이 만들어집니다. cfg 가 대기 조성에 미량 O₃ 를 포함하는 선택
  을 강화합니다.
- **2305.08813** *(d 의 참고문헌, e 가 아님)* 다양한 contamination /
  특성화 작업 — 맥락만 제공합니다.

### Read (instrument-only, not visual-informative)

- **[2203.04173](https://arxiv.org/abs/2203.04173)** Rustamkulov 2022 — JWST NIRSpec lab time-series.
  방법론만 다룹니다.
- **[2407.19167](https://arxiv.org/abs/2407.19167)** 기계 보조 biosignature 분류. e 특화가 아닙니다.

### Not read — no arXiv preprint or low-priority (~34 papers)

e 의 참고문헌은 두 번째로 큽니다 (64 편, 그중 30 편 arXiv). 비-arXiv
논문 대부분은 biosignature 또는 ELT 특화 특성화 계획에 대한 conference
abstract 로, 비주얼-정보 제공은 아닙니다. 주목할 만한 skip 항목.

- **2024–2025 다양** — biosignature 가능성 연구와 JWST 제안 abstract.
  cfg 관련 대기 조성을 갱신할 때가 아니면 그냥 skip 합니다.
- **광화학 프로그램 제안서** — 방법론만 다룹니다.

---

## Open items for follow-up

- Glidden 2025 DREAMS 논문은 "보정되지 않은 stellar contamination 또는
  행성 신호일 수 있는 feature" 가 남아 있음을 인정합니다. 향후 재환원
  이나 새 instrument (NIRISS, MIRI MRS) 가 e 에서 분자 feature 를
  찾아낸다면 대기 조성 표 갱신이 필요할 수 있습니다.
- 채택한 물 질량 분율 범위 (0.05–0.10) 는 Bourgeois 2024 의 0–0.23
  의 중앙값입니다. Acuña 2025 이후의 내부 fit 가 개선되면 좁힐 수
  있습니다.
- "Venus 형" 해석 (1 bar CO₂ + H₂SO₄ 구름) 의 cfg 변형. 해양이 없는
  시각적으로 독특한 yellow-cream 세계입니다. Glidden 2025 가 2σ 에서
  약하게 disfavor 하지만 배제되지는 않습니다.
- "맨 암석 airless" 해석의 cfg 변형. b/c 와 비주얼은 비슷하지만 e 의
  훨씬 차가운 dayside 온도에서 동작합니다 (T_eq ≈ 250 K → 대부분
  얼음으로 코팅된 맨 암석).
- 5% abiotic O₂ 선택 교차 검증. 일부 Lincowski 2018 시나리오에서는
  10–20% 일 수도 있습니다. 하한은 "최소 광분해" 기대치와 맞고, 상한
  은 더 "post-runaway" 쪽에 가깝습니다.
- 이중 중위도 jet 과 적도 superrotation 사이의 구름 morphology 는 본질적으로 GCM 의존적인 예측입니다. 향후 intercomparison 이 이 tipping point 를 해소한다면 cfg 의 `cloud_morphology` 값 (그리고 가능하면 구름 밴드의 비주얼 렌더링) 을 업데이트해야 할 수 있습니다.
- interesting-first 타이브레이크에서 RM22 스케일링 추정값 (~0.08 M_Earth, 훨씬 약함) 대신 Wang 2025 의 지구형 자기장 (0.32 G) 을 채택했습니다. 지구형 케이스가 시각적으로 더 두드러진 자기권 + 오로라 oval 을 만들어내고, 약한 자기장 대안은 보수적 해석을 선호하는 유저를 위해 cfg 변형으로 남겨둡니다.
- 방사선 dose 수치 (12 Sv/yr) 는 e 를 Kerbalism 의 "high-radiation" 구간에 위치시킵니다. 150 kR 오로라 렌더링은 상당히 극적일 수 있으니, 게임플레이용으로 밝기 슬라이더를 두고 싶을 수 있습니다.

## Related

- [trappist-1-d](trappist-1-d.md) — HZ 가장자리에 위치한 내측 형제.
- [trappist-1-f](trappist-1-f.md) — 외측 형제. snowball/eyeball 경계.
- [trappist-1-g](trappist-1-g.md) — 외측 HZ 비교 천체 (완전 snowball).
- [methodology](../reference/methodology.md) — Decisions 스키마.
- [mod-reference](../reference/mod-reference.md) — 이 천체의 대기 + 해양 cfg 를 소비하는 다운스트림 모드.
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — 계의 궤도 epoch 처리.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 이 Phase 3 → REX TRAPPIST-1 델타를 상세히 다룹니다.
