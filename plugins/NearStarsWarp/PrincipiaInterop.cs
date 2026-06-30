// Principia detach/re-seed 접점 — 워프 플래그 올리기·도착 스톡궤도 설정·플래그 내리기. §1 포크 필요
using UnityEngine;

namespace NearStars.Warp
{
    // The ONLY file that cannot work without the §1 Principia fork (the one
    // UnmanageabilityReasons OR-term). It is the seam between the pure cruise core
    // and Principia's authority layer. Spec: warp-patch-draft.md §1, §4.
    //
    // REQUIRES FORK: the patched principia.dll must read the same flag channel
    // IsUnderWarp() raises here. Until the fork lands, Detach() is a no-op and the
    // vessel snaps back every frame (issue #1420) — so this draft is inert without it.
    //
    // On the NON-Principia profile every method is a safe no-op: there is no managed
    // trajectory to detach from, and SigmaBinary + stock conics already let a custom
    // propagator move the vessel. So the cruise core stays profile-agnostic.
    public static class PrincipiaInterop
    {
        // VERIFY: choose the flag channel WITH the fork (warp-patch-draft.md §5.2):
        //   preferred — a conventional value Principia reads by name (KSPField on the
        //   warp part, or a ProtoVessel entry keyed by GUID) so neither assembly
        //   compile-depends on the other. Fallback — a shared static keyed by GUID.
        // This static map is the placeholder for the GUID-keyed channel.
        static readonly System.Collections.Generic.HashSet<System.Guid> warping
            = new System.Collections.Generic.HashSet<System.Guid>();

        public static bool PrincipiaPresent { get; set; } // set at load by an assembly probe

        // ENGAGE side: raise the flag so the patched Principia drops the vessel from
        // its kept-set next tick. No-op (and harmless) without Principia.
        public static void Detach(Vessel vessel)
        {
            if (vessel == null) return;
            warping.Add(vessel.id);
            // VERIFY: if using a KSPField channel, set it here instead of / in addition
            // to the static, so the forked adapter's IsUnderWarp(vessel) sees it.
        }

        // The forked adapter calls into this (or the equivalent KSPField read).
        public static bool IsUnderWarp(Vessel vessel)
            => vessel != null && warping.Contains(vessel.id);

        // DROPOUT side: set the destination stock orbit, then clear the flag. Next tick
        // the vessel is no longer excluded, so Principia's first-insertion seed path
        // (CreateTrajectoryIfNeeded, guarded by trajectory_.empty()) re-adopts it from
        // this stock orbit — no re-seed API needed (warp-patch-draft.md §1.3).
        //
        // VERIFY: the exact stock-orbit set call + that it "sticks" for the one frame
        //   before Principia re-adopts. Under Principia a stock orbit set is normally
        //   overwritten (vessel.cpp ~522) — it works here ONLY because the vessel is
        //   still excluded at the moment we set it, then we clear the flag.
        public static void ReseedAt(Vessel vessel, Orbit destinationStockOrbit, Vector3d arrivalVelBarycentric)
        {
            if (vessel == null || destinationStockOrbit == null) return;

            // VERIFY: KSP orbit set — typically
            //   vessel.orbit.UpdateFromOrbitAtUT(...) or vessel.SetOrbit(destinationStockOrbit).
            //   Confirm the call + units (m, m/s, barycentric) against the live API.
            //   arrivalVelBarycentric carries the frame-(a) inter-stellar relative velocity.

            warping.Remove(vessel.id); // clear AFTER the orbit is set ⇒ Principia re-adopts from it
        }
    }
}
