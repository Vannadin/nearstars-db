<!-- TRAPPIST-1 e Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 e — Phase 3 Synthesis

TRAPPIST-1 e 는 M8V ultra-cool dwarf 를 6.10 일 주기로 도는 0.92 R⊕,
0.69 M⊕ 암석 행성. 안쪽에서 네 번째 행성으로 지구 일조량의 0.66배를
받음 — 보수적 거주 가능 영역 한가운데 위치하며 TRAPPIST-1 시스템에서
**가장 거주 가능성이 높은 단일 세계** (Wolf 2017, Turbet 2018, Lincowski
2018, Way 2025). 최근 JWST NIRSpec PRISM transmission 스펙트럼 (Glidden
et al. 2025 DREAMS, 4회 방문) 은 상당한 stellar contamination 을
겪지만 H₂-rich 대기를 배제하고 Venus-analog CO₂-rich 대기를 2σ 에서
약하게 disfavor. 미량 CO₂ 와 CH₄ 를 가진 N₂-rich 대기는 완전히 허용되며,
맨 암석 해석도 일관됨.

**NearStars 시나리오 선택. 1 bar N₂/CO₂/H₂O 대기를 가진 온대
aqua-planet, 해양 보유, substellar 점 근처에 열린 물과 terminator 및
nightside 의 얼음을 가진 조석 lock "안구(eyeball)" geometry.** 이것은
canonical "최선의 거주 가능 후보" cfg 변형. (여전히 관측과 일관된)
옵션들 중 Wolf 2017 / Turbet 2018 / Way 2025 의 aquaplanet 시나리오를
선택. 대안인 맨 암석 해석은 백업 cfg 변형으로 보존.

## 결정

Kopernicus / atmosphere cfg-ready 값. `Confidence`. high = 직접 측정
또는 강하게 제약, medium = 강한 지지를 가진 이론, low = 허용 윈도우 내
미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 6.10 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00510 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 108 | medium | Agol 2021 (low ecc → 약한 제약) |
| `sidereal_period_days` | 6.1010 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02925 | high | Agol 2021 |
| `mass_mearth` | 0.692 | high | Agol 2021 TTV |
| `radius_rearth` | 0.920 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.818 | high | derived = 0.692 / 0.920² |
| `density_g_cc` | 4.92 | high | Agol 2021 (지구보다 낮음 — water-rich 내부) |
| `water_mass_fraction` | 0.05–0.10 | medium | Agol 2021 + Acuña 2021 — 낮은 질량 + 낮은 밀도가 수 wt% H₂O 와 일관 |
| `insolation_s_earth` | 0.66 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 251 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 230 | high | derived; 지구 analog albedo |
| `bond_albedo` | 0.30 | medium | 지구 + Hapi 2024 aqua-planet GCM 범위 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Wolf 2017 GCM Aquaplanet; Turbet 2018 §4 |
| `surface_temp_nightside_k` | 230 | medium | Wolf 2017 GCM; 얼음으로 덮인 nightside |
| `surface_temp_global_mean_k` | 270 | medium | Wolf 2017 GCM Aquaplanet |
| `atmosphere_present` | true | high | 채택된 시나리오; Glidden 2025 와 일관 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | 1 bar canonical 지구형; Glidden 2025 가 미량 CO₂ 와 함께 N₂-rich 허용 |
| `atmosphere_composition` | N₂ 78%, O₂ ~5% (낮음; abiotic), CO₂ ~1%, H₂O 0.1–1%, Ar 0.5% | medium | Wolf 2017, Lincowski 2018 aquaplanet 평형; outer-HZ 온실 가열용으로 지구 대비 CO₂ 상승 |
| `atmosphere_scale_height_km` | 9.5 | medium | derived. kT/μg with T≈270 K, μ=29, g=8.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a7090` (M-dwarf 적색 이동을 동반한 muted blue) | medium | 2566 K 조명 아래 Rayleigh-blue — dim cyan-gray 쪽으로 강하게 적색 이동 |
| `cloud_cover_fraction` | 0.55 | medium | Wolf 2017 GCM Aquaplanet stratocumulus + cirrus |
| `cloud_tint_rgb_hex` | `#c0a890` (warm cream — 적색 이동된 물 구름) | medium | 물 구름 + 2566 K 조명 → warm cream-orange |
| `ocean_present` | true (substellar 열린 물 disk; 그 외 얼음) | medium | Turbet 2018 aquaplanet; Pierrehumbert 2011 "eyeball Earth" morphology |
| `ocean_extent_substellar_radius_deg` | 35 | medium | Wolf 2017 Aquaplanet — substellar 점에서 ~35° 이내의 열린 해양 |
| `ocean_tint_rgb_hex` | `#1a2540` (낮은 M-dwarf 일조량 아래 어두운 navy) | low | 깊은 해양 + 흐릿한 적색 별 → 어두운 blue-violet |
| `surface_ice_caps` | substellar 열린 물 disk 바깥 전체 커버리지; 표면의 ~60% | medium | Wolf 2017 Aquaplanet ice line 이 substellar 에서 ~35° |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-dwarf 빛 아래 snow / sea ice) | medium | 물 얼음 albedo 0.6–0.8 + 적색 이동 조명 |
| `surface_tint_rgb_hex_accent` | `#7a6a58` (terminator 의 ridge 정상에 노출된 기반암) | low | 얇은 대기 + 얼음 흐름 geometry |
| `surface_morphology` | substellar 의 ~35° 이내 해양; 그 외 sea-ice + 빙하 지형; 얼음 경계의 침수 + 노출 지형 | medium | Hu 2014 / Pierrehumbert 2011 tidally-locked aquaplanet 템플릿 |
| `magnetic_field_present` | true (modest, ~0.1× 지구) | low | 작은 질량 + 느린 자전 → 약한 고유 자기장; 직접 제약 없음 |
| `induction_heating_w_m2` | 0.01–0.1 | medium | Grayver 2022 — e 에서 b/c 보다 훨씬 낮음 |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | Bolmont 2020 — e 에서 최소 |
| `star_apparent_angular_diameter_deg` | 2.17 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 e 는 시스템에서 가장 거주 가능성이 높은 세계. 세 가지
증거선이 수렴.

1. **일조량** (0.66 S⊕) 이 온실 가열을 동반한 어떤 합리적 대기에
   대해서도 보수적 거주 가능 영역 (Kopparapu 2013 / 2014) 안에
   위치. 대기 없으면 e 는 얼어붙음; 1 bar N₂/CO₂ 면 표면 액체 물을
   유지 (Wolf 2017, Turbet 2018 §4).

2. **밀도** (Agol 2021 의 4.92 g/cc) 가 지구의 5.51 g/cc 보다
   낮으며 non-trivial 한 물 질량 분율과 일관. 마그마 바다 모델링
   (Bourgeois et al. 2024 — 2008.09599) 이 e 에 대해 물 질량 분율
   0–0.23 을 제시, 중앙 추정값은 약 0.05–0.10 (질량으로 수 퍼센트 =
   지구 해양 분량의 수 배).

3. **관측 일관성.** Glidden 2025 (DREAMS) 가 H₂-rich 를 배제하고
   Venus-analog 대기를 약하게 disfavor 하지만, 미량 CO₂ 와 CH₄ 를
   가진 N₂-rich 대기는 명시적으로 허용 — 정확히 canonical 지구
   analog 2차 대기.

표면 morphology 의 경우, tidally-locked aquaplanet 템플릿
(Pierrehumbert 2011, Hu & Yang 2014, Wolf 2017) 이 독특한
"eyeball Earth" 패턴을 제공.

- **Substellar disk** (substellar 점에서 ≲35°). 열린 해양, 액체 물에
  충분히 따뜻 (Wolf 2017 Aquaplanet 시나리오에서 substellar 표면 온도
  ~290 K), cirrus 구름 가능.
- **중위도 / 중경도** (substellar 에서 35–90°). ice line 의 수 m 부터
  terminator 근처의 수백 m 까지 두께가 변하는 sea ice.
- **Terminator 와 nightside** (substellar 에서 >90°). 얼어붙은
  해양 위 두꺼운 빙하 얼음 (>1 km); 얼음이 tectonic feature 주변에서
  깨진 ridge 정상에 노출 지형 가능.

**색 선택.** 두 가지 경쟁 효과. (a) 내재적 얼음/눈 albedo 는 높음
(0.6–0.8) 이고 푸르스름한 흰색, (b) 2566 K M-dwarf 조명이 인지되는
hue 를 적-오렌지 쪽으로 강하게 이동. 결합 결과 얼음 커버에 대해
warm cream-white (`#d8d0c4`) 와 깊은 해양에 대해 어두운 navy-violet
(`#1a2540`). Hu 2014 가 명시적으로 지적하기를, M-dwarf 주위
aquaplanet 은 stellar SED 가 Rayleigh-scatter 할 단파장 flux 가
최소이기 때문에 지구보다 "덜 푸르게" 보임.

**산화철 / 기반암.** 노출 제한 — 대부분의 표면적이 얼음으로 덮임.
기반암 외관은 빙하 흐름이 얼음을 얇게 만든 terminator 근처 ridge
정상에 한정. accent `#7a6a58` 은 M-dwarf 빛 아래의 muted weathered-
basalt 톤.

**조석 lock 하의 morphology.** Substellar disk 가 활발한 수문학적
순환을 hosting — 표면 가열이 증발을 이끌고, polar / nightside
cold-trap 에서의 응결이 영구 빙하를 만들고, 빙하 흐름이 물을
substellar disk 쪽으로 되돌림. 이 패턴은 지질학적 시간 척도에서
안정 (Wolf 2017 §6), 계절 사이클이 아닌 영구 기후 영역을 가진
행성을 만들어냄.

## 대기 합성

Glidden 2025 (DREAMS NIRSpec PRISM, 4 transit) 가 e 의 첫 JWST
transmission 스펙트럼을 제시. 0.6–5 μm 전반의 상당한 stellar
contamination 이 추론을 복잡하게 만들지만, Gaussian process 로
stellar feature 를 marginalize 한 후 다음을 발견.

- H₂-rich (부피로 ≳80%) 구름낀 대기 >3σ 에서 배제
- Venus-analog CO₂-rich 대기 2σ 에서 약하게 disfavor
- 미량 CO₂ 와 CH₄ 를 가진 N₂-rich 대기는 **완전히 허용**
- 맨 암석 해석도 적합하지만 설명되지 않은 feature 동반

이는 Wolf 2017 / Lincowski 2018 / Way 2025 모델링에서 기대되는
지구 analog 2차 대기와 일관 — 오히려 지지.

NearStars 는 **1 bar N₂-rich aquaplanet 대기**를 채택.

- **압력** 1 bar (100 kPa) — 지구 analog, Glidden 2025 N₂-rich
  일관성 윈도우 내에 편안하게 위치.
- **조성** N₂ 78% (지구형 배경), Ar 0.5%, CO₂ 1% (outer-HZ 온실
  가열 제공을 위해 지구의 0.04% 대비 상승; Wolf 2017 이 거주 가능
  표면을 위해 1–10× CO₂ 향상 필요하다고 발견), H₂O 0.1–1%
  (substellar 표면 근처는 포화, 그 외에서는 훨씬 적음), O₂ ~5%
  (abiotic 광분해 구동 O₂; cfg 에서 산소 발생 생물권을 가정하지 않으므로
  현재 지구의 21% 보다 낮음).
- **구름.** Wolf 2017 GCM 이 ~55% 전역 구름 커버리지를 만들어냄,
  대부분 열린 물 disk 위의 stratocumulus 와 그 외의 high cirrus.
  Cirrus 가 5–10% 온실 가열 기여.

**하늘 외관.** 1 bar N₂ 대기는 단파장에서 지구형 Rayleigh
scattering 을 가지지만, 2566 K stellar SED 는 0.5 μm 아래에서
최소 flux 를 가짐 — 그래서 산란된 하늘 색은 지구의 푸름에 비해
훨씬 어둡고 오렌지 쪽으로 이동. 천정 하늘은 dim 한 red-blue 혼합
(~`#3a4060`), horizon 근처에서 warm orange (`#a07050`) 로 전환.
물 구름 feature 는 적색 stellar light 를 받는 warm cream 패치
(`#c0a890`) 로 나타남.

호스트 별이 각 크기 2.17° 로 낮의 하늘을 지배 (지구에서 본 태양 각
크기의 약 4배). substellar 점의 표면 조명은 지구의 약 0.66배, 짙게
흐린 지구의 하루와 유사 — 다만 spectral peak 이 적색/근적외선
쪽으로 확실히 이동.

**Nightside.** 직접적인 stellar 조명 없음; 유일한 광원은 (a) 대기
순환을 통해 dayside 에서 운반된 산란광 (무시 가능), (b) 자매 행성에서
반사된 빛 (합 시 f 와 d, 각 크기 ~0.4–0.5°, mv ≈ −10 ~ −13), (c)
먼 별로부터의 starlight (부재한 태양에서의 대기 산란이 없어 보임).
Nightside 하늘은 극적으로 어두움 — KSP nightside ambient 는 dayside
의 ~1% 여야.

## 자전 & spin 합성

e 의 7.6 Gyr 동안 6.10 일 주기에서의 조석 damping 이 동기 (1:1)
구성을 모호함 없이 확립. 황도 경사각은 0 으로 damping (Agol 2021
§6.2). Eccentricity 는 0.00510 (Agol 2021), 3:2 spin-orbit 에는 너무
낮음 (Vinson 2017).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 6.1010 일 (527 127 s).
Kopernicus `rotationPeriod` 가 궤도 `period` 와 초 단위로 같아야 함.

**느린 자전 효과.** 6.1 일 자전 주기로 Coriolis 효과는 지구보다 약함
(Rossby number 상승). Wolf 2017 GCM 은 이것이 지구의 좁은 jet stream
대신 substellar disk 에서 느리고 넓은 동→서 zonal 순환을 만든다고
보임. 구름 패턴에 대한 시각적 함의. 더 매끄럽고 더 큰 규모의 구름
band; 더 적은 cyclonic 활동.

**계절 없음.** 황도 경사각 = 0; libration 유도 일조량 변동 < 0.4%.
substellar 점과 그 열린 물 disk 가 표면 frame 에서 고정.

## 비주얼 스타일

표면과 대기 결정 결합.

- **전역 외관.** 궤도에서 보면 e 는 substellar 점 근처의 warm-cream
  열린 물 "동공" 과 그 주위를 둘러싼 fractal sea-ice 전이 영역,
  그리고 그 너머의 완전한 흰색-크림 빙하 얼음을 가진 눈공처럼 보임.
  영구 구름 커버 (~55% 전역) 가 외관을 부드럽게 만들고, substellar
  해양 위에는 stratocumulus, 얼음 영역 위에는 high cirrus.
- **Substellar disk (열린 물).** 강렬한 적-오렌지 조명 아래 어두운
  navy 해양 (`#1a2540`), warm cream 구름 (`#c0a890`) 으로 점점이
  박힘. 행성의 가장 시각적으로 인상적인 feature.
- **얼음 전이 band.** warm cream (`#d8d0c4`) 얼음과 어두운 해양
  (`#1a2540`) 의 fractal 패턴 — 열린 lead 를 가진 깨진 sea ice.
  전이 반경은 substellar 에서 약 35° (Wolf 2017); KSP 지형이 이것을
  대략 원형의 ice line 으로 보여야 함.
- **빙하 얼음 영역.** 빙하 흐름이 기반암과 만나는 곳에 미묘한 지형
  기복을 가진 매끄러운 warm cream (`#d8d0c4`). Terminator 는 비스듬한
  조명에서 가장 밝은 영역 — 긴 그림자가 압력 ridge 와 crevasse 를
  드러냄.
- **Nightside.** Starlight 를 반사하는 얼음에서 옅은 cyan-white
  sheen 을 가진 어두움. 보이는 feature. 압력 ridge, 균열, 가끔의
  refrozen lead. KSP nightside ambient ≈ dayside 의 1%; 렌더링은
  얼음 feature 만 보여야.
- **Atmosphere haze.** 약 15–25 km 두께의 옅은 gray-blue limb glow
  (`#5a7090`) — Rayleigh-산란된 M-dwarf 빛. M-dwarf SED 때문에
  지구의 푸른 limb 보다 상당히 흐릿.
- **하늘의 별.** TRAPPIST-1 이 e 의 하늘에서 2.17° 차지 (지구에서 본
  태양의 4배) — 팔 길이로 든 큰 식기 접시 정도 크기의 깊은 적-오렌지
  disk (`#ff7a1a`) 로 나타남. substellar 점에서의 표면 조명은 "영원한
  일몰" 처럼 느껴지며, 멀어질수록 황혼과 완전한 밤으로 흐려짐.
- **하늘의 자매 행성.** d (다음 안쪽) 가 합에서 각 크기 ~0.3°; f
  (다음 바깥쪽) 가 ~0.4°. 공명 체인 때문에 며칠마다 합. 전체 시스템은
  거의 동일 평면.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2509.05414** Glidden 2025 (DREAMS NIRSpec PRISM) — e 의 첫 JWST
  transmission 스펙트럼 (4 visit). 구름낀 H₂-rich 대기를 >3σ 에서
  배제; stellar contamination 방법 제약. 초석이 되는 관측 논문.
- **2509.05407** Glidden 2025 (DREAMS Secondary Atmospheres) —
  동반 논문. **미량 CO₂ 와 CH₄ 를 가진 N₂-rich 대기 완전히 허용;
  Venus-analog 를 2σ 에서 약하게 disfavor.** 시나리오 선택 견인.
- **2510.18704** Bourgeois 2025 — e 에 대한 다중모델 앙상블
  (광화학 + 3D 기후 + transmission 스펙트럼). N₂/CO₂/CH₄/H₂O 조성
  공간, 물 구름, 광화학 haze 탐구. 구름 커버 분율과 대기 조성
  혼합에 정보 제공.
- **2502.00132** Way 2025 — TRAPPIST-1 d 를 위한 ROCKE-3D GCM
  스위트지만 e 와의 광범위한 비교 동반. e 를 거주 가능 파라미터
  공간에 위치시키고 Earth/Venus/Dead 삼분법 논의. d Phase 3 에서
  이미 읽음.
- **1809.07498** Lincowski 2018 — 모든 TRAPPIST-1 행성의 진화한
  기후. "Aqua planet e 가 지구형 지질학적 outgassing 과 CO₂ 가
  주어지면 온대 표면을 유지할 수 있음." Aquaplanet cfg 선택을
  직접 동기 부여.
- **2006.11349** Wunderlich 2020 — e 와 f 의 wet vs. dry 대기.
  e 가 E-like geology + CO₂ 로 온대일 수 있음을 확인. cfg 조성
  결정을 지지.
- **2008.09599** Bourgeois 2024 — e/f/g 의 마그마 바다 진화. e 에
  대해 물 질량 분율 범위 0–0.23 제공; 기반암 물 예산 설정. 표면
  합성에 사용.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2403.03403** M dwarf 외계행성이 얼마나 거주 가능한가? 표면 조건
  모델링. 일반 M-dwarf HZ 맥락; e 특화 아님.
- **2412.10192** CO₂-에서 H₂O-지배 대기로. 거주 가능 영역 행성의
  휘발성 cycling 배경; CO₂ 분율 선택에 정보 제공 (outer-HZ 가열을
  위해 0.04% 대신 1%).
- **2206.00028** Felton 2022 — 대기 교환 biosignature false-positive
  (d 의 O₂ 가 e 로 운반). d Phase 3 에서 이미 읽음. abiotic O₂
  배경을 제약하지만 시각 cfg 를 바꾸지 않음.
- **2310.15992** 느리게 자전하는 tidally-locked 행성을 위한 새 2D
  Energy Balance Model. substellar disk 모델링의 방법론 맥락.
- **2211.11887** Cohen 2022 — tidally-locked aquaplanet 의 traveling
  planetary-scale wave. 시각적 흥미를 더할 수 있는 구름 가변성을
  예측하지만 KSP 에서는 게임플레이 무관.
- **2305.08813** *(d 참고문헌에 있음, e 가 아님)* 다양한 contamination
  / 특성화 작업 — 맥락만.

### 읽음 (instrument-only, 시각 정보 아님)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series.
  방법론만.
- **2407.19167** 기계 보조 biosignature 분류. e 특화 아님.

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~34 편)

e 의 참고문헌은 두 번째로 큼 (64 편, 30 편이 arXiv). 대부분의 비-arXiv
논문은 biosignature 나 ELT 특화 특성화 계획에 대한 conference abstract
이며 시각-정보 제공 아님. 주목할 만한 skip 항목.

- **2024–2025 다양** — biosignature 가능성 연구와 JWST 제안 abstract.
  cfg 관련 대기 조성 업데이트할 때만 skip 하지 않음.
- **광화학 프로그램 제안서** — 방법론만.

---

## 후속 follow-up 항목

- Glidden 2025 DREAMS 논문은 "보정되지 않은 stellar contamination
  또는 행성 신호 때문일 수 있는 feature" 를 인정. 미래의 재환원이나
  새 instrument (NIRISS, MIRI MRS) 가 e 에서 분자 feature 를
  발견하면 대기 조성 표 업데이트 필요할 수 있음.
- 물 질량 분율 범위 (채택된 0.05–0.10) 는 Bourgeois 2024 의 0–0.23
  의 중앙값 — Acuña 2025 나 이후의 내부 fit 가 개선되면 좁힐 수
  있음.
- "Venus-analog" 해석 (1 bar CO₂ + H₂SO₄ 구름) cfg 변형. 해양 없는
  시각적으로 독특한 yellow-cream 세계. Glidden 2025 가 2σ 에서 약하게
  disfavor 지만 배제는 아님.
- "맨 암석 airless" 해석 cfg 변형. b/c 와 유사한 비주얼이지만 e 의
  훨씬 더 차가운 dayside 온도 (T_eq ≈ 250 K → 대부분 얼음으로 코팅된
  맨 암석).
- 5% abiotic O₂ 선택 교차 검증 — 일부 Lincowski 2018 시나리오에서는
  10–20% 일 수 있음. 하한은 "최소 광분해" 기대와 일치; 상한은 더
  "post-runaway".
