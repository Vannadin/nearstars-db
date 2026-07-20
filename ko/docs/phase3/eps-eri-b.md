<!-- ε Eridani b Phase 3 합성. cfg-ready 결정과 근거 -->
# ε Eridani b — Phase 3 Synthesis

ε Eridani b 는 어리고 활동성이 강한 K2V 왜성 ε Eridani 를 a =
3.53 ± 0.03 AU, 2671 ± 17 d (7.32 년) 주기로 도는 약 0.66 M_Jup
가스 행성입니다. 이심률은 e = 0.07 로 낮습니다. 20 년 가까이 논쟁이
이어진 시선속도 역사를 거쳐 (Hatzes 2000 의 발견. Benedict 2006 의
HST FGS 시도. 활동도에 의한 가짜 신호 반박이 간헐적으로 제기됨)
마침내 L′ / Ms 밴드 직접 촬영으로 확정되었고 (Mawet 2019, Keck/NIRC2
vortex coronagraph), RV + Hipparcos/Gaia 천체측정 결합으로 정밀화
되었습니다 (Llop-Sayson 2021). Llop-Sayson 2021 의 최확 경사각은
i = 78.81° 로, 행성이 34° 주 고리 평면 (Booth 2017 ALMA 분해
디스크) 에서 약 2σ 기울어져 있을 가능성을 시사합니다. coplanar 한
~32° 해는 약 1σ 에서 허용되지만 선호되지는 않습니다. 투과 / 열방출
스펙트럼은 아직 존재하지 않으며, 행성의
대기 조성, 자전, 위성 집단은 모두 미결입니다.

**NearStars 시나리오 선택. 차갑고 (T_eq ≈ 110 K) 어리며 (~440 Myr)
3.5 AU 저편심 궤도의 jovian 으로, ε Eri 의 삼중 belt debris 디스크
중 안쪽 belt 와 중간 belt 사이의 갭 (3–20 AU) 에 자리합니다. Su
2017 의 Genie 모델은 이 행성을 inner-gap sculptor 로 지목합니다.
시각 스타일링은 Saturn analog 형 차가운 jovian 으로 다루며, K2V
조명 아래에서 따뜻한 크림 색조로 렌더링되는 암모니아 얼음 구름 띠,
K-왜성의 강한 UV 가 CH₄ 광분해를 통해 만드는 옅은 광화학 haze 층,
고리 없음, 그리고 30× 태양 항성풍이 구동하는 H-Balmer α 오로라가
Hill sphere 관측자에게 보이는 Jupiter 규모 자기권을 적용합니다.**
35 개 cfg 픽 중 **14 개는 canonical 일치, 21 개는 tie-break** (스펙트럼
이나 열 지도가 없는 상태에서의 K2V 조명 하 jovian-analog 디폴트),
documented divergence 는 0 개입니다.

## Decisions

Kopernicus / 대기 cfg-ready 값. `Confidence`. high = 직접 측정 혹은
강한 제약, medium = 강한 근거의 이론값, low = 허용 윈도우 내의
미적 선택.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 0.82 M☉ 별 주위 3.5 AU 의 7.32 년 궤도. 조석 감쇠 시간이 Hubble 시간을 훨씬 초과 |
| `obliquity_deg` | 25 | low | Tie-break. 측정 없음. Saturn 의 26.7° 가 Jupiter 의 3.1° 보다 시각적으로 더 두드러져 cfg 가 채택 (cfg 는 고리 없음을 택하더라도). 3.5 AU jovian 의 역학적 안정 윈도우 내 |
| `eccentricity` | 0.07 | high | Llop-Sayson 2021. RV + Hipparcos/Gaia 천체측정 결합 fit |
| `argument_of_periastron_deg` | −19.15 | high | Llop-Sayson 2021 (DB Phase 2) |
| `sidereal_period_days` | 2671 ± 17 | high | Llop-Sayson 2021. RV + 천체측정 정밀화. Mawet 2019 직접 촬영 epoch 와 일관 |
| `semi_major_axis_au` | 3.53 ± 0.03 | high | Llop-Sayson 2021 |
| `inclination_deg` | 78.81 (+29.34/−22.41) | high | Llop-Sayson 2021 최확값 (RV + Hipparcos/Gaia 천체측정). = DB. 디스크 coplanar i ≈ 34° (Booth 2017 고리. Benedict 2006 30°) 는 이로부터 약 1–2σ 떨어져 있으며 Open items 에 노트된 대안으로 보존 |
| `mass_mjup` | 0.66 (+0.12/−0.09) | high | Llop-Sayson 2021. RV + Hipparcos/Gaia 천체측정 + 촬영 결합에서 얻은 진질량 (경사각 marginalize 됨. = DB Phase 2) |
| `mass_mearth` | 210 | high | = 0.66 M_Jup × 317.8 ≈ 210 (DB 209.8) |
| `radius_rjup` | 1.05 | low | Tie-break. 트랜짓 없음. Burrows 2003 / Fortney 2007 진화 트랙은 0.66 M_Jup, 0.44 Gyr, 태양 metallicity 에서 1.03–1.12 R_Jup 예측. cfg 는 중간값 1.05 를 채택. Mawet 2019 Ms-band 미검출이 hot-start 인플레이션 반경 > 1.3 R_Jup 을 배제 |
| `surface_gravity_g_earth` | 1.5 | medium | g = G M / R² 유도. M = 0.66 M_Jup, R = 1.05 R_Jup → 14.8 m/s² = 1.5 g⊕ |
| `density_g_cc` | 0.76 | medium | 유도. 0.66 M_Jup / (1.05 R_Jup)³ × ρ_Jup ≈ 0.76 g/cc |
| `insolation_s_earth` | 0.026 | high | 유도. S = L_star / a² = 0.32 L☉ (Baines & Armstrong 2012, recommended) / (3.53 AU)² = 0.0257 S⊕ |
| `equilibrium_temp_k_a0` | 111 | high | 유도. T_eq = 278 K × (L/a²)^0.25 = 278 × 0.0257^0.25 |
| `equilibrium_temp_k_a03` | 102 | high | 유도. 지구 analog A = 0.3 |
| `bond_albedo` | 0.34 | low | Tie-break. Saturn analog 0.342 (Hanel 1983. Li 2018) 를 Jupiter 의 0.503 보다 선호. T_eq ≈ 111 K 의 차가운 구름 화학이 Jupiter 보다 더 두꺼운 암모니아 구름 데크 쪽으로 기울어 Saturn 과 닮음. Uranus 0.300 도 같은 윈도우 내 |
| `intrinsic_luminosity_w_m2` | 0.5 | low | Tie-break. Burrows 2003 의 0.66 M_Jup, 0.44 Gyr 냉각 트랙이 내부 T ~ 100 K 를 예측. cfg 는 보수적으로 0.5 W/m² 내부 flux 를 선택 (Jupiter 의 5.4 W/m² 보다 훨씬 낮음. 더 늙고 질량이 작고 덜 인플레이션된 상태와 일관) |
| `atmosphere_present` | true | high | 정의상 가스 행성. 태양 조성 M-R 일관성에서 H₂/He 본체 추론 |
| `atmosphere_reference_pressure_pa` | 100 000 | medium | 가스 행성은 단단한 표면이 없음. cfg 기준 1 bar 레벨에서 구름 데크 렌더링. KSP jovian 대기 고도 원점 관례와 일치 |
| `atmosphere_composition` | H₂ ~89%, He ~10%, CH₄ ~0.2%, NH₃ ~0.02%, H₂O ~0.01% (심층), 광화학으로 미량 CO 와 HCN | low | Tie-break. 스펙트럼 없음. Lodders 2003 의 protosolar 풍부도와 Jupiter/Saturn analog volatile inventory, T = 111 K 평형에서 절단된 응결 화학을 따르는 태양 조성 jovian 디폴트 |
| `atmosphere_scale_height_km` | 27 | medium | 유도. H = kT / (μ m_H g). T = 111 K, μ = 2.3, g = 14.8 m/s² ≈ 27 km |
| `atmosphere_tint_rgb_hex` | `#d8c098` (K2V 조명 하의 따뜻한 크림 limb haze) | low | Tie-break. 암모니아 얼음 대기는 본질적으로 거의 흰색. K2V 5039 K SED 가 Sun 조명 Jupiter 대비 따뜻한 쪽으로 인식을 이동 |
| `cloud_cover_fraction` | 0.85 | medium | jovian analog. 거의 완전한 띠상 분포. cfg 는 균질 흐림이 아닌 어두운 belt / 밝은 zone 의 대비를 살리려 0.85 를 채택 |
| `cloud_morphology` | 약 0.5–1 bar 레벨의 암모니아 얼음 구름 데크가 있는 띠상 zonal band. 약 5 bar 에 가능한 물 구름 데크 (가시광 촬영 불가). K2V UV 하의 CH₄ 광분해에서 나오는 100 mbar 위의 옅은 광화학 haze 층 | low | Tie-break. GCM 없음. cfg 는 Saturn analog 의 띠 구조를 채택하면서 ε Eri 의 강한 K-왜성 UV 가 Saturn 보다 약간 더 두드러진 성층권 haze 층을 만든다고 봄 |
| `cloud_tint_rgb_hex` | `#e8dac4` (따뜻한 크림. NH₃ 얼음 + K2V 조명) | low | Tie-break. Saturn 의 암모니아 구름은 태양광 하에서 크림-흰색으로 보임. 5039 K K2V 하에서는 따뜻한 크림 쪽으로 더 이동 |
| `photochemical_haze_present` | true | medium | ε Eri 의 강화된 FUV flux (France 2018 MUSCLES, 태양의 5–20 배) 가 100 mbar 위에서 CH₄ 광분해를 구동. 톨린 / 탄화수소 haze 층은 Titan 대기 화학과 유사하나 jovian H₂ 배경 위에서 작동 |
| `photochemical_haze_tint_rgb_hex` | `#b08858` (K2V UV 하 CH₄ 광분해의 옅은 톨린) | low | Tie-break. 실험실 톨린 화학 (Khare 1984. Hörst 2018) 은 주황-탄 흡수 특성을 보임. haze 층은 얇아서 지배적 색조라기보다는 미묘한 limb 어두워짐으로 렌더 |
| `planet_disk_tint_rgb_hex_primary` | `#e8dac4` (크림-흰색 zone. 행성 규모 관측자에게 보이는 지배적 구름 데크 외관) | low | `cloud_tint_rgb_hex` 의 downstream |
| `planet_disk_tint_rgb_hex_accent` | `#c4a878` (따뜻한 크림-갈색 band. 깊은 구름 층과 톨린 haze 가 비치는 belt 영역) | low | Tie-break. K2V 조명 하 Saturn/Jupiter belt-zone 대비. 낮은 일사량에서 약한 대류 구동 때문에 Jupiter 대비 band 진폭은 축소 |
| `ring_present` | false | medium | Mawet 2019 Ms-band 고대비 촬영은 3.5 AU 분리에서 Saturn 밝기 고리 시스템을 검출했어야 함. 검출 없음. cfg 는 "고리 없음" 으로 기본값 설정 |
| `ring_observed` | false | high | Mawet 2019 Ms-band 직접 촬영에서 고리 성분 검출되지 않음 |
| `rotation_period_hours` | 10 | low | Tie-break. 자전 측정 없음. Jupiter analog 9.93 h (Jupiter 가 태양계에서 가장 빠른 jovian 자전). cfg 는 둥근 Jupiter-like 10 h 를 더 느린 Saturn-like (10.7 h) 나 Uranus-like (17.2 h) 보다 채택. 3.5 AU 에서의 질량 스케일과 각운동량 예산이 Jupiter 급 고속 자전 쪽 |
| `magnetic_field_strength_microtesla_equator` | 660 | medium | 에너지플럭스 다이나모 스케일링 (Christensen et al. 2009 `2009Natur.457..167C`. Reiners & Christensen 2010 `1007.1514`, Table 4.3 + 1 M_J 냉각 트랙). B_dip^pol = 9 G·(age/4.5 Gyr)^−0.33·(M/M_Jup)^0.93 → 0.66 M_Jup, 0.44 Gyr (젊음, gyrochronology) 에서 B_eq ≈ 660 µT (범위 540–810). 젊은 거대 행성은 질량이 낮아도 Jupiter 를 넘어선다. 다이나모를 구동하는 것이 질량이 아니라 내부 광도이기 때문이다. 이전의 "축소판 jovian, Jupiter 보다 ~7% 아래" 설명은 젊음 효과의 방향을 거꾸로 잡은 것이었다. docs/reference/planetary-dynamo-scaling.md 참고 |
| `magnetic_dipole_moment_normalized_earth` | 34000 | low | 660 µT × (1.05 R_Jup)³ 를 Jupiter (적도 4.5 G, Earth 의 20 000배) 와 비교 → 에너지플럭스 스케일링 (`1007.1514`) 으로 ≈ 34 000 × Earth. 선형 질량 0.66 × 20 000 = 13 200 을 대체. R³ 에 민감 → 신뢰도 낮음 |
| `magnetic_dipole_tilt_deg` | 10 | low | Tie-break. Jupiter 9.6°, Saturn 0°, Neptune 47°. cfg 는 시각적으로 명확한 오로라 oval 오프셋을 위해 Jupiter analog 10° 채택. Saturn-aligned 0° 는 시각적으로 단조로움 |
| `aurora_present` | true | medium | ε Eri 의 항성풍 ≈ 30× 태양 질량 손실률 (Wood 2002) + 사이클 활동 corona 가 3.5 AU 에서 강한 입사 플라즈마 flux 구동. jovian 자기권 포획과 결합하면 Jupiter 와 비슷한 오로라 방출이 더 강한 구동으로 나타남 |
| `aurora_color_primary_hex` | `#c84080` (H₂ 풍부 jovian 대기에서 지배적인 H-Balmer α 656 nm 적-분홍) | low | Tie-break. Jupiter UV 오로라는 Lyα + H₂ Lyman/Werner 밴드에서 가장 밝지만 가시광 성분은 H-Balmer α. K2V 조명 맥락에서 가시광 오로라는 적-분홍으로 읽힘 |
| `aurora_oval_magnetic_latitude_deg` | 70 | medium | Jupiter analog 오로라 oval. 65–75° 자기 위도 (Clarke 1996 HST FUV. Bonfond 2017). ε Eri b 의 자기권 standoff 에 맞춰 스케일링 |
| `aurora_intensity_kR_typical` | 1000 | low | Tie-break. Jupiter UV 오로라 ≈ 100–1000 kR (Clarke 2009, 태양풍 상태 의존). ε Eri 의 30× 태양풍이 비례적으로 더 강한 구동. cfg 는 ε Eri 활동 상태의 중간값 1000 kR 채택 |
| `companion_position_relative_belts` | asteroid belt analog (3 AU) 와 중간 belt (20 AU) 사이. Su 2017 Genie 삼중 belt 모델의 inner-gap sculptor | high | Su 2017 §4. gap-clearing 은 두 belt 사이에 M ≳ 0.5 M_Jup 의 행성을 요구. ε Eri b 의 질량과 위치가 요구 조건과 일치 |
| `star_apparent_angular_diameter_deg` | 0.112 | high | 유도. 2 R_star / a = 2 × 0.74 R☉ / 3.53 AU × (180/π). Jupiter 에서 본 태양의 0.10° 와 비슷 |
| `stellar_illumination_color_temp_k` | 5039 | high | host Phase 3 (`docs/phase3/eps-eri.md`) 에서 상속 |

## Surface synthesis

ε Eridani b 는 통상적 의미의 단단한 표면을 가지지 않습니다. 1 M_Jup
규모의 H₂/He 가스 행성입니다. 시각 렌더링에 관련된 "표면" 은 구름
데크로, 광학 불투명도가 위쪽의 맑은 가스에서 아래쪽의 입자 부유 가스로
전환되는 1 bar 압력 레벨이 관례적 기준입니다.

3.5 AU 에서 L_star = 0.32 L☉ 아래의 평형 온도는 T_eq ≈ 111 K (A = 0)
혹은 102 K (A = 0.3) 로, 두 값 모두 Jupiter (T_eq ≈ 110 K) 보다
차갑고 Saturn (T_eq ≈ 81 K) 보다 따뜻합니다. 이 온도에서의 H₂/He
대기 응결 화학은 잘 정립된 Lewis 1969 / Atreya 1999 열화학 시퀀스를
따릅니다. 암모니아 (NH₃) 가 1 bar 레벨 근처에서 응결하고, 물 (H₂O)
이 약 5 bar 깊이에서 더 깊게 응결하며, 메탄 (CH₄) 은 접근 가능한
모든 레벨에서 기체로 남습니다 (CH₄ 응결점은 T < 75 K 를 요구하는데
ε Eri b 의 도달 범위를 넘음). 따라서 cfg 는 ε Eri b 를 암모니아 구름
데크 jovian 으로 렌더링하며, 구조적으로 Saturn 과 가장 유사하지만
더 따뜻하고 더 큰 질량에서 기대되는 Jupiter-like 자전 역학을
가집니다.

구름 데크는 K2V 조명 아래에서 따뜻한 크림-흰색 (`#e8dac4`) 으로
읽힙니다. 실험실에서 암모니아 얼음은 가시광에서 0.8–0.9 의 내재
알베도를 가지며 1.5–2.0 μm 의 미량 흡수에서 옅은 노란 색조를
띱니다. 5039 K K2V 조명 아래에서는 태양광 Jupiter 팔레트 대비 더
따뜻한 크림 쪽으로 인식이 이동합니다. belt-zone 대비 (belt band 에
`#c4a878` 따뜻한 크림-갈색) 는 Jupiter 보다 완화되어 있는데, T_eq ≈
111 K 에서의 대류 구동이 Jupiter 보다 약하기 때문입니다. 그래도
Saturn 보다는 강합니다. 행성 내부 열 flux (~0.5 W/m² 채택) 가
무시할 수 없는 대류 overturn 을 만들기 때문입니다. 이는 Sromovsky
2007 의 belt-zone 진폭 스케일링과 대체로 일관됩니다.

암모니아 구름 데크 위에서는 ε Eri 의 강화된 K-왜성 FUV flux
(France 2018 MUSCLES. 같은 궤도 거리에서 태양의 5–20 배) 가 약
0.1–10 mbar 압력 레벨에서 메탄 광분해를 구동합니다. 광화학 산물 —
더 무거운 탄화수소 (C₂H₂, C₂H₆) 와 톨린 유사 폴리머 — 가 자외선과
청색에 흡수 특성을 갖는 성층권 haze 층으로 축적됩니다 (Khare 1984.
Hörst 2018). cfg 는 이를 `photochemical_haze_present = true` 와
크림-흰 구름 데크 위를 덮는 얇은 limb-haze 층으로 렌더링되는 옅은
톨린 색조 `#b08858` 로 인코딩합니다. haze 가 시각 외관을 지배하지는
않습니다. Jupiter 의 성층권 haze 도 가시 파장에서는 미묘한 limb
어두워짐만 만듭니다. 그러나 앞으로의 JWST coronagraph 나 ELT
고대비 촬영에서 가장 가능성 높은 1차 분광 시그니처일 것입니다.

행성 내부에 매핑되는 표면 feature 는 없습니다. 대류 overturn 이
암모니아 구름 데크 아래에서 수직 혼합된 단열선을 유지합니다. 내부
구조는 약 1 Mbar (≈ 반지름의 90%) 의 금속 수소 전이까지 완전히
유체이며, 5–25 M⊕ 의 중원소 코어가 질량-반지름 모델에서 간접 추론
됩니다 (cfg 는 코어 질량을 인코딩하지 않음. 관측 제약 없음).

## Atmosphere synthesis

ε Eri b 의 투과 / 열방출 스펙트럼은 존재하지 않습니다. Mawet 2019
의 Ms-band (4.6 μm) 직접 촬영 대비 측정은 hot-start 광도에 대한
넓은 상한만 제공하여, 매우 어리고 매우 인플레이션된 jovian 진화
트랙 (Spiegel & Burrows 2012 의 T_eff > 700 K hot-start 모델) 을
약 2σ 수준에서 배제하지만 canonical 한 "cold-start" 열평형 예측
(내부 flux 를 포함해 T_eff ≈ 150 K) 은 데이터와 일관되게 유지합니다.
따라서 대기 조성은 전적으로 Lodders 2003 의 protosolar 풍부도 +
Atreya 1999 의 T = 111 K 평형에서 절단된 응결 화학을 따르는 태양
조성 jovian 디폴트에서 가져옵니다.

**압력 기준.** 가스 행성은 단단한 표면을 갖지 않습니다. cfg 기준
압력은 암모니아 구름 데크가 응결하는 1 bar (100 000 Pa) 로
설정됩니다. KSP 관례의 대기 고도 원점이 이 레벨과 일치합니다.
1 bar 위에서는 압력이 H ≈ 23 km 의 척도 높이로 감소합니다. 더
차가운 온도와 더 높은 중력의 조합 때문에 지구나 Jupiter 의 척도
높이보다 다소 낮습니다.

**조성.** 부피로 H₂ ≈ 89%, He ≈ 10% — 태양 protosolar 비율이며 이
질량과 나이에서는 He 고갈이 무시 가능합니다. volatile. CH₄ ≈ 0.2%
(Jupiter 는 0.21%. Wong 2004 Galileo probe 에 따라 protosolar 대비
약 3× 강화. cfg 는 Jupiter analog 0.2% 채택), NH₃ ≈ 200 ppm (구름
데크 위에서는 응결로 고갈), H₂O ≈ 100 ppm (더 깊은 물 구름 데크
위에서 고갈), 미량 CO ~ 1 ppb 와 HCN ~ 0.1 ppb 는 CH₄ + N₂
광화학에서 옴. 이 volatile 풍부도는 전적으로 tie-break 디폴트이며
스펙트럼이 어느 것도 제약하지 않습니다. 그러나 cfg 가 Jupiter analog
값을 선택하는 이유는 0.66 M_Jup 의 질량과 protosolar metallicity
맥락이 Jupiter 급 disk-accretion 형성 이력을 선호하기 때문입니다.

**광화학 시그니처.** ε Eri 의 강화된 FUV (Lyα. France 2018 MUSCLES.
8 × 10⁻⁴ L_bol 대 태양의 ≈ 6 × 10⁻⁵ L_bol) 는 Jupiter 가 받는 것보다
더 강한 메탄 광분해를 구동합니다. 그 결과의 탄화수소 사슬 (CH₄ →
C₂H₆, C₂H₂, C₂H₄ → 톨린 폴리머) 이 약 100 mbar 압력 위에 성층권
haze 층을 만듭니다. 정량적 모델링 (Moses 2005 Saturn. Hörst 2018
의 sub-Neptune 톨린 화학을 jovian 으로 확장) 은 ε Eri b 의 1 μm
에서의 haze 광학적 깊이가 Jupiter 의 약 2–5 배일 것으로 예측하여,
가시적으로 강화된 limb 어두워짐과 향후 분광에서의 검출 가능한
0.6–0.8 μm 흡수 특성을 만들기에 충분합니다. 근적외선의 오로라 관련
N₂⁺ / H₃⁺ 방출선 (Drossart 1989 의 Jupiter 3.4 μm H₃⁺) 이 향후 가장
진단적인 검출 채널이 될 것입니다. cfg 는 특정 광학적 깊이를
지정하지 않고 haze 의 존재만 인코딩합니다.

**Hill sphere 관측자가 보는 하늘.** 0.82 M☉ 주위 3.53 AU 의
0.66 M_Jup 에 대한 Hill sphere 반경은 r_H ≈ **0.224 AU = 447 R_planet**
입니다 — 상당한 위성 집단을 수용할 만큼 큽니다. 가상의 20 R_planet
(ε Eri b 의 큰 반지름에 스케일된 Io analog 거리) 큰 위성 위의
관측자에게 행성은 하늘에서 ≈ 5.7° 의 시지름 — Earth 에서 본 달
지름의 거의 12 배 — 으로 보이며 띠 진 크림-흰색 디스크로 낮 하늘을
지배합니다. ε Eri 별 자체는 작은 0.112° 의 점입니다 — Earth 에서
본 태양 크기의 1/4, Jupiter 에서 본 태양 기하와 비슷 — K2V 색온도의
짙은 주황 점으로 나타납니다. 따뜻한 크림 행성 디스크와 주황 점광원
사이의 대비가 어떤 wide-orbit fly-by 렌더에서도 시스템에서 가장
사진 같은 feature 일 것입니다.

**Nightside.** 직접 항성 조명 없음. 행성 자신의 내부 flux (~0.5
W/m²) 가 ~110 K 피크 (28 μm) 의 근적외 열 글로를 만듭니다 —
육안에는 보이지 않지만 Mawet 2019 가 행성을 검출한 4.6 μm 에서는
옅은 자체 조명의 적-따뜻 cast 입니다. 오로라 방출이 고자기위도에서
nightside 의 유일한 가시광 시그널을 제공합니다. ≈ 70° 자기 위도의
옅은 H-Balmer α 적-분홍 고리로, ε Eri 의 강화된 항성풍을 고려하면
Jupiter 의 가시광 오로라보다 더 밝을 법합니다.

## Rotation & spin synthesis

ε Eri b 의 자전 측정은 존재하지 않습니다. 도플러 확장 근적외 스펙트럼
(Snellen 2014 가 β Pictoris b 에 적용한 v sin i = 25 km/s 측정 기법)
은 < 0.5 arcsec 분리에서의 고대비 분광 촬영을 요구합니다. ε Eri b
는 host 에서 ≈ 1.1 arcsec 분리되어 현재 장비로도 접근 가능하지만,
작은 질량 (0.66 M_Jup) 과 약한 열방출이 자전 측정을 지금까지
가로막아 왔습니다.

**조석 감쇠 논증.** 0.82 M☉ host 주위 3.5 AU 의 Jupiter 질량 행성
조석 시간 척도는 τ_tide ≈ 10⁴⁰ s (Goldreich & Soter 1966. Q_p ≈
10⁵) — 우주 나이보다 수십 자릿수 더 깁니다. ε Eri b 는 **조석 잠금
이 아닙니다**. cfg 는 `tidally_locked = false` 로 인코딩합니다.

**자전 주기 선택.** 관측된 가스 행성들 사이에서 자전 주기는 질량에
약하게 의존합니다. Jupiter (1.0 M_Jup) ≈ 9.93 h, Saturn (0.3
M_Jup) ≈ 10.7 h, Uranus (0.046 M_Jup) ≈ 17.2 h, Neptune (0.054
M_Jup) ≈ 16.1 h. 0.66 M_Jup 의 ε Eri b 는 3.5 AU 의 disk accretion
에서 상속한 각운동량 예산이 Jupiter 급 고속 자전을 선호합니다.
cfg 는 `rotation_period_hours = 10` 을 둥근 Jupiter analog 값으로
채택 — 윈도우 내 tie-break 이며 제약 없음.

**자전축 기울기.** tie-break 미적 선택. Jupiter 의 3.1° 대 Saturn 의
26.7° 대 Uranus 의 97.8° — 어느 쪽 관측도 없음. cfg 는 25° (Saturn
analog) 를 채택. 적당한 기울기가 Uranus 극단의 "넘어진" 느낌과
시각적으로 구분되면서 렌더에서 애니메이션 축 기울기를 제공하기
때문입니다. 7.32 년 궤도 주기에서는 적당한 기울기도 구름 데크의
관측 가능한 계절 효과를 만들지 않습니다. 대류 overturn 시간 척도
(~년) 가 궤도 주기와 비슷한 정도입니다.

**KSP 구현 노트.** 자전 주기 = 10 h = 36 000 s. Kopernicus
`rotationPeriod = 36000`. 축 기울기 (`initialRotation` 또는 axis-
tilt cfg) = 궤도면 법선으로부터 25°.

**자기 다이나모 기대.** 강한 대류를 가진 H₂/He envelope 가 강한
dipolar 자기장을 유지합니다. 이 자기장은 질량이나 자전 속도가 아니라
**에너지 플럭스** (내부 냉각 광도) 가 결정합니다 (Christensen et al.
2009. Reiners & Christensen 2010, `1007.1514`).
B_dip^pol = 9 G·(age/4.5 Gyr)^−0.33·(M/M_Jup)^0.93. 0.66 M_Jup 의
젊은 0.44 Gyr 에서 ε Eri b 의 자기장은 ≈ 660 μT 적도 (≈ 3.4 × 10⁴ ×
Earth dipole) 로, 질량이 더 낮은데도 Jupiter 를 *넘어섭니다*. 젊다는
것은 더 뜨겁고 광도가 높은 내부를 뜻하기 때문입니다. (이전의 선형
질량 "≈ 400 μT, Jupiter 아래" 설명은 젊음 효과를 거꾸로 잡은
것이었습니다. docs/reference/planetary-dynamo-scaling.md 참고.)
dipole tilt 는 시각적으로 명확한
오로라 oval 렌더링을 위해 Jupiter analog 10° 로 설정합니다.
Jupiter-analog 자전 + 자기장 조합은 ε Eri b 를 "강한 자기권" 영역에
확고히 놓으며, 30× 태양풍 배경에 대해 magnetopause standoff 가
≳ 50 R_planet 입니다.

## Visual styling

표면 (구름 데크) 과 대기 결정을 조합하면.

- **전역 외관.** 궤도에서 ε Eri b 는 Jupiter 보다 약 20% 작은 띠 진
  크림-흰색 jovian — ~1.05 R_Jup = 75 000 km — 으로 읽힙니다.
  belt-zone 대비는 보통 수준 (zone 에 `#e8dac4` 크림-흰, belt 에
  `#c4a878` 따뜻한 크림-갈색) 으로 Jupiter 만큼 강렬하지 않지만
  중간 렌더 거리에서는 가시적. 지속적인 zonal banding (~5 개의 belt
  와 zone) 이 가시 디스크의 ~85% 를 덮음.
- **구름 데크 세부.** 암모니아 얼음 구름 zone 이 옅은 cyclonic eddy
  와 함께 매끄러운 크림-흰 띠로 나타남. Jupiter 의 Great Red Spot
  같은 등가물은 제약되지 않으므로 cfg 는 시각 관심을 위해 몇 개의
  작은 폭풍 vortex (drift 시그너처만) 를 채택. 띠는 동서로 흐르며,
  10 h 자전 + 1.05 R_Jup 반지름에서 행성의 코리올리 파라미터에
  맞춰 폭이 스케일된 위도 띠 패턴.
- **극지방.** 제약 없음. tie-break 미적. cfg 는 Saturn 의 극 hexagon
  형태에서 영감을 받은 옅은 cyclonic polar hood 구조를 렌더하되
  특정 기하 패턴을 확정하지는 않음.
- **Limb haze.** K2V 조명 하의 암모니아 구름 데크에서 산란된
  Rayleigh + Mie 가 만드는 약 20–40 km 두께의 옅은 크림-탄 limb
  글로 (`#d8c098`). 그 위에 day-night terminator 에서 미묘한 흡수를
  더하는 얇은 톨린 haze 층 (`#b08858`) 이 덮임.
- **오로라 고리.** 고자기 위도 (cfg 에서 ~70°) 의 북남 양극 모두에서
  옅은 H-Balmer α 적-분홍 (`#c84080`) 오로라 고리가 보임. ε Eri 의
  강화된 항성풍을 고려하면 Jupiter 의 가시광 오로라보다 더 밝을
  법함. nightside 각도에서만 보이며, dayside 에서는 구름 데크에
  가려짐.
- **하늘의 별.** ε Eridani 는 ε Eri b 에서 0.112° 시지름 — Earth 에서
  본 Saturn 의 시지름과 비슷 — 으로 K2V `#ffd9a8` 짙은 주황색의 점/
  디스크로 나타남. 20 R_planet 의 가상의 큰 위성에서는 행성 자체가
  하늘을 ~5.7° 로 지배하고 별은 근처의 강렬한 주황 핀포인트로 축소.
- **하늘의 자매 행성.** Mawet 2019 coronagraphic 미검출 이후 ε Eri
  시스템에서 확인된 다른 행성은 없음. ~20 AU 의 중간 debris belt 와
  ~64 AU 의 차가운 고리는 ε Eri b 시점에서 큰 일심 위상각에서만
  옅은 확산 글로 띠로 보이며, 분리된 동반체는 검출되지 않음.
- **고리 시스템.** 고리 없음 (cfg `ring_present = false`). Mawet 2019
  Ms-band 촬영은 3.5 AU 분리에서 Saturn 밝기 고리 시스템을 검출
  했어야 함. 미검출이 medium confidence 로 `ring_present = false`
  설정 (Jupiter 만큼 약한 고리는 Mawet 검출 임계값 아래이며 배제되지
  않음).
- **Hill sphere 맥락.** r_H ≈ 0.224 AU = 447 R_planet. 상당한 위성
  집단을 수용할 만큼 큼. cfg 는 특정 위성을 확정하지는 않음 (이번
  Phase 3 의 scope 밖) 그러나 Hill sphere 범위 자체가 영향 권역
  경계의 옅은 구로 렌더될 때 시각적 landmark.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Hatzes A. P. et al. 2000** — *Evidence for a Long-Period Planet
  Orbiting ε Eridani*, ApJ 544, L145 (`2000ApJ...544L.145H`). 원래의
  시선속도 발견 논문. 초기값 P ≈ 6.85 yr, M sin i ≈ 0.86 M_Jup 을
  설정 (이후 정밀화됨).
- **Quillen A. C. & Thorndike S. 2002** — *Structure in the ε Eridani
  Dusty Disk Caused by Mean Motion Resonances with a 0.3 Eccentricity
  Planet at 40 AU*, ApJ 578, L149 (`2002ApJ...578L.149Q`). 차가운
  고리 이심률에서 외부 "ε Eri c" 를 추론한 역사적 시도. Mawet 2019
  직접 촬영으로 배제되었으나 다중 belt 조각 sculpting 맥락에서 중요.
- **Benedict G. F. et al. 2006** — *The Extrasolar Planet ε Eridani b.
  Orbit and Mass from Combined Astrometric and Spectroscopic Data*,
  AJ 132, 2206 (`2006AJ....132.2206B`). HST FGS 천체측정 시도. 직접
  촬영으로 대체되었으나 질량 결정 체인에서 역사적으로 중요.
- **Mawet D. et al. 2019** — *Deep Exploration of ε Eridani with
  Keck Ms-band Vortex Coronagraphy and Radial Velocities*, AJ 157,
  33 (`2019AJ....157...33M`, [arXiv:1810.03794](https://arxiv.org/abs/1810.03794)). L′ / Ms band 에서의
  ε Eri b 직접 촬영 확정. 30 AU 외부에서 행성 질량 > 0.3 M_Jup 의
  외부 ε Eri c 배제. hot-start 인플레이션 jovian 모델을 배제하는
  열방출 상한 제약. **핵심 관측 논문**.
- **Llop-Sayson J. et al. 2021** — *Constraining the Orbit and Mass
  of ε Eridani b with Radial Velocities, Hipparcos IAD-Gaia DR2
  Astrometry, and Multi-epoch Vortex Coronagraphy Upper Limits*,
  AJ 162, 181 (`2021AJ....162..181L`).
  RV + Hipparcos/Gaia 천체측정 결합 fit. 진질량
  M_b = 0.66 (+0.12/−0.09) M_Jup, i = 78.81° (+29.34/−22.41),
  a = 3.48 AU. **핵심 관측 논문**.
- **Roettenbacher R. M. et al. 2022** — *No Reliable Astrometric
  Detection of ε Eridani b*, AJ 163, 19 (`2022AJ....163...19R`,
  [arXiv:2110.10643](https://arxiv.org/abs/2110.10643)). 여러 미션에 걸친 천체측정 cross-check. 개별
  시그널은 marginal 하지만 디스크 평면 coplanarity 논증과 결합하면
  Llop-Sayson 의 RV 전용 78.8° 보다 i ≈ 34° 를 선호.
- **MacGregor M. A. et al. 2015** — *ALMA Observations of the
  Debris Disk around ε Eridani*, ApJ 809, L47
  (`2015ApJ...809L..47M`, [arXiv:1505.03879](https://arxiv.org/abs/1505.03879)). ALMA 1.3 mm 촬영이
  차가운 고리를 64.4 ± 0.5 AU 에서 e ≈ 0.07 로 분해. 디스크 경사각
  기준 좌표계 제공.
- **Booth M. et al. 2017** — *The Northern arc of ε Eridani's
  Debris Ring as seen by ALMA*, MNRAS 469, 3200
  (`2017MNRAS.469.3200B`, [arXiv:1705.05868](https://arxiv.org/abs/1705.05868)). 다중 파장 분해. 삼중
  belt 구조. 차가운 고리 경사각 34 ± 2° — ε Eri b 의 궤도면과 일치
  하는 canonical 경사각 기준.
- **Su K. Y. L. et al. 2017** — *The Inner 25 AU Debris Distribution
  in the ε Eri System*, AJ 153, 226 (`2017AJ....153..226S`,
  [arXiv:1703.10330](https://arxiv.org/abs/1703.10330)). "Genie" 다중 belt 조각 sculpting 모델. 3 AU
  asteroid analog 와 20 AU 중간 belt 사이의 inner-gap sculptor 로
  ε Eri b 를 지목. **`companion_position_relative_belts` 결정을
  구동.**

### Read (context / methodology, not decision-driving)

- **Burrows A. et al. 2003** — *Beyond the T dwarfs* 와 관련 차가운
  jovian 진화 트랙 (`2003ApJ...596..587B`). 0.5–1.5 M_Jup 행성의
  질량-반지름-나이 트랙. 0.66 M_Jup, 0.44 Gyr 에서 ε Eri b 의 반지름
  과 내부 광도 추정에 사용.
- **Fortney J. J. et al. 2007** — *Planetary Radii across Five
  Orders of Magnitude in Mass and Stellar Insolation* (`2007ApJ
  ...659.1661F`). ε Eri b 의 반지름 선택과 관련된 질량-나이 윈도우
  에서 Burrows 트랙을 확인.
- **Spiegel D. S. & Burrows A. 2012** — *Spectral and Photometric
  Diagnostics of Giant Planet Formation Scenarios* (`2012ApJ...745
  ..174S`). hot-start 대 cold-start jovian 진화 트랙. Mawet 2019
  대비 측정이 ε Eri b 의 hot-start 트랙을 배제.
- **Lodders K. 2003** — *Solar System Abundances and Condensation
  Temperatures of the Elements* (`2003ApJ...591.1220L`). protosolar
  풍부도 기준. 대기 조성 디폴트를 구동.
- **Atreya S. K. et al. 1999** — *A comparison of the atmospheres
  of Jupiter and Saturn* 과 관련 응결 화학 참고. 암모니아 / 물 구름
  데크 고도 프레임워크 설정.
- **Lewis J. S. 1969** — *The clouds of Jupiter and the NH₃-H₂O
  and NH₃-H₂S systems* (`1969Icar...10..365L`). 원래의 열화학
  구름 데크 시퀀스. 현대 jovian 대기 모델링에서도 여전히 사용되는
  프레임워크.
- **Sromovsky L. A. et al. 2007** — Jupiter/Saturn 대류 구동과
  belt-zone 진폭 스케일링. Jupiter 와 Saturn 에 대비한 ε Eri b 의
  belt-zone 대비 추정에 사용.
- **Khare B. N. et al. 1984** — *Optical constants of organic
  tholins produced in a simulated Titanian atmosphere* (`1984Icar
  ...60..127K`). 실험실 톨린 화학. 광화학 haze 색조 선택에 사용된
  흡수 시그너처.
- **Hörst S. M. et al. 2018** — *Haze Production Rates in Super-
  Earth and Mini-Neptune Atmosphere Experiments* (`2018Natur
  ...2..303H`). sub-Neptune 톨린 화학을 jovian 으로 확장. Jupiter
  대비 haze 광학적 깊이 스케일링을 구동.
- **Moses J. I. et al. 2005** — *Photochemistry of Saturn's
  atmosphere* (`2005JGRE..110.8001M`). Saturn UV 광화학 기준. K2V
  FUV 하의 ε Eri b 로 스케일.
- **Wood B. E. et al. 2002** — *Measured Mass Loss Rates of Solar-
  like Stars as a Function of Age and Activity* (`2002ApJ...574
  ..412W`, arXiv:astro-ph/0203437). ε Eri 의 질량 손실률 ~30× 태양.
  자기권 구동 강도를 구동.
- **France K. et al. 2018** — *The MUSCLES Treasury Survey* K 왜성
  확장 (`2018ApJS..239...16F`). ε Eri 의 FUV / Lyα flux. 광화학
  강도 추정을 구동.
- **Reiners A. & Christensen U. R. 2010** — *A magnetic field
  evolution scenario for brown dwarfs and giant planets*
  (`2010A&A...522A..13R`, [arXiv:1007.1514](https://arxiv.org/abs/1007.1514), cached). jovian 에 대한
  에너지플럭스 다이나모 스케일링. cfg 의 660 μT 자기장의 근거다 (젊은
  거대 행성은 Jupiter 보다 약한 게 아니라 더 강하다). Christensen,
  Holzwarth & Reiners 2009 (`2009Natur.457..167C`) 의 스케일링 법칙
  위에 세워졌다.
- **Metcalfe T. S. et al. 2013** — *Magnetic Activity Cycles in the
  Exoplanet Host Star ε Eridani*, ApJ 763, L26
  (`2013ApJ...763L..26M`, [arXiv:1212.5343](https://arxiv.org/abs/1212.5343)). ~2.95 년 채층 활동
  사이클의 최초 보고. Open items 에 적힌 사이클 위상 자기권 구동
  동기화를 구동. (b-bibliography 에는 미fetch. host Phase 3 에서
  인용.)
- **Coffaro M. et al. 2020** — *A solar-like magnetic cycle on the
  mature K-dwarf 61 Cygni A and the X-ray cycle of ε Eridani*, A&A
  636, A49 (`2020A&A...636A..49C`, [arXiv:2002.11009](https://arxiv.org/abs/2002.11009)). ε Eri b 궤도
  에서 wind 구동을 변조하는 X 선 사이클 진폭을 정밀화. (host
  bibliography `eps-eri.yaml` 에 핀됨, status fetched. b 용으로는
  별도 핀 안 됨.)
- **Canup R. M. & Ward W. R. 2002** — *Formation of the Galilean
  Satellites: Conditions of Accretion*, AJ 124, 3404
  (`2002AJ....124.3404C`). circumplanetary-disk 위성 강착
  프레임워크. 추측성 위성 시스템 Open item 의 맥락. (b-bibliography
  에는 미fetch.)

### Read (instrument / non-cfg-decisive)

- **Snellen I. A. G. et al. 2014** — *Fast spin of the young
  extrasolar planet β Pictoris b* (`2014Natur.509...63S`). 도플러
  확장 분광 기법. ε Eri b 에는 아직 적용 안 됨.
- **Drossart P. et al. 1989** — *Detection of H₃⁺ on Jupiter*
  (`1989Natur.340..539D`). ε Eri b 의 향후 오로라 검출 채널로서의
  H₃⁺ 방출.
- **Clarke J. T. et al. 1996, 2009** — Jupiter HST FUV 오로라 관측.
  ε Eri b 에 스케일된 오로라 oval 기하 기준 제공.
- **Bonfond B. 2017** — *Jovian auroral aspects* (`2017JGRA
  ...122.4548B`). Jupiter 오로라 oval 위도 기준.
- **Wong M. H. et al. 2004** — *Updated Galileo probe abundance
  measurements* (`2004Icar..171..153W`). Jupiter CH₄ / NH₃ 풍부도
  기준. cfg 가 Jupiter analog 값 채택.
- **Hanel R. A. et al. 1983, Li L. et al. 2018** — Saturn Bond
  알베도 측정 (`1983Icar...53..262H`. `2018NatCo...9.3709L`).
  차가운 jovian Bond 알베도 tie-break 기준값.
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*
  (`1966Icar....5..375G`). 조석 잠금 시간 척도 계산을 위한 조석
  소산 Q factor 기준.

### Not read — no arXiv preprint or low-priority (~30 papers)

- Hatzes 2013 follow-up RV 모니터링 — Llop-Sayson 2021 의 결합 분석
  으로 대체.
- 2000년대 ε Eri b 활동도-오염 반박 시리즈 (Anglada-Escudé 2012.
  Zechmeister 2013) — 역사적 맥락. Mawet 2019 직접 촬영 확정으로
  대체.
- ε Eri b 위성 시스템 추측 논문 — 관측적 동기 없음. 첫 패스 Phase
  3 의 scope 밖.
- ε Eri 표적 SETI / 레이저 방출 검색 (Marcy 2022. Tusay 2022. Saide
  2023) — host Phase 3 에서 이미 인용. b 에 무관.

host star Phase 3 audit trail 은 `phase3/eps_eri/system.yaml` 과
워크스페이스 노트에 보존되지만, 핀된 bibliography
(`docs/phase3/_bib/eps-eri.yaml`) 는 항성 논문만 담고 있으며 행성 b
항목은 하나도 없습니다. 행성 b 논문 집합 (Hatzes 2000, Mawet 2019,
Llop-Sayson 2021, Roettenbacher 2022, Booth 2017, Su 2017) 은 이
문서 위쪽의 자체 Bibliography 에 인용되어 있으나 아직
`docs/phase3/_bib/eps-eri-b.yaml` 로 핀/캐시되지 않았습니다. 전용
b-bibliography fetch 는 follow-up 패스입니다.

## Open items for follow-up

- **JWST coronagraph 분광 of ε Eri b (Cycle 4+)** — NIRCam 또는
  MIRI coronagraph 가 4–5 μm 에서 첫 열방출 스펙트럼을 산출할 수
  있고, T_eff, CH₄/NH₃ 풍부도 비율, 광화학 haze 광학적 깊이를
  제약. 검출되면 `atmosphere_composition`, `photochemical_haze_present`,
  `bond_albedo` Decisions 행을 스펙트럼에서 재유도.
- **도플러 확장 자전 측정** — VLT/CRIRES+ 나 ELT/HARMONI 가 ~1.1
  arcsec 분리에서 행성의 열 대비를 추출할 수 있다면 v sin i 를
  측정 가능. 현재 10 h 자전 주기는 윈도우 내 tie-break. 측정되면
  Confidence 가 low 에서 high 로 이동.
- **경사각-DB 일관성**. cfg 는 Llop-Sayson/DB 값 i = 78.81° (RV +
  Hipparcos/Gaia 천체측정. 경사각 marginalize 됨) 를 채택합니다.
  디스크 coplanar i ≈ 34° (Booth 2017 고리. Benedict 2006 30°) 는
  약 1σ 에서 허용되며, 향후 Phase 2 가 보유할 수 있는 대안 시나리오
  로서 여기에 보존됩니다.
- **위성 시스템 Phase 3**. Hill sphere 반경 ~0.224 AU 는 상당한 위성
  집단을 수용할 만큼 큼. 향후 Phase 3 follow-up 이 (a) protoplanetary
  disk circumplanetary-feeding 맥락 (Canup 2002) 과 (b) 향후 ALMA/
  JWST circumplanetary-disk 먼지 제약을 기반으로 5–50 R_planet
  범위의 얼음/암석 위성을 추측 가능. 이번 첫 패스 Phase 3 의 scope
  밖.
- **고리 시스템 tie-break 보존**. cfg 는 Mawet 2019 Ms-band 의
  Saturn 밝기 고리 미검출에 기반해 `ring_present = false` 를 선택.
  Jupiter 만큼 약한 고리 시스템은 Mawet 검출 임계값 아래이며 배제
  되지 않음. 옅은 고리를 선호하는 사용자를 위한 대안 cfg variant
  로서 여기에 보존.
- **사이클 위상 자기권 구동 동기화**. host star 의 2.95 년 활동
  사이클 (Metcalfe 2013) 이 ε Eri b 궤도에서 약 4 배의 wind 구동
  변조를 만듦 (Coffaro 2020 X 선 사이클 진폭). 향후 cfg 개정이
  오로라 강도 렌더링을 host 사이클 epoch 에 위상 잠금하여 플레이
  연도에 걸쳐 일관된 타이밍을 보이게 할 수 있음 — host eps-eri.md
  Open items 에 플래그된 같은 enhancement.
- **Phase 2 `disk_measurements`/`planet_atmosphere_measurements`
  ingest**. ε Eri b 는 현재 DB 에 Phase 2 대기 블록이 없음. DB
  스키마가 확장되거나 (혹은 `db/planets_atmospheres/` companion
  이 도입될 때) Mawet 2019 열방출 상한과 향후 JWST 측정이 위 cfg
  픽과 일치하는 `recommended` 플래그로 `atmosphere_measurements`
  레코드로 ingest 되어야 함.

## Related

- [eps-eri](eps-eri.md) — host star Phase 3 합성. M_star / R_star /
  L_star / age / 디스크 평면 기준 좌표계와 자기권 구동을 구동하는
  사이클 활동 맥락을 제공
- [tau-cet](tau-cet.md) — 분해된 차가운 debris 고리를 가진 metal-
  poor G8V solar analog 의 host. "분해된 디스크를 가진 가까운 행성
  보유 별" 맥락의 비교 대상
- [fomalhaut](fomalhaut.md) — 분해된 debris 고리와 역사적
  "Fomalhaut b" 직접 촬영 후보를 가진 A3V host. 분해된 디스크 시스템
  에서 직접 촬영 확정된 동반체의 비교 대상
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 이 jovian 의 대기
  + 자기권 결정을 소비하는 downstream Kopernicus / EVE / Scatterer
  cfg writer
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) —
  단일 별 천체측정 전용. ε Eri 는 이중 궤도 전파를 필요로 하지
  않음
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX
  는 ε Eri 에 대해 jovian 없는 기본 항성 항목만 가지고 있음. ε Eri
  b 는 NearStars 전용의 Phase 3 추가
