---
name: ksp-harmony-adapters
description: >-
  Battle-tested conventions for writing Harmony 2 (HarmonyLib / HarmonyKSP) runtime patches in a
  KSP 1.12.x C# plugin — the soft-typed, present-guarded, fail-soft "adapter" pattern used to hook
  another mod's or stock KSP's internals when no public API exists. Use this whenever the task
  involves patching KSP or a KSP mod at runtime: adding a prefix/postfix/finalizer/transpiler,
  reaching into another mod (Kerbalism, MechJeb, kOS, Persistent Thrust, KerbalHealth, RP-1,
  Scatterer, Kopernicus, Principia, Blueshift, KSPIE …) without referencing its assembly, choosing
  where to hook a call graph, deciding whether Harmony is even the right tool, wiring 0Harmony into
  a .csproj/CKAN metadata, or debugging a patch that "doesn't fire". Trigger it even when the user
  only says "hook X", "intercept Y", "make mod Z see my modified value", "patch the stock burn
  timer", or "my Harmony patch isn't working" — anything that ends in a runtime patch inside KSP.
  Do NOT trigger for Harmony patching outside KSP, or for ModuleManager .cfg patching (that is not
  Harmony).
---

# KSP Harmony adapters

Harmony is what you reach for in KSP when the thing you need to change has **no public API** —
which is most things. Stock KSP and nearly every mod expose fields and behaviour, not extension
points. So the working assumption of this skill is: you are patching internals that were never
meant to be patched, in a game where a single unhandled exception in a `FixedUpdate` chain can
brick a player's save.

That assumption drives every convention below. The goal is not just "make the patch work" — it is
**a patch that degrades to nothing** when the target mod is absent, when the target mod updates
and renames a member, or when your own code throws.

## Before you patch: is Harmony the right tool?

Work down this list and stop at the first hit. Harmony is the last resort, not the first.

1. **A public API / event exists** — use it. Some mods do have one (Kerbalism's `KERBALISM.API`,
   for instance), though it is usually narrower than you need. Check before assuming.
2. **A stock-assignable delegate exists** — wrap it. KSP has several public static delegate hooks
   (e.g. `Part.CheckPartG`). Capture the existing value, install your own, chain to the captured
   one inside a `try/finally`. Restoration is native, there is no patch-conflict surface, and it
   is far cheaper than a patch bracket. The known cost is last-writer-wins if another mod
   overwrites the delegate blind afterwards — that is the stock pattern's cost, not yours.
3. **A `PartModule` / `VesselModule` can do it** — prefer adding your own module over patching
   someone else's.
4. **Otherwise: Harmony.** Now read the rest of this file.

## The adapter pattern

Every hook is its own small file — one adapter class per integration target — following this
shape. A skeleton you can copy is in `references/adapter-template.cs`.

```csharp
[KSPAddon(KSPAddon.Startup.MainMenu, true)]   // once per game session; patches persist
public class FooAdapter : MonoBehaviour
{
    void Start()
    {
        MyConfig.EnsureLoaded();
        if (!MyConfig.CompatFoo) return;                       // 1. config gate

        Type t = AccessTools.TypeByName("Foo.BarManager");     // 2. soft-type, no asm reference
        if (t == null) { Debug.Log("[MyMod] Foo not detected — adapter idle."); return; }

        MethodInfo m = AccessTools.Method(t, "Tick", new[] { typeof(Vessel), typeof(double) });
        if (m == null)                                          // 3. version guard
        {
            Debug.LogWarning("[MyMod] Foo.BarManager.Tick not found (version mismatch) — adapter idle.");
            return;
        }

        try                                                     // 4. patch-time guard
        {
            new Harmony("mymod.foo").Patch(m,
                prefix: new HarmonyMethod(AccessTools.Method(typeof(FooAdapter), nameof(TickPrefix))));
            Debug.Log("[MyMod] Foo adapter: Tick dt scaled.");
        }
        catch (Exception e)
        {
            Debug.LogWarning("[MyMod] Foo patch failed, adapter idle: " + e.Message);
        }
    }

    static void TickPrefix(Vessel __0, ref double __1)
    {
        try { /* … */ }
        catch { /* never let the adapter break Foo's simulation */ }   // 5. runtime guard
    }
}
```

The five guards are the whole point, and they fail at different times:

| Guard | Fails when | Result |
|---|---|---|
| 1. Config gate | Player turned the integration off | No patch, no log noise |
| 2. Soft-type null check | Target mod not installed | Quiet `Debug.Log`, adapter idle |
| 3. Member null check | Target mod updated and renamed things | `Debug.LogWarning`, adapter idle |
| 4. `try` around `Patch()` | Signature drift, IL problems, duplicate patch | `Debug.LogWarning`, adapter idle |
| 5. `try/catch` in the patch body | Your own logic throws at runtime | Swallowed; host mod keeps running |

Guard 5 is the one people skip and the one that matters most. Your prefix runs inside someone
else's per-frame loop. An exception there does not fail your feature — it fails *their* simulation,
every frame, and the player blames them. Swallowing is correct here even though swallowing is
usually a smell: your feature silently not applying is a vastly better outcome than a broken save.

### Soft-typing is non-negotiable for cross-mod work

Never add an assembly reference to another mod. `AccessTools.TypeByName` + cached `FieldInfo` /
`MethodInfo` resolved once at startup gives you:

- no hard dependency, so your mod loads fine without theirs,
- no load-order fragility,
- a clean place to detect version drift (the null check).

Some mods make this mandatory rather than merely wise — Kerbalism, for instance, is bootstrap-loaded
from a `.kbin`, so there is no assembly to reference even if you wanted to.

Resolve reflection handles **once in `Start()`** and cache them in statics. Doing `AccessTools.Field`
inside a per-frame patch body is a real performance problem in KSP's `FixedUpdate`.

### Patch IDs

Use one Harmony instance ID per feature, namespaced to your mod: `mymod.kerbalism`,
`mymod.mechjeb`, `mymod.feltg`, `mymod.feltg.parts`. Distinct IDs make conflict reports readable
and let you `UnpatchAll(id)` a single feature. A single mod-wide ID makes both impossible.

## Choosing where to hook

This is the part that decides whether your patch is correct, and it is worth more thought than the
patch mechanics.

**Find the choke point.** Trace the call graph and look for one method that every path funnels
through. Patching one choke point beats patching five call sites: fewer patches, no double-counting,
and it keeps working when the target mod adds a sixth path. A good real example: a background-thrust
mod that edits orbits from both an unloaded path and a warping-loaded path, but both go through a
single `Perturb(Orbit, ref Vector3d, double)` — one prefix covers both.

**Patch leaves, not the branch above them.** The mirror-image mistake. If `Profile.Execute` merely
calls `Rule.Execute` and `Process.Execute`, patching all three double-applies your scaling. Verify
the call graph (dnSpy/ILSpy) before choosing; do not infer it from names.

**Patch inside the callee, not at the call site**, when the callee itself inspects what it did.
If a mod diffs a vector across a call to detect completion, scaling the argument upstream desyncs
its bookkeeping from what was actually applied; scaling inside the call keeps them consistent.

**Watch for disjointness.** If you also hook a real-time path, confirm the background path is truly
inactive for loaded vessels before hooking both, or you will apply your effect twice.

## Patch shapes

Full annotated code for each of these is in `references/patch-shapes.md`. Read it when you are
writing the patch body.

- **Prefix + `ref` argument** — rewrite an input (a `dt`, a Δv, a rate) before the original runs.
  The most common and the least invasive. A by-value parameter can be taken by `ref`.
- **Postfix + `ref __result`** — correct an output. Use for getters, computed properties, estimates
  other mods display.
- **Prefix + Finalizer bracket** — temporarily mutate shared state for the duration of one call and
  restore it after. Use a **finalizer**, not a postfix, so the restore also runs when the original
  throws.
- **Postfix that rewrites a collection** — when the method fills a list/array you need to rescale.
- **Reflection sweep + bulk patch** — patch an interface implementation across *all* loaded
  assemblies (e.g. every `PartModule` implementing `ITorqueProvider`), so modded parts are covered
  for free. Dedupe by `MethodHandle.Value`; resolve skip-lists to `Type` and test with
  `IsAssignableFrom` so subclasses inherit the exemption.
- **Prefix returning `false`** — full replacement. Avoid unless there is no alternative: it makes
  your mod incompatible with every other patch on that method.
- **Transpiler** — last resort. Brittle across game and mod updates. Prefer restructuring the hook.

## Argument injection: the rules that bite

Harmony's magic parameter names are matched by name, and the numbering trips people up constantly.

- `__0`, `__1`, … index the **real parameters**. `this` is *not* counted — it arrives separately as
  `__instance`. A useful consequence: an instance method `Foo.Execute(Vessel v, …, double dt)` and a
  static method `Bar.Update(Vessel v, …, double dt)` can share **one** prefix, because in both
  `__0` is the Vessel and `__3` is the dt.
- You may take a by-value parameter as `ref` to rewrite it.
- Named parameters matching the original's parameter names also work and are more readable — but
  they break silently if the target mod renames a parameter, so `__N` is safer for cross-mod
  patches against code you do not control.
- `__result` (with `ref`) is the return value in a postfix.
- `__state` passes data from prefix to postfix/finalizer.
- `__originalMethod` is useful for logging which of several shared targets fired.
- `__exception` in a finalizer; return null to swallow, return it to rethrow.

Resolve overloads explicitly: `AccessTools.Method(t, "X", new[] { typeof(Orbit), typeof(Vector3d) })`.
Properties need `AccessTools.PropertyGetter` / `PropertySetter`, not `Method`.

**Handle multiple member-name generations.** Mods rename things between release and dev lines. Bind
whichever exists rather than picking one:

```csharp
MethodInfo g = AccessTools.PropertyGetter(t, "ThrustAvailable")
            ?? AccessTools.PropertyGetter(t, "thrustAvailable");
```

## Threading

Some mod internals (fuel-flow simulations, background solvers) run on a worker thread. A patch body
there **must not touch `FlightGlobals`, `HighLogic`, or any Unity object** — that is an instant
crash or silent corruption. Capture whatever you need on the main thread each `FixedUpdate` into a
`volatile` field and read that field from the patch.

## Logging discipline

Debug logs are how you prove a patch actually fires, and how you get blamed for a 500 MB `KSP.log`.

- **Throttle by wall time, not call count.** A "log every 200th call" gate looks conservative until
  it multiplies by rules × vessels × ticks and logs continuously. Use
  `if (debug && Time.unscaledTime >= next) { next = Time.unscaledTime + 300f; … }` — one heartbeat
  per path per 5 minutes is plenty to confirm the hook is live.
- Gate all per-frame logging behind a config `debugMode` flag.
- Prefix every line with `[YourMod]` so players can grep.
- Log the *startup* outcome unconditionally (patched / not detected / version mismatch). That one
  line resolves most support reports.
- Use `CultureInfo.InvariantCulture` in formatted numeric logs.

## Wiring 0Harmony into the build

Depend on the shared KSP-packaged copy at `GameData/000_Harmony/0Harmony.dll`. **Never bundle your
own** — multiple 0Harmony copies in one install is a known breakage.

```xml
<!-- KSPBuildTools ModReference -->
<ModReference Include="0Harmony">
  <DLLPath>GameData/000_Harmony/0Harmony.dll</DLLPath>
  <CKANIdentifier>Harmony2</CKANIdentifier>
</ModReference>
```

Emit `[KSPAssemblyDependency("0Harmony", 2, 0)]` so KSP reports a missing-Harmony install clearly
instead of throwing `TypeLoadException` at the player. On CKAN, `depends: Harmony2`.

Be aware of what this costs: referencing 0Harmony makes Harmony a **hard dependency** of the whole
assembly, even for users who do not have the mod you are adapting to. If keeping a
no-dependency install matters, the alternative is a separate adapter assembly loaded only when both
are present — a real build-structure cost. Most modern mods accept the hard dependency (Harmony is
effectively ubiquitous), but make it a conscious decision, not an accident.

Missing 0Harmony does not fail cleanly: it cascades into unrelated stock `NullReferenceException`s
(e.g. `SoftMasking`, `NavBallBurnVector`). If a user reports a pile of unrelated stock NREs, check
Harmony first.

## When a patch doesn't fire

Diagnose in this order — the first two cover most cases and neither is a code bug.

1. **Is the adapter even reaching `Patch()`?** Check your startup log line. Usually it is the config
   gate or a null member.
2. **Inlining.** A short method, especially one marked `[MethodImpl(MethodImplOptions.AggressiveInlining)]`,
   may be inlined at its call sites, and your patch will silently not take there. This is why the
   throttled heartbeat log exists — it distinguishes "patched" from "actually running". Workaround:
   hook a caller instead, or a different, larger method in the same path.
3. **Wrong overload** — you patched a sibling with the same name.
4. **`KSPAddon` scene never ran** — `Startup.MainMenu` with `once: true` is the safe default for
   patches that should live for the session. For per-scene work use `Startup.Flight` plus a static
   `patchAttempted` guard so re-entering the scene does not double-patch.
5. **Load order** — the target mod's assembly may not be loaded at your `KSPAddon` scene. `MainMenu`
   is late enough for essentially everything.
6. **Another mod patched it first** and its prefix returns `false`, skipping the original and every
   later prefix.

`Harmony.GetPatchInfo(method)` will tell you who else is on a method — useful for a conflict report.

## Documenting the patch

Cross-mod patches are unmaintainable without a paper trail, because the target moves. In the file
header, record:

- **what** the choke point is and **why that one** (the call-graph reasoning),
- the **grounding**: repo + commit/version you read the internals at, and file:line if you have it,
- what you deliberately did **not** patch, and why (this is what stops the next maintainer from
  "fixing" your omission and double-applying),
- the failure mode if the target changes.

A future reader — human or agent — cannot re-derive any of this from the patch code alone.

## Reference files

- `references/adapter-template.cs` — copy-paste skeleton with all five guards.
- `references/patch-shapes.md` — annotated code for each patch shape above, including the
  finalizer bracket and the reflection-sweep bulk patch.
- `references/pitfalls.md` — the failure catalogue in more detail: inlining, load order, threading,
  double-application, mod-version drift, mutual-exclusion reasoning.

For finding the KSP/mod API surface itself (where a class lives, what the stock signature is), use
the `ksp-modding-sources` skill — this skill assumes you already know what you want to patch.
