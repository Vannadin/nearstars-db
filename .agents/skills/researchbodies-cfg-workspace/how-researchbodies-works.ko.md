# ResearchBodies 모드는 어떻게 돌아가는가

> NearStars discoverability 레이어가 올라타는 모드. JPLRepo/ResearchBodies
> v1.13.0.0 소스 정독 기준. 모든 스키마 사실은 `<파일>.cs:line` 으로 확인됨.

## 한 줄 요약

천체를 **"아직 발견 안 된" 상태로 숨긴다.** 플레이어가 망원경/관측소로
직접 발견하기 전까지는 추적소·지도·기동 계획 어디에도 그 천체가 안 보인다.

---

## 플레이어 체감 흐름

1. 게임 시작 시 일부 천체는 **숨겨진 상태**(미발견). 추적소에 점으로도 안 뜬다.
2. 발견하려면 **관측소 연구 플랜**을 돌리거나 **망원경 파트**
   (`ModuleTrackBodies`)로 하늘을 관측한다. 거리·각도·전력 조건을 만족하고
   과학 점수를 지불하면 발견된다.
3. 발견 순간 **ONDISCOVERY 메시지**가 화면에 뜬다(그 천체에 대한 플레이버 텍스트).
4. 발견 후에는 정상적으로 보이고 탐사 가능.
5. (옵션) Contract Configurator 연동 시 "이 천체를 발견하라" 계약도 생성된다.

---

## 우리가 cfg 로 제어할 수 있는 것 — 딱 2개 (per-body)

최상위 노드는 `RESEARCHBODIES` 하나뿐이고, 아래 둘은 그 **서브노드**다.

| 노드 | 역할 | 형식 |
|------|------|------|
| **ONDISCOVERY** | 발견 시 뜨는 메시지 | `바디이름 = 메시지` |
| **IGNORELEVELS** | **시작부터 보일지 / 숨길지**(난도별) | `바디이름 = easy normal medium hard` (true/false 4개) |

서드파티 팩은 반드시 `loadAs = mod` 를 넣어야 한다. 없으면 RB 가 그 노드의
발견 데이터를 **조용히 무시**한다(`Database.cs:289`).

### IGNORELEVELS 가 핵심 메커닉

4개 boolean 이 각각 Easy/Normal/Medium/Hard 난도에 대응하고, 플레이어가 고른
난도의 칸만 읽는다.

- `true` = 시작부터 **보임**(이미 발견 처리)
- `false` = **숨김**(직접 발견해야 함)

예: `Polyphemus = true false false false` → Easy 에선 처음부터 보이지만,
Normal 이상에선 직접 관측해 발견해야 한다.

⚠️ **기본 동작 주의: 항목을 안 쓰면 전 난도에서 숨김**(기본값
`false false false false`, `CelestialBodyInfo.cs:40`). 그래서 항성처럼 "항상
보여야 하는" 천체는 **반드시 `true true true true` 를 명시**해야 한다.

또한 값은 **정확히 4개의 `true`/`false`** 여야 한다. `1`/`0` 은 안 되고, 개수가
모자라면 게임이 throw 한다(`Database.cs:258-259`).

---

## 우리가 제어 못 하는 것 — 전부 전역(global)

발견 비용, 발견 확률(`chances`), 망원경 사거리, 과학 보상 — 전부 모드 전체에
하나로 적용된다. **천체별로 "이건 발견 어렵게"는 불가능.** per-body 세분화
천장이 딱 ONDISCOVERY + IGNORELEVELS 둘이다.

즉 우리가 천체별로 표현할 수 있는 "발견 난도"의 유일한 수단은 **"몇 번째
난도부터 숨길까"** 다.

### 바리센터 자동 처리

반지름 100m 미만 천체(Kopernicus 바리센터/이중성 앵커)는 RB 가 자동으로
감지해 발견 목록 UI 에서 제외한다(`Database.cs:91,164`). 이런 앵커에는 발견
데이터를 쓸 필요가 없다.

---

## NearStars 가 이걸 쓰는 방식

천체의 **실제 검출 상태**를 → **"몇 번째 난도부터 숨길까"** 로 번역한다.
항성만 항상 보이고, **행성은 기본적으로 관측 발견**(Easy 에서만 미리 보임),
가상 위성은 어느 난도든 발견 대상이다.

| 카테고리 (실제 검출 상태) | E N M H | 플레이어 체감 |
|---|---|---|
| `naked_eye` (맨눈 항성) | `T T T T` | 어느 난도든 항상 보임 |
| `confirmed` (확정 행성) | `T F F F` | Easy 만 보이고, Normal+ 에선 관측해 발견 |
| `candidate` (JWST 후보 등) | `T F F F` | 확정 행성과 동일 (관측 발견) |
| `disputed` (논쟁/예측) | `T F F F` | 동일 |
| `fictional` (가상 위성) | `F F F F` | 어느 난도든 직접 도달/관측해야 발견 |

행성은 확정이든 후보든 모두 관측 발견이고, 둘의 차이는 ONDISCOVERY **메시지**에만
남는다(확정=견고한 검출 인용, 후보=잠정 검출 인용). 후보·논쟁 천체의 ONDISCOVERY
메시지에는 **실제 검출 논문을 인용**한다
(예: Polyphemus = Sanghi & Beichman 2025, JWST/MIRI 직접촬영 후보 S1). 이게
NearStars 의 "실제 관측 근거" 정체성 — 인게임 발견이 실제 외계행성 검출을
재현한다.

---

## 출력 예시

```
RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus]
{
    loadAs = mod
    name = NearStars

    ONDISCOVERY
    {
        Polyphemus = JWST/MIRI 15.5um 직접촬영으로 알파 센타우리 A 곁 희미한 동반체 후보 "S1" 포착. (Sanghi & Beichman 2025)
    }
    IGNORELEVELS
    {
        // body = easy normal medium hard
        AlphaCentauriA = true true true true       // naked_eye
        Polyphemus     = true false false false    // candidate
        Pandora        = false false false false   // fictional
    }
}
```

---

## RP-1 호환성 주의

RB 는 발견 메커닉을 굴리려고 **stock 테크트리 망원경 파트**
(`TechRequired = spaceExploration`, `entryCost = 9530`) + **자체 CC 계약**을
들고 온다. RP-1 은 완전히 다른 커스텀 테크트리 + 경제를 써서, 그 파트가
해금 불가가 되면 우리 천체가 영영 숨겨진 채 소프트락이 날 수 있다.

→ **현재 타깃은 비-RP-1**(RSS 의 Sandbox/Science). discoverability 는
`:NEEDS[ResearchBodies&Kopernicus]` 옵셔널이라 RB 미설치 시 전부 정상 가시.
RP-1 통합(allowTrackingStationLvl1 로 파트 의존 제거 + RB 계약 비활성)은
추후 업데이트로 보류, 설계는 `references/rp1-compat.md` 에 문서화됨.
