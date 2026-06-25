<!-- 천체의 구-대비 변형(자전 편평 J2 + 조석고정 triaxial C22)을 근거화 계산해 Principia 중력모델에 채우는 방법 -->
# Body figure grounding — rotational oblateness (J₂) and tidal triaxiality (C₂₂)

모든 NearStars 천체의 2차(degree-2) **형상**을 다루는 방법론 레퍼런스입니다. 천체가 완전한 구에서 얼마나
벗어나는지, 그리고 그 변형을 어떤 중력 계수가 포착하는지를 설명합니다. 물리적 원인은 둘, 계수도 둘입니다.

- **자전**은 천체를 편평한 회전타원체로 누릅니다 → zonal **J₂** (= −√5·C̄₂₀).
- **조석고정 천체의 영구 조석 팽대부**는 천체를 *triaxial*(긴 축이 주성을 향함)로 만듭니다
  → sectoral **C̄₂₂**가 추가됩니다.

여기는 **방법** 자체의 canonical 본거지입니다. *데이터 + cfg 형식* 짝 문서는
[`principia-geopotential-data.md`](principia-geopotential-data.md)이며, 태양계 계수의 verbatim 값,
정규화 규칙(J₂ = −√5·C̄₂₀, J₂ = 10⁄3·C̄₂₂), proto↔KSP-cfg 매핑을 담고 있습니다. 그 문서는 이미
**Polyphemus** 자이언트의 J₂를 완전히 풀어 두었고, 이 문서는 그 레시피를 천체 종류 전반으로 일반화하고
조석 C₂₂를 근거화합니다. J₂/C₂₂는 아트디렉션 선택이 아니라 **도출된 emit**입니다. 자전 + 질량 + 반경 +
중심 응집도로부터 결정론적으로 따라 나오므로, 단위 변환처럼 천체마다 계산됩니다. 인게임에서 왜 중요하냐면,
J₂는 **인공위성**에 작용하는 가장 지배적인 비-Keplerian 섭동(승교점 이동 + 근점 세차 ∝ (R/a)²·cos i)이고,
Principia는 비행체를 완전한 지오포텐셜 안에서 적분하기 때문입니다 — 즉 플레이어가 천체 주위를 도는 모든
궤도의 형태를 좌우합니다.

> 규율. 형상은 **정유체역학 평형** 관계식(Radau–Darwin, Maclaurin, 동기위성 형상)에서 따라 나옵니다 —
> 교과서 결과이므로 "도출값은 논문 근거화" 원칙의 허용된 예외입니다. 그럼에도 인용이 필요한 것은
> **캘리브레이션 앵커**(측정된 태양계 J₂/C₂₂)와 관성모멘트 경계이며, 이들은 NASA ADS로 해소합니다.

## 1. The figure parameter

두 효과 모두 표면에서의 원심(또는 조석) 가속도 대 자체중력 가속도의 무차원 비로 지배됩니다.

    q  =  ω²·R³ / (G·M)            (rotational, ω = 2π/P_rot)

**고정되지 않은** 천체에서 ω는 항성시 기준 자전 각속도입니다. **동기 고정된** 천체에서는 ω = n(궤도 평균
운동)이고, 주성으로부터의 *정적 조석*이 같은 차수의 항을 추가합니다 — 동기 원궤도에서는 leading order로
n²R³/(GM_body) = (M_primary/M_body)(R/a)³가 성립하여 자전 파라미터와 조석 파라미터가 비슷한 크기이기
때문입니다. 고정된 경우는 q_s = n²R³/(GM)로 씁니다.

## 2. Rotational figure — Maclaurin vs Radau–Darwin

q에 대한 1차 근사에서, 편평도 f = (R_eq − R_pol)/R_eq와 J₂는 다음 정유체 관계를 따릅니다.

    J₂  =  (2/3)·f  −  (1/3)·q

남은 자유도는 **중심 응집도**이며, 정규화 관성모멘트 NMoI = C/(M R²)로 표현합니다(0.4 = 균질 구,
작을수록 더 응집).

- **균질(Maclaurin) 극한**, NMoI = 0.4: f = (5/4)q, 따라서 **J₂ = q/2**. 이것이 편평도의
  *균일밀도 상한*입니다.
- **중심 응집 천체**(모든 실제 행성/항성), NMoI < 0.4: **Radau–Darwin** 관계를 사용합니다. 이 관계는
  J₂, q, NMoI를 묶습니다(Helled et al. 2011, `principia-geopotential-data.md`에 재현된 형태입니다).

      NMoI = (2/3)·[1 − (2/5)·√(5q/(q + 3J₂) − 1)]
      inverted →  J₂ = (q/3)·[5/(s²+1) − 1],   s = (5/2)·(1 − (3/2)·NMoI)

  같은 q에서 더 응집된 천체는 편평이 **덜** 일어나므로, J₂/q는 ½ 아래로 떨어집니다.

### Calibration (always verify on the real bodies first)

| 천체 | 종류 | q | NMoI | J₂/q | measured J₂ |
|---|---|---|---|---|---|
| Earth | rocky | 3.45e-3 | 0.331 | 0.31 | 1.083e-3 |
| Mars | rocky | 4.6e-3 | 0.364 | ~0.43* | 1.96e-3 |
| Jupiter | giant | 0.083 | 0.265 | 0.177 | 1.470e-2 |
| Saturn | giant | 0.140 | 0.220 | 0.116 | 1.629e-2 |
| Sun | star | ~2e-5 | ~0.06 | ~0.01 | 2.1e-7 |

\*Mars는 Tharsis에 의한 비-정유체 초과량을 가지므로, 그 *정유체* J₂는 더 낮습니다. 자이언트 캘리브레이션은
Jupiter를 −0 %, Saturn을 −10 %로 재현합니다(1차 절단, q가 커질수록 오차 증가) — 따라서 **빠른 자전체(큰 q)에서는
1차 값이** 참 J₂를 약 10–20 % 과소예측합니다. 항성은 응집의 극단에 위치하여, 느린 자전의 태양조차 J₂ ≈ 2×10⁻⁷를
가집니다(알려진 가장 둥근 천체 중 하나입니다).

## 3. Tidal triaxiality — synchronously locked bodies

(거의) 원궤도에 고정된 천체는 주성을 향하는 **영구** 조석 팽대부를 일으킵니다. 그 2차 형상은
**triaxial**(반축 a > b > c, a는 주성을 향하고 c는 자전축)이 되어, J₂ **와** 실제 sectoral C̄₂₂를 함께
가집니다. 정유체 평형에서 둘은 고정된 비율로 묶입니다.

    J₂  =  (10/3)·C̄₂₂        (equivalently  C₂₂ = 0.3·J₂)

그리고 천체는 축 차이가 (a−c):(b−c) = 4:1인 triaxial 타원체가 됩니다. 이 비율은 **측정된 동기위성들**(Io,
Europa, Ganymede, Titan 모두 J₂/C₂₂ ≈ 10/3)에서 **확인**되며, 그래서 고정된 경우는 측정 불가능한 것이
아니라 *예측 가능*합니다. 크기 또한 같은 천체들로 캘리브레이션됩니다.

    J₂  ≈  (0.9–1.1)·q_s     for differentiated rocky/icy synchronous bodies
    C̄₂₂ ≈ 0.30·J₂

(Io J₂/q_s ≈ 1.08, Europa ≈ 0.88 — 이 폭은 내부 구조 차이입니다.) 따라서 느린 *자유* 회전체와 달리,
가까이 고정된 천체는 자전과 조석이 더해지기 때문에 q_s 자체에 필적하는 J₂를 가집니다.

> **화석 팽대부 주의.** Moon(J₂/C₂₂ ≈ 9, 10/3에서 크게 벗어남)과 Mercury는 정유체가 **아닙니다** —
> 그 팽대부는 더 빠르고/가까웠던 과거 상태가 얼어붙은 기록입니다. 우리 동기 천체들은 별도의 형상을
> 화석화할 역사가 없으므로, 천체의 lore가 그것을 암시하지 않는 한 **정유체**로 가정합니다. 문제가 될 수
> 있는 곳에는 그 선택지를 표시해 둡니다.

## 4. Regimes by body type

| body class | spin | figure | coefficients |
|---|---|---|---|
| **가스 자이언트 / 빠른 자유 회전체** | fast, free | large oblate | scalar **J₂** (+ J₄ ≈ −4 % J₂, J₆), no tesseral |
| **자유 암석체** (드묾; 빠르고 비고정) | P_rot | oblate, J₂ ∝ q | scalar **J₂** (tesseral unmeasurable → omit) |
| **동기 암석/얼음체** (로스터 대부분) | ω = n | **triaxial** | degree-2 full: **C̄₂₀ + C̄₂₂** (J₂ = 10⁄3·C₂₂) |
| **항성** | 대개 느림 | nearly round | scalar **J₂** (tiny; omit unless a fast rotator) |

`reference_radius`(계수가 스케일링되는 기준 반경 — 자전 형상의 경우 **적도** 반경)는 J₂/지오포텐셜을
emit할 때마다 필수입니다. cfg 형식(scalar `j2`, zonal `geopotential_row`, full cos/sin)은
[`principia-geopotential-data.md`](principia-geopotential-data.md)에 정리되어 있습니다.

## 5. Worked examples (NearStars roster, Phase 4 active set)

입력값은 큐레이션된 질량 / 반경 / 자전이며, 고정 상태는
[조석고정 타임스케일 방법](tidal-locking-timescale-methodology.md)에서 가져옵니다.

| body | class | ω source | q (or q_s) | J₂ | C̄₂₂ | note |
|---|---|---|---|---|---|---|
| **Erid** (40 Eri A b) | free rocky | P_rot 5.1 h | **0.056** | **~0.017–0.019** | — | 로스터에서 가장 편평한 암석체 — f ≈ 5 %, 인게임에서 보이는 적도 팽대부; 1차 값은 과소예측(큰 q) |
| **Polyphemus** (α Cen A b) | gas giant | P_rot ~10 h | 0.19 | **~0.023–0.026** | — | geopotential-data.md에서 완전히 풀어 둠 (NMoI ~0.23) |
| **TRAPPIST-1 b** | sync. rocky | n (P 1.51 d) | 1.5e-3 | ~1.5e-3 | **~4.6e-4** | 가까운 고정 → 실제 영구 조석 팽대부, J₂ ≈ 지구 수준 |
| **Proxima b** | sync. rocky | n (P 11.2 d) | 2.8e-5 | ~2.8e-5 | ~8e-6 | 충분히 멀어 형상이 미미함(기록만; C₂₂는 emit 임계 아래로 추정) |
| **Fomalhaut A** | star (A-type) | fast (A4V) | — | (omit) | — | 로스터에서 유일하게 빠르게 자전하는 항성(자전축 측정, Le Bouquin 2009)이라 물리적으로 편평하지만, 발표된 편평도 수치는 없음 — 게다가 그 J₂는 멀리 떨어진 디스크 / Fomalhaut b 궤도(AU 스케일)에 동역학적으로 무의미함. 자전 극만 기록하고 J₂는 omit. 태양형 K/M 호스트 → J₂ ~10⁻⁷, omit. |

핵심 대비는 이렇습니다. **Erid**(빠르고 자유로운 뜨거운 슈퍼지구)는 실제로 편평하지만, 고정된 거주가능
영역 암석체들은 고정이 가까울수록 가파르게 커지는 작은 영구 조석 C₂₂를 제외하면 거의 둥글다는 것입니다
(TRAPPIST-1 b ≫ Proxima b). 항성은 의미 있는 궤도 거리에서는 점광원이나 다름없으므로, 형상은 기록하되
emit하지 않습니다.

## 6. Procedure (per body)

1. 고정 상태 결정(조석고정 타임스케일 방법) → 자유 또는 동기.
2. q(자유: P_rot) 또는 q_s(고정: 궤도 n)를 **적도** 반경을 써서 계산.
3. 천체 종류로부터 NMoI 선택(giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08) — 가정 + 범위를 명시.
4. 자유 회전체 → Radau–Darwin로 J₂(균질 경계로는 Maclaurin q/2). 동기 → J₂ ≈ (0.9–1.1)·q_s,
   C̄₂₂ = 0.3·J₂(정유체).
5. Emit 임계: ~1×10⁻⁶ 아래의 C₂₂(및 J₂)는 건너뜀(값은 기록하되 행은 omit) — 동역학적으로 무의미합니다.
   `reference_radius` = 적도 반경으로 설정.
6. `db/systems/*`를 직접 건드리지 말고 **큐레이션된 source layer**를 통해 작성한 뒤 rebuild.

## 7. Citations

모든 bibcode는 NASA ADS로 검증했습니다.

- **Helled, Anderson, Schubert & Stevenson 2011**, Icarus 216, 440 (`2011Icar..216..440H`,
  arXiv **1109.1627**) — 자이언트에 사용한 Radau–Darwin NMoI ↔ J₂ 관계; §2의 inversion 형태.
  `principia-geopotential-data.md`에 핀.
- **Murray & Dermott 1999**, *Solar System Dynamics* (`1999ssd..book.....M`) §4 — 자전 및
  동기 천체의 정유체 형상; 이 연쇄식의 교과서 본거지.
- **Tricarico 2014**, ApJ 782, 99 (`2014ApJ...782...99T`) — 동기 형상을 현대적으로 엄밀하게 진술,
  곧 J₂/C₂₂ ≈ 10⁄3, (b−c)/(a−c) ≈ 1⁄4, 그리고 고차 Ω²/(πGρ) 보정입니다. **Dermott 1979**,
  Icarus 37, 575 (`1979Icar...37..575D`)와 짝지어 사용 — 위성 형상과 중력 모멘트의 고전적 유도.
- **Chandrasekhar 1969**, *Ellipsoidal Figures of Equilibrium* (`1969efe..book.....C`) —
  Maclaurin spheroid(균질 자전 극한, f = 5q/4).
- **Zharkov & Trubitsyn 1978**, *Physics of Planetary Interiors* (`1978ppi..book.....Z`);
  **Hubbard 1984**, *Planetary Interiors* (`1984plin.book.....H`) — 형상 이론, q–f–J₂–NMoI 연쇄식.
- **측정된 동기 형상 앵커**(J₂ = 10⁄3·C₂₂ 캘리브레이션): Io — Anderson
  et al. 2001 (`2001JGR...10632963A`; 형상 축 a−c = 14.4 km, b−c = 3.6 km → 4:1,
  C/MR² = 0.3769); Europa — Anderson et al. 1998 *Science* 4회 근접
  (`1998Sci...281.2019A`); Ganymede — Anderson et al. 1996 (`1996Natur.384..541A`, J₂ & C₂₂
  직접 보고); Titan — Iess et al. 2010 *Science* (`2010Sci...327.1367I`; a−c = 410 m,
  b−c = 103 m → 비율 3.98 ≈ 4:1, C/MR² ≈ 0.34). 모두 J₂/C₂₂ ≈ 10⁄3을 줍니다.
- **Moon — 비-정유체 / 화석 팽대부**: GRAIL 중력장, Zuber et al. 2013 *Science*
  (`2013Sci...339..668Z`); J₂/C₂₂에서 도출한 관성모멘트 + 내부 해석, Williams et al. 2014
  (`2014JGRE..119.1546W`, I_s/MR² = 0.392728). J₂/C₂₂ ≈ 9 ≠ 10⁄3.
- **Fomalhaut A 자전축** — Le Bouquin et al. 2009, A&A 498, L41 (`2009A&A...498L..41L`,
  VLTI/AMBER): A4V, 자전축 PA 65°로 디스크에 ⊥ — 측정된 극을 가진 빠른 자전체임을 확인하지만,
  편평도 수치는 발표되지 않았습니다(§5 주석 참조).

## Related

- [`principia-geopotential-data.md`](principia-geopotential-data.md) — verbatim
  태양계 계수, 정규화, cfg 형식, Polyphemus 자이언트 워크드 예시.
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — cfg 스키마(노드 문법, 단위).
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) — 고정 상태(형상의 자전 입력).
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) — 반경 입력.
- [`methodology-index.md`](methodology-index.md) — 전체 방법론 인덱스.
