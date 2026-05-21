<!-- TRAPPIST-1 g Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 g — Phase 3 Synthesis

TRAPPIST-1 g 는 M8V ultra-cool dwarf 를 12.35 일 주기로 도는 1.13 R⊕,
1.32 M⊕ 암석 행성. 안쪽에서 여섯 번째 행성으로 지구의 0.26배 일사량을
받음 — 보수적 거주 가능 영역의 한참 바깥. TRAPPIST-1 행성 중 가장 큰
편이며 가장 물이 풍부한 축에 속함. Bourgeois 2024 (2008.09599) 의
magma-ocean 진화 결과는 water mass fraction 0.11–0.24 로 시스템 내
최고치. 2026-05-21 기준 g 에 대한 JWST 관측은 출판된 바 없음. 관측적
그림은 HST haze 한계(Moran 2018) 와 이론적 기후 모델링(Lincowski 2018,
Wolf 2017) 이 지배.

**NearStars 시나리오 선택. 매우 얇은 CO₂ 대기(~0.05 bar) 를 가진 전역
얼음 피복 ocean world, substellar 개방 수역 없음, 빙하 아래 액체 물
바다.** 차가운 outer-HZ 행성에 대한 canonical snowball / "ocean world"
시나리오. CO₂ 온실효과가 강화되어도 g 의 일사량에서는 표면 액체 물
유지 불가(Wolf 2017 §5 에서 ~0.3 S⊕ 이하 완전 snowball 발견). 두꺼운
전역 얼음 피복은 radiogenic heat 로부터의 basal melting 으로 유지되는
상당한 빙하 아래 액체 물 층을 숨김.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 12.35 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00208 | high | Agol 2021 TTV (시스템 최저) |
| `argument_of_periastron_deg` | 191 | medium | Agol 2021 (매우 낮은 ecc → 약한 제약) |
| `sidereal_period_days` | 12.3524 | high | Agol 2021 |
| `semi_major_axis_au` | 0.04683 | high | Agol 2021 |
| `mass_mearth` | 1.321 | high | Agol 2021 TTV |
| `radius_rearth` | 1.129 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.036 | high | derived = 1.321 / 1.129² |
| `density_g_cc` | 5.06 | high | Agol 2021 |
| `water_mass_fraction` | 0.11–0.24 | medium | Bourgeois 2024 — 시스템 최고 |
| `insolation_s_earth` | 0.26 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 194 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.6, snowball) | 154 | high | derived; 고-알베도 snowball |
| `bond_albedo` | 0.55 | medium | snowball 얼음 + 얇은 대기; Wolf 2017 cold-snowball |
| `surface_temp_substellar_k` | 200 | medium | Wolf 2017 cold-snowball; basal-melt 가 표면과 격리 |
| `surface_temp_nightside_k` | 130 | medium | Wolf 2017 GCM; cold-trap nightside |
| `surface_temp_global_mean_k` | 175 | medium | Wolf 2017 cold-snowball 평균 |
| `atmosphere_present` | true (매우 얇은 CO₂) | medium | Moran 2018 이 H₂-rich 배제; outgassing-driven 얇은 CO₂ |
| `atmosphere_surface_pressure_pa` | 5 000 | medium | 0.05 bar CO₂ — weathering sink 없이 누적된 outgassing |
| `atmosphere_composition` | CO₂ 90%, N₂ 8%, 미량 H₂O, Ar | medium | 액체 물 carbonate-silicate cycle 없는 화산 outgassing |
| `atmosphere_scale_height_km` | 4.5 | medium | derived. kT/μg with T≈180 K, μ=43, g=10.2 m/s² |
| `atmosphere_tint_rgb_hex` | `#403028` (무시할 만한 Rayleigh + CO₂ 얼음 haze tint) | low | 매우 얇은 대기, 최소한의 산란 |
| `cloud_cover_fraction` | 0.10 | medium | 매우 제한적 — terminator 의 CO₂ 얼음 cirrus 만 |
| `cloud_tint_rgb_hex` | `#d0c0b0` (CO₂ 얼음 + 먼지, M-dwarf shifted) | medium | 차갑고 얇은 대기에서 최소 구름 생성 |
| `ocean_present` | true (빙하 아래만, 표면 표현 없음) | medium | Bourgeois 2024 wmf 0.11–0.24 + 지구-analog radiogenic heat → basal melt 가능성 높음 |
| `ocean_extent_substellar_radius_deg` | 0 | high | 완전 snowball; Wolf 2017 §5 |
| `ocean_tint_rgb_hex` | n/a (얼음 아래 숨겨짐) | high | 표면에서 보이지 않음 |
| `surface_ice_caps` | 100% 전역 피복 | high | 완전 snowball; Pierrehumbert 2011 outer-HZ branch |
| `surface_tint_rgb_hex_primary` | `#e8e0d4` (M-dwarf 빛 아래 깨끗한 눈) | medium | 고-알베도 눈 + 2566 K 조명 |
| `surface_tint_rgb_hex_accent` | `#a09080` (terminator 의 CO₂ 서리 / 먼지 patch) | low | terminator 근처 승화-퇴적 사이클 |
| `surface_morphology` | 전역 빙하 얼음; 차등 자전으로부터의 tectonic 응력 → pressure ridge; 따뜻한 spot 에서 cryovolcanism 가능 | medium | Wolf 2017 + Europa-Ganymede analog 추론 |
| `magnetic_field_present` | 불확실 (내부 hydrosphere convection 으로 활성화 가능) | low | 사소하지 않은 wmf 가 내부 mantle convection 으로부터 dynamo 유지 가능 |
| `induction_heating_w_m2` | 0.002–0.02 | medium | Grayver 2022 — 거리에 따라 감소 |
| `tidal_heating_w_m2` | 0.0001–0.001 | medium | Bolmont 2020 — g 에서 매우 낮음 |
| `radiogenic_heat_w_m2` | 0.04 | medium | 지구-analog mantle radiogenics |
| `star_apparent_angular_diameter_deg` | 1.36 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 g 는 0.26 S⊕ 에서 보수적 거주 가능 영역 한참 바깥에 위치.
Wolf 2017 §5 는 현실적 대기 탈출 제약 아래에서 10 bar CO₂ 도 g 의
일사량에서 지속적 개방 수역을 만들지 못함을 발견 — cold trap 이 너무
효율적. Lincowski 2018 도 모든 고려된 대기 조성에서 g 를 snowball 로
분류.

g 의 구원하는 지질학적 특징은 매우 높은 water mass fraction. Bourgeois
2024 (2008.09599) 가 g 에 대해 wmf 0.11–0.24 산출 — TRAPPIST-1 시스템에서
최고, 지구 바다 20–50 배에 해당. 대부분은 빙하 아래 액체 물 바다로
존재(얼음-암석 경계에서 지구-analog radiogenic heat ~0.04 W/m² 에 의해
basal-melted) 하며 두꺼운(~50–100 km) 전역 얼음 피복으로 덮임.
Cryovolcanism (Europa / Ganymede analog) 은 플로지블하나 제약되지 않음.

표면 모양에 대해 snowball template 이 다음을 제공.

- **Substellar 부터 substellar 에서 ~30° 까지.** 약간 상승한 일사량으로
  가장 얇은 얼음(~30 km); 더 차가운 terminator 와 nightside 쪽 ice-flow
  에서 tectonic 활동 가능.
- **중간 구역 (substellar 에서 30–120°).** 두꺼운 얼음(~60 km), 큰
  스케일에서 평활.
- **Terminator (~90°).** 가장 높은 pressure-ridge 밀도, 가장 긴 지형
  그림자.
- **Nightside (>120°).** 가장 두꺼운 얼음(~100 km), 가장 차가운 영역에
  CO₂ 서리 퇴적 가능.

**색 선택.** M-dwarf 조명 아래 깨끗한 눈 / 빙하 얼음 알베도. 따뜻한
cream-white `#e8e0d4` primary, terminator 근처 누적된 먼지와 CO₂ 서리
사이클로부터 tan-shaded patch `#a09080`.

**Bedrock / 산화철.** 본질적으로 보이지 않음 — 전역 얼음 피복이 어떤
bedrock 노출에도 너무 두꺼움. pressure 로 인한 얇아짐이 어두운 patch
를 노출할 수 있는 극단적 terminator ridge 꼭대기에서 예외 가능. 매우
낮은 확률이며 궤도에서 보이지 않음.

**조석 lock 아래 모양.** 최소한의 일사량 기울기(substellar-에서-
antistellar 차이 ~70 K) 때문에 얼음 순환이 부드러움. tectonic 활동은
표면 승화/퇴적이 아닌 얼음 껍데기의 basal-melt-driven convection(cf.
Europa) 에 의해 지배. 결과는 따뜻한 spot 에서 cryovolcanic feature 를
갖는 지질학적으로 활성인 얼음 표면 — 시각적으로 미묘하지만 g 를 "죽은
snowball" 과 구분.

## 대기 합성

g 에 대해 출판된 JWST 관측은 없음. HST haze 한계 분석(Moran 2018,
1810.05210) 이 cloud-free 수소-rich 대기를 배제. secondary 대기는 HST 로
제약되지 않음.

이론 모델이 수렴.

- **Wolf 2017.** g 의 일사량에서 완전 snowball; ~10 bar CO₂ 도 액체 물
  에 불충분.
- **Lincowski 2018.** g 는 초기 water inventory 에 따라 "snowball" 또는
  "post-runaway O₂-rich" 로 분류.
- **Bourgeois 2024.** magma-ocean 페이즈가 초기에 ~10 bar O₂ + CO₂ 대기
  생성; 대부분은 hydrodynamic escape 와 표면 산화로 시스템 수명에 걸쳐
  손실.

NearStars 는 **0.05 bar CO₂-rich 얇은 대기**를 채택.

- **압력** 0.05 bar (5 kPa). g 의 온도에서 구름 형성에 필요한 임계값
  아래; 표면이 대부분의 파장에서 우주와 복사적으로 소통할 정도로 얇음.
  CO₂ sink 없는 화산 outgassing(얼어붙은 표면 → carbonate-silicate
  weathering 없음) 이 적당한 CO₂ 를 누적해야 하므로 0 보다 큼.
- **조성** CO₂ 지배 (90%), N₂ (8%), 미량 H₂O / Ar. CO₂ 풍부는 outgassing
  누적 반영; H₂O 는 cold-trap 때문에 미량.
- **구름.** 최소 (~10% 전역). terminator + nightside cold-trap 의 CO₂
  얼음 cirrus 만.

**하늘 외관.** 0.05 bar 대기는 궤도에서 거의 보이지 않음. 표면에서
하늘은 거의 검고 호스트 별이 공허에 대비되는 깊은 적-오렌지 디스크로
나타남. CO₂ 얼음 구름이 terminator 에서 비스듬한 빛을 받아 옅은 cream
wisp 로 나타남.

## 자전 & spin 합성

12.35 일에서 7.6 Gyr 동안의 조석 damping → 동기(1:1) 구성. 황도 경사각
0 으로 damping. 이심률은 0.00208 — 시스템 최저, 3:2 안정성 경계 한참
안쪽(1:1 만 플로지블).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 12.3524 일 (1 067 251 s).

**계절 없음.** 황도 경사각 = 0; libration 으로 인한 일사량 변동 <
0.2%(시스템 최저). Substellar 점이 고정.

## 비주얼 스타일

- **전역 외관.** terminator 근처 미묘한 tan tinting(`#a09080`) 을 가진
  거의 균일한 따뜻한 cream-white snowball (`#e8e0d4`). 명백한 "eyeball"
  feature 없음 — 개방 수역 디스크 없음. 시스템에서 시각적으로 가장
  차분한 행성.
- **Substellar 영역.** 더 차가운 영역 쪽 tectonic ice-flow 로 약간 더
  텍스처화 / 균열된 얼음. 밝은 신선-얼음 patch 로 cryovolcanic feature
  가능.
- **중간 구역과 terminator.** 비스듬한 2566 K 조명 아래의 pressure
  ridge, crevasse, 긴 지형 그림자. Terminator 가 가장 사진발 좋은 영역.
- **Nightside.** CO₂ 서리로부터 약간 더 어두운 cream-tan. KSP nightside
  ambient ≈ dayside 의 1–3%.
- **Atmosphere haze.** 궤도에서 인지 불가; limb 에 hairline 따뜻-회색
  glow (`#403028`) 정도.
- **하늘의 별.** TRAPPIST-1 이 g 의 하늘에서 1.36° 차지(지구에서 본
  태양의 2.7배). 표면 조명은 0.26 S⊕ — 외곽 화성의 태양 flux 와 유사.
  cream 설경에 대비되는 적-오렌지 별이 영구적 어슴푸레-여명 분위기 제공.
- **하늘의 자매 행성.** f (안쪽 다음) 가 conjunction 시 각 크기 ~0.3°;
  h (바깥쪽 다음) 가 outer conjunction 시 ~0.2°. 공명 체인이 빈번한
  다중 행성 정렬 보장.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2008.09599** Bourgeois 2024 — e/f/g 의 Magma ocean 진화. g 를
  시스템에서 가장 물이 풍부한 행성으로 확립(wmf 0.11–0.24). 빙하 아래
  바다 cfg 견인.
- **2412.10192** Cherubim 2024 — magma ocean 페이즈에서 CO₂- 에서 H₂O-
  지배 대기로. g 의 진화된 대기에 대한 조성 프레임워크 제공.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계의 진화된 기후. g 는
  모든 고려된 시나리오에서 snowball 로 분류. d/e/f phase 3 에 이미
  읽음.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited. 경험적
  M-dwarf 대기 retention 선에 대한 g 의 위치. 얇은 대기는 유지하나
  두꺼운 대기는 아닐 가능성.
- **1810.05210** Moran 2018 — HST haze 한계. 안쪽 5 행성(간접적으로 g
  포함) 에 대해 cloud-free H₂-rich 배제. d Phase 3 에 이미 읽음.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2508.12865** Cosmic Shoreline 의 경험적 결정. g 의 retention 상태
  맥락.
- **2504.01182** 중후기 M dwarf 의 Receding Cosmic Shoreline. TRAPPIST-1
  시스템 수준 맥락.
- **2210.02484** HZ 카탈로그. g 를 더 넓은 HZ 후보 중 하나로 등재.
  d 에 이미 읽음.
- **2006.11349** Wunderlich 2020 — Wet/dry e 와 f. g 맥락만. f 에 이미
  읽음.
- **2506.16063** Mass-radius 평면 분류. 카탈로그 맥락만.

### 읽음 (instrument-only, 시각 정보 아님)

(g 에 특화된 것 없음.)

### 읽지 않음 — arXiv preprint 없거나 낮은 우선순위 (~14편)

g 참고문헌은 큼(66편, 52편 arXiv) 이지만 대부분이 SETI / technosignature
서베이, mass-radius 카탈로그, 또는 g 를 지나가듯 언급하는 작품.

- **2509.06310** FAST 와의 Deep SETI search. 시각 아님.
- **2208.02511** SETI drift rate 맥락. 시각 아님.
- **여러 cosmic-shoreline 논문** — retention 질문에 대해 집합적으로
  읽음; 개별 항목은 시각-정보 제공 아님.
- **TESS / non-TRAPPIST-1 카탈로그 논문** — 무관.

---

## 후속 follow-up 항목

- g 에 대한 직접 JWST 관측은 아직 없음; 향후 transmission 또는 emission
  스펙트럼이 출판되면 대기 압력 / 조성 표 재검토 필요. 특히 g 가
  transmission 에서 CO₂ feature 를 보이면 0.05 bar 선택 정교화 가능.
- Cryovolcanism 은 g 에 대해 플로지블하나 제약되지 않음. 향후 cfg
  변형이 Europa-analog 측면(보이는 resurfaced 얼음 patch, 따뜻한 spot
  에서 plume feature 가능) 을 강조하고 싶다면 Phase 3.5 로 구현 가능.
- 0.05 bar CO₂ 선택은 "대기 존재" 의 하한 가장자리 — ~0.01 bar 로
  감소시키거나 완전 무대기 cold-snowball 변형을 위해 0 으로 설정 가능.
- wmf 범위(0.11–0.24) 는 g 가 해저에서 hydrothermal 활동이 있는 거주
  가능 빙하 아래 층을 호스트할 수 있을 만큼 충분히 높음(Europa-
  Enceladus astrobiology analog). 시각적으로 관련 없어도 Principia
  노트 가치 있음.
