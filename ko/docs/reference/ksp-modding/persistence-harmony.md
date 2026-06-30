---
title: KSP persistence & Harmony (기둥 ⑤)
status: draft
created: 2026-06-30
---

# Persistence & Harmony

플러그인 상태를 게임 세이브에 저장하는 것, 그리고 Harmony로 스톡 동작을 패치하는 것을
다룬다. 근거화 정책과 범례는 [`README`](README.md) 참조. 따로 표기하지 않으면 모든 행은
**H**다.

---

## A. Persistence

### A1. `ConfigNode` API (H)

| 메서드 | witnessed | 인용 |
|---|---|---|
| `AddValue(name, val)` | `node.AddValue("subtype", subType)` | ContractConfigurator `ConfiguredContract.cs:517` |
| `GetValue(name) → string` | `node.GetValue("subtype")` | `ConfiguredContract.cs:425` |
| `TryGetValue(name, ref var) → bool` | `node.TryGetValue(nameof(x), ref x)` | KSPCommunityFixes `QoL/AltimeterHorizontalPosition.cs:57` |
| `AddNode(name) → ConfigNode` | `local.AddNode(name)` | MechJeb2 `MechJebCore.cs:638` |
| `GetNode(name)` / `HasNode(name)` | `local.HasNode(name) ? local.GetNode(name) : null` | MechJeb2 `MechJebCore.cs:612` |
| `HasValue(name)` | `cfg.HasValue(key)` | Kerbalism `Lib.cs:~3130` |

### A2. `PartModule` 저장/로드 (H)

`class X : PartModule` → `public override void OnSave(ConfigNode node)` /
`OnLoad(ConfigNode node)` (전체 구현: MechJeb2 `MechJebCore.cs:612/551`; `base.OnSave/OnLoad`만
쓴 최소형: KSP-Recall `Driftless/PartModule.cs:57/63`). 자동 persist되는 필드.
`[KSPField(isPersistant = true)] public bool running;` — MechJeb2
`MechJebCore.cs:45`; KSP-Recall `PartModule.cs:28`.

### A3. `VesselModule` 저장/로드 (혼합)
생명주기 + `OnLoad`는 [`plugin-scaffolding.md` §3](plugin-scaffolding.md)에 근거화되어 있다
(kOS `kOSVesselModule.cs`). **`OnSave(ConfigNode)` 오버라이드는 확인되지 않았다(M)** —
스톡 베이스는 이를 대칭으로 노출한다. 의존하기 전에 확인한다. 이곳이 함선별 상대론
**두-시계 고유시간 누산기**와 **워프 순항 상태**의 자연스러운 집이다.

### A4. `ScenarioModule` (클래스는 H, 속성 인자는 M)
`class X : ScenarioModule`에 `public override void OnSave/OnLoad(ConfigNode)`를 두고
ConfigNode 라운드트립을 하는 형태 — KerbalHealth `KerbalHealthScenario.cs:14,630,661`
(`AddValue` :640, `HasValue` :681).

> **갭 (M):** `[KSPScenario(ScenarioCreationOptions…, GameScenes…)]` 속성 인자와 등록
> 경로(`HighLogic.CurrentGame.scenarios` / `ProtoScenarioModule` / `GamePersistence`)는
> **바이트 단위로 확인하지 않았다**. *글로벌*(함선별이 아닌) 플러그인 상태에는
> ScenarioModule을 쓰되, 출시 전에 속성 인자를 확인한다.

### A5. 함선 `Guid`로 키잉한 커스텀 데이터 (H)
Kerbalism `Database/DB.cs` 관용구: `Dictionary<Guid, VesselData>` (:227); **저장** —
`vesselsNode.AddNode(pv.vesselID.ToString())` (자식 노드 이름 = GUID 문자열,
~:85); **로드** — `vesselsNode.GetNode(pv.vesselID.ToString())` + `dict.Add(pv.vesselID,
vd)` (:56-57). 주의: 로드 시 살아있는 `ProtoVessel.vesselID`에서 GUID를 **재유도**한다
(`new Guid(node.name)`가 아니다).

### A6. `Planetarium.GetUniversalTime() → double` (H; persistence 프레이밍은 L)
`var now = Planetarium.GetUniversalTime()` — Kerbalism `Sim.cs:277`. API(현재 UT
시계) 자체는 H다. **그것을 ConfigNode에 타임스탬프로 쓰는 것**은 확인되지 않았다 — 그
프레이밍은 추론이다(L). 다만 자명하다.

---

## B. Harmony

### B1. 부트스트랩 — `new Harmony(id).PatchAll()` (H)
교과서적 사례(Kerbalism `System/Loader.cs`): `[KSPAddon(Startup.Instantly, false)]`
MonoBehaviour의 `Start()`가 다음을 한다.
```csharp
harmonyInstance = new Harmony("Kerbalism");                  // :75
harmonyInstance.PatchAll(Assembly.GetExecutingAssembly());   // :76
```
대조: KSPCommunityFixes는 `[KSPAddon(Instantly, true)]` 클래스의 static ctor에서
`new Harmony("KSPCommunityFixes")`를 만들고 패치를 개별 적용한다(`PatchAll` 없음) —
`KSPCommunityFixes.cs:10,50,52`.

### B2. 스톡 메서드를 겨냥한 `[HarmonyPatch]` (H)
스톡 `ModuleDataTransmitter`에 대한 split-attribute 형태 — Kerbalism
`Patches/ModuleDataTransmitter_GetInfo.cs:13-15`:
```csharp
[HarmonyPatch(typeof(ModuleDataTransmitter))]
[HarmonyPatch("GetInfo")]
class ModuleDataTransmitter_GetInfo { … }
```
프로그래밍 방식 대안(KSPCF 래퍼): `AddPatch(PatchType.Prefix,
typeof(ModuleReactionWheel), nameof(…))` — `BugFixes/ReactionWheelsPotentialTorque.cs:15`.

> **갭:** `[HarmonyPatch]`의 `new Type[]{…}` 인자 명확화 오버로드는 확인되지 않았다(M,
> 문서 전용).

### B3. Prefix / Postfix / Transpiler 시그니처 (H)
이 레포들에서 패치 종류는 `[HarmonyPostfix]` 속성이 아니라 메서드 **이름**
(`Prefix`/`Postfix`/`Transpiler`)으로 식별된다. 확인된 주입 매직 파라미터.

| 형태 | 인용 |
|---|---|
| `static bool Prefix(ModuleDataTransmitter __instance, ref string __result)` (false 반환 → 원본 스킵; `__result` 기록) | Kerbalism `ModuleDataTransmitter_GetInfo.cs:17,50` |
| `static void Postfix(TooltipController_CrewAC __instance, ProtoCrewMember pcm)` | Kerbalism `TooltipController_CrewAC_SetTooltip.cs:7-13` |
| `static bool Prefix(ModuleReactionWheel __instance, out Vector3 pos, out Vector3 neg)` | KSPCF `ReactionWheelsPotentialTorque.cs:19-20` |
| `static IEnumerable<CodeInstruction> …_Transpiler(IEnumerable<CodeInstruction> instructions)` (`AccessTools.Method/Field/PropertySetter` 사용) | KSPCF `RescaledRoboticParts.cs:23` |

> **갭:** `MethodBase __originalMethod`와 `ILGenerator generator` 주입 파라미터는
> 확인되지 않았다(M, 문서 전용).

### B4. FlightIntegrator 힘 타이밍 — `FashionablyLate` (H, 직접 확인됨)
**이것은 상대론 + 워프 플러그인이 의존하는 핵심 주장이며, Principia에서 직접 확인된다 —
추론이 아니다.**
- FixedUpdate별 콜백 등록.
  `TimingManager.FixedUpdateAdd(TimingManager.TimingStage.FashionablyLate, FashionablyLate)`
  — Principia `ksp_plugin_adapter/ksp_plugin_adapter.cs:866`.
- Principia는 거기서 **누적된** 힘 집계를 읽는다.
  `if (part.force != Vector3d.zero) part_id_to_intrinsic_force_.Add(part.flightID, part.force)`
  (`:1828-1841`; `part.torque`, `part.forces`도), 그리고 `part.forces`/`part.force`/`part.torque`가
  **FlightIntegrator의 FixedUpdate에 의해 클리어된다**는 원문 그대로의 주석(`:1780`)이 붙어 있다.
- 순서(`:1242`): **FashionablyLate 콜백 → FlightIntegrator.FixedUpdate(힘 샘플링 +
  클리어) → Vessel FixedUpdate → 물리 시뮬레이션.**

→ **규칙:** 힘이 적분되게 하려면 `part.force` / `part.AddForce(...)`를 **FashionablyLate
시점 또는 그 이전에** 쓴다. 힘 적용 witness: FAR `FARAeroPartModule.cs:472`가
`part.AddForce(...)` + `part.AddTorque(...)`를 쓴다(그 옆의 `rb.AddForce` 줄들은 주석
처리되어 있다 — 적분기가 샘플링하는 건 `part.AddForce`다). 이것이 정확히
[`relativity-mod.md` §4](../../../gameplay/interstellar-expansion/relativity/relativity-mod.md)와
워프 순항이 의존하는 채널이다.

> **갭:** `part.AddForceAtPosition(...)`은 특정적으로 확인되지 않았다(FAR는 `AddForce`+`AddTorque`를
> 쓴다).

### B5. `GameEvents.<event>.Add(callback)` (H)
- method-ref: `GameEvents.onVesselChange.Add(UnlockControl)` — MechJeb2 `MechJebCore.cs:445`;
  핸들러 `void UnlockControl(Vessel v)` :1204.
- lambda: `GameEvents.onVesselChange.Add(v => OnVesselModified(v))` — Kerbalism
  `Callbacks.cs:98`; 그리고 `onVesselRecovered` :85, `OnTechnologyResearched` :101,
  `onShowUI` :117.

> **갭:** `onVesselSOIChanged.Add`는 주석 처리된 것만 발견됨(L); `onGameStateSave.Add`는
> 받아온 어느 파일에서도 확인되지 않았다.

---

## Gaps summary (do not fabricate)
VesselModule `OnSave` (A3, M) · `[KSPScenario]` 인자 + 등록 (A4, M) ·
UT를 ConfigNode 타임스탬프로 (A6, L) · `[HarmonyPatch(new Type[]{…})]` &
`__originalMethod`/`generator` 파라미터 (B2/B3, M) · `part.AddForceAtPosition` (B4) ·
`onVesselSOIChanged`/`onGameStateSave` (B5, L).

## Provenance
2026-06-30에 확인했다(raw-fetch + read). witness 레포: Kerbalism, KSPCommunityFixes,
MechJeb2, KSP-Recall, ContractConfigurator, Principia, FAR, KerbalHealth. 핵심 퍼머링크
(FashionablyLate): https://github.com/mockingbirdnest/Principia/blob/a440310a9bd48d9e1332bd74abd8f4dcb465ae9b/ksp_plugin_adapter/ksp_plugin_adapter.cs#L866

## Related
- [`README`](README.md) — KB 인덱스 + 근거화 정책
- [`plugin-scaffolding.md`](plugin-scaffolding.md) — OnSave/OnLoad를 호스팅하는 PartModule/VesselModule 생명주기
- [`relativity-mod.md` §4](../../../gameplay/interstellar-expansion/relativity/relativity-mod.md) — 이 문서가 근거화하는 FashionablyLate 힘 훅
- [`warp-patch-draft.md`](../../../../gameplay/interstellar-expansion/warp/warp-patch-draft.md) — 워프 순항도 part-force 채널에 쓴다
