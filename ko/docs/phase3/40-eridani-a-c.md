<!-- 40 Eridani A c Phase 3 합성. 완전히 합성된 NS 시스템 완결용 천체(수성 아날로그 필러) — 실제 검출 없음 -->
# 40 Eridani A c — Phase 3 Synthesis (Synthetic — NS system-completion body)

40 Eridani A c 는 **완전히 지어낸 행성**입니다. 검출도, 후보 신호도,
문헌상의 주장도 뒤에 없습니다 — 이 천체가 존재하는 이유는 오직
NearStars Phase 4 보드가 문화적으로 요구된 b("Vulcan"/"Erid", 그 자체가
철회된 검출이지만 documented divergence 로 유지됨)와 d 의 *Project Hail
Mary* Threeworld 아날로그 사이에 동역학적으로 그럴듯한 필러를 원했기
때문입니다. 아래의 모든 물리 행은 측정값이 아니라 설계값이며, 천체 전체가
`db/planets_curated.json` 에서 `method: theoretical` 로 표기됩니다.

*근거가 있는* 것은 동역학입니다. 궤도(a = 0.4 AU, e = 0.04,
P = 104.62 d)는 먼저 선택된 뒤, 0.78 M☉ K0.5 V 주성 주위 세 행성 전체
시스템에 대한 REBOUND 안정성 적분으로 검증되었습니다. WHFast 로 10⁵ 년,
상대 에너지 오차 4.6×10⁻¹¹, MEGNO = 2.00(정칙, 비카오스)로 세 천체 모두
차분한 이심률 진화 속에 안정으로 판정되었습니다
(`phase3/stability-sim/results/40_eridani_summary.json`). 궤도는 b 바깥의
3:1 주기비 근처, d 안쪽의 2:1 근처에 자리하며 — 공명에 가깝지만 의도적으로
공명 안에는 들지 않게 배치되었습니다.

물리 설계는 **수성 아날로그**입니다. 0.055 M⊕ 와 0.38 R⊕ 는 두 자리까지
수성 자체의 질량과 반지름이며, 그 덕분에 유도되는 밀도(~5.5 g/cc), 표면
중력(0.38 g), 탈출 속도(4.3 km/s)가 자동으로 수성 값에 내려앉습니다.
0.408 L☉ 주성 주위 0.4 AU 에서 복사 조도는 2.5 S⊕ 로 — 원일점의 수성보다
따뜻하고 근일점의 수성보다는 차가워 — 수성 판독은 자기 일관적입니다.
대기 없이 구워지고 크레이터로 뒤덮인 맨암석 세계입니다. 물리적 타당성
게이트에 따르면 이것은 용암 세계가 **아닙니다**(평형 온도 ~352 K 는 규산염
용융점 근처에도 못 미치고, 적용될 내부 가열 메커니즘도 없습니다).

**NearStars 시나리오 선택: 3:2 자전-공전 공명에 든 수성 아날로그 무대기
암석 — 크레이터로 뒤덮인 현무암-회색 레골리스에 옅은 소듐 외기권을
두르고, 낮면은 구워지고 밤면은 얼어붙으며, K0.5 V 주성의 주황빛 아래에
놓입니다.**

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | Synthetic (NS system-completion filler; no detection) | high | 유일한 high-confidence 행. 이 천체는 지어낸 것입니다. DB 엔트리는 `method: theoretical` 이며 설계 근거가 reference 문자열에 담겨 있습니다 |
| `mass_mearth` | 0.055 | low | 설계값 — 수성의 질량. 모든 유도값이 수성의 검증된 자기 일관성을 물려받도록 선택 |
| `radius_rearth` | 0.38 | low | 설계값 — 수성의 반지름. 위 질량과 짝지음 |
| `density_g_cc` | ~5.5 | low | 유도 M/R³ — 수성형 철-풍부 암석 |
| `surface_gravity_g_earth` | ~0.38 | low | 유도 0.055/0.38² |
| `equilibrium_temp_k` (A=0.3) | 322 | low | 유도. (A=0) 352, (A=0.088 수성 알베도) 344 |
| `insolation_s_earth` | ~2.55 | low | 유도 0.4078 L☉ / (0.4 AU)² |
| `surface_temp_k` | ~490 dayside peak / ~100 night | low | 무대기 저속 자전체 영역: 항성직하점 ≈ √2 × Teq(수성 알베도 기준). 수성 아날로그 낮-밤 대비 |
| `bond_albedo` | 0.088 | low | 수성의 본드 알베도 — 우주 풍화된 어두운 현무암 레골리스 |
| `tidally_locked` | false (3:2 spin–orbit resonance) | low | tie-break: e = 0.04 에서 조석 감쇠는 순수 1:1 보다 공명 포획에 유리. 수성 선례를 통째로 채택 |
| `rotation_period_h` | 1674 (= 2/3 × 104.62 d) | low | 3:2 공명 선택에서 따라옴 |
| `atmosphere_composition` | none (trace Na exosphere) | low | ~350 K 에서 4.3 km/s 탈출 속도는 아무것도 붙잡지 못함. 소듐 외기권은 수성 아날로그의 장식 |
| `atmosphere_surface_pressure_pa` | 0 | low | 무대기 |
| `surface_tint_rgb_hex` | `#8d8781` (space-weathered basalt gray) | low | tie-break: 수성 레골리스 톤을 K0.5 V (5143 K) 광원 아래에서 약간 따뜻하게 조정 |
| `sky_tint_rgb_hex` | `#000000` (airless black) | low | 대기 없음, 하늘 색 없음 |

## Surface synthesis

표면은 관측된 것이 아니라 설계된 것이므로, 여기서의 합성 작업은 문헌
정합이 아니라 자기 일관성입니다. 수성의 질량과 반지름을 통째로 채택하면
물리적으로 검증된 패키지를 얻습니다 — 철-풍부 ~5.5 g/cc 내부, 0.38 g 표면
중력, 그리고 이 온도에서 무대기를 보장하는 4.3 km/s 탈출 속도입니다. 설계는
각각 별도의 정당화가 필요한 새로운 물리 파라미터를 지어내는 일을 의도적으로
피합니다.

**열적 영역 — 용암이 아니라 구워진 암석.** 2.55 S⊕ 에서 평형 온도는
~352 K(제로 알베도)이고, 저속 자전 무대기 영역에서 항성직하 낮면 정점은
~490 K 로 — 굽기에는 충분히 뜨겁지만 ~1300 K 규산염 용융점에서 두 영역이나
모자랍니다. 따라서 물리적 타당성 게이트가 맨암석 판독을 강제합니다. 이
천체에 용암이나 마그마 못 렌더링은 옹호 불가하며 명시적으로 배제됩니다.

**크레이터투성이 수성 아날로그 지형.** 대기도 없고 내부 가열 메커니즘도
없으므로 표면 기록은 충돌이 지배합니다 — 심한 크레이터, 전지구 열수축에서
비롯한 엽상 단층애(이 질량대에서 수성의 상징적 구조 지형), 그리고 본드
알베도 ~0.09 까지 어두워진 우주 풍화 레골리스입니다. 1.8 Gyr 시스템
나이(호스트 합성에 채택된 Bond 2017 IFMR)는 4.5 Gyr 수성보다 크레이터가
다소 적음을 뜻하며, 이는 cfg 필드가 아니라 텍스처 패스용 메모입니다.

**낮-밤 대비.** 3:2 공명은 궤도 주기 두 배의 태양일(~209 d)을 주므로 각
반구가 몇 달 동안 구워졌다가 다시 몇 달 동안 얼어붙습니다 — 수성의 극단적
열 순환이 약간 더 높은 복사 조도에서 재현됩니다.

## Atmosphere synthesis

합성할 것이 없습니다. 4.3 km/s 탈출 속도와 ~350–490 K 낮면 온도에서 열적
(Jeans) 탈출이 탈가스된 휘발성 물질 재고를 지질학적으로 짧은 시간 척도에
전부 벗겨냅니다 — 수성에서와 똑같습니다. cfg 는 표면 압력을 0 으로
설정합니다.

**유일한 장식으로서의 소듐 외기권.** 수성은 태양풍과 미소 운석에 의해
레골리스에서 튀어나온 희박하고 광학적으로 무시할 만한 소듐 외기권을
유지합니다. 같은 메커니즘이 이곳에서도 K 왜성 항성풍 아래 작동합니다.
이는 조성 행에 플레이버로 기록될 뿐 — 압력도, 시각적 두께도 없고, 향후 아트
패스에서 옅은 방출 메모가 될 가능성 외에는 cfg 렌더링도 없습니다.

## Rotation & spin synthesis

0.78 M☉ 주위 a = 0.4 AU 에서 조석 감쇠 시간 척도는 충분히 짧아(작은 천체,
가까운 궤도) 원시 자전은 사라졌습니다 — 0.224 AU 의 b 가 고정 시간 척도를
근거로 자유 자전체를 택했던 것과 달리, c 의 더 작은 질량과 1.8 Gyr 나이는
이 천체를 감쇠된 영역에 둡니다. 그렇다면 e = 0.04 에서 최종 상태는 동기
1:1 이거나 자전-공전 공명입니다.

**interesting-first 선택: 수성의 3:2.** 0 이 아닌 설계 이심률에서 3:2
자전-공전 공명으로의 포획은 수성 선례의 결과이며, 시각적으로도 더 흥미로운
쪽입니다 — 표면의 모든 점이 낮과 밤을 모두 겪고, 명암 경계가 이동하며,
열 순환이 위의 구워짐/얼어붙음 대비를 구동합니다. 자전 주기는 정확히
104.62-d 궤도 주기의 2/3(~69.7 d, 1674 h)입니다.

## Visual styling

- **전체 외관.** 회색의 크레이터로 뒤덮인 수성 아날로그(`#8d8781` 기본
  색조)로, 무대기의 날카로운 그림자와 선명한 명암 경계를 지니며, 5143 K
  K0.5 V 주성이 눈에 띄게 주황빛으로 비춥니다 — 40 Eri A 시스템 전체
  팔레트를 Sol 대비 따뜻하게 만드는 바로 그 광원 이동입니다.
- **대기 효과 없음.** 검은 하늘(`#000000`), 림 헤이즈 없음, 산란 없음 —
  두 이웃과의 렌더링 대비가 핵심입니다. b 는 두꺼운 헤이즈의 뜨거운
  super-Earth, d 는 얇은 대기의 서리 세계, c 는 그 사이의 무대기 대조군
  입니다.
- **하늘의 동반체.** 40 Eri 시스템 어디에서나 그렇듯, 백색왜성 B /
  적색왜성 C 쌍(~400 AU 바깥)이 검은 하늘에서 눈부신 점 동반체로
  보입니다.
- **텍스처 패스 메모.** 엽상 단층애, 광조 크레이터, 그리고 수성 대비 약간
  낮은 크레이터 밀도(표면 나이 1.8 Gyr 대 4.5 Gyr).

## Canonical alternatives

**canonical 판독은 행성 없음입니다.** b(실재하지만 철회된 검출)와 달리 이
주기에는 관측상의 주장이 애초에 없었습니다 — c 는 순수한 시스템 완결
설계입니다. 현재 카탈로그의 canonical 40 Eridani A 시스템에는 확정된 행성이
하나도 없으며, NearStars 는 게임플레이 다양성과 *Star Trek* / *Project Hail
Mary* 문화 앵커를 위해 b, c, d 를 documented-divergence 앙상블로
렌더링합니다.

| Reading | System content | Status |
|---|---|---|
| Canonical catalogs (2026) | no confirmed planets around 40 Eri A | observation |
| **cfg pick** | b (refuted, cultural) + c (synthetic filler) + d (PHM Threeworld) | documented divergence (design) |

## Bibliography

지어낸 천체에는 발견이나 특성화 문헌이 없습니다. 참고문헌은 호스트
파라미터에 사용한 근거, 동역학 검증, 그리고 설계 방법을 기록합니다.

### Read (host + dynamics grounding)

- **[Boyajian et al. 2012](https://arxiv.org/abs/1208.2431)** —
  40 Eridani A 의 CHARA 간섭계 반지름/Teff/광도. c 의 복사 조도와 온도
  행을 정하는 0.4078 L☉ 를 줍니다.
- **[Bond et al. 2017](https://arxiv.org/abs/1709.00478)** —
  표면 나이 및 감쇠 논증에 사용한 IFMR 유래 시스템 동일생성 나이
  (~1.8 Gyr).
- **NearStars stability run** —
  `phase3/stability-sim/results/40_eridani_summary.json`: REBOUND
  WHFast, 10⁵ yr, 에너지 오차 4.6×10⁻¹¹, MEGNO 2.00, 모든 천체
  안정/차분(c 의 이심률은 0.040–0.095 사이에서 진동, 유계).

### Method references

- 수성 아날로그 패키지(질량, 반지름, 알베도, 3:2 공명) — 설계 기준선으로
  통째로 채택한 표준 태양계 값. 교과서 수준이라 도출값 근거화 정책의
  교과서 예외에 따라 논문 인용이 필요치 않습니다.
- 무대기 낮면/밤면 온도 영역 — NearStars 무대기 천체 전반에 쓰이는 동일한
  저속 자전체 항성직하점 공식(`docs/reference/methodology.md`).

## Open items for follow-up

- **모든 것이 설계.** 향후 관측이 이 천체를 제약할 것으로 기대되지
  않습니다(존재하지 않으므로). 행들은 Phase 4 보드가 설계 의도를 개정할
  때에만 바뀝니다.
- **공명 근접은 의도적이나 손댈 때 재확인 필요.** 근-3:1(b 와)과
  근-2:1(d 와) 간격은 10⁵ 년에서 검증되었습니다. 어느 이웃의 궤도가
  재설계된다면, 새 요소를 받아들이기 전에 안정성 시뮬레이션을 다시 돌려야
  합니다.
- **이심률 경계 메모.** DB reference 문자열은 "e ≤ 0.05" 라고 적지만,
  10⁵-년 적분은 c 의 이심률이 세속 강제 아래 ~0.095 까지 순환함을 보입니다
  (여전히 차분/안정). 접촉 설계값은 0.04 로 유지하되, 더 넓은 세속 포락선을
  정직성을 위해 여기 기록합니다.

## Related

- [40-eridani-a](40-eridani-a.md) — 호스트 별 Phase 3 (K0.5 V)
- [40-eridani-a-b](40-eridani-a-b.md) — 안쪽 이웃("Vulcan"/
  "Erid", documented divergence 로 유지된 철회 검출)
- [40-eridani-a-d](40-eridani-a-d.md) — 바깥 이웃(*Project Hail
  Mary* Threeworld 아날로그)
- [methodology](../reference/methodology.md) — Decisions 스키마 +
  무대기 열 영역
