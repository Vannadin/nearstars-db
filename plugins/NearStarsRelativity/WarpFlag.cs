// 워프/점프 중 여부를 알려주는 공유 플래그 — 워프 플러그인이 Provider를 채운다. 없으면 항상 false
namespace NearStars.Relativity
{
    // §2.6(ii): the relativity layer must treat a warping/jumping vessel as identity
    // (warp speed is not physical β). The warp plugin owns the truth; it registers a
    // Provider here. Until it does, every vessel reads "not warping" (safe default —
    // relativity simply stays on, which is correct whenever no warp is engaged).
    //
    // VERIFY: decide the concrete channel with the warp plugin — a shared static set
    // each frame, or a per-vessel VesselModule flag queried here. Both plugins are
    // Schultz's lane, so one agreed flag suffices.
    public static class WarpFlag
    {
        public static System.Func<Vessel, bool> Provider;

        public static bool IsWarpingOrJumping(Vessel vessel)
            => Provider != null && vessel != null && Provider(vessel);
    }
}
