# REX vs NearStars 데이터 비교

> 출처. Real Exoplanets mod v0.9.6 (커밋
> [`e32c0ab`](https://github.com/andikisare/Real-Exoplanets/commit/e32c0abcbdf87fdd0f2de42165b23a16d2346afa),
> 2020-04-11) 을 NearStars `db/systems/` 의 recommended 값 (기준일
> 2026-05-21) 과 비교.
> 목적. NearStars README가 spiritual predecessor 로 언급하는 REX (KSP
> 1.8.0 시대) 와 NearStars 사이의 격차를 정량화. 커버리지, 수치값,
> 다성계 토폴로지, 출처. DB 변경 없음 — 발견 사항만 기록.

---

## 한 줄 요약

> **커버리지 갭 없음.** REX의 5개 시스템 전부 우리 DB에 이미 있음.
> REX-only 별/행성 0개.

> **행성 목록 3개가 REX에서 구버전.** Barnard b(Ribas 2018)은
> retracted, Proxima c는 disputed, Teegarden d는 REX 동결 후 발견.
> NearStars는 post-2020 보정 반영.

> **REX는 하이어라키컬 다성계 불가능.** Proxima를 Sun을 도는 단일
> Body로 인코딩. NearStars는 Jacobi 분해 + ICRF Cartesian으로 Principia
> n-body 호환. 이게 NearStars가 REX 패치가 아니라 별도 프로젝트로
> 존재하는 구조적 이유.

> **별 값은 동시대 출처일 때 일치.** 3개 항목만 ≥10% 차이 (Barnard
> 질량, Teegarden 질량, Teegarden T_eff). 모두 REX가 2020-04 동결인
> 탓이고 NS 쪽이 더 최신.

---

## 배경

NearStars README는 "spiritual successor to REX (KSP 1.8.0 era)" 라고만 명시할 뿐 정량 비교는 없음. 이 문서가 그 갭을 메움 — 커버리지, 수치값, 다성계 토폴로지, 출처.

**범위.** REX `v0.9.6`, upstream commit
[`e32c0ab`](https://github.com/andikisare/Real-Exoplanets/commit/e32c0abcbdf87fdd0f2de42165b23a16d2346afa)
(2020-04-11). NearStars 측은 `db/systems/` 의 recommended 값, 기준일
`2026-05-21`. DB 변경 없음.

**외부 참조.**

- REX repo: <https://github.com/andikisare/Real-Exoplanets>
- REX SpaceDock: <https://spacedock.info/mod/2286/Real%20Exoplanets>
- REX KSP Forum:
  <https://forum.kerbalspaceprogram.com/topic/187033-181-real-exoplanets-v096-04032020/>
- NASA Exoplanet Archive: <https://exoplanetarchive.ipac.caltech.edu/>
- 라이선스 — REX README는 "All Rights Reserved", SpaceDock은
  CC-BY-NC-SA. 두 표기 충돌. 재사용 시 ARR로 간주.

---

## 1. 한눈에 비교

| | REX v0.9.6 | NearStars 2026-05 |
|---|---|---|
| **커버리지** | 5 시스템 / 8 별 / 15 행성 | ~50 시스템 / 152 컴포넌트 |
| **마지막 업데이트** | 2020-04-11 (동결) | active |
| **다성계** | Kopernicus barycenter `Body`, flat | Jacobi (`primary_is_barycenter_of`), ICRF Cartesian |
| **좌표계** | KSP equatorial (Space Engine 경유) | ICRF / J2000 |
| **솔버** | 없음 — Kopernicus 런타임 렌더링 | Markley non-iterative cubic, offline |
| **출처** | cfg 내 prose 주석 | per-measurement `bibcode` + `doi` |
| **에포크** | KSP 게임시간 초, origin 불분명 | 명시적 JD (B1950 = JD 2433282.5) |

---

## 2. 커버리지

### REX 시스템

| 시스템 | 별 | 행성 |
|---|---|---|
| Alpha Centauri | A, B, Proxima (+ barycenter Body) | Proxima b, c |
| Barnard's Star | Barnard | b (0.40 AU) |
| Tau Ceti | Tau Ceti | e, f, g, h |
| TRAPPIST-1 | TRAPPIST-1 | b, c, d, e, f, g, h |
| Teegarden's Star | Teegarden | b, c |

### 겹치는 부분

REX 5 시스템과 NearStars 파일의 매핑.

- `alpha_centauri_a.json`, `alpha_centauri_b.json`, `proxima_cen.json`
- `barnards_star.json`
- `tau_cet.json`
- `trappist_1.json`
- `teegardens_star.json`

> **REX-only 별 0개.** REX는 2020 이후 다섯 시스템에서 확장한 적 없음.

NearStars는 그 외에 ~45 시스템 추가 — 36 Oph, 40 Eri, 47 UMa, 55 Cnc,
61 Cyg, 61 Vir, 70 Oph, Altair, Arcturus, AU Mic, Sirius, Fomalhaut,
Eps Eri, Eps Ind, Eta Cas, 그리고 GJ 계열 다수와 implementation
shortlist.

---

## 3. 별 파라미터

REX cfg 값은 `M_⊙ = 1.989e30 kg`, `R_⊙ = 6.957e8 m` 로 변환. REX의
T_eff는 `Atmosphere.temperatureSeaLevel` 에서 읽음 — Kopernicus가 별
body의 "표면 온도"를 그 필드로 인코딩하고, REX가 실제로 이렇게
인코딩함.

### 질량 (M_⊙)

| 별 | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 1.100 | **1.1055** | −0.5% |
| α Cen B | 0.907 | **0.9373** | −3.2% |
| Proxima | 0.123 | **0.1221** | +0.7% |
| Barnard | 0.144 | **0.161** | **−10.5%** ⚠ |
| Tau Ceti | 0.793 | **0.783** | +1.3% |
| TRAPPIST-1 | 0.089 | **0.0898** | −0.9% |
| Teegarden | 0.080 | **0.097** | **−17.5%** ⚠ |

### 반지름 (R_⊙)

| 별 | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 1.227 | **1.2234** | +0.3% |
| α Cen B | 0.865 | **0.8632** | +0.2% |
| Proxima | 0.141 | **0.141** | 0% |
| Barnard | 0.196 | **0.1868** | +4.9% |
| Tau Ceti | 0.793 | **null** | n/a |
| TRAPPIST-1 | 0.121 | **0.1192** | +1.5% |
| Teegarden | 0.127 | **0.12** | +5.8% |

### 유효온도 T_eff (K)

| 별 | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 5790 | **5790** | — |
| α Cen B | 5260 | **5260** | — |
| Proxima | 3042 | **3498** | **−13.0%** ⚠ |
| Barnard | 3134 | **3278** | −4.4% |
| Tau Ceti | 5344 | **5320** | +0.5% |
| TRAPPIST-1 | 2511 | **2566** | −2.1% |
| Teegarden | 2637 | **3034** | **−13.1%** ⚠ |

### ≥10% 차이 항목

> **Barnard 질량 −10.5%.** REX는 Mann 2015 이전 값. NS가 최신.

> **Teegarden 질량 −17.5%.** REX는 CARMENES (Zechmeister 2019,
> Dreizler 2024) 이전. NS가 최신.

> **Proxima T_eff −13%.** REX 3042 K는 Boyajian 2012 간섭계 값. NS의
> 3498 K는 Suárez Mascareño 2025 — 출판된 범위(2900–3500 K)의 상단.
> 어느 보정을 신뢰할지 재검토 가치 있음.

> **Teegarden T_eff −13%.** REX 값은 최신 M 왜성 T_eff 보정 이전. NS가
> 최신.

---

## 4. α Centauri AB 궤도

| 요소 | REX | NearStars |
|---|---|---|
| P (yr) | 79.92 | **79.91 ± 0.01** |
| e | 0.5179 | **0.5179 ± 0.0003** |
| a (AU) | 23.52 | 23.46 |
| i (°) | 234.5 (KSP equatorial) | 79.205 ± 0.05 (ICRF) |
| Ω (°) | 190.486 | 204.85 ± 0.08 |
| ω_A (°) | −17.143 | 231.65 ± 0.08 |
| Epoch | KSP seconds | T_jd_tt = 2435035.7 (= 1954.8) |
| Source | "Space Engine" (cfg 주석) | Pourbaix & Correia 2017 / Kervella 2016 |

> **형태(P, e, a)는 0.01% 이내 일치.** 둘 다 Pourbaix 2002/2017 해를
> 인코딩. 회전각만 frame 차이 (REX = KSP equatorial, NS = ICRF) — 같은
> 물리 궤도를 다른 좌표계로 표현.

**질량비 sanity check.** a_A / a_B 비율에서 추출한 REX의 M_A / M_B =
1.184, 명시 질량에서 나온 NS의 1.179. 사실상 동일.

---

## 5. α Cen AB ↔ Proxima 토폴로지

REX와 NearStars의 가장 본질적인 방법론 차이.

### REX

- Proxima가 **Sun** 을 직접 공전. `mode = 0`,
  `semiMajorAxis = 4.015e16 m` (= 4.24 ly),
  `period = 1.061e13 s` (= 336,000 yr — non-bound 별의 "공전"은 물리적
  의미 없는 임의 값).
- α Cen AB barycenter 도 같은 방식으로 Sun을 공전.
- Proxima와 AB 사이 **하이어라키컬 binding 없음**.

### NearStars

`alpha_centauri_a.json::binary_orbit` 에 `hierarchy = "triple"` 선언,
궤도 2개.

- **AB**(내부) — ORB6 grade 1, 완전한 Kepler 요소.
- **AB-Proxima**(외부) — P = 547,000 yr, e = 0.5, a = 8,700 AU,
  i = 107.6°, 출처 Kervella 2017,
  `primary_is_barycenter_of = ["Alpha Centauri A", "Alpha Centauri B"]`.
  Periastron 에포크 미제약 → `phase_reliable = false`. 빌드
  파이프라인이 Kepler 합성을 건너뛰고 JD 2433282.5 에서 Proxima 위치는
  Gaia DR3 astrometry 직접 사용. Schema-level 그룹화로 향후 Gaia DR4
  NSS 해가 들어올 자리는 미리 마련됨.

> **REX가 이걸 못 하는 이유.** Kopernicus 궤도는 순수
> Keplerian-around-parent — n-body 도 Jacobi 도 없음. NearStars가 ICRF
> Cartesian state를 Principia로 export 하는 게 정확히 이걸 우회하기
> 위함. **NearStars가 REX 패치가 아니라 별도 프로젝트로 존재하는 구조적
> 이유.**

Stellarium 까지 포함한 3-way 비교는
`docs/reference/stellarium-binary-orbit-comparison.md` (승격되면) 또는
`plans/stellarium-binary-orbit-comparison.md` 참조 — Stellarium도
하이어라키컬 다성계는 미지원이지만 NS의 Hilditch 회전 규약은 일치.

---

## 6. 행성 목록

### Proxima Cen

| | REX | NearStars |
|---|---|---|
| 행성 | **b, c** | **b, d** |
| b (a/e) | 0.0480 AU / e=0.21 | 0.04848 AU / e=0.0 |
| 출처 (b) | Anglada-Escudé 2016 | Suárez Mascareño 2025 |
| 그 외 | c at 1.480 AU (Damasso 2020, disputed) | d at 0.02881 AU (Faria 2022) |

### Barnard

| | REX | NearStars |
|---|---|---|
| 행성 | **b 하나** | **d, b, c, e** |
| b (a/질량) | 0.404 AU / 3.75 M_⊕ | 0.0229 AU / 0.30 M_⊕ Msini |
| 출처 | Ribas 2018 | González Hernández 2024 / Basant 2025 |

> **REX의 Barnard b는 retracted.** Lubin et al. 2021이 stellar activity
> artifact 임을 보임. 이후 ESPRESSO 서베이가 0.02–0.04 AU 의 다른
> 4-planet sub-Earth 시스템을 발견. REX 값 obsolete.

### Tau Ceti

| | REX | NearStars |
|---|---|---|
| 행성 | **e, f, g, h** | **f, g, h** (e 없음) |
| 출처 | Feng 2017 | Feng 2017, `pl_controv_flag=1` |

> **NS는 Tau Ceti e 누락.** 같은 출처 논문, 같은 dispute flag. 의도적
> curation 가능성 높지만 (e가 4개 중 가장 disputed) 미확인. → open
> question.

### TRAPPIST-1

| | REX | NearStars |
|---|---|---|
| 행성 | **b–h** (7개) | **b–h** (7개) |
| 출처 | Gillon 2017 era | Agol 2021 |
| 일치도 | 7개 모두 `a` sub-percent | TTV-refined masses |

예시. TRAPPIST-1b의 a = 0.01155 AU (REX) vs 0.01154 AU (NS).

### Teegarden

| | REX | NearStars |
|---|---|---|
| 행성 | **b, c** | **b, c, d** |
| 출처 | Zechmeister 2019 | Dreizler 2024 |

> **NS에는 세 번째 행성(d) 있음.** REX는 그 발견 이전 동결.

### 행성 헤드라인

> 2020 이후 가장 활발하게 서베이된 세 시스템이 정확히 REX가 가장
> 뒤처진 셋 — **Barnard**(전면 개편), **Proxima**(새 내부 d, c 강등),
> **Teegarden**(새 외부 d). TRAPPIST-1과 Tau Ceti는 정밀화는 됐지만
> 재구조화는 없음.

---

## 7. 출처와 방법론

| | REX | NearStars |
|---|---|---|
| Attribution | cfg 내 inline 주석. 예: `// Used Space Engine to approximate` | per-measurement `bibcode`, `doi`, `method`, `recommended` |
| 출처 핀 | 없음 | NEA / SIMBAD / Gaia DR3 + `accessed` 날짜 |
| 경쟁 측정값 | 단일 값, 묵시적 선택 | `*_measurements[]` 배열에 전부 보존. 예: TRAPPIST-1 질량은 Gillon 2016 → Agol 2021까지 6개 |
| 단위 | SI 혼합 + 런타임 스케일 팩터 | SI raw, solar derived, ICRF Cartesian km/km·s⁻¹ |
| 에포크 | KSP 게임 초, origin 불분명 | 명시 JD + label |

> **NS의 가장 방어 가능한 우위.** REX의 prose 주석은 머신 체크 불가능,
> 저자가 그때 읽은 논문 값을 묵시적으로 동결. NS의 per-measurement
> 카탈로그 + `recommended` flag는 큐레이션이 감사 가능하고 후속 문헌과
> freshness 체크 자동화 가능.

---

## 8. NearStars에 시사점

1. **채울 커버리지 갭 없음.** Implementation shortlist 작업이 REX
   때문에 막힌 건 없음.

2. **Retraction 감시.** REX의 Barnard b는 무효화된 발견 사례. NS의
   `bibcode` + `recommended` flag 정책이 보호 장치 — 단 curation
   단계가 retraction을 능동적으로 모니터링해야 작동. NEA의
   `pl_controv_flag` 가 우리 리뷰 경로에 전파되는지 확인 필요.

3. **Tau Ceti e 조사.** Feng 2017의 4개 검출 중 가장 disputed라
   의도적으로 뺐을 가능성이 높지만, 또는 단순 누락. 어느 쪽이든
   `db/systems/tau_cet.json::meta.notes` 에 명시 권장.

4. **Proxima T_eff 재검토.** NS의 3498 K가 출판된 범위 상단에 있음.
   `proxima_cen.json::meta.notes` 에 선택 근거 명시 권장.

5. **Jacobi 다성계 선택 검증.** REX의 flat "Proxima-around-Sun"
   인코딩이 NS의 Jacobi + ICRF Cartesian 으로 얻는 가치를 역으로 보여줌.
   이게 binary-epoch pipeline 이 존재하는 정당화 자체.

6. **라이선스 명확화.** REX README "All Rights Reserved" vs SpaceDock
   "CC-BY-NC-SA" 모순. REX 자산 재사용 시 저자에게 먼저 확인. (현재
   재사용 0건.)

---

## 9. 미해결 질문

- 왜 `tau_cet.json` 에 **e만 빠지고** f/g/h는 있는지 (같은 논문, 같은
  dispute flag). Curation? Oversight?
- 빌드 파이프라인이 NEA `pl_controv_flag=1` 행을 **리뷰 리포트에
  flag** 하는지. 안 한다면 향후 retraction이 다시 들어올 수 있음.
- **REX 대기 곡선** — REX는 모든 body의 `temperatureCurve` /
  `pressureCurve` 를 손튜닝. Kopernicus 설정 출시 시 합성? REX 복사? 새
  큐레이션? 본 문서 범위 밖.
- **REX upstream 상태.** 마지막 커밋 2020-04-11; 사실상 abandoned.
  retraction fix를 push 하려면 fork 필요.

---

## 10. Phase 3 TRAPPIST-1: 합성 깊이 vs REX

Phase 3는 2016–2026년 논문 약 100편을 바탕으로 일곱 행성 전부에 cfg-ready
결정을 내렸다. REX가 작성된 시점에는 존재하지 않았던 JWST 3년치 결과를
포함한다. 이 섹션이 그 격차를 정량화한다.

### 10.1 질량·반경 정밀도

REX는 Gillon 2017 시대 TTV 값 사용. Phase 3는 Agol 2021 (284회 이상 통과로
재분석)을 채택. 반경은 약 3% 수준에서 일치하지만 불확도가 2–3배 줄었고,
질량은 b(+62%)와 f(+53%)에서 크게 달라졌다 — 둘 다 REX 자체 1σ 바깥.

| 행성 | REX 질량 (M⊕) | Phase 3 질량 (M⊕) | Δ | REX 반경 (R⊕) | Phase 3 반경 (R⊕) | Δ |
|---|---|---|---|---|---|---|
| b | 0.85 ± 0.72 | **1.374 ± 0.069** | **+62%** ⚠ | 1.086 ± 0.035 | **1.116 ± 0.014** | +2.8% |
| c | 1.38 ± 0.61 | **1.308 ± 0.056** | −5% | 1.056 ± 0.035 | **1.097 ± 0.014** | +3.9% |
| d | 0.41 ± 0.27 | **0.388 ± 0.012** | −5% | 0.772 ± 0.030 | **0.788 ± 0.011** | +2.1% |
| e | 0.62 ± 0.58 | **0.692 ± 0.022** | +12% | 0.918 ± 0.039 | **0.920 ± 0.013** | +0.2% |
| f | 0.68 ± 0.18 | **1.039 ± 0.031** | **+53%** ⚠ | 1.045 ± 0.038 | **1.045 ± 0.013** | 0% |
| g | 1.34 ± 0.88 | **1.321 ± 0.038** | −1% | 1.127 ± 0.041 | **1.129 ± 0.015** | +0.2% |
| h | 해당 없음 | **0.326 ± 0.020** | 신규 | 0.752 ± 0.032 | **0.755 ± 0.014** | +0.4% |

> **b와 f의 질량 변화는 REX 1σ를 초과한다.** b는 Gillon 2017 중앙값
> (0.85 M⊕)이 Agol 2021 (1.374 ± 0.069 M⊕)의 약 7σ 아래. f는 0.68에서
> 1.039 M⊕로 오르며 화성급에서 지구급으로 분류가 바뀐다. 전체 일곱 행성의
> 불확도는 2–10배 개선됐다. REX의 큰 불확도는 2017년 당시 TTV 축퇴를
> 솔직하게 반영한 것이고, Agol 2021이 4년치 추가 관측으로 이를 해소했다.

### 10.2 대기 결정

REX에는 TRAPPIST-1 행성의 대기 데이터가 전혀 없다. Phase 3는 2022–2026년
JWST 문헌에서 행성당 cfg-ready 시나리오 한 개를 결정했다. 신뢰도는
행성마다 다르다 — b와 c는 JWST가 직접 관측했고, 외곽 행성들은 모델
의존적이다.

| 행성 | REX | Phase 3 시나리오 | 신뢰도 | 핵심 근거 |
|---|---|---|---|---|
| b | — | **무대기** | 높음 | MIRI 위상 곡선 Ducrot 2025; >0.3 bar 배제 |
| c | — | **O₂ 극박 대기** (~0.01 bar) | 낮음 | Zieba 2023 CO₂ 없음; 무대기도 방어 가능 |
| d | — | **극박 아웃가싱** (~0.01 bar) | 낮음 | Piaulet 2025; 무대기도 방어 가능 |
| e | — | **1 bar N₂+CO₂** (수권 행성) | 높음 | Glidden 2025; Hapi 2024 GCM |
| f | — | **박 CO₂ 풍부** (~0.1 bar) | 중간 | Lim 2024; Wolf 2017 눈덩이-HZ |
| g | — | **극박 CO₂** (~0.05 bar) | 중간 | Moran 2018 H₂-rich 배제; 아웃가싱 |
| h | — | **희박 흔적 대기** (~0.005 bar) | 낮음 | Gressier 2022 H₂-rich 배제 |

> **안쪽에서 바깥으로의 기울기.** b는 JWST가 무대기로 확인했고,
> e는 높은 신뢰도로 거주 가능성 우선. 중간 행성(c–d, f–h)은
> 제약이 있지만 비확정. Phase 3는 c·d의 "무대기" 대안 해석을
> 주석으로 명시적으로 보존했다 — REX에는 없던 큐레이션 층이다.

### 10.3 조석 가열

REX에는 조석 가열 추정치가 전혀 없다. Phase 3는 Bolmont 2026(내부 행성),
Bolmont 2020(외곽), Hay & Matsuyama 2019(g)에서 행성별로 산출했다.

| 행성 | REX | Phase 3 추정 (W/m²) | 비고 |
|---|---|---|---|
| b | — | 0.5–1 (평균); 최대 ~407 (2σ 상한) | JWST 야간면 비검출이 상한 제한 |
| c | — | 0.005–0.05 | Bolmont 2026에서 규모 추정 |
| d | — | ~0.1–0.5 (추정) | Piaulet 2025 마그마 오션 내부 구조 |
| e | — | 0.001–0.01 | Bolmont 2020 |
| f | — | 0.0005–0.005 | Bolmont 2020 |
| g | — | 2×10⁻⁷–0.001; 행성간 조석 +2–20% | Hay & Matsuyama 2019 |
| h | — | 0.00001–0.0001 | 무시 가능 |

> **b는 사실상 exo-Io.** 보수적 추정(0.5–1 W/m²)만 해도 Io의
> ~2 W/m²와 비슷하고 화성 방사성 열원 ~0.04 W/m²의 10배 이상이다.
> 이것이 "지속적 화산 활동 + 신선한 용암류"라는 표면 결정을 이끌었다
> — REX는 이 차원을 모델링할 수 없었다.

### 10.4 본드 반사율과 표면 모델

REX는 표면 반사율이나 지형 정보가 없다. Phase 3는 JWST 열복사(내부 행성)와
GCM 문헌(외부 행성)에서 행성별 cfg-ready 반사율과 표면 시나리오를 결정했다.

| 행성 | REX 반사율 | Phase 3 본드 반사율 | 표면 시나리오 |
|---|---|---|---|
| b | — | 0.00 | 어두운 초마피아 현무암 + 냉각 용암 반점 |
| c | — | 0.05 | 민 암석면; 얕은 O₂ 풍화층 |
| d | — | 0.10 | b/c 유사 암석면; 부분 산화 |
| e | — | 0.30 | 열린 바다 + 부분 구름 (수권 행성) |
| f | — | 0.45 | 전지구 눈덩이 얼음 + 박 구름 |
| g | — | 0.55 | 전지구 눈덩이 얼음 + 박 CO₂ 구름 |
| h | — | 0.40 | 혼합 기반암 + CO₂/N₂ 서리 |

### 10.5 JWST 시대: REX가 가질 수 없었던 데이터

REX는 JWST 초도 관측 3년 전인 2020-04-11에 동결됐다.
Phase 3는 핵심 JWST 논문 7편을 직접 반영한다.

| 논문 | 결과 | NearStars 반영 |
|---|---|---|
| Greene 2023 (2303.14849) | b: T_day ≈ 503 K; 두꺼운 대기 없음 | b 무대기; 반사율 = 0 |
| Zieba 2023 (2306.10150) | c: 두꺼운 CO₂ 없음 | c 무대기-또는-박 대기 제약 |
| Ducrot 2024 (2412.11627) | b: 초마피아면 우선 vs CO₂+연무 | b 표면: 신선 초마피아 |
| Ducrot 2025 (2509.02128) | b+c 위상 곡선: 야간면 방출 없음 | b 무대기 결정적 확인 |
| Piaulet 2025 | d: 질량 재확인; 마그마 오션 내부 | d 표면 시나리오 |
| Glidden 2025 | e: 1 bar N₂+CO₂ 호환 | e 수권 행성 시나리오 |
| Lim 2024 | f: H₂-rich 배제; 박 CO₂ 허용 | f 눈덩이 시나리오 |

---

### 10.6 한 줄 요약

> **궤도 일치 유지.** 장반경 일곱 개 모두 <1% 일치 — Phase 2 비교에서
> 이미 확인된 결과와 동일.

> **질량 정밀도 2–10배 향상; b·f 중앙값이 크게 바뀌었다.**
> b +62%, f +53% — 둘 다 REX 1σ 바깥. Gillon 2017-era 질량은
> 내부 구조·밀도 모델링에 더 이상 쓸 수 없다.

> **대기: REX에는 없었고 Phase 3에는 행성마다 방어 가능한 시나리오가 있다.**
> b는 JWST 확인 무대기, e는 JWST 지지 거주 가능. c–d·f–h는
> 대안 시나리오가 명시적으로 기록된 상태로 모델 제약됨.

> **표면: REX에는 없었고 Phase 3에는 cfg-ready 색상·반사율·지형이 있다.**
> b의 용암 지면(A=0)부터 f/g의 전지구 눈덩이(A=0.45–0.55),
> e의 수권 행성(A=0.30)까지.

> **조석 가열: REX에는 없었고 Phase 3는 b를 exo-Io 유사체로 정량화했다.**
> Bolmont 2026이 JWST 야간면 제약을 이용해 상향 수정한 직접적 결과.

## Related

- [methodology](methodology.md) — NearStars 가 사용하는 스키마 원본 (REX 의 산문식 어트리뷰션이 그 대비).
- [guideline](guideline.md) — NearStars 의 프로젝트 가이드라인이 §1 에서 REX 를 선조로 인용합니다.
- [trappist-1-b](../phase3/trappist-1-b.md), [trappist-1-c](../phase3/trappist-1-c.md), [trappist-1-d](../phase3/trappist-1-d.md), [trappist-1-e](../phase3/trappist-1-e.md), [trappist-1-f](../phase3/trappist-1-f.md), [trappist-1-g](../phase3/trappist-1-g.md), [trappist-1-h](../phase3/trappist-1-h.md) — §10 이 REX 대비 TRAPPIST-1 Phase 3 갭을 정량화합니다.
- [proxima-cen-b](../phase3/proxima-cen-b.md) — §6 이 Proxima 행성 로스터 변경을 다룹니다.
- [alpha-centauri-a](../phase3/alpha-centauri-a.md), [alpha-centauri-b](../phase3/alpha-centauri-b.md) — §3–5 가 α Cen 항성 파라미터와 토폴로지 갭을 다룹니다.
