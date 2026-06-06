<!-- 55 Cnc f Phase 3 합성. cfg-ready 결정과 근거 -->
# 55 Cnc f — Phase 3 합성

55 Cnc f 는 이 계의 온대 거대 행성입니다: 55 Cnc A 주위를 260.6일,
이심(e ≈ 0.063) 궤도로 0.802 AU 에서 도는 ~0.15 M_Jup(M sin i ≈ 48.5 M⊕,
Moutou 2025)의 가스/얼음 거대 행성입니다. Fischer 외 2008 이 발견했으며,
von Braun 외 2011 이 이 계의 **거주 가능 영역 행성**으로 지목한 행성입니다.
그 논문은 f 가 "이심 궤도 지속 시간의 대부분을 주성 거주 가능 영역
(0.67–1.32 AU)에서 보내며, 적당한 온실 가열이 있으면 액체 물을 품을 수도
있다"고 했습니다.
통과하지 않으므로 측정된 반지름이 없습니다. 준-토성-질량 거대 행성이라면
~0.7 R_Jup 근처의 반지름이 표준 추정입니다. 모성 광도 L = 0.582 L☉ 로
평형 온도는 T_eq(A=0) ≈ 271 K 가 유도됩니다—진정으로 온대로, 이심 궤도
전체에서 원점 ~263 K 와 근점 ~280 K 를 오갑니다.

**NearStars 시나리오 선택: 거주 가능 영역을 스치는 온대 가스/얼음 거대
행성(~0.15 M_Jup, ~270 K)으로, K0 모성의 노랑-주황 빛 아래 물-얼음 구름 덱
(이 계 안쪽 거대 행성 중 가장 차가운 띠 응결물) 가능성을 가진 차가운 띠
거대 행성으로 렌더링.** 질량은 Msini(RV), 반지름은 추정-전용 준-토성 값이며
cfg 가 둘 다 플래그합니다. f 자체가 거대 가스 행성이라, 그 HZ 거주는 가상의
위성에 대해서만 흥미롭습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 0.802 AU 에서 260.6 d 궤도. 어떤 조석 고정 영역에서도 한참 벗어남 |
| `obliquity_deg` | 0 | low | Tie-break: 낮다고 가정. 미제약 |
| `eccentricity` | 0.063 | medium | Moutou 2025(Bourrier 2018 은 0.08. ±0.048) |
| `argument_of_periastron_deg` | 100 | low | NASA Archive 원시값 |
| `sidereal_period_days` | 260.58 | high | Moutou 2025(Phase 2 추천. Bourrier 2018 259.88 일치) |
| `semi_major_axis_au` | 0.802 | high | Moutou 2025(Phase 2 추천. Bourrier 2018 0.7708) |
| `inclination_deg` | ~89.7(미제약, ±24°) | low | 원시값. 비통과 |
| `mass_mearth` | 48.5(M sin i) | high | Moutou 2025 — RV 최소 질량(Phase 2 추천. Bourrier 2018 47.8) |
| `mass_type` | Msini | high | Moutou 2025 — 시선속도 최소 질량. 비통과 |
| `mass_mjup` | 0.15(M sin i) | high | 유도 = 48.5 / 317.8 |
| `radius_rjup` | ~0.7(추정 전용) | low | 측정 반지름 없음(비통과). ~0.15 M_Jup, ~270 K 의 준-토성 추정 |
| `equilibrium_temp_k` (A=0) | 271 | high | 유도: 278.3·0.582^0.25/√0.802 |
| `equilibrium_temp_k` (A=0.3) | 248 | high | 유도, 목성형 알베도 |
| `equilibrium_temp_k_periastron` (A=0) | 280 | high | a(1−e) = 0.752 AU 에서 유도 |
| `equilibrium_temp_k_apastron` (A=0) | 263 | high | a(1+e) = 0.853 AU 에서 유도 |
| `insolation_s_earth` | 0.9 | high | 유도 = L / a² = 0.582 / 0.802²(≈ 지구형) |
| `bond_albedo` | 0.3 | low | Tie-break: 구름 낀 온대 거대 행성, 목성/토성형 알베도 |
| `atmosphere_present` | true | high | 가스/얼음 거대 행성 — H/He 외피 |
| `atmosphere_reference_pressure_pa` | 100000 | medium | 거대 가스 행성 — 고체 표면 없음. 구름층 렌더링용 1 bar cfg 기준압 |
| `atmosphere_composition` | NH₃ / NH₄SH / 가능한 H₂O-얼음 구름 덱을 가진 H₂/He | medium | ~270 K — 암모니아와 (더 깊은) 물-얼음 응결물에 충분히 차가움, 태양계 거대 행성처럼 |
| `cloud_cover_fraction` | 0.9 | medium | 띠 모양 거대 가스 행성 구름 덱 |
| `cloud_morphology` | 띠 모양. 암모니아 + 암모늄-하이드로설파이드 구름 덱(목성/토성 유사체)에 더 깊은 물 구름 가능 | medium | ~270 K 는 NH₃-구름 영역 — 흰 암모니아 구름에 충분히 차가운 유일한 안쪽 55 Cnc 거대 행성 |
| `cloud_tint_rgb_hex` | `#e8e0d0`(옅은 크림, NH₃-구름 목성형) | low | Tie-break: 차가운 온대-목성형 팔레트 — 따뜻한 안쪽 거대 행성보다 옅고 흼 |
| `atmosphere_tint_rgb_hex` | `#dde4ec`(옅은 차가운-청색 림 헤이즈) | low | Tie-break: 차가운 ~270 K 림, Rayleigh 색조 |
| `star_apparent_angular_diameter_deg` | 0.63 | high | 유도: 2·R★/a = 2·0.943 R☉ / 0.802 AU |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 항성 Teff |

## Surface synthesis

55 Cnc f 는 표면 없는 준-토성-질량 가스/얼음 거대 행성이라, 이 섹션은 구름
꼭대기 "표면"을 다룹니다. T_eq ≈ 271 K 에서 그것은 **진정으로 온대**—네
안쪽 거대 행성 중 가장 차갑고, 암모니아 구름(목성의 시그니처 흰 구름)이
가시 덱에서 응결할 수 있는 유일한 영역에 있습니다. 이심 궤도(e ≈ 0.063)는
평형 온도를 원점 ~263 K 에서 근점 ~280 K 로 운반하며—물의 어는점을 걸치고
궤도 대부분을 von Braun 2011 거주 가능 영역(0.67–1.32 AU) 안에서 보냅니다.

따라서 구름 꼭대기 팔레트는 옅고 크림-흰색(`#e8e0d0`)입니다—암모니아-구름
목성 색으로, b 와 c 의 따뜻한 황갈보다 뚜렷이 차갑고 흽니다. 암모늄
하이드로설파이드(NH₄SH) 구름이 형성되는 곳에서는 목성처럼 벨트에 황갈/주황
색조를 더합니다. 차가운 림은 옅은 청색 Rayleigh 색조(`#dde4ec`)를 띱니다.
5196 K 노랑-주황 모성 빛 아래 행성은 차갑고 크림-황갈 띠 거대 행성으로
읽힙니다—안쪽 계에서 가장 "목성다워" 보이는 세계입니다.

형태: 흰 암모니아 존과 황갈 NH₄SH 벨트를 가진 목성/토성-유사체 띠 모양.
온대 거대 행성으로서 그 띠 대비와 폭풍 활동(대적점 같은 와류, 선택)은
태양계-거대-행성 범위 안에 있습니다.

## Atmosphere synthesis

55 Cnc f 는 심층 H₂/He 외피를 가집니다. ~270 K 에서 가시 응결물은
암모니아 얼음(NH₃)과, 더 깊이 암모늄 하이드로설파이드(NH₄SH) 및 물입니다—
목성과 토성에 색을 입히는 바로 그 구름 화학입니다. 이것이 f 를 진정으로
태양계-닮은 구름 팔레트를 가진 유일한 안쪽 55 Cnc 거대 행성으로 만듭니다.

- **압력 / 구조.** 꼭대기에 NH₃-얼음 구름 덱, 그 아래 NH₄SH, 더 깊이 물
  구름을 가진 연속 H₂/He 대기. 별개 표면 없음.
- **조성.** H₂/He 주체에 NH₃, NH₄SH, H₂O 응결물. 초금속 풍부 모성은 향상된
  중원소 풍부도를 시사.
- **하늘 외관.** 상층 대기에서 하늘은 옅은 크림-청색으로, 모성은 0.63°
  의 소박한 디스크—지구에서 본 태양보다 약간 클 뿐인, 이 계 거대 행성 중
  가장 "태양 같은 하늘"입니다.

**거주 가능 영역 노트.** von Braun 2011 은 f 를 HZ 행성으로 지목했으나,
f 자체가 거대 가스 행성입니다—표면 액체 물을 가질 수 없습니다. 그 HZ
거주는 가상의 큰 위성에 대해서만 의미가 있으며, 이 위성은 원리상 온대일 수
있습니다. 그런 위성은 관측되지 않았고, 여기서 합성하지 않습니다(지어낸 천체
없음). HZ 거주는 f 자체의 거주성 주장이 아니라 맥락으로 기록합니다.

## Rotation & spin synthesis

0.802 AU 에서 260.6일 궤도로, 55 Cnc f 는 어떤 조석 고정 영역에서도 한참
벗어나 자유롭게 자전합니다. 궤도는 약하게 이심(e ≈ 0.063. Moutou 2025)
입니다. 자전 주기는 측정되지 않았습니다.

**KSP 구현 노트.** cfg 는 시각적 띠 모양을 위해 빠른 목성형 자전(~10시간
자릿수, 목성/토성 유사체)을 채택합니다. 이는 tie-break 이며 미제약으로
플래그합니다.

**약한 계절.** e ≈ 0.063 이심은 근점-원점 일사 변동(T_eq ~280 K → ~263 K)
을 주는데, 260일 궤도에 걸친 실제 ~6% 온도 변동이지만, 무시할 만한 자전축
경사라 축 계절은 없습니다.

## Visual styling

- **전체 외관.** 0.802 AU 의 차갑고 크림-황갈 띠 거대 행성—안쪽 계에서 가장
  목성다워 보이는 세계로, 이심 궤도에서 거주 가능 영역을 스칩니다.
- **구름 덱.** 목성-유사체 띠 모양: 흰 암모니아 존(`#e8e0d0`)과 황갈
  NH₄SH 벨트, 선택적 대적점 와류.
- **림 / 헤이즈.** 옅은 차가운-청색 Rayleigh 색조 림(`#dde4ec`), 따뜻한
  안쪽 거대 행성보다 차가운 색조.
- **하늘의 별.** 55 Cnc A 는 0.63° 만 차지—지구에서 본 태양보다 겨우 큼—
  어느 55 Cnc 거대 행성보다 가장 태양 같은 하늘.
- **하늘의 자매 행성.** 행성 c(0.247 AU 안쪽)는 따뜻한 점으로, 차가운 거대
  행성 d(5.6 AU 바깥)는 희미한 먼 점으로 나타남. 먼 M형 왜성 동반성
  55 Cnc B(~1065 AU)는 d 너머 희미한 주황-적색 두 번째 태양.
- **계절 밝기 깜박임(선택).** 이심 궤도에 걸친 ~6% 일사 변동이 260일 주기로
  구름 밝기를 미묘하게 변조할 수 있음—고증적이지만 사소한 터치.
- **고리 없음(기본).** f 는 계의 고리-후보 천체가 아님. 고리는 렌더링 안
  함(차가운 거대 행성 d 가 선택적 예술 고리를 가짐).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). 최신 RV 재피팅: 행성 f P = 260.58 d, a = 0.802 AU,
  e = 0.063, M sin i = 48.5 ± 2.8 M⊕. f 가 폭주-온실과 최대-온실 한계
  사이의 거주 가능 영역(Hill 2022)에 자리하고, 1–2 AU 의 온대 지구-질량
  행성이 동역학적으로 안정함을 확인. **Phase 2 추천 궤도 + 질량.** 모델
  컷오프 이후 출판 — 캐시 텍스트에 대조 확인.
- **von Braun K. et al. 2011** — *The 55 Cancri System… Habitable Zone
  Planet…*, ApJ 740, 49 (`2011ApJ...740...49V`, arXiv:1107.1936). 모성
  L = 0.582 L☉ → T_eq 유도. f 가 이심 궤도 대부분을 HZ(0.67–1.32 AU)에서
  보냄을 식별. **HZ-거주 정박.**

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  arXiv:1807.04301. 재피팅: f 가 a = 0.7708 AU, e = 0.08,
  M sin i = 47.8 M⊕ — 기록된-대안 궤도/질량(Moutou 2025 로 대체).
- **Fischer D. A. et al. 2008** — `2008ApJ...675..790F`. f 의 발견
  논문(260 d 의 0.15 M_Jup). 역사적 맥락.

### Read (instrument-only, not visual-informative)

- **Hill M. L. et al. 2022** — f 를 폭주/최대-온실 HZ 한계 안에
  자리매김(Moutou 2025 경유). HZ-기하 맥락.

### Not read — no arXiv preprint or low-priority (~15 papers)

동역학-안정성 자료(1–2 AU 온대-행성 안정성에 관한 Satyal & Cuntz 2019)와
초기 RV 정제 논문. 완전한 필터링 bib 는 `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **반지름.** 측정 반지름 없음(비통과). ~0.7 R_Jup 은 추정-전용입니다.
  경사/진질량 제약이 반지름 정제를 가능케 할 것입니다.
- **가상 위성.** f 의 HZ 거주는 큰 위성에 흥미롭지만 관측된 것이 없으므로,
  정책상 어떤 천체도 지어내지 않습니다. 위성이 언젠가 검출되면 온대-위성
  Phase 3 후속이 정당화될 것입니다.
- **구름 화학.** NH₃/NH₄SH 구름 배정은 온도 기반 추론입니다. 초금속 풍부
  모성이 구름 색을 옮길 수 있습니다. 미래 방출/투과 제약이 팔레트를 다듬을
  것입니다.

## Related

- [55-cnc](55-cnc.md) — 모성(K0 IV-V, L = 0.582 L☉, HZ 0.67–1.32 AU)
- [55-cnc-c](55-cnc-c.md) — 안쪽 이웃(따뜻한 토성급 거대 행성)
- [55-cnc-d](55-cnc-d.md) — 바깥쪽 이웃(차가운 거대 가스 행성, 고리 후보)
- [methodology](../reference/methodology.md) — Decisions 스키마와 Msini 관례
