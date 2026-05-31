# Planet-Pack Visual Techniques — Reference Mining

> **출처** (읽기 전용 분석, 2026-05-30).
> - **SPVE** — SpacePotato's Volumetric Enhancements,
>   [`TheSpacePotato/...-Volumetric-Enhancements`](https://github.com/TheSpacePotato/SpacePotato-s-Volumetric-Enhancements)
>   @ `c33fefd8d7` (release 1.1, V3 + V5 빌드).
> - **Cosmic Serenity** —
>   [`ProximaCentauri-star/Cosmic-Serenity`](https://github.com/ProximaCentauri-star/Cosmic-Serenity)
>   @ `6f81ac01cf`.
> - **Promised Worlds** —
>   [`PromisedWorlds/PromisedWorlds`](https://github.com/PromisedWorlds/PromisedWorlds)
>   @ `b6484d1078`.
>
> **목적.** 세 개의 레퍼런스 행성/비주얼 팩에서 재사용 가능한 비주얼
> *기법* 과 config *컨벤션* 을 캐내어, NearStars 의 Kopernicus +
> Principia + Scatterer + EVE + Firefly + Parallax 스택에 활용한다.
> **기법만 가져온다 — config 텍스트나 에셋은 이 repo 로 복사하지 않는다.**
> 그 구분이 왜 중요한지, NearStars 가 무엇을 재사용할 수 있고 없는지는
> [§1 Licensing](#1-licensing--attribution) 참고.
>
> **로컬 전용 동반 자료.** Paid-Early-Access (blackrack release-5
> volumetric) 스키마 세부는 이 파일에 없다. [[feedback-patreon-assets]]
> 방침에 따라 `~/Desktop/ksp-mod-refs/_notes/` 에만 둔다.

---

## TL;DR

> **별 렌더링이 가장 값어치 높은 수확이다.** Kopernicus 의 전체
> `ScaledVersion` (sunspot/rim Material + Coronas), `Light` (강도 곡선 4
> 종), photosphere-as-`Atmosphere`, `HazardousBody` 레시피는 전부
> 자유롭게 배포 가능하며, 손으로 튜닝하는 대신 NearStars 가 큐레이션한
> Teff / L / R / mass 로부터 *생성* 할 수 있다. [§2](#2-star--stellar-object-rendering) 참고.

> **debris-disk 기법은 하나가 아니라 네 가지다.** 그중 가장 좋은 새
> 기법은 PW 의 stock-Kopernicus **Asteroid spawner** (무료, 실제로
> 스폰되는 벨트) 다. [§3](#3-debris-disks--rings--four-techniques) 참고.

> **라이선스가 세 팩을 깔끔하게 가른다.** PW config 는 CC-BY-NC-SA
> (호환 — 출처 표기하면 개작 가능), SPVE 는 CC-BY-NC (호환, 크레딧
> 필요), **Cosmic Serenity config 는 GPLv3 (비호환 — 기법은 배우되
> 텍스트는 절대 복사 금지), 텍스처/메시는 All-Rights-Reserved 다.**
> [§1](#1-licensing--attribution) 참고.

---

## 1. Licensing & attribution

**기본 원칙.** *기법·방법·아이디어는 저작권 대상이 아니다 — 구체적인
표현(config 텍스트, 텍스처, 메시, 컴파일된 코드)만 저작권으로 보호된다.*
이 문서에 담긴 것은 전부 **방법** 에 대한 서술이며, NearStars 는 이를
이해한 뒤 자유롭게 재구현할 수 있다. 아래 제약은 오직 **실제 파일을
복사하는 경우** 에만 적용된다.

### 1.1 팩별 라이선스

| Pack | Configs / "everything else" | Textures / meshes | NearStars (CC-BY-NC-SA 4.0) 와 호환? |
|------|------------------------------|-------------------|----------------------------------------------|
| **SPVE** | CC BY-NC 4.0 | CC BY-NC 4.0 | **예** — BY-NC 콘텐츠는 BY-NC-SA 저작물에 포함될 수 있다. 출처 표기 필수. |
| **Cosmic Serenity** | **GPL-3.0** | **All Rights Reserved** (ProximaCentauri) | **아니오 (configs)** — GPL-3.0 ⇄ CC-BY-NC-SA 는 복사한 텍스트에 대해 상호 비호환. **아니오 (assets)** — ARR. |
| **Promised Worlds** | CC-BY-NC-SA | CC-BY-NC-SA (일부 서브라이선스, 1.3 참고) | **예** — 동일 라이선스. 출처 표기 + ShareAlike 조건으로 개작 허용. |

### 1.2 NearStars 가 할 수 있는 것 / 없는 것

- **세 팩 모두.** 읽고, 배우고, **기법을 재구현** 하는 것 → 언제나 가능
  (아이디어는 저작권 대상이 아니다). 이 문서가 바로 그 작업이다.
- **SPVE (CC BY-NC).** config 텍스트 / 참조 스니펫을 **SpacePotato 크레딧과
  함께** 개작 가능. 비상업 한정 (NearStars 는 이미 비상업이다). Laythe
  구름 텍스처는 **StarCrusher96** 의 작업이므로 사용 시 크레딧 표기.
- **Promised Worlds (CC-BY-NC-SA).** config 텍스트를 **Emu /
  "Constructalor" + Promised Worlds Contributors 출처 표기 + ShareAlike**
  조건으로 개작 가능 (NearStars 자체 CC-BY-NC-SA 가 이를 충족한다).
  `PromisedWorlds.dll` 은 건드리지 말 것 (독점, 1.3 참고).
- **Cosmic Serenity.** **config 텍스트는 일절 복사 금지** (GPL-3.0 이
  NearStars config 를 GPL 로 강제하게 되어 CC-BY-NC-SA 와 비호환) 이고,
  **텍스처/메시도 사용 금지** (All Rights Reserved). CS 를 읽고 이해한
  기법을 재구현하는 것은 괜찮지만, cfg 를 붙여넣는 것은 안 된다.
- **blackrack의 True Volumetric Clouds** (별칭 *EVE Volumetrics*, **EVE-Redux**
  내장) — SPVE/CS/PW가 올라타는 볼류메트릭 구름 시스템이다. **V3·V5는 별도
  제품이 아니라 순차 릴리스 번호다.** V3는 무료 공개 릴리스(cfg 노드
  `layerRaymarchedVolume`), V5는 현재 유료 Patreon Early-Access 릴리스
  (`layerRaymarchedVolumeV5`)다. 유료 릴리스는 절대 재배포 금지, V5 전용 스키마
  사실도 로컬 전용으로 유지한다. 무료 release-3 스키마는 공개되어 있다.
  ([[feedback-patreon-assets]], [[reference-volumetric-clouds-naming]] 참고.)

### 1.3 번들된 서드파티 플러그인 (각자 라이선스)

이들은 CS/PW *안에* 함께 실리지만 별개 프로젝트다. MIT 인 것들이
NearStars 가 실제로 **사용/번들** 할 현실적인 후보다 (MIT 고지 유지 +
`NOTICE` 에 추가).

| Plugin | License | Author | 관련성 |
|--------|---------|--------|-----------|
| **VertexHeightOblateAdvanced** (DuckweedUtils) | **MIT** | © 2024 James Glaze | ★ 편평 fast-rotator 형상 — 실제 편평한 별/행성에 사용 가능. |
| **VertexColorMapEmissive** (DuckweedUtils) | **MIT** | © 2024 Lt_Duckweed | 채널별 emissive 지형 (Parallax 비호환 — scaled-space 전용). |
| **MitchellNetravali heightmap** (NiakoUtils) | **MIT** | © 2022 Niako | 더 매끄러운 저해상도 heightmap. `VertexHeightMap` 에 drop-in. |
| **ScaledDecorator** | **GPL-3.0** | (KSP forum) | `.unity3d` 프리팹을 scaled space 에 로드 (혜성 꼬리 / 제트 / 디스크). |
| **KopernicusExpansion Continued-er** | **GPL-3.0** | — | 웜홀 등 (NearStars 범위 밖). |
| **Sigma LoadingScreens** | ARR (cond. redistribution) | Sigma88 | 로딩 스크린 전용. |
| **PromisedWorlds.dll** (settings menu) | **Proprietary, ARR** | © 2026 averageksp | 복사/수정/리버스엔지니어링 금지. |

> **NearStars 가 플러그인을 번들하게 된다면.** `NOTICE` 와
> `docs/reference/data-sources.md` 에 라이선스와 함께 추가한다. MIT →
> 저작권 + 허가 고지 포함. GPL-3.0 → 단순 집합(aggregation) 으로 배포
> (별도 플러그인으로, NearStars 자체 라이선스 콘텐츠에 병합하지 않음).

---

## 2. Star & stellar-object rendering

가장 값어치 높은 영역이다. NearStars 는 **실제 별** 을 싣고 이미 Teff /
L / R / mass 를 큐레이션하므로, 이 팩들이 손으로 튜닝한 값은 전부
**계산해서 생성** 할 수 있다. 이 모든 것은 자유롭게 배포 가능한
Kopernicus 다.

### 2.1 ScaledVersion Material (눈에 보이는 별 표면)

`ScaledVersion { type = Star … Material { … } }` 아래.

- `sunspotTex` — 그레이스케일 photosphere 입상/흑점 맵. `sunspotPower`
  (Teff 가 높을수록 더 날카롭다 — 차가운 별은 관측상 ~10, 뜨거운 별은
  ~40), `sunspotColor` (어두운 흑점의 색조).
- `rimColor` / `rimPower` / `rimBlend` — limb 광채. 뜨거운 별일수록 더
  **좁은** rim 을 쓴다 (낮은 `rimPower`/높은 `rimBlend`).
- `emitColor0` / `emitColor1` — 내재 발광. 일반 별은 거의 검정에 가깝게
  둘 수 있지만 (외부에서 조명받음), **어두운 별(brown/white dwarf)** 은
  빛을 거의 내지 않더라도 잉걸불처럼 스스로 은은히 빛나도록 옅은 색의
  발광을 준다.
- `noiseMap` — photosphere 노이즈 추가 (exotic 별이 사용).

**NearStars 규칙.** 모든 색 (`sunspotColor`, `rimColor`,
`*SunlightColor`, `sunLensFlareColor`) 을 **Teff 의 blackbody→sRGB 변환**
에서 구동한다 — 기존 disk-color/Mie 합성을 재사용. `rimPower` 는 Teff 와
반비례로 유지. 마법 같은 숫자를 복사하지 말고 생성하라.

### 2.2 Coronas

`ScaledVersion { Coronas { <Value|Corona> { scaleSpeed, scaleLimitX/Y,
speed, rotation, updateInterval, Material { texture, invFade,
mainTexScale, mainTexOffset } } } }`. 자식 노드 이름 (`Value` vs
`Corona`) 은 동작에 **영향이 없다** — 둘 다 파싱된다. `mainTexScale = 0,0`
은 사실상 corona 를 억제한다 (밝은 halo 가 없는 dwarf 에 사용).

### 2.3 Light 블록 + 강도 곡선

`Body { … Light { … } }` 필드와 타입별 변화.

- 색상. `sunlightColor`, `scaledSunlightColor`, `IVASunColor`,
  `sunLensFlareColor`, `ambientLightColor` — 타입별로 가장 지배적인
  노브 (M/K 는 따뜻한 주황, G/F 는 흰색, A 는 청백, L/brown dwarf 는
  자홍/근적외, neutron star 는 파랑).
- `luminosity`, `insolation`, `sunAU` — **게임플레이 기준점.** 행성이
  실제 궤도에서 ≈1.0 을 받도록 `insolation` 을 맞추고, `sunAU` 는
  열/태양전지 스케일링용 1-AU-등가 기준 거리(m) 다.
- `sunFlare` — AssetBundle (`…unity3d:flareName`) 을 가리킨다. 팩들은
  **공유 플레어 하나** 만 싣고 별마다 `sunLensFlareColor` 로 재색조한다
  (플레어 N 개를 만드는 대신). 이걸 채택하자 — 단일 플레어 에셋을 Teff
  에서 색조 적용.
- `radiationFactor` — exotic 고방사 별에 존재 (pulsar 0.8).
- **곡선 4종** 이 카메라 거리에 따른 밝기를 구동한다.
  `IntensityCurve` (비행 중 조명), `ScaledIntensityCurve` (맵/원거리),
  `IVAIntensityCurve` (콕핏, 비행값의 ≈0.9×), `brightnessCurve`
  (lens-flare bloom). 레퍼런스 팩에서는 이들이 정확한 도함수 탄젠트를
  지닌 ~20 키 해석적 `1/r²` 스타일 falloff 다 — **명백히 툴로 생성한 뒤
  붙여넣은 것이다.**

> **NearStars 액션.** 제너레이터 하나를 작성한다 — `luminosity` 와 거리
> 그리드가 주어지면 곡선 4종을 전부 출력. Near-field 강도는 √L 로
> 스케일된다 (관측. 더 밝은 레퍼런스 별의 near 값이 어두운 쪽의 ≈2.2×
> 였고, 더 높은 광도를 따라갔다). 곡선을 손으로 편집하지 말 것.

### 2.4 Photosphere 를 `Atmosphere` 외피로

별 본체를 얇은 atmosphere 로 감싸 photosphere 를 물리적으로 만든다.
`enabled = true`, `oxygen = false`, `altitude ∝ stellar radius`,
`adiabaticIndex = 1.667` (단원자), 높은 `staticPressureASL` (~10–100,
단단한 벽), 그리고 **`temperatureSeaLevel = Teff`**. `temperatureCurve`
는 상단 부근에서 다시 올라가 **chromospheric 온도 역전** 을 흉내낼 수
있다. 온도/압력 곡선은 단순한 scale-height 모델에서 생성한다.

### 2.5 HazardousBody — "별 가까이 가면 타 죽는다"

`HazardousBody { Item { ambientTemp = <≈Teff or a death threshold>;
AltitudeCurve { … } } }` 는 반경 거리 → `ambientTemp` 의 분율로
매핑하며, 부품 파괴 온도에 키잉된다 (레퍼런스 주석은 키를 "4000 K = all
stock parts destroyed", "800 K = max EVA" 등으로 매핑한다). 곡선을 stellar
radius/luminosity 에서 생성하면 별마다 치명 반경이 올바르게 스케일된다.
atmosphere 없이도 실제 근접 위험을 부여한다.

### 2.6 Exotic 별

- **Pulsar / neutron star** (한 본체에 4 레이어 합성). 진짜 작은
  `radius` (~12 km), 짧은 `rotationPeriod` (~2.4 s), 파란 색조의 거의
  검은 `Material`, 파란 `Light` + `radiationFactor`, **ScaledDecorator**
  쌍원뿔 제트 프리팹 (`rotatesWithParent`, 자전축에서 기울어진 축), 그리고
  별이 계속 보이도록 `hideCelestialBody = False` 로 얹은 **Singularity**
  렌즈 셰이더 (§7 참고).
- **Brown / L-dwarf.** 어두운 `luminosity` (~1–2), 어두운
  `ambientLightColor`, 자홍/근적외 `emitColor0/1` (내재 잉걸불 발광),
  억제된 corona (`mainTexScale = 0,0`), 가까이서만 플레어가 피어나도록
  가파른 `brightnessCurve`.
- **White dwarf** (직접 관측이 아닌 합성). brown-dwarf 자가 발광 트릭을
  작은 radius + 뜨거운 청백색과 결합하고, 선택적으로 가시 본체에
  Singularity 를 얹어 옅은 렌즈 효과를 준다.

### 2.7 외형 토글

- **RealisticStarSize** — 설정 플래그에 게이트된 `@radius *= <factor>`.
  NearStars 는 (전역 상수 하나가 아니라) 별마다 실제 반경 대 과장된
  게임플레이 기본값으로부터 factor 를 계산해야 한다.
- **TUFX dual-tuning** — material 을 `:NEEDS[TUFX]` vs `:NEEDS[!TUFX]`
  로 이중화. TUFX bloom 이 있을 때는 `sunspotPower` / `rimBlend` /
  `rimPower` 를 *낮춰* 별이 과다 노출되지 않게 한다. bloom 이 인상을
  지배하는 어두운 별에서만 복제할 가치가 있다.
- **DistanceFactor** — `@semiMajorAxis *= <factor>` 로 시스템 간 거리를
  압축/확장.

---

## 3. Debris disks & rings — four techniques

NearStars 는 실제 debris-disk 호스트 (Vega/Fomalhaut/ε Eri 급) 를 갖고
있다. 팩들 전반에 네 가지 별개 메커니즘이 존재하니 경우에 맞게 고른다.

| # | 기법 | 출처 | 두께? | 비용 / 의존성 | NearStars 적합도 |
|---|-----------|--------|-----------|-------------------|---------------|
| 1 | **Raymarched EVE 볼륨, 환형 띠** | SPVE `rings.cfg` | **예** (3D, `min/maxAltitude` 띠) | EVE 만; 무료 V3 스키마로 동작 | ★★★ config 만으로 만드는 가장 좋은 두꺼운 먼지 디스크. |
| 2 | **Stock Kopernicus Asteroid spawner** | PW `Asteroids.cfg` | 해당 없음 (실제 스폰 본체) | Stock Kopernicus, 무료 | ★★★ 실제로 채굴/방문 가능한 벨트. 반경을 DB 와 연결. |
| 3 | **ScaledDecorator `.unity3d` 프리팹** | CS 혜성 꼬리 / pulsar 제트; PW 원시행성 디스크 | 예 (에셋 안에) | ScaledDecorator (GPL-3.0) + 커스텀 Unity 번들 | ★★ 가장 영화적이지만 에셋 제작이 필요. |
| 4 | **Stock Kopernicus Ring** (`useNewShader`) | SPVE/PW 가스 자이언트 | 아니오 (평면) | Stock Kopernicus | ★ 평범한 평면 고리만. |

**기법 1 메커니즘 (무료 V3, 배포 가능).** 전용 `EVE_CLOUDS / OBJECT`
(SPVE `rings.cfg` 안의 `Jool-rings` / `Dres-rings` — `Planets/*.cfg` 의
오로라 오브젝트와는 별개인, 실제 고리 오브젝트) 로, cloud-type `Item` 이
`minAltitude` 와 `maxAltitude` 를 설정한다 — 그 사이의 간격이 *곧*
디스크의 3-D 두께이며, 환형 슬랩으로 raymarch 된다 (예. Jool ≈ 2.95 Mm →
4.67 Mm). red-channel **coverage map** 이 환형과 틈새를 깎아내고, 아주
낮은 `density` + 어두운 `color` 가 불투명 대신 먼지처럼 보이게 한다.
선택적인 **파티클 필드** 가 개별 입자를 흩뿌리고, `ambientSound` 가 볼륨
내부에서 재생될 수 있다. (무료 EVE release-3 레이어와 동일 노드 —
paid-V5 와의 유일한 차이는 노드 *이름* 과 사소한 튜닝이니
`layerRaymarchedVolume` 기준으로 작성하라.)

> **참고.** SPVE 는 이 기법을 **행성 고리** (Jool, Dres) 에 시연한 것이지
> 항성/circumstellar 고리가 아니다 — SPVE 에 항성 고리 예시는 없다. 기법은
> circumstellar debris disk 로 전이되지만 그 적용은 우리 몫이지 복사한
> config 가 아니다. (Jool 은 별도의 평면 Kopernicus `Ring` 도 함께 갖는데,
> 3-D 두께·헤이즈를 만드는 쪽은 EVE 볼륨이다. SPVE 자체는 DLL 을 전혀 쓰지
> 않는다 — 이 효과들은 기존 EVE 렌더링을 활용한 순수 config 이며 엔진 개조가
> 없다.)

**기법 2 메커니즘 (무료).** 예컨대 `ProtoplanetaryDisk-*` 로 명명한
Kopernicus `Asteroid` 정의로, `Locations { Around { Body {
semiMajorAxis = min/max; inclination; eccentricity } } }` 와 여러 반경
존을 둔다 — 실제 소행성을 벨트로 스폰한다. `semiMajorAxis` /
`inclination` 을 실제 디스크 반경에서 구동한다.

> **SpaceDust 는 여기서 디스크-비주얼 옵션이 아니다.** 두 팩 모두
> `SPACEDUST_RESOURCE` (채굴 가능 띠) 만 쓰고 `SPACEDUST_CLOUD` 비주얼
> 렌더링은 전혀 안 쓴다. 모드 자체는 보이는 먼지를 렌더할 *수* 있지만,
> 어느 팩도 그걸 시연하지 않으니 가져올 예제가 없다.

---

## 4. Aurorae & emissive volumetric FX

세 팩 모두 같은 방식으로 aurora 를 렌더하며, **SPVE 가 무료 release-3
스키마에서도 작동함을 증명한다** → 배포 가능.

- 메커니즘. **`layer2D`** (`macroCloudMaterial` 에 높은 `_MinLight` →
  자가 조명 2D 시트) **+ 외부광을 무시하도록 구성한 raymarched 볼륨** 을
  결합한 `EVE_CLOUDS / OBJECT`. `lightMarchSteps = 0`,
  `lightMarchDistance = 0`, `receivedShadowsDensity = 0`,
  `skylightMultiplier = 0`. light marching 이 없으면 볼륨은 태양 방향과
  무관하게 자기 자신의 평평한 `color` 를 렌더한다 → **자가 발광** 으로
  읽히고 밤쪽에서도 보인다. (raymarched volumetric cloud 에는 진짜 발광
  채널이 없으므로 이게 표준 우회법이다.)
- 키가 크고 얇은 고도 띠와 손으로 빚은 `coverageCurve` / `densityCurve`
  를 지닌 `AuroraCurtain` 류 cloud type 이 커튼 형태를 만든다.
- **무료 vs 유료.** `layerRaymarchedVolume` (release-3) 기준으로 작성.
  CS/PW aurora 는 대부분 유료 `…V5` 노드를 쓰니 그 세부는 로컬에 둔다.

같은 `fxOnlyLayer = True`, `density = 0` 보이지 않는 볼륨 패턴이
**지역 앰비언스** (SDF coverage map 을 통한 지리적 사운드/파티클 트리거)
와 **데칼 효과** (무지개, 해안/숲 앰비언스) 에도 재사용된다 — "당신은
영역 X 안에 있다" 를 깔끔하게 표현하는 범용 메커니즘이다.

---

## 5. Atmospheres, oceans, Scatterer

- **Scatterer atmosphere** (`Scatterer_atmosphere { Atmo { … } }`).
  Rayleigh/Mie beta, `useOzone` + `ozoneAbsorption/Height/Falloff` (**범용
  성층권 흡수체** 슬롯 — [[project-phase3-stratospheric-absorbers]] 참고),
  `multipleScattering`, `godrayStrength` (~0.7 이 무난한 기본값),
  `averageGroundReflectance`.
- **재정의 말고 패치하라.** 기존 atmosphere 를 다시 선언하는 대신
  `@Atmo:HAS[#name[X]] { … }` 를 `:LAST`/`:AFTER` 와 함께 써서 재튜닝한다
  — 충돌을 최소화한다.
- **대기 없는 본체의 구름 통합.** Scatterer `planetsList` 에 본체를
  `flatScaledSpaceModel = True` + `usesCloudIntegration = True` 로
  등록하면, 명목상 대기가 없는 본체에도 EVE aurora/디스크가 올바른
  **별 색** 을 받아낼 만큼의 가짜 대기가 생긴다.
- **다중성 Scatterer (필수).** 각 `planetsList` Item 은
  `mainSunCelestialBody = <local star>` 와 본체별 `eclipseCasters` 를
  설정한다. NearStars 의 Scatterer 작성기는 시스템마다 이를 출력해야 한다.
- **Oceans** (`Scatterer_ocean { Ocean { … } }`). `AMP`, `m_windSpeed`,
  `m_omega`, **`m_gravity` = 본체의 실제 표면 중력**, `m_whiteCapStr` /
  `shoreFoam`, `m_oceanUpwellingColor` + `m_UnderwaterColor` (물이 아닌
  외관은 색으로만 — 용암/암모니아는 특수 셰이더 없이 순전히 색으로
  처리), `transparencyDepth` / `darknessDepth`, `refractionIndex = 1.33`,
  그리고 전체 `caustics*` 블록. NearStars 의 어떤 해양 행성에든 turnkey 다.
- **Sunflare 오버라이드 충돌 가드.** 호스트 별의 플레어를 오버라이드할
  때는 `:NEEDS[!BetterKerbol,…]` 로 게이트해 다른 별 모드와 다투지 않게
  한다.

---

## 6. PQS terrain recipes (procedural, no real heightmap)

실제 DEM 이 없는 외계행성을 위해, 이 스택들은 그럴듯한 지형 기복을
생성한다.

- **VoronoiCraters** (multi-pass. big/medium/tiny, 각각 `CraterCurve`
  + `JitterCurve` 베지어, `voronoiFrequency`, `jitterHeight`) — 대기 없는
  위성을 위한 현실적인 크레이터링.
- **VertexHeightNoiseVertHeightCurve2** (Low/High ridged 모드, 서로 다른
  seed, 레이어별 `simplexCurve`) + **VertexRidgedAltitudeCurve** +
  **LandControl** (`createScatter = true, createColors = false` 인
  `_LandClassOcean` 가 재색칠 없이 고도에서 scatter 를 씨앗으로 심는다) —
  완결된 "heightmap 없는" 기복 레시피.
- **VertexHeightOblateAdvanced** (MIT 플러그인). `oblateMode`
  (`PointEquipotential` | `UniformEquipotential` | …), `energyMode`,
  `period`, `geeASL`/`mass` — fast rotator 를 위한 해석적
  Maclaurin/Jacobi 편평도. ★ 실제 편평한 별/행성에 알맞은 도구. 별의
  ScaledVersion 메시를 구동할 수 있는지 검증할 것 (이것은 PQS mod 다).
- **MitchellNetravali heightmap** (MIT 플러그인). `VertexHeightMap` 에
  drop-in 인 bicubic 필터 — 저해상도 맵에서 더 매끄러운 지형.

---

## 7. Parallax conventions (fills the pending Parallax reference)

([[project-nearstars-mod-refs-pending]] 의 "Parallax still unwritten"
항목을 해소한다.)

- **ParallaxScaled / `Terrain.cfg`** (`@ParallaxTerrain … :FINAL`).
  `ParallaxScaledProperties { mode = FromTerrain; Material {
  _ColorMap / _BumpMap / _HeightMap }; TerrainMaterialOverride { … } }`
  에 고도별 텍스처 밴딩 (`_LowMidBlendStart/End`, `_MidHighBlendStart/End`),
  regolith `_Hapke`, `_SteepPower/Contrast/Midpoint`. 범용 subdivision
  노드를 넘어서는, 실제 surface+scaled material 스키마다.
- **Subdivision 주입.** `:NEEDS[ParallaxContinued]` 패치로 본체마다
  `PQS { Mods { Parallax { subdivisionLevel, subdivisionRadius,
  order = 999999 } } }` 를 추가.
- **ParallaxScatters** (표면 scatter 시스템).
  `collisionLevel` (0–4, 착륙용 충돌 가능 바위),
  `BiomeBlacklist { name = … }` (biome 게이트 배치),
  `DistributionNoise { noiseType, inverted, frequency, octaves, seed }`
  (군집화), `Distribution { spawnChance, populationMultiplier,
  min/maxScale, steepPower/Contrast, min/maxAltitude, alignToTerrainNormal,
  coloredByTerrain }`, `LODs { LOD { model, range } }`, 그리고
  `Keywords { REFRACTION; SUBSURFACE_SCATTERING }` + `_RefractionEta` /
  `_SubsurfaceColor` 를 통한 크리스털 scatter. Stock Parallax 모델
  아틀라스를 재사용할 수 있어 커스텀 메시가 필요 없다.

---

## 8. EVE weather / particle / effect library

하우스 스타일로 채택할 만한, 재사용 가능한 named-effect 패턴이다.
효과는 한 번 정의하고 어느 cloud 볼륨에서든 **문자열 이름** 으로
참조하여, "무엇이 일어나는가" 를 "어디서/언제" 와 분리한다.

- `EVE_PARTICLE_FIELD_CONFIG` — 비, 눈, 우박, 재, 먼지, 유성우, 고리
  입자 (`fallSpeed`, `tangentialSpeed`, `fieldParticleCount`,
  `particleSheetCount`, 선택적 `splashes {}`).
- `EVE_DROPLETS_CONFIG` — 렌즈/캐노피 젖음 효과.
- `EVE_LIGHTNING_CONFIG` — 번개 (`spawnChancePerSecond`, `boltHeight`,
  사운드 리스트). cloud type 에서 `lightningFrequency` 로 연결.
- `EVE_WET_SURFACES_CONFIG` — 강수 아래 지형 젖음.
- **에피소드 스케줄러.** `timeSettings { unit; duration; repeatInterval;
  offset; fadeTime }` 가 기능 전체를 시계에 게이트한다 — 예컨대 주기적
  먼지폭풍, 계절성 aurora, 유성우.
- **마스크 하나에서 나오는 일관된 폭풍.** 단일 cloud-type coverage
  그래디언트가 `particleFieldDensity` / `lightningFrequency` /
  `dropletsDensity` / `wetSurfacesIntensity` 를 통해 구름 + 비 + 번개 +
  지면 젖음을 동시에 스케일한다.

이 config *노드 타입* 들은 무료 release-3 EVE 에 존재하며, 전부 무료인
particle/droplet/lightning/wetSurface 라이브러리는 그대로 재사용 가능하다.

---

## 9. Scene-level visuals

- **TUFX post-processing** (`TUFX_PROFILE { Antialiasing; EFFECT
  ColorGrading{ Tonemapper = ACES }; EFFECT Bloom{ Intensity, Threshold,
  Diffusion }; EFFECT AutoExposure }`) — 팩의 비주얼 정체성을 규정한다
  (ACES + 별 광채를 위한 강한 bloom). 프로파일은 이름이 붙고, 씬 바인딩은
  cfg 가 아니라 TUFX 자체 UI 에서 한다.
- **PlanetShine** (`PlanetshineCelestialBody { color (0–255), intensity,
  isSun }`) — 본체별 반사광. 색은 Phase 3 본체 색에서 도출.
- **DistantObjectEnhancement** (`CelestialBodyColor { name, color }`) —
  원거리 플레어/점 색조. 역시 Phase 3 색에서 도출 가능.
- **Rescale 페이드.** real-scale 빌드는 scaledSpace 페이드에
  `@fadeStart *= f` / `@fadeEnd *= f` 가 필요하다 (팩들은 rescale 패치에서
  이를 한다 — NearStars 가 Sol-real-scale 이므로 관련 있다).

---

## 10. Config organization & ModuleManager patterns

가장 강한 *구조적* 교훈이다 (두 다중-시스템 팩이 여기서 수렴한다).

- **시스템별 자기완결 폴더 트리.**
  `_Systems/<Star>/{Configs, EVE, Scatterer, Parallax, Firefly,
  ScaledDecorator}` + 공유 `_Core/` (베이스 텍스처, 사운드) + `Miscs/`.
- **시스템별 sentinel + 삭제 가능성** (PW). `00SystemExists.cfg` 에
  `SYS_DUMMY { name = System<Star> }` 를 정의하고, 하위 패치를 전부
  `:NEEDS[…&System<Star>]` 로 게이트. 한 시스템의 폴더를 지우면 모든 것
  (EVE, 리소스, Scatterer) 이 조용히 no-op 된다. 다수의 별 팩에 탁월하다.
- **중앙 settings 노드 + 플래그 토글.** `:HAS[@<Settings>:HAS[
  #Flag[?rue]]]` (`?rue`/`?alse` 단일 문자 와일드카드가 True/true 대소문자
  를 매칭) 으로 파일을 포크하지 않고 선택 기능을 전환한다.
- **태그 기반 일괄 선택.** 본체를 `Tag` (`NS_Star`, `NS_Planet`, …) 로
  분류하고 이름을 일일이 열거하는 대신 `@Body:HAS[#Tag[NS_Star]]` 로
  패치한다.
- **다중 설치 적응 (NearStars 의 Sol-real-scale MVP 에 직결).**
  `@…:AFTER[SolSystem]:HAS[@Sol_Configuration:HAS[
  #SystemScale[Real|Quarter|Stock]]] { … }` 에 Sun-orbit `:NEEDS[!SolSystem]`
  fallback 을 더한다 — config 하나가 RSS/Sol 스케일이나 stock 에 적응한다.
- **`:HAS[#name[X]]` + `:LAST`/`:AFTER`** 로 기존 Scatterer/EVE 노드를
  외과적으로 패치하고, **`:NEEDS[!OtherPack]`** 가드로 우아하게 degrade
  하며, 플러그인 로드 순서를 위해 숫자 폴더 접두사 (`000_`, `001_`) 를 쓴다.
- **보이지 않는 barycenter 레시피** (PW, Kopernicus/Keplerian 레이어용).
  `Template { name = Jool; removeAtmosphere = true }` 본체를 아주 작은
  `radius` 로 줄이고, `ScaledVersion { invisible = true; Material color =
  0,0,0,0 }`, `hiddenRnD = true`, `mode = OFF` (궤도선 숨김). 보이는
  컴포넌트들은 `referenceBody` 를 이걸로 설정한다. (NearStars 의 비주얼
  바이너리 접근을 확증한다 — 다만 NearStars 는 실제 바이너리를 Keplerian
  이 아니라 Principia n-body 로 푼다.)

기타 주목할 만한 것들. dim interstellar 시스템을 위한 SCANsat
`requireLight = false` 패치, `displayName = …^N` 로컬라이저 마커를 쓴
biome 키 지역 crew report, 5개 언어 로컬라이제이션 레이아웃.

---

## 11. Quality cautions / what NOT to copy

- **전부 stock-scale 이다.** 모든 radii, altitude, SOI, luminosity /
  intensity / temperature 곡선, `HazardousBody` 임계값, raymarching
  `baseStepSize`/`maxStepSize`/`scaledFadeAltitude`, ring 띠가 **stock
  Kerbin 반경과 Kerbol** 에 (또는 ~100× 압축된 시스템 간 거리에) 맞춰져
  있다. **구조는 복사하되 숫자는 절대 복사하지 말 것** — NearStars 는
  Sol-real-scale 이다.
- **두 팩 모두 별이 barycenter 없이 `Sun` 을 직접 돈다.** 이 모델은
  NearStars 의 Principia n-body 실제 바이너리 시스템에는 **이전되지
  않는다.**
- **복붙 아티팩트** 가 넘친다 (별 이름이 틀린 corona 텍스처 경로, 중복된
  `…V5`/`LayerRaymarchedVolumeV5` 노드, 토씨 그대로 복사한 사운드 리스트,
  SPVE 의 "무료" V3 빌드 안에 끼어든 V5 노드). V3 cfg 를 템플릿으로 캘
  때는 배포 전에 **`…V5` 를 솎아낼 것.**
- **VertexColorMapEmissive 의 비호환은 설치 단위가 아니라 표면-레이어
  단위다.** VCME 는 발광을 세 군데 (ScaledVersion / PQS 지형 / Ocean) 에
  넣는데, 자체 README 에 따르면 **지형(PQS)** 레이어는 Parallax Continued
  (자체 지형 셰이딩을 가짐) 가 무효화하고 **Ocean** 레이어는 Scatterer
  바다에선 작동하지 않는다 (스톡 바다만). 세 모드는 한 설치에 공존은
  문제없다 — 다만 NearStars 바디 (Parallax + Scatterer) 에서는 VCME 의
  **ScaledSpace / 궤도뷰** 발광만 작동하고, 근접 지형 발광과 Scatterer 바다
  발광은 안 된다. 따라서 NearStars 에서의 용도는 궤도뷰 발광 (예. 맵/우주에서
  보이는 용암 world) 에 한정된다.
- **이 팩들엔 single source of truth 가 없다** (한 본체를 편집하면 여러
  파일을 건드려야 한다) — NearStars 의 derived-from-DB 파이프라인과는
  정반대다. NearStars 의 생성 모델은 유지하고, 출력 컨벤션만 빌려온다.

---

## 12. Priority adoption list for NearStars

1. **별 렌더링 제너레이터** — Material/Light/Coronas/Atmosphere/
   HazardousBody + intensity 곡선 4종, 전부 큐레이션한 Teff / L / R / mass
   에서 계산. 최고 가치이며 전적으로 무료/배포 가능. (§2)
2. **Debris disk** — raymarched EVE 환형 볼륨 (무료 V3, config-only)
   그리고/또는 stock Asteroid spawner. 호스트별로 골라 실제 디스크
   반경에서 구동. (§3)
3. **Parallax Terrain + Scatters 스키마** 를 Parallax 스킬에 반영. (§7)
4. 실제 편평 fast rotator 를 위한 **`VertexHeightOblateAdvanced` (MIT).** (§6)
5. 다수 별 시스템의 에셋 레이어 조직으로서 **다중-시스템 폴더 +
   sentinel `:NEEDS[&SystemX]` 격리.** (§10)
6. **Scatterer 다중성** (`mainSunCelestialBody` + `eclipseCasters`) 과
   **ocean** 템플릿. (§5)
7. **무료 스키마 aurora** + named EVE 효과 라이브러리 하우스 스타일. (§4, §8)
8. Phase 3 색에서 가져온 **TUFX / PlanetShine / DOE 색 테이블**,
   **rescale fade** 스케일링. (§9)
9. **다중 설치 `:HAS[#SystemScale[…]]` 적응** 패턴. (§10)

---

## Sources

- SPVE — <https://github.com/TheSpacePotato/SpacePotato-s-Volumetric-Enhancements> (CC BY-NC 4.0)
- Cosmic Serenity — <https://github.com/ProximaCentauri-star/Cosmic-Serenity> (configs GPL-3.0; assets ARR)
- Promised Worlds — <https://github.com/PromisedWorlds/PromisedWorlds> (CC-BY-NC-SA; bundled plugins MIT/GPL-3.0; settings DLL proprietary)
- blackrack True Volumetric Clouds / EVE-Redux — Patreon (paid EA; see [[reference-volumetric-clouds-naming]])
