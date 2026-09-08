# Patch shapes

Annotated code for each shape named in SKILL.md. All of these assume the five-guard adapter
skeleton around them (`adapter-template.cs`) — only the patch bodies and the `Patch()` calls are
shown here.

## Contents

- [Prefix + `ref` argument](#prefix--ref-argument) — rewrite an input
- [Shared prefix across instance and static targets](#shared-prefix-across-instance-and-static-targets)
- [Postfix + `ref __result`](#postfix--ref-__result) — correct an output
- [Postfix that rewrites a collection](#postfix-that-rewrites-a-collection)
- [Prefix + Finalizer bracket](#prefix--finalizer-bracket) — temporary state mutation
- [Reflection sweep + bulk patch](#reflection-sweep--bulk-patch) — every implementer of an interface
- [Prefix returning `false`](#prefix-returning-false) — full replacement
- [Constructor patching](#constructor-patching)
- [Main-thread capture for worker-thread patches](#main-thread-capture-for-worker-thread-patches)
- [Delegate wrap — the non-Harmony alternative](#delegate-wrap--the-non-harmony-alternative)

---

## Prefix + `ref` argument

The workhorse. Rewrite an input before the original runs; the original's own bookkeeping then
stays consistent with what was actually applied.

```csharp
new Harmony("mymod.bgthrust").Patch(perturb,
    prefix: new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(PerturbPrefix))));

// Static extension method Perturb(this Orbit o, Vector3d deltaV, double UT):
// __0 = orbit, __1 = deltaV (by-value → ref), __2 = UT.
static void PerturbPrefix(Orbit __0, ref Vector3d __1, double __2)
{
    try
    {
        if (__0 == null) return;
        double beta = __0.getOrbitalVelocityAtUT(__2).magnitude / MyCore.C;
        __1 *= MyCore.ThrustFactor(beta);
    }
    catch { }
}
```

Why scale *inside* `Perturb` rather than at its call sites: the host mod diffs the burn vector
across this call to decide when a manoeuvre node is complete. Scaling upstream would leave its
completion check measuring a number that was never applied.

## Shared prefix across instance and static targets

Because `this` arrives as `__instance` and is never counted in the `__N` numbering, an instance
method and a static method with the same *real* parameter list can share one prefix. This is the
single most useful consequence of Harmony's numbering.

```csharp
// KERBALISM.Process.Execute(Vessel v, …, double elapsed_s)   — instance
// KERBALISM.Background.Update(Vessel v, …, double elapsed_s) — static
// In BOTH: __0 = Vessel, __3 = elapsed_s.
static void ScaleElapsedPrefix(Vessel __0, ref double __3, MethodBase __originalMethod)
{
    try
    {
        if (__0 == null) return;
        __3 *= MyCore.FactorFor(__0);

        if (MyConfig.DebugMode && Time.unscaledTime >= next)
        {
            next = Time.unscaledTime + 300f;
            Debug.Log("[MyMod] " + __originalMethod.DeclaringType.Name + "."
                + __originalMethod.Name + " elapsed_s scaled on " + __0.vesselName);
        }
    }
    catch { }
}
```

`__originalMethod` earns its place here: with one body serving several targets, it is the only way
to know which one fired.

### Excluding specific instances by an internal field

When the same method serves cases you must treat differently, read the discriminator off
`__instance` with a cached `FieldInfo`:

```csharp
static FieldInfo ruleNameField;      // resolved once in Start()
static HashSet<string> excluded;     // from config, so players can adjust without a rebuild

static void RulePrefix(object __instance, Vessel __0, ref double __3)
{
    try
    {
        string name = ruleNameField.GetValue(__instance) as string;
        if (name != null && excluded.Contains(name)) return;   // this rule stays untouched
        __3 *= MyCore.FactorFor(__0);
    }
    catch { }
}
```

Note `object __instance` — you cannot name a soft-typed type at compile time, and you do not need
to.

## Postfix + `ref __result`

For getters, computed properties, and estimates that other mods display to the player.

```csharp
var post = new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(ThrustGetterPostfix)));
harmony.Patch(AccessTools.PropertyGetter(vesselState, "ThrustAvailable"), postfix: post);
harmony.Patch(AccessTools.PropertyGetter(vesselState, "ThrustMinimum"),   postfix: post);
harmony.Patch(AccessTools.PropertyGetter(vesselState, "ThrustCurrent"),   postfix: post);

static void ThrustGetterPostfix(object __instance, ref double __result)
{
    try
    {
        Vessel v = ResolveVessel(__instance);   // via the cached FieldInfo
        if (v == null) return;
        __result *= MyCore.ThrustFactorFor(v);
    }
    catch { }
}
```

One `HarmonyMethod` instance can be reused across several `Patch()` calls.

## Postfix that rewrites a collection

When the method fills a list you need to rescale, do it after it returns.

```csharp
static void RunPostfix(object __instance)
{
    try
    {
        var segments = segmentsField.GetValue(__instance) as System.Collections.IList;
        if (segments == null) return;
        float k = simMultiplier;                       // captured on the main thread; see below
        if (k == 1f) return;
        for (int i = 0; i < segments.Count; i++)
        {
            object seg = segments[i];
            segThrust.SetValue(seg, (double)segThrust.GetValue(seg) * k);
            if (segMaxThrust != null) segMaxThrust.SetValue(seg, (double)segMaxThrust.GetValue(seg) * k);
        }
    }
    catch { }
}
```

Fields that exist only on some versions (`segMaxThrust` here) are resolved optionally and
null-checked at use — that keeps one adapter working across two release lines.

## Prefix + Finalizer bracket

Temporarily mutate shared state for the duration of one call. Use a **finalizer**, not a postfix:
a postfix does not run when the original throws, and you would leak the mutated state into the rest
of the game.

```csharp
new Harmony("mymod.feltg").Patch(
    AccessTools.Method(typeof(ProtoCrewMember), "ActiveFixedUpdate", new[] { typeof(Part) }),
    prefix:    new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(Prefix))),
    finalizer: new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(Finalizer))));

// __state carries the saved value from prefix to finalizer — do not use a static, the call can
// re-enter or interleave across vessels.
static void Prefix(Part __0, out double __state)
{
    __state = double.NaN;
    try
    {
        Vessel v = __0 != null ? __0.vessel : null;
        if (v == null || v.packed) return;         // stock blanks geeForce on rails — don't fight it
        double saved = v.geeForce;
        if (saved == 0.0) return;                  // stock's own suppression window
        v.geeForce = MyCore.FeltG(v);
        __state = saved;
    }
    catch { }
}

static void Finalizer(Part __0, double __state)
{
    try
    {
        if (double.IsNaN(__state)) return;         // nothing was injected
        if (__0 != null && __0.vessel != null) __0.vessel.geeForce = __state;
    }
    catch { }
}
```

`double.NaN` as the "nothing injected" sentinel keeps the finalizer from writing a bogus value when
the prefix bailed early.

## Reflection sweep + bulk patch

Patch every implementation of an interface across all loaded assemblies, so third-party parts are
covered without naming them.

```csharp
Type itp = typeof(ITorqueProvider);
var harmony = new Harmony("mymod.attitude");
var postfix = new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(TorquePostfix)));

// Resolve skip names to TYPES so a subclass of a skipped module is exempt too — matching by
// exact name would miss a modded subclass of ModuleControlSurface.
var skipTypes = new List<Type>();
foreach (string sn in MyConfig.AttitudeSkipModules)
{
    Type st = AccessTools.TypeByName(sn);
    if (st != null) skipTypes.Add(st);
}

var patched = new HashSet<IntPtr>();   // dedupe inherited/shared method bodies (e.g. RCS/RCSFX)
foreach (Assembly asm in AppDomain.CurrentDomain.GetAssemblies())
{
    Type[] types;
    try { types = asm.GetTypes(); }
    catch (ReflectionTypeLoadException e) { types = e.Types; }   // partial list, MAY CONTAIN NULLS
    catch { continue; }                                          // unreadable assembly — skip it

    foreach (Type t in types)
    {
        if (t == null || t.IsAbstract || t.IsInterface) continue;
        if (!itp.IsAssignableFrom(t) || !typeof(PartModule).IsAssignableFrom(t)) continue;

        bool skipped = false;
        for (int s = 0; s < skipTypes.Count; s++)
            if (skipTypes[s].IsAssignableFrom(t)) { skipped = true; break; }
        if (skipped) continue;

        MethodInfo m = AccessTools.Method(t, "GetPotentialTorque");
        if (m == null || !patched.Add(m.MethodHandle.Value)) continue;   // once per real method body

        try { harmony.Patch(m, postfix: postfix); }
        catch (Exception e) { Debug.LogWarning("[MyMod] skipped " + t.Name + " — " + e.Message); }
    }
}
```

Three things here are load-bearing and easy to get wrong:

- `ReflectionTypeLoadException.Types` contains **nulls** for the types that failed to load. A KSP
  install with a half-broken mod hits this routinely; the null check is not defensive padding.
- Dedupe on `MethodHandle.Value`, not on `Type`. Subclasses that do not override the method report
  the same inherited `MethodInfo`, and Harmony will throw on the second patch.
- Wrap each individual `Patch()` so one hostile type does not abort the sweep.

## Prefix returning `false`

Skips the original *and every prefix registered after yours*. That makes your mod silently
incompatible with anyone else patching that method, so treat it as a last resort and say so in the
header comment.

```csharp
static bool ReplacePrefix(ref double __result)
{
    __result = MyCore.Compute();
    return false;   // original does not run
}
```

If you only need to *suppress* behaviour conditionally, prefer returning `false` on a narrow
condition and `true` otherwise, so the common path stays shared.

## Constructor patching

Constructors are patched like any other method; get them with `AccessTools.Constructor`.

```csharp
ConstructorInfo ctor = AccessTools.Constructor(t, new[] { typeof(Vessel), typeof(bool) });
harmony.Patch(ctor, prefix: new HarmonyMethod(AccessTools.Method(typeof(Adapter), nameof(CtorPrefix))));

static void CtorPrefix(Vessel __0, ref bool __1)   // __1 = an env flag we want to force on
{
    try { if (MyCore.IsUnderSustainedAccel(__0)) __1 = true; }
    catch { }
}
```

`__instance` in a constructor prefix is a partially-initialised object — do not read its fields.

## Main-thread capture for worker-thread patches

Some mods run simulations on a background thread. Touching `FlightGlobals` / `HighLogic` / any
Unity object from there crashes or corrupts. Capture on the main thread, read the captured value in
the patch.

```csharp
static volatile float simMultiplier = 1f;   // written on main thread, read on worker thread

void FixedUpdate()                           // main thread, our own MonoBehaviour
{
    Vessel v = FlightGlobals.ActiveVessel;
    simMultiplier = v != null ? (float)MyCore.ThrustFactorFor(v) : 1f;
}
```

Establish which thread a target runs on *before* writing the body — a Unity call there fails in a
way that looks like an unrelated crash.

## Delegate wrap — the non-Harmony alternative

When the target is a public static assignable delegate (KSP has several, e.g. `Part.CheckPartG`),
wrap it instead of patching. `try/finally` restoration is native and there is no patch-conflict
surface.

```csharp
static Action<Part> stockCheckPartG;

void Start()
{
    if (Part.CheckPartG == null) { Debug.LogWarning("[MyMod] CheckPartG null — idle."); return; }
    stockCheckPartG = Part.CheckPartG;
    Part.CheckPartG = WrappedCheckPartG;
}

static void WrappedCheckPartG(Part p)
{
    double saved = double.NaN;
    try { saved = Inflate(p.vessel); } catch { }
    try { stockCheckPartG(p); }
    finally { try { if (!double.IsNaN(saved)) p.vessel.geeForce = saved; } catch { } }
}
```

The cost: last-writer-wins if another mod assigns the delegate blind after you. That is the stock
pattern's known cost, and it is usually cheaper than the Harmony alternative.
