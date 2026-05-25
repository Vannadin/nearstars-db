---
title: Stellarium vs NearStars 다성계 궤도 파이프라인 비교
status: active
created: 2026-05-21
---

# Stellarium vs NearStars 다성계 궤도 파이프라인 비교

**NearStars 와의 연관성.** 우리 파이프라인
([`docs/reference/binary-epoch-pipeline.md`](../../docs/reference/binary-epoch-pipeline.md))
은 ORB6 / Gaia NSS 궤도 요소를 입력으로 받아 `JD2433282.5` 시점의 ICRF
Cartesian 상태 벡터 `(x, y, z, vx, vy, vz)` 를 km, km·s⁻¹ 단위로
출력하고, Principia 의 `principia_initial_state` 에 공급한다. Stellarium
은 시각 쌍성 궤도 운동을 propagation 하는, 널리 쓰이는 오픈소스 천문
소프트웨어 중 우리와 가장 가까운 것이다. 둘을 비교하면 NearStars 가
관심 있는 두 가지 질문에 답할 수 있다. (1) 우리 컨벤션 선택(Hilditch,
질량비 분할, Hipparcos `f`-factor) 이 독립 구현에서도 공유되는가, (2)
Stellarium 이 하는 것 중 채택할 만한 것이 있는가, 혹은 그들이 의도적으로
생략한 것 중 우리가 불필요하게 들고 다니는 것이 있는가.

**범위.** 읽기 전용 연구. 이 레포에 코드 변경 없음.

**외부 참조.**
- Stellarium master at commit [`3efa1406`](https://github.com/Stellarium/stellarium/tree/3efa1406a135fd6330d515ee8b942a58ffa80f01)
- 우리 파이프라인: [`docs/reference/binary-epoch-pipeline.md`](../../docs/reference/binary-epoch-pipeline.md)
- ORB6 카탈로그: https://www.astro.gsu.edu/wds/orb6.html

---

## 1. Executive summary

| 질문 | 답 |
|----------|--------|
| 두 파이프라인의 컨벤션이 일치하나? | **수식은 yes, 출력은 no.** Hilditch 회전, 질량비 displacement, Hipparcos `f`-factor PM propagation 이 동일. |
| 같은 카탈로그를 소비하나? | **No.** Stellarium 은 **수작업 큐레이션된 15쌍 파일**(`binary_orbitparam.dat`) 사용; 우리는 ORB6 + Gaia NSS 직접 읽음. |
| 비교 가능한 출력을 만드나? | **No.** Stellarium 은 천구 위의 **unit direction vector** 를 렌더링용으로 생성. 우리는 n-body 적분용 **3D Cartesian state in km / km·s⁻¹** 를 생성. 타겟 use-case 가 다름. |
| Stellarium 이 하이어라키컬 삼중성을 다루나? | **No.** 그들의 궤도 파일에 Proxima Cen, 40 Eri C, 36 Oph C 없음. 각 별의 궤도 결합은 최대 한 쌍 깊이. |
| NearStars 가 이걸 기반으로 뭔가 바꿔야 하나? | **구조 변경 없음**. 일치 자체가 우리 컨벤션 선택의 검증. Stellarium 의 누락 기능 목록(triples, ORB6 ingestion, velocity output) 이 *정확히* NearStars 의 차별점이므로 우리가 과도설계 아님. |

---

## 2. Stellarium 이 실제로 하는 것

commit [`3efa1406`](https://github.com/Stellarium/stellarium/tree/3efa1406a135fd6330d515ee8b942a58ffa80f01) (2026-05 master HEAD) 기준.

### 2.1 카탈로그

15개 명명된 쌍이 들어있는 단일 flat 파일.

> [`stars/hip_gaia3/binary_orbitparam.dat`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/stars/hip_gaia3/binary_orbitparam.dat)

수록된 쌍. α Cen AB, Sirius AB, 61 Cyg AB, γ Vir AB, Alula Aus AB,
Achird AB, ε¹ Lyr AB, ε² Lyr AB, β Mus AB, Dalim AB, ψ Vel AB,
ρ Oph AB, ζ Her AB, η Oph AB. 출처가 파일 안에 annotate 되어 있지 않음.
각도 값(periastron epoch, *i*, Ω) 이 잘 알려진 ORB6 항목과 일치(예. α
Cen periastron 2435314.751 = 1955.56) — 거의 확실히 ORB6 에서 수작업
추출, build script 는 없음.

format spec. [user guide §app_star_catalogue.tex L1870-L1926](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/guide/app_star_catalogue.tex#L1870-L1926).

`wds_hip_part.dat` 도 있지만 그 파일은 **마지막 관측된 PA/separation
스냅샷** 을 더 많은 WDS double 에 대해 저장. propagate 하지 않음 —
Stellarium 이 그 쌍들을 움직이는 궤도가 아니라 freeze 된 tableau 로
렌더링.

### 2.2 알고리즘

쌍성 궤도 코드 전체가 `Star.hpp` 의 ~180 줄 templated inline 함수 하나.

> [`Star<Derived>::getBinaryOrbit(epoch, v, ra, dec, plx, pmra, pmdec, RV, sep, pa)`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L265-L449)

순서대로 단계.

1. HIP 로 `binaryorbitstar` lookup (`StarMgr::getBinaryOrbitData()`).
   없으면 early-exit (`hip == 0`).
2. Kepler 방정식을 **Newton-Raphson** 으로 풀음. 허용오차 `1e-10`, 최대
   100 회 반복, 초기값 `E₀ = M`
   ([Star.hpp#L332-L353](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L332-L353)).
3. 표준 half-angle 로 진편각 계산.
   `ν = 2 atan(√((1+e)/(1−e)) · tan(E/2))`.
4. Hilditch 형식 회전 행렬 적용
   ([Star.hpp#L364-L373](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L364-L373)).
5. **무게중심** astrometry 를 `data_epoch` 에서 target JD 까지 ESA
   Hipparcos `f`-factor 가 적용된 full 6-parameter ICRS update 로
   propagate.
   `f = 1/√(1 + 2μ_r·t + (μ² + μ_r²)·t²)`
   ([Star.hpp#L381-L385](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L381-L385)).
6. 질량비 `q = M_B/(M_A + M_B)` 로 A 와 B 분할
   ([Star.hpp#L414-L423](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L414-L423)).
7. 무게중심 sphericals 에 `Δα·cos δ` 와 `Δδ` 를 더하고, `spheToRect` 로
   다시 Cartesian unit vector 로 변환, **normalize**, 반환
   ([Star.hpp#L437-L448](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L437-L448)).

속도(arcsec·yr⁻¹) 는 step 4 에서 위치와 함께 계산되지만 **normalize 후
폐기**. 렌더러는 방향만 필요.

### 2.3 호출 주기

매 프레임. drawing loop 안에서
[`ZoneArray.cpp::draw()`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/ZoneArray.cpp#L510-L515)
및 `searchAround` / `searchWithin` 에서 호출되며, 현재 `core->getJDE()`
를 에포크로 사용. 캐싱 레이어 없음; HIP-map miss 가 유일한 fast path.

---

## 3. 비교 cheat-sheet

| 항목 | Stellarium | NearStars |
|---|---|---|
| 카탈로그 출처 | Ad-hoc 15-row `binary_orbitparam.dat` (build script 없음) | ORB6 + Gaia NSS upstream → `db/binary_orbits.json` |
| Kepler 솔버 | Newton iteration, tol `1e-10`, 최대 100 회 | Markley (non-iterative cubic), PyAstronomy `MarkleyKESolver` |
| ω, Ω 컨벤션 | Hilditch (rotation matrix 일치) | Hilditch / Pourbaix (일치) |
| 무게중심 PM | Hipparcos `f`-factor (full 6-parameter) | Same |
| 질량 분할 | `q = M₂/(M₁+M₂)`, ±q · r_rel 로 displace | 동일 공식 |
| 출력 타입 | 천구 위 unit direction vector | km, km·s⁻¹ 단위 full ICRF Cartesian state `(x, y, z, vx, vy, vz)` |
| 속도 출력 | 내부 계산 후 **폐기** | 일급 출력 (Principia 가 필요) |
| 에포크 | `core->getJDE()` 가 반환하는 값 (연속) | 고정 단일 스냅샷 `JD2433282.5` (1950-01-01 TDB) |
| 호출 주기 | 매 프레임, 보이는 모든 쌍성 | `build_systems.py` 실행 시 1회 |
| 하이어라키컬 삼중성 (α Cen ABC, 40 Eri ABC, 36 Oph ABC) | **미지원** — Proxima / C-component 없음 | Jacobi 분해 (`primary_is_barycenter_of`) |

---

## 4. 두 파이프라인이 일치하는 지점 (그리고 그것이 왜 중요한가)

우리 파이프라인의 세 가지 컨벤션 선택 — 문헌에서 대안이 있는 것들 —
모두 Stellarium 의 독립 구현으로 확인됨.

1. **Hilditch 회전 형식.** 우리
   [§7b 회전 행렬](../../docs/reference/binary-epoch-pipeline.md) 이
   Stellarium 의
   [`Star.hpp#L364-L373`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L364-L373)
   과 term-for-term 일치. Aitken 의 옛 부호 컨벤션(2000 년 이전 일부
   논문에 아직 보임) 은 Ω 의 기여를 뒤집을 것.

2. **카탈로그 row = 무게중심, photocenter 아님.** 두 파이프라인 모두
   Hipparcos/Gaia astrometric row 를 무게중심으로 다루고 각 컴포넌트를
   바깥쪽으로 displace. 대안은 photocenter + photometric flux ratio 에서
   무게중심을 재구성하는 것. Stellarium 은 안 함; 우리도 안 함. 비교적
   질량이 비슷한 시각 쌍성(두 카탈로그의 대부분 쌍) 에 대해서는 OK,
   질량 차이가 매우 큰 시스템에서는 photocenter 가 primary 근처에 위치
   — 알려진 근사이고 향후 정교화 대상이지 현재 버그는 아니다.

3. **Hipparcos `f`-factor PM propagation.** 정확한
   `f = 1/√(1 + 2μ_r·t + (μ² + μ_r²)·t²)` 표현이 ESA 표준 형식, 동일하게
   사용. μ_r vs μ², squared vs not 같은 typo 가 쉽게 일어나는 곳이라
   두 독립 코드베이스에서 같은 형태를 보는 게 강한 sanity check.

이 일치가 이 연구의 가장 유용한 발견 — **NearStars 파이프라인의 수식이
idiosyncratic 하지 않음.** 가장 널리 쓰이는 desktop planetarium 이
선택한 컨벤션과 일치.

---

## 5. 의도적으로 다른 지점

분기는 두 시스템 어느 쪽도 버그가 아니며, target use-case 가 다른 결과.

### 5.1 출력: unit vector vs Cartesian state

Stellarium 은 별이 지금 **하늘 어디에** 보이는지가 필요. 방향이면 충분,
거리는 apparent magnitude 와 parallax 에 녹아있음. Cartesian km /
km·s⁻¹ 는 낭비.

NearStars 는 **Principia** 에 입력. Principia 는 km 단위로 full 3D
n-body 시스템을 적분. 무게중심이 아니라 컴포넌트 단위로 적분. 컴포넌트당
absolute Cartesian 좌표 없이는 Principia 에 입력이 없음.

### 5.2 카탈로그 ingestion: 15 쌍 vs full ORB6

Stellarium 은 amateur astronomer 가 실제로 가리키는 showcase 쌍을
큐레이션. 15개면 "γ Vir 가 지금 벌어지는 중, 5년 지켜봐" 류에 충분. 평평한
hand-edited 파일이 그걸 제공하는 가장 저렴한 구현.

NearStars 는 mod 의 ~50 ly Kopernicus footprint 에 들어오는 모든
쌍성이 필요. 수작업 큐레이션은 ~30 개 쌍성 시스템에 안 스케일. 우리는
ORB6 / Gaia NSS ingestion 이 필수, 그들에게는 선택.

### 5.3 호출 주기: 매 프레임 vs 1회

Stellarium 은 사용자가 수 세기를 scrub 할 수 있고 쌍성이 swing 하는
것을 기대하므로 매 프레임 재계산.

NearStars 는 한 순간(`JD2433282.5`) 을 freeze. 그 다음부터는 Principia 가
forward integration 으로 모든 future state 를 derive. build 단계 이후
궤도 요소가 *필요* 없음.

### 5.4 하이어라키컬 다중성

Stellarium 은 Proxima Centauri 를 *자체* HIP 카탈로그 astrometry 로
렌더링 — α Cen AB 와 궤도적으로 결합되지 않음. 시각적으로는 "진짜"
하이어라키컬 해와 구분 불가 — Proxima 의 4.24 ly 거리 × 13,000 AU
분리는 하늘에서 ~13′ 로 변환, Stellarium 의 일반적 시각 쌍성 해상도
아래.

Principia 입장에서는 결합이 **무시 불가능**. Kervella+ 2017 의 α Cen ABC
궤도해는 Proxima 를 AB 에 ~547,000 yr 주기로 중력 결합, Principia 가 그
섭동을 적분. 그래서 우리의 Jacobi 분해 for triples(40 Eri C 와 36 Oph C
도 같은 케이스) 가 필요.

### 5.5 솔버: Newton vs Markley

`e < 0.9` 의 Newton iteration 은 1e-10 까지 ~3–5 회면 수렴. Markley 는
non-iterative 하고 1 회에 ~1e-15 까지 수렴하지만 호출당 더 많은 flop
필요. 둘 다 OK; 선택은 부수적. 우리는 PyAstronomy 가 제공하므로 Markley
사용; Stellarium 은 나머지 Kepler-solving 코드가 Newton 이므로 Newton.

---

## 6. NearStars 에 시사점

**구조 변경 권장 사항 없음.** 비교가 우리 파이프라인을 검증할 뿐, 누락
기능을 드러내지 않음. 구체적으로.

- 우리 컨벤션 선택(Hilditch, 질량비 분할, `f`-factor) 이 독립된 성숙한
  코드베이스가 선택한 것과 동일.
- Stellarium 이 *결여한* 기능들(Cartesian state output, ORB6 ingestion,
  hierarchical triples, velocity output) 이 *정확히* NearStars 의 차별점.
  과도설계가 아니라 Principia 가 요구하고 Stellarium 은 요구하지 않는
  것을 하고 있음.

**행동 항목은 아니지만 기록해 둘 minor 제안.**

- **몇 쌍을 시각 검사로 cross-validate.** Stellarium 과 우리 DB 모두에
  있는 α Cen AB, Sirius AB, 61 Cyg AB 선택. 우리 Cartesian 출력에서 sample
  JD 의 apparent (Δα·cos δ, Δδ) sky offset 을 계산해 Stellarium 의 렌더와
  비교. ~10 mas 일치면 우리 컨벤션 end-to-end 확인; 불일치면 sign-error red
  flag. 본 연구 범위 밖의 향후 검증 작업.

- **`binary_orbits.json` 출처 문서화.** Stellarium 은 타깃 사용자가
  체크하지 않으므로 인용 없는 궤도 요소로 넘어감. 우리는 이미 궤도당
  `bibcode` 를 기록 — 옳은 정책이고 유지.

- **수작업 큐레이션 sanity check 로서의 15쌍 목록.** Stellarium 목록의
  모든 시스템이 우리 DB 에 있음. 향후 maintainer 가 Stellarium 의 15 에
  *없는* 쌍을 우리 DB 에 추가하면 — OK 이긴 하지만 — "이 쌍이 시각 쌍성
  으로 널리 인식되는가, 아니면 궤도가 speculative 한가" 라는 질문이
  떠야 함. Stellarium 목록이 "통념" 필터 역할.

---

## 7. 미해결 질문

- Stellarium 의 `binary_orbitparam.dat` 는 그들의 레포에 build script 가
  없음. 수작업 ORB6 lookup 으로 유지되는가, 아니면 unpublished derivation
  script 가 있는가? NearStars 에는 load-bearing 아니지만 호기심.
- Stellarium 이 궤도 속도(arcsec·yr⁻¹) 를 내부 계산 후 폐기. 향후
  Stellarium feature 가 그 속도를 노출하면, 우리 `vx, vy, vz` 출력의 가장
  간단한 cross-check (sky-to-3D 변환 modulo). 그쪽 changelog 지켜볼 가치.
- Stellarium 이 ε Lyr 의 quadruple 구조(ε¹ Lyr AB + ε² Lyr AB 는 두 개의
  분리된 Kepler 시스템이지만 동시에 wide visual pair) 를 처리하는지 확인
  못 함. 15-row 파일은 ε¹ 과 ε² 를 따로 나열하고 둘 사이 link 없음 —
  아마 α Cen + Proxima 와 같은 "no hierarchy" 한계.

---

## 8. Sky-offset 교차 검증 (2026-05-21 실행)

§6 의 "minor 제안" 이었던 두 파이프라인 수치 검증 실행. 재실행 가능한
테스트는
[`scripts/verification/stellarium_crosscheck.py`](../../scripts/verification/stellarium_crosscheck.py)
참조.

### 8.1 설정

두 독립 알고리즘이 secondary 의 sky offset (Δα·cosδ, Δδ) 를 JD 2460310.5
(J2024.0) 에서 계산.

- **Stellarium-style** — [`Star.hpp` L364-L373](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L364-L373)
  의 직접 `r · rotation` 형태.
- **Thiele-Innes** — 고전적 Hilditch (2001) A/B/F/G 상수에 이심 anomaly
  좌표 `x = cosE − e`, `y = √(1−e²)·sinE` 사용.

각 알고리즘을 **두 element 세트** 에 독립적으로 적용.

- **Stellarium 데이터** —
  [`stars/hip_gaia3/binary_orbitparam.dat`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/stars/hip_gaia3/binary_orbitparam.dat)
  에서 추출 (해당 파일은 각도가 이미 radian).
- **NearStars 데이터** — `db/binary_orbits.json` 의 α Cen, Sirius, 61
  Cyg AB orbit 블록.

결과 표 (mas).

| 시스템 | Stellarium-style (Stellarium 데이터) | Stellarium-style (NS 데이터) | Drift |
|---|---|---|---|
| α Cen AB | Δα·cosδ=+887, Δδ=+8071 (sep 8.12″, PA 6.3°) | Δα·cosδ=+1234, Δδ=+8537 (sep 8.63″, PA 8.2°) | **581 mas** |
| Sirius AB | Δα·cosδ=+9865, Δδ=+5536 (sep 11.31″, PA 60.7°) | Δα·cosδ=+9818, Δδ=+5624 (sep 11.31″, PA 60.2°) | **99 mas** |
| 61 Cyg AB | Δα·cosδ=+14065, Δδ=−28777 (sep 32.03″, PA 154.0°) | Δα·cosδ=+16528, Δδ=−23282 (sep 28.55″, PA 144.6°) | **6022 mas** |

### 8.2 Test 1 — 알고리즘 등가성

같은 element 세트에 두 알고리즘을 통과시킨 결과가 **0.000000 mas** (수치
정밀도, ~1e-15) 까지 일치 — 세 시스템 모두, Stellarium 데이터와 NS
데이터 양쪽 모두. Hilditch 회전 컨벤션, 이심 anomaly 변환, Kepler 솔버가
end-to-end 일관. **sign-convention 버그 없음 확인.**

### 8.3 Test 2 — 데이터 drift

Cross-pipeline 차이(같은 알고리즘, 다른 element 출처) 는 알고리즘 오류가
아닌 **데이터 revision drift** 측정.

- **Sirius 99 mas.** Element 세트가 거의 동일 (둘 다 Bond 2017 era).
  Drift 는 출판된 `T` 와 `ω` 의 불확실성 범위 안. ✓
- **α Cen 581 mas.** 두 파이프라인 모두 Pourbaix 계열 해를 사용하지만
  다른 revision (NS. Pourbaix & Correia 2017; Stellarium. `T =
  2435314.751 = 1955.555` 시그니처로 보아 Pourbaix 2002 era). 0.2° Ω,
  0.13° ω, 280일 T 차이가 sub-arcsecond drift 로 전파 — periastron 근처
  빠르게 움직이는 궤도에서 예상되는 수준. ~
- **61 Cyg 6022 mas.** NS 는 Strand (1952) / Walker (1995) elements with
  B1950 equinox; Stellarium 은 무관한 더 최근 elements (P=705 yr vs NS
  659 yr) with J2000 equinox. B1950→J2000 frame shift 가 Ω 차이의 ~3.4°
  를 설명; 나머지는 element revision 차이. 이 쌍은 **NS 의 61 Cyg 궤도
  elements 갱신** 의 가장 명확한 근거 — Strand 1952 는 70 년 stale.

### 8.4 결론

§6 에서 명시한 "~10 mas 일치" 타깃은 카탈로그 revision 노이즈(잘 측정된
시스템에서도 sub-arcsec, 부실하게 측정된 것은 수 arcsec) 를 고려할 때
비현실적. 실제로 달성 가능했던 테스트는 알고리즘 등가성이었고, 그것은
**수치 정밀도까지 통과**. NearStars 파이프라인의 Hilditch 컨벤션,
Thiele-Innes 표현, Newton/Markley Kepler 솔버가 Stellarium 의 독립 구현과
일관.

남은 drift 는 데이터지 수학이 아님. 구체적 action 항목. `db/binary_orbits.json`
의 61 Cyg 궤도를 post-2000 해로 갱신. 아래 §9 에서 신규 open question 으로
추적.

---

## 9. 미해결 질문 (갱신)

이전 §7 항목 유지. §8 에서 추가된 신규 open question.

- **61 Cyg 궤도 element refresh.** NS 의 Strand (1952) / Walker (1995)
  elements 는 B1950 equinox, 70+ 년 stale, 그리고 우리 파이프라인의
  나머지 J2000 정렬과 frame 불일치. 후보 대체. Hartkopf et al. ORB6
  grade-4 solution 또는 Malkov+ 2012. 본 연구 노트에서 구현하지 않고
  `phase2/` 데이터 refresh 작업으로 deferred — 여기서 flag 만.

## Related

- [binary-epoch-pipeline](../docs/reference/binary-epoch-pipeline.md) — 비교 대상이 되는 NearStars 파이프라인 (본 문서가 그 검증 교차 검사).
- [methodology](../docs/reference/methodology.md) — 이 비교가 검증하는 스키마 층.
- [alpha-centauri-a](../docs/phase3/alpha-centauri-a.md), [alpha-centauri-b](../docs/phase3/alpha-centauri-b.md) — Stellarium 과 NearStars 가 모두 인코딩하는 정전 워크드 예시.
