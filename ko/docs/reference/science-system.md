# KSP 과학 시스템 — NearStars 바디 작성 레퍼런스

> **관점.** 행성 팩이 새 바디마다 무엇을 작성해야 stock KSP 과학과
> Kerbalism/ROKerbalism(RP-1) **양쪽 모두**에서 과학이 동작하는지를 다룬다.
> 업스트림 출처에 근거하며(본문 인용), NearStars는 두 플레이어 스택을 모두
> 겨냥한다. Sol-Configs 위의 Sandbox/Science(stock 과학)와 Sol V1.0 위의
> RP-1(Kerbalism)이다. [`gameplay/rp1-integration/plan.md`](../../gameplay/rp1-integration/plan.md)를 참고한다.

---

## 0. 한 문단으로 보는 결론

**biome + `ScienceValues` 블록**을 **Kopernicus 바디 레벨**에서 한 번만
작성하면 된다. stock 과학과 Kerbalism이 이를 직접 읽으며, Kerbalism은
**자체 per-body 과학 설정이 전혀 없다**. 유일한 차이는 플레이버 텍스트다.
stock `ScienceDefs RESULTS{}` 문자열은 stock 플레이어에게 보이지만
**Kerbalism의 완료 흐름에서는 무시된다**(Kerbalism은 바디 + 상황 + biome
이름에서 제목을 자동 조합하고 일반적인 결과 줄을 쓴다). 진짜로
Kerbalism 고유의 per-body 노브는 **방사선 환경**(벨트/자기권) 하나뿐이며,
이것이 Kerbalism의 방사선 *virtual biome*을 바디에서 해석되게 만든다. 이는
RP-1 통합 WS4와 겹친다.

| 바디 측 산출물 | Stock | Kerbalism/RP-1 | 한 번만 작성? |
|--------------------|:-----:|:--------------:|:------------:|
| `ScienceValues` (9개 필드) | ✅ 읽음 | ✅ 읽음 (이것이 곧 per-body 배율) | **예** |
| Biome map + `Biomes{}` | ✅ 읽음 | ✅ 읽음 (stock `Body.BiomeMap`) | **예** |
| `ScienceDefs RESULTS{}` 플레이버 | ✅ 표시 | ❌ 완료 시 무시 | stock 전용 |
| 방사선 벨트/자기권 | 해당 없음 | 방사선 *virtual biome*을 활성화 — 단 **RP-1 실험 중 이를 쓰는 것은 없음(§3.4)**, latent | Kerbalism 전용 (옵션) |
| 실험 정의 / 부품 | 글로벌 | 글로벌 (RP-1 콘텐츠) | **per-body 작성 안 함** |

---

## 1. Stock 과학 시스템

### 1.1 실험 (기본 12종) + DLC

| `id` | 제목 | 운반체 |
|------|-------|---------|
| `crewReport` | Crew Report | 승무원 탑승 부품 |
| `evaReport` | EVA Report | EVA 중인 커벌 |
| `surfaceSample` | Surface Sample | 지표면 EVA |
| `asteroidSample` | Asteroid Sample | 포획한 소행성에서 EVA |
| `cometSample` | Comet Sample | 혜성에서 EVA |
| `mysteryGoo` | Mystery Goo™ | Goo Containment Unit |
| `mobileMaterialsLab` | **Materials Study** (id ≠ MPL 랩) | SC-9001 Science Jr. |
| `temperatureScan` | Temperature Scan | 2HOT Thermometer |
| `barometerScan` | Atmospheric Pressure Scan | PresMat Barometer |
| `gravityScan` | Gravity Scan | GRAVMAX |
| `seismicScan` | Seismic Scan | Double-C Accelerometer |
| `atmosphereAnalysis` | Atmosphere Analysis | Fluid Spectro-Variometer (대기 한정) |

- **Breaking Ground.** 지표 피처 → `ROCScience_<Feature>`(stock 정의 약 42종,
  예 `ROCScience_MunStone`). 배치형 4종 → `deployedSeismicSensor`,
  `deployedWeatherReport`(대기 한정), `deployedGooObservation`(≠ `mysteryGoo`),
  `deployedIONCollector`(무대기 한정).
- **Making History.** 새 실험 없음.
- 실험이 아닌 것. `recovery`(자금 회수 메커니즘), Mobile Processing Lab(데이터→과학).

출처. stock ScienceDefs 미러 `raw.githubusercontent.com/pjf/ksp-gamedata/master/Squad/Resources/ScienceDefs.cfg`, ROC 체계 `github.com/Kerbalism/Kerbalism/issues/395`.

### 1.2 상황과 마스크

`ExperimentSituations`. `SrfLanded`(착륙/발사 전), `SrfSplashed`(해양 바디
한정), `FlyingLow`/`FlyingHigh`(대기 바디 한정), `InSpaceLow`/`InSpaceHigh`.

비트마스크(`situationMask`와 `biomeMask` 동일 레이아웃).

| 상황 | SrfLanded | SrfSplashed | FlyingLow | FlyingHigh | InSpaceLow | InSpaceHigh |
|-----------|:---------:|:-----------:|:---------:|:----------:|:----------:|:-----------:|
| 값 | 1 | 2 | 4 | 8 | 16 | 32 |

`situationMask`는 실험이 동작하는 위치이고, `biomeMask`는 그중 어떤 상황이
biome별 결과를 주는지를 정한다(situationMask의 부분집합이며 `0`이면 절대
없음). `63`은 여섯 상황 전부다. 대기/해양 게이팅은 대부분 별도 플래그가
아니라 *어느 비트가 켜져 있는가*로 처리한다(stock 1.12.x에서
`requireNoAtmosphere`/`requireSurface`는 **미검증**이고, `requireAtmosphere`는
실재한다).

### 1.3 바디 값 — `Body { Properties { ScienceValues {} } }`

정확히 **9개 필드**(상황별 배율 + 임계값).

| 필드 | 역할 | Kerbin | Mun | Duna | Sun |
|-------|------|:------:|:---:|:----:|:---:|
| `landedDataValue` | × SrfLanded | 0.3 | 4 | 8 | 1 |
| `splashedDataValue` | × SrfSplashed | 0.4 | 1 | 1 | 1 |
| `flyingLowDataValue` | × FlyingLow | 0.7 | 1 | 5 | 1 |
| `flyingHighDataValue` | × FlyingHigh | 0.9 | 1 | 5 | 1 |
| `inSpaceLowDataValue` | × InSpaceLow | 1.0 | 3 | 7 | 11 |
| `inSpaceHighDataValue` | × InSpaceHigh | 1.5 | 2 | 5 | 2 |
| `recoveryValue` | × 회수 시 | 1.0 | 2 | 5 | 4 |
| `flyingAltitudeThreshold` | m, FlyingLow↔High | 18000 | 18000 | 12000 | 18000 |
| `spaceAltitudeThreshold` | m, InSpaceLow↔High | 250000 | 60000 | 140000 | 1E+09 |

- 두 임계값 모두 **per-body**이며 상황 판정을 좌우한다.
- 패턴. 모항성 바디가 가장 낮고, 멀거나 어려운 바디일수록 올라가며, 무대기
  바디는 `flyingLow/High = 1` 플레이스홀더를 유지한다.
- **Sun은 NearStars 항성 바디의 템플릿이다.** `Biomes` 없음,
  `spaceAltitudeThreshold = 1E+09`, 적당한 배율.
- 이 노드에 없는 것. `RnDNormalRate`, `sciSpaceLowMultiplier`(여기 존재하지 않음).

출처. Kopernicus kittopia-dumps, `github.com/Kopernicus/Kopernicus/wiki/Properties`.

### 1.4 Biome

`Body { Properties { } }` 안에서 ScienceValues 옆에 둔다.

```
biomeMap = NearStars-Textures/PluginData/<Body>/<Body>_Biomes.dds   // path sans GameData, with extension
Biomes {
    Biome { name = Lowlands ; value = 1 ; color = RGBA(0,255,255,255) }
    Biome { name = Highlands; value = 1 ; color = RGBA(51,255,255,255) }
}
```

- **단색 평면 한 가지 = biome 하나**이며, Kopernicus는 각 픽셀의 **전체
  RGB(A) 색**으로 매칭한다. 현업에는 두 가지 색 문법이 있다. float `0–1`
  (`color = 0.2,0.5,0.1,1`)과 0–255 `RGBA(...)`. NearStars/Sol-Configs는
  `RGBA(...)` 형식을 쓴다.
- `value`는 biome별 **과학 배율**이다(인덱스/색이 아님).
- 텍스처 규칙. 비압축(DDSLoader가 DXT를 건너뛰도록 DDS를 `PluginData/`에 둔다.
  DXT는 단색을 망가뜨린다), **mipmap 없음**, 경계는 선명하게(AA/그라데이션
  없음), 약 1K면 충분하다.
- 과학 **subject = 실험 × 바디 × 상황 × (해당 상황에 대해 실험의 `biomeMask`가
  활성화하면 biome)**.

> ⚠️ **스킬 정합성 플래그.** `kopernicus-cfg/references/pitfalls.md`는 현재
> biome가 "R 채널만 사용한다"고 적고 있다. 부정확하다. Kopernicus는 전체
> 색으로 매칭하며, 우리 cyan 컨벤션이 우연히 G=B=255 안에서 R만 달리할
> 뿐이다. Kopernicus 소스로 확인하고 그쪽 문구를 고쳐야 한다.

### 1.5 결과 텍스트 — `ScienceDefs RESULTS{}`

```
@EXPERIMENT_DEFINITION:HAS[#id[crewReport]] {
    @RESULTS {
        <Body>InSpaceLow            = ...
        <Body>SrfLanded<BiomeNoSpaces> = #LOC_NearStars_...
    }
}
```

- **키 형식은 연결된 `<Body><Situation><Biome>`이며 `@` 구분자가 없다**(`@`는
  런타임 subject ID에만 나타나고 RESULTS 키에는 없다). Body는 Kopernicus 내부
  바디 이름이다. 실험 접두사는 없다(블록의 `id`가 실험을 식별한다).
- biome의 공백/구두점은 제거된다. `KerbinSrfLandedLaunchPad`.
- 폴백 순서. `<Body><Situation><Biome>` → `<Body><Situation>` → `default`
  (여러 `default =` 허용 → 무작위 선택).
- id 셀렉터 **`:HAS[#id[<exp>]]`**로 주입한다(`:FOR[]`가 아님). `key =`는 새
  키를 추가하고 `%key =`는 기존 키를 덮어쓴다. 우변은 보통 `#LOC_...` 토큰이다.

출처. OPM `Patches/OPM_ScienceDefs.cfg`, GPP `GPP_Science_Defs.cfg`,
`github.com/Amorymeltzer/ksp/blob/main/parseScience.pl`.

---

## 2. Kerbalism / ROKerbalism 과학 (RP-1)

### 2.1 3계층 아키텍처

| 계층 | Repo | 역할 |
|-------|------|------|
| 엔진 | `Kerbalism/Kerbalism` | 파일 기반 과학 *메커니즘*(C# `Experiment`/`HardDrive`/`Laboratory`, 값 계산, virtual biome) |
| 프로파일 | `KSP-RO/ROKerbalism` | 생명 유지/방사선 프로파일 — **실험을 정의하지 않음** |
| 콘텐츠 | `KSP-RO/RP-1` (`GameData/RP-1/Science/`) | 실험 정의 + 실제 계측기 부품(글로벌, **per-body 아님**) |

Kerbalism은 **러너를 교체한다**(자체 `Experiment` PartModule이 stock
`ModuleScienceExperiment`를 대체하고 포드에 `HardDrive`를 자동 추가). 다만
**stock `EXPERIMENT_DEFINITION` 데이터 노드를 재사용하며**(`id`, `baseValue`,
`scienceCap`, `dataScale`, `situationMask`, `biomeMask`를 읽음)
`KERBALISM_EXPERIMENT{}` 하위 노드로 확장한다.

출처. `github.com/Kerbalism/Kerbalism/wiki/TechGuide-~-Supporting-Science-Mods`,
`kerbalism.readthedocs.io/en/latest/science.html`.

### 2.2 파일 기반 모델

실험은 **시간에 걸쳐 진행되며**(언로드된 선박에서도 백그라운드 가능),
**파일**(DSN으로 데이터율에 따라 전송 가능, `sample_mass = 0`) 또는
**샘플**(질량을 가짐, 전송 불가, 회수하거나 랩에서 분석)을 산출한다. RP-1의
로스터는 계층화된 실제 계측기다(`crewReport`/`temperatureScan`/`evaReport`/`surfaceSample`을
재사용하고 `RP0magScan1/2/3`처럼 커스텀 `RP0<name><tier>`를 추가). 약 34개
부품이며 각각 `totalScienceLevel` 비율을 지녀 테크 계층이 점점 큰 %를
돌려준다 — **stock의 Goo/Science-Jr. 패러다임은 전혀 없다**.

### 2.3 조건 — 상황, virtual biome, `requires`

`KERBALISM_EXPERIMENT { Situation = Surface@Biomes; Situation = Space@VirtualBiomes; ... }`

- stock 상황 + 합성(`Space`, `BodyGlobal`) 위에 세워진다. 접미사 `@Biomes`(stock
  biome) 또는 `@VirtualBiomes`.
- **Virtual biome**(환경 기반). `Storm`(태양 폭풍), `Reentry`(>Mach 5
  하강), **`Interstellar`**(항성 SOI 내부, 헬리오포즈 바깥),
  `InnerBelt`/`OuterBelt`/`Magnetosphere`(방사선장), `NoBiome`. **`Reentry`/`Storm`은
  virtual biome이지 상황이 아니다**(흔한 함정). 이는 Kerbalism의 기능이며,
  **RP-1이 배포하는 실험은 virtual biome을 하나도 쓰지 않는다**(§3.4).
- 바디 게이팅. `BodyAllowed`/`BodyNotAllowed` = `HomeBody`, `Suns`, `Planets`, `Moons`, ...
- 모듈 레벨 `requires` 문자열(쉼표 구분, 전부 충족해야 함) — 큰 토큰 집합으로
  `Sunlight`/`Shadow`, `Atmosphere`/`Vacuum`, `Ocean`, `InnerBelt`,
  `Magnetosphere`, `InterPlanetary`, **`InterStellar`**, 궤도/열/압력 최소·최대를 포함한다.

출처. `kerbalism.readthedocs.io/en/latest/modders/modules.html`, `src/Kerbalism/Science/ScienceSituation.cs`.

### 2.4 바디 값과 텍스트 (Kerbalism이 읽는 것 vs 무시하는 것)

- **stock `ScienceValues`를 직접 읽는다.** `ScienceSituation.BodyMultiplier`가
  각 상황을 stock 필드(`landedDataValue`, ..., `inSpaceHighDataValue`)에
  매핑한다. Kopernicus 블록이 **곧** Kerbalism의 per-body 스케일링이다.
- **stock biome map을 읽는다**(`Body.BiomeMap`). `minVirtualBiome`을 넘으면
  인덱스가 virtual biome으로 해석된다. virtual biome은 stock biome *위에*
  얹힌다.
- **완료 시 stock `RESULTS{}` 플레이버를 무시한다.** 플레이어가 보는 것은
  자동 조합된 **제목**(`BodyTitle + SituationTitle + BiomeTitle`) + 일반적인
  무작위 줄(`Sciencresult1..5`) + 실험별 정적 `experiment_desc`다.
  (바디+상황+biome)별 커스텀 결과 텍스트는 사실상 **미지원**이다(코드에
  `file.resultText` 훅이 있지만 설정 경로가 추적되지 않으므로 미지원으로
  취급한다).
- 크레딧 계산. `DataSize = baseValue·dataScale`, `ScienceMaxValue = scienceCap·
  ScienceGainMultiplier · <situation>DataValue`, 수집 MB × (max/size)이며 stock
  RnD subject 상한으로 클램프된다. 수확 체감은 stock과 동일하다.

출처. `src/Kerbalism/Science/` (`ScienceSituation.cs`, `Situation.cs`, `SubjectData.cs`, `ExperimentInfo.cs`, `Science.cs`).

---

## 3. RP-1 실험 로스터와 소요 시간

RP-1에서 플레이어가 연구/수집할 수 있는 것과 각각의 소요 시간이다. RP-1은
stock의 즉시 과학을 대체한다. 수집 시간은 `@data_rate /= N //comment`로
인코딩되며 **N초가 체류/전송 시간**이다. N의 x% 동안 돌리면 과학의 x%를
얻는다(ROKerbalism 부분 크레딧). 문자 그대로의 `duration` 필드는 거의 없고
`data_size`도 없다(파생 = 율 × 시간). 아래의 "Science"는 `baseValue`(= `scienceCap`)다.
출처. `KSP-RO/RP-1` `GameData/RP-1/Science/Experiments/` @ master.

### 3.1 계측기 실험 (stock 스타일 계층형)

| 분야 (id) | 연구 대상 | 상황 | Science | Duration |
|-----------------|---------|------------|:-------:|----------|
| `crewReport` | 승무원 상황 보고 | all (63) | 4 | 5 min |
| `evaReport` | EVA 관측 | Srf+FlyHigh+SpaceHigh (51) | 24 | 2 min |
| `RP0telemetry1` | 선박 텔레메트리 | all (63) | 3 | 5 min |
| `temperatureScan` | 주변 온도 | all (63) | 4 | 10 min |
| `barometerScan` | 대기압 | no-splash (61) | 4 | 10 min |
| `surfaceSample` / `2` / `3` | 지표 스쿱 / 코어 | SrfLanded (1) | 6 / 10 / 15 | 5 min / 20 min / 2.5 h |
| `surfaceAnalysis` | 현장 지표 분석 | SrfLanded (1) | 4 | 30 min |
| `RP0magScan1/2/3` | 자기장 (초기/He/fluxgate) | space + biome (49) | 6 / 12 / 40 | 1 mo / 1 mo / 3 mo |
| `RP0cosmicRay1/2` | 우주선 플럭스 | space (48) | 10 / 30 | 3 mo |
| `RP0RPWS1/2/3` | 전파 및 플라스마 파 | space (49) | 7 / 20 / 30 | 1 wk / 1 mo / 6 mo |
| `RP0massSpec1–4` | 질량 분석 | space + biome (57) | 8 / 12 / 20 / 30 | 2 h / 14 d / 3 mo / 3 mo |
| `RP0infraredRad1–4` | 적외선 복사 측정 | space (48) | 2 / 3 / 4 / 6 | ~3 h / 4 h / ~11 h / 15 d |
| `RP0imageSpec1–4` | 영상 분광 (태양 각도 게이트) | space (48) | 3 / 3 / 4 / 6 | 10 d / 1 h / 96 h / ~78 h |
| `RP0visibleImaging1–5` | TV 영상 (vidicon→HiRISE) | all (63) | 1.5–50 | 40 min → ~405 h |
| `micrometeoriteDetect` | 미소운석 집계 | space (48) | 7 | 3 mo |
| `RP0orbitalPurturbation1` | 궤도 추적 → 중력장 | space (48) | 200 | **10 yr** |
| `RP0bioScan1/2` 🏠 | 생물 표본 | FlyHigh+Space / Space | 22.5 / 40 | 20 min / 1 d |
| `RP0Cherenkov` 🏠 | 고에너지 입자 | space (48) | 20 | 3 mo |
| `RP0photos1–4` 🏠 | 지구 정찰 (V-2→HST) | space | 5 → **10000** | 10 min → **20 yr** |

🏠 = 모항성 바디 전용. (`Purturbation` 오타는 소스 그대로다.)

### 3.2 SCANsat (옵션, `:NEEDS[SCANSat]`)

RP-1은 SCANsat 자체 실험의 **과학 값만 재조정한다**(`SCANsatAltimetryLoRes`/`HiRes`,
`SCANsatBiomeAnomaly`, `SCANsatResources`, 모두 InSpaceLow). 실험과 스캔
커버리지 타이밍은 RP-1이 아니라 SCANsat 모드에 있다.

### 3.3 승무원 / 정거장 과학 (ROKerbalism 시간형)

`Science/Experiments/CrewScience/`(8개 파일, 약 60개 실험)에 큰 별도 계열이
있으며 boolean 계층 플래그로 캡슐/정거장/기지에 부착된다. 소요 시간은 약 18
min → 2 years에 걸친다. 대표 예시다.

| id | 연구 대상 | science | duration |
|----|---------|:-------:|----------|
| `RP0FlightControl` | 요/피치/롤 응답 | 20 | 3 h |
| `RP0EarthPhotography` | 손에 든 지구 촬영 | 40 | 6 h |
| `RP0TelevisionBroadcast` | 달로 가는 도중 생방송 TV | 80 | 4 h |
| `RP0ALFMED` | 우주선 광섬광 | 20 | 4 d |
| `RP0longDurationHabit1/2` | 장기 거주 | 750 / 1500 | ~180 d / **2 yr** |
| `RP0LunarOrbitHabit` | 달 궤도 거주 | 400 | 720 d |
| `RP0lunarSeismicNetwork` | 달 지진 네트워크 | — | 365 d |

(`StationScienceEarly.cfg.disable`은 비활성 상태로 배포된다 — 수집 불가.)

### 3.4 계층화, 적용 범위, 주의점

- **계층화.** 한 분야의 총 과학은 부품의 `totalScienceLevel` 비율을 통해 계측기
  계층에 나뉜다(우주선 T1 `0.375` → T2 `1.0`, 최상위 계층은 생략 = 풀 캡).
  상위 계층일수록 비용이 크고 시간이 길며 게이트가 까다롭다(이심률 / 태양 각도
  / 경사각). `GlobalExperimentPatches.cfg`는 `@dataScale /= baseValue`
  정규화기이며 **계층 엔진이 아니다**.
- **적용 범위.** 대부분의 계측기는 **바디 비종속적**이다 — 상황 마스크만
  충족되면 어떤 바디에서도 동작한다. 모항성 전용 예외. **Photography(전
  계층), Biological Sample, Cherenkov**.
- **RP-1에는 virtual biome이 없다.** **어떤 RP-1 실험도 `InnerBelt`/
  `OuterBelt`/`Magnetosphere`/`Interstellar`/`Storm`** virtual biome을
  참조하지 않는다. 그 Kerbalism 기계 장치는 존재하지만 **배포된 RP-1에서는
  쓰이지 않는다** — 따라서 방사선 벨트 / interstellar 과학은 활성 콘텐츠가
  아니라 *latent* 훅이다.
- **모항성 바디 지표는 과학 ≈ 0**이다(명시적 RP-1 설계 규칙).

출처. 로스터는 `GameData/RP-1/Science/Experiments/` @ master에서 추출했다
(소요 시간은 `@data_rate /= N` 줄에서 인용했으며, 일부 하위 계층 `data_rate` /
`totalScienceLevel` 리터럴은 요약자가 파생한 것이므로 cfg 배포 전에 확인할 것).

---

## 4. Per-body 작성 체크리스트 (NearStars, 양쪽 시스템)

새 바디 `<X>`(Kopernicus 내부 이름)마다 다음을 작성한다.

1. **`ScienceValues` (9개 필드)** — *가장* 중요한 노브이며 양쪽 시스템이
   읽는다. 배율은 거리/난이도에 따라 스케일된다(Kerbin = 0.3–1.5 바닥).
   무대기 → flyingLow/High = 1 플레이스홀더. **항성 → Sun 패턴을 복사한다**(큰
   `spaceAltitudeThreshold`, biome 없음).
2. **Biome map + `Biomes{}`** — 양쪽이 읽는다. 지표/저고도 상황에서 biome별
   다양성을 내려면 필요하다. 단색, mipmap 없음, `PluginData/`에 둔다. 항성은
   생략한다.
3. **상황 임계값** — 1단계의 두 임계값 필드로 처리된다.
4. **`ScienceDefs RESULTS{}`** — stock 실험마다
   `@EXPERIMENT_DEFINITION:HAS[#id[<exp>]]`, 키는 `<X><Situation>[<Biome>]`.
   **stock 플레이어 전용** — Kerbalism만 겨냥한다면 건너뛴다. NearStars가
   배치형/ROC 콘텐츠를 배포한다면 Breaking Ground id를 포함한다.
5. **(방사선 환경 — 게임플레이, RP-1 과학 아님)** — 바디의 방사선
   벨트/자기권을 정의하면(RP-1 통합 WS4. ROKerbalism `RadiationBody`,
   `:NEEDS[ProfileRealismOverhaul]`로 게이트,
   [`gameplay/rp1-integration/plan.md`](../../gameplay/rp1-integration/plan.md)) Kerbalism의
   `InnerBelt`/`OuterBelt`/`Magnetosphere`/`Interstellar` virtual biome이
   해당 바디에서 *해석 가능*해진다. 다만 **RP-1이 배포하는 실험은 virtual
   biome을 참조하지 않으므로(§3.4) 오늘날 RP-1에서는 과학이 나오지 않는다** —
   이는 방사선/생명 유지 사안이며, NearStars가 커스텀 실험으로만 끌어낼 수
   있는 latent 과학 훅이다.

**최소 동작 바디.** ScienceValues만(일반 텍스트, subject/situation 하나).
**풀 플레이버 바디.** ScienceValues + biome map + RESULTS 텍스트.

**겹침 요약.** RP-1에서 per-body 과학 작성은 **사실상 100% stock
작성**이다(biome + ScienceValues) — per-body Kerbalism 과학 cfg는 없고,
실험이나 상황 게이트는 절대 작성하지 않는다(글로벌 RP-1 콘텐츠, §3).
`RESULTS{}` 플레이버만이 stock 전용 투자이며, 방사선 환경은 과학 보상이
latent인 게임플레이/WS4 사안이다.

---

## 5. NearStars 현황과 메모

- **기존 골격.** `kopernicus-cfg` 스킬에 이미 biome 패턴이 있다(`planet-body.md`,
  `gas-giant.md`). `mod-release-layout.md`가 `[Body]-Kopernicus.cfg`(biome) +
  `[Body]-ScienceDefs.cfg`(결과 텍스트) + `[Body]_Biomes.dds`를 정의한다. Phase 4
  체크리스트에 "모든 바디의 과학 실험 텍스트" 항목이 있다. 구조는 존재하지만
  **per-body 과학 콘텐츠는 미작성이다.**
- **DB에는 과학 필드가 없다** — 과학 값/biome/텍스트는 `db/systems/*.json`에
  저장되지 않고 cfg-emit 시점(프로젝트 말미)에 작성된다.
- **Interstellar virtual biome**은 Kerbalism에 존재하며(항성 SOI 내부,
  헬리오포즈 바깥) NearStars에 주제적으로 잘 맞는다 — 다만 **어떤 RP-1 실험도
  이를 참조하지 않으므로(§3.4) 배포된 RP-1에서는 과학이 나오지 않는다**.
  NearStars가 커스텀 Kerbalism 실험으로만 활용할 수 있는 latent 훅이다.
- **이 문서에 반영된 전제 교정.** RESULTS 키에는 `@`가 없다, `:HAS[#id[]]`로
  주입한다, biome 매칭은 전체 RGB다, Kerbalism은 RESULTS 텍스트를 무시한다,
  ScienceValues는 정확히 9개 필드다, RP-1 실험은 virtual biome을 쓰지 않는다.

## Related

- [guideline](guideline.md) — Phase 4 과학 텍스트 체크리스트 항목
- [mod-release-layout](mod-release-layout.md) — `[Body]-ScienceDefs.cfg` / biome DDS 컨벤션
- [gameplay/rp1-integration](../../gameplay/rp1-integration/plan.md) — 방사선 환경 / WS4 겹침
