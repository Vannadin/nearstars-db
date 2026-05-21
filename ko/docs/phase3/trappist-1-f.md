<!-- TRAPPIST-1 f Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 f — Phase 3 Synthesis

TRAPPIST-1 f 는 M8V ultra-cool dwarf 를 9.21 일 주기로 도는 1.04 R⊕,
1.04 M⊕ 의 암석 행성. 다섯 번째 행성으로 지구의 0.38× insolation 을
받음 — 보수적 생명체 거주 가능 영역의 바깥, maximum-greenhouse 한계
근처(Kopparapu 2013). 질량과 반경은 시스템 전체에서 지구와 가장
비슷하지만, bulk density (Agol 2021 의 4.92 g/cc) 가 충분히 낮아 f 는
유의미한 워터 월드일 가능성이 높음. Acuña 2025 (2504.16201) 는 water
mass fraction 을 16.2% ± 9.9% 로 추정. f 의 첫 NIRISS 대기 정찰 (Lim
2024, ADS bibcode 2024ESS.....510106L; arXiv preprint 없음) 은
cloud-free 수소 풍부 대기를 배제했지만 2차 대기에는 강한 제약을
부여하지 못함.

**NearStars 시나리오 선택. 얇은 CO₂-rich 대기(~0.1 bar) 를 가진
전역 얼음 덮인 해양 세계, substellar 점 근처에 높은 CO₂ greenhouse
+ radiogenic heat 로부터의 basal melting 에 의해 유지되는 작은
open-water lens.** Wolf 2017 / Wunderlich 2020 의 outer-HZ
frozen-ocean 시나리오를 채택하되, substellar open water 는
Pierrehumbert 2011 / Hu 2014 (tidally-locked aquaplanet hysteresis)
에 동기. 대안 — substellar open water 없는 완전한 snowball — 은
cfg 변형으로 보존.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 9.21 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.01007 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 8.81 | medium | Agol 2021 |
| `sidereal_period_days` | 9.2075 | high | Agol 2021 |
| `semi_major_axis_au` | 0.03849 | high | Agol 2021 |
| `mass_mearth` | 1.039 | high | Agol 2021 TTV |
| `radius_rearth` | 1.045 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.952 | high | derived = 1.039 / 1.045² |
| `density_g_cc` | 4.92 | high | Agol 2021 |
| `water_mass_fraction` | 0.07–0.16 | high | Acuña 2025 — MAGRATHEA 내부 fit; mantle-to-core 의존 |
| `insolation_s_earth` | 0.38 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 215 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, snowball) | 188 | high | derived; high-albedo snowball 케이스 |
| `bond_albedo` | 0.45 | medium | snowball 얼음 cover, 부분 구름 cover; Wolf 2017 |
| `surface_temp_substellar_k` | 260 | medium | Wolf 2017 + 0.1 bar CO₂ greenhouse → 좁은 open-water disk |
| `surface_temp_nightside_k` | 165 | medium | Wolf 2017 GCM; 얼음 덮인 차가운 nightside |
| `surface_temp_global_mean_k` | 220 | medium | Wolf 2017 GCM cold-snowball 범위 |
| `atmosphere_present` | true (얇은 CO₂-rich) | medium | Lim 2024 가 H₂-rich 배제, 얇은 CO₂ 허용; Wolf 2017 outer-HZ snowball 케이스 |
| `atmosphere_surface_pressure_pa` | 10 000 | medium | 0.1 bar CO₂ — 부분 substellar open water 의 최소값(Wolf 2017) |
| `atmosphere_composition` | CO₂ 95%, N₂ 4%, 미량 H₂O / Ar | medium | outgassing 주도; Wolf 2017 cold-snowball + Wunderlich 2020 dry-f branch |
| `atmosphere_scale_height_km` | 6.5 | medium | derived. kT/μg with T≈220 K, μ=43 (CO₂-rich), g=9.3 m/s² |
| `atmosphere_tint_rgb_hex` | `#604040` (매우 얇은 CO₂ Rayleigh + 먼지 haze) | low | 0.1 bar 에서 최소 scattering; 일부 CO₂ ice haze 가능 |
| `cloud_cover_fraction` | 0.25 | medium | Wolf 2017 — 차갑고 얇은 대기에서 제한된 구름 형성 |
| `cloud_tint_rgb_hex` | `#d8c8b8` (CO₂ 얼음 + 물 얼음 mix, M-dwarf shifted) | medium | terminator + substellar cirrus |
| `ocean_present` | true (sub-glacial; 작은 substellar open-water lens) | medium | Acuña 2025 wmf 16%; basal melting + greenhouse → marginal open water |
| `ocean_extent_substellar_radius_deg` | 8 | medium | Wolf 2017 — 0.1 bar CO₂ 아래 tight open-water disk |
| `ocean_tint_rgb_hex` | `#1a1c30` (깊은 어두운 navy, 대부분 얼음 아래 숨음) | low | sub-glacial / 작은 lens; 궤도에서 거의 안 보임 |
| `surface_ice_caps` | substellar ~8° disk 바깥 전역 cover; 표면의 ~95% | medium | snowball / "lobster-pot" eyeball; Pierrehumbert 2011 |
| `surface_tint_rgb_hex_primary` | `#e0d8d0` (깨끗한 눈 / 빙하 얼음) | medium | 눈 albedo + M-dwarf 조명 |
| `surface_tint_rgb_hex_accent` | `#888070` (CO₂ frost 가 먼지로 얼룩짐 + 능선 정상 bedrock 노출) | low | nightside CO₂ frost over ice; 얇은 sublimation lag |
| `surface_morphology` | 얼어붙은 해양 위 전역 빙하 얼음; pressure-ridge 지형; terminator 능선의 visible bedrock | medium | tidally-locked snowball; Wolf 2017 |
| `magnetic_field_present` | true (약함, ~0.05× Earth) | low | 작은 질량 + 차가운 내부 + 느린 자전 |
| `induction_heating_w_m2` | 0.005–0.05 | medium | Grayver 2022 — f 의 거리에서 최소 |
| `tidal_heating_w_m2` | 0.0005–0.005 | medium | Bolmont 2020 — f 에서 최소 |
| `radiogenic_heat_w_m2` | 0.04 | medium | Earth-analog mantle radiogenics × 1 |
| `star_apparent_angular_diameter_deg` | 1.65 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 f 는 보수적 생명체 거주 가능 영역(Kopparapu 2014) 의
바깥 가장자리에 위치하고 지구 insolation 의 38% 를 받음. 유의미한
greenhouse 가온이 없으면 표면이 전역적으로 얼어붙음 (Wolf 2017
§5). 0.1 bar CO₂ 가 있으면 Wolf 2017 는 빡빡하게 갇힌 substellar
open-water disk 가 유지될 수 있다고 봄 — 다만 기하 구조가 취약하고
초기 상태에 의존(Pierrehumbert 2011 의 aquaplanet 와 snowball 상태
사이 bifurcation).

Acuña 2025 (2504.16201) 가 현재 최선의 내부 fit 제공. 모든 내부
파라미터를 변화 허용하면 water mass fraction 이 16.2% ± 9.9%, 또는
mantle-to-core 비율을 Earth-like 로 고정하면 6.9% ± 2.0%. 어느
쪽이든 f 는 지구보다 상당히 더 hydrated 됨 — 전역 얼음 cover 아래
전역 액체 물 층을 가진 진정한 "ocean world" 일 가능성이 높음.

Bourgeois 2024 (2008.09599) 의 magma-ocean 진화 작업은 f 가 상당량의
대기 물과 산소를 생성한 확장된(>100 Myr) magma ocean phase 를
경험했음을 시사. 대부분의 물은 그 이후 mantle 로 재평형, 광분해
탈출을 통해 우주로 손실, 또는 행성이 식으면서 표면에 응결됨. 남은
ocean (지금은 sub-glacial) 과 얇은 CO₂ 대기가 장기 endpoint.

표면 morphology 의 경우 tidally-locked snowball 템플릿이 다음을
부여.

- **Substellar disk** (≲8° from substellar point). open water lens
  가능; 그렇지 않으면 국지적 균열이 있는 얇은 얼음. 표면 T ≈ 260 K
  가 얼음/물 평형의 marginal 케이스.
- **빙하 얼음 영역** (8–180° from substellar). sub-glacial 액체
  물 ocean 위 두꺼운(>1 km) 빙하 얼음. 표면 T 는 ice line 의
  ~250 K 에서 antistellar 점의 ~170 K 까지 monotonically 감소.
- **Terminator** (~90° from substellar). 차갑고(~190 K) 어두움;
  가장 사진발 좋은 영역. 2566 K 빛 grazing 아래 pressure ridges 가
  긴 그림자를 던짐. 빙하 흐름이 지각 highs 위에서 얼음을 얇게 만든
  곳에서 bedrock 노출 가능.

**색 선택.** 눈 / 빙하 얼음 albedo 는 0.6–0.8 (깨끗하고 신선) 또는
0.4–0.6 (먼지 얼룩짐, 노화됨). M-dwarf 조명 아래 인지되는 hue 는
청-백색이 아닌 따뜻한 크림색 (`#e0d8d0`). nightside 의 CO₂ frost
가 어두운 패치에 약간의 황갈색 tint 기여 (`#888070`).

**산화철 / bedrock.** 제한된 노출 — terminator 근처 능선 정상에서
빙하 흐름이 얼음을 얇게 만든 곳에서만. f 의 거리에서 제한된 stellar
UV 와 대부분의 bedrock 을 광분해 산화로부터 보호하는 지속적 얼음
cover 때문에 산화철 tint 는 안쪽 행성(b, c) 에 비해 희미함.

**조석 lock 아래 morphology.** 얼음 순환. substellar 점의 표면
가열이 얼음을 sublimate (얇은 대기 때문에 낮은 속도); CO₂ + 미량
H₂O 는 대기 순환을 통해 더 차가운 영역(terminator, nightside) 으로
운반되어 응결. 빙하 흐름이 그 후 얼음을 substellar disk 쪽으로
되돌림. 결과는 substellar 점에 지속적인 얇은 open-water lens 가
있는 안정한 얼음 순환.

## 대기 합성

f 의 Lim 2024 NIRISS 정찰 (arXiv preprint 없음, conference abstract
ADS bibcode 2024ESS.....510106L) 은 f 의 첫 JWST transmission 관측
보고. 결과. H₂-rich 대기 배제됨, Moran 2018 (1810.05210) HST
한계와 일관, 하지만 2차 대기 (CO₂, N₂, H₂O-rich) 는 가용한 transit
baseline 으로 제약 불가. 이는 f 의 관측적 그림이 b, c, d, e 보다
더 열려 있다는 의미.

이론적 모델링 (Wolf 2017 §5, Lincowski 2018, Wunderlich 2020) 은
f 가 조금이라도 거주 가능 / 온화하려면 유의미한 CO₂ greenhouse 가
필요하다는 데 동의 — Wolf 2017 는 완전한 open ocean 에는 1 bar
CO₂ 필요, 0.1 bar 는 tight substellar disk 부여, 그보다 적으면
완전한 snowball.

NearStars 는 **substellar open-water lens 가 있는 0.1 bar CO₂-rich
snowball** 채택.

- **압력** 0.1 bar (10 kPa). Wolf 2017 §5 는 이것이 f 의 insolation
  아래 부분 substellar open water 의 최소값임을 발견.
- **조성** CO₂ 지배 (95%), 미량 N₂ (4%), 미량 H₂O (terminator
  cold-trap 에서 포화), 미량 Ar. CO₂-richness 는 carbonate-silicate
  cycle 이 돌지 않는 (표면이 얼어붙고 CO₂ 를 제거할 액체 물 풍화가
  일어나지 않기 때문에) 행성에서 시간에 걸쳐 누적된 화산 outgassing
  을 반영.
- **구름.** 제한적 (~25% 전역). substellar disk 근처의 물 얼음
  cirrus 와 terminator 의 희미한 CO₂ 얼음 구름.

**하늘 외관.** 0.1 bar CO₂ 대기는 지구의 ~5% Rayleigh scattering
가지며 M-dwarf SED 가 단파장 기여를 추가로 감소시킴. substellar
근처 하늘은 별이 지배적인 가운데 희미한 dark-rust (`#604040`);
terminator 근처에는 CO₂ 얼음 구름의 forward-scattering 으로
limb 의 희미한 cyan-white 와 함께 하늘이 어두움.

## 자전 & spin 합성

7.6 Gyr 에 걸친 9.21 일 주기의 f 에 대한 조석 damping 이 동기(1:1)
구성 확립. 황도 경사각은 0 으로 damping. 이심률은 0.01007 — 3:2
spin-orbit 가 marginally 안정해지는 상단 가장자리(Vinson 2017),
하지만 1:1 이 압도적 확률의 상태로 남음.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 9.2075 일 (795 528 s).

**계절 없음.** 황도 경사각 = 0; libration-induced insolation 변동
~ 1% (더 높은 e 때문에 안쪽 행성보다 약간 높음). substellar 점은
본질적으로 고정.

## 비주얼 스타일

- **전역 외관.** 궤도에서 f 는 substellar 점에 작은 어두운 spot
  (open-water lens, `#1a1c30`) 이 있는 거의 균일한 따뜻한 크림색
  snowball (`#e0d8d0`). substellar disk 위 가끔 cirrus 가 있는
  제한된 구름 cover. antistellar 반구는 CO₂ frost 로 약간 황갈색
  얼룩진 얼음을 보임.
- **Substellar disk (open water).** 작은 어두운 패치 ~16° 너비
  (반경 8°). 주변 따뜻한 크림색 얼음과의 대비가 극적.
- **빙하 얼음.** visible 표면의 대부분. 큰 스케일에서 매끄럽고,
  terminator 에서 grazing 빛 아래 pressure ridges 와 crevasses
  visible. 신선한 눈 (`#e0d8d0`) 과 먼지 얼룩진 / refrozen 얼음
  (`#c8c0b0`) 사이의 미묘한 색 변화.
- **Terminator band.** 비스듬한 빛 아래 높은 지형 대비. 능선 정상의
  bedrock 노출 가능 (`#888070` accent).
- **Nightside.** CO₂ frost 의 어두운 크림-황갈색. KSP nightside
  ambient ≈ dayside 의 2–5%.
- **Atmosphere haze.** 매우 얇은 따뜻한 회-적색 limb glow
  (`#604040`), 5–10 km 두께, 행성 limb 의 공간 배경에서만 visible.
- **하늘의 별.** TRAPPIST-1 이 f 의 하늘에서 1.65° 차지 (지구에서
  본 태양의 3배) — 깊은 적-오렌지 disk 로 나타남. 표면 조명은
  0.38 S⊕, deep-Earth twilight 와 유사; 별의 어둑한 적색 빛이
  설경에 영구적인 새벽 tint 부여.
- **하늘의 자매 행성.** e (다음 안쪽) 가 inferior conjunction 시
  각 크기 ~0.3°; g (다음 바깥쪽) 가 outer conjunction 시 ~0.3°.
  Conjunction 은 매 ~25 일 (f-g synodic 주기).

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2504.16201** Acuña 2025 — MAGRATHEA 를 통한 f 의 내부 구조.
  wmf 16.2% ± 9.9% (free CMF) 또는 6.9% ± 2.0% (Earth-like
  mantle-to-core). f 를 ocean world 로 확립. sub-glacial ocean
  cfg 견인.
- **2008.09599** Bourgeois 2024 — e/f/g 의 magma ocean 진화. f 가
  진화를 통해 상당량의 물을 보유했다고 예측.
- **2006.11349** Wunderlich 2020 — Wet vs. dry e 와 f 대기. f 의
  대기를 CO₂-rich (snowball branch) 또는 dry desiccated
  post-runaway 상태로 제약.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계의 진화한 기후.
  f 는 Lincowski 의 모델링이 차갑고 CO₂-rich 한 대기가 평형이라고
  보여주는 행성 중 하나. d Phase 3 / e Phase 3 위해 이미 읽음.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2605.06964** TRAPPIST-1 기후의 에너지 균형 모델. 방법론 논문;
  f 의 snowball 상태 지지.
- **2506.21351** SEPHI 2.0 거주 가능성 지수. 카탈로그 맥락만.
- **2502.00132** Way 2025 — d 초점이지만 f 에 적용되는 tidally-locked
  GCM 의 유용한 방법론 reference.
- **1810.05210** Moran 2018 — HST haze 한계. d Phase 3 위해 이미
  읽음.

### 읽음 (instrument-only, 시각 정보 아님)

(이 깊이에서 f 에 특화된 것 없음.)

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~9 편)

f 참고 문헌은 매우 작음 (15 편, arXiv 6 편).

- **2024ESS.....510106L** Lim 2024 — TRAPPIST-1 f NIRISS 대기 정찰.
  **f 의 핵심 관측 논문이지만 arXiv preprint 없음.** ADS 초록만
  가용. 대기 추론 (H₂-rich 배제, 2차 대기 미제약) 은 초록에서
  소스됨. **arXiv preprint 등장 시 fetch 위해 flag.**
- **2025arXiv...** biosignature feasibility 와 ELT 특성화에 관한
  다양한 conference 요약. Skip.

---

## 후속 follow-up 항목

- arXiv preprint 가 가용해질 때 Lim 2024 NIRISS f 논문 재fetch;
  공식 출판 버전이 2차 대기 제약을 강화할 수 있음.
- 0.1 bar CO₂ 선택은 Wolf 2017 의 모델링에 의해 bracketed 되지만
  f-특화 관측으로 직접 제약되지 않음. 미래 JWST emission 분광이
  f 의 dayside 가 현재 모델 예측보다 더 차갑다는 것을 드러내면
  CO₂ 압력을 낮춰야 함 (또는 0 으로 설정 — 완전한 snowball).
- "완전한 snowball" (substellar open water 없음) 해석을 위한 cfg
  변형 — 시각적으로 더 단순, 완전히 백색 크림색 세계. substellar
  lens 가 KSP 에서 의미 있게 렌더되기에 너무 marginal 한 것으로
  드러나면 사용.
- "1 bar CO₂ + 완전한 ocean" 해석을 위한 cfg 변형 (Wolf 2017 §5
  best-case). 시각적으로 e 와 유사하지만 더 차갑고 얼음 띠가 더
  많음. 더 깊은 거주 가능 영역 대안이 원해질 때 사용.
- water mass fraction (7–16%) 이 충분히 높아서 f 가 그럴듯하게
  Europa 와 비교 가능한 sub-glacial 액체 물 층을 host 할 수 있음
  — 어떤 조석 / radiogenic 가열이 해저에 도달하면 hydrothermal
  활동을 가질 수도. 직접 시각적이지 않지만 Principia annotation
  가치 있음.
