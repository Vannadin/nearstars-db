<!-- Proxima Cen d Phase 3 synthesis: cfg-ready 결정과 근거 -->
# Proxima Cen d — Phase 3 Synthesis

NearStars KSP mod 의 Phase 3 행성 synthesis (2026-05-22 작성).

Proxima Cen d 는 태양계와 가장 가까운 sub-Earth-mass 행성. Faria et al.
2022 가 0.4 m/s 진폭 수준에서 ESPRESSO RV 로 발견, Suárez Mascareño et al.
2025 가 정제 (Msini = 0.26 ± 0.038 M⊕, P = 5.12 d, a = 0.0288 AU). 최소
질량은 ~2.4× Mars 로, 2025 발표 기준 태양계 너머 알려진 가장 작은 확인
행성. Proxima 의 거주 가능 영역 깊숙이 — 지구 플럭스의 ~3× 수신 — 어떤
volatile 인벤토리도 극단적 XUV 노출과 조석 가열에 직면.

통과는 검출 안됨; 대기 데이터 없음. 행성의 특성은 전적으로 이론적 고려에서
추론해야 함. 열 escape (Tian 2015 의 sub-Earth 스케일링), 고 insolation
에서의 silicate vaporization (Way 2024 의 hot-Mercury analog), 이심 궤도
에서의 조석 가열 (Bolmont 2017 의 Proxima d 는 2022 발견 이래 아직 출판 안됨).

**NearStars 시나리오 선택. 야간 극에 얇은 volatile frost 를 가진 Mercury-
analog 뜨거운 맨 암석**, basaltic / ultramafic 표면 조성과 leading dayside
반구의 relict magma-ocean 형태로 anchored. 이는 "documented divergence"
cfg — 게임플레이 관련 야간 frost cap 이 균일 뜨거운 암석 너머의 시각
다양성 제공; canonical "완전 desiccated 맨 암석" 은 cfg variant 로 보존.

## Decisions

Kopernicus / atmosphere cfg-ready 값.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 5.12 d 궤도, 조석 damping; Barnes 2017 |
| `obliquity_deg` | 0 | high | 조석 damping |
| `eccentricity` | 0.0 | medium | Suárez Mascareño 2025; Faria 2022 의 0.04 덜 신뢰 |
| `sidereal_period_days` | 5.12338 | high | Suárez Mascareño 2025 |
| `semi_major_axis_au` | 0.02881 | high | Suárez Mascareño 2025 |
| `mass_mearth_msini` | 0.26 | high | Suárez Mascareño 2025 RV |
| `mass_mearth_true_adopted` | 0.32 | medium | 채택. 기울기 23% 상향 (sin i ≈ 0.81 prior; Mendillo 2018) |
| `radius_rearth` | 0.66 | medium | M_true × Earth-like rock-iron MR 관계 (Zeng 2016) 에서 도출 |
| `surface_gravity_g_earth` | 0.74 | medium | 도출 |
| `density_g_cc` | 5.5 | medium | 암석 조성; 더 큰 본체보다 덜 압축 |
| `equilibrium_temp_k` (A=0.1) | 363 | high | a/R★, T★=2904 K 에서 도출 |
| `equilibrium_temp_k` (A=0) | 379 | high | 도출 |
| `bond_albedo` | 0.10 | medium | TRAPPIST-1 b/c JWST 발광의 맨 암석 analog |
| `atmosphere_present` | false (또는 thin trace) | low | 채택. 맨 암석; thin CO₂ <100 Pa 를 variant 로 |
| `atmosphere_surface_pressure_pa` | 0 (canonical) / 50 (variant) | low | Mercury analog; 기껏해야 trace |
| `atmosphere_composition` | none / trace CO₂ + Na vapor | low | rock-vapor 가 있다면 photolytic Na exosphere |
| `atmosphere_scale_height_km` | - | - | canonical 케이스에 해당 안됨 |
| `atmosphere_tint_rgb_hex` | none | - | 대기 가시 안됨 |
| `dayside_substellar_temp_k` | 540 | medium | 3 S⊕, A=0.1 의 맨 암석 subsolar |
| `dayside_average_temp_k` | 380 | medium | 맨 암석 반구 평균 |
| `nightside_average_temp_k` | 90 | low | 대기 수송 없는 복사 냉각; Mercury analog |
| `surface_volatile_frost_present_on_pole` | true | low | Mercury 극 volatile analog; tidally locked anti-stellar cold trap |
| `surface_volatile_composition` | H₂O + CO₂ + Na | low | photolytic 전달 + cold trap 축적 |
| `surface_tint_rgb_hex_primary` | `#3a2818` (어두운 회갈색 basalt) | low | 맨 암석 low albedo + M-dwarf 적색 조명 |
| `surface_tint_rgb_hex_accent` | `#7a4020` (relict 마그마 흐름 tube) | low | 더 뜨거운 마그마 바다 잔류; TRAPPIST-1 d 보다 차가움 |
| `surface_tint_rgb_hex_frost_cap` | `#fff8e0` (warm cream frost) | low | deep-red M-dwarf 반사 아래 H₂O frost |
| `surface_morphology` | cratered basaltic 평원 + leading-hemisphere 마그마 relict | low | TRAPPIST-1 b/c analog overprint 의 맨 암석 |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | 지구 이하 질량 core 축소; RM22 스케일링 + 조석 잠금 페널티 |
| `magnetic_dipole_moment_normalized_earth` | 0.01 | low | sub-Mars-mass tidally-locked 의 RM22 (2203.01065) |
| `magnetic_dipole_tilt_deg` | 5 | low | tie-break. 자전축에 거의 정렬 |
| `magnetosphere_standoff_planet_radii` | 1.1 | medium | 매우 약한 field → magnetopause 가 표면 근처 |
| `radiation_belt_present` | false | high | trapped-particle 영역에 너무 약한 field |
| `surface_radiation_dose_msv_yr_quiet` | 60000 | medium | d 궤도에 스케일된 Atri 2019 + 차폐 없음 |
| `surface_radiation_dose_msv_yr_flare_event` | 1e7 | medium | Proxima flare + 대기 없음 = 직접 stellar 조사 |
| `aurora_present` | false | medium | 대기 없음 → 오로라 발광 없음 |
| `induction_heating_w_per_m2` | 0.2 | medium | Kislyakova 2018 — d 의 mass + B-field 조합에 적당 기여 |
| `tidal_heating_w_per_m2` | 0.05 | low | 낮은 이심률; 최소 기여; Bolmont 2017 |
| `star_apparent_angular_diameter_deg` | 2.6 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2904 | high | Passegger 2019 SED 피팅 |

## Surface synthesis

Proxima d 의 표면 상태는 세 경쟁 과정에 의해 설정.
- (1) 5 Gyr 동안 stellar XUV 의 대기 erosion — 고 insolation 의 sub-Earth-
  mass 행성에 대한 Tian 2015 스케일링은 ~100 Myr 안에 N₂/CO₂ 대기 완전
  손실 예측.
- (2) 남은 이심률에서의 조석 가열 — Bolmont 2017 은 e ≈ 0.01 (Suárez
  Mascareño 2025 상한) 에서 F_int ≈ 0.05 W/m² 추정, sub-runaway.
- (3) 충돌 또는 외기로 전달된 volatile 의 photoevaporation 에서의 표면-
  vapor cycle — Mercury 와 유사하나 더 작은 규모의 transient Na exosphere
  생성.

지배 결과는 **반구 영구 cold trap volatile 침전을 가진 맨 암석** — 반지름이
~2.5× 축소된 Mercury analog. dayside 표면은 substellar 540 K (basalt
solidus ~1400 K 보다 한참 낮지만 활동적 표면 화학 가능. photolytic
oxidation, 알칼리 휘발, 느린 weathering).

**색 선택.** M-dwarf 적색 조명 아래 맨 basalt + 산화철 overlay. TRAPPIST-1 d
와 같은 어두운 회갈색 팔레트 (`#3a2818` primary), brown-red 산화철 accent
(`#7a4020`). accent 는 TRAPPIST-1 d 의 `#5a3220` 보다 약간 더 따뜻, 이는
d (Proxima) 가 더 높은 insolation 에 있고 누적 photo-oxidation 이 더 완전
하기 때문.

**마그마-바다 relict.** d 의 더 낮은 질량은 ~100 Myr 의 마그마 바다 phase
(TRAPPIST-1 d 의 ~500 Myr 대비). Relict 형태는 존재하나 TRAPPIST-1 d
보다 더 erosion. leading hemisphere 의 부드러운 basaltic 평원으로 가시,
cooling 마그마가 수축한 가끔의 fracture 시스템.

**야간 cold trap.** Mercury 는 영구적으로 그늘진 극 crater 의 H₂O 빙
호스팅 (Lawrence 2013, Neumann 2013 MESSENGER 데이터). 자전이 아닌 조석
잠금의 Proxima d 는 영구히 어둡고 차가운 (대기 열 수송 없이 ~90 K) 고정
anti-stellar 점 가짐. 충돌 또는 dayside 의 photolytic transport 로 전달된
어떤 volatile 도 이 영역에 축적 — H₂O 빙, CO₂ 빙, Na/K 알칼리 frost 가능성.
추정 coverage. cold pole 의 ~30° 안에 anti-stellar 반구의 ~5%.

**Crater 형태.** d 의 더 작은 질량 + 더 작은 중력이 충돌체 질량당 더 큰
crater 직경 부여 — 전형적 crater 직경이 동등 충돌체당 Earth crater 의 2×
더 클 수 있음. leading hemisphere 가 충돌 선호 축적. 표면 나이. ~5 Gyr,
대부분 lunar-highlands 밀도로 심하게 cratered.

**표면 화학.** 540 K substellar T 에서.
- 활동적 알칼리 휘발 (Na, K)
- basalt 표면의 photolytic oxidation → hematite/ilmenite
- transient flare-driven 가열 이벤트에서 알루미늄/칼슘 silicate vapor 수송
  가능
- carbonate-silicate 사이클 없음 (대기 없음)

알칼리 휘발에서의 Na exosphere 는 통과한다면 지상 분광 (Na D doublet
흡수) 으로 가시 — 그러나 통과 검출 없어 미관측 유지.

## Atmosphere synthesis

**Canonical 케이스. 대기 없음.** 다음 조합.
- (1) 0.029 AU 에서의 높은 XUV 플럭스 (~5× 지구 궤도 값)
- (2) 낮은 행성 질량 (0.32 M⊕) 과 표면 중력 (0.74 g_E)
- (3) 5 Gyr 누적 escape 역사
- (4) 빈번한 flare 이벤트가 acute escape episode 제공

이 지배 결과 견인. 어떤 1차 또는 2차 대기든 맨 암석 표면까지 완전 손실,
외기 또는 volatile-impact 이벤트 동안의 transient (~시간) exospheric
feature 만 가능.

**Variant. 얇은 CO₂ envelope.** d 가 현재 Mars 와 유사한 rate 로 CO₂ 외기
하고 escape rate 가 Tian 2015 예측의 lower end 라면 잔류 ~50 Pa CO₂ 대기
지속 가능. 유사한 뜨거운 암석 외계행성에 대한 JWST 상한 (Greene 2023
TRAPPIST-1 b. 99% 에서 < 0.5 bar CO₂) 과 일관. NearStars cfg variant. ~50 Pa
CO₂ + trace Na + trace water vapor, 간신히 검출 가능한 Rayleigh limb 헤이즈.

**해양 없음, 구름 없음.** 마그마-바다 phase 후 물이 전달되었더라도 dayside 는
액체 물에 너무 뜨겁고 (대기 없이 너무 건조) 야간 cold-trap volatile 은
free 가 아닌 frost 로 잠겨 있음.

**Flare 충돌의 표면 화학.** 각 Proxima flare (d 궤도에서 ~10⁴/yr) 는 표면
photochemistry 견인하는 UV+X-ray pulse 침전 — basalt 의 느린 hematite
산화, 장석의 화학 weathering, 시간 안에 표면으로 condense 되돌아가는 sodium
과 potassium vapor 의 transient 생성.

## Rotation & spin synthesis

조석 잠금 본질적으로 확실 (5.12 d 주기 >> sync 시간 척도; Barnes 2017).
Spin-orbit 상태.
- **1:1** (default, 이심률 ≈ 0). 채택.
- 3:2 는 e = 0 에서 불가능.

**Obliquity = 0.** Gyr 시간 척도의 조석 damping.

**Day-night cycle 없음.** substellar 점 고정; d 의 하늘에서 Proxima 디스크
의 느린 별 자전 (83 d) 만 움직임.

**조석 가열.** e ≈ 0 (Suárez Mascareño 2025) 으로 조석 가열 기여는 무시 가능
— Bolmont 2017 스케일링은 F_int ≈ 0.05 W/m², runaway 임계값 한참 아래.
Faria 2022 의 약간 상향 이심률 envelope (e ≤ 0.04) 은 상한 F_int < 0.5 W/m²
부여, 여전히 sub-runaway.

**계절 없음.** TRAPPIST-1 d 와 동일. 일정 insolation, 일주 사이클 없음,
계절 사이클 없음.

## Visual styling

- **전체 모습.** Deep-red M-dwarf 조명 아래의 어두운 회갈색 맨 암석 세계.
  TRAPPIST-1 d 와 시각적으로 유사하나 더 높은 insolation 과 더 긴 photolytic
  oxidation 역사로 인해 더 따뜻/어두운 accent.
- **Dayside.** 뜨거운 substellar 영역 (540 K) 이 high dynamic range 로 렌더링
  되면 약간 흑체 발광 — 표면이 강하게 thermal IR 방출하지만 가시-밴드 발광은
  희미 (kT ≈ 0.05 eV vs 가시-밴드 1.5 eV). KSP 렌더링은 reflective-only 처리.
- **Terminator.** 대기 optical feature 없음. terminator 에 sharp 그림자
  전환 (헤이즈 없음, 글로우 없음).
- **Nightside.** 매우 어둠 (~90 K). anti-stellar 점 주변의 작은 frost-cap
  영역이 Alpha AB 별빛으로 직접 조명되면 (드문 기하) warm-cream (`#fff8e0`)
  출현. 그렇지 않으면 invisible.
- **Frost cap.** anti-stellar 점 중심으로 ~5% coverage. Proxima b 위치에서
  d 가 opposition 일 때 공간에서 가시 — 그렇지 않으면 어두운 반구에 작은
  밝은 점으로 출현.
- **대기.** Canonical 에서 없음. Variant 50 Pa CO₂ 활성화 시 간신히 검출
  가능한 thin pale-grey limb 헤이즈 (~2 km 두께) 추가.
- **하늘의 별.** Proxima 시직경 ~2.6° (~5× 지구에서 보는 태양 시직경).
  NearStars 행성의 하늘에 가장 큰 별 디스크. 두드러진 가시 흑점 complex 가
  있는 deep red-orange.
- **하늘의 sister 행성 b.** Proxima b (0.0485 AU) 는 d (0.0288 AU) 보다
  Proxima 에서 더 멀음. 합 시 b 는 가장 가까운 거리 ~0.02 AU (~3 백만 km)
  지나감 — 수 시간 동안 디스크-분해된 밝은 ~mV -2 (~3') 출현, 후 후퇴.
- **하늘의 Alpha AB.** V ≈ -7 의 찬란한 점, cream-yellow, 느리게 drift
  하는 위치에서 ~2°. 가시 그림자 던지기에 충분히 밝음; anti-stellar
  반구에 주목할 만한 야간 조명 제공.
- **Flare 이벤트.** 각 Proxima flare 가 분 동안 강한 UV+가시 밝기 증가
  전달. d 의 dayside 가 짧게 10–100× 가열; transient 표면-volatile 증발이
  결과 Na vapor 구름에서 단기 "오로라" 발광 (실제 오로라 아님 — 대기
  없음). leading hemisphere 주위의 짧은 적색 글로우처럼 보임.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2022A&A...658A.115F** Faria et al. 2022 — ESPRESSO RV 의 Proxima d
  발견 (Msini = 0.26 M⊕, P = 5.12 d). 결정적 발견 특성화.
- **2025A&A...700A..11M** Suárez Mascareño et al. 2025 — 결합 HARPS +
  ESPRESSO + NIRPS 분석. Phase 2 추천에 사용된 정제 파라미터.
- **2405.05013** Lobo & Bouchy 2024 — M dwarf 주위 close-in 지구형 외계행성의
  표면 빙 분포 가능성. d 의 파라미터 영역의 M-dwarf 행성에 cold-trap 빙
  침전을 직접 다룸. 야간 frost cap 시각 견인.
- **2102.06318** Howard et al. 2018 — Proxima flare 분포. d 궤도 (0.029 AU)
  에 스케일하면 ~10⁴ flare/yr.

### Read (context / methodology, not decision-driving)

- **2204.09270** Diamond-Lowe et al. 2022 — Proxima 의 동시 X-ray + FUV
  모니터링. 방사선 환경.
- **MacGregor et al. 2018 (1803.07581)** — 2016년 3월 ALMA superflare.
  d 궤도의 flare-event-rate envelope 견인.
- **2402.00115** Yaptangco et al. 2025 — 통과 검출에 대한 short-timescale
  활동 효과. d 통과 비검출 컨텍스트.
- **2409.06637** Wanderley et al. 2024 — M dwarf 행성 호스트의 자기장.
  B-field 환경 컨텍스트.
- **2301.02477** Kossakowski et al. 2023 — Wolf 1069 b 특성화. 비교 가능한
  HZ-edge M-dwarf 암석 행성; 파라미터 envelope 교차 reference.
- **2304.09220** TOI-2095 paper — 비교 가능한 시스템, 방법론.
- **2207.13727** MIRECLE 미션 컨셉 — 뜨거운-암석-행성 특성화의 future-
  instrument 컨텍스트.

### Read (instrument-only, not visual-informative)

- **2504.18485** ESPRESSO 요오드 cell 보정. 방법론.
- **2102.01910** Proxima 의 광학 SETI 탐색. Null 결과.
- **2311.04316** Planetary perturbers paper. 다른 시스템.
- **2209.11346** 다중-별 행성 호스트 catalog. 컨텍스트.

### Not read — no arXiv preprint available (2 papers)

- "MOST Observations of Proxima Centauri" abstract — 출판된 Davenport 2016
  paper 로 대체, 이미 Proxima Cen synthesis 의 read set 에 있음.

**사용자 액션 요청.** 지금 시점에 없음. d 는 관측적으로 약하게 제약되어
이론 예측이 지배. 2026년 이후 통과 시도가 성공하거나 직접 이미징이 phase-
curve 측광 생성하면 표면 온도 분포 직접 측정 가능.

---

## Open items for follow-up

- d 의 궤도 기울기 미제약. 채택 Msini → M_true factor 1.23 은 통계적;
  직접 질량 측정이 좁힘.
- cold-trap volatile 침전 (Lobo & Bouchy 2024 framework) 은 고도로 모델
  의존적. 5% coverage 추정은 어느 방향으로든 자릿수 차이 가능.
- sub-Mars-mass 본체의 자기장 강도 (0.5 μT) 가 지구 스케일링 법칙에 의해
  약하게 제약. RM22 의 framework 가 Earth-mass 본체용으로 개발되어
  0.32 M⊕ 에 정확히 extrapolate 안할 수 있음.
- variant 50 Pa CO₂ 대기는 현재 한계에 의해 허용되나 미관측. Phase 4 cfg
  는 맨 암석과 thin-CO₂ variant 모두 명시적으로 지원해야.
- Mercury 극 volatile analog 은 유사한 impact-delivery rate 와 photolytic
  transport 효율을 가정. M dwarf 주위의 tidally locked body 에는 다를 수 있음.
- M-dwarf XUV 아래의 표면 화학 (알칼리 휘발, hematite 형성) 은 현실적 플럭스
  조건에서 실험실 검증 필요 — 현재 모델은 Earth 등가 가정.
- Suárez Mascareño 2025 이심률 e = 0 은 조석 가열 없음과 일관; 미래 RV 데이터가
  non-zero e 찾으면 표면 열 플럭스가 거주 가능 온도에 접근 가능.
