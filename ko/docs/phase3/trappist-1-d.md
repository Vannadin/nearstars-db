<!-- TRAPPIST-1 d Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 d — Phase 3 Synthesis

NearStars KSP mod 의 파일럿 Phase 3 문서 (2026-05-21 작성).

TRAPPIST-1 d 는 M8V ultra-cool dwarf 를 4.05 일 주기로 도는 0.79 R⊕
암석 행성이며 고전적 생명체 거주 가능 영역의 안쪽 가장자리에 위치. 최근
JWST/NIRSpec 관측(Piaulet-Ghorayeb et al. 2025) 이 대기에 엄격한 제약을
부여 — 대부분의 태양계 analog 조성이 >95% 신뢰도로 배제. 관측과 일관된
남은 시나리오는 (A) 대기 없는 맨 암석, 또는 (B) terminator 에서 high-
altitude water aerosol 가능성을 가진 극도로 얇은 대기.

**NearStars 시나리오 선택. terminator water-ice 구름을 가진 얇은
대기**, 압력은 (A) 에 가깝게(~0.01 bar, JWST 3σ 상한) 두되 Turbet 2023
GCM 이 예측하는 terminator 구름 feature 는 유지. JWST 충실도와 Mercury-
clone 맨 암석에서 시각적으로 충분한 구분 사이의 균형.

## 결정

Kopernicus / atmosphere cfg-ready 값. `Confidence`. high = 직접 측정
또는 강하게 제약, medium = 강한 지지를 가진 이론, low = 허용 윈도우 내
미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 4.05 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00638 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 234 | medium | Agol 2021 (low ecc → 약한 제약) |
| `sidereal_period_days` | 4.0508 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02227 | high | Agol 2021 |
| `mass_mearth` | 0.388 | high | Agol 2021 TTV; Piaulet 2025 재확인 |
| `radius_rearth` | 0.788 | high | Agol 2021; Piaulet 2025 transit fit |
| `surface_gravity_g_earth` | 0.624 | high | derived = 0.388 / 0.788² |
| `density_g_cc` | 5.43 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 262 | high | Piaulet 2025 |
| `equilibrium_temp_k` (A=0)   | 287 | high | derived from a/R★, T★ = 2566 K |
| `bond_albedo` | 0.10 | medium | T-1 b/c JWST emission 의 맨 암석 analog; 불확실성 0.05–0.20 |
| `atmosphere_present` | true (very thin) | low | 채택된 시나리오 (B); (A) 대기 없음도 방어 가능 |
| `atmosphere_surface_pressure_pa` | 1 000 | medium | H₂-rich 의 3σ 상한 ~0.01 bar; <2σ 에서 얇은 CO₂ 와 일관; Piaulet 2025 §7.1–7.2 |
| `atmosphere_composition` | N₂ 베이스 + 미량 CO₂ + H₂O vapor | low | CH₄, NH₃, H₂-rich 배제; CO₂ 는 2σ 에서 marginal; H₂O 는 terminator 구름 GCM 로 잔존 |
| `atmosphere_scale_height_km` | 12 | medium | derived. kT/μg with T≈280 K, μ≈30 g/mol (CO₂/N₂ mix), g=6.1 m/s² |
| `atmosphere_tint_rgb_hex` | `#a8b0c0` (옅은 silver-blue, 약함) | low | 2566 K 적색 조명 아래의 terminator H₂O 얼음 + Rayleigh 잔재 |
| `dayside_surface_temp_k` | 390 | medium | A=0.1 의 맨 암석 subsolar; cf. Way 2025 Arid-Venus 1-bar Sim 01 dayside max 364 K (그들의 케이스는 redistribution 이 더 강함) |
| `nightside_surface_temp_k` | 150 | low | 얇은 대기 영역의 약한 redistribution; T-1 b/c analog |
| `terminator_water_ice_clouds` | scattered, high-altitude (~mbar level) | low | Turbet 2023 GCM, Piaulet 2025 §7.3 — water-rich tail 이 terminator 에서 mbar 성층권 구름 형성 |
| `ocean_present` | false | high | T-1 별의 water condensation 한계(0.772 S⊕) 안쪽; Turbet 2023; 모든 H₂O 는 대기에 위치 |
| `surface_ice_caps` | dayside 없음; nightside cold-trap frost 가능 | low | 극단적 day/night 대비; 최소한의 volatile 예산 |
| `surface_tint_rgb_hex_primary` | `#2a2018` (어두운 회갈색 basalt) | low | 맨 암석 low albedo + M-dwarf 적색 조명이 perceived hue 이동; Mercury/Moon analog |
| `surface_tint_rgb_hex_accent` | `#5a3220` (산화철 patch) | low | 장기 tidally-locked dayside 의 광분해 산화 형성 (Turbet 2018 mechanism) |
| `surface_morphology` | cratered basaltic 평원; dayside-terminator 근처 relict 마그마 흐름 feature | low | 맨 암석 해석; 마그마 바다 잔존 ≲500 Myr (Piaulet 2025 §8); 이후 충돌 |
| `star_apparent_angular_diameter_deg` | 2.85 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 의 가장 안쪽 두 행성 b 와 c 는 JWST emission / transmission
데이터가 어둡고 낮은 albedo 의 맨 암석 표면과 일관(Greene 2023, Zieba
2023, Piaulet 2025 에 광범위하게 인용). d 의 경우 emission 직접 제약은
아직 출판 안 됨이지만, JWST transmission 분석이 stellar contamination
제거 후 flat spectrum 과 완전히 일관된 맨 암석 시나리오로 처리(Piaulet
2025 §8). 따라서 맨 암석 해석을 d 까지 확장하되, d 는 b/c 보다 차가운
평형 온도에 위치해 nightside 에 응결된 표면 volatile 를 가질 가능성도
플로지블 이라는 caveat 동반.

**색 선택.** 호스트 별이 2566 K M8V dwarf — SED 가 1.1 μm 근처에서 peak
이고 가파른 적색 continuum. 인간 관찰자가 인지하는 표면 reflectance 는
본래 광물 색과 무관하게 적갈색으로 이동(Domagal-Goldman 2010 의 일반
M-dwarf 표면 조명; d 에 특화되진 않음). 신선한 basaltic 표면에 대해
Mercury / Moon mare analog (broadband visible albedo ≈ 0.05–0.12, Hapke
보정) 가 가장 가까운 태양계 reference. `#2a2018` (어두운 회갈색) 을
primary, `#5a3220` 산화철 patch tint 를 accent 로 선택.

**산화철 patch.** 장기 tidally-locked 지구형 세계에서 광화학은 극도로
얇은 대기에서도 stellar UV 가 접근 가능한 영역에 표면 산화를 만드는
경향이 있음(Turbet 2018 의 dayside 표면 화학 맥락의 photolysis 논의).
substellar 사분면 쪽으로 편향된 patchy 산화철 overlay 예상. 직접
reflectance 측정 없는 low-confidence 미적 선택.

**모양.** 표면 텍스처에 기여하는 세 과정. (1) ≲500 Myr 마그마 바다
페이즈(Piaulet 2025 §8) 가 relict flow / fracture 구조 남김, (2) tidally-
locked 표면에 ~8 Gyr 충돌 누적(locked frame 에서 leading 반구 쪽 cratering
편향), (3) 별-행성 자기 결합으로부터의 induction heating 잠재성(Grayver
2022, Way 2025 에 인용) 으로 제한된 화산 활동 유지 가능 — 다만 d 에
대해서 이를 강제하는 직접 증거 없음. lunar-highlands-density cratering
을 기본값으로 채택, dayside terminator 근처에 visible 마그마 바다 relict
feature (tidally-locked 조사 아래 비균일하게 식은 마그마의 freeze-front
텍스처가 예상되는 위치).

## 대기 합성

JWST NIRSpec/PRISM transmission 분광 (transit 2회, Piaulet-Ghorayeb 2025)
이 stellar contamination 보정 후 ±100–150 ppm 내의 flat spectrum 산출.
이로 다음 배제.

- ~0.01 bar 보다 두꺼운 H₂-rich 대기, >3σ (모든 metallicity ≲100× solar)
- Cloud-free Titan-like (N₂ 안에 1.6% CH₄), >3σ
- 1 bar 의 Archean Earth analog, >3σ (CH₄ partial pressure)
- Cloud-free Venus (~92 bar CO₂), >95%
- Early Mars (1 bar CO₂), >95%
- Cloud-free modern Earth, >95%

2σ 내에서 marginally 일관된 남은 시나리오.

- 극도로 얇은 (<0.01 bar) Mars-like CO₂
- High-altitude 황산 구름이 있는 Venus-like
- CO₂ 를 가리는 물 구름의 modern Earth-like
- terminator 에서 mbar-level 성층권 H₂O 얼음 구름이 형성되는 water-rich
  대기 (Turbet 2023 GCM 이 d 에 대해 특히 예측 — 0.772 S⊕ 의 water
  condensation 한계 안쪽 위치 때문, Piaulet 2025 §7.3)
- 완전한 대기 없는 맨 암석

NearStars 는 "매우 얇은 대기 + terminator water-ice 구름" 시나리오의
합성을 채택.

- **압력** 을 JWST 3σ 상한(~1000 Pa = 0.01 bar) 에 둠. 대기 없음 극단이
  아닌, JWST 데이터와 여전히 일관된 가장 두꺼운 대기 질량.
- **조성** 은 N₂ 가 지배, 미량 CO₂ 와 H₂O. CH₄ 와 NH₃ 는 광분해로 배제
  (Turbet 2018). H₂ 는 형성 + 탈출 논거로 배제 (Hori & Ogihara 2020,
  Piaulet 2025 §7.1 에 인용). 미량 CO₂ 는 marginally 허용되며 outgassing
  모델 지지 (Liggins 2021, Salman 2024). H₂O 는 terminator 구름 feature
  에 필요.
- **Terminator 구름** 은 full overcast 아닌 discrete high-altitude
  water-ice patch. GCM 예측(Turbet 2023, Piaulet 2025 §7.3) 과 일치하며
  완전한 맨 행성과 구별되는 시각적 흥미 제공.

**하늘 외관.** 0.01 bar 표면 압력에서 dayside Rayleigh scattering 은
사실상 부재 — 정오에도 천정 근처는 거의 검고, M8 별이 강렬한 국지
적-오렌지 조명(~2566 K 색온도) 제공. terminator 쪽으로는 high-altitude
water-ice 구름이 비스듬한 stellar light 를 받아 적색 hue 의 horizon 에
대비되는 옅은 cyan-white streak 로 나타남. Nightside 하늘은 오염되지
않고, 합(conjunction) 의 나머지 TRAPPIST-1 행성 체인을 보여줌 (7개
행성이 거의 동일 평면; Agol 2021).

## 자전 & spin 합성

TRAPPIST-1 d 시스템 파라미터가 강한 동기 회전 구성을 강제. 궤도 이심률은
작음(0.00638; Agol 2021), 황도 경사각은 시스템 ≳7 Gyr 나이 동안 조석력에
의해 0 으로 damping(Agol 2021 §6.2), 회전-궤도 공명은 가장 그럴듯하게
1:1 — 다만 Way 2025 는 3:2 회전-궤도 상태가 공식적으로 배제되지 않음을
지적(Correia 2014, Makarov 2018, Revol 2024) 하고 자신의 GCM 시뮬레이션
두 개를 그 가정 아래 실행. NearStars 는 1:1 케이스를 기본으로 채택; 3:2
대안은 후속 cfg 변형 가능.

**KSP 구현 노트.** 진정한 1:1 조석 lock 은 자전 주기 = 궤도 주기 = 4.0508
일. Kopernicus 에서 body 의 `rotationPeriod` 가 궤도 `period` 와 같아야 함
(349 989 s).

**계절 없음.** 황도 경사각 = 0, eccentricity-driven libration 사실상 없음
(궤도당 insolation 변동 < 0.4%) → substellar 점이 표면 frame 에서 고정.
시각적 영향. 모든 표면 위치에 day-night 사이클 없음, 계절적 극관 이동
없음, terminator drift 없음.

## 비주얼 스타일

표면과 대기 결정 결합.

- **전역 색 팔레트.** 어두운 basalt body (`#2a2018` primary, `#5a3220`
  accent) 가 강렬한 적-오렌지 별빛 아래 → 녹색이나 청색 채널 없는 깊은
  ochre-charcoal 세계로 나타남. 가장 높은 시각 대비는 terminator 에서,
  near-grazing 빛이 지형 기복을 드러냄.
- **Dayside.** 밝은 substellar 영역(~390 K, ~118 °C). near-zenith 조명이
  그림자를 평탄화하므로 feature 가 흐려짐. 산화철 patch 는 substellar
  점에서 ~30° 이내에 가장 강함.
- **Terminator band.** 가장 사진발 좋은 영역. high-altitude water ice
  구름이 stellar light 를 받아 적색 표면에 대비되는 옅은 cyan-white wisp
  로 나타남. 상당한 지형 그림자 대비.
- **Nightside.** 차가움(~150 K) 하고 어두움; 열적외 emission 만, visible
  대역 feature 없음. KSP nightside 조명은 매우 낮은 ambient 여야 — 유일한
  광원은 TRAPPIST-1 b, c(드문 close conjunction) 또는 외행성에서 반사된
  starlight.
- **Atmosphere haze.** 0.01 bar 대기는 거의 안 보임. 행성 limb 의 어두운
  공간 배경에서만 보이는 3–5 km 두께의 옅은 silver-blue limb haze
  (`#a8b0c0`) 추가.
- **하늘의 별.** TRAPPIST-1 이 d 의 하늘에서 ~2.85° 차지 (지구에서 본
  태양 각 크기의 약 5.7배). 색은 깊은 적-오렌지 (≈2566 K blackbody → CIE
  chromaticity 가 `#ff7a1a` 근처), 표면 밝기는 Mars-from-Mars 의 태양
  밝기 비슷(~1.12 S⊕). 1 μm 이상 파장에서 별이 두드러진 solar flare 를
  보일 만큼 밝음(Howard 2023, Piaulet 2025 §1 에 인용) — KSP 에서 가끔
  flare 조명 깜빡임이 충실하지만 선택적인 터치.
- **하늘의 자매 행성.** Inferior conjunction 시 TRAPPIST-1 c 가 각
  크기 ~0.5° (지구 표면에서 본 달과 유사), TRAPPIST-1 e 가 ~0.3°. 거의
  동일 평면 geometry 라 conjunction 이 자주(며칠마다) 일어남.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2502.00132** Way 2025 — "TRAPPIST-1 d: Exo-Venus, Exo-Earth or
  Exo-Dead?" 17 가지 boundary-condition 변형 아래의 ROCKE-3D 3D GCM
  스위트. 기후 시나리오 envelope(Arid-Venus 부터 Aquaplanet), 표면 온도
  범위, Wolf 2017 / Turbet 2018 / Rushby 2020 과의 명시적 비교 제공.
- **2508.08416** Piaulet-Ghorayeb 2025 — JWST NIRSpec/PRISM transmission
  스펙트럼. 결정적 관측 제약. 대기 시나리오 선택과 맨 암석 표면 해석
  견인.
- **2511.10801** Salman 2024 — 탄소 사이클이 있는 대기-내부 모델.
  mantle 산소 fugacity 와 초기 물 질량 분율의 함수로 outgassing 조성
  제약. H₂-rich 보다 trace-CO₂ + H₂O 조성 지지.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **1802.02250** de Wit 2018 — HST WFC3 대기 정찰. H₂-rich 대기에 대한
  초기 제약(d 에 대해 8σ). Piaulet 2025 로 대체되었지만 역사적으로
  첫 비검출.
- **1810.05210** Moran 2018 — 업데이트된 질량과의 HST 안개/구름 한계.
  HST 와 일관된 tropospheric 구름과 metallicity > 60× solar 보임. JWST
  로 대체.
- **2103.08600** Welbanks 2021 — Aurora 검색 프레임워크. CO₂-rich 또는
  N₂-rich d 대기에 대한 10-transit JWST NIRSpec 검출 feasibility 예측.
  Piaulet 2025 관측이 이 예측의 실험적 실현(2 transit 으로 예측된
  민감도 달성).
- **2206.00028** Meadows 2022 — 대기 교환 biosignature false-positive
  (d 의 O₂ 가 e 로 운반). 그럴듯한 volatile 운반 메커니즘 제약하지만
  직접 시각적 정보 아님.
- **2210.02484** Hill 2022 — Habitable-zone exoplanet 카탈로그. d 를
  LHS 1140 b 및 K2-3 d 와 함께 후속 관측에 유리한 transiting ≤2 R⊕ HZ
  행성 셋 중 하나로 등재. 맥락만.
- **2304.12490** Hardegree-Ullman 2023 — ELT O₂ 검출 가능성 서베이.
  미래 지상 ELT 로 d–g 의 Earth-like O₂ 검출에 16–55 년 적분 추정.
  시각 정보 아니지만 장기 관측 미래 맥락화.

### 읽음 (instrument-only, 시각 정보 아님)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series
  특성화. Piaulet 2025 관측의 방법론 reference. TRAPPIST-1 d 스펙트럼에
  `inject-recovery` 시뮬레이션 사용했지만 행성은 test case 로만 등장.

### 읽지 않음 — arXiv preprint 없음 (22 편)

ADS 쿼리로 surfacing 됐지만 arXiv preprint 가 없어 기관 도서관 접근이나
PDF paste 필요. Phase 3 d 의 핵심 논문은.

- **2025epsc.conf..178P** Piaulet-Ghorayeb 2025 EPSC abstract — 이미
  읽은 JWST 논문(2508.08416) 의 conference 요약일 가능성 높음. Skip.
- **2024absc.conf00561M / 2024ESS.....550004M / 2023PSJ.....4..192M**
  Mullens et al. 2023–2024 — "Feasibility of Detecting Biosignatures
  in the TRAPPIST-1 System." 같은 연구의 세 venue 출현. 시각 정보 아닐
  가능성(biosignature 초점). 대기 결정 재검토 필요할 때만 확인.
- **Confirmation of a Dynamical Model for the TRAPPIST-1 Exoplanetary
  System** (no arXiv) — *궤도 파라미터에 잠재적으로 중요*. 이 논문이
  Agol 2021 의 dynamics 를 업데이트한다면 위 궤도 결정 수정 필요.
  **접근 가능 시 사용자 paste 요청 flag.**
- **ExoCAM: A Community Climate Modeling Tool** (no arXiv) — 도구 논문,
  과학 아님. Skip.
- **NIRISS Exploration of the Atmospheric diversity of Transiting
  exoplanets (NEAT)** — GTO 프로그램 설명, 과학 콘텐츠 없음. Skip.
- **VizieR Online Data Catalog: NIR transmission spectra of TRAPPIST-1
  planets (Zhang 2018)** — 데이터 카탈로그, 콘텐츠는 Zhang 2018 논문에
  이미 있음. Skip.
- **Limits on Clouds and Hazes in the TRAPPIST-1 Planets: insights from
  the laboratory** — 2018 논문에 대한 Moran 2020 lab follow-up 가능성.
  haze 파라미터에 **약한 관심**; JWST 데이터로 결정에 critical 아님.
- **Insights into the atmospheres of the TRAPPIST-1 planets from the
  laboratory and modeling** — 위와 유사. Skip.
- **Characterizing JWST NIRSpec's Noise Performance with a Lab-Measured
  Time Series** — 장비, 과학 아님. Skip.
- **Prospects for Biosignature Detection with JWST** (x2) — JWST 데이터
  이전. Skip.
- **Experimental Constraints for Improving Terrestrial Exoplanet
  Photochemical Models** — 방법론, d 특화 제약 없음. Skip.
- 나머지 ~10 항목. NEAT 프로그램 / conference 요약.

**사용자 액션 요청.** "Confirmation of a Dynamical Model for the
TRAPPIST-1 Exoplanetary System" 논문이 접근 가능하면 paste 부탁 — 위
궤도 파라미터 테이블 정교화 가능.

---

## 후속 follow-up 항목

- d 의 향후 emission 분광에 대해 Bond albedo 선택(0.10) 검증. T-1 b 는
  0.0 ± 0.1 (Greene 2023), c 는 유사; d 는 volatile/구름 컴포넌트를
  유지하면 다를 수 있음.
- M8V 조명 아래 시각 테스트용 renderer 가 가능하면 표면 tint hex 코드
  정교화.
- 3:2 회전-궤도 케이스 (Way 2025 alt 시나리오) cfg 변형 — KSP/Principia
  게임플레이 구분이 정당화하면.
- Kopernicus PQS+atmosphere 상호작용 모델에 대해 0.01 bar 대기 선택
  교차 검증 — 이 압력에서 대기는 본질적으로 장식.
