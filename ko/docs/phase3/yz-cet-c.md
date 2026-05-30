<!-- YZ Cet c Phase 3 합성. cfg-ready 결정과 근거 -->
# YZ Cet c — Phase 3 Synthesis

YZ Cet c 는 M4.5 V flare star YZ Cet 을 도는 세 행성 중 가운데로,
3.05989 일 주기, a = 0.0216 AU 궤도에 있습니다 (Stock et al. 2020).
형제들과 마찬가지로 비통과 시선속도 행성입니다. 최소질량 M sin i =
1.14 ± 0.11 M⊕ (Stock 2020) — 셋 중 가장 무거움 — 은 측정되지만
반지름은 **측정되지 않으므로**, DB 의 1.05 R⊕ 수치는 관측이 아니라
준경험적 질량-반지름 추정입니다. 호스트의 L = 0.0022 L☉ 에서 평형온도는
알베도 0 에서 T_eq ≈ 410 K (여기서 계산. T_eq = 278.3·L^0.25/√a) 이라,
c 는 **따뜻한 암석 세계** 입니다 — 안쪽 행성 b (471 K) 보다 차갑지만
여전히 지구보다 한참 위로, 지구 일사량의 ~4.7 배입니다.

**NearStars 시나리오 선택. 따뜻하고 조석 고정된 암석 행성으로, 얇거나
없는 이차 대기를 가집니다.** YZ Cet c 는 SPI 구동체가 아닙니다 —
확인된 항성-행성 자기 상호작용은 행성 b 의 궤도로 folding 되고, 전파
버스트는 c 와의 위상 일치가 더 나쁩니다 (Pineda & Villadsen 2023.
Trigilio 2023). 따라서 c 는 "평범한" 따뜻한 암석 행성으로 렌더링합니다.
조금 더 무겁고 조금 더 차가운 가운데 세계입니다. 통과나 식, 투과
스펙트럼이 없으므로 표면과 대기는 low confidence 에 둡니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence` 표기는
high = 직접 측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘
이론, low = 허용 범위 안에서의 미적 선택을 뜻합니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 0.0216 AU 의 3.06 d 궤도. 중간-M 호스트에서 조석 고정 시간이 시스템 나이보다 훨씬 짧음 |
| `obliquity_deg` | 0 | high | 이 궤도에서 조석 damping |
| `eccentricity` | 0.0 | medium | Stock et al. 2020 (Phase 2 recommended). 원궤도 채택 |
| `argument_of_periastron_deg` | n/a | high | 원궤도 (e = 0) — periastron 정의되지 않음 |
| `sidereal_period_days` | 3.05989 | high | Stock et al. 2020 (Phase 2 recommended) |
| `semi_major_axis_au` | 0.02156 | high | Stock et al. 2020 (Phase 2 recommended) |
| `mass_mearth` | ≥ 1.14 ± 0.11 (M sin i) | high | Stock et al. 2020 RV 최소질량 (Phase 2 recommended). 셋 중 가장 무거움. 실제 질량은 1/sin i 만큼 더 큼 |
| `radius_rearth` | ~1.05 (ESTIMATE) | low | 측정 아님 — 통과 없음. 준경험적 M-R 추정 (Stock 2020). Pineda & Villadsen 2023 도 같은 관계에서 R_c = 1.05 R⊕ 인용 |
| `surface_gravity_g_earth` | ~1.03 | low | 유도값 = 1.14 / 1.05² (최소질량 + 추정 반지름). 하한 (실제 질량 더 큼) |
| `density_g_cc` | ~5 (암석 가정) | low | 측정 반지름 없음 → 측정 밀도 없음. 지구형 암석 조성 가정 |
| `insolation_s_earth` | 4.7 | high | 유도값 = L / a² = 0.0022 / 0.02156² |
| `equilibrium_temp_k` (A=0) | 410 | high | 유도값 = 278.3 · L^0.25 / √a (L = 0.0022 L☉, a = 0.02156 AU) |
| `equilibrium_temp_k` (A=0.3) | 376 | high | 유도값, 지구형 Bond 알베도 |
| `bond_albedo` | 0.1 | low | Tie-break. 따뜻한 암석 표면에 대해 낮게 가정. 측정 없음 |
| `atmosphere_present` | thin or absent | low | 투과 스펙트럼 없음. 활동적 flaring M 왜성 주위 따뜻한 암석 RV 행성 — 대기 유지가 marginal. cfg 는 흥미로운 얇은 대기를 렌더링 |
| `atmosphere_surface_pressure_pa` | ~10000 (0.1 bar, tie-break) | low | 측정 없음. airless 보다 흥미로운 얇은 이차 대기 선택. airless 변형은 Open items 에 보존 |
| `atmosphere_composition` | CO₂ / N₂ secondary (가정) | low | 스펙트럼 없음. 대기가 남아 있다면 탈가스 암석 행성 조성 가정 |
| `atmosphere_tint_rgb_hex` | `#c2a07c` (얇은 따뜻한 haze) | low | Tie-break. 얇은 대기가 있다면 3100 K 조명 아래 희미한 따뜻한 사지 haze |
| `dayside_surface_temp_k` | ~450 | medium | substellar 맨 암석 정점이 410 K 전역 T_eq 위 (A=0, 낮은 재분배) |
| `nightside_surface_temp_k` | depends on atmosphere | low | airless → 매우 차가운 nightside. 얇은 대기 → 부분 재분배 |
| `surface_tint_rgb_hex_primary` | `#5e4a3c` (따뜻한 basalt 암석) | low | Tie-break. 붉은 M-왜성 빛 아래 따뜻한 색조의 철 함유 basalt. 더 따뜻한 안쪽 행성 b 보다 약간 밝음 |
| `surface_tint_rgb_hex_accent` | `#74402a` (산화철 patch) | low | Tie-break. 노출된 따뜻한 암석 표면의 광분해 / 산화철 |
| `surface_morphology` | cratered rocky plains, tidally-locked | low | 데이터 없음. 조석 고정 아래 일반적인 따뜻한 암석 형태 |
| `spi_driver` | false | high | Pineda & Villadsen 2023. Trigilio 2023 — SPI 버스트가 c 가 아니라 b 의 궤도로 folding (c 는 위상 일치가 더 나쁨). c 는 flux-tube 구동체가 아님 |
| `planet_magnetic_field_g` | unconstrained | low | c 에 귀속되는 SPI 신호 없음 → 자기장 추론 없음. 제약하지 않고 둠 |
| `star_apparent_angular_diameter_deg` | 3.88 | high | 유도값 = 2 · R★ / a · (180/π), R★ = 0.1571 R☉ |
| `stellar_illumination_color_temp_k` | 3100 | high | Cifuentes et al. 2020 호스트 Teff |

## Surface synthesis

YZ Cet c 는 통과나 식, 투과 측정이 없어, 표면이 전적으로 최소질량과
궤도, 호스트 조명에서 추론됩니다. 반지름 (1.05 R⊕) 은 관측이 아니라
준경험적 질량-반지름 추정 — Pineda & Villadsen 2023 이 Stock 2020
관계에서 인용한 것과 같은 값 (R_c = 1.05 R⊕) 입니다. 최소질량 M sin i
= 1.14 M⊕ (Stock 2020) 은 진짜 하한이고 c 를 세 행성 중 가장 무겁게
만듭니다. 실제 질량은 1/sin i 만큼 더 큽니다. cfg 목적상 c 는
지구질량급 암석 행성으로 다룹니다.

c 는 **녹은 게 아니라 따뜻합니다**. 알베도 0 평형온도는 T_eq ≈ 410 K
(여기서 L = 0.0022 L☉, a = 0.02156 AU 로 계산) 로, 안쪽 행성 b 보다
약 60 K 차갑고 지구 일사량의 ~4.7 배입니다. 지구보다 뜨겁지만 금성의
평형온도보다는 차가워 — 진짜 따뜻하지만 용암은 아닌 세계입니다.
substellar 맨 암석 정점은 ~450 K 입니다.

**색 선택.** 호스트의 3100 K 적등색 조명 아래 c 는 따뜻한 철 함유
basalt 표면 (`#5e4a3c` primary) 에 산화철 patch accent (`#74402a`)
으로 렌더링합니다 — 안쪽의 더 따뜻한 행성 b 보다 약간 밝게 해, 조밀계
가 궤도 view 에서 안→밖 온도 구배를 띠게 합니다. 색조는 low-confidence
입니다. 식이나 반사율 데이터가 없어 광물학이 제약되지 않고, 따뜻한-암석
해석은 밋밋한 회색 구체보다 나은 interesting-first tie-break 입니다.

**형태.** 조석 고정 (3.06 일 궤도가 시스템 나이 안에서 spin 을 동기
자전으로 damping) 이라 substellar 점이 고정됩니다. 기본 텍스처는
따뜻한 dayside 와 차가운 nightside 를 가진 cratered 암석 평원입니다.
확인된 재포장 메커니즘이 없으므로 강제된 화산 지형은 없습니다.

## Atmosphere synthesis

YZ Cet c 의 투과 스펙트럼이 없어, 대기는 허용 범위 안의 합성 선택이며
다른 행성들과 같은 두 고려로 bracket 됩니다. T_eq ≈ 410 K 와 ~4.7 배
지구 일사량에서 얇은 이차 대기는 열적으로 그럴듯하나, kG 자기장과 강한
풍을 가진 적당히 활동적인 flaring M-왜성 호스트와 항성 자기권 깊숙이
공전하는 행성들 (sub-Alfvénic. Trigilio 2023) 때문에 유지가
marginal 합니다.

행성 b 와 달리 c 는 **자신의 SPI 신호가 없습니다** — 전파 버스트가
c 의 궤도로 깔끔히 folding 되지 않습니다 (Pineda & Villadsen 2023.
Trigilio 2023 은 c 와 d 에 더 나쁜 일치를 발견) — 따라서 추가 대기
차폐를 주장할 추론된 자기장이 없습니다. 그러므로 c 는 더 보수적인
경우입니다. 얇은 대기는 가능하나 b 보다 덜 방어됩니다.

NearStars 에는 interesting-first tie-break 로 **얇은 이차 대기
(~0.1 bar, CO₂/N₂)** 를 채택하고, airless 변형은 Open items 에
보존합니다. 이는 c 에 희미한 따뜻한 사지 haze (`#c2a07c`) 와 약간의
주야 열 재분배를 주는 low-confidence 미적 선택입니다.

**하늘 외형.** 얇은 대기가 있으면 3100 K 별 아래 낮 하늘은 천정 부근에
약한 Rayleigh 파랑을 띤 흐린 적등색입니다. airless 면 검고 별 원반은
sharp-edged 입니다. 호스트 별이 ~3.9° 각지름 (지구에서 본 태양의 약
8 배) 으로 하늘을 지배하는 깊은 적등색이고, 안쪽 형제 b 와 바깥 형제
d 는 밝게 움직이는 점으로 보입니다.

## Rotation & spin synthesis

YZ Cet c 는 조석 고정입니다. 0.137 M☉ 별 주위 a = 0.0216 AU 에서 조석
고정 시간척도는 시스템 나이보다 훨씬 짧아, 행성은 3.05989 일 궤도와
동기 자전합니다. 이심률은 원궤도로 채택 (e = 0. Stock 2020) 되어 1:1
spin-orbit 공명이 명확합니다 (3:2 는 삼축성과 함께 e ≳ 0.01 필요.
Vinson 2017 / Makarov 2018). 자전축 기울기는 0 으로 damping 됩니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 3.05989 일 = 264 374 s.
Kopernicus 에서 바디의 `rotationPeriod` 는 궤도 `period` 와 초 단위로
같습니다.

**계절 없음.** 자전축 기울기 = 0 과 원궤도에서 substellar 점은 표면
좌표계에 고정됩니다.

조밀하고 거의 동일평면인 구조에서 c 는 b 와 d 사이, 공명-인접한 빽빽한
사슬에 놓입니다. cfg 에 대한 유일한 spin 결과는 고정된 substellar 점과
계절의 부재입니다.

## Visual styling

표면과 대기 결정을 결합하면.

- **전체 색 팔레트.** 깊은 적등색 3100 K 빛 아래 따뜻한 철-색조 암석
  세계 (`#5e4a3c` primary, `#74402a` 산화 accent) — 안쪽 행성 b 보다
  약간 밝게 해 조밀계의 안→밖 온도 구배를 강화합니다.
- **Dayside.** 따뜻한 substellar 반구 (~450 K 정점) 에 텍스처 있는
  암석 평원. 얇은 대기가 있으면 희미한 따뜻한 사지 haze.
- **Terminator 띠.** airless 면 sharp 하고 고대비. 채택 시나리오에서는
  얇은-대기 산란으로 부드러워집니다.
- **Nightside.** 차가움. 얇은-대기 해석에서는 대기 재분배로 부분
  가열되고, airless 면 near-black. 충시 형제 b, d 의 반사광이 주된
  nightside 광원.
- **SPI 오로라 없음.** b 와 달리 c 는 flux-tube 구동체가 아니므로
  추론된 자기권도 항성-행성 오로라도 없이, 평범한 따뜻한 암석 세계로
  렌더링합니다.
- **하늘의 별.** YZ Cet 은 c 의 하늘에서 ~3.9° (지구에서 본 태양의 약
  8 배) 를 차지하는 깊은 적등색 (3100 K → `#cf5630`) 으로, 표면을
  ~4.7 배 지구 일사량으로 적십니다. 폭발 변광성 호스트의 잦은 flare 가
  조명을 점점이 끊습니다.
- **하늘의 형제 행성.** b (안쪽) 와 d (바깥) 가 밝게 움직이는 점으로
  보입니다. 거의 동일평면 조밀계라 충이 잦습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2020A&A...636A.119S** Stock et al. 2020 — c 의 궤도 (P = 3.05989 d,
  a = 0.02156 AU, e = 0) 와 최소질량 (1.14 M⊕), 준경험적 반지름 추정
  (1.05 R⊕) 의 Phase 2 recommended 출처.
- **2304.00031** Pineda & Villadsen 2023 — VLA SPI 연구. 전파 버스트가
  c 가 **아니라** b 의 궤도로 folding 됨을 확립 (c 는 위상 일치가 더
  나쁨). 따라서 c 는 SPI 구동체가 아닙니다. R_c = 1.05 R⊕ 인용.
- **2305.00809** Trigilio et al. 2023 — uGMRT SPI 확인. 같은 결론
  (c 와 d 는 검출이 궤도에 무작위로 섞여 folding 없음 → c 에 SPI 귀속
  없음). c-is-not-driver 결정의 출처.

### Read (context / methodology, not decision-driving)

- **2017A&A...605L..11A** Astudillo-Defru et al. 2017 — 발견 논문.
  이전 c 궤도/질량 해 (P = 3.06008 d, M sin i = 0.98 M⊕) 는
  `recommended:false` 로 보존.
- 항성 합성 (`yz-cet.md`) — c 의 조명을 정하는 Teff/L/R/M 값.

### Read (instrument-only, not visual-informative)

- 두 SPI 논문의 전파-간섭계 방법론은 c-not-driver 결론을 위해 읽었지만
  추가 c-고유 시각 필드는 주지 않습니다.

### Not read — no arXiv preprint or low-priority (~handful)

c 의 JWST, 통과, 투과-분광 논문은 없습니다 (c 는 통과하지 않음). 따라서
읽을 식/대기 문헌이 없습니다. 두 전파 논문 안의 일반적인 SPI-이론
참고문헌은 맥락용으로 읽었지만 c-고유 cfg 수치는 주지 않습니다.

## Open items for follow-up

- **cfg 변형: airless c.** 채택된 얇은-대기 해석은 interesting-first
  tie-break 입니다. 보수적 airless 변형은 대안 cfg 로 여기 보존합니다.
- **반지름은 측정이 아니라 추정.** c 는 통과하지 않습니다. 1.05 R⊕
  수치는 준경험적입니다. 미래 질량/반지름 측정이 표면 중력과 밀도를
  갱신할 것입니다.
- **대기 검출.** 미래 방출/위상-곡선 캠페인만이 얇은 대기를 확인하거나
  배제할 수 있습니다. 그때까지 압력은 low-confidence 입니다.

## Related

- [yz-cet](yz-cet.md) — 호스트 별. 확인된 SPI 전파 오로라를 가진 M4.5 V flare star
- [yz-cet-b](yz-cet-b.md) — 안쪽 형제이자 SPI 구동체 (≥ 0.4 G 자기장)
- [yz-cet-d](yz-cet-d.md) — 최외측 형제
- [methodology](../reference/methodology.md) — Decisions 표와 confidence 태그의 스키마
