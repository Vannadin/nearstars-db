// 우주선의 바리센터 속도로 β/γ를 구하고 §2.6 가드(활성화/워프/크라켄)를 적용하는 순수 로직 코어
using System;
using UnityEngine;

namespace NearStars.Relativity
{
    // Central β/γ provider + the three §2.6 guards. The arithmetic is pure and
    // verifiable without a KSP runtime; the only engine touchpoints (velocity, SOI)
    // live in BarycentricSpeed and are marked VERIFY. Spec: relativity-mod.md.
    public static class RelativityState
    {
        public const double C        = 299792458.0;  // m/s
        public const double BetaMin  = 0.01;          // §2.6(i) below this ⇒ identity (~3000 km/s). Tunable.
        public const double BetaSane = 0.995;         // §2.6(iii) above this ⇒ treat as glitch ⇒ identity.

        // --- pure functions (no KSP) ---

        // Lorentz factor. Caller must pass a validated 0 <= beta < 1 (Evaluate does this).
        public static double Gamma(double beta) => 1.0 / Math.Sqrt(1.0 - beta * beta);

        // Longitudinal thrust multiplier (effective / nominal) = 1/γ³. §2.1.
        public static double ThrustFactor(double gamma) => 1.0 / (gamma * gamma * gamma);

        // Proper-time resource-rate multiplier = 1/γ. §2.2.
        public static double ResourceFactor(double gamma) => 1.0 / gamma;

        static bool IsFinite(double x) => !(double.IsNaN(x) || double.IsInfinity(x));

        // --- per-frame evaluation ---

        public struct State
        {
            public bool   Active;  // false ⇒ this frame is identity (no correction, no scaling)
            public double Beta;
            public double Gamma;
        }

        // Evaluate one vessel, applying all three §2.6 guards in order. Returns an
        // inactive (identity) state when warping, glitched, or below threshold.
        public static State Evaluate(Vessel vessel, bool underWarpOrJump)
        {
            var s = new State { Active = false, Beta = 0.0, Gamma = 1.0 };

            // (ii) Warp/jump exemption — warp speed is not physical speed-through-space.
            if (underWarpOrJump) return s;

            double beta = BarycentricSpeed(vessel) / C;

            // (iii) Kraken fail-safe — NaN / superluminal ⇒ identity. Do not try to fix it.
            if (!IsFinite(beta) || beta >= BetaSane) return s;

            // (i) Activation gate — insignificant speed ⇒ no-op.
            if (beta <= BetaMin) return s;

            s.Active = true;
            s.Beta   = beta;
            s.Gamma  = Gamma(beta);
            return s;
        }

        // Barycentric speed (m/s). KSP's root body (Sun) is the fixed inertial origin,
        // so "barycentric" == Sun-fixed inertial.
        // VERIFY: in the activation regime the vessel is on solar escape (SOI == Sun),
        //   so obt_velocity is already Sun-relative = barycentric. The chain fallback
        //   (inside a planet SOI, where β is negligible anyway) sums Orbit.GetFrameVel()
        //   up the parent chain. Confirm GetFrameVel() / obt_velocity units are m/s.
        // VERIFY (Principia profile): if Principia is present, prefer its barycentric
        //   velocity (read-only External) over this KSP-derived value, and wire it here.
        static double BarycentricSpeed(Vessel vessel)
        {
            if (vessel == null || vessel.orbit == null) return 0.0;

            // SOI == Sun  ⇔  the reference body has no parent.
            CelestialBody soi = vessel.orbit.referenceBody;
            if (soi != null && soi.orbit == null)
                return vessel.obt_velocity.magnitude;

            // Fallback: sum frame velocities up the parent chain (fixed inertial frame).
            Vector3d vel = vessel.orbit.GetFrameVel();
            Orbit o = soi != null ? soi.orbit : null;
            while (o != null)
            {
                vel += o.GetFrameVel();
                o = o.referenceBody != null ? o.referenceBody.orbit : null;
            }
            return vel.magnitude;
        }
    }
}
