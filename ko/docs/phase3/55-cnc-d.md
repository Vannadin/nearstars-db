<!-- 55 Cnc d Phase 3 합성. cfg-ready 결정과 근거 -->
# 55 Cnc d — Phase 3 합성

55 Cnc d 는 이 계의 차가운 외곽 거대 행성입니다: 55 Cnc A 주위를 긴
~4799일(~13.1년) 이심(e ≈ 0.09) 궤도로 5.6 AU 에서 도는 ~3.8 M_Jup
(M sin i ≈ 1214 M⊕, Moutou 2025)의 거대 가스 행성입니다. 역사상 가장 먼저
발견된 장주기 거대 행성 중 하나로(Marcy 외 2002), 당시 알려진 가장 긴
궤도 주기에 속했습니다. 그 정확한 궤도는 이 계에서 가장 논쟁적인 신호로
남아 있는데, 주기가 별의 ~10.5년 자기 주기와 얽혀 있기 때문입니다—Bourrier
2018 은 5574 d / ~6 AU, Moutou 2025 는 4799 d / 5.6 AU 에 두었고, 다른
연구들은 4825–5285 d 에 걸칩니다. 통과하지 않으므로 측정된 반지름이
없습니다. ~3.8 M_Jup 거대 행성이라면 ~1.1–1.2 R_Jup 근처의 반지름이 표준
추정입니다(무거운 거대 행성은 약간 압축됨). 모성 광도 L = 0.582 L☉ 로
평형 온도는 T_eq(A=0) ≈ 103 K 가 유도됩니다—목성보다 차가운 진정한 **차가운
목성형**으로, 암모니아 구름과 가능한 고리/위성계가 안정한 영역에 있습니다.

**NearStars 시나리오 선택: 5.6 AU 의 차갑고 무거운 목성형(~3.8 M_Jup,
~100 K)으로, 차가운 차분한 색조의 깊은 암모니아-구름 거대 가스 행성으로
렌더링—그리고 디스크-색 / 고리 정책에 따라 이 계의 고리-후보 천체로서
선택적 예술적 토성 같은 고리계(관측 안 됨으로 플래그)를 가짐.** 질량은
Msini(RV), 반지름은 추정-전용이며, 고리는 관측이 아니라 명시적 예술
옵션입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 5.6 AU 에서 4799 d 궤도. 어떤 조석 영역에서도 한참 벗어남 |
| `obliquity_deg` | 0 | low | Tie-break: 낮다고 가정. 미제약 |
| `eccentricity` | 0.0913 | medium | Moutou 2025(Bourrier 2018 은 0.13. 궤도가 주기-얽혀 불확실) |
| `argument_of_periastron_deg` | −90 | low | NASA Archive 원시값 |
| `sidereal_period_days` | 4799 | medium | Moutou 2025(Phase 2 추천. Bourrier 2018 의 5574 d 와 기록된 발산 — Canonical alternatives 참조) |
| `semi_major_axis_au` | 5.6 | medium | Moutou 2025(Phase 2 추천. Bourrier 2018 5.957) |
| `inclination_deg` | ~89.7(미제약, ±24°) | low | 원시값. 비통과 |
| `mass_mearth` | 1214(M sin i) | high | Moutou 2025 — RV 최소 질량(Phase 2 추천. Bourrier 2018 991.6) |
| `mass_type` | Msini | high | Moutou 2025 — 시선속도 최소 질량. 비통과 |
| `mass_mjup` | 3.8(M sin i) | high | 유도 = 1214 / 317.8(Moutou 2025 초록이 3.8 M_Jup 인용) |
| `radius_rjup` | ~1.1(추정 전용) | low | 측정 반지름 없음(비통과). ~3.8 M_Jup, ~100 K 의 무거운-목성형 추정(약간 압축). Fortney, Marley & Barnes 2007 (`astro-ph/0612671`) 의 따뜻한 거대행성 질량-반지름-일사 트랙에서 읽음 |
| `equilibrium_temp_k` (A=0) | 103 | high | 유도: 278.3·0.582^0.25/√5.6 |
| `equilibrium_temp_k` (A=0.3) | 94 | high | 유도, 목성형 알베도 |
| `insolation_s_earth` | 0.019 | high | 유도 = L / a² = 0.582 / 5.6² |
| `bond_albedo` | 0.3 | low | Tie-break: 암모니아-구름 차가운 목성형, 목성형 알베도 |
| `atmosphere_present` | true | high | 거대 가스 행성 — H/He 외피 |
| `atmosphere_reference_pressure_pa` | 100000 | medium | 거대 가스 행성 — 고체 표면 없음. 구름층 렌더링용 1 bar cfg 기준압 |
| `atmosphere_composition` | NH₃ + 더 깊은 NH₄SH / H₂O 구름 덱을 가진 H₂/He. 가능한 CH₄ 색조 | medium | ~100 K — 차가운 목성형, 암모니아-구름 영역. 이 온도에 CH₄ 흡수 가능 |
| `cloud_cover_fraction` | 0.95 | medium | 깊은 띠 모양 거대 가스 행성 구름 덱 |
| `cloud_morphology` | 띠 모양. 깊은 NH₃ + NH₄SH 구름 덱(목성/토성 유사체), 고대비 벨트와 존 | medium | ~100 K — 차가운 태양계 거대 행성의 암모니아-구름 영역에 완전히 속함 |
| `cloud_tint_rgb_hex` | `#dcdcd0`(차가운 옅은 크림-회색, NH₃ 구름) | low | Tie-break: 차가운-목성형 암모니아 팔레트, 약간 회색-차가움 |
| `atmosphere_tint_rgb_hex` | `#cdd8e4`(차가운 옅은-청색 림, Rayleigh + CH₄) | low | Tie-break: ~100 K 차가운 림, CH₄ 색조 |
| `ring_present` | true(예술 옵션 — 관측 안 됨) | low | Tie-break: 관측된 고리 없음. ~100 K 에서 토성 같은 얼음 고리는 그럴듯하며 디스크/고리 정책상 예술 옵션으로 허용 — `ring_observed = false` 로 플래그 |
| `ring_inner_au` | 0.0012 | low | Tie-break: 예술 고리의 ~1.5 R_Jup 안쪽 가장자리(≈ 토성-상대 기하) |
| `ring_outer_au` | 0.0035 | low | Tie-break: ~4.5 R_Jup 바깥 가장자리(토성-상대 기하) |
| `ring_color_hex` | `#e8e4d8`(얼음 크림-흰색) | low | Tie-break: ~100 K 의 차가운 물-얼음 고리, 토성처럼 |
| `ring_opacity` | 0.6 | low | Tie-break: 가시성을 위한 토성 같은 적당한 불투명도 |
| `ring_morphology` | Cassini 같은 간극을 가진 다중-고리 얼음계(예술) | low | Tie-break: 토성 유사체. 순전히 예술적 |
| `ring_observed` | false | high | 관측된 고리 없음. 반-조작 정책에 따라 플래그 — 고리는 명시적 예술 옵션일 뿐 |
| `star_apparent_angular_diameter_deg` | 0.090 | high | 유도: 2·R★/a = 2·0.943 R☉ / 5.6 AU — 별은 작고 밝은 점 |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 항성 Teff |

## Surface synthesis

55 Cnc d 는 표면 없는 무거운(~3.8 M_Jup) 차가운 거대 가스 행성이라, 이
섹션은 구름 꼭대기 "표면"을 다룹니다. T_eq ≈ 103 K 에서 그것은 이 계 유일의
**차가운 목성형**—목성(~110 K)보다 차가워—암모니아-구름 영역에 확고히
속합니다. 그 큰 질량은 d 를 안쪽 네 행성 한참 너머 긴 ~13년 궤도에서 계의
지배적 외곽 천체로 만듭니다(f–d 간극은 ~4 AU).

구름 꼭대기 팔레트는 차가운 옅은 크림-회색(`#dcdcd0`)입니다—그 아래 NH₄SH
와 물 구름을 가진 깊은 암모니아 구름으로, 태양계 거대 행성과 비슷하나 더
차갑고 약간 더 회색입니다. 이 온도의 메탄 흡수가 림에 희미한 차가운-청색
색조(`#cdd8e4`)를 더할 수 있습니다. 초금속 풍부 모성은 풍부하고 고대비의
대기를 시사합니다. 5196 K 모성 빛 아래—이제 d 의 하늘에서 작고 밝은 0.09°
지름 점인—행성은 깊고 고대비의 차가운-색조 띠 거대 행성으로 읽힙니다: 계에서
가장 고전적으로 "거대 가스 행성"다운 세계입니다.

형태: 높은 벨트/존 대비의 깊은 띠 모양(차가운 거대 행성은 강한 띠를 보임),
선택적 장수명 폭풍 와류, 그리고—예술 옵션으로—토성 같은 고리계(아래 참조).

## Atmosphere synthesis

55 Cnc d 는 깊고 무거운 H₂/He 외피를 가집니다. ~100 K 에서 가시 응결물은
암모니아 얼음(NH₃)이며, 더 깊이 암모늄 하이드로설파이드(NH₄SH)와 물 구름,
그리고 차가운-청색 흡수 색조를 만드는 가능한 기체상 메탄이 있습니다—고전적
차가운-거대-행성 구름 화학입니다.

- **압력 / 구조.** NH₃-얼음 구름 덱, 그 아래 NH₄SH 와 물 구름을 가진 깊은
  H₂/He 대기. 별개 표면 없음. 큰 질량이 깊고 고압인 내부를 줍니다.
- **조성.** H₂/He 주체에 NH₃, NH₄SH, H₂O, 가능한 CH₄. 초금속 풍부 모성은
  향상된 중원소 풍부도를 시사.
- **하늘 외관.** 상층 대기에서 하늘은 차가운 옅은 크림-청색으로, 모성은
  작고 밝은 점(0.09°)—어느 55 Cnc 행성보다 가장 어두운 항성 조명에,
  ~1065 AU 멀리의 M형 왜성 동반성 55 Cnc B 가 희미한 주황-적색 두 번째
  태양으로 더해집니다.

## Rotation & spin synthesis

5.6 AU 에서 ~4799일 궤도로, 55 Cnc d 는 어떤 조석 고정 영역에서도 한참
벗어나 태양계 거대 행성처럼 자유롭고 빠르게 자전합니다. 궤도는 약하게
이심(e ≈ 0.09. Moutou 2025)이나, ~13년 궤도가 별의 ~10.5년 자기 주기와
얽혀 있어 이심과 주기 둘 다 불확실합니다. 자전 주기는 측정되지 않았습니다.

**KSP 구현 노트.** cfg 는 시각적 띠 모양을 위해 빠른 목성형 자전(~10시간
자릿수, 목성 유사체)을 채택합니다. 이는 tie-break 이며 미제약으로
플래그합니다.

**계절 없음.** 무시할 만한 자전축 경사 → 축 계절 없음. 약한 이심은 이미
매우 낮은 일사(0.019 S⊕)에 작은 일사 변동만 줍니다.

## Visual styling

- **전체 외관.** 5.6 AU 의 무겁고 차가운 고대비 띠 거대 가스 행성—이 계의
  지배적 외곽 천체이자 가장 고전적으로 "거대 가스 행성"다운 세계로, 선택적
  토성 같은 고리를 두를 수 있습니다.
- **구름 덱.** 차가운 옅은 크림-회색(`#dcdcd0`)의 깊은 띠 모양으로, 높은
  벨트/존 대비와 선택적 장수명 폭풍 와류.
- **림 / 헤이즈.** 차가운 옅은-청색의 메탄 색조 림(`#cdd8e4`).
- **고리계(선택, 예술).** 이 계의 고리-후보 천체로서 d 는 토성 같은 얼음
  고리(`#e8e4d8`, 불투명도 0.6, ~1.5–4.5 R_Jup, Cassini 같은 간극을 가진
  다중-고리)로 렌더링될 수 있습니다. ~100 K 에서 물-얼음 고리는 열적으로
  안정합니다. 이는 **관측이 아니라 명시적 예술 옵션**(`ring_observed =
  false`)으로—고리/디스크 정책에 따라 차가운 거대 행성의 허용된 미적
  선택으로 포함되며, 결코 검출된 것으로 제시되지 않습니다.
- **하늘의 별.** 55 Cnc A 는 0.090° 만 차지—지구에서 본 태양 각지름의 약
  1/6—작고 밝은 따뜻-주황 점. 조명은 어둡습니다(0.019 S⊕, 지구의 ~2%).
- **하늘의 자매 행성.** 안쪽 네 행성은 d 의 시점에서 모두 별에 가깝습니다.
  온대 f(0.80 AU 안쪽)가 가장 가까운, 희미한 점입니다. M형 왜성 동반성
  55 Cnc B(~1065 AU)는 d 궤도 한참 너머 희미한 주황-적색 두 번째 태양입니다.

## Canonical alternatives

55 Cnc d 의 궤도는 이 계에서 가장 논쟁적인 신호이며, cfg 는 두 문헌 주기
사이에서 기록된 선택을 합니다. 고리는 어느 관측도 고리를 주장하지 않으므로
발산이 아니라 명시적 예술 옵션(`ring_observed = false` 플래그)으로 별도로
다룹니다.

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `sidereal_period_days` / `semi_major_axis_au` | 4799 d / 5.6 AU(Moutou 2025) | 5574 d / 5.96 AU(Bourrier 2018) | 두 추천-급 RV 피팅이 주기에서 9σ 차이가 나는데, d 의 ~13년 궤도가 별의 ~10.5년 자기 주기와 얽혀 있고 결과가 주기 모델링 방식(케플러 vs GPR)과 결합 기기 선택에 민감하기 때문입니다. cfg 는 가장 최근값(Moutou 2025, 4799 d)을 Phase 2 추천으로 채택하고, Bourrier 2018 의 5574 d 궤도를 cfg 변종으로 보존합니다. 다른 연구는 4825–5285 d 에 걸칩니다. 이는 게임플레이 선택이 아니라 실제 측정 불일치입니다—cfg 작성자가 추천 궤도를 배포하되 대안의 존재를 알도록 플래그합니다. |

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). 최신 RV 재피팅: 행성 d P = 4799 d(Bourrier 2018 의
  5574 d 보다 9σ 짧음), a = 5.6 AU, e = 0.0913, M sin i = 1214 ± 41 M⊕
  ≈ 3.8 M_Jup. 궤도가 ~10.5년 자기 주기와 얽히고 가능한 추가 외곽
  천체(장기 RV 추세, P > 24 yr)가 있음을 지적. **Phase 2 추천 궤도 +
  질량.** 모델 컷오프 이후 출판 — 캐시 텍스트에 대조 확인.
- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  arXiv:1107.1936. 모성 L = 0.582 L☉ → T_eq 유도.

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  arXiv:1807.04301. 자기-주기 케플러를 포함한 재피팅: d 가 P = 5574 d,
  a = 5.957 AU, e = 0.13, M sin i = 991.6 M⊕ — 기록된-대안
  궤도(Canonical alternatives 참조).
- **Marcy G. W. et al. 2002** — `2002ApJ...581.1375M`. d 의 발견 논문
  (당시 알려진 가장 긴 주기의 거대 행성 중 하나). 역사적 맥락.

### Read (instrument-only, not visual-informative)

- (위 계-수준 논문 외에 d 에 특정한 항목 없음.)

### Not read — no arXiv preprint or low-priority (~15 papers)

장주기-신호 분해 논문(Endl 2012, Baluev 2015, Rosenthal 2021, Laliotis
2023 — 모두 다른 d 주기를 주며, Canonical alternatives 에 정성적으로
포착됨)과 동역학-안정성 자료. 완전한 필터링 bib 는
`docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **궤도 명확화.** d 의 주기는 논쟁적입니다(4799 d Moutou 2025 vs 5574 d
  Bourrier 2018, 다른 곳은 4825–5285 d)—자기-주기 얽힘 때문입니다. 연속
  활동 지표를 가진 균질 장기 nIR + 광학 RV 캠페인(Moutou 2025 Open
  items)이 해결할 것이며, 주기가 개정되면 cfg 는 a, T_eq, 각지름을
  재유도해야 합니다.
- **가능한 추가 외곽 천체.** Moutou 2025 는 P > 24 yr 의 또 다른 천체를
  시사하는 장기 RV 추세(0.84 m/s/yr)를 발견합니다. 확인되면 여섯/일곱 번째
  행성 Decisions 항목이 필요할 수 있습니다.
- **반지름.** 측정 반지름 없음(비통과). ~1.1 R_Jup 은 추정-전용입니다.
  경사/진질량 또는 직접 영상 제약이 다듬을 것입니다.
- **고리 변종.** 토성 같은 고리는 예술 옵션입니다(`ring_observed =
  false`). 무-고리와 고리 cfg 변종을 둘 다 배포하며, 고리는 결코 검출된
  것으로 제시하지 않습니다.

## Related

- [55-cnc](55-cnc.md) — 모성(K0 IV-V, L = 0.582 L☉)
- [55-cnc-f](55-cnc-f.md) — 안쪽 이웃(온대 HZ-스치는 거대 행성). ~4 AU f–d 간극은 계에서 가장 큼
- [eps-eri](eps-eri.md) — 비교용 차가운-목성형 모성 맥락(3.5 AU 의 ε Eri b)
- [methodology](../reference/methodology.md) — Decisions 스키마, Msini 관례, 고리 필드
- [tools](../reference/tools.md) — 디스크/고리 색 합성 정책(반-조작)
