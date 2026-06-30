// 상대론 레이어(§2.6 ii)의 WarpFlag.Provider를 채워 워프 중 우주선을 β/γ 면제시키는 브리지
using UnityEngine;

namespace NearStars.Warp
{
    // Fills NearStars.Relativity.WarpFlag.Provider so the relativity layer treats a
    // warping vessel as identity (warp β is not physical β — else it reads FTL → NaN
    // and would wrongly crush warp "thrust"/slow resource burn). One shared flag, both
    // plugins Schultz's lane. Spec: warp-patch-draft.md §3, relativity-mod.md §2.6(ii).
    //
    // VERIFY: both plugins must load into the same managed domain so this can reference
    //   NearStars.Relativity.WarpFlag. If they ship as separate assemblies, add an
    //   assembly reference (relativity is the dependency-free one). If the relativity
    //   plugin is absent, this whole component is simply not needed (no-op).
    [KSPAddon(KSPAddon.Startup.Flight, false)]
    public class WarpFlagBridge : MonoBehaviour
    {
        void Start()
        {
            NearStars.Relativity.WarpFlag.Provider = IsVesselWarping;
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
