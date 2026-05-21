<!-- TRAPPIST-1 h Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 h — Phase 3 Synthesis

TRAPPIST-1 h 는 M8V ultra-cool dwarf 를 18.77 일 주기로 도는 0.76 R⊕,
0.33 M⊕ sub-Mars 질량 암석 행성. 7 행성 중 가장 바깥쪽이며, 지구
insolation 의 0.16× 만 받음. 궤도 주기와 공명-체인 위치는 K2 mission
데이터를 사용한 Luger 2017 (1703.04166) 으로 확인됨. Gressier 2022
(2112.05510) 가 첫 HST WFC3/G141 근적외 transmission 스펙트럼을
획득하고 cloud-free 수소 풍부 대기를 배제; 2026-05-21 기준 JWST
후속 관측은 출판되지 않음. h 의 흥미로운 반전. Lincowski 2018
(1809.07498) 은 **건조된(desiccated)** h 가 특정 10–100 bar O₂ + CO₂
post-runaway 시나리오 아래에서 maximum-greenhouse 거리 너머에서도
거주 가능한 표면 온도를 유지할 수 있다고 지적 — h 를 시스템에서 가장
반직관적인 거주 가능성 후보로 만듦.

**NearStars 시나리오 선택. 풍화된 기반암 위에 patchy CO₂ + N₂ 얼음
서리가 깔린 얼어붙은 sub-Mars 암석 세계; 후기 outgassing 에서 남은
매우 얇은(~0.005 bar) 잔여 대기.** 이는 낮은 insolation 의 저질량
행성에 대한 cosmic-shoreline 문헌(Castan-Lopez 2025, Zahnle 2017)
의 더 보수적 해석을 채택, 대부분의 휘발성 물질이 손실되었거나 표면에
얼어붙은 경우. 대안 — Lincowski 2018 의 "건조된 거주가능" 시나리오 —
는 cfg 변형으로 보존하지만 시각적으로 덜 구분됨 (따뜻하고 건조한
암석 표면 위 두꺼운 CO₂/O₂ 대기).

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 18.77 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00567 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 339 | medium | Agol 2021 (low ecc → 약한 제약) |
| `sidereal_period_days` | 18.7729 | high | Agol 2021; Luger 2017 K2 확인 |
| `semi_major_axis_au` | 0.06189 | high | Agol 2021 |
| `mass_mearth` | 0.326 | high | Agol 2021 TTV — sub-Mars (Mars 0.107, Mercury 0.055) |
| `radius_rearth` | 0.755 | high | Agol 2021; Gressier 2022 transit fit |
| `surface_gravity_g_earth` | 0.572 | high | derived = 0.326 / 0.755² |
| `density_g_cc` | 4.20 | high | Agol 2021 (water-rich) |
| `water_mass_fraction` | 0.05–0.15 | medium | low density 가 상당한 물과 일관; e/f/g 보다 덜 제약됨 |
| `insolation_s_earth` | 0.16 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 169 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, frosted) | 142 | high | derived; 서리 덮인 표면 케이스 |
| `bond_albedo` | 0.40 | medium | 혼합 기반암 + CO₂/N₂ 서리; full snowball 보다 덜 반사적 |
| `surface_temp_substellar_k` | 175 | medium | 수동적 복사 평형, 미량 대기에서 약한 온실 효과 |
| `surface_temp_nightside_k` | 60 | medium | 매우 차가움; N₂ 얼음 서리점 도달 |
| `surface_temp_global_mean_k` | 140 | medium | 얇은 대기에서 약한 재분배 |
| `atmosphere_present` | true (very tenuous) | low | Gressier 2022 가 H₂-rich 거부; 미량 outgassed CO₂ + N₂ 가능 |
| `atmosphere_surface_pressure_pa` | 500 | low | 0.005 bar — 최소 잔여; Mars-thin |
| `atmosphere_composition` | CO₂ 70%, N₂ 25%, 미량 H₂O / Ar | low | post-magma-ocean outgassed 혼합; 대부분 표면에 얼어붙음 |
| `atmosphere_scale_height_km` | 6.0 | medium | derived. kT/μg with T≈140 K, μ=40, g=5.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#302820` (사실상 인지 불가 Rayleigh) | low | 매우 얇은 대기, M-dwarf SED → 무시할 수 있는 산란 |
| `cloud_cover_fraction` | 0.02 | low | 최소 — 산발적 CO₂ 얼음 권운만 |
| `cloud_tint_rgb_hex` | n/a | high | cfg 관련 tint 에 구름이 너무 희소 |
| `ocean_present` | uncertain (wmf 상한이면 sub-glacial 가능) | low | 저질량 + 저온 → g 보다 적은 기저 용융; 만약 있다면 얇고 Europa 같음 |
| `surface_ice_caps` | 차가운 지역에 전역 CO₂/N₂ 서리, substellar 근처 기반암 노출 | medium | 더 낮은 insolation 의 Mars-Pluto 하이브리드 analog |
| `surface_tint_rgb_hex_primary` | `#3a2c20` (풍화된 철-풍부 기반암, 먼지 + Mars analog) | medium | 저밀도 암석 표면 + 7.6 Gyr 광분해 산화 |
| `surface_tint_rgb_hex_accent` | `#c8b8a0` (CO₂/N₂ 서리 patch + 밝은 얼음) | low | 차가운 지역의 휘발성 서리 퇴적; Mars polar analog |
| `surface_morphology` | substellar 근처 cratered 고대 기반암, terminator 와 nightside 쪽으로 patchy CO₂/N₂ 얼음 서리 | medium | Mars/Mercury analog; 매우 낮은 resurfacing rate |
| `magnetic_field_present` | false (저질량 + 저온 + 느린 자전) | low | 활동적 다이나모 없을 가능성; 작은 화석 자기장 가능 |
| `induction_heating_w_m2` | 0.001–0.01 | medium | Grayver 2022 — 거리 + 작은 질량 때문에 시스템에서 가장 낮음 |
| `tidal_heating_w_m2` | 0.00001–0.0001 | medium | Bolmont 2020 — h 에서 무시할 만함 |
| `radiogenic_heat_w_m2` | 0.025 | medium | 질량으로 스케일링; Earth-analog 보다 약간 적음 |
| `star_apparent_angular_diameter_deg` | 1.03 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 h 는 시스템의 가장 작은 행성(0.326 M⊕, sub-Mars 질량)이며
0.16 S⊕ insolation 에 위치. 조합 — 작은 질량, 낮은 중력(0.572 g),
낮은 insolation — 은 h 를 대기 유지에 어려운 케이스로 만듦. cosmic
shoreline 문헌(Castan-Lopez 2025 — 2504.19872 — , Zahnle 2017) 은
h 를 수소 함유 및 심지어 질소 함유 대기의 경험적 유지 임계값 근처
또는 아래에 둠. 일부 휘발성 물질 유지는 그럴듯함 (CO₂ 는 h 의 온도에서
Jeans 탈출을 견딜 만큼 분자량이 충분히 큼) 이지만 대기 질량은 작을
가능성이 큼.

저질량에도 불구하고, h 의 bulk 밀도(Agol 2021 의 4.20 g/cc) 는 비자명한
물 질량 분율(~5–15%) 을 함의할 만큼 낮음, f 및 g 와 유사하지만 작업할
질량이 훨씬 적음. 이 물의 대부분은 표면에 얼어붙어 있거나 (CO₂ 와
H₂O 얼음) 작은 암석 코어 위의 얇은 sub-glacial 층으로 격리되어
있을 가능성.

Lincowski 2018 (1809.07498) "건조된 h" 시나리오 — 두꺼운(10–100 bar)
CO₂/O₂ post-runaway 대기로부터의 거주 가능한 표면 온도 — 는 cfg
변형으로 보존되지만 정규 선택은 아님. h 의 탈출 속도에서 post-runaway
대기 유지 시간 척도는 짧음(≲ 1 Gyr); 시스템 나이 7.6 Gyr 동안 초기
두꺼운 대기 대부분은 손실됨.

표면 형태에 대해서는 Mars-Pluto 하이브리드 analog 를 채택.

- **Substellar 영역** (substellar 에서 ~0–60°). 기반암 지배,
  Mars 의 남쪽 고원과 유사한 풍화된 철-풍부 표면. 그늘진 분화구에
  일부 patchy CO₂ 서리.
- **Mid-zone** (60–120°). substellar 로부터의 거리에 따라 서리
  덮개 증가.
- **Terminator** (~90°). 높은 서리-기반암 대비; 비스듬한 2566 K
  빛 아래의 긴 지형 그림자.
- **Nightside** (>120°). 주로 ~60 K 의 CO₂ + N₂ 서리 덮개, 능선
  꼭대기에 가끔 어두운 기반암 patch.

**색 선택.** M-dwarf 조명 아래 풍화된 철-풍부 기반암. 어두운 적갈색
primary `#3a2c20` (Mars 녹슴 + M-dwarf 이동에서 더 낮은 albedo).
서리 accent 는 크림-화이트 `#c8b8a0`.

**기반암 / 산화철.** g/f 와 비교해 h 에서 두드러짐 — 노출된 substellar
기반암은 7.6 Gyr 동안 직접 stellar UV 아래 광분해 산화를 겪음. primary
tint 는 이미 이를 포함; 충돌 분화구 가장자리 근처의 특정 밝은 산화철
patch 는 fine-grained PQS 디테일로 좋은 선택.

**조석 lock 아래의 모양.** 거의 resurfacing 없음 — h 의 조석 가열은
무시할 만하고(Bolmont 2020), induction heating 은 최소(Grayver 2022
거리 스케일링), 방사성 열은 화산활동을 일으키기에 너무 낮음(작은
질량). 표면은 시스템의 7.6 Gyr 나이에 걸친 최대 충돌 기록을 보존,
locked frame 의 leading 반구 쪽으로 편향.

## 대기 합성

Gressier 2022 (2112.05510) 가 h 의 첫 HST WFC3/G141 transmission
스펙트럼을 제시, 행성의 유일한 출판된 대기 관측. 데이터는 대기 없음
또는 flat-spectrum 이차 대기와 일관; cloud-free 수소 풍부 대기는
배제됨.

이론 모델링.

- **Lincowski 2018.** h 에 대해 건조된 post-runaway 10–100 bar
  CO₂/O₂ 대기를 고려, 일부가 거주 가능한 표면 온도를 제공함을 발견.
  하지만 h 의 탈출 속도에서 7.6 Gyr 동안 그러한 두꺼운 대기의 유지
  확률은 낮음.
- **Bourgeois 2024.** magma ocean 진화는 ~1 bar (CO₂ + H₂O) 의
  초기 outgassed 대기를 줌; 대부분 시간이 지나며 손실.
- **Castan-Lopez 2025.** cosmic shoreline 분석은 h 가 전형적
  이차 대기의 유지 임계값 근처 또는 아래에 있음을 시사.

NearStars 는 **0.005 bar (Mars-thin) CO₂/N₂ 대기** 채택.

- **압력** 0.005 bar (500 Pa) — Mars 와 비교 가능(~600 Pa, 가변).
  0.3 M⊕ 행성에 일부 outgassing 이 축적되어야 하므로 0 보다 위;
  cosmic-shoreline / Jeans-탈출 제약이 h 가 훨씬 더 많이 유지할 수
  없음을 시사하므로 0.01 bar 보다 아래.
- **조성** CO₂ 지배(70%), N₂ (25%), 미량 H₂O 와 Ar. 심각한 cold-trap
  때문에 H₂O 는 미량; h 의 온도에서 CO₂ 가 표면에 서리화되어 N₂ 에
  대해 가스 상 CO₂ 가 고갈되므로 N₂ 분율은 g 보다 높음.
- **구름.** 최소(~2% 전역). 드문 CO₂ 얼음 권운만, Mars 의 중간권
  구름과 유사.

**하늘 외관.** 0.005 bar 대기는 궤도에서 사실상 안 보임. 표면에서는
호스트 별(1.03° 각 크기, 적-오렌지 디스크) 을 제외하면 하늘이 검음.
0.16 S⊕ 의 표면 조명은 근일점의 외측 Mars 와 유사.

## 자전 & spin 합성

18.77 일에서 7.6 Gyr 에 걸친 조석 damping → 동기(1:1) 구성. 황도
경사각 0 으로 damping. 이심률은 0.00567 — 1:1 우세 영역.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 18.7729 일 (1 621 977 s).

**계절 없음.** 황도 경사각 = 0; libration 유발 insolation 변동 < 0.5%.

**공명 체인 동역학.** Luger 2017 (1703.04166) 이 7 행성 Laplace-공명
체인에서 h 의 위치를 확립 (g 와 8:5 평균-운동 공명). 체인은 궤도
요소에 지속적인 small-amplitude 섭동을 제공하지만, 시각적 / cfg
목적으로는 구성이 안정적.

## 비주얼 스타일

- **전역 외관.** patchy 크림-화이트 서리(`#c8b8a0`) 가 terminator 와
  nightside 쪽으로 증가하는 어두운 적갈색 암석 세계(`#3a2c20`).
  Mars(적갈색 암석) 와 더 작은 Pluto(서리 지배) 사이 어딘가의 시각적
  특성.
- **Substellar 영역.** 대부분 기반암; 풍화된 산화철 갈색. cfg PQS
  해상도에서 충돌 분화구 보임. 그늘진 분화구 내부에 일부 서리.
- **Mid-zone.** 혼합 기반암과 서리 — 크림 서리 위 노출된 어두운
  갈색의 fractal 패턴. KSP 저공 비행에 사진발 좋음.
- **Terminator.** 비스듬한 2566 K 빛 아래 높은 대비; 지형 그림자가
  cratering 과 가능한 tectonic feature 를 드러냄. 서리-기반암 경계는
  여기서 가장 선명.
- **Nightside.** 크림-화이트 서리 덮개(`#c8b8a0`) 와 능선 꼭대기의
  어두운 기반암 patch. KSP nightside ambient ≈ dayside 의 1%.
- **Atmosphere haze.** 인지 불가 — 0.005 bar 대기는 보이는 Rayleigh
  산란을 일으키지 않음. limb 가 선명.
- **하늘의 별.** TRAPPIST-1 이 h 의 하늘에서 1.03° 차지 (지구에서 본
  태양의 2배). 표면 조명 0.16 S⊕ — 지구의 이른 아침 황혼과 비슷.
  ochre-and-cream 표면에 대비되는 적-오렌지 별이 실제 대기 없음에도
  불구하고 h 에 특히 분위기 있는 외관을 줌.
- **하늘의 자매 행성.** g (다음 안쪽) 은 inner conjunction 에서 각
  크기 ~0.3°. h 의 긴 주기 때문에 conjunction 이 내행성보다 덜 빈번.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **1703.04166** Luger 2017 — K2 를 통한 h 의 궤도 주기 발견 / 확인.
  공명 체인의 일곱 번째 행성으로 h 를 확립. 궤도 파라미터의 출처.
- **2112.05510** Gressier 2022 — h 의 HST WFC3/G141 transmission
  스펙트럼. cloud-free H₂-rich 대기 거부. 현재까지 h 의 유일한
  직접 대기 관측.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계의 진화된 기후.
  h 는 snowball 과 "건조된 거주 가능" 이상치 양쪽으로 논의됨.
  정규-대-변형 시나리오 분할을 견인. d/e/f/g 에 대해 이미 읽음.
- **2510.12794** Pearce 2025 — Born Dry or Born Wet? Compact
  multiplanet volatile accretion. 충돌 + 탈출 진화 아래 h 의 물
  예산 고려.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  h 를 유지 임계값 근처에 둠; 얇은 대기 cfg 선택을 지지.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2008.09599** Bourgeois 2024 — e/f/g 의 magma ocean 진화 (h 에
  직접은 아니지만 프레임워크 제공). 이미 읽음.
- **2508.12865** 경험적 cosmic shoreline. 맥락.
- **2507.02136** Nurturing Atmospheres 를 위한 3D Cosmic Shoreline.
  맥락.
- **2603.29743** 새 M Dwarf Cosmic Shoreline 제약. 맥락.
- **1810.05210** Moran 2018 — HST haze 한계, h 포함. 이미 읽음.

### 읽음 (instrument-only, 시각 정보 아님)

(h 에 특화된 것 없음.)

### 읽지 않음 — arXiv preprint 없음 또는 저우선순위 (~10 편)

h 의 참고 문헌은 중간 크기(53 편, arXiv 43 편). 대부분의 비-arXiv
논문은 카탈로그 요약이거나 h 를 지나가듯 언급하는 작업.

- **"Simulating Hydrospheres of TRAPPIST-1 h in Search of Liquid
  Water Layer"** (no arXiv) — *sub-glacial 해양 질문에 잠재적으로
  중요*. **접근 가능 시 paste 요청 flag.**
- **"VizieR Online Data Catalog: TRAPPIST-1 h NIR spectrum
  (Gressier+, 2022)"** — 데이터 카탈로그, 콘텐츠는 이미 2112.05510 에
  있음. Skip.
- **"Characterizing Stellar Activity and Planetary Atmospheres in
  the TRAPPIST-1 System"** (no arXiv) — 관련 가능성 있지만 대기
  결정 재검토 필요할 때만 확인.
- 다양한 SETI / technosignature / 카탈로그 논문 — 무관.

---

## 후속 follow-up 항목

- Lincowski 2018 "건조된 거주 가능 h" 시나리오는 대체 cfg 변형으로
  구현 가능 — 따뜻한(~280 K) 맨 암석 표면을 가진 두꺼운 CO₂/O₂ 대기.
  시각적으로 구분됨. 더 건조하고 먼지 많으며 흐릿한 노란-크림 하늘.
- "Simulating Hydrospheres of TRAPPIST-1 h" 논문(no arXiv) 은 접근
  가능하면 sub-glacial 해양 cfg 를 정교화할 수 있음.
- 2026-05-21 기준 h 에 대해 출판된 JWST 후속 없음; 향후 어떤 emission
  또는 transmission 스펙트럼도 Phase 3 재방문을 trigger 해야 함.
- "Pluto-like full frost" cfg 변형 — 최소한의 기반암 노출, 지배적으로
  크림-화이트 표면. 더 깨끗한 외행성계 analog 원할 때 사용.
- 물 질량 분율(0.05–0.15) 은 잘 제약되지 않음; 0 (암석-건조 analog)
  또는 최대 0.25 (Europa analog) 일 수 있음. Phase 2 는 더 많은
  내부 구조 측정치를 추가해야 함.
