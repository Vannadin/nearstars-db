<!-- Proxima Cen b Phase 3 synthesis: cfg-ready 결정과 근거 -->
# Proxima Cen b — Phase 3 Synthesis

NearStars KSP mod 의 Phase 3 행성 synthesis (2026-05-22 작성).

Proxima Cen b 는 1.302 pc 거리의 가장 가까운 거주 가능 행성 후보입니다.
Anglada-Escudé et al. 2016 이 HARPS 의 radial velocity 로 발견, Faria et
al. 2022 (ESPRESSO) 와 Suárez Mascareño et al. 2025 (HARPS+ESPRESSO+
NIRPS 결합) 가 정제. 지구 등급 질량의 세계 (Msini = 1.055 ± 0.055 M⊕,
Suárez Mascareño 2025), 11.18일 궤도, 0.0485 AU, 지구 플럭스의 ~0.65×
수신 — 2904 K M5.5 호스트의 낙관적 거주 가능 영역 안쪽 가장자리 내부.
통과는 검출 안됨 (ASTERIA, TESS, MEarth-South, ATCA 후속의 다년간 탐색
모두 null), 지구 시선 기준 궤도 기울기 < ~87° 의미.

투과 분광이 없어 대기 상태는 직접 관측으로 제약 안되고 이론적 고려에서
추론해야 함. 5 Gyr 동안의 XUV 견인 escape (Ribas et al. 2016, Zahnle &
Catling 2017), N₂/CO₂ 외기 균형 (Tian 2015, Lichtenberg 2024), tidally
locked 조건의 GCM 기후 모델링 (Turbet et al. 2016, Boutle et al. 2017,
Way et al. 2024 의 spin-orbit resonance 모음).

**NearStars 시나리오 선택. 지속적 substellar 해양과 frozen 극을 가진
온화 eyeball-Earth aquaplanet**, 얇은 N₂/CO₂ 대기 (~0.5 bar) 와 산재된
substellar 구름. 이는 JWST 등가 관측 방어 가능성과 2016 발견 발표 이래
대중 인식을 형성한 "Proxima 의 푸른 점" 모티프의 시각적 차별성 사이의
균형. 채택 desiccated 맨 암석 대안 (Ribas 2016 escape-dominated 케이스) 은
cfg variant 로 보존.

## Decisions

Kopernicus / atmosphere cfg-ready 값.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 11.2 d 궤도, 조석 damping; Barnes 2017 |
| `obliquity_deg` | 0 | medium | 조석 damping, 이 궤도의 쌍성 perturbation 무시 가능 |
| `eccentricity` | 0.02 | medium | Suárez Mascareño 2025; Faria 2022 와 일관; A16 의 0.35 덜 신뢰 |
| `sidereal_period_days` | 11.18465 | high | Suárez Mascareño 2025 |
| `semi_major_axis_au` | 0.04848 | high | Suárez Mascareño 2025 |
| `mass_mearth_msini` | 1.055 | high | Suárez Mascareño 2025 RV |
| `mass_mearth_true_adopted` | 1.30 | medium | 채택. 기울기에 대해 23% 상향 (sin i ≈ 0.81 prior; Mendillo et al. 2018 통계) |
| `radius_rearth` | 1.07 | medium | M_true × Earth-like rock-iron MR 관계 (Zeng 2016) 에서 도출 |
| `surface_gravity_g_earth` | 1.14 | medium | 도출 |
| `density_g_cc` | 6.0 | medium | Earth-like 암석 조성 |
| `equilibrium_temp_k` (A=0.3) | 234 | high | a/R★, T★=2904 K 에서 도출 |
| `equilibrium_temp_k` (A=0) | 254 | high | 도출 |
| `bond_albedo` | 0.20 | medium | substellar 구름 피드백 (Boutle 2017) ~30%; 부분 구름 cover 가 ~20% net |
| `atmosphere_present` | true | low | 채택 시나리오; Tian 2015 N₂ 보존 가능 |
| `atmosphere_surface_pressure_pa` | 50000 | low | ~0.5 bar; 부분 대기 escape 감안하면 Mars (~600 Pa) 와 Earth (~10⁵ Pa) 의 중간 |
| `atmosphere_composition` | N₂ (70%) + CO₂ (28%) + H₂O (2%) | low | Tian 2015 외기 균형; H₂O 변광 |
| `atmosphere_scale_height_km` | 6 | medium | T~250 K, μ~36 g/mol (N₂+CO₂ 혼합), g=11.2 m/s² 에서 도출 |
| `atmosphere_tint_rgb_hex` | `#f0c8a8` (옅은 tan-blue limb) | medium | deep-red M-dwarf 조명 아래 Rayleigh + 얇은 Mie 산란이 흐릿한 하늘 색조 생성 |
| `dayside_substellar_temp_k` | 282 | medium | Turbet 2016 GCM. ~50% 구름 cover 의 open-ocean substellar warm pool |
| `dayside_average_temp_k` | 220 | medium | 대기 순환 + 알베도 피드백 |
| `nightside_average_temp_k` | 175 | medium | 적당 대기에서 약한 day-night 열 수송; antistellar 점에 빙모 |
| `substellar_ocean_present` | true | low | Pierrehumbert 2011 + Boutle 2017 GCM — substellar pool 은 M-dwarf 조명 아래 역학 안정 |
| `surface_ice_fraction_pct` | 70 | low | substellar circle 외 글로벌 빙 coverage (eyeball Earth 시나리오) |
| `surface_ocean_fraction_pct` | 20 | low | substellar ice-free 영역 |
| `surface_continent_fraction_pct` | 10 | low | 조성 도출; 어느 정도 육지 가능 |
| `surface_tint_rgb_hex_ocean` | `#1a4060` (적색 조명 아래 깊은 푸름) | low | 해양 H₂O 흡수 + M-dwarf 적색 선호 반사 |
| `surface_tint_rgb_hex_ice` | `#e0d8c0` (M-dwarf 아래 warm-tint 빙) | low | 적색 조명 아래 ice 산란 |
| `surface_tint_rgb_hex_continent` | `#604020` (어두운 basalt + 산화철 weathering) | low | 어두운 적색 색조 terrain |
| `magnetic_field_strength_microtesla_equator` | 35 | medium | Earth-mass dipole 스케일링 (Olson & Christensen 2006); Garraffo 2016 MHD 컨텍스트 |
| `magnetic_dipole_moment_normalized_earth` | 0.55 | medium | 1.07 R⊕ 와 tidally-locked 자전 (지구의 10× 더 느림) 에서 |
| `magnetosphere_standoff_planet_radii` | 1.5 | medium | Garraffo 2016 — 강한 Proxima wind 가 magnetopause 압축 |
| `radiation_belt_present` | true | low | 약한 dipole + 더 hard 한 stellar wind 로 지구보다 넓은 trapping 영역 |
| `surface_radiation_dose_msv_yr_quiet` | 50 | medium | 평상 배경; 대기 차폐 ~5 g/cm² |
| `surface_radiation_dose_msv_yr_superflare_event` | 1e6 | medium | MacGregor 2018 + Atri 2019 — superflare proton 폭풍 |
| `flare_event_rate_per_yr_observable_at_planet` | 100 | high | Howard 2018 을 b 궤도에 스케일링 |
| `aurora_present` | true | medium | 강한 stellar wind + B-field 가 강한 오로라 활동 부여 |
| `aurora_color_primary_hex` | `#A0E0B0` | low | tie-break. 두꺼운 N₂+CO₂ 대기 아래 [OI] 5577 Å 여기에서 녹색 가시 |
| `aurora_color_secondary_hex` | `#E090A0` | low | proton-driven Hα 6563 Å 발광 (적색); flare 동안 MacGregor superflare 이벤트가 이를 지배 |
| `aurora_oval_magnetic_latitude_deg` | 50 | medium | 약한 dipole 이 더 넓은 oval; Vidotto 2013 스케일링 |
| `aurora_intensity_kR_quiet` | 80 | medium | quiet Proxima wind 가 적당한 오로라 |
| `aurora_intensity_kR_flare` | 5000 | medium | flare/superflare 밝기 |
| `induction_heating_w_per_m2` | 0.05 | medium | Kislyakova 2018 sub-Earth 스케일링, 약한 기여 |
| `star_apparent_angular_diameter_deg` | 1.5 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2904 | high | Passegger 2019 SED 피팅 |

## Surface synthesis

Proxima b 는 정통 M-dwarf eyeball 행성 후보. Pierrehumbert 2011 이 tidally
locked aquaplanet 의 "eyeball Earth" 기후 상태를 처음 articulate. deep-red
M-dwarf 조명 아래, ice-albedo 피드백이 집중된 substellar 가열과 결합하여
호스트 별 바로 아래에 작은 액체 물 영역을 가진 글로벌 frozen world 생성.
substellar liquid 대 글로벌 ice 비는 insolation, 대기 열 수송 효율, 자전
상태에 의존.

Boutle et al. 2017 의 Proxima b 에 특화된 1-bar N₂+H₂O 대기 GCM 시뮬레이션은
eyeball 상태가 역학적으로 안정 — substellar 점의 대류 updraft 가 그렇지
않으면 극에서 inward 로 전파될 sea ice 를 효율적으로 제거하고, substellar
영역의 결과 구름 cover 가 안정화 알베도 피드백 제공 ("M-dwarf 구름 억제"
메커니즘이 *runaway-greenhouse* 경로가 아님).

Turbet et al. 2016 이 세 시나리오 고려.
- (A) Earth-twin 1-bar N₂+H₂O. ~30% 표면 ice-free 의 eyeball. 채택.
- (B) 1-bar CO₂ + ice 의 snowball 상태. 훨씬 낮은 CO₂ 분압에서만 안정.
- (C) 두꺼운 CO₂ 대기의 hot greenhouse. 역학적으로 불안정; Myr 시간 척도에서
  (A) 로 붕괴.

NearStars cfg 는 (A) 를 canonical 케이스로 채택.

**색 선택.** 해양. M-dwarf 조명 아래 매우 깊은 푸름 — 물은 매우 강한
장파장 흡수가 있어 단파장에서의 선호 반사가 매우 작은 입사 플럭스로 공급
(M dwarf SED 가 IR 지배), 가시-밴드 반사가 표면당으로는 Earth 의 해양보다
*더 푸르*되 절대 밝기로는 *더 어두움*. RGB ≈ `#1a4060`.

**표면 빙.** H₂O 빙 위 M-dwarf 조명은 warm-tinted 반사 생성 (빙은 가시광에서
밝아 적색 SED 수용). RGB ≈ `#e0d8c0`. 극관은 deep red-illuminated 어두운
세계의 warm cream-white fringe 로 출현.

**대륙.** M-dwarf 세계의 맨 basalt + 산화철 weathering 은 TRAPPIST-1 d 에서처럼
표면 산화 경향. 대륙 (존재 시) 은 빙모와 substellar 해양 사이 어두운
brown-red 패치로 출현.

**Substellar 영역 형태.** 지속적 대류 구름이 있는 open ocean; 구름 cover
~50% (Boutle 2017). 구름 덮인 해양은 substellar 점에 ~30° 시직경의 밝은
cream-white 원으로 출현, 주변 빙에 embedded. 이것이 eyeball Earth 의
"눈" — 상징적 시각 feature.

**Cratering.** ~5 Gyr 나이 + tidally locked → leading hemisphere crater 비대칭
(Mercury 의 노년 표면과 유사), 그러나 야간/극 영역의 ice resurfacing 과
substellar 해양의 sediment burial 로 부분적으로 지워짐.

**거주 가능성 컨텍스트.** Heller & Armstrong 2014 의 "Superhabitable worlds"
는 K-dwarf 와 더 이른 M-dwarf 온화 세계가 호스트의 더 긴 주계열 수명으로
안정 장기 baseline 기후를 가짐을 강조. 5 Gyr 의 Proxima b 는 중년이며 (A)
가 초기 상태라면 그 기간 동안 안정 온화 조건을 호스팅했을 수 있음.

## Atmosphere synthesis

Proxima b 의 직접 대기 관측 없음. XUV 역사, 조석 잠금, 평형 화학에서의
이론적 추론.

**XUV escape 역사.** Ribas et al. 2016 이 b 의 5 Gyr 누적 XUV flux 모델링.
~10× 현재 지구 값 시간 적분. 1–10 Earth-ocean 질량의 물 손실을 hydrodynamic
escape 로 견인하기에 충분. 초기 물 인벤토리가 Earth-like 였다면, *잔류*
물 예산이 불확실 — fully desiccated (Zahnle & Catling 2017 wet 케이스) 와
~Earth-equivalent (행성이 훨씬 많은 초기 물을 가졌다면) 사이.

**대기 보존.** Tian 2015 N₂ 보존 모델은 1-bar N₂ 대기가 b 궤도의 Earth-mass
행성에 대해 thermal escape 에 안정 예측. 비-thermal escape (sputtering,
stellar wind 의 ion pickup) 가 더 공격적 — Garraffo et al. 2016 MHD 모델은
stellar wind 강화 동안 부분 대기 stripping. Net. 현재 ~0.1–1 bar N₂ 대기
가능.

**조성.** Earth-like fO₂ 의 mantle 에서의 외기 균형은 dominant N₂ + CO₂
(~70:28) 와 trace H₂O 생성. CH₄ 와 NH₃ 는 M-dwarf XUV 에 의해 volcanic
외기로 보충될 수 있는 것보다 빠르게 광해리. H₂O 광해리에서 O₂ 축적
가능하나 인벤토리는 escape rate 에 민감 (Meadows 2017 false-positive
biosignature 분석).

**대기 순환.** 표준 tidally-locked GCM 은 강한 substellar updraft, 적도
superrotating jet, terminator-zone descending air 의 단일 반구 대류 cell
생성. day-night 열 재분배 효율은 표면 압력에 의존 — 0.5 bar 에서 야간
온도가 ~175 K 로 조절 (CO₂ condensation 위, CO₂ 빙 cap 없음).

**번개.** Braam et al. 2023 이 tidally locked Earth-like 세계의 번개 화학
모델링. substellar updraft 의 lightning-driven NO 생성이 Earth rate 의
~30%, 검출 가능한 대기 화학 서명 생성. NearStars 시각. substellar cloud
deck 아래 야간 통과 동안 가시 가끔의 번개 섬광.

**구름 구조.** Cohen et al. 2022 가 "traveling planetary-scale waves" 가
tidally locked aquaplanet 의 구름 변광 생성을 보임 — 행성파 속도 (~며칠
시간 척도) 로 회전하는 stratus 패치. 시각. terminator 영역의 subglacial
구름 띠, ~3-일 시간 척도에 fragmenting 과 reforming.

**오존.** Chen et al. 2023 이 동기적으로 회전하는 외계행성의 성층권 오존
모델링. 오존은 day-night terminator 에 photolytic transport 로 집중. 시각.
terminator 에만 옅은 UV-blue 오존 layer (글로벌 아님).

**Flare 대기 화학.** b 궤도 (0.0485 AU) 에 스케일된 Howard 2023 flare 통계는
행성 위치에서 ~100 flare/yr 부여. 각 이벤트가 대기를 일시적으로 30–80%
해리, post-flare relaxation phase 동안 NO₂/NO 로 condense 하는 반응성
질소 species 의 "flare smog" 생성.

## Rotation & spin synthesis

조석 잠금은 b 궤도에서 본질적으로 확실. 동기화 시간 척도 << 5 Gyr (Barnes
2017 의 적당 viscosity). Spin-orbit 상태 가능성.

- **1:1** (default) — 궤도 이심률 ≈ 0 이 이 상태 선호. 채택.
- **3:2** — 과거에 궤도가 더 이심적이었다면 가능 (Way et al. 2024 가 유사
  행성들에 고려).

**Obliquity = 0.** Gyr 시간 척도의 조석 damping 이 강한 동반자 perturbation
없는 tidally locked 세계의 자전축 기울기를 0 으로 견인. Proxima 의 wide
AB hierarchical 궤도가 현 에포크에서 b 의 spin axis 에 무시 가능 perturbation
제공.

**Day-night cycle 없음.** 1:1 잠금과 0 자전축 기울기로 substellar 점이 표면
좌표에 고정. 시각. 일주 조명 변광 없음, terminator drift 없음. 유일한 시간
척도는 별 자전 주기 (83 d) 가 생성하는 느린 별 디스크 자전과 합 (conjunction)
동안 Alpha AB 의 일식/엄폐를 생성하는 궤도 주기 (11.2 d).

**Day-night 열 수송.** 정상상태 insolation 기하임에도 대규모 대기 순환이
강한 day-night 열 수송 생성. substellar warm pool (282 K) 은 anti-stellar
cold spot (~150 K 의 full atmospheric heat transport; 대기 얇거나 stripped
일 때 ~120 K) 에 대해 균형.

## Visual styling

표면과 대기 결정의 조합.

- **전체 색 팔레트.** Proxima 에서 deep-red 환경 조명 지배. substellar
  영역이 warm cream (구름 + 빙 + 해양 혼합) 글로우; 극 영역은 어두운
  warm-cream 빙; 대륙 (있다면) 은 어두운 brown-red basalt.
- **Substellar 뷰.** "상징적" Proxima b 외관. 위에서 substellar 점을 내려다보면
  세계는 Pierrehumbert 의 eyeball Earth 닮음 — 밝은 중앙 구름-덮인 해양이
  빙으로 둘러싸임. 구름 중심에 검출 가능한 형태 (폭풍, 대류 cell).
- **Terminator 띠.** 가장 동적인 영역. 구름 띠가 fragment 와 reform; 얇은
  오존 layer 가 day-night 경계에 공간에서 가시 옅은 UV-blue 글로우 생성;
  ±50° 자기 위도에 집중된 입사 stellar wind proton 의 오로라 발광.
- **Nightside.** 매우 어둡고 차가움 (~175 K). insolation 없음; Alpha AB
  (cream-yellow) 의 반사광, 오로라 글로우 (greenish-red), substellar 구름
  대류 동안 가끔의 번개 섬광만. Milky Way 와 Alpha AB 가 야간 하늘 지배.
- **대기 헤이즈.** 0.5 bar 대기는 옅은 pale tan-blue limb 헤이즈 (~10 km
  두께) 생성, 검은 우주 limb 조명에 대해서만 가시.
- **하늘의 별.** Proxima 시직경 ~1.5° (지구에서 보는 태양의 3× 시직경).
  Deep red-orange (`~#ff6028`), 83-일 자전 주기에 drift 하는 흑점 complex
  로 가시적 freckled. 궤도에서 태양-질량 등가 조명 (~0.65 S⊕).
- **하늘의 sister 행성 d.** Proxima d 는 0.0288 AU 로 b 보다 별에 가까움.
  b 와의 inferior conjunction 시 d 는 ~0.02 AU (~3 백만 km) 안으로 지나감
  — 수 시간 동안 밝은 ~mV -2 별로 출현 후 후퇴. 궤도가 완전 coplanar 가
  아니어서 full transit 은 아님.
- **하늘의 Alpha AB.** V ≈ -7 의 찬란한 점, cream-yellow, 수 세기 걸쳐
  매우 느리게 drift 하는 위치에서 ~2°. 검출 가능한 그림자 던질 정도로 밝음.
- **Flare 이벤트 시각.** 약 4일에 한 번 flare 가 Proxima 를 분 동안 5–50×
  밝게 함. substellar 영역이 짧은 강한 UV-blue 빛 pulse 수신, 정상 적색
  조명 wash out. 오로라가 극적으로 강화. 조명 효과는 b 주변 어떤 KSP
  게임플레이에서나 jarring — "활동적 M dwarf 근처에 사는 것" 의 주요 feature.
- **Superflare 이벤트.** b 의 궤도 위치에서 ~1 yr 마다 ~10³³ erg flare 가
  Proxima 를 100–1000× 밝게. 30분 지속, 행성이 짧게 다중-태양 등가 플럭스
  수신, 대기 화학과 오로라 폭풍 trigger.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2016Natur.536..437A** Anglada-Escudé et al. 2016 — Proxima b 발견 paper.
  발견 시점 결정적 RV 특성화.
- **2022A&A...658A.115F** Faria et al. 2022 — ESPRESSO 정제 + Proxima d
  발견. b 의 더 나은 질량 제약 (Msini 1.07 ± 0.06).
- **2025A&A...700A..11M** Suárez Mascareño et al. 2025 — HARPS + ESPRESSO
  + NIRPS 결합 분석. b 와 d 의 Phase 2 추천에 사용된 정제 파라미터.
- **2016A&A...596A.111T** Turbet et al. 2016 — 세 대기 시나리오 (snowball,
  eyeball, greenhouse) 의 Proxima b 용 GCM 시뮬레이션. (A) eyeball 시나리오
  선택 견인.
- **2017MNRAS.471.4628B** Boutle et al. 2017 — M-dwarf 조명 아래 eyeball
  안정성을 보여주는 cloud-resistant ocean GCM.
- **2016ApJ...823L..14R** Ribas et al. 2016 — Proxima b 의 XUV escape
  역사. 시간 적분 대기 손실 추정.
- **1607.06677** Zahnle & Catling 2017 — 대기 escape 결과 envelope.
  맨 암석 케이스를 cfg 대안으로.
- **1802.00141** Hu et al. 2018 — M-dwarf 행성의 biohabitability. UV-flare
  컨텍스트.
- **2204.09270** Diamond-Lowe et al. 2022 — Proxima 의 동시 X-ray + FUV
  모니터링. b 궤도의 방사선 환경 정량화.
- **2306.03004** Chen et al. 2023 — 동기 회전 외계행성의 성층권 오존.
  terminator-zone 오존 시각 견인.
- **2209.12502** Braam et al. 2023 — tidally locked Earth-like 의 번개
  화학. 번개 시각 견인.
- **2211.11887** Cohen et al. 2022 — 행성파에서의 구름 변광. terminator
  zone 구름 역학 견인.
- **2410.19108** Way et al. 2024 — spin-orbit resonance 기후 변형. 3:2
  대안 cfg 제공.
- **2402.12253** Schreyer et al. 2024 — 물 vapor 통과 retrieval 모호성.
  대기 retrieval 기대 컨텍스트.
- **2204.03501** Quick et al. 2023 — Tidal-driven tectonic 활동.
  b 가 판 tectonics 가능 주장.

### Read (context / methodology, not decision-driving)

- **2312.01893** Lichtenberg et al. 2024 — HZ 암석 외계행성의 물 함량.
  초기 물 예산 컨텍스트.
- **MacGregor et al. 2018 (1803.07581)** — 2016년 3월 ALMA superflare.
  b 궤도의 superflare rate envelope 견인.
- **2102.06318** Howard et al. 2018 — ASAS-SN flare 누적 분포.
- **1706.04617** Garraffo et al. 2016 — Proxima b 의 star-planet 자기
  상호작용 MHD 시뮬레이션. 자기권 standoff 견인.
- **1909.13740** Garraffo et al. 2020 — 업데이트된 wind 모델.
- **1805.00929** Morel 2018 — AB 쌍의 화학 조성; 시스템 나이와 금속함량
  컨텍스트.
- **2410.01621** Garraffo et al. 2024 — Magnetized wind.
- **1802.00141** Mullan & MacDonald 2018 — 거주 가능성 물리.

### Read (instrument-only, not visual-informative)

- **2503.18538** PIAA/nuller 코로나그라프 paper.
- **2311.18117** 고대비 이미징으로의 biosignature 검출. future-instrument
  컨텍스트.

### Not read — no arXiv preprint available (84 papers)

미독 핵심 예시.
- "A Catalog of Habitable Zone Exoplanets" — 컨텍스트만.
- "Prospects for Cryovolcanic Activity on Cold Ocean Planets" — 흥미롭지만
  b 의 파라미터 영역 밖 (b 는 우리 cfg 의 cold-ocean 이 아니라 substellar
  warm pool 의 eyeball).
- Alpha + Proxima 주위의 다수 SETI 탐색 paper — null 결과, 방법론만.

**사용자 액션 요청.** JWST 나 미래 직접 이미징 미션 (HabEx, LUVOIR 후속)
이 b 의 실제 대기 분광을 생성하면, 전체 대기 섹션이 수정 필요. 2025–2026
ELT 직접 이미징 캠페인 (Carlomagno 2023 framework) 이 첫 반사광 제약을
생성할 수 있음.

---

## Open items for follow-up

- b 의 궤도 기울기 미제약 (통과 검출 없음). 채택된 Msini → M_true factor
  1.23 은 Mendillo 2018 통계 prior; 진정한 직접 측정이 질량을 좁힘.
- Pierrehumbert eyeball 상태 가정은 Boutle 2017 기준 robust 하나 초기 물
  인벤토리에 의존; b 가 진정으로 desiccated (Ribas 2016 worst case) 라면
  시각은 baked Mars 에 더 가까움 (cfg variant 필요).
- Earth 등가 자기장 가정 (35 μT 적도) 은 지구 dipole 스케일링 기반; b 가
  조석 잠금으로 인해 더 약한 dynamo 가지면 field 가 < 10 μT 가 될 수 있고
  오로라가 훨씬 밝고 더 낮은 위도가 됨.
- 3:2 spin-orbit resonance variant (Way 2024) 는 daylight 이동 사이클 생성
  — 두드러지게 다른 cfg.
- 번개 rate (Braam 2023) 와 시각 섬광 빈도가 더 나은 시각 렌더링 필요 —
  substellar cloud-deck 통과 동안 미세한 subglacial 섬광으로 출현해야.
- flare 일정 (b 궤도에서 100/yr) 이 b 의 "거주 조건" 을 어떤 KSP 승무원
  운영에도 주목할 만하게 적대적으로 만듦 — 방사선 게임플레이를 위해
  cfg 코멘트에 강조 가치.
- 2030 까지의 직접 이미징 follow-up (NEAR, ELT, KPIC) 이 표면과 대기
  시각을 Phase 4 cfg 수정이 정당화되는 수준까지 정제 가능.
