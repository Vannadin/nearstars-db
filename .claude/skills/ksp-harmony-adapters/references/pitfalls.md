# Pitfalls

The failure catalogue. Most of these cost a debugging session the first time and are invisible in
code review, so it is worth skimming this before writing a cross-mod patch rather than after.

## Contents

- [The patch silently does not fire](#the-patch-silently-does-not-fire)
- [Double application](#double-application)
- [Mod version drift](#mod-version-drift)
- [Load order and scenes](#load-order-and-scenes)
- [Threading](#threading)
- [Exceptions in patch bodies](#exceptions-in-patch-bodies)
- [Performance](#performance)
- [Log flooding](#log-flooding)
- [Multiple 0Harmony copies](#multiple-0harmony-copies)
- [Reflection sweeps over a real install](#reflection-sweeps-over-a-real-install)
- [Mutual exclusion as a correctness argument](#mutual-exclusion-as-a-correctness-argument)
- [Save-game and difficulty interaction](#save-game-and-difficulty-interaction)
- [Patching Principia-adjacent code](#patching-principia-adjacent-code)

---

## The patch silently does not fire

Harmony reports success and nothing happens. In rough order of likelihood:

**Inlining.** The JIT inlines short methods at their call sites, and an inlined call site does not
go through your patch. `[MethodImpl(MethodImplOptions.AggressiveInlining)]` on the target makes this
near-certain, but the JIT will inline plenty of unmarked small methods too. There is no fix at the
patch level — hook a caller, or a larger method on the same path. This is the single best reason to
keep a throttled "the patch is running" heartbeat log: it distinguishes *patched* from *executing*,
and those are different states.

**Wrong overload.** You resolved a same-named sibling. Always pass the explicit parameter type array
to `AccessTools.Method`.

**Property vs method.** `AccessTools.Method(t, "Foo")` returns null for a property `Foo`; you need
`AccessTools.PropertyGetter`.

**Another mod's prefix returns `false`.** It skips the original *and every prefix ordered after it*.
`Harmony.GetPatchInfo(method)` lists every patch owner on a method — put that behind a debug key or
a diagnostic command; it turns "conflicts with X" reports into one log line.

**The adapter never reached `Patch()`.** Check your own startup log line first. It is usually the
config gate or a null member, not Harmony.

## Double application

The most common *correctness* bug, and it produces plausible-looking wrong numbers rather than a
crash — so it survives testing.

- **Patching a branch and its leaves.** If `Profile.Execute` merely calls `Rule.Execute` and
  `Process.Execute`, patching all three scales twice. Verify the call graph in IL; do not infer it
  from names.
- **Patching a background path and a real-time path that overlap.** Before hooking both, confirm
  they are genuinely disjoint — e.g. that the background thrust path zeroes itself for
  physics-loaded vessels. If they overlap for even one vessel state, you double-apply there.
- **Two of your own adapters targeting mods that both wrap the same stock call.**

The defence is documentation: record in the header what you deliberately did *not* patch and why.
Without it, a future maintainer sees an obvious gap and "fixes" it.

## Mod version drift

Your patch targets internals with no compatibility contract. Assume they move.

- **Naming generations.** A mod's dev line and release line frequently differ (PascalCase vs
  camelCase properties, `_core` vs `vesselRef`). Bind whichever exists with `??` rather than picking
  one and calling the other version unsupported.
- **Optional members.** Fields added in a newer version: resolve optionally, null-check at use, and
  let the adapter run degraded on older versions.
- **Volatile internals.** If a mod has announced a rewrite, say so in the header and expect the
  adapter to need a rewrite too. Version-pin in CKAN metadata if the failure would be silent and
  harmful rather than merely inert.
- **Bootstrap-loaded mods** (loaded from a `.kbin` or similar rather than a plain DLL) can only ever
  be reached by string-based reflection — there is no assembly to reference.

Every one of these is why the member null check must log a *distinguishable* warning ("not found —
version mismatch") rather than sharing the "mod not installed" path. The two need different support
answers.

## Load order and scenes

- `[KSPAddon(KSPAddon.Startup.MainMenu, true)]` is the safe default for session-lifetime patches:
  late enough that every mod assembly is loaded, and `once: true` means it runs one time.
- For per-scene adapters (`Startup.Flight, false`), add a `static bool patchAttempted` guard.
  Harmony throws on a duplicate patch, and re-entering the scene will otherwise attempt one every
  time.
- `Startup.Instantly` / `SpaceCentre` may run before the target mod's assembly is available.
- Patches are global and persist for the process. There is no "unpatch on scene exit" unless you
  write it, and you usually should not.

## Threading

Worker threads exist inside mods more often than people expect — fuel-flow simulations, background
resource solvers, pathfinders. From a patch body running on one:

- **Never** touch `FlightGlobals`, `HighLogic`, `PartLoader`, or any `UnityEngine.Object`. Unity's
  API is main-thread only; violations crash or corrupt rather than throwing something readable.
- Capture what you need on the main thread each `FixedUpdate` into a `volatile` field and read that.
- `Debug.Log` from a worker thread is also risky — buffer it or skip it.

Determine the thread before writing the body. The symptom of getting this wrong looks like an
unrelated crash elsewhere.

## Exceptions in patch bodies

Your prefix runs inside another mod's per-frame loop. An unhandled exception there:

- fires every frame, flooding `KSP.log` (hundreds of MB in a long session),
- aborts *their* method mid-way, corrupting their state,
- gets blamed on them, not you.

So wrap every patch body in `try/catch` and swallow. Swallowing is normally a smell; here it is the
correct trade — your feature silently not applying is enormously better than a broken save. If you
want visibility, log once behind a throttle, not on every catch.

Use a **finalizer** rather than a postfix whenever you must undo something, so the undo also runs on
the original's exception path.

## Performance

`FixedUpdate`-path patches run 50×/second × every vessel × every module.

- Resolve all reflection handles once in `Start()`; cache in statics. `AccessTools.Field` inside a
  patch body is a measurable frame-time cost.
- `FieldInfo.GetValue`/`SetValue` box and are slow — acceptable a few times per frame, not
  thousands. For hot paths build a delegate once (`AccessTools.FieldRefAccess` /
  `MethodInvoker.GetHandler`).
- Bail out early and cheaply: null checks and an "is this feature even active for this vessel"
  check before any real work.
- Do not allocate per call (no LINQ, no new lists) in a hot patch — KSP's GC pressure shows up as
  stutter.

## Log flooding

A "log every 200th call" gate sounds conservative and is not: multiply by rules × vessels × ticks
and it logs continuously through normal play. Throttle by **wall time**:

```csharp
static float nextDbgLog;
if (MyConfig.DebugMode && Time.unscaledTime >= nextDbgLog)
{
    nextDbgLog = Time.unscaledTime + 300f;
    Debug.Log(...);
}
```

One heartbeat per path per five minutes is enough to prove the hook is live. Keep a separate
throttle variable per patch path, or the noisy path starves the quiet one. Gate everything behind a
config `debugMode`, and always use `CultureInfo.InvariantCulture` for formatted numbers — a comma
decimal separator makes logs unparseable for players in much of the world.

## Multiple 0Harmony copies

Never bundle your own `0Harmony.dll`. Depend on the shared `GameData/000_Harmony/0Harmony.dll`
(CKAN: `Harmony2`). Two copies in one install produce type-identity failures that surface as
nonsense errors far from the cause.

A *missing* 0Harmony does not fail cleanly either: KSP cascades into unrelated stock NREs
(`SoftMasking`, `NavBallBurnVector`, …). A support report showing a pile of unrelated stock
exceptions is a Harmony-install report until proven otherwise. `[KSPAssemblyDependency("0Harmony", 2, 0)]`
makes KSP say so up front.

## Reflection sweeps over a real install

Iterating `AppDomain.CurrentDomain.GetAssemblies()` on a modded install is hostile territory:

- `asm.GetTypes()` throws `ReflectionTypeLoadException` for any assembly with an unresolvable
  dependency — routine in a heavily modded install. Catch it and use `e.Types`, which is a partial
  list **containing nulls**. Null-check every element.
- Catch and `continue` on any other exception; one broken mod must not abort your sweep.
- Skip abstract types and interfaces.
- Dedupe on `MethodInfo.MethodHandle.Value`. Subclasses that do not override report the same
  inherited method body, and the second `Patch()` on it throws.
- Wrap each individual `Patch()` call so one hostile type is a warning, not a dead adapter.
- Resolve config skip-lists to `Type` and test with `IsAssignableFrom`, so a modded subclass of a
  skipped type inherits the exemption. Name-string matching silently misses those.

## Mutual exclusion as a correctness argument

Two mods that CKAN declares as conflicting can never both be installed, so their two adapters can
never both be live. That is a legitimate argument that a shared code path is not double-hooked —
but write it down in the header, because it is invisible in the code and a future reader will
"discover" the apparent bug.

## Save-game and difficulty interaction

- A `cfg` file is install-wide; a `GameParameters.CustomParameterNode` is per-save. If you offer
  both, define which wins (the usual answer: the cfg is the master switch that decides whether the
  patch is installed at all, the per-save setting gates behaviour inside it).
- Read `HighLogic.CurrentGame` defensively — it is null in the main menu, which is exactly where
  your `KSPAddon` runs.
- If you inflate a stock value that stock also uses for damage, check the game's own suppression
  windows first (packed/on-rails vessels, `IgnoreGForces`, an exact `0.0` sentinel). Resurrecting a
  value inside a window stock deliberately blanked can destroy the player's craft.

## Patching Principia-adjacent code

Principia replaces KSP's integrator and rewrites orbits. Patches that edit `Orbit` state directly
are typically overwritten or actively harmful under Principia. Detect it
(`AccessTools.TypeByName("principia.ksp_plugin_adapter.PrincipiaPluginAdapter") != null`) and
either skip the orbit-editing adapter or take a different route. Say which in the header.
