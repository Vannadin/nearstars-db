<!-- Barnard's Star b Phase 3 합성. 4행성 시스템의 헤드라인 sub-Earth, Ribas 2018 반박 후 새로 정의된 b -->
# Barnard's Star b — Phase 3 Synthesis

Barnard's Star b 는 두 번째로 가까운 항성 호스트 주위 4-행성
ESPRESSO/MAROON-X 시스템의 원래 "헤드라인" 행성입니다. González
Hernández 외 2024 가 발견 논문에서 bona-fide 확정 행성으로 선언한
네 행성 중 유일한 것입니다. 후보 c, d, e 는 후속 Basant 외 2025
MAROON-X 분석에서 확정 상태로 격상되었습니다. 중요하게도, 현재 Barnard
b 는 0.4 AU 의 역사적 Ribas 외 2018 super-Earth 후보와 *다른* 천체입니다
— Lubin 외 2021 이 그 검출을 항성 활동의 1년 alias 로 반박했고, González
Hernández 2024 는 156 회 ESPRESSO 관측에서 Ribas 주기의 신호를 명시적으로
회수하지 못했습니다. NearStars 와 현재 문헌의 b 라벨은 전적으로 P =
3.154-d 행성을 가리킵니다.

행성은 0.0229 AU 의 거의 원형 3.1542-일 궤도에서 Msini = 0.299 ± 0.026
M⊕ 를 가집니다 (Basant 2025. ESPRESSO 전용 González Hernández 2024 는
0.37 M⊕ 를 보고했으나 공동 MAROON-X 피팅으로 정제). 지구의 6.8× 일사를
받아 평형 온도 438 K (Basant 2025 Table 3, A = 0, 완전 열재분배) 를
가지며 — Kopparapu 2014 의 M4 V 호스트 보수적 거주 가능 영역 (HZ 안쪽
가장자리 ~0.1 AU, P ≈ 10 d) 의 한참 안쪽입니다. 행성은 transit 을 보이지
않으므로 (González Hernández 2024 + Stefanov 2024 TESS 비검출), 반지름과
조성은 Msini 와 더 폭넓은 hot rocky USP analog 에서 추론됩니다.

3.15-일 궤도는 조석 잠금을 본질적으로 확실하게 만듭니다 (이 질량과
호스트에서 Walterová 2020 시간 척도 < 10⁵ yr). substellar 점이 행성
프레임에 고정됩니다. Basant 2025 의 β-분포-prior 이심률은 e = 0.03
± 0.03 — 원과 일치하며, SPOCK 안정성 테스트는 장기 4-행성 공존을 위해
e < 0.02 를 선호합니다. 6.8 S⊕ 일사와 안쪽 형제 d 에 영향을 미치는
동일한 France 2020 대기 손실 환경에서, b 는 10 Gyr 에 걸쳐 어떤 1차
대기도 대부분 strip 된 것으로 예상됩니다. cfg 는 canonical 시각 기준선
으로 잔여 sodium-vapor exosphere 가 있는 노출 암석 시나리오를 채택합니다.

**NearStars 시나리오 선택. 노출된 basalt 표면, sub-Mercury exosphere,
Barnard 의 flare 활동에 대한 대기 차폐가 없는 뜨거운 조석잠금 sub-Earth
질량 암석 행성입니다. 형제 d 보다 차갑지만 여전히 어떤 물 안정성
임계값 위에 잘 위치. 시각적으로 더 어두운 빨강-갈색 노출 암석 세계.**
32 cfg 픽. 16 canonical-aligned, 16 tie-break. 문서화된 divergence 없음.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 3.15-d 궤도 → 조석 잠금 < 10⁵ yr (Walterová 2020) |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.03 | medium | Basant 2025 β-prior 피팅. 원 궤도와 일관 |
| `sidereal_period_days` | 3.1542 ± 0.0004 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0229 ± 0.0003 | high | Basant 2025 |
| `argument_of_periapsis_deg` | 3.8 | medium | Basant 2025 (낮은 ecc → 약한 제약) |
| `epoch_jd` | 2460243.38 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.299 ± 0.026 | high | Basant 2025 Msini |
| `radius_rearth` | 0.72 | medium | Tie-break. 비-transit. 0.3 M⊕ 지구 analog 암석의 질량-반지름 → 0.66–0.76 R⊕. interesting-first 가 0.72 선택 |
| `surface_gravity_g_earth` | 0.58 | medium | 유도 = 0.299 / 0.72² |
| `density_g_cc` | 5.0 | medium | Tie-break. d 보다 약간 낮음 (지구 analog 암석 대 Mercury-밀도 철 농축) |
| `insolation_s_earth` | 6.79 | high | L = 0.00356 L☉ 와 a = 0.0229 AU 로 유도 |
| `equilibrium_temp_k` (A=0, full redistribution) | 438 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 521 | high | dayside 공식으로 유도 |
| `equilibrium_temp_k` (A=0.1) | 426 | high | 유도 |
| `bond_albedo` | 0.10 | medium | Tie-break. 노출 암석 다크-basalt 범위 0.06–0.15 |
| `surface_temp_substellar_k` | 700 | medium | Tie-break. 6.8 S⊕ 의 무대기 dayside 스케일링 → ~720 K. 얇은 Na exosphere → ~700 K |
| `surface_temp_nightside_k` | 130 | medium | Tie-break. basalt 열관성을 가진 무대기 cold-trap → ~130 K |
| `atmosphere_present` | false (잔여 Na exosphere 만) | medium | Tie-break. 6.8 S⊕ + flare 환경이 strip 선호. Mercury analog Na exosphere |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break. Mercury-analog 칼럼 밀도 × 스케일 등가 |
| `atmosphere_composition` | Na 우위 sputter exosphere. 미량 K, Ca | low | Tie-break. Mercury analog |
| `atmosphere_tint_rgb_hex` | n/a | high | 유도 (가시 대기 없음) |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `ocean_present` | false | high | T > 500 K 가 표면 물 배제 |
| `surface_tint_rgb_hex_primary` | `#5e3526` (차가운 산화철 basalt. d 보다 약간 어두움) | medium | Tie-break. 노출 basalt × M 왜성 SED. d 보다 낮은 substellar T (700 K vs 800 K) → 적은 열복사 오버레이 |
| `surface_tint_rgb_hex_accent` | `#7a4530` (terminator 산능 basalt) | low | Tie-break. 제한된 열복사. terminator 의 bedrock 톤 |
| `surface_morphology` | impact 크레이터 basalt 지형. substellar partial-melt 없음. antistellar cold-trap | medium | Tie-break. d 보다 약간 낮은 평형 온도의 Mercury analog |
| `magnetic_field_present` | true (약함, 유도) | low | Tie-break. 유도-구동 장. 작은 코어 |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break. Mercury 류 매우 작은 쌍극자 |
| `radiation_belt_present` | false | high | 대기 없음 + 무시 가능 B-field |
| `surface_radiation_dose_msv_yr` | 7000 | medium | Atri 2020 스케일링. 무대기 + 6.8 S⊕ XUV × France 2020 flare 듀티 사이클 |
| `atmospheric_shielding_g_cm2` | 0 | high | 무대기 |
| `aurora_present` | false | high | 대기 없음 |
| `star_apparent_angular_diameter_deg` | 4.34 | high | 유도. 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard b 의 표면은 형제 d 의 더 차가운 대응물입니다. ~700 K 의
substellar 온도는 d 에서 보이는 광범위한 silicate partial-melt 에
도달하지 못하므로, cfg 는 d 의 partial-melt 액센트의 *부재* 로 b 를
d 와 구분합니다. 지배적인 톤은 산화철 basalt regolith (`#5e3526`) —
같은 M 왜성 조명에서 더 낮은 열복사 기여 때문에 d 보다 약간 더 어둡고
차가운 색입니다. terminator 산능 bedrock (`#7a4530`) 이 모데스트한
시각 변동을 제공합니다.

antistellar 반구는 깊은 cold-trap 입니다 (~130 K — d 의 100 K 보다
약간 더 따뜻한 이유는 약간 더 두꺼운 열적 regolith 의 더 큰 열-flux
retention 때문). Gyr 시간 척도에 걸쳐 휘발성을 축적합니다. d 와
마찬가지로 antistellar cold-trap 에서의 휘발성 sequestration 은
plausible 이지만 직접 관측 가능하지 않습니다.

표면 형태는 Mercury / hot-rocky 템플릿을 따릅니다. 4 Gyr 의 impact
cratering, 판 구조 없음, 그리고 과거 partial-melt 가동이 발생했다면
가능한 매끄러운 sub-substellar 영역. cfg 의 `surface_morphology` 필드는
substellar 영역이 terminator 와 antistellar 영역보다 텍스처가 약간 더
매끄러운 크게 cratered 된 basalt 기준선을 캡처합니다.

Stefanov 2024 의 TESS transit 비검출은 b 의 반지름에 대한 간접 제약
을 제공합니다 — 행성이 약 1.5 R⊕ 보다 컸다면 기존 광도 모니터링
윈도우에서 transit 이 검출됐을 것입니다. cfg 의 R = 0.72 R⊕ 는 이
임계값 한참 아래이며, 0.3 M⊕ 지구 analog 암석 물질에 대한 질량-반지름
스케일링은 0.66–0.76 R⊕ 를 주며, 0.72 값이 시각 구분을 위한 중간값으로
선택됩니다.

## Atmosphere synthesis

b 는 의미 있는 대기가 없습니다. France 2020 의 HZ (0.1 AU) 에서의
대기 손실 계산은 25% flare 듀티 사이클 하에서 ~87 지구대기 Gyr⁻¹
의 열적 escape 를 줍니다. b 의 0.0229 AU 에서 내부 시스템 강화 인자
는 대략 19× (반경 XUV 스케일링) 이므로, 10 Gyr 누적 손실은 0.3-M⊕
행성에 대한 어떤 plausible 1차 대기 질량보다 수 자리수 더 큽니다.

살아남는 대기 서명은 Mercury 의 analog 인 sputter-구동 sodium exosphere
입니다. basalt 표면을 두드리는 Barnard 의 별바람은 Na (그리고 K, Ca
미량) 원자를 지속 분리시키며 ~10¹⁰ atoms cm⁻² 의 칼럼 밀도를 가진
중력적으로 unbound 인 exosphere 를 생성합니다. 표면 압력 등가는
~10⁻⁹ Pa — 어떤 Rayleigh 산란 서명도 한참 밑돌아 가시 외관은 표면
톤에 의해 전적으로 지배됩니다 (cfg `atmosphere_tint_rgb_hex = n/a`).

Barnard 의 모데스트한 flare 동안의 에피소드 강화 (~25% 듀티 사이클,
개별 에너지 ~10²⁹·² – 10²⁹·⁵ erg, France 2020) 가 일시적인 sputtering
증가를 구동합니다. 이는 analog Proxima superflare 사건보다 훨씬 작지만,
10 Gyr 에 걸친 누적 대기 손실의 대부분에 기여합니다. 게임 내 효과는
sub-resolution 렌더링에 제한 — 가시 exospheric plume 없음.

## Rotation & spin synthesis

b 는 1:1 (동기) 로 조석 잠겨 있으며 substellar 점이 행성 프레임 0°
경도에 고정되어 있습니다. 0.16 M☉ M 왜성 주위 0.0229 AU 의 0.3-M⊕
암석 행성에 대한 Walterová 2020 조석 잠금 시간 척도는 10⁵ 년을 한참
밑돌아, 10 Gyr 시스템 나이보다 훨씬 짧습니다. 경사 또한 0° 로 감쇠.

Basant 2025 의 e = 0.03 은 1σ 에서 원과 일관됩니다. SPOCK 안정성은
e < 0.02 를 선호합니다. 이 낮은 이심률에서 1:1 동기 구성이 지배하며
(3:2 trap 없음), libration 진폭은 작습니다 (< 1°).

다른 세 행성과 결합해서, b 는 컴팩트 근-공명 체인에 참여합니다 (주기
비 3.15:4.12 ≈ 4:5. 2.34:3.15 ≈ 3:4). 그러나 시스템은 Basant 2025 SPOCK
분석 당 엄격한 mean-motion 공명에는 *없습니다* — 행성들은 공명 잠금
없이 장기 안정성을 위해 충분히 잘 분리되어 있습니다.

## Visual styling

Barnard b 는 d 의 더 차가운 어두운-빨강 형제입니다. cfg 의 `#5e3526`
1차 톤은 d 의 `#6a3a26` 보다 더 어둡고 약간 더 갈색 톤입니다. 이는
더 낮은 substellar 온도 (700 K vs 800 K) 와 partial-melt 열복사의 부재
모두를 반영합니다. 궤도에서 b 는 d 와 동일한 sharp-terminator hot-rocky
위상 곡선을 보이며, 대기 헤이즈 없고 최소 limb darkening 입니다.

Barnard 는 b 의 하늘에서 4.3° 를 차지 — 지구에서 본 태양의 약 8×
. 어둑한 빨강 조명은 영구히 어둑한 따뜻한-오렌지 표면 조명을 만듭니다.
누적 표면 dose 는 정상 플레이에서 치명적으로 유지됩니다 (cfg
`surface_radiation_dose_msv_yr = 7000`, d 의 것보다 약간 낮음 — 차가운
substellar T 와 더 큰 궤도 반경에서의 감소된 XUV 플럭스 때문).

aurora cfg 필드는 모두 `false` / `n/a`. Barnard 의 flare 사건은
cfg 의 flare-duty-cycle 속도 (~25%) 에서 일시적인 ~5000-s 주변광
brightening 으로 나타나며, exotic 스펙트럼 특징은 없습니다. 게임 내
렌더링은 더 차가운 톤 basalt 표면을 강조해 b 를 더 뜨겁고 partial-melt
액센트가 있는 d 와 시각적으로 구분해야 합니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). MAROON-X 확인. P = 3.1542 d, Msini = 0.299 ±
  0.026 M⊕, a = 0.0229 AU, T_eq = 438 K (A=0, full redistribution).
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO 발견. 현대 Barnard 시스템의 첫 확정 행성. 약간 다른
  항성 매개변수 세트에서 abstract 에 T_eq = 400 K 명시.
- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). TESS 비검출이 transit 을 배제. R 을 간접적으로
  < 1.5 R⊕ 로 제약.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra. 25% flare 듀티 사이클. b 의 대기-strip
  시나리오를 뒷받침하는 대기 손실률.
- **Lubin J. et al. 2021** — *Stellar Activity Manifesting at a
  One-year Alias Explains Barnard b as a False Positive*
  (`2021AJ....162...61L`. arXiv preprint 없음). Ribas 2018 반박 —
  현재 Barnard b 가 2018 후보와 다른 행성임을 확립.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). 조석 잠금
  시간 척도 스케일링.

### Read (context / methodology, not decision-driving)

- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star* (`2018Natur.563..365R`,
  arXiv:1811.05955). 역사적 클레임, 반박됨. b 라벨의 역사적 문헌
  맥락으로 보존.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). 행성의 일사 환경 기반의 호스트
  회전 + 활동.

### Read (instrument-only, not visual-informative)

- **Choi J. et al. 2013** — *Precise Doppler Monitoring of Barnard's
  Star* (arXiv:1208.2273). 발견 이전 RV 상한.

### Not read — no arXiv preprint or low-priority (~140 papers)

대부분 Ribas 2018 후보 (현재 반박됨), 일반 M 왜성 행성 형성 이론,
Barnard 를 RV 표준으로 언급하는 기기 개발 논문에 대한 역사적 2024
년 이전 논문. `docs/phase3/_bib/barnards-star-b.yaml` 에 `status:
skipped` 로 보존.

## Open items for follow-up

- **직접 반지름 측정**. transit 없음. 미래 astrometric 검출 (Gaia
  DR4 또는 직접 영상화) 이 실제 질량과 반지름을 제약할 수 있습니다.
  cfg 의 `radius_rearth = 0.72` 는 tie-break.
- **질량-반지름에 의한 조성**. 반지름 없이는 암석 대 얼음 풍부가
  축퇴됩니다. cfg 는 지구 analog 암석을 기본값으로 사용하며, Mercury
  류 철 농축 대안도 윈도우 내.
- **Lubin 2021 반박 세부**. 반박 논문은 arXiv preprint 가 없습니다.
  미래 사용자가 붙여넣은 abstract 나 본문이 있다면 인용된 요약에
  의존하지 않고 반박 방법론을 deep-read 할 수 있습니다.
- **이심률 vs. 안정성**. Basant 2025 의 e = 0.03 ± 0.03 은 b 가
  정확히 원이거나 약하게 이심률인지를 열어둡니다. 30 cm/s 정밀도의
  장기 모니터링이 이를 개선할 수 있습니다.
- **대기 유지 재-모델링**. France 2020 은 0.1 AU 의 자기장 없는 1
  M⊕ 행성을 가정. M 왜성 바람 ram-pressure 스케일링과 0.0229 AU
  의 0.299 M⊕ 에 대한 b 전용 모델은 cfg 의 `atmosphere_present`
  결정을 개선할 것입니다. 현재 tie-break 은 노출 암석으로 기울어짐.

## Related

- [barnards-star](barnards-star.md) — 호스트 별. 조용한 노쇠 M4 V
- [barnards-star-c](barnards-star-c.md) — 다음 외곽. 더 낮은 일사에서 비교 가능한 표면 조건
- [barnards-star-d](barnards-star-d.md) — 안쪽 형제. 더 뜨거움 (substellar partial-melt 가시)
- [barnards-star-e](barnards-star-e.md) — 가장 바깥. HZ 안쪽 가장자리에 가장 가까움
- [proxima-cen-b](proxima-cen-b.md) — 다른 "b" 라벨, 다른 호스트 활동 환경. 대기 유지 로직에 유용한 비교
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 하류 cfg writer
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX 는 Ribas-2018 류 super-Earth b 리스트. NS 는 2024-이후 sub-Earth b 반영
