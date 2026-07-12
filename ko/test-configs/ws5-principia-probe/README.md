# WS5 Principia 프로브 — 테스트용 항성 cfg

NearStars 항성 4개 (α Centauri A, α Centauri B, Proxima Centauri, TRAPPIST-1) 를 담았습니다.
**행성 없이 항성만**, 텍스처는 placeholder 입니다. WS5 프로브가 실제 먼 항성 근처에 선박을
띄우고 자기중력 서브시스템이 형성되는 걸 관찰하려고 만든 물건입니다.

여기 들어있는 건 **생성 산출물의 커밋된 스냅샷**입니다. 정상 빌드 경로는 `dist/` 에 쓰고
그쪽은 gitignore 대상인데, 프로브 설치본이 GitHub 에서 바로 받아갈 수 있도록 예외적으로
체크인했습니다. 손으로 고치지 말고 아래 "재생성" 절차를 쓰세요.

## 설치 (스톡 Kerbol + Principia Keplerian 경로)

`GameData/` 를 프로브 설치본의 `GameData/` 에 덮어쓰고, **Kopernicus** 를 추가하면 됩니다.
Kopernicus 가 없으면 천체 자체가 생기지 않습니다.

```
GameData/
├── Kopernicus/                         ← 직접 넣으셔야 합니다
├── NearStars-Configs/
│   ├── NearStars-Stars-Kopernicus.cfg          항성 4개 (@Kopernicus:FOR[NearStarsSystem])
│   ├── NearStars-StockKeplerian-Orbits.cfg     실제 궤도 계층 (@Kopernicus:AFTER[...])
│   └── NearStars-StockKeplerian-GravityModel.cfg   @principia_gravity_model, initial_state 없음
└── NearStars-Textures/PluginData/…             placeholder sunspot + corona DDS
```

설치는 이게 전부입니다. `NearStarsSystem` 은 실제 모드 폴더가 아니라, Kopernicus cfg 의
`:FOR[NearStarsSystem]` 패스가 선언하는 태그입니다. 나머지 두 패치가 그 태그를 물고 들어옵니다.

### 왜 이게 Keplerian 경로인가

`principia_initial_state` 가 **없습니다**. 그래서 Principia 는 각 천체의 상태를 Kopernicus
접촉 궤도요소에서 유도하고 (`InsertCelestialJacobiKeplerian`), 스톡 Kerbol / Kerbin / Mun 은
Cartesian 항목이 필요 없어집니다. 모든 천체를 커버해야 하는 일관성 검사(= 빠지면 `Log.Fatal`)
자체가 돌지 않습니다.

`initial_state` 가 없을 때의 부수효과가 하나 있습니다. Principia 가 스톡 Jool 계에
`StabilizeKSP()` 를 겁니다 (Vall/Tylo 평균운동을 1:2:4 공명에서 밀어내고 Bop 을 역행으로 뒤집음).
이건 Keplerian 모드 설치본이면 다 겪는 일이지, 이 cfg 가 새로 만드는 문제는 아닙니다.

## `cartesian-sol-base/` 는 설치하지 마세요

여기엔 **릴리스 경로**의 Principia 패치가 들어있습니다. `gravity_model` + `initial_state`,
Cartesian, `NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]`, 좌표는 Sol 바리센트릭 ICRS 프레임
기준 `solar_system_epoch = JD 2433282.5` 입니다.

Cartesian 은 all-or-nothing 이라 `FlightGlobals.Bodies` 의 모든 천체가 `initial_state` 항목을
가져야 합니다. 스톡 Kerbol 천체엔 그게 없으니, 스톡 설치본에 넣으면 100% `Log.Fatal` 입니다.
실제 Sol-Configs 기반 빌드가 무엇을 뽑는지 보여주는 레퍼런스로만 남겨뒀고, 그래서 일부러
`GameData/` 밖에 뒀습니다.

## 천체 구성

| 천체 | 부모 | 궤도 |
|---|---|---|
| `AlphaCentauriA` | `Sun` | 4.158e16 m (4.395 ly, 실제 거리), 원궤도 placeholder |
| `AlphaCentauriB` | `AlphaCentauriA` | a = 23.675 AU, e = 0.5179, i = 79.205° — 실측 ORB6 grade-1 |
| `ProximaCen` | `AlphaCentauriA` | a = 8700 AU, e = 0.5 |
| `TRAPPIST1` | `Sun` | 3.848e17 m (40.7 ly), 원궤도 placeholder |

`Sun` 은 스톡 항성의 내부 body name 이기도 해서, `referenceBody = Sun` 은 스톡 Kerbol 과
Sol-Configs 양쪽에서 다 해석됩니다.

α Cen A–B 는 실측 궤도요소 (Pourbaix & Correia 2017) 라서 Principia 하에서 진짜 자기중력
쌍성으로 굴러갑니다. 프로브가 보려는 서브시스템이 바로 이겁니다.

**Kopernicus 바리센터 바디는 넣지 않았습니다.** Principia 에는 바리센터 개념이 없어서,
`M_A + M_B` 를 들고 있는 바리센터 바디는 `FlightGlobals.Bodies` 에 진짜 중력원으로 들어가
계 질량을 이중 계산합니다. 대신 B 를 A 의 자식으로 매달았고, Principia 의 Jacobi 변환이 이를
올바른 상호궤도로 풀어줍니다. 바리센터가 필요한 건 Principia 없는 Kopernicus 2-body 폴백
빌드뿐입니다.

### 알아둘 점

- **Proxima 의 위상은 임의값입니다.** 근점 통과 시각이 문헌에서 미구속이라
  (`db/binary_orbits.json` 의 `phase_reliable: false`) `meanAnomalyAtEpochD = 0` 은 placeholder
  입니다. 궤도의 모양은 실측이지만 "지금 어디 있는가" 는 근거가 없습니다.
- **A–B 주기가 카탈로그와 0.9% 어긋납니다.** 카탈로그 a (23.675 AU, 시차 742.12 mas) 와 우리
  GM 을 조합하면 P = 80.60 yr 이 나오는데 카탈로그값은 79.91 yr 입니다. a 와 GM 을 살리고 주기는
  emergent 로 뒀습니다 — Principia 는 P 가 아니라 a + GM 으로 적분합니다.
- **거리는 압축하지 않았습니다.** 1e16–1e17 m 에서 맵뷰나 부동소수점 정밀도가 말썽이면 `Sun` 을
  참조하는 두 천체 (`AlphaCentauriA`, `TRAPPIST1`) 의 `semiMajorAxis` 만 줄이면 됩니다. A–B 쌍성은
  자식 궤도라 영향받지 않습니다.
- **SOI 를 덮어씁니다.** `NearStars-Stars-Kopernicus.cfg` 는 모든 항성에
  `sphereOfInfluence = Infinity` 를 넣는데 (루트 바디에만 유효합니다), 궤도 패치가 이를 교체합니다.
  A = 3e15 m (Proxima 원점 1.952e15 m 를 감싸야 함), B = 1e12, Proxima = 1.5e14, TRAPPIST-1 = 1e15.
- **`flightGlobalsIndex` 는 Kopernicus 자동 할당**입니다. 테스트 로드엔 지장 없지만, 릴리스
  빌드는 `.claude/skills/kopernicus-cfg/references/file-structure.md` 의 1000+ 블록에서 배정해야
  합니다.
- **텍스처는 64×64 대역품**입니다. 균일 백색 sunspot, 방사형 알파 corona. 항성 셰이더가 null
  `noiseMap` 을 물지 않게 하는 용도, 그 이상은 아닙니다.

## 재생성

```sh
python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py \
    alpha_centauri_a alpha_centauri_b proxima_cen trappist_1
python3 .claude/skills/principia-cfg/scripts/emit_principia_cfg.py \
    --system alpha_centauri_a --system alpha_centauri_b \
    --system proxima_cen --system trappist_1
python3 scripts/make_placeholder_textures.py
```

이걸로 `NearStars-Stars-Kopernicus.cfg` (= `dist/…/Kopernicus/stars.cfg`),
`cartesian-sol-base/*`, 텍스처가 다시 나옵니다. 단 `NearStars-StockKeplerian-*.cfg` 두 개는
**손으로 쓴 파일**이라 emitter 가 없습니다 — 릴리스 경로가 Cartesian/Sol 이기 때문입니다. DB 의
α Cen 궤도나 GM 값이 바뀌면 `db/binary_orbits.json` 에서 숫자를 다시 계산해 넣어야 합니다.
