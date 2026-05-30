<!-- 55 Cnc c Phase 3 합성. cfg-ready 결정과 근거 -->
# 55 Cnc c — Phase 3 합성

55 Cnc c 는 55 Cnc A 주위를 44.4일, 약하게 이심인 궤도로 0.247 AU 에서
도는 토성급 거대 행성으로, McArthur 외 2004 가 발견했습니다. 시선속도
최소 질량은 M sin i ≈ 56.6 M⊕ ≈ 0.18 M_Jup(Moutou 2025)으로—대략
토성-질량입니다. 통과하지 않으므로 측정된 반지름이 없습니다. 토성-질량
거대 행성이라면 ~0.8 R_Jup 근처의 반지름이 표준 추정입니다. 모성 광도
L = 0.582 L☉ 로 평형 온도는 T_eq(A=0) ≈ 489 K 가 유도됩니다—따뜻한
토성급 거대 행성으로, 안쪽 뜨거운 목성 b 보다 차갑지만 여전히 온대 영역보다
한참 위입니다.

**NearStars 시나리오 선택: K0 모성의 노랑-주황 빛 아래 따뜻하고 차분한
색조의 띠 구름 덱으로 렌더링되는 따뜻한 토성급 거대 가스 행성
(~0.18 M_Jup, ~490 K).** 질량은 Msini(RV), 반지름은 추정-전용 토성급
값이며 cfg 가 둘 다 그에 맞게 플래그합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | medium | 44.4 d 궤도. 0.247 AU 에서 거대 가스 행성 조석 고정 시간 척도가 계 나이를 한참 초과 |
| `obliquity_deg` | 0 | low | Tie-break: 낮다고 가정. 미제약 |
| `eccentricity` | 0.088 | medium | Moutou 2025(Bourrier 2018 은 0.03. 큰 불확실성 ±0.23) |
| `argument_of_periastron_deg` | 31 | low | NASA Archive 원시값 |
| `sidereal_period_days` | 44.3936 | high | Moutou 2025(Phase 2 추천. Bourrier 2018 44.3989 일치) |
| `semi_major_axis_au` | 0.247 | high | Moutou 2025(Phase 2 추천. Bourrier 2018 0.2373) |
| `inclination_deg` | ~89.7(미제약, ±24°) | low | 원시값. 비통과 |
| `mass_mearth` | 56.6(M sin i) | high | Moutou 2025 — RV 최소 질량(Phase 2 추천. Bourrier 2018 51.2) |
| `mass_type` | Msini | high | Moutou 2025 — 시선속도 최소 질량. 비통과 |
| `mass_mjup` | 0.18(M sin i) | high | 유도 = 56.6 / 317.8 |
| `radius_rjup` | ~0.8(추정 전용) | low | 측정 반지름 없음(비통과). ~0.18 M_Jup, ~490 K 의 토성급 추정 |
| `equilibrium_temp_k` (A=0) | 489 | high | 유도: 278.3·0.582^0.25/√0.247 |
| `equilibrium_temp_k` (A=0.3) | 447 | high | 유도, 목성형 알베도 |
| `insolation_s_earth` | 9.5 | high | 유도 = L / a² = 0.582 / 0.247² |
| `bond_albedo` | 0.3 | low | Tie-break: 구름 낀 따뜻 토성급, 목성/토성형 알베도 |
| `atmosphere_present` | true | high | 거대 가스 행성 — H/He 외피 |
| `atmosphere_composition` | 알칼리 금속을 가진 H₂/He, 황화물/규산염 응결 구름 | medium | ~490 K 따뜻-토성형 화학. 초금속 풍부 모성은 풍부한 금속도를 선호 |
| `cloud_cover_fraction` | 0.9 | medium | 띠 모양 거대 가스 행성 구름 덱 |
| `cloud_morphology` | 띠 모양. 토성의 암모니아 구름보다 따뜻하나 55 Cnc b 의 규산염보다 차가운 황화물/알칼리-염 구름 덱 | medium | ~490 K — b 의 규산염 구름과 태양계 거대 행성의 NH₃ 구름 사이 |
| `cloud_tint_rgb_hex` | `#d4b890`(따뜻하고 차분한 황갈) | low | Tie-break: 따뜻-토성형 응결물 팔레트, b 의 더 뜨거운 규산염 황갈보다 부드럽고 옅음 |
| `atmosphere_tint_rgb_hex` | `#e0c8a0`(옅고 따뜻한 림 헤이즈) | low | Tie-break: ~490 K 토성급 림 |
| `star_apparent_angular_diameter_deg` | 2.04 | high | 유도: 2·R★/a = 2·0.943 R☉ / 0.247 AU |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 항성 Teff |

## Surface synthesis

55 Cnc c 는 표면 없는 토성-질량 거대 가스 행성이라, 이 섹션은 구름 꼭대기
"표면"을 다룹니다. T_eq ≈ 489 K 에서 그것은 **따뜻한 토성급** 세계입니다—
안쪽 뜨거운 목성 b(708 K)보다 차갑지만 여전히 암모니아/물-얼음 구름에는
너무 따뜻합니다. 이 온도의 가시 응결물은 알칼리-금속염(Na₂S, KCl)과
황화물로, 태양계 거대 행성의 암모니아 구름보다 깊고 높은 온도에 자리합니다.

구름 꼭대기 팔레트는 따뜻하고 차분한 황갈(`#d4b890`)입니다—더 차가운 응결
화학을 반영해 55 Cnc b 의 더 뜨거운 규산염-황갈보다 부드럽고 옅습니다.
초태양 모성 금속도([Fe/H] ≈ +0.32)는 다시 더 강한 알칼리 흡수와 더 짙은
구름 색을 가진 풍부한 대기를 시사합니다. 5196 K 노랑-주황 모성 빛 아래
행성은 따뜻하고 부드럽게 띠진 황갈 거대 행성으로 읽힙니다.

형태: 더 뜨거운 b 보다 다소 낮은 대비의 띠 모양(차가운 대기는 더 미묘한
띠로 향함). cfg 는 행성 팔레트로 따뜻하게·차분하게 한 토성-유사체 띠 모양을
렌더링합니다.

## Atmosphere synthesis

55 Cnc c 는 심층 H₂/He 외피를 가집니다. ~490 K 에서 가시-고도 응결물은
알칼리-금속염과 황화물이며, 기체상 Na/K 가 광학 흡수를 만듭니다. 초금속
풍부 모성은 풍부한 금속도를 시사하여 구름 색을 짙게 합니다.

- **압력 / 구조.** 알칼리/황화물 준위의 응결 구름 덱을 가진 연속 H₂/He
  대기. 별개 표면 없음.
- **조성.** H₂/He 주체에 Na/K 와 황화물/규산염 응결물. 초태양 모성에서
  향상된 중원소 풍부도 가능성.
- **하늘 외관.** 상층 대기에서 하늘은 옅은 따뜻 황갈로, 알칼리/황화물
  구름으로 흐려지며, 모성(각지름 2.0°)이 두드러지나 안쪽 행성들에서처럼
  압도적으로 지배하지는 않습니다.

## Rotation & spin synthesis

0.247 AU 에서 44.4일 궤도로, 55 Cnc c 는 조석 고정되지 않습니다—이 거리의
거대 가스 행성 조석 고정 시간 척도가 ~10 Gyr 계 나이를 한참 초과합니다.
궤도는 약하게 이심(e = 0.088, 큰 불확실성 동반. Moutou 2025)입니다. 자전
주기는 측정되지 않았습니다.

**KSP 구현 노트.** cfg 는 시각적 띠 모양을 위해 빠른 목성형 자전(~10–11시간
자릿수, 토성 유사체)을 채택합니다. 이는 tie-break 이며 미제약으로
플래그합니다.

**약한 계절.** e ≈ 0.088 이심은 적당한 근점-원점 일사 변동(원점 ~470 K
에서 근점 ~510 K 의 T_eq)을 주지만, 무시할 만한 자전축 경사라 축 계절은
없습니다.

## Visual styling

- **전체 외관.** 0.247 AU 의 따뜻하고 차분한-황갈 토성급 띠 거대 행성—이 계
  네 거대 행성 중 둘째로, 더 뜨거운 안쪽 b 와 온대 f 사이입니다.
- **구름 덱.** 따뜻한 황갈(`#d4b890`)의 띠 모양으로, b 보다 부드럽고
  옅으며, 밝은-존 / 어두운-벨트가 부드럽게 번갈음.
- **림 / 헤이즈.** 옅고 따뜻한 림 헤이즈(`#e0c8a0`).
- **하늘의 별.** 55 Cnc A 는 2.04° 를 차지—지구에서 본 태양 각지름의 약
  4 배—두드러진 따뜻-주황 디스크.
- **하늘의 자매 행성.** 행성 b(0.118 AU 안쪽)와 행성 f(0.80 AU 바깥)가
  따뜻한 점으로 나타나며, 용암 초지구 e 는 별 근처에 묻힘.
- **고리 없음(기본).** ~490 K 에서 c 는 안정한 얼음 고리에는 너무 따뜻함.
  고리는 렌더링 안 함(차가운 거대 행성 d 가 계의 고리-후보 천체).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). 최신 RV 재피팅: 행성 c P = 44.3936 d,
  a = 0.247 AU, e = 0.088, M sin i = 56.6 ± 2.2 M⊕. **Phase 2 추천 궤도
  + 질량.** 모델 컷오프 이후 출판 — 캐시 텍스트에 대조 확인.
- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  arXiv:1107.1936. 모성 L = 0.582 L☉ → T_eq 유도.

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  arXiv:1807.04301. 재피팅: c 가 a = 0.2373 AU, e = 0.03,
  M sin i = 51.2 M⊕ — 기록된-대안 궤도/질량(Moutou 2025 로 대체).
- **McArthur B. E. et al. 2004** — `2004ApJ...614L..81M`. 발견 논문.
  역사적 맥락.

### Read (instrument-only, not visual-informative)

- (위 계-수준 논문 외에 c 에 특정한 항목 없음.)

### Not read — no arXiv preprint or low-priority (~15 papers)

초기 RV 정제 논문(Fischer 2008)과 동역학-안정성 자료. 완전한 필터링
bib 는 `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **반지름.** 측정 반지름 없음(비통과). ~0.8 R_Jup 은 추정-전용입니다.
  경사/진질량 제약이 반지름 정제를 가능케 할 것입니다.
- **이심.** e = 0.088 은 큰 불확실성을 동반합니다(큐레이션 항목에서 ±0.23).
  더 정밀한 RV 해가 약한-계절 처리를 굳힐 것입니다.
- **대기 금속도.** 초금속 풍부 모성에서 풍부한 조성이 예상됩니다. 미래
  방출/투과 제약이 구름 색을 다듬을 것입니다.

## Related

- [55-cnc](55-cnc.md) — 모성(K0 IV-V, L = 0.582 L☉)
- [55-cnc-b](55-cnc-b.md) — 안쪽 이웃(더 뜨거운 목성형)
- [55-cnc-f](55-cnc-f.md) — 바깥쪽 이웃(온대, HZ-스치는 거대 행성)
- [methodology](../reference/methodology.md) — Decisions 스키마와 Msini 관례
