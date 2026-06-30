// β/γ·유효추력·자원 소비배율을 보여주는 IMGUI 계기판 (Flight 씬, 메커닉이 켜졌을 때만 표시)
using UnityEngine;

namespace NearStars.Relativity
{
    // The split readout IS the mechanic's identity (relativity-mod.md §1): the player
    // sees nominal vs effective thrust diverge as β climbs. Shown only while the layer
    // is active (β > β_min, not warping/glitched), so it stays invisible in normal play.
    //
    // FULL UX SPEC: gameplay/interstellar-expansion/relativity/relativity-ux.md — this
    // stub draws the minimal β/γ/thrust/supply readout; the spec's §6 extends it with
    // the two-mode (Simple/Expert) layout, the light-wall speed gauge, the two-clock
    // (UT vs crew ∫dt/γ) counter, the brake-authority cue, and the collapsed WARP panel
    // (speed in c-multiples, read from the warp plugin) when WarpFlag is up.
    [KSPAddon(KSPAddon.Startup.Flight, false)]
    public class RelativityDashboard : MonoBehaviour
    {
        Rect window = new Rect(60f, 60f, 250f, 0f);
        RelativityState.State st;

        // Evaluate once per frame; OnGUI runs several times per frame so don't compute there.
        void Update()
        {
            Vessel v = FlightGlobals.ActiveVessel;
            st = v != null
                ? RelativityState.Evaluate(v, WarpFlag.IsWarpingOrJumping(v))
                : default(RelativityState.State);
        }

        void OnGUI()
        {
            if (!st.Active) return;   // hidden whenever the mechanic isn't doing anything
            // VERIFY: GUI id uniqueness; optionally gate behind an ApplicationLauncher button.
            window = GUILayout.Window(GetInstanceID(), window, DrawWindow, "Relativity");
        }

        void DrawWindow(int id)
        {
            double thrustPct = RelativityState.ThrustFactor(st.Gamma) * 100.0;  // 1/γ³
            double burnPct   = RelativityState.ResourceFactor(st.Gamma) * 100.0; // 1/γ

            GUILayout.BeginVertical();
            GUILayout.Label(string.Format("β = {0:F4} c", st.Beta));
            GUILayout.Label(string.Format("γ = {0:F3}", st.Gamma));
            GUILayout.Label(string.Format("thrust   {0:F1} %  (×1/γ³)", thrustPct));
            GUILayout.Label(string.Format("supplies {0:F1} %  rate (×1/γ)", burnPct));
            GUILayout.EndVertical();
            GUI.DragWindow();
        }
    }
}
