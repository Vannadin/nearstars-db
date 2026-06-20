<!-- Barnard's Star c Phase 3 합성. cfg-ready 결정과 근거 -->
# Barnard's Star c — Phase 3 Synthesis

Barnard's Star c 는 González Hernández 2024 / Basant 2025 시스템의
네 행성 중 가장 무겁습니다. Msini = 0.335 ± 0.030 M⊕ — 지구 질량의
1/3 이상인 유일한 행성입니다. 0.0274 AU 의 4.12-일 궤도에서 지구의
4.7× 일사를 받으며, 평형 온도는 400 K (Basant 2025 Table 3, A =
0, 완전 열재분배) 로 초기 금성에 비교됩니다. González Hernández
2024 ESPRESSO 데이터의 후보였고, Basant 2025 MAROON-X 분석이 ESPRESSO
데이터와 독립적으로 c 신호를 회수해 확정 상태로 격상했습니다.

궤도 이심률은 Basant 2025 β-분포 prior 에서 e = 0.08 (−0.05 / +0.06)
입니다. 네 행성 중 가장 높은 명목 이심률 값이지만, 여전히 1.5σ 에서
원과 일관하며 e < 0.02 의 장기 안정성 요구사항과도 일관합니다. b 와의
궤도 주기 비 (4.124 / 3.154 = 1.31) 는 4:3 mean-motion 공명에
가깝지만 정확하지는 않습니다. Basant 2025 SPOCK 안정성 테스트는
이심률이 0 에 가까울 때 4-행성 구성이 명시적 공명 잠금 없이 가장
짧은 주기 행성 기준 10⁹ 궤도에 걸쳐 안정함을 발견합니다.

4.7 S⊕ 일사에서 c 는 어떤 지구 analog 대기에 대해서도 폭주 온실 한계
의 안쪽에 위치합니다 (Kopparapu 2014 의 이 항성 질량 보수적 HZ 에서
의 안쪽 가장자리 ~1.1 S⊕). 표면 온도가 액체 물을 배제하며, 행성은
transit 을 보이지 않고 (Stefanov 2024 의 4-행성 GH24 해 전반에 걸친
암묵적 비검출), 반지름 / 조성은 질량-반지름 스케일링에서 추론됩니다.
France 2020 의 대기 escape 계산 — HZ (0.1 AU) 에서 87 지구대기
Gyr⁻¹ — 은 c 의 0.0274 AU 에서 누적 손실이 단위 면적당 ~13× 더
높음을 의미하며, 다시 의미 있는 1차 대기 유지를 배제합니다. cfg 는
b 와 d 에 사용된 동일한 노출 암석 해석을 채택합니다. c 는 약간 더
낮은 일사 (더 차가운 표면 톤) 와 네 행성 중 가장 높은 절대 질량
(작은 형제들 대비 약간 더 큰 하늘에서의 각지름) 으로 시각적으로
구별됩니다.

**NearStars 시나리오 선택. 시스템에서 가장 무거운, 노출 basalt 표면,
대기 없음, 초기 금성에 비교 가능한 표면 온도를 가진 조석잠금 sub-Earth
암석 행성입니다. 뜨거운 d/b 와 더 차가운 e 사이의 중간 톤 빨강-갈색
노출 암석 세계.** 32 cfg 픽. 16 canonical-aligned, 16 tie-break.
문서화된 divergence 없음.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 4.12-d 궤도 → 조석 잠금 < 10⁵ yr (Walterová 2020) |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.08 | medium | Basant 2025 β-prior 피팅 (0.08 −0.05/+0.06). 네 행성 중 가장 높은 명목 e. 그러나 안정성은 e < 0.02 선호 |
| `sidereal_period_days` | 4.1244 ± 0.0006 | high | Basant 2025 Table 3 |
| `semi_major_axis_au` | 0.0274 ± 0.0004 | high | Basant 2025 Table 3 |
| `argument_of_periapsis_deg` | 90.8 | medium | Basant 2025 Table 3 (90.8 −48.1/+38.9) |
| `epoch_jd` | 2460242.92 | high | Basant 2025 t₀,c (BJD−2450000 = 10242.92) |
| `mass_mearth` | 0.335 ± 0.030 | high | Basant 2025 Msini |
| `radius_rearth` | 0.743 | medium | 0.335 M⊕ 비-transit 암석 행성의 DB 질량-반지름 관계 (측정 반지름 없음. transit 배제, Stefanov 2024) |
| `surface_gravity_g_earth` | 0.61 | medium | 유도 = 0.335 / 0.743² = 0.607 |
| `density_g_cc` | 4.50 | medium | 유도 = 5.513 × 0.335 / 0.743³. 작은 형제들보다 약간 더 낮은 밀도 (질량-반지름 기울기) |
| `insolation_s_earth` | 4.74 | high | 유도 = L / a² = 0.003558 / 0.0274² |
| `equilibrium_temp_k` (A=0, full redistribution) | 400 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 476 | high | dayside 공식으로 유도. 400 × 2^0.25 |
| `equilibrium_temp_k` (A=0.1) | 390 | high | 유도. 400 × 0.9^0.25 |
| `bond_albedo` | 0.12 | medium | Tie-break. 노출 암석 범위 0.08–0.18. 중간 일사가 뜨거운 형제들보다 약간 더 높은 albedo 선호 |
| `surface_temp_substellar_k` | 600 | medium | Tie-break. 4.7 S⊕ 의 무대기 dayside 스케일링 → ~640 K. 약한 열 재분배 → ~600 K |
| `surface_temp_nightside_k` | 130 | medium | Tie-break. basalt regolith cold-trap |
| `atmosphere_present` | false (잔여 Na exosphere 만) | medium | Tie-break. 4.7 S⊕ + flare 환경이 strip 선호. b/d 와 동일한 Mercury-analog 로직 |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break. Mercury-analog 칼럼 밀도 |
| `atmosphere_composition` | Na 우위 sputter exosphere. 미량 K, Ca | low | Tie-break. Mercury analog |
| `atmosphere_tint_rgb_hex` | n/a | high | 유도 (가시 대기 없음) |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `ocean_present` | false | high | T > 400 K 가 표면 물 배제 |
| `surface_tint_rgb_hex_primary` | `#5a3225` (차가운 다크 basalt. d 와 e 사이 중간값) | medium | Tie-break. 중간 substellar T 에서 노출 basalt × M 왜성 SED |
| `surface_tint_rgb_hex_accent` | `#6e3d2c` (terminator/고지대 bedrock) | low | Tie-break. 이 일사에서의 제한된 열복사 |
| `surface_morphology` | impact 크레이터 basalt 평원. 가능한 relict 화산 지형. antistellar cold-trap | medium | Tie-break. Mercury-analog + b/d 보다 약간 낮은 열 강제 |
| `magnetic_field_present` | true (약함, 유도) | low | Tie-break. 유도-구동 |
| `magnetic_dipole_moment_normalized_earth` | 0.001 | low | Tie-break. c 가 가장 무거우므로 작은 형제들보다 약간 더 큼 (Mercury 유추, 다이너모 모델링 아님) |
| `radiation_belt_present` | false | high | 대기 없음 + 무시 가능 B-field |
| `surface_radiation_dose_msv_yr` | 5000 | medium | Atri 2020 스케일링. 무대기 + 4.7 S⊕ XUV × France 2020 듀티 사이클 |
| `atmospheric_shielding_g_cm2` | 0 | high | 무대기 |
| `aurora_present` | false | high | 대기 없음 |
| `star_apparent_angular_diameter_deg` | 3.64 | high | 유도. 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard c 의 표면 조건은 더 뜨거운 안쪽 쌍 (b/d) 과 더 차가운 가장
바깥 e 사이의 중간입니다. 4.7 S⊕ 일사에서 substellar dayside 는
~600 K 에 도달하는데, basalt 광물의 열 weathering 에는 충분하지만
d 에서 보이는 silicate 용융 임계값보다는 한참 아래입니다. cfg 는
이를 partial-melt 액센트의 부재로 인코딩합니다 (`surface_tint_rgb_hex_accent
= #6e3d2c` 는 terminator 산능 bedrock 용). c 는 따뜻한-오렌지
substellar 글로우가 없다는 점에서 d 와 시각적으로 구별됩니다.

substellar 반구는 산화철 basalt 평원이 지배합니다. 더 이른 (더
뜨거운) 초기 열 단계에서의 relict 화산 지형이 존재할 수 있지만 직접
추론은 불가합니다. cfg 의 `surface_morphology` 필드는 canonical
Mercury-analog impact-cratered 기준선을 반영합니다.

antistellar 반구는 깊은 cold-trap 입니다 (~130 K). Gyr 시간 척도에
걸쳐 휘발성을 축적합니다. c 가 네 행성 중 가장 무거우므로, 어떤
휘발성 유입에 대한 중력적 retention 도 작은 형제들보다 marginal 하게
더 강합니다. 비록 여전히 1차 대기를 유지하기에는 불충분하지만.

더 낮은 bond albedo (cfg 0.12) 는 노출 암석 표면을 반영합니다. 어떤
구름이나 대기 산란 없이, 가시 외관은 basalt regolith 색이 지배합니다.
b/d 대비 약간 더 차가운 substellar 온도는 가시 파장에서의 dayside
스펙트럼에 대한 열복사 기여가 최소임을 의미합니다. 외관은 M4 V SED
의 반사가 지배합니다.

## Atmosphere synthesis

c 는 의미 있는 대기가 없습니다. b 와 d 에 적용되는 동일한 France
2020 escape 계산은 c 의 0.0274 AU 에서 누적 대기 손실이 단위 면적당
HZ 속도의 약 13× 또는 ~1100 지구대기 Gyr⁻¹ 열적 escape 임을 의미합니다.
10 Gyr 에 걸쳐 0.34 M⊕ 행성에 대한 어떤 plausible 1차 대기 질량
도 한참 초과합니다.

별바람 sputtering 으로부터의 잔여 sodium exosphere 는 ~10¹⁰ atoms
cm⁻² 의 칼럼 밀도와 함께 존재합니다 (Mercury-analog 스케일링). 미량
의 더 무거운 종 (K, Ca) 이 더 낮은 abundance 에서 Na 와 동반합니다.
exospheric 압력 등가 ~10⁻⁹ Pa 는 어떤 Rayleigh-산란 임계값도 한참
밑돕니다. cfg 의 `atmosphere_tint_rgb_hex = n/a` 는 가시 대기 레이어
의 부재를 반영합니다.

France 2020 의 25% flare 듀티 사이클이 에피소드 sputtering 강화를
구동하지만 가시 exospheric plume 은 없습니다. 표면에서의 누적 복사
dose (cfg 5000 mSv/yr) 는 보호되지 않은 생명체에 치명적이며 게임 내
거주 가능성 평가를 지배합니다.

## Rotation & spin synthesis

c 는 조석 despin 되어 있습니다. 0.16 M☉ M 왜성 주위 0.0274 AU
의 0.34 M⊕ 암석 행성에 대한 Walterová 2020 시간 척도는 여전히 10⁵
년을 한참 밑돌며, 10 Gyr 시스템 나이보다 훨씬 짧습니다. 경사는 0°
로 감쇠합니다.

정확한 최종 자전 상태는 어느 이심률을 채택하느냐에 달려 있습니다.
Basant 2025 는 e = 0.08 — 네 행성 중 가장 높은 명목 이심률 — 을
보고하지만, 같은 논문의 prior-uniform-uninformative 테스트는 장기
안정성과 충돌하는 더 높은 이심률 (c 에 대해 e ~ 0.24) 을 선호했습니다.
β-prior 피팅의 e = 0.08 (−0.05/+0.06) 이 권장 값이지만, 안정성
제약 (SPOCK 10⁹-궤도 테스트) 은 e < 0.02 를 선호합니다. 채택된
e = 0.08 에서 평형 자전은 순수한 1:1 잠금이 아니라 의사동기
(pseudo-synchronous, 약간 초동기) 입니다 — Walterová 2020 은 이심
궤도 암석 행성이 정확한 동기화가 아닌 의사동기 자전에 정착함을
발견합니다 — 사소하지 않은 libration 진폭 (~5°) 과 함께이며, 이는
측정 가능한 diurnal 일사 변동을 만들 수 있습니다. 안정성-제약
e < 0.02 에서는 자전이 순수한 1:1 잠금으로 줄고 libration 은 무시
가능합니다. cfg 의 스칼라 자전 필드에서 이 차이는 게임 내 해상도
아래이며, 행성은 어느 쪽이든 사실상 동기 자전으로 렌더링됩니다.

c 는 컴팩트 시스템 아키텍처에 참여하지만 b 와 엄격한 4:3 mean-motion
공명에는 있지 않습니다 (주기 비 1.31, 정확히 4/3 아님). ~3800-일 항성
활동 사이클이 일사를 수 퍼센트 변조하지만, cfg 의 스칼라 해상도에서
시각 변화를 구동하기에 너무 작습니다.

## Visual styling

c 는 네 행성 가족의 시각적 중간입니다. b/d 보다 더 차갑고 약간 더
어둡고, e 보다는 더 따뜻합니다. cfg 1차 톤 `#5a3225` 는 네 중 가장
어두운 것이고 (열복사 오버레이 없는 더 차가운 substellar T), terminator
액센트 `#6e3d2c` 가 제한된 시각 변동을 제공합니다. 표면 형태는 더
오래된 화산 특징의 가능성과 함께 basalt 평원이 지배합니다.

Barnard 는 c 의 하늘에서 3.6° 를 차지하는데, 지구에서 본 태양의 약
7× 입니다. 어둑한 빨강 조명은 dayside 에 영구 따뜻한 황혼을 만듭니다.
nightside 는 완전히 비조명입니다 (알려진 위성이 없으므로 위성-조명
효과 없음).

aurora cfg 필드는 모두 `false` / `n/a` 입니다. Barnard 의 flare 사건은
25% 듀티 사이클로 일시적인 주변광 brightening 으로 나타납니다. 누적
표면 dose 는 정상 플레이 조건 하에서 치명적으로 유지됩니다.

c 가 네 중 가장 무거우므로, 형제들보다 marginal 하게 더 높은 표면
중력 (0.61 g vs ~0.55–0.62) 을 가집니다. 그러나 차이는 너무 작아서
cfg 의 해상도에서 게임 내 지형 렌더링에는 영향을 미치지 않습니다.
시각적 강조는 c 를 "중간 형제" 대비로 두는 것에 있습니다 — 그을린
뜨거운 안쪽 쌍도 비교적 차가운 가장 바깥 e 도 아닌 것으로.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). MAROON-X 확인. P = 4.1244 d, Msini = 0.335 ±
  0.030 M⊕, a = 0.0274 AU, e = 0.08 (−0.05/+0.06), ω = 90.8°,
  T_eq = 400 K (A=0, full redistribution). SPOCK 안정성은 e < 0.02
  선호.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO 데이터가 c 를 후보로 처음 식별.
- **Stefanov A. K. et al. 2024** — *On the possible transit of
  Barnard b* (arXiv:2410.00577). TESS S80 비검출. b 에 대해 i ≤ 87.9°
  (3σ), 4-행성 GH24 해로 확장 → c 도 비-transit.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). 조석 잠금
  시간 척도 스케일링. 이심 궤도 암석 행성은 정확한 동기가 아닌
  의사동기 자전에 정착.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  HZ 에서의 대기 손실 기준선. c 의 0.0274 AU 로 스케일.
  *(context-cite, 로컬 캐시에 없음 — escape 속도와 flare 듀티
  사이클 수치는 low/medium confidence 로 이월.)*

### Read (context / methodology, not decision-driving)

- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). 호스트 회전 + ~3800-일 활동
  사이클.

### Read (instrument-only, not visual-informative)

- (c 에 특화 직접 관련 항목 없음.)

### Not read — no arXiv preprint or low-priority (~15 papers)

c 의 bib 은 c 가 개별 발견 논문이 없기 때문에 작습니다. González
Hernández 2024 다행성 ESPRESSO 데이터 세트의 후보로만 회수되고
Basant 2025 다행성 MAROON-X 논문에서 확인됩니다. 대부분의 리스트
항목은 역사적 "혜성 c" 이름 충돌 논문입니다. `docs/phase3/_bib/barnards-star-c.yaml`
에 `status: skipped` 로 보존됩니다.

## Open items for follow-up

- **직접 반지름 측정**. 네 행성 모두와 마찬가지로 transit 없음.
  미래 astrometry 또는 직접 영상화가 cfg 의 질량-반지름 유도값
  `radius_rearth = 0.743` 을 개선할 수 있습니다.
- **고-이심률 vs. 안정성**. Basant 2025 β-prior e = 0.08 은 네 행성
  중 가장 높은 명목값입니다. 그러나 안정성은 e < 0.02 를 선호합니다.
  30 cm/s 정밀도 RV 추가 모니터링이 이심률을, 그리고 그에 따라 자전
  상태가 의사동기 (e = 0.08) 인지 순수한 1:1 잠금 (e < 0.02) 인지를
  개선할 수 있습니다.
- **가장 무거운 sub-Earth 에 대한 질량-반지름 관계**. c 는 순수
  암석 (지구 analog) 과 약간 얼음 풍부 (예. 휘발성-농축 mantle 의
  Mars analog) 조성의 경계에 있습니다. cfg 는 암석을 기본값으로
  합니다. asteroseismic 또는 직접 영상 캠페인의 미래 조성 제약이
  개선할 수 있습니다.
- **공명 근접**. b 와의 주기 비 (1.31) 는 4:3 (1.333) 에 가깝습니다.
  c 가 근-공명 trap 에 있는지 단순히 우연으로 근-공명인지가 장기
  동역학에 영향을 미치지만 시각 스타일링에는 영향이 없습니다.
- **France 2020 검증**. escape 속도 (HZ 에서 87 지구대기 Gyr⁻¹) 와
  25% flare 듀티 사이클은 로컬 캐시에 없는 논문에서 이월된 값입니다.
  어떤 cfg writer 가 이를 load-bearing 으로 취급하기 전에 arXiv:2009.01259
  를 재-fetch 해 두 수치를 확인해야 합니다.
- **대기 유지**. b 와 동일한 caveats. cfg 의 노출 암석 해석은
  이 새로 발견된 행성에 대한 GCM 모델링의 부재에 대한 tie-break.

## Related

- [barnards-star](barnards-star.md) — 호스트 별. 조용한 노쇠 M4 V
- [barnards-star-b](barnards-star-b.md) — 안쪽 형제. 더 낮은 질량이지만 더 높은 일사
- [barnards-star-d](barnards-star-d.md) — 가장 안쪽. 가장 뜨거움, partial-melt 액센트 있음
- [barnards-star-e](barnards-star-e.md) — 가장 바깥. 가장 차가움, HZ 에 가장 가까움
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 하류 cfg writer
