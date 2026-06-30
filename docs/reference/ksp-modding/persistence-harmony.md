---
title: KSP persistence & Harmony (pillar ⑤)
status: draft
created: 2026-06-30
---

# Persistence & Harmony

Saving plugin state to the game's save, and patching stock behaviour with Harmony.
Grounding policy + legend: [`README`](README.md). All rows **H** unless marked.

---

## A. Persistence

### A1. `ConfigNode` API (H)

| Method | witnessed | citation |
|---|---|---|
| `AddValue(name, val)` | `node.AddValue("subtype", subType)` | ContractConfigurator `ConfiguredContract.cs:517` |
| `GetValue(name) → string` | `node.GetValue("subtype")` | `ConfiguredContract.cs:425` |
| `TryGetValue(name, ref var) → bool` | `node.TryGetValue(nameof(x), ref x)` | KSPCommunityFixes `QoL/AltimeterHorizontalPosition.cs:57` |
| `AddNode(name) → ConfigNode` | `local.AddNode(name)` | MechJeb2 `MechJebCore.cs:638` |
| `GetNode(name)` / `HasNode(name)` | `local.HasNode(name) ? local.GetNode(name) : null` | MechJeb2 `MechJebCore.cs:612` |
| `HasValue(name)` | `cfg.HasValue(key)` | Kerbalism `Lib.cs:~3130` |

### A2. `PartModule` save/load (H)

`class X : PartModule` → `public override void OnSave(ConfigNode node)` /
`OnLoad(ConfigNode node)` (full impl: MechJeb2 `MechJebCore.cs:612/551`; minimal with
`base.OnSave/OnLoad`: KSP-Recall `Driftless/PartModule.cs:57/63`). Auto-persisted
fields: `[KSPField(isPersistant = true)] public bool running;` — MechJeb2
`MechJebCore.cs:45`; KSP-Recall `PartModule.cs:28`.

### A3. `VesselModule` save/load (mixed)
Lifecycle + `OnLoad` are grounded in [`plugin-scaffolding.md` §3](plugin-scaffolding.md)
(kOS `kOSVesselModule.cs`). **`OnSave(ConfigNode)` override not witnessed (M)** — the
stock base exposes it symmetrically; confirm before relying. This is the natural home
for the relativity **two-clock proper-time accumulator** and **warp cruise state**
per vessel.

### A4. `ScenarioModule` (H for the class; attribute args M)
`class X : ScenarioModule` with `public override void OnSave/OnLoad(ConfigNode)` doing a
ConfigNode round-trip — KerbalHealth `KerbalHealthScenario.cs:14,630,661` (`AddValue`
:640, `HasValue` :681).

> **Gap (M):** the `[KSPScenario(ScenarioCreationOptions…, GameScenes…)]` attribute args
> and the registration path (`HighLogic.CurrentGame.scenarios` / `ProtoScenarioModule` /
> `GamePersistence`) were **not byte-verified**. Use a ScenarioModule for *global*
> (not per-vessel) plugin state; confirm the attribute args before shipping.

### A5. Custom data keyed by vessel `Guid` (H)
Kerbalism `Database/DB.cs` idiom: `Dictionary<Guid, VesselData>` (:227); **save** —
`vesselsNode.AddNode(pv.vesselID.ToString())` (child-node name = the GUID string,
~:85); **load** — `vesselsNode.GetNode(pv.vesselID.ToString())` + `dict.Add(pv.vesselID,
vd)` (:56-57). Note: it **re-derives** the GUID from the live `ProtoVessel.vesselID` on
load (not `new Guid(node.name)`).

### A6. `Planetarium.GetUniversalTime() → double` (H; persistence framing L)
`var now = Planetarium.GetUniversalTime()` — Kerbalism `Sim.cs:277`. The API (current UT
clock) is H; **writing it into a ConfigNode as a timestamp** was not witnessed — that
framing is inferred (L), though trivial.

---

## B. Harmony

### B1. Bootstrap — `new Harmony(id).PatchAll()` (H)
Textbook (Kerbalism `System/Loader.cs`): a `[KSPAddon(Startup.Instantly, false)]`
MonoBehaviour whose `Start()` does
```csharp
harmonyInstance = new Harmony("Kerbalism");                  // :75
harmonyInstance.PatchAll(Assembly.GetExecutingAssembly());   // :76
```
Contrast: KSPCommunityFixes makes `new Harmony("KSPCommunityFixes")` in a static ctor of
a `[KSPAddon(Instantly, true)]` class and applies patches individually (no `PatchAll`) —
`KSPCommunityFixes.cs:10,50,52`.

### B2. `[HarmonyPatch]` targeting a stock method (H)
Split-attribute form on stock `ModuleDataTransmitter` — Kerbalism
`Patches/ModuleDataTransmitter_GetInfo.cs:13-15`:
```csharp
[HarmonyPatch(typeof(ModuleDataTransmitter))]
[HarmonyPatch("GetInfo")]
class ModuleDataTransmitter_GetInfo { … }
```
Programmatic alternative (KSPCF wrapper): `AddPatch(PatchType.Prefix,
typeof(ModuleReactionWheel), nameof(…))` — `BugFixes/ReactionWheelsPotentialTorque.cs:15`.

> **Gap:** the `new Type[]{…}` argument-disambiguation overload of `[HarmonyPatch]` was
> not witnessed (M, doc-only).

### B3. Prefix / Postfix / Transpiler signatures (H)
Patch kind is identified by method **name** (`Prefix`/`Postfix`/`Transpiler`) in these
repos (not `[HarmonyPostfix]` attributes). Injected magic params witnessed:

| Form | citation |
|---|---|
| `static bool Prefix(ModuleDataTransmitter __instance, ref string __result)` (return false → skip original; write `__result`) | Kerbalism `ModuleDataTransmitter_GetInfo.cs:17,50` |
| `static void Postfix(TooltipController_CrewAC __instance, ProtoCrewMember pcm)` | Kerbalism `TooltipController_CrewAC_SetTooltip.cs:7-13` |
| `static bool Prefix(ModuleReactionWheel __instance, out Vector3 pos, out Vector3 neg)` | KSPCF `ReactionWheelsPotentialTorque.cs:19-20` |
| `static IEnumerable<CodeInstruction> …_Transpiler(IEnumerable<CodeInstruction> instructions)` (uses `AccessTools.Method/Field/PropertySetter`) | KSPCF `RescaledRoboticParts.cs:23` |

> **Gap:** `MethodBase __originalMethod` and `ILGenerator generator` injected params not
> witnessed (M, doc-only).

### B4. FlightIntegrator force timing — `FashionablyLate` (H, directly witnessed)
**This is the load-bearing claim the relativity + warp plugins depend on, and it is
directly witnessed in Principia — not inferred.**
- Register a per-FixedUpdate callback:
  `TimingManager.FixedUpdateAdd(TimingManager.TimingStage.FashionablyLate, FashionablyLate)`
  — Principia `ksp_plugin_adapter/ksp_plugin_adapter.cs:866`.
- Principia reads the **accumulated** force census there:
  `if (part.force != Vector3d.zero) part_id_to_intrinsic_force_.Add(part.flightID, part.force)`
  (`:1828-1841`; also `part.torque`, `part.forces`), with the verbatim comment (`:1780`)
  that `part.forces`/`part.force`/`part.torque` **are cleared by the FlightIntegrator's
  FixedUpdate**.
- Ordering (`:1242`): **FashionablyLate callbacks → FlightIntegrator.FixedUpdate (samples
  + clears forces) → Vessel FixedUpdate → physics sim.**

→ **Rule:** to have a force integrated, write `part.force` / `part.AddForce(...)` **at or
before FashionablyLate**. Force-application witnesses: FAR `FARAeroPartModule.cs:472`
uses `part.AddForce(...)` + `part.AddTorque(...)` (the `rb.AddForce` lines sit
commented-out beside them — `part.AddForce` is the one the integrator samples). This is
exactly the channel [`relativity-mod.md` §4](../../../gameplay/interstellar-expansion/relativity/relativity-mod.md)
and the warp cruise rely on.

> **Gap:** `part.AddForceAtPosition(...)` specifically not witnessed (FAR uses
> `AddForce`+`AddTorque`).

### B5. `GameEvents.<event>.Add(callback)` (H)
- method-ref: `GameEvents.onVesselChange.Add(UnlockControl)` — MechJeb2 `MechJebCore.cs:445`;
  handler `void UnlockControl(Vessel v)` :1204.
- lambda: `GameEvents.onVesselChange.Add(v => OnVesselModified(v))` — Kerbalism
  `Callbacks.cs:98`; also `onVesselRecovered` :85, `OnTechnologyResearched` :101,
  `onShowUI` :117.

> **Gaps:** `onVesselSOIChanged.Add` found only commented-out (L); `onGameStateSave.Add`
> not witnessed in any fetched file.

---

## Gaps summary (do not fabricate)
VesselModule `OnSave` (A3, M) · `[KSPScenario]` args + registration (A4, M) ·
UT-into-ConfigNode timestamp (A6, L) · `[HarmonyPatch(new Type[]{…})]` &
`__originalMethod`/`generator` params (B2/B3, M) · `part.AddForceAtPosition` (B4) ·
`onVesselSOIChanged`/`onGameStateSave` (B5, L).

## Provenance
Verified 2026-06-30 (raw-fetch + read). Witness repos: Kerbalism, KSPCommunityFixes,
MechJeb2, KSP-Recall, ContractConfigurator, Principia, FAR, KerbalHealth. Key permalink
(FashionablyLate): https://github.com/mockingbirdnest/Principia/blob/a440310a9bd48d9e1332bd74abd8f4dcb465ae9b/ksp_plugin_adapter/ksp_plugin_adapter.cs#L866

## Related
- [`README`](README.md) — KB index + grounding policy
- [`plugin-scaffolding.md`](plugin-scaffolding.md) — PartModule/VesselModule lifecycle that hosts OnSave/OnLoad
- [`relativity-mod.md` §4](../../../gameplay/interstellar-expansion/relativity/relativity-mod.md) — the FashionablyLate force hook this grounds
- [`warp-patch-draft.md`](../../../gameplay/interstellar-expansion/warp/warp-patch-draft.md) — warp cruise also writes the part-force channel
