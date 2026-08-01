// Blueshift·KSPIE의 워프 가동 상태를 감지해 Principia 릴리스 채널(warpEngaged)을 대신 주장하는 마이크로 브리지
using System;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;

namespace PrincipiaWarpBridge {

// Difficulty-settings page for the bridge (stock dialog: new game or
// in-game Settings → Difficulty Options).
public class WarpBridgeSettings : GameParameters.CustomParameterNode {
  [GameParameters.CustomParameterUI(
      "Blueshift: preserve inertial velocity on cruise exit",
      toolTip = "Blueshift's rails-timewarp cruise ends co-moving with the " +
                "current main body (its stock behaviour).  With this on, " +
                "the ship's pre-cruise inertial velocity is restored " +
                "instead — a realistic arrival that must be braked off.",
      autoPersistance = true)]
  public bool preserveInertialVelocity = false;

  public override string Title => "Warp bridge";
  public override string Section => "PrincipiaWarpBridge";
  public override string DisplaySection => "Principia Warp Bridge";
  public override int SectionOrder => 1;
  public override GameParameters.GameMode GameMode =>
      GameParameters.GameMode.ANY;
  public override bool HasPresets => false;
}

// Detects an engaged warp drive from Blueshift (WBIWarpEngine) or KSP
// Interstellar Extended (AlcubierreDrive) on any loaded vessel and asserts
// the Principia fork's warp release channel (PrincipiaWarpStatus.warpEngaged)
// on that vessel's behalf every FixedUpdate while the cruise lasts.  The
// channel is a dead man's switch on the Principia side (~10 s grace), so a
// bridge failure merely lets the vessel be re-adopted; nothing gets stranded.
// All three mods are reached by reflection only: an absent mod disables its
// detector, and an absent Principia fork leaves the bridge inert.
[KSPAddon(KSPAddon.Startup.Flight, false)]
public sealed class WarpBridge : MonoBehaviour {
  private void Start() {
    if (!initialized_) {
      initialized_ = true;
      ResolveTypes();
    }
  }

  private void FixedUpdate() {
    if (warp_engaged_ == null ||
        (blueshift_engine_type_ == null && kspie_drive_type_ == null) ||
        !FlightGlobals.ready) {
      return;
    }
    bool preserve_velocity = blueshift_engine_type_ != null &&
                             PreserveInertialVelocityEnabled();
    List<Vessel> vessels = FlightGlobals.VesselsLoaded;
    for (int i = 0; i < vessels.Count; ++i) {
      Vessel vessel = vessels[i];
      if (vessel == null || vessel.parts == null) {
        continue;
      }
      try {
        ScanVessel(vessel,
                   out bool engaged,
                   out bool cruise_locked,
                   out bool has_blueshift_drive);
        bool needs_state = engaged || cruise_locked ||
                           (preserve_velocity && has_blueshift_drive);
        if (!states_.TryGetValue(vessel.id, out VesselState state)) {
          if (!needs_state) {
            continue;
          }
          state = new VesselState();
          states_[vessel.id] = state;
        }

        // Cruise-exit velocity bookkeeping (Blueshift's timewarp cruise
        // rebases the ship to co-move with its main body; when the
        // difficulty option asks for it, restore the pre-cruise inertial
        // velocity instead).  The candidate is sampled every unlocked frame,
        // frozen at lock start (pre-injection either way, since the lock
        // flag and the injection are set in the same synchronous call), and
        // replayed as an absolute target right after the unlock.
        if (preserve_velocity && has_blueshift_drive) {
          if (cruise_locked && !state.cruise_locked && state.has_candidate) {
            state.frozen_velocity = state.candidate_velocity;
            state.has_frozen = true;
            Debug.Log("[PrincipiaWarpBridge] Timewarp cruise on " +
                      vessel.vesselName +
                      "; captured pre-cruise inertial velocity");
          } else if (!cruise_locked && state.cruise_locked &&
                     state.has_frozen && state.asserting) {
            RestoreInertialVelocity(vessel, state.frozen_velocity);
            state.has_frozen = false;
          }
          if (!cruise_locked) {
            state.candidate_velocity = vessel.orbit.GetFrameVel();
            state.has_candidate = true;
          }
        }
        state.cruise_locked = cruise_locked;

        bool warping = engaged && AssertReleaseFlag(vessel);
        if (warping) {
          if (!state.asserting) {
            Debug.Log("[PrincipiaWarpBridge] Warp engaged on " +
                      vessel.vesselName +
                      "; asserting the Principia release flag");
          }
          state.asserting = true;
          state.disengaged_frames = 0;
        } else if (state.asserting) {
          // Clear our own assertion once the drive has stayed disengaged
          // past a one-frame guard, so re-adoption is near-immediate instead
          // of waiting out the dead-man grace; the guard absorbs a
          // single-frame flameout or throttle flicker mid-cruise, and a
          // wrongly cleared cruise costs one bounded adopt/release cycle,
          // never corruption.  A mod asserting the channel directly
          // re-raises the flag the next frame.
          if (++state.disengaged_frames >= clear_after_disengaged_frames) {
            SetReleaseFlag(vessel, false);
            state.asserting = false;
            Debug.Log("[PrincipiaWarpBridge] Warp ended on " +
                      vessel.vesselName +
                      "; clearing the release flag for prompt re-adoption");
          }
        }
      } catch (Exception e) {
        if (!error_logged_) {
          error_logged_ = true;
          Debug.LogWarning(
              "[PrincipiaWarpBridge] Detection error (logged once): " + e);
        }
      }
    }
  }

  private static void ScanVessel(Vessel vessel,
                                 out bool engaged,
                                 out bool cruise_locked,
                                 out bool has_blueshift_drive) {
    engaged = false;
    cruise_locked = false;
    has_blueshift_drive = false;
    List<Part> parts = vessel.parts;
    for (int p = 0; p < parts.Count; ++p) {
      PartModuleList modules = parts[p].Modules;
      int module_count = modules.Count;
      for (int m = 0; m < module_count; ++m) {
        PartModule module = modules[m];
        if (module == null) {
          continue;
        }
        Type type = module.GetType();
        if (blueshift_engine_type_ != null &&
            blueshift_engine_type_.IsAssignableFrom(type)) {
          has_blueshift_drive = true;
          if (module is ModuleEngines engine && engine.EngineIgnited &&
              (bool)blueshift_locked_cruise_.GetValue(module)) {
            cruise_locked = true;
            engaged = true;
          } else if (BlueshiftEngineIsWarping(module)) {
            engaged = true;
          }
        } else if (kspie_drive_type_ != null &&
                   kspie_drive_type_.IsAssignableFrom(type) &&
                   (bool)kspie_is_enabled_.GetValue(module)) {
          engaged = true;
        }
      }
    }
  }

  // Mirrors the preconditions under which WBIWarpEngine applies its warp
  // translation: ignited, throttled up, elected as the vessel's translating
  // engine, in space, above the minimum warp altitude, and holding warp
  // capacity.  The election gate (applyWarpTranslation) matters on
  // multi-engine ships: support engines skip the update that refreshes the
  // three precondition flags, so their stale values must never be trusted;
  // the elected engine refreshes all of them every frame.
  private static bool BlueshiftEngineIsWarping(PartModule module) {
    var engine = module as ModuleEngines;
    if (engine == null || !engine.EngineIgnited) {
      return false;
    }
    // Under rails timewarp Blueshift cruises by INJECTING the warp velocity
    // into the stock orbit (addWarpCruiseVelocity), flagged by
    // lockedCourseAndSpeed, and subtracts it back when the cruise ends.
    // While that flag is up the stock orbit is not a valid re-adoption
    // state — a vessel re-adopted then would keep warpSpeed × c forever —
    // so it counts as warping regardless of throttle or flameout.  The
    // ignition gate above matters: a shut-down engine never runs the
    // cancel path, so its flag can be stale forever and must be ignored.
    if ((bool)blueshift_locked_cruise_.GetValue(module)) {
      return true;
    }
    if (engine.flameout || engine.requestedThrottle <= 0f) {
      return false;
    }
    return (bool)blueshift_apply_translation_.GetValue(module) &&
           (bool)blueshift_is_in_space_.GetValue(module) &&
           (bool)blueshift_meets_warp_altitude_.GetValue(module) &&
           (bool)blueshift_has_warp_capacity_.GetValue(module);
  }

  // Rewrites the stock orbit so the vessel's total inertial velocity equals
  // the pre-cruise capture, mirroring the GoOnRails/UpdateFromStateVectors
  // pattern Blueshift itself uses.  Runs while the vessel is still released,
  // so Principia adopts the corrected orbit.  The target is absolute, which
  // makes the correction independent of whatever the cruise arithmetic left
  // in the orbit.
  private static void RestoreInertialVelocity(Vessel vessel,
                                              Vector3d target_velocity) {
    Orbit orbit = vessel.orbit;
    Vector3d delta = target_velocity - orbit.GetFrameVel();
    if (delta.sqrMagnitude < 1e-6) {
      return;
    }
    vessel.IgnoreGForces(2);
    bool was_packed = vessel.packed;
    try {
      if (!was_packed) {
        vessel.GoOnRails();
      }
      orbit.UpdateFromStateVectors(orbit.pos,
                                   orbit.vel + delta,
                                   orbit.referenceBody,
                                   Planetarium.GetUniversalTime());
    } finally {
      if (!was_packed) {
        vessel.GoOffRails();
      }
    }
    Debug.Log("[PrincipiaWarpBridge] Restored pre-cruise inertial velocity " +
              "on " + vessel.vesselName + " (difficulty option); Δv " +
              delta.magnitude.ToString("F1") + " m/s");
  }

  private static bool PreserveInertialVelocityEnabled() {
    Game game = HighLogic.CurrentGame;
    if (game == null) {
      return false;
    }
    WarpBridgeSettings settings =
        game.Parameters.CustomParams<WarpBridgeSettings>();
    return settings != null && settings.preserveInertialVelocity;
  }

  private static bool AssertReleaseFlag(Vessel vessel) {
    return SetReleaseFlag(vessel, true);
  }

  private static bool SetReleaseFlag(Vessel vessel, bool engaged) {
    List<VesselModule> modules = vessel.vesselModules;
    if (modules == null) {
      return false;
    }
    for (int i = 0; i < modules.Count; ++i) {
      VesselModule vessel_module = modules[i];
      if (vessel_module != null &&
          warp_status_type_.IsInstanceOfType(vessel_module)) {
        warp_engaged_.SetValue(vessel_module, engaged, null);
        return true;
      }
    }
    return false;
  }

  private static void ResolveTypes() {
    foreach (AssemblyLoader.LoadedAssembly loaded in
             AssemblyLoader.loadedAssemblies) {
      Assembly assembly = loaded.assembly;
      if (assembly == null) {
        continue;
      }
      try {
        if (warp_engaged_ == null) {
          Type type = assembly.GetType(
              "principia.ksp_plugin_adapter.PrincipiaWarpStatus");
          if (type != null && typeof(VesselModule).IsAssignableFrom(type)) {
            PropertyInfo engaged = type.GetProperty(
                "warpEngaged",
                BindingFlags.Instance | BindingFlags.Public);
            if (engaged != null && engaged.PropertyType == typeof(bool) &&
                engaged.CanWrite) {
              warp_status_type_ = type;
              warp_engaged_ = engaged;
            }
          }
        }
        if (blueshift_engine_type_ == null) {
          Type type = assembly.GetType("Blueshift.WBIWarpEngine");
          if (type != null && typeof(ModuleEngines).IsAssignableFrom(type)) {
            FieldInfo in_space = BoolField(type, "isInSpace");
            FieldInfo altitude = BoolField(type, "meetsWarpAltitude");
            FieldInfo capacity = BoolField(type, "hasWarpCapacity");
            FieldInfo translating = BoolField(type, "applyWarpTranslation");
            FieldInfo locked = BoolField(type, "lockedCourseAndSpeed");
            if (in_space != null && altitude != null && capacity != null &&
                translating != null && locked != null) {
              blueshift_engine_type_ = type;
              blueshift_is_in_space_ = in_space;
              blueshift_meets_warp_altitude_ = altitude;
              blueshift_has_warp_capacity_ = capacity;
              blueshift_apply_translation_ = translating;
              blueshift_locked_cruise_ = locked;
            }
          }
        }
        if (kspie_drive_type_ == null) {
          Type type = assembly.GetType("FNPlugin.Propulsion.AlcubierreDrive");
          if (type != null && typeof(PartModule).IsAssignableFrom(type)) {
            FieldInfo enabled = BoolField(type, "IsEnabled");
            if (enabled != null) {
              kspie_drive_type_ = type;
              kspie_is_enabled_ = enabled;
            }
          }
        }
      } catch (Exception e) {
        Debug.LogWarning("[PrincipiaWarpBridge] Type resolution error in " +
                         loaded.name + ": " + e.Message);
      }
    }
    Debug.Log(string.Format(
        "[PrincipiaWarpBridge] Principia release channel {0}; " +
        "Blueshift {1}; KSP Interstellar Extended {2}",
        warp_engaged_ != null ? "found" : "ABSENT — bridge inert",
        blueshift_engine_type_ != null ? "detected" : "absent",
        kspie_drive_type_ != null ? "detected" : "absent"));
  }

  // NonPublic is included for Blueshift's protected applyWarpTranslation.
  private static FieldInfo BoolField(Type type, string name) {
    FieldInfo field = type.GetField(
        name,
        BindingFlags.Instance | BindingFlags.Public |
        BindingFlags.NonPublic);
    return field != null && field.FieldType == typeof(bool) ? field : null;
  }

  private sealed class VesselState {
    public bool asserting;          // Release flag raised and not yet cleared.
    public int disengaged_frames;   // Consecutive frames without a live drive.
    public bool cruise_locked;      // Blueshift timewarp cruise in progress.
    public bool has_candidate;      // candidate_velocity is valid.
    public bool has_frozen;         // frozen_velocity is valid.
    public Vector3d candidate_velocity;  // Latest unlocked inertial velocity.
    public Vector3d frozen_velocity;     // Pre-cruise inertial velocity.
  }

  private static bool initialized_ = false;
  private static Type warp_status_type_;
  private static PropertyInfo warp_engaged_;
  private static Type blueshift_engine_type_;
  private static FieldInfo blueshift_is_in_space_;
  private static FieldInfo blueshift_meets_warp_altitude_;
  private static FieldInfo blueshift_has_warp_capacity_;
  private static FieldInfo blueshift_apply_translation_;
  private static FieldInfo blueshift_locked_cruise_;
  private static Type kspie_drive_type_;
  private static FieldInfo kspie_is_enabled_;

  // Consecutive disengaged physics frames before the bridge clears the flag
  // instead of letting the ~10 s dead-man grace run out; 2 keeps a
  // one-frame flicker guard while making re-adoption near-immediate.
  private const int clear_after_disengaged_frames = 2;

  private readonly Dictionary<Guid, VesselState> states_ =
      new Dictionary<Guid, VesselState>();
  private bool error_logged_ = false;
}

}  // namespace PrincipiaWarpBridge
