// 워프 크루즈 상태머신(engage→cruise→dropout)과 v0 캐리·FTL 전진을 담는 순수 로직 코어
using System;
using UnityEngine;

namespace NearStars.Warp
{
    // The correctness core. Engage/cruise/dropout state machine + velocity-continuity
    // (frame (a): barycentric preserve) + the FTL continuous step. Pure: no KSP calls
    // here — the PartModule feeds it dt, heading, captured v0, and reads back a delta.
    // Spec: gameplay/interstellar-expansion/warp-patch-draft.md §2.
    public static class WarpCruise
    {
        public const double C = 299792458.0; // m/s

        public enum Phase { Idle, Spooling, Cruising, Dropout }

        // Per-vessel cruise state. The PartModule owns one of these.
        public class State
        {
            public Phase  Phase   = Phase.Idle;
            public double WarpBeta;          // target cruise speed, multiples of c (β_s, may be > 1 — FTL)
            public Vector3d V0;              // captured barycentric velocity at engage (m/s) — carried unchanged
            public Vector3d Heading;         // unit travel direction (barycentric)
            public double SpoolT;            // seconds spent in current ramp
            public const double SpoolDur = 3.0; // ramp length (s) — continuity, no teleport pop. Tunable.
        }

        // β_s ramps 0→target over SpoolDur (and target→0 on dropout) so speed is continuous.
        public static double RampFactor(double spoolT)
        {
            double x = Clamp01(spoolT / State.SpoolDur);
            return x * x * (3.0 - 2.0 * x); // smoothstep
        }

        // The continuous, steerable FTL step for one FixedUpdate. Returns the position
        // delta (m) to apply to the detached vessel this frame. Carries v0 unchanged
        // (frame (a)) and adds the warp velocity along the current heading.
        //   Δx = (v0 + heading · β_s·c·ramp) · dt
        // Coasting / non-cruising phases contribute only the carried v0 (or nothing when Idle).
        public static Vector3d StepDelta(State s, double dt)
        {
            switch (s.Phase)
            {
                case Phase.Idle:
                    return Vector3d.zero;

                case Phase.Spooling:
                {
                    s.SpoolT += dt;
                    double warpV = s.WarpBeta * C * RampFactor(s.SpoolT);
                    Vector3d v = s.V0 + s.Heading * warpV;
                    if (s.SpoolT >= State.SpoolDur) s.Phase = Phase.Cruising;
                    return v * dt;
                }

                case Phase.Cruising:
                {
                    double warpV = s.WarpBeta * C;
                    return (s.V0 + s.Heading * warpV) * dt;
                }

                case Phase.Dropout:
                {
                    s.SpoolT += dt;
                    double warpV = s.WarpBeta * C * (1.0 - RampFactor(s.SpoolT));
                    Vector3d v = s.V0 + s.Heading * warpV;
                    if (s.SpoolT >= State.SpoolDur) s.Phase = Phase.Idle; // PartModule then re-seeds the stock orbit
                    return v * dt;
                }
            }
            return Vector3d.zero;
        }

        // Transitions. Engage captures v0 (barycentric) + heading; dropout ramps speed back down.
        public static void Engage(State s, double warpBeta, Vector3d v0Barycentric, Vector3d heading)
        {
            s.Phase    = Phase.Spooling;
            s.WarpBeta = warpBeta;
            s.V0       = v0Barycentric;
            s.Heading  = heading.normalized;
            s.SpoolT   = 0.0;
        }

        public static void BeginDropout(State s)
        {
            if (s.Phase == Phase.Cruising || s.Phase == Phase.Spooling)
            {
                s.Phase  = Phase.Dropout;
                s.SpoolT = 0.0;
            }
        }

        // The relativity layer (§2.6(ii)) reads this: any non-Idle phase is "under warp",
        // so its β/γ mechanic stays identity (warp speed is not physical speed-through-space).
        public static bool IsUnderWarp(State s) => s != null && s.Phase != Phase.Idle;

        static double Clamp01(double x) => x < 0.0 ? 0.0 : (x > 1.0 ? 1.0 : x);
    }
}
