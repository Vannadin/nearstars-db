// 상대론 레이어(§2.6 ii)의 WarpFlag.Provider를 채워 워프 중 우주선을 β/γ 면제시키는 브리지
using UnityEngine;

namespace NearStars.Warp
{
    // Fills Relativity.WarpFlag.Provider so the relativity layer treats a warping vessel
    // as identity (warp β is not physical β — else it reads FTL → NaN and would wrongly
    // crush warp "thrust"/slow resource burn). Spec: warp-patch-draft.md §3,
    // relativity-mod.md §2.6(ii).
    //
    // NOTE (2026-07-01): the relativity layer is now the SEPARATE, external mod
    //   `ksp-relativity` (namespace `Relativity`, its own assembly) — no longer bundled
    //   here. This bridge is a cross-mod integration point: add a (soft/optional) assembly
    //   reference to that mod's public `Relativity.WarpFlag`, and if the mod is absent this
    //   whole component is simply not needed (no-op). Keep `WarpFlag` a generic hook there.
    // VERIFY: the FindPartModuleImplementing API name below.
    [KSPAddon(KSPAddon.Startup.Flight, false)]
    public class WarpFlagBridge : MonoBehaviour
    {
        void Start()
        {
            Relativity.WarpFlag.Provider = IsVesselWarping;
        }

        // A vessel is "under warp" iff its WarpDriveModule cruise state is non-Idle.
        static bool IsVesselWarping(Vessel vessel)
        {
            if (vessel == null) return false;
            var mod = vessel.FindPartModuleImplementing<WarpDriveModule>(); // VERIFY: API name
            return mod != null && WarpCruise.IsUnderWarp(mod.CruiseState);
        }
    }
}
