# RP-1 integration — checklist

## Research (grounding) — done
- [x] RSS identity, MM tags, root body name, scale
- [x] Principia config location + epoch + patch pattern
- [x] RP-1 tech tree node names + reseat target (`scienceSatellite`)
- [x] RP-1 contract coexistence rule (ship RB contracts `:NEEDS[!RP-0]`)
- [x] RealAntennas interstellar behaviour (fails safe to rate 0)
- [x] ROKerbalism profile tag (`ProfileRealismOverhaul`) + radiation node schema
- [x] Verdict: RP-1 ⊥ Sol-Configs officially; Sol-Configs side building RP-1 compat (owner)

## Strategy — confirmed (2026-06-26)
- [x] Stay Sol-based; ride on upstream Sol-Configs RP-1 compat
- [x] Drop classic-RSS Kopernicus variant + RSS Principia coordinate variant
- [x] NearStars owns only base-independent career layers (gate on RP-0 / RO / profile / Principia)

## Design capture (no emit yet)
- [x] Write `plan.md` (revised to Sol-based strategy)
- [ ] Rewrite `researchbodies-cfg/references/rp1-compat.md`
      (reseat → `scienceSatellite`; contracts → `:NEEDS[!RP-0]`; no observatory mechanic)
- [ ] Spec ROKerbalism RadiationBody output mode for the kerbalism-cfg writer
- [ ] Document RealAntennas interstellar limitation

## Gated on upstream / project-end
- [ ] In-game validation once Sol-Configs RP-1 compat lands
- [ ] Principia stability for real-distance stars (REBOUND cross-check)
- [ ] Emit pass (project end): career-layer cfgs gated on RP-0 / ProfileRealismOverhaul
