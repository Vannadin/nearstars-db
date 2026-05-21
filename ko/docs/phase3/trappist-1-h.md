<!-- TRAPPIST-1 h Phase 3 합성: cfg-ready 결정과 근거 -->
# TRAPPIST-1 h — Phase 3 Synthesis

TRAPPIST-1 h 는 M8V ultra-cool dwarf 를 18.77 일 주기로 도는 0.76 R⊕,
0.33 M⊕ 의 sub-Mars 질량 암석 행성입니다. 7 행성 중 가장 바깥에 있고
지구 insolation 의 0.16 배만 받습니다. K2 mission 데이터를 쓴 Luger
2017 (1703.04166) 이 궤도 주기와 공명 체인 내 위치를 확정했고,
Gressier 2022 (2112.05510) 가 최초의 HST WFC3/G141 근적외 transmission
스펙트럼을 얻어 cloud-free 한 수소 풍부 대기를 배제했습니다. JWST
후속 관측은 2026-05-21 기준 아직 출판되지 않았습니다. h 의 흥미로운
반전은 따로 있습니다. Lincowski 2018 (1809.07498) 은 **건조된
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
| `insolation_s_earth` | 0.144 | high | Agol 2021 / Gillon 2024 (2401.11815) — 이전 라운드의 0.16 에서 보정됨 |
| `equilibrium_temp_k` (A=0)   | 169 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, frosted) | 142 | high | derived. 서리 덮인 표면 케이스 |
| `bond_albedo` | 0.40 | medium | 기반암 + CO₂/N₂ 서리 혼합으로, full snowball 보다는 덜 반사적 |
| `surface_temp_substellar_k` | 175 | medium | 수동 복사 평형 + 미량 대기의 약한 온실 효과 |
| `surface_temp_nightside_k` | 60 | medium | 매우 차가워서 N₂ 얼음 서리점에 도달 |
| `surface_temp_global_mean_k` | 140 | medium | 얇은 대기로 인한 약한 재분배 |
| `atmosphere_present` | true (very tenuous) | low | Gressier 2022 가 H₂-rich 대기를 배제했고, 미량의 outgassed CO₂ + N₂ 는 가능 |
| `atmosphere_surface_pressure_pa` | 500 | low | 0.005 bar — 최소 잔여, Mars-thin 수준 |
| `atmosphere_composition` | N₂ ~90%, 미량 CO₂ ≲1000 ppm, Ar / H₂O 미량 | low | Bolmont 2018 review 가 배경 가스와 무관하게 p_CO₂ 분압을 100–1000 ppm 으로 한정함. 표면 CO₂ cold-trap 이 지배적 |
| `atmosphere_scale_height_km` | 6.0 | medium | derived. kT/μg 로 T≈140 K, μ=40, g=5.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#302820` (Rayleigh 산란 사실상 인지 불가) | low | 매우 얇은 대기 + M-dwarf SED 이므로 산란 무시 가능 |
| `cloud_cover_fraction` | 0.02 | low | 최소 — 산발적인 CO₂ 얼음 권운만 |
| `cloud_tint_rgb_hex` | n/a | high | cfg 에 반영할 만큼의 구름이 안 됨 |
| `ocean_present` | uncertain (wmf 상한이면 sub-glacial 가능) | low | 저질량 + 저온이라 g 보다 기저 용융이 적고, 있더라도 얇은 Europa 형 |
| `surface_ice_caps` | 차가운 영역의 전역 CO₂/N₂ 서리, substellar 부근의 기반암 노출 | medium | insolation 더 낮은 Mars-Pluto 하이브리드 analog |
| `surface_tint_rgb_hex_primary` | `#3a2c20` (풍화된 철-풍부 기반암, 먼지, Mars analog) | medium | 저밀도 암석 표면 + 7.6 Gyr 의 광분해 산화 |
| `surface_tint_rgb_hex_accent` | `#c8b8a0` (CO₂/N₂ 서리 패치와 밝은 얼음) | low | 차가운 영역의 휘발성 서리 퇴적, Mars 극관 analog |
| `surface_morphology` | substellar 근방의 cratered 고대 기반암, terminator 와 nightside 쪽으로 patchy 한 CO₂/N₂ 얼음 서리 | medium | Mars/Mercury analog, resurfacing rate 가 매우 낮음 |
| `magnetic_field_present` | false (저질량 + 저온 + 느린 자전) | low | 활동성 다이나모 없을 가능성, 작은 화석 자기장은 여지 있음 |
| `induction_heating_w_m2` | 0.001–0.01 | medium | Grayver 2022 — 거리와 작은 질량 때문에 시스템에서 가장 낮음 |
| `tidal_heating_w_m2` | 0.00001–0.0001 | medium | Bolmont 2020 — h 에서는 무시할 만함 |
| `radiogenic_heat_w_m2` | 0.025 | medium | 질량으로 스케일링, Earth-analog 보다 약간 낮음 |
| `star_apparent_angular_diameter_deg` | 1.03 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 h 는 시스템에서 가장 작은 행성(0.326 M⊕, sub-Mars 질량)
이며 insolation 은 0.16 S⊕ 입니다. 작은 질량, 낮은 중력(0.572 g),
낮은 insolation 의 조합 때문에 h 는 대기 유지에 까다로운 케이스
입니다. cosmic shoreline 문헌(Castan-Lopez 2025 — 2504.19872 — ,
Zahnle 2017) 은 h 를 수소 함유는 물론 질소 함유 대기에 대해서도
경험적 유지 임계값 근처 또는 그 아래에 놓고 있습니다. 일부 휘발성
유지는 그럴듯한데, CO₂ 정도면 h 의 온도에서 Jeans 탈출을 견딜 만큼
분자량이 충분히 크지만, 대기 질량 자체는 작을 가능성이 높습니다.

저질량임에도 h 의 bulk 밀도(Agol 2021 의 4.20 g/cc) 는 비자명한 물
질량 분율(~5–15%) 을 함의할 만큼 낮습니다. f, g 와 비슷한 양상이지만
이쪽은 활용 가능한 전체 질량이 훨씬 적습니다. 이 물의 대부분은 표면
얼음 형태(CO₂ + H₂O 얼음) 이거나 작은 암석 코어 위 얇은 sub-glacial
층으로 격리되어 있을 가능성이 큽니다.

Lincowski 2018 (1809.07498) 의 "건조된 h" 시나리오 — 두꺼운(10–100
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

**색 선택.** M-dwarf 조명 아래의 풍화된 철-풍부 기반암이므로
primary 는 어두운 적갈색 `#3a2c20` (Mars 의 녹슨 색 + M-dwarf 이동
으로 인한 낮은 albedo). 서리 accent 는 크림-화이트 `#c8b8a0`.

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

Gressier 2022 (2112.05510) 가 h 의 첫 HST WFC3/G141 transmission
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

- **압력** 0.005 bar (500 Pa). Mars (~600 Pa, 변동) 와 비슷한 수준
  입니다. 0.3 M⊕ 행성에도 일부 outgassing 은 축적되므로 0 보다는
  위에 있어야 하고, cosmic-shoreline / Jeans 탈출 제약상 h 가
  이보다 많이는 유지하지 못한다는 점에서 0.01 bar 아래여야 합니다.
- **조성** N₂ 지배(~90%) + 미량 CO₂ (~0.1% = 1000 ppm). 70% CO₂
  였던 이전 초안에서 수정된 부분입니다. 근거는 **Bolmont 2018
  (1810.11255)** review 로, h 의 GCM 이 N₂ 배경 가스 양과 무관하게
  CO₂ 를 100–1000 ppm 이상 축적하지 못한다는 결과를 제시합니다.
  표면 cold-trapping 이 outgassing 보충보다 빠르게 CO₂ 를 nightside
  얼음 퇴적층으로 보내기 때문입니다. 나머지 10% 는 Ar, 서리 순환의
  H₂O 증기, 화석 O₂ 사이에서 분배됩니다.
- **구름.** 최소 (~2% 전역). Mars 의 중간권 구름과 비슷한 드문
  CO₂ 얼음 권운 정도.

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

**공명 체인 동역학.** Luger 2017 (1703.04166) 이 7 행성 Laplace 공명
체인 안에서 h 의 위치를 확립했습니다(g 와 8:5 평균 운동 공명). 체인
은 궤도 요소에 지속적인 small-amplitude 섭동을 주지만, 시각적/cfg
목적상 구성은 안정적입니다.

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

- **1703.04166** Luger 2017 — K2 를 통한 h 의 궤도 주기 발견 / 확인.
  공명 체인의 일곱 번째 행성으로 h 를 확립. 궤도 파라미터의 출처.
- **2112.05510** Gressier 2022 — h 의 HST WFC3/G141 transmission
  스펙트럼. cloud-free H₂-rich 대기를 배제. 현재까지 h 에 대한 유일한
  직접 대기 관측.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계들의 진화된 기후.
  h 는 snowball 과 "건조된 거주 가능" 이상치 양쪽으로 논의됩니다.
  정규-대-변형 시나리오 분기를 견인했고, d/e/f/g 단계에서 이미 읽음.
- **2510.12794** Pearce 2025 — Born Dry or Born Wet? Compact
  multiplanet volatile accretion. 충돌 + 탈출 진화 아래에서 h 의
  물 예산을 다룹니다.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  h 를 유지 임계값 근처에 놓아 얇은 대기 cfg 선택을 지지.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2008.09599** Bourgeois 2024 — e/f/g 의 magma ocean 진화 (h 에
  직접 적용된 건 아니지만 프레임워크 제공). 이미 읽음.
- **2508.12865** 경험적 cosmic shoreline. 맥락.
- **2507.02136** Nurturing Atmospheres 를 위한 3D Cosmic Shoreline.
  맥락.
- **2603.29743** 새 M Dwarf Cosmic Shoreline 제약. 맥락.
- **1810.05210** Moran 2018 — HST haze 한계, h 포함. 이미 읽음.
- **1810.11255** Bolmont 2018 review — Constraining the environment
  and habitability of TRAPPIST-1. 직접 인용. "TRAPPIST-1 h 는 표면
  액체 물을 유지할 수 없다. 배경 가스의 양과 무관하게 10²–10³ ppm
  이상의 CO₂ 를 축적하지 못한다." 이 결과가 N₂ 지배 + 미량 CO₂ 로의
  대기 조성 수정을 견인.
- **1708.09484** Bourrier 2017 — XUV 와 물 함량의 시간 진화. h 는
  시스템에서 **질량 손실이 가장 작음**. 현실적인 photolysis-limited
  탈출(ε_α = 0.2) 기준으로 8 Gyr 에 걸쳐 0.37–0.43 EO_H 만 손실
  합니다. 짧은 HZ-runaway 단계(33–67 Myr) 가 축적된 물 대부분을
  보존하지만, ²⁶Al 건조화 논거(Lichtenberg 2019) 가 초기 축적량
  자체를 낮춥니다.
- **1902.04026** Lichtenberg 2019 — TRAPPIST-1 전구 planetesimal 의
  ²⁶Al 건조화. 시스템 전체가 f_H₂O ≪ 15 wt%, 어쩌면 ≲ 1 wt% 로
  형성되었다고 주장. h 의 물 질량 분율을 하한 쪽으로 좁히는 역할.
- **1909.13859** Gonzales 2019 — TRAPPIST-1 fundamental parameter
  재분석. field age (0.5–10 Gyr) 가 Burgasser & Mamajek 2017 의
  7.6 ± 2.2 Gyr 와 일관함을 확인. cfg 변경은 필요 없음.
- **2401.11815** Gillon 2024 — TRAPPIST-1 시스템 종합 review.
  h 의 파라미터를 확인하면서 **insolation 을 0.16 에서 0.144 ±
  0.006 S⊕ 로 보정**. Childs 2023 의 형성 모델링을 인용해 바깥쪽
  다섯 행성은 "유의미한 휘발성 함량을 필요로 했다", 안쪽 두 행성은
  "거의 완전히 건조"라고 정리. h 에 비자명한 물 함량을 유지하는
  선택을 지지.
- **1702.07004** Bourrier 2017a — TRAPPIST-1 의 Lyman-α 정찰.
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
  (Gressier+, 2022)"** — 데이터 카탈로그. 내용은 이미 2112.05510 에
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
- 2026-05-21 기준 h 에 대한 JWST 후속 관측은 출판되지 않았습니다.
  향후 emission 이나 transmission 스펙트럼이 나오면 Phase 3 를
  다시 봐야 합니다.
- "Pluto-like full frost" cfg 변형도 가능합니다. 기반암 노출을 최소
  화하고 크림-화이트 표면이 지배하는 형태로, 더 깔끔한 외행성계
  analog 가 필요할 때 쓸 수 있습니다.
- 물 질량 분율(0.05–0.15) 은 제약이 약합니다. 0 (암석 건조 analog)
  부터 최대 0.25 (Europa analog) 까지 가능하며, Phase 2 에서 내부
  구조 측정치를 더 보태야 합니다.
