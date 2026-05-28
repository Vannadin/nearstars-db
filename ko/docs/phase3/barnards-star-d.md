<!-- Barnard's Star d Phase 3 합성. 4행성 시스템에서 가장 안쪽·가장 뜨거운 sub-Earth, Mercury 닮은 시각 벤치마크 -->
# Barnard's Star d — Phase 3 Synthesis

Barnard's Star d 는 González Hernández 외 2024 (ESPRESSO) 가 발표하고
Basant 외 2025 (MAROON-X 공동 분석) 가 확정한 4개 sub-Earth 행성
가족 중 가장 안쪽 행성입니다. 0.0188 AU·2.34-일 궤도에서 0.00356 L☉
의 M4 V 호스트로부터 지구의 약 10× 일사를 받는 — 네 행성 중 가장
뜨거운 — 행성으로, 평형 온도는 Basant 2025 Table 3 의 알베도 0,
완전 열재분배 가정에서 483 K, 대기 수송이 없을 때는 최대 496 K
까지 올라갑니다. 최소 질량은 MAROON-X + ESPRESSO 공동 RV 로 0.263
± 0.024 M⊕ 이며, 행성은 transit 을 보이지 않으므로 (Stefanov 2024
TESS 비검출) 반지름, 밀도, 조성은 질량-반지름 스케일링과 더 폭넓은
Mercury / hot-rocky-USP analog 에서 추론됩니다.

궤도는 약간의 이심률을 가지며 (Basant 2025 의 β 분포 prior 에서
e = 0.04 ± 0.05), 정확한 원이 아니지만 그에 가깝습니다. Basant 논문의
SPOCK 동역학적 안정성 테스트는 4-행성 구성이 가장 짧은 주기 행성인
d 의 10⁹ 궤도에 걸쳐 안정적으로 유지됨을 보입니다 (이심률 0, 경사
20°–90° 의 경우). 장기 유지를 위해서는 e < 0.02 가 선호됩니다. 2.34-일
주기는 조석 잠금 시간 척도를 10⁵ 년 훨씬 아래로 두므로 (Walterová 2020
스케일링), d 는 1:1 spin-orbit 동기 구성으로 잠겨 있습니다.

지구의 10× 일사에서 d 는 초기 금성이나 Mercury 와 비교됩니다 — 모든
거주 가능 영역 정의의 한참 안쪽입니다. Kopparapu 2014 의 M4 V 호스트
내부 가장자리는 ~0.1 AU (P = 10 d) 이며, d 의 0.0188 AU 궤도는 별에서
5× 더 가깝습니다. Barnard 의 flare 환경 (France 2020. ~25% 듀티 사이클,
0.1 AU 에서 ~87 지구대기 Gyr⁻¹ 의 열적 escape) 과 결합하면, d 거리에서
의 내부 시스템 XUV 노출은 ~28× 만큼 스케일 업되어 — d 의 대기 유지
전망은 거의 없습니다. cfg 는 Mercury analog 해석을 채택합니다. 노출된
basalt 표면, 별바람 sputtering 으로 생성되는 잔여 sodium-vapor exosphere,
그리고 의미 있는 대기 차폐 없음.

**NearStars 시나리오 선택. 부분적으로 녹은 substellar 풀, 그 외에는
산화철 basalt regolith, sputtering 으로 구동되는 얇은 Na exosphere
를 가진 뜨거운 조석잠금 Mercury 류 sub-Earth 암석 행성입니다. 네
Barnard 행성 중 가장 뜨거운 — d 는 이 시스템에서 "그을린 암석" 렌더링
의 시각 벤치마크입니다.** 32 cfg 픽 중 16 은 canonical-aligned (궤도
+ bulk + 유도 열량), 16 은 tie-break (표면 시각, 조성, exosphere,
자기장) 입니다. 문서화된 divergence 는 없습니다 — d 는 너무 새로
발견되어 canonical climate 모델이 아직 없습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.34-d 궤도 → 조석 잠금 < 10⁵ yr (Walterová 2020 스케일링) |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.04 | medium | Basant 2025 β-prior 피팅. 1σ 이내에서 원 궤도와 일관. 안정성은 e < 0.02 선호 |
| `sidereal_period_days` | 2.3402 ± 0.0003 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0188 ± 0.0003 | high | Basant 2025 |
| `argument_of_periapsis_deg` | −51.8 | medium | Basant 2025 (낮은 ecc → 약한 제약) |
| `epoch_jd` | 2460243.7 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.263 ± 0.024 | high | Basant 2025 Msini |
| `radius_rearth` | 0.65 | medium | Tie-break. 비-transit. 0.26 M⊕ 지구 analog 암석의 질량-반지름 → 0.60–0.70 R⊕. interesting-first 가 0.65 선택 |
| `surface_gravity_g_earth` | 0.62 | medium | 유도 = 0.263 / 0.65² |
| `density_g_cc` | 5.3 | medium | Tie-break. 지구 analog 암석. Mercury 밀도 5.4 대안도 윈도우 내 |
| `insolation_s_earth` | 10.07 | high | L = 0.00356 L☉ 와 a = 0.0188 AU 로 유도 |
| `equilibrium_temp_k` (A=0, full redistribution) | 483 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 575 | high | dayside 공식으로 유도 |
| `equilibrium_temp_k` (A=0.1) | 470 | high | 유도 |
| `bond_albedo` | 0.10 | medium | Tie-break. 뜨거운 노출 암석 범위 0.06–0.15. Mercury 0.12. partial-melt 가 더 어둡게 — 0.10 중간값 |
| `surface_temp_substellar_k` | 800 | medium | Tie-break. 무대기 dayside 스케일링 → ~830 K. 얇은 Na exosphere + 열 재분배 → ~800 K |
| `surface_temp_nightside_k` | 100 | medium | Tie-break. Mercury 극지 그림자 analog 의 무대기 cold-trap. basalt regolith 의 열관성 → ~100 K |
| `atmosphere_present` | false (잔여 Na exosphere 만) | medium | Tie-break. 10 S⊕ + flare 환경이 strip 을 강력하게 선호. Mercury analog Na exosphere |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break. Mercury Na exosphere 칼럼 ~10¹⁰ atoms cm⁻² ↔ 10⁻⁹ Pa 등가 (Killen 2007 analog) |
| `atmosphere_composition` | Na 우위 sputter exosphere. 미량 K, Ca, Mg | low | Tie-break. Mercury analog. basalt regolith 에 대한 Barnard 바람 sputtering |
| `atmosphere_tint_rgb_hex` | n/a | high | 유도 (가시 대기 없음) |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `ocean_present` | false | high | T > 600 K 가 표면 물 배제 |
| `surface_tint_rgb_hex_primary` | `#6a3a26` (딥 레드 별 아래 산화철 basalt regolith) | medium | Tie-break. Mercury 표면 ferrous 환원 × M 왜성 SED |
| `surface_tint_rgb_hex_accent` | `#9c5532` (substellar partial-melt magma 글로우 + 열복사 피크) | medium | Tie-break. T_substellar ≥ 800 K → partial silicate melt 가시. 열복사가 dayside 색에 기여 |
| `surface_morphology` | impact 크레이터 basalt 와 substellar partial-melt 풀. antistellar cold-trap regolith | medium | Tie-break. Mercury analog + 10 S⊕ partial-melt 열 강제 |
| `magnetic_field_present` | true (약함, 유도) | low | Tie-break. 작은 철 코어 + Barnard 바람 → 유도-구동 장. Mercury analog |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break. Mercury 류 매우 작은 코어 쌍극자 |
| `radiation_belt_present` | false | high | 대기 없음 + 무시 가능 B-field → trapped 집단 없음 |
| `surface_radiation_dose_msv_yr` | 10000 | medium | Atri 2020 스케일링. 무대기 + 10 S⊕ XUV × France 2020 flare 듀티 사이클. Proxima d 보다 낮은 이유는 Barnard 의 flare 에너지가 10⁴× 작기 때문 |
| `atmospheric_shielding_g_cm2` | 0 | high | 무대기 |
| `aurora_present` | false | high | 여기시킬 대기 없음 |
| `star_apparent_angular_diameter_deg` | 5.3 | high | 유도. 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard d 의 표면은 4-행성 시스템에서 가장 뜨겁습니다 — 약 800 K
의 substellar dayside 온도가 노출된 암석 조건에서 지구의 10× 일사
에 의해 유지됩니다. substellar 반구는 철이 풍부한 basalt 가 연화되고
풀처럼 모이는 partial-melt 영역을 호스팅합니다. cfg 는 이를 더 따뜻한
액센트 톤 (`#9c5532`) 으로 인코딩해 d 를 더 차가운 노출 암석 형제들과
시각적으로 구분합니다. 이는 (a) 완전 고화 regolith (더 보수적, 낮은
일사의 Mercury) 와 (b) 진정한 마그마 바다 (이 크기에서 10 S⊕ 보다
더 높은 일사 필요) 사이의 tie-break 선택입니다. Partial-melt 풀은
지구 질량 행성에 대한 5–10 S⊕ Stamenković & Spohn 의 열 모델, 그리고
조석 잠금 하에서의 지속적인 substellar 열 강제와 일관됩니다.

antistellar 반구는 깊이 차가운 (~100 K) 휘발성 cold-trap 이며, Mercury
의 영구 그림자 극지 크레이터의 analog 이지만 nightside 반구 전체를
포괄합니다. 10 Gyr 에 걸쳐 혜성이나 성간 먼지 유입으로 전달된
휘발성은 여기 sequester 될 수 있습니다 — 물 얼음, 황 화합물, sodium
— 비록 1.8 pc 의 sub-Earth USP 행성에 대해 직접 검출은 불가능합니다.
terminator 의 bedrock 은 산화철 basalt (`#6a3a26` cfg 톤) 이며 더
폭넓은 Mercury / hot-rocky regolith 템플릿과 일관됩니다. M 왜성
조명이 인지된 색을 더욱 따뜻한 빨강-갈색 쪽으로 기울입니다.

표면 형태는 전적으로 Mercury analog 에서 추론됩니다. 4 Gyr 의 누적
충돌 cratering, 그리고 근-substellar 영역에 매끄러운 화산 평원을
생성할 수 있는 substellar partial-melt 흐름이 덮입니다. cfg 는 이를
`surface_morphology` 필드에 인코딩합니다. 특정 게임 내 지형 생성은
substellar 패치를 더 매끄러운 텍스처로, 차가운 antistellar 반구를
크게 cratered 된 지형으로 편향해야 합니다.

## Atmosphere synthesis

d 는 통상적인 의미의 대기가 없습니다. 0.62 g 표면 중력과 800 K
substellar 온도에서, 어떤 plausible 2차 대기에 대해서도 Jeans escape
매개변수는 Gyr 시간 척도에 걸쳐 손실에 유리합니다. H₂ 는 열적으로
escape 하고, H₂O 는 해리되고 H 가 hydrodynamic 하게 escape 하며, CO₂
는 XUV 광분해되어 더 가벼운 산물이 손실됩니다. France 2020 (arXiv:2009.01259)
은 Barnard 의 HZ (0.1 AU) 에서 자기장 없는 1 M⊕ 행성에 대해 누적 대기
손실을 ~87 지구대기 Gyr⁻¹ 로 모델링했고, d 의 0.0188 AU 와 0.26 M⊕
질량으로 외삽하면 단위 면적당 효과 속도는 약 25× 더 높아 10 Gyr 누적
대기 유지를 비현실적으로 만듭니다.

살아남는 것은 Mercury 의 sputter-구동 exosphere analog 입니다. 별바람
이온이 basalt 표면을 두드려 feldspar / pyroxene 격자에서 Na (그리고
정도가 덜한 K, Ca, Mg) 원자를 분리시키며, 그 결과 d 의 온도에서
중력적으로 unbound 이지만 지속 sputtering 으로 유지되는 구름이 됩니다.
칼럼 밀도는 ~10¹⁰ atoms cm⁻², 표면 압력은 ~10⁻⁹ Pa 등가 — 가시 Rayleigh
산란 서명을 한참 밑돌아, cfg 는 `atmosphere_tint_rgb_hex = n/a` 를
설정합니다.

Barnard 의 모데스트한 flare 동안의 에피소드 강화는 예상되지만 Proxima
analog 보다 훨씬 덜 극적입니다. France 2020 은 개별 사건을 ~10²⁹·²
– 10²⁹·⁵ erg 로 검출했고, Proxima 의 ~10³³-erg superflare 보다 수
자리수 작습니다. flare 상태 동안의 강화된 XUV (Duvvuri 2021. quiescent
대비 ~8× EUV) 는 일시적인 sputtering 증가를 구동하지만, cfg 의 스칼라
톤 해상도에서 가시 exospheric plume 을 만들지는 않습니다.

## Rotation & spin synthesis

d 는 1:1 (동기) 로 조석 잠겨 있으며 substellar 점이 행성 프레임 0°
경도에 고정되어 있습니다. 0.16 M☉ M 왜성 주위 0.0188 AU 의 0.26
M⊕ 암석 행성에 대한 조석 감쇠 시간 척도는 Walterová 2020 스케일링
에서 10⁵ 년을 한참 밑돌아, 10 Gyr 시스템 나이보다 훨씬 짧습니다.
경사 또한 0° 로 감쇠되어 있습니다.

Basant 2025 의 최적합 이심률 (β-prior 에서 e = 0.04) 은 명목상 0 이
아니지만, 안정성 제약은 e < 0.02 를 선호합니다. 낮은 이심률에서는
동기 공명이 고차 (예. 3:2 Mercury 스타일) 구성보다 지배적입니다
(Makarov 2012 프레임워크). libration 진폭은 작으며 (< 1°), substellar
점은 행성 프레임에 고정되어 있습니다.

10 년 항성 활동 사이클 (Toledo-Padrón 2019) 은 substellar XUV 노출을
수배 변조합니다. 이는 exosphere 칼럼 밀도에 영향을 미치지만 cfg 의
해상도에서 표면 톤에는 영향을 주지 않습니다.

## Visual styling

Barnard d 는 시스템의 시각적 "뜨거운 그을린 암석" 입니다. 딥 레드 M4
V 조명 (`stellar_color_temp_k = 3195`) 이 산화철 basalt 표면과 결합해
따뜻한 빨강-갈색 글로벌 톤 (`#6a3a26`) 을 만들고, partial-melt 흐름과
약간 상승한 열복사가 결합해 색을 오렌지 쪽으로 이동시키는 더 밝은
substellar 액센트 (`#9c5532`) 가 있습니다.

궤도에서 보면, 행성은 고전적인 hot-Mercury 위상 곡선을 보입니다.
대기 헤이즈 없는 날카로운 terminator, 거의 0 인 limb darkening,
거의 검은색에 가까운 nightside 로 빠르게 페이드 아웃하는 완전히
조명된 dayside. Barnard 는 d 의 하늘에서 5.3° 를 차지 — 지구에서 본
태양의 약 10× — 하며, 일정한 어둑한 빨강 원반으로 시각 장면을 지배합니다.

Barnard 의 flare 사건은 d 에 모데스트한 밝기 변조만 만들지만 (France
2020 사건은 Proxima 의 것에 비해 약함), ~25% 듀티 사이클은 flare 상태
조명이 빈번한 발생임을 의미합니다. 게임 내 렌더링은 게임 시간 1 지구
주당 1–2 회 짧은 (~5000 s) 주변광 brightening 사건을 인코딩해야
합니다. aurora cfg 필드는 모두 `false` / `n/a` 인데, 여기시킬 대기가
없기 때문입니다.

d 표면의 객체에 대한 누적 표면 dose (cfg `surface_radiation_dose_msv_yr
= 10000`) 는 정상 플레이 조건 하에서 치명적 수준에 도달하며, 게임 내
거주 가능성을 불가능하게 만듭니다. 행성은 순수하게 플레이어 탐험을
위한 hot-rocky 시각 목적지입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). MAROON-X 확인 논문. P = 2.3402 ± 0.0003 d,
  Msini = 0.263 ± 0.024 M⊕, a = 0.0188 ± 0.0003 AU, T_eq = 483 K
  (A=0, full redistribution) 보고. e < 0.02 에 대한 10⁹ 궤도에 걸친
  SPOCK 안정성.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO 발견 논문. d 의 첫 후보 식별. 활동 사이클 3200 d. 회전
  140 d.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra. 25% flare 듀티 사이클. 0.1 AU 에서 87
  지구대기/Gyr 열적 손실 (d 의 0.0188 AU 에서 스케일 업).
- **Duvvuri G. et al. 2021** — *Reconstructing the EUV Emission of
  Cool Dwarfs* (arXiv:2102.08493). quiescent + flaring EUV 플럭스
  재구성. 복사 환경 cfg 정보 제공.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). 조석 잠금
  시간 척도 스케일링.

### Read (context / methodology, not decision-driving)

- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). TESS 데이터에서 d transit 배제.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). 호스트 활동 사이클 + 회전.
  대기 escape 계산의 기반.

### Read (instrument-only, not visual-informative)

- (제한적. d-특화 deep_read 세트가 작음.)

### Not read — no arXiv preprint or low-priority (~150 papers)

d 의 bib 은 이름 충돌 잡음 (혜성 관측자 Barnard + 혜성 d-letter 우연)
과 상기 인용된 공유 다행성 논문이 지배합니다. `docs/phase3/_bib/barnards-star-d.yaml`
에 `status: skipped` 로 보존됩니다. 주목할 항목.

- Barnard 를 언급하지만 개별 행성 매개변수를 제약하지 않는 다중
  저자 M 왜성 행성 발생률 논문
- Barnard 를 RV 표준으로 사용하는 TESS 표준 칸델라 광도 논문

## Open items for follow-up

- **직접 질량 / 반지름 측정**. d 는 transit 을 보이지 않습니다
  (Stefanov 2024). Gaia DR4 또는 JWST-MIRI 와의 미래 astrometric
  또는 직접 영상 캠페인이 실제 질량 + 반지름을 산출할 수 있습니다.
  cfg `radius_rearth = 0.65` 는 tie-break placeholder.
- **질량-반지름 관계에 의한 조성**. Msini 만으로는 조성 (암석 vs.
  얼음 풍부) 가 제약되지 않습니다. cfg 는 암석 지구 analog 밀도
  (5.3 g/cc) 를 기본값으로 사용하며, Mercury 류 철 농축 (~6.5 g/cc)
  내부도 viable.
- **Partial-melt 형태**. substellar partial-melt 영역은 tie-break
  선택입니다. 10 S⊕ 의 0.26 M⊕ 암석 행성에 대한 Stamenković
  스타일 열 모델은 substellar-대-심부 열 구배를 개선할 수 있습니다.
- **휘발성 cold-trap 서명**. antistellar cold-trap 은 10 Gyr 에 걸친
  성간 먼지 유입으로 전달된 물 얼음과 다른 휘발성을 retain 할 수
  있습니다. 미래 cfg 변이는 `subsurface_ice` 패치를 추가할 수 있습니다.
- **별바람 sputtering 수율**. cfg 는 Mercury analog Na exosphere
  를 tie-break 으로 채택합니다. Barnard 에 맞춤화된 직접 MHD 바람
  시뮬레이션은 존재하지 않습니다. 노쇠하고 조용한 M 왜성에 대한
  Garraffo 스타일 3D 바람 모델이 exosphere 칼럼 밀도를 개선할 것입니다.
- **이심률 vs. 안정성**. Basant 2025 는 e = 0.04 를 보고하지만 안정성은
  e < 0.02 를 선호합니다. 더 단단한 prior 와의 미래 공동 피팅이
  궤도 이심률을 개선할 수 있습니다.

## Related

- [barnards-star](barnards-star.md) — 호스트 별. 조용한 노쇠 M4 V. Proxima 보다 덜 공격적인 flare 환경
- [barnards-star-b](barnards-star-b.md) — 외곽 형제 (여전히 뜨거운 암석). Ribas 반박 후 canonical "b" 라벨
- [barnards-star-c](barnards-star-c.md) — 중간 형제. T_eq 가 금성에 비교 가능
- [barnards-star-e](barnards-star-e.md) — 가장 바깥. 네 중 HZ 안쪽 가장자리에 가장 가까움
- [proxima-cen-d](proxima-cen-d.md) — analog 비교. 다른 M 왜성 주위의 비슷한 Msini sub-Earth USP 암석 행성. 그러나 훨씬 강한 flare 환경
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 하류 cfg writer
