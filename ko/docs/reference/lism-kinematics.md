# 국부 성간물질(LISM) 운동학과 태양권/성간풍 뷰어

`db/refs/lism_kinematics.yaml`(55 ly 범위의 LISM 인구조사)와, 이를 바탕으로 3D 뷰어가
만들어내는 **태양권(heliosphere)** + **성간풍(interstellar-wind)** 레이어에 대한 레퍼런스다.
영어 원본은 `docs/reference/lism-kinematics.md`.

## 무엇인가

뷰어는 별마다 **항성권(astrosphere, 항성풍 거품 + 후류 꼬리)** 을 보여줄 수 있고,
국부 공간 전체에 걸쳐서는 **성간풍 벡터장**을 보여줄 수 있다. 두 가지 모두 국부운
구름의 운동학과 각 별의 공간속도를 묶은 하나의 큐레이션 데이터셋에서 나온다.
방향(orientation) 모델은 발표된 항성권 측정값으로 검증되어 있다.

## 데이터셋 — `db/refs/lism_kinematics.yaml`

bibcode로 고정된 ~17 pc(55 ly) 이내 국부 성간물질 인구조사이며, 독립적으로 검증되었다
(핵심값 6/6 일치, 2026-06-16).

| block | source | content |
|---|---|---|
| `clouds` (15) | Redfield & Linsky 2008, `2008ApJ...673..283R` (Tables 16 & 18) | 따뜻한 구름의 태양중심 속도 벡터 = 성간풍 **벡터장** |
| `astrospheres` (27) | Wood et al. 2021, `2021ApJ...915...37W` (Tables 2 & 3) | 측정된 항성권 — **검증 + 구름 할당 + 바람 세기**용이지, 벡터장 앵커가 아님 |
| `astrospheres_xray` (3) | Kislyakova et al. 2024, `2024NatAs...8..596K` | X선으로 검출된 항성권(더 큰 질량손실; 방법론 충돌, 따로 분리해 보관) |
| `insitu_he` | Bzowski/McComas 2015, `2015ApJS..220...28B` | 태양에서 직접 측정한 IBEX He 유입 |

**컨벤션(중요).**
- 구름의 `(l_deg, b_deg)`는 **풍하(downwind)** 방향, 즉 가스가 *향해* 흘러가는 쪽이다.
  은하좌표이며 `v0_kms > 0`. 태양정지(heliocentric, solar-rest) 좌표계다. 풍상(upwind)
  근원 정점(apex)은 그 대척점 `(l−180, −b)`이다.
- `insitu_he`는 **황도 유입(ecliptic inflow)** 방향으로 주어진다 — 구름 벡터와 합칠 때
  좌표계/컨벤션 차이에 유의할 것.
- `astrospheres[].v_ism_stellar_kms`는 **항성정지(stellar rest) 좌표계** 값이다(항성권이
  제약하는 ISM-대-별 흐름 속도) — 태양중심값이 **아니다**. 구름 할당과 바람 세기에는
  쓰되, 절대 태양중심 벡터장 앵커로 쓰지 말 것. 벡터장은 구름 벡터다.
- 3D 구름 깊이는 제약이 약하다. 하늘에서의 방향은 확실하지만, `near_pc`는 **가까운 쪽
  가장자리의 상한선**일 뿐 위치가 아니다.

## 모델 (하이브리드)

별마다 태양중심 ISM 속도는 다음과 같다.

```
v_ISM(pos) = blend( IDW over cloud vectors by sky angular distance,  LIC vector,  w_local )
w_local = exp( -(distance_pc) / 4 )          # LIC envelops the Sun → dominates nearby
v_rel = v_star(heliocentric) − v_ISM         # nose = +v_rel (faces the wind), tail = −v_rel
```

- **구름 벡터에 대한 IDW**는 각 구름에 `1/(θ² + θ0²)` 가중치를 준다. θ는 별의 하늘
  방향에서 그 구름 영역 중심까지의 각거리. 모델에서 `θ0 = 20°`.
- **LIC-국부 혼합**은 필수이며 제거해서는 안 된다. 국부성간운(Local Interstellar Cloud)이
  태양을 둘러싸고 있어서 ~4 pc 이내에서는 LIC가 지배적이다. 순수한 방향 IDW만 쓰면
  가까운 별(실제로는 LIC 내부에 있는)이 하늘 영역이 겹치는 먼 구름에 잘못 할당되어,
  태양권 노즈가 30~90° 어긋났다. 이 혼합은 Wood et al.의 7 pc 이내 LIC 기본값과 맞는다.
- 태양 자신은 직접 측정한 IBEX He 벡터를 쓴다(`v_star = 0 → v_rel = −v_ISM`).
- 은하좌표→ICRS 변환은 표준 J2000 행렬(`build_starmap.py`의 `_GAL2ICRS`)로 한다.

**의존성.** v_rel은 별의 *완전한 3D* 공간속도가 필요하므로, 시선속도가 빠지면 노즈
방향이 오염된다. [[project-nearstars-rv-gap]]를 보라 — 시선속도 없는 별 21개를 바로 이
모델이 작동하도록 `MANUAL_RV`로 큐레이션했다.

## 검증 (문헌과 대조)

태양 항성권 노즈 → 황도 λ=75.8°, β=−5.2° = **IBEX 풍상과 정확히 일치**.

모델 θ(풍상/노즈와 우리 시선 사이 각도) 대 Wood et al. 2021 측정 θ.

| star | model | Wood | star | model | Wood |
|---|---|---|---|---|---|
| HD 219134 | 60° | 60° | α Cen | 87° | 79° |
| Barnard | 45° | 43° | τ Cet | 55° | 59° |
| 61 Vir | 96° | 98° | ε Eri | 76° | 76° |

(ε Eri는 빠져 있던 시선속도를 큐레이션한 뒤에야 일치했다 — RV 갭을 찾아낸 진단이었다.)
v_rel 크기도 마찬가지로 Wood의 항성정지 V_ISM을 잘 따라간다. 물리적으로, 빠른 별의
노즈는 자기 운동 방향을 향하고, 태양(LIC 안에서 거의 정지)은 순수하게 풍상을 향한다.
즉 풍하 바람장 화살표와 반대 방향이며 — 이건 버그가 아니라 옳은 결과다.

**구름 간 편차.** 방향은 꽤 일관적이지만(LIC로부터 평균 21°; 핵심 구름들은 ~10° 이내),
**속도는 4배 넘게 차이난다**(Blue/Hyades ~14 km/s … Aql/Cet ~60 km/s).

## 뷰어 레이어

- **Heliosphere** 토글(시스템 뷰): 항성풍 호스트 7개 + Sol에 대해 점박이 물방울 모양
  항성권(THREE.Points). 뭉툭한 노즈가 풍상, 긴 꼬리가 풍하. 색 = 방사선 등급(medium =
  amber, high = red; `HELIO_GRADE`에 고정, 아직 DB 필드가 아닌 Phase-3 결론), 크기 ∝
  `mass_loss_solar`. 도식적 스케일.
- **ISM wind** 토글(맵 뷰): 국부 `v_ISM`을 나타내는 화살표의 3D 격자(8 ly 간격, 50 ly
  이내), 단일 `LineSegments` 드로콜 하나. **화살표 길이 ∝ ISM 속도**(가독성을 위해
  과장 — 방향이 비슷하므로 원래 4배의 속도 편차가 실질적 변별 요소다), **지배 구름별
  색상**(+ 범례). 격자는 모델보다 **더 날카로운 IDW(θ0 = 12°)**로 샘플링해 구름 영역이
  뚜렷이 구분되어 보이게 한다. 격자 전용이며 모델에는 영향 없음.

**코드.** `build_starmap.py`의 `load_lism` / `_ism_velocity` / `wind_for` / `heliosphere_for`가
`wind`(클러스터별)와 `heliosphere`(호스트별), 그리고 격자용 `lism`(구름 벡터장)을 내보낸다.
`starmap_template.html`의 `ismSample`(격자 샘플링) / `makeHeliosphere`(거품)가 이를 렌더한다.

## 출처 / 정직성

- 구름 벡터는 표준 R&L 2008 세트이며, 이후 연구가 이를 대체하지 않았다(형태/컬럼을
  정밀화할 뿐이다). 항성권 표본은 작지만(역대 측정된 게 ~20개) 여기서는 빠짐없이 담았다.
- `radiation_surface` 등급은 Phase-3 합성 결론으로, kerbalism-cfg 파이프라인이 이를
  공식화할 때까지 코드에 고정해 둔다([[project-nearstars-stellar-wind-kerbalism]]).
- 성간풍 벡터장은 하늘 방향에 따라 달라진다(구름은 각(角) 영역이다). 안쪽 ~10 ly가
  균일한 LIC인 것은 실제다(우리가 그 안에 있다). 차이는 바깥으로 갈수록 커진다.
