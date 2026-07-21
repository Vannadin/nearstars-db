<!-- 쌍극 자기장 세기+항성풍에서 자기권 크기·모양과 방사선대 강도(다요인)를 도출해 Kerbalism 지오메트리로 매핑하는 방법(논문 근거) -->
# 행성 자기권 지오메트리 근거화: standoff·방사선대·Kerbalism 매핑

바디의 **쌍극 자기장 세기**([암석형](rocky-planet-dynamo-methodology.md) 또는
[거대행성](planetary-dynamo-scaling.md) 다이나모 레시피 산출)를 **자기권의 모양과
크기** — 자기권계면 standoff, 방사선대 범위, 벨트 강도 — 로 바꾸고, 이를 Kerbalism이
실제로 소비하는 필드로 매핑하는 방법 문서입니다. Kerbalism은 Tesla 단위 물리 자기장을
들고 있지 않습니다. 방사선 환경을 *지오메트리*(`RadiationModel` 벨트/pause 셸) +
*강도*(`radiation_inner/outer/pause/surface`, rad/h) + 쌍극축 방향
(`geomagnetic_pole_lat/lon`)으로 모델링합니다. 이 문서가 그것들을 물리에서 도출하는
레시피입니다.

**핵심 규율(이 문서가 존재하는 이유).** 자기장 세기는 *그릇*을 정하지 *내용물*을 정하지
않습니다. standoff와 벨트 반경은 자기장으로 스케일되지만, **벨트 강도는 별개 요인** —
입자 공급원과 손실의 균형, 그리고 Kennel–Petschek 안정포획 한계로 상한 — 의 지배를
받으며 자기장 세기만의 함수가 *아닙니다*. 벨트 강도를 B에서 읽어내려는 것이 이 문서가
막는 전형적 실수입니다.

## Part A — 자기장에서 지오메트리(모양 + 크기)

### 자기권계면 standoff (Chapman–Ferraro 균형)

주간측 자기권계면은 행성 자기압이 주변 램압과 평형을 이루는 곳입니다(Chapman & Ferraro
1931, `1931TeMAE..36...77C`; 경험식 Shue et al. 1997/1998, `1997JGR...102.9497S` /
`1998JGR...10317691S`). 쌍극장이 `B(r) = B_eq·(R_p/r)³`로 감소하고 Chapman–Ferraro
표면전류가 경계에서 場을 약 2배로 만든다면(계수 `f ≈ 2`).

    R_mp / R_p  =  [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)      (μ₀ = 4π×10⁻⁷)

여기서 `P_ram = ρ v²`는 바디를 스쳐 흐르는 것의 램압입니다 — 행성이면 **항성풍**,
임베디드 위성이면 **모행성의 공회전 자기권 플라스마**(regime 참조). `^(1/6)` 멱은
입력 오차에 매우 강건합니다. B나 P가 8배 틀려도 R_mp는 2배만 움직입니다.

**적도(sub-solar) 자기장**만 개입합니다 — 자기권계면 코는 자기적도에 있습니다. 극
자기장은 여기 등장하지 않습니다. 순수 쌍극이면 그냥 `2·B_eq`라 독립적 지오메트리 정보가
없습니다(다극장에서만 정보값을 가짐 — regime 참조).

### 벨트 범위

포획 입자는 닫힌 쌍극 자기력선(L-shell)을 타므로, 벨트는 바깥으로 **자기권계면에
갇히고**(`R_outer ≲ 0.6–0.8 R_mp`) 안으로는 대기/표면(`R_inner ≈ 1.1–2 R_p`)에
갇힙니다. 강한 場 → 큰 standoff → 벨트가 더 멀리 놓일 여지. 자기장 세기가 벨트를 직접
크기 정하는 유일한 지점입니다.

## Part B — 벨트 강도는 다요인 (자기장 세기 아님)

벨트 강도는 **공급원 − 손실 균형, 場/플라스마 상한으로 캡**됩니다.

1. **공급원**이 바닥을 정합니다. 항성풍 포획, **CRAND**(우주선 알베도 중성자 붕괴,
   내부벨트 양성자원, Lenchek 1961 `1961JGR....66.4027L`), 안쪽으로의 방사확산(Schulz &
   Lanzerotti 1974 `1974pdrb.book.....S`), 그리고 **내부 플라스마원** — 화산 위성 하나가
   전부를 지배할 수 있습니다(Io가 목성 벨트에 ~1 ton/s 주입, Bagenal 1994 Io torus
   `1994JGR....9911043B`, Divine & Garrett 1983 목성 모델 `1983JGR....88.6889D`).
2. **Kennel–Petschek 상한**이 캡합니다. *최대 안정포획 플럭스*가 존재해, 그 위에서는
   입자 자신의 whistler-mode 파동이 성장해 loss cone으로 산란시킵니다(Kennel & Petschek
   1966, `1966JGR....71....1K`, 2600+ 인용). 이 한계는 場과 냉플라스마 밀도에 의존하지만
   **공급원 세기와 무관**합니다 — 그래서 강공급원 자기권(지구·목성)은 K–P 천장에서
   *포화*하고, 공급을 더 늘려도 강도가 오르지 않습니다.
3. **손실**이 끌어내립니다. 파동–입자 산란(chorus/hiss/EMIC, Thorne 2010
   `2010GeoRL..3722107T`, 리뷰 Ripoll 2020 `2020JGRA..12526735R`), Coulomb/대기 손실,
   그리고 **위성·고리에 의한 흡수** — 토성 벨트는 고리/위성에 쓸려나갑니다(Cooper 1983,
   `1983JGR....88.3945C`).

도출 상의 귀결: **벨트 강도를 B_eq에서 읽을 수 없습니다.** 같은 場을 가진 두 바디도
공급원(화산 위성 유무)과 손실(고리/위성 sweeping)에 따라 벨트 선량이 자릿수로 다를 수
있습니다. 場은 벨트가 *어디서 포획되는가*를 알려주고, 공급원/손실/K–P 균형이 *얼마나
강한가*를 정합니다. 따라서 벨트 강도는 공식 출력이 아니라 **공급원·손실을 명시한 regime
판정**으로 남습니다.

## Part C — Kerbalism 매핑

| 물리량 | Kerbalism 필드 | 도출 |
|---|---|---|
| 자기권계면 standoff | `pause_radius` (+ `has_pause`) | Part A의 R_mp/R_p |
| 차폐 품질(GCR) | `radiation_pause` (음수) | 깊은 standoff → 강한 차폐 |
| 벨트 범위 | `radiation_inner`/`outer` 벨트 반경 (DB `..._belt_radius_planet_radii`) | Part A 경계 |
| 벨트 강도(rad/h) | `radiation_inner`/`radiation_outer` | Part B regime: 공급원 − 손실, K–P 캡 — **B가 아니라 명시된 공급원/손실에서** |
| 쌍극축 방향 | `geomagnetic_pole_lat`/`lon` | = `magnetic_dipole_tilt_deg` |
| 벨트 존재 게이트 | (벨트가 아예 있나) | `B_eq ≳ 0.1× 지구`. 이하면 안정 포획 없음 |

## 검증

- **지구**: B_eq = 31 µT, 항성풍 P_ram ≈ 2 nPa → R_mp/R_p = [2²·(3.1e-5)²/(2μ₀·2e-9)]^(1/6) ≈ **9.6** — 관측된 ~10 R_E sub-solar 자기권계면과 일치. 내부벨트 ~1.2 R_E(CRAND 양성자), 외부 ~3–7 R_E(확산 + chorus), 강도는 K–P 천장 부근. ✓
- **목성**: 場만으로는(~4.3 G 적도) 극단적 벨트를 예측하지 못함. Io 플라스마원이 전자 K–P 한계까지(그 이상까지) 몰아붙임 — 강도 ≠ f(B)의 교과서적 증거. ✓
- **Polyphemus**(NearStars): 170 µT vs α Cen A 풍 램 0.38 nPa → R_mp ≈ **22 R_p**(Phase 4 보드의 독립 23.5 R_p와 같은 균형). ✓

## 유효 범위: regime

1. **쌍극 고유**(지구, Pandora): standoff 공식 적용; 벨트는 L-shell 위; 공급원이 강하면
   K–P 캡.
2. **다극 고유**(천왕성/해왕성, Proxima c; `Ro_ℓ > 0.12` 암석 다극 regime): offset/기운
   場 → **비대칭·얼룩진 벨트**와 틀어진 오로라 오벌. standoff 공식은 근사일 뿐이고, 여기서
   **극/적도 비 ≠ 2**가 다극 성분을 실제로 인코딩합니다 — 두 場을 다 들고 있는 게 redundant
   가 아니라 정보값이 되는 유일한 경우입니다.
3. **임베디드 위성**(거대행성 자기권 안의 위성. **Pandora = 가니메데 아날로그**, Kivelson
   1996 `1996Natur.384..537K`): standoff를 항성풍이 아니라 **모행성의 공회전 자기권
   플라스마**에 대해 잡습니다. 결과는 미니자기권. 위성 위치의 벨트 선량은 *모행성*의 그
   L-shell 벨트(모행성엔 손실/공급항) + 위성 자체 차폐로 결정됩니다.
4. **유도 / 다이나모 없음**(금성, Io, 사멸 암석행성): 고유 포획 없음, 벨트 없음.
   상호작용은 전리층/유도형이고 표면 선량은 직접 풍 + GCR입니다.
5. **약장/무대기**: `B_eq < 0.1× 지구` → 안정 벨트 없음, 표면 선량 직접.

## 워크드 예제 (NearStars)

- **Polyphemus**: 170 µT → R_mp ≈ 22 R_p. **5개 위성 전부 자기권 안**에서 공전. 벨트
  강도는 場 읽기가 아니라 *공급원 − 손실* 이야기입니다. Dante의 극단적 화산(~820× Io)이
  강한 내부벨트를 먹이고(공급원), 고리 + 5위성이 입자를 쓸어냅니다(손실, 토성 참조).
  Kerbalism은 큰 `pause_radius`, 높은 내부벨트 `radiation_inner`, 강한 음수 `radiation_pause`.
- **Pandora**(임베디드, 가니메데 아날로그): 자체 75 µT 쌍극 → Polyphemus 場 *안* 3.53 R_p
  에 미니자기권. **Polyphemus 두 벨트 사이 gap**에 위치하고 자체 場이 차폐를 더함 →
  거주가능의 물리 근거. standoff는 항성풍이 아니라 Polyphemus 국소 플라스마에 대해 계산.
- **Proxima b**(약 쌍극 ~0.06–0.1 ℳ⊕): 작은 자기권, standoff 몇 R_p뿐; 벨트 미미;
  표면 선량은 직접 M왜성 풍 + 플레어 지배.
- **Proxima c**(빙거성, offset/기운 다극): 비대칭 벨트, 틀어진 오벌; standoff 공식 근사;
  47° 틀림이 off-axis 오로라 구동.

신뢰도: standoff 지오메트리는 **medium**(강건한 `^(1/6)` 법칙, 지구/Polyphemus 검증).
벨트 강도는 본질상 **low** — 외계행성에서 그 자체로 불확실한 공급원·손실 항에 의존하며,
바로 그래서 계산값이 아니라 documented regime 판정으로 둡니다.

## 인용

- **Chapman & Ferraro 1931**, Terr. Magn. Atmos. Electr. 36, 77 (`1931TeMAE..36...77C`).
  자기권계면 / 압력균형 개념의 기원.
- **Shue et al. 1997 / 1998**, JGR 102, 9497 (`1997JGR...102.9497S`) / JGR 103, 17691
  (`1998JGR...10317691S`). 경험적 자기권계면 standoff + 풍 변화에 따른 형상.
- **Kennel & Petschek 1966**, JGR 71, 1 (`1966JGR....71....1K`). 안정포획 플럭스 한계 —
  벨트 강도의 공급원-무관 천장. Part B의 핵심.
- **Schulz & Lanzerotti 1974**, *Particle Diffusion in the Radiation Belts* (`1974pdrb.book.....S`).
  벨트를 채우는 방사확산 수송.
- **Lenchek et al. 1961**, JGR 66, 4027 (`1961JGR....66.4027L`). CRAND 내부벨트 공급원.
- **Divine & Garrett 1983**, JGR 88, 6889 (`1983JGR....88.6889D`); **Bagenal 1994**,
  JGR 99, 11043 (`1994JGR....9911043B`). 목성 방사선 + Io 내부 플라스마원 — "강도는 場이
  아니라 공급원이 정한다"의 canonical 사례.
- **Thorne 2010**, GRL 37, L22107 (`2010GeoRL..3722107T`); **Ripoll et al. 2020**,
  JGRA 125, e26735 (`2020JGRA..12526735R`). 파동–입자 가속·손실; 현대 벨트 동역학 리뷰.
- **Cooper 1983**, JGR 88, 3945 (`1983JGR....88.3945C`). 벨트 손실로서의 고리/위성 흡수 —
  Polyphemus 고리 + 위성 케이스.
- **Kivelson et al. 1996**, Nature 384, 537 (`1996Natur.384..537K`). 가니메데 임베디드
  자기권 — Pandora 아날로그.
- **Griessmeier et al. 2004**, A&A 425, 753 (`2004A&A...425..753G`); **Vidotto et al.
  2013**, A&A 557, A67 (`2013A&A...557A..67V`). 항성풍/조석고정 대비 외계행성 자기권 크기 —
  근접 행성 standoff 적용.

## Related

- [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md), 
  [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — 이 방법이 소비하는
  `B_eq`를 공급.
- `../../.claude/skills/nearstars-phase3/references/mod-grounded-fields.md` — 이 방법이
  방출 대상으로 삼는 Kerbalism `RadiationBody`/`RadiationModel` 필드 스키마.
- `methodology-index.md` — 모든 도출값 레시피의 살아있는 인덱스.
