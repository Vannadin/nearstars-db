<!-- 40 Eridani A b Phase 3 합성. 철회된("Vulcan"/"Erid") 검출을 프로젝트 결정에 따라 documented divergence 로 재등재 -->
# 40 Eridani A b — Phase 3 Synthesis (Refuted — included as documented divergence)

40 Eridani A b 는 발표된 모든 철회 외계행성 중 문화적으로 가장 유명한
천체입니다. 이 별은 *Star Trek* 의 Spock 의 고향 행성 **Vulcan**
이며 — Gene Roddenberry 가 1991 년 *Sky & Telescope* 에 보낸 편지(Sallie
Baliunas 와 동료들이 공동 서명)가 Epsilon Eridani 대신 40 Eridani A 를
캐넌으로 확정했습니다 — 동시에 Andy Weir 의 *Project Hail Mary* (2021)
에서 외계인 Rocky 의 고향 행성 **Erid** 이기도 합니다. 다른 어떤 철회
검출도 이만한 문화적 무게를 지니지 못하며, 바로 그 점이 이 천체가
NearStars 데이터베이스에 남아 있는 유일한 이유입니다.

이 후보는 Ma et al. 2018 (`2018AJ....155..117M`, Dharma Planet Survey
RV 프로그램)이 40 Eridani 삼중계의 K0.5 V 주성 주위에서 M sin i ≈ 8.47
M⊕, P = 42.245 일 주기, a = 0.224 AU 의 super-Earth 로 발표한 것입니다.
40 Eri 는 5.0 pc 거리의 실재하는 인근 카탈로그 시스템으로, beyond-50-ly
대상이 **아닙니다** — 맨눈으로 보이는 가장 가까운 별 중 하나입니다. 모성은
Teff 5143 K, L = 0.408 L☉, M = 0.78 M☉ 의 K0.5 V 왜성으로, 이 후보를
거주 가능 영역 안쪽 가장자리보다 훨씬 안쪽에 둡니다 — 평형 온도가
Teq(A=0.3) = 430 K, Teq(A=0) = 470 K 인 *뜨거운* super-Earth 입니다.

**이 검출은 Burrows et al. 2024 와 Lubin et al. 2024 가 철회했습니다.**
16 년에 걸친 다중기기 RV 기준선은 42 일 신호가 Keplerian 행성이 아니라
별의 자전 주기임을 보였습니다 — 40 Eri A 호스트 합성이 가짜 "Vulcan"
신호로 다루는 바로 그 활동성 기인 주기성입니다. 따라서 canonical 판독은
*행성 없음* 입니다.

**프로젝트 결정에 따라 b 는** 예외적인 문화적 무게(*Star Trek* 의 Vulcan +
*Project Hail Mary* 의 Erid) 때문에, 철회 이전 Ma 2018 값으로 반박표기
documented divergence 로서 `db/systems/40_eridani.json::planets[]` 에
**재등재**됩니다. 아래의 모든 행은 `disposition` 행을 제외하고 Confidence=low
인데, 근거 신호 자체가 이제는 아티팩트로 간주되기 때문입니다. 철회 사실은
합성된 천체 뒤에 숨기지 않고 문서 전반에 걸쳐 분명하게 드러냅니다.

**NearStars 시나리오 선택: 뜨거운(~430–500 K), 붉은빛, 고중력(~2.3 g)
의 암석-철 super-Earth — 철회 이전 Ma 2018 질량·궤도로 documented
divergence 로서 합성되며, 주황색 K0.5 V 주성 아래 녹슨 현무암 Vulcan
사막으로 렌더링됩니다.** interesting-first 판독은 높은 표면 중력으로 두꺼운
헤이즈 대기를 붙잡은 치밀한 암석 행성입니다. canonical 판독은 여전히 행성
없음입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | Refuted (Burrows/Lubin 2024) | high | 42 일 신호 = 항성 자전, Keplerian 아님. 다중기기 16 년 RV. 이 표에서 유일한 high-confidence 행 |
| `mass_mearth` | 8.47 (M sin i; true mass ≥ this) | low | Ma 2018 RV. 신호 철회됨 |
| `radius_rearth` | ~1.9 | low | tie-break / interesting-first: 암석-철 8.5 M⊕ super-Earth 의 mass–radius (≈ Weir 의 Erid 2.01 R⊕). RV 전용, 측정된 적 없음 |
| `density_g_cc` | ~6.8 | low | 유도 M/R³ — 암석-금속, 지구보다 치밀 |
| `surface_gravity_g_earth` | ~2.35 | low | 유도 8.47/1.9² (≈ Erid 의 2.09 g) |
| `equilibrium_temp_k` (A=0.3) | 430 | low | 유도. (A=0) 470 |
| `insolation_s_earth` | ~8.1 | low | 유도 0.408 L☉ / (0.224 AU)² — 뜨거움, HZ 안쪽 가장자리보다 훨씬 안쪽 |
| `surface_temp_k` | ~450–500 | low | tie-break: 기본 Teq + 적당한 온실효과. Erid lore 는 표면을 210 °C ≈ 483 K 로 둠 |
| `bond_albedo` | 0.20 | low | tie-break: 어두운 헤이즈 / 현무암 |
| `tidally_locked` | false | low | a = 0.224 AU, 0.78 M☉ 주위 → 조석 고정 시간 척도가 긺. interesting-first 는 자전체를 택함 (Erid 의 빠른 자전) |
| `rotation_period_h` | ~5–10 (fast) | low | tie-break + Erid lore (5.1 h 빠른 자전체 → 강한 다이나모). 철회된 천체에는 의미 없음 |
| `atmosphere_composition` | thick CO₂/N₂ with high-altitude haze | low | tie-break: 축퇴. interesting-first — 높은 중력이 이 Teq 에서 두꺼운 대기를 붙잡음 |
| `atmosphere_surface_pressure_pa` | ~1×10⁶ (≈10 bar) | low | tie-break: interesting-first 두꺼운 대기 |
| `surface_tint_rgb_hex` | `#b5603a` (rusty basaltic-orange desert) | medium | tie-break: interesting-first + Vulcan 의 상징적인 붉은 사막. 뜨거운 암석 표면의 산화철 / 현무암 |
| `sky_tint_rgb_hex` | `#c98a5a` (dusty orange) | low | tie-break: K0.5 V (5143 K) 빛 아래 두꺼운 헤이즈 대기 |

## Surface synthesis

철회 이전 Ma 2018 의 그림에서 b 는 ~8.1 S⊕ 에 자리잡고 있었습니다 — K0.5
V 호스트의 거주 가능 영역 안쪽 가장자리보다 훨씬 안쪽으로, A = 0.3 bond
albedo 아래 평형 온도 430 K(제로 알베도에서 470 K)를 줍니다. 이것은
온대가 아니라 명백히 *뜨거운* super-Earth 입니다. Vulcan 픽션은 발견보다
앞서 지구를 닮은 사막 행성을 가정했지만, 실제 궤도 기하는 b 를 얇은 대기의
물 안정성 한계를 한참 넘어선 뜨거운-암석 영역에 둡니다.

**interesting-first 판독은 치밀한 암석-철 super-Earth 입니다.** 8.47 M⊕
(M sin i) 와 tie-break 반지름 ~1.9 R⊕ — Weir 의 Erid 2.01 R⊕ 와 거의
일치 — 로, 이 천체는 유도 밀도 ~6.8 g/cc, 표면 중력 ~2.35 g 의 암석-금속체이며,
Erid 가 제시한 2.09 g 에 매우 가깝습니다. 이 중 어떤 값도 측정된 적이
없습니다. 검출은 RV 전용이고 신호도 이제 철회되었기에, 반지름·밀도·중력은
관측이 아니라 tie-break 반지름에서 모두 cascade 합니다.

**색 선택 — 녹슨 현무암 Vulcan 사막.** 일차 표면 색조 `#b5603a` 는
뜨거운 산화철 / 현무암 사막을 인코딩하며, 시각 행 중 유일하게
중간(medium) 신뢰도를 갖는데 그 이유가 중첩되어 있기 때문입니다 — 뜨거운
암석 표면에 대한 데이터 기반 판독인 동시에 *Star Trek* 의 Vulcan 의
상징적인 붉은 사막에 대한 직접적인 오마주입니다. 이 판독에서 표면 온도는
~450–500 K 로, 기본 Teq 에 두꺼운 대기의 적당한 온실 기여를 더한 값이며,
이는 Erid lore 가 제시한 210 °C(≈ 483 K) 표면과 들어맞습니다.

**철회 맥락.** 42.245 일의 Ma 2018 신호는 Keplerian 행성이 아니라 40
Eridani A 의 자전 주기였음이 드러났습니다. Burrows et al. 2024 는 NEID
line-by-line 활동성 진단과 16 년 다중기기 RV 기준선을 사용해 이 주기성이
반사 궤도가 아니라 채층 활동을 따른다는 것을 보였고, Lubin et al. 2024 는
독립적으로 같은 결론에 도달했습니다. 이는 40 Eri A 호스트 합성에 기록된
바로 그 ~42 일 자전 변조이며, disposition 을 Refuted 로 확정짓습니다.

## Atmosphere synthesis

대기는 완전히 축퇴되어 있습니다. 검출은 RV 전용이었고 — 통과도, 투과
스펙트럼도, 직접 촬영도 없었습니다 — 따라서 대기에 관해 관측된 것은
아무것도 없으며, 천체 자체가 철회되었습니다. 합성은 interesting-first
판독을 채택하고 문화적 판독들을 명시적인 대안으로 펼쳐 둡니다.

**압력과 조성 — interesting-first 두꺼운 대기.** ~2.35 g 의 표면 중력에서
b 는 같은 Teq 의 저질량 천체보다 두꺼운 대기를 훨씬 쉽게 붙잡으므로, cfg 는
~1×10⁶ Pa(≈10 bar)의 고고도 헤이즈를 동반한 두꺼운 CO₂/N₂ 외피를
채택합니다. 이는 tie-break 입니다 — 높은 중력은 보유에 유리하고, 헤이즈는
Bond albedo 를 0.20 으로 어둡게 하며, 적당한 온실효과는 표면을 맨평형
온도 위 450–500 K 범위로 끌어올립니다.

**대안으로서의 문화적 판독.** 픽션은 데이터와도, 그리고 서로와도 크게
갈라집니다. *Star Trek* 의 Vulcan 은 붉은 사막 하늘을 가진 얇은 대기의
행성입니다 — 전형적인 뜨거운 사막 고향 행성입니다. *Project Hail Mary*
의 Weir 의 Erid 는 정반대 극단으로, 210 °C 에서 두꺼운 ~28 atm NH₃ 대기를
가지며, Eridian 들은 그 짙은 헤이즈 아래 거의 완전한 어둠 속에서 눈 없이
진화했습니다(소설에서 표면은 사실상 빛이 없습니다). cfg 의
interesting-first 선택은 그 둘 사이에 있습니다 — 두껍고 헤이즈 끼고 뜨거운
대기이지만, NH₃ 특정 값이 데이터 기반이 아니라 만들어낸 worldbuilding
선택이기에 Erid 의 NH₃ 가 아니라 CO₂/N₂ 입니다.

**2026 년 *Project Hail Mary* 영화의 짙은 파란 대기는 픽션입니다.** 영화는
Erid 를 짙은 파란 대기로 묘사합니다 — Weir 의 무색 NH₃ worldbuilding 과
데이터 기반 뜨거운-붉은 판독 모두에 어긋나는 미술 연출 선택입니다. 이는
cfg 값으로 채택되지 **않습니다**. 먼지 낀 주황색 `sky_tint_rgb_hex`
`#c98a5a` 가 K0.5 V (5143 K) 주성 아래의 데이터 기반 하늘 색이며, 영화의
파란색은 `docs/reference/cultural-context.md § 40 Eridani A` 에만
기록됩니다.

**손실 맥락.** 철회된 천체에는 어떤 손실 계산도 의미가 없습니다. 정성적
요점은 단지 높은 중력이 interesting-first 시나리오에서 두꺼운 대기를
*그럴듯하게* 만든다는 것뿐입니다 — 행성이 없으므로 실제 보유 문제는 의미가
없습니다.

## Rotation & spin synthesis

b 가 존재했다면 **조석 고정되지 않았을** 것입니다. a = 0.224 AU, 0.78 M☉
호스트 주위에서 조석 고정 시간 척도는 깁니다 — 근접 M 왜성 행성보다 훨씬
길어서 — 따라서 원시 자전이 살아남고, 천체는 동기 자전체가 아니라 자유
자전체가 됩니다. 이 궤도 거리에서는 자전 감쇠가 작동할 시간이 없었습니다.

**interesting-first 빠른 자전체.** cfg 는 Erid 의 lore 값인 5.1 h 항성일에
맞춰 ~5–10 h 의 빠른 자전 주기를 채택합니다. Weir 의 worldbuilding 에서
빠른 자전은 두꺼운 암모니아 대기를 붙잡는 데 필요한 Erid 의 강한
다이나모(지구의 ≈ 25 배 자기장)를 구동하는 요인입니다. interesting-first
선택은 NH₃ 특정 자기장 세기 없이 빠른 자전체만 차용합니다.

**철회된 천체에는 의미 없음.** 자전 주기, 고정 상태, 다이나모는 모두
제약되지 않으며 궁극적으로 의미가 없습니다. 42 일 RV 신호가 곧 호스트의
자전이기 때문입니다 — 측정할 행성 자전이 없습니다. 빠른 자전체 값은 물리적
추론이 아니라 문화적 플레이버 tie-break 입니다.

## Visual styling

이 섹션은 행성을 "존재하는 대로"가 아니라(존재하지 않으므로)
"documented divergence 로서 렌더링된다면"의 관점에서 다룹니다.

- **전체 외관 (interesting-first).** 뜨겁고 붉은빛이 도는 고중력
  super-Earth — 주황색 K0.5 V 주성이 비추는, 먼지 낀 주황색 헤이즈 하늘
  (`#c98a5a`) 아래의 녹슨 현무암-주황 사막(`#b5603a`)입니다. 시각적
  성격은 더 뜨겁고 더 치밀하며 산화철로 더 짙게 물든, 두꺼운 헤이즈층에
  싸인 화성 톤 행성에 가장 가깝습니다.
- **대기 헤이즈 (interesting-first).** 두꺼운 ~10 bar 헤이즈 외피는
  무대기 천체의 날카로운 명암 경계 대신 부드러운 먼지 주황 림과 옅은 표면
  대비를 줍니다. 높은 중력이 척도 높이를 압축하므로 헤이즈는 짙은 저층으로
  깔립니다.
- **하늘의 동반체 — 40 Eri 삼중계.** b 의 표면에서 멀리 떨어진 백색왜성
  40 Eri B 와 적색왜성 플레어별 40 Eri C 는 하늘에서 눈부신 점으로 보입니다
  (B–C 쌍은 ~400 AU 에서 A 주성을 공전합니다). K0.5 V 주성의 주황색 낮빛
  아래 펼쳐지는 독특한 삼중계 하늘 풍경입니다.
- **영화 픽션은 명시적으로 배제.** 2026 년 *Project Hail Mary* 영화의 짙은
  파란 대기와 고리계는 **픽션**이며 cfg 에 렌더링되지 **않습니다**. cfg 는
  데이터 기반 뜨거운-붉은 판독(녹슨 사막, 먼지 주황 헤이즈 하늘)을
  사용하며, 영화의 파란 대기와 고리는 `docs/reference/cultural-context.md
  § 40 Eridani A` 에만 기록됩니다.
- **"Vulcan / Erid" 문화 교차참조.** 이 Phase 3 마크다운은 합성 + 문화
  교차참조의 본거지로, `docs/reference/cultural-context.md § 40 Eridani A`
  와 짝을 이룹니다. 프로젝트 결정에 따라 NearStars 는 b 를 documented
  divergence 로 포함하며 — 철회된 신호에도 불구하고 interesting-first
  판독으로 렌더링됩니다(canonical = 행성 없음).

## Canonical alternatives

**canonical 판독은 행성 없음입니다.** 42 일 신호는 Keplerian 궤도가 아니라
40 Eridani A 의 자전 주기(Burrows/Lubin 2024)이며, 현대 카탈로그는 이
주기에 확정된 행성을 싣지 않습니다. cfg 는 예외적인 문화적 무게 때문에
오로지 documented divergence 로서 합성된 천체를 포함합니다. 아래 표는 세
문화적 판독을 cfg 의 interesting-first 선택과 대조해 펼칩니다.

| Reading | Atmosphere | Surface / appearance | Status |
|---|---|---|---|
| *Star Trek* Vulcan | thin atmosphere | red desert sky, hot desert homeworld | fiction (predates discovery) |
| Weir's Erid (*Project Hail Mary*) | thick ~28 atm NH₃, 210 °C | dark — Eridians evolved blind in near-total darkness | fiction (worldbuilding) |
| *Project Hail Mary* 2026 film | deep-blue atmosphere | ring system | fiction (art direction — **not** in cfg) |
| **cfg interesting-first pick** | thick CO₂/N₂ + high-altitude haze (~10 bar) | hot reddish basaltic desert, dusty-orange hazy sky | documented divergence (canonical = no planet) |

## Bibliography

### Read (discovery + refutation)

- **Ma B. et al. 2018** — *The First Super-Earth Detection from the
  High Cadence and High Radial Velocity Precision Dharma Planet
  Survey* (`2018AJ....155..117M`). 발견 논문. b 를 K0.5 V 주성 주위
  P = 42.245 d, M sin i ≈ 8.47 M⊕, a ≈ 0.224 AU 로 보고합니다. 위
  철회 이전 Decisions 행들을 고정합니다.
- **Burrows R. et al. 2024** — *The Death of Vulcan: NEID Reveals
  the Planet Candidate Orbiting HD 26965 Is Stellar Activity*
  (철회). 다중기기 16 년 RV 기준선에 걸친 NEID line-by-line 활동성
  진단이 42 일 신호가 Keplerian 반사 궤도가 아니라 40 Eridani A 의 항성
  자전을 따른다는 것을 보입니다. Refuted disposition 을 구동합니다.
- **Lubin J. et al. 2024** — *Stellar Activity and the 42-day Signal
  of HD 26965* (독립 철회). Burrows 2024 와 같은 부정적 결론에
  도달합니다 — 신호는 행성이 아니라 자전 활동입니다.

### Read (cultural cross-reference)

- **Roddenberry G. & Baliunas S. et al. 1991** — *Sky & Telescope*
  에 보낸 편지로, 40 Eridani A 를(Epsilon Eridani 대신) Spock 의 고향
  행성 Vulcan 의 *Star Trek* 캐넌 위치로 확정합니다. 이 시스템의 가장
  두드러진 문화적 앵커입니다. `docs/reference/cultural-context.md § 40
  Eridani A` 에 기록되어 있습니다.
- **Weir A. 2021** — *Project Hail Mary* (소설). 40 Eridani A 의 행성을
  외계인 Rocky 의 고향 Erid 으로 명명합니다. Weir 의 worldbuilding 동반
  문서는 Erid 에 28 atm NH₃, 210 °C, 2.09 g, 5.1 h 항성일, Ma 2018 측정
  질량 8.47 M⊕ 에서 지구의 ≈ 25 배 자기장을 부여합니다. 소설은 2024 년
  철회보다 앞섭니다.

### Not read — superseded or low-priority

- **각종 거주가능성 / Vulcan 대중과학 다룸 (2018–2024)** — 철회 이전에
  쓰인 Ma 2018 후보 평가들. Refuted disposition 아래에서 cfg 관련성
  없음.
- **Dharma Planet Survey 기기 논문들** — EXPRES/DPS RV 파이프라인을
  서술하며 40 Eri 를 관측 대상으로만 언급합니다. 시각적 관련성 없음.

## Open items for follow-up

- **철회됨 — 실재 행성 없음.** disposition 은 확정되었습니다. 42 일 신호는
  항성 자전입니다(Burrows/Lubin 2024). b 를 재승격할 향후 후속은 예상되지
  않습니다. 합성된 천체는 문화적 무게를 위한 documented divergence 로서만
  cfg 에 존재합니다.
- **반지름 / 밀도 / 대기 / 자전이 모두 tie-break.** 검출은 RV 전용입니다 —
  반지름을 제약한 통과가 없었으므로, ~1.9 R⊕ 반지름과 유도된
  `density_g_cc`, `surface_gravity_g_earth` 가 모두 단일 tie-break 선택에서
  cascade 합니다. 측정된 반지름이 있다면 셋을 함께 갱신하겠지만, 기하학적으로
  통과가 기대되지 않고 신호도 철회되었습니다.
- **진질량 ≥ M sin i.** Ma 2018 질량은 시선속도 최소값입니다. 진질량은
  아래로 8.47 M⊕ 에 의해 경계지어지지만 위로는 제약되지 않으며, 신호가
  행성성이 아니므로 의미가 없습니다.
- **cultural-context 교차참조가 canonical 본거지.** 향후 "Vulcan / Erid"
  렌더링은 cfg 천체를 실재 검출처럼 다루는 대신
  `docs/reference/cultural-context.md § 40 Eridani A` 를 참조해야 합니다.
  영화의 짙은 파란 대기 + 고리는 픽션이며 그 문서에만 존재합니다.

## Related

- [40-eridani-a](40-eridani-a.md) — host star Phase 3 (K0.5 V;
  Vulcan 으로 위장했던 42 일 자전)
- [tau-cet-e](tau-cet-e.md) — sibling *Project Hail Mary* world
  (Adrian). 또 하나의 철회된 PHM-문화 documented divergence
- [cultural-context](../reference/cultural-context.md) — § 40
  Eridani A, *Star Trek* 의 Vulcan + *Project Hail Mary* 의 Erid
- [methodology](../reference/methodology.md) — Decisions schema
