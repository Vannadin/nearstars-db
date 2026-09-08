// <한 줄 역할 설명 — 예: Foo 모드의 틱 dt를 우리 계수로 스케일하는 Harmony 어댑터>
//
// HEADER DOC — fill this in, it is not optional for cross-mod patches:
//   Target      : Foo.BarManager.Tick(Vessel, double)  — the single choke point every Foo
//                 resource path funnels through (verified in IL, Foo 1.4.2 @ <commit>).
//   Why here    : Tick is called from both the loaded and unloaded paths; patching its two
//                 callers instead would double-apply.
//   NOT patched : Foo.Baz.Recalc — it only calls Tick, so scaling it too would double-scale.
//   Drift       : if Foo renames Tick, the member guard logs a warning and the adapter goes
//                 idle; Foo keeps working, our feature silently does nothing.
using System;
using System.Reflection;
using HarmonyLib;
using UnityEngine;

namespace MyMod
{
    [KSPAddon(KSPAddon.Startup.MainMenu, true)]   // once per game session; the patch persists
    public class FooAdapter : MonoBehaviour
    {
        static FieldInfo someCachedField;   // resolve reflection ONCE here, never per-frame

        void Start()
        {
            // (1) Config gate — players can turn an integration off without touching files.
            MyConfig.EnsureLoaded();
            if (!MyConfig.CompatFoo) return;

            // (2) Soft-type. No assembly reference to Foo anywhere in the project.
            Type barManager = AccessTools.TypeByName("Foo.BarManager");
            if (barManager == null)
            {
                Debug.Log("[MyMod] Foo not detected — adapter idle.");
                return;
            }

            // (3) Version guard. Resolve the overload explicitly; properties need PropertyGetter.
            //     Bind alternate spellings when a mod has diverging release/dev naming.
            MethodInfo tick = AccessTools.Method(barManager, "Tick",
                new[] { typeof(Vessel), typeof(double) });
            someCachedField = AccessTools.Field(barManager, "state")
                           ?? AccessTools.Field(barManager, "_state");
            if (tick == null || someCachedField == null)
            {
                Debug.LogWarning("[MyMod] Foo.BarManager.Tick/state not found (version mismatch) — adapter idle.");
                return;
            }

            // (4) Patch-time guard. One Harmony id per feature: mymod.foo, mymod.foo.parts, …
            try
            {
                new Harmony("mymod.foo").Patch(tick,
                    prefix: new HarmonyMethod(AccessTools.Method(typeof(FooAdapter), nameof(TickPrefix))));
                Debug.Log("[MyMod] Foo adapter: BarManager.Tick dt scaled.");
            }
            catch (Exception e)
            {
                Debug.LogWarning("[MyMod] Foo patch failed, adapter idle: " + e.Message);
            }
        }

        static float nextDbgLog;   // wall-time throttle, NOT a call counter

        // __0 = Vessel, __1 = dt (by-value → ref so we can rewrite it). `this` is __instance and
        // is never counted in the __N numbering.
        static void TickPrefix(Vessel __0, ref double __1)
        {
            // (5) Runtime guard. This body runs inside Foo's per-frame loop: an exception here
            //     breaks Foo's simulation every frame, not just our feature. Swallow.
            try
            {
                if (__0 == null) return;

                double factor = MyCore.FactorFor(__0);
                if (factor == 1.0) return;
                __1 *= factor;

                if (MyConfig.DebugMode && Time.unscaledTime >= nextDbgLog)
                {
                    nextDbgLog = Time.unscaledTime + 300f;   // one heartbeat / 5 min proves it fires
                    Debug.Log(string.Format(System.Globalization.CultureInfo.InvariantCulture,
                        "[MyMod] Foo dilation: dt ×{0:F3} on {1}", factor, __0.vesselName));
                }
            }
            catch { /* never let the adapter break Foo's simulation */ }
        }
    }
}
