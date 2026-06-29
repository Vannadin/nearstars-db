// 엔진 추력을 Principia stage-7 이전에 part-force 채널에서 ×1/γ³로 보정하는 힘 훅 (API 접촉부 VERIFY)
using UnityEngine;

namespace NearStars.Relativity
{
    // Applies the relativistic thrust suppression as a CORRECTIVE force, so propellant
    // keeps burning at its nominal coordinate-time rate. We deliberately do NOT patch
    // engine thrust (that would also cut fuel — relativity-mod.md §2.2/§3).
    //
    // Net integrated force must become F_engine / γ³. We add  −(1 − 1/γ³)·F_engine
    // into part.force, which Principia reads at TimingManager stage FashionablyLate (7)
    // and the stock FlightIntegrator reads too — so this works on BOTH profiles.
    //
    // TIMING (the one thing to VERIFY at the keyboard): the correction must land after
    // engines compute thrust and BEFORE stage 7. Two strategies:
    //   (A) TimingManager.FixedUpdateAdd at a stage < FashionablyLate  — implemented here.
    //   (B) a Harmony postfix on the engine thrust step that calls ApplyCorrection —
    //       more robust ordering; PREFERRED. ApplyCorrection is static for that use.
    [KSPAddon(KSPAddon.Startup.Flight, false)]
    public class ThrustCorrector : MonoBehaviour
    {
        // VERIFY: confirm this stage runs after engine thrust deposit and before
        // Principia's FashionablyLate(7). If Normal is too early, move earlier-than-7
        // or switch to strategy (B).
        const TimingManager.TimingStage Stage = TimingManager.TimingStage.Normal;

        void Start()    => TimingManager.FixedUpdateAdd(Stage, OnTick);
        void OnDestroy() => TimingManager.FixedUpdateRemove(Stage, OnTick);

        void OnTick()
        {
            // MVP: the loaded/active vessel. VERIFY/TODO: unloaded vessels thrusting in
            // Principia background are not corrected here (acceptable for a first cut).
            ApplyCorrection(FlightGlobals.ActiveVessel);
        }

        // Public + static so a Harmony postfix (strategy B) can drive it per vessel.
        public static void ApplyCorrection(Vessel vessel)
        {
            if (vessel == null || !vessel.loaded) return;

            RelativityState.State st =
                RelativityState.Evaluate(vessel, WarpFlag.IsWarpingOrJumping(vessel));
            if (!st.Active) return;                       // all §2.6 guards handled inside

            float drop = (float)(1.0 - RelativityState.ThrustFactor(st.Gamma));  // 1 − 1/γ³
            if (drop <= 0f) return;

            foreach (Part part in vessel.parts)
            {
                Vector3 thrust = EngineThrustVector(part);   // kN, this part's engines
                if (thrust == Vector3.zero) continue;
                // NOTE: applies γ³ to the full thrust vector (longitudinal model, §2.1).
                //   Off-axis refinement (γ³ along v, γ across) is a minor later tweak.
                // VERIFY: Part.AddForce expects kN and is the channel Principia samples.
                part.AddForce(-drop * thrust);
            }
        }

        // Sum the thrust this part's engine module(s) produce this frame.
        // VERIFY: ModuleEngines.finalThrust (kN); thrust direction = −thrustTransform.forward.
        static Vector3 EngineThrustVector(Part part)
        {
            Vector3 total = Vector3.zero;
            for (int i = 0; i < part.Modules.Count; i++)
            {
                var eng = part.Modules[i] as ModuleEngines;
                if (eng == null || !eng.isOperational || eng.finalThrust <= 0f) continue;

                Vector3 dir = Vector3.zero;
                for (int t = 0; t < eng.thrustTransforms.Count; t++)
                    dir += -eng.thrustTransforms[t].forward;
                if (eng.thrustTransforms.Count > 0)
                    total += dir.normalized * eng.finalThrust;   // kN
            }
            return total;
        }
    }
}
