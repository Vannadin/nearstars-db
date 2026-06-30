// 워프 드라이브 PartModule — engage/disengage, ExoticMatter 검사·소모, 크루즈 상태머신 구동
using UnityEngine;

namespace NearStars.Warp
{
    // The KSP-facing driver. Owns one WarpCruise.State, gates engage on ExoticMatter
    // (gameplay energy model, prototypes/warp_exotic_matter.py), and on each
    // FixedUpdate detaches via PrincipiaInterop + applies the cruise step to the
    // detached vessel. Spec: warp-patch-draft.md §2, §4.
    //
    // VERIFY: PartModule lifecycle + the part-move call (this draft asserts the API
    //   shapes; Schultz confirms against the live KSP assemblies).
    public class WarpDriveModule : PartModule
    {
        // --- tunables (move to .cfg via GameDatabase before ship) ---
        [KSPField] public double warpBeta       = 10.0;  // cruise speed, multiples of c (β_s)
        [KSPField] public double exoticPerTonne = 0.5;   // ExoticMatter units to hold the bubble (standing load)
        [KSPField] public double mjPerTonneLy   = 2.0;   // drive energy MJ per (tonne · ly) — drained over cruise

        readonly WarpCruise.State state = new WarpCruise.State();
        public WarpCruise.State CruiseState => state; // WarpFlagBridge reads this

        Orbit destinationOrbit;       // set by the planner before engage (lead-intercept result)
        Vector3d arrivalVelBary;      // frame-(a) arrival relative velocity (from the planner)

        [KSPEvent(guiActive = true, guiName = "Engage warp")]
        public void EngageWarp()
        {
            if (state.Phase != WarpCruise.Phase.Idle) return;
            if (destinationOrbit == null) { ScreenMsg("No warp target plotted."); return; }

            double shipT = vessel.totalMass; // VERIFY: tonnes
            if (!ConsumeExotic(shipT * exoticPerTonne)) { ScreenMsg("Not enough ExoticMatter."); return; }

            // VERIFY: barycentric v0 — reuse the relativity layer's BarycentricSpeed
            //   derivation (SOI==Sun fast path) but as a vector. On the Principia
            //   profile, source it from Principia (read-only).
            Vector3d v0 = vessel.obt_velocity;            // VERIFY units/frame (m/s, barycentric)
            Vector3d heading = HeadingToTarget();

            WarpCruise.Engage(state, warpBeta, v0, heading);
            PrincipiaInterop.Detach(vessel);              // raise the §1 fork flag (no-op without fork)
        }

        [KSPEvent(guiActive = true, guiName = "Disengage warp")]
        public void DisengageWarp() => WarpCruise.BeginDropout(state);

        public void FixedUpdate()
        {
            if (state.Phase == WarpCruise.Phase.Idle) return;

            double dt = TimeWarp.fixedDeltaTime;          // VERIFY: physics dt while detached
            // Drain drive energy in coordinate time (NOT proper-time scaled — it powers
            // the bubble, like engine propellant in the relativity layer §2.2).
            DrainDriveEnergy(dt);

            Vector3d delta = WarpCruise.StepDelta(state, dt);

            // VERIFY: move the detached vessel by `delta`. While the §1 flag is up,
            //   Principia is NOT overwriting the transform, so a direct set sticks.
            //   Likely vessel.SetPosition(vessel.GetWorldPos3D() + delta) or the
            //   floating-origin-safe equivalent. Confirm against live API + Krakensafe.
            vessel.SetPosition(vessel.GetWorldPos3D() + delta);

            if (state.Phase == WarpCruise.Phase.Idle)     // dropout ramp just finished
                PrincipiaInterop.ReseedAt(vessel, destinationOrbit, arrivalVelBary);
        }

        // --- gameplay energy model (prototype) ---
        bool ConsumeExotic(double units)
        {
            // VERIFY: part.RequestResource("ExoticMatter", units) >= units (KSPIE resource).
            return part.RequestResource("ExoticMatter", units) >= units - 1e-6;
        }

        void DrainDriveEnergy(double dt)
        {
            // MJ ∝ shipMass · cruise-distance-rate. Per second ≈ mass · (β_s·c in ly/s) · mjPerTonneLy.
            const double LY_M = 9.4607e15;
            double lyPerSec = warpBeta * WarpCruise.C / LY_M;
            double mj = vessel.totalMass * lyPerSec * mjPerTonneLy * dt;
            // VERIFY: part.RequestResource("Megajoules", mj); abort/dropout if starved.
            part.RequestResource("Megajoules", mj);
        }

        Vector3d HeadingToTarget()
        {
            // VERIFY: heading toward the lead-intercept point (planner output), in the
            //   barycentric frame. Placeholder uses the target orbit's current position.
            if (destinationOrbit == null) return Vector3d.forward;
            Vector3d to = destinationOrbit.pos - vessel.orbit.pos;
            return to.normalized;
        }

        // Called by the interstellar planner UI to plot a course before engage.
        public void PlotCourse(Orbit dest, Vector3d arrivalVel)
        {
            destinationOrbit = dest;
            arrivalVelBary   = arrivalVel;
        }

        static void ScreenMsg(string m) =>
            ScreenMessages.PostScreenMessage(m, 4f, ScreenMessageStyle.UPPER_CENTER);
    }
}
