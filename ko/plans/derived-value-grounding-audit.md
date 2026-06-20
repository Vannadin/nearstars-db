<!-- 도출값 논문 근거화 규칙의 소급 전수 감사 결과 (2026-06-20) — 수정 백로그 -->
# Derived-Value Grounding Audit (retroactive, 2026-06-20)

새로 도입된 도출값 method-grounding 규칙(`phase2/curation-data-contract/SPEC.md`의
"Derived astrophysical values")을 기존 작업 전체에 소급 적용한 전수 감사다. 방법은
method 단위 서브에이전트 3개(색 / 항성물리 / 궤도-구조) + 바디 단위 전수 커버리지
서브에이전트 4개(자이언트 자기장, 암석형 자기장, 항성풍 필드, 디스크 색)였다.

**핵심 결론.** 규율과 기계장치 자체는 대체로 건전하다. 교과서 closed-form은 면제 처리가
정확하고, 합성값 대부분은 실제 관계식을 인용하거나 솔직하게 low-confidence로 표기돼 있으며,
*조작된* 값은 하나도 없었다. 진짜 갭은 **가스자이언트/준항성급 자기장**과 **잔해 디스크 blend
색**에 몰려 있고, 여기에 별개의 **phantom-citation** 실패 모드가 더해진다. 항성풍 필드는 아직
cfg-emit되지 않으므로(Kerbalism writer 보류 중) 출처(provenance)만 갖춘 상태다.

---

## Resolution — RESOLVED 2026-06-20

모든 tier를 한 번에 수정했다. method grounding은 메인 스레드에서 처리했고, 기계적 적용과
ko 미러는 위임 후 검증했다(결정론적 재계산 + 인용된 모든 arXiv ID가 `_papers/`에 실재함을 확인).

- **1a 자이언트 (method gap).** **Reiners & Christensen 2010**(`1007.1514`, 에너지-플럭스
  dynamo 스케일링, Christensen et al. 2009 `2009Natur.457..167C` 기반)을 캐시했다.
  재사용 가능한 worked method를 `docs/reference/planetary-dynamo-scaling.md`(+ko)에 작성했다.
  `B_dip^pol = 9 G·(age/4.5 Gyr)^−0.33·(M/M_Jup)^0.93`. 논문 자체의 목성(9 G)·ε Eri b(19 G)
  행으로 검증했다. **진짜 자이언트** 3개를 선형 질량이 아니라 내부 광도 기반으로 재도출했다.
  **ε Eri b 400→660 µT**(젊으므로 목성보다 강함 — 부호가 거꾸로였다), **ε Ind A b 1000→3200 µT**,
  **GJ 896 A b 900→2000 µT**(+ dipole 행, 키 철자 정규화). **AU Mic b/c/e**는 ≥0.3 M_J 영역
  아래라 → 솔직한 ice-giant(해왕성/천왕성) analog로 재근거화하고, **phantom인 Yadav &
  Thorngren 2017을 제거**했다. **AU Mic d**(암석형) → RM22 `2203.01065`로 바꿔 자이언트 논문
  오인용을 제거했다. 스킬 `mod-grounded-fields.md`는 이제 바디 클래스별로 라우팅한다.
- **1b 디스크 blend (method gap).** `disk_color_mie.py`의 `ice_sil`/`sil_org`가 이제
  ε=(n+ik)²에 대한 **Maxwell-Garnett** effective-medium 혼합을 쓴다(부피 분율은 50/50 질량 +
  bulk 밀도에서). 지어낸 선형 n,k 평균을 대체했다. 방출된 tint를 갱신했다.
  ε Eri cold `#fffcfc→#fff5ef`, τ Cet `#ffe4bd→#ffe2bb`. AU Mic-blue / Fomalhaut-grey 검증은
  여전히 유효하다.
- **Tier 2.** Barnard dose. Atri(`1910.09871`) + France(`2009.01259`)를 핀했다(둘 다 실제로는
  캐시돼 있었다. 거짓 "not in cache"를 제거했다). HD 69830 c/d 자기장 신뢰도 medium/high→**low**.
  Barnard b/c/d/e dipole에 "Mercury analogy, not dynamo-modeled" 태그를 달았다. astrosphere
  v_wind=400 km/s + Wood 2002/2005를 각 사용처에 명기했다. q=3.5에 Dohnanyi 1969(`1969JGR....74.2531D`)
  인용. ρ=2.5는 플래그.
- **Tier 3.** τ Cet e/f의 "RM22 (Reiners-Christensen)"를 → "RM22 (Rodríguez-Mozos & Moya 2022,
  `2203.01065`)"로 de-conflate했다.

모든 ko 미러를 동기화하고 HTML을 재빌드했다. `check.sh`는 이 작업과 무관한 기존
data.json / docs-wiki 오탐을 빼면 clean이다.

### Re-sweep follow-up — RESOLVED 2026-06-20

위 작업 이후, 독립적인 clean-agent가 (자기장/디스크 *바깥*의) method gap을 찾는 재전수
감사를 한 번 더 돌렸고, 새로 추가된 인용 전부에 대해 two-prior 적대적 검증을 했다. 인용
검증에서는 두 에이전트(하나는 실재 가정, 하나는 phantom 가정)가 각각 독립적으로 인용된
논문이 모두 실재하며 모든 arXiv ID/bibcode가 주장된 논문으로 resolve됨을 확인했다 — 조작
없음. 원래 전수 감사가 놓친 method gap 4건을 추가로 근거화했다.

- **Radiogenic heat (`radiogenic_heat_w_m2`, 약 10개 바디).** 인용 없이 지구 analog로
  질량 스케일링돼 있었다(SPEC의 "paper/synth" 필드 → 계약 위반). Wang et al. 2020(`2020A&A...644A..19W`,
  Eu→Th/U radiogenic 진단)을 근거로 삼되, 호스트 abundance는 큐레이션하지 않았으므로 지구
  analog임을 명시했다. 신뢰도 → low. tau-cet-e/f/g/h, 61-vir-b, hd-219134-b/c, trappist-1-f/g/h.
- **Day-night / 온실 온도 델타 (약 8개 바디).** T_eq 위로 얹는 구체적 K offset이 이제 Cowan &
  Agol 2011(`1001.0012`)의 열 재순환 parameterization을 인용한다. hd-69830-b/c/d, au-mic-b/c/d/e
  (au-mic-b의 잘못된 "Plavchan §6" 온실 귀속을 제거했다). 40-eri-a-b 온실은 Asimov lore에서
  파생된 픽션으로 플래그했다(반증된 바디라 논문을 붙이지 않았다).
- **Energy-limited escape (au-mic c/e).** 이제 Lecavelier des Etangs 2007(`astro-ph/0609744`,
  캐시됨)을 인용하며, b의 Allart-2023-앵커값에서 스케일했다.
- **가스자이언트 반지름 (55 Cnc b/c/d/f).** 이제 Fortney, Marley & Barnes 2007(`astro-ph/0612671`)의
  warm-giant 질량-반지름-insolation 트랙을 인용한다.

코퍼스는 그 밖엔 clean이다(조석 가열, 질량-반지름, 안정성, 항성풍 모두 이미 근거화돼 있다).
값은 바뀌지 않았다. method 인용 + 신뢰도만 추가했다.

---

## How to attack — method-gap vs value-fix

대부분의 발견은 독립적인 바디별 오류가 아니라 **method gap**이다(근거 있는 method가 애초에
정의된 적이 없어 → 바디마다 즉흥적으로 처리됐다). method를 **한 번** 고친 뒤, 영향받은 바디를
일괄 재도출하면 된다. 자이언트 자기장 7개를 하나씩 고치는 건 이 사태를 일으킨 즉흥성을 그대로
재현할 뿐이다. 진짜 셀 단위 value-fix에 해당하는 항목은 몇 개뿐이다.

| Finding | Type | Fix shape |
|---|---|---|
| 1a giant B-fields + phantom-cite | **method gap** (no grounded giant-dynamo method, cf. rocky's RM22) | define + cache Christensen 2009 energy-flux scaling → re-derive 7 giants uniformly |
| 1b disk blends | **method gap** (code uses linear n,k average) | one code fix (Maxwell-Garnett) → eps Eri + tau Cet auto-correct |
| flare boost | **method gap** (no flare→dose relation) | define relation/policy → apply to 2 hosts |
| Dohnanyi q / grain ρ | **method gap** (uncited code constants) | cite once in the code |
| astrosphere v_wind=400 | doc/traceability | surface the assumption at each host |
| HD 69830 c/d confidence | **value fix** | 2 cells → low |
| Barnard dipoles | **value fix** | add anchor or "analogy" note, 4 cells |
| tau-cet label / code comment | value / hygiene | text cleanup |

**역할 분담.** **method grounding**(관계식 논문 정독, 캐시, 실제 자이언트로 calibration — J2
템플릿)은 판단의 핵심인 *동시에* phantom-citation 위험 구역이라, 메인 스레드에서 처리하거나
빡빡하게 검증하며, 절대 블라인드 위임하지 않는다. **기계적 적용**(바디별 재계산), **코드 수정**,
**value cleanup**은 서브에이전트에 위임한 뒤 **결정론적 재계산 + 인용된 모든 논문이 실제로
`_papers/` 캐시에 resolve되는지 확인**으로 검증한다(이것이 phantom-citation 가드다).

---

## The phantom-citation pattern (the most important systemic finding)

일부 도출값은 실제 논문 이름을 대지만 그 논문이 **`_papers/` 캐시와 bib YAML에 부재한다** —
back-of-envelope 추측을 grounded인 양 세탁하는 셈이다. 이는 솔직한 "no citation,
low-confidence" 표기보다 *더 나쁘고*, convergence 규칙(`bibcode` + `arxiv_id` + 캐시로 인용)도
위반한다. 확인된 사례. **Yadav & Thorngren 2017**(arXiv/bibcode 없음, 2026-06-03 감사에서 이미
uncacheable로 플래그됨)이 au-mic-b/c/e에서 인용됨. **Reiners & Christensen 2010**이 eps-eri-b와
au-mic-d에서 인용됐으나 이 repo 캐시엔 없음. 수정 = 실제 논문을 캐시하거나, 근거를 솔직하게 다시 쓴다.

---

## Tier 1 — real, cfg-emitting, fix needed

### 1a. Gas-giant / substellar magnetic field + dipole (gates aurora / radiation belts)

| Body | Value | Problem | Verdict |
|---|---|---|---|
| ε Eri b | 400 µT, dipole 13200× | linear-mass "scaled jovian"; cites Reiners&Christensen 2010 **not in cache** + physics contradicts (real dynamo scaling is energy-flux, not linear-mass) | AD-HOC + phantom-cite |
| GJ 896 A b | 900 µT | "scaled jovian, ~2× Jupiter" — **no citation** | AD-HOC |
| ε Ind A b | 1000 µT | "~2× Jupiter by mass/convection" — no citation (self-labels "aesthetic, no measurement" → partially mitigated) | AD-HOC (flagged) |
| AU Mic b | 100 µT | cites **Yadav & Thorngren 2017** (phantom — not in cache) | phantom-cite |
| AU Mic c | 50 µT | same phantom Yadav & Thorngren 2017 | phantom-cite |
| AU Mic d | 5 µT | cites **Reiners & Christensen 2010** (phantom — not in this report's biblio/cache) | phantom-cite |
| AU Mic e | 30 µT | same phantom Yadav & Thorngren 2017 | phantom-cite |

**수정.** 실제로 캐시된 dynamo 스케일링에 근거를 둔다 — **Christensen, Holzwarth & Reiners
2009**(에너지-플럭스 스케일링, `2009Natur.457..167C`) 또는 Reiners & Christensen 2010(제대로
캐시)을 써서 선형 질량이 아니라 에너지 플럭스에서 자기장을 재계산한다. 또는 솔직한
low-confidence analog로 강등한다(아래의 compliant 패턴). dipole moment는 *내부적으로*
일관됨에 유의(ε Eri 13200 = 0.66×20000). 즉 문제는 method이지 산술이 아니다.

**이미 compliant인 사례(솔직한 analog, 거짓 인용 없음 — 따라 할 패턴).**
α Cen A b / Polyphemus(500 µT, "Saturn-analog, no measurement", low), HD 69830 b
(Neptune-analog, low). **단 HD 69830 c/d**는 인용 없는 Neptune-analog 비율에 confidence를
medium/high로 표기 — `low`여야 한다(Tier 2).

### 1b. Debris-disk blend optical constants

`scripts/phase3/disk_color_mie.py`의 `ice_sil`과 `sil_org`는 **지어낸 값**이다 — 끝점들의 정확한
선형 n,k 평균이지(확인됨), effective-medium 이론(Maxwell-Garnett / Bruggeman)도 아니고 어떤
optical-constants 논문에서 온 것도 아니다. 이 둘이 방출된(low-conf 플래그된) tint 2개를 만든다.
**eps Eri cold ring**(`#fffcfc`)과 **tau Cet broad belt**(`#ffe4bd`). `ice_sil`은 Fomalhaut-grey
검증 앵커이기도 해서 → 검증이 다소 순환적이다. 단일 물질 5개(astrosil/carbon/ice/olivine/tholin)는
근거가 있다(Draine 2003, Warren & Brandt 2008, Jäger 2003, Khare 1984, Rouleau & Martin 1991).
문헌과 일관된다. **수정.** blend에 대해 ε=(n+ik)²에 Maxwell-Garnett 혼합을 적용하거나, 인용된
단일 물질을 택하거나, blend n,k를 명시적 가정으로 플래그한다.

---

## Tier 2 — mitigated / honest, polish at emit time

- **`stellar_radiation_surface`의 flare boost**(Proxima ~5 over quiescent ~0.3; Barnard
  ~0.1 over ~0.03). boost *크기*가 flare-energy→dose 스케일링을 인용하지 않는다. 완화됨 —
  quiescent-only 대안을 inline에 플래그, low–medium으로 사전 선언. **아직 cfg-emit 안 됨.**
  수정. SEP-fluence / flare-FFD→dose 관계식을 핀하거나, headline을 quiescent로 강등.
- **`astrosphere_standoff`의 v_wind = 400 km/s** 가정 + LIC-density 상쇄. spec/workspace
  수준엔 문서화돼 있으나 **사용처에서 재진술되지 않음**. "Wood" 출처가 unpinned.
  수정. 호스트당 한 줄 + wind-speed 출처 핀.
- **HD 69830 c/d 자기장 confidence 과장됨**(medium/high → 인용 없는 analog이므로 low여야 함).
- **Barnard b/c/d/e dipole.** 인용 없는 Mercury-analog 서수 추측, low로 플래그, 어느 것도
  Kerbalism을 구동하지 않음(belts off). RM22/Zuluaga 앵커 또는 명시적 "analogy, not modeled"
  노트를 추가.
- **디스크 `rho = 2.5 g/cc`와 `q = 3.5`** 하드코딩 + 인용 없음(a_min에 load-bearing). q=3.5는
  표준 Dohnanyi 1969 값 — 인용. rho는 플래그.

---

## Tier 3 — citation hygiene

- tau-cet-e/f 라벨 "RM22 (Reiners-Christensen)" — 서로 다른 두 논문을 뒤섞음(RM22 =
  Rodríguez-Mozos & Moya 2022, 이 값의 실제 출처. Reiners & Christensen 2010 = 별개의
  rotation-dynamo 법칙). 이름을 de-conflate한다.
- `disk_color_mie.py`의 주석 "50/50 mass-ish blends"는 엄밀함을 과장(실제론 가중치 없는 선형
  n,k 평균).
- Barnard `surface_radiation_dose`가 Atri 2020 / France 2020을 "context-cite, not in cache"로
  인용 — 솔직하지만 uncached.

---

## Confirmed grounded / exempt (the bulk — no action)

- **색 엔진.** Saha-Boltzmann LTE(Cristoforetti 2010 + NIST), CIE→sRGB(Wyman 2013),
  Mie 알고리즘(Bohren & Huffman, AU Mic blue / Fomalhaut grey로 검증), 분자 밴드(Huber &
  Herzberg + per-species 출처). Chromophore 카탈로그(교과서, veto-gated).
- **암석형 행성 자기장.** RM22(Rodríguez-Mozos & Moya 2022, `2203.01065`, 캐시됨)가 TRAPPIST-1
  패밀리를 담당. proxima-b(Zuluaga 2018), yz-cet-b(Trigilio 2023 측정), Wang 2025, Garraffo,
  Driscoll & Olson — 모두 근거 있음 또는 솔직한 low-conf.
- **Closed-form (면제).** T_eq / insolation / surface gravity / scale height(recompute-gate
  강제), Roche, Hill, Kepler, angular size, Planck, blowout radius, x=2πa/λ.
- **온실 온도.** 인용된 GCM에서(Boutle 2017, Del Genio 2019). 금성 벤치마크가 "T_eq는
  하한이다" 가드레일을 근거 짓는다.
- **aspect_ratio**(Boley 2012 / Daley 2019), **J2**(Radau–Darwin, Helled+2011,
  calibration-verified), **C22 = 0.3·J2**(hydrostatic, Galilean-verified).
- **Stability-sim 선택**(Barnard, α Cen, 위성). 건전한 integrator 정책(TRACE Lu+2024),
  태양계 self-validation, 문헌 cross-check(GH2024, Basant 2025, Domingos+2006).
- **항성풍 입력**(질량손실 Wood, L_X Wargelin/France, rotation/activity) — Phase 2 측정 + 인용.
- **Phase 4 art-direction**(Pandora +70 K 온실, Hades e, synthetic-noise e≲0.05). art-direction
  / documented-limitation으로 플래그, 아직 emit 안 함.

---

## Recommended fix order

1. **자이언트/준항성급 자기장 (1a)** — 임팩트 최고(emit + aurora/belts gate)이자 phantom-citation의
   핵심. 바디별로 Christensen 2009 / Reiners 2010(캐시)에 근거를 두거나, 솔직한 analog로 강등.
   ~7개 바디 + dynamo 논문 캐시.
2. **디스크 blend (1b)** — emit된 tint 2개. Maxwell-Garnett 또는 단일 물질 또는 플래그.
3. **Tier 2 polish** — flare-boost grounding, v_wind 사용처, HD 69830 c/d confidence,
   Barnard dipole 앵커, Dohnanyi/rho 인용.
4. **Tier 3 hygiene** — 라벨/주석 cleanup.

각 수정은 J2 템플릿을 따른다. method 논문 정독(캐시), 재계산, 인용 + 가정 + 불확실성과 함께 기록.
