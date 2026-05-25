# Binary / Multiple Star Epoch Pipeline Reference

> 출처: mockingbirdnest/Principia, RSS-Reborn/Sol-Configs,
> CharonSSS/RSS-Origin-2 (v1.0.0, 2026-05-21), USNO/GSU orb6 카탈로그,
> Gaia DR3 NSS 문서, Bond+ 2017, Akeson+ 2021, Kervella+ 2017 전반에 걸친
> 조사를 바탕으로 작성됨.
> 목적: JPL HORIZONS 데이터가 없는 쌍성/삼중성/다중성계에 대해,
> `solar_system_epoch = JD2433282.5` (1950-01-01 TDB) 시점의 ICRF 직교 상태 벡터를 계산함.
> 계산된 벡터는 NearStars의 Principia `principia_initial_state`에 입력됨.

## 목차

1. [선형 역전파가 실패하는 이유와 Sol/RSS의 해결 방식](#1-선형-역전파가-실패하는-이유와-solrss의-해결-방식)
2. [가까운 별에 대한 일반화. 수학적 배경](#2-가까운-별에-대한-일반화-수학적-배경)
3. [카탈로그 접근 — USNO/GSU orb6](#3-카탈로그-접근--usnogsu-orb6)
4. [카탈로그 접근 — Gaia DR3 NSS](#4-카탈로그-접근--gaia-dr3-nss)
5. [시스템별 표준 논문 (orb6보다 우선)](#5-시스템별-표준-논문-orb6보다-우선)
6. [삼중성계 처리](#6-삼중성계-처리)
7. [코드 스니펫](#7-코드-스니펫)
8. [무게중심 천문 측정 — 결정 트리](#8-무게중심-천문-측정--결정-트리)
9. [계산 예시 1 — JD2433282.5에서의 α Centauri AB](#9-계산-예시-1--jd24332825에서의-α-centauri-ab)
10. [계산 예시 2 — JD2433282.5에서의 Sirius AB](#10-계산-예시-2--jd24332825에서의-sirius-ab)
11. [알려진 함정](#11-알려진-함정)
12. [파이프라인 요약](#12-파이프라인-요약)
13. [출처](#13-출처)

---

## 1. 선형 역전파가 실패하는 이유와 Sol/RSS의 해결 방식

### 단순한 방법의 실패

긴밀한 쌍성 (Pluto-Charon ~6.4일, 소행성 쌍성 ~수 시간~수 일)의 경우, J2000에서 게임 에포크까지
`x_t0 = x_J2000 − v · Δt`와 같이 직선 운동으로 역전파하면 수십에서 수천 번의 공전이 이 간격
안에 완료되므로, 선형 추정치는 궤도 타원 위의 임의 위치를 가리키게 됨.

### Sol/RSS/RSS-Origin 2 패턴 (올바른 방법)

| 에포크 | JD | 날짜 | 역할 |
|---|---|---|---|
| `solar_system_epoch` | 2433282.5 | 1950-01-01 TDB | 상태 벡터를 이 시점 기준으로 제공 |
| `game_epoch` | 2433647.5 | 1951-01-01 TDB | KSP `UT = 0` |
| J2000 | 2451545.0 | 2000-01-01 TDB | 이 모드들에서는 **사용하지 않음** |

문제를 함께 해결하는 세 가지 구조적 선택.

1. **`solar_system_epoch`를 `game_epoch`보다 앞에 설정** — 이렇게 하면 역전파 자체가 불필요함.
   Principia의 심플렉틱 n체 적분기가 `solar_system_epoch`에서 `game_epoch`까지 *정방향*으로
   적분하면서 그 사이의 모든 궤도 운동을 정확하게 처리함 (Pluto-Charon은 365일 간격 동안
   약 57바퀴를 공전하며, 적분기가 이를 자연스럽게 처리함).

2. **두 쌍성 구성 요소를 동일한 에포크의 독립적인 절대 직교 벡터로 기재.**
   `principia_initial_state`에서 "주성/반성" 계층 구조를 사용하지 않음.
   각 `body { name = X; x = ...; vx = ... }` 블록은 `solar_system_epoch` 시점의
   ICRF 값임. Kopernicus의 `referenceBody`는 시각적 궤도 표시에만 사용되며,
   Principia는 역학 계산에서 이를 무시함.

3. **정확히 해당 에포크의 고정밀 소스에서 상태 벡터를 가져옴.**
   Sol의 경우 JPL HORIZONS가 소스임. 가까운 별들의 경우 HORIZONS 데이터가 없으므로,
   궤도 요소 자체가 전파기 역할을 함 (§3–5 참조).

### 예시. Sol-Configs의 Pluto-Charon (`Real_Sol-InitialState.cfg`)

```
principia_initial_state {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body { name = Pluto
    x  = -3.969308899525761e+09 km   y  = +3.031459117686943e+09 km
    z  = +2.141687156699421e+09 km
    vx = -2.220297402287733e+00 km/s  vy = -4.555001506883357e+00 km/s
    vz = -7.354838392738812e-01 km/s }
  body { name = Charon
    x  = -3.969297506358897e+09 km   y  = +3.031467748409172e+09 km
    z  = +2.141673752024598e+09 km
    vx = -2.320549242462520e+00 km/s  vy = -4.672609388474288e+00 km/s
    vz = -8.964243487721187e-01 km/s }
}
```

위치 벡터 차이 = **19,595 km** (알려진 Pluto-Charon 반장축 ~19,591 km과 일치함).
상대 속도 0.223 km/s — 해당 거리에서의 원형 궤도 속도와 일관됨.

RSS-Origin 2 의 쌍성 소행성들 (617-Patroclus + Menoetius, 47171-Lempo +
Paha + Hiisi 삼중계, 58534-Logos + Zoe, 65489-Ceto + Phorcys,
3548-Eurybates + Queta, 243-Ida + Dactyl) 모두 동일한 패턴을 따름.
각 구성 요소는 `JD2433282.5` 시점의 절대 ICRF 직교 상태로 자체
`body { }` 블록을 가짐. 쌍성별 `epoch` 오버라이드는 없음.

---

## 2. 가까운 별에 대한 일반화. 수학적 배경

별에 대해서는 HORIZONS 데이터가 없음. 대신 **궤도 요소 자체를 전파기로 사용** —
`solar_system_epoch` 시점에서 케플러 궤도를 해석적으로 평가함.

쌍성당 입력값. `P, T, e, a [AU], i, ω, Ω`, 시차 `π [mas]`, 질량
`M_A, M_B`, 목표 에포크 `t = JD2433282.5`.

### 좌표계 규약

하늘 평면 정규 직교 프레임 `(P̂, Q̂, Ŵ)`.
- `P̂` = 북 (NCP 방향, +Dec 방향)
- `Q̂` = 동 (하늘에서의 +RA 방향)
- `Ŵ` = 관측자 반대 방향 (양의 시선 속도 방향)

- `Ω`는 하늘에서 북에서 동으로 측정 (관측 시 반시계 방향)
- `ω`는 승교점에서 궤도면 내 궤도 운동 방향으로 측정
- `i = 0` → 궤도가 하늘 평면에 위치, 관측 시 반시계 방향 운동
- `i = 90°` → edge-on
- `i = 180°` → face-on, 시계 방향 운동

**교점 거울 모호성.** 시선 속도 데이터 없이는
`(i, ω, Ω)`과 `(180°−i, −ω, Ω+180°)`이 동일한 겉보기 하늘 운동을 만들어냄.
orb6는 RV로 해소된 경우를 Ω 뒤의 `*`로 표시함. 규약을 정하고 문서화할 것.

### 파이프라인 (구성 요소별. A와 B에 대해 각각 실행)

1. **평균 근점각.**
   `M = 2π(t − T) / P` (mod 2π로 축소)

2. **이심 근점각.** `M = E − e sin E` 풀기 (Markley 방법, `e ≈ 0.9`에서도 안정적).

3. **진 근점각과 궤도 반경.**
   ```
   ν = 2 · atan2( √(1+e) sin(E/2), √(1−e) cos(E/2) )
   r = a (1 − e cos E)
   ```

4. **근일점 기준 상태** (궤도면. `x̂` → 근일점, `ŷ` 90° 전방).
   ```
   x_p = r cos ν                            y_p = r sin ν
   n   = 2π / P
   vx_p = −(n·a/√(1−e²)) sin E              vy_p = (n·a/√(1−e²)) · √(1−e²) cos E
   ```
   단위. `a`는 AU, `P`는 년 → 속도는 AU/yr. 4.74047을 곱하면 km/s.

5. **Thiele-Innes 회전 → 하늘 프레임.** Thiele-Innes 상수
   (`A, B, F, G, C, H`)는 `ω, Ω, i, a`를 하나로 인코딩함.
   ```
   A = a ( cos ω cos Ω − sin ω sin Ω cos i)
   B = a ( cos ω sin Ω + sin ω cos Ω cos i)
   F = a (−sin ω cos Ω − cos ω sin Ω cos i)
   G = a (−sin ω sin Ω + cos ω cos Ω cos i)
   C = a · sin ω · sin i
   H = a · cos ω · sin i
   ```
   그러면 (위치, Hilditch / Pourbaix 컨벤션 — `build_systems.py:_thiele_innes_per_unit_a` + `solve_orbit_relative` 와 일치).
   ```
   ΔN = (A/a)·x_p + (F/a)·y_p     (북, +Dec)
   ΔE = (B/a)·x_p + (G/a)·y_p     (동, +RA)
   ΔW = (C/a)·x_p + (H/a)·y_p     (관측자 반대 방향)
   ```
   속도에는 **동일한 행렬**을 `(vx_p, vy_p)`에 적용함.

   Thiele-Innes 행렬은 길이 보존이므로 `√(ΔN² + ΔE² + ΔW²) = r` (step 3 의 궤도 반지름).

6. **무게중심 방향을 통한 ICRS 변환.** 무게중심의 RA/Dec `(α, δ)`에서 단위 벡터 계산.
   ```
   r̂_los = ( cos δ cos α,  cos δ sin α,  sin δ )
   N̂     = (−sin δ cos α, −sin δ sin α,  cos δ )
   Ê     = (−sin α,         cos α,        0     )
   ```
   상대 ICRS 위치. `r_rel = ΔN·N̂ + ΔE·Ê + ΔW·r̂_los`.
   질량비로 분리.
   ```
   q_A = M_B / (M_A + M_B)    q_B = M_A / (M_A + M_B)
   r_A_rel = − q_A · r_rel    r_B_rel = + q_B · r_rel
   ```
   (A는 B − A 벡터 기준으로 무게중심 반대편에 위치함.)
   속도도 동일하게 분리함.

7. **무게중심 전파.** 카탈로그 천문 측정값은 보통 J2016.0 (Gaia DR3) 또는 J1991.25
   (Hipparcos) 기준임. `astropy.coordinates.SkyCoord.apply_space_motion`을 사용하여
   무게중심 ICRS 상태를 `JD2433282.5`로 전파함.

8. **최종 조합.**
   ```
   r_A(t) = R_bary(t) + r_A_rel(t)        v_A(t) = V_bary(t) + v_A_rel(t)
   r_B(t) = R_bary(t) + r_B_rel(t)        v_B(t) = V_bary(t) + v_B_rel(t)
   ```

이 벡터들이 HORIZONS 상당 상태 벡터임. Principia의 `principia_initial_state` body
블록에 직접 입력할 수 있음.

---

## 3. 카탈로그 접근 — USNO/GSU orb6

### URL

| 자료 | URL | 비고 |
|---|---|---|
| 형식 명세 | `http://www.astro.gsu.edu/wds/orb6/orb6format.txt` | 먼저 읽을 것 |
| 메인 카탈로그 (고정폭) | `http://www.astro.gsu.edu/wds/orb6/orb6orbits.txt` | 단일 정보 출처 |
| 노트 파일 | `http://www.astro.gsu.edu/wds/orb6/orb6notes.txt` | 궤도별 주석 |
| HTML 인덱스 | `http://www.astro.gsu.edu/wds/orb6.html` | 브라우징 전용 |

**VizieR 미러.** `B/orb6` (카탈로그 "Sixth Catalog of Orbits of Visual Binary
Stars"). 메인 테이블 `B/orb6/orb6orbits`. TAP 엔드포인트
`https://tapvizier.cds.unistra.fr/TAPVizieR/tap`. 상류 대비 수개월 지연됨. 대량
ADQL 쿼리에는 VizieR를 사용하고, 최신 grade-1 결과에는 GSU 파일을 사용할 것.

공식 CSV/TSV는 없음. 열 명세 표를 참고하여 고정폭 파싱.

### 필드 맵 (고정폭 바이트 범위, 1-indexed inclusive)

| 필드 | 바이트 | 타입 | 비고 |
|---|---|---|---|
| WDS 지정자 | 1–10 | A10 | `06451-1643` |
| 발견자 코드 | 19–25 | A7 | `AGC  1` (Sirius) |
| HD 번호 | 38–43 | I6 | |
| Hipparcos 번호 | 45–50 | I6 | |
| `P` (공전 주기) | 81–91 | F11.6 | 값 |
| `P_unit_code` | 92 | A1 | 아래 참조 |
| `a` (반장축) | 105–112 | F8.4 | 값 |
| `a_unit_code` | 113 | A1 | 아래 참조 |
| `i` (기울기) | 126–133 | F8.3 | 도 |
| `Ω` (교점) | 143–150 | F8.3 | 도 |
| `Ω_node_marker` | 151 | A1 | RV로 승교점 해소 시 `*` |
| `T` (근일점 에포크) | 162–173 | F12.6 | 값 |
| `T_unit_code` | 174 | A1 | 아래 참조 |
| `e` (이심률) | 188–195 | F8.6 | `0 ≤ e < 1` |
| `ω` (근일점 편각) | 206–213 | F8.3 | 별도 표기 없으면 반성 기준 |
| 분점 | 233–236 | A4 | 보통 `1900`/`1950`/`2000` |
| 등급 | 238 | I1 | 1–5 |
| 참고문헌 코드 | 246–253 | A8 | bibcode 유사 형식 |
| 노트 플래그 | 255 | A1 | `orb6notes.txt`에 항목 있으면 `N` |

**주의.** 바이트 오프셋은 버전마다 ±1씩 달라질 수 있음. 항상 **현재**
`orb6format.txt`와 대조 확인할 것. 이 표는 시작 템플릿으로만 사용할 것.

### 단위 코드 표

**주기 (col 92).**

| 코드 | 의미 | 연(year)으로 변환 |
|---|---|---|
| `m` | 분 | `P / (60·24·365.25)` |
| `h` | 시간 | `P / (24·365.25)` |
| `d` | 일 | `P / 365.25` |
| `y` | 연 (가장 일반적) | `P` |
| `c` | 세기 | `P · 100` |

**반장축 (col 113).**

| 코드 | 의미 | 각초(arcsec)로 변환 |
|---|---|---|
| `a` | 각초 (가장 일반적) | `a` |
| `m` | 밀리각초 | `a / 1000` |
| `M` | 각분 | `a · 60` |
| `u` | 마이크로각초 | `a / 1e6` |

**근일점 에포크 (col 174).**

| 코드 | 의미 | JD (TT)로 변환 |
|---|---|---|
| `y` | Besselian 년 (예. `1894.130`) | `JD = 2415020.31352 + (B−1900)·365.242198781` |
| `m` | 수정 줄리안 날짜 | `JD = MJD + 2400000.5` |
| `d` | 절단 JD | `JD = T + 2400000` |

참고. `y`는 역사적으로 Besselian이지만, 2010년 이후 항목은 Julian 년을 의미하는 경우도 있음.
`y`이면서 2000년 이후 에포크이면 Julian을 의심하고 참고문헌 논문을 확인할 것.

### 등급 필터

| 등급 | 의미 | NearStars 정책 |
|---|---|---|
| 1 | 확정 — 여러 주기 관측, 잔차 양호 | 사용, `phase_reliable: true` |
| 2 | 양호 — 궤도의 대부분 관측 | 사용, `phase_reliable: true` |
| 3 | 신뢰 — 절반 이상 관측 | 사용, `phase_reliable: true` |
| 4 | 예비 — 소수만 관측, P 불확실 | 요소 사용, `phase_reliable: false` |
| 5 | 불확정 — 추측성, P 종종 가정 | **궤도 건너뜀**, 정적 CPM 쌍으로 처리 |

기준. `grade ≤ 3` ⇒ 1950 위상 신뢰. Grade 4 ⇒ 요소는 포함하되 플래그 표시.
Grade 5 ⇒ 카탈로그 기준 에포크에서 관측된 PA/sep를 사용하는 정적 분리 벡터로 격하.

---

## 4. 카탈로그 접근 — Gaia DR3 NSS

### 테이블

| 테이블 | 용도 |
|---|---|
| `gaiadr3.nss_two_body_orbit` | **주 테이블.** 완전한 케플러 궤도, Thiele-Innes 상수, SB1/SB2/천문 측정 해 |
| `gaiadr3.nss_acceleration_astro` | 가속도 해 — 주기 없음, 상태 벡터에 사용 불가 |
| `gaiadr3.nss_non_linear_spectro` | 천문 측정 성분 없는 SB 궤도 — 단독으로는 보통 사용 불가 |
| `gaiadr3.nss_vim_fl` | 변광 유발 이동성 — 특수 케이스, 건너뜀 |

시차, PM, RV, G 등급을 얻기 위해 `source_id` 기준으로 `gaiadr3.gaia_source`에 조인.
Hipparcos와 크로스 매칭 시 `gaiadr3.hipparcos2_best_neighbour` 사용.

### `nss_two_body_orbit`의 주요 열

| 물리량 | 열 | 단위 | 비고 |
|---|---|---|---|
| 소스 ID | `source_id` | — | 조인 키 |
| 해 유형 | `nss_solution_type` | 문자열 | 필터용 |
| 주기 | `period` | 일 | 연으로 변환 |
| 근일점 에포크 | `t_periastron` | 일, Gaia 내부 기준점으로부터의 오프셋 | JD 아님 — 문서 주의 깊게 확인 |
| 이심률 | `eccentricity` | — | |
| 기울기 | `inclination` | 도 | SB1 전용이면 NaN |
| 근일점 편각 | `arg_periastron` | 도 | 반성 기준 (ω₂) |
| 교점 | `nodeangle` | 도 | 구 문서에서는 `node`로 표기되기도 함 |
| 반장축 (천문 측정, 광심) | `semi_major_axis` | mas | |
| RV 반진폭 | `rv_semiamplitude_primary` / `_secondary` | km/s | SB 해 |
| 질량비 | `mass_ratio` | — | SB2 전용 |
| 무게중심 시차 | `parallax` | mas | 이 값 사용, `gaia_source.parallax` 사용하지 말 것 |
| 무게중심 PM | `pmra`, `pmdec` | mas/yr | |
| Thiele-Innes | `a_thiele_innes`, `b_thiele_innes`, `f_thiele_innes`, `g_thiele_innes` | mas | A, B, F, G만 공개 — C, H는 미공개 |

파싱할 때마다 공식 데이터모델 페이지에서 정확한 열 이름을 확인할 것.
`https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_non-single_stars_tables/ssec_dm_nss_two_body_orbit.html`

### 사용 가능한 `nss_solution_type` 값

| `nss_solution_type` | 천문 측정 여부 | i, Ω 제공 여부 | 사용 여부 |
|---|---|---|---|
| `Orbital` | 예 | 예 | **사용 — 최선** |
| `OrbitalTargetedSearch` | 예 | 예 | **사용** |
| `OrbitalTargetedSearchValidated` | 예 | 예 | **사용** |
| `AstroSpectroSB1` | 예 | 예 (+RV로 교점 해소) | **사용 — 교점 거울 자동 해소** |
| `SB1` | 분광 전용 | 아니오 | 보완 데이터 없으면 건너뜀 |
| `SB2` | 분광 전용 | 아니오 | 보완 데이터 없으면 건너뜀 |
| `EclipsingBinary` | 아니오 | 부분 | 궤도 계산에는 건너뜀 |
| `Acceleration7/9` | 아니오 | 아니오 | **건너뜀** |
| `FirstDegreeTrendSB1` | 아니오 | 아니오 | **건너뜀** |

```sql
WHERE nss_solution_type IN (
  'Orbital',
  'OrbitalTargetedSearch',
  'OrbitalTargetedSearchValidated',
  'AstroSpectroSB1'
)
```

### C, H 채우기 (Gaia는 A, B, F, G만 공개)

**경로 1 — Campbell 열 직접 읽기 (권장).**
`Orbital`/`OrbitalTargetedSearch` 행에서 Gaia DR3는 Thiele-Innes 상수와 함께
`inclination`, `arg_periastron`, `nodeangle`을 공개함. 이를 직접 사용한 뒤.
```
C = a · sin(ω) · sin(i)
H = a · cos(ω) · sin(i)
```

**경로 2 — Thiele-Innes에서 Campbell 복원 (대안).**
Campbell 열이 NULL인 경우.
```
u = (A² + B² + F² + G²) / 2
v = A·G − B·F
ω+Ω = atan2( B − F,  A + G)
ω−Ω = atan2(−B − F,  A − G)
ω   = ((ω+Ω) + (ω−Ω)) / 2
Ω   = ((ω+Ω) − (ω−Ω)) / 2
a   = sqrt( u + sqrt(u² − v²) )
i   = 2 · atan( sqrt( (u − sqrt(u²−v²)) / (u + sqrt(u²−v²)) ) )
```
그 후 위의 수식으로 C, H를 계산함.

경로 2의 `ω − Ω` 사분면이 교점 거울 모호성임. Gaia의 Campbell 열(공개된 경우)은
이미 선택이 이루어진 것이므로, 다른 소스와 교차 확인 시 달리 나타나지 않는 한 신뢰할 것.

---

## 5. 시스템별 표준 논문 (orb6보다 우선)

유명한 근방 성계에는 orb6 대신 전용 논문을 사용할 것.

| 성계 | 표준 참고문헌 |
|---|---|
| α Cen AB | Akeson et al. 2021, AJ 162, 14 |
| Proxima → α Cen 무게중심 | Kervella, Thévenin, Lovis 2017, A&A 598 L7 |
| Sirius AB | Bond et al. 2017, ApJ 840, 70 |
| Procyon AB | Bond et al. 2015, ApJ 813, 106 |
| 61 Cyg AB | Malkov et al. 2012 / Gorshanov et al. 2006 |
| Luyten 726-8 (UV + BL Cet) | Geyer 1975, Kervella 2016으로 정밀화 |

항상 DB 항목의 `source` 필드에 출처를 명시할 것
(예. `"akeson_2021"`, `"orb6:grade=1"`, `"gaia_dr3_nss:Orbital"`).

---

## 6. 삼중성계 처리

### 계층적 야코비 분해

안정적인 삼중성계는 항상 계층적 구조를 가짐. 두 개의 독립적인 케플러 문제로 분해함.

```
          (AB+C 무게중심, "G")
                  |
           +------+------+
           |             |
        (AB 무게중심)      C
          "g"   |
            +---+---+
            |       |
            A       B
```

- **내부 궤도.** `g` (AB 무게중심) 주변의 A와 B. 질량비에 M_A, M_B 사용.
- **외부 궤도.** `G` 주변의 `g` (질량 `M_A + M_B`인 점질량으로 처리)와 C. 질량비에 `M_AB = M_A + M_B` vs `M_C` 사용.

### 합성

```
r_inner = 내부 요소에 대한 Kepler/T-I 파이프라인의 (B − A) 벡터
r_outer = 외부 요소에 대한 Kepler/T-I 파이프라인의 (C − g) 벡터

r_A_from_g = − (M_B  / M_AB)    · r_inner
r_B_from_g = + (M_A  / M_AB)    · r_inner
r_g_from_G = − (M_C  / M_total) · r_outer
r_C_from_G = + (M_AB / M_total) · r_outer

r_A_ICRS = R_bary + r_g_from_G + r_A_from_g
r_B_ICRS = R_bary + r_g_from_G + r_B_from_g
r_C_ICRS = R_bary + r_C_from_G
```

속도도 동일하게 합성함.

### 광시야 CPM 동반성 (궤도 미결정)

궤도 결과가 없는 넓은 공통 고유 운동 동반성 (일반적으로 ρ > 5″, P > 1000 yr)의 경우.

- JD2433282.5 에포크에서의 궤도 운동은 생략함.
- 카탈로그 기준 에포크에서 관측된 `(ρ, θ)`로부터 구한 내부 성계 대비 고정 오프셋에 배치.
- 주성의 계통 고유 운동과 시선 속도를 공유함.
- `orbit_type: "static_cpm"`으로 플래그 표시, LOS 성분은 추정값으로 표시.

```python
sep_au  = rho_arcsec * (1000.0 / parallax_mas)   # small-angle, parsec definition
delta_N =  sep_au * cos(radians(theta_deg))
delta_E =  sep_au * sin(radians(theta_deg))
delta_W =  0.0   # unknown
```

### 스키마 참조

`binary_orbits.json` 의 전체 스키마 — 컴포넌트 / 궤도 필드 표, 조건부 필수
규칙 (`primary` vs `primary_is_barycenter_of`, `a_arcsec` vs `a_au`,
`phase_reliable=true` 일 때만 `T_jd_tt`), 하이브리드 천체측정 저장
(컴포넌트 수준의 `astrometry_source` 규칙 + 시스템 수준
`barycenter_astrometry` 블록, 컴포넌트당 좌표값은 저장하지 않음) — 은
[`methodology.md §다중성계 에포크`](methodology.md#다중성계-에포크) 에서
정의됩니다. 본 문서의 수학은 그 스키마가 요구하는 값을 산출합니다.

---

## 7. 코드 스니펫

### 7a. 케플러 솔버 (PyAstronomy MarkleyKESolver)

```python
from PyAstronomy.pyasl import MarkleyKESolver
solver = MarkleyKESolver()  # 닫힌 형식 Padé + Halley 스텝. e → 1에서도 안정적
# 입력: M은 라디안, e는 [0, 1)
# 출력: E는 라디안, M과 동일한 분기
E = solver.getE(M, e)   # solver.solveKE가 아님 — 구 API 이름
# e = 0.9, M = 1.0 rad일 때: E ≈ 1.8607 rad을 마이크로초 단위로 반환
```

Markley는 비반복적이며 `e > 0.8`에서도 안정적임. `e ≥ 0.99`이면 보편 변수
공식으로 전환할 것. orb6에는 해당하는 시스템이 거의 없음.

### 7b. Thiele-Innes 회전 (numpy)

```python
import numpy as np

def perifocal_to_sky(x_p, y_p, vx_p, vy_p, A, B, F, G, C, H):
    """Perifocal (AU, AU/yr) -> sky-frame (N, E, W) relative offset and velocity.
       A..H here are dimensionless per-unit-a Thiele-Innes constants.
       Row convention: A,F -> N ; B,G -> E ; C,H -> W (line of sight).
    """
    M = np.array([[A, F],   # North
                  [B, G],   # East
                  [C, H]])  # away from observer
    pos = M @ np.array([x_p,  y_p])
    vel = M @ np.array([vx_p, vy_p])
    return pos, vel
```

전치된 M 버그는 쌍성 궤도 코드에서 가장 흔히 발생하는 침묵의 오류임.
항상 소스 논문의 어떤 상수가 East-계수이고 어떤 것이 North-계수인지 라벨링을
교차 확인할 것.

### 7c. 무게중심 전파 (astropy)

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time

bary_now = SkyCoord(
    ra            = 219.9020833 * u.deg,
    dec           = -60.8339722 * u.deg,
    distance      = (1000.0 / 750.81) * u.pc,   # parallax_mas -> pc
    pm_ra_cosdec  = -3679.25 * u.mas / u.yr,    # Gaia pmra is already cos(δ)-multiplied
    pm_dec        =   473.67 * u.mas / u.yr,
    radial_velocity = -22.39 * u.km / u.s,
    obstime       = Time('J2016.0', scale='tcb'),   # Gaia DR3 ref epoch is TCB
    frame         = 'icrs',
)
bary_1950 = bary_now.apply_space_motion(new_obstime=Time('1950-01-01', scale='tdb'))
# bary_1950.cartesian.xyz  -> ICRS position
# bary_1950.velocity       -> ICRS velocity
```

### 7d. 각도 분리 → 시차를 통한 AU 변환

```python
def arcsec_sep_to_au(sep_arcsec, parallax_mas):
    """Exact by parsec definition: 1 pc * 1 arcsec = 1 AU."""
    distance_pc = 1000.0 / parallax_mas
    return sep_arcsec * distance_pc

def gaia_ti_mas_to_au(ti_mas, parallax_mas):
    """Thiele-Innes constants in mas / parallax in mas -> AU directly."""
    return ti_mas / parallax_mas
```

### 7e. RV를 통한 교점 거울 해소

```python
import numpy as np
from PyAstronomy.pyasl import MarkleyKESolver

def predicted_rv_secondary(t, T, P, e, omega_deg, K2_kms, gamma_kms):
    """SB1 secondary RV at time t."""
    M = (2 * np.pi * (t - T) / P) % (2 * np.pi)
    E = MarkleyKESolver().getE(M, e)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))
    w = np.radians(omega_deg)
    return gamma_kms + K2_kms * (np.cos(nu + w) + e * np.cos(w))

def resolve_node_mirror(t_rv, rv_obs, T, P, e, i_deg, omega_deg, Omega_deg,
                        K2_kms, gamma_kms):
    rv_A = predicted_rv_secondary(t_rv, T, P, e,  omega_deg,        K2_kms, gamma_kms)
    rv_B = predicted_rv_secondary(t_rv, T, P, e, (-omega_deg) % 360, K2_kms, gamma_kms)
    if abs(rv_A - rv_obs) <= abs(rv_B - rv_obs):
        return i_deg, omega_deg, Omega_deg, "primary_branch"
    return 180 - i_deg, (-omega_deg) % 360, (Omega_deg + 180) % 360, "mirror_branch"
```

K2는 두 분기 모두에서 양수로 유지됨 — ω만 (위상 변화를 담아) 부호가 바뀌고,
i도 함께 바뀜.

---

## 8. 무게중심 천문 측정 — 결정 트리

세 가지 옵션.
- **(A)** 주성의 단일 성분 천문 측정 + 케플러 오프셋
- **(B)** 두 구성 요소의 단일 성분 천문 측정값을 질량 가중 평균
- **(C)** 전용 무게중심 해 (Hipparcos 다중성 부록, Gaia NSS)

```
Gaia DR3 NSS Orbital / AstroSpectroSB1 행이 있는가?
├── YES → 옵션 C: nss_two_body_orbit.parallax / pmra / pmdec 사용
│         (구조적으로 무게중심 기준)
│
└── NO  → 쌍이 분해되어 있는가 (분리 > Gaia 분해능 ≈ 0.4–1″)?
          ├── YES, 두 성분 모두 Gaia 5매개변수 해를 가짐
          │     → 옵션 B: 질량 가중 평균
          │         barycenter_PM      = (M_A·PM_A + M_B·PM_B) / (M_A + M_B)
          │         barycenter_parallax = 가중 평균 (보통 σ 이내)
          │       참고: P < 20 yr이면 각 성분의 PM에 궤도 접선 속도가 포함됨.
          │       질량 가중 평균으로 이것이 상쇄됨 — 옵션 B가 옳으며, 편법이 아님.
          │
          └── NO (미분해, 단일 Gaia 행)
                ├── Hipparcos 다중성 해 사용 가능
                │   (DMSA 플래그 'C', 'O', 'V', 'X')
                │   └── YES → 옵션 C': Hipparcos 무게중심 해 사용.
                │             가능하면 장기 기선 정밀도를 위해
                │             Gaia DR3의 PM으로 업데이트
                │
                └── NO → 옵션 A (주의 포함): Gaia gaia_source 천문 측정은
                        광심(photocenter) 해임. 광심 흔들림이 중요한 경우.
                          • P < 10 yr  AND  플럭스 비 < 10  AND  a_photo > 0.1 mas
                          • PM/시차에 일관된 ~0.1–1 mas 진동 추가
                          • 1950 시점 위치 오차: 최대 (PM_error · 66 yr)
                            ≈ 가장 가까운 미분해 쌍에서 60 mas
                        astrometry_quality: "photocenter_contaminated" 플래그 표시.
```

참고.
- **광심 흔들림 vs Gaia 임무 기간 (~5–10 yr).** `P < mission`일 때 중요함. `5 < P < 30 yr`이면
  PM/시차에 누출됨. `P > 50 yr`이면 PM에 흡수되는 느린 드리프트로 나타남 (편향되지만 탐지 불가).
- **분해된 쌍 (>2″).** 각 성분이 자체 Gaia 5매개변수 해를 가짐.
  옵션 B 사용. 성분별 흔들림은 PM 오차보다 훨씬 작음.
- **Hipparcos 다중성 부록 (1997).** H59 필드 플래그 `C/O/V/X`를 가진 8542개 시스템.
  orb6의 HIP 번호를 통해 교차 참조.
- **아무것도 알려지지 않은 경우 기본값.** 분해되었으면 옵션 B, 그렇지 않으면 광심 오염
  플래그가 붙은 옵션 A.

---

## 9. 계산 예시 1 — JD2433282.5에서의 α Centauri AB

요소 (Akeson et al. 2021, ICRS J2000.0).

| 요소 | 값 |
|---|---|
| P | 79.762 yr |
| T | 1955.564 (Besselian) → JD 2435291.6 |
| e | 0.51947 |
| a | 17.4930 arcsec |
| π | 750.81 mas → d = 1.3319 pc → a = 23.300 AU |
| i | 79.2430° |
| ω | 231.519° |
| Ω | 205.073° |
| M_A | 1.0788 M☉ |
| M_B | 0.9092 M☉ |
| q_A | M_B/M_tot = 0.4574 |
| q_B | M_A/M_tot = 0.5426 |

J2019.5 기준 무게중심 (ICRS): α = 14h 39m 36.494s, δ = −60° 50′ 02.37″,
μ_α* = −3639.95 mas/yr, μ_δ = +700.40 mas/yr, v_r = −22.3796 km/s.

### `t = JD2433282.5`에서의 계산 단계

```
1. Δt_yr = (2433282.5 − 2435291.6) / 365.25 = −5.500 yr
2. M  = 2π · (−5.500 / 79.762) = −0.4334 rad   (≡ 335.18°)
3. E  ≈ −0.7728 rad        (Markley solver)
4. ν  ≈ −1.1782 rad        r = 23.300·(1 − 0.51947·cos(−0.7728)) = 14.61 AU
5. Perifocal:
     n = 2π / 79.762 = 0.07879 rad/yr
     n·a / √(1−e²) = 2.1487 AU/yr
     x_p =  +5.587 AU      y_p = −13.50 AU
     vx_p = +1.985 AU/yr   vy_p = +1.932 AU/yr
6. Thiele-Innes (per-unit-a):
     A/a = +0.5021   F/a = −0.7578
     B/a = +0.3971   G/a = −0.4377
     C/a = −0.7683   H/a = −0.6121
7. Sky-frame relative (B − A):
     ΔN = +13.04 AU    vN = −0.467 AU/yr
     ΔE =  +8.13 AU    vE = −0.058 AU/yr
     ΔW =  +3.97 AU    vW = −2.708 AU/yr
   → B는 1950-01-01 기준 시선 방향으로 A보다 약 4 AU 뒤에 위치함.
```

ICRS에 임베드하는 방법.
- `SkyCoord.apply_space_motion`으로 무게중심 천문 측정값을 J2019.5에서 JD2433282.5로
  전파 (시선 방향 운동으로 거리 ~328 AU 변화).
- 1950 기준 RA/Dec에서 `N̂, Ê, r̂_los` 구축.
- `q_A, q_B`로 분리하고 `R_bary, V_bary` 더함.

---

## 10. 계산 예시 2 — JD2433282.5에서의 Sirius AB

요소 (Bond et al. 2017, Table 5. ICRS J2000.0).

| 요소 | 값 |
|---|---|
| P | 50.1284 yr |
| T | 1994.5715 (Besselian) — **참고: 자주 인용되는 "1894.13"은 한 주기 이전이며 위상은 동일** |
| e | 0.59142 |
| a | 7.4957 arcsec |
| π | 379.21 mas → d = 2.6371 pc → a = 19.766 AU |
| i | 136.336° |
| ω | 149.161° (J2000) |
| Ω | 45.400° (J2000) |
| M_A | 2.063 M☉ |
| M_B | 1.018 M☉ |

### `t = JD2433282.5`에서의 계산 단계 (사용자 제공 기준값 T = 1894.13 사용. T = 1994.5715와 위상 동일)

```
1. Δt = 55.871 yr     N_periods = 55.871 / 50.1284 = 1.1146
   Phase = 0.1146 past periastron
2. M = 2π · 0.1146 = 0.7200 rad   (≈ 41.25°)
3. Newton iteration: E₀ = 1.1098, E₁ = 1.2994, E₂ = 1.2882
   E ≈ 1.2881 rad   (73.81°)
4. ν = 2 · atan2( √1.59142·sin(0.6441), √0.40858·cos(0.6441) )
      = 2 · atan2( 0.7577, 0.5111 )
      = 1.9526 rad   (111.87°)
   r/a = 1 − e·cos E = 1 − 0.59142·0.2785 = 0.8353
   r = 0.8353 · 19.766 = 16.510 AU
5. Perifocal:
     n = 2π/50.1284 = 0.12534 rad/yr
     n·a/√(1−e²) = 3.0728 AU/yr,  with √(1−e²) = 0.8061
     x_p = 16.510 · cos(1.9526) = −6.155 AU
     y_p = 16.510 · sin(1.9526) = +15.321 AU
     vx_p = −3.0728 · sin(1.2881) = −2.953 AU/yr
     vy_p = +2.4773 · cos(1.2881) = +0.6872 AU/yr
6. Thiele-Innes (per-unit-a, with ω=149.161°, Ω=45.400°, i=136.336°):
     cω = −0.8587   sω = +0.5125
     cΩ = +0.7022   sΩ = +0.7120
     ci = −0.7235   si = +0.6903

     A/a = cω·cΩ − sω·sΩ·ci = −0.3390
     B/a = cω·sΩ + sω·cΩ·ci = −0.8718
     F/a = −sω·cΩ − cω·sΩ·ci = −0.8023
     G/a = −sω·sΩ + cω·cΩ·ci = +0.0714
     C/a = sω·si = +0.3538
     H/a = cω·si = −0.5928
7. Sky-frame relative (B − A), Hilditch 컨벤션:
     ΔN = (A/a)·x_p + (F/a)·y_p
        = (−0.3390)(−6.155) + (−0.8023)(15.321) = +2.087 − 12.292 = −10.20 AU
     ΔE = (B/a)·x_p + (G/a)·y_p
        = (−0.8718)(−6.155) + (0.0714)(15.321) = +5.366 + 1.094 = +6.46 AU
     ΔW = (C/a)·x_p + (H/a)·y_p
        = (0.3538)(−6.155) + (−0.5928)(15.321) = −2.178 − 9.082 = −11.26 AU

     vN = (−0.3390)(−2.953) + (−0.8023)(0.6872) = +1.001 − 0.551 = +0.450 AU/yr
     vE = (−0.8718)(−2.953) + (0.0714)(0.6872)  = +2.574 + 0.049 = +2.624 AU/yr
     vW = (0.3538)(−2.953) + (−0.5928)(0.6872)  = −1.045 − 0.407 = −1.452 AU/yr

   |Δr| = √(10.20² + 6.46² + 11.26²) ≈ 16.51 AU  (step 4 의 r = 16.510 과 일치)
8. 합리성 검사:
   T = 1894.13은 근일점 통과를 1894.13 + n·50.13에 배치함. 가장 가까운
   통과: 1944.26과 1994.39. 따라서 1950-01-01은 1944 근일점 약 5.74 yr 이후 —
   근일점 직후 팽창 단계임. 계산된 r = 16.5 AU는 이 구간과 일치함.
   (주의: "1940년대 Sirius B가 A의 광망 속으로 사라졌다"는 설명은 i = 136°에서
   r이 증가하더라도 수축하는 투영 각도 분리를 가리킴. 1940년대 중반의 물리적
   거리는 ~9 AU이며, 1969년경 근점에서 ~31 AU로 증가함.)
   Bond+ 2017의 T = 1994.5715 직접 사용: 위상
   = (1950.0 − 1994.5715)/50.1284 = −0.889 ≡ 0.111 (mod 1) — 동일한 답.
```

반올림 오차 예산.
- 단계 3 Newton 절단: ~10⁻⁴ rad → ~0.01 AU
- 단계 6 삼각함수 절단: ~10⁻⁴ → 위치에서 ~0.05 AU
- 전체 수치 잡음 ~0.1 AU. 요소 불확실도 (a ±0.03%, T ±0.006 yr)는
  근일점 부근에서만 지배적.

---

## 11. 알려진 함정

### 시간 척도 및 에포크 규약
- **Besselian vs Julian 년.** `B → JD = 2415020.31352 + (B−1900)·365.242198781`.
  `J → JD = 2451545.0 + (J−2000)·365.25`. 1900년에는 일치하며, 2000년까지 ~0.013 d,
  1894년까지 ~0.03 d 차이.
- **orb6의 `y` 모호성.** 역사적으로 Besselian이나 2010년 이후 항목은 Julian을 의미하는
  경우도 있음. 판단이 어려운 경우 참고문헌 논문 확인.
- **JD 에포크의 TDB vs UTC.** TT − UTC = 1950년에 +29 s, 2025년에 +69 s.
  궤도 위상에는 무시할 수 있는 수준이나 astropy에서 항상 `scale=`을 명시적으로 설정할 것
  (`Time(..., scale='tdb')`). 기본값 사용 금지.
- **Ω, ω의 분점.** 1990년 이전 orb6 항목은 B1950, 최근 항목은 J2000,
  Gaia NSS는 사실상 ICRS 기준. B1950→J2000 세차 운동으로 Ω가 ~0.64° 회전함.
  항상 J2000/ICRS로 세차 변환하고 원래 분점을 메타데이터로 저장할 것.
- **Gaia 기준 에포크.** DR3 = J2016.0 (TCB), DR2 = J2015.5, DR1 = J2015.0.
  Hipparcos = J1991.25. 카탈로그 메타데이터에서 읽어오며, 절대 하드코딩하지 말 것.

### 천문 측정 / 역학
- **기울기 규약.** 시각 쌍성과 천문 측정 해는 `i ∈ [0°, 180°]` 사용 (직행 vs 역행 구분 가능).
  SB 전용 궤도는 흔히 `i ∈ [0°, 90°]` 사용 (역행 방향 없음 — 교점 거울임).
  절대 i를 [0°, 90°]으로 정규화하지 말 것 — 정보가 손실됨.
- **대원 위의 고유 운동, 평면이 아님.** 선형 외삽 `α + μ·t`의 오차는
  `~μ²·t² / sin δ`. Sirius (δ ≈ −16.7°, μ_α ≈ 546 mas/yr)에서 66 yr 동안: ~1.4″.
  눈에 띄는 수준임. `SkyCoord.apply_space_motion` 사용. Δt > 10 yr인 경우
  절대 직접 구현하지 말 것. 극점 근처 (Polaris)에서는 선형 형식이 의미 없으므로
  단위 벡터 전파 필요.
- **광행시 및 광행차.** 연간 광행차는 Gaia ICRS에 이미 반영됨.
  궤도를 가로지르는 광행시: Sirius (a = 20 AU)는 3 h / 50 yr =
  7·10⁻⁶ 위상. 무시할 수 있음.

### 규약 함정
- **ω₂ vs ω₁.** orb6, Gaia DR3 NSS, Hipparcos DMSA 모두 **반성** (ω₂)의 근일점 편각을
  공개함. 일부 구식 SB 논문은 ω₁ = ω₂ + 180°를 게재함. 불분명한 경우 문서화하고 orb6 신뢰.
- **질량비 규약.** A = 밝은 주성, B = 반성. `q = M_B/M_A`, `0 < q ≤ 1`.
  Sirius A (주계열성)가 Sirius B (백색 왜성)보다 밝으므로, 근방 성계에서는 레이블이
  간단함.
- **Gaia NSS `inclination` 단위.** 도, 라디안이 아님. 시각 쌍성과 동일한 규약
  (`i=0` face-on, `i=90` edge-on). 데이터모델 페이지에서 확인할 것 —
  TAP 단위 메타데이터가 잘못된 경우가 있음.

### 부동소수점 및 수치
- 항상 `atan2(y, x)` 사용. `atan(y/x)` 절대 사용 금지 — ν 변환에서 사분면이 중요함.
- M, E, ν를 하나의 규약([0, 2π) 또는 [−π, π))으로 일관되게 처리할 것.
- 거의 원형 궤도 (e < 10⁻³): ω가 비정의가 되고, T가 위상에 종속적으로 됨.
  비특이 요소로 전환할 것 (h = e·sin(ω+Ω), k = e·cos(ω+Ω), λ = M+ω+Ω).
  orb6는 e < 0.01을 공개하지 않지만 Gaia NSS는 간혹 공개함.
- 고이심률 (e > 0.95): Newton-Raphson이 진동함. Markley 솔버가 처리하므로
  직접 구현하지 말 것.

### 위치 vs 궤도 분점
(Ω, ω)가 J2000으로 세차 변환되었더라도 별의 (α, δ)는 다른 분점 기준 (구식
Hipparcos 시대 논문에서는 B1950)일 수 있음. B1950 RA/Dec를 J2000 (Ω, ω)과 혼합하면
0.64° 회전되었지만 잘못된 하늘 위치에 고정된 궤도가 생성됨. DB에서 모든 것을
ICRS/J2000으로 세차 변환하고 원래 분점은 메타데이터로 저장할 것. 절대 혼용하지 말 것.

---

## 12. 파이프라인 요약

```
1.  궤도 요소 로드 (orb6 / 시스템별 논문 / Gaia DR3 NSS).
2.  단위 정규화: a→AU (시차를 통해), P→years, angles→radians,
    T→JD_TDB. 등급 검증 (그대로 사용은 ≥3, 4는 플래그, 5 → static).
3.  승교점 규약 결정 (orb6 '*' 표시 / 논문 / RV).
4.  단위 a당 Thiele-Innes (A,B,F,G,C,H) 계산 — 시스템별로 저장.
5.  t=JD2433282.5에서: 케플러 풀기 → (x_p, y_p, vx_p, vy_p).
6.  Thiele-Innes 회전 → (ΔN, ΔE, ΔW) 위치, (vN, vE, vW) 속도.
7.  에포크 t에서 무게중심 (α, δ)의 (N̂, Ê, r̂_los) 구축.
8.  질량비로 분리 → ICRS에서의 (r_A_rel, r_B_rel, v_A_rel, v_B_rel).
9.  카탈로그 기준 에포크에서 t로 무게중심 전파 (
    SkyCoord.apply_space_motion) → R_bary(t), V_bary(t).
10. r_X(t) = R_bary(t) + r_X_rel(t);   v_X(t) = V_bary(t) + v_X_rel(t).
11. binary_orbits.json (또는 동등한 파일)에 solar_system_epoch = JD2433282.5
    기준 ICRS 직교 좌표로 저장.
12. CFG 빌드 단계에서 principia_initial_state 내의
    `body { name = X; x = ...; vx = ... }` 블록 생성.
```

이 방법은 태양계 외 천체에 대한 HORIZONS의 "에포크 시점 정확한 상태" 기능을 재현함.
보간 없음, n체 역전파 없음. 궤도 결과 자체가 **전파기임**.

---

## 13. 출처

- mockingbirdnest/Principia repo, `astronomy/sol_initial_state_jd_2433282_500000000.cfg`
- RSS-Reborn/Sol-Configs: `Patches/Principia/Real_Sol-InitialState.cfg`
- CharonSSS/RSS-Origin-2 (v1.0.0): 바디별 `<Body>_Principia.cfg` 파일 (Patroclus, Lempo + Paha + Hiisi, Logos + Zoe, Ceto + Phorcys, Eurybates + Queta, Ida + Dactyl), `GameData/RSSOrigin2/MinorPlanets/.../` 하위에 위치
- USNO Sixth Catalog of Orbits of Visual Binary Stars: `http://www.astro.gsu.edu/wds/orb6.html`
  - 형식: `orb6format.txt`. 데이터: `orb6orbits.txt`. VizieR: `B/orb6`.
- Gaia DR3 NSS 데이터모델:
  `https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_non-single_stars_tables/ssec_dm_nss_two_body_orbit.html`
- Akeson et al. 2021, AJ 162, 14 (α Cen AB 정밀 궤도)
- Bond et al. 2017, ApJ 840, 70 (Sirius AB)
- Bond et al. 2015, ApJ 813, 106 (Procyon AB)
- Kervella, Thévenin, Lovis 2017, A&A 598 L7 (Proxima 궤도)
- Pourbaix 1995, BABel 152, 55 (Thiele-Innes 형식론)
- Halbwachs 2009, MNRAS 394, 1075 (시차 효과)
- orbitize reference implementation: `http://orbitize.info/en/latest/_modules/orbitize/kepler.html`
- PyAstronomy MarkleyKESolver:
  `https://pyastronomy.readthedocs.io/en/latest/pyaslDoc/aslDoc/keplerOrbitAPI.html`
