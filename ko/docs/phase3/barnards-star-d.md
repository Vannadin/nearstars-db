<!-- Barnard's Star d Phase 3 합성. cfg-ready 결정과 근거 -->
# Barnard's Star d — Phase 3 Synthesis

Barnard's Star d 는 Barnard's Star 를 도는 네 sub-Earth 행성 중 가장
안쪽에 있는 행성입니다. González Hernández 외 2024 (ESPRESSO) 가 후보로
식별했고 Basant 외 2025 (MAROON-X 공동 분석) 가 확정했습니다. 2.3402-일
궤도·0.0188 AU 에서 0.003558 L☉ 의 M4 V 호스트로부터 지구의 약 10×
일사를 받으며, 네 행성 중 가장 뜨겁습니다. 평형 온도는 483 K 입니다
(Basant 2025 Table 3, 알베도 0·완전 열재분배 가정). 최소 질량은 MAROON-X
+ ESPRESSO 공동 RV 피팅에서 0.263 ± 0.024 M⊕ 이며, 행성은 transit 을
보이지 않으므로 (Stefanov 2024 의 TESS 비검출, i < 87.9°) 반지름·밀도·조성은
질량-반지름 관계 (DB 반지름 0.694 R⊕) 와 더 폭넓은 hot-rocky / Mercury
analog 에서 추론합니다.

궤도의 최적합 이심률은 낮습니다 (e = 0.04, −0.03/+0.05, Basant 2025 의
β 분포 prior). 원에 가깝지만 정확한 원은 아닙니다. Basant 논문의 SPOCK
동역학적 안정성 테스트는, 이심률 0 과 경사 20°–90° 에서 가장 짧은 주기
행성인 d 의 10⁹ 궤도에 걸쳐 4-행성 구성이 안정적으로 유지됨을 보입니다.
장기 유지를 위해서는 e < 0.02 가 선호됩니다. 2.34-일 주기는 조석 잠금
시간 척도를 8.5–10 Gyr 시스템 나이보다 훨씬 짧게 만들므로 (Walterová
2020 의 despinning 물리), d 는 1:1 동기 회전으로 잠겨 있습니다.

약 10× 일사에서 d 는 Mercury 와 비교됩니다. 모든 거주 가능 영역 정의의
한참 안쪽입니다 (Basant 은 이 호스트의 HZ 가 P = 10–42 d 임을 확인하며,
d 의 2.34-일 궤도는 네 행성 중 가장 안쪽입니다). 이 노쇠한 M 왜성이지만
검출 가능한 고에너지 환경 (González Hernández 2024 가 France 2020 을
인용해 Chandra 로부터 log(L_X/L_bol) ≈ −5.8 을 보고) 과 결합하면, d 의
0.0188 AU 궤도 — 거주 가능 영역보다 다섯 배 더 가까운 — 에서의 내부
시스템 XUV 노출은 Gyr 시간 척도의 대기 유지를 비현실적으로 만듭니다.
cfg 는 Mercury analog 해석을 채택합니다. 노출된 basalt 표면, 별바람
sputtering 으로 생성되는 잔여 sodium-vapor exosphere, 그리고 의미 있는
대기 차폐 없음.

**NearStars 시나리오 선택. 산화철 basalt regolith, 더 따뜻한 substellar
영역 (마그마가 아닌 뜨거운 암석 — T_eq 483 K 는 silicate solidus 를 한참
밑돕니다), 그리고 sputtering 으로 구동되는 얇은 Na exosphere 를 가진,
뜨거운 조석잠금 sub-Earth 노출 암석 행성입니다. 네 Barnard 행성 중 가장
뜨거운 d 는 이 시스템에서 "그을린 암석" 렌더링의 시각 벤치마크입니다.**
이는 canonical-aligned 합성입니다. 궤도·bulk 매개변수는 Basant 2025 로
직접 추적되고, 표면·exosphere 시각은 윈도우 내 tie-break 입니다. 문서화된
divergence 는 없습니다 — d 는 너무 새로 발견되어 canonical climate 모델이
아직 없으며, tie-break 선택들에는 발산할 만한 weight-advantaged canonical
reading 자체가 없습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.34-d 궤도 → 시스템 나이를 한참 밑도는 조석 잠금 (Walterová 2020 despinning 물리) |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.04 | medium | Basant 2025 Table 3 (e = 0.04, −0.03/+0.05, β-prior). 1σ 이내에서 원 궤도와 일관. 안정성은 e < 0.02 선호 |
| `sidereal_period_days` | 2.3402 ± 0.0003 | high | Basant 2025 Table 3 |
| `semi_major_axis_au` | 0.0188 ± 0.0003 | high | Basant 2025 Table 3 |
| `argument_of_periapsis_deg` | −51.8 | medium | Basant 2025 Table 3 (낮은 ecc → 약한 제약, −93.5/+190.8) |
| `epoch_jd` | 2460243.70 | high | Basant 2025 Table 3 t₀ (BJD−2450000 = 10243.70) |
| `mass_mearth` | 0.263 ± 0.024 | high | Basant 2025 Table 3 (M sin i) |
| `radius_rearth` | 0.694 | medium | DB 질량-반지름 관계 (비-transit → 측정 반지름 없음). 네 행성 중 가장 안쪽의 질량-반지름 스케일링 |
| `surface_gravity_g_earth` | 0.55 | medium | 유도 = 0.263 / 0.694² |
| `density_g_cc` | 4.34 | medium | 유도 = 5.513 · 0.263 / 0.694³ (DB 질량-반지름 반지름에서 따름. 지구 bulk 보다 낮은 이유는 M-R 관계가 0.26 M⊕ 바디에 상대적으로 큰 반지름을 부여하기 때문) |
| `insolation_s_earth` | 10.07 | high | 유도 = L/a² = 0.003558 / 0.0188² |
| `equilibrium_temp_k` (A=0, full redistribution) | 483 | high | Basant 2025 Table 3 (footnote a. 알베도 0·완전 열재분배) |
| `equilibrium_temp_k` (A=0.3) | 453 | high | 유도 = 278.3·(L·0.7)^0.25/√a, 지구 analog Bond 알베도 |
| `bond_albedo` | 0.10 | medium | Tie-break. 뜨거운 노출 암석 범위 0.06–0.15. Mercury 0.12. 철이 풍부한 더 어두운 basalt → 0.10 중간값 |
| `surface_temp_substellar_k` | 700 | medium | Tie-break. 무대기 substellar 피크 (재분배 없음, A=0) = T_eq,full·√2 ≈ 700 K. silicate solidus (~1300 K) 를 한참 밑돌아 → 뜨거운 고체 암석, 용융 없음 |
| `surface_temp_nightside_k` | 100 | medium | Tie-break. Mercury 영구 그림자 극지 크레이터의 무대기 cold-trap analog. basalt regolith 의 열관성 → ~100 K |
| `atmosphere_present` | false (잔여 Na exosphere 만) | medium | Tie-break. 10 S⊕ + 내부 시스템 XUV 가 strip 을 강력하게 선호. Mercury analog Na exosphere |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break. Mercury Na exosphere 칼럼 ~10¹⁰ atoms cm⁻² ↔ ~10⁻⁹ Pa 등가 (Mercury exosphere analog) |
| `atmosphere_composition` | Na 우위 sputter exosphere. 미량 K, Ca, Mg | low | Tie-break. Mercury analog. basalt regolith 에 대한 Barnard 바람 sputtering |
| `atmosphere_tint_rgb_hex` | n/a | high | 유도 (가시 대기 없음) |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `ocean_present` | false | high | T_eq 483 K 가 표면 물 배제 |
| `surface_tint_rgb_hex_primary` | `#6a3a26` (딥 레드 별 아래 산화철 basalt regolith) | medium | Tie-break. Mercury 류 ferrous 표면 × M 왜성 SED |
| `surface_tint_rgb_hex_accent` | `#9c5532` (더 따뜻한 substellar regolith + 약간 상승한 열복사) | medium | Tie-break. 가장 뜨거운 substellar 영역이 더 따뜻하게·오렌지로 읽힘. 483 K 에서는 마그마 없는 뜨거운 노출 암석 |
| `surface_morphology` | impact 크레이터 basalt, 더 따뜻한 노출 암석 substellar 영역. antistellar cold-trap regolith | medium | Tie-break. Mercury analog + 10 S⊕ 열 강제 (483 K 에서 용융 없음) |
| `magnetic_field_present` | true (약함, 유도) | low | Tie-break. 작은 철 코어 + Barnard 바람 → 유도-구동 장. Mercury analog |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break. Mercury 류 매우 작은 코어 쌍극자 (Mercury 유추, 다이너모 모델링 아님) |
| `radiation_belt_present` | false | high | 대기 없음 + 무시 가능 B-field → trapped 집단 없음 |
| `surface_radiation_dose_msv_yr` | 10000 | low | Context-cite 스케일링 (Atri 2020 류 무대기 dose + 내부 시스템 XUV). 캐시에 Barnard 특화 표면-dose 논문 없음 — 자릿수 추정만 |
| `atmospheric_shielding_g_cm2` | 0 | high | 무대기 |
| `aurora_present` | false | high | 여기시킬 대기 없음 |
| `star_apparent_angular_diameter_deg` | 5.3 | high | 유도 = 2 R★/a × (180/π), R★ = 0.187 R☉ |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff (González Hernández 2024) |

## Surface synthesis

Barnard d 의 표면은 4-행성 시스템에서 가장 뜨겁습니다. substellar
dayside 는 약 700 K 까지 오릅니다 — 10× 일사·알베도 0 에서의 무대기
재분배-없음 한계 (T_eq,full · √2) — 한편 완전 열재분배 하의 행성-전체
평형 온도는 483 K 입니다 (Basant 2025 Table 3). 결정적으로 700 K 는
silicate solidus (~1300 K) 를 한참 밑돕니다. d 는 용암 세계가 아니라
뜨거운 *고체* 암석입니다. 따라서 substellar 반구는 마그마 풀이 아니라
더 따뜻하고 오렌지빛의 regolith 영역 (액센트 톤 `#9c5532`) 으로 렌더링됩니다.
이는 의도적인 물리 게이트입니다 — cfg 는 483 K 바디에 용융 표면을 두지
않으며, 인용된 어떤 내부 가열 메커니즘 (조석, 유도) 도 근-원형 궤도의
0.26 M⊕ 행성에 대해 용융 온도에 도달하지 않습니다.

antistellar 반구는 깊이 차가운 (~100 K) 휘발성 cold-trap 이며, Mercury
의 영구 그림자 극지 크레이터의 analog 이지만 nightside 반구 전체를
포괄합니다. ~9 Gyr 에 걸쳐 혜성이나 성간 먼지 유입으로 전달된 휘발성은
여기 sequester 될 수 있습니다 — 물 얼음, 황 화합물, sodium — 비록 1.8
pc 의 sub-Earth USP 행성에 대해 직접 검출은 불가능합니다. terminator 의
bedrock 은 산화철 basalt (`#6a3a26` cfg 톤) 이며, 폭넓은 Mercury /
hot-rocky regolith 템플릿과 일관됩니다. M 왜성 조명이 인지된 색을 더욱
따뜻한 빨강-갈색 쪽으로 기울입니다.

표면 형태는 전적으로 Mercury analog 에서 추론됩니다. ~9 Gyr 의 누적
충돌 cratering 이 양 반구에 걸쳐 있습니다. cfg 는 이를 `surface_morphology`
필드에 인코딩합니다. 특정 게임 내 지형 생성은 따뜻한 substellar 패치를
더 매끄럽고 오렌지빛의 regolith 로, 차가운 antistellar 반구를 크게
cratered 된 지형으로 편향해야 합니다.

## Atmosphere synthesis

d 는 통상적인 의미의 대기가 없습니다. 0.55 g 표면 중력과 ~700 K
substellar 온도에서, 어떤 plausible 2차 대기에 대해서도 Jeans escape
매개변수는 Gyr 시간 척도에 걸쳐 손실에 유리합니다. H₂ 는 열적으로
escape 하고, H₂O 는 해리되어 H 가 escape 하며, CO₂ 는 XUV 광분해되어
더 가벼운 산물이 손실됩니다. González Hernández 2024 는 France 2020 을
인용해 이 노쇠한 M 왜성에 여전히 검출 가능한 고에너지 환경이 있음을
보고합니다 (Chandra 로부터 log(L_X/L_bol) ≈ −5.8). d 의 0.0188 AU
궤도 — 거주 가능 영역보다 다섯 배 더 가까운 — 에서의 내부 시스템 XUV 는
시스템 수명에 걸친 누적 대기 유지를 비현실적으로 만듭니다.

살아남는 것은 Mercury 의 sputter-구동 exosphere analog 입니다. 별바람
이온이 basalt 표면을 두드려 feldspar / pyroxene 격자에서 Na (그리고
정도가 덜한 K, Ca, Mg) 원자를 분리시키며, 그 결과 d 의 온도에서
중력적으로 unbound 이지만 지속 sputtering 으로 유지되는 구름이 됩니다.
칼럼 밀도는 ~10¹⁰ atoms cm⁻², 표면 압력은 ~10⁻⁹ Pa 등가 — 가시 Rayleigh
산란 서명을 한참 밑돌아, cfg 는 `atmosphere_tint_rgb_hex = n/a` 를
설정합니다.

Barnard 의 모데스트한 flare 동안의 에피소드 강화는 예상되지만 Proxima
analog 보다 훨씬 약합니다 (Barnard 은 매우 조용한 노쇠 M 왜성, log R'HK
= −5.82. Toledo-Padrón 2019). Barnard's Star 의 EUV 환경은 Duvvuri 2021
이 재구성했으며 (HST + Chandra 데이터에 대한 DEM 기법), 이것이 복사 환경
컨텍스트를 뒷받침합니다. flare 동안의 일시적 sputtering 증가는 cfg 의
스칼라 톤 해상도에서 가시 exospheric plume 을 만들지 않습니다.

## Rotation & spin synthesis

d 는 1:1 (동기) 로 조석 잠겨 있으며 substellar 점이 행성 프레임 0°
경도에 고정되어 있습니다. 0.162 M☉ M 왜성 주위 0.0188 AU 의 0.26 M⊕
암석 행성에 대한 조석 despinning 시간 척도는 8.5–10 Gyr 시스템 나이보다
훨씬 짧으므로 (Walterová 2020 despinning 물리), 경사는 0° 로 감쇠되고
스핀은 동기화됩니다.

Basant 2025 의 최적합 이심률 (β-prior 에서 e = 0.04) 은 명목상 0 이
아니지만, 안정성 제약은 e < 0.02 를 선호합니다. 이 낮은 이심률에서는
동기 1:1 공명이 고차 (예. 3:2 Mercury 스타일) 구성보다 지배적입니다.
실제 이심률이 posterior 의 높은 쪽에 있다면 작은 pseudo-synchronous
libration (진폭 < 1°) 이 예상되지만, substellar 점은 행성 프레임에서
사실상 고정되어 있습니다.

~10 년 항성 활동 사이클 (Toledo-Padrón 2019. 3800 ± 600 d) 은 substellar
XUV 노출을 수배 변조합니다. 이는 exosphere 칼럼 밀도에 영향을 미치지만
cfg 의 해상도에서 표면 톤에는 영향을 주지 않습니다.

## Visual styling

Barnard d 는 시스템의 시각적 "뜨거운 그을린 암석" 입니다.

- **글로벌 외관.** 딥 레드 M4 V 조명 (`stellar_color_temp_k = 3195`)
  아래 따뜻한 빨강-갈색 원반 (`#6a3a26`). 가장 뜨거운 노출 암석과 약간
  상승한 열복사가 결합한 더 밝고 오렌지빛의 substellar 액센트
  (`#9c5532`) 가 있습니다.
- **Dayside 디테일.** 고전적인 hot-Mercury 위상 곡선 — 거의 0 인 limb
  darkening 과 대기 헤이즈 없는, 완전히 조명되고 거의 균일하게 cratered
  된 dayside.
- **Terminator 밴드.** 헤이즈 링 없는 날카로운 terminator. 전체에 걸쳐
  노출 암석 bedrock 톤.
- **Nightside.** 거의 검은색의 ~100 K cold-trap 반구로 빠르게 페이드
  아웃합니다.
- **대기 헤이즈.** 없음 — Na exosphere 는 가시 산란 서명을 한참 밑돕니다.
- **하늘의 별.** Barnard 는 d 의 하늘에서 5.3° 를 차지 — 지구에서 본
  태양의 약 10× — 하며, 일정한 어둑한 빨강 원반으로 장면을 지배합니다.
- **하늘의 형제 행성들.** b, c, e (모두 비슷하게 컴팩트한 궤도) 는 밝게
  움직이는 점으로 나타나며, 합 시점에 가장 가까운 형제는 작지만 분해
  가능한 원반을 차지합니다.
- **Flare 변조.** Barnard 의 flare 는 활동적인 M 왜성에 비해 약합니다.
  게임 내 렌더링은 짧고 드문 주변광 brightening 사건을 인코딩할 수
  있지만, 미묘합니다.

aurora cfg 필드는 모두 `false` / `n/a` 인데, 여기시킬 대기가 없기
때문입니다. 누적 표면 dose (cfg `surface_radiation_dose_msv_yr = 10000`,
자릿수 추정만) 는 정상 플레이 하에서 치명적 수준에 도달하며, 게임 내
거주 가능성을 불가능하게 만듭니다. d 는 순수하게 플레이어 탐험을 위한
hot-rocky 시각 목적지입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2503.08095** — Basant R. 외 2025, *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`).
  MAROON-X 확인 논문이며 모든 load-bearing 궤도/bulk 값의 출처. P =
  2.3402 ± 0.0003 d, M sin i = 0.263 ± 0.024 M⊕, a = 0.0188 ± 0.0003 AU,
  e = 0.04 (−0.03/+0.05), ω = −51.8°, T_eq = 483 K (A=0, full
  redistribution). e < 0.02 선호로 10⁹ 궤도 SPOCK 안정성, HZ 는 P = 10–42 d.
- **2410.00569** — González Hernández J. I. 외 2024, *A sub-Earth-mass
  planet orbiting Barnard's star* (`2024A&A...690A..79G`). ESPRESSO 발견
  논문. d 후보의 첫 식별. 활동 사이클 3200 d, 회전 140 d. France 2020
  을 인용해 log(L_X/L_bol) ≈ −5.8 (Chandra) 보고.
- **2102.08493** — Duvvuri G. 외 2021, *Reconstructing the EUV Emission
  of Cool Dwarfs*. HST + Chandra 로부터 Barnard's Star EUV 의 DEM 재구성.
  복사 환경 컨텍스트 정보 제공.
- **2007.12459** — Walterová M. & Běhounková M. 2020, *Thermal and
  Orbital Evolution of Low-mass Exoplanets*. 근접 암석 행성의 동기 /
  pseudo-synchronous 회전으로의 조석 despinning. 조석 잠금 결정의 근거.

### Read (context / methodology, not decision-driving)

- **2410.00577** — Stefanov A. K. 외 2024, *A sub-Earth-mass planet
  orbiting Barnard's star: No evidence of transits in TESS photometry*.
  transit 배제 ("no evidence of transiting Barnard b, or any other
  body"). 3σ 상한 i < 87.9°.
- **1812.06712** — Toledo-Padrón B. 외 2019, *Stellar activity analysis
  of Barnard's Star*. P_rot = 145 ± 15 d, 장기 활동 사이클 3800 ± 600 d
  (~10 yr), log R'HK ≈ −5.86. 조용한 호스트·활동 사이클 추론의 기반.

### Read (instrument-only, not visual-informative)

- (제한적. d-특화 deep_read 세트가 작음.)

### Not read — context-cites NOT in the paper cache (flagged for audit)

이들은 이전 드래프트에서 물리 컨텍스트로 인용되었으나
**`docs/phase3/_papers/` 에 없어** 직접 검증할 수 없었습니다. 이들의
구체 수치는 Decisions 헤드라인 값으로 사용하지 않습니다.

- **France K. 외 2020** (arXiv:2009.01259) — *The High-Energy Radiation
  Environment Around a 10 Gyr M Dwarf*. 캐시에 없음. 이전 드래프트의
  구체 수치 (25% flare 듀티 사이클, 0.1 AU 에서 87 지구대기 Gyr⁻¹ 손실,
  ×25–28 스케일링, 10²⁹·²–10²⁹·⁵ erg flare 에너지) 는 검증할 수 없어
  prose 에서 제거했고, González Hernández 2024 가 corroborate 하는 존재 +
  X-ray 컨텍스트만 유지합니다.
- **Atri D. 2020** — 표면 복사 dose 스케일링. 캐시에 없음.
  `surface_radiation_dose_msv_yr` 행은 자릿수 추정만이며 Confidence low.
- **Killen 2007 / Stamenković & Spohn / Makarov 2012 / Kopparapu 2014** —
  analog/context 인용 (Mercury exosphere, 용암 세계 열 모델, spin-orbit
  프레임워크, HZ 안쪽 가장자리). 캐시에 standalone 으로 없음. 헤드라인
  값이 아니라 정성적 analog 으로만 사용.

### Not read — no arXiv preprint or low-priority

d 의 bib 은 이름 충돌 잡음 (혜성 관측자 Barnard + 혜성 "d" 우연) 과
상기 인용된 공유 다행성 논문이 지배합니다. 주목할 스킵 항목.

- Barnard 를 언급하지만 개별 행성 매개변수를 제약하지 않는 다중 저자 M
  왜성 행성 발생률 논문.
- Barnard 를 RV 표준으로 사용하는 TESS 표준 칸델라 광도 논문.

## Open items for follow-up

- **직접 질량 / 반지름 측정**. d 는 transit 을 보이지 않습니다 (Stefanov
  2024). Gaia DR4, JWST-MIRI 와의 미래 astrometric 또는 직접 영상 캠페인이
  실제 질량과 반지름을 산출할 수 있습니다. cfg `radius_rearth = 0.694`
  는 측정이 아니라 DB 질량-반지름 값입니다.
- **질량-반지름 관계에 의한 조성**. M sin i 만으로는 조성 (암석 vs. 철
  농축) 이 제약되지 않습니다. DB 반지름은 ρ ≈ 4.34 g/cc 를 함의하며,
  Mercury 류 철 농축 (더 조밀하고 작은) 내부도 cfg 변이로 viable.
- **France 2020 (2009.01259) 재페치**. 고에너지-환경 논문을 재캐시해
  듀티 사이클과 대기-손실 수치를 직접 검증으로 복원해야 합니다. 그때까지
  대기-손실 prose 는 정성적입니다.
- **표면-dose 논문 (Atri 류)**. 1차 복사 dose 스케일링 레퍼런스를
  캐시해 `surface_radiation_dose_msv_yr` 을 자릿수 추정 이상으로
  단단하게 만들어야 합니다.
- **휘발성 cold-trap 서명**. antistellar cold-trap 은 Gyr 시간 척도에
  걸쳐 전달된 얼음을 retain 할 수 있습니다. 미래 cfg 변이는
  `subsurface_ice` 패치를 추가할 수 있습니다.
- **이심률 vs. 안정성**. Basant 2025 는 e = 0.04 를 보고하지만 안정성은
  e < 0.02 를 선호합니다. 더 단단한 prior 와의 미래 공동 피팅이 궤도
  이심률 (그리고 pseudo-sync libration 노트) 을 개선할 수 있습니다.

## Related

- [barnards-star](barnards-star.md) — 호스트 별. 조용한 노쇠 M4 V. 약한 flare 환경
- [barnards-star-b](barnards-star-b.md) — 다음 바깥 형제 (여전히 뜨거운 암석)
- [barnards-star-c](barnards-star-c.md) — 중간 형제
- [barnards-star-e](barnards-star-e.md) — 가장 바깥. 네 중 HZ 안쪽 가장자리에 가장 가까움
- [proxima-cen-d](proxima-cen-d.md) — analog 비교. 다른 M 왜성 주위의 비슷한 M sin i sub-Earth USP 암석 행성. 그러나 훨씬 강한 flare 환경
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 하류 cfg writer
