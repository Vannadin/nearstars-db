---
title: KSP 모드 제작 지식 베이스 — 인덱스
status: living
created: 2026-06-30
---

# KSP 모드 제작 지식 베이스

**무엇인가.** NearStars C# 플러그인(상대론·워프·플래너·플럭스튜브)을 KSP 1.12.x에서 작성하기 위한, 클로드가 참조하는 **근거화된** 지식 베이스다. 스톡 API 지식이 그간 근거 없는 훈련 기억이었고 — 그 기억이 최소 한 번 틀렸기 때문에(`ScaledSpace.Factor` → 실제로는 `ScaleFactor`) — 존재한다. 이 KB는 주장을 인용으로 대체하며, **기억 덤프가 아니라 근거화로 누적**한다.

**근거화 정책(여기 모든 문서에 적용).**
- KSP는 **클로즈드소스**다. `file:line`으로 인용할 공개 KSP 레포가 없으므로, 모든 스톡 API 주장은 **그 API를 호출하는 오픈소스 모드가 witness**가 된다(모드가 `FlightGlobals.fetch.SetVesselTarget(...)`을 컴파일한다는 건 그 멤버가 존재한다는 증거다). 인용은 `repo path:line`(+ permalink)이며 raw 파일을 직접 받아 확인한다.
- **신뢰도:** **H** 직접 코드 witness · **M** 디컴파일 XML 문서 미러 / 간접 · **L** 미확인 / 추정.
- **DLL 디컴파일이 gold standard이나 보류** — 이 개발 머신에 KSP 설치본이 없다. 확보되면 `Assembly-CSharp.dll`(ILSpy/dnSpy)이 M-신뢰도 항목을 대체한다. 라이선스: **interop 사실만** 커밋하고, DLL과 원시 디컴파일 덤프는 로컬·gitignore로 둔다. [[project_ksp_stock_api_grounding]] 참조.

---

## 커버리지 맵

| # | 기둥 | 집 | 상태 |
|:-:|--------|------|--------|
| ① | **스톡 C# API** (Assembly-CSharp 표면) | [`ksp-stock-api.md`](ksp-stock-api.md) | **live** — 플래너 슬라이스(타깃·맵 카메라·scaled-space 렌더·궤도/바디 데이터). 건드릴 때마다 확장 |
| ② | **플러그인 스캐폴딩·빌드** (KSPAddon, PartModule, VesselModule, MonoBehaviour 생명주기, .csproj/refs, AssemblyLoader, 배포) | [`plugin-scaffolding.md`](plugin-scaffolding.md) | **live** |
| ③ | **Unity-for-KSP** (GameObject/Transform, 코루틴, LineRenderer/GL, IMGUI, 레이어, ScaledSpace) | [`unity-for-ksp.md`](unity-for-ksp.md) | **live** |
| ④ | ModuleManager & ConfigNode (패치 문법, persistence 노드) | — | 보류(우선순위 낮음. cfg 쪽은 아래 스킬에 일부 있음) |
| ⑤ | **Persistence & Harmony** (OnSave/OnLoad, ProtoVessel, 시나리오 모듈, Harmony 패턴, part-force / `FashionablyLate` 채널) | [`persistence-harmony.md`](persistence-harmony.md) | **live** |
| ⑥ | 통합 서브시스템 (Kopernicus, Principia, Kerbalism, Firefly, ResearchBodies) | *스킬 + 레퍼런스* | **이미 근거화됨** — 아래 참조, 여기서 중복하지 않음 |

**2026-06-30 선택 범위:** **플러그인 작성 코어(①②③⑤)** 우선 — NearStars C# 플러그인을 막고 있는 진짜 갭이다. ④는 보류, ⑥은 이미 커버됨.

### ⑥은 이미 다른 곳에서 근거화됨(중복 금지)
- cfg 작성 스킬: `kopernicus-cfg`, `firefly-cfg`, `principia-cfg`, `researchbodies-cfg`
- [`principia-cfg-reference`](../principia-cfg-reference.md) — 오픈소스(MIT), `file:line` 인용

---

## 열림 / 보류 (단정 금지)
- **성간 스케일 맵뷰** — 광년 밖 바디를 스톡 맵뷰에서 선택/렌더할 수 있는가? 공개 소스로 답할 수 없고, DLL이나 인게임 실측이 필요하다. [`ksp-stock-api.md` §6](ksp-stock-api.md) 참조.
- **KB 미확인 갭** (M/L, witness 대기) — `VesselModule.OnSave` 오버라이드, `[KSPScenario]` 속성 인자+등록 경로, `part.AddForceAtPosition`, `WaitForSeconds`/`WaitForFixedUpdate`. 각 기둥 문서의 *Gaps* 절 참조.
- **DLL 디컴파일** — gold-standard 근거화, KSP 설치본 확보 시까지 보류.

## Related
- [`gameplay/interstellar-expansion/`](../../../gameplay/interstellar-expansion/) — 이 KB가 봉사하는 플러그인들
- [`plugins/`](../../../../plugins/) — 이 KB가 해소하는 draft C#의 `// VERIFY:` 마커들
