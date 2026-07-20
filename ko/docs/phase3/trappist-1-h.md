<!-- TRAPPIST-1 h Phase 3 합성: cfg-ready 결정과 근거 -->
# TRAPPIST-1 h — Phase 3 Synthesis

TRAPPIST-1 h 는 M8V ultra-cool dwarf 를 18.77 일 주기로 도는 0.76 R⊕,
0.33 M⊕ 의 sub-Mars 질량 암석 행성입니다. 7 행성 중 가장 바깥에 있고
지구 insolation 의 0.16 배만 받습니다. K2 mission 데이터를 쓴 Luger
2017 ([1703.04166](https://arxiv.org/abs/1703.04166)) 이 궤도 주기와 공명 체인 내 위치를 확정했고,
Gressier 2022 ([2112.05510](https://arxiv.org/abs/2112.05510)) 가 최초의 HST WFC3/G141 근적외 transmission
스펙트럼을 얻어 cloud-free 한 수소 풍부 대기를 배제했습니다. JWST
후속 관측은 2026-05-22 기준 아직 출판되지 않았습니다. h 의 흥미로운
반전은 따로 있습니다. Lincowski 2018 ([1809.07498](https://arxiv.org/abs/1809.07498)) 은 **건조된
(desiccated)** h 가 10–100 bar 의 O₂ + CO₂ post-runaway 시나리오에서는
maximum-greenhouse 거리 바깥에서도 거주 가능한 표면 온도를 유지할 수
있다고 지적했고, 이 때문에 h 는 시스템에서 가장 반직관적인 거주
가능성 후보가 됩니다.

**NearStars 시나리오 선택. 풍화된 기반암 위에 patchy 한 CO₂ + N₂
얼음 서리가 깔린 얼어붙은 sub-Mars 암석 세계, 그리고 후기 outgassing
으로 남은 매우 얇은 (~0.005 bar) 잔여 대기.** 저질량 행성이 낮은
insolation 환경에 놓였을 때 휘발성 물질이 대부분 손실되거나 표면에
얼어붙는다고 보는 cosmic-shoreline 문헌(Castan-Lopez 2025, Zahnle
2017) 의 보수적 해석을 따른 것입니다. 대안인 Lincowski 2018 의
"건조된 거주 가능" 시나리오는 cfg 변형으로만 남겨두는데, 따뜻하고
건조한 암석 표면 위 두꺼운 CO₂/O₂ 대기는 시각적으로 덜 구분되기
때문입니다.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 18.77 d 궤도와 조석 damping, Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping, Agol 2021 |
| `eccentricity` | 0.00567 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 339 | medium | Agol 2021 (이심률이 낮아 제약이 약함) |
| `sidereal_period_days` | 18.7729 | high | Agol 2021, Luger 2017 K2 확정 |
| `semi_major_axis_au` | 0.06189 | high | Agol 2021 |
| `mass_mearth` | 0.326 | high | Agol 2021 TTV — sub-Mars 급 (Mars 0.107, Mercury 0.055) |
| `radius_rearth` | 0.755 | high | Agol 2021, Gressier 2022 transit fit |
| `surface_gravity_g_earth` | 0.572 | high | derived = 0.326 / 0.755² |
| `density_g_cc` | 4.20 | high | Agol 2021 (water-rich) |
| `water_mass_fraction` | 0.03–0.10 | medium | 이전의 0.05–0.15 에서 좁혔습니다. Lichtenberg 2019 의 ²⁶Al 건조화 논거가 하한 쪽을 지지하고, Bourrier 2017 의 짧은 runaway 단계(33–67 Myr) 가 축적된 물의 대부분을 보존합니다 |
| `insolation_s_earth` | 0.144 | high | Agol 2021 / Gillon 2024 ([2401.11815](https://arxiv.org/abs/2401.11815)) — 이전 라운드의 0.16 에서 보정됨 |
| `equilibrium_temp_k` (A=0)   | 169 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, frosted) | 142 | high | derived. 서리 덮인 표면 케이스 |
| `bond_albedo` | 0.40 | medium | 기반암 + CO₂/N₂ 서리 혼합으로, full snowball 보다는 덜 반사적 |
| `surface_temp_substellar_k` | 175 | medium | 수동 복사 평형 + 미량 대기의 약한 온실 효과 |
| `surface_temp_nightside_k` | 60 | medium | 매우 차가워서 N₂ 얼음 서리점에 도달 |
| `surface_temp_global_mean_k` | 140 | medium | 얇은 대기로 인한 약한 재분배 |
| `atmosphere_present` | true (very tenuous) | low | Gressier 2022 가 H₂-rich 대기를 배제했고, 미량의 outgassed CO₂ + N₂ 는 가능 |
| `atmosphere_surface_pressure_pa` | 500 | low | 0.005 bar — 최소 잔여, Mars-thin 수준 |
| `atmosphere_composition` | N₂ ~90%, 미량 CO₂ 10–100 ppm, Ar / H₂O 미량 | low | Bolmont 2018 review 가 배경 가스와 무관하게 p_CO₂ 분압을 100–1000 ppm 으로 한정하고, Turbet 2017 은 h 의 표면 온도 영역(1 bar N₂ 배경) 에서 "수십 ppm 수준" 으로 더 좁힙니다. pure-CO₂ 평형은 145 K 에서 4 mbar 인데 N₂ 배경에서는 기체상 미량 CO₂ 가 훨씬 낮아집니다 |
| `atmosphere_scale_height_km` | 6.0 | medium | derived. kT/μg 로 T≈140 K, μ=40, g=5.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#302820` (Rayleigh 산란 사실상 인지 불가) | low | 매우 얇은 대기 + M-dwarf SED 이므로 산란 무시 가능 |
| `cloud_cover_fraction` | 0.02 | low | 최소 — 산발적인 CO₂ 얼음 권운만 |
| `cloud_tint_rgb_hex` | n/a | high | cfg 에 반영할 만큼의 구름이 안 됨 |
| `ocean_present` | uncertain (wmf 상한이면 sub-glacial 가능) | low | 저질량 + 저온이라 g 보다 기저 용융이 적고, 있더라도 얇은 Europa 형 |
| `surface_ice_caps` | 전역적인 H₂O 얼음 덮개와 그 아래 매장된 CO₂ 얼음, substellar 부근 소량 기반암 노출 | medium | Turbet 2017 ([1707.06927](https://arxiv.org/abs/1707.06927)) 은 h 표면의 CO₂ 얼음이 중력적으로 불안정하여 지질학적 시간 척도에서 H₂O 얼음 껍질 아래로 매장된다고 보입니다. 표면 서리는 H₂O 얼음이 지배적이고 CO₂ 얼음은 더 깊은 층으로 존재합니다 |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-dwarf 조명 아래 H₂O 얼음 / 눈) | medium | 표면은 H₂O 얼음이 지배적(Turbet 2017 매장 논거) 이며, 철-풍부 기반암은 국소적인 substellar 영역에서만 노출됩니다. Mars-Pluto 하이브리드 프레이밍과 색 팔레트가 반전되어 크림-화이트가 지배적, 어두운 기반암이 보조 accent 가 됩니다 |
| `surface_tint_rgb_hex_accent` | `#3a2c20` (풍화된 철-풍부 기반암 — 보조, substellar 한정) | low | 표면은 H₂O 얼음이 지배적(Turbet 2017 매장 논거) 이며, 철-풍부 기반암은 국소적인 substellar 영역에서만 노출됩니다. Mars-Pluto 하이브리드 프레이밍과 색 팔레트가 반전되어 크림-화이트가 지배적, 어두운 기반암이 보조 accent 가 됩니다 |
| `surface_morphology` | substellar 근방의 cratered 고대 기반암, terminator 와 nightside 쪽으로 patchy 한 CO₂/N₂ 얼음 서리 | medium | Mars/Mercury analog, resurfacing rate 가 매우 낮음 |
| `magnetic_field_present` | false (저질량 + 저온 + 느린 자전) | low | 활동성 다이나모 없을 가능성, 작은 화석 자기장은 여지 있음 |
| `induction_heating_w_m2` | 0.001–0.01 | medium | Grayver 2022 — 거리와 작은 질량 때문에 시스템에서 가장 낮음 |
| `tidal_heating_w_m2` | 0.00001–0.0001 | medium | Bolmont 2020 — h 에서는 무시할 만함 |
| `radiogenic_heat_w_m2` | 0.025 | low | 지구형 BSE(bulk-silicate-Earth) 방사성 열류속(현재값 ~0.04 W/m²)을 질량으로 스케일(이 저질량 바디에서는 지구형보다 약간 낮음). 방법은 Wang et al. 2020 (`2020A&A...644A..19W`)의 외계행성 방사성 열 프레임워크를 따름. 다만 Eu→Th/U 호스트 원소비 보정은 호스트별 원소비를 큐레이션하지 않아 적용하지 않았고, 대신 지구형 원소비를 가정함 |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | sub-Mars 질량(0.33 M⊕) 이라 다이나모가 거의 꺼졌을 가능성. Mars 와 유사한 지각 잔류 자기장만 남음 |
| `magnetic_dipole_moment_normalized_earth` | 0.005 | medium | [2208.06523](https://arxiv.org/abs/2208.06523) 의 thermal evolution + RM22. 저질량 행성은 1 Gyr 이내에 다이나모 셧다운에 도달 |
| `magnetic_dipole_tilt_deg` | 10 | low | tie-break 으로 10° offset. Mars 처럼 명확한 dipole 축 없이 지각 이상(crustal anomaly) 지배 가능성 |
| `magnetosphere_standoff_planet_radii` | 1.2 | medium | 전역 자기권 사실상 없음. Venus/Mars 와 같은 induced magnetosphere 만 존재하고 ionopause 의 standoff 는 R_planet 근방 |
| `radiation_belt_present` | false | high | 자기장이 지구의 0.1 배 미만이라 Van-Allen 형 trapped 영역 자체가 없음 |
| `surface_radiation_dose_msv_yr` | 4000 | low | Atri 2019 ([1910.09871](https://arxiv.org/abs/1910.09871)) 의 스케일링을 0.062 AU 의 h 에 적용. shielding 이 약해 GCR 배경이 지배. Atri 가 보고하는 값은 event 당 Gray + 무차원 enhancement-over-GCR 계수이지 연간 mSv/yr 가 아니므로, 이 연간값은 변환 추정 → low |
| `atmospheric_shielding_g_cm2` | 5 | medium | Phase 3 cfg 의 0.005 bar 압력 → 약 5 g/cm² column |
| `aurora_present` | true | medium | 대기 + 지각/induced 자기장 → patchy 한 Mars 형 discrete aurora |
| `aurora_color_primary_hex` | `#4DFF4D` | low | N₂ Vegard-Kaplan bands + 미량 O 가 있으면 [NI] 520 nm green. tie-break 으로 UV-only 가 아닌 visible green 채택 |
| `aurora_color_secondary_hex` | `#B19CD9` | low | N₂ Lyman-Birge-Hopfield bands 가 UV 로 인지되는 violet |
| `aurora_emission_species_primary` | `N₂ Vegard-Kaplan bands 200–300 nm + N₂⁺ 391.4 nm + N₂ Lyman-Birge-Hopfield` | low | 얇은 N₂ 지배 대기 |
| `aurora_oval_magnetic_latitude_deg` | 15 | low | 조직된 dipole 이 없으니 patchy 한 지각 aurora 가 무작위 위도에 발생. 대표값 |
| `aurora_intensity_kR_typical` | 30 | low | 가장 얇은 대기 + 가장 약한 자기장. 입자 한 개당은 밝지만 충돌 대상이 적음 |
| `star_apparent_angular_diameter_deg` | 1.03 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 h 는 시스템에서 가장 작은 행성(0.326 M⊕, sub-Mars 질량)
이며 insolation 은 0.16 S⊕ 입니다. 작은 질량, 낮은 중력(0.572 g),
낮은 insolation 의 조합 때문에 h 는 대기 유지에 까다로운 케이스
입니다. cosmic shoreline 문헌(Castan-Lopez 2025 — [2504.19872](https://arxiv.org/abs/2504.19872) — ,
Zahnle 2017) 은 h 를 수소 함유는 물론 질소 함유 대기에 대해서도
경험적 유지 임계값 근처 또는 그 아래에 놓고 있습니다. 일부 휘발성
유지는 그럴듯한데, CO₂ 정도면 h 의 온도에서 Jeans 탈출을 견딜 만큼
분자량이 충분히 크지만, 대기 질량 자체는 작을 가능성이 높습니다.

저질량임에도 h 의 bulk 밀도(Agol 2021 의 4.20 g/cc) 는 비자명한 물
질량 분율(~5–15%) 을 함의할 만큼 낮습니다. f, g 와 비슷한 양상이지만
이쪽은 활용 가능한 전체 질량이 훨씬 적습니다. 이 물의 대부분은 표면
얼음 형태(CO₂ + H₂O 얼음) 이거나 작은 암석 코어 위 얇은 sub-glacial
층으로 격리되어 있을 가능성이 큽니다.

Lincowski 2018 ([1809.07498](https://arxiv.org/abs/1809.07498)) 의 "건조된 h" 시나리오 — 두꺼운(10–100
bar) CO₂/O₂ post-runaway 대기가 거주 가능한 표면 온도를 만드는 경우
— 는 cfg 변형으로 남겨두지만 정규 선택은 아닙니다. h 의 탈출 속도에
서 post-runaway 대기 유지 시간 척도가 짧고(≲ 1 Gyr), 7.6 Gyr 의
시스템 나이 동안 초기 두꺼운 대기는 대부분 손실되었을 것이기 때문
입니다.

표면 형태는 Mars-Pluto 하이브리드 analog 를 채택합니다.

- **Substellar 영역** (substellar 에서 ~0–60°). 기반암이 지배하며,
  Mars 의 남부 고원과 유사한 풍화된 철-풍부 표면. 그늘진 분화구
  내부에는 일부 patchy 한 CO₂ 서리.
- **Mid-zone** (60–120°). substellar 로부터 멀어질수록 서리 덮개가
  증가.
- **Terminator** (~90°). 서리-기반암 대비가 크고, 비스듬히 들어오는
  2566 K 빛 아래로 긴 지형 그림자가 깔림.
- **Nightside** (>120°). 주로 ~60 K 의 CO₂ + N₂ 서리 덮개, 능선
  꼭대기에 가끔 어두운 기반암 patch.

**색 선택 — H₂O 얼음 지배.** Turbet 2017 은 h 의 대기가 저압에서
미량 CO₂ 에 의해 지배된다 해도 표면 서리 조성은 **주로 H₂O 얼음**
이라는 점을 보입니다(이전에 가정한 CO₂/N₂ 서리가 아닙니다). CO₂
얼음 퇴적은 일시적으로 형성되지만 중력적으로 불안정해서 지질학적
시간 척도에서 H₂O 얼음 껍질 아래로 매장됩니다. 가시 표면은 따라서
M-dwarf 조명 아래의 깨끗한 H₂O 얼음에서 오는 크림-화이트(`#d8d0c4`)
가 되고, 풍화된 철-풍부 기반암 패치(`#3a2c20`) 는 얼음이 승화된
국소 substellar 영역에서만 노출됩니다. Mars-Pluto 하이브리드 프레임
은 반전됩니다. 전역적으로는 크림-화이트가 지배적이고, 어두운 기반암
이 표면의 주된 색조가 아니라 보조 accent 가 됩니다.

**내부 구조.** Barr 2018 ([1712.05641](https://arxiv.org/abs/1712.05641)) 은 h 가 1030 km 의 암석 코어
(평균 밀도 케이스) 를 갖는다고 봅니다. 최대 밀도 구성이면 암석 위로
H₂O 껍질이 ~100 km 만 허용됩니다. 현재 cfg 의 WMF 0.03–0.10 은 이
두 극단 사이에 위치합니다. h 의 CMF 는 시스템에서 낮은 쪽(~0.23)
으로, 상대적으로 철이 적은 암석체와 일관됩니다.

**Mars 형 patchy 오로라 지오메트리.** 조직된 전역 다이나모가 없는
상태(7.6 Gyr 동안 얼어붙은 sub-Mars 코어) 에서 h 의 자기장은 국소적
패치 형태의 **지각 잔류 자기장** 이 지배합니다. Mars 의 상황과 그대로
대응됩니다(Acuña 1999 의 MAG/ER 발견). 얇은 N₂ 대기와 합쳐지면 지구
나 g 에서 보이는 규칙적인 auroral oval 대신 *patchy* 한 오로라
지오메트리가 만들어집니다. 각각의 지각 자기 이상이 stellar-wind 입자
를 자기장이 강한 지역 위로 깔때기처럼 끌어들여 그 위에 국소 오로라
스폿을 만들고, 결과적으로 N₂ Vegard-Kaplan green + N₂⁺ violet 가
산발적으로 흩어져 빛납니다. 어디서 어떻게 켜질지는 사실상 무작위로,
지각 자화가 살아남은 자리마다 한 점씩 떠오릅니다. 내행성들의 조직된
auroral band 와는 시각적 인상이 완전히 다릅니다. cfg 에서는 이걸
`#4DFF4D` green 과 `#B19CD9` violet 가 저-중위도 자기 위도대에
흩어진 점들로 렌더링합니다. 극지방에 몰린 균일한 띠가 아닙니다.
interesting-first tie-break 에서 대안인 "균일하고 흐릿한 전역
glow" 대신 이 Mars 형 렌더링을 선택했습니다.

**기반암 / 산화철.** g, f 와 비교해 h 에서 더 두드러집니다. 노출된
substellar 기반암이 7.6 Gyr 동안 직접 stellar UV 아래에서 광분해
산화를 받아온 결과입니다. primary tint 가 이미 이를 반영하고 있으며,
충돌 분화구 가장자리 부근의 밝은 산화철 패치는 fine-grained PQS
디테일로 좋습니다.

**조석 lock 아래의 모폴로지.** resurfacing 이 거의 없습니다. h 의
조석 가열은 무시할 만하고(Bolmont 2020), induction heating 도
최소이며(Grayver 2022 거리 스케일링), 방사성 열은 화산 활동을
일으키기에 너무 낮습니다(작은 질량). 표면은 시스템 나이 7.6 Gyr 의
충돌 기록을 거의 그대로 보존하며, locked frame 의 leading 반구 쪽
으로 편향됩니다.

## 대기 합성

Gressier 2022 ([2112.05510](https://arxiv.org/abs/2112.05510)) 가 h 의 첫 HST WFC3/G141 transmission
스펙트럼을 제시했고, 이는 현재까지 h 의 유일한 출판된 대기 관측
입니다. 데이터는 대기 없음 또는 flat-spectrum 이차 대기와 일관
하며, cloud-free 한 수소 풍부 대기는 배제됩니다.

이론 모델링은 다음과 같습니다.

- **Lincowski 2018.** h 에 대해 건조된 post-runaway 10–100 bar
  CO₂/O₂ 대기를 검토하고 일부 케이스에서 거주 가능한 표면 온도가
  나오는 것을 확인했습니다. 다만 h 의 탈출 속도에서 7.6 Gyr 동안
  그렇게 두꺼운 대기를 유지할 확률은 낮습니다.
- **Bourgeois 2024.** magma ocean 진화가 초기에 ~1 bar (CO₂ + H₂O)
  의 outgassed 대기를 만들지만, 대부분 시간이 지나면서 손실됩니다.
- **Castan-Lopez 2025.** cosmic shoreline 분석은 h 가 전형적 이차
  대기 유지 임계값 근처 또는 그 아래에 있다고 시사합니다.

NearStars 는 **0.005 bar (Mars-thin) 의 N₂ 지배 + 미량 CO₂ 대기**
를 채택합니다.

- **압력** 0.005 bar (500 Pa). Mars 와 비슷한 수준입니다. 0.3 M⊕
  행성에도 일부 outgassing 은 축적되므로 0 보다는 위에 있어야 하고,
  cosmic-shoreline / Jeans 탈출 제약상 h 가 이보다 많이는 유지하지
  못한다는 점에서 0.01 bar 아래여야 합니다.
- **조성** N₂ 지배(~90%) + 미량 CO₂ (10–100 ppm 으로, 1000 이 아닙
  니다). 근거는 Bolmont 2018 review 의 cold-trap 논거에 더해 Turbet
  2017 의 구체적인 계산입니다. h 의 pure-CO₂ 평형은 145 K 에서 4
  mbar 에 불과하고, N₂ 배경 시나리오에서는 기체상에 "수십 ppm
  수준" 의 CO₂ 만 남습니다. 나머지 ~10% 는 Ar, 서리 순환의 H₂O 증기,
  화석 O₂ 사이에서 분배됩니다.
- **구름.** 최소 (~2% 전역). 드문 CO₂ 얼음 권운 정도.

**ion escape 논거에 의해 대기 유지가 오히려 유리.** cosmic-shoreline
임계값 프레이밍에도 불구하고 Dong 2018 ([1705.05535](https://arxiv.org/abs/1705.05535)) 은 h 가 시스템
에서 가장 낮은 ion escape rate (1.29×10²⁶ s⁻¹) 와 가장 높은 대기
유지 시간 척도(~10¹⁰ yr) 를 갖는다고 봅니다. "h 는 대기 ion 손실의
관점에서 가장 안정적인 행성이어야 한다" 는 결론입니다. h 위치에서의
stellar wind dynamic pressure 는 지구의 "단지" 100–300 배인데, b 에
서는 10³–10⁴ 배입니다. Krissansen-Totton 2022 ([2207.04164](https://arxiv.org/abs/2207.04164)) 도 마찬
가지로 외행성들은 "사실상 모든 모델 시뮬레이션에서 상당한 표면 휘발
성 물질을 유지" 하며 "상당한 대기를 유지하는 모든 행성에서 CO₂ 지배
또는 CO₂-O₂ 대기" 가 된다고 결론짓습니다. cfg 의 얇은 N₂ + 미량 CO₂
선택은 이에 비해 보수적이며, 더 두꺼운(~0.1 bar) 대기도 충분히
방어 가능합니다.

**오로라 화학.** N₂ 가 지배하는 얇은 대기(CO₂ ≲ 100 ppm) 는 깨끗한
질소 오로라 화학을 만듭니다. N₂ Vegard-Kaplan bands 가 200–300 nm
UV 에서 빛나고 일부는 가시광 cyan-violet 쪽으로 산란되며, N₂⁺ 의
391.4 nm First Negative 가 blue, 그리고 Lyman-Birge-Hopfield bands
가 따라옵니다. photolysis 로 미량 O₂ 가 있다면 [OI] 557.7 nm green
도 더해집니다. 위에서 본 지각 이상 지오메트리 때문에 이 방출들은
연속된 띠가 아니라 작은 스폿에 집중됩니다. 강도 ~30 kR 은 매우 얇은
대기 탓에 시스템에서 가장 낮지만, 침투 입자가 얇은 대기 깊숙이까지
들어가기 때문에 개별 스폿의 단위 면적당 밝기는 오히려 높습니다.
cfg 렌더링용으로 정리하면, 조직된 극지 지오메트리 없이 흐릿한
green/violet 패치가 흩뿌려진 모습입니다.

**하늘 외관.** 0.005 bar 대기는 궤도에서는 사실상 보이지 않습니다.
표면에서는 호스트 별(1.03° 각 크기의 적-오렌지 디스크) 을 빼면 하늘
이 검습니다. 0.16 S⊕ 의 표면 조명은 근일점 외곽의 Mars 와 비슷한
수준입니다.

## 자전 & spin 합성

18.77 일 주기에서 7.6 Gyr 동안 조석 damping 이 진행되면 동기(1:1)
구성에 도달하고, 황도 경사각은 0 으로 damping 됩니다. 이심률 0.00567
은 1:1 우세 영역입니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 18.7729 일 (1 621 977 s).

**계절 없음.** 황도 경사각 = 0 이고, libration 으로 인한 insolation
변동도 < 0.5% 입니다.

**공명 체인 동역학.** Luger 2017 ([1703.04166](https://arxiv.org/abs/1703.04166)) 이 7 행성 Laplace 공명
체인 안에서 h 의 위치를 확립했습니다(g 와 8:5 평균 운동 공명). 체인
은 궤도 요소에 지속적인 small-amplitude 섭동을 주지만, 시각적/cfg
목적상 구성은 안정적입니다.

**자기 다이나모 예상.** h 의 작은 질량(0.33 M⊕, sub-Mars), 진전된
나이(7.6 Gyr), 그리고 매우 느린 조석 고정 자전(18.8 d) 이 합쳐지면
지속 가능한 전역 다이나모는 사실상 불가능합니다. [2208.06523](https://arxiv.org/abs/2208.06523)
(Thermal Evolution and Magnetic History of Rocky Planets) 은 ~0.5
M⊕ 이하의 천체가 보통 1–2 Gyr 안에 다이나모를 꺼버린다고 보는데,
h 는 이 시간 척도를 한참 지나 있습니다. 남은 자기 구조는 지각
잔류 — h 가 더 젊고 다이나모가 있었을 때 화석화된 자화 — 이며,
수십억 년의 충돌 가드닝과 열적 변형 끝에 패치들로 흩어진 상태
입니다. 이는 오늘의 Mars 그대로입니다. ~1 μT 의 지각 패치만 있고
전역 dipole 은 없는 상황. 따라서 오로라는 조직된 극지 oval 이 아닌
자화된 지형 위의 국소 스폿에서 발생합니다. RM22 ([2203.01065](https://arxiv.org/abs/2203.01065)) 의
스케일링이 돌려주는 dipole moment 는 지구의 ~0.005 배로, 활동성
다이나모라기보다 잔류 시그니처에 가깝습니다.

**조석 가열 노트.** Makarov 2018 은 h 의 3:2 spin-orbit 포획 확률을
0.017(사실상 0) 로 계산했고 1:1 lock 이 확인되었습니다. 조석 소산
peak 는 Maxwell time ~0.20 d (궤도 주기에 가까움) 에 있어 총
5.3×10¹³ W, 정규화하면 ~7×10⁻³ W/m² 입니다. 이는 현재 cfg 값
0.00001–0.0001 W/m² 보다 1–2 자릿수 더 크므로 실제 flux 를
과소평가하고 있을 수 있습니다.

## 비주얼 스타일

- **전역 외관.** 어두운 적갈색의 암석 세계(`#3a2c20`) 에 patchy 한
  크림-화이트 서리(`#c8b8a0`) 가 깔리고, terminator 와 nightside
  쪽으로 갈수록 서리 비중이 커집니다. 시각적으로는 Mars(적갈색 암석)
  와 좀 더 작은 Pluto(서리 지배) 사이 어딘가입니다.
- **Substellar 영역.** 대부분 기반암이고 풍화된 산화철 갈색입니다.
  cfg PQS 해상도에서 충돌 분화구가 보이며, 그늘진 분화구 내부에는
  일부 서리가 남아 있습니다.
- **Mid-zone.** 기반암과 서리가 섞입니다. 크림 서리 위에 어두운
  갈색이 노출되는 fractal 패턴으로, KSP 저공 비행에 사진발이 좋은
  영역입니다.
- **Terminator.** 비스듬한 2566 K 빛 아래로 대비가 크고, 지형 그림자
  가 cratering 과 가능한 tectonic feature 를 드러냅니다. 서리-기반암
  경계가 가장 선명한 곳입니다.
- **Nightside.** 크림-화이트 서리 덮개(`#c8b8a0`) 위로 능선 꼭대기에
  어두운 기반암 patch 가 노출됩니다. KSP nightside ambient ≈ dayside
  의 1%.
- **Atmosphere haze.** 인지 불가. 0.005 bar 대기는 보일 만한 Rayleigh
  scattering 을 만들지 않고 limb 가 선명합니다.
- **Mars 형 patchy 오로라.** `#4DFF4D` green 과 `#B19CD9` violet 의
  스폿들이 저-중위도 자기 위도대에 흩어집니다. 극지방이 아니라 자화
  된 지각 위에 집중됩니다. 강도 ~30 kR 로 어두운 nightside 에서만
  보이고, 이 점박이 패턴이 h 의 얼어붙은 코어 + 지각-이상-전용
  자기 환경을 그대로 비춰주는 시각 시그니처입니다.
- **하늘의 별.** TRAPPIST-1 이 h 의 하늘에서 1.03° 를 차지하므로
  지구에서 본 태양의 2 배 크기입니다. 표면 조명은 0.144 S⊕ 로 지구
  의 이른 아침 황혼 수준입니다. 적-오렌지 별이 ochre-and-cream 표면
  과 대비를 이루어, 실제로는 대기가 거의 없음에도 h 는 특히 분위기
  있는 외관을 갖습니다.
- **하늘의 자매 행성.** 안쪽으로 한 단계 가까운 g 가 inner
  conjunction 에서 각 크기 ~0.3°. h 의 긴 주기 때문에 conjunction
  자체는 내행성보다 드물게 일어납니다.

## 참고 문헌

### 읽음 (시각 정보 제공, 위 결정 견인)

- **[1703.04166](https://arxiv.org/abs/1703.04166)** Luger 2017 — K2 를 통한 h 의 궤도 주기 발견 / 확인.
  공명 체인의 일곱 번째 행성으로 h 를 확립. 궤도 파라미터의 출처.
- **[2112.05510](https://arxiv.org/abs/2112.05510)** Gressier 2022 — h 의 HST WFC3/G141 transmission
  스펙트럼. cloud-free H₂-rich 대기를 배제. 현재까지 h 에 대한 유일한
  직접 대기 관측.
- **[1809.07498](https://arxiv.org/abs/1809.07498)** Lincowski 2018 — TRAPPIST-1 세계들의 진화된 기후.
  h 는 snowball 과 "건조된 거주 가능" 이상치 양쪽으로 논의됩니다.
  정규-대-변형 시나리오 분기를 견인했고, d/e/f/g 단계에서 이미 읽음.
- **[2510.12794](https://arxiv.org/abs/2510.12794)** Pearce 2025 — Born Dry or Born Wet? Compact
  multiplanet volatile accretion. 충돌 + 탈출 진화 아래에서 h 의
  물 예산을 다룹니다.
- **[2504.19872](https://arxiv.org/abs/2504.19872)** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  h 를 유지 임계값 근처에 놓아 얇은 대기 cfg 선택을 지지.
- **[1707.06927](https://arxiv.org/abs/1707.06927)** Turbet 2017 — TRAPPIST-1 행성들의 기후 다양성, 조석
  동역학, 휘발성 운명. h 의 pure-CO₂ 평형압(145 K 에서 4 mbar) 을
  특정하고, 표면 CO₂ 얼음이 H₂O 얼음 아래로 매장되는 과정을 보임.
  **주요한 표면 조성 수정(CO₂ 서리가 아닌 H₂O 얼음 지배) 의 견인.**
- **[1712.05641](https://arxiv.org/abs/1712.05641)** Barr 2018 — 내부 구조와 조석 가열. h 의 암석 코어
  1030 km, 최대 H₂O 껍질 100 km. 내행성 3 개 다음으로 시스템 내 가장
  낮은 밀도 / CMF.
- **[1705.05535](https://arxiv.org/abs/1705.05535)** Dong 2018 — TRAPPIST-1 행성들의 대기 탈출. h 가
  가장 낮은 ion escape rate 와 ~10¹⁰ yr 의 대기 유지 시간을 가짐.
  **cosmic-shoreline-threshold 프레이밍에 반대 논거.** ion-escape
  물리는 h 가 대기를 유지하는 쪽을 지지합니다.
- **[2207.04164](https://arxiv.org/abs/2207.04164)** Krissansen-Totton 2022 — 결합된 대기-내부 모델.
  사실상 모든 시뮬레이션에서 외행성들이 CO₂ 지배 또는 CO₂-O₂ 대기
  를 가짐을 예측. h 에 비자명한 대기를 유지하는 선택을 지지.
- **[1803.07453](https://arxiv.org/abs/1803.07453)** Makarov 2018 — spin-orbit 조석 동역학. h 의 3:2
  포획 확률 0.017 → 1:1 lock 확인.
- **[1706.04617](https://arxiv.org/abs/1706.04617)** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. 외행성 자기권 맥락 제공.
- **[2203.01065](https://arxiv.org/abs/2203.01065)** RM22 — 암석 행성 다이나모 스케일링. h 의 거의 0 에
  가까운 dipole moment 를 지지.
- **[2208.06523](https://arxiv.org/abs/2208.06523)** Thermal Evolution and Magnetic History of Rocky
  Planets. sub-Mars 질량 행성이 1–2 Gyr 이내에 다이나모를 끄는 점을
  확인.
- **[1910.09871](https://arxiv.org/abs/1910.09871)** Atri 2019 — h 의 표면 dose 테이블.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **[2008.09599](https://arxiv.org/abs/2008.09599)** Bourgeois 2024 — e/f/g 의 magma ocean 진화 (h 에
  직접 적용된 건 아니지만 프레임워크 제공). 이미 읽음.
- **[2508.12865](https://arxiv.org/abs/2508.12865)** 경험적 cosmic shoreline. 맥락.
- **[2507.02136](https://arxiv.org/abs/2507.02136)** Nurturing Atmospheres 를 위한 3D Cosmic Shoreline.
  맥락.
- **[2603.29743](https://arxiv.org/abs/2603.29743)** 새 M Dwarf Cosmic Shoreline 제약. 맥락.
- **[1810.05210](https://arxiv.org/abs/1810.05210)** Moran 2018 — HST haze 한계, h 포함. 이미 읽음.
- **[1810.11255](https://arxiv.org/abs/1810.11255)** Bolmont 2018 review — Constraining the environment
  and habitability of TRAPPIST-1. 직접 인용. "TRAPPIST-1 h 는 표면
  액체 물을 유지할 수 없다. 배경 가스의 양과 무관하게 10²–10³ ppm
  이상의 CO₂ 를 축적하지 못한다." 이 결과가 N₂ 지배 + 미량 CO₂ 로의
  대기 조성 수정을 견인.
- **[1708.09484](https://arxiv.org/abs/1708.09484)** Bourrier 2017 — XUV 와 물 함량의 시간 진화. h 는
  시스템에서 **질량 손실이 가장 작음**. 현실적인 photolysis-limited
  탈출(ε_α = 0.2) 기준으로 8 Gyr 에 걸쳐 0.37–0.43 EO_H 만 손실
  합니다. 짧은 HZ-runaway 단계(33–67 Myr) 가 축적된 물 대부분을
  보존하지만, ²⁶Al 건조화 논거(Lichtenberg 2019) 가 초기 축적량
  자체를 낮춥니다.
- **[1902.04026](https://arxiv.org/abs/1902.04026)** Lichtenberg 2019 — TRAPPIST-1 전구 planetesimal 의
  ²⁶Al 건조화. 시스템 전체가 f_H₂O ≪ 15 wt%, 어쩌면 ≲ 1 wt% 로
  형성되었다고 주장. h 의 물 질량 분율을 하한 쪽으로 좁히는 역할.
- **[1909.13859](https://arxiv.org/abs/1909.13859)** Gonzales 2019 — TRAPPIST-1 fundamental parameter
  재분석. field age (0.5–10 Gyr) 가 Burgasser & Mamajek 2017 의
  7.6 ± 2.2 Gyr 와 일관함을 확인. cfg 변경은 필요 없음.
- **[2401.11815](https://arxiv.org/abs/2401.11815)** Gillon 2024 — TRAPPIST-1 시스템 종합 review.
  h 의 파라미터를 확인하면서 **insolation 을 0.16 에서 0.144 ±
  0.006 S⊕ 로 보정**. Childs 2023 의 형성 모델링을 인용해 바깥쪽
  다섯 행성은 "유의미한 휘발성 함량을 필요로 했다", 안쪽 두 행성은
  "거의 완전히 건조"라고 정리. h 에 비자명한 물 함량을 유지하는
  선택을 지지.
- **[1702.07004](https://arxiv.org/abs/1702.07004)** Bourrier 2017a — TRAPPIST-1 의 Lyman-α 정찰.
  h 위치에서의 XUV flux. F_X ≈ 34 erg/s/cm², F_EUV ≈ 12 erg/s/cm²,
  F_Lyα ≈ 13 erg/s/cm². h 궤도에서 중성 H 의 광이온화 수명은 약
  25 일로 h 의 궤도 주기보다 길어 exosphere 모델링과 관련은 있지만
  시각에는 영향 없음.

### 읽음 (instrument-only, 시각 정보 아님)

(h 에 특화된 것 없음.)

### 읽지 않음 — arXiv preprint 없거나 저우선순위 (~10 편)

h 의 참고 문헌은 중간 규모입니다(53 편 중 arXiv 43 편). 비-arXiv
대부분은 카탈로그 요약이거나 h 를 지나가듯 언급하는 작업입니다.

- **"Simulating Hydrospheres of TRAPPIST-1 h in Search of Liquid
  Water Layer"** (no arXiv) — *sub-glacial 해양 문제에 잠재적으로
  중요*. **접근 가능 시 paste 요청 flag.**
- **"VizieR Online Data Catalog: TRAPPIST-1 h NIR spectrum
  (Gressier+, 2022)"** — 데이터 카탈로그. 내용은 이미 [2112.05510](https://arxiv.org/abs/2112.05510) 에
  포함. Skip.
- **"Characterizing Stellar Activity and Planetary Atmospheres in
  the TRAPPIST-1 System"** (no arXiv) — 관련 가능성은 있지만 대기
  결정을 다시 봐야 할 때만 확인.
- 각종 SETI / technosignature / 카탈로그 논문 — 무관.

---

## 후속 follow-up 항목

- Lincowski 2018 의 "건조된 거주 가능 h" 시나리오를 대체 cfg 변형
  으로 구현할 수 있습니다. 두꺼운 CO₂/O₂ 대기 + 따뜻한(~280 K)
  맨 암석 표면 조합으로, 시각적으로 더 건조하고 먼지가 많으며
  흐릿한 노란-크림 하늘을 갖는 형태로 구분됩니다.
- "Simulating Hydrospheres of TRAPPIST-1 h" 논문(no arXiv) 은 접근
  가능해지면 sub-glacial 해양 cfg 를 정교화할 수 있습니다.
- 2026-05-22 기준 h 에 대한 JWST 후속 관측은 출판되지 않았습니다.
  향후 emission 이나 transmission 스펙트럼이 나오면 Phase 3 를
  다시 봐야 합니다.
- "Pluto-like full frost" cfg 변형도 가능합니다. 기반암 노출을 최소
  화하고 크림-화이트 표면이 지배하는 형태로, 더 깔끔한 외행성계
  analog 가 필요할 때 쓸 수 있습니다.
- 물 질량 분율(0.05–0.15) 은 제약이 약합니다. 0 (암석 건조 analog)
  부터 최대 0.25 (Europa analog) 까지 가능하며, Phase 2 에서 내부
  구조 측정치를 더 보태야 합니다.
- Lincowski 2018 의 "건조된 거주 가능 h" 대안 시나리오는 여전히
  cfg 변형으로 유효합니다. Dong 2018 / Krissansen-Totton 2022 의
  유지-우호적 논거가 그 prior 를 일정 부분 끌어올립니다. 정규 0.005
  bar 보다 0.1 bar 변형이 더 현실적일 수 있습니다.
- Makarov 2018 에 따라 `tidal_heating_w_m2` 가 1–2 자릿수 과소평가
  되었을 가능성이 있습니다(peak ~7×10⁻³ W/m² 대 cfg 의
  0.00001–0.0001). 더 최근의 Bolmont 후속 논문들과 다시 대조해야
  합니다.
- Mars 형 patchy 오로라 지오메트리는 interesting-first 선택입니다.
  대안인 "균일하고 흐릿한 전역 glow" 는 cfg 변형으로 보존합니다.
- 표면 방사 dose ~4 Sv/yr 은 Kerbalism 의 "moderate" 방사 등급에
  해당합니다. 더 얇은 대기에도 불구하고 e 나 f 보다 양호한데, h
  의 먼 거리가 stellar 입자 flux 를 줄여주기 때문입니다.

## Related

- [trappist-1-g](trappist-1-g.md) — 인접한 내측 형제. 둘 다 얼음으로 덮여 있지만 g 가 질량과 물이 훨씬 많습니다.
- [trappist-1-f](trappist-1-f.md) — 휘발성 풍부한 외측 HZ 비교 천체.
- [methodology](../reference/methodology.md) — Decisions 스키마와 신뢰도 룰.
- [mod-reference](../reference/mod-reference.md) — 다운스트림 모드.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10. h 는 REX 에서 완전히 부재 (b–g 만 다룸) — Phase 3 가 h 의 첫 cfg-ready 처리입니다.
